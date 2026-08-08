"""
Affiliate App DRF Serializers
Provides REST API serialization for affiliate portal and merchant dashboard
"""

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count, DecimalField, OuterRef, Subquery, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Affiliate, AffiliateProgramMembership, Click, Commission, Link, Payout, Program

User = get_user_model()


def resolve_acting_id(context, requested_id, owner_id, mismatch_error):
    """Return the entity id an API caller is authorised to act on.

    Ownership guard shared by identity-bearing serializers: non-staff callers
    are pinned to their own resource, so a client cannot act on behalf of an
    arbitrary user/affiliate by posting someone else's id.

    - Staff may target any explicitly requested id.
    - Non-staff are restricted to ``owner_id`` (their own resource); an explicit
      id that differs raises ``mismatch_error``.
    - With no authenticated request in context (trusted internal calls that set
      the id server-side), the requested id is used as-is.
    """
    request = context.get("request")
    user = getattr(request, "user", None)
    if user is None or not getattr(user, "is_authenticated", False):
        return requested_id
    if user.is_staff and requested_id:
        return requested_id
    if requested_id and owner_id is not None and requested_id != owner_id:
        raise serializers.ValidationError(mismatch_error)
    return owner_id if owner_id is not None else requested_id


# ============================================
# Program Serializers
# ============================================


class ProgramListSerializer(serializers.ModelSerializer):
    """Serializer for program list view"""

    merchant_name = serializers.CharField(source="merchant.username", read_only=True)
    commission_display = serializers.SerializerMethodField()
    affiliates_count = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            "id",
            "name",
            "slug",
            "merchant",
            "merchant_name",
            "description",
            "commission_type",
            "commission_value",
            "commission_display",
            "cookie_lifetime_days",
            "status",
            "auto_approve_affiliates",
            "minimum_payout",
            "affiliates_count",
            "created_at",
        ]
        read_only_fields = ["slug", "created_at"]

    def get_commission_display(self, obj) -> str:
        """Format commission for display"""
        if obj.commission_type == "percentage":
            return f"{obj.commission_value}%"
        return f"${obj.commission_value}"

    def get_affiliates_count(self, obj) -> int:
        """Count of approved affiliates"""
        return obj.affiliates.filter(affiliateprogrammembership__status="approved").count()


class ProgramDetailSerializer(serializers.ModelSerializer):
    """Serializer for program detail view with statistics"""

    merchant_name = serializers.CharField(source="merchant.username", read_only=True)
    commission_display = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            "id",
            "name",
            "slug",
            "merchant",
            "merchant_name",
            "description",
            "commission_type",
            "commission_value",
            "commission_display",
            "cookie_lifetime_days",
            "status",
            "auto_approve_affiliates",
            "minimum_payout",
            "statistics",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "created_at", "updated_at"]

    def get_commission_display(self, obj) -> str:
        """Format commission for display"""
        if obj.commission_type == "percentage":
            return f"{obj.commission_value}%"
        return f"${obj.commission_value}"

    def get_statistics(self, obj) -> dict:
        """Get program statistics"""
        affiliates_count = obj.affiliates.filter(
            affiliateprogrammembership__status="approved"
        ).count()
        pending_count = obj.affiliates.filter(affiliateprogrammembership__status="pending").count()

        total_clicks = Click.objects.filter(link__program=obj).count()
        total_commissions = obj.commissions.aggregate(Sum("amount"))["amount__sum"] or 0
        pending_commissions = (
            obj.commissions.filter(status="pending").aggregate(Sum("amount"))["amount__sum"] or 0
        )
        paid_commissions = (
            obj.commissions.filter(status="paid").aggregate(Sum("amount"))["amount__sum"] or 0
        )

        return {
            "affiliates": {
                "active": affiliates_count,
                "pending": pending_count,
                "total": affiliates_count + pending_count,
            },
            "clicks": {
                "total": total_clicks,
            },
            "commissions": {
                "total": float(total_commissions),
                "pending": float(pending_commissions),
                "paid": float(paid_commissions),
            },
        }


# ============================================
# Affiliate Serializers
# ============================================


class AffiliateListSerializer(serializers.ModelSerializer):
    """Serializer for affiliate list view"""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField()
    programs_count = serializers.SerializerMethodField()
    total_earned = serializers.SerializerMethodField()

    class Meta:
        model = Affiliate
        fields = [
            "id",
            "user",
            "user_email",
            "user_name",
            "affiliate_code",
            "company_name",
            "website",
            "payment_email",
            "payment_method",
            "status",
            "programs_count",
            "total_earned",
            "created_at",
        ]
        read_only_fields = ["affiliate_code", "created_at"]

    def get_user_name(self, obj) -> str:
        """Get full name or username"""
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username

    def get_programs_count(self, obj) -> int:
        """Count of approved programs"""
        return obj.programs.filter(affiliateprogrammembership__status="approved").count()

    def get_total_earned(self, obj) -> float:
        """Total commissions earned"""
        total = (
            obj.commissions.filter(status__in=["approved", "paid"]).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        return float(total)


class AffiliateDetailSerializer(serializers.ModelSerializer):
    """Serializer for affiliate detail view with statistics"""

    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Affiliate
        fields = [
            "id",
            "user",
            "user_email",
            "user_name",
            "affiliate_code",
            "company_name",
            "website",
            "payment_email",
            "payment_method",
            "status",
            "statistics",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["affiliate_code", "created_at", "updated_at"]

    def get_user_name(self, obj) -> str:
        """Get full name or username"""
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username

    def get_statistics(self, obj) -> dict:
        """Get affiliate statistics"""
        total_links = obj.links.count()
        active_links = obj.links.filter(is_active=True).count()
        total_clicks = Click.objects.filter(link__affiliate=obj).count()

        total_earned = (
            obj.commissions.filter(status__in=["approved", "paid"]).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        pending = (
            obj.commissions.filter(status="pending").aggregate(Sum("amount"))["amount__sum"] or 0
        )
        approved = (
            obj.commissions.filter(status="approved").aggregate(Sum("amount"))["amount__sum"] or 0
        )
        paid = obj.commissions.filter(status="paid").aggregate(Sum("amount"))["amount__sum"] or 0

        total_payouts = (
            obj.payouts.filter(status="completed").aggregate(Sum("amount"))["amount__sum"] or 0
        )

        # Last 30 days stats
        thirty_days_ago = timezone.now() - timedelta(days=30)
        recent_clicks = Click.objects.filter(
            link__affiliate=obj, clicked_at__gte=thirty_days_ago
        ).count()
        recent_commissions = (
            obj.commissions.filter(created_at__gte=thirty_days_ago).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

        return {
            "links": {"total": total_links, "active": active_links},
            "clicks": {"total": total_clicks, "last_30_days": recent_clicks},
            "commissions": {
                "total_earned": float(total_earned),
                "pending": float(pending),
                "approved": float(approved),
                "paid": float(paid),
                "last_30_days": float(recent_commissions),
            },
            "payouts": {"total": float(total_payouts)},
        }


class AffiliateRegistrationSerializer(serializers.Serializer):
    """Serializer for new affiliate registration"""

    user_id = serializers.IntegerField(required=False)
    company_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    payment_email = serializers.EmailField(required=True)
    payment_method = serializers.CharField(max_length=50, default="paypal")

    def validate(self, attrs):
        """Resolve the target user from the caller and validate eligibility.

        The profile owner is derived from the authenticated user; a supplied
        ``user_id`` is honoured only for staff, so a caller cannot create an
        affiliate profile linked to another user.
        """
        request = self.context.get("request")
        user = getattr(request, "user", None)
        owner_id = None
        if user is not None and getattr(user, "is_authenticated", False):
            owner_id = user.id
        resolved_id = resolve_acting_id(
            self.context,
            attrs.get("user_id"),
            owner_id,
            {"user_id": _("You cannot create an affiliate profile for another user.")},
        )
        if not resolved_id:
            raise serializers.ValidationError({"user_id": _("User is required")})

        try:
            target_user = User.objects.get(id=resolved_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": _("User does not exist")})

        if hasattr(target_user, "affiliate_profile"):
            raise serializers.ValidationError(
                {"user_id": _("User already has an affiliate profile")}
            )

        attrs["user"] = target_user
        return attrs

    def create(self, validated_data):
        """Create new affiliate profile"""
        affiliate = Affiliate.objects.create(
            user=validated_data["user"],
            company_name=validated_data.get("company_name", ""),
            website=validated_data.get("website", ""),
            payment_email=validated_data["payment_email"],
            payment_method=validated_data.get("payment_method", "paypal"),
            status="pending",
        )
        return affiliate


# ============================================
# Program Membership Serializers
# ============================================


class AffiliateProgramMembershipSerializer(serializers.ModelSerializer):
    """Serializer for program membership"""

    affiliate_code = serializers.CharField(source="affiliate.affiliate_code", read_only=True)
    program_name = serializers.CharField(source="program.name", read_only=True)

    class Meta:
        model = AffiliateProgramMembership
        fields = [
            "id",
            "affiliate",
            "affiliate_code",
            "program",
            "program_name",
            "status",
            "notes",
            "applied_at",
            "approved_at",
        ]
        read_only_fields = ["applied_at", "approved_at"]


class ProgramApplicationSerializer(serializers.Serializer):
    """Serializer for applying to a program"""

    affiliate_id = serializers.IntegerField(required=True)
    program_id = serializers.IntegerField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        """Validate affiliate and program exist"""
        try:
            affiliate = Affiliate.objects.get(id=data["affiliate_id"])
        except Affiliate.DoesNotExist:
            raise serializers.ValidationError({"affiliate_id": _("Affiliate does not exist")})

        try:
            program = Program.objects.get(id=data["program_id"])
        except Program.DoesNotExist:
            raise serializers.ValidationError({"program_id": _("Program does not exist")})

        # Check if already applied
        if AffiliateProgramMembership.objects.filter(affiliate=affiliate, program=program).exists():
            raise serializers.ValidationError(_("Already applied to this program"))

        data["affiliate"] = affiliate
        data["program"] = program
        return data

    def create(self, validated_data):
        """Create program application"""
        membership = AffiliateProgramMembership.objects.create(
            affiliate=validated_data["affiliate"],
            program=validated_data["program"],
            notes=validated_data.get("notes", ""),
            status="approved" if validated_data["program"].auto_approve_affiliates else "pending",
        )

        if membership.status == "approved":
            membership.approved_at = timezone.now()
            membership.save()

        return membership


# ============================================
# Link Serializers
# ============================================


class LinkListSerializer(serializers.ModelSerializer):
    """Serializer for link list view"""

    affiliate_code = serializers.CharField(source="affiliate.affiliate_code", read_only=True)
    program_name = serializers.CharField(source="program.name", read_only=True)
    clicks_count = serializers.SerializerMethodField()
    tracking_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = [
            "id",
            "affiliate",
            "affiliate_code",
            "program",
            "program_name",
            "link_code",
            "destination_url",
            "label",
            "is_active",
            "clicks_count",
            "tracking_url",
            "created_at",
        ]
        read_only_fields = ["link_code", "created_at"]

    def get_clicks_count(self, obj) -> int:
        """Get click count"""
        return obj.clicks.count()

    def get_tracking_url(self, obj) -> str:
        """Get full tracking URL"""
        return obj.get_tracking_url()


class LinkDetailSerializer(serializers.ModelSerializer):
    """Serializer for link detail view with statistics"""

    affiliate_code = serializers.CharField(source="affiliate.affiliate_code", read_only=True)
    program_name = serializers.CharField(source="program.name", read_only=True)
    tracking_url = serializers.SerializerMethodField()
    statistics = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = [
            "id",
            "affiliate",
            "affiliate_code",
            "program",
            "program_name",
            "link_code",
            "destination_url",
            "label",
            "is_active",
            "tracking_url",
            "statistics",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["link_code", "created_at", "updated_at"]

    def get_tracking_url(self, obj) -> str:
        """Get full tracking URL"""
        return obj.get_tracking_url()

    def get_statistics(self, obj) -> dict:
        """Get link statistics"""
        total_clicks = obj.clicks.count()
        last_7_days = timezone.now() - timedelta(days=7)
        recent_clicks = obj.clicks.filter(clicked_at__gte=last_7_days).count()

        conversions = obj.clicks.filter(commissions__isnull=False).distinct().count()
        conversion_rate = (conversions / total_clicks * 100) if total_clicks > 0 else 0

        total_revenue = (
            obj.clicks.filter(commissions__status__in=["approved", "paid"]).aggregate(
                Sum("commissions__amount")
            )["commissions__amount__sum"]
            or 0
        )

        return {
            "clicks": {"total": total_clicks, "last_7_days": recent_clicks},
            "conversions": {"total": conversions, "rate": round(conversion_rate, 2)},
            "revenue": {"total": float(total_revenue)},
        }


class LinkCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tracking links.

    The affiliate field is read-only and auto-assigned from the
    authenticated user in LinkViewSet.perform_create().
    """

    class Meta:
        model = Link
        fields = ["affiliate", "program", "destination_url", "label", "is_active"]
        read_only_fields = ["affiliate"]


# ============================================
# Click Serializers
# ============================================


class ClickSerializer(serializers.ModelSerializer):
    """Serializer for click tracking data"""

    link_code = serializers.CharField(source="link.link_code", read_only=True)
    affiliate_code = serializers.CharField(source="link.affiliate.affiliate_code", read_only=True)
    has_conversion = serializers.SerializerMethodField()

    class Meta:
        model = Click
        fields = [
            "id",
            "link",
            "link_code",
            "affiliate_code",
            "ip_address",
            "user_agent",
            "referrer",
            "session_id",
            "cookie_value",
            "clicked_at",
            "has_conversion",
        ]
        read_only_fields = ["clicked_at"]

    def get_has_conversion(self, obj) -> bool:
        """Check if click resulted in conversion"""
        return obj.commissions.exists()


# ============================================
# Commission Serializers
# ============================================


class CommissionListSerializer(serializers.ModelSerializer):
    """Serializer for commission list view"""

    affiliate_code = serializers.CharField(source="affiliate.affiliate_code", read_only=True)
    program_name = serializers.CharField(source="program.name", read_only=True)
    order_id = serializers.IntegerField(source="order.id", read_only=True)

    class Meta:
        model = Commission
        fields = [
            "id",
            "affiliate",
            "affiliate_code",
            "program",
            "program_name",
            "order",
            "order_id",
            "click",
            "amount",
            "status",
            "created_at",
            "approved_at",
            "paid_at",
        ]
        read_only_fields = ["created_at", "approved_at", "paid_at"]


class CommissionDetailSerializer(serializers.ModelSerializer):
    """Serializer for commission detail view"""

    affiliate_code = serializers.CharField(source="affiliate.affiliate_code", read_only=True)
    affiliate_name = serializers.SerializerMethodField()
    program_name = serializers.CharField(source="program.name", read_only=True)
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = Commission
        fields = [
            "id",
            "affiliate",
            "affiliate_code",
            "affiliate_name",
            "program",
            "program_name",
            "order",
            "order_details",
            "click",
            "amount",
            "status",
            "notes",
            "created_at",
            "approved_at",
            "paid_at",
        ]
        read_only_fields = ["created_at", "approved_at", "paid_at"]

    def get_affiliate_name(self, obj) -> str:
        """Get affiliate user name"""
        if obj.affiliate.user.first_name and obj.affiliate.user.last_name:
            return f"{obj.affiliate.user.first_name} {obj.affiliate.user.last_name}"
        return obj.affiliate.user.username

    def get_order_details(self, obj) -> dict:
        """Get basic order information"""
        return {
            "id": obj.order.id,
            "total": float(obj.order.total) if hasattr(obj.order, "total") else 0,
            "created_at": obj.order.created_at if hasattr(obj.order, "created_at") else None,
        }


# ============================================
# Payout Serializers
# ============================================


class PayoutListSerializer(serializers.ModelSerializer):
    """Serializer for payout list view"""

    affiliate_code = serializers.CharField(source="affiliate.affiliate_code", read_only=True)
    affiliate_email = serializers.EmailField(source="affiliate.payment_email", read_only=True)

    class Meta:
        model = Payout
        fields = [
            "id",
            "affiliate",
            "affiliate_code",
            "affiliate_email",
            "amount",
            "method",
            "status",
            "reference",
            "created_at",
            "processed_at",
            "completed_at",
        ]
        read_only_fields = ["created_at", "processed_at", "completed_at"]


class PayoutDetailSerializer(serializers.ModelSerializer):
    """Serializer for payout detail view"""

    affiliate_code = serializers.CharField(source="affiliate.affiliate_code", read_only=True)
    affiliate_name = serializers.SerializerMethodField()
    affiliate_email = serializers.EmailField(source="affiliate.payment_email", read_only=True)

    class Meta:
        model = Payout
        fields = [
            "id",
            "affiliate",
            "affiliate_code",
            "affiliate_name",
            "affiliate_email",
            "amount",
            "method",
            "status",
            "reference",
            "notes",
            "created_at",
            "processed_at",
            "completed_at",
        ]
        read_only_fields = ["created_at", "processed_at", "completed_at"]

    def get_affiliate_name(self, obj) -> str:
        """Get affiliate user name"""
        if obj.affiliate.user.first_name and obj.affiliate.user.last_name:
            return f"{obj.affiliate.user.first_name} {obj.affiliate.user.last_name}"
        return obj.affiliate.user.username


class PayoutRequestSerializer(serializers.Serializer):
    """Serializer for requesting a payout"""

    affiliate_id = serializers.IntegerField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    method = serializers.CharField(max_length=50, default="paypal")

    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError(_("Amount must be greater than zero"))
        return value

    def validate(self, data):
        """Resolve the target affiliate from the caller and validate the request.

        The affiliate is derived from the authenticated user's profile; a
        supplied ``affiliate_id`` is honoured only for staff, so a caller cannot
        request a payout for another affiliate. The authoritative balance check
        happens under lock in ``create()`` to prevent over-committing funds.
        """
        request = self.context.get("request")
        user = getattr(request, "user", None)
        owner_id = None
        if user is not None and getattr(user, "is_authenticated", False) and not user.is_staff:
            own = getattr(user, "affiliate_profile", None)
            if own is None:
                raise serializers.ValidationError(_("You do not have an affiliate profile"))
            owner_id = own.id

        resolved_id = resolve_acting_id(
            self.context,
            data.get("affiliate_id"),
            owner_id,
            {"affiliate_id": _("You cannot request a payout for another affiliate.")},
        )

        try:
            affiliate = Affiliate.objects.get(id=resolved_id)
        except Affiliate.DoesNotExist:
            raise serializers.ValidationError({"affiliate_id": _("Affiliate does not exist")})

        if affiliate.status != "active":
            raise serializers.ValidationError(_("Affiliate is not active"))

        # Check minimum payout from programs
        programs = affiliate.programs.filter(affiliateprogrammembership__status="approved")
        if programs.exists():
            min_payout = min([p.minimum_payout for p in programs])
            if data["amount"] < min_payout:
                raise serializers.ValidationError(
                    _("Amount is below minimum payout threshold of ${}".format(min_payout))
                )

        data["affiliate"] = affiliate
        return data

    def create(self, validated_data):
        """Create payout request, reserving funds under a row lock.

        Locking the affiliate row serialises concurrent/sequential requests so
        the available balance (approved commissions minus already pending or
        processing payouts) is evaluated atomically, preventing two requests
        from over-committing the same funds.
        """
        affiliate = validated_data["affiliate"]
        amount = validated_data["amount"]

        with transaction.atomic():
            locked_affiliate = Affiliate.objects.select_for_update().get(pk=affiliate.pk)

            approved_balance = (
                locked_affiliate.commissions.filter(status="approved").aggregate(Sum("amount"))[
                    "amount__sum"
                ]
                or 0
            )
            # Reserve funds already committed to in-flight payouts.
            reserved = (
                locked_affiliate.payouts.filter(status__in=["pending", "processing"]).aggregate(
                    Sum("amount")
                )["amount__sum"]
                or 0
            )
            available = approved_balance - reserved

            if amount > available:
                raise serializers.ValidationError(
                    _("Insufficient balance. Available: ${}".format(available))
                )

            payout = Payout.objects.create(
                affiliate=locked_affiliate,
                amount=amount,
                method=validated_data["method"],
                status="pending",
            )
        return payout


# ============================================
# Dashboard Serializers
# ============================================


class AffiliateDashboardSerializer(serializers.Serializer):
    """Serializer for affiliate dashboard statistics"""

    overview = serializers.SerializerMethodField()
    recent_clicks = serializers.SerializerMethodField()
    recent_commissions = serializers.SerializerMethodField()
    top_links = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.affiliate = self.context.get("affiliate")

    def get_overview(self, obj) -> dict:
        """Get overview statistics"""
        total_clicks = Click.objects.filter(link__affiliate=self.affiliate).count()
        total_earned = (
            self.affiliate.commissions.filter(status__in=["approved", "paid"]).aggregate(
                Sum("amount")
            )["amount__sum"]
            or 0
        )
        pending_balance = (
            self.affiliate.commissions.filter(status="approved").aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )
        active_links = self.affiliate.links.filter(is_active=True).count()

        return {
            "total_clicks": total_clicks,
            "total_earned": float(total_earned),
            "pending_balance": float(pending_balance),
            "active_links": active_links,
        }

    def get_recent_clicks(self, obj) -> int:
        """Get recent clicks (last 24 hours)"""
        yesterday = timezone.now() - timedelta(days=1)
        return Click.objects.filter(
            link__affiliate=self.affiliate, clicked_at__gte=yesterday
        ).count()

    def get_recent_commissions(self, obj) -> list:
        """Get recent commissions"""
        recent = self.affiliate.commissions.order_by("-created_at")[:5]
        return CommissionListSerializer(recent, many=True).data

    def get_top_links(self, obj) -> list:
        """Get top performing links"""
        links = self.affiliate.links.annotate(clicks_count=Count("clicks")).order_by(
            "-clicks_count"
        )[:5]
        return LinkListSerializer(links, many=True).data


class MerchantDashboardSerializer(serializers.Serializer):
    """Serializer for merchant dashboard statistics"""

    overview = serializers.SerializerMethodField()
    pending_applications = serializers.SerializerMethodField()
    pending_commissions = serializers.SerializerMethodField()
    top_affiliates = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.merchant = self.context.get("merchant")

    def get_overview(self, obj) -> dict:
        """Get overview statistics"""
        programs = Program.objects.filter(merchant=self.merchant)
        total_affiliates = (
            Affiliate.objects.filter(
                programs__in=programs, affiliateprogrammembership__status="approved"
            )
            .distinct()
            .count()
        )
        total_clicks = Click.objects.filter(link__program__in=programs).count()
        total_commissions = (
            Commission.objects.filter(program__in=programs).aggregate(Sum("amount"))["amount__sum"]
            or 0
        )

        return {
            "total_programs": programs.count(),
            "total_affiliates": total_affiliates,
            "total_clicks": total_clicks,
            "total_commissions": float(total_commissions),
        }

    def get_pending_applications(self, obj) -> list:
        """Get pending affiliate applications"""
        programs = Program.objects.filter(merchant=self.merchant)
        pending = AffiliateProgramMembership.objects.filter(
            program__in=programs, status="pending"
        ).order_by("-applied_at")[:5]
        return AffiliateProgramMembershipSerializer(pending, many=True).data

    def get_pending_commissions(self, obj) -> list:
        """Get pending commissions"""
        programs = Program.objects.filter(merchant=self.merchant)
        pending = Commission.objects.filter(program__in=programs, status="pending").order_by(
            "-created_at"
        )[:5]
        return CommissionListSerializer(pending, many=True).data

    def get_top_affiliates(self, obj) -> list:
        """Get top performing affiliates"""
        programs = Program.objects.filter(merchant=self.merchant)
        # Compute each affiliate's commission total via a subquery so the
        # program-membership join can't fan out and multiply the sum for
        # affiliates approved in more than one of the merchant's programs.
        commission_total = (
            Commission.objects.filter(affiliate=OuterRef("pk"))
            .order_by()
            .values("affiliate")
            .annotate(total=Sum("amount"))
            .values("total")
        )
        affiliates = (
            Affiliate.objects.filter(
                programs__in=programs, affiliateprogrammembership__status="approved"
            )
            .distinct()
            .annotate(
                total_commissions=Coalesce(
                    Subquery(
                        commission_total,
                        output_field=DecimalField(max_digits=12, decimal_places=2),
                    ),
                    Value(Decimal("0"), output_field=DecimalField(max_digits=12, decimal_places=2)),
                )
            )
            .order_by("-total_commissions")[:5]
        )
        return AffiliateListSerializer(affiliates, many=True).data
