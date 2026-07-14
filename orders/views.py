"""
API Views for Orders and Addresses
"""

import logging

from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.authentication import HeadlessAPIMixin

logger = logging.getLogger(__name__)

from .models import Address, Order, OrderItem, OrderNote, ReturnRequest
from .serializers import (
    CancelOrderSerializer,
    CreateAddressSerializer,
    CreateOrderNoteSerializer,
    CreateReturnRequestSerializer,
    OrderAddressSerializer,
    OrderDetailSerializer,
    OrderSerializer,
    OrderSummarySerializer,
    OrderTrackingSerializer,
    ReturnRequestSerializer,
    ReturnRequestSummarySerializer,
    UpdateAddressSerializer,
)
from .services import AddressService, OrderService


class OrderPagination(PageNumberPagination):
    """Pagination for order lists"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


@extend_schema_view(
    list=extend_schema(tags=["Orders"]),
    retrieve=extend_schema(tags=["Orders"]),
    packing_slip=extend_schema(tags=["Orders"], summary=_("Get order packing slip PDF")),
    commercial_invoice=extend_schema(
        tags=["Orders"], summary=_("Get order commercial invoice PDF")
    ),
    list_notes=extend_schema(tags=["Orders"], summary=_("List order notes")),
    add_note=extend_schema(tags=["Orders"], summary=_("Add note to order")),
)
class OrderViewSet(HeadlessAPIMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for order operations

    Endpoints:
    - GET /orders/ - List user's orders
    - GET /orders/{order_number}/ - Get order details
    - GET /orders/{order_number}/tracking/ - Get tracking info
    - POST /orders/{order_number}/cancel/ - Cancel order
    - POST /orders/{order_number}/reorder/ - Reorder
    """

    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination
    lookup_field = "order_number"

    def get_queryset(self):
        """Get orders for current user"""
        user = self.request.user
        status_filter = self.request.query_params.get("status")

        return OrderService.get_order_history(user=user, status=status_filter)

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == "list":
            return OrderSummarySerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def list(self, request):
        """List user's orders"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, order_number=None):
        """Get detailed order information"""
        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(order, context={"request": request})
        return Response(serializer.data)

    @extend_schema(tags=["Orders"])
    @action(detail=True, methods=["get"], url_path="tracking")
    def get_tracking(self, request, order_number=None):
        """Get order tracking information"""
        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        tracking_info = OrderService.get_tracking_info(order, request.user)

        if not tracking_info:
            return Response(
                {"success": False, "message": _("Tracking information not available")},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OrderTrackingSerializer(tracking_info)
        return Response(serializer.data)

    @extend_schema(tags=["Orders"])
    @action(detail=True, methods=["post"])
    def cancel(self, request, order_number=None):
        """Cancel an order"""
        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate request data
        serializer = CancelOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Cancel order
        success, message = OrderService.cancel_order(
            order=order,
            user=request.user,
            reason=serializer.validated_data.get("reason", ""),
            restore_stock=serializer.validated_data.get("restore_stock", True),
        )

        if success:
            order_serializer = OrderDetailSerializer(order, context={"request": request})
            return Response(
                {"success": True, "message": str(message), "order": order_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(tags=["Orders"])
    @action(detail=True, methods=["post"])
    def reorder(self, request, order_number=None):
        """Create new cart from previous order"""
        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        success, message, cart = OrderService.reorder(order, request.user)

        response_data = {
            "success": success,
            "message": str(message),
            "cart_id": cart.id if cart else None,
        }

        if success:
            return Response(response_data)
        else:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(tags=["Orders"])
    @action(detail=False, methods=["get"], url_path="statistics")
    def get_statistics(self, request):
        """Get order statistics for user"""
        stats = OrderService.get_order_statistics(request.user)
        return Response(stats)

    # Phase 6: Document Generation Endpoints
    @action(detail=True, methods=["get"], url_path="documents/packing-slip")
    def packing_slip(self, request, order_number=None):
        """
        Generate and return packing slip PDF for this order.
        GET /api/orders/{order_number}/documents/packing-slip/

        Convenience endpoint that retrieves the order's shipment and generates
        the packing slip document. If the order has multiple shipments, returns
        the packing slip for the first/primary shipment.

        Returns the packing slip PDF as a data URI (base64-encoded).
        """
        from shipping.services.document_service import DocumentService

        # Get order
        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get order's shipment(s)
        shipments = order.shipments.all()

        if not shipments.exists():
            return Response(
                {"success": False, "message": _("No shipment found for this order")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Use first shipment
        shipment = shipments.first()

        # Generate or retrieve packing slip
        if not shipment.packing_slip_url:
            try:
                data_uri = DocumentService.generate_packing_slip(shipment)
                shipment.packing_slip_url = data_uri
                shipment.save(update_fields=["packing_slip_url"])
            except Exception as e:
                return Response(
                    {"success": False, "error": f"Failed to generate packing slip: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "success": True,
                "document_url": shipment.packing_slip_url,
                "document_type": "packing_slip",
                "order_number": order_number,
                "shipment_id": str(shipment.id),
            }
        )

    @action(detail=True, methods=["get"], url_path="documents/commercial-invoice")
    def commercial_invoice(self, request, order_number=None):
        """
        Generate and return commercial invoice PDF for this order.
        GET /api/orders/{order_number}/documents/commercial-invoice/

        Convenience endpoint that retrieves the order's shipment and generates
        the commercial invoice document with customs data.

        Returns the commercial invoice PDF as a data URI (base64-encoded).
        """
        from shipping.services.document_service import DocumentService

        # Get order
        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get order's shipment(s)
        shipments = order.shipments.all()

        if not shipments.exists():
            return Response(
                {"success": False, "message": _("No shipment found for this order")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Use first shipment
        shipment = shipments.first()

        # Generate or retrieve commercial invoice
        if not shipment.commercial_invoice_url:
            try:
                data_uri = DocumentService.generate_commercial_invoice(shipment)
                shipment.commercial_invoice_url = data_uri
                shipment.save(update_fields=["commercial_invoice_url"])
            except Exception as e:
                return Response(
                    {"success": False, "error": f"Failed to generate commercial invoice: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(
            {
                "success": True,
                "document_url": shipment.commercial_invoice_url,
                "document_type": "commercial_invoice",
                "order_number": order_number,
                "shipment_id": str(shipment.id),
            }
        )

    # ========================================================================
    # Order Notes Endpoints
    # ========================================================================

    @extend_schema(
        tags=["Orders"],
        summary=_("List order notes"),
        description=_("Get all notes on this order that are visible to the customer."),
        responses={
            200: OpenApiResponse(description=_("List of order notes")),
            404: OpenApiResponse(description=_("Order not found")),
        },
    )
    @action(detail=True, methods=["get"], url_path="notes")
    def list_notes(self, request, order_number=None):
        """
        List all notes on an order visible to the customer.

        Returns notes marked as customer-visible, including both
        customer-submitted notes and merchant responses.
        """
        from .models import OrderNote
        from .serializers import OrderNoteSerializer

        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Get notes visible to customer (is_customer_note=True)
        notes = OrderNote.objects.filter(order=order, is_customer_note=True).order_by("-created_at")

        serializer = OrderNoteSerializer(notes, many=True, context={"request": request})

        return Response(
            {"success": True, "data": {"notes": serializer.data, "count": notes.count()}}
        )

    @extend_schema(
        tags=["Orders"],
        summary=_("Add note to order"),
        description=_("Add a customer note to an order. The merchant will be notified."),
        request=CreateOrderNoteSerializer,
        responses={
            201: OpenApiResponse(description=_("Note added successfully")),
            400: OpenApiResponse(description=_("Validation error")),
            404: OpenApiResponse(description=_("Order not found")),
        },
    )
    @action(detail=True, methods=["post"], url_path="notes/add")
    def add_note(self, request, order_number=None):
        """
        Add a customer note to an order.

        Customer notes are visible to both the customer and merchant.
        The merchant will be notified of new customer notes.
        """
        from .models import OrderNote
        from .serializers import CreateOrderNoteSerializer, OrderNoteSerializer

        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validate request data
        serializer = CreateOrderNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the note
        note = OrderNote.objects.create(
            order=order,
            author=request.user,
            note=serializer.validated_data["note"],
            is_customer_note=True,  # Customer notes are always visible
            is_read=False,  # Merchant hasn't read it yet
        )

        response_serializer = OrderNoteSerializer(note, context={"request": request})

        return Response(
            {
                "success": True,
                "message": _("Note added successfully"),
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
    list=extend_schema(tags=["Orders"]),
    create=extend_schema(tags=["Orders"]),
    retrieve=extend_schema(tags=["Orders"]),
    update=extend_schema(tags=["Orders"]),
    partial_update=extend_schema(tags=["Orders"]),
    destroy=extend_schema(tags=["Orders"]),
)
class AddressViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for address operations

    Endpoints:
    - GET /addresses/ - List user's addresses
    - POST /addresses/ - Create new address
    - GET /addresses/{id}/ - Get address details
    - PUT /addresses/{id}/ - Update address
    - DELETE /addresses/{id}/ - Delete address
    - POST /addresses/{id}/set-default/ - Set as default
    """

    serializer_class = OrderAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get addresses for current user"""
        address_type = self.request.query_params.get("type")
        return AddressService.get_user_addresses(user=self.request.user, address_type=address_type)

    def list(self, request):
        """List user's addresses"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Create new address"""
        serializer = CreateAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Validate address data
        is_valid, errors = AddressService.validate_address(serializer.validated_data)
        if not is_valid:
            return Response(
                {"success": False, "errors": errors}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create address
        success, message, address = AddressService.create_address(
            user=request.user, **serializer.validated_data
        )

        if success:
            address_serializer = OrderAddressSerializer(address)
            return Response(
                {"success": True, "message": str(message), "address": address_serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Get address details"""
        address = get_object_or_404(Address, pk=pk, user=request.user)
        serializer = self.get_serializer(address)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Update address"""
        address = get_object_or_404(Address, pk=pk, user=request.user)

        serializer = UpdateAddressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Update address
        success, message, updated_address = AddressService.update_address(
            address=address, user=request.user, **serializer.validated_data
        )

        if success:
            address_serializer = OrderAddressSerializer(updated_address or address)
            return Response(
                {"success": True, "message": str(message), "address": address_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        """Delete address"""
        address = get_object_or_404(Address, pk=pk, user=request.user)

        success, message = AddressService.delete_address(address, request.user)

        if success:
            return Response(
                {"success": True, "message": str(message)}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(tags=["Orders"])
    @action(detail=True, methods=["post"], url_path="set-default")
    def set_default(self, request, pk=None):
        """Set address as default"""
        address = get_object_or_404(Address, pk=pk, user=request.user)

        # Optional: allow changing address type when setting as default
        address_type = request.data.get("address_type")

        success, message = AddressService.set_default_address(
            address=address, user=request.user, address_type=address_type
        )

        if success:
            address_serializer = OrderAddressSerializer(address)
            return Response(
                {"success": True, "message": str(message), "address": address_serializer.data}
            )
        else:
            return Response(
                {"success": False, "message": str(message)}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(tags=["Orders"])
    @action(detail=False, methods=["get"], url_path="default")
    def get_default(self, request):
        """Get default address for user"""
        address_type = request.query_params.get("type", "both")

        address = AddressService.get_default_address(user=request.user, address_type=address_type)

        if address:
            serializer = self.get_serializer(address)
            return Response(serializer.data)
        else:
            return Response(
                {"success": False, "message": _("No default address found")},
                status=status.HTTP_404_NOT_FOUND,
            )


# Phase 7: Returns & RMA Workflow


@extend_schema_view(
    list=extend_schema(tags=["Returns"]),
    retrieve=extend_schema(tags=["Returns"]),
    create=extend_schema(tags=["Returns"]),
    update=extend_schema(tags=["Returns"]),
    partial_update=extend_schema(tags=["Returns"]),
    destroy=extend_schema(tags=["Returns"]),
)
class ReturnRequestViewSet(HeadlessAPIMixin, viewsets.ModelViewSet):
    """
    ViewSet for return request operations

    Endpoints:
    - GET /return-requests/ - List user's return requests
    - GET /return-requests/{id}/ - Get return request details
    - POST /return-requests/create-for-order/{order_number}/ - Create return request for an order
    - GET /return-requests/{id}/return-label/ - Get return shipping label
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ReturnRequestSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        """Get return requests for current user"""
        return (
            ReturnRequest.objects.filter(user=self.request.user)
            .select_related("order", "user", "refund")
            .order_by("-requested_at")
        )

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == "list":
            return ReturnRequestSummarySerializer
        elif self.action == "create_for_order":
            return CreateReturnRequestSerializer
        return ReturnRequestSerializer

    def list(self, request):
        """List user's return requests"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Get detailed return request information"""
        return_request = get_object_or_404(ReturnRequest, pk=pk, user=request.user)

        serializer = self.get_serializer(return_request)
        return Response(serializer.data)

    @extend_schema(
        tags=["Returns"],
        parameters=[
            OpenApiParameter(
                name="order_number",
                type=str,
                location=OpenApiParameter.PATH,
                description=_("Order number for which to create a return request"),
            )
        ],
    )
    @action(detail=False, methods=["post"], url_path="create-for-order/(?P<order_number>[^/.]+)")
    def create_for_order(self, request, order_number=None):
        """
        Create a return request for a specific order

        POST /api/return-requests/create-for-order/{order_number}/

        Request body:
        {
            "reason": "defective",
            "items": [
                {
                    "order_item_id": 123,
                    "quantity": 1,
                    "reason": "defective",
                    "notes": "Screen flickering"
                }
            ],
            "customer_notes": "Would like replacement if possible"
        }
        """
        # Get order
        order = OrderService.get_order_detail(order_number=order_number, user=request.user)

        if not order:
            return Response(
                {"success": False, "message": _("Order not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if order can be returned
        if order.status not in ["delivered", "completed"]:
            return Response(
                {"success": False, "message": _("Only delivered orders can be returned")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate request data
        serializer = CreateReturnRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Validate items belong to this order
        validated_items = []
        for item_data in serializer.validated_data["items"]:
            try:
                order_item = order.items.get(id=item_data["order_item_id"])

                # Validate quantity
                if item_data["quantity"] > order_item.quantity:
                    return Response(
                        {
                            "success": False,
                            "message": _(
                                "Return quantity cannot exceed ordered quantity for item %(sku)s"
                            )
                            % {"sku": order_item.sku},
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                validated_items.append(
                    {
                        "order_item_id": order_item.id,
                        "quantity": item_data["quantity"],
                        "reason": item_data["reason"],
                        "notes": item_data.get("notes", ""),
                    }
                )
            except OrderItem.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": _("Invalid order item ID: %(id)s")
                        % {"id": item_data["order_item_id"]},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Create return request
        return_request = ReturnRequest.objects.create(
            order=order,
            user=request.user,
            reason=serializer.validated_data["reason"],
            items_json=validated_items,
            customer_notes=serializer.validated_data.get("customer_notes", ""),
            status="pending",
        )

        # Send confirmation email
        from .emails import send_return_request_confirmation

        send_return_request_confirmation(return_request)

        # Return created return request
        return_serializer = ReturnRequestSerializer(return_request, context={"request": request})
        return Response(
            {
                "success": True,
                "message": _(
                    "Return request created successfully. We will review your request and send you a return label."
                ),
                "return_request": return_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(tags=["Returns"])
    @action(detail=True, methods=["get"], url_path="return-label")
    def return_label(self, request, pk=None):
        """
        Get return shipping label PDF

        GET /api/return-requests/{id}/return-label/

        Returns the return label PDF as a data URI if generated.
        """
        return_request = get_object_or_404(ReturnRequest, pk=pk, user=request.user)

        if not return_request.return_label_generated:
            return Response(
                {
                    "success": False,
                    "message": _(
                        "Return label has not been generated yet. Please wait for approval."
                    ),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not return_request.return_label_url:
            return Response(
                {"success": False, "message": _("Return label is not available")},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "success": True,
                "label_url": return_request.return_label_url,
                "tracking_number": return_request.return_tracking_number,
                "status": return_request.status,
                "return_request_id": return_request.id,
            }
        )


# ========================================
# Admin Order Editing HTMX Views
# ========================================

from decimal import Decimal, InvalidOperation

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods

from .forms import (
    OrderAddressInlineForm,
    OrderCustomerChangeForm,
    OrderVoucherApplicationForm,
    QuickOrderStatusForm,
)
from .utils import (
    add_order_item,
    apply_voucher_to_order,
    recalculate_order_totals,
    remove_order_item,
    remove_voucher_from_order,
    sync_address_to_customer,
    update_order_customer,
    update_order_item,
    validate_order_editable,
)


@staff_member_required
@require_http_methods(["POST"])
def order_item_add_view(request, order_id):
    """
    HTMX endpoint to add an item to an order
    POST /api/admin/order/{order_id}/item/add/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)

    # Check if order can be edited
    is_editable, reason = validate_order_editable(order)
    if not is_editable:
        return JsonResponse({"success": False, "message": str(reason)}, status=400)

    try:
        from djmoney.money import Money

        from catalog.models import Product, ProductVariant

        # Get form data
        product_id = request.POST.get("product")
        variant_id = request.POST.get("variant")
        quantity = request.POST.get("quantity", "1")
        unit_price = request.POST.get("unit_price")

        # Validate required fields
        if not product_id:
            return JsonResponse({"success": False, "message": _("Product is required")}, status=400)

        # Get product
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": _("Product not found")}, status=400)

        # Get variant if specified
        variant = None
        if variant_id and variant_id not in ("", "None", "null"):
            try:
                variant = ProductVariant.objects.get(pk=variant_id, product=product)
            except ProductVariant.DoesNotExist:
                return JsonResponse(
                    {"success": False, "message": _("Product variant not found")}, status=400
                )

        # Parse quantity
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError()
        except (ValueError, TypeError):
            return JsonResponse({"success": False, "message": _("Invalid quantity")}, status=400)

        # Parse unit price if provided
        unit_price_obj = None
        if unit_price:
            try:
                unit_price_obj = Money(unit_price, order.total_amount.currency)
            except Exception as e:
                logger.error(f"Error parsing unit_price '{unit_price}' for order {order_id}: {e}")
                return JsonResponse(
                    {
                        "success": False,
                        "message": _("Invalid price format: %(error)s") % {"error": str(e)},
                    },
                    status=400,
                )

        # Add item to order
        add_order_item(
            order=order,
            product=product,
            variant=variant,
            quantity=quantity,
            unit_price=unit_price_obj,
            customizations={},
        )

        # Render updated items section and totals
        items_html = render_to_string(
            "admin/orders/order/partials/items_section.html",
            {
                "order": order,
                "original": order,
            },
            request=request,
        )

        totals_html = render_to_string(
            "admin/orders/order/partials/totals_section.html",
            {
                "order": order,
            },
            request=request,
        )

        return JsonResponse(
            {
                "success": True,
                "message": _("Item added successfully"),
                "items_html": items_html,
                "totals_html": totals_html,
            }
        )

    except ValidationError as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Error adding item to order {order_id}: {e}")
        return JsonResponse(
            {"success": False, "message": _("Error adding item. Please try again.")}, status=500
        )


@staff_member_required
@require_http_methods(["POST"])
def order_item_update_view(request, order_id, item_id):
    """
    HTMX endpoint to update an order item
    POST /api/admin/order/{order_id}/item/{item_id}/update/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)
    item = get_object_or_404(OrderItem, pk=item_id, order=order)

    # Check if order can be edited
    is_editable, reason = validate_order_editable(order)
    if not is_editable:
        return JsonResponse({"success": False, "message": str(reason)}, status=400)

    try:
        quantity = request.POST.get("quantity")
        unit_price = request.POST.get("unit_price")
        discount_type = request.POST.get("discount_type")
        discount_value = request.POST.get("discount_value")
        discount_reason = request.POST.get("discount_reason")
        exclude_from_vouchers = request.POST.get("exclude_from_vouchers")

        quantity = int(quantity) if quantity else None

        if unit_price:
            from djmoney.money import Money

            unit_price = Money(unit_price, order.total_amount.currency)
        else:
            unit_price = None

        discount_value = float(discount_value) if discount_value else None

        if exclude_from_vouchers:
            exclude_from_vouchers = exclude_from_vouchers.lower() in ("true", "1", "yes")
        else:
            exclude_from_vouchers = None

        # Update item
        item = update_order_item(
            item,
            quantity=quantity,
            unit_price=unit_price,
            discount_type=discount_type,
            discount_value=discount_value,
            discount_reason=discount_reason,
            exclude_from_vouchers=exclude_from_vouchers,
        )

        # Render updated items section and totals
        items_html = render_to_string(
            "admin/orders/order/partials/items_section.html",
            {
                "order": order,
                "original": order,
            },
            request=request,
        )

        totals_html = render_to_string(
            "admin/orders/order/partials/totals_section.html",
            {
                "order": order,
            },
            request=request,
        )

        return JsonResponse(
            {
                "success": True,
                "message": _("Item updated successfully"),
                "items_html": items_html,
                "totals_html": totals_html,
            }
        )

    except ValidationError as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Error updating item {item_id} in order {order_id}: {e}")
        return JsonResponse(
            {"success": False, "message": _("Error updating item. Please try again.")}, status=500
        )


@staff_member_required
@require_http_methods(["POST"])
def order_item_remove_view(request, order_id, item_id):
    """
    HTMX endpoint to remove an item from an order
    POST /api/admin/order/{order_id}/item/{item_id}/remove/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)
    item = get_object_or_404(OrderItem, pk=item_id, order=order)

    # Check if order can be edited
    is_editable, reason = validate_order_editable(order)
    if not is_editable:
        return JsonResponse({"success": False, "message": str(reason)}, status=400)

    try:
        # Remove item
        remove_order_item(item)

        # Render updated items section and totals
        items_html = render_to_string(
            "admin/orders/order/partials/items_section.html",
            {
                "order": order,
                "original": order,
            },
            request=request,
        )

        totals_html = render_to_string(
            "admin/orders/order/partials/totals_section.html",
            {
                "order": order,
            },
            request=request,
        )

        return JsonResponse(
            {
                "success": True,
                "message": _("Item removed successfully"),
                "items_html": items_html,
                "totals_html": totals_html,
            }
        )

    except Exception as e:
        logger.error(f"Error removing item {item_id} from order {order_id}: {e}")
        return JsonResponse(
            {"success": False, "message": _("Error removing item. Please try again.")}, status=500
        )


@staff_member_required
@require_http_methods(["POST"])
def order_calculate_totals_view(request, order_id):
    """
    HTMX endpoint to recalculate order totals
    POST /api/admin/order/{order_id}/calculate-totals/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)

    try:
        # Recalculate totals
        order = recalculate_order_totals(order)
        order.save()

        # Render updated totals
        totals_html = render_to_string(
            "admin/orders/order/partials/totals_section.html",
            {
                "order": order,
            },
            request=request,
        )

        return JsonResponse(
            {
                "success": True,
                "totals_html": totals_html,
            }
        )

    except Exception as e:
        logger.error(f"Error recalculating totals for order {order_id}: {e}")
        return JsonResponse(
            {"success": False, "message": _("Error recalculating totals. Please try again.")},
            status=500,
        )


@staff_member_required
@require_http_methods(["POST"])
def order_voucher_apply_view(request, order_id):
    """
    HTMX endpoint to apply a voucher to an order
    POST /api/admin/order/{order_id}/voucher/apply/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)

    # Check if order can be edited
    is_editable, reason = validate_order_editable(order)
    if not is_editable:
        return JsonResponse({"success": False, "message": str(reason)}, status=400)

    form = OrderVoucherApplicationForm(request.POST, order=order)

    if form.is_valid():
        try:
            voucher_code = form.cleaned_data["voucher_code"]

            # Apply voucher
            success, message, voucher = apply_voucher_to_order(order, voucher_code)

            # Render updated discounts section and totals
            discounts_html = render_to_string(
                "admin/orders/order/partials/discounts_section.html",
                {
                    "order": order,
                },
                request=request,
            )

            totals_html = render_to_string(
                "admin/orders/order/partials/totals_section.html",
                {
                    "order": order,
                },
                request=request,
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": str(message),
                    "discounts_html": discounts_html,
                    "totals_html": totals_html,
                }
            )

        except ValidationError as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error applying voucher to order {order_id}: {e}")
            return JsonResponse(
                {"success": False, "message": _("Error applying voucher. Please try again.")},
                status=500,
            )
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


@staff_member_required
@require_http_methods(["POST"])
def order_voucher_remove_view(request, order_id, voucher_id):
    """
    HTMX endpoint to remove a voucher from an order
    POST /api/admin/order/{order_id}/voucher/{voucher_id}/remove/
    """
    from vouchers.models import VoucherCode

    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)
    voucher = get_object_or_404(VoucherCode, pk=voucher_id)

    # Check if order can be edited
    is_editable, reason = validate_order_editable(order)
    if not is_editable:
        return JsonResponse({"success": False, "message": str(reason)}, status=400)

    try:
        # Remove voucher
        success, message = remove_voucher_from_order(order, voucher)

        # Render updated discounts section and totals
        discounts_html = render_to_string(
            "admin/orders/order/partials/discounts_section.html",
            {
                "order": order,
            },
            request=request,
        )

        totals_html = render_to_string(
            "admin/orders/order/partials/totals_section.html",
            {
                "order": order,
            },
            request=request,
        )

        return JsonResponse(
            {
                "success": True,
                "message": str(message),
                "discounts_html": discounts_html,
                "totals_html": totals_html,
            }
        )

    except ValidationError as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)
    except Exception as e:
        logger.error(f"Error removing voucher from order {order_id}: {e}")
        return JsonResponse(
            {"success": False, "message": _("Error removing voucher. Please try again.")},
            status=500,
        )


@staff_member_required
@require_http_methods(["POST"])
def order_manual_discount_apply_view(request, order_id):
    """
    HTMX endpoint to apply a manual discount to an order
    POST /api/admin/order/{order_id}/discount/apply/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)

    # Check if order can be edited
    is_editable, reason = validate_order_editable(order)
    if not is_editable:
        return JsonResponse({"success": False, "message": str(reason)}, status=400)

    try:
        discount_type = request.POST.get("discount_type")
        discount_value = request.POST.get("discount_value")
        reason = request.POST.get("reason", "")

        # Validate inputs
        if not discount_type or not discount_value:
            return JsonResponse(
                {"success": False, "message": _("Please provide discount type and value.")},
                status=400,
            )

        try:
            discount_value = Decimal(str(discount_value))
            if discount_value < 0:
                raise ValueError("Discount value must be positive")
        except (ValueError, InvalidOperation):
            return JsonResponse(
                {"success": False, "message": _("Invalid discount value.")}, status=400
            )

        # Calculate discount amount
        from djmoney.money import Money

        if discount_type == "percentage":
            if discount_value > 100:
                return JsonResponse(
                    {"success": False, "message": _("Percentage discount cannot exceed 100%.")},
                    status=400,
                )

            # Calculate percentage discount from subtotal
            discount_amount = order.subtotal.amount * discount_value / 100
            discount_money = Money(discount_amount, order.subtotal.currency)

        elif discount_type == "fixed":
            discount_money = Money(discount_value, order.subtotal.currency)

            # Make sure discount doesn't exceed subtotal
            if discount_money > order.subtotal:
                return JsonResponse(
                    {
                        "success": False,
                        "message": _("Discount amount cannot exceed order subtotal."),
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {"success": False, "message": _("Invalid discount type.")}, status=400
            )

        # Apply the discount
        order.discount_amount = discount_money
        order.save()

        # Recalculate totals
        recalculate_order_totals(order)

        # Render updated discounts section and totals
        discounts_html = render_to_string(
            "admin/orders/order/partials/discounts_section.html",
            {
                "order": order,
            },
            request=request,
        )

        totals_html = render_to_string(
            "admin/orders/order/partials/totals_section.html",
            {
                "order": order,
            },
            request=request,
        )

        message = _("Manual discount of {discount} applied successfully.").format(
            discount=f"{discount_money.amount} {discount_money.currency}"
            if discount_type == "fixed"
            else f"{discount_value}%"
        )
        if reason:
            message += f" Reason: {reason}"

        return JsonResponse(
            {
                "success": True,
                "message": str(message),
                "discounts_html": discounts_html,
                "totals_html": totals_html,
            }
        )

    except Exception as e:
        logger.error(f"Error applying manual discount to order {order_id}: {e}")
        return JsonResponse(
            {"success": False, "message": _("Error applying discount. Please try again.")},
            status=500,
        )


def get_previous_order_addresses(user, exclude_order_id=None):
    """
    Extract unique shipping and billing addresses from customer's previous orders.

    Args:
        user: User object
        exclude_order_id: Order ID to exclude (typically the current order being edited)

    Returns:
        List of unique address dictionaries with metadata
    """
    from collections import OrderedDict

    from .models import Order

    # Get previous orders with addresses
    previous_orders = Order.objects.filter(user=user)

    if exclude_order_id:
        previous_orders = previous_orders.exclude(id=exclude_order_id)

    # Only include orders that have addresses
    previous_orders = (
        previous_orders.filter(shipping_address1__isnull=False)
        .exclude(shipping_address1="")
        .order_by("-created_at")[:50]
    )  # Limit to last 50 orders for performance

    def make_address_key(name, address1, city, state, postal_code, country):
        """Create a normalized key for deduplication"""
        return (
            (name or "").strip().lower(),
            (address1 or "").strip().lower(),
            (city or "").strip().lower(),
            (state or "").strip().lower(),
            (postal_code or "").strip().replace(" ", "").replace("-", "").lower(),
            (country or "").strip().lower(),
        )

    # Deduplicate shipping addresses
    shipping_seen = OrderedDict()
    billing_seen = OrderedDict()

    for order in previous_orders:
        # Process shipping address
        if order.shipping_address1:
            ship_key = make_address_key(
                order.shipping_name,
                order.shipping_address1,
                order.shipping_city,
                order.shipping_state,
                order.shipping_postal_code,
                order.shipping_country,
            )

            if ship_key not in shipping_seen:
                shipping_seen[ship_key] = {
                    "name": order.shipping_name or "",
                    "company": "",  # Orders don't have company field
                    "address1": order.shipping_address1 or "",
                    "address2": order.shipping_address2 or "",
                    "city": order.shipping_city or "",
                    "state": order.shipping_state or "",
                    "postal_code": order.shipping_postal_code or "",
                    "country": order.shipping_country or "",
                    "phone": order.shipping_phone
                    or order.phone
                    or "",  # Prefer shipping_phone, fallback to phone for backward compatibility
                    "last_used": order.created_at.isoformat(),
                    "order_number": order.order_number,
                    "address_type": "shipping",
                }

        # Process billing address (if not same as shipping)
        if order.billing_address1 and not order.billing_same_as_shipping:
            bill_key = make_address_key(
                order.billing_name,
                order.billing_address1,
                order.billing_city,
                order.billing_state,
                order.billing_postal_code,
                order.billing_country,
            )

            if bill_key not in billing_seen:
                billing_seen[bill_key] = {
                    "name": order.billing_name or "",
                    "company": "",
                    "address1": order.billing_address1 or "",
                    "address2": order.billing_address2 or "",
                    "city": order.billing_city or "",
                    "state": order.billing_state or "",
                    "postal_code": order.billing_postal_code or "",
                    "country": order.billing_country or "",
                    "phone": order.billing_phone
                    or order.phone
                    or "",  # Prefer billing_phone, fallback to phone for backward compatibility
                    "last_used": order.created_at.isoformat(),
                    "order_number": order.order_number,
                    "address_type": "billing",
                }

    # Combine and return (limit to 20 unique addresses total)
    all_addresses = list(shipping_seen.values()) + list(billing_seen.values())

    # Sort by last used (most recent first)
    all_addresses.sort(key=lambda x: x["last_used"], reverse=True)

    return all_addresses[:20]


@staff_member_required
@require_http_methods(["POST"])
def order_customer_update_view(request, order_id):
    """
    HTMX endpoint to update order customer
    POST /api/admin/order/{order_id}/customer/update/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)

    # Check if order can be edited
    is_editable, reason = validate_order_editable(order)
    if not is_editable:
        return JsonResponse({"success": False, "message": str(reason)}, status=400)

    form = OrderCustomerChangeForm(request.POST)

    if form.is_valid():
        try:
            customer_type = form.cleaned_data["customer_type"]
            customer_addresses = None
            has_existing_addresses = False

            # Check if order already has addresses (non-empty shipping address)
            has_existing_addresses = bool(order.shipping_address1)

            if customer_type == "existing":
                new_user = form.cleaned_data["user"]
                order = update_order_customer(order, new_user=new_user)

                # Fetch customer's addresses (prefer default, fallback to most recent)
                from .models import Address

                # Try to get default shipping address, fallback to most recent
                shipping_address = Address.objects.filter(
                    user=new_user, address_type__in=["shipping", "both"], is_default=True
                ).first()

                if not shipping_address:
                    shipping_address = (
                        Address.objects.filter(user=new_user, address_type__in=["shipping", "both"])
                        .order_by("-updated_at")
                        .first()
                    )

                # Try to get default billing address, fallback to most recent
                billing_address = Address.objects.filter(
                    user=new_user, address_type__in=["billing", "both"], is_default=True
                ).first()

                if not billing_address:
                    billing_address = (
                        Address.objects.filter(user=new_user, address_type__in=["billing", "both"])
                        .order_by("-updated_at")
                        .first()
                    )

                # Prepare address data for response
                if shipping_address or billing_address:
                    customer_addresses = {
                        "shipping": {
                            "name": shipping_address.name if shipping_address else "",
                            "address1": shipping_address.address1 if shipping_address else "",
                            "address2": shipping_address.address2 if shipping_address else "",
                            "city": shipping_address.city if shipping_address else "",
                            "state": shipping_address.state if shipping_address else "",
                            "postal_code": shipping_address.postal_code if shipping_address else "",
                            "country": shipping_address.country if shipping_address else "",
                            "phone": shipping_address.phone if shipping_address else "",
                        }
                        if shipping_address
                        else None,
                        "billing": {
                            "name": billing_address.name if billing_address else "",
                            "address1": billing_address.address1 if billing_address else "",
                            "address2": billing_address.address2 if billing_address else "",
                            "city": billing_address.city if billing_address else "",
                            "state": billing_address.state if billing_address else "",
                            "postal_code": billing_address.postal_code if billing_address else "",
                            "country": billing_address.country if billing_address else "",
                        }
                        if billing_address
                        else None,
                    }
            else:  # guest
                guest_email = form.cleaned_data["guest_email"]
                guest_phone = form.cleaned_data.get("guest_phone", "")
                order = update_order_customer(
                    order, guest_email=guest_email, guest_phone=guest_phone
                )

            # Render updated customer section
            customer_html = render_to_string(
                "admin/orders/order/partials/customer_section.html",
                {
                    "order": order,
                },
                request=request,
            )

            response_data = {
                "success": True,
                "message": _("Customer updated successfully"),
                "customer_html": customer_html,
            }

            # Include address data if available
            if customer_addresses:
                response_data["customer_addresses"] = customer_addresses
                response_data["has_existing_addresses"] = has_existing_addresses

            # Include previous order addresses for existing customers
            if customer_type == "existing" and new_user:
                previous_addresses = get_previous_order_addresses(new_user, order.id)
                if previous_addresses:
                    response_data["previous_order_addresses"] = previous_addresses

            return JsonResponse(response_data)

        except ValidationError as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error updating customer for order {order_id}: {e}")
            return JsonResponse(
                {"success": False, "message": _("Error updating customer. Please try again.")},
                status=500,
            )
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


@staff_member_required
@require_http_methods(["POST"])
def order_address_update_view(request, order_id):
    """
    HTMX endpoint to update order shipping/billing address
    POST /api/admin/order/{order_id}/address/update/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)

    # Check if order can be edited
    is_editable, reason = validate_order_editable(order)
    if not is_editable:
        return JsonResponse({"success": False, "message": str(reason)}, status=400)

    address_type = request.POST.get("address_type", "shipping")

    # Check if this is a bulk update from customer address population
    is_bulk_update = (
        "shipping_name" in request.POST
        and "billing_name" in request.POST
        or "shipping_name" in request.POST
        and request.POST.get("billing_same_as_shipping") == "true"
    )

    if is_bulk_update:
        # Handle bulk update from customer address population
        try:
            # Update shipping address
            if "shipping_name" in request.POST:
                order.shipping_name = request.POST.get("shipping_name", "")
                order.shipping_address1 = request.POST.get("shipping_address1", "")
                order.shipping_address2 = request.POST.get("shipping_address2", "")
                order.shipping_city = request.POST.get("shipping_city", "")
                order.shipping_state = request.POST.get("shipping_state", "")
                order.shipping_postal_code = request.POST.get("shipping_postal_code", "")
                order.shipping_country = request.POST.get("shipping_country", "")
                order.shipping_phone = request.POST.get("shipping_phone", "")

                # Also update legacy phone field for backward compatibility
                if request.POST.get("shipping_phone"):
                    order.phone = request.POST.get("shipping_phone")

            # Update billing address
            billing_same_as_shipping = (
                request.POST.get("billing_same_as_shipping", "false") == "true"
            )

            if billing_same_as_shipping:
                order.billing_same_as_shipping = True
                # Clear billing fields when same as shipping
                order.billing_name = ""
                order.billing_address1 = ""
                order.billing_address2 = ""
                order.billing_city = ""
                order.billing_state = ""
                order.billing_postal_code = ""
                order.billing_country = ""
                order.billing_phone = ""
            elif "billing_name" in request.POST:
                order.billing_same_as_shipping = False
                order.billing_name = request.POST.get("billing_name", "")
                order.billing_address1 = request.POST.get("billing_address1", "")
                order.billing_address2 = request.POST.get("billing_address2", "")
                order.billing_city = request.POST.get("billing_city", "")
                order.billing_state = request.POST.get("billing_state", "")
                order.billing_postal_code = request.POST.get("billing_postal_code", "")
                order.billing_country = request.POST.get("billing_country", "")
                order.billing_phone = request.POST.get("billing_phone", "")

            order.save()

            # Log the change
            OrderNote.objects.create(
                order=order,
                note=_("Customer addresses populated to order"),
                is_customer_note=False,
            )

            # Render updated address section
            addresses_html = render_to_string(
                "admin/orders/order/partials/addresses_section.html",
                {
                    "order": order,
                },
                request=request,
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": _("Addresses populated successfully"),
                    "addresses_html": addresses_html,
                    "shipping_html": addresses_html,  # For backwards compatibility
                    "billing_html": addresses_html,  # For backwards compatibility
                }
            )

        except Exception as e:
            logger.error(f"Error populating addresses for order {order_id}: {e}")
            return JsonResponse(
                {"success": False, "message": _("Error populating addresses. Please try again.")},
                status=500,
            )

    # Standard single address update with form validation
    form = OrderAddressInlineForm(request.POST, order=order, address_type=address_type)

    if form.is_valid():
        try:
            # Update order address
            if address_type == "shipping":
                order.shipping_name = form.cleaned_data["name"]
                order.shipping_address1 = form.cleaned_data["address1"]
                order.shipping_address2 = form.cleaned_data["address2"]
                order.shipping_city = form.cleaned_data["city"]
                order.shipping_state = form.cleaned_data["state"]
                order.shipping_postal_code = form.cleaned_data["postal_code"]
                order.shipping_country = form.cleaned_data["country"]
                order.shipping_phone = form.cleaned_data.get("phone", "")
                # Also update legacy phone field for backward compatibility
                order.phone = form.cleaned_data.get("phone", "")
            else:  # billing
                order.billing_name = form.cleaned_data["name"]
                order.billing_address1 = form.cleaned_data["address1"]
                order.billing_address2 = form.cleaned_data["address2"]
                order.billing_city = form.cleaned_data["city"]
                order.billing_state = form.cleaned_data["state"]
                order.billing_postal_code = form.cleaned_data["postal_code"]
                order.billing_country = form.cleaned_data["country"]
                order.billing_phone = form.cleaned_data.get("phone", "")

            order.save()

            # Optionally sync to customer addresses
            if form.cleaned_data.get("save_to_customer") and order.user:
                address_data = {
                    "name": form.cleaned_data["name"],
                    "address1": form.cleaned_data["address1"],
                    "address2": form.cleaned_data["address2"],
                    "city": form.cleaned_data["city"],
                    "state": form.cleaned_data["state"],
                    "postal_code": form.cleaned_data["postal_code"],
                    "country": form.cleaned_data["country"],
                    "phone": form.cleaned_data.get("phone", ""),
                }
                sync_address_to_customer(order.user, address_data, address_type)

            # Log the change
            OrderNote.objects.create(
                order=order,
                note=_("%(type)s address updated") % {"type": address_type.title()},
                is_customer_note=False,
            )

            # Render updated address section
            addresses_html = render_to_string(
                "admin/orders/order/partials/addresses_section.html",
                {
                    "order": order,
                },
                request=request,
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": _("Address updated successfully"),
                    "addresses_html": addresses_html,
                }
            )

        except Exception as e:
            logger.error(f"Error updating address for order {order_id}: {e}")
            return JsonResponse(
                {"success": False, "message": _("Error updating address. Please try again.")},
                status=500,
            )
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


@staff_member_required
@require_http_methods(["POST"])
def order_status_update_view(request, order_id):
    """
    HTMX endpoint to update order status
    POST /api/admin/order/{order_id}/status/update/
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    order = get_object_or_404(Order, pk=order_id)

    form = QuickOrderStatusForm(request.POST)

    if form.is_valid():
        try:
            new_status = form.cleaned_data["status"]
            send_notification = form.cleaned_data.get("send_notification", False)

            old_status = order.status
            order.status = new_status
            order.save()

            # Log the status change
            OrderNote.objects.create(
                order=order,
                note=_("Status changed from %(old)s to %(new)s")
                % {"old": old_status, "new": new_status},
                is_customer_note=False,
            )

            if send_notification:
                from django.db import transaction as db_transaction

                from .emails import send_order_status_update

                _order = order
                _old = old_status
                db_transaction.on_commit(lambda: send_order_status_update(_order, _old))

            # Render updated header section
            header_html = render_to_string(
                "admin/orders/order/partials/header_section.html",
                {
                    "order": order,
                },
                request=request,
            )

            return JsonResponse(
                {
                    "success": True,
                    "message": _("Order status updated successfully"),
                    "header_html": header_html,
                }
            )

        except Exception as e:
            logger.error(f"Error updating status for order {order_id}: {e}")
            return JsonResponse(
                {"success": False, "message": _("Error updating status. Please try again.")},
                status=500,
            )
    else:
        return JsonResponse({"success": False, "errors": form.errors}, status=400)


@staff_member_required
@require_http_methods(["GET"])
def product_search_api_view(request):
    """
    HTMX endpoint for product search (for adding items to orders)
    GET /api/admin/product-search/?q=search_term
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    from catalog.models import Product

    search_term = request.GET.get("q", "").strip()

    if len(search_term) < 2:
        return JsonResponse(
            {"success": False, "message": _("Please enter at least 2 characters to search")},
            status=400,
        )

    # Search products by name or SKU
    products = (
        Product.objects.filter(Q(name__icontains=search_term) | Q(sku__icontains=search_term))
        .select_related("category")
        .prefetch_related("variants", "images")[:20]
    )

    results = []
    for product in products:
        # Get product thumbnail
        product_thumbnail = None
        if product.images.exists():
            first_image = product.images.first()
            if first_image and hasattr(first_image, "thumbnail_small"):
                product_thumbnail = first_image.thumbnail_small

        # If product has variants, include them
        if product.variants.exists():
            for variant in product.variants.all():
                # For variants, prefer variant image over product image
                variant_thumbnail = product_thumbnail  # Default to product thumbnail
                if hasattr(variant, "image") and variant.image:
                    variant_thumbnail = variant.image.url

                # Get price amount (not formatted Money string)
                variant_price = variant.price if hasattr(variant, "price") else product.price
                price_amount = (
                    str(variant_price.amount) if hasattr(variant_price, "amount") else "0.00"
                )

                # Get stock information
                track_inventory = product.track_inventory
                available_stock = variant.available_stock if track_inventory else None

                results.append(
                    {
                        "id": f"variant_{variant.id}",
                        "product_id": product.id,
                        "variant_id": variant.id,
                        "name": f"{product.name} - {variant.name}",
                        "sku": variant.sku if hasattr(variant, "sku") else product.sku,
                        "price": price_amount,
                        "image": variant_thumbnail,
                        "has_variant": True,
                        "track_inventory": track_inventory,
                        "available_stock": available_stock,
                    }
                )
        else:
            # Product without variants
            # Get price amount (not formatted Money string)
            product_price = product.price if hasattr(product, "price") else None
            price_amount = (
                str(product_price.amount)
                if product_price and hasattr(product_price, "amount")
                else "0.00"
            )

            # Get stock information
            track_inventory = product.track_inventory
            available_stock = product.available_stock if track_inventory else None

            results.append(
                {
                    "id": f"product_{product.id}",
                    "product_id": product.id,
                    "variant_id": None,
                    "name": product.name,
                    "sku": product.sku,
                    "price": price_amount,
                    "image": product_thumbnail,
                    "has_variant": False,
                    "track_inventory": track_inventory,
                    "available_stock": available_stock,
                }
            )

    # Render search results HTML
    results_html = render_to_string(
        "admin/orders/order/partials/product_search_results.html",
        {"results": results, "search_term": search_term},
        request=request,
    )

    return JsonResponse(
        {"success": True, "results": results, "results_html": results_html, "count": len(results)}
    )


@staff_member_required
@require_http_methods(["GET"])
def customer_search_api_view(request):
    """
    AJAX endpoint for customer search
    GET /api/admin/customer-search/?q=search_term

    Searches customers by name, email, or phone number
    Returns JSON with customer data and rendered HTML
    """
    # Security: Only allow AJAX requests
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Invalid request"}, status=400)

    search_term = request.GET.get("q", "").strip()

    if not search_term or len(search_term) < 2:
        return JsonResponse({"success": True, "results": [], "results_html": "", "count": 0})

    from django.contrib.auth import get_user_model

    User = get_user_model()

    # Search customers by first name, last name, email, or phone
    customers = (
        User.objects.filter(
            Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
            | Q(email__icontains=search_term)
            | Q(username__icontains=search_term)
        )
        .filter(is_active=True)
        .exclude(
            email=""  # Exclude users without email
        )
        .order_by("email")[:20]
    )  # Limit to 20 results

    # Build results list
    results = []
    for customer in customers:
        full_name = customer.get_full_name()
        display_name = full_name if full_name else customer.email

        results.append(
            {
                "id": customer.id,
                "email": customer.email,
                "full_name": full_name,
                "display_name": display_name,
                "username": customer.username,
            }
        )

    # Render search results HTML
    results_html = render_to_string(
        "admin/orders/order/partials/customer_search_results.html",
        {"results": results, "search_term": search_term},
        request=request,
    )

    return JsonResponse(
        {"success": True, "results": results, "results_html": results_html, "count": len(results)}
    )
