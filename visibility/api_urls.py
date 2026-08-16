"""Neutral visibility API — mounted at /api/visibility/ (outside i18n_patterns).

Used by the shared visibility editor to list rule groups, read/set an object's
attached rule groups, and quick-create a single-rule group.
"""

from django.urls import path

from . import api_views

app_name = "visibility_api"

urlpatterns = [
    path("rule-groups/", api_views.RuleGroupOptionsView.as_view(), name="rule_groups"),
    path("attach/", api_views.VisibilityAttachView.as_view(), name="attach"),
    path("quick-rule/", api_views.QuickRuleGroupView.as_view(), name="quick_rule"),
]
