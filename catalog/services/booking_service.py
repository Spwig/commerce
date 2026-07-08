"""
Booking Availability & Management Service

Core service for the booking product type. Handles:
- Availability calculation (dates, slots, capacity)
- Price calculation (base + person types + resources + rules)
- Slot reservation (TTL pattern matching StockReservation)
- Booking creation, cancellation, waitlist processing
- iCal generation for calendar sync
"""
from datetime import datetime, timedelta, date, time, timezone as dt_timezone
from decimal import Decimal
from typing import Optional, Tuple, List, Dict
from collections import defaultdict
import uuid
import logging

from django.db import transaction
from django.db.models import Q, Sum
from django.utils import timezone

from catalog.models import (
    Product, BookingConfig, BookingResource, BookingPersonType,
    BookingAvailabilityRule, BookingRecurrenceRule,
    Booking, BookingWaitlist, BookingSlotReservation,
)

logger = logging.getLogger(__name__)

SLOT_RESERVATION_TTL = {
    'web': timedelta(minutes=30),
    'pos': timedelta(minutes=15),
}


class BookingAvailabilityService:
    """Service for checking booking availability and generating time slots."""

    @staticmethod
    def get_available_dates(
        product: Product,
        year: int,
        month: int,
        resource_id: Optional[int] = None,
    ) -> List[Dict]:
        """
        Get available dates for a booking product in a given month.

        Returns a list of date dicts with availability info:
        [{"date": "2026-03-15", "available": True, "slots_available": 5}, ...]
        """
        try:
            config = product.booking_config
        except BookingConfig.DoesNotExist:
            return []

        import calendar
        _, days_in_month = calendar.monthrange(year, month)

        results = []
        now = timezone.now()

        for day_num in range(1, days_in_month + 1):
            check_date = date(year, month, day_num)

            # Skip past dates
            if datetime.combine(check_date, time(23, 59), tzinfo=dt_timezone.utc) < now:
                results.append({
                    'date': check_date.isoformat(),
                    'available': False,
                    'reason': 'past',
                })
                continue

            # Check advance booking window
            if not BookingAvailabilityService._within_advance_window(config, check_date):
                results.append({
                    'date': check_date.isoformat(),
                    'available': False,
                    'reason': 'outside_window',
                })
                continue

            # Check availability rules
            is_available = BookingAvailabilityService._check_date_availability(
                product, config, check_date, resource_id
            )

            if is_available:
                # Count available slots
                slots = BookingAvailabilityService.get_available_slots(
                    product, check_date, resource_id
                )
                available_count = sum(1 for s in slots if s['available'])
                results.append({
                    'date': check_date.isoformat(),
                    'available': available_count > 0,
                    'slots_available': available_count,
                })
            else:
                results.append({
                    'date': check_date.isoformat(),
                    'available': False,
                    'reason': 'unavailable',
                })

        return results

    @staticmethod
    def get_available_slots(
        product: Product,
        booking_date: date,
        resource_id: Optional[int] = None,
    ) -> List[Dict]:
        """
        Get available time slots for a specific date.

        Returns list of time slot dicts:
        [{"start": "09:00", "end": "10:00", "available": True, "capacity_remaining": 3, "price": "50.00"}, ...]
        """
        try:
            config = product.booking_config
        except BookingConfig.DoesNotExist:
            return []

        # For accommodation (day/night units), return single all-day slot
        if config.booking_type == 'accommodation':
            return BookingAvailabilityService._get_accommodation_slots(
                product, config, booking_date, resource_id
            )

        # Generate time slots based on duration and available times
        slots = []
        available_times = BookingAvailabilityService._get_available_times(
            product, config, booking_date, resource_id
        )

        duration_minutes = BookingAvailabilityService._duration_to_minutes(
            config.duration, config.duration_unit
        )

        for start_time, end_time in available_times:
            current = datetime.combine(booking_date, start_time)
            slot_end_limit = datetime.combine(booking_date, end_time)

            while current + timedelta(minutes=duration_minutes) <= slot_end_limit:
                slot_start = current.time()
                slot_end = (current + timedelta(minutes=duration_minutes)).time()

                # Check capacity for this slot
                capacity = BookingAvailabilityService._check_slot_capacity(
                    product, config, booking_date,
                    slot_start, slot_end, resource_id
                )

                # Calculate price
                price = BookingAvailabilityService._calculate_slot_price(
                    product, config, booking_date, slot_start, slot_end, resource_id
                )

                slots.append({
                    'start': slot_start.strftime('%H:%M'),
                    'end': slot_end.strftime('%H:%M'),
                    'available': capacity > 0,
                    'capacity_remaining': capacity,
                    'price': str(price),
                })

                # Advance by duration + buffer
                buffer_minutes = config.buffer_before + config.buffer_after
                current += timedelta(minutes=duration_minutes + buffer_minutes)

        return slots

    @staticmethod
    def check_availability(
        product: Product,
        start_dt: datetime,
        end_dt: datetime,
        resource_id: Optional[int] = None,
        persons: Optional[Dict] = None,
        exclude_reservation_id: Optional[int] = None,
    ) -> Tuple[bool, str, Optional[Decimal]]:
        """
        Check if a specific time slot is available and calculate the price.

        Returns (is_available, message, total_price)
        """
        try:
            config = product.booking_config
        except BookingConfig.DoesNotExist:
            return False, 'Product is not configured for bookings', None

        booking_date = start_dt.date()

        # Check advance window
        if not BookingAvailabilityService._within_advance_window(config, booking_date):
            return False, 'Outside advance booking window', None

        # Accommodation: validate min/max stay and every night in the range
        if config.booking_type == 'accommodation':
            checkin = start_dt.date()
            checkout = end_dt.date()
            num_nights = (checkout - checkin).days
            if num_nights < 1:
                num_nights = 1

            # Enforce max_stay FIRST to prevent DoS from huge date ranges
            effective_max = config.max_stay if config.max_stay and config.max_stay > 0 else 365
            if num_nights > effective_max:
                return False, f'Maximum stay is {effective_max} night(s)', None

            # Sanitise person counts — reject negative values
            if persons:
                for ptype, count in persons.items():
                    if not isinstance(count, (int, float)) or count < 0:
                        return False, 'Invalid person count', None

            # Enforce max occupancy across all person types
            if persons and config.max_occupancy and config.max_occupancy > 0:
                total_guests = sum(int(c) for c in persons.values())
                if total_guests > config.max_occupancy:
                    return (
                        False,
                        f'Maximum occupancy is {config.max_occupancy} guest(s)',
                        None,
                    )

            # Determine effective minimum stay (config + rule overrides)
            effective_min = config.min_stay or 1
            override_rules = product.booking_availability_rules.filter(
                min_stay_override__isnull=False,
            )
            if resource_id:
                override_rules = override_rules.filter(
                    Q(resource_id=resource_id) | Q(resource__isnull=True)
                )
            else:
                override_rules = override_rules.filter(resource__isnull=True)
            for rule in override_rules:
                for day_offset in range(num_nights):
                    night_date = checkin + timedelta(days=day_offset)
                    if BookingAvailabilityService._rule_matches_date(rule, night_date):
                        effective_min = max(effective_min, rule.min_stay_override)

            if num_nights < effective_min:
                return False, f'Minimum stay is {effective_min} night(s)', None

            # Check date availability and capacity for every night
            for day_offset in range(num_nights):
                night_date = checkin + timedelta(days=day_offset)
                if not BookingAvailabilityService._check_date_availability(
                    product, config, night_date, resource_id
                ):
                    return False, f'{night_date.isoformat()} is not available', None

                capacity = BookingAvailabilityService._check_accommodation_capacity(
                    product, config, night_date, resource_id,
                    exclude_reservation_id=exclude_reservation_id,
                )
                if capacity <= 0:
                    return (
                        False,
                        f'{night_date.isoformat()} is fully booked',
                        None,
                    )
        else:
            # Non-accommodation: single date check
            if not BookingAvailabilityService._check_date_availability(
                product, config, booking_date, resource_id
            ):
                return False, 'Date is not available', None

            # Enforce max occupancy
            if persons and config.max_occupancy and config.max_occupancy > 0:
                total_guests = sum(int(c) for c in persons.values())
                if total_guests > config.max_occupancy:
                    return (
                        False,
                        f'Maximum occupancy is {config.max_occupancy} guest(s)',
                        None,
                    )

            # Check capacity
            capacity = BookingAvailabilityService._check_slot_capacity(
                product, config, booking_date,
                start_dt.time(), end_dt.time(), resource_id,
                exclude_reservation_id=exclude_reservation_id,
            )

            # Check person count against capacity
            if persons:
                total_persons = sum(
                    count for ptype, count in persons.items()
                    if BookingAvailabilityService._is_counted_for_capacity(product, ptype)
                )
                if total_persons > capacity:
                    return False, f'Only {capacity} spot(s) remaining', None

            if capacity <= 0:
                return False, 'Time slot is fully booked', None

        # Calculate price
        price = BookingAvailabilityService.calculate_booking_price(
            product, start_dt, end_dt, resource_id, persons
        )

        return True, 'Available', price

    @staticmethod
    def calculate_booking_price(
        product: Product,
        start_dt: datetime,
        end_dt: datetime,
        resource_id: Optional[int] = None,
        persons: Optional[Dict] = None,
    ) -> Decimal:
        """
        Calculate total price for a booking.

        For accommodation: delegates to per-night engine.
        For other types: base + resource + person_type + rule adjustments.
        """
        try:
            config = product.booking_config
        except BookingConfig.DoesNotExist:
            return Decimal('0')

        # Accommodation uses the per-night engine
        if config.booking_type == 'accommodation':
            result = BookingAvailabilityService.calculate_accommodation_price(
                product, start_dt.date(), end_dt.date(), resource_id, persons
            )
            return result['total']

        booking_date = start_dt.date()
        start_time = start_dt.time()
        end_time = end_dt.time()

        # Base price from product
        base_price = product.price.amount if product.price else Decimal('0')

        # Check for cost override/adjustment from availability rules
        rule_price = BookingAvailabilityService._get_rule_price_adjustment(
            product, booking_date, start_time, end_time, resource_id
        )
        if rule_price['override'] is not None:
            base_price = rule_price['override']
        elif rule_price['adjustment'] is not None:
            base_price += rule_price['adjustment']

        # For customer-selected duration, scale price by duration
        if config.duration_type == 'customer_selected':
            actual_minutes = (end_dt - start_dt).total_seconds() / 60
            base_minutes = BookingAvailabilityService._duration_to_minutes(
                config.duration, config.duration_unit
            )
            if base_minutes > 0:
                base_price = base_price * Decimal(str(actual_minutes / base_minutes))

        # Resource cost adjustment
        if resource_id:
            try:
                resource = BookingResource.objects.get(pk=resource_id, product=product)
                base_price += resource.base_cost_adjustment
            except BookingResource.DoesNotExist:
                pass

        # Person type adjustments
        total_price = base_price
        if persons:
            person_types = {
                pt.name: pt for pt in product.booking_person_types.all()
            }
            for ptype_name, count in persons.items():
                if ptype_name in person_types:
                    pt = person_types[ptype_name]
                    total_price += pt.cost_adjustment * count
        else:
            total_price = base_price

        return max(total_price, Decimal('0'))

    @staticmethod
    def calculate_booking_price_with_breakdown(
        product: Product,
        start_dt: datetime,
        end_dt: datetime,
        resource_id: Optional[int] = None,
        persons: Optional[Dict] = None,
    ) -> Tuple[Decimal, Dict]:
        """
        Calculate price and return full breakdown.

        Returns (total, breakdown_dict).
        """
        try:
            config = product.booking_config
        except BookingConfig.DoesNotExist:
            return Decimal('0'), {'total': Decimal('0')}

        if config.booking_type == 'accommodation':
            result = BookingAvailabilityService.calculate_accommodation_price(
                product, start_dt.date(), end_dt.date(), resource_id, persons
            )
            return result['total'], result

        total = BookingAvailabilityService.calculate_booking_price(
            product, start_dt, end_dt, resource_id, persons
        )
        return total, {'total': total, 'nightly_breakdown': None}

    @staticmethod
    def calculate_accommodation_price(
        product: Product,
        checkin_date: date,
        checkout_date: date,
        resource_id: Optional[int] = None,
        persons: Optional[Dict] = None,
    ) -> Dict:
        """
        Calculate per-night accommodation pricing with full breakdown.

        Iterates each night independently, applying base rate, rules,
        resource surcharge, and per-person charges.
        """
        config = product.booking_config
        base_rate = product.price.amount if product.price else Decimal('0')
        num_nights = (checkout_date - checkin_date).days
        if num_nights < 1:
            num_nights = 1

        # Cap to max_stay to prevent runaway iteration
        effective_max = config.max_stay if config.max_stay and config.max_stay > 0 else 365
        num_nights = min(num_nights, effective_max)

        # Sanitise person counts — clamp negatives to zero
        if persons:
            persons = {k: max(0, int(v)) for k, v in persons.items()
                       if isinstance(v, (int, float, str)) and str(v).lstrip('-').isdigit()}

        # Load resource
        resource = None
        resource_surcharge = Decimal('0')
        if resource_id:
            try:
                resource = BookingResource.objects.get(pk=resource_id, product=product)
                resource_surcharge = resource.base_cost_adjustment
            except BookingResource.DoesNotExist:
                pass

        # Load person types
        person_type_objs = {
            pt.name: pt for pt in product.booking_person_types.all()
        }

        # Load custom_cost rules (sorted by priority ascending — higher overwrites)
        cost_rules = list(
            product.booking_availability_rules.filter(
                rule_type='custom_cost',
            ).order_by('priority')
        )
        if resource_id:
            cost_rules = [
                r for r in cost_rules
                if r.resource_id is None or r.resource_id == resource_id
            ]
        else:
            cost_rules = [r for r in cost_rules if r.resource_id is None]

        # Separate length-of-stay discount rules from nightly rules
        los_rules = [r for r in cost_rules if r.length_of_stay_min is not None]
        nightly_rules = [r for r in cost_rules if r.length_of_stay_min is None]

        # Calculate days until check-in (for lead-time rules)
        today = timezone.now().date()
        days_until_checkin = (checkin_date - today).days

        # Per-night iteration
        nightly_breakdown = []
        nightly_total_sum = Decimal('0')

        for day_offset in range(num_nights):
            night_date = checkin_date + timedelta(days=day_offset)
            nightly_rate = base_rate
            applied_rule_name = None

            # Apply nightly pricing rules
            for rule in nightly_rules:
                if not BookingAvailabilityService._rule_matches_date(rule, night_date):
                    continue

                # Check lead-time constraints
                if rule.lead_time_min_days is not None and days_until_checkin < rule.lead_time_min_days:
                    continue
                if rule.lead_time_max_days is not None and days_until_checkin > rule.lead_time_max_days:
                    continue

                # Apply override or adjustment (last matching wins)
                if rule.cost_override is not None:
                    nightly_rate = rule.cost_override
                    applied_rule_name = str(rule)
                if rule.cost_adjustment is not None:
                    if rule.cost_adjustment_type == 'percentage':
                        nightly_rate += nightly_rate * (rule.cost_adjustment / Decimal('100'))
                    else:
                        nightly_rate += rule.cost_adjustment
                    applied_rule_name = applied_rule_name or str(rule)

            # Resource surcharge (per-night)
            night_resource = Decimal('0')
            if resource and resource.is_per_night:
                night_resource = resource_surcharge

            # Person charges (per-night)
            night_person_charges = Decimal('0')
            if persons:
                for ptype_name, count in persons.items():
                    if ptype_name in person_type_objs:
                        pt = person_type_objs[ptype_name]
                        if pt.is_per_night and pt.cost_adjustment != 0:
                            night_person_charges += pt.cost_adjustment * count

            night_total = max(nightly_rate + night_resource + night_person_charges, Decimal('0'))
            nightly_total_sum += night_total

            nightly_breakdown.append({
                'date': night_date.isoformat(),
                'base_rate': str(nightly_rate),
                'resource_surcharge': str(night_resource),
                'person_charges': str(night_person_charges),
                'rule_name': applied_rule_name,
                'nightly_total': str(night_total),
            })

        subtotal = nightly_total_sum

        # Add one-time charges (non-per-night resource/person adjustments)
        one_time_charges = Decimal('0')
        if resource and not resource.is_per_night:
            one_time_charges += resource_surcharge
        if persons:
            for ptype_name, count in persons.items():
                if ptype_name in person_type_objs:
                    pt = person_type_objs[ptype_name]
                    if not pt.is_per_night and pt.cost_adjustment != 0:
                        one_time_charges += pt.cost_adjustment * count

        subtotal += one_time_charges

        # Length-of-stay discount
        los_discount = None
        for rule in sorted(los_rules, key=lambda r: r.priority):
            if rule.length_of_stay_min and num_nights >= rule.length_of_stay_min:
                if rule.length_of_stay_discount_percent:
                    discount_amount = subtotal * (rule.length_of_stay_discount_percent / Decimal('100'))
                    los_discount = {
                        'percent': str(rule.length_of_stay_discount_percent),
                        'amount': str(discount_amount),
                        'label': f"{rule.length_of_stay_min}+ nights: {rule.length_of_stay_discount_percent}% off",
                    }
                    subtotal -= discount_amount

        total = max(subtotal, Decimal('0'))

        return {
            'total': total,
            'num_nights': num_nights,
            'nightly_breakdown': nightly_breakdown,
            'subtotal_before_discount': str(nightly_total_sum + one_time_charges),
            'length_of_stay_discount': los_discount,
            'resource_name': resource.name if resource else None,
            'one_time_charges': str(one_time_charges) if one_time_charges else None,
        }

    # -------------------------------------------------------------------------
    # Slot Reservation (TTL pattern)
    # -------------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def create_slot_reservation(
        cart_item,
        product: Product,
        start_dt: datetime,
        end_dt: datetime,
        resource_id: Optional[int] = None,
        persons: Optional[Dict] = None,
        channel: str = 'web',
    ) -> Tuple[bool, str, Optional[BookingSlotReservation]]:
        """
        Create a temporary slot reservation tied to a cart item.

        Returns (success, message, reservation)
        """
        # Check availability first
        is_available, msg, price = BookingAvailabilityService.check_availability(
            product, start_dt, end_dt, resource_id, persons
        )

        if not is_available:
            return False, msg, None

        # Release any existing reservation for this cart item
        BookingSlotReservation.objects.filter(cart_item=cart_item).delete()

        resource = None
        if resource_id:
            resource = BookingResource.objects.filter(
                pk=resource_id, product=product
            ).first()

        ttl = SLOT_RESERVATION_TTL.get(channel, SLOT_RESERVATION_TTL['web'])
        expires_at = timezone.now() + ttl

        reservation = BookingSlotReservation.objects.create(
            product=product,
            resource=resource,
            cart_item=cart_item,
            start_datetime=start_dt,
            end_datetime=end_dt,
            persons=persons or {},
            expires_at=expires_at,
        )

        return True, 'Slot reserved', reservation

    @staticmethod
    def release_slot_reservation(cart_item) -> bool:
        """Release slot reservation for a cart item."""
        deleted, _ = BookingSlotReservation.objects.filter(cart_item=cart_item).delete()
        return deleted > 0

    @staticmethod
    def cleanup_expired_reservations() -> int:
        """Remove expired slot reservations. Called by Celery task."""
        now = timezone.now()
        deleted, _ = BookingSlotReservation.objects.filter(expires_at__lt=now).delete()
        if deleted:
            logger.info(f"Cleaned up {deleted} expired booking slot reservations")
        return deleted

    # -------------------------------------------------------------------------
    # Booking Creation & Management
    # -------------------------------------------------------------------------

    @staticmethod
    @transaction.atomic
    def confirm_booking(
        order_item,
        booking_data: Dict,
    ) -> Tuple[bool, str, Optional[Booking]]:
        """
        Create a confirmed booking from a completed order.

        Called during checkout when order is placed.
        """
        product = order_item.product

        try:
            config = product.booking_config
        except BookingConfig.DoesNotExist:
            return False, 'Product has no booking config', None

        start_dt = booking_data.get('start_datetime')
        end_dt = booking_data.get('end_datetime')
        resource_id = booking_data.get('resource_id')
        persons = booking_data.get('persons', {})

        resource = None
        if resource_id:
            resource = BookingResource.objects.filter(
                pk=resource_id, product=product
            ).first()

        # Determine initial status
        status = 'pending_confirmation' if config.confirmation_required else 'confirmed'

        # Calculate deposit if enabled
        total_cost = booking_data.get('total_cost', Decimal('0'))
        deposit_amount = Decimal('0')
        if config.deposit_enabled:
            if config.deposit_type == 'fixed':
                deposit_amount = min(config.deposit_amount, total_cost)
            elif config.deposit_type == 'percentage':
                deposit_amount = total_cost * (config.deposit_amount / Decimal('100'))

        # Sanitise price_breakdown for JSON storage (convert Decimals to strings)
        raw_breakdown = booking_data.get('price_breakdown', {})
        price_breakdown = {}
        if raw_breakdown:
            import json
            price_breakdown = json.loads(
                json.dumps(raw_breakdown, default=str)
            )

        booking = Booking.objects.create(
            product=product,
            resource=resource,
            order=order_item.order,
            order_item=order_item,
            customer=getattr(order_item.order, 'customer', None),
            start_datetime=start_dt,
            end_datetime=end_dt,
            status=status,
            persons=persons,
            total_cost=total_cost,
            deposit_amount=deposit_amount,
            price_breakdown=price_breakdown,
            customer_name=booking_data.get('customer_name', ''),
            customer_email=booking_data.get('customer_email', ''),
            customer_phone=booking_data.get('customer_phone', ''),
            customer_notes=booking_data.get('customer_notes', ''),
            customer_timezone=booking_data.get('customer_timezone', ''),
            ical_uid=f"booking-{uuid.uuid4()}@spwig",
        )

        # Remove slot reservation if exists
        BookingSlotReservation.objects.filter(
            product=product,
            start_datetime=start_dt,
            end_datetime=end_dt,
        ).delete()

        logger.info(f"Booking #{booking.pk} created for {product.name} ({status})")

        # Send lifecycle emails and create audit note
        template_type = (
            'booking_pending_confirmation' if config.confirmation_required
            else 'booking_confirmation'
        )
        BookingLifecycleService.send_booking_email(booking, template_type)
        BookingLifecycleService.send_admin_email(booking, 'admin_new_booking')
        BookingLifecycleService.add_note(
            booking, 'Booking created from order', note_type='system',
        )

        return True, f'Booking {status}', booking

    @staticmethod
    @transaction.atomic
    def cancel_booking(
        booking: Booking,
        reason: str = '',
    ) -> Tuple[bool, str]:
        """
        Cancel a booking and check waitlist.
        """
        if booking.status in ('cancelled', 'completed', 'no_show'):
            return False, f'Cannot cancel booking in {booking.status} status'

        if not booking.is_cancellable:
            return False, 'Cancellation deadline has passed'

        booking.status = 'cancelled'
        booking.cancellation_reason = reason
        booking.save(update_fields=['status', 'cancellation_reason', 'updated_at'])

        # Audit log and email
        BookingLifecycleService.add_note(
            booking, f'Booking cancelled: {reason}' if reason else 'Booking cancelled',
            note_type='status_change',
        )
        if booking.customer_email:
            BookingLifecycleService.send_booking_email(booking, 'booking_cancelled')

        # Process waitlist for this slot
        BookingAvailabilityService._process_waitlist(
            booking.product,
            booking.start_datetime.date(),
            booking.start_datetime.time(),
            booking.end_datetime.time(),
        )

        logger.info(f"Booking #{booking.pk} cancelled")
        return True, 'Booking cancelled'

    # -------------------------------------------------------------------------
    # Waitlist
    # -------------------------------------------------------------------------

    @staticmethod
    def join_waitlist(
        product: Product,
        customer_email: str,
        desired_date: date,
        customer_name: str = '',
        desired_time_start: Optional[time] = None,
        desired_time_end: Optional[time] = None,
        desired_persons: Optional[Dict] = None,
        customer=None,
    ) -> Tuple[bool, str, Optional[BookingWaitlist]]:
        """Add a customer to the waitlist for a booking product."""
        # Check for duplicate
        existing = BookingWaitlist.objects.filter(
            product=product,
            customer_email=customer_email,
            desired_date=desired_date,
            status='waiting',
        ).first()

        if existing:
            return False, 'Already on waitlist for this date', existing

        entry = BookingWaitlist.objects.create(
            product=product,
            customer=customer,
            customer_email=customer_email,
            customer_name=customer_name,
            desired_date=desired_date,
            desired_time_start=desired_time_start,
            desired_time_end=desired_time_end,
            desired_persons=desired_persons or {},
        )

        return True, 'Added to waitlist', entry

    @staticmethod
    def _process_waitlist(
        product: Product,
        booking_date: date,
        start_time: time,
        end_time: time,
    ):
        """Notify waitlisted customers when a slot opens up."""
        entries = BookingWaitlist.objects.filter(
            product=product,
            desired_date=booking_date,
            status='waiting',
        ).order_by('created_at')

        for entry in entries:
            # Check if desired time matches (if specified)
            if entry.desired_time_start and entry.desired_time_start != start_time:
                continue

            entry.status = 'notified'
            entry.notified_at = timezone.now()
            entry.save(update_fields=['status', 'notified_at'])

            # Send waitlist notification email
            try:
                from email_system.services.email_sender import EmailSendingService
                from email_system.utils.language import _get_site_default_language
                EmailSendingService.send_template_email(
                    to_email=entry.customer_email,
                    template_type='booking_waitlist_notification',
                    context={
                        'customer_name': entry.customer_name,
                        'product_name': product.name,
                        'available_date': entry.desired_date.strftime('%b %d, %Y'),
                    },
                    language=_get_site_default_language(),
                )
            except Exception as e:
                logger.error(f"Failed to send waitlist email: {e}")

            logger.info(f"Waitlist notification sent to {entry.customer_email}")
            break  # Notify one at a time

    # -------------------------------------------------------------------------
    # iCal Generation
    # -------------------------------------------------------------------------

    @staticmethod
    def generate_ical(booking: Booking) -> str:
        """Generate iCal event string for a booking."""
        now = timezone.now().strftime('%Y%m%dT%H%M%SZ')
        start = booking.start_datetime.strftime('%Y%m%dT%H%M%SZ')
        end = booking.end_datetime.strftime('%Y%m%dT%H%M%SZ')

        summary = f"Booking: {booking.product.name}"
        if booking.resource:
            summary += f" with {booking.resource.name}"

        description = f"Customer: {booking.customer_name or booking.customer_email}"
        if booking.customer_notes:
            description += f"\\nNotes: {booking.customer_notes}"

        uid = booking.ical_uid or f"booking-{booking.pk}@spwig"

        ical = (
            "BEGIN:VCALENDAR\r\n"
            "VERSION:2.0\r\n"
            "PRODID:-//Spwig//Booking//EN\r\n"
            "BEGIN:VEVENT\r\n"
            f"UID:{uid}\r\n"
            f"DTSTAMP:{now}\r\n"
            f"DTSTART:{start}\r\n"
            f"DTEND:{end}\r\n"
            f"SUMMARY:{summary}\r\n"
            f"DESCRIPTION:{description}\r\n"
            f"STATUS:{'CONFIRMED' if booking.status == 'confirmed' else 'TENTATIVE'}\r\n"
            "END:VEVENT\r\n"
            "END:VCALENDAR\r\n"
        )

        return ical

    # -------------------------------------------------------------------------
    # Resource Availability for Date Ranges (accommodation)
    # -------------------------------------------------------------------------

    @staticmethod
    def check_resources_for_date_range(
        product: Product,
        checkin_date: date,
        checkout_date: date,
    ) -> List[Dict]:
        """
        Check which customer-selectable resources are available for a date range.

        Uses date-based overlap: a booking checking out on the 3rd does NOT
        block a new check-in on the 3rd (back-to-back bookings are allowed).

        Overlap condition: existing.checkin_date < requested.checkout_date
                       AND existing.checkout_date > requested.checkin_date
        """
        resources = product.booking_resources.filter(
            is_active=True,
            assignment_type='customer_selected',
        ).order_by('sort_order')

        results = []
        now = timezone.now()

        for resource in resources:
            # Check confirmed/pending bookings that overlap this date range
            has_overlap = Booking.objects.filter(
                product=product,
                resource=resource,
                status__in=['pending_confirmation', 'confirmed'],
                start_datetime__date__lt=checkout_date,
                end_datetime__date__gt=checkin_date,
            ).exists()

            # Check active slot reservations (only if no booking overlap)
            has_reservation = False
            if not has_overlap:
                has_reservation = BookingSlotReservation.objects.filter(
                    product=product,
                    resource=resource,
                    expires_at__gt=now,
                    start_datetime__date__lt=checkout_date,
                    end_datetime__date__gt=checkin_date,
                ).exists()

            results.append({
                'id': resource.pk,
                'name': resource.name,
                'available': not has_overlap and not has_reservation,
            })

        return results

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _within_advance_window(config: BookingConfig, booking_date: date) -> bool:
        """Check if date is within the min/max advance booking window."""
        now = timezone.now()

        # Min advance
        min_hours = BookingAvailabilityService._advance_to_hours(
            config.min_advance, config.min_advance_unit
        )
        earliest = now + timedelta(hours=min_hours)
        if datetime.combine(booking_date, time(23, 59), tzinfo=dt_timezone.utc) < earliest:
            return False

        # Max advance
        max_hours = BookingAvailabilityService._advance_to_hours(
            config.max_advance, config.max_advance_unit
        )
        latest = now + timedelta(hours=max_hours)
        if datetime.combine(booking_date, time(0, 0), tzinfo=dt_timezone.utc) > latest:
            return False

        return True

    @staticmethod
    def _advance_to_hours(value: int, unit: str) -> float:
        """Convert advance value to hours."""
        multipliers = {
            'hour': 1,
            'day': 24,
            'week': 168,
            'month': 730,  # ~30.4 days
        }
        return value * multipliers.get(unit, 1)

    @staticmethod
    def _check_date_availability(
        product: Product,
        config: BookingConfig,
        booking_date: date,
        resource_id: Optional[int] = None,
    ) -> bool:
        """Check if a date is available based on availability rules."""
        rules = product.booking_availability_rules.all().order_by('-priority')
        if resource_id:
            rules = rules.filter(Q(resource_id=resource_id) | Q(resource__isnull=True))
        else:
            rules = rules.filter(resource__isnull=True)

        # Default: available (if no rules, assume available)
        is_available = True

        for rule in rules:
            if BookingAvailabilityService._rule_matches_date(rule, booking_date):
                if rule.rule_type == 'unavailable':
                    is_available = False
                elif rule.rule_type == 'available':
                    is_available = True
                # custom_cost doesn't affect availability

        return is_available

    @staticmethod
    def _rule_matches_date(rule: BookingAvailabilityRule, booking_date: date) -> bool:
        """Check if an availability rule matches a given date."""
        if rule.scope == 'all_dates':
            return True
        elif rule.scope == 'date_range':
            if rule.start_date and booking_date < rule.start_date:
                return False
            if rule.end_date and booking_date > rule.end_date:
                return False
            return True
        elif rule.scope == 'days_of_week':
            return booking_date.weekday() in (rule.days_of_week or [])
        elif rule.scope == 'specific_dates':
            return booking_date.isoformat() in (rule.specific_dates or [])
        elif rule.scope == 'time_range':
            # Time range rules don't match dates, only times
            return True
        return False

    @staticmethod
    def _get_available_times(
        product: Product,
        config: BookingConfig,
        booking_date: date,
        resource_id: Optional[int] = None,
    ) -> List[Tuple[time, time]]:
        """
        Get available time ranges for a date based on rules.

        Returns list of (start_time, end_time) tuples.
        """
        # Check recurrence rules first
        recurrence_times = []
        if config.recurrence_enabled:
            recurrence_rules = product.booking_recurrence_rules.filter(
                is_active=True,
                start_date__lte=booking_date,
            ).filter(Q(end_date__isnull=True) | Q(end_date__gte=booking_date))

            for rule in recurrence_rules:
                if BookingAvailabilityService._recurrence_matches_date(rule, booking_date):
                    recurrence_times.append((rule.start_time, rule.end_time))

        if recurrence_times:
            return recurrence_times

        # Fall back to availability rules
        rules = product.booking_availability_rules.filter(
            rule_type='available',
        ).order_by('-priority')

        if resource_id:
            rules = rules.filter(Q(resource_id=resource_id) | Q(resource__isnull=True))
        else:
            rules = rules.filter(resource__isnull=True)

        time_ranges = []
        for rule in rules:
            if BookingAvailabilityService._rule_matches_date(rule, booking_date):
                if rule.start_time and rule.end_time:
                    time_ranges.append((rule.start_time, rule.end_time))

        # Default business hours if no rules define times
        if not time_ranges:
            time_ranges = [(time(9, 0), time(17, 0))]

        return time_ranges

    @staticmethod
    def _recurrence_matches_date(rule: BookingRecurrenceRule, booking_date: date) -> bool:
        """Check if a recurrence rule generates a slot on the given date."""
        if rule.frequency == 'daily':
            return True
        elif rule.frequency == 'weekly':
            return rule.day_of_week is not None and booking_date.weekday() == rule.day_of_week
        elif rule.frequency == 'biweekly':
            if rule.day_of_week is None or booking_date.weekday() != rule.day_of_week:
                return False
            # Check if it's an even week from start
            delta_days = (booking_date - rule.start_date).days
            delta_weeks = delta_days // 7
            return delta_weeks % 2 == 0
        elif rule.frequency == 'monthly':
            return rule.day_of_month is not None and booking_date.day == rule.day_of_month
        return False

    @staticmethod
    def _check_slot_capacity(
        product: Product,
        config: BookingConfig,
        booking_date: date,
        start_time: time,
        end_time: time,
        resource_id: Optional[int] = None,
        exclude_reservation_id: Optional[int] = None,
    ) -> int:
        """
        Check remaining capacity for a time slot.

        Counts existing bookings + active slot reservations against max_bookings_per_slot.
        """
        max_capacity = config.max_bookings_per_slot

        start_dt = datetime.combine(booking_date, start_time, tzinfo=dt_timezone.utc)
        end_dt = datetime.combine(booking_date, end_time, tzinfo=dt_timezone.utc)

        # Count confirmed/pending bookings that overlap
        overlapping_bookings = Booking.objects.filter(
            product=product,
            status__in=['pending_confirmation', 'confirmed'],
            start_datetime__lt=end_dt,
            end_datetime__gt=start_dt,
        )
        if resource_id:
            overlapping_bookings = overlapping_bookings.filter(resource_id=resource_id)

        booking_count = overlapping_bookings.count()

        # Count active slot reservations that overlap
        now = timezone.now()
        overlapping_reservations = BookingSlotReservation.objects.filter(
            product=product,
            expires_at__gt=now,
            start_datetime__lt=end_dt,
            end_datetime__gt=start_dt,
        )
        if resource_id:
            overlapping_reservations = overlapping_reservations.filter(resource_id=resource_id)
        if exclude_reservation_id:
            overlapping_reservations = overlapping_reservations.exclude(pk=exclude_reservation_id)

        reservation_count = overlapping_reservations.count()

        return max(0, max_capacity - booking_count - reservation_count)

    @staticmethod
    def _check_accommodation_capacity(
        product: Product,
        config: BookingConfig,
        booking_date: date,
        resource_id: Optional[int] = None,
        exclude_reservation_id: Optional[int] = None,
    ) -> int:
        """
        Check remaining accommodation capacity for a single night.

        When no resource is selected and the product has customer-selected
        resources, sums capacity across all active resources so that one
        room being booked doesn't mark the entire date as fully booked.
        """
        check_in = config.check_in_time or time(15, 0)

        if not resource_id:
            customer_resources = product.booking_resources.filter(
                is_active=True, assignment_type='customer_selected',
            )
            if customer_resources.exists():
                return sum(
                    BookingAvailabilityService._check_slot_capacity(
                        product, config, booking_date, check_in,
                        time(23, 59), res_pk,
                        exclude_reservation_id=exclude_reservation_id,
                    )
                    for res_pk in customer_resources.values_list(
                        'pk', flat=True
                    )
                )

        return BookingAvailabilityService._check_slot_capacity(
            product, config, booking_date, check_in,
            time(23, 59), resource_id,
            exclude_reservation_id=exclude_reservation_id,
        )

    @staticmethod
    def _get_accommodation_slots(
        product: Product,
        config: BookingConfig,
        booking_date: date,
        resource_id: Optional[int] = None,
    ) -> List[Dict]:
        """Get availability for accommodation (day/night-based bookings)."""
        check_in = config.check_in_time or time(15, 0)
        check_out = config.check_out_time or time(11, 0)

        capacity = BookingAvailabilityService._check_accommodation_capacity(
            product, config, booking_date, resource_id,
        )

        base_price = product.price.amount if product.price else Decimal('0')

        return [{
            'start': check_in.strftime('%H:%M'),
            'end': check_out.strftime('%H:%M'),
            'available': capacity > 0,
            'capacity_remaining': capacity,
            'price': str(base_price),
            'type': 'accommodation',
        }]

    @staticmethod
    def _calculate_slot_price(
        product: Product,
        config: BookingConfig,
        booking_date: date,
        start_time: time,
        end_time: time,
        resource_id: Optional[int] = None,
    ) -> Decimal:
        """Calculate base price for a slot (without person types)."""
        base_price = product.price.amount if product.price else Decimal('0')

        # Apply rule price adjustments
        rule_price = BookingAvailabilityService._get_rule_price_adjustment(
            product, booking_date, start_time, end_time, resource_id
        )
        if rule_price['override'] is not None:
            base_price = rule_price['override']
        elif rule_price['adjustment'] is not None:
            base_price += rule_price['adjustment']

        # Resource adjustment
        if resource_id:
            try:
                resource = BookingResource.objects.get(pk=resource_id, product=product)
                base_price += resource.base_cost_adjustment
            except BookingResource.DoesNotExist:
                pass

        return max(base_price, Decimal('0'))

    @staticmethod
    def _get_rule_price_adjustment(
        product: Product,
        booking_date: date,
        start_time: time,
        end_time: time,
        resource_id: Optional[int] = None,
    ) -> Dict:
        """Get price override/adjustment from custom_cost rules."""
        result = {'override': None, 'adjustment': None}

        rules = product.booking_availability_rules.filter(
            rule_type='custom_cost',
        ).order_by('priority')  # Lower priority first, higher overrides

        if resource_id:
            rules = rules.filter(Q(resource_id=resource_id) | Q(resource__isnull=True))
        else:
            rules = rules.filter(resource__isnull=True)

        for rule in rules:
            if BookingAvailabilityService._rule_matches_date(rule, booking_date):
                # Also check time range match
                if rule.scope == 'time_range':
                    if rule.start_time and start_time < rule.start_time:
                        continue
                    if rule.end_time and end_time > rule.end_time:
                        continue

                if rule.cost_override is not None:
                    result['override'] = rule.cost_override
                if rule.cost_adjustment is not None:
                    result['adjustment'] = rule.cost_adjustment

        return result

    @staticmethod
    def _duration_to_minutes(duration: int, unit: str) -> int:
        """Convert duration to minutes."""
        multipliers = {
            'minute': 1,
            'hour': 60,
            'day': 1440,
            'night': 1440,
        }
        return duration * multipliers.get(unit, 1)

    @staticmethod
    def _is_counted_for_capacity(product: Product, person_type_name: str) -> bool:
        """Check if a person type counts against capacity."""
        try:
            pt = product.booking_person_types.get(name=person_type_name)
            return pt.is_counted_for_capacity
        except BookingPersonType.DoesNotExist:
            return True  # Default to counting


class BookingLifecycleService:
    """
    Centralised service for booking lifecycle management.

    Handles status transitions, rescheduling, cancellation, email sending,
    and audit logging via BookingNote. Used by admin change form, customer
    self-service API, and internal services.

    Status transition rules:
        pending_confirmation -> confirmed, cancelled
        confirmed -> completed, cancelled, no_show
        completed, cancelled, no_show -> terminal (no transitions)
    """

    VALID_TRANSITIONS = {
        'pending_confirmation': ['confirmed', 'cancelled'],
        'confirmed': ['completed', 'cancelled', 'no_show'],
    }

    STATUS_EMAIL_MAP = {
        'confirmed': 'booking_confirmation',
        'cancelled': 'booking_cancelled',
        'completed': 'booking_completed',
        'no_show': 'booking_no_show',
    }

    # ------------------------------------------------------------------
    # Status transitions
    # ------------------------------------------------------------------

    @classmethod
    def change_status(
        cls,
        booking: Booking,
        new_status: str,
        author=None,
        reason: str = '',
        send_email: bool = True,
    ) -> Tuple[bool, str]:
        """
        Validate and execute a status transition.

        Args:
            booking: The Booking instance.
            new_status: Target status string.
            author: User performing the action (None for system).
            reason: Optional reason (used for cancellation).
            send_email: Whether to send the lifecycle email.

        Returns:
            (success, message)
        """
        old_status = booking.status
        allowed = cls.VALID_TRANSITIONS.get(old_status, [])

        if new_status not in allowed:
            return False, f'Cannot change from {old_status} to {new_status}'

        booking.status = new_status
        update_fields = ['status', 'updated_at']

        if new_status == 'cancelled' and reason:
            booking.cancellation_reason = reason
            update_fields.append('cancellation_reason')

        booking.save(update_fields=update_fields)

        # Log the transition
        cls.add_note(
            booking,
            f'Status changed from {old_status} to {new_status}'
            + (f': {reason}' if reason else ''),
            author=author,
            note_type='status_change',
        )

        # Send lifecycle email
        if send_email:
            template_type = cls.STATUS_EMAIL_MAP.get(new_status)
            if template_type and booking.customer_email:
                cls.send_booking_email(booking, template_type)

        logger.info(
            f"Booking #{booking.pk} status: {old_status} -> {new_status}"
            + (f" by user {author}" if author else "")
        )
        return True, f'Booking {new_status}'

    @classmethod
    def confirm_from_admin(cls, booking: Booking, author=None) -> Tuple[bool, str]:
        """Confirm a pending booking from the admin."""
        return cls.change_status(booking, 'confirmed', author=author)

    @classmethod
    def mark_completed(cls, booking: Booking, author=None) -> Tuple[bool, str]:
        """Mark a confirmed booking as completed."""
        return cls.change_status(booking, 'completed', author=author)

    @classmethod
    def mark_no_show(cls, booking: Booking, author=None) -> Tuple[bool, str]:
        """Mark a confirmed booking as no-show."""
        return cls.change_status(booking, 'no_show', author=author)

    @classmethod
    @transaction.atomic
    def cancel_booking(
        cls,
        booking: Booking,
        author=None,
        reason: str = '',
        initiated_by: str = 'admin',
    ) -> Tuple[bool, str]:
        """
        Cancel a booking, process waitlist, and send notifications.

        Args:
            initiated_by: 'admin' or 'customer' - affects which emails are sent.
        """
        if booking.status in ('cancelled', 'completed', 'no_show'):
            return False, f'Cannot cancel booking in {booking.status} status'

        old_status = booking.status
        booking.status = 'cancelled'
        booking.cancellation_reason = reason
        booking.save(update_fields=['status', 'cancellation_reason', 'updated_at'])

        cls.add_note(
            booking,
            f'Booking cancelled by {initiated_by}'
            + (f': {reason}' if reason else ''),
            author=author,
            note_type='status_change',
        )

        # Send cancellation email to customer
        if booking.customer_email:
            cls.send_booking_email(booking, 'booking_cancelled', {
                'initiated_by': initiated_by,
            })

        # If customer-initiated, also notify merchant
        if initiated_by == 'customer':
            cls.send_admin_email(booking, 'admin_booking_cancelled')

        # Process waitlist for this slot
        BookingAvailabilityService._process_waitlist(
            booking.product,
            booking.start_datetime.date(),
            booking.start_datetime.time(),
            booking.end_datetime.time(),
        )

        logger.info(f"Booking #{booking.pk} cancelled by {initiated_by}")
        return True, 'Booking cancelled'

    # ------------------------------------------------------------------
    # Reschedule
    # ------------------------------------------------------------------

    @classmethod
    @transaction.atomic
    def reschedule_booking(
        cls,
        booking: Booking,
        new_start: datetime,
        new_end: datetime,
        new_resource_id: Optional[int] = None,
        author=None,
        send_email: bool = True,
    ) -> Tuple[bool, str]:
        """
        Reschedule a booking to a new date/time.

        Checks availability, recalculates price, updates the booking,
        and sends reschedule notification email.
        """
        if booking.status not in ('pending_confirmation', 'confirmed'):
            return False, f'Cannot reschedule booking in {booking.status} status'

        product = booking.product

        # Resolve resource
        resource = None
        resource_id = new_resource_id or (booking.resource_id if booking.resource else None)
        if resource_id:
            resource = BookingResource.objects.filter(
                pk=resource_id, product=product
            ).first()

        # Check availability at new time (exclude current booking from capacity)
        is_available, msg, new_price = BookingAvailabilityService.check_availability(
            product, new_start, new_end,
            resource_id=resource_id,
            persons=booking.persons,
        )

        if not is_available:
            return False, f'New time slot not available: {msg}'

        # Store old values for the note and email
        old_start = booking.start_datetime
        old_end = booking.end_datetime
        old_resource = booking.resource

        # Update booking
        booking.start_datetime = new_start
        booking.end_datetime = new_end
        if resource is not None:
            booking.resource = resource
        if new_price is not None:
            booking.total_cost = new_price

        # Regenerate iCal UID for updated event
        booking.ical_uid = f"booking-{uuid.uuid4()}@spwig"
        booking.save(update_fields=[
            'start_datetime', 'end_datetime', 'resource',
            'total_cost', 'ical_uid', 'updated_at',
        ])

        # Log
        note_text = (
            f'Rescheduled from {old_start.strftime("%b %d, %Y %H:%M")} - '
            f'{old_end.strftime("%H:%M")} to '
            f'{new_start.strftime("%b %d, %Y %H:%M")} - '
            f'{new_end.strftime("%H:%M")}'
        )
        if old_resource != booking.resource:
            note_text += f' (resource: {old_resource} -> {booking.resource})'

        cls.add_note(booking, note_text, author=author, note_type='reschedule')

        # Send email
        if send_email and booking.customer_email:
            cls.send_booking_email(booking, 'booking_rescheduled', {
                'old_date': old_start.strftime('%b %d, %Y'),
                'old_time_start': old_start.strftime('%H:%M'),
                'old_time_end': old_end.strftime('%H:%M'),
            })

        logger.info(f"Booking #{booking.pk} rescheduled to {new_start}")
        return True, 'Booking rescheduled'

    # ------------------------------------------------------------------
    # Notes
    # ------------------------------------------------------------------

    @classmethod
    def add_note(
        cls,
        booking: Booking,
        text: str,
        author=None,
        is_customer_visible: bool = False,
        note_type: str = 'manual',
    ):
        """Create a BookingNote for the booking."""
        from catalog.models import BookingNote

        return BookingNote.objects.create(
            booking=booking,
            author=author,
            note=text,
            note_type=note_type,
            is_customer_visible=is_customer_visible,
        )

    # ------------------------------------------------------------------
    # Email sending
    # ------------------------------------------------------------------

    @classmethod
    def send_booking_email(
        cls,
        booking: Booking,
        template_type: str,
        extra_context: Optional[Dict] = None,
    ):
        """
        Send a lifecycle email to the booking customer.

        Builds the standard booking context dict and delegates to
        EmailSendingService.send_template_email().
        """
        if not booking.customer_email:
            logger.warning(
                f"Cannot send {template_type} for booking #{booking.pk}: no customer email"
            )
            return

        try:
            from email_system.services.email_sender import EmailSendingService
            from core.models import SiteSettings

            site_settings = SiteSettings.objects.first()

            context = cls._build_email_context(booking, site_settings)
            if extra_context:
                context.update(extra_context)

            from email_system.utils.language import get_user_email_language, get_order_email_language, _get_site_default_language
            # Determine language: from order if available, then customer user, then site default
            if booking.order_id:
                _lang = get_order_email_language(booking.order)
            elif booking.customer_id and hasattr(booking.customer, 'user') and booking.customer.user:
                _lang = get_user_email_language(booking.customer.user)
            else:
                _lang = _get_site_default_language()

            EmailSendingService.send_template_email(
                to_email=booking.customer_email,
                template_type=template_type,
                context=context,
                language=_lang,
            )

            # Log the email send as a note
            cls.add_note(
                booking,
                f'Email sent: {template_type}',
                note_type='email',
            )

        except Exception as e:
            logger.error(
                f"Failed to send {template_type} email for booking #{booking.pk}: {e}",
                exc_info=True,
            )

    @classmethod
    def send_admin_email(
        cls,
        booking: Booking,
        template_type: str,
        extra_context: Optional[Dict] = None,
    ):
        """Send a notification email to the merchant/admin."""
        try:
            from email_system.services.email_sender import EmailSendingService
            from core.models import SiteSettings

            site_settings = SiteSettings.objects.first()
            admin_email = getattr(site_settings, 'admin_email', None) or ''

            if not admin_email:
                logger.info(
                    f"No admin email configured, skipping {template_type} "
                    f"for booking #{booking.pk}"
                )
                return

            context = cls._build_email_context(booking, site_settings)
            if extra_context:
                context.update(extra_context)

            EmailSendingService.send_template_email(
                to_email=admin_email,
                template_type=template_type,
                context=context,
                language='en',  # Admin notifications use English
            )

        except Exception as e:
            logger.error(
                f"Failed to send admin email {template_type} for booking #{booking.pk}: {e}",
                exc_info=True,
            )

    @classmethod
    def _build_email_context(cls, booking: Booking, site_settings=None) -> Dict:
        """Build standard context dict for booking email templates."""
        from django.urls import reverse

        # Duration
        duration_minutes = booking.duration_minutes
        if duration_minutes >= 60:
            hours = duration_minutes // 60
            mins = duration_minutes % 60
            duration_display = f"{hours}h" + (f" {mins}m" if mins else "")
        else:
            duration_display = f"{duration_minutes}m"

        # Persons display
        persons_display = ''
        if booking.persons:
            parts = [f"{count} {ptype}" for ptype, count in booking.persons.items()]
            persons_display = ', '.join(parts)

        # URLs
        product_slug = booking.product.slug if booking.product else ''
        ical_url = ''
        if booking.ical_uid and product_slug:
            try:
                ical_url = reverse(
                    'catalog_api:booking-ical',
                    kwargs={
                        'product_slug': product_slug,
                        'ical_uid': booking.ical_uid,
                    },
                )
            except Exception:
                pass

        admin_booking_url = ''
        try:
            admin_booking_url = reverse(
                'admin:catalog_booking_change',
                args=[booking.pk],
            )
        except Exception:
            pass

        # Customer-facing cancel/reschedule URLs
        cancel_url = ''
        reschedule_url = ''
        try:
            cancel_url = reverse(
                'accounts:booking_cancel_action',
                args=[booking.pk],
            )
            reschedule_url = reverse(
                'accounts:booking_reschedule_action',
                args=[booking.pk],
            )
        except Exception:
            pass

        shop_name = ''
        if site_settings:
            shop_name = getattr(site_settings, 'site_name', '')

        return {
            'booking_id': booking.pk,
            'customer_name': booking.customer_name or '',
            'customer_email': booking.customer_email or '',
            'product_name': booking.product.name if booking.product else '',
            'booking_date': booking.start_datetime.strftime('%b %d, %Y'),
            'booking_time_start': booking.start_datetime.strftime('%H:%M'),
            'booking_time_end': booking.end_datetime.strftime('%H:%M'),
            'duration_display': duration_display,
            'resource_name': booking.resource.name if booking.resource else '',
            'persons_display': persons_display,
            'total_cost': str(booking.total_cost) if booking.total_cost else '',
            'deposit_amount': str(booking.deposit_amount) if booking.deposit_amount else '',
            'status': booking.get_status_display(),
            'cancellation_reason': booking.cancellation_reason or '',
            'ical_url': ical_url,
            'cancel_url': cancel_url,
            'reschedule_url': reschedule_url,
            'admin_booking_url': admin_booking_url,
            'shop_name': shop_name,
        }
