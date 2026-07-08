"""
Magento 2 Data Mappers
Transform Magento 2 REST API data to internal platform format.

Handles Magento-specific structures:
- EAV custom_attributes array (attribute_code/value pairs with option ID resolution)
- Configurable product children as separate simple products
- Category tree with nested children_data
- Order shipping via extension_attributes.shipping_assignments
"""
from typing import Dict, List, Optional
from decimal import Decimal
from .base import BaseMapper
from migration.utils.magento_transformers import (
    resolve_custom_attribute,
    resolve_attribute_label,
    transform_magento_status,
    transform_magento_product_type,
    transform_magento_order_status,
    transform_magento_payment_status,
    transform_magento_discount_type,
    transform_magento_rating,
    clean_cms_directives,
)
import logging

logger = logging.getLogger(__name__)


class MagentoCategoryMapper(BaseMapper):
    """Map Magento categories to internal Category model.

    Magento returns categories as a recursive tree from /V1/categories.
    This mapper works on individual flattened category nodes.
    """

    def map(self, source_data: Dict) -> Dict:
        """
        Map a single Magento category node to internal format.

        Magento category node (from tree or flat list):
        {
            "id": 3,
            "parent_id": 2,
            "name": "Clothing",
            "is_active": true,
            "position": 1,
            "level": 2,
            "product_count": 28,
            "children_data": [...],
            "custom_attributes": [
                {"attribute_code": "url_key", "value": "clothing"},
                {"attribute_code": "description", "value": "..."},
                {"attribute_code": "image", "value": "clothing.jpg"}
            ]
        }
        """
        try:
            custom_attrs = source_data.get('custom_attributes', [])

            mapped = {
                # Basic fields
                'name': source_data.get('name', ''),
                'slug': self.generate_slug(
                    resolve_custom_attribute(custom_attrs, 'url_key')
                    or source_data.get('name', '')
                ),
                'description': self.parse_html(
                    resolve_custom_attribute(custom_attrs, 'description') or ''
                ),

                # Hierarchy
                'parent_id': source_data.get('parent_id', 0),

                # Display
                'sort_order': source_data.get('position', 0),
                'is_active': source_data.get('is_active', True),
                'is_featured': False,

                # SEO
                'meta_title': resolve_custom_attribute(custom_attrs, 'meta_title') or '',
                'meta_description': (
                    resolve_custom_attribute(custom_attrs, 'meta_description') or ''
                )[:255],

                # Image
                'image_url': resolve_custom_attribute(custom_attrs, 'image') or None,
                'image_alt': '',

                # Display settings
                'page_template': 'grid',
                'products_per_page': 24,
                'show_subcategories': True,

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'magento',
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map category: {e}", source_data)
            raise

    @staticmethod
    def flatten_category_tree(tree_node: Dict, result: List[Dict] = None,
                              skip_root: bool = True) -> List[Dict]:
        """Recursively flatten Magento category tree into a flat list.

        Args:
            tree_node: Root category node from /V1/categories
            result: Accumulator list (internal use)
            skip_root: Skip the Magento root category (id=1) and default category (id=2)

        Returns:
            Flat list of category nodes
        """
        if result is None:
            result = []

        node_id = tree_node.get('id', 0)
        # Skip root category (id=1) and optionally the default root (id=2)
        if not skip_root or node_id > 2:
            # Create a clean copy without children_data to avoid passing huge nested structures
            node_copy = {k: v for k, v in tree_node.items() if k != 'children_data'}
            result.append(node_copy)

        for child in tree_node.get('children_data', []):
            MagentoCategoryMapper.flatten_category_tree(child, result, skip_root=False)

        return result


class MagentoProductMapper(BaseMapper):
    """Map Magento products to internal Product model.

    Handles EAV custom_attributes resolution and configurable product detection.
    """

    def __init__(self, migration_job=None, attribute_options_cache: Dict = None,
                 store_url: str = ''):
        super().__init__(migration_job)
        self.attribute_options_cache = attribute_options_cache or {}
        self.store_url = store_url.rstrip('/')

    def map(self, source_data: Dict) -> Dict:
        """
        Map Magento product to internal format.

        Magento product structure:
        {
            "id": 1036,
            "sku": "WSH12-28-Green",
            "name": "Erika Running Short",
            "attribute_set_id": 9,
            "price": 45.00,
            "status": 1,
            "visibility": 4,
            "type_id": "simple",
            "weight": 1.0,
            "created_at": "2024-01-15 10:30:00",
            "updated_at": "2024-06-15 14:20:00",
            "extension_attributes": {
                "stock_item": {"qty": 100, "is_in_stock": true, "manage_stock": true},
                "category_links": [{"category_id": "23"}]
            },
            "custom_attributes": [
                {"attribute_code": "description", "value": "<p>HTML</p>"},
                {"attribute_code": "url_key", "value": "erika-running-short"},
                {"attribute_code": "color", "value": "53"},
                ...
            ],
            "media_gallery_entries": [
                {"id": 945, "file": "/w/s/wsh12.jpg", "position": 1, "label": "Main"}
            ]
        }
        """
        try:
            custom_attrs = source_data.get('custom_attributes', [])
            ext_attrs = source_data.get('extension_attributes', {})
            stock_item = ext_attrs.get('stock_item', {})
            type_id = source_data.get('type_id', 'simple')

            mapped = {
                # Basic information
                'name': source_data.get('name', ''),
                'slug': self.generate_slug(
                    resolve_custom_attribute(custom_attrs, 'url_key')
                    or source_data.get('name', '')
                ),
                'sku': source_data.get('sku', ''),

                # Product type
                'product_type': transform_magento_product_type(type_id),

                # Descriptions
                'full_description': self.parse_html(
                    resolve_custom_attribute(custom_attrs, 'description') or ''
                ),
                'short_description': self.parse_html(
                    resolve_custom_attribute(custom_attrs, 'short_description') or ''
                )[:500],

                # Pricing
                'price': self._parse_price(source_data.get('price')),
                'regular_price': self._parse_price(source_data.get('price')),
                'sale_price': self._parse_price(
                    resolve_custom_attribute(custom_attrs, 'special_price')
                ),

                # Categories
                'category_ids': [
                    int(link.get('category_id', 0))
                    for link in ext_attrs.get('category_links', [])
                ],
                'primary_category_id': (
                    int(ext_attrs.get('category_links', [{}])[0].get('category_id', 0))
                    if ext_attrs.get('category_links')
                    else None
                ),

                # Inventory
                'track_inventory': stock_item.get('manage_stock', False),
                'stock_quantity': int(stock_item.get('qty', 0) or 0),
                'allow_backorders': int(stock_item.get('backorders', 0) or 0) > 0,
                'low_stock_threshold': int(stock_item.get('notify_stock_qty', 5) or 5),

                # Physical attributes
                'weight': self._parse_decimal(source_data.get('weight')),
                'length': None,
                'width': None,
                'height': None,

                # Status
                'status': transform_magento_status(source_data.get('status', 2)),
                'is_featured': False,
                'is_digital': type_id in ('virtual', 'downloadable'),

                # SEO
                'meta_title': resolve_custom_attribute(custom_attrs, 'meta_title') or source_data.get('name', ''),
                'meta_description': (
                    resolve_custom_attribute(custom_attrs, 'meta_description') or ''
                )[:255],

                # Images
                'images': self._map_images(source_data.get('media_gallery_entries', [])),

                # Custom attributes (resolved)
                'attributes': self._map_custom_attributes(custom_attrs),
                'specifications': {},

                # Variations
                'has_variations': type_id == 'configurable',
                'variation_ids': ext_attrs.get('configurable_product_links', []),

                # Tags (Magento doesn't have native tags; skip)
                'tags': [],

                # Reviews
                'reviews_allowed': True,
                'average_rating': 0,
                'rating_count': 0,

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'magento',
                'source_data': {
                    'type_id': type_id,
                    'attribute_set_id': source_data.get('attribute_set_id'),
                    'visibility': source_data.get('visibility'),
                    'created_at': source_data.get('created_at'),
                    'updated_at': source_data.get('updated_at'),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(
                f"Failed to map product: {e}",
                {'id': source_data.get('id'), 'name': source_data.get('name')}
            )
            raise

    def _map_images(self, media_entries: List[Dict]) -> List[Dict]:
        """Map Magento media_gallery_entries to internal image format."""
        mapped_images = []
        for idx, entry in enumerate(media_entries):
            if entry.get('disabled', False):
                continue
            file_path = entry.get('file', '')
            mapped_images.append({
                'external_id': str(entry.get('id', '')),
                'src': f"{self.store_url}/media/catalog/product{file_path}" if file_path else '',
                'name': '',
                'alt_text': entry.get('label') or '',
                'position': entry.get('position', idx),
                'is_primary': idx == 0 or 'image' in entry.get('types', []),
            })
        return mapped_images

    def _map_custom_attributes(self, custom_attrs: List[Dict]) -> Dict:
        """Map Magento custom_attributes to key-value pairs.

        Resolves select/multiselect option IDs to labels using the cache.
        Skips standard fields that are mapped directly.
        """
        SKIP_CODES = {
            'description', 'short_description', 'url_key', 'meta_title',
            'meta_description', 'meta_keyword', 'image', 'small_image',
            'thumbnail', 'swatch_image', 'special_price', 'special_from_date',
            'special_to_date', 'tax_class_id', 'status', 'visibility',
        }

        attributes = {}
        for attr in custom_attrs:
            code = attr.get('attribute_code', '')
            value = attr.get('value')
            if not code or code in SKIP_CODES or value is None or value == '':
                continue

            # Resolve option IDs to labels if this attribute is in the cache
            if code in self.attribute_options_cache:
                value = resolve_attribute_label(value, code, self.attribute_options_cache)

            attributes[code] = str(value)

        return attributes

    def _parse_price(self, price) -> Optional[Decimal]:
        """Parse price to Decimal."""
        if not price:
            return None
        try:
            return Decimal(str(price))
        except (ValueError, TypeError):
            self.log_warning(f"Failed to parse price: {price}")
            return None

    def _parse_decimal(self, value) -> Optional[Decimal]:
        """Parse decimal value."""
        if not value:
            return None
        try:
            return Decimal(str(value))
        except (ValueError, TypeError):
            return None


class MagentoCustomerMapper(BaseMapper):
    """Map Magento customers to internal User/Customer model."""

    def map(self, source_data: Dict) -> Dict:
        """
        Map Magento customer to internal format.

        Magento customer structure:
        {
            "id": 1,
            "email": "john@example.com",
            "firstname": "John",
            "lastname": "Doe",
            "group_id": 1,
            "store_id": 1,
            "website_id": 1,
            "created_at": "2024-01-15 10:00:00",
            "default_billing": "1",
            "default_shipping": "2",
            "addresses": [
                {
                    "id": 1,
                    "customer_id": 1,
                    "firstname": "John",
                    "lastname": "Doe",
                    "street": ["123 Main St", "Apt 4"],
                    "city": "Springfield",
                    "region": {"region": "Illinois", "region_code": "IL"},
                    "postcode": "62701",
                    "country_id": "US",
                    "telephone": "555-1234",
                    "default_billing": true,
                    "default_shipping": true
                }
            ]
        }
        """
        try:
            addresses = source_data.get('addresses', [])
            default_billing_id = source_data.get('default_billing')
            default_shipping_id = source_data.get('default_shipping')

            billing_addr = self._find_address(addresses, default_billing_id, 'default_billing')
            shipping_addr = self._find_address(addresses, default_shipping_id, 'default_shipping')

            mapped = {
                # User fields
                'email': source_data.get('email', ''),
                'username': (
                    source_data.get('email', '').split('@')[0]
                    if source_data.get('email')
                    else ''
                ),
                'first_name': source_data.get('firstname') or '',
                'last_name': source_data.get('lastname') or '',

                # Customer profile
                'is_active': True,

                # Addresses
                'billing_address': self._map_address(billing_addr),
                'shipping_address': self._map_address(shipping_addr),

                # Metadata
                'total_orders': 0,  # Not available in customer API
                'total_spent': None,

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'magento',
                'source_data': {
                    'created_at': source_data.get('created_at'),
                    'updated_at': source_data.get('updated_at'),
                    'group_id': source_data.get('group_id'),
                    'store_id': source_data.get('store_id'),
                    'website_id': source_data.get('website_id'),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(
                f"Failed to map customer: {e}",
                {'id': source_data.get('id'), 'email': source_data.get('email')}
            )
            raise

    def _find_address(self, addresses: List[Dict], address_id,
                      flag_field: str) -> Dict:
        """Find a specific address by ID or by default flag."""
        if not addresses:
            return {}

        # Try by ID first
        if address_id:
            for addr in addresses:
                if str(addr.get('id')) == str(address_id):
                    return addr

        # Try by flag
        for addr in addresses:
            if addr.get(flag_field, False):
                return addr

        # Fall back to first address
        return addresses[0] if addresses else {}

    def _map_address(self, address_data: Dict) -> Dict:
        """Map Magento address format to internal format."""
        if not address_data:
            return {}

        # Magento street is an array
        street = address_data.get('street', [])
        address_1 = street[0] if street else ''
        address_2 = street[1] if len(street) > 1 else ''

        region = address_data.get('region', {})
        state = ''
        if isinstance(region, dict):
            state = region.get('region_code') or region.get('region', '')
        elif isinstance(region, str):
            state = region

        return {
            'first_name': address_data.get('firstname') or '',
            'last_name': address_data.get('lastname') or '',
            'company': address_data.get('company') or '',
            'address_1': address_1,
            'address_2': address_2,
            'city': address_data.get('city') or '',
            'state': state,
            'postcode': address_data.get('postcode') or '',
            'country': address_data.get('country_id') or '',
            'phone': address_data.get('telephone') or '',
            'email': '',  # Magento addresses don't include email
        }


class MagentoOrderMapper(BaseMapper):
    """Map Magento orders to internal Order model."""

    def map(self, source_data: Dict) -> Dict:
        """
        Map Magento order to internal format.

        Magento order structure:
        {
            "entity_id": 1,
            "increment_id": "000000001",
            "status": "processing",
            "state": "processing",
            "customer_email": "john@example.com",
            "customer_id": 1,
            "subtotal": 100.00,
            "discount_amount": -10.00,
            "shipping_amount": 5.00,
            "tax_amount": 8.50,
            "grand_total": 103.50,
            "order_currency_code": "USD",
            "payment": {"method": "checkmo"},
            "billing_address": {...},
            "extension_attributes": {
                "shipping_assignments": [{
                    "shipping": {
                        "address": {...},
                        "method": "flatrate_flatrate"
                    }
                }]
            },
            "items": [...]
        }
        """
        try:
            ext_attrs = source_data.get('extension_attributes', {})
            shipping_assignments = ext_attrs.get('shipping_assignments', [])
            shipping_info = (
                shipping_assignments[0].get('shipping', {})
                if shipping_assignments
                else {}
            )
            payment = source_data.get('payment', {})

            mapped = {
                # Order identification
                'order_number': str(
                    source_data.get('increment_id')
                    or source_data.get('entity_id')
                ),

                # Customer
                'customer_id': source_data.get('customer_id', 0),
                'customer_email': source_data.get('customer_email', ''),

                # Status
                'status': transform_magento_order_status(
                    source_data.get('status', 'pending')
                ),
                'payment_status': transform_magento_payment_status(
                    source_data.get('status', 'pending')
                ),

                # Amounts (discount_amount is negative in Magento)
                'subtotal': self._parse_price(source_data.get('subtotal', 0)),
                'discount_total': self._parse_price(
                    abs(float(source_data.get('discount_amount', 0) or 0))
                ),
                'shipping_total': self._parse_price(
                    source_data.get('shipping_amount', 0)
                ),
                'tax_total': self._parse_price(source_data.get('tax_amount', 0)),
                'total': self._parse_price(source_data.get('grand_total', 0)),

                # Currency
                'currency': source_data.get('order_currency_code', 'USD'),

                # Payment
                'payment_method': payment.get('method', ''),
                'payment_method_id': payment.get('method', ''),

                # Addresses
                'billing_address': self._map_address(
                    source_data.get('billing_address', {})
                ),
                'shipping_address': self._map_address(
                    shipping_info.get('address', {})
                ),

                # Line items
                'line_items': self._map_line_items(source_data.get('items', [])),

                # Shipping
                'shipping_lines': self._map_shipping_lines(shipping_info),

                # Notes
                'customer_note': source_data.get('customer_note', '') or '',

                # Dates
                'created_at': source_data.get('created_at'),
                'updated_at': source_data.get('updated_at'),
                'paid_at': None,  # Not directly available
                'completed_at': None,

                # Source tracking
                'source_id': str(source_data.get('entity_id')),
                'source_platform': 'magento',
                'source_data': {
                    'state': source_data.get('state'),
                    'status': source_data.get('status'),
                    'increment_id': source_data.get('increment_id'),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(
                f"Failed to map order: {e}",
                {
                    'entity_id': source_data.get('entity_id'),
                    'increment_id': source_data.get('increment_id'),
                }
            )
            raise

    def _map_address(self, address_data: Dict) -> Dict:
        """Map Magento order address format."""
        if not address_data:
            return {}

        street = address_data.get('street', [])
        if isinstance(street, str):
            street = [street]
        address_1 = street[0] if street else ''
        address_2 = street[1] if len(street) > 1 else ''

        return {
            'first_name': address_data.get('firstname') or '',
            'last_name': address_data.get('lastname') or '',
            'company': address_data.get('company') or '',
            'address_1': address_1,
            'address_2': address_2,
            'city': address_data.get('city') or '',
            'state': address_data.get('region_code') or address_data.get('region') or '',
            'postcode': address_data.get('postcode') or '',
            'country': address_data.get('country_id') or '',
            'phone': address_data.get('telephone') or '',
            'email': address_data.get('email') or '',
        }

    def _map_line_items(self, items: List[Dict]) -> List[Dict]:
        """Map Magento order items."""
        mapped_items = []
        for item in items:
            # Skip configurable parent items (they duplicate child simple items)
            if item.get('product_type') == 'configurable':
                continue

            mapped_items.append({
                'product_id': item.get('product_id'),
                'variation_id': 0,
                'name': item.get('name', ''),
                'sku': item.get('sku', ''),
                'quantity': int(item.get('qty_ordered', 1) or 1),
                'subtotal': self._parse_price(item.get('row_total', 0)),
                'total': self._parse_price(item.get('row_total_incl_tax', 0)),
                'tax_total': self._parse_price(item.get('tax_amount', 0)),
                'price': self._parse_price(item.get('price', 0)),
            })
        return mapped_items

    def _map_shipping_lines(self, shipping_info: Dict) -> List[Dict]:
        """Map Magento shipping method info."""
        if not shipping_info:
            return []

        method = shipping_info.get('method', '')
        if not method:
            return []

        return [{
            'method_id': method,
            'method_title': method.replace('_', ' ').title(),
            'total': None,  # Shipping total is on the order level
            'tax_total': None,
        }]

    def _parse_price(self, price) -> Optional[Decimal]:
        """Parse price to Decimal."""
        if price is None:
            return None
        try:
            return Decimal(str(price))
        except (ValueError, TypeError):
            self.log_warning(f"Failed to parse price: {price}")
            return None


class MagentoReviewMapper(BaseMapper):
    """Map Magento product reviews to internal format."""

    def map(self, source_data: Dict) -> Dict:
        """
        Map Magento review to internal format.

        Magento review:
        {
            "id": 1,
            "title": "Great product",
            "detail": "I love this product...",
            "nickname": "John D",
            "customer_id": null,
            "entity_pk_value": 42,
            "ratings": [{"percent": 80, "rating_name": "Quality"}],
            "review_status": 1,
            "created_at": "2024-01-15"
        }
        """
        try:
            mapped = {
                'title': source_data.get('title', ''),
                'content': source_data.get('detail', ''),
                'reviewer_name': source_data.get('nickname', ''),
                'rating': transform_magento_rating(source_data.get('ratings', [])),
                'product_external_id': str(source_data.get('entity_pk_value', '')),
                'is_approved': source_data.get('review_status') == 1,
                'created_at': source_data.get('created_at'),

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'magento',
                'source_data': {
                    'customer_id': source_data.get('customer_id'),
                    'review_type': source_data.get('review_type'),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map review: {e}", source_data)
            raise


class MagentoCouponMapper(BaseMapper):
    """Map Magento sales rules + coupons to internal VoucherCode model."""

    def map(self, source_data: Dict) -> Dict:
        """
        Map Magento sales rule + associated coupon to internal format.

        Expects combined data:
        {
            "sales_rule": {
                "rule_id": 1,
                "name": "Summer Sale",
                "description": "...",
                "from_date": "2024-06-01",
                "to_date": "2024-08-31",
                "is_active": true,
                "simple_action": "by_percent",
                "discount_amount": 10.00,
                "uses_per_customer": 1,
                "times_used": 5,
                "coupon_type": 2
            },
            "coupon": {
                "coupon_id": 1,
                "rule_id": 1,
                "code": "SUMMER10",
                "usage_limit": 100,
                "times_used": 5
            }
        }
        """
        try:
            rule = source_data.get('sales_rule', source_data)
            coupon = source_data.get('coupon', {})

            mapped = {
                'code': coupon.get('code', '') or rule.get('name', '').upper().replace(' ', ''),
                'discount_type': transform_magento_discount_type(
                    rule.get('simple_action', 'by_fixed')
                ),
                'discount_value': self._parse_price(rule.get('discount_amount', 0)),
                'description': rule.get('description', '') or rule.get('name', ''),
                'start_date': rule.get('from_date'),
                'end_date': rule.get('to_date'),
                'is_active': rule.get('is_active', False),
                'current_uses': coupon.get('times_used', 0) or rule.get('times_used', 0),
                'max_uses_total': coupon.get('usage_limit'),
                'max_uses_per_customer': rule.get('uses_per_customer'),

                # Source tracking
                'source_id': str(rule.get('rule_id')),
                'source_platform': 'magento',
                'source_data': {
                    'simple_action': rule.get('simple_action'),
                    'coupon_type': rule.get('coupon_type'),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map coupon: {e}", source_data)
            raise

    def _parse_price(self, price) -> Optional[Decimal]:
        """Parse price to Decimal."""
        if not price:
            return None
        try:
            return abs(Decimal(str(price)))
        except (ValueError, TypeError):
            return None


class MagentoCmsPageMapper(BaseMapper):
    """Map Magento CMS pages to internal BlogPost model."""

    def __init__(self, migration_job=None, store_url: str = ''):
        super().__init__(migration_job)
        self.store_url = store_url.rstrip('/')

    def map(self, source_data: Dict) -> Dict:
        """
        Map Magento CMS page to internal format.

        Magento CMS page:
        {
            "id": 1,
            "identifier": "about-us",
            "title": "About Us",
            "content": "<p>Content with {{media}} directives</p>",
            "content_heading": "About Our Store",
            "meta_title": "About Us",
            "meta_description": "...",
            "active": true,
            "creation_time": "2024-01-15 10:00:00",
            "update_time": "2024-06-15 14:00:00"
        }
        """
        try:
            raw_content = source_data.get('content', '')
            cleaned_content = clean_cms_directives(raw_content, self.store_url)

            mapped = {
                'title': source_data.get('title', ''),
                'slug': self.generate_slug(
                    source_data.get('identifier', '')
                    or source_data.get('title', '')
                ),
                'content': cleaned_content,
                'excerpt': source_data.get('content_heading', ''),
                'status': 'published' if source_data.get('active') else 'draft',
                'author_name': '',

                # Dates
                'created_at': source_data.get('creation_time'),
                'published_at': source_data.get('creation_time') if source_data.get('active') else None,

                # SEO
                'meta_title': source_data.get('meta_title', ''),
                'meta_description': source_data.get('meta_description', ''),

                # No tags or featured image in Magento CMS
                'tags': [],
                'featured_image_url': None,
                'featured_image_alt': '',

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'magento',
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map CMS page: {e}", source_data)
            raise
