"""
License Checkout API Views

Endpoints for the license purchase flow on spwig.com:
1. GET  /api/license-checkout/catalog/                         — Public product catalog
2. POST /api/license-checkout/trial/                           — Start free trial
3. POST /api/license-checkout/checkout/                        — Initiate paid checkout
4. GET  /api/license-checkout/status/<uuid:intent>/            — Check payment status
5. GET  /api/license-checkout/renew-info/<str:license_key>/    — Get renewal pricing
6. POST /api/license-checkout/renew/                           — Initiate renewal checkout

Hosted subscription endpoints:
7. GET  /api/license-checkout/hosted-catalog/                  — Hosted plan catalog
8. GET  /api/license-checkout/check-store-name/                — Store slug availability
9. POST /api/license-checkout/hosted-checkout/                 — Initiate hosted checkout
10. GET /api/license-checkout/hosted-status/<uuid:checkout_id>/ — Hosted checkout status
"""

import logging
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.utils import timezone

from rest_framework import status, serializers as drf_serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer

from core.api.throttling import (
    HostingWebhookThrottle, MarketplaceCheckoutThrottle, MarketplaceStatusThrottle,
)

from .models import (
    LicenseProduct, LicenseCheckoutRequest,
    HostedPlan, HostedCheckoutRequest, HostedSubscription,
)
from .services import provision_trial_license, get_renewal_info

logger = logging.getLogger(__name__)
User = get_user_model()


_ALLOWED_RETURN_DOMAINS = frozenset({
    'spwig.com', 'www.spwig.com',
    'myspwig.com', 'www.myspwig.com',
    'localhost', '127.0.0.1',
})


def _safe_return_base(raw_url, default='https://spwig.com'):
    """Extract origin + optional locale prefix from a return_base_url.

    Prevents path doubling (e.g. /purchase/return/purchase/return/) when
    the frontend sends the full current page URL as return_base_url.
    Validates against an allowlist to prevent open redirects.
    """
    from urllib.parse import urlparse
    from django.conf import settings

    url = (raw_url or '').strip().rstrip('/')
    if not url:
        return default
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return default

    # Strip port for domain comparison (e.g. localhost:8000 → localhost)
    hostname = parsed.netloc.split(':')[0].lower()
    if hostname not in _ALLOWED_RETURN_DOMAINS:
        logger.warning('Rejected return_base_url with unknown domain: %s', hostname)
        return default

    base = f"{parsed.scheme}://{parsed.netloc}"
    # Preserve first path segment if it's a known locale code
    # (e.g. /en, /de, /zh-hans, /zh-hant)
    path_parts = [p for p in parsed.path.split('/') if p]
    if path_parts:
        locale_codes = {code for code, _ in settings.LANGUAGES}
        if path_parts[0] in locale_codes:
            base += f"/{path_parts[0]}"
    return base


def _mask_email(email):
    """Mask email for safe logging."""
    if '@' not in email:
        return '***'
    local, domain = email.split('@', 1)
    masked_local = local[:2] + '***' if len(local) > 2 else '***'
    return f"{masked_local}@{domain}"


class LicenseCatalogView(APIView):
    """
    Return the public license product catalog with pricing.

    Used by the spwig.com frontend to display product cards with
    dynamic pricing from the backend.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['License Checkout'],
        summary=_("Get license product catalog"),
        description=_("Returns all active license products with pricing. "
                    "Used by spwig.com to display product cards. HQ only."),
        responses={
            200: inline_serializer(
                name='LicenseCatalogResponse',
                fields={
                    'products': drf_serializers.ListField(
                        child=drf_serializers.DictField()
                    ),
                },
            ),
        },
    )
    def get(self, request):
        products = LicenseProduct.objects.filter(
            is_active=True,
        ).exclude(
            slug='maintenance-renewal',  # Renewal has dynamic pricing, not shown in catalog
        ).order_by('sort_order')

        data = []
        for p in products:
            data.append({
                'slug': p.slug,
                'name': p.name,
                'product_type': p.product_type,
                'price': str(p.price.amount),
                'price_currency': str(p.price.currency),
                'regular_price': str(p.regular_price.amount),
                'features': p.features,
                'savings_amount': str(p.savings_amount.amount) if p.savings_amount else None,
                'includes_pos': p.includes_pos,
                'trial_days': p.trial_days,
                'is_featured': p.is_featured,
                'note': p.note,
                'note_link': p.note_link,
            })

        return Response({'products': data})


class StartTrialView(APIView):
    """
    Start a free 30-day trial — provisions a license and setup token
    on the upgrade server without requiring payment.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceCheckoutThrottle]

    @extend_schema(
        tags=['License Checkout'],
        summary=_("Start free trial"),
        description=_("Provision a free trial license and setup token. "
                    "One trial per email address. HQ only."),
        request=inline_serializer(
            name='StartTrialRequest',
            fields={
                'email': drf_serializers.EmailField(),
                'name': drf_serializers.CharField(required=False),
            },
        ),
        responses={
            201: inline_serializer(
                name='StartTrialResponse',
                fields={
                    'success': drf_serializers.BooleanField(),
                    'message': drf_serializers.CharField(),
                },
            ),
            400: OpenApiResponse(description=_("Invalid email or trial already used")),
            502: OpenApiResponse(description=_("Upgrade server unreachable")),
        },
    )
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        name = request.data.get('name', '').strip()
        language = request.data.get('language', '').strip() or 'en'

        if not email:
            return Response(
                {'success': False, 'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_email(email)
        except DjangoValidationError:
            return Response(
                {'success': False, 'error': 'Invalid email address'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if this email already has an active trial
        existing_trial = LicenseCheckoutRequest.objects.filter(
            email__iexact=email,
            license_product__product_type=LicenseProduct.ProductType.TRIAL,
            status=LicenseCheckoutRequest.Status.COMPLETED,
        ).exists()

        if existing_trial:
            return Response(
                {'success': False, 'error': 'A trial has already been activated for this email address'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find the trial product
        trial_product = LicenseProduct.objects.filter(
            product_type=LicenseProduct.ProductType.TRIAL,
            is_active=True,
        ).first()

        if not trial_product:
            return Response(
                {'success': False, 'error': 'Trial product is not available'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create checkout request
        checkout_request = LicenseCheckoutRequest.objects.create(
            license_product=trial_product,
            email=email,
            name=name,
            user=request.user if request.user and request.user.is_authenticated else None,
            status=LicenseCheckoutRequest.Status.PROVISIONING,
            metadata={'language': language},
        )

        # Provision the trial
        try:
            provision_trial_license(checkout_request)
        except ValueError as e:
            logger.warning(f"Trial provisioning ValueError for {_mask_email(email)}: {e}")
            checkout_request.status = LicenseCheckoutRequest.Status.FAILED
            checkout_request.error_message = str(e)[:500]
            checkout_request.save(update_fields=['status', 'error_message'])
            return Response(
                {'success': False, 'error': 'Unable to activate trial. Please try again later.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Trial provisioning failed for {_mask_email(email)}: {e}")
            checkout_request.status = LicenseCheckoutRequest.Status.FAILED
            checkout_request.error_message = str(e)[:500]
            checkout_request.save(update_fields=['status', 'error_message'])
            return Response(
                {'success': False, 'error': 'Unable to activate trial. Please try again later.'},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            {'success': True, 'message': 'Trial activated — check your email for setup instructions'},
            status=status.HTTP_201_CREATED,
        )


class InitiateCheckoutView(APIView):
    """
    Initiate a paid license checkout.

    Creates a user (if needed), cart, checkout session, and payment intent
    for a license purchase. Returns embedded payment configuration
    (handler_config + client_secret) for the Airwallex SDK.

    Idempotent: if a valid checkout session already exists for the same
    email + product, returns the existing payment configuration.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceCheckoutThrottle]

    @extend_schema(
        tags=['License Checkout'],
        summary=_("Initiate license checkout"),
        description=_("Create a paid checkout for a license product. Returns embedded payment "
                    "configuration for Airwallex SDK. Idempotent for same email+product. HQ only."),
        request=inline_serializer(
            name='LicenseCheckoutRequest',
            fields={
                'product_slug': drf_serializers.SlugField(),
                'email': drf_serializers.EmailField(),
                'name': drf_serializers.CharField(required=False),
                'billing_country': drf_serializers.CharField(required=False),
                'return_base_url': drf_serializers.URLField(required=False),
            },
        ),
        responses={
            200: OpenApiResponse(description=_("Existing active checkout returned (idempotent)")),
            201: inline_serializer(
                name='LicenseCheckoutResponse',
                fields={
                    'success': drf_serializers.BooleanField(),
                    'checkout_url': drf_serializers.URLField(),
                    'payment_intent_id': drf_serializers.UUIDField(),
                    'order_number': drf_serializers.CharField(allow_null=True),
                },
            ),
            400: OpenApiResponse(description=_("Invalid input or product not found")),
            500: OpenApiResponse(description=_("No payment provider configured")),
        },
    )
    @transaction.atomic
    def post(self, request):
        product_slug = request.data.get('product_slug', '').strip()
        email = request.data.get('email', '').strip().lower()
        name = request.data.get('name', '').strip()
        company = request.data.get('company', '').strip()
        billing_country = request.data.get('billing_country', '').strip()
        billing_address = request.data.get('billing_address', '').strip()
        billing_city = request.data.get('billing_city', '').strip()
        billing_state = request.data.get('billing_state', '').strip()
        billing_postal_code = request.data.get('billing_postal_code', '').strip()
        language = request.data.get('language', '').strip() or 'en'

        # Validate required fields
        if not product_slug:
            return Response(
                {'success': False, 'error': 'Please select a product'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not email:
            return Response(
                {'success': False, 'error': 'Email address is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not name:
            return Response(
                {'success': False, 'error': 'Full name is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not billing_country:
            return Response(
                {'success': False, 'error': 'Billing country is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not billing_address:
            return Response(
                {'success': False, 'error': 'Billing address is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not billing_city:
            return Response(
                {'success': False, 'error': 'City is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not billing_postal_code:
            return Response(
                {'success': False, 'error': 'Postal code is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_email(email)
        except DjangoValidationError:
            return Response(
                {'success': False, 'error': 'Invalid email address'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find the license product
        try:
            license_product = LicenseProduct.objects.get(
                slug=product_slug,
                is_active=True,
                product_type__in=[
                    LicenseProduct.ProductType.LICENSE,
                    LicenseProduct.ProductType.BUNDLE,
                ],
            )
        except LicenseProduct.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Product not found'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Idempotency: check for existing active checkout
        from cart.models import CheckoutSession
        from payment_providers.models import PaymentIntent

        existing_request = LicenseCheckoutRequest.objects.filter(
            email__iexact=email,
            license_product=license_product,
            status=LicenseCheckoutRequest.Status.PENDING,
            created_at__gte=timezone.now() - timedelta(hours=2),
        ).first()

        if existing_request and existing_request.payment_intent:
            intent = existing_request.payment_intent
            # Only reuse intents that are freshly created (< 5 min old) and not yet
            # acted upon. Once a user enters card details, the provider-side intent
            # is consumed even if our DB never updated (e.g. due to webhook failure).
            intent_age = timezone.now() - intent.created_at
            reusable_statuses = ['created', 'requires_payment_method']
            is_fresh = intent_age.total_seconds() < 300  # 5 minutes
            if intent.status in reusable_statuses or (intent.status == 'requires_action' and is_fresh):
                if intent.client_secret or intent.checkout_url:
                    from payment_providers.api_serializers import PaymentIntentResponseSerializer
                    serialized = PaymentIntentResponseSerializer(intent).data
                    return Response({
                        'success': True,
                        'checkout_url': intent.checkout_url or '',
                        'payment_intent_id': str(intent.id),
                        'order_number': intent.order.order_number if intent.order else None,
                        'client_secret': intent.client_secret,
                        'handler_config': serialized.get('handler_config'),
                        'sdk_dependencies': serialized.get('sdk_dependencies', []),
                    }, status=status.HTTP_200_OK)

        # Create checkout request
        checkout_request = LicenseCheckoutRequest.objects.create(
            license_product=license_product,
            email=email,
            name=name,
            company=company,
            billing_country=billing_country,
            user=request.user if request.user and request.user.is_authenticated else None,
            status=LicenseCheckoutRequest.Status.PENDING,
            metadata={'language': language},
        )

        # Find or create user — reuse existing registered user, or create guest
        from accounts.services.account_creation_service import AccountCreationService

        # Check for existing registered (non-guest) user first
        user = User.objects.filter(
            email__iexact=email
        ).exclude(username__startswith='guest_').first()

        if user:
            logger.info(f"Reusing existing user for license checkout: {_mask_email(email)}")
        else:
            # Create proper guest user (handles dedup, sets guest_ prefix, unusable password)
            user = AccountCreationService.create_guest_user(
                email=email,
                first_name=name.split(' ')[0] if name else '',
                last_name=' '.join(name.split(' ')[1:]) if name and ' ' in name else '',
            )
            logger.info(f"Created guest user for license checkout: {_mask_email(email)}")

        # Find or create digital Product in catalog
        from catalog.models import Product, Category
        from djmoney.money import Money

        license_category, _ = Category.objects.get_or_create(
            slug='licenses',
            defaults={'name': 'Licenses'},
        )

        product_sku = f'lic-{license_product.slug}'
        product, _ = Product.objects.get_or_create(
            sku=product_sku,
            defaults={
                'name': license_product.name,
                'slug': f'license-{license_product.slug}',
                'product_type': 'digital',
                'price': license_product.price,
                'status': 'published',
                'track_inventory': False,
                'category': license_category,
            }
        )
        # Update price if changed in LicenseProduct
        if product.price != license_product.price:
            product.price = license_product.price
            product.save(update_fields=['price', 'price_currency'])

        # Create cart with product
        from cart.models import Cart
        from cart.services.cart_service import CartService

        cart = Cart.objects.create(user=user)
        success, msg, cart_item = CartService.add_item(
            cart=cart, product_id=product.id, quantity=1,
        )
        if not success:
            logger.error(f"Cart add_item failed for lic-{license_product.slug}: {msg}")
            return Response(
                {'success': False, 'error': 'Unable to process your order. Please try again.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create checkout session with license metadata and billing address
        session = CheckoutSession.objects.create(
            cart=cart,
            subtotal=product.price,
            total_amount=product.price,
            step_completed='payment',
            billing_same_as_shipping=False,
            billing_address_data={
                'name': name,
                'address1': billing_address,
                'city': billing_city,
                'state': billing_state,
                'postal_code': billing_postal_code,
                'country': billing_country,
            },
            metadata={
                'license_checkout': True,
                'license_product_slug': license_product.slug,
                'license_checkout_request_id': str(checkout_request.id),
                'includes_pos': license_product.includes_pos,
                'language': language,
            },
            expires_at=timezone.now() + timedelta(hours=2),
        )

        # Select payment provider
        from payment_providers.models import PaymentProviderAccount

        provider_account = PaymentProviderAccount.objects.filter(
            is_active=True,
            connection_status='connected',
        ).first()

        if not provider_account:
            logger.error("License checkout: no active payment provider account configured")
            return Response(
                {'success': False, 'error': 'Payment processing is temporarily unavailable. Please try again later.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        session.payment_provider = provider_account
        session.save(update_fields=['payment_provider'])

        # Create Airwallex customer for recurring billing (maintenance subscriptions).
        # Only for products that require maintenance (not trials or dev licenses).
        intent_metadata = {
            'license_checkout': True,
            'license_product_slug': license_product.slug,
            'license_checkout_request_id': str(checkout_request.id),
        }

        needs_subscription = license_product.slug not in ('trial-core-pos', 'dev-license')
        if needs_subscription:
            try:
                from subscriptions.provider_base import get_provider as get_subscription_provider
                sub_provider = get_subscription_provider(provider_account)
                customer_result = sub_provider.create_customer(user, email)
                airwallex_customer_id = customer_result.get('customer_id', '')
                if airwallex_customer_id:
                    checkout_request.metadata['airwallex_customer_id'] = airwallex_customer_id
                    checkout_request.save(update_fields=['metadata'])
                    intent_metadata['airwallex_customer_id'] = airwallex_customer_id
                    logger.info(f"Created Airwallex customer {airwallex_customer_id} for {_mask_email(email)}")
            except Exception as e:
                logger.warning(
                    f"Failed to create Airwallex customer for {_mask_email(email)}: {e}. "
                    f"Subscription setup will be skipped."
                )

        # Create payment intent
        from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService

        frontend_base = _safe_return_base(request.data.get('return_base_url', ''))

        # Include checkout_request.id in return URL so the frontend can find
        # the payment intent even if sessionStorage is lost (e.g. cross-device)
        payment_return_url = f"{frontend_base}/purchase/return/?checkout_id={checkout_request.id}"
        payment_cancel_url = f"{frontend_base}/purchase/?cancelled=true"

        pi_success, intent, message = PaymentOrchestrationService.create_payment_intent(
            checkout_session=session,
            provider_account=provider_account,
            return_url=payment_return_url,
            cancel_url=payment_cancel_url,
            metadata=intent_metadata,
        )

        if not pi_success:
            logger.error(f"Payment intent creation failed for {_mask_email(email)}: {message}")
            return Response(
                {'success': False, 'error': 'Unable to initiate payment. Please try again later.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Link payment intent to checkout request
        checkout_request.payment_intent = intent
        checkout_request.save(update_fields=['payment_intent'])

        from payment_providers.api_serializers import PaymentIntentResponseSerializer
        serialized = PaymentIntentResponseSerializer(intent).data

        return Response({
            'success': True,
            'checkout_url': intent.checkout_url or '',
            'payment_intent_id': str(intent.id),
            'order_number': intent.order.order_number if intent.order else None,
            'client_secret': intent.client_secret,
            'handler_config': serialized.get('handler_config'),
            'sdk_dependencies': serialized.get('sdk_dependencies', []),
        }, status=status.HTTP_201_CREATED)


class PaymentStatusView(APIView):
    """
    Check payment status for a license purchase.

    Called by the spwig.com frontend on the return page to poll for
    payment completion and license provisioning.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceStatusThrottle]

    @extend_schema(
        tags=['License Checkout'],
        summary=_("Check license payment status"),
        description=_("Check payment and provisioning status for a license purchase. "
                    "Called by spwig.com to poll for completion. HQ only."),
        responses={
            200: inline_serializer(
                name='LicensePaymentStatusResponse',
                fields={
                    'success': drf_serializers.BooleanField(),
                    'payment_status': drf_serializers.CharField(),
                    'order_number': drf_serializers.CharField(allow_null=True),
                    'product_name': drf_serializers.CharField(),
                    'license_provisioned': drf_serializers.BooleanField(),
                },
            ),
            404: OpenApiResponse(description=_("Payment intent not found")),
        },
    )
    def get(self, request, intent_id):
        from payment_providers.models import PaymentIntent

        try:
            intent = PaymentIntent.objects.select_related(
                'order', 'provider_account', 'provider_account__component',
            ).get(
                id=intent_id,
                created_at__gte=timezone.now() - timedelta(hours=2),
            )
        except PaymentIntent.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Verify with provider if not yet terminal (handles delayed/missing webhooks)
        from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
        PaymentOrchestrationService.verify_and_sync_payment_status(intent)

        order = intent.order

        # Check if license has been provisioned
        checkout_request = LicenseCheckoutRequest.objects.filter(
            payment_intent=intent,
        ).first()

        license_provisioned = (
            checkout_request is not None
            and checkout_request.status == LicenseCheckoutRequest.Status.COMPLETED
        )

        return Response({
            'success': True,
            'payment_status': intent.status,
            'order_number': order.order_number if order else None,
            'order_status': order.payment_status if order else None,
            'product_name': checkout_request.license_product.name if checkout_request else '',
            'license_provisioned': license_provisioned,
        })


class PaymentStatusByCheckoutView(APIView):
    """
    Check payment status by checkout request ID.

    Fallback for when the frontend doesn't have the payment intent ID
    (e.g. sessionStorage was lost during redirect). The checkout_id is
    embedded in the Airwallex return URL.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceStatusThrottle]

    @extend_schema(
        tags=['License Checkout'],
        summary=_("Check payment status by checkout ID"),
        description=_("Check payment status using the checkout request ID "
                    "(fallback when intent_id unavailable). HQ only."),
        responses={
            200: inline_serializer(
                name='LicensePaymentStatusByCheckoutResponse',
                fields={
                    'success': drf_serializers.BooleanField(),
                    'payment_status': drf_serializers.CharField(),
                    'order_number': drf_serializers.CharField(allow_null=True),
                    'product_name': drf_serializers.CharField(),
                    'license_provisioned': drf_serializers.BooleanField(),
                },
            ),
            404: OpenApiResponse(description=_("Checkout request not found")),
        },
    )
    def get(self, request, checkout_id):
        checkout_request = LicenseCheckoutRequest.objects.filter(
            id=checkout_id,
            created_at__gte=timezone.now() - timedelta(hours=2),
        ).select_related(
            'license_product', 'payment_intent', 'payment_intent__provider_account', 'order',
        ).first()

        if not checkout_request:
            return Response(
                {'success': False, 'error': 'Payment not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        intent = checkout_request.payment_intent
        order = checkout_request.order

        # Verify with provider if not yet terminal (handles delayed/missing webhooks)
        if intent:
            from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService
            result = PaymentOrchestrationService.verify_and_sync_payment_status(intent)
            if result.get('synced'):
                checkout_request.refresh_from_db()

        license_provisioned = (
            checkout_request.status == LicenseCheckoutRequest.Status.COMPLETED
        )

        return Response({
            'success': True,
            'payment_status': intent.status if intent else 'pending',
            'order_number': order.order_number if order else None,
            'order_status': order.payment_status if order else None,
            'product_name': checkout_request.license_product.name,
            'license_provisioned': license_provisioned,
        })


class RenewalInfoView(APIView):
    """
    Return renewal pricing and maintenance status for a license key.

    Called by the spwig.com frontend when a merchant visits the purchase
    page with a ?renew=<license_key> query parameter.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceStatusThrottle]

    @extend_schema(
        tags=['License Checkout'],
        summary=_("Get maintenance renewal info"),
        description=_("Validate a license key and return renewal pricing "
                    "(25% of current list price) plus maintenance status. HQ only."),
        responses={
            200: inline_serializer(
                name='RenewalInfoResponse',
                fields={
                    'success': drf_serializers.BooleanField(),
                    'license_key': drf_serializers.CharField(),
                    'renewal_price': drf_serializers.CharField(),
                    'currency': drf_serializers.CharField(),
                    'owner_email': drf_serializers.EmailField(),
                    'maintenance_active': drf_serializers.BooleanField(),
                },
            ),
            400: OpenApiResponse(description=_("Invalid license key")),
            404: OpenApiResponse(description=_("License not found")),
        },
    )
    def get(self, request, license_key):
        if not license_key or len(license_key) < 10:
            return Response(
                {'success': False, 'error': 'Invalid license key'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            info = get_renewal_info(license_key)
        except ValueError as e:
            error_msg = str(e)
            if 'not found' in error_msg.lower():
                return Response(
                    {'success': False, 'error': error_msg},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(
                {'success': False, 'error': error_msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({'success': True, **info})


class InitiateRenewalView(APIView):
    """
    Initiate a maintenance renewal checkout.

    Similar to InitiateCheckoutView but for renewing maintenance on an
    existing license. Price is calculated dynamically as 25% of the
    license product's current list price.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceCheckoutThrottle]

    @extend_schema(
        tags=['License Checkout'],
        summary=_("Initiate maintenance renewal checkout"),
        description=_("Create a paid checkout for maintenance renewal. Price is "
                    "calculated as 25% of the current list price. HQ only."),
        request=inline_serializer(
            name='RenewalCheckoutRequest',
            fields={
                'license_key': drf_serializers.CharField(),
                'email': drf_serializers.EmailField(),
                'name': drf_serializers.CharField(),
                'billing_country': drf_serializers.CharField(),
                'billing_address': drf_serializers.CharField(),
                'billing_city': drf_serializers.CharField(),
                'billing_postal_code': drf_serializers.CharField(),
            },
        ),
        responses={
            201: inline_serializer(
                name='RenewalCheckoutResponse',
                fields={
                    'success': drf_serializers.BooleanField(),
                    'payment_intent_id': drf_serializers.UUIDField(),
                    'client_secret': drf_serializers.CharField(),
                },
            ),
            400: OpenApiResponse(description=_("Invalid input")),
        },
    )
    @transaction.atomic
    def post(self, request):
        license_key = request.data.get('license_key', '').strip()
        email = request.data.get('email', '').strip().lower()
        name = request.data.get('name', '').strip()
        billing_country = request.data.get('billing_country', '').strip()
        billing_address = request.data.get('billing_address', '').strip()
        billing_city = request.data.get('billing_city', '').strip()
        billing_state = request.data.get('billing_state', '').strip()
        billing_postal_code = request.data.get('billing_postal_code', '').strip()
        language = request.data.get('language', '').strip() or 'en'

        # Validate required fields
        for field_name, field_val in [
            ('license_key', license_key),
            ('email', email),
            ('name', name),
            ('billing_country', billing_country),
            ('billing_address', billing_address),
            ('billing_city', billing_city),
            ('billing_postal_code', billing_postal_code),
        ]:
            if not field_val:
                return Response(
                    {'success': False, 'error': f'{field_name} is required'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            validate_email(email)
        except DjangoValidationError:
            return Response(
                {'success': False, 'error': 'Invalid email address'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate license and get pricing
        try:
            renewal_info = get_renewal_info(license_key)
        except ValueError as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if renewal_info.get('upgrade_required'):
            return Response(
                {
                    'success': False,
                    'error': (
                        'A new major version has been released. '
                        'Please purchase a new license to continue '
                        'receiving updates.'
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        renewal_price = Decimal(renewal_info['renewal_price'])
        if renewal_price <= 0:
            return Response(
                {'success': False, 'error': 'Unable to calculate renewal price'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get the maintenance-renewal LicenseProduct
        try:
            renewal_product = LicenseProduct.objects.get(
                slug='maintenance-renewal', is_active=True,
            )
        except LicenseProduct.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Renewal product not available'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create checkout request with renewal metadata
        checkout_request = LicenseCheckoutRequest.objects.create(
            license_product=renewal_product,
            email=email,
            name=name,
            billing_country=billing_country,
            status=LicenseCheckoutRequest.Status.PENDING,
            metadata={
                'language': language,
                'renewal_license_key': license_key,
                'renewal_price': str(renewal_price),
                'product_type': renewal_info['product_type'],
                'base_product_name': renewal_info['base_product_name'],
            },
        )

        # Find or create user
        from accounts.services.account_creation_service import AccountCreationService

        user = User.objects.filter(
            email__iexact=email
        ).exclude(username__startswith='guest_').first()

        if not user:
            user = AccountCreationService.create_guest_user(
                email=email,
                first_name=name.split(' ')[0] if name else '',
                last_name=' '.join(name.split(' ')[1:]) if name and ' ' in name else '',
            )

        # Create catalog product with dynamic price
        from catalog.models import Product, Category
        from djmoney.money import Money

        license_category, _ = Category.objects.get_or_create(
            slug='licenses',
            defaults={'name': 'Licenses'},
        )

        # Each renewal gets a unique product with the calculated price
        product = Product.objects.create(
            name=f"Maintenance Renewal — {renewal_info['base_product_name']}",
            slug=f"renewal-{checkout_request.id}",
            sku=f"renewal-{checkout_request.id}",
            product_type='digital',
            price=Money(renewal_price, renewal_info['currency']),
            status='published',
            track_inventory=False,
            category=license_category,
        )

        # Create cart and checkout session
        from cart.models import Cart, CheckoutSession
        from cart.services.cart_service import CartService

        cart = Cart.objects.create(user=user)
        success, msg, _ = CartService.add_item(
            cart=cart, product_id=product.id, quantity=1,
        )
        if not success:
            logger.error(f"Cart add_item failed for renewal: {msg}")
            return Response(
                {'success': False, 'error': 'Unable to process your order'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = CheckoutSession.objects.create(
            cart=cart,
            subtotal=product.price,
            total_amount=product.price,
            step_completed='payment',
            billing_same_as_shipping=False,
            billing_address_data={
                'name': name,
                'address1': billing_address,
                'city': billing_city,
                'state': billing_state,
                'postal_code': billing_postal_code,
                'country': billing_country,
            },
            metadata={
                'license_checkout': True,
                'license_product_slug': 'maintenance-renewal',
                'license_checkout_request_id': str(checkout_request.id),
                'language': language,
            },
            expires_at=timezone.now() + timedelta(hours=2),
        )

        # Select payment provider
        from payment_providers.models import PaymentProviderAccount

        provider_account = PaymentProviderAccount.objects.filter(
            is_active=True,
            connection_status='connected',
        ).first()

        if not provider_account:
            return Response(
                {'success': False, 'error': 'Payment processing is temporarily unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        session.payment_provider = provider_account
        session.save(update_fields=['payment_provider'])

        intent_metadata = {
            'license_checkout': True,
            'license_product_slug': 'maintenance-renewal',
            'license_checkout_request_id': str(checkout_request.id),
        }

        # Create payment intent
        from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService

        frontend_base = _safe_return_base(request.data.get('return_base_url', ''))

        payment_return_url = f"{frontend_base}/purchase/return/?checkout_id={checkout_request.id}"
        payment_cancel_url = f"{frontend_base}/purchase/?cancelled=true"

        pi_success, intent, message = PaymentOrchestrationService.create_payment_intent(
            checkout_session=session,
            provider_account=provider_account,
            return_url=payment_return_url,
            cancel_url=payment_cancel_url,
            metadata=intent_metadata,
        )

        if not pi_success:
            logger.error(f"Payment intent failed for renewal: {message}")
            return Response(
                {'success': False, 'error': 'Unable to initiate payment'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        checkout_request.payment_intent = intent
        checkout_request.save(update_fields=['payment_intent'])

        from payment_providers.api_serializers import PaymentIntentResponseSerializer
        serialized = PaymentIntentResponseSerializer(intent).data

        return Response({
            'success': True,
            'checkout_url': intent.checkout_url or '',
            'payment_intent_id': str(intent.id),
            'order_number': intent.order.order_number if intent.order else None,
            'client_secret': intent.client_secret,
            'handler_config': serialized.get('handler_config'),
            'sdk_dependencies': serialized.get('sdk_dependencies', []),
        }, status=status.HTTP_201_CREATED)


class HostingEventWebhookView(APIView):
    """Receive provisioning lifecycle events from the update server.

    POST /api/hosting-events/
    Authenticated via X-API-KEY header (shared UPGRADE_SERVER_INTERNAL_API_KEY).

    Payload: {"event": "provision_complete|provision_failed", "data": {...}}
    """
    permission_classes = [AllowAny]
    throttle_classes = [HostingWebhookThrottle]

    def post(self, request):
        import hmac

        api_key = request.META.get('HTTP_X_API_KEY', '')
        expected_key = getattr(settings, 'UPGRADE_SERVER_INTERNAL_API_KEY', '')

        if not api_key or not expected_key or not hmac.compare_digest(api_key, expected_key):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        event_type = request.data.get('event', '')
        payload = request.data.get('data', {})

        if not event_type or not isinstance(payload, dict):
            return Response(
                {'error': 'Invalid payload: event and data required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from .services import handle_hosting_event
        result = handle_hosting_event(event_type, payload)

        if result is False and event_type not in ('provision_complete', 'provision_failed'):
            return Response(
                {'error': f'Unknown event type: {event_type}'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({'success': bool(result)})


# ---------------------------------------------------------------------------
# Hosted Subscription Endpoints
# ---------------------------------------------------------------------------

HOSTED_REGIONS = [
    {'id': 'us-east', 'name': 'Americas', 'location': 'Newark, NJ'},
    {'id': 'eu-central', 'name': 'Europe & Middle East', 'location': 'Frankfurt, DE'},
    {'id': 'ap-south', 'name': 'Asia & Oceania', 'location': 'Singapore'},
]


class HostedCatalogView(APIView):
    """
    Return hosted plan catalog with pricing for both billing intervals.
    Used by the spwig.com pricing page.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        tags=['Hosted Checkout'],
        summary=_("Get hosted plan catalog"),
        description=_("Returns active hosted plans with monthly/annual pricing, "
                      "POS addon pricing, and available regions. HQ only."),
    )
    def get(self, request):
        plans = HostedPlan.objects.filter(is_active=True).order_by('sort_order')

        data = []
        for p in plans:
            plan_data = {
                'slug': p.slug,
                'name': p.name,
                'tagline': p.tagline,
                'monthly_price': str(p.monthly_price.amount),
                'annual_price': str(p.annual_price.amount),
                'annual_total': str(p.annual_total),
                'currency': str(p.monthly_price.currency),
                'infra_tier': p.infra_tier,
                'max_products': p.max_products,
                'max_staff': p.max_staff,
                'storage_gb': p.storage_gb,
                'emails_monthly': p.emails_monthly,
                'includes_pos': p.includes_pos,
                'includes_api': p.includes_api,
                'includes_sla': p.includes_sla,
                'includes_custom_domain': p.includes_custom_domain,
                'features': p.features,
                'is_featured': p.is_featured,
            }
            # Introductory offer — separate monthly and annual
            if p.has_monthly_intro:
                plan_data['intro_monthly'] = {
                    'discount_percent': p.intro_monthly_discount_percent,
                    'cycles': p.intro_monthly_discount_cycles,
                    'price': str(p.intro_monthly_price),
                }
            if p.has_annual_intro:
                plan_data['intro_annual'] = {
                    'discount_percent': p.intro_annual_discount_percent,
                    'cycles': p.intro_annual_discount_cycles,
                    'price': str(p.intro_annual_price),
                    'total': str(p.intro_annual_price * 12),
                }
            data.append(plan_data)

        return Response({
            'plans': data,
            'addons': [
                {
                    'slug': 'pos-addon',
                    'name': 'POS Add-on',
                    'price': '29.00',
                    'currency': 'EUR',
                },
            ],
            'regions': HOSTED_REGIONS,
        })


class CheckStoreNameView(APIView):
    """
    Check if a store slug is available for a hosted instance.
    Validates the slug format and checks uniqueness against existing checkout
    requests and, when available, the update server.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceStatusThrottle]

    @extend_schema(
        tags=['Hosted Checkout'],
        summary=_("Check store name availability"),
        description=_("Validate store slug and check availability. HQ only."),
    )
    def get(self, request):
        import re

        slug = request.query_params.get('slug', '').strip().lower()

        if not slug:
            return Response(
                {'available': False, 'error': 'Store name is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate format: lowercase alphanumeric + hyphens, 3-63 chars
        if not re.match(r'^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$', slug):
            return Response({
                'available': False,
                'error': 'Store name must be 3-63 characters, lowercase letters, '
                         'numbers, and hyphens only',
            })

        # Reserved slugs
        reserved = {
            'www', 'mail', 'ftp', 'admin', 'api', 'app', 'blog', 'shop',
            'store', 'test', 'demo', 'staging', 'dev', 'support', 'help',
            'docs', 'status', 'updates', 'spwig', 'myspwig',
        }
        if slug in reserved:
            suggestions = self._suggest_alternatives(slug)
            return Response({
                'available': False,
                'error': 'This name is reserved',
                'suggestions': suggestions,
            })

        # Check against existing hosted checkout requests
        exists_locally = HostedCheckoutRequest.objects.filter(
            store_slug=slug,
            status__in=[
                HostedCheckoutRequest.Status.PENDING,
                HostedCheckoutRequest.Status.PAYMENT_PROCESSING,
                HostedCheckoutRequest.Status.PROVISIONING,
                HostedCheckoutRequest.Status.COMPLETED,
            ],
        ).exists()

        if exists_locally:
            suggestions = self._suggest_alternatives(slug)
            return Response({
                'available': False,
                'error': 'This name is already taken',
                'suggestions': suggestions,
            })

        # TODO: Also check against the update server's HostedInstance table
        # when the check-name endpoint is implemented there.
        # For now, local check is sufficient since all checkouts go through us.

        return Response({
            'available': True,
            'subdomain': f'{slug}.myspwig.com',
        })

    def _suggest_alternatives(self, slug):
        """Generate available alternative slugs."""
        active_statuses = [
            HostedCheckoutRequest.Status.PENDING,
            HostedCheckoutRequest.Status.PAYMENT_PROCESSING,
            HostedCheckoutRequest.Status.PROVISIONING,
            HostedCheckoutRequest.Status.COMPLETED,
        ]
        candidates = []

        # Suffixed variants
        for suffix in ('store', 'shop', 'co', 'hq'):
            candidates.append(f'{slug}-{suffix}')
        # Prefixed variants
        for prefix in ('my', 'the', 'get'):
            candidates.append(f'{prefix}-{slug}')
        # Numbered variants
        for i in range(2, 5):
            candidates.append(f'{slug}-{i}')

        # Filter to available ones
        taken = set(
            HostedCheckoutRequest.objects.filter(
                store_slug__in=candidates,
                status__in=active_statuses,
            ).values_list('store_slug', flat=True)
        )
        return [c for c in candidates if c not in taken][:5]


class InitiateHostedCheckoutView(APIView):
    """
    Initiate a hosted plan checkout.

    Creates a payment intent for the first billing cycle. After payment
    succeeds (via webhook), provision_hosted_subscription() triggers
    license creation and instance provisioning on the update server.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceCheckoutThrottle]

    @extend_schema(
        tags=['Hosted Checkout'],
        summary=_("Initiate hosted plan checkout"),
        description=_("Create a checkout for a hosted subscription plan. Returns "
                      "embedded payment config for Airwallex SDK. HQ only. "
                      "Optionally accepts Token auth to link the checkout to an account."),
    )
    @transaction.atomic
    def post(self, request):
        plan_slug = request.data.get('plan_slug', '').strip()
        billing_interval = request.data.get('billing_interval', '').strip()
        store_name = request.data.get('store_name', '').strip()
        store_slug = request.data.get('store_slug', '').strip().lower()
        region = request.data.get('region', '').strip()
        pos_addon = bool(request.data.get('pos_addon', False))
        admin_password = request.data.get('admin_password', '')
        email = request.data.get('email', '').strip().lower()
        name = request.data.get('name', '').strip()
        company = request.data.get('company', '').strip()
        billing_country = request.data.get('billing_country', '').strip()
        billing_address = request.data.get('billing_address', '').strip()
        billing_city = request.data.get('billing_city', '').strip()
        billing_state = request.data.get('billing_state', '').strip()
        billing_postal_code = request.data.get('billing_postal_code', '').strip()
        language = request.data.get('language', '').strip() or 'en'

        # --- Validation ---
        errors = {}
        if not plan_slug:
            errors['plan_slug'] = 'Please select a plan'
        if billing_interval not in ('monthly', 'annual'):
            errors['billing_interval'] = 'Must be monthly or annual'
        if not store_name:
            errors['store_name'] = 'Store name is required'
        if not store_slug:
            errors['store_slug'] = 'Store slug is required'
        if not region:
            errors['region'] = 'Region is required'
        if not email:
            errors['email'] = 'Email is required'
        if not name:
            errors['name'] = 'Full name is required'
        if not billing_country:
            errors['billing_country'] = 'Billing country is required'
        if not billing_address:
            errors['billing_address'] = 'Billing address is required'
        if not billing_city:
            errors['billing_city'] = 'City is required'
        if not billing_postal_code:
            errors['billing_postal_code'] = 'Postal code is required'
        if not admin_password or len(admin_password) < 8:
            errors['admin_password'] = 'Password must be at least 8 characters'

        if errors:
            return Response(
                {'success': False, 'errors': errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_email(email)
        except DjangoValidationError:
            return Response(
                {'success': False, 'errors': {'email': 'Invalid email address'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate store slug format
        import re
        if not re.match(r'^[a-z0-9](?:[a-z0-9-]{0,60}[a-z0-9])?$', store_slug):
            return Response(
                {'success': False, 'errors': {
                    'store_slug': 'Store name must be 2-63 characters, lowercase '
                                  'letters, numbers, and hyphens only',
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate plan
        try:
            plan = HostedPlan.objects.get(slug=plan_slug, is_active=True)
        except HostedPlan.DoesNotExist:
            return Response(
                {'success': False, 'errors': {'plan_slug': 'Plan not found'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate region
        valid_regions = {r['id'] for r in HOSTED_REGIONS}
        if region not in valid_regions:
            return Response(
                {'success': False, 'errors': {'region': 'Invalid region'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate store slug availability (inside transaction for atomicity)
        slug_taken = HostedCheckoutRequest.objects.filter(
            store_slug=store_slug,
            status__in=[
                HostedCheckoutRequest.Status.PENDING,
                HostedCheckoutRequest.Status.PAYMENT_PROCESSING,
                HostedCheckoutRequest.Status.PROVISIONING,
                HostedCheckoutRequest.Status.COMPLETED,
            ],
        ).exists()
        if not slug_taken:
            slug_taken = HostedSubscription.objects.filter(store_slug=store_slug).exists()
        if slug_taken:
            return Response(
                {'success': False, 'errors': {'store_slug': 'This store name is already taken'}},
                status=status.HTTP_409_CONFLICT,
            )

        # POS addon: not needed if plan includes POS
        if plan.includes_pos:
            pos_addon = False

        # Idempotency: check for recent active checkout
        existing = HostedCheckoutRequest.objects.filter(
            email__iexact=email,
            hosted_plan=plan,
            store_slug=store_slug,
            status=HostedCheckoutRequest.Status.PENDING,
            created_at__gte=timezone.now() - timedelta(hours=2),
        ).first()

        if existing and existing.payment_intent:
            intent = existing.payment_intent
            intent_age = timezone.now() - intent.created_at
            reusable = ['created', 'requires_payment_method']
            is_fresh = intent_age.total_seconds() < 300
            if intent.status in reusable or (intent.status == 'requires_action' and is_fresh):
                if intent.client_secret or intent.checkout_url:
                    from payment_providers.api_serializers import PaymentIntentResponseSerializer
                    serialized = PaymentIntentResponseSerializer(intent).data
                    return Response({
                        'success': True,
                        'checkout_request_id': str(existing.id),
                        'payment_intent_id': str(intent.id),
                        'client_secret': intent.client_secret,
                        'handler_config': serialized.get('handler_config'),
                        'sdk_dependencies': serialized.get('sdk_dependencies', []),
                    }, status=status.HTTP_200_OK)

        # --- Calculate first payment amount (apply intro discount) ---
        if billing_interval == 'annual':
            if plan.has_annual_intro:
                base_amount = plan.intro_annual_price * 12
            else:
                base_amount = plan.annual_price.amount * 12
        else:
            if plan.has_monthly_intro:
                base_amount = plan.intro_monthly_price
            else:
                base_amount = plan.monthly_price.amount

        if pos_addon:
            addon_amount = Decimal('29.00')
            # Apply intro discount to addon too
            if billing_interval == 'annual' and plan.has_annual_intro:
                multiplier = Decimal(100 - plan.intro_annual_discount_percent) / Decimal(100)
                addon_amount = (addon_amount * multiplier).quantize(Decimal('0.01'))
            elif billing_interval == 'monthly' and plan.has_monthly_intro:
                multiplier = Decimal(100 - plan.intro_monthly_discount_percent) / Decimal(100)
                addon_amount = (addon_amount * multiplier).quantize(Decimal('0.01'))
            if billing_interval == 'annual':
                addon_amount *= 12
            base_amount += addon_amount

        # --- Create checkout request ---
        from django.contrib.auth.hashers import make_password
        checkout_request = HostedCheckoutRequest.objects.create(
            hosted_plan=plan,
            billing_interval=billing_interval,
            email=email,
            name=name,
            company=company,
            billing_country=billing_country,
            store_name=store_name,
            store_slug=store_slug,
            region=region,
            pos_addon=pos_addon,
            status=HostedCheckoutRequest.Status.PENDING,
            metadata={
                'language': language,
                'admin_password_hash': make_password(admin_password),
            },
        )

        # --- Find or create user ---
        from accounts.services.account_creation_service import AccountCreationService

        # Prefer authenticated user (from account portal), then existing full account, then guest
        if request.user and request.user.is_authenticated:
            user = request.user
        else:
            user = User.objects.filter(
                email__iexact=email
            ).exclude(username__startswith='guest_').first()

            if not user:
                user = AccountCreationService.create_guest_user(
                    email=email,
                    first_name=name.split(' ')[0] if name else '',
                    last_name=' '.join(name.split(' ')[1:]) if name and ' ' in name else '',
                )

        # --- Create catalog product for the plan ---
        from catalog.models import Product, Category
        from djmoney.money import Money

        license_category, _ = Category.objects.get_or_create(
            slug='hosted-plans',
            defaults={'name': 'Hosted Plans'},
        )

        product_sku = f'hosted-{plan.slug}-{billing_interval}'
        product, _ = Product.objects.get_or_create(
            sku=product_sku,
            defaults={
                'name': f'{plan.name} ({billing_interval.title()})',
                'slug': f'hosted-{plan.slug}-{billing_interval}',
                'product_type': 'digital',
                'price': Money(base_amount, 'EUR'),
                'status': 'published',
                'track_inventory': False,
                'category': license_category,
            }
        )
        # Update price if plan pricing changed
        if product.price.amount != base_amount:
            product.price = Money(base_amount, 'EUR')
            product.save(update_fields=['price', 'price_currency'])

        # --- Create cart + checkout session ---
        from cart.models import Cart, CheckoutSession
        from cart.services.cart_service import CartService

        cart = Cart.objects.create(user=user)
        success, msg, cart_item = CartService.add_item(
            cart=cart, product_id=product.id, quantity=1,
        )
        if not success:
            logger.error("Hosted checkout cart add_item failed: %s", msg)
            return Response(
                {'success': False, 'error': 'Unable to process your order'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = CheckoutSession.objects.create(
            cart=cart,
            subtotal=Money(base_amount, 'EUR'),
            total_amount=Money(base_amount, 'EUR'),
            step_completed='payment',
            billing_same_as_shipping=False,
            billing_address_data={
                'name': name,
                'company': company,
                'address1': billing_address,
                'city': billing_city,
                'state': billing_state,
                'postal_code': billing_postal_code,
                'country': billing_country,
            },
            metadata={
                'hosted_checkout': True,
                'hosted_plan_slug': plan.slug,
                'hosted_checkout_request_id': str(checkout_request.id),
                'billing_interval': billing_interval,
                'store_name': store_name,
                'store_slug': store_slug,
                'region': region,
                'pos_addon': pos_addon,
                'language': language,
            },
            expires_at=timezone.now() + timedelta(hours=2),
        )

        # --- Select payment provider ---
        from payment_providers.models import PaymentProviderAccount

        provider_account = PaymentProviderAccount.objects.filter(
            is_active=True,
            connection_status='connected',
        ).first()

        if not provider_account:
            logger.error("Hosted checkout: no active payment provider configured")
            return Response(
                {'success': False, 'error': 'Payment processing is temporarily unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        session.payment_provider = provider_account
        session.save(update_fields=['payment_provider'])

        # --- Create Airwallex customer for recurring billing ---
        intent_metadata = {
            'hosted_checkout': True,
            'hosted_plan_slug': plan.slug,
            'hosted_checkout_request_id': str(checkout_request.id),
        }

        try:
            from subscriptions.provider_base import get_provider as get_subscription_provider
            sub_provider = get_subscription_provider(provider_account)
            customer_result = sub_provider.create_customer(user, email)
            airwallex_customer_id = customer_result.get('customer_id', '')
            if airwallex_customer_id:
                checkout_request.metadata['airwallex_customer_id'] = airwallex_customer_id
                checkout_request.save(update_fields=['metadata'])
                intent_metadata['airwallex_customer_id'] = airwallex_customer_id
                logger.info(
                    "Created Airwallex customer %s for hosted checkout %s",
                    airwallex_customer_id, _mask_email(email),
                )
        except Exception as e:
            logger.warning(
                "Failed to create Airwallex customer for %s: %s. "
                "Subscription billing consent will need manual setup.",
                _mask_email(email), e,
            )

        # --- Create payment intent ---
        from payment_providers.services.payment_orchestration_service import PaymentOrchestrationService

        frontend_base = _safe_return_base(request.data.get('return_base_url', ''))

        payment_return_url = (
            f"{frontend_base}/purchase/return/"
            f"?hosted=true&checkout_id={checkout_request.id}"
        )
        payment_cancel_url = (
            f"{frontend_base}/purchase/"
            f"?plan={plan.slug}&interval={billing_interval}&cancelled=true"
        )

        pi_success, intent, message = PaymentOrchestrationService.create_payment_intent(
            checkout_session=session,
            provider_account=provider_account,
            return_url=payment_return_url,
            cancel_url=payment_cancel_url,
            metadata=intent_metadata,
        )

        if not pi_success:
            logger.error(
                "Hosted checkout payment intent failed for %s: %s",
                _mask_email(email), message,
            )
            return Response(
                {'success': False, 'error': 'Unable to initiate payment'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Link payment intent to checkout request
        checkout_request.payment_intent = intent
        checkout_request.status = HostedCheckoutRequest.Status.PAYMENT_PROCESSING
        checkout_request.save(update_fields=['payment_intent', 'status'])

        from payment_providers.api_serializers import PaymentIntentResponseSerializer
        serialized = PaymentIntentResponseSerializer(intent).data

        return Response({
            'success': True,
            'checkout_request_id': str(checkout_request.id),
            'payment_intent_id': str(intent.id),
            'order_number': intent.order.order_number if intent.order else None,
            'checkout_url': intent.checkout_url or '',
            'client_secret': intent.client_secret,
            'handler_config': serialized.get('handler_config'),
            'sdk_dependencies': serialized.get('sdk_dependencies', []),
        }, status=status.HTTP_201_CREATED)


class HostedCheckoutStatusView(APIView):
    """
    Check hosted checkout status including provisioning progress.
    Polled by the frontend after payment to track provisioning.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [MarketplaceStatusThrottle]

    @extend_schema(
        tags=['Hosted Checkout'],
        summary=_("Check hosted checkout status"),
        description=_("Returns checkout and provisioning status. Polled by "
                      "spwig.com frontend after payment. HQ only."),
    )
    def get(self, request, checkout_id):
        try:
            checkout = HostedCheckoutRequest.objects.select_related(
                'hosted_plan',
            ).get(
                id=checkout_id,
                created_at__gte=timezone.now() - timedelta(hours=24),
            )
        except HostedCheckoutRequest.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Checkout not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        response_data = {
            'success': True,
            'status': checkout.status,
            'store_slug': checkout.store_slug,
            'store_name': checkout.store_name,
            'plan_name': checkout.hosted_plan.name,
            'region': checkout.region,
            'store_url': checkout.metadata.get('store_url'),
            'admin_url': checkout.metadata.get('admin_url'),
        }

        if checkout.status == HostedCheckoutRequest.Status.FAILED:
            response_data['error_message'] = (
                'We encountered an issue setting up your store. '
                'Our team has been notified and will resolve this shortly.'
            )

        return Response(response_data)


class CancelHostedSubscriptionView(APIView):
    """
    Self-service subscription cancellation.

    Called from the merchant's admin panel via the license phone-home
    pattern (authenticated with the internal API key). Sets the
    subscription to cancel at end of current billing period.
    """
    authentication_classes = []
    permission_classes = [AllowAny]
    throttle_classes = [HostingWebhookThrottle]

    @extend_schema(
        tags=['Hosted Checkout'],
        summary=_("Cancel hosted subscription"),
        description=_("Cancel a hosted subscription at end of billing period. "
                      "Authenticated via internal API key. HQ only."),
    )
    @transaction.atomic
    def post(self, request):
        import hmac as hmac_module

        # Authenticate via internal API key (same as hosting events)
        api_key = request.headers.get('X-API-KEY', '')
        expected_key = getattr(settings, 'UPGRADE_SERVER_INTERNAL_API_KEY', '')

        if not api_key or not expected_key or not hmac_module.compare_digest(api_key, expected_key):
            return Response(
                {'error': 'Unauthorized'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        license_key = request.data.get('license_key', '').strip()
        reason = request.data.get('reason', '').strip()

        if not license_key:
            return Response(
                {'success': False, 'error': 'License key is required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if already cancelled (distinct error message)
        already_cancelled = HostedSubscription.objects.filter(
            license_key=license_key,
            status__in=[
                HostedSubscription.Status.CANCELLED,
                HostedSubscription.Status.TERMINATED,
            ],
        ).exists()
        if already_cancelled:
            return Response(
                {'success': False, 'error': 'This subscription has already been cancelled'},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            subscription = HostedSubscription.objects.select_for_update().select_related(
                'hosted_plan',
            ).get(
                license_key=license_key,
                status__in=[
                    HostedSubscription.Status.ACTIVE,
                    HostedSubscription.Status.PAST_DUE,
                    HostedSubscription.Status.SUSPENDED,
                ],
            )
        except HostedSubscription.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Active subscription not found for this license'},
                status=status.HTTP_404_NOT_FOUND,
            )

        now = timezone.now()
        access_until = subscription.current_period_end or (now + timedelta(days=1))
        # For suspended subscriptions the period may already be in the past —
        # clamp to now so the email shows a sensible date and the termination
        # countdown starts from the moment of cancellation.
        if access_until < now:
            access_until = now
        termination_date = access_until + timedelta(days=30)

        subscription.cancellation_type = HostedSubscription.CancellationType.END_OF_PERIOD
        subscription.cancelled_at = now
        subscription.cancellation_reason = reason[:500]
        subscription.termination_scheduled_at = termination_date
        # Status stays active until period end; then process_terminations handles it
        subscription.status = HostedSubscription.Status.CANCELLED
        subscription.save(update_fields=[
            'cancellation_type', 'cancelled_at', 'cancellation_reason',
            'termination_scheduled_at', 'status', 'updated_at',
        ])

        # Send cancellation confirmation email
        from .services import _send_hosting_email, notify_update_server_subscription

        _send_hosting_email(
            to_email=subscription.email,
            template_type='hosted_cancellation_confirmation',
            context={
                'store_name': subscription.store_name,
                'plan_name': subscription.hosted_plan.name,
                'access_until_date': access_until.strftime('%d %B %Y'),
                'termination_date': termination_date.strftime('%d %B %Y'),
            },
            label='cancellation confirmation',
        )

        # Notify update server — include access_until so it defers suspension
        try:
            notify_update_server_subscription(
                event_type='subscription.cancelled',
                data={
                    'license_key': license_key,
                    'access_until': access_until.isoformat(),
                },
            )
        except Exception as e:
            logger.error('Failed to notify update server of cancellation: %s', e)

        # Cancel any pending onboarding emails (Fix 9)
        try:
            from email_system.models import ScheduledEmail
            cancelled_count = ScheduledEmail.objects.filter(
                recipient_email=subscription.email,
                status='pending',
                template_type__startswith='hosted_onboarding',
            ).update(status='cancelled')
            if cancelled_count:
                logger.info('Cancelled %d pending onboarding emails for %s', cancelled_count, subscription.store_slug)
        except Exception as e:
            logger.warning('Could not cancel onboarding emails: %s', e)

        logger.info(
            'Hosted subscription cancelled for %s (access until %s, terminate %s)',
            subscription.store_slug, access_until, termination_date,
        )

        return Response({
            'success': True,
            'access_until': access_until.isoformat(),
            'termination_date': termination_date.isoformat(),
        })
