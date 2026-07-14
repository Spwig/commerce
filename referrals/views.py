"""
Referral Program Views

Admin views for dashboard, filtering, and managing referrals.
"""

import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import (
    ReferralAttribution,
    ReferralEvent,
    ReferralIdentity,
    ReferralProgram,
    ReferralReward,
)
from .services import create_rewards, issue_reward, revoke_reward


@staff_member_required
def referral_dashboard(request):
    """
    Main referral program dashboard showing KPIs, analytics, and settings.
    """
    # Get or create program
    program = ReferralProgram.get_program()

    # Get date range (default: last 30 days)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate KPIs
    total_referrals = ReferralAttribution.objects.count()

    # Pending approvals
    pending_approvals = ReferralAttribution.objects.filter(status="pending").count()

    # Success rate (approved / total)
    approved_count = ReferralAttribution.objects.filter(status="approved").count()
    success_rate = (approved_count / total_referrals * 100) if total_referrals > 0 else 0

    # Top referrer
    top_referrer = None
    top_referrer_data = (
        ReferralAttribution.objects.filter(status="approved", referrer_identity__isnull=False)
        .values(
            "referrer_identity__id",
            "referrer_identity__customer__email",
            "referrer_identity__customer__first_name",
            "referrer_identity__customer__last_name",
        )
        .annotate(referral_count=Count("id"))
        .order_by("-referral_count")
        .first()
    )

    if top_referrer_data:
        full_name = f"{top_referrer_data['referrer_identity__customer__first_name']} {top_referrer_data['referrer_identity__customer__last_name']}".strip()
        top_referrer = {
            "id": top_referrer_data["referrer_identity__id"],
            "name": full_name or top_referrer_data["referrer_identity__customer__email"],
            "count": top_referrer_data["referral_count"],
        }

    # Total rewards issued
    total_rewards_issued = (
        ReferralReward.objects.filter(status__in=["issued", "redeemed"]).aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    # Conversion rate (orders / clicks)
    total_clicks = ReferralEvent.objects.filter(event_type="click").count()
    total_orders = ReferralEvent.objects.filter(event_type="order").count()
    conversion_rate = (total_orders / total_clicks * 100) if total_clicks > 0 else 0

    # Referrals over time (last 30 days)
    referrals_trend = []
    for i in range(30):
        date = start_date + timedelta(days=i)
        next_date = date + timedelta(days=1)
        count = ReferralAttribution.objects.filter(
            created_at__gte=date, created_at__lt=next_date
        ).count()
        referrals_trend.append({"date": date.strftime("%Y-%m-%d"), "count": count})

    # Conversion funnel data
    funnel_data = {
        "clicks": ReferralEvent.objects.filter(event_type="click").count(),
        "signups": ReferralEvent.objects.filter(event_type="signup").count(),
        "orders": ReferralEvent.objects.filter(event_type="order").count(),
        "approved": ReferralAttribution.objects.filter(status="approved").count(),
    }

    # Reward distribution by status
    reward_distribution = []
    statuses = ReferralReward.STATUS_CHOICES
    for status_code, status_name in statuses:
        count = ReferralReward.objects.filter(status=status_code).count()
        if count > 0:
            # Status colors
            colors = {
                "pending": "#ffc107",
                "issued": "#28a745",
                "redeemed": "#17a2b8",
                "expired": "#6c757d",
                "revoked": "#dc3545",
            }
            reward_distribution.append(
                {
                    "status": status_code,
                    "name": str(status_name),
                    "count": count,
                    "color": colors.get(status_code, "#666"),
                }
            )

    # Top 10 referrers
    top_referrers = []
    top_referrer_list = (
        ReferralAttribution.objects.filter(status="approved", referrer_identity__isnull=False)
        .values(
            "referrer_identity__id",
            "referrer_identity__customer__id",
            "referrer_identity__customer__email",
            "referrer_identity__customer__first_name",
            "referrer_identity__customer__last_name",
        )
        .annotate(referral_count=Count("id"))
        .order_by("-referral_count")[:10]
    )

    for data in top_referrer_list:
        full_name = f"{data['referrer_identity__customer__first_name']} {data['referrer_identity__customer__last_name']}".strip()
        top_referrers.append(
            {
                "id": data["referrer_identity__customer__id"],
                "identity_id": data["referrer_identity__id"],
                "name": full_name or data["referrer_identity__customer__email"],
                "count": data["referral_count"],
            }
        )

    # Pending attributions (last 10)
    pending_attributions = (
        ReferralAttribution.objects.filter(status="pending")
        .select_related("referrer_identity__customer", "referee_customer", "first_order")
        .order_by("-created_at")[:10]
    )

    # Recent rewards (last 10)
    recent_rewards = (
        ReferralReward.objects.filter(status__in=["issued", "redeemed"])
        .select_related("customer", "referrer_identity__customer")
        .order_by("-issued_at")[:10]
    )

    # Fraud flags queue (high risk pending attributions)
    fraud_flags = (
        ReferralAttribution.objects.filter(status="pending", risk_score__gte=50)
        .select_related("referrer_identity__customer", "referee_customer")
        .order_by("-risk_score")[:10]
    )

    # Handle settings form submission
    if request.method == "POST":
        # Update program settings
        program.status = request.POST.get("status", "draft")
        program.name = request.POST.get("name", program.name)
        program.save()

        messages.success(request, _("Referral program settings updated successfully."))
        return redirect("referrals:dashboard")

    context = {
        # KPIs
        "total_referrals": total_referrals,
        "pending_approvals": pending_approvals,
        "success_rate": round(success_rate, 1),
        "top_referrer": top_referrer,
        "total_rewards_issued": total_rewards_issued,
        "conversion_rate": round(conversion_rate, 1),
        # Charts data (JSON)
        "referrals_trend_json": json.dumps(referrals_trend),
        "funnel_data_json": json.dumps(funnel_data),
        "reward_distribution_json": json.dumps(reward_distribution),
        # Lists
        "top_referrers": top_referrers,
        "pending_attributions": pending_attributions,
        "recent_rewards": recent_rewards,
        "fraud_flags": fraud_flags,
        # Program settings
        "program": program,
        "status_choices": ReferralProgram.STATUS_CHOICES,
        # Date range
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "admin/referrals/dashboard.html", context)


@staff_member_required
def approve_attribution(request, pk):
    """
    Approve a pending referral attribution and create rewards.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    attribution = get_object_or_404(ReferralAttribution, pk=pk)

    if attribution.status != "pending":
        return JsonResponse(
            {"success": False, "message": _("Attribution is not pending")}, status=400
        )

    # Approve attribution
    attribution.approve(reviewed_by=request.user)

    # Create rewards
    try:
        referrer_reward, referee_reward = create_rewards(attribution)
        messages.success(request, _("Attribution approved and rewards created."))

        return JsonResponse(
            {
                "success": True,
                "message": _("Attribution approved successfully"),
                "attribution": {
                    "id": attribution.id,
                    "status": attribution.status,
                    "rewards_created": True,
                },
            }
        )
    except Exception as e:
        return JsonResponse(
            {
                "success": False,
                "message": str(_("Error creating rewards: %(error)s") % {"error": str(e)}),
            },
            status=500,
        )


@staff_member_required
def reject_attribution(request, pk):
    """
    Reject a pending referral attribution.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    attribution = get_object_or_404(ReferralAttribution, pk=pk)

    if attribution.status != "pending":
        return JsonResponse(
            {"success": False, "message": _("Attribution is not pending")}, status=400
        )

    # Get rejection reason and notes from request
    reason = request.POST.get("reason", "manual_rejection")
    notes = request.POST.get("notes", "")

    # Reject attribution
    attribution.reject(reason=reason, notes=notes, reviewed_by=request.user)

    messages.success(request, _("Attribution rejected."))

    return JsonResponse(
        {
            "success": True,
            "message": _("Attribution rejected successfully"),
            "attribution": {
                "id": attribution.id,
                "status": attribution.status,
                "rejection_reason": attribution.rejection_reason,
            },
        }
    )


@staff_member_required
def issue_reward_view(request, pk):
    """
    Issue a pending reward to customer.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    reward = get_object_or_404(ReferralReward, pk=pk)

    if reward.status != "pending":
        return JsonResponse({"success": False, "message": _("Reward is not pending")}, status=400)

    # Issue reward
    try:
        success = issue_reward(reward)

        if success:
            messages.success(request, _("Reward issued successfully."))
            return JsonResponse(
                {
                    "success": True,
                    "message": _("Reward issued successfully"),
                    "reward": {
                        "id": reward.id,
                        "status": reward.status,
                        "issued_at": reward.issued_at.isoformat() if reward.issued_at else None,
                    },
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": _("Failed to issue reward")}, status=500
            )

    except Exception as e:
        return JsonResponse(
            {
                "success": False,
                "message": str(_("Error issuing reward: %(error)s") % {"error": str(e)}),
            },
            status=500,
        )


@staff_member_required
def revoke_reward_view(request, pk):
    """
    Revoke an issued reward.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    reward = get_object_or_404(ReferralReward, pk=pk)

    if reward.status not in ["pending", "issued"]:
        return JsonResponse(
            {"success": False, "message": _("Reward cannot be revoked")}, status=400
        )

    # Get revocation reason from request
    reason = request.POST.get("reason", "Manual revocation")

    # Revoke reward
    try:
        success = revoke_reward(reward, reason=reason)

        if success:
            messages.success(request, _("Reward revoked successfully."))
            return JsonResponse(
                {
                    "success": True,
                    "message": _("Reward revoked successfully"),
                    "reward": {
                        "id": reward.id,
                        "status": reward.status,
                        "revocation_reason": reward.revocation_reason,
                    },
                }
            )
        else:
            return JsonResponse(
                {"success": False, "message": _("Failed to revoke reward")}, status=500
            )

    except Exception as e:
        return JsonResponse(
            {
                "success": False,
                "message": str(_("Error revoking reward: %(error)s") % {"error": str(e)}),
            },
            status=500,
        )


@staff_member_required
def filter_referrers(request):
    """
    AJAX endpoint for filtering referrers (ReferralIdentity).

    Supports filtering by:
    - search: Customer name, email, or token
    - sort: Sort field (created_at, total_conversions, total_rewards_earned)
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all referrers
    referrers = ReferralIdentity.objects.select_related("customer")

    # Apply search filter
    search = request.GET.get("search", "").strip()
    if search:
        referrers = referrers.filter(
            Q(customer__first_name__icontains=search)
            | Q(customer__last_name__icontains=search)
            | Q(customer__email__icontains=search)
            | Q(token__icontains=search)
        )

    # Apply sort
    sort = request.GET.get("sort", "-created_at").strip()
    valid_sorts = [
        "created_at",
        "-created_at",
        "total_conversions",
        "-total_conversions",
        "total_rewards_earned",
        "-total_rewards_earned",
        "total_clicks",
        "-total_clicks",
    ]
    if sort in valid_sorts:
        referrers = referrers.order_by(sort)
    else:
        referrers = referrers.order_by("-created_at")

    # Pagination (limit to 50)
    referrers = referrers[:50]

    # Render partial template
    html = render_to_string(
        "admin/referrals/partials/referrer_cards.html", {"referrers": referrers}, request=request
    )

    return JsonResponse({"html": html, "count": referrers.count()})


@staff_member_required
def filter_attributions(request):
    """
    AJAX endpoint for filtering referral attributions.

    Supports filtering by:
    - search: Customer email, referrer name
    - status: pending, approved, rejected
    - has_order: yes, no
    - sort: created_at, -created_at, status
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all attributions
    attributions = ReferralAttribution.objects.select_related(
        "referee_customer", "referrer_identity__customer", "first_order"
    )

    # Apply search filter
    search = request.GET.get("search", "").strip()
    if search:
        attributions = attributions.filter(
            Q(referee_customer__email__icontains=search)
            | Q(referee_customer__first_name__icontains=search)
            | Q(referee_customer__last_name__icontains=search)
            | Q(referrer_identity__customer__first_name__icontains=search)
            | Q(referrer_identity__customer__last_name__icontains=search)
            | Q(referrer_identity__customer__email__icontains=search)
        )

    # Apply status filter
    status = request.GET.get("status", "").strip()
    if status:
        attributions = attributions.filter(status=status)

    # Apply has_order filter
    has_order = request.GET.get("has_order", "").strip()
    if has_order == "yes":
        attributions = attributions.filter(first_order__isnull=False)
    elif has_order == "no":
        attributions = attributions.filter(first_order__isnull=True)

    # Apply sort
    sort = request.GET.get("sort", "-created_at").strip()
    valid_sorts = ["created_at", "-created_at", "status", "-status"]
    if sort in valid_sorts:
        attributions = attributions.order_by(sort)
    else:
        attributions = attributions.order_by("-created_at")

    # Pagination (limit to 50)
    attributions = attributions[:50]

    # Render partial template
    html = render_to_string(
        "admin/referrals/partials/attribution_cards.html",
        {"attributions": attributions},
        request=request,
    )

    return JsonResponse({"html": html, "count": attributions.count()})


@staff_member_required
def filter_rewards(request):
    """
    AJAX endpoint for filtering referral rewards.

    Supports filtering by:
    - search: Referrer email, voucher code
    - status: pending, issued, revoked
    - reward_type: percentage, fixed, custom
    - expired: active, expired
    - sort: created_at, -created_at, amount, -amount, expires_at
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all rewards
    rewards = ReferralReward.objects.select_related(
        "referrer_identity__customer", "attribution", "customer"
    )

    # Apply search filter
    search = request.GET.get("search", "").strip()
    if search:
        rewards = rewards.filter(
            Q(referrer_identity__customer__email__icontains=search)
            | Q(referrer_identity__customer__first_name__icontains=search)
            | Q(referrer_identity__customer__last_name__icontains=search)
            | Q(customer__email__icontains=search)
        )

    # Apply status filter
    status = request.GET.get("status", "").strip()
    if status:
        rewards = rewards.filter(status=status)

    # Apply reward type filter
    reward_type = request.GET.get("reward_type", "").strip()
    if reward_type:
        rewards = rewards.filter(kind=reward_type)

    # Apply expiration filter
    expired = request.GET.get("expired", "").strip()
    if expired == "active":
        from django.utils import timezone

        rewards = rewards.filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now()))
    elif expired == "expired":
        from django.utils import timezone

        rewards = rewards.filter(expires_at__lte=timezone.now())

    # Apply sort
    sort = request.GET.get("sort", "-created_at").strip()
    valid_sorts = ["created_at", "-created_at", "amount", "-amount", "expires_at", "-expires_at"]
    rewards = rewards.order_by(sort) if sort in valid_sorts else rewards.order_by("-created_at")

    # Pagination (limit to 50)
    rewards = rewards[:50]

    # Render partial template
    html = render_to_string(
        "admin/referrals/partials/reward_cards.html", {"rewards": rewards}, request=request
    )

    return JsonResponse({"html": html, "count": rewards.count()})


@staff_member_required
def filter_events(request):
    """
    AJAX endpoint for filtering referral events.

    Supports filtering by:
    - search: Customer email, referral token
    - event_type: click, signup, order
    - date_from: Start date
    - date_to: End date
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Start with all events
    events = ReferralEvent.objects.select_related(
        "customer", "referrer_identity__customer", "order"
    )

    # Apply filters
    search = request.GET.get("search", "").strip()
    if search:
        events = events.filter(
            Q(customer__email__icontains=search)
            | Q(referrer_identity__token__icontains=search)
            | Q(order__order_number__icontains=search)
        )

    event_type = request.GET.get("event_type", "").strip()
    if event_type:
        events = events.filter(event_type=event_type)

    date_from = request.GET.get("date_from", "").strip()
    if date_from:
        events = events.filter(created_at__gte=date_from)

    date_to = request.GET.get("date_to", "").strip()
    if date_to:
        events = events.filter(created_at__lte=date_to)

    # Sort
    sort = request.GET.get("sort", "-created_at").strip()
    valid_sorts = ["created_at", "-created_at"]
    events = events.order_by(sort) if sort in valid_sorts else events.order_by("-created_at")

    # Pagination (limit to 50)
    events = events[:50]

    # Render partial template
    html = render_to_string(
        "admin/referrals/partials/event_cards.html", {"events": events}, request=request
    )

    return JsonResponse({"html": html, "count": events.count()})
