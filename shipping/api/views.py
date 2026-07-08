"""
Shipping API Views
DRF viewsets for shipping endpoints
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view

from shipping.models import CarrierPreset, Shipment, TrackingEvent, ProviderAccount
from shipping.api.serializers import (
    CarrierPresetSerializer,
    ShipmentSerializer,
    ShipmentCreateSerializer,
    TrackingEventSerializer,
    ProviderAccountSerializer,
    ProviderAccountListSerializer,
)
from shipping.api.permissions import (
    IsShipmentOwner,
    IsStaffOrReadOnly,
    IsProviderOwner,
    IsAuthenticatedOrStaffReadOnly,
)
from core.api.authentication import HeadlessAPIMixin


@extend_schema_view(
    list=extend_schema(
        tags=['Shipping'],
        summary=_("List carrier presets"),
        description=_("Get all active shipping carrier presets available for creating shipments. Returns carrier name, slug, logo, and supported service types.")
    ),
    retrieve=extend_schema(
        tags=['Shipping'],
        summary=_("Get carrier preset details"),
        description=_("Get detailed information about a specific carrier preset including configuration, service types, and integration status.")
    )
)
class CarrierPresetViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for carrier presets.

    list: Get all active carriers
    retrieve: Get a specific carrier by ID
    """
    queryset = CarrierPreset.objects.filter(is_active=True).order_by('name')
    serializer_class = CarrierPresetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'slug']
    ordering_fields = ['name', 'slug']


@extend_schema_view(
    list=extend_schema(
        tags=['Shipping'],
        summary=_("List shipments"),
        description=_("Get all shipments for the authenticated user. Staff members can view all shipments. Supports filtering by status, order, carrier, and provider.")
    ),
    retrieve=extend_schema(
        tags=['Shipping'],
        summary=_("Get shipment details"),
        description=_("Get detailed information about a specific shipment including tracking number, status, carrier details, and tracking events.")
    ),
    create=extend_schema(
        tags=['Shipping'],
        summary=_("Create new shipment"),
        description=_("Create a new shipment for an order. Requires order ID, carrier preset, shipping address, and package details. Optionally integrates with shipping provider APIs to generate labels.")
    ),
    update=extend_schema(
        tags=['Shipping'],
        summary=_("Update shipment"),
        description=_("Update shipment information (staff only). Can modify tracking number, status, carrier details, and package information.")
    ),
    partial_update=extend_schema(
        tags=['Shipping'],
        summary=_("Partially update shipment"),
        description=_("Partially update shipment fields (staff only). Useful for updating specific fields like status or tracking number without sending full shipment data.")
    ),
    destroy=extend_schema(
        tags=['Shipping'],
        summary=_("Delete shipment"),
        description=_("Delete a shipment record (staff only). Caution: This is permanent and cannot be undone.")
    ),
    tracking=extend_schema(
        tags=['Shipping'],
        summary=_("Get tracking events"),
        description=_("Get all tracking events for a shipment in chronological order. Includes status updates, location changes, and delivery confirmations.")
    ),
    by_order=extend_schema(
        tags=['Shipping'],
        summary=_("Get shipments by order"),
        description=_("Get all shipments associated with a specific order. Useful for orders with multiple packages or split shipments.")
    ),
    packing_slip=extend_schema(
        tags=['Shipping'],
        summary=_("Generate packing slip PDF"),
        description=_("Generate and retrieve packing slip PDF for this shipment. Returns base64-encoded data URI. Cached after first generation for performance.")
    ),
    commercial_invoice=extend_schema(
        tags=['Shipping'],
        summary=_("Generate commercial invoice PDF"),
        description=_("Generate commercial invoice PDF for international shipments. Includes customs data, HS codes, country of origin, and item values. Required for customs clearance.")
    ),
    customs_form=extend_schema(
        tags=['Shipping'],
        summary=_("Generate customs declaration PDF"),
        description=_("Generate customs declaration form (CN22 for small parcels or CN23 for larger shipments). Required for international shipping with postal services.")
    )
)
class ShipmentViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    API endpoint for shipments.

    list: Get user's shipments (staff can see all)
    retrieve: Get a specific shipment
    create: Create a new shipment
    update: Update a shipment (staff only)
    destroy: Delete a shipment (staff only)
    """
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated, IsShipmentOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'order', 'carrier_preset', 'provider_account']
    search_fields = ['tracking_id', 'order__order_number']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return shipments for current user.
        Staff can see all shipments.
        """
        user = self.request.user

        if user.is_staff:
            return Shipment.objects.select_related(
                'order',
                'user',
                'carrier_preset',
                'provider_account',
                'provider_account__component'
            ).prefetch_related('tracking_events').all()

        # Regular users only see their own shipments
        return Shipment.objects.filter(
            order__user=user
        ).select_related(
            'order',
            'user',
            'carrier_preset',
            'provider_account',
            'provider_account__component'
        ).prefetch_related('tracking_events').all()

    def get_serializer_class(self):
        """Use different serializer for create action"""
        if self.action == 'create':
            return ShipmentCreateSerializer
        return ShipmentSerializer

    @action(detail=True, methods=['get'])
    def tracking(self, request, pk=None):
        """
        Get tracking events for a shipment.
        GET /api/shipping/shipments/{id}/tracking/
        """
        shipment = self.get_object()
        events = shipment.tracking_events.all().order_by('-occurred_at')
        serializer = TrackingEventSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_order(self, request):
        """
        Get shipments for a specific order.
        GET /api/shipping/shipments/by_order/?order_id=123
        """
        order_id = request.query_params.get('order_id')

        if not order_id:
            return Response(
                {'error': 'order_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(order_id=order_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Phase 6: Document Generation Endpoints
    @action(detail=True, methods=['get'], url_path='documents/packing-slip')
    def packing_slip(self, request, pk=None):
        """
        Generate and return packing slip PDF for this shipment.
        GET /api/shipping/shipments/{id}/documents/packing-slip/

        Returns the packing slip PDF as a data URI (base64-encoded).
        If already generated, returns the cached version.
        """
        from shipping.services.document_service import DocumentService

        shipment = self.get_object()

        # Check if already generated
        if not shipment.packing_slip_url:
            # Generate new packing slip
            try:
                data_uri = DocumentService.generate_packing_slip(shipment)
                shipment.packing_slip_url = data_uri
                shipment.save(update_fields=['packing_slip_url'])
            except Exception as e:
                return Response(
                    {'error': f'Failed to generate packing slip: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({
            'document_url': shipment.packing_slip_url,
            'document_type': 'packing_slip',
            'shipment_id': str(shipment.id)
        })

    @action(detail=True, methods=['get'], url_path='documents/commercial-invoice')
    def commercial_invoice(self, request, pk=None):
        """
        Generate and return commercial invoice PDF for this shipment.
        GET /api/shipping/shipments/{id}/documents/commercial-invoice/

        Returns the commercial invoice PDF as a data URI (base64-encoded).
        Includes customs data (HS codes, country of origin, values).
        If already generated, returns the cached version.
        """
        from shipping.services.document_service import DocumentService

        shipment = self.get_object()

        # Check if already generated
        if not shipment.commercial_invoice_url:
            # Generate new commercial invoice
            try:
                data_uri = DocumentService.generate_commercial_invoice(shipment)
                shipment.commercial_invoice_url = data_uri
                shipment.save(update_fields=['commercial_invoice_url'])
            except Exception as e:
                return Response(
                    {'error': f'Failed to generate commercial invoice: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({
            'document_url': shipment.commercial_invoice_url,
            'document_type': 'commercial_invoice',
            'shipment_id': str(shipment.id)
        })

    @action(detail=True, methods=['get'], url_path='documents/customs-form')
    def customs_form(self, request, pk=None):
        """
        Generate and return customs declaration form PDF (CN22/CN23).
        GET /api/shipping/shipments/{id}/documents/customs-form/?form_type=CN22

        Query Parameters:
            form_type: 'CN22' (default, for small parcels) or 'CN23' (for larger shipments)

        Returns the customs form PDF as a data URI (base64-encoded).
        If already generated, returns the cached version.
        """
        from shipping.services.document_service import DocumentService

        shipment = self.get_object()
        form_type = request.query_params.get('form_type', 'CN22')

        # Validate form type
        if form_type not in ['CN22', 'CN23']:
            return Response(
                {'error': 'form_type must be CN22 or CN23'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already generated
        if not shipment.customs_form_url:
            # Generate new customs form
            try:
                data_uri = DocumentService.generate_customs_form(shipment, form_type=form_type)
                shipment.customs_form_url = data_uri
                shipment.save(update_fields=['customs_form_url'])
            except Exception as e:
                return Response(
                    {'error': f'Failed to generate customs form: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({
            'document_url': shipment.customs_form_url,
            'document_type': 'customs_form',
            'form_type': form_type,
            'shipment_id': str(shipment.id)
        })


@extend_schema_view(
    list=extend_schema(
        tags=['Shipping'],
        summary=_("List tracking events"),
        description=_("Get all tracking events for the authenticated user's shipments. Staff can view all events. Filter by shipment ID or status. Ordered by occurrence date (newest first).")
    ),
    retrieve=extend_schema(
        tags=['Shipping'],
        summary=_("Get tracking event details"),
        description=_("Get detailed information about a specific tracking event including timestamp, location, status code, and description.")
    )
)
class TrackingEventViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for tracking events (read-only).

    list: Get all tracking events (filtered by user's shipments)
    retrieve: Get a specific tracking event
    """
    serializer_class = TrackingEventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['shipment', 'status']
    ordering_fields = ['occurred_at', 'created_at']
    ordering = ['-occurred_at']

    def get_queryset(self):
        """
        Return tracking events for user's shipments.
        Staff can see all events.
        """
        user = self.request.user

        if user.is_staff:
            return TrackingEvent.objects.select_related('shipment').all()

        # Regular users only see events for their shipments
        return TrackingEvent.objects.filter(
            shipment__order__user=user
        ).select_related('shipment').all()


@extend_schema_view(
    list=extend_schema(
        tags=['Shipping'],
        summary=_("List provider accounts"),
        description=_("Get all shipping provider accounts for the authenticated user. Staff can view all accounts. Returns account names, providers, and connection status. Credentials are never exposed.")
    ),
    retrieve=extend_schema(
        tags=['Shipping'],
        summary=_("Get provider account details"),
        description=_("Get detailed information about a specific provider account including display name, provider type, connection status, and configuration. API credentials are hidden for security.")
    ),
    create=extend_schema(
        tags=['Shipping'],
        summary=_("Create provider account"),
        description=_("Create a new shipping provider account (staff only). Requires provider component slug, display name, and API credentials. Credentials are encrypted before storage.")
    ),
    update=extend_schema(
        tags=['Shipping'],
        summary=_("Update provider account"),
        description=_("Update provider account settings including display name and credentials. Credentials are encrypted. Previous credentials are replaced, not merged.")
    ),
    partial_update=extend_schema(
        tags=['Shipping'],
        summary=_("Partially update provider account"),
        description=_("Update specific fields of a provider account. Useful for changing display name or connection settings without resending credentials.")
    ),
    destroy=extend_schema(
        tags=['Shipping'],
        summary=_("Delete provider account"),
        description=_("Delete a shipping provider account. Warning: This will disable all shipments using this account. Ensure you have migrated to another account first.")
    ),
    test_connection=extend_schema(
        tags=['Shipping'],
        summary=_("Test provider connection"),
        description=_("Test connection to the shipping provider API using stored credentials. Verifies authentication and API accessibility. Updates account connection status based on result.")
    )
)
class ProviderAccountViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    API endpoint for provider accounts.

    list: Get user's provider accounts (staff can see all)
    retrieve: Get a specific provider account
    create: Create a new provider account (staff only)
    update: Update a provider account
    destroy: Delete a provider account

    Note: Credentials are never exposed through the API
    """
    permission_classes = [IsAuthenticated, IsProviderOwner]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['display_name', 'component__name']
    ordering_fields = ['created_at', 'display_name']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return provider accounts for current user.
        Staff can see all accounts.
        """
        user = self.request.user

        if user.is_staff:
            return ProviderAccount.objects.select_related('component', 'user').all()

        # Regular users only see their own provider accounts
        return ProviderAccount.objects.filter(user=user).select_related('component', 'user').all()

    def get_serializer_class(self):
        """Use minimal serializer for list action"""
        if self.action == 'list':
            return ProviderAccountListSerializer
        return ProviderAccountSerializer

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """
        Test provider connection.
        POST /api/shipping/providers/{id}/test_connection/
        """
        provider_account = self.get_object()

        try:
            from shipping.providers.registry import ProviderRegistry

            # Get provider class
            provider_class = ProviderRegistry.get_provider(provider_account.component.slug)

            if not provider_class:
                return Response(
                    {'error': 'Provider implementation not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create provider instance and test
            provider = provider_class(credentials=provider_account.credentials)
            result = provider.test_connection()

            # Update provider account status
            if result.get('success'):
                provider_account.connection_status = 'connected'
                provider_account.connection_error = None
            else:
                provider_account.connection_status = 'error'
                provider_account.connection_error = result.get('error', result.get('message'))

            provider_account.save()

            return Response(result)

        except Exception as e:
            return Response(
                {'success': False, 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
