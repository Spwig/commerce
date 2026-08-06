"""
Template Tags and Filters for Multi-Currency Support

Provides template tags and filters for displaying and converting prices in different currencies.

Usage in templates:
    {% load currency_tags %}

    {{ product.price|money:request.currency }}
    {{ product.price|convert_currency:request.currency }}
    {% show_price product %}
    {% show_price product show_original=True %}
"""

import logging
from decimal import Decimal

from babel.numbers import format_currency as babel_format_currency
from django import template
from django.utils.html import format_html
from djmoney.money import Money

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def money(value, currency_code=None):
    """
    Format a price as Money object in specified currency.

    Usage:
        {{ product.price|money:request.currency }}
        {{ 19.99|money:"EUR" }}

    Args:
        value: Decimal, float, int, or Money object
        currency_code: Target currency code (optional)

    Returns:
        Formatted money string (e.g., "$19.99", "€19,99")
    """
    if value is None:
        return ""

    try:
        # If value is already Money and no currency specified, just format it
        if isinstance(value, Money):
            if not currency_code:
                return _format_money_display(value.amount, str(value.currency))
            # Convert to different currency
            from exchange_rates.services.exchange_service import ExchangeRateService

            service = ExchangeRateService()
            converted = service.convert(value.amount, str(value.currency), currency_code)
            return _format_money_display(converted, currency_code)

        # If value is Decimal/int/float and currency specified
        if currency_code:
            return _format_money_display(Decimal(str(value)), currency_code)

        # Fallback
        return str(value)

    except Exception as e:
        logger.error(f"Error formatting money: {e}")
        return str(value)


@register.filter
def convert_currency(money_obj, target_currency):
    """
    Convert Money object to different currency.

    Usage:
        {{ product.price|convert_currency:request.currency }}

    Args:
        money_obj: Money object
        target_currency: Target currency code

    Returns:
        Money object in target currency
    """
    if not isinstance(money_obj, Money):
        return money_obj

    if str(money_obj.currency) == target_currency:
        return money_obj

    try:
        from exchange_rates.services.exchange_service import ExchangeRateService

        service = ExchangeRateService()

        converted_amount = service.convert(
            money_obj.amount, str(money_obj.currency), target_currency
        )

        return Money(converted_amount, target_currency)

    except Exception as e:
        logger.error(f"Error converting currency: {e}")
        return money_obj


@register.simple_tag(takes_context=True)
def show_price(context, product, show_original=False, css_class=""):
    """
    Display product price in customer's currency.
    Optionally show original price if converted.

    Usage:
        {% show_price product %}
        {% show_price product show_original=True %}
        {% show_price product show_original=True css_class="product-price" %}

    Args:
        context: Template context
        product: Product object
        show_original: Show original price if currency was converted
        css_class: CSS class to add to price element

    Returns:
        HTML string with formatted price
    """
    request = context.get("request")
    if not request:
        return ""

    currency = getattr(request, "currency", None)
    if not currency:
        from core.models import SiteSettings

        currency = SiteSettings.get_settings().default_currency

    try:
        # Get price in customer's currency
        price = product.get_price_in_currency(currency)

        # Format price
        price_html = _format_money_display(price.amount, currency)

        # Build CSS classes
        classes = ["price"]
        if css_class:
            classes.append(css_class)

        # Show original price if converted and requested
        if show_original and str(product.price.currency) != currency:
            original_html = _format_money_display(product.price.amount, str(product.price.currency))
            return format_html(
                '<span class="{converted_class}">{converted}</span> '
                '<span class="original-price text-muted small">({original})</span>',
                converted_class=" ".join(classes + ["converted-price"]),
                converted=price_html,
                original=original_html,
            )

        return format_html('<span class="{}">{}</span>', " ".join(classes), price_html)

    except Exception as e:
        logger.error(f"Error showing price: {e}")
        return ""


@register.simple_tag(takes_context=True)
def show_sale_price(context, product, show_original=False):
    """
    Display product sale price with strikethrough regular price.

    Usage:
        {% show_sale_price product %}
        {% show_sale_price product show_original=True %}

    Args:
        context: Template context
        product: Product object with price and sale_price
        show_original: Show original currency if converted

    Returns:
        HTML string with formatted price and sale price
    """
    request = context.get("request")
    if not request:
        return ""

    currency = getattr(request, "currency", None)
    if not currency:
        from core.models import SiteSettings

        currency = SiteSettings.get_settings().default_currency

    try:
        # Check if product has sale price
        if not hasattr(product, "sale_price") or not product.sale_price:
            # No sale, just show regular price
            return show_price(context, product, show_original=show_original)

        # Get prices in customer's currency
        regular_price = product.get_price_in_currency(currency)

        # Get sale price - check if it's a fixed price or needs conversion
        if hasattr(product, "get_sale_price_in_currency"):
            sale_price = product.get_sale_price_in_currency(currency)
        else:
            # Fallback: convert sale price
            from exchange_rates.services.exchange_service import ExchangeRateService

            service = ExchangeRateService()
            sale_amount = service.convert(
                product.sale_price.amount, str(product.sale_price.currency), currency
            )
            sale_price = Money(sale_amount, currency)

        # Format prices
        regular_html = _format_money_display(regular_price.amount, currency)
        sale_html = _format_money_display(sale_price.amount, currency)

        return format_html(
            '<span class="price-wrapper">'
            '<span class="price sale-price">{sale}</span> '
            '<span class="price regular-price text-muted"><del>{regular}</del></span>'
            "</span>",
            sale=sale_html,
            regular=regular_html,
        )

    except Exception as e:
        logger.error(f"Error showing sale price: {e}")
        return ""


@register.filter
def format_currency(amount, currency_code):
    """
    Format amount in specified currency using locale-aware formatting.

    Usage:
        {{ 19.99|format_currency:"USD" }}
        {{ total|format_currency:request.currency }}

    Args:
        amount: Decimal or float amount
        currency_code: Currency code (e.g., "USD", "EUR")

    Returns:
        Formatted currency string
    """
    if amount is None:
        return ""

    try:
        return _format_money_display(Decimal(str(amount)), currency_code)
    except Exception as e:
        logger.error(f"Error formatting currency: {e}")
        return str(amount)


@register.filter
def product_price(product, currency_code):
    """
    Return product's effective price formatted in the given currency (plain text).

    Usage:
        {{ product|product_price:current_currency.code }}
    """
    if not currency_code:
        return str(product.effective_price)
    try:
        price = product.get_price_in_currency(currency_code)
        return _format_money_display(price.amount, currency_code)
    except Exception as e:
        logger.error(f"Error in product_price filter: {e}")
        return str(product.effective_price)


@register.filter
def product_price_range(product, currency_code):
    """
    Return a variable product's variant price range formatted in the given
    currency: a single price when all variants match ("$59.99"), or a range
    ("$59.99 – $89.99") otherwise. Non-variable products (or variable products
    with no priced variants) fall back to the single ``product_price``.

    Usage:
        {{ product|product_price_range:current_currency.code }}
    """
    try:
        price_range = product.get_variant_price_range(currency_code)
    except Exception as e:
        logger.error(f"Error in product_price_range filter: {e}")
        price_range = None

    if not price_range:
        return product_price(product, currency_code)

    low, high = price_range
    code = currency_code or str(low.currency)
    low_str = _format_money_display(low.amount, code)
    if low.amount == high.amount:
        return low_str
    return f"{low_str} – {_format_money_display(high.amount, code)}"


@register.filter
def product_compare_price(product, currency_code):
    """
    Return product's regular (non-sale) price formatted in the given currency (plain text).
    Used for strikethrough/compare display when product is on sale.

    Usage:
        {{ product|product_compare_price:current_currency.code }}
    """
    if not currency_code:
        return str(product.price)
    try:
        from exchange_rates.services.exchange_service import ExchangeRateService

        base_price = product.price
        if str(base_price.currency) == currency_code:
            return _format_money_display(base_price.amount, currency_code)
        service = ExchangeRateService()
        converted = service.convert(base_price.amount, str(base_price.currency), currency_code)
        return _format_money_display(Decimal(str(converted)), currency_code)
    except Exception as e:
        logger.error(f"Error in product_compare_price filter: {e}")
        return str(product.price)


@register.inclusion_tag("page_builder/partials/_price_display.html")
def product_price_display(product, currency_code=None, show_badge=True):
    """
    Canonical storefront price block. One place for the price + sale rendering
    logic so every surface stays consistent: effective (sale) price as the
    current price; the regular price struck through + a Sale badge when on sale;
    and, for variable products, the sale-aware variant price range (striking a
    single "was" price only when the range collapses to one value). Fixes both
    the "variable products drop the sale presentation" bug and the multi-currency
    drift from surfaces that used the base-currency ``formatted_price`` property.

    NOTE: after ADDING this tag, a running dev server on this setup (NAS +
    CachedThemeTemplateLoader) must be fully restarted (kill + ``cache.clear()``)
    — the autoreloader will not pick up a newly-registered tag on its own.

    Usage:
        {% product_price_display product current_currency.code %}
        {% product_price_display product current_currency.code show_badge=False %}
    """
    on_sale = bool(getattr(product, "is_on_sale", False))
    is_variable = getattr(product, "product_type", None) == "variable"
    original = None
    if is_variable:
        current = product_price_range(product, currency_code)
        # Sale presentation is valid only when the displayed variant range
        # actually reflects the parent sale — i.e. the variants INHERIT the
        # parent price. A variant with its own price is NOT sale-adjusted by
        # get_effective_price(), so its range is the regular price; showing a
        # Sale badge/strikethrough there would be misleading. (Guarded by
        # is_on_sale so the extra query only runs for on-sale variable products.)
        if on_sale:
            active = list(product.variants.filter(is_active=True))
            inherits = bool(active) and all(v.price is None for v in active)
            if inherits:
                rng = None
                try:
                    rng = product.get_variant_price_range(currency_code)
                except Exception:
                    rng = None
                if (not rng) or (rng[0].amount == rng[1].amount):
                    original = product_compare_price(product, currency_code)
            else:
                on_sale = False
    else:
        current = product_price(product, currency_code)
        if on_sale:
            original = product_compare_price(product, currency_code)
    return {"current": current, "original": original, "on_sale": on_sale, "show_badge": show_badge}


@register.simple_tag
def currency_symbol(currency_code):
    """
    Get currency symbol for a currency code.

    Usage:
        {% currency_symbol "USD" %} -> $
        {% currency_symbol request.currency %}

    Args:
        currency_code: Currency code (e.g., "USD", "EUR")

    Returns:
        Currency symbol string
    """
    from moneyed import CURRENCIES

    try:
        if currency_code in CURRENCIES:
            currency_obj = CURRENCIES[currency_code]
            return getattr(currency_obj, "symbol", currency_code)
        return currency_code
    except Exception as e:
        logger.error(f"Error getting currency symbol: {e}")
        return currency_code


@register.simple_tag
def currency_name(currency_code):
    """
    Get full currency name for a currency code.

    Usage:
        {% currency_name "USD" %} -> US Dollar
        {% currency_name request.currency %}

    Args:
        currency_code: Currency code (e.g., "USD", "EUR")

    Returns:
        Currency name string
    """
    from moneyed import CURRENCIES

    try:
        if currency_code in CURRENCIES:
            return CURRENCIES[currency_code].name
        return currency_code
    except Exception as e:
        logger.error(f"Error getting currency name: {e}")
        return currency_code


@register.simple_tag(takes_context=True)
def get_exchange_rate(context, from_currency, to_currency):
    """
    Get exchange rate between two currencies.

    Usage:
        {% get_exchange_rate "USD" "EUR" %}
        {% get_exchange_rate product.price.currency request.currency %}

    Args:
        context: Template context
        from_currency: Source currency code
        to_currency: Target currency code

    Returns:
        Exchange rate as Decimal, or None if unavailable
    """
    try:
        from exchange_rates.services.exchange_service import ExchangeRateService

        service = ExchangeRateService()
        rate = service.get_rate(from_currency, to_currency)
        return rate
    except Exception as e:
        logger.error(f"Error getting exchange rate: {e}")
        return None


# Helper function for consistent money formatting
def _format_money_display(amount, currency_code, locale=None):
    """
    Format money amount with currency symbol using Babel.

    Args:
        amount: Decimal amount
        currency_code: Currency code (e.g., "USD", "EUR")
        locale: Locale for formatting (default: from settings)

    Returns:
        Formatted money string (e.g., "$19.99", "€19,99")
    """
    from django.utils.translation import get_language

    from core.models import SiteSettings

    try:
        # Get locale from current language or settings
        if not locale:
            locale = get_language() or "en"

        # Get decimal places for currency
        from core.utils.currency_helpers import get_currency_decimal_places

        decimal_places = get_currency_decimal_places(currency_code)

        # Round to appropriate decimal places
        if decimal_places == 0:
            amount = amount.quantize(Decimal("1"))
        elif decimal_places == 3:
            amount = amount.quantize(Decimal("0.001"))
        elif decimal_places == 4:
            amount = amount.quantize(Decimal("0.0001"))
        else:  # default 2 decimal places
            amount = amount.quantize(Decimal("0.01"))

        # Check if locale formatting is enabled
        settings = SiteSettings.get_settings()
        if settings.enable_locale_formatting:
            # Use Babel for locale-aware formatting
            formatted = babel_format_currency(amount, currency_code, locale=locale)
            return formatted
        else:
            # Simple formatting with currency symbol
            from moneyed import CURRENCIES

            if currency_code in CURRENCIES:
                symbol = getattr(CURRENCIES[currency_code], "symbol", currency_code)
                return f"{symbol}{amount:,.{decimal_places}f}"
            else:
                return f"{currency_code} {amount:,.{decimal_places}f}"

    except Exception as e:
        logger.error(f"Error formatting money display: {e}")
        # Fallback to simple formatting
        return f"{currency_code} {amount}"
