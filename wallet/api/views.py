"""
Wallet API Views

DRF ViewSets for customer-facing and admin wallet endpoints.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)

from wallet.models import CustomerWallet, WalletTransaction
from wallet.services import WalletService, InsufficientBalance, WalletFrozen
from core.api.authentication import HeadlessAPIMixin
from wallet.api.serializers import (
    WalletBalanceSerializer,
    WalletTransactionListSerializer,
    WalletTransactionSerializer,
    CustomerWalletSerializer,
    CustomerWalletListSerializer,
    AdminTransactionSerializer,
    WalletCreditSerializer,
    WalletDebitSerializer,
)


# =====================================================================
# CUSTOMER-FACING ENDPOINTS
# =====================================================================

@extend_schema_view(
    list=extend_schema(
        tags=['Wallet'],
        summary=_("Get wallet balance"),
        description=_(
            "Get the authenticated customer's wallet balance. "
            "Creates a wallet automatically if the customer does not have one."
        ),
        responses={
            200: WalletBalanceSerializer,
            401: OpenApiResponse(description=_("Authentication required")),
        },
    ),
)
class WalletBalanceViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Customer wallet balance endpoint.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        wallet = WalletService.get_or_create_wallet(request.user)
        serializer = WalletBalanceSerializer(wallet)
        return Response({'success': True, 'data': serializer.data})


@extend_schema_view(
    list=extend_schema(
        tags=['Wallet'],
        summary=_("List wallet transactions"),
        description=_(
            "Get the authenticated customer's wallet transaction history, "
            "ordered by most recent first. Supports filtering by type, source, "
            "and status."
        ),
        parameters=[
            OpenApiParameter(
                name='type', description=_("Filter by transaction type"),
                enum=['credit', 'debit', 'refund', 'adjustment', 'reversal'],
                required=False,
            ),
            OpenApiParameter(
                name='source', description=_("Filter by source"),
                enum=['referral', 'refund', 'promotion', 'manual', 'order'],
                required=False,
            ),
            OpenApiParameter(
                name='status', description=_("Filter by status"),
                enum=['completed', 'pending', 'reversed'],
                required=False,
            ),
            OpenApiParameter(
                name='limit', description=_("Number of results (default 20, max 100)"),
                type=int, required=False,
            ),
            OpenApiParameter(
                name='offset', description=_("Pagination offset"),
                type=int, required=False,
            ),
        ],
        responses={
            200: WalletTransactionListSerializer(many=True),
            401: OpenApiResponse(description=_("Authentication required")),
        },
    ),
)
class WalletTransactionViewSet(HeadlessAPIMixin, viewsets.ViewSet):
    """
    Customer wallet transaction history endpoint.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            wallet = CustomerWallet.objects.get(customer=request.user)
        except CustomerWallet.DoesNotExist:
            return Response({
                'success': True,
                'data': [],
                'pagination': {
                    'total': 0, 'limit': 20, 'offset': 0, 'has_more': False,
                },
            })

        queryset = WalletTransaction.objects.filter(
            wallet=wallet,
        ).order_by('-created_at')

        # Filters
        txn_type = request.query_params.get('type')
        if txn_type:
            queryset = queryset.filter(transaction_type=txn_type)

        source = request.query_params.get('source')
        if source:
            queryset = queryset.filter(source=source)

        txn_status = request.query_params.get('status')
        if txn_status:
            queryset = queryset.filter(status=txn_status)

        # Pagination
        total = queryset.count()
        try:
            limit = min(int(request.query_params.get('limit', 20)), 100)
        except (ValueError, TypeError):
            limit = 20
        try:
            offset = max(int(request.query_params.get('offset', 0)), 0)
        except (ValueError, TypeError):
            offset = 0
        page = queryset[offset:offset + limit]

        serializer = WalletTransactionListSerializer(page, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total,
            },
        })


# =====================================================================
# ADMIN ENDPOINTS
# =====================================================================

@extend_schema_view(
    list=extend_schema(
        tags=['Wallet'],
        summary=_("List customer wallets"),
        description=_(
            "List all customer wallets. Supports search by email or name, "
            "and filtering by active status."
        ),
        parameters=[
            OpenApiParameter(
                name='search', description=_("Search by customer email or name"),
                required=False,
            ),
            OpenApiParameter(
                name='is_active', description=_("Filter by active status"),
                type=bool, required=False,
            ),
        ],
    ),
    retrieve=extend_schema(
        tags=['Wallet'],
        summary=_("Get wallet details"),
        description=_("Get full details of a customer wallet."),
    ),
    credit=extend_schema(
        tags=['Wallet'],
        summary=_("Credit a wallet"),
        description=_(
            "Manually add credit to a customer's wallet. "
            "Requires amount, currency, source, and description."
        ),
        request=WalletCreditSerializer,
        responses={
            200: WalletTransactionSerializer,
            400: OpenApiResponse(description=_("Invalid input or wallet frozen")),
        },
    ),
    debit=extend_schema(
        tags=['Wallet'],
        summary=_("Debit a wallet"),
        description=_(
            "Manually debit a customer's wallet. "
            "Fails if the wallet has insufficient balance or is frozen."
        ),
        request=WalletDebitSerializer,
        responses={
            200: WalletTransactionSerializer,
            400: OpenApiResponse(description=_("Insufficient balance, invalid input, or wallet frozen")),
        },
    ),
    freeze=extend_schema(
        tags=['Wallet'],
        summary=_("Toggle wallet freeze"),
        description=_(
            "Freeze or unfreeze a customer's wallet. "
            "A frozen wallet cannot process credits or debits."
        ),
        request=None,
        responses={
            200: CustomerWalletSerializer,
        },
    ),
)
class AdminWalletViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin ViewSet for managing customer wallets.
    """
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerWalletListSerializer
        return CustomerWalletSerializer

    def get_queryset(self):
        queryset = CustomerWallet.objects.select_related('customer').order_by('-updated_at')

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(customer__email__icontains=search) |
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search)
            )

        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'success': True, 'data': serializer.data})

    @action(detail=True, methods=['post'], url_path='credit')
    def credit(self, request, pk=None):
        """Manually credit a customer wallet."""
        wallet = self.get_object()

        serializer = WalletCreditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            txn = WalletService.credit(
                user=wallet.customer,
                amount=data['amount'],
                currency=data['currency'],
                source=data['source'],
                description=data['description'],
                reference_id=data.get('reference_id', ''),
                created_by=request.user,
            )
        except WalletFrozen:
            return Response(
                {'success': False, 'error': _('Wallet is frozen')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            'success': True,
            'message': _('Wallet credited successfully'),
            'data': WalletTransactionSerializer(txn).data,
        })

    @action(detail=True, methods=['post'], url_path='debit')
    def debit(self, request, pk=None):
        """Manually debit a customer wallet."""
        wallet = self.get_object()

        serializer = WalletDebitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            txn = WalletService.debit(
                user=wallet.customer,
                amount=data['amount'],
                currency=data['currency'],
                source=data['source'],
                description=data['description'],
                reference_id=data.get('reference_id', ''),
            )
        except InsufficientBalance:
            return Response(
                {'success': False, 'error': _('Insufficient wallet balance')},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except WalletFrozen:
            return Response(
                {'success': False, 'error': _('Wallet is frozen')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({
            'success': True,
            'message': _('Wallet debited successfully'),
            'data': WalletTransactionSerializer(txn).data,
        })

    @action(detail=True, methods=['post'], url_path='freeze')
    def freeze(self, request, pk=None):
        """Toggle wallet frozen state."""
        wallet = self.get_object()
        wallet.is_active = not wallet.is_active
        wallet.save(update_fields=['is_active', 'updated_at'])

        state = _('unfrozen') if wallet.is_active else _('frozen')
        return Response({
            'success': True,
            'message': _('Wallet %s successfully') % state,
            'data': CustomerWalletSerializer(wallet).data,
        })


@extend_schema_view(
    list=extend_schema(
        tags=['Wallet'],
        summary=_("List all transactions"),
        description=_(
            "List wallet transactions across all customers. "
            "Supports filtering by wallet, type, source, status, and search."
        ),
        parameters=[
            OpenApiParameter(
                name='wallet_id', description=_("Filter by wallet ID"),
                type=int, required=False,
            ),
            OpenApiParameter(
                name='type', description=_("Filter by transaction type"),
                enum=['credit', 'debit', 'refund', 'adjustment', 'reversal'],
                required=False,
            ),
            OpenApiParameter(
                name='source', description=_("Filter by source"),
                enum=['referral', 'refund', 'promotion', 'manual', 'order'],
                required=False,
            ),
            OpenApiParameter(
                name='status', description=_("Filter by status"),
                enum=['completed', 'pending', 'reversed'],
                required=False,
            ),
            OpenApiParameter(
                name='search', description=_("Search by customer email"),
                required=False,
            ),
            OpenApiParameter(
                name='limit', description=_("Number of results (default 50, max 100)"),
                type=int, required=False,
            ),
            OpenApiParameter(
                name='offset', description=_("Pagination offset"),
                type=int, required=False,
            ),
        ],
    ),
    retrieve=extend_schema(
        tags=['Wallet'],
        summary=_("Get transaction details"),
        description=_("Get full details of a wallet transaction."),
    ),
)
class AdminTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Admin ViewSet for viewing all wallet transactions.
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminTransactionSerializer

    def get_queryset(self):
        queryset = WalletTransaction.objects.select_related(
            'wallet__customer', 'created_by',
        ).order_by('-created_at')

        wallet_id = self.request.query_params.get('wallet_id')
        if wallet_id:
            queryset = queryset.filter(wallet_id=wallet_id)

        txn_type = self.request.query_params.get('type')
        if txn_type:
            queryset = queryset.filter(transaction_type=txn_type)

        source = self.request.query_params.get('source')
        if source:
            queryset = queryset.filter(source=source)

        txn_status = self.request.query_params.get('status')
        if txn_status:
            queryset = queryset.filter(status=txn_status)

        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(wallet__customer__email__icontains=search)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total = queryset.count()
        try:
            limit = min(int(request.query_params.get('limit', 50)), 100)
        except (ValueError, TypeError):
            limit = 50
        try:
            offset = max(int(request.query_params.get('offset', 0)), 0)
        except (ValueError, TypeError):
            offset = 0
        page = queryset[offset:offset + limit]
        serializer = self.get_serializer(page, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total,
            },
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'success': True, 'data': serializer.data})
