"""
Form Builder Admin URLs

These URLs are included inside i18n_patterns under /admin/form_builder/
"""
from django.urls import path
from . import views

app_name = 'form_builder'

urlpatterns = [
    # Form preview
    path('forms/<int:pk>/preview/', views.preview_form, name='preview_form'),

    # Form duplication
    path('forms/<int:pk>/duplicate/', views.duplicate_form, name='duplicate_form'),

    # Field reordering (AJAX)
    path('forms/<int:pk>/fields/reorder/', views.reorder_fields, name='reorder_fields'),

    # Response export
    path('responses/<int:form_pk>/export/', views.export_responses, name='export_responses'),

    # Visual Builder
    path('forms/create/', views.create_form, name='create_form'),
    path('forms/<int:pk>/builder/', views.visual_builder, name='visual_builder'),
    path('forms/<int:pk>/builder/save/', views.save_form_builder, name='save_form_builder'),
    path('forms/<int:pk>/builder/fields/add/', views.add_field, name='add_field'),
    path('forms/<int:pk>/builder/fields/<int:field_id>/delete/', views.delete_field, name='delete_field'),
    path('forms/<int:pk>/builder/fields/<int:field_id>/update/', views.update_field, name='update_field'),

    # Step CRUD (Visual Builder)
    path('forms/<int:pk>/builder/steps/add/', views.add_step, name='add_step'),
    path('forms/<int:pk>/builder/steps/<int:step_id>/update/', views.update_step, name='update_step'),
    path('forms/<int:pk>/builder/steps/<int:step_id>/delete/', views.delete_step, name='delete_step'),

    # Conditional Rule CRUD (Visual Builder)
    path('forms/<int:pk>/builder/rules/', views.list_rules, name='list_rules'),
    path('forms/<int:pk>/builder/rules/add/', views.add_rule, name='add_rule'),
    path('forms/<int:pk>/builder/rules/<int:rule_id>/update/', views.update_rule, name='update_rule'),
    path('forms/<int:pk>/builder/rules/<int:rule_id>/delete/', views.delete_rule, name='delete_rule'),

    # Form Action CRUD (Visual Builder)
    path('forms/<int:pk>/builder/actions/', views.list_actions, name='list_actions'),
    path('forms/<int:pk>/builder/actions/add/', views.add_action, name='add_action'),
    path('forms/<int:pk>/builder/actions/<int:action_id>/update/', views.update_action, name='update_action'),
    path('forms/<int:pk>/builder/actions/<int:action_id>/delete/', views.delete_action, name='delete_action'),

]
