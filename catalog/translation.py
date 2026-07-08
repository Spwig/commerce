from modeltranslation.translator import register, TranslationOptions
from .models import Brand, Collection


# NOTE: Category no longer uses django-modeltranslation.
# It uses the JSON-based translation system with TranslatableAdminMixin
# and TranslatableFieldWidget per rules_llm.md guidelines.
# Translations are stored in Category.translations JSONField.


@register(Brand)
class BrandTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'meta_title',
        'meta_description'
    )


@register(Collection)
class CollectionTranslationOptions(TranslationOptions):
    fields = (
        'name',
        'description',
        'meta_title',
        'meta_description'
    )