"""
WooCommerce-specific data transformers
Custom transformation functions for mapping WooCommerce data to platform models
"""

import logging
from decimal import Decimal

from djmoney.money import Money

logger = logging.getLogger(__name__)


def transform_woocommerce_status(value):
    """
    Transform WooCommerce product status to platform status.

    WooCommerce: publish, draft, pending, private
    Platform: published, draft, discontinued

    Args:
        value: WooCommerce status string

    Returns:
        str: Platform status
    """
    mapping = {
        "publish": "published",
        "draft": "draft",
        "pending": "draft",
        "private": "draft",
    }
    return mapping.get(value, "draft")


def transform_woocommerce_type(value):
    """
    Transform WooCommerce product type to platform product type.

    WooCommerce core: simple, variable, grouped, external
    WooCommerce extensions: subscription, variable-subscription, bundle, composite,
                           booking, accommodation-booking
    Platform: simple, variable, bundle, digital, gift_card, customizable, configurable

    Args:
        value: WooCommerce product type

    Returns:
        str: Platform product type
    """
    mapping = {
        # Core WooCommerce types
        "simple": "simple",
        "variable": "variable",
        "grouped": "bundle",
        "external": "simple",  # External/affiliate treated as simple
        # WooCommerce Subscriptions (keep base type, subscription flag set separately)
        "subscription": "simple",
        "variable-subscription": "variable",
        # WooCommerce Product Bundles plugin (distinct from 'grouped')
        "bundle": "bundle",
        # WooCommerce Composite Products
        "composite": "configurable",
        # WooCommerce Bookings
        "booking": "booking",
        "accommodation-booking": "booking",
    }
    return mapping.get(value, "simple")


def transform_money(value, currency=None):
    """
    Convert string price to Money object.

    Args:
        value: Price as string or number
        currency: Currency code (default: merchant's configured currency)

    Returns:
        Money: Money object or None if empty
    """
    if currency is None:
        from core.utils import get_default_currency

        currency = get_default_currency()

    if value is None or value == "":
        return None

    try:
        return Money(Decimal(str(value)), currency)
    except (ValueError, TypeError, ArithmeticError) as e:
        logger.warning(f"Failed to convert price '{value}' to Money: {e}")
        return None


def safe_money(value, currency=None):
    """
    Like transform_money but returns Money(0, currency) instead of None.
    Use for non-nullable MoneyFields where the DB does not allow NULL.
    """
    if currency is None:
        from core.utils import get_default_currency

        currency = get_default_currency()

    result = transform_money(value, currency)
    if result is None:
        return Money(Decimal("0"), currency)
    return result


def safe_decimal(value, default="0"):
    """
    Safely convert a value to Decimal, returning Decimal(default) if None or invalid.
    Handles Shopify/WooCommerce sending explicit null for numeric fields.
    """
    if value is None or value == "":
        return Decimal(default)
    try:
        return Decimal(str(value))
    except (ValueError, TypeError, ArithmeticError):
        return Decimal(default)


def transform_integer_nullable(value):
    """
    Convert value to integer, returning None for empty values.

    Args:
        value: Value to convert

    Returns:
        int or None
    """
    if value is None or value == "":
        return None

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def transform_decimal_nullable(value):
    """
    Convert value to Decimal, returning None for empty values.

    Args:
        value: Value to convert

    Returns:
        Decimal or None
    """
    if value is None or value == "":
        return None

    try:
        return Decimal(str(value))
    except (ValueError, TypeError, ArithmeticError):
        return None


def transform_woocommerce_backorders(value):
    """
    Convert WooCommerce backorders setting to boolean.

    WooCommerce: 'yes', 'no', 'notify'
    Platform: True (allow backorders), False (don't allow)

    Args:
        value: WooCommerce backorders value

    Returns:
        bool: True if backorders allowed
    """
    return value in ["yes", "notify"]


def extract_seo_meta(meta_data_array):
    """
    Extract important SEO fields from WooCommerce meta_data array.

    Extracts:
    - Primary category ID (_yoast_wpseo_primary_product_cat)
    - Product identifiers (GTIN, ISBN, MPN)
    - SEO score

    Args:
        meta_data_array: List of meta_data dicts from WooCommerce

    Returns:
        dict: Extracted SEO fields
    """
    seo_fields = {}

    for item in meta_data_array:
        key = item.get("key", "")
        value = item.get("value", "")

        # Extract Yoast primary category
        if key == "_yoast_wpseo_primary_product_cat":
            seo_fields["primary_category_id"] = value

        # Extract Yoast primary brand
        elif key == "_yoast_wpseo_primary_product_brand":
            seo_fields["primary_brand_id"] = value

        # Extract SEO content score
        elif key == "_yoast_wpseo_content_score":
            try:
                seo_fields["seo_score"] = int(value)
            except (ValueError, TypeError):
                pass

        # Extract product identifiers
        elif key == "wpseo_global_identifier_values":
            import json

            try:
                identifiers = json.loads(value) if isinstance(value, str) else value
                if identifiers:
                    seo_fields["identifiers"] = identifiers
            except (json.JSONDecodeError, TypeError):
                pass

        # Extract GTIN
        elif key == "_cr_gtin" and value:
            seo_fields["gtin"] = value

    return seo_fields


def filter_meta_data(meta_data_array, ignore_prefixes):
    """
    Filter out plugin noise from WooCommerce meta_data.

    Args:
        meta_data_array: List of meta_data dicts
        ignore_prefixes: List of prefixes to ignore

    Returns:
        list: Filtered meta_data array
    """
    filtered = []

    for item in meta_data_array:
        key = item.get("key", "")

        # Skip if key starts with any ignore prefix
        if any(key.startswith(prefix) for prefix in ignore_prefixes):
            continue

        # Skip internal WordPress fields (start with _) unless they're important
        # Important fields are handled separately in extract_seo_meta
        if key.startswith("_"):
            continue

        filtered.append(item)

    return filtered


def apply_price_adjustment(price, adjustment_type, adjustment_value):
    """
    Apply price adjustment (increase/decrease by percentage or fixed amount).

    Args:
        price: Original price (Money object or Decimal)
        adjustment_type: 'percentage', 'fixed', or 'none'
        adjustment_value: Adjustment value (e.g., 10 for 10% or $10)

    Returns:
        Money or Decimal: Adjusted price
    """
    if adjustment_type == "none" or not adjustment_value:
        return price

    if price is None:
        return None

    try:
        adjustment = Decimal(str(adjustment_value))

        if isinstance(price, Money):
            if adjustment_type == "percentage":
                # Calculate percentage adjustment
                multiplier = Decimal("1") + (adjustment / Decimal("100"))
                return Money(price.amount * multiplier, price.currency)
            elif adjustment_type == "fixed":
                return Money(price.amount + adjustment, price.currency)

        else:  # Decimal
            if adjustment_type == "percentage":
                multiplier = Decimal("1") + (adjustment / Decimal("100"))
                return price * multiplier
            elif adjustment_type == "fixed":
                return price + adjustment

    except (ValueError, TypeError, ArithmeticError) as e:
        logger.warning(f"Failed to apply price adjustment: {e}")

    return price


def resolve_category_by_external_id(external_id, job):
    """
    Find a Category by its external_id (WooCommerce category ID).

    Used for resolving parent categories and product categories.

    Args:
        external_id: WooCommerce category ID
        job: MigrationJob instance

    Returns:
        Category instance or None
    """
    from catalog.models import Category

    try:
        return Category.objects.get(external_id=str(external_id))
    except Category.DoesNotExist:
        logger.warning(f"Category with external_id {external_id} not found (job {job.id})")
        return None
    except Category.MultipleObjectsReturned:
        logger.error(f"Multiple categories with external_id {external_id} found")
        return Category.objects.filter(external_id=str(external_id)).first()


def transform_tax_status_boolean(value):
    """
    Convert WooCommerce tax_status to boolean.

    WooCommerce: 'taxable', 'shipping', 'none'
    Platform: True (is_taxable), False (not taxable)

    Args:
        value: WooCommerce tax_status value

    Returns:
        bool: True if taxable
    """
    return value in ["taxable", "shipping"]


def transform_woocommerce_order_status(value):
    """
    Transform WooCommerce order status to platform status.

    WooCommerce: pending, processing, on-hold, completed, cancelled, refunded, failed
    Platform: pending, processing, delivered, cancelled, refunded

    Args:
        value: WooCommerce order status

    Returns:
        str: Platform order status
    """
    mapping = {
        "pending": "pending",
        "processing": "processing",
        "on-hold": "pending",
        "completed": "delivered",
        "cancelled": "cancelled",
        "refunded": "refunded",
        "failed": "cancelled",
    }
    return mapping.get(value, "pending")


def transform_review_status(value):
    """
    Transform WooCommerce review status to boolean.

    WooCommerce: 'approved', 'hold', 'spam', 'unspam', 'trash', 'untrash'
    Platform: True (approved), False (not approved)

    Args:
        value: WooCommerce review status

    Returns:
        bool: True if approved
    """
    return value == "approved"


def transform_coupon_discount_type(value):
    """
    Transform WooCommerce coupon discount type to platform type.

    WooCommerce: percent, fixed_cart, fixed_product
    Platform: percentage, fixed

    Args:
        value: WooCommerce discount type

    Returns:
        str: Platform discount type
    """
    mapping = {
        "percent": "percentage",
        "fixed_cart": "fixed",
        "fixed_product": "fixed",
    }
    return mapping.get(value, "percentage")


# =============================================================================
# Special Product Type Detection
# =============================================================================


def detect_subscription_product(product_data):
    """
    Detect WooCommerce subscription products (WooCommerce Subscriptions plugin).

    Subscriptions are identified by:
    - Product type: 'subscription' or 'variable-subscription'
    - Meta fields: _subscription_period, _subscription_price, etc.

    Args:
        product_data: WooCommerce product data dict

    Returns:
        tuple: (is_subscription: bool, subscription_details: dict)
    """
    product_type = product_data.get("type", "")
    meta_data = product_data.get("meta_data", [])

    # Check product type
    is_subscription = product_type in ["subscription", "variable-subscription"]

    # Subscription-related meta keys
    subscription_keys = [
        "_subscription_period",  # day, week, month, year
        "_subscription_period_interval",  # number of periods
        "_subscription_price",  # recurring price
        "_subscription_sign_up_fee",  # one-time setup fee
        "_subscription_trial_period",  # trial period type
        "_subscription_trial_length",  # trial length
        "_subscription_length",  # total subscription length (0 = unlimited)
        "_subscription_limit",  # purchase limit
        "_subscription_one_time_shipping",  # ship once or every renewal
    ]

    subscription_meta = {}
    for item in meta_data:
        key = item.get("key", "")
        if key in subscription_keys:
            subscription_meta[key] = item.get("value")
            is_subscription = True

    subscription_details = {
        "original_type": product_type,
        "meta": subscription_meta,
    }

    # Parse period for readability
    if "_subscription_period" in subscription_meta:
        period = subscription_meta["_subscription_period"]
        interval = subscription_meta.get("_subscription_period_interval", "1")
        subscription_details["billing_description"] = f"Every {interval} {period}(s)"

    if "_subscription_price" in subscription_meta:
        subscription_details["recurring_price"] = subscription_meta["_subscription_price"]

    if "_subscription_sign_up_fee" in subscription_meta:
        subscription_details["setup_fee"] = subscription_meta["_subscription_sign_up_fee"]

    return is_subscription, subscription_details


def detect_digital_product(product_data):
    """
    Detect WooCommerce downloadable/virtual products.

    Digital products are identified by:
    - downloadable: true
    - virtual: true
    - downloads: array of download files

    Args:
        product_data: WooCommerce product data dict

    Returns:
        tuple: (is_digital: bool, digital_details: dict)
    """
    is_downloadable = product_data.get("downloadable", False)
    is_virtual = product_data.get("virtual", False)
    downloads = product_data.get("downloads", [])

    is_digital = is_downloadable or (is_virtual and len(downloads) > 0)

    digital_details = {
        "is_downloadable": is_downloadable,
        "is_virtual": is_virtual,
        "download_limit": product_data.get("download_limit", -1),  # -1 = unlimited
        "download_expiry": product_data.get("download_expiry", -1),  # days, -1 = never
        "downloads": downloads,  # [{id, name, file}, ...]
        "files_count": len(downloads),
    }

    return is_digital, digital_details


def detect_external_product(product_data):
    """
    Detect WooCommerce external/affiliate products.

    External products link to an external URL instead of being purchasable.

    Args:
        product_data: WooCommerce product data dict

    Returns:
        tuple: (is_external: bool, external_details: dict)
    """
    is_external = product_data.get("type") == "external"

    external_details = {
        "external_url": product_data.get("external_url", ""),
        "button_text": product_data.get("button_text", "Buy Now"),
    }

    return is_external, external_details


def parse_woocommerce_datetime(date_string):
    """
    Parse WooCommerce datetime string to timezone-aware datetime.

    WooCommerce format: "2023-01-15T10:30:00" or "2023-01-15T10:30:00Z"

    Args:
        date_string: ISO format datetime string from WooCommerce

    Returns:
        datetime: Timezone-aware datetime or None if parsing fails
    """
    from datetime import datetime

    if not date_string:
        return None

    try:
        # Handle Z suffix or no timezone
        cleaned = date_string.replace("Z", "+00:00")
        if "+" not in cleaned and "-" not in cleaned[-6:]:
            # No timezone info - assume UTC
            cleaned += "+00:00"
        return datetime.fromisoformat(cleaned)
    except (ValueError, TypeError):
        return None


def detect_addon_product(product_data):
    """
    Detect WooCommerce Product Add-Ons.

    Add-ons are stored in _product_addons meta field as a serialized array
    of add-on definitions (text fields, selects, file uploads, etc.).

    Args:
        product_data: WooCommerce product data dict

    Returns:
        tuple: (has_addons: bool, addon_details: list)
    """
    meta_data = product_data.get("meta_data", [])

    addons = None
    for item in meta_data:
        if item.get("key") == "_product_addons":
            addons = item.get("value")
            break

    if not addons:
        return False, []

    # Ensure it's a list (WC REST API should deserialize PHP arrays)
    if isinstance(addons, str):
        import json

        try:
            addons = json.loads(addons)
        except (json.JSONDecodeError, TypeError):
            return False, []

    if not isinstance(addons, list) or len(addons) == 0:
        return False, []

    return True, addons


def detect_bundle_product(product_data):
    """
    Detect WooCommerce Product Bundles plugin data.

    WC Bundles plugin uses product type 'bundle' (not 'grouped') and stores
    component data in _bundled_items meta field.

    Args:
        product_data: WooCommerce product data dict

    Returns:
        tuple: (is_bundle: bool, bundle_details: dict)
    """
    product_type = product_data.get("type", "")
    meta_data = product_data.get("meta_data", [])

    # Check product type
    if product_type != "bundle":
        return False, {}

    # Extract bundled items meta
    bundled_items = None
    bundle_data = {}

    for item in meta_data:
        key = item.get("key", "")
        if key == "_bundled_items":
            bundled_items = item.get("value")
        elif key == "_bundle_sell_ids":
            bundle_data["cross_sell_ids"] = item.get("value")
        elif key == "_bundle_layout":
            bundle_data["layout"] = item.get("value")

    if bundled_items:
        if isinstance(bundled_items, str):
            import json

            try:
                bundled_items = json.loads(bundled_items)
            except (json.JSONDecodeError, TypeError):
                bundled_items = {}
        bundle_data["items"] = bundled_items

    return True, bundle_data


def detect_gift_card_product(product_data):
    """
    Detect WooCommerce Gift Card products.

    Supports multiple gift card plugins: WooCommerce Gift Cards (official),
    YITH WooCommerce Gift Cards, PW WooCommerce Gift Cards, AFGC.

    Args:
        product_data: WooCommerce product data dict

    Returns:
        tuple: (is_gift_card: bool, gift_card_details: dict)
    """
    meta_data = product_data.get("meta_data", [])
    product_type = product_data.get("type", "")

    gift_card_data = {}
    is_gift_card = False

    # Check for product type hints
    if product_type in ("pw-gift-card", "gift-card", "yith-gift-card"):
        is_gift_card = True

    for item in meta_data:
        key = item.get("key", "")
        value = item.get("value")

        # Official WooCommerce Gift Cards
        if key == "_gift_card_amounts":
            gift_card_data["amounts"] = value
            is_gift_card = True
        elif key == "_gift_card_type":
            gift_card_data["type"] = value  # physical, virtual, email
            is_gift_card = True

        # YITH Gift Cards
        elif key == "_ywgc_amounts":
            gift_card_data["amounts"] = value
            is_gift_card = True
        elif key == "_ywgc_amounts_type":
            gift_card_data["amounts_type"] = value  # default, custom, both
            is_gift_card = True

        # PW Gift Cards
        elif key == "_pw_gift_card_default_amount":
            gift_card_data["default_amount"] = value
            is_gift_card = True
        elif key == "_pw_is_gift_card":
            if value == "yes":
                is_gift_card = True

        # AFGC Gift Cards
        elif key.startswith("afgc_"):
            gift_card_data[key] = value
            is_gift_card = True

    return is_gift_card, gift_card_data


def detect_composite_product(product_data):
    """
    Detect WooCommerce Composite Products.

    Composite products use type 'composite' and store component data
    in _composite_data or _bto_data (legacy) meta fields.

    Args:
        product_data: WooCommerce product data dict

    Returns:
        tuple: (is_composite: bool, composite_details: dict)
    """
    product_type = product_data.get("type", "")
    meta_data = product_data.get("meta_data", [])

    if product_type != "composite":
        return False, {}

    composite_data = {}

    for item in meta_data:
        key = item.get("key", "")
        value = item.get("value")

        if key in ("_composite_data", "_bto_data"):
            if isinstance(value, str):
                import json

                try:
                    value = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    value = []
            composite_data["components"] = value
        elif key == "_composite_layout":
            composite_data["layout"] = value
        elif key == "_composite_add_to_cart_form_location":
            composite_data["form_location"] = value

    return True, composite_data


def detect_booking_product(product_data):
    """
    Detect WooCommerce Bookings and Accommodation Bookings.

    WC types: 'booking' or 'accommodation-booking'.
    Meta fields: _wc_booking_* and _wc_accommodation_booking_*

    Args:
        product_data: WooCommerce product data dict

    Returns:
        tuple: (is_booking: bool, booking_details: dict)
    """
    product_type = product_data.get("type", "")
    meta_data = product_data.get("meta_data", [])

    is_booking = product_type in ("booking", "accommodation-booking")
    if not is_booking:
        return False, {}

    booking_data = {
        "is_accommodation": product_type == "accommodation-booking",
        "original_type": product_type,
    }

    booking_meta = {}
    for item in meta_data:
        key = item.get("key", "")
        value = item.get("value")

        if key.startswith("_wc_booking_") or key.startswith("_wc_accommodation_booking_"):
            booking_meta[key] = value

    booking_data["meta"] = booking_meta

    # Extract key fields for readability
    if "_wc_booking_duration" in booking_meta:
        booking_data["duration"] = booking_meta["_wc_booking_duration"]
        booking_data["duration_type"] = booking_meta.get("_wc_booking_duration_type", "fixed")
        booking_data["duration_unit"] = booking_meta.get("_wc_booking_duration_unit", "hour")

    if "_wc_booking_has_resources" in booking_meta:
        booking_data["has_resources"] = booking_meta["_wc_booking_has_resources"] == "yes"

    if "_wc_booking_has_persons" in booking_meta:
        booking_data["has_persons"] = booking_meta["_wc_booking_has_persons"] == "yes"

    if "_wc_booking_requires_confirmation" in booking_meta:
        booking_data["requires_confirmation"] = (
            booking_meta["_wc_booking_requires_confirmation"] == "yes"
        )

    return True, booking_data


# Registry of transform functions for dynamic lookup
TRANSFORM_FUNCTIONS = {
    "woocommerce_status": transform_woocommerce_status,
    "woocommerce_type": transform_woocommerce_type,
    "woocommerce_order_status": transform_woocommerce_order_status,
    "woocommerce_backorders": transform_woocommerce_backorders,
    "money": transform_money,
    "integer_nullable": transform_integer_nullable,
    "decimal_nullable": transform_decimal_nullable,
    "tax_status_boolean": transform_tax_status_boolean,
    "review_status": transform_review_status,
    "coupon_discount_type": transform_coupon_discount_type,
}


def get_transform_function(transform_type):
    """
    Get transformation function by name.

    Args:
        transform_type: Transform type string

    Returns:
        callable: Transform function or None
    """
    return TRANSFORM_FUNCTIONS.get(transform_type)
