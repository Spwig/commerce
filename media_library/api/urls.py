from django.urls import path
from . import translation_endpoints

app_name = 'media_library_api'

urlpatterns = [
    # Translation endpoints
    path('translate/', translation_endpoints.translate_media_asset, name='translate_media'),
    path('media/<str:media_id>/translation-status/', translation_endpoints.media_translation_status, name='translation_status'),
    path('media/<str:media_id>/save-translations/', translation_endpoints.save_media_translations, name='save_translations'),
    path('media/<str:media_id>/clear-translations/', translation_endpoints.clear_media_translations, name='clear_translations'),
]