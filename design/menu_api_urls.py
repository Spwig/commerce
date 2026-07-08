"""
API URL patterns for menu builder
These routes are included outside i18n_patterns at /api/menu/
"""

from django.urls import path
from .menu_api_views import (
    MenuListAPIView,
    MenuDetailAPIView,
    MenuItemCreateAPIView,
    MenuItemDetailAPIView,
    MenuItemsReorderAPIView,
    QuickAddSourcesAPIView,
    MenuPreviewAPIView,
    MenuSaveStructureAPIView,
    MenuTokensAPIView,
)

app_name = 'menu_api'

urlpatterns = [
    # Menu CRUD
    path('', MenuListAPIView.as_view(), name='menu_list'),
    path('<int:pk>/', MenuDetailAPIView.as_view(), name='menu_detail'),
    path('<int:pk>/preview/', MenuPreviewAPIView.as_view(), name='menu_preview'),
    path('<int:pk>/save-structure/', MenuSaveStructureAPIView.as_view(), name='menu_save_structure'),

    # Menu Item CRUD
    path('items/', MenuItemCreateAPIView.as_view(), name='item_create'),
    path('items/<int:pk>/', MenuItemDetailAPIView.as_view(), name='item_detail'),
    path('items/reorder/', MenuItemsReorderAPIView.as_view(), name='items_reorder'),

    # Quick-add sources
    path('sources/', QuickAddSourcesAPIView.as_view(), name='quick_add_sources'),

    # Menu design tokens (for menu builder styling)
    path('tokens/', MenuTokensAPIView.as_view(), name='menu_tokens'),
]
