"""
Admin views for accounts app.

Provides staff-only views for analytics and reporting.
"""

import json
from datetime import datetime, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET

from accounts.models import CommunicationPreference, PreferenceChangeLog
from accounts.services.preference_analytics_service import PreferenceAnalyticsService


@staff_member_required
def preference_analytics_dashboard(request):
    """
    Analytics dashboard for communication preferences.

    Shows opt-in rates, verification rates, trends, and engagement metrics.
    """
    # Get period from request (default: last_30_days)
    period = request.GET.get("period", "last_30_days")
    compare = request.GET.get("compare") == "true"

    # Custom date range
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        try:
            start_date = datetime.fromisoformat(start_date)
            end_date = datetime.fromisoformat(end_date)
            period = "custom"
        except ValueError:
            start_date = None
            end_date = None

    # Get date range
    date_range = PreferenceAnalyticsService.get_date_range_for_period(
        period=period, start_date=start_date, end_date=end_date
    )

    # Get all metrics
    action_cards = PreferenceAnalyticsService.get_action_cards()
    opt_in_metrics = PreferenceAnalyticsService.get_opt_in_metrics(
        start_date=date_range[0], end_date=date_range[1], compare=compare
    )
    app_breakdown = PreferenceAnalyticsService.get_app_preference_breakdown()
    opt_in_trend = PreferenceAnalyticsService.get_opt_in_over_time(
        start_date=date_range[0], end_date=date_range[1]
    )
    verification_funnel = PreferenceAnalyticsService.get_verification_funnel()

    context = {
        "title": "Communication Preference Analytics",
        "period": period,
        "compare": compare,
        "start_date": date_range[0].strftime("%Y-%m-%d"),
        "end_date": date_range[1].strftime("%Y-%m-%d"),
        "action_cards": action_cards,
        "opt_in_metrics": opt_in_metrics,
        "app_breakdown": app_breakdown,
        "opt_in_trend": mark_safe(json.dumps(opt_in_trend)),
        "verification_funnel": verification_funnel,
    }

    return render(request, "admin/accounts/preference_analytics_dashboard.html", context)


@staff_member_required
@require_GET
def filter_preferences(request):
    """AJAX filter endpoint for CommunicationPreference change list."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = CommunicationPreference.objects.select_related("user").all()

    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(user__email__icontains=search)
            | Q(user__username__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
        )

    email = request.GET.get("email", "").strip()
    if email == "true":
        queryset = queryset.filter(email_enabled=True)
    elif email == "false":
        queryset = queryset.filter(email_enabled=False)

    sms = request.GET.get("sms", "").strip()
    if sms == "true":
        queryset = queryset.filter(sms_enabled=True)
    elif sms == "false":
        queryset = queryset.filter(sms_enabled=False)

    marketing = request.GET.get("marketing", "").strip()
    if marketing == "opted_in":
        queryset = queryset.filter(Q(email_marketing=True) | Q(sms_marketing=True))
    elif marketing == "opted_out":
        queryset = queryset.filter(email_marketing=False, sms_marketing=False)

    source = request.GET.get("source", "").strip()
    if source:
        queryset = queryset.filter(consent_source=source)

    total_count = queryset.count()
    preferences = queryset.order_by("-updated_at")[:100]

    html = render_to_string(
        "admin/accounts/communicationpreference/partials/preference_cards.html",
        {"preferences": preferences},
        request=request,
    )

    return JsonResponse({"html": html, "count": total_count})


@staff_member_required
@require_GET
def filter_preference_changelogs(request):
    """AJAX filter endpoint for PreferenceChangeLog change list."""
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    queryset = PreferenceChangeLog.objects.select_related("user", "preference").all()

    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(user__email__icontains=search)
            | Q(user__username__icontains=search)
            | Q(action__icontains=search)
            | Q(ip_address__icontains=search)
        )

    source = request.GET.get("source", "").strip()
    if source:
        queryset = queryset.filter(source=source)

    period = request.GET.get("period", "").strip()
    if period:
        now = timezone.now()
        if period == "today":
            queryset = queryset.filter(timestamp__date=now.date())
        elif period == "7days":
            queryset = queryset.filter(timestamp__gte=now - timedelta(days=7))
        elif period == "30days":
            queryset = queryset.filter(timestamp__gte=now - timedelta(days=30))
        elif period == "90days":
            queryset = queryset.filter(timestamp__gte=now - timedelta(days=90))

    total_count = queryset.count()
    logs = queryset.order_by("-timestamp")[:100]

    html = render_to_string(
        "admin/accounts/preferencechangelog/partials/changelog_cards.html",
        {"logs": logs},
        request=request,
    )

    return JsonResponse({"html": html, "count": total_count})
