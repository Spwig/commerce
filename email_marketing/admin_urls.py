"""Admin-side (i18n) URLs for the Campaign Studio builder."""

from django.urls import path

from . import admin_views

app_name = "email_marketing_admin"

urlpatterns = [
    path("dashboard/", admin_views.campaign_studio_dashboard, name="dashboard"),
    path("wizard/", admin_views.campaign_wizard, name="campaign_wizard"),
    path("filter/campaigns/", admin_views.filter_campaigns, name="filter_campaigns"),
    path("filter/journeys/", admin_views.filter_journeys, name="filter_journeys"),
    path("filter/subscribers/", admin_views.filter_subscribers, name="filter_subscribers"),
    path("filter/segments/", admin_views.filter_segments, name="filter_segments"),
    path(
        "filter/campaign-sends/",
        admin_views.filter_campaign_sends,
        name="filter_campaign_sends",
    ),
    path(
        "segments/seed-starters/",
        admin_views.seed_starter_segments_view,
        name="seed_starter_segments",
    ),
    path("<uuid:campaign_id>/builder/", admin_views.campaign_builder, name="campaign_builder"),
    path("<uuid:campaign_id>/report/", admin_views.campaign_report, name="campaign_report"),
    path(
        "<uuid:campaign_id>/recipients/",
        admin_views.campaign_recipients,
        name="campaign_recipients",
    ),
    path(
        "<uuid:campaign_id>/recipients/<uuid:send_id>/activity/",
        admin_views.campaign_recipient_activity,
        name="campaign_recipient_activity",
    ),
    path(
        "journeys/<uuid:journey_id>/builder/",
        admin_views.journey_builder,
        name="journey_builder",
    ),
    path(
        "journeys/<uuid:journey_id>/report/",
        admin_views.journey_report,
        name="journey_report",
    ),
    # A/B testing
    path("<uuid:campaign_id>/ab-test/", admin_views.ab_test_setup, name="ab_test_setup"),
    path("ab-test/<uuid:ab_test_id>/", admin_views.ab_test_detail, name="ab_test_detail"),
    path("ab-test/<uuid:ab_test_id>/start/", admin_views.ab_test_start, name="ab_test_start"),
    path("ab-test/<uuid:ab_test_id>/cancel/", admin_views.ab_test_cancel, name="ab_test_cancel"),
]
