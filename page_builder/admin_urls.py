"""
Page Builder Admin URL Configuration
Admin interface AJAX endpoints and visual builder routes.
All routes here are mounted at /admin/page_builder/ and gated
by AdminAccessMiddleware (role-based admin access control).
"""
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from . import admin_views, views

app_name = 'page_builder_admin'

urlpatterns = [
    # Admin AJAX Endpoints
    path('page/filter/', admin_views.filter_pages, name='filter_pages'),
    path('pagetemplate/filter/', admin_views.filter_page_templates, name='filter_page_templates'),

    # Visibility Rules Admin Endpoints
    path('visibilityrule/filter/', admin_views.filter_visibility_rules, name='filter_visibility_rules'),
    path('visibilityrule/<int:rule_id>/toggle-status/', admin_views.toggle_visibility_rule_status, name='toggle_visibility_rule_status'),
    path('visibilityrule/wizard/', admin_views.visibility_rule_wizard_view, name='visibility_rule_wizard'),
    path('visibilityrule/wizard/<int:rule_id>/', admin_views.visibility_rule_wizard_view, name='visibility_rule_wizard_edit'),

    # Rule Group Admin Endpoints
    path('rulegroup/filter/', admin_views.filter_rule_groups, name='filter_rule_groups'),
    path('rulegroup/<int:group_id>/toggle-status/', admin_views.toggle_rule_group_status, name='toggle_rule_group_status'),

    # Rule Builder Views
    path('rulegroup/builder/', admin_views.rule_builder_view, name='rule_builder'),
    path('rulegroup/builder/<int:group_id>/', admin_views.rule_builder_view, name='rule_builder_edit'),
    path('rulegroup/builder-popup/', admin_views.rule_builder_popup_view, name='rule_builder_popup'),
    path('rulegroup/builder-popup/<int:group_id>/', admin_views.rule_builder_popup_view, name='rule_builder_popup_edit'),

    # Visual Builder (migrated from page_builder/urls.py)
    path('builder/<int:page_id>/', views.visual_builder, name='visual_builder'),

    # Preview URLs (migrated from page_builder/urls.py)
    path('preview/<slug:slug>/', views.page_preview, name='page_preview'),
    path('builder-preview/<slug:slug>/', views.builder_preview, name='builder_preview'),

    # AJAX element rendering (migrated from page_builder/urls.py)
    path('ajax/element/<int:element_id>/', views.render_element_ajax, name='render_element_ajax'),

    # Utility template URLs (migrated from page_builder/urls.py)
    path('utilities/color_picker/template/',
         staff_member_required(TemplateView.as_view(template_name='components/utilities/color_picker/template.html')),
         name='color_picker_template'),
    path('utilities/gradient_creator/template/',
         staff_member_required(TemplateView.as_view(template_name='components/utilities/gradient_creator/template.html')),
         name='gradient_creator_template'),
    path('utilities/border_editor/template/',
         staff_member_required(TemplateView.as_view(template_name='components/utilities/border_editor/template.html')),
         name='border_editor_template'),
    path('utilities/shadow_editor/template/',
         staff_member_required(TemplateView.as_view(template_name='components/utilities/shadow_editor/template.html')),
         name='shadow_editor_template'),
    path('utilities/unit_selector/template/',
         staff_member_required(TemplateView.as_view(template_name='components/utilities/unit_selector/template.html')),
         name='unit_selector_template'),
]
