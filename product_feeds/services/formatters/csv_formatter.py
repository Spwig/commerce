"""
CSV feed formatter for product feeds.

Generates CSV files compatible with Google Merchant Center and other providers.
"""

import csv
import io
from typing import Dict, Any, List, Optional, Iterator

from .base import BaseFeedFormatter, ProductFeedItem


class CSVFeedFormatter(BaseFeedFormatter):
    """
    CSV feed formatter.

    Generates tab-separated or comma-separated files compatible with:
    - Google Merchant Center
    - Microsoft Advertising
    - Many marketplaces (Amazon, eBay via bulk upload)
    """

    format_name = 'csv'
    content_type = 'text/csv; charset=utf-8'
    file_extension = 'csv'

    # Standard column headers matching Google Merchant Center specification
    DEFAULT_COLUMNS = [
        'id',
        'title',
        'description',
        'link',
        'image_link',
        'additional_image_link',
        'availability',
        'price',
        'sale_price',
        'sale_price_effective_date',
        'google_product_category',
        'product_type',
        'brand',
        'gtin',
        'mpn',
        'identifier_exists',
        'condition',
        'adult',
        'age_group',
        'color',
        'gender',
        'material',
        'pattern',
        'size',
        'size_type',
        'size_system',
        'item_group_id',
        'shipping',
        'tax',
        'custom_label_0',
        'custom_label_1',
        'custom_label_2',
        'custom_label_3',
        'custom_label_4',
    ]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.delimiter = self.config.get('delimiter', '\t')  # Tab by default for Google
        self.quoting = self.config.get('quoting', csv.QUOTE_MINIMAL)
        self.columns = self.config.get('columns', self.DEFAULT_COLUMNS)
        self.include_header = self.config.get('include_header', True)

    def format_feed(self, items: List[ProductFeedItem], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Format products as CSV/TSV.

        Args:
            items: List of ProductFeedItem objects
            metadata: Ignored for CSV format

        Returns:
            CSV content string
        """
        output = io.StringIO()
        writer = csv.writer(
            output,
            delimiter=self.delimiter,
            quoting=self.quoting,
            lineterminator='\n'
        )

        # Write header row
        if self.include_header:
            writer.writerow(self.columns)

        # Write product rows
        for item in items:
            row = self._item_to_row(item)
            writer.writerow(row)

        return output.getvalue()

    def format_item(self, item: ProductFeedItem) -> str:
        """
        Format a single product as CSV row.

        Args:
            item: ProductFeedItem to format

        Returns:
            Single CSV row string
        """
        output = io.StringIO()
        writer = csv.writer(
            output,
            delimiter=self.delimiter,
            quoting=self.quoting,
            lineterminator='\n'
        )
        row = self._item_to_row(item)
        writer.writerow(row)
        return output.getvalue().rstrip('\n')

    def _item_to_row(self, item: ProductFeedItem) -> List[str]:
        """
        Convert ProductFeedItem to list of column values.

        Args:
            item: ProductFeedItem to convert

        Returns:
            List of string values matching column order
        """
        # Build additional_image_link value (comma-separated)
        additional_images = ','.join(item.additional_image_links[:10]) if item.additional_image_links else ''

        # Determine identifier_exists
        identifier_exists = 'yes' if (item.gtin or item.mpn) else 'no'

        # Map item fields to columns
        field_mapping = {
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'link': item.link,
            'image_link': item.image_link,
            'additional_image_link': additional_images,
            'availability': item.availability,
            'price': item.price,
            'sale_price': item.sale_price,
            'sale_price_effective_date': item.sale_price_effective_date,
            'google_product_category': item.google_product_category,
            'product_type': item.product_type,
            'brand': item.brand,
            'gtin': item.gtin,
            'mpn': item.mpn,
            'identifier_exists': identifier_exists,
            'condition': item.condition,
            'adult': 'yes' if item.adult else '',
            'age_group': item.age_group,
            'color': item.color,
            'gender': item.gender,
            'material': item.material,
            'pattern': item.pattern,
            'size': item.size,
            'size_type': item.size_type,
            'size_system': item.size_system,
            'item_group_id': item.item_group_id,
            'shipping': item.shipping,
            'tax': item.tax,
            'custom_label_0': item.custom_label_0,
            'custom_label_1': item.custom_label_1,
            'custom_label_2': item.custom_label_2,
            'custom_label_3': item.custom_label_3,
            'custom_label_4': item.custom_label_4,
        }

        # Build row in column order
        row = []
        for col in self.columns:
            value = field_mapping.get(col, '')
            # Also check custom_attributes
            if not value and item.custom_attributes:
                value = item.custom_attributes.get(col, '')
            row.append(self.escape_text(str(value) if value else ''))

        return row

    def escape_text(self, text: str) -> str:
        """
        Escape text for CSV content.

        CSV library handles most escaping, but we clean up newlines.

        Args:
            text: Text to escape

        Returns:
            Escaped text
        """
        if not text:
            return ""
        # Replace newlines with spaces for CSV compatibility
        return text.replace('\n', ' ').replace('\r', ' ')

    def stream_feed(self, items: Iterator[ProductFeedItem], metadata: Optional[Dict[str, Any]] = None) -> Iterator[str]:
        """
        Stream CSV feed for large product catalogs.

        Yields:
            CSV content chunks (header + rows)
        """
        # Yield header
        if self.include_header:
            output = io.StringIO()
            writer = csv.writer(
                output,
                delimiter=self.delimiter,
                quoting=self.quoting,
                lineterminator='\n'
            )
            writer.writerow(self.columns)
            yield output.getvalue()

        # Yield each row
        for item in items:
            yield self.format_item(item) + '\n'

    def get_content_type(self) -> str:
        """Get MIME type based on delimiter."""
        if self.delimiter == '\t':
            return 'text/tab-separated-values; charset=utf-8'
        return 'text/csv; charset=utf-8'

    def get_file_extension(self) -> str:
        """Get file extension based on delimiter."""
        if self.delimiter == '\t':
            return 'tsv'
        return 'csv'
