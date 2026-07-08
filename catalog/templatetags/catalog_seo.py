"""
Template tags for catalog SEO optimization
Includes structured data and hreflang tags for multi-location inventory
"""
import json
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from catalog.models import SalesRegion

register = template.Library()


@register.simple_tag(takes_context=True)
def product_structured_data(context, product):
    """
    Generate Schema.org Product structured data with regional offers.

    Includes:
    - Product information
    - Regional pricing and availability
    - Aggregate offers for different regions
    """
    request = context.get('request')

    # Get all active regions
    regions = SalesRegion.objects.filter(is_active=True)

    # Build base product data
    structured_data = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": product.name,
        "description": product.short_description or product.description[:200] if product.description else "",
        "sku": product.sku,
    }

    # Add primary image if available
    if product.images.filter(is_primary=True).exists():
        primary_image = product.images.filter(is_primary=True).first()
        if primary_image and primary_image.media_asset and primary_image.media_asset.image:
            image_url = primary_image.media_asset.image.url
            if request:
                image_url = request.build_absolute_uri(image_url)
            structured_data["image"] = image_url

    # Add brand if available
    if product.brand:
        structured_data["brand"] = {
            "@type": "Brand",
            "name": product.brand.name
        }

    # Add category if available
    if product.category:
        structured_data["category"] = product.category.name

    # Build offers array with regional pricing
    offers = []

    for region in regions:
        # Calculate regional stock
        regional_stock_items = product.stock_items.filter(
            warehouse__region=region,
            warehouse__is_active=True
        )
        total_available = sum(item.available for item in regional_stock_items)

        # Determine availability
        if not product.track_inventory:
            availability = "https://schema.org/InStock"
        elif total_available > 0:
            availability = "https://schema.org/InStock"
        elif product.allow_backorders:
            availability = "https://schema.org/PreOrder"
        else:
            availability = "https://schema.org/OutOfStock"

        # Create offer for this region
        offer = {
            "@type": "Offer",
            "price": str(product.price.amount),
            "priceCurrency": region.default_currency,
            "availability": availability,
            "url": request.build_absolute_uri(product.get_absolute_url()) if request and hasattr(product, 'get_absolute_url') else ""
        }

        # Add eligible region (first country from region)
        if region.countries and len(region.countries) > 0:
            offer["eligibleRegion"] = {
                "@type": "Country",
                "name": region.countries[0]
            }

        offers.append(offer)

    # If there are multiple offers, use AggregateOffer
    if len(offers) > 1:
        structured_data["offers"] = {
            "@type": "AggregateOffer",
            "offers": offers,
            "lowPrice": str(product.price.amount),
            "highPrice": str(product.price.amount),
            "priceCurrency": regions.first().default_currency if regions.exists() else "USD"
        }
    elif len(offers) == 1:
        structured_data["offers"] = offers[0]

    # Add aggregate rating if product has reviews
    if hasattr(product, 'reviews'):
        from django.db.models import Avg, Count
        review_stats = product.reviews.filter(is_approved=True).aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )

        if review_stats['review_count'] and review_stats['review_count'] > 0:
            structured_data["aggregateRating"] = {
                "@type": "AggregateRating",
                "ratingValue": str(round(review_stats['avg_rating'], 1)),
                "reviewCount": str(review_stats['review_count'])
            }

    # Return as JSON-LD script tag
    json_str = json.dumps(structured_data, indent=2, ensure_ascii=False)
    return format_html(
        '<script type="application/ld+json">\n{}\n</script>',
        mark_safe(json_str)
    )


@register.simple_tag(takes_context=True)
def product_hreflang_tags(context, product):
    """
    Generate hreflang tags for regional product variations.

    Helps search engines understand which regional version to show
    to users in different countries.
    """
    request = context.get('request')
    if not request or not hasattr(product, 'get_absolute_url'):
        return ''

    # Get all active regions
    regions = SalesRegion.objects.filter(is_active=True)

    if not regions.exists():
        return ''

    # Build hreflang tags
    tags = []
    product_url = request.build_absolute_uri(product.get_absolute_url())

    # Add tag for each region
    for region in regions:
        if region.countries and len(region.countries) > 0:
            # Use first country code from region
            country_code = region.countries[0].lower()
            # Default language based on country (simplified)
            lang_map = {
                'us': 'en',
                'gb': 'en',
                'ca': 'en',
                'au': 'en',
                'nz': 'en',
                'fr': 'fr',
                'de': 'de',
                'es': 'es',
                'it': 'it',
                'pt': 'pt',
                'br': 'pt',
                'mx': 'es',
                'jp': 'ja',
                'cn': 'zh',
                'kr': 'ko',
            }
            lang = lang_map.get(country_code, 'en')

            # Create hreflang tag
            tags.append(
                format_html(
                    '<link rel="alternate" hreflang="{}-{}" href="{}" />',
                    lang,
                    region.code.lower(),
                    product_url
                )
            )

    # Add x-default for catch-all
    tags.append(
        format_html(
            '<link rel="alternate" hreflang="x-default" href="{}" />',
            product_url
        )
    )

    return mark_safe('\n'.join(str(tag) for tag in tags))


@register.simple_tag
def warehouse_structured_data(warehouse):
    """
    Generate Schema.org LocalBusiness structured data for warehouse/store.

    Used on store locator pages and pickup location displays.
    """
    structured_data = {
        "@context": "https://schema.org",
        "@type": "Store",
        "name": warehouse.name,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": f"{warehouse.address_line1} {warehouse.address_line2}".strip(),
            "addressLocality": warehouse.city,
            "addressRegion": warehouse.state_province,
            "postalCode": warehouse.postal_code,
            "addressCountry": warehouse.country
        }
    }

    # Add coordinates if available
    if warehouse.latitude and warehouse.longitude:
        structured_data["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": str(warehouse.latitude),
            "longitude": str(warehouse.longitude)
        }

    # Add contact info
    if warehouse.contact_phone:
        structured_data["telephone"] = warehouse.contact_phone

    if warehouse.contact_email:
        structured_data["email"] = warehouse.contact_email

    json_str = json.dumps(structured_data, indent=2, ensure_ascii=False)
    return format_html(
        '<script type="application/ld+json">\n{}\n</script>',
        mark_safe(json_str)
    )


@register.simple_tag
def breadcrumb_structured_data(breadcrumbs):
    """
    Generate Schema.org BreadcrumbList structured data.

    Args:
        breadcrumbs: List of dicts with 'name' and 'url' keys

    Example:
        {% breadcrumb_structured_data breadcrumbs %}
    """
    if not breadcrumbs:
        return ''

    structured_data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }

    for i, crumb in enumerate(breadcrumbs, 1):
        structured_data["itemListElement"].append({
            "@type": "ListItem",
            "position": i,
            "name": crumb.get('name', ''),
            "item": crumb.get('url', '')
        })

    json_str = json.dumps(structured_data, indent=2, ensure_ascii=False)
    return format_html(
        '<script type="application/ld+json">\n{}\n</script>',
        mark_safe(json_str)
    )
