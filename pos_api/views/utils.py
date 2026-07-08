"""
POS API shared utilities.

Common helpers used across POS view modules for terminal resolution,
shift management, and cart serialization.
"""
from rest_framework import status
from rest_framework.response import Response


def get_terminal(request):
    """
    Get POSTerminal from X-Terminal-UUID header.

    Returns:
        Tuple of (terminal, error_response). On success error_response is None.
        On failure terminal is None and error_response is a Response.
    """
    import uuid as uuid_lib

    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if not terminal_uuid:
        return None, Response(
            {
                'success': False,
                'error': {
                    'code': 'TERMINAL_REQUIRED',
                    'message': 'X-Terminal-UUID header is required.',
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Validate UUID format before DB query to return clean 400 instead of 500
    try:
        uuid_lib.UUID(terminal_uuid)
    except (ValueError, AttributeError):
        return None, Response(
            {
                'success': False,
                'error': {
                    'code': 'INVALID_UUID',
                    'message': 'Invalid terminal UUID format.',
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    from pos_app.models import POSTerminal
    try:
        terminal = POSTerminal.objects.select_related('warehouse').get(
            uuid=terminal_uuid, is_active=True
        )
        return terminal, None
    except POSTerminal.DoesNotExist:
        return None, Response(
            {
                'success': False,
                'error': {
                    'code': 'TERMINAL_NOT_FOUND',
                    'message': 'Terminal not found or inactive.',
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )


def get_warehouse_id(request):
    """Extract warehouse ID from terminal UUID header or query param."""
    warehouse_id = request.query_params.get('warehouse_id')
    if warehouse_id:
        return int(warehouse_id)

    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if terminal_uuid:
        from pos_app.models import POSTerminal
        try:
            terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
            return terminal.warehouse_id
        except POSTerminal.DoesNotExist:
            pass

    return None


def get_open_shift(request, terminal):
    """
    Get the open shift for the current cashier on the given terminal.

    Returns:
        Tuple of (shift, error_response). On success error_response is None.
        On failure shift is None and error_response is a Response.
    """
    from pos_app.models import POSShift
    shift = POSShift.objects.filter(
        terminal=terminal,
        cashier=request.user,
        ended_at__isnull=True,
    ).first()

    if not shift:
        return None, Response(
            {
                'success': False,
                'error': {
                    'code': 'NO_OPEN_SHIFT',
                    'message': 'No open shift found. Please open a shift first.',
                },
            },
            status=status.HTTP_409_CONFLICT,
        )

    return shift, None


def get_terminal_currency(request):
    """Get effective currency for the terminal making this request."""
    terminal_uuid = request.headers.get('X-Terminal-UUID')
    if terminal_uuid:
        from pos_app.models import POSTerminal
        try:
            terminal = POSTerminal.objects.get(uuid=terminal_uuid, is_active=True)
            return terminal.effective_currency
        except POSTerminal.DoesNotExist:
            pass
    from core.models import SiteSettings
    settings = SiteSettings.objects.first()
    return str(settings.default_currency) if settings else 'EUR'


def serialize_cart(cart, currency=None, request=None):
    """
    Build full cart response dict for POS endpoints.

    Returns a dict compatible with POSCartSerializer.
    When ``request`` is provided, tax is calculated via TaxService using
    the terminal's warehouse location.
    """
    if not currency:
        from core.models import SiteSettings
        settings = SiteSettings.objects.first()
        currency = str(settings.default_currency) if settings else 'EUR'

    items_data = []
    for item in cart.items.select_related(
        'product', 'variant'
    ).filter(parent_bundle__isnull=True).order_by('id'):
        image = None
        if hasattr(item.product, 'images') and item.product.images.exists():
            primary = (
                item.product.images.select_related('media_asset').filter(is_primary=True).first()
                or item.product.images.select_related('media_asset').first()
            )
            if primary and primary.media_asset:
                image = primary.media_asset.get_thumbnail('medium')

        # Calculate item manual discount
        item_manual_discount = None
        if hasattr(item, 'manual_discount_type') and item.manual_discount_type != 'none':
            item_line_total = item.unit_price.amount * item.quantity if item.unit_price else 0
            if item.manual_discount_type == 'percentage':
                calculated_discount = item_line_total * item.manual_discount_value / 100
            else:
                calculated_discount = item.manual_discount_value
            item_manual_discount = {
                'type': item.manual_discount_type,
                'value': str(item.manual_discount_value),
                'calculated_amount': str(calculated_discount),
                'reason': item.manual_discount_reason or '',
                'applied_by': (
                    item.manual_discount_applied_by.get_full_name() or item.manual_discount_applied_by.username
                ) if item.manual_discount_applied_by else None,
                'approved_by': (
                    item.manual_discount_approved_by.get_full_name() or item.manual_discount_approved_by.username
                ) if item.manual_discount_approved_by else None,
            }

        item_dict = {
            'id': item.id,
            'product_id': item.product_id,
            'product_name': str(item.product.name),
            'variant_id': item.variant_id,
            'variant_name': item.variant.name if item.variant else '',
            'sku': item.variant.sku if item.variant and item.variant.sku else (item.product.sku or ''),
            'quantity': item.quantity,
            'unit_price': str(item.unit_price.amount) if item.unit_price else '0.00',
            'line_total': str(item.total_price.amount) if item.total_price else '0.00',
            'image': image,
            'manual_discount': item_manual_discount,
        }

        # Include component breakdown for configurable/bundle products
        child_items = cart.items.filter(
            parent_bundle=item
        ).select_related('product', 'variant', 'variant__image_asset')
        if child_items.exists():
            is_bundle = item.product.product_type == 'bundle'
            children_data = []
            for child in child_items:
                child_image = None
                if child.variant and child.variant.image_asset:
                    child_image = child.variant.image_asset.get_thumbnail('medium')
                if not child_image and hasattr(child.product, 'images') and child.product.images.exists():
                    child_primary = (
                        child.product.images.select_related('media_asset').filter(is_primary=True).first()
                        or child.product.images.select_related('media_asset').first()
                    )
                    if child_primary and child_primary.media_asset:
                        child_image = child_primary.media_asset.get_thumbnail('medium')
                children_data.append({
                    'id': child.id,
                    'product_name': str(child.product.name),
                    'variant_name': child.variant.name if child.variant else '',
                    'quantity': child.quantity,
                    'unit_price': str(child.unit_price.amount) if child.unit_price else '0.00',
                    'image': child_image,
                })
            if is_bundle:
                item_dict['is_bundle'] = True
            else:
                item_dict['is_configurable'] = True
            item_dict['components'] = children_data

        items_data.append(item_dict)

    subtotal = str(cart.subtotal.amount) if hasattr(cart.subtotal, 'amount') else str(cart.subtotal)
    total = str(cart.grand_total.amount) if hasattr(cart.grand_total, 'amount') else str(cart.grand_total)

    discount_amount = '0.00'
    if hasattr(cart, 'voucher_discount_amount') and cart.voucher_discount_amount:
        discount_amount = str(
            cart.voucher_discount_amount.amount
            if hasattr(cart.voucher_discount_amount, 'amount')
            else cart.voucher_discount_amount
        )

    voucher_code = None
    if hasattr(cart, 'applied_vouchers'):
        first_voucher = cart.applied_vouchers.first()
        if first_voucher:
            voucher_code = first_voucher.voucher.code if hasattr(first_voucher, 'voucher') else str(first_voucher)

    # Build cart-level manual discount
    cart_manual_discount = None
    if hasattr(cart, 'pos_manual_discount_type') and cart.pos_manual_discount_type != 'none':
        from decimal import Decimal
        subtotal_value = cart.subtotal.amount if hasattr(cart.subtotal, 'amount') else Decimal(str(cart.subtotal))
        if cart.pos_manual_discount_type == 'percentage':
            calculated_discount = subtotal_value * cart.pos_manual_discount_value / 100
        else:
            calculated_discount = cart.pos_manual_discount_value
        cart_manual_discount = {
            'type': cart.pos_manual_discount_type,
            'value': str(cart.pos_manual_discount_value),
            'calculated_amount': str(calculated_discount),
            'reason': cart.pos_manual_discount_reason or '',
            'applied_by': (
                cart.pos_manual_discount_applied_by.get_full_name() or cart.pos_manual_discount_applied_by.username
            ) if cart.pos_manual_discount_applied_by else None,
            'approved_by': (
                cart.pos_manual_discount_approved_by.get_full_name() or cart.pos_manual_discount_approved_by.username
            ) if cart.pos_manual_discount_approved_by else None,
        }

    # Calculate tax using terminal's warehouse location
    from decimal import Decimal
    tax_amount_decimal = Decimal('0')
    tax_rate_display = Decimal('0')
    if request:
        try:
            terminal, _err = get_terminal(request)
            if terminal:
                warehouse = terminal.warehouse
                if warehouse and warehouse.country:
                    from cart.services.tax_service import TaxService
                    tax_items = []
                    for item in cart.items.select_related('product').filter(
                        parent_bundle__isnull=True
                    ):
                        unit_price = (
                            item.unit_price.amount
                            if hasattr(item.unit_price, 'amount')
                            else Decimal(str(item.unit_price))
                        )
                        line_total = unit_price * item.quantity
                        tax_items.append((item.product, item.quantity, line_total))
                    if tax_items:
                        tax_amount_decimal, _breakdown = TaxService.calculate_tax(
                            items=tax_items,
                            shipping_cost=Decimal('0'),
                            country=warehouse.country,
                            state=warehouse.state_province or '',
                            city=warehouse.city or '',
                            postal_code=warehouse.postal_code or '',
                        )
                        # Derive effective rate for display
                        subtotal_decimal = (
                            cart.subtotal.amount
                            if hasattr(cart.subtotal, 'amount')
                            else Decimal(str(cart.subtotal))
                        )
                        if subtotal_decimal > 0:
                            tax_rate_display = (
                                tax_amount_decimal / subtotal_decimal
                            ).quantize(Decimal('0.0001'))
        except Exception:
            import logging
            logging.getLogger(__name__).warning(
                'POS cart tax calculation failed', exc_info=True
            )

    # Adjust total to include tax
    total_decimal = (
        cart.grand_total.amount
        if hasattr(cart.grand_total, 'amount')
        else Decimal(str(cart.grand_total))
    ) + tax_amount_decimal

    return {
        'id': cart.id,
        'items': items_data,
        'item_count': len(items_data),
        'subtotal': subtotal,
        'tax_amount': str(tax_amount_decimal),
        'tax_rate': str(tax_rate_display),
        'discount_amount': discount_amount,
        'total': str(total_decimal),
        'currency': currency,
        'voucher_code': voucher_code,
        'gift_card_applied': str(
            cart.gift_card_discount_amount.amount
            if hasattr(cart.gift_card_discount_amount, 'amount')
            else cart.gift_card_discount_amount
        ) if cart.gift_card_discount_amount else '0.00',
        'manual_discount': cart_manual_discount,
    }
