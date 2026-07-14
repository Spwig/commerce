"""
Social Sharing Views

Admin views for filtering and managing social shares.
"""

from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import ShareCount, SocialShare
from .settings_models import SocialSharingSettings


@staff_member_required
def social_sharing_dashboard(request):
    """
    Main social sharing dashboard showing KPIs, analytics, and settings.
    """
    # Get date range (default: last 30 days)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Calculate KPIs
    total_shares = SocialShare.objects.count()

    # Shares today
    shares_today = SocialShare.objects.filter(shared_at__gte=today_start).count()

    # Shares this month (last 30 days)
    shares_this_month = SocialShare.objects.filter(
        shared_at__gte=start_date, shared_at__lte=end_date
    ).count()

    # Top platform
    top_platform_data = (
        ShareCount.objects.values("platform")
        .annotate(total_count=Sum("count"))
        .order_by("-total_count")
        .first()
    )

    top_platform = {
        "platform": top_platform_data["platform"] if top_platform_data else None,
        "count": top_platform_data["total_count"] if top_platform_data else 0,
    }

    # Top shared product
    product_ct = ContentType.objects.filter(model="product").first()
    top_product = None
    if product_ct:
        top_product_data = (
            ShareCount.objects.filter(content_type=product_ct)
            .values("object_id")
            .annotate(total_count=Sum("count"))
            .order_by("-total_count")
            .first()
        )

        if top_product_data:
            from catalog.models import Product

            try:
                product = Product.objects.get(id=top_product_data["object_id"])
                top_product = {
                    "id": product.id,
                    "name": product.name,
                    "count": top_product_data["total_count"],
                    "thumbnail": product.images.first().thumbnail_small
                    if product.images.exists()
                    else None,
                }
            except Product.DoesNotExist:
                pass

    # Most active sharer
    most_active_sharer = None
    top_sharer_data = (
        SocialShare.objects.filter(user__isnull=False, shared_at__gte=start_date)
        .values("user", "user__email", "user__first_name", "user__last_name")
        .annotate(share_count=Count("id"))
        .order_by("-share_count")
        .first()
    )

    if top_sharer_data:
        full_name = (
            f"{top_sharer_data['user__first_name']} {top_sharer_data['user__last_name']}".strip()
        )
        most_active_sharer = {
            "id": top_sharer_data["user"],
            "name": full_name or top_sharer_data["user__email"],
            "count": top_sharer_data["share_count"],
        }

    # Shares over time (last 30 days) — single aggregated query
    daily_shares = (
        SocialShare.objects.filter(shared_at__gte=start_date, shared_at__lte=end_date)
        .annotate(date=TruncDate("shared_at"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    daily_counts = {entry["date"]: entry["count"] for entry in daily_shares}
    shares_trend = []
    for i in range(30):
        date = (start_date + timedelta(days=i)).date()
        shares_trend.append({"date": date.strftime("%Y-%m-%d"), "count": daily_counts.get(date, 0)})

    # Shares by platform
    platform_distribution = []
    platforms = SocialShare.PLATFORM_CHOICES
    for platform_code, platform_name in platforms:
        count = (
            ShareCount.objects.filter(platform=platform_code).aggregate(total=Sum("count"))["total"]
            or 0
        )

        if count > 0:
            # Platform colors
            colors = {
                "facebook": "#1877f2",
                "twitter": "#1da1f2",
                "linkedin": "#0a66c2",
                "pinterest": "#e60023",
                "whatsapp": "#25d366",
                "telegram": "#0088cc",
                "email": "#6c757d",
            }

            platform_distribution.append(
                {
                    "platform": platform_code,
                    "name": str(platform_name),
                    "count": count,
                    "color": colors.get(platform_code, "#666"),
                }
            )

    # Top 10 sharers (in period)
    top_sharers = []
    top_sharer_list = (
        SocialShare.objects.filter(user__isnull=False, shared_at__gte=start_date)
        .values("user", "user__email", "user__first_name", "user__last_name")
        .annotate(share_count=Count("id"))
        .order_by("-share_count")[:10]
    )

    for data in top_sharer_list:
        full_name = f"{data['user__first_name']} {data['user__last_name']}".strip()
        top_sharers.append(
            {
                "id": data["user"],
                "name": full_name or data["user__email"],
                "count": data["share_count"],
            }
        )

    # Top 5 platforms by share count
    top_platforms = []
    platform_counts = (
        ShareCount.objects.values("platform")
        .annotate(total_count=Sum("count"))
        .order_by("-total_count")[:5]
    )

    for platform_data in platform_counts:
        platform_name = dict(SocialShare.PLATFORM_CHOICES).get(
            platform_data["platform"], platform_data["platform"]
        )
        top_platforms.append(
            {
                "platform": platform_data["platform"],
                "name": platform_name,
                "count": platform_data["total_count"],
            }
        )

    # Recent shares (last 10)
    recent_shares = SocialShare.objects.select_related("user", "content_type").order_by(
        "-shared_at"
    )[:10]

    # Top 5 most shared content
    top_shared_content = ShareCount.objects.select_related("content_type").order_by("-count")[:5]

    # Get settings
    settings = SocialSharingSettings.get_settings()

    # Handle settings form submission
    if request.method == "POST":
        # Update settings
        settings.enable_on_products = request.POST.get("enable_on_products") == "on"
        settings.enable_on_categories = request.POST.get("enable_on_categories") == "on"
        settings.enable_on_blog_posts = request.POST.get("enable_on_blog_posts") == "on"
        settings.enable_on_pages = request.POST.get("enable_on_pages") == "on"
        settings.placement_position = request.POST.get("placement_position", "below_content")
        settings.show_counts = request.POST.get("show_counts") == "on"
        settings.track_shares = request.POST.get("track_shares") == "on"
        settings.updated_by = request.user
        settings.save()

        messages.success(request, _("Social sharing settings updated successfully."))
        return redirect("social_sharing:dashboard")

    context = {
        # KPIs
        "total_shares": total_shares,
        "shares_today": shares_today,
        "shares_this_month": shares_this_month,
        "top_platform": top_platform,
        "top_product": top_product,
        "most_active_sharer": most_active_sharer,
        # Charts data (raw Python — rendered via json_script in template)
        "shares_trend_json": shares_trend,
        "platform_distribution_json": platform_distribution,
        # Lists
        "top_sharers": top_sharers,
        "top_platforms": top_platforms,
        "recent_shares": recent_shares,
        "top_shared_content": top_shared_content,
        # Settings
        "settings": settings,
        "position_choices": SocialSharingSettings.POSITION_CHOICES,
        # Date range
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "admin/social_sharing/dashboard.html", context)


@staff_member_required
def filter_shares(request):
    """
    AJAX endpoint for filtering social shares.

    Supports filtering by:
    - search: User email, URL
    - platform: facebook, twitter, linkedin, etc.
    - content_type: ContentType ID
    - device: desktop, mobile, tablet
    - date_from: Start date
    - date_to: End date
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    platform = request.GET.get("platform", "").strip()
    content_type_id = request.GET.get("content_type", "").strip()
    device = request.GET.get("device", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    # Build query
    shares = SocialShare.objects.select_related("user", "content_type").order_by("-shared_at")

    # Apply filters
    if search:
        shares = shares.filter(
            Q(user__email__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(shared_url__icontains=search)
            | Q(ip_address__icontains=search)
        )

    if platform:
        shares = shares.filter(platform=platform)

    if content_type_id:
        try:
            shares = shares.filter(content_type_id=int(content_type_id))
        except (ValueError, TypeError):
            pass

    if device:
        shares = shares.filter(device_type=device)

    if date_from:
        shares = shares.filter(shared_at__date__gte=date_from)

    if date_to:
        shares = shares.filter(shared_at__date__lte=date_to)

    # Render results as HTML
    html = render_to_string(
        "admin/social_sharing/partials/share_cards.html",
        {
            "shares": shares,
        },
    )

    return JsonResponse({"html": html, "count": shares.count()})


@staff_member_required
def filter_sharecounts(request):
    """
    AJAX endpoint for filtering share counts.

    Supports filtering by:
    - search: Object ID
    - platform: facebook, twitter, linkedin, etc.
    - content_type: ContentType ID
    - min_count: Minimum share count threshold
    - sort: Sort order field
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    platform = request.GET.get("platform", "").strip()
    content_type_id = request.GET.get("content_type", "").strip()
    min_count = request.GET.get("min_count", "").strip()
    sort = request.GET.get("sort", "-count").strip()

    # Build query
    sharecounts = ShareCount.objects.select_related("content_type")

    # Apply filters
    if search:
        try:
            sharecounts = sharecounts.filter(object_id=int(search))
        except (ValueError, TypeError):
            pass

    if platform:
        sharecounts = sharecounts.filter(platform=platform)

    if content_type_id:
        try:
            sharecounts = sharecounts.filter(content_type_id=int(content_type_id))
        except (ValueError, TypeError):
            pass

    if min_count:
        try:
            sharecounts = sharecounts.filter(count__gte=int(min_count))
        except (ValueError, TypeError):
            pass

    # Apply sorting
    valid_sort_fields = ["-count", "count", "-last_updated", "last_updated"]
    if sort in valid_sort_fields:
        sharecounts = sharecounts.order_by(sort)
    else:
        sharecounts = sharecounts.order_by("-count")

    # Render results as HTML
    html = render_to_string(
        "admin/social_sharing/partials/sharecount_cards.html",
        {
            "sharecounts": sharecounts,
        },
    )

    return JsonResponse({"html": html, "count": sharecounts.count()})
