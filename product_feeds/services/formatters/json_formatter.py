"""
JSON feed formatter for product feeds.

Generates JSON feeds compatible with various providers.
"""

import json
from collections.abc import Iterator
from typing import Any

from .base import BaseFeedFormatter, ProductFeedItem


class JSONFeedFormatter(BaseFeedFormatter):
    """
    JSON feed formatter.

    Generates JSON feeds compatible with:
    - Meta (Facebook/Instagram) Catalog API
    - Various marketplaces with JSON import
    - Custom integrations
    """

    format_name = "json"
    content_type = "application/json; charset=utf-8"
    file_extension = "json"

    def __init__(self, config: dict[str, Any] | None = None):
        super().__init__(config)
        self.pretty_print = self.config.get("pretty_print", True)
        self.indent = self.config.get("indent", 2)
        self.include_metadata = self.config.get("include_metadata", True)
        self.output_format = self.config.get("output_format", "google")  # 'google' or 'meta'

    def format_feed(
        self, items: list[ProductFeedItem], metadata: dict[str, Any] | None = None
    ) -> str:
        """
        Format products as JSON feed.

        Args:
            items: List of ProductFeedItem objects
            metadata: Optional feed metadata

        Returns:
            JSON feed string
        """
        metadata = metadata or {}

        # Build feed structure based on format
        if self.output_format == "meta":
            feed_data = self._build_meta_feed(items, metadata)
        else:
            feed_data = self._build_google_feed(items, metadata)

        # Serialize to JSON
        if self.pretty_print:
            return json.dumps(feed_data, indent=self.indent, ensure_ascii=False)
        return json.dumps(feed_data, ensure_ascii=False)

    def format_item(self, item: ProductFeedItem) -> str:
        """
        Format a single product as JSON object.

        Args:
            item: ProductFeedItem to format

        Returns:
            JSON string for single item
        """
        item_dict = self._item_to_dict(item)

        if self.pretty_print:
            return json.dumps(item_dict, indent=self.indent, ensure_ascii=False)
        return json.dumps(item_dict, ensure_ascii=False)

    def _build_google_feed(
        self, items: list[ProductFeedItem], metadata: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Build Google-compatible JSON feed structure.

        Args:
            items: List of products
            metadata: Feed metadata

        Returns:
            Feed dictionary
        """
        feed = {}

        if self.include_metadata:
            feed["feed"] = {
                "title": metadata.get("title", "Product Feed"),
                "description": metadata.get("description", "Product catalog feed"),
                "link": metadata.get("link", ""),
                "updated": metadata.get("updated", ""),
            }

        feed["items"] = [self._item_to_dict(item) for item in items]

        return feed

    def _build_meta_feed(
        self, items: list[ProductFeedItem], metadata: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Build Meta (Facebook) Catalog compatible JSON feed.

        Args:
            items: List of products
            metadata: Feed metadata

        Returns:
            Feed dictionary in Meta format
        """
        # Meta uses a slightly different structure
        return {
            "catalog": {
                "name": metadata.get("title", "Product Catalog"),
                "product_count": len(items),
            },
            "data": [self._item_to_meta_dict(item) for item in items],
        }

    def _item_to_dict(self, item: ProductFeedItem) -> dict[str, Any]:
        """
        Convert ProductFeedItem to Google-style dictionary.

        Args:
            item: ProductFeedItem to convert

        Returns:
            Dictionary representation
        """
        result = {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "link": item.link,
            "image_link": item.image_link,
            "price": item.price,
            "availability": item.availability,
            "condition": item.condition,
        }

        # Add optional fields only if they have values
        optional_fields = [
            ("product_type", item.product_type),
            ("google_product_category", item.google_product_category),
            ("brand", item.brand),
            ("gtin", item.gtin),
            ("mpn", item.mpn),
            ("sale_price", item.sale_price),
            ("sale_price_effective_date", item.sale_price_effective_date),
            ("age_group", item.age_group),
            ("color", item.color),
            ("gender", item.gender),
            ("material", item.material),
            ("pattern", item.pattern),
            ("size", item.size),
            ("size_type", item.size_type),
            ("size_system", item.size_system),
            ("item_group_id", item.item_group_id),
            ("shipping", item.shipping),
            ("tax", item.tax),
            ("custom_label_0", item.custom_label_0),
            ("custom_label_1", item.custom_label_1),
            ("custom_label_2", item.custom_label_2),
            ("custom_label_3", item.custom_label_3),
            ("custom_label_4", item.custom_label_4),
        ]

        for key, value in optional_fields:
            if value:
                result[key] = value

        # Handle boolean fields
        if item.adult:
            result["adult"] = "yes"

        # Handle additional images
        if item.additional_image_links:
            result["additional_image_links"] = item.additional_image_links[:10]

        # Handle identifier_exists
        if not item.gtin and not item.mpn:
            result["identifier_exists"] = "no"

        # Add custom attributes
        if item.custom_attributes:
            for key, value in item.custom_attributes.items():
                if key not in result:
                    result[key] = value

        return result

    def _item_to_meta_dict(self, item: ProductFeedItem) -> dict[str, Any]:
        """
        Convert ProductFeedItem to Meta (Facebook) Catalog format.

        Args:
            item: ProductFeedItem to convert

        Returns:
            Dictionary in Meta format
        """
        # Meta uses slightly different field names
        result = {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "availability": item.availability,
            "condition": item.condition,
            "price": item.price,
            "link": item.link,
            "image_link": item.image_link,
            "brand": item.brand or "",
        }

        # Meta-specific mappings
        if item.product_type:
            result["product_type"] = item.product_type
        if item.google_product_category:
            result["google_product_category"] = item.google_product_category
        if item.sale_price:
            result["sale_price"] = item.sale_price
        if item.gtin:
            result["gtin"] = item.gtin
        if item.color:
            result["color"] = item.color
        if item.size:
            result["size"] = item.size
        if item.gender:
            result["gender"] = item.gender
        if item.age_group:
            result["age_group"] = item.age_group
        if item.item_group_id:
            result["item_group_id"] = item.item_group_id
        if item.additional_image_links:
            result["additional_image_link"] = item.additional_image_links[:10]

        # Custom labels
        if item.custom_label_0:
            result["custom_label_0"] = item.custom_label_0
        if item.custom_label_1:
            result["custom_label_1"] = item.custom_label_1
        if item.custom_label_2:
            result["custom_label_2"] = item.custom_label_2
        if item.custom_label_3:
            result["custom_label_3"] = item.custom_label_3
        if item.custom_label_4:
            result["custom_label_4"] = item.custom_label_4

        return result

    def stream_feed(
        self, items: Iterator[ProductFeedItem], metadata: dict[str, Any] | None = None
    ) -> Iterator[str]:
        """
        Stream JSON feed for large product catalogs.

        Uses JSON Lines format for streaming.

        Yields:
            JSON content chunks
        """
        metadata = metadata or {}

        # For streaming, use JSON Lines format (one JSON object per line)
        # First yield metadata if enabled
        if self.include_metadata:
            meta_obj = {
                "type": "metadata",
                "title": metadata.get("title", "Product Feed"),
                "description": metadata.get("description", ""),
            }
            yield json.dumps(meta_obj, ensure_ascii=False) + "\n"

        # Yield each item on its own line
        for item in items:
            item_dict = self._item_to_dict(item)
            item_dict["type"] = "item"
            yield json.dumps(item_dict, ensure_ascii=False) + "\n"
