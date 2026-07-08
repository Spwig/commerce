"""
Loyalty Program API Views

Customer-facing API endpoints for loyalty program.
Provides access to loyalty status, rewards, and redemptions.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models, transaction
from django.db.models import Sum
from decimal import Decimal
import uuid as uuid_lib

from core.api.authentication import HeadlessAPIMixin
from loyalty.models import (
    LoyaltyMember,
    LoyaltyBalance,
    LoyaltyTransaction,
    LoyaltyTier,
    LoyaltyBadge,
    LoyaltyMemberBadge,
    LoyaltyRule,
    LoyaltyReward,
    LoyaltyRedemption,
)
from .serializers import (
    LoyaltyStatusSerializer,
    LoyaltyProgressSerializer,
    LoyaltyTransactionSerializer,
    LoyaltyTierSerializer,
    LoyaltyBadgeSerializer,
    LoyaltyMemberBadgeSerializer,
    LoyaltyRewardSerializer,
    LoyaltyRewardDetailSerializer,
    LoyaltyRedemptionSerializer,
    RedeemRewardSerializer,
    RedemptionResponseSerializer,
    LoyaltyRuleSerializer,
    LoyaltyEarningRulesSerializer,
)


class RedemptionRateThrottle(UserRateThrottle):
    """Rate limiting for reward redemptions"""
    rate = '10/hour'


@extend_schema_view(
    list=extend_schema(
        tags=['Loyalty'],
        summary=_("Get loyalty status"),
        description=_("Get the authenticated customer's loyalty program status including points balance and tier information."),
        responses={
            200: LoyaltyStatusSerializer,
            401: OpenApiResponse(description=_("Authentication required")),
            404: OpenApiResponse(description=_("Not enrolled in loyalty program")),
        }
    ),
)
class LoyaltyStatusViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Loyalty Status ViewSet

    Provides customer's loyalty program status and progress.

    Endpoints:
    - GET /api/loyalty/status/ - Get current loyalty status
    - GET /api/loyalty/progress/ - Get tier progress information
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Get customer's loyalty status

        Returns:
        - Member info (UUID, enrollment date, active status)
        - Points balance (available, pending, lifetime)
        - Current tier with benefits
        - Badges earned count
        """
        try:
            member = request.user.loyalty_member
        except LoyaltyMember.DoesNotExist:
            return Response({
                'success': False,
                'message': _('You are not enrolled in the loyalty program'),
                'enrolled': False
            }, status=status.HTTP_404_NOT_FOUND)

        # Get or create balance
        try:
            balance = member.balance
        except LoyaltyBalance.DoesNotExist:
            balance = LoyaltyBalance.objects.create(member=member)

        # Build status data
        status_data = {
            'member_uuid': member.uuid,
            'enrolled_at': member.enrolled_at,
            'is_active': member.is_active,
            'available_points': balance.available_points,
            'pending_points': balance.pending_points,
            'total_points': balance.total_points,
            'lifetime_earned': balance.lifetime_earned,
            'lifetime_redeemed': balance.lifetime_redeemed,
            'current_tier': member.current_tier,
            'badges_earned_count': member.badges_earned.count(),
        }

        serializer = LoyaltyStatusSerializer(status_data)

        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Loyalty'],
        summary=_("Get tier progress"),
        description=_("Get the customer's progress toward the next loyalty tier."),
        responses={
            200: LoyaltyProgressSerializer,
            401: OpenApiResponse(description=_("Authentication required")),
            404: OpenApiResponse(description=_("Not enrolled in loyalty program")),
        }
    )
    @action(detail=False, methods=['get'])
    def progress(self, request):
        """
        Get customer's tier progress

        Returns:
        - Current tier info
        - Next tier info (if available)
        - Progress percentages (spend, orders, points)
        - Remaining amounts to reach next tier
        """
        try:
            member = request.user.loyalty_member
        except LoyaltyMember.DoesNotExist:
            return Response({
                'success': False,
                'message': _('You are not enrolled in the loyalty program'),
                'enrolled': False
            }, status=status.HTTP_404_NOT_FOUND)

        # Get customer's current stats from their profile/orders
        from orders.models import Order
        from django.db.models import Sum, Count

        # Calculate customer's lifetime values
        order_stats = Order.objects.filter(
            user=request.user,
            status__in=['completed', 'delivered']
        ).aggregate(
            total_spend=Sum('total'),
            order_count=Count('id')
        )

        current_spend = order_stats['total_spend'] or Decimal('0.00')
        current_orders = order_stats['order_count'] or 0

        try:
            current_points_earned = member.balance.lifetime_earned
        except LoyaltyBalance.DoesNotExist:
            current_points_earned = 0

        current_tier = member.current_tier
        next_tier = member.get_next_tier()

        # Calculate progress
        progress_data = {
            'current_tier': current_tier,
            'next_tier': next_tier,
            'current_spend': current_spend,
            'current_orders': current_orders,
            'current_points_earned': current_points_earned,
            'spend_progress_percent': 0,
            'orders_progress_percent': 0,
            'points_progress_percent': 0,
            'spend_remaining': None,
            'orders_remaining': None,
            'points_remaining': None,
            'progress_message': '',
        }

        if next_tier:
            # Calculate progress percentages
            if next_tier.min_spend > 0:
                progress_data['spend_progress_percent'] = min(
                    100,
                    int((current_spend / next_tier.min_spend) * 100)
                )
                progress_data['spend_remaining'] = max(
                    Decimal('0.00'),
                    next_tier.min_spend - current_spend
                )

            if next_tier.min_orders > 0:
                progress_data['orders_progress_percent'] = min(
                    100,
                    int((current_orders / next_tier.min_orders) * 100)
                )
                progress_data['orders_remaining'] = max(
                    0,
                    next_tier.min_orders - current_orders
                )

            if next_tier.min_points_earned > 0:
                progress_data['points_progress_percent'] = min(
                    100,
                    int((current_points_earned / next_tier.min_points_earned) * 100)
                )
                progress_data['points_remaining'] = max(
                    0,
                    next_tier.min_points_earned - current_points_earned
                )

            # Generate progress message
            best_progress = max(
                progress_data['spend_progress_percent'],
                progress_data['orders_progress_percent'],
                progress_data['points_progress_percent']
            )
            progress_data['progress_message'] = _(
                "You're %(percent)s%% of the way to %(tier)s!"
            ) % {'percent': best_progress, 'tier': next_tier.name}
        else:
            progress_data['progress_message'] = _(
                "Congratulations! You've reached the highest tier."
            )

        serializer = LoyaltyProgressSerializer(progress_data)

        return Response({
            'success': True,
            'data': serializer.data
        })


@extend_schema_view(
    list=extend_schema(
        tags=['Loyalty'],
        summary=_("List all tiers"),
        description=_("Get all available loyalty tiers with their requirements and benefits."),
        responses={200: LoyaltyTierSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=['Loyalty'],
        summary=_("Get tier details"),
        description=_("Get details of a specific loyalty tier."),
        responses={200: LoyaltyTierSerializer}
    ),
)
class LoyaltyTierViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    Loyalty Tiers ViewSet

    Provides read-only access to loyalty tier information.

    Endpoints:
    - GET /api/loyalty/tiers/ - List all active tiers
    - GET /api/loyalty/tiers/{slug}/ - Get tier details
    """
    permission_classes = [AllowAny]
    serializer_class = LoyaltyTierSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return LoyaltyTier.objects.filter(is_active=True).order_by('rank')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'success': True,
            'data': serializer.data
        })


@extend_schema_view(
    list=extend_schema(
        tags=['Loyalty'],
        summary=_("List points history"),
        description=_("Get the authenticated customer's loyalty points transaction history."),
        parameters=[
            OpenApiParameter(
                name='type',
                description=_('Filter by transaction type (earn, redeem, expire, bonus)'),
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='limit',
                description=_('Number of transactions to return (default: 20)'),
                required=False,
                type=int
            ),
            OpenApiParameter(
                name='offset',
                description=_('Offset for pagination'),
                required=False,
                type=int
            ),
        ],
        responses={
            200: LoyaltyTransactionSerializer(many=True),
            401: OpenApiResponse(description=_("Authentication required")),
            404: OpenApiResponse(description=_("Not enrolled in loyalty program")),
        }
    ),
)
class LoyaltyHistoryViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Loyalty History ViewSet

    Provides customer's points transaction history.

    Endpoints:
    - GET /api/loyalty/history/ - List points transactions
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Get points transaction history

        Query parameters:
        - type: Filter by transaction type (earn, redeem, expire, bonus)
        - limit: Number of results (default: 20, max: 100)
        - offset: Pagination offset
        """
        try:
            member = request.user.loyalty_member
        except LoyaltyMember.DoesNotExist:
            return Response({
                'success': False,
                'message': _('You are not enrolled in the loyalty program'),
                'enrolled': False
            }, status=status.HTTP_404_NOT_FOUND)

        # Get transactions
        transactions = LoyaltyTransaction.objects.filter(
            member=member
        ).order_by('-created_at')

        # Filter by type
        tx_type = request.query_params.get('type')
        if tx_type and tx_type in dict(LoyaltyTransaction.TRANSACTION_TYPES):
            transactions = transactions.filter(transaction_type=tx_type)

        # Pagination
        limit = min(int(request.query_params.get('limit', 20)), 100)
        offset = int(request.query_params.get('offset', 0))

        total_count = transactions.count()
        transactions = transactions[offset:offset + limit]

        serializer = LoyaltyTransactionSerializer(transactions, many=True)

        return Response({
            'success': True,
            'data': serializer.data,
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_count
            }
        })


@extend_schema_view(
    list=extend_schema(
        tags=['Loyalty'],
        summary=_("List available rewards"),
        description=_("Get all available rewards that can be redeemed with loyalty points."),
        parameters=[
            OpenApiParameter(
                name='type',
                description=_('Filter by reward type (discount, product, shipping, experience)'),
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='featured',
                description=_('Show only featured rewards'),
                required=False,
                type=bool
            ),
            OpenApiParameter(
                name='affordable',
                description=_('Show only rewards the user can afford'),
                required=False,
                type=bool
            ),
        ],
        responses={200: LoyaltyRewardSerializer(many=True)}
    ),
    retrieve=extend_schema(
        tags=['Loyalty'],
        summary=_("Get reward details"),
        description=_("Get detailed information about a specific reward including eligibility."),
        responses={200: LoyaltyRewardDetailSerializer}
    ),
)
class LoyaltyRewardViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    Loyalty Rewards ViewSet

    Provides access to available rewards and redemption.

    Endpoints:
    - GET /api/loyalty/rewards/ - List available rewards
    - GET /api/loyalty/rewards/{uuid}/ - Get reward details
    - POST /api/loyalty/rewards/{uuid}/redeem/ - Redeem a reward
    """
    permission_classes = [AllowAny]
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LoyaltyRewardDetailSerializer
        return LoyaltyRewardSerializer

    def get_queryset(self):
        queryset = LoyaltyReward.objects.filter(
            is_active=True
        ).order_by('display_order', '-featured', 'points_cost')

        # Filter by type
        reward_type = self.request.query_params.get('type')
        if reward_type and reward_type in dict(LoyaltyReward.REWARD_TYPES):
            queryset = queryset.filter(reward_type=reward_type)

        # Filter featured only
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(featured=True)

        # Filter affordable (for authenticated users)
        affordable = self.request.query_params.get('affordable')
        if affordable and affordable.lower() == 'true' and self.request.user.is_authenticated:
            try:
                member = self.request.user.loyalty_member
                available_points = member.balance.available_points
                queryset = queryset.filter(points_cost__lte=available_points)
            except (LoyaltyMember.DoesNotExist, LoyaltyBalance.DoesNotExist):
                pass

        # Exclude expired or out-of-stock rewards
        now = timezone.now()
        queryset = queryset.exclude(end_date__lt=now)
        queryset = queryset.exclude(quantity_remaining=0)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})

        return Response({
            'success': True,
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})

        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Loyalty'],
        summary=_("Redeem a reward"),
        description=_("Redeem a reward using loyalty points. Returns the redemption details including any voucher codes generated."),
        responses={
            200: RedemptionResponseSerializer,
            400: OpenApiResponse(description=_("Cannot redeem reward")),
            401: OpenApiResponse(description=_("Authentication required")),
            404: OpenApiResponse(description=_("Reward not found or not enrolled")),
        }
    )
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        throttle_classes=[RedemptionRateThrottle]
    )
    def redeem(self, request, uuid=None):
        """
        Redeem a reward

        Deducts points and creates a redemption record.
        For discount rewards, generates a voucher code.
        """
        # Get reward
        try:
            reward = LoyaltyReward.objects.get(uuid=uuid, is_active=True)
        except LoyaltyReward.DoesNotExist:
            return Response({
                'success': False,
                'message': _('Reward not found'),
                'redemption': None
            }, status=status.HTTP_404_NOT_FOUND)

        # Get member
        try:
            member = request.user.loyalty_member
        except LoyaltyMember.DoesNotExist:
            return Response({
                'success': False,
                'message': _('You are not enrolled in the loyalty program'),
                'redemption': None
            }, status=status.HTTP_404_NOT_FOUND)

        # Check eligibility
        can_redeem, message = reward.can_member_redeem(member)
        if not can_redeem:
            return Response({
                'success': False,
                'message': message,
                'redemption': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Process redemption
        with transaction.atomic():
            # Generate redemption code
            redemption_code = f"LOYALTY-{uuid_lib.uuid4().hex[:5].upper()}-{uuid_lib.uuid4().hex[:5].upper()}"

            # Create redemption record
            redemption = LoyaltyRedemption.objects.create(
                member=member,
                reward=reward,
                points_spent=reward.points_cost,
                status=LoyaltyRedemption.STATUS_PENDING,
                redemption_code=redemption_code,
                expires_at=timezone.now() + timezone.timedelta(
                    days=reward.redemption_expires_days or 365
                )
            )

            # Create points transaction (deduction)
            points_tx = LoyaltyTransaction.objects.create(
                member=member,
                transaction_type=LoyaltyTransaction.TYPE_REDEEM,
                points=-reward.points_cost,
                status=LoyaltyTransaction.STATUS_REDEEMED,
                description=f"Redeemed: {reward.name}",
                reason=f"Redemption #{redemption.redemption_code}",
                related_object_type='redemption',
                related_object_id=str(redemption.id)
            )

            # Link transaction to redemption
            redemption.transaction = points_tx
            redemption.save(update_fields=['transaction'])

            # Update balance
            balance = member.balance
            balance.available_points -= reward.points_cost
            balance.lifetime_redeemed += reward.points_cost
            balance.last_redeemed_at = timezone.now()
            balance.save(update_fields=[
                'available_points',
                'lifetime_redeemed',
                'last_redeemed_at'
            ])

            # Update reward quantity if limited
            if reward.quantity_remaining is not None:
                reward.quantity_remaining -= 1
                reward.save(update_fields=['quantity_remaining'])

            # For discount rewards, create a voucher code
            if reward.reward_type == LoyaltyReward.TYPE_DISCOUNT:
                try:
                    from vouchers.services import VoucherService
                    voucher = VoucherService.create_loyalty_voucher(
                        reward=reward,
                        redemption=redemption,
                        member=member
                    )
                    if voucher:
                        redemption.voucher_code = voucher
                        redemption.save(update_fields=['voucher_code'])
                except (ImportError, AttributeError):
                    # VoucherService not implemented yet - voucher will be created manually
                    pass

            # Mark as confirmed
            redemption.status = LoyaltyRedemption.STATUS_CONFIRMED
            redemption.confirmed_at = timezone.now()
            redemption.save(update_fields=['status', 'confirmed_at'])

        serializer = LoyaltyRedemptionSerializer(redemption)

        return Response({
            'success': True,
            'message': _('Reward redeemed successfully!'),
            'redemption': serializer.data
        })


@extend_schema_view(
    list=extend_schema(
        tags=['Loyalty'],
        summary=_("List redemptions"),
        description=_("Get the authenticated customer's reward redemption history."),
        parameters=[
            OpenApiParameter(
                name='status',
                description=_('Filter by status (pending, confirmed, fulfilled, cancelled, expired)'),
                required=False,
                type=str
            ),
        ],
        responses={
            200: LoyaltyRedemptionSerializer(many=True),
            401: OpenApiResponse(description=_("Authentication required")),
            404: OpenApiResponse(description=_("Not enrolled in loyalty program")),
        }
    ),
    retrieve=extend_schema(
        tags=['Loyalty'],
        summary=_("Get redemption details"),
        description=_("Get details of a specific redemption."),
        responses={200: LoyaltyRedemptionSerializer}
    ),
)
class LoyaltyRedemptionViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    Loyalty Redemptions ViewSet

    Provides access to customer's redemption history.

    Endpoints:
    - GET /api/loyalty/redemptions/ - List redemptions
    - GET /api/loyalty/redemptions/{uuid}/ - Get redemption details
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LoyaltyRedemptionSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        try:
            member = self.request.user.loyalty_member
            queryset = LoyaltyRedemption.objects.filter(
                member=member
            ).select_related('reward').order_by('-created_at')

            # Filter by status
            redemption_status = self.request.query_params.get('status')
            if redemption_status and redemption_status in dict(LoyaltyRedemption.STATUSES):
                queryset = queryset.filter(status=redemption_status)

            return queryset
        except LoyaltyMember.DoesNotExist:
            return LoyaltyRedemption.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            request.user.loyalty_member
        except LoyaltyMember.DoesNotExist:
            return Response({
                'success': False,
                'message': _('You are not enrolled in the loyalty program'),
            }, status=status.HTTP_404_NOT_FOUND)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'success': True,
            'data': serializer.data
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({
            'success': True,
            'data': serializer.data
        })


@extend_schema_view(
    list=extend_schema(
        tags=['Loyalty'],
        summary=_("List earned badges"),
        description=_("Get the authenticated customer's earned loyalty badges."),
        responses={
            200: LoyaltyMemberBadgeSerializer(many=True),
            401: OpenApiResponse(description=_("Authentication required")),
            404: OpenApiResponse(description=_("Not enrolled in loyalty program")),
        }
    ),
)
class LoyaltyBadgeViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Loyalty Badges ViewSet

    Provides access to customer's earned badges.

    Endpoints:
    - GET /api/loyalty/badges/ - List earned badges
    - GET /api/loyalty/badges/available/ - List all available badges
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get customer's earned badges"""
        try:
            member = request.user.loyalty_member
        except LoyaltyMember.DoesNotExist:
            return Response({
                'success': False,
                'message': _('You are not enrolled in the loyalty program'),
            }, status=status.HTTP_404_NOT_FOUND)

        badges = LoyaltyMemberBadge.objects.filter(
            member=member
        ).select_related('badge').order_by('-earned_at')

        serializer = LoyaltyMemberBadgeSerializer(badges, many=True)

        return Response({
            'success': True,
            'data': serializer.data
        })

    @extend_schema(
        tags=['Loyalty'],
        summary=_("List available badges"),
        description=_("Get all visible badges that can be earned."),
        responses={200: LoyaltyBadgeSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def available(self, request):
        """Get all available badges"""
        badges = LoyaltyBadge.objects.filter(
            is_active=True,
            is_visible=True
        ).order_by('display_order', 'name')

        serializer = LoyaltyBadgeSerializer(badges, many=True)

        return Response({
            'success': True,
            'data': serializer.data
        })


@extend_schema_view(
    list=extend_schema(
        tags=['Loyalty'],
        summary=_("List earning rules"),
        description=_("Get all active rules for earning loyalty points."),
        responses={200: LoyaltyEarningRulesSerializer}
    ),
)
class LoyaltyEarningRulesViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Loyalty Earning Rules ViewSet

    Provides access to point earning rules.

    Endpoints:
    - GET /api/loyalty/earning-rules/ - List earning rules
    """
    permission_classes = [AllowAny]

    def list(self, request):
        """Get earning rules grouped by type"""
        now = timezone.now()

        # Get active rules
        active_rules = LoyaltyRule.objects.filter(
            is_active=True
        ).filter(
            models.Q(start_date__isnull=True) | models.Q(start_date__lte=now)
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
        ).order_by('priority')

        # Group by type
        spend_rules = active_rules.filter(rule_type=LoyaltyRule.TYPE_SPEND_BASED)
        action_rules = active_rules.filter(rule_type=LoyaltyRule.TYPE_ACTION_BASED)
        bonus_rules = active_rules.filter(
            rule_type__in=[LoyaltyRule.TYPE_EVENT_BASED, LoyaltyRule.TYPE_ITEM_BASED]
        )

        data = {
            'spend_rules': LoyaltyRuleSerializer(spend_rules, many=True).data,
            'action_rules': LoyaltyRuleSerializer(action_rules, many=True).data,
            'bonus_rules': LoyaltyRuleSerializer(bonus_rules, many=True).data,
        }

        return Response({
            'success': True,
            'data': data
        })
