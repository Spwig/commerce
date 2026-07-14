"""
Base class for feed formatters.

All feed format implementations (XML, CSV, JSON) must inherit from this class.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ProductFeedItem:
    """
    Standardized product data structure for feed generation.

    Maps Spwig product fields to common feed attributes.
    """

    # Required identifiers
    id: str
    title: str
    description: str
    link: str
    image_link: str
    price: str  # Format: "19.99 USD"
    availability: str  # "in_stock", "out_of_stock", "preorder", "backorder"

    # Category & Brand
    product_type: str = ""  # Store's product category path
    google_product_category: str = ""  # Google taxonomy ID
    brand: str = ""

    # Identifiers
    gtin: str = ""  # GTIN/EAN/UPC/ISBN
    mpn: str = ""  # Manufacturer Part Number

    # Pricing
    sale_price: str = ""  # Format: "14.99 USD"
    sale_price_effective_date: str = ""  # ISO 8601 format

    # Product details
    condition: str = "new"  # "new", "refurbished", "used"
    adult: bool = False
    age_group: str = ""  # "newborn", "infant", "toddler", "kids", "adult"
    color: str = ""
    gender: str = ""  # "male", "female", "unisex"
    material: str = ""
    pattern: str = ""
    size: str = ""
    size_type: str = ""  # "regular", "petite", "plus", "tall", "big", "maternity"
    size_system: str = ""  # "US", "UK", "EU", etc.
    item_group_id: str = ""  # For product variants

    # Shipping & Tax
    shipping: str = ""
    tax: str = ""

    # Additional images (up to 10)
    additional_image_links: list[str] = None

    # Custom labels for merchant segmentation (0-4)
    custom_label_0: str = ""
    custom_label_1: str = ""
    custom_label_2: str = ""
    custom_label_3: str = ""
    custom_label_4: str = ""

    # Inventory
    quantity: int = 0

    # Additional custom attributes
    custom_attributes: dict[str, Any] = None

    def __post_init__(self):
        if self.additional_image_links is None:
            self.additional_image_links = []
        if self.custom_attributes is None:
            self.custom_attributes = {}


class BaseFeedFormatter(ABC):
    """
    Abstract base class for feed formatters.

    Subclasses implement format-specific output generation.
    """

    format_name: str = None  # e.g., 'xml', 'csv', 'json'
    content_type: str = None  # e.g., 'application/xml', 'text/csv'
    file_extension: str = None  # e.g., 'xml', 'csv', 'json'

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialize formatter with optional configuration.

        Args:
            config: Formatter-specific configuration
        """
        self.config = config or {}

    @abstractmethod
    def format_feed(
        self, items: list[ProductFeedItem], metadata: dict[str, Any] | None = None
    ) -> str:
        """
        Format list of products into feed string.

        Args:
            items: List of ProductFeedItem objects
            metadata: Optional feed metadata (title, description, etc.)

        Returns:
            Formatted feed content as string
        """
        pass

    @abstractmethod
    def format_item(self, item: ProductFeedItem) -> str:
        """
        Format a single product item.

        Args:
            item: ProductFeedItem to format

        Returns:
            Formatted item string
        """
        pass

    def stream_feed(
        self, items: Iterator[ProductFeedItem], metadata: dict[str, Any] | None = None
    ) -> Iterator[str]:
        """
        Stream feed content for large feeds.

        Override for format-specific streaming implementation.

        Args:
            items: Iterator of ProductFeedItem objects
            metadata: Optional feed metadata

        Yields:
            Feed content chunks
        """
        # Default: collect all and format at once
        items_list = list(items)
        yield self.format_feed(items_list, metadata)

    def get_content_type(self) -> str:
        """Get MIME content type for this format."""
        return self.content_type or "text/plain"

    def get_file_extension(self) -> str:
        """Get file extension for this format."""
        return self.file_extension or "txt"

    def validate_item(self, item: ProductFeedItem) -> list[str]:
        """
        Validate a product item for required fields.

        Args:
            item: ProductFeedItem to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Required fields
        if not item.id:
            errors.append("Missing required field: id")
        if not item.title:
            errors.append("Missing required field: title")
        if not item.description:
            errors.append("Missing required field: description")
        if not item.link:
            errors.append("Missing required field: link")
        if not item.image_link:
            errors.append("Missing required field: image_link")
        if not item.price:
            errors.append("Missing required field: price")
        if not item.availability:
            errors.append("Missing required field: availability")

        return errors

    def escape_text(self, text: str) -> str:
        """
        Escape text for the specific format.

        Override in subclasses for format-specific escaping.

        Args:
            text: Text to escape

        Returns:
            Escaped text
        """
        return text if text else ""

    def format_price(self, price: float, currency: str = "USD") -> str:
        """
        Format price value consistently.

        Args:
            price: Price as float
            currency: Currency code

        Returns:
            Formatted price string (e.g., "19.99 USD")
        """
        return f"{price:.2f} {currency}"

    def format_datetime(self, dt: datetime) -> str:
        """
        Format datetime in ISO 8601 format.

        Args:
            dt: datetime object

        Returns:
            ISO 8601 formatted string
        """
        return dt.strftime("%Y-%m-%dT%H:%M:%S%z") if dt else ""
