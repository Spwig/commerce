"""
Payment Orchestration API Views

Public API views for payment orchestration.
These endpoints are used by headless frontends to initiate and manage payments.

API Tag: Payment Methods (per rules_llm.md approved tags list)
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
import logging

from core.api.authentication import HeadlessAPIMixin
from cart.models import CheckoutSession
from payment_providers.models import PaymentIntent, PaymentProviderAccount
from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
from payment_providers.api_serializers import (
    CreatePaymentIntentSerializer,
    PaymentIntentResponseSerializer,
    PaymentIntentStatusSerializer,
    ConfirmPaymentIntentSerializer,
    CancelPaymentIntentSerializer,
    SavedPaymentMethodSerializer,
    CreateSavedPaymentMethodSerializer,
)

logger = logging.getLogger(__name__)


class PaymentIntentCreateView(HeadlessAPIMixin, APIView):
    """
    Create a payment intent for checkout.

    This endpoint creates an order (with 'unpaid' status) and a payment intent
    with the specified provider. It returns either a checkout URL for hosted
    checkout or a client secret for embedded checkout.

    The order is created first with stock allocated. If payment fails, the
    customer can retry, and a new intent will be created for the same order.
    """
    permission_classes = [AllowAny]  # Allow guest checkout

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Create payment intent"),
        description=_("""
Create a payment intent for checkout.

**Process:**
1. Creates an Order with `payment_status='unpaid'` (stock is allocated)
2. Creates a PaymentIntent with the selected payment provider
3. Returns `checkout_url` (hosted) or `client_secret` (embedded)

**Authentication:** Optional - supports guest checkout with session cookie.

**Checkout Flows:**
- **Hosted checkout:** Redirect user to `checkout_url` returned in response
- **Embedded checkout:** Use `client_secret` with provider's JavaScript SDK

**Retry Handling:**
If payment fails, the customer can retry. A new PaymentIntent will be created
for the same Order (stock remains allocated).

**Security:**
- Checkout session is validated for ownership
- Provider must be active and connected
- Amounts are validated against checkout session totals
        """),
        request=CreatePaymentIntentSerializer,
        responses={
            201: OpenApiResponse(
                response=PaymentIntentResponseSerializer,
                description=_("Payment intent created successfully")
            ),
            400: OpenApiResponse(
                description=_("Invalid request, checkout not ready, or validation failed")
            ),
            404: OpenApiResponse(
                description=_("Checkout session not found")
            ),
        }
    )
    def post(self, request):
        serializer = CreatePaymentIntentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        # Get checkout session
        checkout_session = self._get_checkout_session(request, data.get('checkout_session_id'))
        if not checkout_session:
            return Response(
                {'success': False, 'message': _("Checkout session not found")},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get provider account
        provider_account = self._get_provider_account(checkout_session, data.get('provider_id'))
        if not provider_account:
            return Response(
                {'success': False, 'message': _("Payment provider not found or not configured")},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create payment intent
        success, intent, message = PaymentOrchestrationService.create_payment_intent(
            checkout_session=checkout_session,
            provider_account=provider_account,
            return_url=data['return_url'],
            cancel_url=data['cancel_url'],
            saved_method_id=str(data.get('saved_method_id')) if data.get('saved_method_id') else None,
            metadata=data.get('metadata', {})
        )

        if not success:
            return Response(
                {'success': False, 'message': str(message)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serialize response
        response_data = PaymentIntentResponseSerializer(intent).data
        response_data['success'] = True

        return Response(response_data, status=status.HTTP_201_CREATED)

    def _get_checkout_session(self, request, session_id=None):
        """Get checkout session from ID or current user's cart."""
        if session_id:
            try:
                session = CheckoutSession.objects.select_related(
                    'cart', 'shipping_address', 'billing_address', 'payment_provider'
                ).get(id=session_id)
                # Verify ownership
                if request.user.is_authenticated:
                    if session.cart.user != request.user:
                        return None
                return session
            except CheckoutSession.DoesNotExist:
                return None

        # Get from current user's cart
        if request.user.is_authenticated:
            try:
                from cart.models import Cart
                cart = Cart.objects.get(user=request.user)
                return cart.checkout_session
            except (Cart.DoesNotExist, CheckoutSession.DoesNotExist):
                return None

        # Guest checkout - try session key
        session_key = request.session.session_key
        if session_key:
            try:
                from cart.models import Cart
                # Get most recent cart for this session (in case of duplicates from testing)
                cart = Cart.objects.filter(session_key=session_key).order_by('-updated_at').first()
                if cart:
                    return cart.checkout_session
            except (Cart.DoesNotExist, CheckoutSession.DoesNotExist):
                return None

        return None

    def _get_provider_account(self, checkout_session, provider_id=None):
        """Get provider account from ID or session's selected provider."""
        if provider_id:
            try:
                return PaymentProviderAccount.objects.get(
                    id=provider_id,
                    is_active=True
                )
            except PaymentProviderAccount.DoesNotExist:
                return None

        # Use session's selected provider
        if checkout_session.payment_provider:
            return checkout_session.payment_provider

        # Fall back to default provider
        return PaymentProviderAccount.objects.filter(
            is_active=True,
            is_default=True
        ).first()


class PaymentIntentDetailView(HeadlessAPIMixin, APIView):
    """
    Get payment intent status.

    Use this endpoint to poll for payment status after redirecting
    from hosted checkout or after embedded checkout completion.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Get payment intent status"),
        description=_("""
        Get the current status of a payment intent.

        Use this endpoint to:
        - Check payment status after hosted checkout redirect
        - Poll for status during processing
        - Get order details after successful payment

        **Statuses**:
        - `created`: Intent created, awaiting payment method
        - `requires_payment_method`: Needs payment method
        - `requires_action`: Customer action required (3DS)
        - `processing`: Payment is processing
        - `succeeded`: Payment successful
        - `failed`: Payment failed
        - `canceled`: Payment was canceled
        """),
        parameters=[
            OpenApiParameter(
                name='intent_id',
                type=str,
                location=OpenApiParameter.PATH,
                description=_("Payment intent UUID")
            )
        ],
        responses={
            200: OpenApiResponse(
                response=PaymentIntentResponseSerializer,
                description=_("Payment intent details (full handler data for active intents, status-only for terminal states)")
            ),
            404: OpenApiResponse(description=_("Payment intent not found")),
        }
    )
    def get(self, request, intent_id):
        intent = get_object_or_404(
            PaymentIntent.objects.select_related('order', 'provider_account', 'provider_account__component'),
            id=intent_id
        )

        # Verify with provider if not yet terminal (handles delayed/missing webhooks)
        PaymentOrchestrationService.verify_and_sync_payment_status(intent)

        # Return full handler data for active intents (needed for page refresh recovery)
        # Use status-only serializer for terminal states
        if intent.status in ('succeeded', 'failed', 'canceled'):
            serializer = PaymentIntentStatusSerializer(intent)
        else:
            serializer = PaymentIntentResponseSerializer(intent)
        return Response(serializer.data)


class PaymentIntentConfirmView(HeadlessAPIMixin, APIView):
    """
    Confirm a payment intent after customer action (3DS, etc.)
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Confirm payment intent"),
        description=_("""
        Confirm a payment intent after customer completes required action.

        Use this endpoint after:
        - 3DS authentication completes
        - Customer authorizes payment on redirect
        - Any other required customer action

        The confirmation may succeed immediately or require additional actions.
        """),
        request=ConfirmPaymentIntentSerializer,
        responses={
            200: OpenApiResponse(
                response=PaymentIntentStatusSerializer,
                description=_("Confirmation result")
            ),
            400: OpenApiResponse(description=_("Confirmation failed")),
            404: OpenApiResponse(description=_("Payment intent not found")),
        }
    )
    def post(self, request, intent_id):
        intent = get_object_or_404(PaymentIntent, id=intent_id)

        serializer = ConfirmPaymentIntentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        success, message = PaymentOrchestrationService.confirm_payment_intent(
            intent=intent,
            confirmation_data=serializer.validated_data.get('payment_method_data')
        )

        if not success:
            return Response(
                {'success': False, 'message': str(message)},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Refresh intent from database
        intent.refresh_from_db()
        response_data = PaymentIntentStatusSerializer(intent).data
        response_data['success'] = True

        return Response(response_data)


class PaymentIntentCancelView(HeadlessAPIMixin, APIView):
    """
    Cancel a payment intent.

    This will also cancel the associated order and release allocated stock.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Cancel payment intent"),
        description=_("""
        Cancel a payment intent.

        This will:
        - Cancel the payment intent with the provider
        - Cancel the associated order (if no other active intents)
        - Release allocated stock

        **Note**: Cannot cancel intents in terminal states (succeeded, failed, canceled).
        """),
        request=CancelPaymentIntentSerializer,
        responses={
            200: OpenApiResponse(description=_("Payment canceled successfully")),
            400: OpenApiResponse(description=_("Cannot cancel this payment")),
            404: OpenApiResponse(description=_("Payment intent not found")),
        }
    )
    def post(self, request, intent_id):
        intent = get_object_or_404(PaymentIntent, id=intent_id)

        success, message = PaymentOrchestrationService.cancel_payment_intent(intent)

        if not success:
            return Response(
                {'success': False, 'message': str(message)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'success': True, 'message': str(message)})


class SavedMethodListCreateView(HeadlessAPIMixin, APIView):
    """
    List and create saved payment methods.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("List saved payment methods"),
        description=_("List all saved payment methods for the authenticated user."),
        responses={
            200: OpenApiResponse(
                response=SavedPaymentMethodSerializer(many=True),
                description=_("List of saved payment methods")
            ),
        }
    )
    def get(self, request):
        from subscriptions.models import PaymentToken

        tokens = PaymentToken.objects.filter(
            user=request.user
        ).select_related('provider_account').order_by('-is_default', '-created_at')

        serializer = SavedPaymentMethodSerializer(tokens, many=True)
        return Response(serializer.data)

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Save a new payment method"),
        description=_("""
        Save a new payment method for future use.

        The payment_method_token should be obtained from the provider's SDK
        after collecting card details on the client side.
        """),
        request=CreateSavedPaymentMethodSerializer,
        responses={
            201: OpenApiResponse(
                response=SavedPaymentMethodSerializer,
                description=_("Payment method saved successfully")
            ),
            400: OpenApiResponse(description=_("Invalid request")),
        }
    )
    def post(self, request):
        serializer = CreateSavedPaymentMethodSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'success': False, 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        # Get provider account
        try:
            provider_account = PaymentProviderAccount.objects.get(
                id=data['provider_id'],
                is_active=True
            )
        except PaymentProviderAccount.DoesNotExist:
            return Response(
                {'success': False, 'message': _("Payment provider not found")},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save payment method via provider
        try:
            provider = provider_account.get_provider_instance()

            if not hasattr(provider, 'save_payment_method'):
                return Response(
                    {'success': False, 'message': _("Provider does not support saved payment methods")},
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = provider.save_payment_method(
                token=data['payment_method_token'],
                customer_email=request.user.email
            )

            if not result.get('success'):
                return Response(
                    {'success': False, 'message': result.get('message', 'Failed to save payment method')},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create PaymentToken record
            from subscriptions.models import PaymentToken

            # Unset default if setting this as default
            if data.get('set_as_default'):
                PaymentToken.objects.filter(user=request.user, is_default=True).update(is_default=False)

            token = PaymentToken.objects.create(
                user=request.user,
                provider_account=provider_account,
                token_id=result.get('token_id'),
                payment_method_type=result.get('payment_method_type', 'card'),
                last_four=result.get('last_four', ''),
                brand=result.get('brand', ''),
                exp_month=result.get('exp_month'),
                exp_year=result.get('exp_year'),
                is_default=data.get('set_as_default', False)
            )

            response_serializer = SavedPaymentMethodSerializer(token)
            return Response(
                {'success': True, **response_serializer.data},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error(f"Error saving payment method: {e}")
            return Response(
                {'success': False, 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class SavedMethodDetailView(HeadlessAPIMixin, APIView):
    """
    Get or delete a saved payment method.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Get saved payment method details"),
        responses={
            200: OpenApiResponse(
                response=SavedPaymentMethodSerializer,
                description=_("Payment method details")
            ),
            404: OpenApiResponse(description=_("Payment method not found")),
        }
    )
    def get(self, request, method_id):
        from subscriptions.models import PaymentToken

        token = get_object_or_404(
            PaymentToken.objects.select_related('provider_account'),
            token_id=method_id,
            user=request.user
        )

        serializer = SavedPaymentMethodSerializer(token)
        return Response(serializer.data)

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Delete saved payment method"),
        responses={
            200: OpenApiResponse(description=_("Payment method deleted")),
            404: OpenApiResponse(description=_("Payment method not found")),
        }
    )
    def delete(self, request, method_id):
        from subscriptions.models import PaymentToken

        token = get_object_or_404(
            PaymentToken,
            token_id=method_id,
            user=request.user
        )

        # Try to delete from provider
        try:
            provider = token.provider_account.get_provider_instance()
            if hasattr(provider, 'delete_payment_method'):
                provider.delete_payment_method(token.token_id)
        except Exception as e:
            logger.warning(f"Failed to delete payment method from provider: {e}")

        token.delete()
        return Response({'success': True, 'message': _("Payment method deleted")})


class SetDefaultMethodView(HeadlessAPIMixin, APIView):
    """
    Set a saved payment method as default.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Set default payment method"),
        responses={
            200: OpenApiResponse(description=_("Default payment method updated")),
            404: OpenApiResponse(description=_("Payment method not found")),
        }
    )
    def post(self, request, method_id):
        from subscriptions.models import PaymentToken

        token = get_object_or_404(
            PaymentToken,
            token_id=method_id,
            user=request.user
        )

        # Unset current default
        PaymentToken.objects.filter(user=request.user, is_default=True).update(is_default=False)

        # Set new default
        token.is_default = True
        token.save(update_fields=['is_default'])

        return Response({'success': True, 'message': _("Default payment method updated")})


class PaymentSDKFailureReportView(HeadlessAPIMixin, APIView):
    """
    Report a payment SDK loading failure from the frontend.
    Used to notify merchants when a payment provider has issues.
    """
    permission_classes = [AllowAny]  # Must work for guest checkout

    @extend_schema(
        tags=['Payment Methods'],
        summary=_("Report payment SDK failure"),
        description=_("""
Report a payment SDK loading failure. Used by the checkout frontend
to notify the merchant when a payment provider's SDK fails to load.

Notifications are rate-limited to 1 per provider per hour to prevent
flooding the merchant's inbox.

**Authentication:** Not required (supports guest checkout).
        """),
        responses={
            200: OpenApiResponse(description=_("Failure reported")),
        }
    )
    def post(self, request):
        provider_key = request.data.get('provider_key', 'unknown')
        error_type = request.data.get('error_type', 'sdk_load_failure')

        # Rate-limit check using Django cache
        from django.core.cache import cache
        cache_key = f'payment_sdk_failure:{provider_key}'
        failure_count = cache.get(cache_key, 0)

        # Increment failure count (track for 1 hour)
        cache.set(cache_key, failure_count + 1, 3600)

        # Only send notification on first failure per provider per hour
        if failure_count == 0:
            from payment_providers.tasks import notify_merchant_sdk_failure
            notify_merchant_sdk_failure.delay(
                provider_key=provider_key,
                error_type=error_type,
                page_url=request.data.get('page_url', ''),
                user_agent=request.data.get('user_agent', ''),
            )

        return Response({
            'success': True,
            'message': 'Failure reported',
        })
