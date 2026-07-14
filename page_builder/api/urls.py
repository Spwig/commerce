"""
URL configuration for page builder API endpoints
"""

from django.urls import path

from . import translation_endpoints

app_name = "page_builder_api"

urlpatterns = [
    # Translation endpoints
    path(
        "translation-health/", translation_endpoints.translation_health, name="translation_health"
    ),
    path("translate-element/", translation_endpoints.translate_element, name="translate_element"),
    path(
        "element/<str:element_id>/translation-status/",
        translation_endpoints.element_translation_status,
        name="element_translation_status",
    ),
    path(
        "element/<str:element_id>/save-translations/",
        translation_endpoints.save_element_translations,
        name="save_element_translations",
    ),
    path(
        "element/<str:element_id>/clear-translations/",
        translation_endpoints.clear_element_translations,
        name="clear_translations",
    ),
    path(
        "schedule-page-translation/",
        translation_endpoints.schedule_page_translation,
        name="schedule_page_translation",
    ),
    path(
        "available-languages/",
        translation_endpoints.get_available_languages_api,
        name="available_languages",
    ),
    path(
        "translation-status/<int:job_id>/",
        translation_endpoints.get_translation_job_status,
        name="translation_job_status",
    ),
]
