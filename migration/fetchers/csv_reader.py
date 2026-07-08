"""
CSV Data Reader
Reads uploaded CSV files and returns data in WooCommerce-compatible format
for use with the ImportExecutor. Supports flexible column mapping.
"""
import csv
import logging
from typing import Dict, List, Optional

from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


class CSVDataReader:
    """
    Reads CSV files and returns data in a format compatible with the
    ImportExecutor's _import_single_* methods.

    Column mappings (set in step4) tell the reader which CSV column maps
    to which expected field. The reader then transforms expected field names
    to WooCommerce-compatible keys that the executor understands.
    """

    # Expected fields per data type (matching our CSV templates)
    EXPECTED_FIELDS = {
        'products': ['id', 'name', 'slug', 'description', 'price', 'sku', 'stock_quantity', 'category'],
        'categories': ['id', 'name', 'slug', 'description', 'parent_id'],
        'customers': ['id', 'email', 'first_name', 'last_name', 'phone'],
        'orders': ['id', 'customer_email', 'order_date', 'status', 'total', 'currency'],
        'reviews': ['id', 'product_id', 'customer_email', 'rating', 'comment', 'date'],
    }

    # Map our expected field names -> WooCommerce-compatible keys used by executor
    FIELD_TO_WOO = {
        'products': {
            'price': 'regular_price',
            'category': '_csv_category_name',
        },
        'categories': {
            'parent_id': 'parent',
        },
        'customers': {
            # first_name, last_name, email match WooCommerce format already
        },
        'orders': {
            'order_date': 'date_created',
            'customer_email': '_csv_customer_email',
        },
        'reviews': {
            'customer_email': 'reviewer_email',
            'comment': 'review',
            'date': 'date_created',
        },
    }

    # Common aliases for fuzzy auto-detection of column mappings
    FIELD_ALIASES = {
        'id': ['id', 'identifier', 'item_id', 'product_id', 'category_id', 'customer_id', 'order_id', 'review_id', '#'],
        'name': ['name', 'title', 'product_name', 'product_title', 'item_name', 'category_name'],
        'slug': ['slug', 'url_slug', 'handle', 'permalink', 'url_key'],
        'description': ['description', 'desc', 'body', 'content', 'product_description', 'long_description', 'body_html'],
        'price': ['price', 'regular_price', 'unit_price', 'sale_price', 'base_price', 'amount'],
        'sku': ['sku', 'sku_code', 'product_sku', 'item_sku', 'barcode', 'item_number', 'part_number'],
        'stock_quantity': ['stock_quantity', 'stock', 'quantity', 'qty', 'inventory', 'in_stock', 'stock_level'],
        'category': ['category', 'category_name', 'product_category', 'type', 'collection'],
        'parent_id': ['parent_id', 'parent', 'parent_category', 'parent_category_id'],
        'email': ['email', 'email_address', 'customer_email', 'e_mail', 'user_email'],
        'first_name': ['first_name', 'firstname', 'given_name', 'fname'],
        'last_name': ['last_name', 'lastname', 'family_name', 'surname', 'lname'],
        'phone': ['phone', 'phone_number', 'telephone', 'mobile', 'tel'],
        'customer_email': ['customer_email', 'email', 'buyer_email', 'billing_email'],
        'order_date': ['order_date', 'date', 'created_at', 'date_created', 'order_created', 'placed_at'],
        'status': ['status', 'order_status', 'state'],
        'total': ['total', 'order_total', 'grand_total', 'amount', 'total_amount'],
        'currency': ['currency', 'currency_code'],
        'product_id': ['product_id', 'product', 'item_id'],
        'rating': ['rating', 'score', 'stars', 'review_rating'],
        'comment': ['comment', 'review', 'review_text', 'body', 'content', 'text', 'message'],
        'date': ['date', 'created_at', 'review_date', 'posted_at', 'timestamp'],
    }

    def __init__(self, csv_files_config: dict, column_mappings: Optional[dict] = None):
        """
        Args:
            csv_files_config: {type: {path: str, headers: list}} from connection_config
            column_mappings: {type: {csv_header: expected_field}} from step4
        """
        self.csv_files = csv_files_config
        self.column_mappings = column_mappings or {}
        self._cache = {}

    def get_total_counts(self) -> Dict[str, int]:
        """Get row counts for each CSV file (excluding header)."""
        counts = {}
        for file_type, file_info in self.csv_files.items():
            data = self._read_csv_raw(file_type)
            counts[file_type] = len(data)
        return counts

    def fetch_products(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        return self._fetch_page('products', page, per_page)

    def fetch_categories(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        return self._fetch_page('categories', page, per_page)

    def fetch_customers(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        return self._fetch_page('customers', page, per_page)

    def fetch_orders(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        return self._fetch_page('orders', page, per_page)

    def fetch_reviews(self, page: int = 1, per_page: int = 100) -> List[Dict]:
        return self._fetch_page('reviews', page, per_page)

    def _fetch_page(self, file_type: str, page: int, per_page: int) -> List[Dict]:
        """Fetch a page of data from a CSV file, returning WooCommerce-compatible dicts."""
        if file_type not in self.csv_files:
            return []

        all_data = self._read_and_transform(file_type)

        # Paginate
        start = (page - 1) * per_page
        end = start + per_page
        return all_data[start:end]

    def _read_csv_raw(self, file_type: str) -> List[Dict]:
        """Read CSV file and return list of dicts with original headers."""
        cache_key = f'raw_{file_type}'
        if cache_key in self._cache:
            return self._cache[cache_key]

        file_info = self.csv_files.get(file_type)
        if not file_info:
            return []

        file_path = file_info['path']
        rows = []

        try:
            with default_storage.open(file_path, 'rb') as f:
                content = f.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8-sig')

                reader = csv.DictReader(content.splitlines())
                for row in reader:
                    # Strip whitespace from keys and values
                    cleaned = {k.strip(): v.strip() if v else '' for k, v in row.items() if k}
                    rows.append(cleaned)
        except Exception as e:
            logger.error(f"Failed to read CSV file {file_path}: {e}")

        self._cache[cache_key] = rows
        return rows

    def _read_and_transform(self, file_type: str) -> List[Dict]:
        """Read CSV and transform columns using mappings, then to WooCommerce format."""
        cache_key = f'transformed_{file_type}'
        if cache_key in self._cache:
            return self._cache[cache_key]

        raw_rows = self._read_csv_raw(file_type)
        col_mapping = self.column_mappings.get(file_type, {})
        woo_mapping = self.FIELD_TO_WOO.get(file_type, {})

        transformed = []
        for raw_row in raw_rows:
            woo_row = {}

            for csv_header, value in raw_row.items():
                # Step 1: Map CSV header -> expected field name
                expected_field = col_mapping.get(csv_header)

                if not expected_field or expected_field == '__skip__':
                    # No mapping — try direct match (header already matches expected field)
                    if expected_field == '__skip__':
                        continue
                    expected_field = csv_header

                # Step 2: Map expected field -> WooCommerce key
                woo_key = woo_mapping.get(expected_field, expected_field)
                woo_row[woo_key] = value

            # Add type-specific defaults/transformations
            if file_type == 'products':
                self._transform_product_row(woo_row)
            elif file_type == 'categories':
                self._transform_category_row(woo_row)
            elif file_type == 'orders':
                self._transform_order_row(woo_row)

            transformed.append(woo_row)

        self._cache[cache_key] = transformed
        return transformed

    def _transform_product_row(self, row: dict):
        """Add WooCommerce-compatible defaults for product rows."""
        # Ensure id exists
        if 'id' not in row:
            row['id'] = row.get('sku', '')

        # Build categories list from category name
        cat_name = row.pop('_csv_category_name', '')
        if cat_name:
            row['categories'] = [{'name': cat_name}]
        else:
            row.setdefault('categories', [])

        # Set product type (CSV imports are simple products)
        row.setdefault('type', 'simple')

        # Ensure manage_stock is set if stock_quantity present
        if row.get('stock_quantity'):
            row['manage_stock'] = True

    def _transform_category_row(self, row: dict):
        """Add WooCommerce-compatible defaults for category rows."""
        # Ensure parent is int-like for parent resolution
        parent = row.get('parent', '')
        if parent:
            try:
                row['parent'] = int(parent)
            except (ValueError, TypeError):
                row['parent'] = 0
        else:
            row['parent'] = 0

    def _transform_order_row(self, row: dict):
        """Add WooCommerce-compatible defaults for order rows."""
        # Map customer email into billing dict (executor looks for billing.email)
        email = row.pop('_csv_customer_email', '')
        if email:
            row.setdefault('billing', {})
            row['billing']['email'] = email

        # Ensure customer_id is 0 (guest) so executor creates from email
        row.setdefault('customer_id', 0)

    @classmethod
    def auto_detect_mappings(cls, csv_headers: List[str], file_type: str) -> Dict[str, str]:
        """
        Auto-detect column mappings by fuzzy matching CSV headers to expected fields.

        Returns: {csv_header: expected_field_name} for each matched header
        """
        expected_fields = cls.EXPECTED_FIELDS.get(file_type, [])
        mappings = {}
        used_fields = set()

        for header in csv_headers:
            normalized = header.lower().strip().replace(' ', '_').replace('-', '_')

            # Try exact match to expected field names first
            if normalized in expected_fields and normalized not in used_fields:
                mappings[header] = normalized
                used_fields.add(normalized)
                continue

            # Try alias matching
            matched = False
            for field_name in expected_fields:
                if field_name in used_fields:
                    continue
                aliases = cls.FIELD_ALIASES.get(field_name, [])
                if normalized in aliases:
                    mappings[header] = field_name
                    used_fields.add(field_name)
                    matched = True
                    break

            if not matched:
                # No match — will be skipped unless user maps it in step4
                mappings[header] = '__skip__'

        return mappings
