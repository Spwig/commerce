"""
WooCommerce Data Mappers
Transform WooCommerce API data to internal platform format
"""
from typing import Dict, List, Optional
from decimal import Decimal
from .base import BaseMapper
import logging

logger = logging.getLogger(__name__)


class WooCommerceCategoryMapper(BaseMapper):
    """Map WooCommerce categories to internal Category model"""

    def map(self, source_data: Dict) -> Dict:
        """
        Map WooCommerce category to internal format

        WooCommerce category structure:
        {
            "id": 9,
            "name": "Clothing",
            "slug": "clothing",
            "parent": 0,
            "description": "Category description",
            "display": "default",
            "image": {
                "id": 30,
                "src": "http://example.com/image.jpg",
                "name": "image.jpg",
                "alt": "Image alt text"
            },
            "menu_order": 0,
            "count": 36
        }
        """
        try:
            mapped = {
                # Basic fields
                'name': source_data.get('name', ''),
                'slug': self.generate_slug(source_data.get('slug', '') or source_data.get('name', '')),
                'description': self.parse_html(source_data.get('description', '')),

                # Hierarchy
                'parent_id': source_data.get('parent', 0),  # Will be resolved later

                # Display
                'sort_order': source_data.get('menu_order', 0),
                'is_active': True,  # WooCommerce doesn't have an active field
                'is_featured': False,

                # SEO
                'meta_title': '',
                'meta_description': source_data.get('description', '')[:255] if source_data.get('description') else '',

                # Image
                'image_url': self.safe_get(source_data, 'image', 'src'),
                'image_alt': self.safe_get(source_data, 'image', 'alt', default=''),

                # Display settings (using defaults)
                'page_template': self._map_page_template(source_data.get('display', 'default')),
                'products_per_page': 24,
                'show_subcategories': True,

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'woocommerce',
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map category: {e}", source_data)
            raise

    def _map_page_template(self, wc_display: str) -> str:
        """Map WooCommerce display types to internal page templates"""
        mapping = {
            'default': 'grid',
            'products': 'grid',
            'subcategories': 'grid',
            'both': 'grid',
        }
        return mapping.get(wc_display, 'grid')


class WooCommerceProductMapper(BaseMapper):
    """Map WooCommerce products to internal Product model"""

    def map(self, source_data: Dict) -> Dict:
        """
        Map WooCommerce product to internal format

        WooCommerce product structure is complex with many fields.
        We map the most important ones for a standard e-commerce platform.
        """
        try:
            mapped = {
                # Basic information
                'name': source_data.get('name', ''),
                'slug': self.generate_slug(source_data.get('slug', '') or source_data.get('name', '')),
                'sku': source_data.get('sku', ''),

                # Product type
                'product_type': self._map_product_type(source_data.get('type', 'simple')),

                # Descriptions
                'full_description': self.parse_html(source_data.get('description', '')),
                'short_description': self.parse_html(source_data.get('short_description', ''))[:500],

                # Pricing
                'price': self._parse_price(source_data.get('price')),
                'regular_price': self._parse_price(source_data.get('regular_price')),
                'sale_price': self._parse_price(source_data.get('sale_price')),

                # Categories
                'category_ids': [cat['id'] for cat in source_data.get('categories', [])],
                'primary_category_id': source_data.get('categories', [{}])[0].get('id') if source_data.get('categories') else None,

                # Inventory
                'track_inventory': source_data.get('manage_stock', False),
                'stock_quantity': int(source_data.get('stock_quantity', 0)) if source_data.get('stock_quantity') else 0,
                'allow_backorders': source_data.get('backorders', 'no') != 'no',
                'low_stock_threshold': int(source_data.get('low_stock_amount', 5)) if source_data.get('low_stock_amount') else 5,

                # Physical attributes
                'weight': self._parse_decimal(source_data.get('weight')),
                'length': self._parse_decimal(source_data.get('dimensions', {}).get('length')),
                'width': self._parse_decimal(source_data.get('dimensions', {}).get('width')),
                'height': self._parse_decimal(source_data.get('dimensions', {}).get('height')),

                # Status
                'status': self._map_status(source_data.get('status', 'publish')),
                'is_featured': source_data.get('featured', False),
                'is_digital': source_data.get('virtual', False) or source_data.get('downloadable', False),

                # SEO
                'meta_title': source_data.get('name', ''),
                'meta_description': source_data.get('short_description', '')[:255] if source_data.get('short_description') else '',

                # Images
                'images': self._map_images(source_data.get('images', [])),

                # Attributes and specifications
                'attributes': self._map_attributes(source_data.get('attributes', [])),
                'specifications': {},

                # Variations (for variable products)
                'has_variations': len(source_data.get('variations', [])) > 0,
                'variation_ids': source_data.get('variations', []),

                # Tags
                'tags': [tag['name'] for tag in source_data.get('tags', [])],

                # Reviews
                'reviews_allowed': source_data.get('reviews_allowed', True),
                'average_rating': float(source_data.get('average_rating', 0)),
                'rating_count': int(source_data.get('rating_count', 0)),

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'woocommerce',
                'source_data': {
                    'permalink': source_data.get('permalink'),
                    'date_created': source_data.get('date_created'),
                    'date_modified': source_data.get('date_modified'),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map product: {e}", {'id': source_data.get('id'), 'name': source_data.get('name')})
            raise

    def _map_product_type(self, wc_type: str) -> str:
        """Map WooCommerce product types including extension types"""
        mapping = {
            # Core types
            'simple': 'simple',
            'variable': 'variable',
            'grouped': 'bundle',
            'external': 'simple',
            'virtual': 'digital',
            # Extension types
            'subscription': 'simple',
            'variable-subscription': 'variable',
            'bundle': 'bundle',
            'composite': 'configurable',
            'booking': 'simple',
            'accommodation-booking': 'simple',
        }
        return mapping.get(wc_type, 'simple')

    def _map_status(self, wc_status: str) -> str:
        """Map WooCommerce status to internal status"""
        mapping = {
            'publish': 'published',
            'draft': 'draft',
            'pending': 'draft',
            'private': 'draft',
        }
        return mapping.get(wc_status, 'draft')

    def _parse_price(self, price: any) -> Optional[Decimal]:
        """Parse price to Decimal"""
        if not price:
            return None

        try:
            return Decimal(str(price))
        except (ValueError, TypeError):
            self.log_warning(f"Failed to parse price: {price}")
            return None

    def _parse_decimal(self, value: any) -> Optional[Decimal]:
        """Parse decimal value"""
        if not value:
            return None

        try:
            return Decimal(str(value))
        except (ValueError, TypeError):
            return None

    def _map_images(self, wc_images: List[Dict]) -> List[Dict]:
        """Map WooCommerce images"""
        mapped_images = []

        for idx, img in enumerate(wc_images):
            mapped_images.append({
                'src': img.get('src'),
                'name': img.get('name', ''),
                'alt_text': img.get('alt', ''),
                'position': idx,
                'is_primary': idx == 0,
            })

        return mapped_images

    def _map_attributes(self, wc_attributes: List[Dict]) -> Dict:
        """Map WooCommerce attributes to key-value pairs"""
        attributes = {}

        for attr in wc_attributes:
            name = attr.get('name', '')
            options = attr.get('options', [])

            if name and options:
                # Join options if multiple values
                attributes[name] = ', '.join([str(opt) for opt in options])

        return attributes


class WooCommerceCustomerMapper(BaseMapper):
    """Map WooCommerce customers to internal User/Customer model"""

    def map(self, source_data: Dict) -> Dict:
        """
        Map WooCommerce customer to internal format

        WooCommerce customer structure:
        {
            "id": 25,
            "email": "customer@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "billing": {...},
            "shipping": {...}
        }
        """
        try:
            mapped = {
                # User fields
                'email': source_data.get('email', ''),
                'username': source_data.get('username', '') or source_data.get('email', '').split('@')[0],
                'first_name': source_data.get('first_name', ''),
                'last_name': source_data.get('last_name', ''),

                # Customer profile
                'is_active': True,

                # Addresses
                'billing_address': self._map_address(source_data.get('billing', {}), 'billing'),
                'shipping_address': self._map_address(source_data.get('shipping', {}), 'shipping'),

                # Metadata
                'total_orders': source_data.get('orders_count', 0),
                'total_spent': self._parse_price(source_data.get('total_spent', 0)),

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'woocommerce',
                'source_data': {
                    'date_created': source_data.get('date_created'),
                    'date_modified': source_data.get('date_modified'),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map customer: {e}", {'id': source_data.get('id'), 'email': source_data.get('email')})
            raise

    def _map_address(self, address_data: Dict, address_type: str) -> Dict:
        """Map WooCommerce address format"""
        if not address_data:
            return {}

        return {
            'first_name': address_data.get('first_name', ''),
            'last_name': address_data.get('last_name', ''),
            'company': address_data.get('company', ''),
            'address_1': address_data.get('address_1', ''),
            'address_2': address_data.get('address_2', ''),
            'city': address_data.get('city', ''),
            'state': address_data.get('state', ''),
            'postcode': address_data.get('postcode', ''),
            'country': address_data.get('country', ''),
            'phone': address_data.get('phone', ''),
            'email': address_data.get('email', ''),
        }


class WooCommerceOrderMapper(BaseMapper):
    """Map WooCommerce orders to internal Order model"""

    def map(self, source_data: Dict) -> Dict:
        """
        Map WooCommerce order to internal format

        WooCommerce order structure is complex with line items, shipping, tax, etc.
        """
        try:
            mapped = {
                # Order identification
                'order_number': source_data.get('number', str(source_data.get('id'))),

                # Customer
                'customer_id': source_data.get('customer_id', 0),
                'customer_email': source_data.get('billing', {}).get('email', ''),

                # Status
                'status': self._map_order_status(source_data.get('status', 'pending')),
                'payment_status': self._map_payment_status(source_data.get('status', 'pending')),

                # Amounts
                'subtotal': self._parse_price(source_data.get('total', 0)),
                'discount_total': self._parse_price(source_data.get('discount_total', 0)),
                'shipping_total': self._parse_price(source_data.get('shipping_total', 0)),
                'tax_total': self._parse_price(source_data.get('total_tax', 0)),
                'total': self._parse_price(source_data.get('total', 0)),

                # Currency
                'currency': source_data.get('currency', 'USD'),

                # Payment
                'payment_method': source_data.get('payment_method_title', ''),
                'payment_method_id': source_data.get('payment_method', ''),

                # Addresses
                'billing_address': self._map_address(source_data.get('billing', {})),
                'shipping_address': self._map_address(source_data.get('shipping', {})),

                # Line items
                'line_items': self._map_line_items(source_data.get('line_items', [])),

                # Shipping
                'shipping_lines': self._map_shipping_lines(source_data.get('shipping_lines', [])),

                # Notes
                'customer_note': source_data.get('customer_note', ''),

                # Dates
                'created_at': source_data.get('date_created'),
                'updated_at': source_data.get('date_modified'),
                'paid_at': source_data.get('date_paid'),
                'completed_at': source_data.get('date_completed'),

                # Source tracking
                'source_id': str(source_data.get('id')),
                'source_platform': 'woocommerce',
                'source_data': {
                    'order_key': source_data.get('order_key'),
                    'transaction_id': source_data.get('transaction_id'),
                },
            }

            return mapped

        except Exception as e:
            self.log_error(f"Failed to map order: {e}", {'id': source_data.get('id'), 'number': source_data.get('number')})
            raise

    def _map_order_status(self, wc_status: str) -> str:
        """Map WooCommerce order status"""
        mapping = {
            'pending': 'pending',
            'processing': 'processing',
            'on-hold': 'on_hold',
            'completed': 'completed',
            'cancelled': 'cancelled',
            'refunded': 'refunded',
            'failed': 'failed',
        }
        return mapping.get(wc_status, 'pending')

    def _map_payment_status(self, wc_status: str) -> str:
        """Map to payment status"""
        mapping = {
            'pending': 'pending',
            'processing': 'paid',
            'on-hold': 'pending',
            'completed': 'paid',
            'cancelled': 'cancelled',
            'refunded': 'refunded',
            'failed': 'failed',
        }
        return mapping.get(wc_status, 'pending')

    def _map_address(self, address_data: Dict) -> Dict:
        """Map address format"""
        if not address_data:
            return {}

        return {
            'first_name': address_data.get('first_name', ''),
            'last_name': address_data.get('last_name', ''),
            'company': address_data.get('company', ''),
            'address_1': address_data.get('address_1', ''),
            'address_2': address_data.get('address_2', ''),
            'city': address_data.get('city', ''),
            'state': address_data.get('state', ''),
            'postcode': address_data.get('postcode', ''),
            'country': address_data.get('country', ''),
            'phone': address_data.get('phone', ''),
            'email': address_data.get('email', ''),
        }

    def _map_line_items(self, line_items: List[Dict]) -> List[Dict]:
        """Map order line items"""
        mapped_items = []

        for item in line_items:
            mapped_items.append({
                'product_id': item.get('product_id'),
                'variation_id': item.get('variation_id', 0),
                'name': item.get('name', ''),
                'sku': item.get('sku', ''),
                'quantity': item.get('quantity', 1),
                'subtotal': self._parse_price(item.get('subtotal', 0)),
                'total': self._parse_price(item.get('total', 0)),
                'tax_total': self._parse_price(item.get('total_tax', 0)),
                'price': self._parse_price(item.get('price', 0)),
            })

        return mapped_items

    def _map_shipping_lines(self, shipping_lines: List[Dict]) -> List[Dict]:
        """Map shipping lines"""
        mapped_shipping = []

        for line in shipping_lines:
            mapped_shipping.append({
                'method_id': line.get('method_id', ''),
                'method_title': line.get('method_title', ''),
                'total': self._parse_price(line.get('total', 0)),
                'tax_total': self._parse_price(line.get('total_tax', 0)),
            })

        return mapped_shipping
