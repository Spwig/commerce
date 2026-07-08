"""
Deep product indexing service.

Provides methods to build searchable indexes from products,
including attributes, custom fields, reviews, and document content.
"""
from typing import Dict, List, Any, Optional


class IndexingService:
    """
    Service for building searchable indexes from products and other content.

    Handles deep indexing of:
    - Product names, descriptions, SKUs
    - Product attributes (color, size, etc.)
    - Custom fields
    - Review content
    - Digital asset document content
    """

    def index_product(self, product) -> Dict[str, List[str]]:
        """
        Build searchable index for a product.

        Returns dict with lists of searchable text for each field type.
        """
        from ..models import SearchSettings

        settings = SearchSettings.get_settings()

        index = {
            'name': [product.name],
            'sku': [],
            'description': [],
            'attributes': [],
            'custom_fields': [],
            'reviews': [],
            'documents': [],
            'translations': {},
        }

        # SKU
        if settings.index_skus:
            if product.sku:
                index['sku'].append(product.sku)
            # Variant SKUs
            for variant in product.variants.all():
                if variant.sku:
                    index['sku'].append(variant.sku)

        # Descriptions
        if product.short_description:
            index['description'].append(product.short_description)
        if product.full_description:
            index['description'].append(product.full_description)

        # Attributes
        if settings.index_attributes:
            index['attributes'] = self._extract_product_attributes(product)

        # Custom fields
        if settings.index_custom_fields:
            index['custom_fields'] = self._extract_custom_fields(product)

        # Reviews
        if settings.index_reviews:
            index['reviews'] = self._extract_review_content(product)

        # Translations
        if hasattr(product, 'translations') and product.translations:
            for lang, trans_data in product.translations.items():
                if lang.startswith('_'):  # Skip _meta
                    continue
                index['translations'][lang] = {
                    'name': trans_data.get('name', ''),
                    'description': trans_data.get('short_description', '') or
                                   trans_data.get('full_description', ''),
                }

        return index

    def _extract_product_attributes(self, product) -> List[str]:
        """Extract searchable attribute values from a product."""
        attributes = []

        # Product attribute values
        if hasattr(product, 'attribute_values'):
            for attr_value in product.attribute_values.all():
                if attr_value.value:
                    attributes.append(str(attr_value.value))
                if hasattr(attr_value, 'attribute') and attr_value.attribute:
                    # Include attribute name for context
                    attributes.append(attr_value.attribute.name)

        # Variant attributes
        for variant in product.variants.all():
            if hasattr(variant, 'attribute_values'):
                for attr_value in variant.attribute_values.all():
                    if attr_value.value and str(attr_value.value) not in attributes:
                        attributes.append(str(attr_value.value))

        return attributes

    def _extract_custom_fields(self, product) -> List[str]:
        """Extract custom field values from a product."""
        custom_fields = []

        if hasattr(product, 'custom_fields') and product.custom_fields:
            for field_name, field_value in product.custom_fields.items():
                if field_value:
                    # Add both field name and value
                    custom_fields.append(str(field_name))
                    custom_fields.append(str(field_value))

        return custom_fields

    def _extract_review_content(self, product) -> List[str]:
        """Extract searchable content from product reviews."""
        reviews = []

        if hasattr(product, 'reviews'):
            for review in product.reviews.filter(is_approved=True):
                if review.title:
                    reviews.append(review.title)
                if review.comment:
                    reviews.append(review.comment)

        return reviews

    def get_searchable_fields(self, product) -> Dict[str, Any]:
        """
        Get all searchable content for a product as a flat dict.

        Useful for quick searching or building search queries.
        """
        index = self.index_product(product)

        return {
            'names': index['name'],
            'skus': index['sku'],
            'descriptions': index['description'],
            'attributes': index['attributes'],
            'custom_fields': index['custom_fields'],
            'reviews': index['reviews'],
            'all_text': self._combine_index_text(index),
        }

    def _combine_index_text(self, index: Dict) -> str:
        """Combine all indexed text into a single searchable string."""
        text_parts = []

        for key, value in index.items():
            if key == 'translations':
                for lang_data in value.values():
                    if isinstance(lang_data, dict):
                        text_parts.extend(v for v in lang_data.values() if v)
            elif isinstance(value, list):
                text_parts.extend(str(v) for v in value if v)
            elif value:
                text_parts.append(str(value))

        return ' '.join(text_parts)

    def get_searchable_content_multilang(self, product, language: str = None) -> Dict[str, str]:
        """
        Get searchable content for a product in a specific language.

        Returns dict with field names and their values in the requested language.
        Falls back to base values if translation not available.
        """
        result = {
            'name': product.name,
            'description': product.short_description or product.full_description or '',
            'sku': product.sku or '',
        }

        # If a specific language is requested, try to get translated values
        if language and language != 'en':
            if hasattr(product, 'translations') and product.translations:
                lang_data = product.translations.get(language, {})
                if 'name' in lang_data and lang_data['name']:
                    result['name'] = lang_data['name']
                if 'short_description' in lang_data and lang_data['short_description']:
                    result['description'] = lang_data['short_description']
                elif 'full_description' in lang_data and lang_data['full_description']:
                    result['description'] = lang_data['full_description']

        return result

    def index_category(self, category) -> Dict[str, Any]:
        """Build searchable index for a category."""
        index = {
            'name': [category.name],
            'description': [category.description] if category.description else [],
            'translations': {},
        }

        if hasattr(category, 'translations') and category.translations:
            for lang, trans_data in category.translations.items():
                if lang.startswith('_'):
                    continue
                index['translations'][lang] = {
                    'name': trans_data.get('name', ''),
                    'description': trans_data.get('description', ''),
                }

        return index

    def index_blog_post(self, post) -> Dict[str, Any]:
        """Build searchable index for a blog post."""
        index = {
            'title': [post.title],
            'excerpt': [post.excerpt] if post.excerpt else [],
            'content': [post.simple_content] if hasattr(post, 'simple_content') and post.simple_content else [],
            'tags': [],
            'translations': {},
        }

        # Tags
        if hasattr(post, 'tags'):
            for tag in post.tags.all():
                index['tags'].append(tag.name)

        # Translations
        if hasattr(post, 'translations') and post.translations:
            for lang, trans_data in post.translations.items():
                if lang.startswith('_'):
                    continue
                index['translations'][lang] = {
                    'title': trans_data.get('title', ''),
                    'excerpt': trans_data.get('excerpt', ''),
                }

        return index
