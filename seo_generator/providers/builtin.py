"""
Builtin Deterministic SEO Provider

CPU-based SEO generation using keyword extraction and template-based generation.
No external APIs, no ML models - completely deterministic and fast.
"""

import re
from typing import Dict, List
from collections import Counter
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.translation import gettext_lazy as _

from seo_generator.providers.base import BaseSEOProvider, GenerationError


# Common English stop words to filter out
STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he',
    'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'will',
    'with', 'this', 'but', 'they', 'have', 'had', 'what', 'when', 'where', 'who',
    'which', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'can', 'just', 'should', 'now'
}


class DeterministicSEOProvider(BaseSEOProvider):
    """
    Builtin SEO provider using deterministic keyword extraction and templates.

    Features:
    - CPU-bound keyword extraction using word frequency
    - Template-based meta title and description generation
    - No external APIs or ML models required
    - Fast and predictable results
    """

    provider_key = 'deterministic'
    provider_name = _('Built-in Generator')
    requires_credentials = False

    @property
    def capabilities(self) -> Dict[str, bool]:
        """Provider capabilities."""
        return {
            'meta_title': True,
            'meta_description': True,
            'keywords': True,
            'multi_language': False,  # V1 focuses on primary language
            'bulk_generation': True,
        }

    def _clean_text(self, text: str) -> str:
        """
        Clean text by stripping HTML and normalizing whitespace.

        Args:
            text: Raw text potentially containing HTML

        Returns:
            Cleaned plain text
        """
        if not text:
            return ''

        # Strip HTML tags
        text = strip_tags(text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _extract_words(self, text: str) -> List[str]:
        """
        Extract words from text, removing punctuation and stop words.

        Args:
            text: Cleaned text

        Returns:
            List of significant words
        """
        if not text:
            return []

        # Convert to lowercase
        text = text.lower()

        # Extract words (alphanumeric only)
        words = re.findall(r'\b[a-z0-9]+\b', text)

        # Filter out stop words and single-character words
        significant_words = [
            word for word in words
            if len(word) > 1 and word not in STOP_WORDS
        ]

        return significant_words

    def extract_keywords(self, content: Dict[str, str], max_keywords: int = 10) -> List[str]:
        """
        Extract keywords from content using word frequency analysis.

        Args:
            content: Dictionary with content fields
            max_keywords: Maximum number of keywords to return

        Returns:
            List of keyword strings ordered by relevance
        """
        try:
            # Combine all content fields
            combined_text = []

            # Name gets higher weight (appears 3x)
            if content.get('name'):
                combined_text.extend([content['name']] * 3)

            # Description
            if content.get('description'):
                combined_text.append(content['description'])

            # Category and brand (if present)
            if content.get('category'):
                combined_text.append(content['category'])

            if content.get('brand'):
                combined_text.append(content['brand'])

            # Clean and extract words from all text
            all_text = ' '.join(combined_text)
            cleaned = self._clean_text(all_text)
            words = self._extract_words(cleaned)

            # Count word frequency
            word_counts = Counter(words)

            # Get top keywords
            keywords = [word for word, count in word_counts.most_common(max_keywords)]

            return keywords

        except Exception as e:
            raise GenerationError(
                _("Keyword extraction failed: %(error)s") % {'error': e}
            )

    def generate_meta_title(self, content: Dict[str, str], language: str = 'en') -> str:
        """
        Generate SEO meta title using template-based approach.

        Format:
        - Product: "{Name} - {Brand} | {Category}"
        - Category: "{Name} - Shop {Category Products}"
        - Brand: "{Name} - Official {Brand} Products"
        - Page: "{Title}"

        All truncated to ~60 characters.

        Args:
            content: Dictionary with content fields
            language: Target language (currently unused in V1)

        Returns:
            Generated meta title (~60 chars)
        """
        try:
            name = content.get('name', '').strip()
            if not name:
                raise GenerationError(_("Content must have a 'name' field"))

            brand = content.get('brand', '').strip()
            category = content.get('category', '').strip()
            content_type = content.get('type', 'product').lower()

            # Build title based on content type
            if content_type == 'product':
                parts = [name]
                if brand:
                    parts.append(brand)
                if category:
                    parts.append(category)
                title = ' - '.join(parts)

            elif content_type == 'category':
                if category:
                    title = f"{name} - Shop {category}"
                else:
                    title = f"{name} - Shop Now"

            elif content_type == 'brand':
                title = f"{name} - Official Products"

            elif content_type in ('page', 'blogpost'):
                title = name

            elif content_type == 'blogcategory':
                title = f"{name} - Blog"

            else:
                # Fallback
                title = name

            # Truncate to 60 characters
            truncator = Truncator(title)
            return truncator.chars(60, truncate='...')

        except GenerationError:
            raise
        except Exception as e:
            raise GenerationError(
                _("Meta title generation failed: %(error)s") % {'error': e}
            )

    def generate_meta_description(self, content: Dict[str, str], language: str = 'en') -> str:
        """
        Generate SEO meta description using template-based approach.

        Extracts key information and creates a concise, compelling description.
        Truncated to ~155 characters.

        Args:
            content: Dictionary with content fields
            language: Target language (currently unused in V1)

        Returns:
            Generated meta description (~155 chars)
        """
        try:
            name = content.get('name', '').strip()
            if not name:
                raise GenerationError(_("Content must have a 'name' field"))

            description = content.get('description', '').strip()
            brand = content.get('brand', '').strip()
            category = content.get('category', '').strip()
            content_type = content.get('type', 'product').lower()

            # Build description based on content type
            if content_type == 'product':
                # Try to use first sentence of description
                if description:
                    cleaned_desc = self._clean_text(description)
                    # Get first sentence or first 100 chars
                    first_sentence = re.split(r'[.!?]\s', cleaned_desc)[0]
                    if len(first_sentence) > 100:
                        first_sentence = first_sentence[:100]

                    parts = [f"Shop {name}"]
                    if brand:
                        parts.append(f"by {brand}")
                    parts.append(f"- {first_sentence}")
                    desc = ' '.join(parts)
                else:
                    parts = [f"Shop {name}"]
                    if brand:
                        parts.append(f"by {brand}")
                    if category:
                        parts.append(f"in {category}")
                    parts.append("- High quality products with fast shipping")
                    desc = ' '.join(parts)

            elif content_type == 'category':
                if description:
                    cleaned_desc = self._clean_text(description)
                    desc = f"Browse our {name} collection. {cleaned_desc}"
                else:
                    desc = f"Discover amazing {name} products. Shop the latest collection with great prices and fast shipping."

            elif content_type == 'brand':
                if description:
                    cleaned_desc = self._clean_text(description)
                    desc = f"Shop official {name} products. {cleaned_desc}"
                else:
                    desc = f"Explore the complete {name} product range. Authentic products with fast delivery and great customer service."

            elif content_type in ('page', 'blogpost'):
                if description:
                    desc = self._clean_text(description)
                else:
                    desc = f"Learn more about {name}. Visit our page for detailed information."

            elif content_type == 'blogcategory':
                if description:
                    desc = self._clean_text(description)
                else:
                    desc = f"Browse articles about {name}. Read the latest posts and insights."

            else:
                # Fallback
                if description:
                    desc = self._clean_text(description)
                else:
                    desc = f"Discover {name}. Quality products and excellent service."

            # Truncate to 155 characters
            truncator = Truncator(desc)
            return truncator.chars(155, truncate='...')

        except GenerationError:
            raise
        except Exception as e:
            raise GenerationError(
                _("Meta description generation failed: %(error)s") % {'error': e}
            )
