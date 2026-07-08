"""
Media Library API URLs
These URLs should be included WITHOUT language prefixes
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for API viewsets
router = DefaultRouter()
router.register(r'assets', views.MediaAssetViewSet, basename='asset')
router.register(r'folders', views.MediaFolderViewSet, basename='folder')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'jobs', views.MediaProcessingJobViewSet, basename='processingjob')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # Translation API endpoints
    path('', include('media_library.api.urls')),

    # Additional API endpoints
    path('upload-progress/', views.upload_progress, name='upload_progress'),

    # Auto-save endpoint for MediaAsset ForeignKey fields
    path('auto-save/', views.MediaFieldAutoSaveAPIView.as_view(), name='media_field_auto_save'),

    # CKEditor 5 upload endpoint (routes uploads through media library)
    path('ckeditor-upload/', views.ckeditor_media_library_upload, name='ckeditor_media_library_upload'),
]