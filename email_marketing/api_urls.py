"""Builder API URLs (non-i18n, staff-only)."""

from django.urls import path

from . import api_views

app_name = "email_marketing_api"

urlpatterns = [
    path("blocks/", api_views.create_block, name="create_block"),
    path("blocks/<uuid:block_id>/", api_views.update_block, name="update_block"),
    path("blocks/<uuid:block_id>/delete/", api_views.delete_block, name="delete_block"),
    path("blocks/reorder/", api_views.reorder_blocks, name="reorder_blocks"),
    path("segments/preview-count/", api_views.preview_segment_count, name="preview_segment_count"),
    path("vouchers/", api_views.voucher_search, name="voucher_search"),
    # Journey builder — flowchart node + edge CRUD.
    path(
        "journeys/<uuid:journey_id>/nodes/",
        api_views.create_journey_node,
        name="create_journey_node",
    ),
    path(
        "journeys/nodes/<uuid:node_id>/",
        api_views.update_journey_node,
        name="update_journey_node",
    ),
    path(
        "journeys/nodes/<uuid:node_id>/delete/",
        api_views.delete_journey_node,
        name="delete_journey_node",
    ),
    path(
        "journeys/<uuid:journey_id>/edges/",
        api_views.create_journey_edge,
        name="create_journey_edge",
    ),
    path(
        "journeys/edges/<uuid:edge_id>/delete/",
        api_views.delete_journey_edge,
        name="delete_journey_edge",
    ),
    # Starters + sharing (import/export).
    path("journeys/templates/", api_views.list_journey_templates, name="list_journey_templates"),
    path(
        "journeys/<uuid:journey_id>/apply-template/",
        api_views.apply_journey_template,
        name="apply_journey_template",
    ),
    path(
        "journeys/<uuid:journey_id>/export/",
        api_views.export_journey,
        name="export_journey",
    ),
    path(
        "journeys/<uuid:journey_id>/import/",
        api_views.import_journey,
        name="import_journey",
    ),
    # Live stats + validation + activation gate.
    path(
        "journeys/<uuid:journey_id>/node-stats/",
        api_views.journey_node_stats,
        name="journey_node_stats",
    ),
    path(
        "journeys/<uuid:journey_id>/validate/",
        api_views.validate_journey_view,
        name="validate_journey",
    ),
    path(
        "journeys/<uuid:journey_id>/status/",
        api_views.set_journey_status,
        name="set_journey_status",
    ),
    path("campaigns/<uuid:campaign_id>/save/", api_views.save_campaign, name="save_campaign"),
    path(
        "campaigns/<uuid:campaign_id>/preview/",
        api_views.preview_campaign,
        name="preview_campaign",
    ),
]
