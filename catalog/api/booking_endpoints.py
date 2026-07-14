"""
Booking API endpoints for catalog app.

Provides customer-facing endpoints for:
- Checking booking availability (dates and time slots)
- Validating and pricing a specific booking
- iCal feed download
- Joining the waitlist
"""

from datetime import UTC, date, datetime, time
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from catalog.models import Booking, Product
from catalog.services.booking_service import BookingAvailabilityService, BookingLifecycleService

# =============================================================================
# Serializers for drf-spectacular documentation
# =============================================================================


class BookingConfigSerializer(serializers.Serializer):
    booking_type = serializers.CharField()
    duration_type = serializers.CharField()
    duration = serializers.IntegerField()
    duration_unit = serializers.CharField()
    min_duration = serializers.IntegerField(allow_null=True)
    max_duration = serializers.IntegerField(allow_null=True)
    calendar_display = serializers.CharField()
    customer_timezone_enabled = serializers.BooleanField()
    deposit_enabled = serializers.BooleanField()
    deposit_type = serializers.CharField(allow_null=True)
    deposit_amount = serializers.CharField(allow_null=True)
    confirmation_required = serializers.BooleanField()
    min_stay = serializers.IntegerField(help_text="Minimum number of nights (accommodation)")
    max_stay = serializers.IntegerField(help_text="Maximum number of nights (accommodation)")
    standard_occupancy = serializers.IntegerField(help_text="Guests included in base nightly rate")


class BookingResourceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    resource_type = serializers.CharField()
    cost_adjustment = serializers.CharField()
    is_per_night = serializers.BooleanField(
        help_text="Whether cost adjustment is applied per night"
    )


class BookingPersonTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    cost_adjustment = serializers.CharField()
    min_persons = serializers.IntegerField()
    max_persons = serializers.IntegerField()
    is_per_night = serializers.BooleanField(
        help_text="Whether cost adjustment is charged per night"
    )


class AvailableDateSerializer(serializers.Serializer):
    date = serializers.CharField(help_text="ISO 8601 date string (YYYY-MM-DD)")
    available = serializers.BooleanField()
    slots_available = serializers.IntegerField(required=False)
    reason = serializers.CharField(required=False)


class BookingAvailabilityResponseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    config = BookingConfigSerializer()
    resources = BookingResourceSerializer(many=True)
    person_types = BookingPersonTypeSerializer(many=True)
    available_dates = AvailableDateSerializer(many=True)
    year = serializers.IntegerField()
    month = serializers.IntegerField()


class TimeSlotSerializer(serializers.Serializer):
    start = serializers.CharField(help_text="Start time (HH:MM)")
    end = serializers.CharField(help_text="End time (HH:MM)")
    available = serializers.BooleanField()
    remaining = serializers.IntegerField(help_text="Remaining capacity")
    capacity = serializers.IntegerField(help_text="Total capacity for this slot")
    price = serializers.CharField()


class BookingSlotsResponseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    date = serializers.CharField()
    slots = TimeSlotSerializer(many=True)


class BookingCheckRequestSerializer(serializers.Serializer):
    date = serializers.DateField(help_text="Booking date (YYYY-MM-DD)")
    time_start = serializers.CharField(
        required=False, help_text="Start time (HH:MM). Required for non-accommodation bookings."
    )
    time_end = serializers.CharField(
        required=False, help_text="End time (HH:MM). Required for non-accommodation bookings."
    )
    end_date = serializers.DateField(
        required=False, help_text="End date for accommodation/date-range bookings (YYYY-MM-DD)."
    )
    resource_id = serializers.IntegerField(required=False, help_text="Selected resource ID")
    persons = serializers.DictField(
        child=serializers.IntegerField(),
        required=False,
        help_text='Person type counts, e.g. {"Adult": 2, "Child": 1}',
    )
    duration = serializers.IntegerField(
        required=False, help_text="Custom duration when duration_type is customer_selected"
    )
    timezone = serializers.CharField(
        required=False, help_text="Customer timezone (IANA identifier)"
    )


class NightlyBreakdownSerializer(serializers.Serializer):
    date = serializers.CharField(help_text="Night date (YYYY-MM-DD)")
    base_rate = serializers.CharField(help_text="Base nightly rate after rule adjustments")
    resource_surcharge = serializers.CharField(help_text="Per-night resource surcharge")
    person_charges = serializers.CharField(help_text="Per-night extra-person charges")
    rule_name = serializers.CharField(allow_null=True, help_text="Name of applied pricing rule")
    nightly_total = serializers.CharField(help_text="Total for this night")


class LengthOfStayDiscountSerializer(serializers.Serializer):
    percent = serializers.CharField(help_text="Discount percentage")
    amount = serializers.CharField(help_text="Discount amount")
    label = serializers.CharField(help_text="Display label, e.g. '7+ nights: 10% off'")


class BookingCheckResponseSerializer(serializers.Serializer):
    available = serializers.BooleanField()
    reason = serializers.CharField(help_text="Availability message or unavailability reason")
    total_price = serializers.CharField(required=False, help_text="Total booking price")
    deposit_amount = serializers.CharField(required=False, help_text="Deposit amount due now")
    deposit_type = serializers.CharField(required=False, help_text="fixed or percentage")
    # Accommodation-specific fields (included when booking_type is accommodation)
    num_nights = serializers.IntegerField(
        required=False, help_text="Number of nights (accommodation only)"
    )
    nightly_breakdown = NightlyBreakdownSerializer(
        many=True, required=False, help_text="Per-night pricing breakdown (accommodation only)"
    )
    length_of_stay_discount = LengthOfStayDiscountSerializer(
        required=False, allow_null=True, help_text="Length-of-stay discount if applicable"
    )
    subtotal_before_discount = serializers.CharField(
        required=False, help_text="Subtotal before length-of-stay discount"
    )
    one_time_charges = serializers.CharField(
        required=False, allow_null=True, help_text="One-time non-per-night charges"
    )
    resource_name = serializers.CharField(
        required=False, allow_null=True, help_text="Name of selected resource"
    )
    min_stay = serializers.IntegerField(required=False, help_text="Minimum stay in nights")
    max_stay = serializers.IntegerField(required=False, help_text="Maximum stay in nights")
    standard_occupancy = serializers.IntegerField(
        required=False, help_text="Guests included in base rate"
    )


class WaitlistRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="Customer email address")
    name = serializers.CharField(required=False, help_text="Customer name")
    desired_date = serializers.DateField(help_text="Desired booking date (YYYY-MM-DD)")
    desired_time_start = serializers.CharField(
        required=False, help_text="Desired start time (HH:MM)"
    )
    desired_time_end = serializers.CharField(required=False, help_text="Desired end time (HH:MM)")
    desired_persons = serializers.DictField(
        child=serializers.IntegerField(),
        required=False,
        help_text='Desired person counts, e.g. {"Adult": 2}',
    )


class WaitlistResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    waitlist_id = serializers.IntegerField(allow_null=True)


# =============================================================================
# API Endpoints
# =============================================================================


@extend_schema(
    tags=["Catalog"],
    summary=_("Get booking availability"),
    description=_("""
    Returns available dates for a booking product in a given month, along with
    the booking configuration, customer-selectable resources, and person types.

    **Authentication:** None required (public endpoint).

    **Use case:** Called by the booking product page to populate the calendar,
    date picker, or dropdown with available dates.

    Dates are categorized as available or unavailable based on:
    - Booking availability rules configured by the merchant
    - Advance booking window (min/max advance notice)
    - Existing bookings and capacity
    """),
    parameters=[
        OpenApiParameter(
            name="product_slug",
            location=OpenApiParameter.PATH,
            type=str,
            description=_("Product URL slug"),
        ),
        OpenApiParameter(
            name="year",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Year to check (default: current year)"),
        ),
        OpenApiParameter(
            name="month",
            type=int,
            location=OpenApiParameter.QUERY,
            description=_("Month to check, 1-12 (default: current month)"),
        ),
        OpenApiParameter(
            name="resource_id",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_("Filter availability by a specific resource ID"),
        ),
        OpenApiParameter(
            name="timezone",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_("Customer timezone (IANA identifier, e.g. 'America/New_York')"),
        ),
    ],
    responses={
        200: BookingAvailabilityResponseSerializer,
        400: OpenApiResponse(description=_("Invalid year or month parameter")),
        404: OpenApiResponse(description=_("Product not found or not a booking product")),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def booking_availability(request, product_slug):
    """Get available dates for a booking product in a given month."""
    product = get_object_or_404(
        Product.objects.filter(product_type="booking", status="published"),
        slug=product_slug,
    )

    try:
        year = int(request.GET.get("year", timezone.now().year))
        month = int(request.GET.get("month", timezone.now().month))
    except (ValueError, TypeError):
        return Response(
            {"error": "Invalid year or month"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    resource_id = request.GET.get("resource_id")
    if resource_id:
        try:
            resource_id = int(resource_id)
        except (ValueError, TypeError):
            resource_id = None

    dates = BookingAvailabilityService.get_available_dates(product, year, month, resource_id)

    # Include booking config summary for frontend
    config = product.booking_config
    config_data = {
        "booking_type": config.booking_type,
        "duration_type": config.duration_type,
        "duration": config.duration,
        "duration_unit": config.duration_unit,
        "min_duration": config.min_duration,
        "max_duration": config.max_duration,
        "calendar_display": config.calendar_display,
        "customer_timezone_enabled": config.customer_timezone_enabled,
        "deposit_enabled": config.deposit_enabled,
        "deposit_type": config.deposit_type if config.deposit_enabled else None,
        "deposit_amount": str(config.deposit_amount) if config.deposit_enabled else None,
        "confirmation_required": config.confirmation_required,
        "min_stay": config.min_stay,
        "max_stay": config.max_stay,
        "standard_occupancy": config.standard_occupancy,
        "max_occupancy": config.max_occupancy,
    }

    # Include resources if customer-selected
    resources = []
    for r in product.booking_resources.filter(
        is_active=True, assignment_type="customer_selected"
    ).order_by("sort_order"):
        resources.append(
            {
                "id": r.pk,
                "name": r.name,
                "resource_type": r.resource_type,
                "cost_adjustment": str(r.base_cost_adjustment),
                "is_per_night": r.is_per_night,
            }
        )

    # Include person types
    person_types = []
    for pt in product.booking_person_types.all().order_by("sort_order"):
        person_types.append(
            {
                "name": pt.name,
                "cost_adjustment": str(pt.cost_adjustment),
                "min_persons": pt.min_persons,
                "max_persons": pt.max_persons,
                "is_per_night": pt.is_per_night,
            }
        )

    return Response(
        {
            "product_id": product.pk,
            "product_name": product.name,
            "config": config_data,
            "resources": resources,
            "person_types": person_types,
            "available_dates": dates,
            "year": year,
            "month": month,
        }
    )


@extend_schema(
    tags=["Catalog"],
    summary=_("Get booking time slots"),
    description=_("""
    Returns available time slots for a specific date on a booking product.

    **Authentication:** None required (public endpoint).

    **Use case:** Called after the customer selects a date to show available
    time slots. Each slot includes remaining capacity and price.

    For accommodation bookings, a single all-day slot is returned.
    """),
    parameters=[
        OpenApiParameter(
            name="product_slug",
            location=OpenApiParameter.PATH,
            type=str,
            description=_("Product URL slug"),
        ),
        OpenApiParameter(
            name="date",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Date to check (YYYY-MM-DD format)"),
            required=True,
        ),
        OpenApiParameter(
            name="resource_id",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_("Filter slots by a specific resource ID"),
        ),
        OpenApiParameter(
            name="timezone",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=_("Customer timezone (IANA identifier)"),
        ),
    ],
    responses={
        200: BookingSlotsResponseSerializer,
        400: OpenApiResponse(description=_("Missing or invalid date parameter")),
        404: OpenApiResponse(description=_("Product not found or not a booking product")),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def booking_slots(request, product_slug):
    """Get available time slots for a specific date."""
    product = get_object_or_404(
        Product.objects.filter(product_type="booking", status="published"),
        slug=product_slug,
    )

    date_str = request.GET.get("date")
    if not date_str:
        return Response(
            {"error": "date parameter is required (YYYY-MM-DD)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        booking_date = date.fromisoformat(date_str)
    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    resource_id = request.GET.get("resource_id")
    if resource_id:
        try:
            resource_id = int(resource_id)
        except (ValueError, TypeError):
            resource_id = None

    raw_slots = BookingAvailabilityService.get_available_slots(product, booking_date, resource_id)

    # Normalize slot keys for frontend: capacity_remaining → remaining, add capacity
    slots = []
    try:
        max_capacity = product.booking_config.max_bookings_per_slot
    except Exception:
        max_capacity = 1

    for s in raw_slots:
        slots.append(
            {
                "start": s["start"],
                "end": s["end"],
                "available": s["available"],
                "remaining": s.get("capacity_remaining", 0),
                "capacity": max_capacity,
                "price": s.get("price", "0.00"),
            }
        )

    return Response(
        {
            "product_id": product.pk,
            "date": date_str,
            "slots": slots,
        }
    )


@extend_schema(
    tags=["Catalog"],
    summary=_("Check booking availability and price"),
    description=_("""
    Validate a specific booking configuration and calculate the total price.

    **Authentication:** None required (public endpoint).

    **Use case:** Called by the frontend booking widget when the customer has
    selected a date, time, resource, and/or person counts. Returns whether
    the booking is available and the calculated price including any deposit.

    **Request format:**
    - For time-based bookings: send `date` + `time_start` + `time_end`
    - For accommodation/date-range bookings: send `date` + `end_date`
    - Resource and persons are optional depending on product configuration

    **Side effects:** None. This is a read-only price check.
    """),
    request=BookingCheckRequestSerializer,
    responses={
        200: BookingCheckResponseSerializer,
        400: OpenApiResponse(description=_("Missing required fields (date, time)")),
        404: OpenApiResponse(description=_("Product not found or not a booking product")),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def booking_check(request, product_slug):
    """Validate a booking and calculate the price."""
    product = get_object_or_404(
        Product.objects.filter(product_type="booking", status="published"),
        slug=product_slug,
    )

    data = request.data

    # Accept the frontend's date + time_start/time_end format
    booking_date_str = data.get("date")
    if not booking_date_str:
        return Response(
            {"error": "date is required (YYYY-MM-DD)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if isinstance(booking_date_str, str):
            booking_date = date.fromisoformat(booking_date_str)
        else:
            booking_date = booking_date_str
    except (ValueError, TypeError):
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Build start/end datetimes from date + time_start/time_end
    time_start_str = data.get("time_start")
    time_end_str = data.get("time_end")
    end_date_str = data.get("end_date")

    try:
        if time_start_str and time_end_str:
            # Time-based booking (appointment, class, event, rental)
            start_time = time.fromisoformat(time_start_str)
            end_time = time.fromisoformat(time_end_str)
            start_dt = datetime.combine(booking_date, start_time, tzinfo=UTC)
            end_dt = datetime.combine(booking_date, end_time, tzinfo=UTC)
        elif end_date_str:
            # Date-range booking (accommodation)
            if isinstance(end_date_str, str):
                end_date_obj = date.fromisoformat(end_date_str)
            else:
                end_date_obj = end_date_str
            start_dt = datetime.combine(booking_date, time(0, 0), tzinfo=UTC)
            end_dt = datetime.combine(end_date_obj, time(0, 0), tzinfo=UTC)
        else:
            # Fallback: use product's default duration
            try:
                config = product.booking_config
                from datetime import timedelta

                start_dt = datetime.combine(booking_date, time(0, 0), tzinfo=UTC)
                duration_minutes = config.duration
                if config.duration_unit == "hour":
                    duration_minutes = config.duration * 60
                elif config.duration_unit == "day":
                    duration_minutes = config.duration * 1440
                end_dt = start_dt + timedelta(minutes=duration_minutes)
            except Exception:
                return Response(
                    {"error": "time_start/time_end or end_date is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
    except (ValueError, TypeError) as e:
        return Response(
            {"error": f"Invalid time format: {e}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    resource_id = data.get("resource_id")
    persons = data.get("persons", {})

    # Validate person counts — must be non-negative integers
    if persons and isinstance(persons, dict):
        for ptype, count in persons.items():
            try:
                c = int(count)
            except (TypeError, ValueError):
                return Response(
                    {"error": f"Invalid person count for {ptype}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if c < 0:
                return Response(
                    {"error": f"Person count cannot be negative for {ptype}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        persons = {k: int(v) for k, v in persons.items()}

    is_available, message, price = BookingAvailabilityService.check_availability(
        product, start_dt, end_dt, resource_id, persons
    )

    response_data = {
        "available": is_available,
        "reason": message,
    }

    if price is not None:
        response_data["total_price"] = str(price)

        # For accommodation, include full nightly breakdown
        try:
            config = product.booking_config
            if is_available and config.booking_type == "accommodation":
                _, breakdown = BookingAvailabilityService.calculate_booking_price_with_breakdown(
                    product, start_dt, end_dt, resource_id, persons
                )
                response_data["num_nights"] = breakdown.get("num_nights", 0)
                response_data["nightly_breakdown"] = breakdown.get("nightly_breakdown", [])
                response_data["length_of_stay_discount"] = breakdown.get("length_of_stay_discount")
                response_data["subtotal_before_discount"] = breakdown.get(
                    "subtotal_before_discount"
                )
                response_data["one_time_charges"] = breakdown.get("one_time_charges")
                response_data["resource_name"] = breakdown.get("resource_name")
                response_data["min_stay"] = config.min_stay or 1
                response_data["max_stay"] = config.max_stay or 365
                response_data["standard_occupancy"] = config.standard_occupancy or 2
                response_data["max_occupancy"] = config.max_occupancy or 0
        except Exception:
            pass

        # Calculate deposit if applicable
        try:
            config = product.booking_config
            if config.deposit_enabled:
                if config.deposit_type == "fixed":
                    deposit = min(config.deposit_amount, price)
                else:
                    deposit = price * (config.deposit_amount / Decimal("100"))
                response_data["deposit_amount"] = str(deposit)
                response_data["deposit_type"] = config.deposit_type
        except Exception:
            pass

    return Response(response_data)


@extend_schema(
    tags=["Catalog"],
    summary=_("Check per-resource availability for a date range"),
    description=_("""
    Returns availability status for each customer-selectable resource over a date range.

    **Authentication:** None required (public endpoint).

    **Use case:** Called by the accommodation booking widget after the customer
    selects check-in and check-out dates. Disables room cards that are already
    booked for those dates.

    **Overlap logic:** Uses date-based overlap. A booking checking out on the 3rd
    does NOT block a new check-in on the 3rd (back-to-back bookings are allowed).
    """),
    parameters=[
        OpenApiParameter(
            name="product_slug",
            location=OpenApiParameter.PATH,
            type=str,
            description=_("Product URL slug"),
        ),
        OpenApiParameter(
            name="checkin",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Check-in date (YYYY-MM-DD)"),
            required=True,
        ),
        OpenApiParameter(
            name="checkout",
            type=str,
            location=OpenApiParameter.QUERY,
            description=_("Check-out date (YYYY-MM-DD)"),
            required=True,
        ),
    ],
    responses={
        200: inline_serializer(
            name="ResourceAvailabilityResponse",
            fields={
                "resources": serializers.ListField(
                    child=inline_serializer(
                        name="ResourceAvailabilityItem",
                        fields={
                            "id": serializers.IntegerField(),
                            "name": serializers.CharField(),
                            "available": serializers.BooleanField(),
                        },
                    ),
                ),
            },
        ),
        400: OpenApiResponse(description=_("Missing or invalid checkin/checkout parameters")),
        404: OpenApiResponse(description=_("Product not found or not a booking product")),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def booking_resource_availability(request, product_slug):
    """Check per-resource availability for a date range (accommodation)."""
    product = get_object_or_404(
        Product.objects.filter(product_type="booking", status="published"),
        slug=product_slug,
    )

    checkin_str = request.GET.get("checkin")
    checkout_str = request.GET.get("checkout")
    if not checkin_str or not checkout_str:
        return Response(
            {"error": "checkin and checkout parameters are required (YYYY-MM-DD)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        checkin_date = date.fromisoformat(checkin_str)
        checkout_date = date.fromisoformat(checkout_str)
    except ValueError:
        return Response(
            {"error": "Invalid date format. Use YYYY-MM-DD"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if checkout_date <= checkin_date:
        return Response(
            {"error": "checkout must be after checkin"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    results = BookingAvailabilityService.check_resources_for_date_range(
        product,
        checkin_date,
        checkout_date,
    )

    return Response({"resources": results})


@extend_schema(
    tags=["Catalog"],
    summary=_("Get booking resource detail with images"),
    description=_("Returns full detail for a single booking resource, including images/media."),
    responses={
        200: inline_serializer(
            name="BookingResourceDetailResponse",
            fields={
                "id": serializers.IntegerField(),
                "name": serializers.CharField(),
                "description": serializers.CharField(),
                "resource_type": serializers.CharField(),
                "base_cost_adjustment": serializers.CharField(),
                "images": serializers.ListField(
                    child=inline_serializer(
                        name="BookingResourceImageItem",
                        fields={
                            "url": serializers.CharField(),
                            "thumbnail": serializers.CharField(),
                            "alt_text": serializers.CharField(),
                            "is_primary": serializers.BooleanField(),
                            "is_video": serializers.BooleanField(),
                        },
                    ),
                ),
            },
        ),
        404: OpenApiResponse(description=_("Product or resource not found")),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def booking_resource_detail(request, product_slug, resource_id):
    """Get full detail for a booking resource including images."""
    product = get_object_or_404(
        Product.objects.filter(product_type="booking", status="published"),
        slug=product_slug,
    )
    resource = get_object_or_404(
        product.booking_resources.filter(is_active=True),
        pk=resource_id,
    )
    images = []
    for img in resource.images.select_related("media_asset").all():
        images.append(
            {
                "url": img.media_asset.get_display_url(),
                "thumbnail": img.media_asset.get_thumbnail("medium"),
                "alt_text": img.alt_text or img.media_asset.alt_text,
                "is_primary": img.is_primary,
                "is_video": img.media_asset.is_video(),
                "video_type": img.media_asset.mime_type if img.media_asset.is_video() else None,
                "poster": img.media_asset.poster_image.url
                if img.media_asset.is_video() and img.media_asset.poster_image
                else None,
            }
        )
    return Response(
        {
            "id": resource.pk,
            "name": resource.name,
            "description": resource.description,
            "resource_type": resource.resource_type,
            "base_cost_adjustment": str(resource.base_cost_adjustment),
            "images": images,
        }
    )


@extend_schema(
    tags=["Catalog"],
    summary=_("Download booking iCal file"),
    description=_("""
    Download an iCal (.ics) calendar file for a specific booking.

    **Authentication:** None required. The iCal UID serves as a private token.

    **Use case:** Linked from booking confirmation emails so customers can add
    the booking to Google Calendar, Outlook, or Apple Calendar.

    **Security:** The iCal UID is a UUID, making it unguessable. No personal
    data is exposed beyond what's in the iCal event itself.
    """),
    parameters=[
        OpenApiParameter(
            name="product_slug",
            location=OpenApiParameter.PATH,
            type=str,
            description=_("Product URL slug"),
        ),
        OpenApiParameter(
            name="ical_uid",
            location=OpenApiParameter.PATH,
            type=str,
            description=_("Unique iCal identifier for the booking"),
        ),
    ],
    responses={
        (200, "text/calendar"): OpenApiResponse(description=_("iCal file download (.ics)")),
        404: OpenApiResponse(description=_("Booking not found")),
    },
)
@api_view(["GET"])
@permission_classes([AllowAny])
def booking_ical(request, product_slug, ical_uid):
    """Download iCal file for a booking."""
    booking = get_object_or_404(
        Booking.objects.select_related("product", "resource"),
        product__slug=product_slug,
        ical_uid=ical_uid,
    )

    ical_content = BookingAvailabilityService.generate_ical(booking)

    response = HttpResponse(ical_content, content_type="text/calendar")
    response["Content-Disposition"] = f'attachment; filename="booking-{booking.pk}.ics"'
    return response


@extend_schema(
    tags=["Catalog"],
    summary=_("Join booking waitlist"),
    description=_("""
    Add the customer to the waitlist for a booking product.

    **Authentication:** Optional. If authenticated, the customer profile is
    linked to the waitlist entry.

    **Use case:** When a desired time slot is fully booked, the customer
    can join the waitlist. They will be notified by email if a spot opens
    due to a cancellation.

    **Side effects:** Creates a waitlist entry. If a slot opens later,
    the system automatically sends a notification email.

    **Duplicate handling:** Returns 409 Conflict if the customer is already
    on the waitlist for the same date/time.
    """),
    request=WaitlistRequestSerializer,
    responses={
        201: WaitlistResponseSerializer,
        400: OpenApiResponse(description=_("Missing email or desired_date")),
        404: OpenApiResponse(description=_("Product not found or not a booking product")),
        409: WaitlistResponseSerializer,
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def booking_waitlist(request, product_slug):
    """Join the waitlist for a booking product."""
    product = get_object_or_404(
        Product.objects.filter(product_type="booking", status="published"),
        slug=product_slug,
    )

    data = request.data

    email = data.get("email")
    if not email:
        return Response(
            {"error": "email is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        desired_date = date.fromisoformat(data["desired_date"])
    except (KeyError, ValueError):
        return Response(
            {"error": "desired_date is required (YYYY-MM-DD)"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    desired_time_start = None
    desired_time_end = None
    if data.get("desired_time_start"):
        try:
            desired_time_start = time.fromisoformat(data["desired_time_start"])
        except ValueError:
            pass
    if data.get("desired_time_end"):
        try:
            desired_time_end = time.fromisoformat(data["desired_time_end"])
        except ValueError:
            pass

    customer = None
    if request.user.is_authenticated:
        customer = getattr(request.user, "profile", None)

    success, message, entry = BookingAvailabilityService.join_waitlist(
        product=product,
        customer_email=email,
        desired_date=desired_date,
        customer_name=data.get("name", ""),
        desired_time_start=desired_time_start,
        desired_time_end=desired_time_end,
        desired_persons=data.get("desired_persons", {}),
        customer=customer,
    )

    return Response(
        {
            "success": success,
            "message": message,
            "waitlist_id": entry.pk if entry else None,
        },
        status=status.HTTP_201_CREATED if success else status.HTTP_409_CONFLICT,
    )


# =============================================================================
# Customer Self-Service Endpoints
# =============================================================================


class MyBookingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField()
    resource_name = serializers.CharField(allow_null=True)
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    status = serializers.CharField()
    status_display = serializers.CharField()
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    customer_name = serializers.CharField()
    ical_uid = serializers.CharField(allow_null=True)
    is_cancellable = serializers.BooleanField()
    can_reschedule = serializers.BooleanField()


def _get_customer_booking(request, booking_id):
    """
    Helper to get a booking that belongs to the authenticated user.
    Returns (booking, error_response).
    """
    customer = getattr(request.user, "profile", None)
    if not customer:
        return None, Response(
            {"error": "No customer profile found"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        booking = Booking.objects.select_related(
            "product",
            "resource",
        ).get(pk=booking_id, customer=customer)
        return booking, None
    except Booking.DoesNotExist:
        return None, Response(
            {"error": "Booking not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


def _serialize_booking(booking):
    """Serialize a booking for the customer API."""
    return {
        "id": booking.pk,
        "product_name": booking.product.name if booking.product else "",
        "resource_name": booking.resource.name if booking.resource else None,
        "start_datetime": booking.start_datetime.isoformat(),
        "end_datetime": booking.end_datetime.isoformat(),
        "status": booking.status,
        "status_display": booking.get_status_display(),
        "total_cost": str(booking.total_cost) if booking.total_cost else None,
        "deposit_amount": str(booking.deposit_amount) if booking.deposit_amount else None,
        "customer_name": booking.customer_name or "",
        "persons": booking.persons or {},
        "duration_minutes": booking.duration_minutes,
        "ical_uid": booking.ical_uid,
        "is_cancellable": booking.status in ("pending_confirmation", "confirmed"),
        "can_reschedule": booking.status in ("pending_confirmation", "confirmed"),
        "created_at": booking.created_at.isoformat(),
    }


@extend_schema(
    tags=["Bookings - Customer"],
    summary=_("List my bookings"),
    description=_(
        "Returns all bookings for the authenticated customer, ordered by start date (newest first)."
    ),
    responses={200: MyBookingSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    """List bookings for the authenticated customer."""
    customer = getattr(request.user, "profile", None)
    if not customer:
        return Response({"bookings": []})

    bookings = (
        Booking.objects.filter(
            customer=customer,
        )
        .select_related("product", "resource")
        .order_by("-start_datetime")
    )

    return Response(
        {
            "bookings": [_serialize_booking(b) for b in bookings],
        }
    )


@extend_schema(
    tags=["Bookings - Customer"],
    summary=_("Get booking detail"),
    description=_(
        "Returns detailed information about a specific booking owned by the authenticated customer."
    ),
    responses={200: MyBookingSerializer},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def booking_detail_api(request, booking_id):
    """Get a specific booking for the authenticated customer."""
    booking, error = _get_customer_booking(request, booking_id)
    if error:
        return error

    # Include customer-visible notes
    notes = (
        booking.booking_notes.filter(
            is_customer_visible=True,
        )
        .order_by("-created_at")
        .values("note", "created_at", "note_type")
    )

    data = _serialize_booking(booking)
    data["notes"] = list(notes)
    return Response(data)


@extend_schema(
    tags=["Bookings - Customer"],
    summary=_("Cancel my booking"),
    description=_("Cancel a booking. Only pending or confirmed bookings can be cancelled."),
    request=inline_serializer(
        name="CancelBookingRequest",
        fields={"reason": serializers.CharField(required=False)},
    ),
    responses={
        200: inline_serializer(
            name="CancelBookingResponse",
            fields={
                "success": serializers.BooleanField(),
                "message": serializers.CharField(),
            },
        ),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def booking_cancel(request, booking_id):
    """Cancel a booking for the authenticated customer."""
    booking, error = _get_customer_booking(request, booking_id)
    if error:
        return error

    reason = request.data.get("reason", "")

    ok, msg = BookingLifecycleService.cancel_booking(
        booking,
        author=request.user,
        reason=reason,
        initiated_by="customer",
    )

    return Response(
        {"success": ok, "message": msg},
        status=status.HTTP_200_OK if ok else status.HTTP_400_BAD_REQUEST,
    )


@extend_schema(
    tags=["Bookings - Customer"],
    summary=_("Reschedule my booking"),
    description=_("""
    Reschedule a booking to a new date and time. Checks availability before
    confirming the change. Only pending or confirmed bookings can be rescheduled.
    """),
    request=inline_serializer(
        name="RescheduleBookingRequest",
        fields={
            "date": serializers.DateField(),
            "time_start": serializers.CharField(),
            "time_end": serializers.CharField(),
            "resource_id": serializers.IntegerField(required=False),
        },
    ),
    responses={
        200: inline_serializer(
            name="RescheduleBookingResponse",
            fields={
                "success": serializers.BooleanField(),
                "message": serializers.CharField(),
            },
        ),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def booking_reschedule_api(request, booking_id):
    """Reschedule a booking for the authenticated customer."""
    booking, error = _get_customer_booking(request, booking_id)
    if error:
        return error

    data = request.data
    date_str = data.get("date")
    start_str = data.get("time_start")
    end_str = data.get("time_end")

    if not (date_str and start_str and end_str):
        return Response(
            {"error": "date, time_start, and time_end are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        new_date = date.fromisoformat(str(date_str))
        new_start = datetime.combine(
            new_date,
            time.fromisoformat(str(start_str)),
        ).replace(tzinfo=UTC)
        new_end = datetime.combine(
            new_date,
            time.fromisoformat(str(end_str)),
        ).replace(tzinfo=UTC)
    except (ValueError, TypeError):
        return Response(
            {"error": "Invalid date or time format"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    resource_id = data.get("resource_id")

    ok, msg = BookingLifecycleService.reschedule_booking(
        booking,
        new_start,
        new_end,
        new_resource_id=resource_id,
        author=request.user,
    )

    return Response(
        {"success": ok, "message": msg},
        status=status.HTTP_200_OK if ok else status.HTTP_400_BAD_REQUEST,
    )
