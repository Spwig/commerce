"""
Base Mapper
Abstract base class for all data mappers
"""

import logging
from abc import ABC, abstractmethod
from typing import Any

from django.utils.text import slugify

logger = logging.getLogger(__name__)


class BaseMapper(ABC):
    """
    Abstract base class for mapping external data to internal format

    All mappers should inherit from this class and implement the map() method
    """

    def __init__(self, migration_job=None):
        """
        Initialize mapper

        Args:
            migration_job: Optional MigrationJob instance for context
        """
        self.migration_job = migration_job
        self.errors = []
        self.warnings = []

    @abstractmethod
    def map(self, source_data: dict) -> dict:
        """
        Map source data to internal format

        Args:
            source_data: Raw data from external platform

        Returns:
            Dictionary in internal format
        """
        pass

    def safe_get(self, data: dict, *keys, default=None):
        """
        Safely get nested dictionary values

        Args:
            data: Dictionary to search
            *keys: Keys to traverse
            default: Default value if not found

        Returns:
            Value at nested key or default
        """
        result = data
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key)
                if result is None:
                    return default
            else:
                return default
        return result if result is not None else default

    def generate_slug(self, text: str, max_length: int = 200) -> str:
        """
        Generate a URL-safe slug

        Args:
            text: Text to slugify
            max_length: Maximum slug length

        Returns:
            URL-safe slug
        """
        if not text:
            return ""

        slug = slugify(text)
        return slug[:max_length] if len(slug) > max_length else slug

    def parse_html(self, html: str) -> str:
        """
        Clean and parse HTML content

        Args:
            html: HTML string

        Returns:
            Cleaned HTML
        """
        if not html:
            return ""

        # Basic HTML cleaning - can be enhanced with bleach or similar
        return html.strip()

    def parse_price(self, price_str: str) -> float | None:
        """
        Parse price string to float

        Args:
            price_str: Price as string

        Returns:
            Price as float or None
        """
        if not price_str:
            return None

        try:
            # Remove currency symbols and commas
            cleaned = str(price_str).replace("$", "").replace(",", "").strip()
            return float(cleaned)
        except (ValueError, TypeError):
            self.warnings.append(f"Failed to parse price: {price_str}")
            return None

    def parse_bool(self, value: Any) -> bool:
        """
        Parse various boolean representations

        Args:
            value: Value to parse

        Returns:
            Boolean value
        """
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1", "on")

        return bool(value)

    def log_error(self, message: str, data: dict | None = None):
        """
        Log a mapping error

        Args:
            message: Error message
            data: Optional data context
        """
        error = {"message": message}
        if data:
            error["data"] = data

        self.errors.append(error)
        logger.error(f"Mapping error: {message}")

    def log_warning(self, message: str, data: dict | None = None):
        """
        Log a mapping warning

        Args:
            message: Warning message
            data: Optional data context
        """
        warning = {"message": message}
        if data:
            warning["data"] = data

        self.warnings.append(warning)
        logger.warning(f"Mapping warning: {message}")

    def get_errors(self) -> list[dict]:
        """Get all logged errors"""
        return self.errors

    def get_warnings(self) -> list[dict]:
        """Get all logged warnings"""
        return self.warnings

    def has_errors(self) -> bool:
        """Check if any errors were logged"""
        return len(self.errors) > 0

    def clear_logs(self):
        """Clear error and warning logs"""
        self.errors = []
        self.warnings = []
