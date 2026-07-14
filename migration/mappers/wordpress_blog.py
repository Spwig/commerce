"""
WordPress Blog Content Mappers.

Maps WordPress blog data structures to Spwig blog models.
"""

import logging
import re
from html import unescape

from django.utils.text import slugify

logger = logging.getLogger(__name__)


class WordPressBlogCategoryMapper:
    """
    Map WordPress category data to Spwig BlogCategory format.

    WordPress category structure:
    {
        "id": 1,
        "name": "Technology",
        "slug": "tech",
        "description": "...",
        "parent": 0,  # 0 means no parent
        "count": 10
    }
    """

    def map(self, source_data: dict) -> dict:
        """
        Map a WordPress category to Spwig format.

        Args:
            source_data: WordPress category data

        Returns:
            Dict with mapped fields
        """
        name = self._clean_html(source_data.get("name", ""))

        return {
            "name": name,
            "slug": self._generate_slug(source_data.get("slug", ""), name),
            "description": self._clean_html(source_data.get("description", "")),
            "parent_id": source_data.get("parent", 0),  # 0 means no parent
            "is_active": True,
            "source_id": str(source_data.get("id")),
            "source_platform": "wordpress",
        }

    def _generate_slug(self, original_slug: str, name: str) -> str:
        """Generate a valid slug."""
        if original_slug:
            return slugify(original_slug)
        return slugify(name) if name else "category"

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and decode entities."""
        if not text:
            return ""
        # Remove HTML tags
        clean = re.sub(r"<[^>]+>", "", text)
        # Decode HTML entities
        return unescape(clean).strip()


class WordPressBlogTagMapper:
    """
    Map WordPress tag data to Spwig BlogTag format.

    WordPress tag structure:
    {
        "id": 5,
        "name": "Python",
        "slug": "python",
        "description": "...",
        "count": 15
    }
    """

    def map(self, source_data: dict) -> dict:
        """
        Map a WordPress tag to Spwig format.

        Args:
            source_data: WordPress tag data

        Returns:
            Dict with mapped fields
        """
        name = self._clean_html(source_data.get("name", ""))

        return {
            "name": name,
            "slug": self._generate_slug(source_data.get("slug", ""), name),
            "source_id": str(source_data.get("id")),
            "source_platform": "wordpress",
        }

    def _generate_slug(self, original_slug: str, name: str) -> str:
        """Generate a valid slug."""
        if original_slug:
            return slugify(original_slug)
        return slugify(name) if name else "tag"

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and decode entities."""
        if not text:
            return ""
        clean = re.sub(r"<[^>]+>", "", text)
        return unescape(clean).strip()


class WordPressBlogPostMapper:
    """
    Map WordPress post data to Spwig BlogPost format.

    WordPress post structure:
    {
        "id": 1,
        "date": "2024-01-15T10:30:00",
        "date_gmt": "2024-01-15T15:30:00",
        "slug": "hello-world",
        "status": "publish",
        "title": {"rendered": "Hello World"},
        "content": {"rendered": "<p>...</p>"},
        "excerpt": {"rendered": "<p>...</p>"},
        "author": 1,
        "featured_media": 123,  # Media attachment ID
        "categories": [1, 3],
        "tags": [5, 7],
        "modified": "2024-01-20T08:00:00"
    }
    """

    # Status mapping
    STATUS_MAP = {
        "publish": "published",
        "draft": "draft",
        "pending": "draft",
        "private": "draft",
        "future": "scheduled",
        "trash": "archived",
    }

    def map(self, source_data: dict) -> dict:
        """
        Map a WordPress post to Spwig format.

        Args:
            source_data: WordPress post data

        Returns:
            Dict with mapped fields
        """
        # Extract rendered content from nested structures
        title = self._extract_rendered(source_data.get("title", {}))
        content = self._extract_rendered(source_data.get("content", {}))
        excerpt = self._extract_rendered(source_data.get("excerpt", {}))

        # Clean excerpt (remove HTML for summary)
        clean_excerpt = self._clean_html(excerpt)
        if len(clean_excerpt) > 500:
            clean_excerpt = clean_excerpt[:497] + "..."

        return {
            "title": title,
            "slug": self._generate_slug(source_data.get("slug", ""), title),
            "status": self._map_status(source_data.get("status", "draft")),
            "simple_content": content,  # Keep HTML for CKEditor
            "excerpt": clean_excerpt,
            "featured_media_id": source_data.get("featured_media", 0),
            "category_ids": source_data.get("categories", []),
            "tag_ids": source_data.get("tags", []),
            "author_id": source_data.get("author"),
            "date_created": source_data.get("date"),
            "date_created_gmt": source_data.get("date_gmt"),
            "date_modified": source_data.get("modified"),
            "date_modified_gmt": source_data.get("modified_gmt"),
            "source_id": str(source_data.get("id")),
            "source_platform": "wordpress",
        }

    def _extract_rendered(self, field_data) -> str:
        """Extract rendered content from WordPress nested structure."""
        if isinstance(field_data, dict):
            return field_data.get("rendered", "")
        return str(field_data) if field_data else ""

    def _generate_slug(self, original_slug: str, title: str) -> str:
        """Generate a valid slug."""
        if original_slug:
            return slugify(original_slug)
        return slugify(title) if title else "post"

    def _map_status(self, wp_status: str) -> str:
        """Map WordPress status to Spwig status."""
        return self.STATUS_MAP.get(wp_status, "draft")

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and decode entities."""
        if not text:
            return ""
        clean = re.sub(r"<[^>]+>", "", text)
        return unescape(clean).strip()
