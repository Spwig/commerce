"""
Shopify-specific transformation functions for field mapping
"""
from decimal import Decimal
from typing import Optional


def transform_shopify_status(value: str) -> str:
    """Transform Shopify product status to internal status"""
    mapping = {
        'active': 'published',
        'draft': 'draft',
        'archived': 'discontinued',
    }
    return mapping.get(str(value).lower(), 'draft')


def transform_shopify_order_status(financial_status: str,
                                   fulfillment_status: Optional[str] = None,
                                   cancelled_at: Optional[str] = None) -> str:
    """
    Transform Shopify compound order status to single internal status.

    Shopify separates financial and fulfillment status:
    - financial_status: pending, authorized, partially_paid, paid, partially_refunded, refunded, voided
    - fulfillment_status: null (unfulfilled), partial, fulfilled
    """
    if cancelled_at:
        return 'cancelled'
    if financial_status == 'refunded':
        return 'refunded'
    if financial_status == 'voided':
        return 'cancelled'
    if fulfillment_status == 'fulfilled':
        return 'completed'
    if fulfillment_status == 'partial':
        return 'processing'
    if financial_status in ('paid', 'partially_paid'):
        return 'processing'
    if financial_status == 'authorized':
        return 'on_hold'
    return 'pending'


def transform_shopify_payment_status(financial_status: str) -> str:
    """Transform Shopify financial status to payment status"""
    mapping = {
        'pending': 'pending',
        'authorized': 'pending',
        'partially_paid': 'partially_paid',
        'paid': 'paid',
        'partially_refunded': 'partially_refunded',
        'refunded': 'refunded',
        'voided': 'failed',
    }
    return mapping.get(str(financial_status).lower(), 'pending')


def transform_shopify_discount_type(value_type: str) -> str:
    """Transform Shopify discount value_type to internal type"""
    mapping = {
        'percentage': 'percentage',
        'fixed_amount': 'fixed',
    }
    return mapping.get(str(value_type).lower(), 'fixed')


def transform_shopify_discount_value(value: str) -> Decimal:
    """
    Transform Shopify discount value (negative) to positive Decimal.
    Shopify stores values like "-10.0" for a 10% or $10 discount.
    """
    try:
        return abs(Decimal(str(value)))
    except (ValueError, TypeError):
        return Decimal('0')


def transform_shopify_inventory_tracked(inventory_management: Optional[str]) -> bool:
    """Transform Shopify inventory_management to boolean track_inventory"""
    return inventory_management == 'shopify'


def transform_shopify_inventory_policy(inventory_policy: str) -> bool:
    """Transform Shopify inventory_policy to boolean allow_backorders"""
    return str(inventory_policy).lower() == 'continue'


def parse_shopify_tags(tags_string: str) -> list:
    """Parse Shopify comma-separated tags string to list"""
    if not tags_string:
        return []
    return [tag.strip() for tag in str(tags_string).split(',') if tag.strip()]
