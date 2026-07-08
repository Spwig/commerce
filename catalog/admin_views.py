"""
Admin views for catalog app
Handles variation builder and other admin-specific functionality
"""
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction, models
from django.db.models import Max
from django.utils.translation import gettext_lazy as _, gettext
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from itertools import product as itertools_product

from core.utils import get_default_currency
from .models import (
    Product, ProductVariant, ProductVariantImage, ProductAttributeAssignment,
    ProductAttribute, AttributeValue, Warehouse, StockItem, StockMovement,
    ConfigurationSlot, ConfigurationSlotOption, CompatibilityRule, ConfigurationPreset,
    Booking, BookingConfig, BookingResource, BookingResourceImage, BookingPersonType,
    BookingAvailabilityRule, BookingRecurrenceRule,
    ProductReview,
)


@staff_member_required
def variation_builder(request, product_id):
    """
    Display the variation builder interface for generating product variants.
    Modern, user-friendly UI with no JSON fields visible.
    """
    product_obj = get_object_or_404(Product, pk=product_id)

    # Get all attribute assignments for this product
    assignments = product_obj.attribute_assignments.select_related('attribute').prefetch_related('allowed_values').order_by('sort_order')

    # Get all warehouses for stock item creation
    warehouses = Warehouse.objects.filter(is_active=True).order_by('name')

    context = {
        'product': product_obj,
        'assignments': assignments,
        'warehouses': warehouses,
        'has_attributes': assignments.exists(),
    }

    return render(request, 'admin/catalog/variation_builder.html', context)


@staff_member_required
@require_http_methods(["POST"])
def generate_variations(request, product_id):
    """
    Generate product variants based on selected attribute combinations.
    Creates variants with SKU patterns and optional price adjustments.
    """
    product_obj = get_object_or_404(Product, pk=product_id)

    try:
        # Parse form data
        selected_attributes = {}
        for key, values in request.POST.lists():
            if key.startswith('attribute_'):
                attr_id = key.split('_')[1]
                selected_attributes[int(attr_id)] = [int(v) for v in values if v]

        if not selected_attributes:
            messages.error(request, _("Please select at least one attribute value."))
            return redirect('catalog_admin:variation_builder', product_id=product_id)

        # Get configuration options
        sku_pattern = request.POST.get('sku_pattern', '').strip()
        price_strategy = request.POST.get('price_strategy', 'none')
        price_amount = request.POST.get('price_amount', '0')

        # Validate price amount if needed
        try:
            price_adjustment = float(price_amount) if price_amount else 0
        except ValueError:
            price_adjustment = 0

        # Get attribute value objects
        attr_values_map = {}
        for attr_id, value_ids in selected_attributes.items():
            attr_values_map[attr_id] = list(
                AttributeValue.objects.filter(
                    id__in=value_ids,
                    attribute_id=attr_id
                ).select_related('attribute')
            )

        # Generate all combinations
        attribute_ids = sorted(attr_values_map.keys())
        value_lists = [attr_values_map[attr_id] for attr_id in attribute_ids]

        combinations = list(itertools_product(*value_lists))

        if not combinations:
            messages.error(request, _("No combinations to generate."))
            return redirect('catalog_admin:variation_builder', product_id=product_id)

        # Create variants in a transaction
        with transaction.atomic():
            created_count = 0
            skipped_count = 0

            for combination in combinations:
                # Generate SKU
                if sku_pattern:
                    sku = _generate_sku_from_pattern(sku_pattern, combination, product_obj)
                else:
                    # Default SKU pattern
                    value_slugs = '-'.join([av.slug for av in combination])
                    sku = f"{product_obj.sku}-{value_slugs}"

                # Check if variant with these attributes already exists
                existing_variant = _find_existing_variant(product_obj, combination)
                if existing_variant:
                    skipped_count += 1
                    continue

                # Generate variant name
                variant_name = ' / '.join([av.value for av in combination])

                # Calculate price
                variant_price = None
                pricing_strategy = 'inherit'

                if price_strategy == 'fixed_add':
                    variant_price = product_obj.price.amount + price_adjustment
                    pricing_strategy = 'custom'
                elif price_strategy == 'fixed_subtract':
                    variant_price = max(0.01, product_obj.price.amount - price_adjustment)
                    pricing_strategy = 'custom'
                elif price_strategy == 'percentage_add':
                    variant_price = product_obj.price.amount * (1 + price_adjustment / 100)
                    pricing_strategy = 'custom'

                # Create variant
                variant = ProductVariant.objects.create(
                    product=product_obj,
                    name=variant_name,
                    sku=sku,
                    price=variant_price,
                    pricing_strategy=pricing_strategy,
                    is_active=True
                )

                # Assign selected attributes to variant
                variant.selected_attributes.set(combination)

                # Create stock items for all active warehouses
                for warehouse in Warehouse.objects.filter(is_active=True):
                    StockItem.objects.get_or_create(
                        product=product_obj,
                        warehouse=warehouse,
                        variant=variant,
                        defaults={'on_hand': 0, 'allocated': 0}
                    )

                created_count += 1

            # Success message
            if created_count > 0:
                messages.success(
                    request,
                    _(f"Successfully created {created_count} variant(s).")
                )
            if skipped_count > 0:
                messages.info(
                    request,
                    _(f"Skipped {skipped_count} variant(s) that already exist.")
                )

    except Exception as e:
        messages.error(request, _(f"Error generating variations: {str(e)}"))
        return redirect('catalog_admin:variation_builder', product_id=product_id)

    # Redirect back to product change page
    return redirect(f'/en/admin/catalog/product/{product_id}/change/')


def _generate_sku_from_pattern(pattern, combination, product):
    """
    Generate SKU from pattern with placeholders.
    Example: "TSHIRT-{size}-{color}" → "TSHIRT-M-RED"
    """
    sku = pattern

    # Replace {product_sku} placeholder
    sku = sku.replace('{product_sku}', product.sku)
    sku = sku.replace('{sku}', product.sku)

    # Replace attribute placeholders
    for attr_value in combination:
        attr_name = attr_value.attribute.slug.lower()
        attr_value_slug = attr_value.slug.upper()

        sku = sku.replace(f'{{{attr_name}}}', attr_value_slug)

    return sku


def _find_existing_variant(product, combination):
    """
    Check if a variant with this exact attribute combination already exists.
    """
    # Get all variants for this product
    for variant in product.variants.all():
        variant_attrs = set(variant.selected_attributes.values_list('id', flat=True))
        combination_ids = set([av.id for av in combination])

        if variant_attrs == combination_ids:
            return variant

    return None


# ============================================================================
# Digital Products Analytics Dashboard
# ============================================================================

@staff_member_required
def digital_products_analytics_dashboard(request):
    """
    Digital Products Analytics Dashboard
    Shows comprehensive analytics for digital product downloads, license keys, and revenue
    """
    from django.db.models import Count, Sum, Q, Avg, F
    from django.utils import timezone
    from datetime import timedelta
    from catalog.models import DigitalAsset, DigitalDownload, LicenseKey
    from orders.models import OrderItem

    # Calculate date ranges
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    seven_days_ago = now - timedelta(days=7)

    # ========================================================================
    # Overview Statistics
    # ========================================================================

    # Total digital assets
    total_assets = DigitalAsset.objects.filter(is_active=True).count()

    # Total downloads
    total_downloads = DigitalDownload.objects.count()
    completed_downloads = DigitalDownload.objects.filter(status='completed').count()
    failed_downloads = DigitalDownload.objects.filter(status='failed').count()

    # Download success rate
    download_success_rate = (
        (completed_downloads / total_downloads * 100)
        if total_downloads > 0 else 0
    )

    # Total license keys
    total_license_keys = LicenseKey.objects.count()
    active_license_keys = LicenseKey.objects.filter(status='active').count()

    # Recent activity (last 30 days)
    recent_downloads = DigitalDownload.objects.filter(
        downloaded_at__gte=thirty_days_ago
    ).count()
    recent_license_keys = LicenseKey.objects.filter(
        issued_at__gte=thirty_days_ago
    ).count()

    # Revenue from digital products (last 30 days)
    digital_revenue = OrderItem.objects.filter(
        product__is_digital=True,
        order__status__in=['processing', 'completed', 'delivered'],
        order__created_at__gte=thirty_days_ago
    ).aggregate(
        total=Sum('line_total')
    )['total'] or 0

    # ========================================================================
    # Download Trends (Last 30 Days)
    # ========================================================================

    download_trends = []
    for i in range(30, -1, -1):
        date = now - timedelta(days=i)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date_start + timedelta(days=1)

        downloads_count = DigitalDownload.objects.filter(
            downloaded_at__gte=date_start,
            downloaded_at__lt=date_end
        ).count()

        download_trends.append({
            'date': date_start.strftime('%Y-%m-%d'),
            'count': downloads_count
        })

    # ========================================================================
    # Top Downloaded Products
    # ========================================================================

    top_products = DigitalAsset.objects.annotate(
        download_count=Count('downloads')
    ).filter(
        download_count__gt=0
    ).select_related('product').order_by('-download_count')[:10]

    # ========================================================================
    # License Key Statistics by Status
    # ========================================================================

    license_stats = {
        'active': LicenseKey.objects.filter(status='active').count(),
        'expired': LicenseKey.objects.filter(status='expired').count(),
        'revoked': LicenseKey.objects.filter(status='revoked').count(),
        'suspended': LicenseKey.objects.filter(status='suspended').count(),
    }

    # ========================================================================
    # Download Status Distribution
    # ========================================================================

    download_stats = {
        'completed': DigitalDownload.objects.filter(status='completed').count(),
        'failed': DigitalDownload.objects.filter(status='failed').count(),
        'in_progress': DigitalDownload.objects.filter(status='in_progress').count(),
        'pending': DigitalDownload.objects.filter(status='pending').count(),
    }

    # ========================================================================
    # Recent Download Activity
    # ========================================================================

    recent_download_activity = DigitalDownload.objects.select_related(
        'digital_asset', 'digital_asset__product', 'user', 'order_item__order'
    ).order_by('-downloaded_at')[:20]

    # ========================================================================
    # Failed Downloads Analysis
    # ========================================================================

    failed_downloads_by_asset = DigitalDownload.objects.filter(
        status='failed'
    ).values(
        'digital_asset__filename',
        'digital_asset__product__name',
        'digital_asset_id'
    ).annotate(
        failed_count=Count('id')
    ).order_by('-failed_count')[:10]

    # ========================================================================
    # License Key Activation Metrics
    # ========================================================================

    # Total device activations
    total_activations = sum(
        lic.current_activations for lic in LicenseKey.objects.all()
    )

    # Average activations per license
    avg_activations = LicenseKey.objects.aggregate(
        avg=Avg('current_activations')
    )['avg'] or 0

    # Licenses at capacity (100% activated)
    licenses_at_capacity = LicenseKey.objects.filter(
        max_activations__isnull=False,
        current_activations__gte=F('max_activations')
    ).count()

    # ========================================================================
    # Weekly Comparison
    # ========================================================================

    this_week_downloads = DigitalDownload.objects.filter(
        downloaded_at__gte=seven_days_ago
    ).count()

    last_week_start = seven_days_ago - timedelta(days=7)
    last_week_downloads = DigitalDownload.objects.filter(
        downloaded_at__gte=last_week_start,
        downloaded_at__lt=seven_days_ago
    ).count()

    download_growth = (
        ((this_week_downloads - last_week_downloads) / last_week_downloads * 100)
        if last_week_downloads > 0 else 0
    )

    # ========================================================================
    # Prepare Context
    # ========================================================================

    context = {
        'title': 'Digital Products Analytics',
        'has_permission': True,
        'site_title': 'Digital Products Analytics',
        'site_header': 'Digital Products Analytics',

        # Overview stats
        'total_assets': total_assets,
        'total_downloads': total_downloads,
        'completed_downloads': completed_downloads,
        'failed_downloads': failed_downloads,
        'download_success_rate': round(download_success_rate, 1),
        'total_license_keys': total_license_keys,
        'active_license_keys': active_license_keys,
        'recent_downloads': recent_downloads,
        'recent_license_keys': recent_license_keys,
        'digital_revenue': digital_revenue,

        # Charts data
        'download_trends': download_trends,
        'top_products': top_products,
        'license_stats': license_stats,
        'download_stats': download_stats,

        # Tables
        'recent_download_activity': recent_download_activity,
        'failed_downloads_by_asset': failed_downloads_by_asset,

        # License metrics
        'total_activations': total_activations,
        'avg_activations': round(avg_activations, 1),
        'licenses_at_capacity': licenses_at_capacity,

        # Growth metrics
        'this_week_downloads': this_week_downloads,
        'last_week_downloads': last_week_downloads,
        'download_growth': round(download_growth, 1),
    }

    return render(request, 'admin/catalog/digital_products_analytics.html', context)


# ============================================================================
# Quick Add Attribute (AJAX Endpoint)
# ============================================================================

@staff_member_required
@require_POST
def quick_add_attribute(request):
    """
    AJAX endpoint for quickly creating an attribute and its values.

    Expected POST data (JSON):
    {
        "attribute_name": "Color",
        "attribute_type": "color",
        "values": ["Red", "Blue", "Green"],
        "product_id": 123  # Optional - if provided, auto-assign to product
    }

    Returns:
    {
        "success": true,
        "attribute": {"id": 1, "name": "Color", "type": "color"},
        "values": [
            {"id": 1, "value": "Red", "slug": "red"},
            {"id": 2, "value": "Blue", "slug": "blue"}
        ]
    }
    """
    try:
        # Parse JSON request body
        data = json.loads(request.body)

        attribute_name = data.get('attribute_name', '').strip()
        attribute_type = data.get('attribute_type', 'text')
        values_list = data.get('values', [])
        product_id = data.get('product_id')

        # Validation
        errors = []
        if not attribute_name:
            errors.append(gettext('Attribute name is required'))
        if not values_list or len(values_list) == 0:
            errors.append(gettext('At least one value is required'))

        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)

        # Get or create attribute - if it exists, we'll add values to it
        attribute_slug = slugify(attribute_name)

        # Create attribute and values in a transaction
        with transaction.atomic():
            # Use get_or_create to support adding values to existing attributes
            attribute, attribute_created = ProductAttribute.objects.get_or_create(
                slug=attribute_slug,
                defaults={
                    'name': attribute_name,
                    'type': attribute_type
                }
            )

            # Get the highest existing sort_order for this attribute's values
            existing_max_order = AttributeValue.objects.filter(
                attribute=attribute
            ).aggregate(max_order=Max('sort_order'))['max_order'] or 0

            # Create values - track which were created vs skipped (already exist)
            created_values = []
            skipped_values = []

            for idx, value_name in enumerate(values_list):
                value_name = value_name.strip()
                if not value_name:
                    continue

                value_slug = slugify(value_name)
                if not value_slug:
                    continue

                # Check if this value already exists for this attribute
                existing_value = AttributeValue.objects.filter(
                    attribute=attribute,
                    slug=value_slug
                ).first()

                if existing_value:
                    # Value already exists - track it as skipped
                    skipped_values.append(value_name)
                else:
                    # Create new value with incrementing sort order
                    value = AttributeValue.objects.create(
                        attribute=attribute,
                        value=value_name,
                        slug=value_slug,
                        sort_order=existing_max_order + ((idx + 1) * 10)
                    )
                    created_values.append(value)

            # If product_id provided, auto-assign to product
            if product_id:
                try:
                    product = Product.objects.get(pk=product_id)
                    assignment, _ = ProductAttributeAssignment.objects.get_or_create(
                        product=product,
                        attribute=attribute,
                        defaults={'sort_order': 0}
                    )

                    # Add new values to allowed_values (keep existing ones)
                    if created_values:
                        assignment.allowed_values.add(*created_values)

                except Product.DoesNotExist:
                    # Product not found - still return success since attribute was created/updated
                    pass

        # Get all values for this attribute (for populating the filter_horizontal widget)
        all_attribute_values = AttributeValue.objects.filter(
            attribute=attribute
        ).order_by('sort_order', 'value')

        # Return success response with information about what was created vs skipped
        return JsonResponse({
            'success': True,
            'attribute_created': attribute_created,
            'attribute': {
                'id': attribute.id,
                'name': attribute.name,
                'slug': attribute.slug,
                'type': attribute.type
            },
            'created_values': [
                {
                    'id': v.id,
                    'value': v.value,
                    'slug': v.slug
                } for v in created_values
            ],
            'all_values': [
                {
                    'id': v.id,
                    'value': v.value,
                    'slug': v.slug
                } for v in all_attribute_values
            ],
            'skipped_values': skipped_values
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'errors': [gettext('Invalid JSON data')]
        }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': [str(e)]
        }, status=500)


# =============================================================================
# License Provider Product Mapping Views
# =============================================================================

@staff_member_required
@require_http_methods(["GET"])
def get_product_mappings(request, provider_id):
    """
    Get current product mappings for a license provider.
    Returns the mapping data along with product details.
    """
    from .models import LicenseProvider

    try:
        provider = get_object_or_404(LicenseProvider, pk=provider_id)
        mappings = provider.product_mapping or {}

        # Enrich mapping data with product details
        enriched_mappings = []
        for product_id_str, external_id in mappings.items():
            try:
                product_id = int(product_id_str)
                product = Product.objects.get(pk=product_id)
                enriched_mappings.append({
                    'product_id': product_id,
                    'product_name': product.name,
                    'product_sku': product.sku or '',
                    'external_id': external_id,
                })
            except (ValueError, Product.DoesNotExist):
                # Product might have been deleted - still include mapping
                enriched_mappings.append({
                    'product_id': product_id_str,
                    'product_name': f'[Deleted Product #{product_id_str}]',
                    'product_sku': '',
                    'external_id': external_id,
                })

        return JsonResponse({
            'success': True,
            'mappings': enriched_mappings,
            'provider_name': provider.name,
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["POST"])
def save_product_mapping(request, provider_id):
    """
    Save a product mapping for a license provider.
    Adds or updates a single product-to-external-ID mapping.
    """
    from .models import LicenseProvider

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        external_id = data.get('external_id', '').strip()

        if not product_id:
            return JsonResponse({
                'success': False,
                'error': gettext('Product ID is required')
            }, status=400)

        provider = get_object_or_404(LicenseProvider, pk=provider_id)

        # Verify product exists and is digital
        product = get_object_or_404(Product, pk=product_id)
        if not product.is_digital:
            return JsonResponse({
                'success': False,
                'error': gettext('Only digital products can be mapped to license providers')
            }, status=400)

        # Update the mapping
        if provider.product_mapping is None:
            provider.product_mapping = {}

        product_id_str = str(product_id)

        if external_id:
            # Add/update mapping
            provider.product_mapping[product_id_str] = external_id
        else:
            # Remove mapping if external_id is empty
            provider.product_mapping.pop(product_id_str, None)

        provider.save(update_fields=['product_mapping'])

        return JsonResponse({
            'success': True,
            'message': gettext('Product mapping saved successfully'),
            'product_name': product.name,
            'external_id': external_id,
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': gettext('Invalid JSON data')
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["POST"])
def delete_product_mapping(request, provider_id):
    """
    Delete a product mapping from a license provider.
    """
    from .models import LicenseProvider

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if not product_id:
            return JsonResponse({
                'success': False,
                'error': gettext('Product ID is required')
            }, status=400)

        provider = get_object_or_404(LicenseProvider, pk=provider_id)

        # Remove the mapping
        product_id_str = str(product_id)
        if provider.product_mapping and product_id_str in provider.product_mapping:
            del provider.product_mapping[product_id_str]
            provider.save(update_fields=['product_mapping'])

        return JsonResponse({
            'success': True,
            'message': gettext('Product mapping removed successfully'),
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': gettext('Invalid JSON data')
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@staff_member_required
@require_http_methods(["GET"])
def search_digital_products(request):
    """
    Search for digital products to map to a license provider.
    Returns products that are digital and not already mapped.
    """
    try:
        query = request.GET.get('q', '').strip()
        provider_id = request.GET.get('provider_id')
        limit = int(request.GET.get('limit', 20))

        # Get digital products
        products = Product.objects.filter(is_digital=True, is_active=True)

        if query:
            products = products.filter(
                models.Q(name__icontains=query) |
                models.Q(sku__icontains=query)
            )

        # Optionally exclude already mapped products
        if provider_id:
            from .models import LicenseProvider
            try:
                provider = LicenseProvider.objects.get(pk=provider_id)
                if provider.product_mapping:
                    mapped_ids = [int(pid) for pid in provider.product_mapping.keys()]
                    products = products.exclude(pk__in=mapped_ids)
            except (LicenseProvider.DoesNotExist, ValueError):
                pass

        products = products.order_by('name')[:limit]

        results = [
            {
                'id': p.id,
                'name': p.name,
                'sku': p.sku or '',
                'thumbnail': p.thumbnail.url if p.thumbnail else '',
            }
            for p in products
        ]

        return JsonResponse({
            'success': True,
            'products': results,
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# =============================================================================
# License Template Preview (AJAX Endpoint)
# =============================================================================

@staff_member_required
@require_http_methods(["GET"])
def get_license_template_preview(request, template_id):
    """
    Get preview information for a license key template.
    Returns the pattern and sample generated keys.
    """
    from .models import LicenseKeyTemplate

    try:
        template = get_object_or_404(LicenseKeyTemplate, pk=template_id)

        # Generate sample keys
        samples = []
        for _ in range(3):
            try:
                sample_key = template.generate_sample_key()
                samples.append(sample_key)
            except Exception as e:
                # If key generation fails, show placeholder
                samples.append(f"[Error: {str(e)}]")

        # Build display pattern
        display_pattern = template.pattern
        if template.prefix:
            display_pattern = f"{template.prefix}{display_pattern}"
        if template.suffix:
            display_pattern = f"{display_pattern}{template.suffix}"

        return JsonResponse({
            'success': True,
            'pattern': template.pattern,
            'display_pattern': display_pattern,
            'prefix': template.prefix or '',
            'suffix': template.suffix or '',
            'samples': samples,
            'name': template.name,
            'description': template.description or '',
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ============================================================================
# Bundle Item Variant Lookup
# ============================================================================

@staff_member_required
@require_http_methods(["GET"])
def get_product_variants(request, product_id):
    """
    Get all variants for a given product plus product details.
    Used by bundle item inline to filter variant dropdown and display product card.
    """
    try:
        product = get_object_or_404(Product, pk=product_id)

        # Get product thumbnail
        thumbnail_url = None
        first_image = product.images.first()
        if first_image:
            thumbnail_url = first_image.thumbnail_small

        # Get product price
        price_display = str(product.price) if product.price else None

        # Build product info
        product_info = {
            'id': product.id,
            'name': product.name,
            'sku': product.sku,
            'price': price_display,
            'price_amount': float(product.price.amount) if product.price else 0,
            'currency': str(product.price.currency) if product.price else get_default_currency(),
            'thumbnail': thumbnail_url,
            'product_type': product.product_type,
            'status': product.status,
        }

        # Only variable products have variants
        variants = []
        if product.product_type == 'variable':
            for v in product.variants.filter(is_active=True).order_by('name'):
                variant_price = v.price if v.price else product.price
                variants.append({
                    'id': v.id,
                    'name': v.name,
                    'sku': v.sku,
                    'display': f"{v.name} ({v.sku})" if v.sku else v.name,
                    'price': str(variant_price) if variant_price else None,
                    'price_amount': float(variant_price.amount) if variant_price else 0,
                })

        return JsonResponse({
            'success': True,
            'product': product_info,
            'variants': variants,
            'has_variants': len(variants) > 0,
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# =============================================================================
# Bundle Component Product Autocomplete
# =============================================================================

@staff_member_required
@require_http_methods(["GET"])
def autocomplete_component_products(request):
    """
    Autocomplete endpoint for bundle component products.
    Filters out bundle products - only returns simple and variable products.
    Compatible with Django admin's select2 autocomplete format.
    """
    term = request.GET.get('term', '')
    page = int(request.GET.get('page', 1))
    page_size = 20

    # Filter out product types that cannot be bundle components
    queryset = Product.objects.exclude(
        product_type__in=['bundle', 'configurable', 'gift_card']
    ).filter(
        status='published'
    )

    if term:
        queryset = queryset.filter(
            models.Q(name__icontains=term) | models.Q(sku__icontains=term)
        )

    # Order by name
    queryset = queryset.order_by('name')

    # Paginate
    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    products = queryset[start:end]

    results = []
    for product in products:
        # Format: "Product Name (SKU)" or just "Product Name"
        text = product.name
        if product.sku:
            text = f"{product.name} ({product.sku})"

        results.append({
            'id': product.id,
            'text': text,
        })

    return JsonResponse({
        'results': results,
        'pagination': {
            'more': end < total
        }
    })


# =============================================================================
# Product Variant AJAX Deletion
# =============================================================================

@staff_member_required
@require_http_methods(["POST"])
def delete_product_variant(request, variant_id):
    """
    AJAX endpoint to delete a product variant.
    Returns JSON response with success status.
    """
    try:
        variant = get_object_or_404(ProductVariant, pk=variant_id)

        # Store info for response before deletion
        variant_name = variant.name
        product_id = variant.product_id

        # Check if user has permission to delete (they should be staff at minimum)
        # Additional permission checks could be added here

        # Delete the variant (this will cascade delete related stock items)
        variant.delete()

        return JsonResponse({
            'success': True,
            'message': gettext('Variant "%(name)s" has been deleted.') % {'name': variant_name},
            'variant_id': variant_id,
            'product_id': product_id,
        })

    except ProductVariant.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': gettext('Variant not found.')
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# =============================================================================
# Product Variant Cards AJAX Endpoints
# =============================================================================

def _build_variant_card_data(variant, product=None):
    """Build the summary data for a single variant card/row."""
    if product is None:
        product = variant.product

    # Get primary image thumbnail
    thumbnail_url = None
    primary_image = variant.images.filter(is_primary=True).select_related('media_asset').first()
    if not primary_image:
        primary_image = variant.images.select_related('media_asset').first()
    if primary_image and primary_image.media_asset:
        thumbnail_url = primary_image.thumbnail_small

    # Get effective price
    price = variant.get_effective_price()
    price_display = str(price) if price else None

    # Get stock totals
    total_stock = variant.total_stock
    available_stock = variant.available_stock
    stock_status = variant.stock_status

    # Get color hex from color-type attribute
    color_hex = None
    color_attrs = variant.selected_attributes.filter(
        attribute__type='color'
    ).first()
    if color_attrs and color_attrs.color_hex:
        color_hex = color_attrs.color_hex

    # Build attributes display
    attr_dict = variant.get_attribute_dict()
    attributes_display = ' \u2022 '.join(f"{k}: {v}" for k, v in attr_dict.items()) if attr_dict else ''

    # Build attribute pills data
    attribute_pills = []
    for attr_val in variant.selected_attributes.select_related('attribute').order_by('attribute__sort_order'):
        attribute_pills.append({
            'attribute_name': attr_val.attribute.name,
            'value': attr_val.value,
            'color_hex': attr_val.color_hex if attr_val.attribute.type == 'color' else None,
        })

    return {
        'id': variant.id,
        'name': variant.name,
        'sku': variant.sku or '',
        'is_active': variant.is_active,
        'price_display': price_display,
        'pricing_strategy': variant.pricing_strategy,
        'total_stock': total_stock,
        'available_stock': available_stock,
        'stock_status': stock_status,
        'thumbnail_url': thumbnail_url,
        'color_hex': color_hex,
        'attributes_display': attributes_display,
        'attribute_pills': attribute_pills,
    }


@staff_member_required
def list_variants(request, product_id):
    """Return JSON array of variant summary data for the card grid."""
    product = get_object_or_404(Product, pk=product_id)

    variants = product.variants.prefetch_related(
        'selected_attributes__attribute',
        'images__media_asset',
        'stock_items__warehouse',
    ).order_by('name')

    data = [_build_variant_card_data(v, product) for v in variants]

    return JsonResponse({
        'success': True,
        'variants': data,
        'count': len(data),
    })


@staff_member_required
def variant_form_context(request, product_id):
    """Return form context for the variant edit/create modal."""
    product = get_object_or_404(Product, pk=product_id)

    # Get assigned attributes with their allowed values
    assignments = product.attribute_assignments.select_related(
        'attribute'
    ).prefetch_related(
        'allowed_values'
    ).order_by('sort_order')

    attributes = []
    for assignment in assignments:
        attr = assignment.attribute
        values = []
        for val in assignment.allowed_values.order_by('sort_order', 'value'):
            values.append({
                'id': val.id,
                'value': val.value,
                'slug': val.slug,
                'color_hex': val.color_hex or '',
            })
        attributes.append({
            'id': attr.id,
            'name': attr.name,
            'slug': attr.slug,
            'type': attr.type,
            'is_required': attr.is_required,
            'values': values,
        })

    # Get active warehouses
    warehouses = []
    for wh in Warehouse.objects.filter(is_active=True).order_by('name'):
        warehouses.append({
            'id': wh.id,
            'name': wh.name,
            'code': wh.code,
        })

    # Get shipping packages
    from shipping.models import ShippingPackage
    packages = []
    for pkg in ShippingPackage.objects.filter(is_active=True).order_by('name'):
        packages.append({
            'id': pkg.id,
            'name': pkg.name,
        })

    # Product defaults for inheritance display
    product_defaults = {
        'price': str(product.price) if product.price else None,
        'weight': str(product.weight) if product.weight else None,
        'length': str(product.length) if product.length else None,
        'width': str(product.width) if product.width else None,
        'height': str(product.height) if product.height else None,
    }

    from core.models import SiteSettings
    site_settings = SiteSettings.get_settings()

    return JsonResponse({
        'success': True,
        'attributes': attributes,
        'warehouses': warehouses,
        'shipping_packages': packages,
        'product_defaults': product_defaults,
        'default_currency': site_settings.default_currency,
    })


@staff_member_required
def variant_detail(request, variant_id):
    """Return full variant data for the edit modal."""
    variant = get_object_or_404(
        ProductVariant.objects.select_related('product', 'preferred_shipping_package')
        .prefetch_related(
            'selected_attributes__attribute',
            'images__media_asset',
            'stock_items__warehouse',
        ),
        pk=variant_id
    )

    # Selected attributes
    selected_attrs = []
    for val in variant.selected_attributes.select_related('attribute').order_by('attribute__sort_order'):
        selected_attrs.append({
            'id': val.id,
            'attribute_id': val.attribute.id,
            'attribute_name': val.attribute.name,
            'attribute_type': val.attribute.type,
            'value': val.value,
            'color_hex': val.color_hex or '',
        })

    # Stock items per warehouse
    stock_items = []
    for si in variant.stock_items.select_related('warehouse').order_by('warehouse__name'):
        stock_items.append({
            'stock_item_id': si.id,
            'warehouse_id': si.warehouse.id,
            'warehouse_name': si.warehouse.name,
            'warehouse_code': si.warehouse.code,
            'on_hand': si.on_hand,
            'allocated': si.allocated,
            'available': si.available,
            'low_stock_threshold': si.low_stock_threshold,
        })

    # Images
    images = []
    for img in variant.images.select_related('media_asset').order_by('position', 'id'):
        images.append({
            'id': img.id,
            'media_asset_id': img.media_asset.id,
            'thumbnail_url': img.thumbnail_small,
            'image_url': img.image_url,
            'alt_text': img.alt_text or '',
            'is_primary': img.is_primary,
            'show_in_gallery': img.show_in_gallery,
            'show_in_listing': img.show_in_listing,
            'position': img.position,
        })

    # Price
    price_amount = None
    price_currency = None
    if variant.price:
        price_amount = float(variant.price.amount)
        price_currency = str(variant.price.currency)

    data = {
        'id': variant.id,
        'name': variant.name,
        'sku': variant.sku or '',
        'is_active': variant.is_active,
        'pricing_strategy': variant.pricing_strategy,
        'price_amount': price_amount,
        'price_currency': price_currency,
        'weight': str(variant.weight) if variant.weight else '',
        'length': str(variant.length) if variant.length else '',
        'width': str(variant.width) if variant.width else '',
        'height': str(variant.height) if variant.height else '',
        'barcode': variant.barcode or '',
        'preferred_shipping_package_id': variant.preferred_shipping_package_id,
        'selected_attributes': selected_attrs,
        'stock_items': stock_items,
        'images': images,
    }

    return JsonResponse({'success': True, 'variant': data})


@staff_member_required
@require_http_methods(["POST"])
def create_variant(request, product_id):
    """Create a new variant via AJAX and return its card data."""
    product = get_object_or_404(Product, pk=product_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    name = data.get('name', '').strip()
    sku = data.get('sku', '').strip()

    if not name:
        return JsonResponse({'success': False, 'error': gettext('Variant name is required.')}, status=400)
    if not sku:
        return JsonResponse({'success': False, 'error': gettext('SKU is required.')}, status=400)

    # Check SKU uniqueness
    if ProductVariant.objects.filter(sku=sku).exists():
        return JsonResponse({'success': False, 'error': gettext('SKU "%(sku)s" already exists.') % {'sku': sku}}, status=400)

    try:
        with transaction.atomic():
            variant = ProductVariant.objects.create(
                product=product,
                name=name,
                sku=sku,
                is_active=data.get('is_active', True),
                pricing_strategy=data.get('pricing_strategy', 'inherit'),
                barcode=data.get('barcode', ''),
            )

            # Set price if custom pricing
            if data.get('pricing_strategy') == 'custom' and data.get('price_amount') is not None:
                from djmoney.money import Money
                currency = data.get('price_currency', get_default_currency())
                variant.price = Money(data['price_amount'], currency)
                variant.save(update_fields=['price', 'price_currency'])

            # Set physical attributes
            for field in ('weight', 'length', 'width', 'height'):
                val = data.get(field)
                if val is not None and val != '':
                    try:
                        setattr(variant, field, val)
                    except (ValueError, TypeError):
                        pass
            variant.save()

            # Set shipping package
            pkg_id = data.get('preferred_shipping_package_id')
            if pkg_id:
                variant.preferred_shipping_package_id = pkg_id
                variant.save(update_fields=['preferred_shipping_package'])

            # Set selected attributes
            attr_value_ids = data.get('selected_attribute_ids', [])
            if attr_value_ids:
                variant.selected_attributes.set(attr_value_ids)

            # Create stock items for all active warehouses
            warehouses = Warehouse.objects.filter(is_active=True)
            for warehouse in warehouses:
                StockItem.objects.get_or_create(
                    product=product,
                    variant=variant,
                    warehouse=warehouse,
                    defaults={'on_hand': 0, 'allocated': 0, 'low_stock_threshold': 0}
                )

        # Refetch for card data
        variant = ProductVariant.objects.prefetch_related(
            'selected_attributes__attribute',
            'images__media_asset',
            'stock_items__warehouse',
        ).get(pk=variant.pk)

        card_data = _build_variant_card_data(variant, product)

        return JsonResponse({
            'success': True,
            'variant': card_data,
            'message': gettext('Variant "%(name)s" created successfully.') % {'name': name},
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def update_variant(request, variant_id):
    """Update an existing variant via AJAX."""
    variant = get_object_or_404(ProductVariant, pk=variant_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    try:
        with transaction.atomic():
            # Update basic fields
            if 'name' in data:
                variant.name = data['name'].strip()
            if 'sku' in data:
                new_sku = data['sku'].strip()
                # Check uniqueness excluding self
                if ProductVariant.objects.filter(sku=new_sku).exclude(pk=variant.pk).exists():
                    return JsonResponse({'success': False, 'error': gettext('SKU "%(sku)s" already exists.') % {'sku': new_sku}}, status=400)
                variant.sku = new_sku
            if 'is_active' in data:
                variant.is_active = data['is_active']
            if 'pricing_strategy' in data:
                variant.pricing_strategy = data['pricing_strategy']
            if 'barcode' in data:
                variant.barcode = data['barcode']

            # Price
            if data.get('pricing_strategy') == 'custom' and data.get('price_amount') is not None:
                from djmoney.money import Money
                currency = data.get('price_currency', get_default_currency())
                variant.price = Money(data['price_amount'], currency)
            elif data.get('pricing_strategy') == 'inherit':
                variant.price = None

            # Physical attributes
            for field in ('weight', 'length', 'width', 'height'):
                if field in data:
                    val = data[field]
                    if val is not None and val != '':
                        try:
                            setattr(variant, field, val)
                        except (ValueError, TypeError):
                            pass
                    else:
                        setattr(variant, field, None)

            # Shipping package
            if 'preferred_shipping_package_id' in data:
                variant.preferred_shipping_package_id = data['preferred_shipping_package_id'] or None

            variant.save()

            # Update selected attributes
            if 'selected_attribute_ids' in data:
                variant.selected_attributes.set(data['selected_attribute_ids'])

        # Refetch for card data
        variant = ProductVariant.objects.prefetch_related(
            'selected_attributes__attribute',
            'images__media_asset',
            'stock_items__warehouse',
        ).get(pk=variant.pk)

        card_data = _build_variant_card_data(variant)

        return JsonResponse({
            'success': True,
            'variant': card_data,
            'message': gettext('Variant "%(name)s" updated successfully.') % {'name': variant.name},
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def update_variant_stock(request, variant_id):
    """Update stock items for a variant via AJAX."""
    variant = get_object_or_404(ProductVariant, pk=variant_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    stock_updates = data.get('stock_items', [])

    try:
        with transaction.atomic():
            for item_data in stock_updates:
                stock_item_id = item_data.get('stock_item_id')
                if not stock_item_id:
                    continue

                try:
                    stock_item = StockItem.objects.get(pk=stock_item_id, variant=variant)
                except StockItem.DoesNotExist:
                    continue

                updated = False

                # Update on_hand
                if 'on_hand' in item_data:
                    new_on_hand = int(item_data['on_hand'])
                    if stock_item.on_hand != new_on_hand:
                        old_on_hand = stock_item.on_hand
                        stock_item.on_hand = new_on_hand
                        updated = True

                        # Create stock movement audit record
                        StockMovement.objects.create(
                            stock_item=stock_item,
                            movement_type='adjustment',
                            quantity=new_on_hand - old_on_hand,
                            previous_quantity=old_on_hand,
                            new_quantity=new_on_hand,
                            reason=f'Stock adjusted for variant via product admin by {request.user.username}'
                        )

                # Update low_stock_threshold
                if 'low_stock_threshold' in item_data:
                    new_threshold = int(item_data['low_stock_threshold'])
                    if stock_item.low_stock_threshold != new_threshold:
                        stock_item.low_stock_threshold = new_threshold
                        updated = True

                if updated:
                    stock_item.save()

        return JsonResponse({
            'success': True,
            'message': gettext('Stock updated successfully.'),
        })

    except (ValueError, TypeError) as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def update_variant_images(request, variant_id):
    """Update images for a variant via AJAX."""
    variant = get_object_or_404(ProductVariant, pk=variant_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    images_data = data.get('images', [])

    try:
        with transaction.atomic():
            from media_library.models import MediaAsset

            existing_image_ids = set(variant.images.values_list('id', flat=True))
            updated_image_ids = set()

            for image_data in images_data:
                image_id = image_data.get('id')
                media_asset_id = image_data.get('media_asset_id')

                if not media_asset_id:
                    continue

                if image_id and not str(image_id).startswith('new_'):
                    # Update existing image
                    try:
                        variant_image = ProductVariantImage.objects.get(id=image_id, variant=variant)
                        variant_image.media_asset_id = media_asset_id
                        variant_image.alt_text = image_data.get('alt_text', '')
                        variant_image.show_in_gallery = image_data.get('show_in_gallery', True)
                        variant_image.show_in_listing = image_data.get('show_in_listing', True)
                        variant_image.is_primary = image_data.get('is_primary', False)
                        variant_image.position = image_data.get('position', 0)
                        variant_image.save()
                        updated_image_ids.add(variant_image.id)
                    except ProductVariantImage.DoesNotExist:
                        image_id = None

                if not image_id or str(image_id).startswith('new_'):
                    # Create new image
                    try:
                        media_asset = MediaAsset.objects.get(id=media_asset_id)
                        variant_image = ProductVariantImage.objects.create(
                            variant=variant,
                            media_asset=media_asset,
                            alt_text=image_data.get('alt_text', ''),
                            show_in_gallery=image_data.get('show_in_gallery', True),
                            show_in_listing=image_data.get('show_in_listing', True),
                            is_primary=image_data.get('is_primary', False),
                            position=image_data.get('position', 0),
                        )
                        updated_image_ids.add(variant_image.id)
                    except MediaAsset.DoesNotExist:
                        continue

            # Delete images that were removed
            images_to_delete = existing_image_ids - updated_image_ids
            if images_to_delete:
                ProductVariantImage.objects.filter(id__in=images_to_delete).delete()

        # Return updated images list
        images = []
        for img in variant.images.select_related('media_asset').order_by('position', 'id'):
            images.append({
                'id': img.id,
                'media_asset_id': img.media_asset.id,
                'thumbnail_url': img.thumbnail_small,
                'image_url': img.image_url,
                'alt_text': img.alt_text or '',
                'is_primary': img.is_primary,
                'show_in_gallery': img.show_in_gallery,
                'show_in_listing': img.show_in_listing,
                'position': img.position,
            })

        return JsonResponse({
            'success': True,
            'images': images,
            'message': gettext('Images updated successfully.'),
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@staff_member_required
@require_http_methods(["POST"])
def update_attribute_color(request, value_id):
    """Update the color_hex of an AttributeValue via AJAX."""
    attr_value = get_object_or_404(AttributeValue, pk=value_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    color_hex = data.get('color_hex', '').strip()

    # Basic validation
    if color_hex and not (color_hex.startswith('#') and len(color_hex) == 7):
        return JsonResponse({'success': False, 'error': gettext('Invalid color hex format. Use #RRGGBB.')}, status=400)

    attr_value.color_hex = color_hex
    attr_value.save(update_fields=['color_hex'])

    return JsonResponse({
        'success': True,
        'color_hex': color_hex,
        'message': gettext('Color updated.'),
    })


@staff_member_required
def filter_gift_cards(request):
    """
    AJAX endpoint for filtering gift cards in the admin change list.
    Returns rendered HTML and count for the gift card cards.
    """
    from django.template.loader import render_to_string
    from django.db.models import Q
    from django.utils import timezone
    from datetime import timedelta
    from .models import GiftCard

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    balance = request.GET.get('balance', '')
    date_filter = request.GET.get('date', '')

    queryset = GiftCard.objects.select_related('product', 'order_item__order').all()

    # Search filter
    if search:
        queryset = queryset.filter(
            Q(code__icontains=search) |
            Q(recipient_email__icontains=search) |
            Q(recipient_name__icontains=search) |
            Q(sender_name__icontains=search)
        )

    # Status filter
    now = timezone.now()
    if status == 'active':
        queryset = queryset.filter(is_active=True)
    elif status == 'inactive':
        queryset = queryset.filter(is_active=False)
    elif status == 'expired':
        queryset = queryset.filter(expires_at__lt=now, is_active=True)
    elif status == 'fully_redeemed':
        queryset = queryset.filter(current_balance__amount=0, is_active=True)
    elif status == 'partially_used':
        queryset = queryset.filter(
            first_used_at__isnull=False,
            current_balance__amount__gt=0,
            is_active=True
        )

    # Balance filter
    if balance == 'has_balance':
        queryset = queryset.filter(current_balance__amount__gt=0)
    elif balance == 'zero_balance':
        queryset = queryset.filter(current_balance__amount=0)

    # Date filter
    if date_filter == 'today':
        queryset = queryset.filter(created_at__date=now.date())
    elif date_filter == 'week':
        week_ago = now - timedelta(days=7)
        queryset = queryset.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = now - timedelta(days=30)
        queryset = queryset.filter(created_at__gte=month_ago)
    elif date_filter == 'year':
        year_ago = now - timedelta(days=365)
        queryset = queryset.filter(created_at__gte=year_ago)

    # Order by most recent first
    queryset = queryset.order_by('-created_at')

    html = render_to_string(
        'admin/catalog/giftcard/partials/gift_card_cards.html',
        {'gift_cards': queryset, 'request': request}
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count()
    })


@staff_member_required
def filter_gift_card_transactions(request):
    """
    AJAX endpoint for filtering gift card transactions in the admin change list.
    Returns rendered HTML and count for the transaction cards.
    """
    from django.template.loader import render_to_string
    from django.db.models import Q
    from django.utils import timezone
    from datetime import timedelta
    from .models import GiftCardTransaction

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    search = request.GET.get('search', '')
    transaction_type = request.GET.get('type', '')
    direction = request.GET.get('direction', '')
    date_filter = request.GET.get('date', '')

    queryset = GiftCardTransaction.objects.select_related(
        'gift_card', 'order', 'created_by'
    ).all()

    # Search filter
    if search:
        queryset = queryset.filter(
            Q(gift_card__code__icontains=search) |
            Q(notes__icontains=search)
        )

    # Transaction type filter
    if transaction_type:
        queryset = queryset.filter(transaction_type=transaction_type)

    # Amount direction filter
    if direction == 'positive':
        queryset = queryset.filter(amount__gte=0)
    elif direction == 'negative':
        queryset = queryset.filter(amount__lt=0)

    # Date filter
    now = timezone.now()
    if date_filter == 'today':
        queryset = queryset.filter(created_at__date=now.date())
    elif date_filter == 'week':
        week_ago = now - timedelta(days=7)
        queryset = queryset.filter(created_at__gte=week_ago)
    elif date_filter == 'month':
        month_ago = now - timedelta(days=30)
        queryset = queryset.filter(created_at__gte=month_ago)
    elif date_filter == 'year':
        year_ago = now - timedelta(days=365)
        queryset = queryset.filter(created_at__gte=year_ago)

    # Order by most recent first
    queryset = queryset.order_by('-created_at')

    html = render_to_string(
        'admin/catalog/giftcardtransaction/partials/transaction_cards.html',
        {'transactions': queryset, 'request': request}
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count()
    })


# ============================================================================
# PRODUCT CONFIGURATOR MANAGEMENT VIEWS
# ============================================================================


@staff_member_required
def slot_options_manager(request, slot_id):
    """
    Management view for configuring options within a configuration slot.
    Renders a card-based UI for adding/removing products as slot options.
    """
    from django.template.loader import render_to_string

    slot = get_object_or_404(
        ConfigurationSlot.objects.select_related('product'),
        pk=slot_id
    )
    product_obj = slot.product

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add_option':
            product_id = request.POST.get('product_id')
            variant_id = request.POST.get('variant_id') or None
            if product_id:
                option_product = get_object_or_404(Product, pk=product_id)
                option_variant = None
                if variant_id:
                    option_variant = get_object_or_404(ProductVariant, pk=variant_id, product=option_product)

                _, created = ConfigurationSlotOption.objects.get_or_create(
                    slot=slot,
                    option_product=option_product,
                    option_variant=option_variant,
                    defaults={
                        'sort_order': slot.options.count(),
                    }
                )
                if created:
                    messages.success(request, _('Added {} to slot.').format(option_product.name))
                else:
                    messages.info(request, _('Product already in this slot.'))
            return redirect('catalog_admin:slot_options_manager', slot_id=slot.pk)

        elif action == 'remove_option':
            option_id = request.POST.get('option_id')
            if option_id:
                ConfigurationSlotOption.objects.filter(pk=option_id, slot=slot).delete()
                messages.success(request, _('Option removed from slot.'))
            return redirect('catalog_admin:slot_options_manager', slot_id=slot.pk)

        elif action == 'update_option':
            option_id = request.POST.get('option_id')
            if option_id:
                try:
                    option = ConfigurationSlotOption.objects.get(pk=option_id, slot=slot)
                    option.is_default = request.POST.get('is_default') == 'on'
                    option.is_popular = request.POST.get('is_popular') == 'on'
                    option.sort_order = int(request.POST.get('sort_order', 0))
                    option.quantity = int(request.POST.get('quantity', 1))

                    # Compatibility tags
                    tags_str = request.POST.get('compatibility_tags', '')
                    if tags_str:
                        option.compatibility_tags = [t.strip() for t in tags_str.split(',') if t.strip()]
                    else:
                        option.compatibility_tags = []

                    # Price adjustment
                    price_adj = request.POST.get('price_adjustment', '0')
                    try:
                        from decimal import Decimal as D
                        option.price_adjustment = D(price_adj)
                    except Exception:
                        pass

                    option.save()
                    messages.success(request, _('Option updated.'))
                except ConfigurationSlotOption.DoesNotExist:
                    messages.error(request, _('Option not found.'))
            return redirect('catalog_admin:slot_options_manager', slot_id=slot.pk)

    # GET: render the management page
    options = slot.options.select_related(
        'option_product', 'option_variant'
    ).order_by('sort_order', 'pk')

    context = {
        'slot': slot,
        'product': product_obj,
        'options': options,
        'title': _('Manage Options: {} - {}').format(product_obj.name, slot.name),
        'site_title': 'Spwig',
    }
    return render(request, 'admin/catalog/configurator/slot_options.html', context)


@staff_member_required
def slot_options_search_products(request, slot_id):
    """AJAX endpoint: search products to add to a slot."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    from django.template.loader import render_to_string

    slot = get_object_or_404(ConfigurationSlot, pk=slot_id)
    search = request.GET.get('search', '').strip()

    # Get IDs of products already in this slot
    existing_ids = slot.options.values_list('option_product_id', flat=True)

    products = Product.objects.filter(
        status='published'
    ).exclude(
        pk=slot.product_id  # Don't allow self-reference
    ).exclude(
        product_type='configurable'  # Don't nest configurables
    ).exclude(
        pk__in=existing_ids
    )

    if search:
        products = products.filter(
            models.Q(name__icontains=search) |
            models.Q(sku__icontains=search)
        )

    products = products[:20]

    html = render_to_string(
        'admin/catalog/configurator/partials/product_search_results.html',
        {'products': products, 'slot': slot, 'request': request}
    )

    return JsonResponse({'html': html, 'count': len(products)})


@staff_member_required
def compatibility_matrix_manager(request, product_id):
    """
    Management view for the compatibility matrix.
    Allows merchants to define which options are compatible across slots.
    """
    product_obj = get_object_or_404(
        Product.objects.prefetch_related(
            'configuration_slots__options__option_product',
            'compatibility_rules__source_option',
            'compatibility_rules__target_slot',
            'compatibility_rules__compatible_options',
        ),
        pk=product_id,
        product_type='configurable'
    )

    slots = product_obj.configuration_slots.all().order_by('sort_order')
    rules = product_obj.compatibility_rules.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'save_rule':
            source_option_id = request.POST.get('source_option_id')
            target_slot_id = request.POST.get('target_slot_id')
            rule_type = request.POST.get('rule_type', 'requires')
            compatible_ids = request.POST.getlist('compatible_options')

            if source_option_id and target_slot_id:
                source_option = get_object_or_404(ConfigurationSlotOption, pk=source_option_id)
                target_slot = get_object_or_404(ConfigurationSlot, pk=target_slot_id)

                # Get or create the rule
                rule, created = CompatibilityRule.objects.get_or_create(
                    configurable_product=product_obj,
                    source_option=source_option,
                    target_slot=target_slot,
                    defaults={'rule_type': rule_type}
                )
                if not created:
                    rule.rule_type = rule_type
                    rule.save()

                # Set compatible options
                rule.compatible_options.set(compatible_ids)
                messages.success(request, _('Compatibility rule saved.'))

            return redirect('catalog_admin:compatibility_matrix', product_id=product_obj.pk)

        elif action == 'delete_rule':
            rule_id = request.POST.get('rule_id')
            if rule_id:
                CompatibilityRule.objects.filter(
                    pk=rule_id, configurable_product=product_obj
                ).delete()
                messages.success(request, _('Rule deleted.'))
            return redirect('catalog_admin:compatibility_matrix', product_id=product_obj.pk)

        elif action == 'generate_from_tags':
            # Auto-generate requires rules from matching compatibility tags
            created_count = _generate_rules_from_tags(product_obj)
            if created_count > 0:
                messages.success(request, _('Generated {} compatibility rule(s) from tags.').format(created_count))
            else:
                messages.info(request, _('No new rules generated. Ensure options have matching compatibility tags across different slots.'))
            return redirect('catalog_admin:compatibility_matrix', product_id=product_obj.pk)

    # Build a structured view of rules for the template
    rules_by_source = {}
    for rule in rules:
        key = rule.source_option_id
        if key not in rules_by_source:
            rules_by_source[key] = []
        rules_by_source[key].append({
            'rule': rule,
            'target_slot': rule.target_slot,
            'compatible_option_ids': set(rule.compatible_options.values_list('id', flat=True)),
        })

    context = {
        'product': product_obj,
        'slots': slots,
        'rules': rules,
        'rules_by_source': rules_by_source,
        'title': _('Compatibility Matrix: {}').format(product_obj.name),
        'site_title': 'Spwig',
    }
    return render(request, 'admin/catalog/configurator/compatibility_matrix.html', context)


@staff_member_required
def compatibility_rule_api(request, product_id):
    """AJAX endpoint: get/save compatibility rules for a source option."""
    product_obj = get_object_or_404(Product, pk=product_id, product_type='configurable')

    if request.method == 'GET':
        source_option_id = request.GET.get('source_option_id')
        target_slot_id = request.GET.get('target_slot_id')

        if source_option_id and target_slot_id:
            try:
                rule = CompatibilityRule.objects.get(
                    configurable_product=product_obj,
                    source_option_id=source_option_id,
                    target_slot_id=target_slot_id,
                )
                return JsonResponse({
                    'exists': True,
                    'rule_id': rule.pk,
                    'rule_type': rule.rule_type,
                    'compatible_option_ids': list(
                        rule.compatible_options.values_list('id', flat=True)
                    ),
                })
            except CompatibilityRule.DoesNotExist:
                return JsonResponse({'exists': False})

        return JsonResponse({'error': 'Missing parameters'}, status=400)

    elif request.method == 'POST':
        data = json.loads(request.body)
        source_option_id = data.get('source_option_id')
        target_slot_id = data.get('target_slot_id')
        rule_type = data.get('rule_type', 'requires')
        compatible_ids = data.get('compatible_option_ids', [])

        if not source_option_id or not target_slot_id:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        rule, _ = CompatibilityRule.objects.update_or_create(
            configurable_product=product_obj,
            source_option_id=source_option_id,
            target_slot_id=target_slot_id,
            defaults={'rule_type': rule_type}
        )
        rule.compatible_options.set(compatible_ids)

        return JsonResponse({
            'success': True,
            'rule_id': rule.pk,
            'compatible_count': len(compatible_ids),
        })

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def _generate_rules_from_tags(product):
    """
    Auto-generate compatibility rules from matching tags across slots.
    For each unique tag, options in different slots that share the tag
    are made compatible with each other via 'requires' rules.
    """
    slots = product.configuration_slots.prefetch_related('options').all()
    created_count = 0

    # Build tag → [(slot_id, option)] mapping
    tag_map = {}
    for slot in slots:
        for option in slot.options.all():
            for tag in option.compatibility_tags:
                if tag not in tag_map:
                    tag_map[tag] = []
                tag_map[tag].append((slot.pk, option))

    # For each tag, create rules between options in different slots
    for tag, options_list in tag_map.items():
        # Group by slot
        by_slot = {}
        for slot_id, option in options_list:
            by_slot.setdefault(slot_id, []).append(option)

        # Only useful if the tag spans multiple slots
        if len(by_slot) < 2:
            continue

        slot_ids = list(by_slot.keys())
        for source_slot_id in slot_ids:
            for target_slot_id in slot_ids:
                if source_slot_id == target_slot_id:
                    continue

                target_slot = ConfigurationSlot.objects.get(pk=target_slot_id)
                compatible_in_target = by_slot[target_slot_id]

                for source_option in by_slot[source_slot_id]:
                    rule, created = CompatibilityRule.objects.get_or_create(
                        configurable_product=product,
                        source_option=source_option,
                        target_slot=target_slot,
                        defaults={'rule_type': 'requires'}
                    )
                    # Add compatible options (merge, don't replace)
                    for target_option in compatible_in_target:
                        rule.compatible_options.add(target_option)
                    if created:
                        created_count += 1

    return created_count


# ============================================================================
# Configuration Slot AJAX CRUD
# ============================================================================

@staff_member_required
def list_slots(request, product_id):
    """AJAX: List all configuration slots for a product."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    product_obj = get_object_or_404(Product, pk=product_id, product_type='configurable')
    include_options = request.GET.get('include_options') == '1'
    slots = ConfigurationSlot.objects.filter(
        product=product_obj
    ).annotate(
        option_count=models.Count('options')
    ).order_by('sort_order', 'pk')

    if include_options:
        slots = slots.prefetch_related('options__option_product')

    lang = request.LANGUAGE_CODE or 'en'
    slots_data = []
    for slot in slots:
        slot_dict = {
            'id': slot.pk,
            'name': str(slot.name),
            'slug': slot.slug,
            'description': str(slot.description) if slot.description else '',
            'icon': slot.icon or 'fas fa-puzzle-piece',
            'is_required': slot.is_required,
            'min_selections': slot.min_selections,
            'max_selections': slot.max_selections,
            'sort_order': slot.sort_order,
            'option_count': slot.option_count,
            'options_url': f'/{lang}/admin/catalog/slot/{slot.pk}/options/',
        }
        if include_options:
            options = []
            for opt in slot.options.order_by('sort_order'):
                options.append({
                    'id': opt.pk,
                    'name': str(opt.option_product.name),
                    'variant_name': opt.option_variant.name if opt.option_variant else None,
                })
            slot_dict['options'] = options
        slots_data.append(slot_dict)

    return JsonResponse({'success': True, 'slots': slots_data, 'count': len(slots_data)})


@staff_member_required
@require_POST
def create_slot(request, product_id):
    """AJAX: Create a new configuration slot."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    product_obj = get_object_or_404(Product, pk=product_id, product_type='configurable')
    data = json.loads(request.body)

    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False, 'error': gettext('Name is required.')}, status=400)

    slug = data.get('slug', '').strip() or slugify(name)
    # Ensure unique slug
    base_slug = slug
    counter = 1
    while ConfigurationSlot.objects.filter(product=product_obj, slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    max_order = ConfigurationSlot.objects.filter(product=product_obj).aggregate(
        m=Max('sort_order')
    )['m'] or 0

    slot = ConfigurationSlot.objects.create(
        product=product_obj,
        name=name,
        slug=slug,
        description=data.get('description', ''),
        icon=data.get('icon', ''),
        is_required=data.get('is_required', True),
        min_selections=int(data.get('min_selections', 1)),
        max_selections=int(data.get('max_selections', 1)),
        sort_order=int(data.get('sort_order', max_order + 1)),
    )

    return JsonResponse({
        'success': True,
        'slot': {
            'id': slot.pk,
            'name': str(slot.name),
            'slug': slot.slug,
        }
    })


@staff_member_required
def slot_detail(request, slot_id):
    """AJAX: Get full slot data for edit modal."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    slot = get_object_or_404(ConfigurationSlot, pk=slot_id)

    return JsonResponse({
        'success': True,
        'slot': {
            'id': slot.pk,
            'name': str(slot.name),
            'slug': slot.slug,
            'description': str(slot.description) if slot.description else '',
            'icon': slot.icon or '',
            'is_required': slot.is_required,
            'min_selections': slot.min_selections,
            'max_selections': slot.max_selections,
            'sort_order': slot.sort_order,
        }
    })


@staff_member_required
@require_POST
def update_slot(request, slot_id):
    """AJAX: Update a configuration slot."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    slot = get_object_or_404(ConfigurationSlot, pk=slot_id)
    data = json.loads(request.body)

    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False, 'error': gettext('Name is required.')}, status=400)

    slot.name = name
    if 'slug' in data and data['slug'].strip():
        new_slug = data['slug'].strip()
        if ConfigurationSlot.objects.filter(
            product=slot.product, slug=new_slug
        ).exclude(pk=slot.pk).exists():
            return JsonResponse({'success': False, 'error': gettext('Slug already exists.')}, status=400)
        slot.slug = new_slug

    slot.description = data.get('description', slot.description)
    slot.icon = data.get('icon', slot.icon)
    slot.is_required = data.get('is_required', slot.is_required)
    slot.min_selections = int(data.get('min_selections', slot.min_selections))
    slot.max_selections = int(data.get('max_selections', slot.max_selections))
    slot.sort_order = int(data.get('sort_order', slot.sort_order))
    slot.save()

    return JsonResponse({'success': True})


@staff_member_required
@require_POST
def delete_slot(request, slot_id):
    """AJAX: Delete a configuration slot."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    slot = get_object_or_404(ConfigurationSlot, pk=slot_id)
    slot.delete()

    return JsonResponse({'success': True})


# ============================================================================
# Configuration Preset AJAX CRUD
# ============================================================================

@staff_member_required
def list_presets(request, product_id):
    """AJAX: List all configuration presets for a product."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    product_obj = get_object_or_404(Product, pk=product_id, product_type='configurable')
    presets = ConfigurationPreset.objects.filter(
        product=product_obj
    ).order_by('sort_order', 'pk')

    presets_data = []
    for preset in presets:
        # Count selections
        selection_count = sum(len(opts) for opts in preset.selections.values()) if preset.selections else 0

        # Image URL
        image_url = None
        if preset.image_asset:
            try:
                image_url = preset.image_asset.thumbnail_small
            except Exception:
                pass

        presets_data.append({
            'id': preset.pk,
            'name': str(preset.name),
            'slug': preset.slug,
            'description': str(preset.description) if preset.description else '',
            'is_featured': preset.is_featured,
            'sort_order': preset.sort_order,
            'selection_count': selection_count,
            'image_url': image_url,
        })

    return JsonResponse({'success': True, 'presets': presets_data, 'count': len(presets_data)})


@staff_member_required
@require_POST
def create_preset(request, product_id):
    """AJAX: Create a new configuration preset."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    product_obj = get_object_or_404(Product, pk=product_id, product_type='configurable')
    data = json.loads(request.body)

    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False, 'error': gettext('Name is required.')}, status=400)

    slug = data.get('slug', '').strip() or slugify(name)
    base_slug = slug
    counter = 1
    while ConfigurationPreset.objects.filter(product=product_obj, slug=slug).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1

    max_order = ConfigurationPreset.objects.filter(product=product_obj).aggregate(
        m=Max('sort_order')
    )['m'] or 0

    preset = ConfigurationPreset.objects.create(
        product=product_obj,
        name=name,
        slug=slug,
        description=data.get('description', ''),
        is_featured=data.get('is_featured', False),
        sort_order=int(data.get('sort_order', max_order + 1)),
        selections=data.get('selections', {}),
    )

    return JsonResponse({
        'success': True,
        'preset': {
            'id': preset.pk,
            'name': str(preset.name),
            'slug': preset.slug,
        }
    })


@staff_member_required
def preset_detail(request, preset_id):
    """AJAX: Get full preset data for edit modal."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    preset = get_object_or_404(ConfigurationPreset, pk=preset_id)

    # Also return available slots and options for the selection UI
    slots_with_options = []
    slots = ConfigurationSlot.objects.filter(
        product=preset.product
    ).prefetch_related('options__option_product').order_by('sort_order')

    for slot in slots:
        options = []
        for opt in slot.options.order_by('sort_order'):
            options.append({
                'id': opt.pk,
                'name': str(opt.option_product.name),
                'variant_name': opt.option_variant.name if opt.option_variant else None,
            })
        slots_with_options.append({
            'id': slot.pk,
            'name': str(slot.name),
            'icon': slot.icon or 'fas fa-puzzle-piece',
            'is_required': slot.is_required,
            'max_selections': slot.max_selections,
            'options': options,
        })

    return JsonResponse({
        'success': True,
        'preset': {
            'id': preset.pk,
            'name': str(preset.name),
            'slug': preset.slug,
            'description': str(preset.description) if preset.description else '',
            'is_featured': preset.is_featured,
            'sort_order': preset.sort_order,
            'selections': preset.selections or {},
        },
        'slots': slots_with_options,
    })


@staff_member_required
@require_POST
def update_preset(request, preset_id):
    """AJAX: Update a configuration preset."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    preset = get_object_or_404(ConfigurationPreset, pk=preset_id)
    data = json.loads(request.body)

    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'success': False, 'error': gettext('Name is required.')}, status=400)

    preset.name = name
    if 'slug' in data and data['slug'].strip():
        new_slug = data['slug'].strip()
        if ConfigurationPreset.objects.filter(
            product=preset.product, slug=new_slug
        ).exclude(pk=preset.pk).exists():
            return JsonResponse({'success': False, 'error': gettext('Slug already exists.')}, status=400)
        preset.slug = new_slug

    preset.description = data.get('description', preset.description)
    preset.is_featured = data.get('is_featured', preset.is_featured)
    preset.sort_order = int(data.get('sort_order', preset.sort_order))
    if 'selections' in data:
        preset.selections = data['selections']
    preset.save()

    return JsonResponse({'success': True})


@staff_member_required
@require_POST
def delete_preset(request, preset_id):
    """AJAX: Delete a configuration preset."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    preset = get_object_or_404(ConfigurationPreset, pk=preset_id)
    preset.delete()

    return JsonResponse({'success': True})


@staff_member_required
@require_GET
def filter_stock_items(request):
    """AJAX endpoint for filtering stock items with aggregated statistics."""
    from django.template.loader import render_to_string
    from django.db.models import Q, F, Sum
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    warehouse_id = request.GET.get('warehouse', '').strip()
    stock_status = request.GET.get('stock_status', '').strip()

    # Build queryset
    queryset = StockItem.objects.select_related(
        'product', 'warehouse', 'variant'
    ).all()

    if search:
        queryset = queryset.filter(
            Q(product__name__icontains=search) |
            Q(product__sku__icontains=search) |
            Q(warehouse__name__icontains=search) |
            Q(warehouse__code__icontains=search)
        )

    if warehouse_id:
        queryset = queryset.filter(warehouse_id=warehouse_id)

    if stock_status == 'low':
        queryset = queryset.filter(on_hand__lte=F('low_stock_threshold'))
    elif stock_status == 'adequate':
        queryset = queryset.filter(on_hand__gt=F('low_stock_threshold'))
    elif stock_status == 'out':
        queryset = queryset.filter(on_hand__lte=F('allocated'))
    elif stock_status == 'allocated':
        queryset = queryset.filter(allocated__gt=0)

    # Calculate statistics
    total_items = queryset.count()
    total_on_hand = queryset.aggregate(Sum('on_hand'))['on_hand__sum'] or 0
    total_allocated = queryset.aggregate(Sum('allocated'))['allocated__sum'] or 0
    total_available = total_on_hand - total_allocated

    low_stock_count = queryset.filter(on_hand__lte=F('low_stock_threshold')).count()
    out_of_stock_count = queryset.filter(on_hand__lte=F('allocated')).count()

    # Render results
    html = render_to_string(
        'admin/catalog/stockitem/partials/stockitem_cards.html',
        {'stock_items': queryset},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': total_items,
        'stats': {
            'total_items': total_items,
            'total_on_hand': total_on_hand,
            'total_allocated': total_allocated,
            'total_available': total_available,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
        }
    })


@staff_member_required
@require_GET
def filter_warehouses(request):
    """AJAX endpoint for filtering warehouses."""
    from django.template.loader import render_to_string
    from django.db.models import Q, Count
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    region_id = request.GET.get('region', '').strip()
    country = request.GET.get('country', '').strip()
    
    # Get current tab status from URL
    is_active = request.GET.get('is_active', '').strip()
    is_retail = request.GET.get('is_retail', '').strip()

    # Build queryset with annotations
    queryset = Warehouse.objects.select_related('region').annotate(
        stock_count=Count('stock_items')
    )

    # Apply tab filters (from URL)
    if is_active == '1':
        queryset = queryset.filter(is_active=True)
    elif is_active == '0':
        queryset = queryset.filter(is_active=False)
    
    if is_retail == '1':
        queryset = queryset.filter(is_retail_location=True)

    # Apply AJAX filters
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(city__icontains=search) |
            Q(address_line1__icontains=search)
        )

    if region_id:
        queryset = queryset.filter(region_id=region_id)

    if country:
        queryset = queryset.filter(country=country)

    # Order by priority
    queryset = queryset.order_by('-fulfillment_priority', 'name')

    # Render results
    html = render_to_string(
        'admin/catalog/warehouse/partials/warehouse_cards.html',
        {'warehouses': queryset},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count()
    })


@staff_member_required
@require_GET
def filter_sales_regions(request):
    """AJAX endpoint for filtering sales regions."""
    from django.template.loader import render_to_string
    from django.db.models import Q, Count
    
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # Extract filters
    search = request.GET.get('search', '').strip()
    currency = request.GET.get('currency', '').strip()
    
    # Get current tab status from URL
    is_active = request.GET.get('is_active', '').strip()

    # Build queryset
    queryset = SalesRegion.objects.all()

    # Apply tab filters (from URL)
    if is_active == '1':
        queryset = queryset.filter(is_active=True)
    elif is_active == '0':
        queryset = queryset.filter(is_active=False)

    # Apply AJAX filters
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )

    if currency:
        queryset = queryset.filter(default_currency=currency)

    # Order by priority
    queryset = queryset.order_by('-priority', 'name')

    # Render results
    html = render_to_string(
        'admin/catalog/salesregion/partials/salesregion_cards.html',
        {'regions': queryset},
        request=request
    )

    return JsonResponse({
        'html': html,
        'count': queryset.count()
    })

# ============================================================================
# Product Recycle Bin View
# ============================================================================

@staff_member_required
def product_recycle_bin(request):
    """View for product recycle bin - manage soft-deleted products"""
    from catalog.models import Product
    from django.contrib import messages, admin
    from django.db import models
    from django.core.exceptions import ValidationError

    if request.method == 'POST':
        action = request.POST.get('action')
        product_ids = request.POST.getlist('product_ids')

        if action == 'restore':
            products = Product.all_objects.filter(id__in=product_ids, is_deleted=True)
            count = 0
            errors = []

            for product in products:
                try:
                    product.restore()
                    count += 1
                except ValidationError as e:
                    errors.append(f'{product.name}: {str(e)}')

            if count:
                messages.success(request, f'Restored {count} product(s)')
            if errors:
                messages.error(request, 'Some products could not be restored: ' + '; '.join(errors))

        elif action == 'permanent_delete':
            products = Product.all_objects.filter(id__in=product_ids, is_deleted=True)

            # Check for PROTECT constraints
            errors = []
            count = 0

            for product in products:
                try:
                    product.hard_delete()
                    count += 1
                except models.ProtectedError as e:
                    errors.append(f'{product.name} (has orders)')

            if count:
                messages.success(request, f'Permanently deleted {count} product(s)')
            if errors:
                messages.error(request, 'Some products have orders and cannot be permanently deleted: ' + ', '.join(errors))

        elif action == 'empty_bin':
            deleted_products = Product.all_objects.filter(is_deleted=True)
            errors = []
            count = 0

            for product in deleted_products:
                try:
                    product.hard_delete()
                    count += 1
                except models.ProtectedError:
                    errors.append(product.name)

            if count:
                messages.success(request, f'Recycle bin emptied ({count} products permanently deleted)')
            if errors:
                messages.warning(
                    request,
                    f'{len(errors)} products with orders were skipped: {", ".join(errors[:5])}'
                )

    # Get deleted products with related data
    deleted_products = Product.all_objects.filter(is_deleted=True).select_related(
        'category', 'brand', 'deleted_by'
    ).order_by('-deleted_at')

    # Check if products have orders (PROTECT constraint)
    from orders.models import OrderItem
    for product in deleted_products:
        product.has_orders = OrderItem.objects.filter(product=product).exists()

    context = {
        'deleted_products': deleted_products,
        'title': _('Product Recycle Bin'),
        'has_permission': True,
        'site_header': admin.site.site_header,
        'site_title': admin.site.site_title,
        'opts': Product._meta,
    }

    return render(request, 'admin/catalog/product/recycle_bin.html', context)


@staff_member_required
@require_GET
def booking_calendar_api(request):
    """
    AJAX endpoint for booking calendar data.
    Returns JSON booking data for a given month/year.
    Used by the calendar view in the Booking admin change_list.
    """
    import calendar as cal_module
    from django.utils import timezone as tz

    year = int(request.GET.get('year', tz.now().year))
    month = int(request.GET.get('month', tz.now().month))

    first_day = tz.datetime(year, month, 1, tzinfo=tz.utc)
    _, last_day_num = cal_module.monthrange(year, month)
    last_day = tz.datetime(year, month, last_day_num, 23, 59, 59, tzinfo=tz.utc)

    bookings = Booking.objects.filter(
        start_datetime__gte=first_day,
        start_datetime__lte=last_day,
    ).select_related('product', 'resource')

    # Apply filters
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)

    product_id = request.GET.get('product_id')
    if product_id:
        bookings = bookings.filter(product_id=product_id)

    status_colors = {
        'pending_confirmation': '#f59e0b',
        'confirmed': '#16a34a',
        'cancelled': '#dc2626',
        'completed': '#2563eb',
        'no_show': '#6b7280',
    }
    events = []
    for b in bookings:
        events.append({
            'id': b.pk,
            'title': f"{b.product.name}" + (f" - {b.resource.name}" if b.resource else ''),
            'start': b.start_datetime.isoformat(),
            'end': b.end_datetime.isoformat(),
            'status': b.status,
            'color': status_colors.get(b.status, '#777'),
            'customer': b.customer_name or b.customer_email,
            'url': f'../../booking/{b.pk}/change/',
        })

    return JsonResponse({
        'events': events,
        'year': year,
        'month': month,
    })


@staff_member_required
@require_GET
def filter_bookings(request):
    """AJAX filter endpoint for Booking list view cards."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    from django.template.loader import render_to_string
    from django.db.models import Q

    queryset = Booking.objects.select_related(
        'product', 'resource', 'customer'
    ).all()

    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(customer_name__icontains=search) |
            Q(customer_email__icontains=search) |
            Q(customer_phone__icontains=search) |
            Q(product__name__icontains=search) |
            Q(resource__name__icontains=search)
        )

    status = request.GET.get('status', '').strip()
    if status:
        queryset = queryset.filter(status=status)

    product_id = request.GET.get('product', '').strip()
    if product_id:
        queryset = queryset.filter(product_id=product_id)

    total_count = queryset.count()
    bookings = queryset.order_by('-start_datetime')[:100]

    html = render_to_string(
        'admin/catalog/booking/partials/booking_cards.html',
        {'bookings': bookings},
        request=request
    )

    return JsonResponse({'html': html, 'count': total_count})


# ============================================================================
# Booking AJAX CRUD Views
# ============================================================================

def _check_booking_ajax(request, product_id=None):
    """Validate AJAX request and return product if product_id given."""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return None, JsonResponse({'error': 'Invalid request'}, status=400)
    if product_id:
        product_obj = get_object_or_404(Product, pk=product_id, product_type='booking')
        return product_obj, None
    return True, None


def _serialize_time(t):
    """Serialize a time field to HH:MM string."""
    return t.strftime('%H:%M') if t else ''


def _serialize_date(d):
    """Serialize a date field to YYYY-MM-DD string."""
    return d.isoformat() if d else ''


def _serialize_booking_config(config):
    """Serialize BookingConfig to dict."""
    return {
        'id': config.pk,
        'booking_type': config.booking_type,
        'duration_type': config.duration_type,
        'duration': config.duration,
        'duration_unit': config.duration_unit,
        'min_duration': config.min_duration,
        'max_duration': config.max_duration,
        'buffer_before': config.buffer_before,
        'buffer_after': config.buffer_after,
        'min_advance': config.min_advance,
        'min_advance_unit': config.min_advance_unit,
        'max_advance': config.max_advance,
        'max_advance_unit': config.max_advance_unit,
        'max_bookings_per_slot': config.max_bookings_per_slot,
        'confirmation_required': config.confirmation_required,
        'cancellation_allowed': config.cancellation_allowed,
        'cancellation_deadline': config.cancellation_deadline,
        'cancellation_deadline_unit': config.cancellation_deadline_unit,
        'calendar_display': config.calendar_display,
        'customer_timezone_enabled': config.customer_timezone_enabled,
        'deposit_enabled': config.deposit_enabled,
        'deposit_type': config.deposit_type,
        'deposit_amount': str(config.deposit_amount),
        'check_in_time': _serialize_time(config.check_in_time),
        'check_out_time': _serialize_time(config.check_out_time),
        'recurrence_enabled': config.recurrence_enabled,
        'reminder_enabled': config.reminder_enabled,
        'reminder_hours_before': config.reminder_hours_before or [],
        'standard_occupancy': config.standard_occupancy,
        'max_occupancy': config.max_occupancy,
        'min_stay': config.min_stay,
        'max_stay': config.max_stay,
    }


def _serialize_resource(r):
    """Serialize BookingResource to dict."""
    images = []
    for img in r.images.select_related('media_asset').all():
        images.append({
            'id': img.pk,
            'media_asset_id': str(img.media_asset_id),
            'url': img.media_asset.get_display_url(),
            'thumbnail': img.media_asset.get_thumbnail('small'),
            'alt_text': img.alt_text or img.media_asset.alt_text,
            'is_primary': img.is_primary,
            'is_video': img.media_asset.is_video(),
            'position': img.position,
        })
    return {
        'id': r.pk,
        'name': r.name,
        'description': r.description,
        'resource_type': r.resource_type,
        'resource_type_display': r.get_resource_type_display(),
        'quantity': r.quantity,
        'base_cost_adjustment': str(r.base_cost_adjustment),
        'assignment_type': r.assignment_type,
        'assignment_type_display': r.get_assignment_type_display(),
        'email': r.email,
        'tags': r.tags or [],
        'sort_order': r.sort_order,
        'is_active': r.is_active,
        'is_per_night': r.is_per_night,
        'images': images,
    }


def _save_resource_images(resource, images_data):
    """Replace all images for a resource from a list of dicts."""
    from media_library.models import MediaAsset
    resource.images.all().delete()
    if not images_data or not isinstance(images_data, list):
        return
    for i, img_data in enumerate(images_data):
        media_asset_id = img_data.get('media_asset_id')
        if not media_asset_id:
            continue
        try:
            asset = MediaAsset.objects.get(pk=media_asset_id)
        except MediaAsset.DoesNotExist:
            continue
        BookingResourceImage.objects.create(
            resource=resource,
            media_asset=asset,
            alt_text=img_data.get('alt_text', ''),
            is_primary=bool(img_data.get('is_primary', False)),
            position=img_data.get('position', i),
        )


def _serialize_person_type(pt):
    """Serialize BookingPersonType to dict."""
    return {
        'id': pt.pk,
        'name': pt.name,
        'cost_adjustment': str(pt.cost_adjustment),
        'min_persons': pt.min_persons,
        'max_persons': pt.max_persons,
        'is_counted_for_capacity': pt.is_counted_for_capacity,
        'is_per_night': pt.is_per_night,
        'sort_order': pt.sort_order,
    }


def _serialize_availability_rule(rule):
    """Serialize BookingAvailabilityRule to dict."""
    return {
        'id': rule.pk,
        'resource_id': rule.resource_id,
        'resource_name': rule.resource.name if rule.resource else '',
        'rule_type': rule.rule_type,
        'rule_type_display': rule.get_rule_type_display(),
        'scope': rule.scope,
        'scope_display': rule.get_scope_display(),
        'start_date': _serialize_date(rule.start_date),
        'end_date': _serialize_date(rule.end_date),
        'start_time': _serialize_time(rule.start_time),
        'end_time': _serialize_time(rule.end_time),
        'days_of_week': rule.days_of_week or [],
        'specific_dates': rule.specific_dates or [],
        'cost_override': str(rule.cost_override) if rule.cost_override is not None else '',
        'cost_adjustment': str(rule.cost_adjustment) if rule.cost_adjustment is not None else '',
        'cost_adjustment_type': rule.cost_adjustment_type,
        'min_stay_override': rule.min_stay_override,
        'length_of_stay_min': rule.length_of_stay_min,
        'length_of_stay_discount_percent': str(rule.length_of_stay_discount_percent) if rule.length_of_stay_discount_percent is not None else '',
        'lead_time_min_days': rule.lead_time_min_days,
        'lead_time_max_days': rule.lead_time_max_days,
        'priority': rule.priority,
    }


def _serialize_recurrence_rule(rule):
    """Serialize BookingRecurrenceRule to dict."""
    return {
        'id': rule.pk,
        'frequency': rule.frequency,
        'frequency_display': rule.get_frequency_display(),
        'day_of_week': rule.day_of_week,
        'day_of_month': rule.day_of_month,
        'start_time': _serialize_time(rule.start_time),
        'end_time': _serialize_time(rule.end_time),
        'start_date': _serialize_date(rule.start_date),
        'end_date': _serialize_date(rule.end_date),
        'auto_create_days_ahead': rule.auto_create_days_ahead,
        'is_active': rule.is_active,
    }


def _parse_time(val):
    """Parse HH:MM string to time object or None."""
    from datetime import time as dt_time
    if not val:
        return None
    try:
        parts = val.split(':')
        return dt_time(int(parts[0]), int(parts[1]))
    except (ValueError, IndexError):
        return None


def _parse_date(val):
    """Parse YYYY-MM-DD string to date object or None."""
    from datetime import date as dt_date
    if not val:
        return None
    try:
        parts = val.split('-')
        return dt_date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return None


def _safe_int(val, default=None):
    """Convert *val* to int, returning *default* on failure or empty."""
    if val in (None, ''):
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


# --- BookingConfig (singleton) ---

@staff_member_required
def booking_config_detail(request, product_id):
    """AJAX GET: Return booking config for a product, or {exists: false}."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    try:
        config = BookingConfig.objects.get(product=product_obj)
        return JsonResponse({'success': True, 'exists': True, 'config': _serialize_booking_config(config)})
    except BookingConfig.DoesNotExist:
        return JsonResponse({'success': True, 'exists': False, 'config': None})


@staff_member_required
@require_POST
def booking_config_save(request, product_id):
    """AJAX POST: Create or update booking config for a product."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    config, created = BookingConfig.objects.get_or_create(product=product_obj)

    # String choice fields
    for field in ['booking_type', 'duration_type', 'duration_unit', 'min_advance_unit',
                  'max_advance_unit', 'cancellation_deadline_unit', 'calendar_display',
                  'deposit_type']:
        if field in data:
            setattr(config, field, data[field])

    # Integer fields
    for field in ['duration', 'min_duration', 'max_duration', 'buffer_before', 'buffer_after',
                  'min_advance', 'max_advance', 'max_bookings_per_slot', 'cancellation_deadline',
                  'standard_occupancy', 'max_occupancy', 'min_stay', 'max_stay']:
        if field in data:
            setattr(config, field, _safe_int(data[field]))

    # Boolean fields
    for field in ['confirmation_required', 'cancellation_allowed', 'customer_timezone_enabled',
                  'deposit_enabled', 'recurrence_enabled', 'reminder_enabled']:
        if field in data:
            setattr(config, field, bool(data[field]))

    # Decimal fields
    from decimal import Decimal, InvalidOperation
    if 'deposit_amount' in data:
        try:
            config.deposit_amount = Decimal(str(data['deposit_amount']))
        except (InvalidOperation, ValueError):
            config.deposit_amount = Decimal('0')

    # Time fields
    if 'check_in_time' in data:
        config.check_in_time = _parse_time(data['check_in_time'])
    if 'check_out_time' in data:
        config.check_out_time = _parse_time(data['check_out_time'])

    # JSON fields
    if 'reminder_hours_before' in data:
        val = data['reminder_hours_before']
        if isinstance(val, list):
            config.reminder_hours_before = val
        elif isinstance(val, str):
            try:
                config.reminder_hours_before = json.loads(val)
            except json.JSONDecodeError:
                config.reminder_hours_before = []

    config.save()
    return JsonResponse({
        'success': True,
        'created': created,
        'config': _serialize_booking_config(config),
    })


# --- BookingResource CRUD ---

@staff_member_required
def list_booking_resources(request, product_id):
    """AJAX GET: List all resources for a booking product."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    resources = BookingResource.objects.filter(product=product_obj).order_by('sort_order', 'name')
    return JsonResponse({
        'success': True,
        'resources': [_serialize_resource(r) for r in resources],
        'count': resources.count(),
    })


@staff_member_required
@require_POST
def create_booking_resource(request, product_id):
    """AJAX POST: Create a new booking resource."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from decimal import Decimal, InvalidOperation
    try:
        cost = Decimal(str(data.get('base_cost_adjustment', 0)))
    except (InvalidOperation, ValueError):
        cost = Decimal('0')

    resource = BookingResource.objects.create(
        product=product_obj,
        name=data.get('name', ''),
        description=data.get('description', ''),
        resource_type=data.get('resource_type', 'generic'),
        quantity=int(data.get('quantity', 1)),
        base_cost_adjustment=cost,
        assignment_type=data.get('assignment_type', 'customer_selected'),
        email=data.get('email', ''),
        tags=data.get('tags', []),
        sort_order=int(data.get('sort_order', 0)),
        is_active=bool(data.get('is_active', True)),
        is_per_night=bool(data.get('is_per_night', True)),
    )
    if 'images' in data:
        _save_resource_images(resource, data['images'])
    return JsonResponse({'success': True, 'resource': _serialize_resource(resource)})


@staff_member_required
def booking_resource_detail(request, resource_id):
    """AJAX GET: Return a single resource."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    resource = get_object_or_404(BookingResource, pk=resource_id)
    return JsonResponse({'success': True, 'resource': _serialize_resource(resource)})


@staff_member_required
@require_POST
def update_booking_resource(request, resource_id):
    """AJAX POST: Update an existing booking resource."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    resource = get_object_or_404(BookingResource, pk=resource_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from decimal import Decimal, InvalidOperation

    for field in ['name', 'description', 'resource_type', 'assignment_type', 'email']:
        if field in data:
            setattr(resource, field, data[field])
    if 'quantity' in data:
        resource.quantity = int(data['quantity'])
    if 'base_cost_adjustment' in data:
        try:
            resource.base_cost_adjustment = Decimal(str(data['base_cost_adjustment']))
        except (InvalidOperation, ValueError):
            pass
    if 'tags' in data:
        resource.tags = data['tags'] if isinstance(data['tags'], list) else []
    if 'sort_order' in data:
        resource.sort_order = int(data['sort_order'])
    if 'is_active' in data:
        resource.is_active = bool(data['is_active'])
    if 'is_per_night' in data:
        resource.is_per_night = bool(data['is_per_night'])

    resource.save()
    if 'images' in data:
        _save_resource_images(resource, data['images'])
    return JsonResponse({'success': True, 'resource': _serialize_resource(resource)})


@staff_member_required
@require_POST
def delete_booking_resource(request, resource_id):
    """AJAX POST: Delete a booking resource."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    resource = get_object_or_404(BookingResource, pk=resource_id)
    resource.delete()
    return JsonResponse({'success': True})


# --- BookingPersonType CRUD ---

@staff_member_required
def list_booking_person_types(request, product_id):
    """AJAX GET: List all person types for a booking product."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    pts = BookingPersonType.objects.filter(product=product_obj).order_by('sort_order', 'name')
    return JsonResponse({
        'success': True,
        'person_types': [_serialize_person_type(pt) for pt in pts],
        'count': pts.count(),
    })


@staff_member_required
@require_POST
def create_booking_person_type(request, product_id):
    """AJAX POST: Create a new person type."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from decimal import Decimal, InvalidOperation
    try:
        cost = Decimal(str(data.get('cost_adjustment', 0)))
    except (InvalidOperation, ValueError):
        cost = Decimal('0')

    pt = BookingPersonType.objects.create(
        product=product_obj,
        name=data.get('name', ''),
        cost_adjustment=cost,
        min_persons=int(data.get('min_persons', 0)),
        max_persons=int(data.get('max_persons', 10)),
        is_counted_for_capacity=bool(data.get('is_counted_for_capacity', True)),
        is_per_night=bool(data.get('is_per_night', True)),
        sort_order=int(data.get('sort_order', 0)),
    )
    return JsonResponse({'success': True, 'person_type': _serialize_person_type(pt)})


@staff_member_required
def booking_person_type_detail(request, person_type_id):
    """AJAX GET: Return a single person type."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    pt = get_object_or_404(BookingPersonType, pk=person_type_id)
    return JsonResponse({'success': True, 'person_type': _serialize_person_type(pt)})


@staff_member_required
@require_POST
def update_booking_person_type(request, person_type_id):
    """AJAX POST: Update an existing person type."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    pt = get_object_or_404(BookingPersonType, pk=person_type_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from decimal import Decimal, InvalidOperation
    if 'name' in data:
        pt.name = data['name']
    if 'cost_adjustment' in data:
        try:
            pt.cost_adjustment = Decimal(str(data['cost_adjustment']))
        except (InvalidOperation, ValueError):
            pass
    if 'min_persons' in data:
        pt.min_persons = int(data['min_persons'])
    if 'max_persons' in data:
        pt.max_persons = int(data['max_persons'])
    if 'is_counted_for_capacity' in data:
        pt.is_counted_for_capacity = bool(data['is_counted_for_capacity'])
    if 'is_per_night' in data:
        pt.is_per_night = bool(data['is_per_night'])
    if 'sort_order' in data:
        pt.sort_order = int(data['sort_order'])

    pt.save()
    return JsonResponse({'success': True, 'person_type': _serialize_person_type(pt)})


@staff_member_required
@require_POST
def delete_booking_person_type(request, person_type_id):
    """AJAX POST: Delete a person type."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    pt = get_object_or_404(BookingPersonType, pk=person_type_id)
    pt.delete()
    return JsonResponse({'success': True})


# --- BookingAvailabilityRule CRUD ---

@staff_member_required
def list_booking_availability_rules(request, product_id):
    """AJAX GET: List all availability rules for a booking product."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    rules = BookingAvailabilityRule.objects.filter(
        product=product_obj
    ).select_related('resource').order_by('-priority', 'start_date')
    # Optional rule_type filter (e.g., ?rule_type=unavailable for blackout periods)
    rule_type_filter = request.GET.get('rule_type')
    if rule_type_filter:
        rules = rules.filter(rule_type=rule_type_filter)
    # Also return resources for the dropdown
    resources = BookingResource.objects.filter(product=product_obj, is_active=True).order_by('sort_order', 'name')
    return JsonResponse({
        'success': True,
        'rules': [_serialize_availability_rule(r) for r in rules],
        'count': rules.count(),
        'resources': [{'id': r.pk, 'name': r.name} for r in resources],
    })


@staff_member_required
@require_POST
def create_booking_availability_rule(request, product_id):
    """AJAX POST: Create a new availability rule."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from decimal import Decimal, InvalidOperation

    resource = None
    if data.get('resource_id'):
        resource = get_object_or_404(BookingResource, pk=data['resource_id'], product=product_obj)

    cost_override = None
    if data.get('cost_override') not in (None, ''):
        try:
            cost_override = Decimal(str(data['cost_override']))
        except (InvalidOperation, ValueError):
            pass

    cost_adjustment = None
    if data.get('cost_adjustment') not in (None, ''):
        try:
            cost_adjustment = Decimal(str(data['cost_adjustment']))
        except (InvalidOperation, ValueError):
            pass

    # Parse new optional fields
    cost_adjustment_type = data.get('cost_adjustment_type', 'flat')
    if cost_adjustment_type not in ('flat', 'percentage'):
        cost_adjustment_type = 'flat'

    los_discount = None
    if data.get('length_of_stay_discount_percent') not in (None, ''):
        try:
            los_discount = Decimal(str(data['length_of_stay_discount_percent']))
        except (InvalidOperation, ValueError):
            pass

    rule = BookingAvailabilityRule.objects.create(
        product=product_obj,
        resource=resource,
        rule_type=data.get('rule_type', 'available'),
        scope=data.get('scope', 'all_dates'),
        start_date=_parse_date(data.get('start_date')),
        end_date=_parse_date(data.get('end_date')),
        start_time=_parse_time(data.get('start_time')),
        end_time=_parse_time(data.get('end_time')),
        days_of_week=data.get('days_of_week', []),
        specific_dates=data.get('specific_dates', []),
        cost_override=cost_override,
        cost_adjustment=cost_adjustment,
        cost_adjustment_type=cost_adjustment_type,
        min_stay_override=_safe_int(data.get('min_stay_override')),
        length_of_stay_min=_safe_int(data.get('length_of_stay_min')),
        length_of_stay_discount_percent=los_discount,
        lead_time_min_days=_safe_int(data.get('lead_time_min_days')),
        lead_time_max_days=_safe_int(data.get('lead_time_max_days')),
        priority=_safe_int(data.get('priority'), default=10),
    )
    return JsonResponse({'success': True, 'rule': _serialize_availability_rule(rule)})


@staff_member_required
def booking_availability_rule_detail(request, rule_id):
    """AJAX GET: Return a single availability rule."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    rule = get_object_or_404(BookingAvailabilityRule.objects.select_related('resource'), pk=rule_id)
    return JsonResponse({'success': True, 'rule': _serialize_availability_rule(rule)})


@staff_member_required
@require_POST
def update_booking_availability_rule(request, rule_id):
    """AJAX POST: Update an existing availability rule."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    rule = get_object_or_404(BookingAvailabilityRule, pk=rule_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from decimal import Decimal, InvalidOperation

    if 'resource_id' in data:
        if data['resource_id']:
            rule.resource = get_object_or_404(BookingResource, pk=data['resource_id'], product=rule.product)
        else:
            rule.resource = None

    for field in ['rule_type', 'scope']:
        if field in data:
            setattr(rule, field, data[field])

    if 'start_date' in data:
        rule.start_date = _parse_date(data['start_date'])
    if 'end_date' in data:
        rule.end_date = _parse_date(data['end_date'])
    if 'start_time' in data:
        rule.start_time = _parse_time(data['start_time'])
    if 'end_time' in data:
        rule.end_time = _parse_time(data['end_time'])
    if 'days_of_week' in data:
        rule.days_of_week = data['days_of_week'] if isinstance(data['days_of_week'], list) else []
    if 'specific_dates' in data:
        rule.specific_dates = data['specific_dates'] if isinstance(data['specific_dates'], list) else []

    if 'cost_override' in data:
        if data['cost_override'] not in (None, ''):
            try:
                rule.cost_override = Decimal(str(data['cost_override']))
            except (InvalidOperation, ValueError):
                pass
        else:
            rule.cost_override = None

    if 'cost_adjustment' in data:
        if data['cost_adjustment'] not in (None, ''):
            try:
                rule.cost_adjustment = Decimal(str(data['cost_adjustment']))
            except (InvalidOperation, ValueError):
                pass
        else:
            rule.cost_adjustment = None

    if 'priority' in data:
        p = _safe_int(data['priority'], default=10)
        rule.priority = p

    if 'cost_adjustment_type' in data:
        val = data['cost_adjustment_type']
        rule.cost_adjustment_type = val if val in ('flat', 'percentage') else 'flat'

    for int_field in ['min_stay_override', 'length_of_stay_min', 'lead_time_min_days', 'lead_time_max_days']:
        if int_field in data:
            setattr(rule, int_field, _safe_int(data[int_field]))

    if 'length_of_stay_discount_percent' in data:
        val = data['length_of_stay_discount_percent']
        if val not in (None, ''):
            try:
                rule.length_of_stay_discount_percent = Decimal(str(val))
            except (InvalidOperation, ValueError):
                pass
        else:
            rule.length_of_stay_discount_percent = None

    rule.save()
    return JsonResponse({'success': True, 'rule': _serialize_availability_rule(rule)})


@staff_member_required
@require_POST
def delete_booking_availability_rule(request, rule_id):
    """AJAX POST: Delete an availability rule."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    rule = get_object_or_404(BookingAvailabilityRule, pk=rule_id)
    rule.delete()
    return JsonResponse({'success': True})


# --- BookingRecurrenceRule CRUD ---

@staff_member_required
def list_booking_recurrence_rules(request, product_id):
    """AJAX GET: List all recurrence rules for a booking product."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    rules = BookingRecurrenceRule.objects.filter(product=product_obj).order_by('start_date', 'start_time')
    return JsonResponse({
        'success': True,
        'rules': [_serialize_recurrence_rule(r) for r in rules],
        'count': rules.count(),
    })


@staff_member_required
@require_POST
def create_booking_recurrence_rule(request, product_id):
    """AJAX POST: Create a new recurrence rule."""
    product_obj, err = _check_booking_ajax(request, product_id)
    if err:
        return err
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    start_time = _parse_time(data.get('start_time', '09:00'))
    end_time = _parse_time(data.get('end_time', '17:00'))
    start_date = _parse_date(data.get('start_date'))

    if not start_time or not end_time or not start_date:
        return JsonResponse({'error': 'start_time, end_time, and start_date are required'}, status=400)

    rule = BookingRecurrenceRule.objects.create(
        product=product_obj,
        frequency=data.get('frequency', 'weekly'),
        day_of_week=int(data['day_of_week']) if data.get('day_of_week') not in (None, '') else None,
        day_of_month=int(data['day_of_month']) if data.get('day_of_month') not in (None, '') else None,
        start_time=start_time,
        end_time=end_time,
        start_date=start_date,
        end_date=_parse_date(data.get('end_date')),
        auto_create_days_ahead=int(data.get('auto_create_days_ahead', 90)),
        is_active=bool(data.get('is_active', True)),
    )
    return JsonResponse({'success': True, 'rule': _serialize_recurrence_rule(rule)})


@staff_member_required
def booking_recurrence_rule_detail(request, rule_id):
    """AJAX GET: Return a single recurrence rule."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    rule = get_object_or_404(BookingRecurrenceRule, pk=rule_id)
    return JsonResponse({'success': True, 'rule': _serialize_recurrence_rule(rule)})


@staff_member_required
@require_POST
def update_booking_recurrence_rule(request, rule_id):
    """AJAX POST: Update an existing recurrence rule."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    rule = get_object_or_404(BookingRecurrenceRule, pk=rule_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if 'frequency' in data:
        rule.frequency = data['frequency']
    if 'day_of_week' in data:
        rule.day_of_week = int(data['day_of_week']) if data['day_of_week'] not in (None, '') else None
    if 'day_of_month' in data:
        rule.day_of_month = int(data['day_of_month']) if data['day_of_month'] not in (None, '') else None
    if 'start_time' in data:
        t = _parse_time(data['start_time'])
        if t:
            rule.start_time = t
    if 'end_time' in data:
        t = _parse_time(data['end_time'])
        if t:
            rule.end_time = t
    if 'start_date' in data:
        d = _parse_date(data['start_date'])
        if d:
            rule.start_date = d
    if 'end_date' in data:
        rule.end_date = _parse_date(data['end_date'])
    if 'auto_create_days_ahead' in data:
        rule.auto_create_days_ahead = int(data['auto_create_days_ahead'])
    if 'is_active' in data:
        rule.is_active = bool(data['is_active'])

    rule.save()
    return JsonResponse({'success': True, 'rule': _serialize_recurrence_rule(rule)})


@staff_member_required
@require_POST
def delete_booking_recurrence_rule(request, rule_id):
    """AJAX POST: Delete a recurrence rule."""
    _, err = _check_booking_ajax(request)
    if err:
        return err
    rule = get_object_or_404(BookingRecurrenceRule, pk=rule_id)
    rule.delete()
    return JsonResponse({'success': True})


@staff_member_required
@require_GET
def filter_reviews(request):
    """AJAX filter endpoint for ProductReview entries."""
    from django.template.loader import render_to_string
    from django.db.models import Q

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    queryset = ProductReview.objects.select_related('product', 'user').prefetch_related('product__images__media_asset').all()

    search = request.GET.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(product__name__icontains=search) |
            Q(user__username__icontains=search) |
            Q(title__icontains=search)
        )

    rating = request.GET.get('rating', '').strip()
    if rating:
        queryset = queryset.filter(rating=int(rating))

    approved = request.GET.get('approved', '').strip()
    if approved == 'true':
        queryset = queryset.filter(is_approved=True)
    elif approved == 'false':
        queryset = queryset.filter(is_approved=False)

    verified = request.GET.get('verified', '').strip()
    if verified == 'true':
        queryset = queryset.filter(is_verified_purchase=True)
    elif verified == 'false':
        queryset = queryset.filter(is_verified_purchase=False)

    total_count = queryset.count()
    reviews = queryset.order_by('-created_at')[:100]

    html = render_to_string(
        'admin/catalog/productreview/partials/review_cards.html',
        {'reviews': reviews},
        request=request
    )

    return JsonResponse({'html': html, 'count': total_count})


@staff_member_required
def booking_check_reschedule(request, booking_id):
    """
    AJAX endpoint for checking reschedule availability from the admin change form.

    Returns JSON: {available: bool, message: str, price: str|null}
    """
    from datetime import datetime as dt, timezone as dt_tz
    from catalog.models import Booking
    from catalog.services.booking_service import BookingAvailabilityService

    try:
        booking = Booking.objects.select_related('product').get(pk=booking_id)
    except Booking.DoesNotExist:
        return JsonResponse({'available': False, 'message': 'Booking not found'}, status=404)

    date_str = request.GET.get('date', '')
    start_str = request.GET.get('time_start', '')
    end_str = request.GET.get('time_end', '')

    if not (date_str and start_str and end_str):
        return JsonResponse({'available': False, 'message': 'Missing date or time'}, status=400)

    try:
        new_start = dt.fromisoformat(f'{date_str}T{start_str}').replace(tzinfo=dt_tz.utc)
        new_end = dt.fromisoformat(f'{date_str}T{end_str}').replace(tzinfo=dt_tz.utc)
    except (ValueError, TypeError):
        return JsonResponse({'available': False, 'message': 'Invalid date/time format'}, status=400)

    is_available, message, price = BookingAvailabilityService.check_availability(
        booking.product, new_start, new_end,
        resource_id=booking.resource_id,
        persons=booking.persons,
    )

    return JsonResponse({
        'available': is_available,
        'message': message,
        'price': str(price) if price is not None else None,
    })
