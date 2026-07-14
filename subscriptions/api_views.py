"""
Subscription REST API Views
Following rules.md API standards with drf-spectacular documentation.
"""

import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.authentication import HeadlessAPIMixin
from payment_providers.models import PaymentProviderAccount

from .manager import SubscriptionManager
from .models import CustomerSubscription, PaymentToken, SubscriptionPlan
from .serializers import (
    BillingCycleLogSerializer,
    CancelScheduledChangeSerializer,
    CancelSubscriptionSerializer,
    ChangePlanSerializer,
    CreatePaymentTokenSerializer,
    CreateSubscriptionSerializer,
    CustomerSubscriptionSerializer,
    PauseSubscriptionSerializer,
    PaymentTokenSerializer,
    ReactivateSubscriptionSerializer,
    SubscriptionPlanSerializer,
    UpdatePaymentMethodSerializer,
)

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(
        tags=["Subscriptions"],
        summary=_("List subscription plans"),
        description=_("""Get all available subscription plans.

        **Filtering**: Only returns active and public plans unless user is staff.

        **Use Case**: Display available subscription options to customers during checkout or on pricing pages.

        **Security**: Public endpoint - no authentication required."""),
    ),
    retrieve=extend_schema(
        tags=["Subscriptions"],
        summary=_("Get subscription plan details"),
        description=_("""Get detailed information about a specific subscription plan.

        **Use Case**: Show plan details before subscription creation or on plan comparison pages.

        **Security**: Public endpoint - no authentication required."""),
    ),
)
class SubscriptionPlanViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for subscription plans.

    Provides read-only access to available subscription plans.
    Only shows active and public plans to non-staff users.
    """

    serializer_class = SubscriptionPlanSerializer
    lookup_field = "plan_id"
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter plans based on user permissions"""
        if self.request.user.is_staff:
            return SubscriptionPlan.objects.all()

        return SubscriptionPlan.objects.filter(is_active=True, is_public=True)


@extend_schema_view(
    list=extend_schema(
        tags=["Subscriptions"],
        summary=_("List payment tokens"),
        description=_("""Get all payment tokens for the authenticated user.

        **Filtering**: Only returns active tokens unless user is staff.

        **Use Case**: Show saved payment methods to users when subscribing or updating subscription payment method.

        **Security**: Requires authentication. Users can only see their own tokens."""),
    ),
    retrieve=extend_schema(
        tags=["Subscriptions"],
        summary=_("Get payment token details"),
        description=_("""Get detailed information about a specific payment token.

        **Security**: Requires authentication. Users can only access their own tokens."""),
    ),
    create=extend_schema(
        tags=["Subscriptions"],
        summary=_("Create payment token"),
        description=_("""Create a new payment token for recurring billing.

        **Provider-Specific Data Required**:

        **Stripe**:
        - `payment_method_id`: From Stripe.js on frontend
        - `set_as_default`: Boolean

        **Square**:
        - `card_nonce`: From Square Payment Form
        - `billing_postal_code`: Cardholder ZIP
        - `cardholder_name`: Cardholder name

        **Use Case**: Save a payment method for recurring subscription billing.

        **Security**: Requires authentication. Rate limited to prevent abuse."""),
        request=CreatePaymentTokenSerializer,
        responses={
            201: OpenApiResponse(
                description=_("Payment token created successfully"), response=PaymentTokenSerializer
            ),
            400: OpenApiResponse(description=_("Invalid payment method data")),
            401: OpenApiResponse(description=_("Authentication required")),
        },
    ),
    destroy=extend_schema(
        tags=["Subscriptions"],
        summary=_("Delete payment token"),
        description=_("""Delete a payment token.

        **Warning**: Cannot delete token if it's being used by an active subscription.

        **Security**: Requires authentication. Users can only delete their own tokens."""),
    ),
)
class PaymentTokenViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for payment tokens.

    Manages tokenized payment methods for recurring billing.
    """

    serializer_class = PaymentTokenSerializer
    lookup_field = "token_id"
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        """Filter tokens to current user"""
        return PaymentToken.objects.filter(user=self.request.user).select_related(
            "provider_account"
        )

    def perform_create(self, serializer):
        """Create payment token via SubscriptionManager"""
        data = serializer.validated_data
        provider_account = PaymentProviderAccount.objects.get(id=data["provider_account_id"])

        manager = SubscriptionManager(provider_account)

        payment_token = manager.create_customer_token(
            user=self.request.user,
            payment_method_data=data["payment_method_data"],
            set_as_default=data["set_as_default"],
        )

        return payment_token

    def create(self, request, *args, **kwargs):
        """Override create to use SubscriptionManager"""
        serializer = CreatePaymentTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        try:
            payment_token = self.perform_create(serializer)

            output_serializer = PaymentTokenSerializer(payment_token)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(f"Failed to create payment token: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        """Delete payment token - check for active subscriptions first"""
        # Check if token is used by active subscriptions
        active_subs = CustomerSubscription.objects.filter(
            payment_token=instance, status__in=["trial", "active", "past_due", "paused"]
        ).exists()

        if active_subs:
            raise serializers.ValidationError(
                "Cannot delete payment token - it's being used by active subscriptions"
            )

        # Delete token at provider
        from .provider_base import get_provider

        provider = get_provider(instance.provider_account)
        provider.delete_payment_token(instance.gateway_token_id)

        # Delete local record
        instance.delete()


@extend_schema_view(
    list=extend_schema(
        tags=["Subscriptions"],
        summary=_("List customer subscriptions"),
        description=_("""Get all subscriptions for the authenticated user.

        **Filtering**: Supports filtering by status.

        **Use Case**: Show user's active and past subscriptions in their account dashboard.

        **Security**: Requires authentication. Users can only see their own subscriptions."""),
        parameters=[
            OpenApiParameter(
                name="status",
                type=str,
                location=OpenApiParameter.QUERY,
                description=_(
                    "Filter by status (trial, active, past_due, paused, canceled, expired)"
                ),
                required=False,
            ),
        ],
    ),
    retrieve=extend_schema(
        tags=["Subscriptions"],
        summary=_("Get subscription details"),
        description=_("""Get detailed information about a specific subscription.

        **Security**: Requires authentication. Users can only access their own subscriptions."""),
    ),
    create=extend_schema(
        tags=["Subscriptions"],
        summary=_("Create subscription"),
        description=_("""Create a new subscription.

        **Required Fields**:
        - `plan_id`: UUID of subscription plan
        - `payment_token_id`: UUID of saved payment token

        **Optional Fields**:
        - `product_id`: Link subscription to specific product
        - `variant_id`: Link subscription to specific product variant
        - `trial_override_days`: Override plan's default trial period

        **Use Case**: Subscribe user to a plan during checkout or from pricing page.

        **Security**: Requires authentication. Creates subscription for authenticated user."""),
        request=CreateSubscriptionSerializer,
        responses={
            201: OpenApiResponse(
                description=_("Subscription created successfully"),
                response=CustomerSubscriptionSerializer,
            ),
            400: OpenApiResponse(description=_("Invalid subscription data")),
            401: OpenApiResponse(description=_("Authentication required")),
        },
    ),
)
class CustomerSubscriptionViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for customer subscriptions.

    Manages customer subscription lifecycle including creation, viewing, and management.
    """

    serializer_class = CustomerSubscriptionSerializer
    lookup_field = "subscription_id"
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post"]  # Create and read only - updates via actions

    def get_queryset(self):
        """Filter subscriptions to current user"""
        queryset = CustomerSubscription.objects.filter(user=self.request.user).select_related(
            "plan", "payment_provider_account", "payment_token", "product", "variant"
        )

        # Filter by status if provided
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def create(self, request, *args, **kwargs):
        """Create subscription via SubscriptionManager"""
        serializer = CreateSubscriptionSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        try:
            from .models import PlanPricingTier

            # Get plan, pricing tier, and payment token
            plan = SubscriptionPlan.objects.get(plan_id=serializer.validated_data["plan_id"])
            pricing_tier = PlanPricingTier.objects.get(
                tier_id=serializer.validated_data["pricing_tier_id"]
            )
            payment_token = PaymentToken.objects.get(
                token_id=serializer.validated_data["payment_token_id"], user=request.user
            )

            # Get product and optional variant
            from catalog.models import Product

            product = Product.objects.get(id=serializer.validated_data["product_id"])

            variant = None
            if serializer.validated_data.get("variant_id"):
                from catalog.models import ProductVariant

                variant = ProductVariant.objects.get(id=serializer.validated_data["variant_id"])

            # Create subscription via manager
            manager = SubscriptionManager(payment_token.provider_account)
            subscription = manager.create_subscription(
                user=request.user,
                plan=plan,
                pricing_tier=pricing_tier,
                payment_token=payment_token,
                product=product,
                variant=variant,
                quantity=serializer.validated_data.get("quantity", 1),
                trial_override_days=serializer.validated_data.get("trial_override_days"),
            )

            output_serializer = CustomerSubscriptionSerializer(subscription)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(f"Failed to create subscription: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Subscriptions"],
        summary=_("Cancel subscription"),
        description=_("""Cancel a subscription.

        **Options**:
        - `immediately`: If true, cancel immediately; otherwise cancel at period end
        - `reason`: Optional cancellation reason for analytics

        **Use Case**: Allow users to cancel their subscription from account settings.

        **Security**: Requires authentication. Users can only cancel their own subscriptions."""),
        request=CancelSubscriptionSerializer,
        responses={
            200: OpenApiResponse(
                description=_("Subscription canceled successfully"),
                response=CustomerSubscriptionSerializer,
            ),
            400: OpenApiResponse(description=_("Cannot cancel subscription")),
            404: OpenApiResponse(description=_("Subscription not found")),
        },
    )
    @action(detail=True, methods=["post"])
    def cancel(self, request, subscription_id=None):
        """Cancel subscription"""
        subscription = self.get_object()

        serializer = CancelSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            manager = SubscriptionManager(subscription.payment_provider_account)
            updated_subscription = manager.cancel_subscription(
                subscription=subscription,
                immediately=serializer.validated_data.get("immediately", False),
                reason=serializer.validated_data.get("reason", ""),
            )

            output_serializer = CustomerSubscriptionSerializer(updated_subscription)
            return Response(output_serializer.data)

        except Exception as e:
            logger.exception(f"Failed to cancel subscription: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Subscriptions"],
        summary=_("Pause subscription"),
        description=_("""Pause a subscription temporarily.

        **Options**:
        - `reason`: Optional pause reason
        - `auto_resume_date`: Optional date to automatically resume

        **Use Case**: Allow users to pause subscription during vacation or temporary inactivity.

        **Security**: Requires authentication. Users can only pause their own subscriptions."""),
        request=PauseSubscriptionSerializer,
        responses={
            200: OpenApiResponse(
                description=_("Subscription paused successfully"),
                response=CustomerSubscriptionSerializer,
            ),
            400: OpenApiResponse(description=_("Cannot pause subscription")),
            404: OpenApiResponse(description=_("Subscription not found")),
        },
    )
    @action(detail=True, methods=["post"])
    def pause(self, request, subscription_id=None):
        """Pause subscription"""
        subscription = self.get_object()

        serializer = PauseSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            manager = SubscriptionManager(subscription.payment_provider_account)
            updated_subscription = manager.pause_subscription(
                subscription=subscription,
                reason=serializer.validated_data.get("reason", ""),
                auto_resume_date=serializer.validated_data.get("auto_resume_date"),
            )

            output_serializer = CustomerSubscriptionSerializer(updated_subscription)
            return Response(output_serializer.data)

        except Exception as e:
            logger.exception(f"Failed to pause subscription: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Subscriptions"],
        summary=_("Resume subscription"),
        description=_("""Resume a paused subscription.

        **Use Case**: Allow users to resume paused subscription.

        **Security**: Requires authentication. Users can only resume their own subscriptions."""),
        responses={
            200: OpenApiResponse(
                description=_("Subscription resumed successfully"),
                response=CustomerSubscriptionSerializer,
            ),
            400: OpenApiResponse(description=_("Cannot resume subscription")),
            404: OpenApiResponse(description=_("Subscription not found")),
        },
    )
    @action(detail=True, methods=["post"])
    def resume(self, request, subscription_id=None):
        """Resume paused subscription"""
        subscription = self.get_object()

        try:
            manager = SubscriptionManager(subscription.payment_provider_account)
            updated_subscription = manager.resume_subscription(subscription)

            output_serializer = CustomerSubscriptionSerializer(updated_subscription)
            return Response(output_serializer.data)

        except Exception as e:
            logger.exception(f"Failed to resume subscription: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Subscriptions"],
        summary=_("Update payment method"),
        description=_("""Update subscription payment method.

        **Required Field**:
        - `payment_token_id`: UUID of new payment token

        **Use Case**: Allow users to change credit card used for subscription.

        **Security**: Requires authentication. Users can only update their own subscriptions."""),
        request=UpdatePaymentMethodSerializer,
        responses={
            200: OpenApiResponse(
                description=_("Payment method updated successfully"),
                response=CustomerSubscriptionSerializer,
            ),
            400: OpenApiResponse(description=_("Invalid payment token")),
            404: OpenApiResponse(description=_("Subscription not found")),
        },
    )
    @action(detail=True, methods=["post"])
    def update_payment_method(self, request, subscription_id=None):
        """Update subscription payment method"""
        subscription = self.get_object()

        serializer = UpdatePaymentMethodSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        try:
            new_token = PaymentToken.objects.get(
                token_id=serializer.validated_data["payment_token_id"], user=request.user
            )

            manager = SubscriptionManager(subscription.payment_provider_account)
            updated_subscription = manager.update_payment_method(
                subscription=subscription, payment_token=new_token
            )

            output_serializer = CustomerSubscriptionSerializer(updated_subscription)
            return Response(output_serializer.data)

        except PaymentToken.DoesNotExist:
            return Response({"error": "Payment token not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"Failed to update payment method: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Subscriptions"],
        summary=_("Get billing history"),
        description=_("""Get billing history for a subscription.

        Shows all billing attempts, successful and failed, with retry information.

        **Use Case**: Display subscription billing history to users.

        **Security**: Requires authentication. Users can only view their own subscription history."""),
        responses={
            200: OpenApiResponse(
                description=_("Billing history retrieved successfully"),
                response=BillingCycleLogSerializer(many=True),
            ),
            404: OpenApiResponse(description=_("Subscription not found")),
        },
    )
    @action(detail=True, methods=["get"])
    def billing_history(self, request, subscription_id=None):
        """Get billing history for subscription"""
        subscription = self.get_object()

        logs = subscription.billing_logs.all().order_by("-billing_date")

        serializer = BillingCycleLogSerializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=["Subscriptions"],
        summary=_("Change subscription plan"),
        description=_("""Change the subscription to a different plan.

        **Required Fields**:
        - `new_plan_id`: UUID of the new subscription plan
        - `new_tier_id`: UUID of the new pricing tier

        **Optional Fields**:
        - `mode`: 'auto' (default, uses plan-configured behavior), 'immediate', or 'at_renewal'

        **Behavior**:
        - **Upgrades**: By default applied immediately with prorated charge
        - **Downgrades**: By default deferred to next renewal with prorated credit
        - The `mode` parameter overrides plan-configured behavior

        **Security**: Requires authentication. Users can only change their own subscriptions."""),
        request=ChangePlanSerializer,
        responses={
            200: OpenApiResponse(
                description=_("Plan changed or scheduled successfully"),
                response=CustomerSubscriptionSerializer,
            ),
            400: OpenApiResponse(description=_("Cannot change plan")),
            404: OpenApiResponse(description=_("Subscription not found")),
        },
    )
    @action(detail=True, methods=["post"])
    def change_plan(self, request, subscription_id=None):
        """Change subscription plan (upgrade/downgrade)"""
        subscription = self.get_object()

        serializer = ChangePlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            from .models import PlanPricingTier

            new_plan = SubscriptionPlan.objects.get(
                plan_id=serializer.validated_data["new_plan_id"]
            )
            new_tier = PlanPricingTier.objects.get(tier_id=serializer.validated_data["new_tier_id"])

            manager = SubscriptionManager(subscription.payment_provider_account)
            updated_subscription = manager.change_plan(
                subscription=subscription,
                new_plan=new_plan,
                new_tier=new_tier,
                mode=serializer.validated_data.get("mode", "auto"),
            )

            output_serializer = CustomerSubscriptionSerializer(updated_subscription)
            return Response(output_serializer.data)

        except SubscriptionPlan.DoesNotExist:
            return Response(
                {"error": "Subscription plan not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except PlanPricingTier.DoesNotExist:
            return Response({"error": "Pricing tier not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Failed to change plan: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        tags=["Subscriptions"],
        summary=_("Cancel scheduled plan change"),
        description=_("""Cancel a pending scheduled plan change.

        If a plan change is scheduled for the next billing cycle, this action
        cancels it and keeps the current plan.

        **Use Case**: User changed their mind about a deferred plan change.

        **Security**: Requires authentication. Users can only modify their own subscriptions."""),
        request=CancelScheduledChangeSerializer,
        responses={
            200: OpenApiResponse(
                description=_("Scheduled change canceled"), response=CustomerSubscriptionSerializer
            ),
            400: OpenApiResponse(description=_("No scheduled change to cancel")),
            404: OpenApiResponse(description=_("Subscription not found")),
        },
    )
    @action(detail=True, methods=["post"])
    def cancel_scheduled_change(self, request, subscription_id=None):
        """Cancel a scheduled plan change"""
        subscription = self.get_object()

        if not subscription.has_scheduled_plan_change():
            return Response(
                {"error": "No scheduled plan change to cancel"}, status=status.HTTP_400_BAD_REQUEST
            )

        subscription.cancel_scheduled_plan_change()

        output_serializer = CustomerSubscriptionSerializer(subscription)
        return Response(output_serializer.data)

    @extend_schema(
        tags=["Subscriptions"],
        summary=_("Reactivate canceled subscription"),
        description=_("""Reactivate a previously canceled subscription within the reactivation window.

        **Optional Fields**:
        - `payment_token_id`: UUID of payment token (uses existing if not provided)

        **Behavior**:
        - Starts a new billing period from today
        - For native providers: creates a new provider subscription
        - Requires the reactivation deadline to not have passed

        **Use Case**: Allow customers to resubscribe after canceling, using the same plan and settings.

        **Security**: Requires authentication. Users can only reactivate their own subscriptions."""),
        request=ReactivateSubscriptionSerializer,
        responses={
            200: OpenApiResponse(
                description=_("Subscription reactivated successfully"),
                response=CustomerSubscriptionSerializer,
            ),
            400: OpenApiResponse(description=_("Cannot reactivate subscription")),
            404: OpenApiResponse(description=_("Subscription not found")),
        },
    )
    @action(detail=True, methods=["post"])
    def reactivate(self, request, subscription_id=None):
        """Reactivate a canceled subscription"""
        subscription = self.get_object()

        serializer = ReactivateSubscriptionSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        # Resolve payment token if provided
        payment_token = None
        token_id = serializer.validated_data.get("payment_token_id")
        if token_id:
            try:
                payment_token = PaymentToken.objects.get(token_id=token_id, user=request.user)
            except PaymentToken.DoesNotExist:
                return Response(
                    {"error": "Payment token not found"}, status=status.HTTP_404_NOT_FOUND
                )

        try:
            manager = SubscriptionManager(subscription.payment_provider_account)
            updated_subscription = manager.reactivate_subscription(
                subscription=subscription, payment_token=payment_token
            )

            output_serializer = CustomerSubscriptionSerializer(updated_subscription)
            return Response(output_serializer.data)

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Failed to reactivate subscription: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
