from modeltranslation.translator import TranslationOptions, register

from .models import Element

# NOTE: Page model now uses JSON-based translations (Page.translations JSONField)
# instead of django-modeltranslation. This allows merchant-translatable content
# to be handled by our Translation Service rather than admin interface translations.


@register(Element)
class ElementTranslationOptions(TranslationOptions):
    fields = ("name",)
