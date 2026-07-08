"""
Auto-detect field mappings from source data
"""
import logging
from ..models import MigrationMapping
from ..mapping_config import (
    WOOCOMMERCE_MAPPINGS,
    SEO_META_FIELDS,
    should_skip_meta_field
)

logger = logging.getLogger(__name__)


def _get_platform_config(platform):
    """Get mapping config for a platform."""
    if platform == 'woocommerce':
        return WOOCOMMERCE_MAPPINGS
    elif platform == 'shopify':
        from ..mapping_config_shopify import SHOPIFY_MAPPINGS
        return SHOPIFY_MAPPINGS
    elif platform == 'magento':
        from ..mapping_config_magento import MAGENTO_MAPPINGS
        return MAGENTO_MAPPINGS
    return {}


def create_standard_mappings(job, platform='woocommerce', selected_types=None):
    """
    Create MigrationMapping records for standard fields.

    Args:
        job: MigrationJob instance
        platform: Source platform ('woocommerce', 'shopify', etc.)
        selected_types: Optional set of config keys to include (e.g. {'products', 'blog_posts'}).
                       If None, all types are included.

    Returns:
        int: Number of mappings created
    """
    mappings_created = 0

    config = _get_platform_config(platform)

    for source_type, field_map in config.items():
        if selected_types and source_type not in selected_types:
            continue
        # Remove plural (products → product, categories → category)
        # Handle special cases properly
        if source_type.endswith('ies'):
            singular_type = source_type[:-3] + 'y'  # categories → category
        elif source_type.endswith('s'):
            singular_type = source_type[:-1]  # products → product
        else:
            singular_type = source_type

        for source_field, (dest_model, dest_field, transform_type) in field_map.items():
            # Skip special handling fields (will process separately)
            if dest_model in ['special', 'meta']:
                continue

            # Create or get mapping
            mapping, created = MigrationMapping.objects.get_or_create(
                job=job,
                source_type=singular_type,
                source_field=source_field,
                defaults={
                    'dest_model': dest_model,
                    'dest_field': dest_field,
                    'transform_type': transform_type,
                    'is_auto_detected': True,
                    'source_field_label': format_field_label(source_field),
                    'dest_field_label': format_field_label(dest_field),
                }
            )

            if created:
                mappings_created += 1
                logger.debug(f"Created mapping: {source_field} → {dest_model}.{dest_field}")

    logger.info(f"Created {mappings_created} standard field mappings for {platform}")
    return mappings_created


def detect_custom_fields(sample_items, source_type='product', limit=20,
                         platform='woocommerce'):
    """
    Detect custom fields in meta_data/metafields that might be useful.

    Args:
        sample_items: List of item dictionaries from WooCommerce or Shopify
        source_type: Type of source data ('product', 'customer', 'order')
        limit: Maximum number of custom fields to return
        platform: Source platform ('woocommerce' or 'shopify')

    Returns:
        list: Custom field dictionaries with name, type, source_type, sample values
    """
    SOURCE_TYPE_LABELS = {
        'product': 'Product',
        'customer': 'Customer',
        'order': 'Order',
    }

    custom_fields = {}

    for item in sample_items:
        if platform == 'shopify':
            # Shopify uses metafields with namespace.key structure
            meta_data = item.get('metafields', [])
            if not meta_data:
                continue
            for meta_item in meta_data:
                namespace = meta_item.get('namespace', '')
                key = meta_item.get('key', '')
                value = meta_item.get('value', '')
                full_key = f'{namespace}.{key}' if namespace else key
                _track_custom_field(custom_fields, full_key, value,
                                    source_type, SOURCE_TYPE_LABELS)
        else:
            # WooCommerce uses meta_data array
            meta_data = item.get('meta_data', [])
            for meta_item in meta_data:
                key = meta_item.get('key', '')
                value = meta_item.get('value', '')
                if should_skip_meta_field(key):
                    continue
                _track_custom_field(custom_fields, key, value,
                                    source_type, SOURCE_TYPE_LABELS)

    # Convert to list and sort by frequency
    fields_list = list(custom_fields.values())
    fields_list.sort(key=lambda x: x['count'], reverse=True)

    # Return top N fields
    return fields_list[:limit]


def _track_custom_field(custom_fields, key, value, source_type, labels):
    """Track a custom field occurrence."""
    if key not in custom_fields:
        custom_fields[key] = {
            'id': f'{source_type}__{key}',
            'name': key,
            'source_type': source_type,
            'source_type_label': labels.get(source_type, source_type.title()),
            'type': infer_field_type(value),
            'count': 0,
            'sample_values': [],
            'sample_value': None,
        }

    field_info = custom_fields[key]
    field_info['count'] += 1

    # Store up to 3 sample values
    if len(field_info['sample_values']) < 3 and value:
        field_info['sample_values'].append(str(value)[:100])

    # Set primary sample value (first non-empty)
    if not field_info['sample_value'] and value:
        field_info['sample_value'] = str(value)[:100]


def infer_field_type(value):
    """
    Infer the data type of a field value.

    Args:
        value: Field value

    Returns:
        str: Inferred type (string, integer, decimal, boolean, json)
    """
    if value is None or value == '':
        return 'string'

    # Boolean
    if isinstance(value, bool):
        return 'boolean'
    if str(value).lower() in ['true', 'false', 'yes', 'no', '0', '1']:
        return 'boolean'

    # Integer
    try:
        int_val = int(value)
        if str(int_val) == str(value):
            return 'integer'
    except (ValueError, TypeError):
        pass

    # Decimal
    try:
        float(value)
        return 'decimal'
    except (ValueError, TypeError):
        pass

    # JSON (dict or list)
    if isinstance(value, (dict, list)):
        return 'json'

    # Check if it's JSON string
    if isinstance(value, str):
        if value.startswith('{') or value.startswith('['):
            try:
                import json
                json.loads(value)
                return 'json'
            except:
                pass

    # Default to string
    return 'string'


def format_field_label(field_name):
    """
    Convert field name to human-readable label.

    Args:
        field_name: Field name (e.g., 'regular_price', 'stock_quantity')

    Returns:
        str: Formatted label (e.g., 'Regular Price', 'Stock Quantity')
    """
    # Handle nested fields (dimensions.length → Length)
    if '.' in field_name:
        field_name = field_name.split('.')[-1]

    # Replace underscores with spaces and title case
    return field_name.replace('_', ' ').title()


def analyze_category_mapping(job, woo_categories, existing_categories):
    """
    Analyze if WooCommerce categories match existing platform categories.

    Args:
        job: MigrationJob instance
        woo_categories: List of WooCommerce category dicts
        existing_categories: QuerySet of existing Category objects

    Returns:
        dict: Analysis with matched, unmatched, and suggestions
    """
    analysis = {
        'total_woo_categories': len(woo_categories),
        'total_existing': existing_categories.count(),
        'matched': [],
        'unmatched': [],
        'needs_mapping': False,
    }

    # Build lookup of existing categories by slug and name
    existing_by_slug = {cat.slug: cat for cat in existing_categories}
    existing_by_name = {cat.name.lower(): cat for cat in existing_categories}

    for woo_cat in woo_categories:
        woo_slug = woo_cat.get('slug', '')
        woo_name = woo_cat.get('name', '')

        # Try to match by slug first (most reliable)
        if woo_slug in existing_by_slug:
            analysis['matched'].append({
                'woo_category': woo_name,
                'platform_category': existing_by_slug[woo_slug].name,
                'match_type': 'slug',
            })
        # Try to match by name (case-insensitive)
        elif woo_name.lower() in existing_by_name:
            analysis['matched'].append({
                'woo_category': woo_name,
                'platform_category': existing_by_name[woo_name.lower()].name,
                'match_type': 'name',
            })
        else:
            # No match found
            analysis['unmatched'].append({
                'id': woo_cat.get('id'),
                'name': woo_name,
                'slug': woo_slug,
                'product_count': woo_cat.get('count', 0),
            })
            analysis['needs_mapping'] = True

    return analysis
