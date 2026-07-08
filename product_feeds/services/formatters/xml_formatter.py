"""
XML/RSS feed formatter for Google Merchant Center and compatible providers.

Generates RSS 2.0 with Google namespace extensions.
"""

from typing import Dict, Any, List, Optional, Iterator
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import html
from datetime import datetime

from .base import BaseFeedFormatter, ProductFeedItem


class XMLFeedFormatter(BaseFeedFormatter):
    """
    XML/RSS 2.0 feed formatter with Google namespace support.

    Compatible with:
    - Google Merchant Center
    - Microsoft Advertising (Bing Shopping)
    - Meta (Facebook/Instagram Shops)
    - Pinterest
    - Many others that accept Google Shopping format
    """

    format_name = 'xml'
    content_type = 'application/xml; charset=utf-8'
    file_extension = 'xml'

    # Google namespace
    GOOGLE_NS = "http://base.google.com/ns/1.0"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.pretty_print = self.config.get('pretty_print', True)
        self.include_namespace = self.config.get('include_namespace', True)

    def format_feed(self, items: List[ProductFeedItem], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Format products as RSS 2.0 XML feed.

        Args:
            items: List of ProductFeedItem objects
            metadata: Feed metadata (title, description, link)

        Returns:
            XML feed string
        """
        metadata = metadata or {}

        # Create root RSS element
        rss = Element('rss', {
            'version': '2.0',
            'xmlns:g': self.GOOGLE_NS
        })

        # Create channel
        channel = SubElement(rss, 'channel')

        # Add channel metadata
        title = SubElement(channel, 'title')
        title.text = metadata.get('title', 'Product Feed')

        link = SubElement(channel, 'link')
        link.text = metadata.get('link', '')

        description = SubElement(channel, 'description')
        description.text = metadata.get('description', 'Product catalog feed')

        # Add items
        for item in items:
            item_element = self._create_item_element(item)
            channel.append(item_element)

        # Convert to string
        xml_string = tostring(rss, encoding='unicode')

        if self.pretty_print:
            # Pretty print with proper indentation
            dom = minidom.parseString(xml_string)
            xml_string = dom.toprettyxml(indent='  ', encoding=None)
            # Remove extra XML declaration if present
            if xml_string.startswith('<?xml'):
                xml_string = xml_string.split('\n', 1)[1] if '\n' in xml_string else xml_string

        # Add XML declaration
        return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_string}'

    def format_item(self, item: ProductFeedItem) -> str:
        """
        Format a single product as XML item element.

        Args:
            item: ProductFeedItem to format

        Returns:
            XML string for single item
        """
        item_element = self._create_item_element(item)
        xml_string = tostring(item_element, encoding='unicode')

        if self.pretty_print:
            dom = minidom.parseString(xml_string)
            return dom.toprettyxml(indent='  ', encoding=None)

        return xml_string

    def _create_item_element(self, item: ProductFeedItem) -> Element:
        """
        Create XML Element for a product item.

        Args:
            item: ProductFeedItem to convert

        Returns:
            XML Element
        """
        item_elem = Element('item')

        # Standard RSS fields
        self._add_element(item_elem, 'title', item.title)
        self._add_element(item_elem, 'link', item.link)
        self._add_element(item_elem, 'description', item.description)

        # Google namespace fields (g:*)
        self._add_g_element(item_elem, 'id', item.id)
        self._add_g_element(item_elem, 'image_link', item.image_link)
        self._add_g_element(item_elem, 'price', item.price)
        self._add_g_element(item_elem, 'availability', item.availability)
        self._add_g_element(item_elem, 'condition', item.condition)

        # Category & Brand
        if item.product_type:
            self._add_g_element(item_elem, 'product_type', item.product_type)
        if item.google_product_category:
            self._add_g_element(item_elem, 'google_product_category', item.google_product_category)
        if item.brand:
            self._add_g_element(item_elem, 'brand', item.brand)

        # Identifiers
        if item.gtin:
            self._add_g_element(item_elem, 'gtin', item.gtin)
        if item.mpn:
            self._add_g_element(item_elem, 'mpn', item.mpn)

        # If no GTIN/MPN, set identifier_exists to false
        if not item.gtin and not item.mpn:
            self._add_g_element(item_elem, 'identifier_exists', 'false')

        # Pricing
        if item.sale_price:
            self._add_g_element(item_elem, 'sale_price', item.sale_price)
        if item.sale_price_effective_date:
            self._add_g_element(item_elem, 'sale_price_effective_date', item.sale_price_effective_date)

        # Product details
        if item.adult:
            self._add_g_element(item_elem, 'adult', 'yes')
        if item.age_group:
            self._add_g_element(item_elem, 'age_group', item.age_group)
        if item.color:
            self._add_g_element(item_elem, 'color', item.color)
        if item.gender:
            self._add_g_element(item_elem, 'gender', item.gender)
        if item.material:
            self._add_g_element(item_elem, 'material', item.material)
        if item.pattern:
            self._add_g_element(item_elem, 'pattern', item.pattern)
        if item.size:
            self._add_g_element(item_elem, 'size', item.size)
        if item.size_type:
            self._add_g_element(item_elem, 'size_type', item.size_type)
        if item.size_system:
            self._add_g_element(item_elem, 'size_system', item.size_system)
        if item.item_group_id:
            self._add_g_element(item_elem, 'item_group_id', item.item_group_id)

        # Shipping & Tax
        if item.shipping:
            self._add_g_element(item_elem, 'shipping', item.shipping)
        if item.tax:
            self._add_g_element(item_elem, 'tax', item.tax)

        # Additional images
        for img_link in item.additional_image_links[:10]:  # Max 10 images
            self._add_g_element(item_elem, 'additional_image_link', img_link)

        # Custom labels
        if item.custom_label_0:
            self._add_g_element(item_elem, 'custom_label_0', item.custom_label_0)
        if item.custom_label_1:
            self._add_g_element(item_elem, 'custom_label_1', item.custom_label_1)
        if item.custom_label_2:
            self._add_g_element(item_elem, 'custom_label_2', item.custom_label_2)
        if item.custom_label_3:
            self._add_g_element(item_elem, 'custom_label_3', item.custom_label_3)
        if item.custom_label_4:
            self._add_g_element(item_elem, 'custom_label_4', item.custom_label_4)

        return item_elem

    def _add_element(self, parent: Element, tag: str, text: str) -> None:
        """Add a standard element if text is not empty."""
        if text:
            elem = SubElement(parent, tag)
            elem.text = self.escape_text(text)

    def _add_g_element(self, parent: Element, tag: str, text: str) -> None:
        """Add a Google namespace element if text is not empty."""
        if text:
            elem = SubElement(parent, f'g:{tag}')
            elem.text = self.escape_text(text)

    def escape_text(self, text: str) -> str:
        """
        Escape text for XML content.

        Args:
            text: Text to escape

        Returns:
            XML-escaped text
        """
        if not text:
            return ""
        # html.escape handles &, <, >, " and '
        return html.escape(str(text), quote=False)

    def stream_feed(self, items: Iterator[ProductFeedItem], metadata: Optional[Dict[str, Any]] = None) -> Iterator[str]:
        """
        Stream XML feed for large product catalogs.

        Yields:
            XML content chunks
        """
        metadata = metadata or {}

        # Yield XML declaration and opening tags
        yield '<?xml version="1.0" encoding="UTF-8"?>\n'
        yield f'<rss version="2.0" xmlns:g="{self.GOOGLE_NS}">\n'
        yield '  <channel>\n'
        yield f'    <title>{self.escape_text(metadata.get("title", "Product Feed"))}</title>\n'
        yield f'    <link>{self.escape_text(metadata.get("link", ""))}</link>\n'
        yield f'    <description>{self.escape_text(metadata.get("description", "Product catalog feed"))}</description>\n'

        # Yield items
        for item in items:
            item_xml = self.format_item(item)
            # Indent for readability
            indented = '\n'.join('    ' + line for line in item_xml.split('\n') if line.strip())
            yield indented + '\n'

        # Yield closing tags
        yield '  </channel>\n'
        yield '</rss>'
