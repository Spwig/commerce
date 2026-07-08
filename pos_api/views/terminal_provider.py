"""
POS Terminal Provider API views.

Handles terminal SDK operations: connection tokens, reader listing,
PaymentIntent creation, capture, and cancellation.
All endpoints require staff authentication and valid POS license.
"""
import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from admin_api.authentication import MobileTokenAuthentication
from pos_api.permissions import IsStaffUser
from core.api.api_descriptions import INVALID_AUTH_TOKEN, PERMISSION_DENIED
from pos_api.serializers.terminal_provider import (
    CreatePaymentIntentSerializer,
    CapturePaymentSerializer,
    CancelPaymentSerializer,
    InitiateCloudPaymentSerializer,
    CancelCloudPaymentSerializer,
    CloudPaymentInitiatedSerializer,
    CloudPaymentStatusSerializer,
    ProviderConfigResponseSerializer,
    ReaderListResponseSerializer,
    ErrorResponseSerializer,
    SuccessResponseSerializer,
    ConnectionTokenResponseSerializer,
    PaymentIntentResponseSerializer,
)
from pos_api.views.utils import get_terminal

logger = logging.getLogger(__name__)


def _get_provider_instance(terminal):
    """
    Get the active terminal provider instance for the given terminal.

    Looks for a POSTerminalReader assigned to this terminal,
    then returns the provider instance from its POSTerminalProvider.
    Falls back to 'manual' if no reader is assigned.
    """
    from pos_app.models import POSTerminalProvider

    # Check if terminal has an assigned card reader
    reader = getattr(terminal, 'card_reader', None)
    if reader and reader.provider and reader.provider.is_active:
        return reader.provider.get_provider_instance(), reader.provider

    # Fall back to active provider (prefer non-manual)
    provider_account = (
        POSTerminalProvider.objects.filter(is_active=True)
        .exclude(provider_key='manual')
        .first()
    )
    if provider_account:
        return provider_account.get_provider_instance(), provider_account

    return None, None


@extend_schema(
    summary=_("Get terminal provider config"),
    description=_(
        "Returns the terminal provider configuration for the current terminal, "
        "including the integration mode (sdk, cloud, or manual) and connected reader details. "
        "Used by the POS frontend on startup to determine if an integrated card "
        "reader is available and which payment flow to use."
    ),
    responses={
        200: ProviderConfigResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        403: OpenApiResponse(description=PERMISSION_DENIED),
    },
    tags=['POS - Terminal'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def provider_config(request):
    """Return terminal provider configuration for the current terminal."""
    terminal, err = get_terminal(request)
    if err:
        return err

    reader = getattr(terminal, 'card_reader', None)
    if reader and reader.provider and reader.provider.is_active:
        provider_account = reader.provider
        try:
            provider_instance = provider_account.get_provider_instance()
            integration_mode = provider_instance.integration_mode
        except Exception:
            integration_mode = 'sdk'
        return Response({
            'success': True,
            'provider_key': provider_account.provider_key,
            'provider_name': provider_account.display_name or provider_account.provider_key,
            'integration_mode': integration_mode,
            'has_reader': True,
            'reader': {
                'id': str(reader.id),
                'provider_reader_id': reader.provider_reader_id,
                'label': reader.reader_label,
                'type': reader.reader_type,
                'status': reader.status,
            },
        })

    return Response({
        'success': True,
        'provider_key': 'manual',
        'provider_name': 'Manual Entry',
        'integration_mode': 'manual',
        'has_reader': False,
        'reader': None,
    })


@extend_schema(
    summary=_("Create connection token"),
    description=_(
        "Creates a short-lived connection token for SDK-mode terminal providers "
        "(e.g. Stripe Terminal JS SDK). The frontend calls this endpoint when "
        "initializing the SDK to establish a direct connection with the reader. "
        "SDK only. Cloud providers do not use connection tokens. "
        "Returns 400 if the provider does not support SDK tokens."
    ),
    responses={
        200: ConnectionTokenResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        404: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def connection_token(request):
    """Create a connection token for the terminal SDK."""
    terminal, err = get_terminal(request)
    if err:
        return err

    provider_instance, provider_account = _get_provider_instance(terminal)
    if not provider_instance:
        return Response(
            {
                'success': False,
                'error': {
                    'code': 'NO_PROVIDER',
                    'message': 'No terminal payment provider configured.',
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        result = provider_instance.create_connection_token()
        if result.get('success'):
            return Response({'success': True, 'secret': result['secret']})
        return Response(
            {'success': False, 'error': {'code': 'TOKEN_FAILED', 'message': result.get('message', 'Unknown error')}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except NotImplementedError:
        return Response(
            {'success': False, 'error': {'code': 'NOT_SUPPORTED', 'message': 'Provider does not support SDK tokens.'}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.error(f"Connection token error: {e}")
        return Response(
            {'success': False, 'error': {'code': 'TOKEN_ERROR', 'message': str(e)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    summary=_("List card readers"),
    description=_(
        "List available card readers from the terminal provider. Works for both "
        "SDK-mode and cloud-mode providers. "
        "Each reader object contains: id, label, type, serial_number, and status."
    ),
    responses={
        200: ReaderListResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        500: ErrorResponseSerializer,
    },
    tags=['POS - Terminal'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def list_readers(request):
    """List card readers from the terminal provider."""
    terminal, err = get_terminal(request)
    if err:
        return err

    provider_instance, provider_account = _get_provider_instance(terminal)
    if not provider_instance:
        return Response({'success': True, 'readers': []})

    try:
        result = provider_instance.list_readers()
        return Response(result)
    except Exception as e:
        logger.error(f"List readers error: {e}")
        return Response(
            {'success': False, 'error': {'code': 'READER_ERROR', 'message': str(e)}, 'readers': []},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    summary=_("Create payment intent for terminal"),
    description=_(
        "Creates a PaymentIntent for card_present collection on the terminal reader. "
        "The frontend uses the returned client_secret to collect payment via the SDK. "
        "SDK only. Cloud providers should use initiate-cloud-payment. "
        "If currency is omitted, defaults to the terminal's configured currency."
    ),
    request=CreatePaymentIntentSerializer,
    responses={
        200: PaymentIntentResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        404: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def create_payment_intent(request):
    """Create a PaymentIntent for terminal card collection."""
    terminal, err = get_terminal(request)
    if err:
        return err

    serializer = CreatePaymentIntentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data['amount']
    currency = serializer.validated_data.get('currency') or terminal.effective_currency

    provider_instance, provider_account = _get_provider_instance(terminal)
    if not provider_instance:
        return Response(
            {'success': False, 'error': {'code': 'NO_PROVIDER', 'message': 'No terminal provider configured.'}},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        result = provider_instance.create_payment_intent(
            amount=amount,
            currency=currency,
            metadata={
                'terminal_uuid': str(terminal.uuid),
                'terminal_name': terminal.name,
                'cashier': request.user.get_full_name() or request.user.username,
            },
        )
        if result.get('success'):
            return Response(result)

        # Return structured error from provider
        error_code = result.get('error_code', 'INTENT_FAILED')
        error_response = {
            'success': False,
            'error': {
                'code': error_code,
                'message': result.get('message', 'Unknown error'),
            },
        }
        # Include currency in error for CURRENCY_NOT_SUPPORTED
        if error_code == 'CURRENCY_NOT_SUPPORTED' and result.get('currency'):
            error_response['error']['currency'] = result['currency']

        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Create payment intent error: {e}")
        return Response(
            {'success': False, 'error': {'code': 'INTENT_ERROR', 'message': str(e)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    summary=_("Capture/verify terminal payment"),
    description=_(
        "Verifies that a PaymentIntent was successfully processed on the terminal "
        "reader and returns card details (brand, last4) from the provider. "
        "SDK only."
    ),
    request=CapturePaymentSerializer,
    responses={
        200: SuccessResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        404: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def capture_payment(request):
    """Verify/capture a terminal payment."""
    terminal, err = get_terminal(request)
    if err:
        return err

    serializer = CapturePaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    payment_intent_id = serializer.validated_data['payment_intent_id']

    provider_instance, provider_account = _get_provider_instance(terminal)
    if not provider_instance:
        return Response(
            {'success': False, 'error': {'code': 'NO_PROVIDER', 'message': 'No terminal provider configured.'}},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        result = provider_instance.capture_payment_intent(payment_intent_id)
        return Response(result)
    except Exception as e:
        logger.error(f"Capture payment error: {e}")
        return Response(
            {'success': False, 'error': {'code': 'CAPTURE_ERROR', 'message': str(e)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    summary=_("Cancel terminal payment"),
    description=_(
        "Cancel a pending PaymentIntent on the terminal reader (e.g. customer cancelled). "
        "SDK only. Cloud providers should use cancel-cloud-payment."
    ),
    request=CancelPaymentSerializer,
    responses={
        200: SuccessResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        404: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def cancel_payment(request):
    """Cancel a pending terminal payment."""
    terminal, err = get_terminal(request)
    if err:
        return err

    serializer = CancelPaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    payment_intent_id = serializer.validated_data['payment_intent_id']

    provider_instance, provider_account = _get_provider_instance(terminal)
    if not provider_instance:
        return Response(
            {'success': False, 'error': {'code': 'NO_PROVIDER', 'message': 'No terminal provider configured.'}},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        result = provider_instance.cancel_payment_intent(payment_intent_id)
        return Response(result)
    except Exception as e:
        logger.error(f"Cancel payment error: {e}")
        return Response(
            {'success': False, 'error': {'code': 'CANCEL_ERROR', 'message': str(e)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ── Cloud Payment Endpoints ──────────────────────────────────────────────


@extend_schema(
    summary=_("Initiate cloud payment on reader"),
    description=_(
        "Sends a payment request to a card reader via the provider's cloud API. "
        "For cloud-mode terminal providers only (Adyen, Square, SumUp, Zettle). "
        "Cloud only. Returns 400 if provider uses SDK mode. "
        "If currency is omitted, defaults to the terminal's configured currency."
    ),
    request=InitiateCloudPaymentSerializer,
    responses={
        200: CloudPaymentInitiatedSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        404: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def initiate_cloud_payment(request):
    """Initiate a payment on a reader via cloud API."""
    terminal, err = get_terminal(request)
    if err:
        return err

    serializer = InitiateCloudPaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    amount = serializer.validated_data['amount']
    currency = serializer.validated_data.get('currency') or terminal.effective_currency
    reader_id = serializer.validated_data['reader_id']

    provider_instance, provider_account = _get_provider_instance(terminal)
    if not provider_instance:
        return Response(
            {'success': False, 'error': {'code': 'NO_PROVIDER', 'message': 'No terminal provider configured.'}},
            status=status.HTTP_404_NOT_FOUND,
        )

    if provider_instance.integration_mode != 'cloud':
        return Response(
            {'success': False, 'error': {'code': 'WRONG_MODE', 'message': 'This provider uses SDK mode, not cloud mode.'}},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        result = provider_instance.initiate_cloud_payment(
            amount=amount,
            currency=currency,
            reader_id=reader_id,
            metadata={
                'terminal_uuid': str(terminal.uuid),
                'terminal_name': terminal.name,
                'cashier': request.user.get_full_name() or request.user.username,
            },
        )
        if result.get('success'):
            return Response(result)

        return Response(
            {'success': False, 'error': {'code': result.get('error_code', 'CLOUD_PAYMENT_FAILED'), 'message': result.get('message', 'Unknown error')}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except NotImplementedError:
        return Response(
            {'success': False, 'error': {'code': 'NOT_SUPPORTED', 'message': 'Provider does not support cloud payments.'}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.error(f"Initiate cloud payment error: {e}")
        return Response(
            {'success': False, 'error': {'code': 'CLOUD_PAYMENT_ERROR', 'message': str(e)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    summary=_("Check cloud payment status"),
    description=_(
        "Poll the status of a cloud-initiated payment. Returns the current "
        "status: pending, succeeded, failed, or canceled. "
        "When status is 'succeeded', the response includes card_brand, last4, "
        "and the provider payment_id. When 'canceled', includes cancel_reason. "
        "Frontend should poll every 2 seconds until status is no longer 'pending'."
    ),
    parameters=[
        OpenApiParameter(
            name='transaction_id',
            type=str,
            location=OpenApiParameter.PATH,
            description=_('Provider-specific transaction ID returned by initiate-cloud-payment'),
            required=True,
        ),
    ],
    responses={
        200: CloudPaymentStatusSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        404: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    tags=['POS - Terminal'],
)
@api_view(['GET'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def check_payment_status(request, transaction_id):
    """Check the status of a cloud-initiated payment."""
    terminal, err = get_terminal(request)
    if err:
        return err

    provider_instance, provider_account = _get_provider_instance(terminal)
    if not provider_instance:
        return Response(
            {'success': False, 'error': {'code': 'NO_PROVIDER', 'message': 'No terminal provider configured.'}},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        result = provider_instance.check_payment_status(transaction_id)
        return Response(result)
    except NotImplementedError:
        return Response(
            {'success': False, 'error': {'code': 'NOT_SUPPORTED', 'message': 'Provider does not support payment status checks.'}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.error(f"Check payment status error: {e}")
        return Response(
            {'success': False, 'error': {'code': 'STATUS_ERROR', 'message': str(e)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    summary=_("Cancel cloud payment"),
    description=_(
        "Cancel a pending cloud-initiated payment on the reader. "
        "Cloud only. Behavior varies by provider."
    ),
    request=CancelCloudPaymentSerializer,
    responses={
        200: SuccessResponseSerializer,
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=INVALID_AUTH_TOKEN),
        404: ErrorResponseSerializer,
        500: ErrorResponseSerializer,
    },
    tags=['POS - Terminal'],
)
@api_view(['POST'])
@authentication_classes([MobileTokenAuthentication])
@permission_classes([IsStaffUser])
def cancel_cloud_payment(request):
    """Cancel a pending cloud payment."""
    terminal, err = get_terminal(request)
    if err:
        return err

    serializer = CancelCloudPaymentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    transaction_id = serializer.validated_data['transaction_id']

    provider_instance, provider_account = _get_provider_instance(terminal)
    if not provider_instance:
        return Response(
            {'success': False, 'error': {'code': 'NO_PROVIDER', 'message': 'No terminal provider configured.'}},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        result = provider_instance.cancel_cloud_payment(transaction_id)
        return Response(result)
    except NotImplementedError:
        return Response(
            {'success': False, 'error': {'code': 'NOT_SUPPORTED', 'message': 'Provider does not support cloud payment cancellation.'}},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.error(f"Cancel cloud payment error: {e}")
        return Response(
            {'success': False, 'error': {'code': 'CANCEL_ERROR', 'message': str(e)}},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
