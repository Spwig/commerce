"""
Referrals API Views (DRF)
REST API endpoints for referral program management
"""

from django.db.models import Avg, Q, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from core.api.authentication import HeadlessAPIMixin
from referrals.api.serializers import (
    ApproveAttributionSerializer,
    ReferralAttributionListSerializer,
    ReferralAttributionSerializer,
    ReferralEventSerializer,
    ReferralIdentityListSerializer,
    ReferralIdentitySerializer,
    ReferralProgramSerializer,
    ReferralRewardListSerializer,
    ReferralRewardSerializer,
    RejectAttributionSerializer,
)
from referrals.models import (
    ReferralAttribution,
    ReferralEvent,
    ReferralIdentity,
    ReferralProgram,
    ReferralReward,
)


@extend_schema_view(
    list=extend_schema(tags=["Referrals"], summary=_("Get referral program configuration")),
    retrieve=extend_schema(tags=["Referrals"], summary=_("Get referral program configuration")),
    update=extend_schema(tags=["Referrals"], summary=_("Update referral program")),
    partial_update=extend_schema(
        tags=["Referrals"], summary=_("Partially update referral program")
    ),
    stats=extend_schema(tags=["Referrals"], summary=_("Get program statistics")),
)
class ReferralProgramViewSet(viewsets.ModelViewSet):
    """
    ViewSet for referral program configuration (singleton)
    """

    queryset = ReferralProgram.objects.all()
    serializer_class = ReferralProgramSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "put", "patch"]  # No create/delete for singleton

    def get_object(self):
        """Always return the singleton program instance"""
        return ReferralProgram.get_program()

    def list(self, request):
        """List returns the singleton instance"""
        program = self.get_object()
        serializer = self.get_serializer(program)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        """
        Get overall program statistics
        GET /api/referrals/program/stats/
        """
        program = self.get_object()

        # Get attribution stats
        attributions = ReferralAttribution.objects.filter(program=program)

        stats = {
            "total_referrers": ReferralIdentity.objects.count(),
            "total_clicks": ReferralIdentity.objects.aggregate(total=Sum("total_clicks"))["total"]
            or 0,
            "total_signups": ReferralIdentity.objects.aggregate(total=Sum("total_signups"))["total"]
            or 0,
            "total_conversions": ReferralIdentity.objects.aggregate(total=Sum("total_conversions"))[
                "total"
            ]
            or 0,
            "total_rewards_issued": ReferralReward.objects.filter(
                program=program, status="issued"
            ).count(),
            "total_rewards_redeemed": ReferralReward.objects.filter(
                program=program, status="redeemed"
            ).count(),
            "pending_attributions": attributions.filter(status="pending").count(),
            "approved_attributions": attributions.filter(status="approved").count(),
            "rejected_attributions": attributions.filter(status="rejected").count(),
            "average_risk_score": attributions.exclude(risk_score__isnull=True).aggregate(
                avg=Avg("risk_score")
            )["avg"]
            or 0,
        }

        return Response(stats)


@extend_schema_view(
    list=extend_schema(tags=["Referrals"], summary=_("List referral identities")),
    retrieve=extend_schema(tags=["Referrals"], summary=_("Get referral identity details")),
    create=extend_schema(tags=["Referrals"], summary=_("Create referral identity")),
    update=extend_schema(tags=["Referrals"], summary=_("Update referral identity")),
    partial_update=extend_schema(
        tags=["Referrals"], summary=_("Partially update referral identity")
    ),
    destroy=extend_schema(tags=["Referrals"], summary=_("Delete referral identity")),
    me=extend_schema(tags=["Referrals"], summary=_("Get current user's referral identity")),
    generate_qr=extend_schema(tags=["Referrals"], summary=_("Generate QR code for referral link")),
)
class ReferralIdentityViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing referral identities
    """

    queryset = ReferralIdentity.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Use list serializer for list action"""
        if self.action == "list":
            return ReferralIdentityListSerializer
        return ReferralIdentitySerializer

    def get_permissions(self):
        """Admin-only for create/update/delete"""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter based on user permissions"""
        queryset = ReferralIdentity.objects.select_related("customer")

        # Non-admins only see their own identity
        if not self.request.user.is_staff:
            queryset = queryset.filter(customer=self.request.user)

        # Search by customer email or name
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(customer__email__icontains=search)
                | Q(customer__first_name__icontains=search)
                | Q(customer__last_name__icontains=search)
                | Q(token__icontains=search)
            )

        # Order by conversions for admins
        if self.request.user.is_staff:
            queryset = queryset.order_by("-total_conversions", "-total_clicks")

        return queryset

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        Get current user's referral identity
        GET /api/referrals/identities/me/
        """
        identity, created = ReferralIdentity.objects.get_or_create(customer=request.user)
        serializer = self.get_serializer(identity)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="generate-qr")
    def generate_qr(self, request, pk=None):
        """
        Generate QR code for referral link
        POST /api/referrals/identities/{id}/generate-qr/
        """
        from io import BytesIO

        import qrcode
        from django.core.files.base import ContentFile

        identity = self.get_object()
        referral_link = request.build_absolute_uri(identity.get_referral_link())

        qr = qrcode.make(referral_link, box_size=10, border=2)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        filename = f"referral_qr_{identity.token}.png"
        identity.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)

        return Response(
            {
                "success": True,
                "qr_code_url": request.build_absolute_uri(identity.qr_code.url),
                "referral_link": referral_link,
            }
        )


@extend_schema_view(
    list=extend_schema(tags=["Referrals"], summary=_("List referral events")),
    retrieve=extend_schema(tags=["Referrals"], summary=_("Get event details")),
)
class ReferralEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing referral events (read-only)
    """

    queryset = ReferralEvent.objects.all()
    serializer_class = ReferralEventSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """Filter events"""
        queryset = ReferralEvent.objects.select_related(
            "referrer_identity", "customer", "program"
        ).order_by("-created_at")

        # Filter by event type
        event_type = self.request.query_params.get("event_type")
        if event_type:
            queryset = queryset.filter(event_type=event_type)

        # Filter by referrer
        referrer_id = self.request.query_params.get("referrer_identity")
        if referrer_id:
            queryset = queryset.filter(referrer_identity_id=referrer_id)

        # Filter by customer
        customer_id = self.request.query_params.get("customer")
        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)

        return queryset


@extend_schema_view(
    list=extend_schema(tags=["Referrals"], summary=_("List referral attributions")),
    retrieve=extend_schema(tags=["Referrals"], summary=_("Get attribution details")),
    update=extend_schema(tags=["Referrals"], summary=_("Update attribution")),
    partial_update=extend_schema(tags=["Referrals"], summary=_("Partially update attribution")),
    approve=extend_schema(tags=["Referrals"], summary=_("Approve attribution")),
    reject=extend_schema(tags=["Referrals"], summary=_("Reject attribution")),
    pending=extend_schema(tags=["Referrals"], summary=_("List pending attributions")),
)
class ReferralAttributionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing referral attributions
    """

    queryset = ReferralAttribution.objects.all()
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "put", "patch"]  # No create/delete

    def get_serializer_class(self):
        """Use list serializer for list action"""
        if self.action == "list":
            return ReferralAttributionListSerializer
        return ReferralAttributionSerializer

    def get_queryset(self):
        """Filter attributions"""
        queryset = ReferralAttribution.objects.select_related(
            "referrer_identity", "referee", "first_order", "program"
        ).order_by("-created_at")

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by referrer
        referrer_id = self.request.query_params.get("referrer_identity")
        if referrer_id:
            queryset = queryset.filter(referrer_identity_id=referrer_id)

        # Filter by risk score
        high_risk = self.request.query_params.get("high_risk")
        if high_risk == "true":
            queryset = queryset.filter(risk_score__gte=70)

        return queryset

    @action(detail=False, methods=["get"], url_path="pending")
    def pending(self, request):
        """
        Get pending attributions requiring review
        GET /api/referrals/attributions/pending/
        """
        queryset = self.get_queryset().filter(status="pending")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        """
        Approve an attribution
        POST /api/referrals/attributions/{id}/approve/
        Body: {"note": "Optional approval note"}
        """
        attribution = self.get_object()

        if attribution.status != "pending":
            return Response(
                {"error": "Only pending attributions can be approved"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ApproveAttributionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Update attribution
        attribution.status = "approved"
        attribution.approved_at = timezone.now()
        attribution.reviewed_by = request.user
        attribution.save()

        # Create and issue rewards (idempotent — signal may also fire)
        from referrals.services.rewards import create_and_issue_rewards

        create_and_issue_rewards(attribution)

        return Response(
            {
                "success": True,
                "message": "Attribution approved successfully",
                "attribution": ReferralAttributionSerializer(attribution).data,
            }
        )

    @action(detail=True, methods=["post"], url_path="reject")
    def reject(self, request, pk=None):
        """
        Reject an attribution
        POST /api/referrals/attributions/{id}/reject/
        Body: {"rejection_reason": "fraud_risk", "rejection_note": "Optional note"}
        """
        attribution = self.get_object()

        if attribution.status != "pending":
            return Response(
                {"error": "Only pending attributions can be rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RejectAttributionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Update attribution
        attribution.status = "rejected"
        attribution.rejection_reason = serializer.validated_data["rejection_reason"]
        attribution.rejection_note = serializer.validated_data.get("rejection_note", "")
        attribution.save()

        return Response(
            {
                "success": True,
                "message": "Attribution rejected successfully",
                "attribution": ReferralAttributionSerializer(attribution).data,
            }
        )


@extend_schema_view(
    list=extend_schema(tags=["Referrals"], summary=_("List referral rewards")),
    retrieve=extend_schema(tags=["Referrals"], summary=_("Get reward details")),
    update=extend_schema(tags=["Referrals"], summary=_("Update reward")),
    partial_update=extend_schema(tags=["Referrals"], summary=_("Partially update reward")),
    my_rewards=extend_schema(tags=["Referrals"], summary=_("Get current user's rewards")),
    revoke=extend_schema(tags=["Referrals"], summary=_("Revoke a reward")),
)
class ReferralRewardViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing referral rewards
    """

    queryset = ReferralReward.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "patch"]  # No create/delete

    def get_serializer_class(self):
        """Use list serializer for list action"""
        if self.action == "list":
            return ReferralRewardListSerializer
        return ReferralRewardSerializer

    def get_permissions(self):
        """Admin-only for update"""
        if self.action in ["update", "partial_update", "revoke"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Filter rewards based on permissions"""
        queryset = ReferralReward.objects.select_related(
            "customer", "attribution", "program"
        ).order_by("-created_at")

        # Non-admins only see their own rewards
        if not self.request.user.is_staff:
            queryset = queryset.filter(customer=self.request.user)

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by recipient type
        recipient_type = self.request.query_params.get("recipient_type")
        if recipient_type:
            queryset = queryset.filter(recipient_type=recipient_type)

        # Filter by kind
        kind = self.request.query_params.get("kind")
        if kind:
            queryset = queryset.filter(kind=kind)

        # Filter expiring soon
        expiring_soon = self.request.query_params.get("expiring_soon")
        if expiring_soon == "true":
            # Rewards expiring in next 7 days
            soon_date = timezone.now() + timezone.timedelta(days=7)
            queryset = queryset.filter(expires_at__lte=soon_date, status="issued")

        return queryset

    @action(detail=False, methods=["get"], url_path="my-rewards")
    def my_rewards(self, request):
        """
        Get current user's rewards
        GET /api/referrals/rewards/my-rewards/
        """
        queryset = self.get_queryset().filter(customer=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="revoke")
    def revoke(self, request, pk=None):
        """
        Revoke a reward
        POST /api/referrals/rewards/{id}/revoke/
        Body: {"reason": "Order refunded"}
        """
        reward = self.get_object()

        if reward.status not in ["pending", "issued"]:
            return Response(
                {"error": "Only pending or issued rewards can be revoked"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason = request.data.get("reason", "")

        from referrals.services.rewards import revoke_reward

        revoke_reward(reward, reason=reason)

        return Response(
            {
                "success": True,
                "message": "Reward revoked successfully",
                "reward": ReferralRewardSerializer(reward).data,
            }
        )
