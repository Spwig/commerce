"""
URL configuration for SEO Generator API
"""

from django.urls import path
from seo_generator.api import endpoints

app_name = 'seo_generator_api'

urlpatterns = [
    # Single object SEO generation
    path('generate/<str:model_type>/<int:object_id>/', endpoints.generate_seo, name='generate'),

    # Batch generation
    path('batch/', endpoints.batch_generate, name='batch_generate'),

    # Status check
    path('status/<str:model_type>/<int:object_id>/', endpoints.seo_status, name='status'),
]
