"""
Affiliate App Views
Provides views for affiliate portal, merchant dashboard, and tracking system
"""

import logging
from datetime import timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, F, Q, Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .decorators import rate_limit, track_affiliate_click
from .models import (
    Affiliate,
    AffiliateProgramMembership,
    AffiliateSettings,
    Click,
    Commission,
    Link,
    Payout,
    Program,
)
from .serializers import (
    AffiliateDashboardSerializer,
    AffiliateDetailSerializer,
    AffiliateListSerializer,
    AffiliateRegistrationSerializer,
    CommissionDetailSerializer,
    CommissionListSerializer,
    LinkCreateSerializer,
    LinkDetailSerializer,
    LinkListSerializer,
    PayoutDetailSerializer,
    PayoutListSerializer,
    PayoutRequestSerializer,
    ProgramApplicationSerializer,
    ProgramDetailSerializer,
    ProgramListSerializer,
)

logger = logging.getLogger(__name__)


# ============================================
# Mixins and Permissions
# ============================================


class AffiliateBrandingMixin:
    """Mixin to provide storefront branding context to affiliate views"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get brand CSS URL from ThemeBranding if available
        try:
            from design.theme_models import ThemeBranding

            branding = ThemeBranding.objects.first()
            if branding:
                context["brand_css_url"] = branding.get_css_url()
        except Exception:
            pass

        return context


class AffiliateRequiredMixin(UserPassesTestMixin):
    """Mixin to require user to have affiliate profile"""

    def test_func(self):
        return hasattr(self.request.user, "affiliate_profile")

    def handle_no_permission(self):
        messages.error(self.request, _("You need an affiliate account to access this page."))
        return redirect("affiliate:portal")


class MerchantRequiredMixin(UserPassesTestMixin):
    """Mixin to require user to be a merchant (have programs)"""

    def test_func(self):
        # Merchant dashboard is staff-only; previously merchants with programs
        # could access. Tighten to staff to match expected access control.
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, _("You need merchant access to view this page."))
        return redirect("affiliate:portal")


class IsAffiliateOrReadOnly(permissions.BasePermission):
    """API permission: owner can edit, others can read"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class IsMerchantOrReadOnly(permissions.BasePermission):
    """API permission: merchant can edit their programs"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.merchant == request.user


# ============================================
# Public Affiliate Portal Views
# ============================================


class AffiliatePortalView(AffiliateBrandingMixin, TemplateView):
    """Landing page for affiliate program"""

    template_name = "affiliate/portal.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, "affiliate_profile"):
            return redirect("affiliate:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_programs"] = Program.objects.filter(status="active").count()
        context["total_affiliates"] = Affiliate.objects.filter(status="active").count()

        # Load affiliate portal settings
        settings = AffiliateSettings.get_settings()
        context["settings"] = settings

        # Pass individual settings for easier template access
        context["hero_title"] = settings.get_translated_field("hero_title")
        context["hero_subtitle"] = settings.get_translated_field("hero_subtitle")
        context["features_title"] = settings.get_translated_field("features_title")
        context["features"] = settings.features
        context["how_it_works_title"] = settings.get_translated_field("how_it_works_title")
        context["steps"] = settings.steps
        context["cta_title"] = settings.get_translated_field("cta_title")
        context["cta_description"] = settings.get_translated_field("cta_description")

        # Determine registration eligibility
        if self.request.user.is_authenticated:
            if hasattr(self.request.user, "affiliate_profile"):
                context["is_affiliate"] = True
                context["affiliate"] = self.request.user.affiliate_profile
            else:
                context["is_affiliate"] = False
                context["can_register"] = True
        else:
            # Guest user - can register if allow_guest_registration is enabled
            context["is_affiliate"] = False
            context["can_register"] = settings.allow_guest_registration

        return context


# ============================================
# Affiliate Dashboard Views
# ============================================


class AffiliateDashboardView(
    AffiliateBrandingMixin, LoginRequiredMixin, AffiliateRequiredMixin, TemplateView
):
    """Main dashboard for affiliates"""

    template_name = "affiliate/affiliate/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        affiliate = self.request.user.affiliate_profile

        # Overview statistics
        thirty_days_ago = timezone.now() - timedelta(days=30)
        context["total_clicks"] = Click.objects.filter(link__affiliate=affiliate).count()
        context["recent_clicks"] = Click.objects.filter(
            link__affiliate=affiliate, clicked_at__gte=thirty_days_ago
        ).count()

        # Get complete balance summary
        balance_summary = affiliate.get_balance_summary()
        context["total_earned"] = balance_summary["total_earned"]
        context["pending_approval"] = balance_summary["pending_approval"]
        context["outstanding_balance"] = balance_summary["outstanding_balance"]
        context["total_paid"] = balance_summary["total_paid"]
        context["total_payouts"] = balance_summary["total_payouts"]
        context["pending_payouts"] = balance_summary["pending_payouts"]

        context["active_links"] = affiliate.links.filter(is_active=True).count()
        context["active_programs"] = affiliate.programs.filter(
            affiliateprogrammembership__status="approved"
        ).count()

        # Recent activity
        context["recent_commissions"] = affiliate.commissions.order_by("-created_at")[:5]
        context["recent_clicks_list"] = (
            Click.objects.filter(link__affiliate=affiliate)
            .select_related("link", "link__program")
            .order_by("-clicked_at")[:10]
        )

        # Top performing links
        context["top_links"] = affiliate.links.annotate(clicks_count=Count("clicks")).order_by(
            "-clicks_count"
        )[:5]

        # Recent payouts
        context["recent_payouts"] = affiliate.payouts.order_by("-created_at")[:3]

        # Chart data: clicks and commissions by day for last 30 days
        import datetime as dt
        import json
        from collections import OrderedDict

        from django.db.models.functions import TruncDate

        clicks_by_day = (
            Click.objects.filter(link__affiliate=affiliate, clicked_at__gte=thirty_days_ago)
            .annotate(date=TruncDate("clicked_at"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        commissions_by_day = (
            Commission.objects.filter(
                affiliate=affiliate,
                created_at__gte=thirty_days_ago,
                status__in=["approved", "paid"],
            )
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(revenue=Sum("amount"))
            .order_by("date")
        )

        # Build zero-filled date series
        chart_data = OrderedDict()
        current = thirty_days_ago.date()
        today = timezone.now().date()
        while current <= today:
            chart_data[current.isoformat()] = {"clicks": 0, "revenue": 0.0}
            current += dt.timedelta(days=1)

        for item in clicks_by_day:
            key = item["date"].isoformat()
            if key in chart_data:
                chart_data[key]["clicks"] = item["count"]

        for item in commissions_by_day:
            key = item["date"].isoformat()
            if key in chart_data:
                chart_data[key]["revenue"] = float(item["revenue"])

        context["chart_labels"] = json.dumps(list(chart_data.keys()))
        context["chart_clicks"] = json.dumps([v["clicks"] for v in chart_data.values()])
        context["chart_revenue"] = json.dumps([v["revenue"] for v in chart_data.values()])
        context["has_chart_data"] = any(
            v["clicks"] > 0 or v["revenue"] > 0 for v in chart_data.values()
        )

        return context


class AffiliateLinksView(
    AffiliateBrandingMixin, LoginRequiredMixin, AffiliateRequiredMixin, ListView
):
    """List of affiliate tracking links"""

    template_name = "affiliate/affiliate/links.html"
    context_object_name = "links"
    paginate_by = 20

    def get_queryset(self):
        affiliate = self.request.user.affiliate_profile
        return (
            Link.objects.filter(affiliate=affiliate)
            .select_related("program")
            .annotate(clicks_count=Count("clicks"))
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        affiliate = self.request.user.affiliate_profile
        context["enrolled_programs"] = Program.objects.filter(
            affiliateprogrammembership__affiliate=affiliate,
            affiliateprogrammembership__status="approved",
            status="active",
        )
        return context


class AffiliateCommissionsView(
    AffiliateBrandingMixin, LoginRequiredMixin, AffiliateRequiredMixin, ListView
):
    """List of affiliate commissions"""

    template_name = "affiliate/affiliate/commissions.html"
    context_object_name = "commissions"
    paginate_by = 20

    def get_queryset(self):
        affiliate = self.request.user.affiliate_profile
        return (
            Commission.objects.filter(affiliate=affiliate)
            .select_related("program", "order")
            .order_by("-created_at")
        )


class AffiliatePayoutsView(
    AffiliateBrandingMixin, LoginRequiredMixin, AffiliateRequiredMixin, ListView
):
    """List of affiliate payouts"""

    template_name = "affiliate/affiliate/payouts.html"
    context_object_name = "payouts"
    paginate_by = 20

    def get_queryset(self):
        affiliate = self.request.user.affiliate_profile
        return Payout.objects.filter(affiliate=affiliate).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        affiliate = self.request.user.affiliate_profile
        context["affiliate_id"] = affiliate.id

        # Get complete balance summary
        balance_summary = affiliate.get_balance_summary()
        context["available_balance"] = balance_summary["outstanding_balance"]
        context["total_paid"] = balance_summary["total_paid"]
        context["pending_approval"] = balance_summary["pending_approval"]
        context["pending_payouts"] = balance_summary["pending_payouts"]

        # Get minimum payout threshold
        programs = affiliate.programs.filter(affiliateprogrammembership__status="approved")
        if programs.exists():
            context["minimum_payout"] = min([p.minimum_payout for p in programs])
        else:
            context["minimum_payout"] = 0

        # Payout statistics
        context["total_payouts_count"] = affiliate.payouts.filter(status="completed").count()
        context["pending_payouts_count"] = affiliate.payouts.filter(
            status__in=["pending", "processing"]
        ).count()

        return context


class AffiliateProgramsView(
    AffiliateBrandingMixin, LoginRequiredMixin, AffiliateRequiredMixin, ListView
):
    """List of available affiliate programs"""

    template_name = "affiliate/affiliate/programs.html"
    context_object_name = "programs"
    paginate_by = 20

    def get_queryset(self):
        return Program.objects.filter(status="active").select_related("merchant")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        affiliate = self.request.user.affiliate_profile

        # Get programs affiliate is already in
        context["my_programs"] = affiliate.programs.filter(
            affiliateprogrammembership__status="approved"
        ).values_list("id", flat=True)

        # Get pending applications
        context["pending_programs"] = affiliate.programs.filter(
            affiliateprogrammembership__status="pending"
        ).values_list("id", flat=True)

        return context


# ============================================
# Merchant Dashboard Views
# ============================================


class MerchantDashboardView(LoginRequiredMixin, MerchantRequiredMixin, TemplateView):
    """Main dashboard for merchants"""

    template_name = "affiliate/merchant/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        programs = Program.objects.filter(merchant=self.request.user)

        # Overview statistics
        context["total_programs"] = programs.count()
        context["active_programs"] = programs.filter(status="active").count()

        context["total_affiliates"] = (
            Affiliate.objects.filter(
                programs__in=programs, affiliateprogrammembership__status="approved"
            )
            .distinct()
            .count()
        )

        context["pending_applications"] = AffiliateProgramMembership.objects.filter(
            program__in=programs, status="pending"
        ).count()

        context["total_clicks"] = Click.objects.filter(link__program__in=programs).count()

        context["total_commissions"] = (
            Commission.objects.filter(program__in=programs).aggregate(Sum("amount"))["amount__sum"]
            or 0
        )

        context["pending_commissions_amount"] = (
            Commission.objects.filter(program__in=programs, status="pending").aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )

        context["pending_commissions_count"] = Commission.objects.filter(
            program__in=programs, status="pending"
        ).count()

        # Revenue chart data (last 30 days)
        from django.db.models.functions import TruncDate

        thirty_days_ago = timezone.now() - timedelta(days=30)

        revenue_by_day = (
            Commission.objects.filter(
                program__in=programs,
                created_at__gte=thirty_days_ago,
                status__in=["approved", "paid"],
            )
            .annotate(date=TruncDate("created_at"))
            .values("date")
            .annotate(revenue=Sum("amount"))
            .order_by("date")
        )

        context["revenue_chart_labels"] = [
            item["date"].strftime("%Y-%m-%d") for item in revenue_by_day
        ]
        context["revenue_chart_data"] = [float(item["revenue"]) for item in revenue_by_day]
        context["has_revenue_data"] = len(revenue_by_day) > 0

        # Total affiliate orders (orders with commissions)
        affiliate_orders = (
            Commission.objects.filter(program__in=programs)
            .select_related("order", "affiliate", "program")
            .order_by("-created_at")[:20]
        )

        context["affiliate_orders"] = affiliate_orders
        context["total_affiliate_orders"] = (
            Commission.objects.filter(program__in=programs).values("order").distinct().count()
        )

        # Recent activity
        context["recent_applications"] = (
            AffiliateProgramMembership.objects.filter(program__in=programs, status="pending")
            .select_related("affiliate", "program")
            .order_by("-applied_at")[:5]
        )

        context["recent_commissions"] = (
            Commission.objects.filter(program__in=programs)
            .select_related("affiliate", "program", "order")
            .order_by("-created_at")[:10]
        )

        # Top 10 performing affiliates

        top_affiliates = (
            Commission.objects.filter(program__in=programs, status__in=["approved", "paid"])
            .values("affiliate")
            .annotate(
                total_revenue=Sum("amount"),
                total_orders=Count("order", distinct=True),
                total_commissions=Count("id"),
            )
            .order_by("-total_revenue")[:10]
        )

        # Enrich with affiliate details and payout information
        top_affiliates_data = []
        for item in top_affiliates:
            affiliate = Affiliate.objects.select_related("user").get(id=item["affiliate"])

            # Get total payouts for this affiliate
            total_payouts = (
                Payout.objects.filter(
                    affiliate=affiliate, status__in=["completed", "processing"]
                ).aggregate(Sum("amount"))["amount__sum"]
                or 0
            )

            top_affiliates_data.append(
                {
                    "affiliate": affiliate,
                    "total_revenue": item["total_revenue"],
                    "total_orders": item["total_orders"],
                    "total_commissions": item["total_commissions"],
                    "total_payouts": total_payouts,
                }
            )

        context["top_affiliates"] = top_affiliates_data

        return context


class ProgramListView(LoginRequiredMixin, MerchantRequiredMixin, ListView):
    """List of merchant programs"""

    template_name = "affiliate/merchant/programs.html"
    context_object_name = "programs"
    paginate_by = 20

    def get_queryset(self):
        return (
            Program.objects.filter(merchant=self.request.user)
            .annotate(
                affiliates_count=Count(
                    "affiliates", filter=Q(affiliateprogrammembership__status="approved")
                ),
                clicks_count=Count("links__clicks"),
            )
            .order_by("-created_at")
        )


class ProgramDetailView(LoginRequiredMixin, MerchantRequiredMixin, DetailView):
    """Detail view for a program"""

    template_name = "affiliate/merchant/program_detail.html"
    context_object_name = "program"

    def get_queryset(self):
        return Program.objects.filter(merchant=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        program = self.object

        # Statistics
        context["affiliates_count"] = program.affiliates.filter(
            affiliateprogrammembership__status="approved"
        ).count()

        context["total_clicks"] = Click.objects.filter(link__program=program).count()

        context["total_commissions"] = (
            program.commissions.aggregate(Sum("amount"))["amount__sum"] or 0
        )

        context["pending_commissions"] = (
            program.commissions.filter(status="pending").aggregate(Sum("amount"))["amount__sum"]
            or 0
        )

        # Recent affiliates
        context["recent_affiliates"] = program.affiliates.filter(
            affiliateprogrammembership__status="approved"
        ).order_by("-affiliateprogrammembership__approved_at")[:10]

        return context


class ProgramAffiliatesView(LoginRequiredMixin, MerchantRequiredMixin, ListView):
    """List of affiliates for a program"""

    template_name = "affiliate/merchant/program_affiliates.html"
    context_object_name = "affiliates"
    paginate_by = 20

    def get_queryset(self):
        self.program = get_object_or_404(
            Program, pk=self.kwargs["program_id"], merchant=self.request.user
        )
        return (
            self.program.affiliates.filter(affiliateprogrammembership__status="approved")
            .select_related("user")
            .annotate(
                total_clicks=Count("links__clicks", filter=Q(links__program=self.program)),
                total_commissions=Sum(
                    "commissions__amount", filter=Q(commissions__program=self.program)
                ),
            )
            .order_by("-total_commissions")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["program"] = self.program
        return context


class ProgramApplicationsView(LoginRequiredMixin, MerchantRequiredMixin, ListView):
    """List of pending affiliate applications"""

    template_name = "affiliate/merchant/applications.html"
    context_object_name = "applications"
    paginate_by = 20

    def get_queryset(self):
        programs = Program.objects.filter(merchant=self.request.user)
        return (
            AffiliateProgramMembership.objects.filter(program__in=programs, status="pending")
            .select_related("affiliate", "program", "affiliate__user")
            .order_by("-applied_at")
        )


# ============================================
# Tracking Views
# ============================================


class TrackingRedirectView(View):
    """Handle tracking link clicks and redirect"""

    @method_decorator(csrf_exempt)
    @method_decorator(rate_limit(max_requests=100, window_seconds=60, key_prefix="affiliate_track"))
    @method_decorator(track_affiliate_click)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, link_code):
        # Find the tracking link
        try:
            link = Link.objects.select_related("affiliate", "program").get(
                link_code=link_code, is_active=True
            )
        except Link.DoesNotExist:
            logger.warning(f"Invalid tracking link accessed: {link_code}")
            return HttpResponse("Invalid tracking link", status=404)

        # Check if program is active
        if link.program.status != "active":
            logger.warning(f"Inactive program accessed: {link.program.name}")
            return HttpResponse("Program is no longer active", status=410)

        # Record the click
        click = Click.objects.create(
            link=link,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            referrer=request.META.get("HTTP_REFERER", "")[:500],
            session_id=request.session.session_key or "",
            cookie_value=self.generate_cookie_value(link),
        )

        # Set affiliate cookie
        response = HttpResponseRedirect(link.destination_url)
        cookie_name = f"aff_{link.program.id}"
        response.set_cookie(
            cookie_name,
            click.cookie_value,
            max_age=link.program.cookie_lifetime_days * 24 * 60 * 60,
            httponly=True,
            samesite="Lax",
        )

        logger.info(f"Tracking click: {link_code} -> {link.destination_url}")
        return response

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
        return ip[:45]  # Max length for IP address field

    def generate_cookie_value(self, link):
        """Generate unique cookie value for tracking"""
        import secrets

        return f"{link.affiliate.affiliate_code}_{secrets.token_urlsafe(16)}"


class ConversionPostbackView(View):
    """Handle conversion postback (called when order is placed)"""

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        """Record conversion from order system"""
        # This will be called by the orders app when an order is completed
        # Implementation depends on how orders app integrates
        order_id = request.POST.get("order_id")
        request.POST.get("order_total")

        # Check for affiliate cookie in the order session
        # This is a placeholder - actual implementation depends on integration
        logger.info(f"Conversion postback received for order {order_id}")

        return JsonResponse({"status": "success"})


# ============================================
# API ViewSets
# ============================================


@extend_schema_view(
    list=extend_schema(tags=["Affiliate"]),
    create=extend_schema(tags=["Affiliate"]),
    retrieve=extend_schema(tags=["Affiliate"]),
    update=extend_schema(tags=["Affiliate"]),
    partial_update=extend_schema(tags=["Affiliate"]),
    destroy=extend_schema(tags=["Affiliate"]),
    statistics=extend_schema(tags=["Affiliate"], summary=_("Get program statistics")),
    apply=extend_schema(tags=["Affiliate"], summary=_("Apply to join a program")),
)
class ProgramViewSet(viewsets.ModelViewSet):
    """API ViewSet for Programs"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsMerchantOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Program.objects.all()
            return Program.objects.filter(Q(merchant=self.request.user) | Q(status="active"))
        return Program.objects.filter(status="active")

    def get_serializer_class(self):
        if self.action == "list":
            return ProgramListSerializer
        return ProgramDetailSerializer

    @action(detail=True, methods=["get"])
    def statistics(self, request, pk=None):
        """Get program statistics"""
        program = self.get_object()
        serializer = ProgramDetailSerializer(program, context={"request": request})
        return Response(serializer.data["statistics"])

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def apply(self, request, pk=None):
        """Apply to join a program as an affiliate"""
        program = self.get_object()

        if not hasattr(request.user, "affiliate_profile"):
            return Response(
                {"detail": _("You must be registered as an affiliate first.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        affiliate = request.user.affiliate_profile
        serializer = ProgramApplicationSerializer(
            data={
                "affiliate_id": affiliate.id,
                "program_id": program.id,
                "notes": request.data.get("notes", ""),
            }
        )
        serializer.is_valid(raise_exception=True)
        membership = serializer.save()

        return Response(
            {
                "detail": _("Application submitted successfully."),
                "status": membership.status,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
    list=extend_schema(tags=["Affiliate"]),
    create=extend_schema(tags=["Affiliate"]),
    retrieve=extend_schema(tags=["Affiliate"]),
    update=extend_schema(tags=["Affiliate"]),
    partial_update=extend_schema(tags=["Affiliate"]),
    destroy=extend_schema(tags=["Affiliate"]),
    dashboard=extend_schema(tags=["Affiliate"], summary=_("Get affiliate dashboard data")),
    register=extend_schema(
        tags=["Affiliate"],
        summary=_("Register as affiliate"),
        description=_(
            "Register as an affiliate. Supports both authenticated users and guest registration "
            "(if allow_guest_registration is enabled). Creates affiliate profile, saves custom form "
            "response if configured, and returns success with affiliate code and redirect URL."
        ),
        request=AffiliateRegistrationSerializer,
        responses={
            201: OpenApiResponse(description=_("Affiliate registered successfully")),
            400: OpenApiResponse(description=_("Validation error or duplicate affiliate account")),
            401: OpenApiResponse(description=_("Login required (guest registration disabled)")),
        },
    ),
)
class AffiliateViewSet(viewsets.ModelViewSet):
    """API ViewSet for Affiliates"""

    permission_classes = [permissions.IsAuthenticated, IsAffiliateOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Affiliate.objects.all()
        if hasattr(self.request.user, "affiliate_profile"):
            return Affiliate.objects.filter(user=self.request.user)
        return Affiliate.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return AffiliateRegistrationSerializer
        if self.action == "list":
            return AffiliateListSerializer
        return AffiliateDetailSerializer

    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):
        """Get affiliate dashboard data"""
        affiliate = self.get_object()
        serializer = AffiliateDashboardSerializer(
            {}, context={"affiliate": affiliate, "request": request}
        )
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        permission_classes=[permissions.AllowAny],
    )
    def register(self, request):
        """
        Register as affiliate - supports both existing users and new registration.

        Flow:
        1. If user not authenticated AND allow_guest_registration is enabled:
           - Create new user account from form data (email, password, first_name, last_name)
           - Auto-login the new user
        2. Create Affiliate record linked to user
        3. Save form response to form_builder.FormResponse if using custom form
        4. Return success with redirect URL
        """
        from django.contrib.auth import get_user_model, login

        User = get_user_model()

        settings = AffiliateSettings.get_settings()
        data = request.data.copy()

        # Determine the user (existing or new)
        user = None
        if request.user.is_authenticated:
            user = request.user
        else:
            # Guest registration flow
            if not settings.allow_guest_registration:
                return Response(
                    {"error": _("You must be logged in to register as an affiliate.")},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Validate required fields for new user creation
            email = data.get("email", "").strip()
            password = data.get("password", "")
            first_name = data.get("first_name", "").strip()
            last_name = data.get("last_name", "").strip()

            if not email:
                return Response(
                    {"error": _("Email is required.")}, status=status.HTTP_400_BAD_REQUEST
                )
            if not password:
                return Response(
                    {"error": _("Password is required.")}, status=status.HTTP_400_BAD_REQUEST
                )

            # Check if email already exists
            if User.objects.filter(email__iexact=email).exists():
                return Response(
                    {
                        "error": _(
                            "An account with this email already exists. Please log in instead."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                # Create new user account
                user = User.objects.create_user(
                    username=email,  # Use email as username
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                )
                # Auto-login the new user
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                logger.info(f"Created new user account for affiliate registration: {email}")
            except Exception as e:
                logger.error(f"Failed to create user account: {e}")
                return Response(
                    {"error": _("Failed to create user account. Please try again.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        # Check if user already has an affiliate profile
        if hasattr(user, "affiliate_profile"):
            return Response(
                {"error": _("You already have an affiliate account.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate terms acceptance
        terms_accepted = data.get("terms_accepted", False)
        if isinstance(terms_accepted, str):
            terms_accepted = terms_accepted.lower() in ("true", "1", "on", "yes")
        if not terms_accepted:
            return Response(
                {"error": _("You must accept the terms and conditions to register.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Prepare affiliate data
        data["user_id"] = user.id

        # Use the registration serializer
        serializer = AffiliateRegistrationSerializer(data=data)
        if serializer.is_valid():
            affiliate = serializer.save()

            # Save form response if using custom form
            if settings.registration_form:
                try:
                    from form_builder.models import FormResponse

                    FormResponse.objects.create(
                        form=settings.registration_form,
                        data=dict(data),
                        user=user,
                        status="completed",
                    )
                except Exception as e:
                    logger.warning(f"Failed to save form response: {e}")

            logger.info(
                f"New affiliate registered: {affiliate.affiliate_code} (user: {user.email})"
            )

            return Response(
                {
                    "success": True,
                    "affiliate_id": affiliate.id,
                    "affiliate_code": affiliate.affiliate_code,
                    "status": affiliate.status,
                    "message": settings.welcome_message
                    or _("Thank you for registering! Your application is being reviewed."),
                    "redirect_url": "/affiliate/dashboard/",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(tags=["Affiliate"]),
    create=extend_schema(tags=["Affiliate"]),
    retrieve=extend_schema(tags=["Affiliate"]),
    update=extend_schema(tags=["Affiliate"]),
    partial_update=extend_schema(tags=["Affiliate"]),
    destroy=extend_schema(tags=["Affiliate"]),
)
class LinkViewSet(viewsets.ModelViewSet):
    """API ViewSet for Tracking Links"""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Link.objects.all()
        if hasattr(self.request.user, "affiliate_profile"):
            return Link.objects.filter(affiliate=self.request.user.affiliate_profile)
        return Link.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return LinkCreateSerializer
        if self.action == "list":
            return LinkListSerializer
        return LinkDetailSerializer

    def perform_create(self, serializer):
        """Auto-assign affiliate from authenticated user and validate membership."""
        if not hasattr(self.request.user, "affiliate_profile"):
            raise PermissionDenied(_("You must be an affiliate to create links."))

        affiliate = self.request.user.affiliate_profile
        program = serializer.validated_data["program"]

        if not AffiliateProgramMembership.objects.filter(
            affiliate=affiliate, program=program, status="approved"
        ).exists():
            from rest_framework.exceptions import ValidationError

            raise ValidationError({"program": _("You are not approved for this program.")})

        serializer.save(affiliate=affiliate)


@extend_schema_view(
    list=extend_schema(tags=["Affiliate"]),
    retrieve=extend_schema(tags=["Affiliate"]),
)
class CommissionViewSet(viewsets.ReadOnlyModelViewSet):
    """API ViewSet for Commissions (read-only for affiliates)"""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Commission.objects.all()
        if hasattr(self.request.user, "affiliate_profile"):
            return Commission.objects.filter(affiliate=self.request.user.affiliate_profile)
        # Merchant view
        programs = Program.objects.filter(merchant=self.request.user)
        return Commission.objects.filter(program__in=programs)

    def get_serializer_class(self):
        if self.action == "list":
            return CommissionListSerializer
        return CommissionDetailSerializer


@extend_schema_view(
    list=extend_schema(tags=["Affiliate"]),
    create=extend_schema(tags=["Affiliate"]),
    retrieve=extend_schema(tags=["Affiliate"]),
    update=extend_schema(tags=["Affiliate"]),
    partial_update=extend_schema(tags=["Affiliate"]),
    destroy=extend_schema(tags=["Affiliate"]),
)
class PayoutViewSet(viewsets.ModelViewSet):
    """API ViewSet for Payouts"""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payout.objects.all()
        if hasattr(self.request.user, "affiliate_profile"):
            return Payout.objects.filter(affiliate=self.request.user.affiliate_profile)
        return Payout.objects.none()

    def get_serializer_class(self):
        if self.action == "create":
            return PayoutRequestSerializer
        if self.action == "list":
            return PayoutListSerializer
        return PayoutDetailSerializer


# ============================================
# Admin AJAX Endpoints
# ============================================


@staff_member_required
def filter_programs(request):
    """
    AJAX endpoint for filtering affiliate programs.
    Returns filtered program list as HTML with count.
    """
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    status_filter = request.GET.get("status", "").strip()
    commission_type = request.GET.get("commission_type", "").strip()
    order = request.GET.get("order", "-created_at").strip()

    # Build query with annotations for card display
    programs = Program.objects.select_related("merchant").annotate(
        affiliates_count=Count(
            "affiliates", filter=Q(affiliateprogrammembership__status="approved")
        ),
        active_affiliates=Count(
            "affiliates", filter=Q(affiliateprogrammembership__status="approved")
        ),
        total_earned=Sum("commissions__amount"),
    )

    # Apply search filter
    if search:
        programs = programs.filter(
            Q(name__icontains=search)
            | Q(slug__icontains=search)
            | Q(description__icontains=search)
            | Q(merchant__username__icontains=search)
        )

    # Apply status filter
    if status_filter:
        programs = programs.filter(status=status_filter)

    # Apply commission type filter
    if commission_type:
        programs = programs.filter(commission_type=commission_type)

    # Apply ordering
    programs = programs.order_by(order) if order else programs.order_by("-created_at")

    # Render results as HTML
    html = render_to_string(
        "admin/affiliate/partials/program_cards.html",
        {
            "programs": programs,
        },
    )

    return JsonResponse({"html": html, "count": programs.count()})


@staff_member_required
def toggle_program_status(request, program_id):
    """
    AJAX endpoint for activating or pausing a program.
    Determines action from the URL path.
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        program = Program.objects.get(id=program_id)

        # Determine action from URL path
        path = request.path
        if "activate" in path:
            if program.status in ["paused", "archived"]:
                program.status = "active"
                program.save()
                action_msg = _("Program activated successfully.")
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Program cannot be activated from its current status."),
                    },
                    status=400,
                )
        elif "pause" in path:
            if program.status == "active":
                program.status = "paused"
                program.save()
                action_msg = _("Program paused successfully.")
            else:
                return JsonResponse(
                    {"success": False, "error": _("Only active programs can be paused.")},
                    status=400,
                )
        else:
            return JsonResponse({"success": False, "error": _("Invalid action.")}, status=400)

        return JsonResponse({"success": True, "status": program.status, "message": action_msg})
    except Program.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Program not found.")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# ============================================
# Admin Wizard Views
# ============================================


@staff_member_required
def program_wizard(request):
    """
    Multi-step wizard for creating affiliate programs.
    Handles both GET (display form) and POST (save program).
    """
    from django.utils.text import slugify

    if request.method == "POST":
        # Get form data
        name = request.POST.get("name", "").strip()
        slug = request.POST.get("slug", "").strip()
        description = request.POST.get("description", "").strip()
        status_value = request.POST.get("status", "active").strip()
        commission_type = request.POST.get("commission_type", "percentage").strip()
        commission_value = request.POST.get("commission_value", "").strip()
        cookie_lifetime_days = request.POST.get("cookie_lifetime_days", "30").strip()
        auto_approve = request.POST.get("auto_approve_affiliates") == "on"
        minimum_payout = request.POST.get("minimum_payout", "50.00").strip()

        # Validation
        errors = {}

        if not name:
            errors["name"] = _("Program name is required.")
        elif len(name) > 200:
            errors["name"] = _("Program name must be 200 characters or fewer.")

        # Auto-generate slug if not provided
        if not slug:
            slug = slugify(name)

        # Check slug uniqueness
        if slug:
            existing = Program.objects.filter(slug=slug)
            if existing.exists():
                # Add a number suffix to make it unique
                base_slug = slug
                counter = 1
                while Program.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

        if not commission_value:
            errors["commission_value"] = _("Commission value is required.")
        else:
            try:
                commission_val = float(commission_value)
                if commission_val < 0:
                    errors["commission_value"] = _("Commission value must be positive.")
                if commission_type == "percentage" and commission_val > 100:
                    errors["commission_value"] = _("Percentage cannot exceed 100%.")
            except ValueError:
                errors["commission_value"] = _("Invalid commission value.")

        try:
            cookie_days = int(cookie_lifetime_days)
            if cookie_days < 1 or cookie_days > 365:
                errors["cookie_lifetime_days"] = _(
                    "Cookie lifetime must be between 1 and 365 days."
                )
        except ValueError:
            errors["cookie_lifetime_days"] = _("Invalid cookie lifetime.")

        try:
            min_payout = float(minimum_payout)
            if min_payout < 0:
                errors["minimum_payout"] = _("Minimum payout must be positive.")
        except ValueError:
            errors["minimum_payout"] = _("Invalid minimum payout.")

        if errors:
            return JsonResponse({"success": False, "errors": errors}, status=400)

        # Create the program
        try:
            program = Program.objects.create(
                name=name,
                slug=slug,
                merchant=request.user,
                description=description,
                status=status_value,
                commission_type=commission_type,
                commission_value=float(commission_value),
                cookie_lifetime_days=int(cookie_lifetime_days),
                auto_approve_affiliates=auto_approve,
                minimum_payout=float(minimum_payout),
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": _("Affiliate program created successfully."),
                    "redirect_url": reverse("admin:affiliate_program_change", args=[program.pk]),
                }
            )

        except Exception as e:
            return JsonResponse({"success": False, "errors": {"__all__": str(e)}}, status=500)

    # GET request - display wizard form
    context = {
        "title": _("Create Affiliate Program"),
        "commission_types": [
            ("percentage", _("Percentage"), _("Pay a percentage of each sale"), "fa-percentage"),
            ("fixed", _("Fixed Amount"), _("Pay a fixed amount per sale"), "fa-dollar-sign"),
        ],
        "status_choices": [
            ("active", _("Active"), _("Program is live and accepting affiliates")),
            ("paused", _("Paused"), _("Program is temporarily paused")),
        ],
    }

    return render(request, "admin/affiliate/program/wizard.html", context)


@staff_member_required
def filter_affiliates(request):
    """
    AJAX endpoint for filtering affiliates.
    Returns filtered affiliate list as HTML with count.
    """
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    status_filter = request.GET.get("status", "").strip()
    payment_method = request.GET.get("payment_method", "").strip()
    order = request.GET.get("order", "-created_at").strip()

    # Build query with annotations for card display
    # Use different names to avoid conflict with model @property methods
    affiliates = Affiliate.objects.select_related("user").annotate(
        programs_count=Count("programs", filter=Q(affiliateprogrammembership__status="approved")),
        links_count=Count("links"),
        # Annotations for sorting (prefixed to avoid property conflict)
        sort_total_earned=Sum(
            "commissions__amount", filter=Q(commissions__status__in=["approved", "paid"])
        ),
        sort_outstanding_balance=Sum(
            "commissions__amount", filter=Q(commissions__status="approved")
        ),
    )

    # Apply search filter
    if search:
        affiliates = affiliates.filter(
            Q(affiliate_code__icontains=search)
            | Q(user__username__icontains=search)
            | Q(user__email__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(company_name__icontains=search)
            | Q(payment_email__icontains=search)
        )

    # Apply status filter
    if status_filter:
        affiliates = affiliates.filter(status=status_filter)

    # Apply payment method filter
    if payment_method:
        affiliates = affiliates.filter(payment_method=payment_method)

    # Apply ordering
    affiliates = affiliates.order_by(order) if order else affiliates.order_by("-created_at")

    # Render results as HTML
    html = render_to_string(
        "admin/affiliate/partials/affiliate_cards.html",
        {
            "affiliates": affiliates,
        },
    )

    return JsonResponse({"html": html, "count": affiliates.count()})


@staff_member_required
def toggle_affiliate_status(request, affiliate_id):
    """
    AJAX endpoint for changing affiliate status (approve/suspend/activate).
    Determines action from the URL path.
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        affiliate = Affiliate.objects.get(id=affiliate_id)

        # Determine action from URL path
        path = request.path
        if "approve" in path:
            if affiliate.status == "pending":
                affiliate.status = "active"
                affiliate.save()
                action_msg = _("Affiliate approved successfully.")
            else:
                return JsonResponse(
                    {"success": False, "error": _("Only pending affiliates can be approved.")},
                    status=400,
                )
        elif "suspend" in path:
            if affiliate.status == "active":
                affiliate.status = "suspended"
                affiliate.save()
                action_msg = _("Affiliate suspended successfully.")
            else:
                return JsonResponse(
                    {"success": False, "error": _("Only active affiliates can be suspended.")},
                    status=400,
                )
        elif "activate" in path:
            if affiliate.status in ["suspended", "rejected"]:
                affiliate.status = "active"
                affiliate.save()
                action_msg = _("Affiliate activated successfully.")
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error": _("Affiliate cannot be activated from current status."),
                    },
                    status=400,
                )
        else:
            return JsonResponse({"success": False, "error": _("Invalid action.")}, status=400)

        return JsonResponse({"success": True, "status": affiliate.status, "message": action_msg})
    except Affiliate.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Affiliate not found.")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def filter_memberships(request):
    """
    AJAX endpoint for filtering program memberships.
    Returns filtered membership list as HTML with count.
    """
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    status_filter = request.GET.get("status", "").strip()
    program_filter = request.GET.get("program", "").strip()
    order = request.GET.get("order", "-applied_at").strip()

    # Build query with annotations for card display
    memberships = AffiliateProgramMembership.objects.select_related(
        "affiliate__user", "program"
    ).annotate(
        commissions_count=Count(
            "affiliate__commissions", filter=Q(affiliate__commissions__program=F("program"))
        ),
        total_earned=Sum(
            "affiliate__commissions__amount",
            filter=Q(
                affiliate__commissions__program=F("program"),
                affiliate__commissions__status__in=["approved", "paid"],
            ),
        ),
        links_count=Count("affiliate__links", filter=Q(affiliate__links__program=F("program"))),
    )

    # Apply search filter
    if search:
        memberships = memberships.filter(
            Q(affiliate__affiliate_code__icontains=search)
            | Q(affiliate__user__username__icontains=search)
            | Q(affiliate__user__email__icontains=search)
            | Q(affiliate__user__first_name__icontains=search)
            | Q(affiliate__user__last_name__icontains=search)
            | Q(program__name__icontains=search)
            | Q(notes__icontains=search)
        )

    # Apply status filter
    if status_filter:
        memberships = memberships.filter(status=status_filter)

    # Apply program filter
    if program_filter:
        memberships = memberships.filter(program_id=program_filter)

    # Apply ordering
    memberships = memberships.order_by(order) if order else memberships.order_by("-applied_at")

    # Render results as HTML
    html = render_to_string(
        "admin/affiliate/partials/membership_cards.html",
        {
            "memberships": memberships,
        },
    )

    return JsonResponse({"html": html, "count": memberships.count()})


@staff_member_required
def toggle_membership_status(request, membership_id):
    """
    AJAX endpoint for changing membership status (approve/reject).
    Determines action from the URL path.
    """
    from django.utils import timezone

    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        membership = AffiliateProgramMembership.objects.get(id=membership_id)

        # Determine action from URL path
        path = request.path
        if "approve" in path:
            if membership.status == "pending":
                membership.status = "approved"
                membership.approved_at = timezone.now()
                membership.save()
                action_msg = _("Membership approved successfully.")
            else:
                return JsonResponse(
                    {"success": False, "error": _("Only pending memberships can be approved.")},
                    status=400,
                )
        elif "reject" in path:
            if membership.status == "pending":
                membership.status = "rejected"
                membership.save()
                action_msg = _("Membership rejected successfully.")
            else:
                return JsonResponse(
                    {"success": False, "error": _("Only pending memberships can be rejected.")},
                    status=400,
                )
        else:
            return JsonResponse({"success": False, "error": _("Invalid action.")}, status=400)

        return JsonResponse({"success": True, "status": membership.status, "message": action_msg})
    except AffiliateProgramMembership.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Membership not found.")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def filter_program_members(request, program_id):
    """
    AJAX endpoint for filtering program members in the program detail dashboard.
    Used by the members list in the program change form.
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        program = Program.objects.get(id=program_id)
    except Program.DoesNotExist:
        return JsonResponse({"error": "Program not found"}, status=404)

    # Get filters from query params
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "")

    # Base queryset with annotations
    members = (
        AffiliateProgramMembership.objects.filter(program=program)
        .select_related("affiliate__user")
        .annotate(
            member_commissions=Count(
                "affiliate__commissions", filter=Q(affiliate__commissions__program=program)
            ),
            member_earned=Sum(
                "affiliate__commissions__amount",
                filter=Q(
                    affiliate__commissions__program=program,
                    affiliate__commissions__status__in=["approved", "paid"],
                ),
            ),
            member_clicks=Count(
                "affiliate__links__clicks", filter=Q(affiliate__links__program=program)
            ),
        )
    )

    # Apply search filter
    if search:
        members = members.filter(
            Q(affiliate__affiliate_code__icontains=search)
            | Q(affiliate__user__username__icontains=search)
            | Q(affiliate__user__email__icontains=search)
            | Q(affiliate__user__first_name__icontains=search)
            | Q(affiliate__user__last_name__icontains=search)
        )

    # Apply status filter
    if status:
        members = members.filter(status=status)

    # Order by applied date (newest first)
    members = members.order_by("-applied_at")

    # Render results as HTML
    from django.template.loader import render_to_string

    html = render_to_string(
        "admin/affiliate/program/partials/program_member_cards.html",
        {
            "members": members,
            "program": program,
        },
    )

    return JsonResponse({"html": html, "count": members.count()})


@staff_member_required
def update_program_status(request, program_id, new_status):
    """
    AJAX endpoint for updating program status (activate/pause/archive).
    """
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    # Validate status
    valid_statuses = ["active", "paused", "archived"]
    if new_status not in valid_statuses:
        return JsonResponse({"success": False, "error": _("Invalid status.")}, status=400)

    try:
        program = Program.objects.get(id=program_id)
        program.status = new_status
        program.save()

        status_messages = {
            "active": _("Program activated successfully."),
            "paused": _("Program paused successfully."),
            "archived": _("Program archived successfully."),
        }

        return JsonResponse(
            {"success": True, "status": program.status, "message": status_messages.get(new_status)}
        )
    except Program.DoesNotExist:
        return JsonResponse({"success": False, "error": _("Program not found.")}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@staff_member_required
def filter_payouts(request):
    """
    AJAX endpoint for filtering payouts.
    Returns filtered payout list as HTML with count.
    """
    from django.db.models import Q
    from django.template.loader import render_to_string

    # Ensure this is an AJAX request
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    # Get filter parameters
    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    method = request.GET.get("method", "").strip()
    provider = request.GET.get("provider", "").strip()

    # Build query with select_related and prefetch_related for performance
    payouts = Payout.objects.select_related("affiliate__user", "provider_account").prefetch_related(
        "commissions"
    )

    # Apply search filter
    if search:
        payouts = payouts.filter(
            Q(affiliate__affiliate_code__icontains=search)
            | Q(affiliate__user__username__icontains=search)
            | Q(affiliate__user__email__icontains=search)
            | Q(reference__icontains=search)
        )

    # Apply status filter
    if status:
        payouts = payouts.filter(status=status)

    # Apply method filter
    if method:
        payouts = payouts.filter(method__iexact=method)

    # Apply provider filter
    if provider:
        payouts = payouts.filter(provider_account_id=provider)

    # Order by most recent
    payouts = payouts.order_by("-created_at")

    # Render partial template
    html = render_to_string(
        "admin/affiliate/payout/partials/payout_cards.html",
        {"payouts": payouts, "request": request},
    )

    return JsonResponse({"html": html, "count": payouts.count()})
