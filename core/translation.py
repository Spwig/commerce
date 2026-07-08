from modeltranslation.translator import register, TranslationOptions
from .models import SiteSettings


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    # Note: Frontend-facing fields (site_name, site_tagline, site_description, meta_*, etc.)
    # use JSON-based translations via the 'translations' field, not modeltranslation.
    # Only admin UI-specific fields that need column-based translation should be listed here.
    fields = (
        # Currently no fields - all translatable content uses JSON field
    )