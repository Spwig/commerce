from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from admin_api.authentication import MobileTokenAuthentication
from pos_api.permissions import IsStaffUser
from core.api.api_descriptions import TERMINAL_NOT_FOUND, VALIDATION_ERROR
from pos_api.serializers.terminal import (
    POSTerminalSerializer, POSTerminalRegisterSerializer
)


def _get_client_ip(request):
    """Extract client IP from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def _log_lock_event(request, terminal, event_type, locked_by_user=None, performed_by_user=None,
                    manager_override=False, failed_count=0, cart_items=0, cart_total=None,
                    unlock_method='pin'):
    """Create a TerminalLockEvent audit record."""
    from pos_app.models import TerminalLockEvent, POSShift

    # Get current shift if any
    shift = POSShift.objects.filter(
        terminal=terminal,
        ended_at__isnull=True
    ).first()

    TerminalLockEvent.objects.create(
        terminal=terminal,
        shift=shift,
        event_type=event_type,
        performed_by=performed_by_user,
        locked_by=locked_by_user,
        manager_override=manager_override,
        failed_attempt_count=failed_count,
        cart_item_count=cart_items,
        cart_total=cart_total,
        ip_address=_get_client_ip(request),
        unlock_method=unlock_method,
    )


@extend_schema(
    summary=_("Register POS terminal"),
    description=_(
        "Register a new device as a POS terminal using a pairing code. "
        "The pairing code is generated in the admin panel when creating a terminal."
    ),
    request=POSTerminalRegisterSerializer,
    responses={
        200: OpenApiResponse(description=_("Terminal registered successfully, returns terminal config")),
        404: OpenApiResponse(description=_("Invalid or expired pairing code")),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def register_terminal(request):
    """Register a terminal using its pairing code (public — pairing code is the auth)."""
    serializer = POSTerminalRegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    pairing_code = serializer.validated_data['pairing_code'].upper()

    from pos_app.models import POSTerminal
    try:
        terminal = POSTerminal.objects.select_related('warehouse').get(
            pairing_code=pairing_code, is_active=True
        )
    except POSTerminal.DoesNotExist:
        return Response(
            {'success': False, 'error': {'code': 'INVALID_CODE', 'message': 'Invalid or expired pairing code.'}},
            status=status.HTTP_404_NOT_FOUND
        )

    # Update heartbeat
    terminal.last_heartbeat = timezone.now()
    terminal.save(update_fields=['last_heartbeat'])

    return Response({
        'success': True,
        'terminal': POSTerminalSerializer(terminal).data,
        'warehouse': {
            'id': terminal.warehouse_id,
            'name': terminal.warehouse.pos_display_name or terminal.warehouse.name,
        },
    })


@extend_schema(
    summary=_("Get terminal configuration"),
    description=_("Returns the current terminal's configuration including hardware settings."),
    responses={
        200: POSTerminalSerializer,
        404: OpenApiResponse(description=TERMINAL_NOT_FOUND),
    },
    tags=['POS - Terminal'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def terminal_config(request):
    """Get terminal configuration."""
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_TERMINAL', 'message': 'X-Terminal-UUID header is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    from pos_app.models import POSTerminal
    try:
        terminal = POSTerminal.objects.select_related('warehouse').get(
            uuid=terminal_uuid, is_active=True
        )
    except POSTerminal.DoesNotExist:
        return Response(
            {'success': False, 'error': {'code': 'TERMINAL_NOT_FOUND', 'message': 'Terminal not found.'}},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        'success': True,
        'terminal': POSTerminalSerializer(terminal).data,
    })


@extend_schema(
    summary=_("Terminal heartbeat"),
    description=_("Report that the terminal is online. Should be called every 60 seconds."),
    responses={
        200: OpenApiResponse(description=_("Heartbeat recorded")),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def terminal_heartbeat(request):
    """Record terminal heartbeat."""
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return Response({'success': True})  # Silently accept if no terminal

    from pos_app.models import POSTerminal
    POSTerminal.objects.filter(uuid=terminal_uuid).update(
        last_heartbeat=timezone.now()
    )

    return Response({'success': True})


@extend_schema(
    summary=_("Get receipt template"),
    description=_(
        "Returns the receipt template for the terminal's warehouse. "
        "Falls back to the default template (no warehouse assigned) if "
        "the warehouse has no specific template. Returns sensible defaults "
        "if no template exists at all."
    ),
    responses={
        200: OpenApiResponse(description=_("Receipt template data")),
    },
    tags=['POS - Terminal'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def receipt_template(request):
    """Get receipt template for the current terminal's warehouse.

    Template lookup order:
    1. Specific store template (warehouse set)
    2. Store group template (store_group set)
    3. Default template (both null)
    """
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_TERMINAL', 'message': 'X-Terminal-UUID header is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    from pos_app.models import POSTerminal, ReceiptTemplate

    try:
        terminal = POSTerminal.objects.select_related(
            'warehouse', 'warehouse__store_group'
        ).get(uuid=terminal_uuid, is_active=True)
    except POSTerminal.DoesNotExist:
        return Response(
            {'success': False, 'error': {'code': 'TERMINAL_NOT_FOUND', 'message': 'Terminal not found.'}},
            status=status.HTTP_404_NOT_FOUND
        )

    warehouse = terminal.warehouse
    store_group = warehouse.store_group if warehouse else None

    # Template lookup: specific store → store group → default
    template = None

    # 1. Try specific store template
    try:
        template = ReceiptTemplate.objects.select_related('logo', 'warehouse').get(
            warehouse=warehouse
        )
    except ReceiptTemplate.DoesNotExist:
        pass

    # 2. Try store group template
    if template is None and store_group:
        try:
            template = ReceiptTemplate.objects.select_related('logo', 'store_group').get(
                store_group=store_group, warehouse__isnull=True
            )
        except ReceiptTemplate.DoesNotExist:
            pass

    # 3. Try default template (both null)
    if template is None:
        try:
            template = ReceiptTemplate.objects.select_related('logo').get(
                warehouse__isnull=True, store_group__isnull=True
            )
        except ReceiptTemplate.DoesNotExist:
            pass

    if template:
        logo_url = ''
        if template.logo and template.logo.file:
            logo_url = request.build_absolute_uri(template.logo.file.url)

        data = {
            'paper_width': template.paper_width,
            'logo_url': logo_url,
            'header_text': template.get_effective_header(),
            'show_store_address': template.show_store_address,
            'address': template.get_effective_address(),
            'show_store_phone': template.show_store_phone,
            'phone': template.get_effective_phone(),
            'show_store_email': template.show_store_email,
            'email': template.get_effective_email(),
            'tax_id_label': template.tax_id_label,
            'tax_id_number': template.tax_id_number,
            'business_registration': template.business_registration,
            'show_sku': template.show_sku,
            'show_cashier': template.show_cashier,
            'show_terminal_name': template.show_terminal_name,
            'footer_text': template.footer_text,
            'return_policy': template.return_policy,
            'qr_enabled': template.qr_enabled,
            'qr_url': template.qr_url,
            'qr_label': template.qr_label,
            'show_powered_by': template.show_powered_by,
        }
    else:
        # Sensible defaults when no template exists
        data = {
            'paper_width': '80',
            'logo_url': '',
            'header_text': warehouse.pos_display_name or warehouse.name,
            'show_store_address': True,
            'address': warehouse.full_address,
            'show_store_phone': True,
            'phone': warehouse.contact_phone,
            'show_store_email': False,
            'email': '',
            'tax_id_label': '',
            'tax_id_number': '',
            'business_registration': '',
            'show_sku': False,
            'show_cashier': True,
            'show_terminal_name': False,
            'footer_text': 'Thank you for your purchase!',
            'return_policy': '',
            'qr_enabled': False,
            'qr_url': '',
            'qr_label': '',
            'show_powered_by': True,
        }

    return Response({'success': True, 'template': data})


@extend_schema(
    summary=_("Get promo slides"),
    description=_(
        "Returns promotional slides for the terminal's warehouse. "
        "Slides are displayed on the customer-facing display during idle periods."
    ),
    responses={
        200: OpenApiResponse(description=_("List of promo slides with image URLs")),
    },
    tags=['POS - Terminal'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def promo_slides(request):
    """Get promo slides for the current terminal's warehouse.

    Slides are filtered by scope hierarchy:
    - All stores (store_group=null, warehouse=null)
    - This store's group (if warehouse has a store_group)
    - This specific store
    """
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return Response({'success': True, 'slides': []})

    from django.db.models import Q
    from pos_app.models import POSTerminal, PromoSlide

    try:
        terminal = POSTerminal.objects.select_related(
            'warehouse', 'warehouse__store_group'
        ).get(uuid=terminal_uuid, is_active=True)
    except POSTerminal.DoesNotExist:
        return Response({'success': True, 'slides': []})

    warehouse = terminal.warehouse
    store_group = warehouse.store_group if warehouse else None

    # Build filter: All stores OR this group OR this specific store
    slide_filter = Q(is_active=True) & (
        # All stores (both null)
        Q(store_group__isnull=True, warehouse__isnull=True) |
        # This store's group (if set)
        (Q(store_group=store_group) if store_group else Q(pk__isnull=True)) |
        # This specific store
        Q(warehouse=warehouse)
    )

    slides = PromoSlide.objects.filter(slide_filter).select_related(
        'image'
    ).order_by('sort_order', 'created_at')

    slide_data = []
    for slide in slides:
        image_url = ''
        if slide.image:
            # Prefer webp for better compression, fall back to original
            if slide.image.webp_file:
                image_url = request.build_absolute_uri(slide.image.webp_file.url)
            elif slide.image.original_file:
                image_url = request.build_absolute_uri(slide.image.original_file.url)

        slide_data.append({
            'id': slide.id,
            'image_url': image_url,
            'title': slide.title,
            'subtitle': slide.subtitle,
        })

    return Response({'success': True, 'slides': slide_data})


@extend_schema(
    summary=_("Generate display pairing code"),
    description=_(
        "Generate a short-lived 6-digit pairing code for customer display authentication. "
        "The code expires after 5 minutes and can only be used once. "
        "Generating a new code invalidates any existing unused codes for this terminal."
    ),
    responses={
        200: OpenApiResponse(description=_("Pairing code generated")),
        404: OpenApiResponse(description=TERMINAL_NOT_FOUND),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def generate_display_pairing_code(request):
    """Generate a new pairing code for customer display authentication."""
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_TERMINAL', 'message': 'X-Terminal-UUID header is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    from pos_app.models import POSTerminal, DisplayPairingCode

    try:
        terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
    except POSTerminal.DoesNotExist:
        return Response(
            {'success': False, 'error': {'code': 'TERMINAL_NOT_FOUND', 'message': 'Terminal not found.'}},
            status=status.HTTP_404_NOT_FOUND
        )

    # Create a new pairing code (invalidates any existing unused codes)
    pairing = DisplayPairingCode.create_for_terminal(terminal)

    return Response({
        'success': True,
        'code': pairing.code,
        'expires_at': pairing.expires_at.isoformat(),
    })


@extend_schema(
    summary=_("List managers for unlock override"),
    description=_("Return list of managers (id and name) for the manager override unlock flow."),
    responses={
        200: OpenApiResponse(description=_("List of managers")),
    },
    tags=['POS - Terminal'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def list_managers(request):
    """Return list of managers for the lock screen override flow."""
    from pos_app.models import POSStaffDiscount

    managers = POSStaffDiscount.objects.filter(
        is_manager=True,
        manager_pin__isnull=False,
    ).exclude(manager_pin='').select_related('user')

    return Response({
        'success': True,
        'managers': [
            {
                'id': m.user_id,
                'name': m.user.get_full_name() or m.user.email,
            }
            for m in managers
        ],
    })


@extend_schema(
    summary=_("Verify unlock PIN"),
    description=_(
        "Verify a cashier or manager PIN to unlock the terminal. "
        "After 3 failed attempts, only manager PIN will be accepted. "
        "All attempts are logged for audit purposes."
    ),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'pin': {'type': 'string', 'description': '4-6 digit PIN'},
                'locked_by_user_id': {'type': 'integer', 'description': 'User ID who locked the terminal'},
                'failed_attempts': {'type': 'integer', 'description': 'Number of previous failed attempts'},
                'cart_item_count': {'type': 'integer', 'description': 'Number of items in cart'},
                'cart_total': {'type': 'string', 'description': 'Cart total amount'},
                'manager_override': {'type': 'boolean', 'description': 'If true, verify against specific manager'},
                'manager_user_id': {'type': 'integer', 'description': 'Manager user ID for targeted override'},
            },
            'required': ['pin'],
        }
    },
    responses={
        200: OpenApiResponse(description=_("PIN verified successfully")),
        400: OpenApiResponse(description=_("Invalid PIN")),
        404: OpenApiResponse(description=TERMINAL_NOT_FOUND),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def verify_unlock_pin(request):
    """Verify PIN for terminal unlock."""
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_TERMINAL', 'message': 'X-Terminal-UUID header is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    from pos_app.models import POSTerminal, POSStaffDiscount
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
    except POSTerminal.DoesNotExist:
        return Response(
            {'success': False, 'error': {'code': 'TERMINAL_NOT_FOUND', 'message': 'Terminal not found.'}},
            status=status.HTTP_404_NOT_FOUND
        )

    pin = request.data.get('pin', '')
    locked_by_user_id = request.data.get('locked_by_user_id')
    try:
        failed_attempts = int(request.data.get('failed_attempts', 0))
    except (TypeError, ValueError):
        failed_attempts = 0
    try:
        cart_items = int(request.data.get('cart_item_count', 0))
    except (TypeError, ValueError):
        cart_items = 0
    cart_total = request.data.get('cart_total')
    manager_override = request.data.get('manager_override', False)
    manager_user_id = request.data.get('manager_user_id')
    require_manager = failed_attempts >= 3

    # Get the user who locked the terminal
    locked_by_user = None
    if locked_by_user_id:
        try:
            locked_by_user = User.objects.get(pk=locked_by_user_id)
        except User.DoesNotExist:
            pass

    # Try cashier PIN first (if not locked out due to failures and not in manager override mode)
    if not require_manager and not manager_override and locked_by_user_id:
        try:
            staff = POSStaffDiscount.objects.select_related('user').get(user_id=locked_by_user_id)
            if staff.verify_cashier_pin(pin):
                _log_lock_event(
                    request, terminal, 'unlock_cashier',
                    locked_by_user=locked_by_user,
                    performed_by_user=staff.user,
                    cart_items=cart_items,
                    cart_total=cart_total,
                )
                return Response({
                    'success': True,
                    'unlock_type': 'cashier',
                    'user_name': staff.user.get_full_name() or staff.user.email,
                })
        except POSStaffDiscount.DoesNotExist:
            pass

    # Try manager PIN — targeted if manager_user_id provided, broad search otherwise
    manager_staff = None
    if manager_override and manager_user_id:
        try:
            candidate = POSStaffDiscount.objects.select_related('user').get(
                user_id=manager_user_id, is_manager=True)
            if candidate.verify_pin(pin):
                manager_staff = candidate
        except POSStaffDiscount.DoesNotExist:
            pass
    else:
        manager_staff = POSStaffDiscount.objects.filter(
            is_manager=True, manager_pin=pin
        ).select_related('user').first()

    if manager_staff:
        _log_lock_event(
            request, terminal, 'unlock_manager',
            locked_by_user=locked_by_user,
            performed_by_user=manager_staff.user,
            manager_override=True,
            cart_items=cart_items,
            cart_total=cart_total,
        )
        return Response({
            'success': True,
            'unlock_type': 'manager',
            'user_name': manager_staff.user.get_full_name() or manager_staff.user.email,
        })

    # Failed attempt
    new_count = failed_attempts + 1
    _log_lock_event(
        request, terminal, 'unlock_failed',
        locked_by_user=locked_by_user,
        performed_by_user=request.user,
        failed_count=new_count,
        cart_items=cart_items,
        cart_total=cart_total,
    )

    # Log lockout if triggered
    if new_count >= 3 and failed_attempts < 3:
        _log_lock_event(
            request, terminal, 'lockout_triggered',
            locked_by_user=locked_by_user,
            performed_by_user=request.user,
            failed_count=new_count,
            cart_items=cart_items,
            cart_total=cart_total,
        )

    return Response({
        'success': False,
        'error': {'code': 'INVALID_PIN', 'message': 'Invalid PIN'},
        'require_manager': new_count >= 3,
        'failed_attempts': new_count,
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary=_("Log terminal lock event"),
    description=_(
        "Log when a terminal is locked (manually or via auto-lock timeout). "
        "This endpoint is for audit logging only and does not change terminal state."
    ),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'event_type': {'type': 'string', 'enum': ['lock_manual', 'lock_auto']},
                'cart_item_count': {'type': 'integer', 'description': 'Number of items in cart'},
                'cart_total': {'type': 'string', 'description': 'Cart total amount'},
            },
            'required': ['event_type'],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Event logged successfully")),
        400: OpenApiResponse(description=_("Invalid event type")),
        404: OpenApiResponse(description=TERMINAL_NOT_FOUND),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def log_lock_event(request):
    """Log a terminal lock event for audit purposes."""
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_TERMINAL', 'message': 'X-Terminal-UUID header is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    from pos_app.models import POSTerminal

    try:
        terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
    except POSTerminal.DoesNotExist:
        return Response(
            {'success': False, 'error': {'code': 'TERMINAL_NOT_FOUND', 'message': 'Terminal not found.'}},
            status=status.HTTP_404_NOT_FOUND
        )

    event_type = request.data.get('event_type')
    if event_type not in ('lock_manual', 'lock_auto'):
        return Response(
            {'success': False, 'error': {'code': 'INVALID_EVENT', 'message': 'Invalid event type. Use lock_manual or lock_auto.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    cart_items = request.data.get('cart_item_count', 0)
    cart_total = request.data.get('cart_total')

    _log_lock_event(
        request, terminal, event_type,
        locked_by_user=request.user,
        performed_by_user=request.user,
        cart_items=cart_items,
        cart_total=cart_total,
    )

    return Response({'success': True})


@extend_schema(
    summary=_("Verify unlock card"),
    description=_(
        "Verify a staff ID card swipe to unlock the terminal. "
        "Card data is hashed and compared against stored card hashes. "
        "After 3 failed PIN attempts, only manager cards are accepted."
    ),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'card_data': {'type': 'string', 'description': 'Raw card swipe data'},
                'locked_by_user_id': {'type': 'integer'},
                'failed_attempts': {'type': 'integer'},
                'cart_item_count': {'type': 'integer'},
                'cart_total': {'type': 'string'},
                'manager_override': {'type': 'boolean'},
            },
            'required': ['card_data'],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Card verified successfully")),
        400: OpenApiResponse(description=_("Card not recognized")),
        404: OpenApiResponse(description=TERMINAL_NOT_FOUND),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def verify_unlock_card(request):
    """Verify card swipe for terminal unlock."""
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_TERMINAL', 'message': 'X-Terminal-UUID header is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    from pos_app.models import POSTerminal, POSStaffDiscount
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
    except POSTerminal.DoesNotExist:
        return Response(
            {'success': False, 'error': {'code': 'TERMINAL_NOT_FOUND', 'message': 'Terminal not found.'}},
            status=status.HTTP_404_NOT_FOUND
        )

    card_data = request.data.get('card_data', '')
    if not card_data:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_CARD', 'message': 'Card data is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    locked_by_user_id = request.data.get('locked_by_user_id')
    failed_attempts = request.data.get('failed_attempts', 0)
    cart_items = request.data.get('cart_item_count', 0)
    cart_total = request.data.get('cart_total')
    manager_override = request.data.get('manager_override', False)
    require_manager = failed_attempts >= 3

    locked_by_user = None
    if locked_by_user_id:
        try:
            locked_by_user = User.objects.get(pk=locked_by_user_id)
        except User.DoesNotExist:
            pass

    card_hash = POSStaffDiscount.hash_card_data(card_data)

    # Try cashier card first (if not in manager mode)
    if not require_manager and not manager_override and locked_by_user_id:
        try:
            staff = POSStaffDiscount.objects.select_related('user').get(
                user_id=locked_by_user_id, card_identifier=card_hash
            )
            _log_lock_event(
                request, terminal, 'unlock_card',
                locked_by_user=locked_by_user,
                performed_by_user=staff.user,
                cart_items=cart_items,
                cart_total=cart_total,
                unlock_method='card',
            )
            return Response({
                'success': True,
                'unlock_type': 'cashier',
                'user_name': staff.user.get_full_name() or staff.user.email,
            })
        except POSStaffDiscount.DoesNotExist:
            pass

    # Try manager card
    manager_staff = POSStaffDiscount.objects.filter(
        is_manager=True, card_identifier=card_hash
    ).select_related('user').first()

    if manager_staff:
        _log_lock_event(
            request, terminal, 'unlock_card',
            locked_by_user=locked_by_user,
            performed_by_user=manager_staff.user,
            manager_override=True,
            cart_items=cart_items,
            cart_total=cart_total,
            unlock_method='card',
        )
        return Response({
            'success': True,
            'unlock_type': 'manager',
            'user_name': manager_staff.user.get_full_name() or manager_staff.user.email,
        })

    # Card not recognized
    new_count = failed_attempts + 1
    _log_lock_event(
        request, terminal, 'unlock_failed',
        locked_by_user=locked_by_user,
        performed_by_user=request.user,
        failed_count=new_count,
        cart_items=cart_items,
        cart_total=cart_total,
        unlock_method='card',
    )

    return Response({
        'success': False,
        'error': {'code': 'UNKNOWN_CARD', 'message': 'Card not recognized'},
        'require_manager': new_count >= 3,
        'failed_attempts': new_count,
    }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary=_("Register staff unlock card"),
    description=_("Register a card swipe for the current user's quick terminal unlock."),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'card_data': {'type': 'string', 'description': 'Raw card swipe data'},
            },
            'required': ['card_data'],
        }
    },
    responses={
        200: OpenApiResponse(description=_("Card registered successfully")),
        409: OpenApiResponse(description=_("Card already registered to another user")),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def register_staff_card(request):
    """Register a card for quick terminal unlock."""
    from pos_app.models import POSStaffDiscount

    card_data = request.data.get('card_data', '')
    if not card_data:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_CARD', 'message': 'Card data is required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    card_hash = POSStaffDiscount.hash_card_data(card_data)

    # Check no other user has this card
    existing = POSStaffDiscount.objects.filter(card_identifier=card_hash).exclude(user=request.user).first()
    if existing:
        return Response(
            {'success': False, 'error': {'code': 'CARD_IN_USE', 'message': 'This card is registered to another user.'}},
            status=status.HTTP_409_CONFLICT
        )

    staff, _ = POSStaffDiscount.objects.get_or_create(user=request.user)
    staff.card_identifier = card_hash
    staff.save(update_fields=['card_identifier'])

    return Response({'success': True})


@extend_schema(
    summary=_("Remove staff unlock card"),
    description=_("Remove the current user's registered unlock card."),
    responses={
        200: OpenApiResponse(description=_("Card removed successfully")),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def remove_staff_card(request):
    """Remove the current user's registered unlock card."""
    from pos_app.models import POSStaffDiscount

    try:
        staff = POSStaffDiscount.objects.get(user=request.user)
        staff.card_identifier = ''
        staff.save(update_fields=['card_identifier'])
    except POSStaffDiscount.DoesNotExist:
        pass

    return Response({'success': True})


@extend_schema(
    summary=_("Set cashier PIN"),
    description=_(
        "Set or update the current user's cashier PIN for terminal lock/unlock. "
        "PIN must be 4-6 digits. Both pin and pin_confirm must match."
    ),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'pin': {'type': 'string', 'description': '4-6 digit PIN'},
                'pin_confirm': {'type': 'string', 'description': 'PIN confirmation (must match pin)'},
            },
            'required': ['pin', 'pin_confirm'],
        }
    },
    responses={
        200: OpenApiResponse(description=_("PIN set successfully")),
        400: OpenApiResponse(description=VALIDATION_ERROR),
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def set_staff_pin(request):
    """Set or update the current user's cashier PIN."""
    import re
    from django.contrib.auth.hashers import make_password
    from pos_app.models import POSStaffDiscount

    pin = request.data.get('pin', '')
    pin_confirm = request.data.get('pin_confirm', '')

    if not pin or not pin_confirm:
        return Response(
            {'success': False, 'error': {'code': 'MISSING_PIN', 'message': 'PIN and confirmation are required.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not re.match(r'^\d{4,6}$', pin):
        return Response(
            {'success': False, 'error': {'code': 'INVALID_PIN', 'message': 'PIN must be 4-6 digits.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    if pin != pin_confirm:
        return Response(
            {'success': False, 'error': {'code': 'PIN_MISMATCH', 'message': 'PINs do not match.'}},
            status=status.HTTP_400_BAD_REQUEST
        )

    staff, _ = POSStaffDiscount.objects.get_or_create(user=request.user)
    staff.cashier_pin = ''
    staff.cashier_pin_hash = make_password(pin)
    staff.save(update_fields=['cashier_pin', 'cashier_pin_hash'])

    return Response({'success': True})
