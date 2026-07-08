"""
Management command to simulate one day of realistic store activity for demo sites.

Designed to run nightly via cron to keep demo dashboards looking alive.
Uses showcase users and products created by seed_showcase_data.

Usage:
    python manage.py simulate_daily_activity
    python manage.py simulate_daily_activity --date 2026-03-20
    python manage.py simulate_daily_activity --dry-run
    python manage.py simulate_daily_activity --force
"""

import random
import secrets
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from core.management.commands.seed_showcase_data import (
    ABANDONMENT_REASONS_WEIGHTED,
    COUNTRIES,
    CUSTOMER_MESSAGE_TEMPLATES,
    REFERRER_URLS,
    REVIEW_TEMPLATES,
    SHOWCASE_EMAIL_DOMAIN,
    SHOWCASE_EMAIL_PREFIX,
    USER_AGENTS,
    UTM_CAMPAIGNS,
    _pick_country,
    _weighted_choice,
    disable_auto_now,
)

User = get_user_model()

DAILY_ORDER_PREFIX = 'SCD-'

SOURCE_WEIGHTS = [
    ('direct', 35), ('organic', 25), ('email', 12), ('social', 10),
    ('utm_tracked', 8), ('referral', 5), ('loyalty', 3), ('unknown', 2),
]
PAYMENT_WEIGHTS = [
    ('credit_card', 55), ('paypal', 25), ('bank_transfer', 10), ('apple_pay', 10),
]


class Command(BaseCommand):
    help = 'Simulate one day of realistic store activity for demo sites'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Log what would be done without touching the database',
        )
        parser.add_argument(
            '--date',
            type=str,
            help='Simulate a specific date (YYYY-MM-DD). Defaults to today.',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Run even if activity for this date already exists',
        )

    def handle(self, *args, **options):
        self.dry_run = options.get('dry_run', False)
        self.force = options.get('force', False)

        date_str = options.get('date')
        if date_str:
            try:
                self.sim_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                raise CommandError(f'Invalid date format: {date_str}. Use YYYY-MM-DD.')
        else:
            self.sim_date = timezone.now().date()

        self.sim_datetime = timezone.make_aware(
            datetime.combine(self.sim_date, datetime.min.time())
        )
        self.is_weekend = self.sim_date.weekday() >= 5

        # Seed random with date for reproducibility
        random.seed(int(self.sim_date.strftime('%Y%m%d')))

        self.stdout.write(f'\nSimulating activity for {self.sim_date} '
                          f'({"weekend" if self.is_weekend else "weekday"})')

        if not self.force and self._check_already_run():
            self.stdout.write(self.style.WARNING(
                f'Activity for {self.sim_date} already exists. Use --force to re-run.'))
            return

        self._load_context()

        phases = [
            ('New Orders', self._create_new_orders),
            ('Order Lifecycle', self._progress_order_lifecycle),
            ('Visitors', self._create_visitors),
            ('Product Reviews', self._create_reviews),
            ('Abandoned Carts', self._create_abandoned_carts),
            ('Stock Updates', self._update_stock),
            ('Shipment Tracking', self._progress_shipments),
            ('Customer Messages', self._create_customer_messages),
            ('Loyalty Activity', self._process_loyalty_activity),
            ('Affiliate Activity', self._process_affiliate_activity),
            ('Voucher Usage', self._apply_voucher_usage),
            ('Customer Metrics', self._update_customer_metrics),
        ]

        for name, func in phases:
            if self.dry_run:
                self.stdout.write(f'  [DRY RUN] {name} — skipped')
                continue
            try:
                func()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  {name} failed: {e}'))
                import traceback
                traceback.print_exc()

        self.stdout.write(self.style.SUCCESS(
            f'\nDaily activity simulation for {self.sim_date} complete.'))

    # ── Setup ─────────────────────────────────────────────────────────

    def _check_already_run(self):
        from orders.models import Order
        prefix = f'{DAILY_ORDER_PREFIX}{self.sim_date.strftime("%Y%m%d")}-'
        return Order.objects.filter(order_number__startswith=prefix).exists()

    def _load_context(self):
        from catalog.models import Product
        from core.models import SiteSettings

        self.showcase_users = list(
            User.objects.filter(
                email__startswith=SHOWCASE_EMAIL_PREFIX,
                email__endswith=f'@{SHOWCASE_EMAIL_DOMAIN}',
            )
        )
        if not self.showcase_users:
            raise CommandError('No showcase users found. Run seed_showcase_data first.')

        self.products = list(Product.objects.filter(status='published'))
        if not self.products:
            self.products = list(Product.objects.all()[:50])
        if len(self.products) < 5:
            raise CommandError('Not enough products in database (need at least 5).')

        bestseller_count = max(1, len(self.products) // 3)
        self.product_weights = [
            3 if i < bestseller_count else 1 for i in range(len(self.products))
        ]

        self.currency = 'USD'
        try:
            settings = SiteSettings.get_settings()
            if settings and settings.default_currency:
                self.currency = settings.default_currency
        except Exception:
            pass

        self.todays_orders = []

    # ── Phase 1: New Orders ───────────────────────────────────────────

    def _create_new_orders(self):
        from orders.models import Order, OrderItem

        count = random.randint(3, 7) if self.is_weekend else random.randint(2, 5)
        date_str = self.sim_date.strftime('%Y%m%d')
        new_status_weights = [('pending', 60), ('processing', 30), ('shipped', 10)]

        with disable_auto_now(Order, ['created_at']):
            for seq in range(1, count + 1):
                order_number = f'{DAILY_ORDER_PREFIX}{date_str}-{seq:05d}'
                hour = random.randint(6, 23)
                minute = random.randint(0, 59)
                timestamp = self.sim_datetime + timedelta(hours=hour, minutes=minute)

                status = _weighted_choice(new_status_weights)
                source = _weighted_choice(SOURCE_WEIGHTS)
                payment_method = _weighted_choice(PAYMENT_WEIGHTS)
                country = _pick_country()
                user = random.choice(self.showcase_users)

                # Build items from real product prices
                num_items = random.choices([1, 2, 3, 4], weights=[40, 35, 15, 10], k=1)[0]
                selected = random.choices(
                    self.products, weights=self.product_weights, k=num_items)
                seen = set()
                unique_products = []
                for p in selected:
                    if p.pk not in seen:
                        seen.add(p.pk)
                        unique_products.append(p)

                item_details = []
                subtotal = Decimal('0.00')
                for product in unique_products:
                    qty = random.choices([1, 2, 3], weights=[70, 20, 10], k=1)[0]
                    unit_price = (product.price.amount
                                  if hasattr(product.price, 'amount')
                                  else Decimal(str(product.price or '29.99')))
                    item_total = (unit_price * qty).quantize(Decimal('0.01'))
                    subtotal += item_total
                    item_details.append((product, qty, unit_price, item_total))

                tax_rate = Decimal(str(round(random.uniform(0.08, 0.12), 2)))
                tax_amount = (subtotal * tax_rate).quantize(Decimal('0.01'))
                shipping_cost = (Decimal('0.00') if subtotal >= 100
                                 else Decimal(str(random.choice([5.99, 9.99, 14.99]))))
                discount_amount = Decimal('0.00')
                if random.random() < 0.25:
                    discount_pct = Decimal(str(round(random.uniform(0.05, 0.20), 2)))
                    discount_amount = (subtotal * discount_pct).quantize(Decimal('0.01'))

                total_amount = (subtotal + tax_amount + shipping_cost - discount_amount
                                ).quantize(Decimal('0.01'))
                if total_amount < 0:
                    total_amount = subtotal

                if status in ('processing', 'shipped'):
                    payment_status = 'paid'
                else:
                    payment_status = random.choice(['unpaid', 'pending', 'paid'])
                paid_at = (timestamp + timedelta(minutes=random.randint(1, 30))
                           if payment_status == 'paid' else None)

                order = Order(
                    order_number=order_number,
                    user=user,
                    status=status,
                    source=source,
                    email=user.email,
                    phone=f'+1{random.randint(2000000000, 9999999999)}',
                    shipping_name=f'{user.first_name} {user.last_name}',
                    shipping_address1=(
                        f'{random.randint(100, 9999)} '
                        f'{random.choice(["Main", "Oak", "Elm", "Cedar", "Park", "Maple"])} '
                        f'{random.choice(["St", "Ave", "Blvd", "Dr", "Ln"])}'),
                    shipping_address2=(f'Apt {random.randint(1, 500)}'
                                       if random.random() < 0.3 else ''),
                    shipping_city=random.choice(country['cities']),
                    shipping_state='',
                    shipping_postal_code=f'{random.randint(10000, 99999)}',
                    shipping_country=country['code'],
                    billing_same_as_shipping=True,
                    subtotal=subtotal,
                    subtotal_currency=self.currency,
                    tax_amount=tax_amount,
                    tax_amount_currency=self.currency,
                    shipping_cost=shipping_cost,
                    shipping_cost_currency=self.currency,
                    discount_amount=discount_amount,
                    discount_amount_currency=self.currency,
                    gift_card_discount=Decimal('0.00'),
                    gift_card_discount_currency=self.currency,
                    total_amount=total_amount,
                    total_amount_currency=self.currency,
                    payment_status=payment_status,
                    payment_method_type=payment_method,
                    payment_method_last4=f'{random.randint(1000, 9999)}',
                    paid_at=paid_at,
                    amount_paid=(total_amount if payment_status == 'paid'
                                 else Decimal('0.00')),
                    amount_paid_currency=self.currency,
                    amount_refunded=Decimal('0.00'),
                    amount_refunded_currency=self.currency,
                    base_currency=self.currency,
                    created_at=timestamp,
                )
                order.compute_base_amounts()
                order.save()

                for product, qty, unit_price, item_total in item_details:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        variant_name='',
                        sku=product.sku,
                        quantity=qty,
                        unit_price=unit_price,
                        unit_price_currency=self.currency,
                        total_price=item_total,
                        total_price_currency=self.currency,
                        unit_price_base=unit_price,
                        total_price_base=item_total,
                    )

                self.todays_orders.append(order)

        self.stdout.write(f'  New Orders: created {len(self.todays_orders)}')

    # ── Phase 2: Order Lifecycle ──────────────────────────────────────

    def _progress_order_lifecycle(self):
        from orders.models import Order
        from shipping.models import Shipment, TrackingEvent

        cutoff_1d = self.sim_datetime - timedelta(days=1)
        cutoff_2d = self.sim_datetime - timedelta(days=2)
        cutoff_3d = self.sim_datetime - timedelta(days=3)
        cutoff_5d = self.sim_datetime - timedelta(days=5)
        admin_user = User.objects.filter(is_superuser=True).first() or self.showcase_users[0]

        # pending -> processing
        pending = list(Order.objects.filter(
            order_number__startswith='SC', status='pending', created_at__lt=cutoff_1d))
        sample_size = min(len(pending), max(1, int(len(pending) * random.uniform(0.3, 0.5))))
        to_process = random.sample(pending, k=sample_size) if pending else []
        for order in to_process:
            order.status = 'processing'
            order.payment_status = 'paid'
            order.paid_at = order.created_at + timedelta(hours=random.randint(1, 12))
            order.amount_paid = order.total_amount
            order.amount_paid_currency = self.currency
            order.save(update_fields=[
                'status', 'payment_status', 'paid_at',
                'amount_paid', 'amount_paid_currency'])

        # processing -> shipped
        processing = list(Order.objects.filter(
            order_number__startswith='SC', status='processing', created_at__lt=cutoff_1d))
        sample_size = min(len(processing), max(1, int(len(processing) * random.uniform(0.2, 0.4))))
        to_ship = random.sample(processing, k=sample_size) if processing else []
        for order in to_ship:
            order.status = 'shipped'
            order.save(update_fields=['status'])

            tracking_id = f'TRK{random.randint(10000000, 99999999)}'
            shipment = Shipment.objects.create(
                order=order,
                user=admin_user,
                origin_country='US',
                dest_country=order.shipping_country or 'US',
                packages=[{
                    'weight_g': random.randint(200, 5000),
                    'length_cm': 30, 'width_cm': 20, 'height_cm': 15,
                }],
                service_level=random.choice(['standard', 'express', 'economy']),
                shipping_cost=order.shipping_cost,
                shipping_cost_currency=self.currency,
                tracking_id=tracking_id,
                status='in_transit',
            )
            TrackingEvent.objects.create(
                shipment=shipment, status='info_received',
                description='Shipment information received',
                location='Distribution Center',
                occurred_at=self.sim_datetime,
            )
            TrackingEvent.objects.create(
                shipment=shipment, status='in_transit',
                description='Package in transit',
                location='Sorting Facility',
                occurred_at=self.sim_datetime + timedelta(
                    hours=random.randint(2, 8)),
            )

        # shipped -> delivered
        shipped = list(Order.objects.filter(
            order_number__startswith='SC', status='shipped', created_at__lt=cutoff_3d))
        sample_size = min(len(shipped), max(1, int(len(shipped) * random.uniform(0.15, 0.3))))
        to_deliver = random.sample(shipped, k=sample_size) if shipped else []
        for order in to_deliver:
            order.status = 'delivered'
            order.delivered_at = self.sim_datetime
            order.save(update_fields=['status', 'delivered_at'])

            shipment = order.shipments.first()
            if shipment:
                shipment.status = 'delivered'
                shipment.save(update_fields=['status'])
                TrackingEvent.objects.create(
                    shipment=shipment, status='delivered',
                    description='Package delivered',
                    location=order.shipping_city or 'Delivered',
                    occurred_at=self.sim_datetime,
                )

        # Occasional cancellation (~15% daily chance)
        cancel_count = 0
        if random.random() < 0.15:
            cancel_candidates = list(Order.objects.filter(
                order_number__startswith='SC', status='pending',
                created_at__lt=cutoff_2d)[:10])
            if cancel_candidates:
                order = random.choice(cancel_candidates)
                order.status = 'cancelled'
                order.save(update_fields=['status'])
                cancel_count = 1

        # Occasional refund (~5% daily chance)
        refund_count = 0
        if random.random() < 0.05:
            refund_candidates = list(Order.objects.filter(
                order_number__startswith='SC', status='delivered',
                created_at__lt=cutoff_5d)[:20])
            if refund_candidates:
                order = random.choice(refund_candidates)
                order.status = 'refunded'
                order.payment_status = 'refunded'
                order.amount_refunded = order.total_amount
                order.amount_refunded_currency = self.currency
                order.save(update_fields=[
                    'status', 'payment_status',
                    'amount_refunded', 'amount_refunded_currency'])
                refund_count = 1

        self.stdout.write(
            f'  Order Lifecycle: {len(to_process)} processed, '
            f'{len(to_ship)} shipped, {len(to_deliver)} delivered, '
            f'{cancel_count} cancelled, {refund_count} refunded')

    # ── Phase 3: Visitors ─────────────────────────────────────────────

    def _create_visitors(self):
        from geoip.models import VisitorLocation

        count = random.randint(20, 40) if self.is_weekend else random.randint(15, 30)
        date_str = self.sim_date.strftime('%Y%m%d')
        device_types = [('desktop', 38), ('mobile', 48), ('tablet', 10), ('unknown', 4)]
        visitors = []

        for i in range(count):
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            timestamp = self.sim_datetime + timedelta(hours=hour, minutes=minute)

            country = _pick_country()
            device = _weighted_choice(device_types)
            referrer = _weighted_choice(REFERRER_URLS)
            utm = random.choice(UTM_CAMPAIGNS) if random.random() < 0.3 else None
            session_key = f'showcase_daily_{date_str}_{i}_{random.randint(1000, 9999)}'

            visitors.append(VisitorLocation(
                session_key=session_key,
                ip_address=(f'{random.randint(10, 220)}.{random.randint(1, 255)}'
                            f'.{random.randint(1, 255)}.{random.randint(1, 255)}'),
                resolved_country=country['code'],
                resolved_region='',
                resolved_city=random.choice(country['cities']),
                device_type=device,
                referrer_url=referrer,
                utm_source=utm['source'] if utm else '',
                utm_medium=utm['medium'] if utm else '',
                utm_campaign=utm['campaign'] if utm else '',
                utm_term=utm.get('term', '') if utm else '',
                utm_content=utm.get('content', '') if utm else '',
                user_agent=random.choice(
                    USER_AGENTS.get(device, USER_AGENTS['desktop'])),
                page_views=random.choices(
                    range(1, 21),
                    weights=[15, 20, 18, 12, 8, 6, 5, 4, 3, 2,
                             2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    k=1)[0],
                first_seen=timestamp,
                last_seen=timestamp + timedelta(minutes=random.randint(1, 45)),
            ))

        with disable_auto_now(VisitorLocation, ['first_seen', 'last_seen']):
            VisitorLocation.objects.bulk_create(visitors, batch_size=500)

        self.stdout.write(f'  Visitors: created {count}')

    # ── Phase 4: Product Reviews ──────────────────────────────────────

    def _create_reviews(self):
        from catalog.models import ProductReview

        roll = random.random()
        count = 0 if roll < 0.60 else (1 if roll < 0.85 else 2)
        if count == 0:
            self.stdout.write('  Reviews: none today')
            return

        rating_weights = [5, 10, 15, 30, 40]  # 1-5 star weights
        existing_pairs = set(
            ProductReview.objects.filter(user__in=self.showcase_users)
            .values_list('product_id', 'user_id')
        )
        created = 0

        for _ in range(count):
            for _attempt in range(10):
                product = random.choices(
                    self.products, weights=self.product_weights, k=1)[0]
                user = random.choice(self.showcase_users)
                pair = (product.pk, user.pk)
                if pair not in existing_pairs:
                    existing_pairs.add(pair)
                    break
            else:
                continue

            rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights, k=1)[0]
            matching = [t for t in REVIEW_TEMPLATES if t[0] == rating]
            if matching:
                _, title, comment = random.choice(matching)
            else:
                title, comment = 'Good product', 'Satisfied with my purchase.'

            ProductReview.objects.create(
                product=product,
                user=user,
                rating=rating,
                title=title,
                comment=comment,
                is_verified_purchase=random.random() < 0.70,
                is_approved=random.random() < 0.70,
                helpful_count=0,
            )
            created += 1

        self.stdout.write(f'  Reviews: created {created}')

    # ── Phase 5: Abandoned Carts ──────────────────────────────────────

    def _create_abandoned_carts(self):
        from cart.models import Cart, CartItem
        from customers.models import AbandonedCart

        count = random.randint(1, 3)
        date_str = self.sim_date.strftime('%Y%m%d')

        with disable_auto_now(Cart, ['created_at', 'updated_at']):
            for i in range(count):
                user = random.choice(self.showcase_users)
                hour = random.randint(8, 23)
                timestamp = self.sim_datetime + timedelta(
                    hours=hour, minutes=random.randint(0, 59))

                cart = Cart.objects.create(
                    user=user,
                    session_key=f'showcase_daily_cart_{date_str}_{i}',
                    created_at=timestamp,
                    updated_at=timestamp,
                )

                num_items = random.randint(1, 3)
                total_value = Decimal('0.00')
                for _ in range(num_items):
                    product = random.choice(self.products)
                    qty = random.randint(1, 2)
                    price = (product.price.amount
                             if hasattr(product.price, 'amount')
                             else Decimal('29.99'))
                    CartItem.objects.create(
                        cart=cart, product=product, quantity=qty,
                        unit_price=price, unit_price_currency=self.currency,
                    )
                    total_value += price * qty

                reason = _weighted_choice(ABANDONMENT_REASONS_WEIGHTED)
                AbandonedCart.objects.create(
                    user=user,
                    cart=cart,
                    total_items=num_items,
                    total_value=total_value,
                    total_value_currency=self.currency,
                    recovered=False,
                    estimated_reason=reason,
                    recovery_emails_sent=0,
                )

        # Recover 0-1 older abandoned carts (30% chance)
        recover_count = 0
        if random.random() < 0.30:
            unrecovered = AbandonedCart.objects.filter(
                user__in=self.showcase_users,
                recovered=False,
                abandoned_at__lt=self.sim_datetime - timedelta(days=1),
            ).order_by('?')[:1]
            for ac in unrecovered:
                ac.recovered = True
                ac.recovered_at = self.sim_datetime + timedelta(
                    hours=random.randint(10, 20))
                ac.save(update_fields=['recovered', 'recovered_at'])
                recover_count = 1

        self.stdout.write(
            f'  Abandoned Carts: created {count}, recovered {recover_count}')

    # ── Phase 6: Stock Updates ────────────────────────────────────────

    def _update_stock(self):
        from catalog.models import StockItem

        # Restock low items
        low_stocks = list(StockItem.objects.filter(on_hand__lt=10).order_by('on_hand')[:3])
        restocked = 0
        for stock in low_stocks:
            if random.random() < 0.5:
                stock.on_hand += random.randint(20, 100)
                stock.save(update_fields=['on_hand'])
                restocked += 1

        # Decrease stock for today's orders
        decreased = 0
        for order in self.todays_orders:
            for item in order.items.all():
                stock = StockItem.objects.filter(product=item.product).first()
                if stock and stock.on_hand > 0:
                    stock.on_hand = max(0, stock.on_hand - item.quantity)
                    stock.save(update_fields=['on_hand'])
                    decreased += 1

        self.stdout.write(
            f'  Stock: restocked {restocked}, decreased {decreased}')

    # ── Phase 7: Shipment Tracking ────────────────────────────────────

    def _progress_shipments(self):
        from shipping.models import Shipment, TrackingEvent

        # in_transit -> out_for_delivery
        in_transit = list(Shipment.objects.filter(
            order__order_number__startswith='SC',
            status='in_transit',
            created_at__lt=self.sim_datetime - timedelta(days=2),
        ))
        sample_size = min(len(in_transit), max(1, len(in_transit) // 3))
        progressed = 0
        for shipment in random.sample(in_transit, k=sample_size) if in_transit else []:
            shipment.status = 'out_for_delivery'
            shipment.save(update_fields=['status'])
            TrackingEvent.objects.create(
                shipment=shipment, status='out_for_delivery',
                description='Out for delivery',
                location=shipment.order.shipping_city or 'Local Facility',
                occurred_at=self.sim_datetime + timedelta(
                    hours=random.randint(6, 14)),
            )
            progressed += 1

        # out_for_delivery -> delivered
        ofd = list(Shipment.objects.filter(
            order__order_number__startswith='SC',
            status='out_for_delivery',
        ))
        sample_size = min(len(ofd), max(1, len(ofd) // 2))
        delivered = 0
        for shipment in random.sample(ofd, k=sample_size) if ofd else []:
            shipment.status = 'delivered'
            shipment.save(update_fields=['status'])
            TrackingEvent.objects.create(
                shipment=shipment, status='delivered',
                description='Package delivered',
                location=shipment.order.shipping_city or 'Delivered',
                occurred_at=self.sim_datetime + timedelta(
                    hours=random.randint(10, 18)),
            )
            delivered += 1

        self.stdout.write(
            f'  Shipments: {progressed} out for delivery, {delivered} delivered')

    # ── Phase 8: Customer Messages ────────────────────────────────────

    def _create_customer_messages(self):
        from admin_api.models import CustomerMessage
        from orders.models import Order

        roll = random.random()
        count = 0 if roll < 0.40 else (1 if roll < 0.80 else 2)
        if count == 0:
            self.stdout.write('  Messages: none today')
            return

        admin_user = (User.objects.filter(is_superuser=True).first()
                      or self.showcase_users[0])

        with disable_auto_now(CustomerMessage, ['created_at', 'updated_at']):
            for _ in range(count):
                template = random.choice(CUSTOMER_MESSAGE_TEMPLATES)
                msg_type, subject, body, reply = template
                user = random.choice(self.showcase_users)
                hour = random.randint(8, 22)
                timestamp = self.sim_datetime + timedelta(
                    hours=hour, minutes=random.randint(0, 59))

                # Substitute order number if type is 'order'
                order_ref = None
                if msg_type == 'order':
                    sample_order = (Order.objects
                                    .filter(order_number__startswith='SC')
                                    .order_by('?').first())
                    if sample_order:
                        order_ref = sample_order
                        body = body.replace('{order_number}',
                                            sample_order.order_number)
                    else:
                        body = body.replace('{order_number}',
                                            'my recent order')
                else:
                    body = body.replace('{order_number}', 'my recent order')

                # Most new messages are unread
                if random.random() < 0.70:
                    status = 'unread'
                    read_at = None
                    read_by = None
                else:
                    status = 'read'
                    read_at = timestamp + timedelta(
                        hours=random.randint(1, 4))
                    read_by = admin_user

                CustomerMessage.objects.create(
                    name=f'{user.first_name} {user.last_name}',
                    email=user.email,
                    phone='',
                    user=user,
                    subject=subject,
                    message=body,
                    message_type=msg_type,
                    order=order_ref if msg_type == 'order' else None,
                    status=status,
                    read_at=read_at,
                    read_by=read_by,
                    created_at=timestamp,
                    updated_at=read_at or timestamp,
                )

        self.stdout.write(f'  Messages: created {count}')

    # ── Phase 9: Loyalty Activity ─────────────────────────────────────

    def _process_loyalty_activity(self):
        from loyalty.models import (
            LoyaltyBalance, LoyaltyMember, LoyaltyRedemption,
            LoyaltyReward, LoyaltyTransaction,
        )

        # Earn points for today's orders
        earned = 0
        for order in self.todays_orders:
            if not order.user:
                continue
            member = LoyaltyMember.objects.filter(
                customer=order.user, is_active=True).first()
            if not member:
                continue

            total = (order.total_amount.amount
                     if hasattr(order.total_amount, 'amount')
                     else Decimal(str(order.total_amount or 0)))
            points = int(total)
            if points <= 0:
                continue

            LoyaltyTransaction.objects.create(
                member=member,
                transaction_type='earn',
                points=points,
                description=f'Purchase reward (Order {order.order_number})',
                reason=f'Order {order.order_number}',
                status='available',
            )

            balance, _ = LoyaltyBalance.objects.get_or_create(member=member)
            balance.available_points += points
            balance.lifetime_earned += points
            balance.save(update_fields=['available_points', 'lifetime_earned'])
            earned += 1

        # Occasional redemption (10% daily chance)
        redeemed = 0
        if random.random() < 0.10:
            rewards = list(LoyaltyReward.objects.filter(is_active=True))
            if rewards:
                members_with_points = list(
                    LoyaltyMember.objects.filter(
                        customer__in=self.showcase_users,
                        is_active=True,
                        balance__available_points__gte=300,
                    )
                )
                if members_with_points:
                    member = random.choice(members_with_points)
                    reward = random.choice(rewards)
                    if member.balance.available_points >= reward.points_cost:
                        LoyaltyRedemption.objects.create(
                            member=member,
                            reward=reward,
                            redemption_code=(
                                f'LOYALTY-SCD-{secrets.token_hex(5).upper()}'),
                            points_spent=reward.points_cost,
                            status='fulfilled',
                            fulfilled_at=self.sim_datetime,
                        )
                        member.balance.available_points -= reward.points_cost
                        member.balance.lifetime_redeemed += reward.points_cost
                        member.balance.save(update_fields=[
                            'available_points', 'lifetime_redeemed'])
                        redeemed = 1

        self.stdout.write(
            f'  Loyalty: {earned} earn transactions, {redeemed} redemptions')

    # ── Phase 10: Affiliate Activity ──────────────────────────────────

    def _process_affiliate_activity(self):
        from affiliate.models import Affiliate, Click, Commission, Link, Program

        program = Program.objects.filter(status='active').first()
        if not program:
            self.stdout.write('  Affiliates: no active program')
            return

        affiliates = list(Affiliate.objects.filter(status='active'))
        if not affiliates:
            self.stdout.write('  Affiliates: no active affiliates')
            return

        # New clicks
        click_count = random.randint(3, 10)
        clicks_created = 0
        for _ in range(click_count):
            affiliate = random.choice(affiliates)
            link = Link.objects.filter(
                affiliate=affiliate, is_active=True).first()
            if not link:
                continue
            Click.objects.create(
                link=link,
                ip_address=(f'{random.randint(10, 220)}.{random.randint(1, 255)}'
                            f'.{random.randint(1, 255)}.{random.randint(1, 255)}'),
                user_agent=random.choice(
                    USER_AGENTS['desktop'] + USER_AGENTS['mobile']),
                referrer='',
                session_id=(f'aff_daily_{self.sim_date.strftime("%Y%m%d")}'
                            f'_{random.randint(1000, 9999)}'),
                cookie_value=secrets.token_urlsafe(16),
            )
            clicks_created += 1

        # Commission for referral-sourced orders
        commission_count = 0
        referral_orders = [o for o in self.todays_orders if o.source == 'referral']
        for order in referral_orders[:1]:
            affiliate = random.choice(affiliates)
            total = (order.total_amount.amount
                     if hasattr(order.total_amount, 'amount')
                     else Decimal('50.00'))
            commission_amount = (total * Decimal('0.10')).quantize(Decimal('0.01'))
            Commission.objects.create(
                affiliate=affiliate,
                program=program,
                order=order,
                amount=commission_amount,
                currency=self.currency,
                amount_base=commission_amount,
                base_currency=self.currency,
                status='pending',
            )
            commission_count += 1

        self.stdout.write(
            f'  Affiliates: {clicks_created} clicks, '
            f'{commission_count} commissions')

    # ── Phase 11: Voucher Usage ───────────────────────────────────────

    def _apply_voucher_usage(self):
        from vouchers.models import VoucherCode, VoucherUsage

        active_vouchers = list(VoucherCode.objects.filter(
            start_date__lte=self.sim_datetime,
            end_date__gte=self.sim_datetime,
        ))
        if not active_vouchers:
            self.stdout.write('  Vouchers: no active vouchers')
            return

        usage_count = 0
        for order in self.todays_orders:
            if random.random() < 0.25 and order.discount_amount:
                voucher = random.choice(active_vouchers)
                discount_amt = (order.discount_amount.amount
                                if hasattr(order.discount_amount, 'amount')
                                else Decimal('5.00'))
                VoucherUsage.objects.create(
                    voucher=voucher,
                    user=order.user,
                    order=order,
                    discount_amount=discount_amt,
                    discount_amount_currency=self.currency,
                    cart_total=order.total_amount,
                    cart_total_currency=self.currency,
                )
                voucher.current_uses += 1
                voucher.save(update_fields=['current_uses'])
                usage_count += 1

        self.stdout.write(f'  Vouchers: {usage_count} uses applied')

    # ── Phase 12: Customer Metrics ────────────────────────────────────

    def _update_customer_metrics(self):
        from customers.models import CustomerMetrics
        from django.db.models import Avg, Count, Max, Min, Sum
        from orders.models import Order

        affected_users = {o.user for o in self.todays_orders if o.user}
        updated = 0

        for user in affected_users:
            user_orders = Order.objects.filter(
                user=user,
                order_number__startswith='SC',
                status__in=('delivered', 'shipped', 'processing'),
            )
            stats = user_orders.aggregate(
                total_spent=Sum('total_amount_base'),
                avg_order=Avg('total_amount_base'),
                count=Count('id'),
                first_purchase=Min('created_at'),
                last_purchase=Max('created_at'),
            )
            if stats['count'] and stats['count'] > 0:
                CustomerMetrics.objects.update_or_create(
                    user=user,
                    defaults={
                        'total_spent': stats['total_spent'] or 0,
                        'total_spent_currency': self.currency,
                        'lifetime_value': stats['total_spent'] or 0,
                        'lifetime_value_currency': self.currency,
                        'total_orders': stats['count'],
                        'completed_orders': user_orders.filter(
                            status='delivered').count(),
                        'average_order_value': stats['avg_order'] or 0,
                        'average_order_value_currency': self.currency,
                        'first_purchase_date': stats['first_purchase'],
                        'last_purchase_date': stats['last_purchase'],
                    },
                )
                updated += 1

        self.stdout.write(f'  Metrics: updated {updated} customers')
