"""
API URL configuration for page builder.
All API endpoints are consolidated here to be included outside i18n_patterns.
"""
from django.urls import path, include
from . import api_views

app_name = 'page_builder_api'

urlpatterns = [
    # Visual Builder API endpoints
    path('page/<int:page_id>/', api_views.get_page_data, name='page_data'),
    path('elements/', api_views.ElementAPIView.as_view(), name='elements'),
    path('elements/<int:element_id>/', api_views.ElementAPIView.as_view(), name='element_detail'),
    path('elements/config/<str:element_type>/', api_views.get_element_config, name='element_config'),
    path('elements/reorder/', api_views.reorder_elements, name='reorder_elements'),

    # Versioning API endpoints
    path('page/<int:page_id>/save-draft/', api_views.save_page_draft, name='save_draft'),
    path('page/<int:page_id>/publish/', api_views.publish_page, name='publish'),
    path('page/<int:page_id>/versions/', api_views.get_page_versions, name='versions'),
    path('page/<int:page_id>/revert/<int:version_id>/', api_views.revert_to_version, name='revert'),
    path('page/<int:page_id>/preview/<int:version_id>/', api_views.preview_version, name='preview_version'),
    path('page/<int:page_id>/publish-history/', api_views.get_publish_history, name='publish_history'),

    # Page Settings API endpoints
    path('page/<int:page_id>/settings/', api_views.get_page_settings_config, name='page_settings_config'),
    path('page/<int:page_id>/settings/update/', api_views.update_page_settings, name='update_page_settings'),

    # Preview thumbnail capture
    path('page/<int:page_id>/capture-thumbnail/', api_views.capture_page_thumbnail, name='capture_thumbnail'),

    # Translation API endpoints (from page_builder.api.urls)
    path('translation/', include('page_builder.api.urls')),

    # Public Pages API (Headless Frontend)
    path('public/legal/', api_views.get_legal_pages, name='public_legal_pages'),
    path('public/type/<str:page_type>/', api_views.get_page_by_type, name='public_page_by_type'),
    path('public/<slug:slug>/', api_views.get_public_page, name='public_page'),

    # Visibility Rules API
    path('visibility-rules/', api_views.get_visibility_rule_groups, name='visibility_rule_groups'),

    # Rule Builder API - Rule Groups
    path('rule-groups/', api_views.RuleGroupAPIView.as_view(), name='rule_groups'),
    path('rule-groups/<int:group_id>/', api_views.RuleGroupAPIView.as_view(), name='rule_group_detail'),
    path('rule-groups/<int:group_id>/structure/', api_views.save_rule_group_structure, name='rule_group_structure'),

    # Rule Builder API - Visibility Rules
    path('rules/', api_views.VisibilityRuleAPIView.as_view(), name='rules'),
    path('rules/<int:rule_id>/', api_views.VisibilityRuleAPIView.as_view(), name='rule_detail'),
    path('rules/config/', api_views.get_rule_types_config, name='rule_types_config'),

    # Link Selector API
    path('link-sources/', api_views.get_link_sources, name='link_sources'),

    # Product Picker API (enriched search for product grid element)
    path('product-search/', api_views.product_search, name='product_search'),
]
