"""
Serializer mixins for handling translated fields in the catalog app
"""

from django.utils import translation

from core.translation_utils import get_primary_language

# Map serializer field names to model field names where they differ
_MODEL_FIELD_MAP = {
    "description": "full_description",
}


class TranslatedFieldsMixin:
    """
    Mixin to handle extraction of translated fields from JSONField translations.

    This mixin provides helper methods to extract translated content from the
    translations JSONField used throughout the platform for multi-language support.
    """

    def get_translated_field(self, obj, field_name, prefer_html=True):
        """
        Extract a translated field from the translations JSON.

        Args:
            obj: The model instance
            field_name: Base name of the field (e.g., 'description', 'short_description')
            prefer_html: If True, prefer HTML version over plain text

        Returns:
            The translated content or empty string if not found
        """
        model_field = _MODEL_FIELD_MAP.get(field_name, field_name)

        if not hasattr(obj, "translations") or not obj.translations:
            # No translations — fall back to raw model field
            return getattr(obj, model_field, "") or ""

        # Get current language, falling back to the merchant's primary language
        primary_lang = get_primary_language()
        lang = translation.get_language() or primary_lang

        # Try current language first
        if lang in obj.translations:
            content = self._extract_field(obj.translations[lang], field_name, prefer_html)
            if content:
                return content

        # Fallback to the merchant's primary language if current language not available
        if lang != primary_lang and primary_lang in obj.translations:
            content = self._extract_field(obj.translations[primary_lang], field_name, prefer_html)
            if content:
                return content

        # Fallback to the raw model field if no translation exists
        return getattr(obj, model_field, "") or ""

    @staticmethod
    def _extract_field(lang_data, field_name, prefer_html):
        """Extract a field from a language data dict, trying html/text variants."""
        if prefer_html:
            return (
                lang_data.get(f"{field_name}_html")
                or lang_data.get(f"{field_name}_text")
                or lang_data.get(field_name, "")
            )
        else:
            return (
                lang_data.get(f"{field_name}_text")
                or lang_data.get(f"{field_name}_html")
                or lang_data.get(field_name, "")
            )

    def get_translated_name(self, obj):
        """Get translated name"""
        return self.get_translated_field(obj, "name", prefer_html=False)

    def get_translated_description(self, obj):
        """Get translated description (prefers HTML)"""
        return self.get_translated_field(obj, "description", prefer_html=True)

    def get_translated_short_description(self, obj):
        """Get translated short description (prefers HTML)"""
        return self.get_translated_field(obj, "short_description", prefer_html=True)

    def get_translated_meta_title(self, obj):
        """Get translated meta title"""
        return self.get_translated_field(obj, "meta_title", prefer_html=False)

    def get_translated_meta_description(self, obj):
        """Get translated meta description"""
        return self.get_translated_field(obj, "meta_description", prefer_html=False)


class TranslationAwareSerializer:
    """
    Base class for serializers that need translation awareness.

    Provides language detection from the request and automatic translation of
    fields listed in ``Meta.translated_fields`` from the model's ``translations``
    JSONField.
    """

    def get_current_language(self):
        """
        Get the current language from the request or fallback to default.

        Parses the Accept-Language header respecting quality weights, e.g.
        ``en;q=0.5,fr;q=0.9`` correctly returns ``'fr'``.

        Returns:
            Language code (e.g., 'en', 'es', 'ar')
        """
        request = self.context.get("request")
        if request:
            accept_lang = request.META.get("HTTP_ACCEPT_LANGUAGE")
            if accept_lang:
                return _parse_accept_language(accept_lang)

        # Fallback to Django's current language or the merchant's primary
        return translation.get_language() or get_primary_language()

    def to_representation(self, instance):
        """
        Override to set language based on request before serialization,
        then apply translations from Meta.translated_fields if defined.
        """
        current_lang = self.get_current_language()
        with translation.override(current_lang):
            data = super().to_representation(instance)

        # Apply translations from the model's translations JSONField
        translated_fields = getattr(getattr(self, "Meta", None), "translated_fields", None)
        if translated_fields and hasattr(instance, "translations") and instance.translations:
            primary_lang = get_primary_language()
            # Try requested language, then primary language
            lang_data = instance.translations.get(current_lang)
            if not lang_data and current_lang != primary_lang:
                lang_data = instance.translations.get(primary_lang)
            if lang_data:
                for field_name in translated_fields:
                    value = lang_data.get(field_name)
                    if value and field_name in data:
                        data[field_name] = value

        return data


def _parse_accept_language(header):
    """
    Parse an Accept-Language header and return the preferred language code.

    Respects quality weights: ``en;q=0.5,fr;q=0.9`` returns ``'fr'``.
    Strips region subtags: ``en-GB`` becomes ``'en'``.
    """
    best_lang = None
    best_q = -1
    for part in header.split(","):
        part = part.strip()
        if not part:
            continue
        pieces = part.split(";")
        lang = pieces[0].strip().split("-")[0]
        q = 1.0
        for param in pieces[1:]:
            param = param.strip()
            if param.startswith("q="):
                try:
                    q = float(param[2:])
                except ValueError:
                    pass
        if q > best_q:
            best_q = q
            best_lang = lang
    return best_lang or get_primary_language()
