"""Admin-side view for the visual campaign builder.

Renders the builder shell: admin chrome (styled by admin-base.css, like the rest
of the admin) around an isolated canvas that carries the shop's frontend theme
tokens so the merchant sees their own branding while composing.
"""

import logging
import uuid
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext
from django.views.decorators.http import require_GET, require_POST

from staff_roles.decorators import requires_category

from .block_registry import get_block, get_palette
from .merge_fields import available_merge_fields
from .models import Campaign
from .services.block_serializer import render_block_canvas

logger = logging.getLogger("email_marketing")


def _site():
    from django.contrib.sites.models import Site

    return Site.objects.get(pk=1)


def _ajax_only(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


@staff_member_required
@requires_category("marketing", "full")
@require_GET
def filter_campaigns(request):
    """AJAX card filter for the Campaign changelist."""
    if not _ajax_only(request):
        return JsonResponse({"error": "invalid"}, status=400)
    # Only real campaigns: exclude child campaigns (A/B variants, winner sends,
    # recurring occurrences) which carry a parent. select_related the A/B sidecar
    # so the card's A/B badge doesn't N+1.
    qs = Campaign.objects.filter(site=_site(), parent__isnull=True).select_related(
        "segment", "ab_test"
    )
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(subject__icontains=search))
    for field in ("status", "campaign_type", "message_type"):
        val = request.GET.get(field, "").strip()
        if val:
            qs = qs.filter(**{field: val})
    total = qs.count()
    html = render_to_string(
        "admin/email_marketing/partials/campaign_cards.html",
        {"campaigns": qs.order_by("-created_at")[:100]},
        request=request,
    )
    return JsonResponse({"html": html, "count": total})


@staff_member_required
@requires_category("marketing", "full")
@require_GET
def filter_journeys(request):
    """AJAX card filter for the Journey changelist."""
    from .models import Journey, JourneyNode

    if not _ajax_only(request):
        return JsonResponse({"error": "invalid"}, status=400)
    qs = Journey.objects.filter(site=_site()).annotate(
        step_count=Count("nodes", filter=Q(nodes__node_type=JourneyNode.TYPE_SEND_EMAIL))
    )
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(name__icontains=search)
    for field in ("status", "trigger_event"):
        val = request.GET.get(field, "").strip()
        if val:
            qs = qs.filter(**{field: val})
    total = qs.count()
    html = render_to_string(
        "admin/email_marketing/partials/journey_cards.html",
        {"journeys": qs.order_by("-created_at")[:100]},
        request=request,
    )
    return JsonResponse({"html": html, "count": total})


@staff_member_required
@requires_category("marketing", "full")
@require_GET
def filter_subscribers(request):
    """AJAX card filter for the Subscriber changelist."""
    from .models import Subscriber

    if not _ajax_only(request):
        return JsonResponse({"error": "invalid"}, status=400)
    qs = Subscriber.objects.filter(site=_site()).select_related("user").prefetch_related("tags")
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(email__icontains=search)
    for field in ("status", "source"):
        val = request.GET.get(field, "").strip()
        if val:
            qs = qs.filter(**{field: val})
    tag = request.GET.get("tag", "").strip()
    if tag:
        qs = qs.filter(tags__slug=tag)
    total = qs.count()
    html = render_to_string(
        "admin/email_marketing/partials/subscriber_cards.html",
        {"subscribers": qs.order_by("-created_at")[:100]},
        request=request,
    )
    return JsonResponse({"html": html, "count": total})


@staff_member_required
@requires_category("marketing", "full")
@require_GET
def filter_segments(request):
    """AJAX card filter for the Segment changelist."""
    from .models import Segment

    if not _ajax_only(request):
        return JsonResponse({"error": "invalid"}, status=400)
    qs = Segment.objects.filter(site=_site())
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(Q(name__icontains=search) | Q(slug__icontains=search))
    kind = request.GET.get("kind", "").strip()
    if kind:
        qs = qs.filter(kind=kind)
    active = request.GET.get("is_active", "").strip()
    if active in ("0", "1"):
        qs = qs.filter(is_active=(active == "1"))
    total = qs.count()
    html = render_to_string(
        "admin/email_marketing/partials/segment_cards.html",
        {"segments": qs.order_by("name")[:100]},
        request=request,
    )
    return JsonResponse({"html": html, "count": total})


def _daily_series(qs, date_field, since, days):
    """Return (labels, counts) for a per-day count over the trailing window.

    Thin delegate to the shared ``reporting.daily_counts`` (single source of the
    per-day bucketing used by both the dashboard trends and the campaign report).
    """
    from .services.reporting import daily_counts

    return daily_counts(qs, date_field, since, days)


@staff_member_required
@requires_category("marketing", "full")
def campaign_studio_dashboard(request):
    """Central Campaign Studio hub: KPIs, trends, quick actions, recent activity."""
    from django.contrib.sites.models import Site

    from .models import (
        CampaignSend,
        Journey,
        JourneyEnrollment,
        Subscriber,
        SuppressionEntry,
    )

    site = Site.objects.get(pk=1)
    now = timezone.now()
    window_days = 30
    since = now - timedelta(days=window_days)

    subscribers = Subscriber.objects.filter(site=site)
    total_subscribers = subscribers.filter(status=Subscriber.STATUS_ACTIVE).count()
    new_subscribers = subscribers.filter(created_at__gte=since).count()

    campaigns = Campaign.objects.filter(site=site)
    active_campaigns = campaigns.filter(
        status__in=[Campaign.STATUS_SCHEDULED, Campaign.STATUS_SENDING]
    ).count()
    campaigns_sent = campaigns.filter(sent_at__gte=since).count()

    journeys = Journey.objects.filter(site=site)
    active_journeys = journeys.filter(status=Journey.STATUS_ACTIVE).count()
    enrolled_active = JourneyEnrollment.objects.filter(
        journey__site=site, status=JourneyEnrollment.STATUS_ACTIVE
    ).count()

    sends = CampaignSend.objects.filter(
        campaign__site=site,
        status__in=[
            CampaignSend.STATUS_QUEUED,
            CampaignSend.STATUS_SENDING,
            CampaignSend.STATUS_SENT,
        ],
    )
    sends_30d = sends.filter(created_at__gte=since).count()
    sent_total = sends.count()
    opened = sends.filter(opened=True).count()
    clicked = sends.filter(clicked=True).count()
    open_rate = round(opened / sent_total * 100, 1) if sent_total else 0.0
    click_rate = round(clicked / sent_total * 100, 1) if sent_total else 0.0

    # List hygiene: active (not-released) suppressed addresses; .objects excludes
    # soft-deleted entries, so this is the live do-not-mail count.
    suppressed_active = SuppressionEntry.objects.filter(site=site)
    suppressed_total = suppressed_active.count()
    suppressed_new = suppressed_active.filter(created_at__gte=since).count()

    growth_labels, growth_counts = _daily_series(subscribers, "created_at", since, window_days)
    send_labels, send_counts = _daily_series(sends, "created_at", since, window_days)

    recent_campaigns = campaigns.filter(parent__isnull=True).order_by("-created_at")[:6]
    active_journey_list = journeys.filter(status=Journey.STATUS_ACTIVE).order_by("-created_at")[:6]

    # Attributed revenue from the email channel over the window (best-effort — a
    # hiccup in the attribution layer must never break the Studio dashboard).
    email_revenue_display = None
    try:
        from decimal import Decimal

        from attribution.constants import CHANNEL_EMAIL
        from attribution.services import reporting as attribution_reporting
        from core.models import SiteSettings
        from core.utils.currency_helpers import format_money

        email_rev = next(
            (
                r["revenue"]
                for r in attribution_reporting.revenue_by_channel(since, now)
                if r["channel"] == CHANNEL_EMAIL
            ),
            Decimal("0.00"),
        )
        ccy = SiteSettings.get_settings().default_currency or "USD"
        email_revenue_display = format_money(email_rev, ccy)
    except Exception:  # noqa: BLE001
        logger.debug("dashboard: attributed email revenue unavailable", exc_info=True)

    context = {
        **admin_site_context(request),
        **_dashboard_ab_summary(site, since),
        "title": "Campaign Studio",
        "total_subscribers": total_subscribers,
        "new_subscribers": new_subscribers,
        "active_campaigns": active_campaigns,
        "campaigns_sent": campaigns_sent,
        "active_journeys": active_journeys,
        "enrolled_active": enrolled_active,
        "sends_30d": sends_30d,
        "open_rate": open_rate,
        "click_rate": click_rate,
        "suppressed_total": suppressed_total,
        "suppressed_new": suppressed_new,
        "email_revenue_display": email_revenue_display,
        "recent_campaigns": recent_campaigns,
        "active_journey_list": active_journey_list,
        "window_days": window_days,
        "start_date": since,
        "end_date": now,
        "chart_data": {
            "growth": {"labels": growth_labels, "counts": growth_counts},
            "sends": {"labels": send_labels, "counts": send_counts},
        },
    }
    return render(request, "admin/email_marketing/dashboard.html", context)


def admin_site_context(request):
    """Minimal admin context so base_site.html renders its chrome/sidebar."""
    from django.contrib import admin

    return admin.site.each_context(request)


@staff_member_required
@requires_category("marketing", "full")
def campaign_wizard(request):
    """Guided New-Campaign flow: pick type + details + audience, then design.

    Creates a draft Campaign and drops the merchant straight into the visual
    builder. Scheduling / recurrence stay on the campaign's change form (design
    the email first, then decide when it goes out).
    """
    from django.contrib.sites.models import Site
    from django.shortcuts import redirect

    from .models import MESSAGE_TYPE_CHOICES, Segment

    site = Site.objects.get(pk=1)

    if request.method == "POST":
        ctype = request.POST.get("campaign_type")
        if ctype not in (Campaign.TYPE_BROADCAST, Campaign.TYPE_RECURRING):
            ctype = Campaign.TYPE_BROADCAST
        message_type = request.POST.get("message_type") or "newsletter"
        if message_type not in dict(MESSAGE_TYPE_CHOICES):
            message_type = "newsletter"
        segment_id = request.POST.get("segment") or None
        segment = Segment.objects.filter(site=site, id=segment_id).first() if segment_id else None
        campaign = Campaign.objects.create(
            site=site,
            campaign_type=ctype,
            name=(request.POST.get("name") or "").strip() or "Untitled campaign",
            subject=(request.POST.get("subject") or "").strip(),
            preview_text=(request.POST.get("preview_text") or "").strip(),
            message_type=message_type,
            segment=segment,
            status=Campaign.STATUS_DRAFT,
            created_by=request.user if request.user.is_authenticated else None,
        )
        return redirect("email_marketing_admin:campaign_builder", campaign_id=campaign.id)

    context = {
        **admin_site_context(request),
        "title": "New Campaign",
        "segments": Segment.objects.filter(site=site, is_active=True).order_by("name"),
        "message_types": MESSAGE_TYPE_CHOICES,
        "total_subscribers": _active_subscriber_count(site),
    }
    return render(request, "admin/email_marketing/wizard.html", context)


def _active_subscriber_count(site):
    from .models import Subscriber

    return Subscriber.objects.filter(site=site, status=Subscriber.STATUS_ACTIVE).count()


def _theme_tokens() -> dict:
    """Flat {--theme-<key>: value} map from the shop's default theme.

    Applied to the canvas container by the builder JS so blocks render with the
    merchant's brand typography/colours — matching the storefront's own token
    prefix convention (design.theme_models) so cross-references resolve:
      colours     → --theme-color-{key}
      typography  → --theme-{key}          (fonts, sizes, weights, line-heights)
      elements    → --theme-element-{category}-{key}  (e.g. heading h1 size/font)
    """
    try:
        from design.theme_models import Theme

        theme = (
            Theme.objects.filter(is_default=True).first()
            or Theme.objects.filter(is_active=True).first()
        )
        if not theme:
            return {}
        tokens = theme.get_tokens() or {}
        out = {}
        for key, value in (tokens.get("colors") or {}).items():
            if isinstance(value, str):
                out[f"--theme-color-{key}"] = value
        for key, value in (tokens.get("typography") or {}).items():
            if isinstance(value, str):
                out[f"--theme-{key}"] = value
        # Element tokens are nested (elements.heading.h1-size, …) so the canvas
        # can style headings exactly as the storefront theme does.
        for category, props in (tokens.get("elements") or {}).items():
            if isinstance(props, dict):
                for key, value in props.items():
                    if isinstance(value, str):
                        out[f"--theme-element-{category}-{key}"] = value
        return out
    except Exception as exc:  # noqa: BLE001 — canvas still works without tokens
        logger.warning("Could not load theme tokens for builder: %s", exc)
        return {}


def _block_schemas() -> dict:
    """block_type -> {name, properties} for the property panel."""
    from .block_registry import get_registry

    return {
        bt: {"name": cfg.name, "properties": cfg.properties} for bt, cfg in get_registry().items()
    }


def _theme_css_url() -> str:
    """The shop's compiled theme CSS URL (element rules + @font-face + tokens).

    Loaded into the canvas Shadow DOM so blocks render with the real storefront
    typography, isolated from the admin.
    """
    try:
        from design.theme_models import Theme

        theme = (
            Theme.objects.filter(is_default=True).first()
            or Theme.objects.filter(is_active=True).first()
        )
        return theme.css_url if theme else ""
    except Exception:  # noqa: BLE001 — canvas still works without theme CSS
        return ""


@staff_member_required
@requires_category("marketing", "full")
def campaign_builder(request, campaign_id):
    """Render the visual builder for a single campaign."""
    campaign = get_object_or_404(Campaign, id=campaign_id)

    blocks = []
    for block in campaign.blocks.all():
        cfg = get_block(block.block_type)
        blocks.append(
            {
                "id": str(block.id),
                "block_type": block.block_type,
                "order": block.order,
                "content": block.content,
                "html": render_block_canvas(block),
                "name": cfg.name if cfg else block.block_type,
                "properties": cfg.properties if cfg else {},
            }
        )

    # Shared utility editors (color picker, etc.) + their base — the same
    # auto-discovered assets Page Builder / branding / Site Settings use, so the
    # email builder's controls stay visually consistent across the admin.
    from component_updates.utility_registry import get_utility_assets

    utility_assets = get_utility_assets()

    from django.templatetags.static import static

    context = {
        "campaign": campaign,
        "palette": get_palette(),
        "utility_css_files": utility_assets.get("css", []),
        "utility_js_files": utility_assets.get("js", []),
        # Passed via {{ ...|json_script }} in the template (CSP- and XSS-safe).
        "blocks_data": blocks,
        "schemas_data": _block_schemas(),
        "theme_tokens_data": _theme_tokens(),
        "merge_fields_data": available_merge_fields(),
        "builder_config": {"campaign_id": str(campaign.id)},
        # Stylesheets injected into the canvas Shadow DOM for storefront parity.
        "builder_assets": {
            "canvas_css": static("email_marketing/css/canvas.css"),
            "fa_css": static("core/vendor/fontawesome/css/all.min.css"),
            "theme_css": _theme_css_url(),
        },
        "admin_theme": getattr(request, "admin_theme", "light"),
    }
    return render(request, "email_marketing/builder.html", context)


# The node types a merchant can drag onto the journey canvas. The entry node is
# created automatically (the graph's root), so it isn't offered in the palette.
JOURNEY_NODE_PALETTE = [
    {
        "node_type": "send_email",
        "name": "Send email",
        "icon": "fas fa-envelope",
        "description": "Send a campaign to the subscriber.",
    },
    {
        "node_type": "wait_delay",
        "name": "Wait",
        "icon": "fas fa-clock",
        "description": "Pause before the next step.",
    },
    {
        "node_type": "branch",
        "name": "Branch",
        "icon": "fas fa-code-branch",
        "description": "Split the path on a Yes/No condition.",
    },
    {
        "node_type": "exit",
        "name": "Exit",
        "icon": "fas fa-flag-checkered",
        "description": "End the journey for the subscriber.",
    },
]


@staff_member_required
@requires_category("marketing", "full")
def journey_builder(request, journey_id):
    """Render the node/flowchart canvas for designing a journey.

    Reuses the campaign builder's CSP-safe scaffolding (json_script data-in,
    hidden CSRF form, external assets) around our own SVG-connector canvas.
    """
    from django.templatetags.static import static

    from .models import Journey, JourneyNode

    journey = get_object_or_404(Journey, id=journey_id)

    # Every journey has exactly one entry node — the graph's root. Create it on
    # first open so the canvas always has a starting point to build from.
    if not journey.nodes.filter(node_type=JourneyNode.TYPE_ENTRY).exists():
        JourneyNode.objects.create(
            journey=journey, node_type=JourneyNode.TYPE_ENTRY, pos_x=340, pos_y=40
        )

    nodes = [
        {
            "id": str(n.id),
            "node_type": n.node_type,
            "pos_x": n.pos_x,
            "pos_y": n.pos_y,
            "config": n.config or {},
        }
        for n in journey.nodes.all()
    ]
    edges = [
        {
            "id": str(e.id),
            "from": str(e.from_node_id),
            "to": str(e.to_node_id),
            "branch": e.branch,
        }
        for e in journey.edges.all()
    ]

    campaigns = [
        {"id": str(c.id), "name": c.name}
        for c in Campaign.objects.filter(site=_site()).order_by("name")
    ]
    from .models import Segment

    segments = [
        {"id": str(s.id), "name": s.name}
        for s in Segment.objects.filter(site=_site()).order_by("name")
    ]

    context = {
        "journey": journey,
        "admin_theme": getattr(request, "admin_theme", "light"),
        "nodes_data": nodes,
        "edges_data": edges,
        "palette_data": JOURNEY_NODE_PALETTE,
        "campaigns_data": campaigns,
        "segments_data": segments,
        "builder_config": {
            "journey_id": str(journey.id),
            "trigger": journey.get_trigger_event_display(),
            "audience": journey.target_segment.name if journey.target_segment_id else None,
            "status": journey.status,
            "status_display": journey.get_status_display(),
            "unit_choices": [
                {"value": v, "label": str(label)} for v, label in JourneyNode.UNIT_CHOICES
            ],
        },
        "builder_assets": {
            "fa_css": static("core/vendor/fontawesome/css/all.min.css"),
        },
    }
    return render(request, "email_marketing/journey_builder.html", context)


# ---------------------------------------------------------------------------
# A/B testing — setup wizard + results hub (reuses the campaign wizard +
# dashboard components; the engine lives in services/ab_testing.py).
# ---------------------------------------------------------------------------


def _clamp(value, lo, hi, default):
    try:
        return max(lo, min(int(value), hi))
    except (TypeError, ValueError):
        return default


@staff_member_required
@requires_category("marketing", "full")
def ab_test_setup(request, campaign_id):
    """Create an A/B test on a built campaign (subject or content variants)."""
    from django.contrib import messages
    from django.shortcuts import redirect

    from .models import ABTest
    from .services.ab_testing import create_ab_test

    campaign = get_object_or_404(Campaign, id=campaign_id, site=_site())

    # Recurring campaigns A/B test per occurrence via their Schedule, not this
    # one-shot broadcast wizard (a test on the template would never send) — send
    # the merchant to the schedule settings instead.
    if campaign.campaign_type == Campaign.TYPE_RECURRING:
        messages.info(
            request,
            "Recurring campaigns are A/B tested from their Schedule settings — add "
            "two or more subject lines there to test each occurrence.",
        )
        return redirect("admin:email_marketing_campaign_change", campaign.id)

    # Already has a test → jump to its hub rather than making a second one.
    existing = ABTest.objects.filter(campaign=campaign).first()
    if existing and existing.status != ABTest.STATUS_DRAFT:
        return redirect("email_marketing_admin:ab_test_detail", ab_test_id=existing.id)

    if request.method == "POST":
        test_type = request.POST.get("test_type")
        if test_type not in (ABTest.TYPE_SUBJECT, ABTest.TYPE_CONTENT):
            test_type = ABTest.TYPE_SUBJECT
        metric = request.POST.get("winner_metric")
        if metric not in (ABTest.METRIC_OPENS, ABTest.METRIC_CLICKS):
            metric = None
        result = create_ab_test(
            campaign,
            test_type=test_type,
            variant_subjects=[s for s in request.POST.getlist("subject") if s.strip()],
            num_variants=_clamp(request.POST.get("num_variants"), 2, 4, 2),
            sample_percent=_clamp(request.POST.get("sample_percent"), 2, 100, 20),
            winner_metric=metric,
            test_window_hours=_clamp(request.POST.get("test_window_hours"), 1, 168, 4),
            auto_send_winner=request.POST.get("auto_send_winner") == "on",
        )
        if result.get("error"):
            messages.error(request, _ab_error_message(result["error"]))
        else:
            return redirect("email_marketing_admin:ab_test_detail", ab_test_id=result["ab_test_id"])

    context = {
        **admin_site_context(request),
        "title": "Set up A/B test",
        "campaign": campaign,
        "type_choices": ABTest.TYPE_CHOICES,
        "metric_choices": ABTest.METRIC_CHOICES,
    }
    return render(request, "admin/email_marketing/abtest/setup.html", context)


@staff_member_required
@requires_category("marketing", "full")
def ab_test_detail(request, ab_test_id):
    """The A/B test hub: configure + start (draft), live results (testing/complete)."""
    import json

    from django.templatetags.static import static

    from .models import ABTest

    test = get_object_or_404(
        ABTest.objects.select_related("campaign", "winner").filter(campaign__site=_site()),
        id=ab_test_id,
    )
    rows = _ab_variant_rows(test)
    chart = {
        "labels": [r["label"] for r in rows],
        "open_rate": [r["open_rate"] for r in rows],
        "click_rate": [r["click_rate"] for r in rows],
    }
    significance = None
    if test.status in (ABTest.STATUS_TESTING, ABTest.STATUS_COMPLETE):
        winner_label = test.winner.label if test.winner_id else None
        significance = _significance(rows, test.winner_metric, winner_label)
    context = {
        **admin_site_context(request),
        "title": f"A/B test — {test.campaign.name}",
        "test": test,
        "variant_rows": rows,
        "significance": significance,
        "chart_data": chart,
        "is_content": test.test_type == ABTest.TYPE_CONTENT,
        "builder_url_name": "email_marketing_admin:campaign_builder",
        "chart_js": static("core/vendor/js/chart.umd.min.js"),
    }
    context["chart_data_json"] = json.dumps(chart)
    return render(request, "admin/email_marketing/abtest/detail.html", context)


@staff_member_required
@requires_category("marketing", "full")
@require_POST
def ab_test_start(request, ab_test_id):
    """Start a draft A/B test (send each variant to its bucket)."""
    from django.contrib import messages
    from django.shortcuts import redirect

    from .models import ABTest
    from .services.ab_testing import start_ab_test

    test = get_object_or_404(ABTest.objects.filter(campaign__site=_site()), id=ab_test_id)
    result = start_ab_test(test)
    if result.get("error"):
        messages.error(request, _ab_error_message(result["error"]))
    else:
        messages.success(request, "A/B test started — the winner is picked automatically.")
    return redirect("email_marketing_admin:ab_test_detail", ab_test_id=test.id)


@staff_member_required
@requires_category("marketing", "full")
@require_POST
def ab_test_cancel(request, ab_test_id):
    """Cancel a draft/testing A/B test."""
    from django.contrib import messages
    from django.shortcuts import redirect

    from .models import ABTest
    from .services.ab_testing import cancel_ab_test

    test = get_object_or_404(ABTest.objects.filter(campaign__site=_site()), id=ab_test_id)
    cancel_ab_test(test)
    messages.info(request, "A/B test cancelled.")
    return redirect("email_marketing_admin:ab_test_detail", ab_test_id=test.id)


@staff_member_required
@requires_category("marketing", "full")
def campaign_report(request, campaign_id):
    """Per-campaign delivery & engagement report (reach, opens/clicks, bounces)."""
    from .services import reporting

    campaign = get_object_or_404(Campaign.objects.filter(site=_site()), id=campaign_id)
    report = reporting.campaign_report(campaign)
    chart_data = reporting.campaign_timeseries(campaign)
    # Translated legend labels travel in the JSON payload (json_script can't carry
    # data-* attrs); the service stays i18n-free.
    chart_data["legend"] = {
        "sends": gettext("Sent"),
        "opens": gettext("Opened"),
        "clicks": gettext("Clicked"),
    }
    context = {
        **admin_site_context(request),
        "title": f"Report — {campaign.name}",
        "campaign": campaign,
        "report": report,
        "chart_data": chart_data,
        "link_clicks": reporting.campaign_link_clicks(campaign),
        "revenue": _revenue_with_display(reporting.campaign_revenue(campaign)),
    }
    return render(request, "admin/email_marketing/campaign/report.html", context)


def _revenue_with_display(rev):
    """Add base-currency display strings to the campaign_revenue dict for templating."""
    from core.models import SiteSettings
    from core.utils.currency_helpers import format_money

    ccy = SiteSettings.get_settings().default_currency or "USD"
    rev["revenue_display"] = format_money(rev["revenue"], ccy)
    rev["aov_display"] = format_money(rev["aov"], ccy)
    rev["revenue_per_email_display"] = format_money(rev["revenue_per_email"], ccy)
    return rev


@staff_member_required
@requires_category("marketing", "full")
def journey_report(request, journey_id):
    """Per-journey attributed revenue (total + per send-step) + enrollment funnel."""
    from .models import Journey
    from .services import reporting

    journey = get_object_or_404(Journey.objects.filter(site=_site()), id=journey_id)
    context = {
        **admin_site_context(request),
        "title": f"Report — {journey.name}",
        "journey": journey,
        "funnel": reporting.journey_funnel(journey),
        "revenue": _journey_revenue_display(reporting.journey_revenue(journey)),
    }
    return render(request, "admin/email_marketing/journey/report.html", context)


def _journey_revenue_display(rev):
    """Add base-currency display strings to the journey_revenue dict (+ each step)."""
    from core.models import SiteSettings
    from core.utils.currency_helpers import format_money

    ccy = SiteSettings.get_settings().default_currency or "USD"
    rev["revenue_display"] = format_money(rev["revenue"], ccy)
    rev["aov_display"] = format_money(rev["aov"], ccy)
    rev["revenue_per_enrollee_display"] = format_money(rev["revenue_per_enrollee"], ccy)
    for step in rev["steps"]:
        step["revenue_display"] = format_money(step["revenue"], ccy)
    return rev


@staff_member_required
@requires_category("marketing", "full")
def campaign_recipients(request, campaign_id):
    """Per-recipient activity drill-down for one campaign (list + timeline)."""
    campaign = get_object_or_404(Campaign.objects.filter(site=_site()), id=campaign_id)
    context = {
        **admin_site_context(request),
        "title": f"Recipients — {campaign.name}",
        "campaign": campaign,
    }
    return render(request, "admin/email_marketing/campaign/recipients.html", context)


@staff_member_required
@requires_category("marketing", "full")
@require_GET
def filter_campaign_sends(request):
    """AJAX card filter for a campaign's per-recipient sends (?campaign=<uuid>)."""
    from .models import Campaign, CampaignSend
    from .services.reporting import _scope_ids

    if not _ajax_only(request):
        return JsonResponse({"error": "invalid"}, status=400)
    try:
        cid = uuid.UUID(str(request.GET.get("campaign")))
    except (ValueError, TypeError):
        raise Http404("invalid campaign")
    campaign = get_object_or_404(Campaign.objects.filter(site=_site()), id=cid)

    qs = CampaignSend.objects.filter(campaign_id__in=_scope_ids(campaign)).select_related(
        "subscriber"
    )
    search = request.GET.get("search", "").strip()
    if search:
        qs = qs.filter(subscriber__email__icontains=search)
    engagement = request.GET.get("engagement", "").strip()
    if engagement == "opened":
        qs = qs.filter(opened=True)
    elif engagement == "clicked":
        qs = qs.filter(clicked=True)
    elif engagement == "bounced":
        qs = qs.filter(bounced=True)
    elif engagement == "not_opened":
        # Delivered but never opened — the re-engagement candidates.
        qs = qs.filter(status=CampaignSend.STATUS_SENT, bounced=False, opened=False)

    total = qs.count()
    html = render_to_string(
        "admin/email_marketing/partials/campaign_send_cards.html",
        {"sends": qs.order_by("-created_at")[:100], "campaign": campaign},
        request=request,
    )
    return JsonResponse({"html": html, "count": total})


@staff_member_required
@requires_category("marketing", "full")
@require_GET
def campaign_recipient_activity(request, campaign_id, send_id):
    """The tracked event timeline (opens/clicks/bounces) for one recipient's send."""
    from email_system.models import EmailEvent

    from .models import CampaignSend
    from .services.reporting import _scope_ids

    if not _ajax_only(request):
        return JsonResponse({"error": "invalid"}, status=400)
    campaign = get_object_or_404(Campaign.objects.filter(site=_site()), id=campaign_id)
    # Scope the send to this campaign (+ its A/B/recurring children) so a send from
    # another campaign can't be read via a guessed id.
    send = get_object_or_404(
        CampaignSend.objects.select_related("subscriber"),
        id=send_id,
        campaign_id__in=_scope_ids(campaign),
    )
    events = []
    if send.outbox_id:
        events = list(EmailEvent.objects.filter(email_id=send.outbox_id).order_by("occurred_at"))
    html = render_to_string(
        "admin/email_marketing/partials/recipient_activity.html",
        {"send": send, "events": events},
        request=request,
    )
    return JsonResponse({"html": html})


def _ab_variant_rows(test):
    """Per-variant rows for the detail page — snapshot when complete, else live."""
    from .models import ABTest, CampaignSend

    rows = []
    # Snapshots (ABVariant.opened/clicked) are only written when a test is *decided*.
    # A cancelled test — whether cancelled as a draft or mid-run — never got a
    # snapshot, so fall through to its live CampaignSend metrics instead of showing 0%.
    complete = test.status == ABTest.STATUS_COMPLETE
    for variant in test.variants.select_related("campaign").order_by("label"):
        if complete:
            recipients, opened, clicked = variant.recipients, variant.opened, variant.clicked
        else:
            sends = CampaignSend.objects.filter(campaign=variant.campaign)
            recipients = sends.exclude(status=CampaignSend.STATUS_SKIPPED).count()
            opened = sends.filter(opened=True).count()
            clicked = sends.filter(clicked=True).count()
        rows.append(
            {
                "id": str(variant.id),
                "label": variant.label,
                "subject": variant.campaign.subject,
                "campaign_id": str(variant.campaign_id),
                "recipients": recipients,
                "opened": opened,
                "clicked": clicked,
                "open_rate": round(100 * opened / recipients, 1) if recipients else 0.0,
                "click_rate": round(100 * clicked / recipients, 1) if recipients else 0.0,
                "is_winner": test.winner_id == variant.id,
            }
        )
    return rows


def _significance(rows, metric, winner_label=None):
    """Statistical verdict for the results hub, from the per-variant rows.

    Compares the leader (the decided winner, else the top-rate arm) against its
    closest rival and returns ``{verdict, confidence, leader}`` — or None when
    there aren't two arms to compare. ``verdict`` is one of "significant",
    "inconclusive", or "insufficient" (not enough data to trust). Works off the
    same rows for a live (testing) or snapshotted (complete) test.
    """
    from email_marketing.models import ABTest
    from email_marketing.services.ab_stats import is_reliable, two_proportion_confidence

    if len(rows) < 2:
        return None
    success_key = "clicked" if metric == ABTest.METRIC_CLICKS else "opened"

    def _raw_rate(row):
        # Rank on the exact rate, not the display value — rounded percentages can
        # tie two arms that actually differ, badging the wrong live leader.
        return row[success_key] / row["recipients"] if row["recipients"] else 0.0

    ranked = sorted(rows, key=_raw_rate, reverse=True)
    leader = next((r for r in rows if r["label"] == winner_label), None) or ranked[0]
    rival = next((r for r in ranked if r["label"] != leader["label"]), None)
    if rival is None:
        return None

    lw, ln = leader[success_key], leader["recipients"]
    rw, rn = rival[success_key], rival["recipients"]
    confidence = two_proportion_confidence(lw, ln, rw, rn)
    if not is_reliable(lw, ln, rw, rn):
        verdict = "insufficient"
    elif confidence >= ABTest.SIGNIFICANCE_THRESHOLD:
        verdict = "significant"
    else:
        verdict = "inconclusive"
    return {"verdict": verdict, "confidence": round(confidence * 100, 1), "leader": leader["label"]}


def _dashboard_ab_summary(site, since):
    """A/B activity for the Campaign Studio dashboard: running/decided counts, the
    most recent tests each with a trust verdict, and a compact journey split-test
    tally.

    Completed tests read the stored ``winner_confidence`` (null when the result
    was too small to trust — surfaced as "not enough data"); running tests get a
    live verdict from their current sends. Broadcast and recurring-occurrence
    tests are both ``ABTest`` rows, so both are included.
    """
    from .models import ABTest, Journey, JourneyNode

    tests = ABTest.objects.filter(campaign__site=site)
    running = tests.filter(status=ABTest.STATUS_TESTING).count()
    decided_30d = tests.filter(status=ABTest.STATUS_COMPLETE, decided_at__gte=since).count()

    recent = []
    recent_qs = (
        tests.filter(status__in=[ABTest.STATUS_TESTING, ABTest.STATUS_COMPLETE])
        .select_related("campaign", "winner")
        .order_by("-updated_at")[:6]
    )
    for test in recent_qs:
        winner_label = test.winner.label if test.winner_id else None
        if test.status == ABTest.STATUS_COMPLETE:
            conf = test.winner_confidence
            if conf is not None:
                verdict = "significant" if conf >= ABTest.SIGNIFICANCE_THRESHOLD else "inconclusive"
                confidence = round(conf * 100, 1)
            else:
                # None = a genuinely-unreliable test OR a legacy test decided before
                # winner_confidence existed. Recompute from the (cheap, snapshot-based)
                # rows rather than always reading "not enough data".
                sig = _significance(_ab_variant_rows(test), test.winner_metric, winner_label)
                verdict = sig["verdict"] if sig else "insufficient"
                confidence = sig["confidence"] if sig else None
            leader = winner_label
        else:  # testing — live verdict from current sends
            sig = _significance(_ab_variant_rows(test), test.winner_metric)
            verdict = sig["verdict"] if sig else None
            confidence = sig["confidence"] if sig else None
            leader = sig["leader"] if sig else None
        recent.append(
            {
                "id": str(test.id),
                "campaign_name": test.campaign.name,
                "test_type_display": test.get_test_type_display(),
                "status": test.status,
                "status_display": test.get_status_display(),
                "winner_label": winner_label,
                "leader": leader,
                "verdict": verdict,
                "confidence": confidence,
            }
        )

    # Journey A/B is a per-node continuous split test (no ABTest row) — tally it.
    journey_ab_steps = journey_ab_winners = 0
    for node in JourneyNode.objects.filter(
        journey__site=site,
        journey__status=Journey.STATUS_ACTIVE,
        node_type=JourneyNode.TYPE_SEND_EMAIL,
    ):
        if node.is_ab_send:
            journey_ab_steps += 1
            if node.ab_winner_label:
                journey_ab_winners += 1

    return {
        "ab_running": running,
        "ab_decided_30d": decided_30d,
        "recent_ab_tests": recent,
        "journey_ab_steps": journey_ab_steps,
        "journey_ab_winners": journey_ab_winners,
    }


def _ab_error_message(code):
    return {
        "audience_too_small": "Your audience is too small to split for a test.",
        "need_two_variants": "An A/B test needs at least two variants.",
        "need_two_subjects": "Enter at least two subject lines to test.",
        "test_already_running": "This campaign already has a running A/B test.",
        "no_account": "No sending email account is configured.",
        "invalid_status": "This test can't be started in its current state.",
    }.get(code, "Something went wrong with the A/B test.")


@staff_member_required
@requires_category("marketing", "full")
@require_POST
def seed_starter_segments_view(request):
    """Seed ready-made starter audiences from the store's own customer, loyalty
    and affiliate data (idempotent)."""
    from django.contrib import messages
    from django.shortcuts import redirect

    from .services.starter_segments import seed_starter_segments

    result = seed_starter_segments(_site())
    created, skipped = result["created"], result["skipped"]
    if created:
        messages.success(
            request,
            f"Added {len(created)} starter audience(s): {', '.join(created)}.",
        )
    elif skipped:
        messages.info(
            request,
            f"Starter audiences are already set up ({len(skipped)} already exist).",
        )
    else:
        messages.info(
            request,
            "No starter audiences to add yet — set up loyalty tiers, customer "
            "segments or affiliates first.",
        )
    return redirect("admin:email_marketing_segment_changelist")
