"""
Admin API Document Generation Views

PDF document generation endpoints: invoices, packing slips, pick lists,
and batch document ZIP downloads.
"""

import logging
import secrets
import zipfile
from io import BytesIO

from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, extend_schema
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from admin_api.permissions import category_permission
from admin_api.serializers.auth import ErrorResponseSerializer
from admin_api.serializers.bulk_operations import BatchDocumentsSerializer
from admin_api.throttling import AdminAPIThrottle
from core.api.api_descriptions import AUTH_REQUIRED, PERMISSION_DENIED, RATE_LIMIT_EXCEEDED
from core.models import SiteSettings
from orders.models import Order

logger = logging.getLogger(__name__)


def generate_error_reference():
    """Generate a unique error reference for debugging."""
    return f"ERR-{secrets.token_hex(3).upper()}"


def _get_site_settings():
    """Get SiteSettings singleton, returning None if not configured."""
    try:
        return SiteSettings.objects.first()
    except Exception:
        return None


def _get_styles():
    """Get common text styles for documents."""
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="CompanyName",
            parent=styles["Heading1"],
            fontSize=18,
            textColor=colors.HexColor("#2c3e50"),
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="DocumentTitle",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#34495e"),
            spaceAfter=12,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeader",
            parent=styles["Heading3"],
            fontSize=11,
            textColor=colors.HexColor("#2c3e50"),
            spaceAfter=6,
            spaceBefore=12,
        )
    )

    styles.add(ParagraphStyle(name="Normal_Right", parent=styles["Normal"], alignment=TA_RIGHT))

    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["Normal"],
            fontSize=8,
            textColor=colors.HexColor("#7f8c8d"),
        )
    )

    return styles


def _format_money(money_obj):
    """Format Money object for display."""
    if money_obj and hasattr(money_obj, "amount"):
        return f"{money_obj.currency} {money_obj.amount:,.2f}"
    return ""


def _format_address(name, address1, address2, city, state, postal_code, country):
    """Format address as multi-line HTML string."""
    lines = [name, address1]
    if address2:
        lines.append(address2)
    lines.append(f"{city}, {state} {postal_code}")
    lines.append(country)
    return "<br/>".join(line for line in lines if line)


def _create_pdf_buffer(title, pagesize=letter):
    """Create a PDF buffer and document template."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title=title,
    )
    return buffer, doc


def _build_store_header(styles, site_settings):
    """Build store branding header elements."""
    elements = []

    store_name = "Store"
    if site_settings:
        store_name = site_settings.site_name or "Store"

    elements.append(Paragraph(store_name, styles["CompanyName"]))

    # Store address
    if site_settings:
        address_parts = []
        if getattr(site_settings, "address_line_1", ""):
            address_parts.append(site_settings.address_line_1)
        if getattr(site_settings, "address_line_2", ""):
            address_parts.append(site_settings.address_line_2)
        city_state = []
        if getattr(site_settings, "city", ""):
            city_state.append(site_settings.city)
        if getattr(site_settings, "state_province", ""):
            city_state.append(site_settings.state_province)
        if city_state:
            postal = getattr(site_settings, "postal_code", "")
            address_parts.append(f"{', '.join(city_state)} {postal}".strip())
        if getattr(site_settings, "country", ""):
            address_parts.append(site_settings.country)

        if address_parts:
            elements.append(Paragraph("<br/>".join(address_parts), styles["Normal"]))

        # Contact info
        contact_parts = []
        if getattr(site_settings, "phone_number", ""):
            contact_parts.append(f"Tel: {site_settings.phone_number}")
        if getattr(site_settings, "admin_email", ""):
            contact_parts.append(site_settings.admin_email)
        if contact_parts:
            elements.append(Paragraph(" | ".join(contact_parts), styles["SmallText"]))

    elements.append(Spacer(1, 0.2 * inch))
    return elements


def _generate_invoice_pdf(order, site_settings=None):
    """
    Generate invoice PDF for an order.
    Returns raw PDF bytes.
    """
    if site_settings is None:
        site_settings = _get_site_settings()

    buffer, doc = _create_pdf_buffer(f"Invoice - {order.order_number}")
    styles = _get_styles()
    story = []

    # Store header
    story.extend(_build_store_header(styles, site_settings))

    # Document title
    story.append(Paragraph(_("INVOICE"), styles["DocumentTitle"]))
    story.append(Spacer(1, 0.2 * inch))

    # Invoice metadata table
    invoice_info = [
        [_("Invoice Number:"), order.order_number],
        [_("Invoice Date:"), order.created_at.strftime("%Y-%m-%d")],
        [_("Order Status:"), order.get_status_display()],
        [_("Payment Status:"), order.get_payment_status_display()],
    ]

    # Tax ID if available
    tax_id = getattr(site_settings, "tax_id", "") if site_settings else ""
    if tax_id:
        invoice_info.append([_("Tax ID:"), tax_id])

    info_table = Table(invoice_info, colWidths=[2 * inch, 4 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 0.3 * inch))

    # Billing and shipping addresses side by side
    billing_address = _format_address(
        order.billing_name or order.shipping_name,
        order.billing_address1 or order.shipping_address1,
        order.billing_address2 or order.shipping_address2,
        order.billing_city or order.shipping_city,
        order.billing_state or order.shipping_state,
        order.billing_postal_code or order.shipping_postal_code,
        order.billing_country or order.shipping_country,
    )
    shipping_address = _format_address(
        order.shipping_name,
        order.shipping_address1,
        order.shipping_address2,
        order.shipping_city,
        order.shipping_state,
        order.shipping_postal_code,
        order.shipping_country,
    )

    address_data = [
        [
            Paragraph("<b>" + _("Bill To:") + "</b>", styles["Normal"]),
            Paragraph("<b>" + _("Ship To:") + "</b>", styles["Normal"]),
        ],
        [
            Paragraph(billing_address, styles["Normal"]),
            Paragraph(shipping_address, styles["Normal"]),
        ],
    ]

    address_table = Table(address_data, colWidths=[3 * inch, 3 * inch])
    address_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(address_table)
    story.append(Spacer(1, 0.3 * inch))

    # Line items
    story.append(Paragraph(_("Items"), styles["SectionHeader"]))

    items_header = [_("SKU"), _("Product"), _("Qty"), _("Unit Price"), _("Total")]
    items_data = [items_header]

    for item in order.items.all():
        product_desc = item.product_name
        if item.variant_name:
            product_desc += f" - {item.variant_name}"

        items_data.append(
            [
                item.sku,
                product_desc,
                str(item.quantity),
                _format_money(item.unit_price),
                _format_money(item.total_price),
            ]
        )

    items_table = Table(
        items_data, colWidths=[1 * inch, 2.5 * inch, 0.5 * inch, 1 * inch, 1 * inch]
    )
    items_table.setStyle(
        TableStyle(
            [
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                # Data rows
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("TOPPADDING", (0, 1), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                # Right-align price columns
                ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
            ]
        )
    )
    story.append(items_table)
    story.append(Spacer(1, 0.2 * inch))

    # Totals
    totals_data = [
        [_("Subtotal:"), _format_money(order.subtotal)],
    ]

    if order.discount_amount and order.discount_amount.amount > 0:
        totals_data.append([_("Discount:"), f"-{_format_money(order.discount_amount)}"])

    if order.shipping_cost and order.shipping_cost.amount > 0:
        totals_data.append([_("Shipping:"), _format_money(order.shipping_cost)])

    if order.tax_amount and order.tax_amount.amount > 0:
        totals_data.append([_("Tax:"), _format_money(order.tax_amount)])

    # Total row with bold
    totals_data.append(
        [
            Paragraph("<b>" + _("Total:") + "</b>", styles["Normal_Right"]),
            Paragraph("<b>" + _format_money(order.total_amount) + "</b>", styles["Normal_Right"]),
        ]
    )

    totals_table = Table(totals_data, colWidths=[4.5 * inch, 1.5 * inch])
    totals_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -2), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
            ]
        )
    )
    story.append(totals_table)
    story.append(Spacer(1, 0.3 * inch))

    # Invoice footer
    invoice_footer = getattr(site_settings, "invoice_footer_text", "") if site_settings else ""
    if invoice_footer:
        story.append(Paragraph(invoice_footer, styles["SmallText"]))

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def _generate_packing_slip_pdf(order, site_settings=None):
    """
    Generate packing slip PDF for an order.
    Items and quantities only, NO pricing.
    Returns raw PDF bytes.
    """
    if site_settings is None:
        site_settings = _get_site_settings()

    buffer, doc = _create_pdf_buffer(f"Packing Slip - {order.order_number}")
    styles = _get_styles()
    story = []

    # Store header
    story.extend(_build_store_header(styles, site_settings))

    # Document title
    story.append(Paragraph(_("PACKING SLIP"), styles["DocumentTitle"]))
    story.append(Spacer(1, 0.2 * inch))

    # Order info
    order_info = [
        [_("Order Number:"), order.order_number],
        [_("Order Date:"), order.created_at.strftime("%Y-%m-%d")],
    ]
    if order.tracking_number:
        order_info.append([_("Tracking Number:"), order.tracking_number])

    info_table = Table(order_info, colWidths=[2 * inch, 4 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 0.3 * inch))

    # Ship To address
    story.append(Paragraph(_("Ship To:"), styles["SectionHeader"]))
    ship_to_text = _format_address(
        order.shipping_name,
        order.shipping_address1,
        order.shipping_address2,
        order.shipping_city,
        order.shipping_state,
        order.shipping_postal_code,
        order.shipping_country,
    )
    story.append(Paragraph(ship_to_text, styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Items table (NO pricing)
    story.append(Paragraph(_("Items"), styles["SectionHeader"]))

    items_data = [[_("SKU"), _("Product"), _("Variant"), _("Quantity")]]
    for item in order.items.all():
        items_data.append(
            [item.sku, item.product_name, item.variant_name or "-", str(item.quantity)]
        )

    items_table = Table(items_data, colWidths=[1.2 * inch, 2.5 * inch, 1.3 * inch, 1 * inch])
    items_table.setStyle(
        TableStyle(
            [
                # Header
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                # Data
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("TOPPADDING", (0, 1), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(items_table)
    story.append(Spacer(1, 0.3 * inch))

    # Packing slip footer
    packing_footer = getattr(site_settings, "packing_slip_footer_text", "") if site_settings else ""
    if packing_footer:
        story.append(Paragraph(packing_footer, styles["SmallText"]))
    else:
        story.append(
            Paragraph(
                _("Please verify all items are included before shipping."), styles["SmallText"]
            )
        )

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


def _generate_pick_list_pdf(order, site_settings=None):
    """
    Generate pick list PDF for an order.
    Organized by warehouse location with SKU, product name, quantity, variant.
    Returns raw PDF bytes.
    """
    if site_settings is None:
        site_settings = _get_site_settings()

    buffer, doc = _create_pdf_buffer(f"Pick List - {order.order_number}")
    styles = _get_styles()
    story = []

    # Store header (minimal)
    store_name = site_settings.site_name if site_settings else "Store"
    story.append(Paragraph(store_name, styles["CompanyName"]))
    story.append(Spacer(1, 0.1 * inch))

    # Document title
    story.append(Paragraph(_("PICK LIST"), styles["DocumentTitle"]))
    story.append(Spacer(1, 0.2 * inch))

    # Order info
    order_info = [
        [_("Order Number:"), order.order_number],
        [_("Order Date:"), order.created_at.strftime("%Y-%m-%d")],
        [_("Customer:"), order.shipping_name],
    ]
    info_table = Table(order_info, colWidths=[2 * inch, 4 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 0.3 * inch))

    # Group items by warehouse
    items_by_warehouse = {}
    for item in order.items.select_related("warehouse").all():
        warehouse_name = item.warehouse.name if item.warehouse else _("Default Warehouse")
        if warehouse_name not in items_by_warehouse:
            items_by_warehouse[warehouse_name] = []
        items_by_warehouse[warehouse_name].append(item)

    # If no warehouse assignment, group all under default
    if not items_by_warehouse:
        items_by_warehouse[_("Default Warehouse")] = list(order.items.all())

    for warehouse_name, items in items_by_warehouse.items():
        story.append(Paragraph(f"{_('Warehouse')}: {warehouse_name}", styles["SectionHeader"]))

        pick_data = [[_("SKU"), _("Product"), _("Variant"), _("Qty"), _("Picked")]]
        for item in items:
            pick_data.append(
                [
                    item.sku,
                    item.product_name,
                    item.variant_name or "-",
                    str(item.quantity),
                    "[ ]",  # Checkbox placeholder for warehouse staff
                ]
            )

        pick_table = Table(
            pick_data, colWidths=[1.2 * inch, 2.3 * inch, 1.2 * inch, 0.6 * inch, 0.7 * inch]
        )
        pick_table.setStyle(
            TableStyle(
                [
                    # Header
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#34495e")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    # Data
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 9),
                    ("TOPPADDING", (0, 1), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (3, 0), (4, -1), "CENTER"),
                ]
            )
        )
        story.append(pick_table)
        story.append(Spacer(1, 0.2 * inch))

    # Picker signature line
    story.append(Spacer(1, 0.5 * inch))
    story.append(
        Paragraph(
            _("Picked by: ____________________  Date: ____________________"), styles["Normal"]
        )
    )

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


# =============================================================================
# API Endpoints
# =============================================================================


@extend_schema(
    tags=["Admin - Documents"],
    summary=_("Generate order invoice PDF"),
    description=_("""
    Generate an invoice PDF for a specific order.

    **Rate Limit:** 300 requests per minute

    Returns a PDF file with:
    - Store branding (name, address, contact info)
    - Order details and dates
    - Billing and shipping addresses
    - Line items with pricing
    - Subtotals, discounts, shipping, tax, and total
    """),
    responses={
        200: OpenApiResponse(description=_("PDF file download")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        404: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("orders", "view")])
@throttle_classes([AdminAPIThrottle])
def order_invoice_pdf(request, order_number):
    """
    Generate and return an invoice PDF for the specified order.
    """
    try:
        order = Order.objects.prefetch_related("items").get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        pdf_bytes = _generate_invoice_pdf(order)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="invoice_{order.order_number}.pdf"'
        return response

    except Exception as e:
        logger.error(f"Invoice PDF generation failed for order {order_number}: {e}", exc_info=True)
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to generate invoice PDF."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    tags=["Admin - Documents"],
    summary=_("Generate order packing slip PDF"),
    description=_("""
    Generate a packing slip PDF for a specific order.

    **Rate Limit:** 300 requests per minute

    Returns a PDF file with:
    - Store branding
    - Order and shipping details
    - Items with quantities and variants (NO pricing)
    """),
    responses={
        200: OpenApiResponse(description=_("PDF file download")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        404: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("orders", "view")])
@throttle_classes([AdminAPIThrottle])
def order_packing_slip_pdf(request, order_number):
    """
    Generate and return a packing slip PDF for the specified order.
    """
    try:
        order = Order.objects.prefetch_related("items").get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        pdf_bytes = _generate_packing_slip_pdf(order)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="packing_slip_{order.order_number}.pdf"'
        )
        return response

    except Exception as e:
        logger.error(
            f"Packing slip PDF generation failed for order {order_number}: {e}", exc_info=True
        )
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to generate packing slip PDF."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    tags=["Admin - Documents"],
    summary=_("Generate order pick list PDF"),
    description=_("""
    Generate a pick list PDF for a specific order.

    **Rate Limit:** 300 requests per minute

    Returns a PDF file organized by warehouse with:
    - SKU, product name, variant, quantity
    - Checkbox column for warehouse staff
    - Signature line for verification
    """),
    responses={
        200: OpenApiResponse(description=_("PDF file download")),
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        404: ErrorResponseSerializer,
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["GET"])
@permission_classes([category_permission("orders", "view")])
@throttle_classes([AdminAPIThrottle])
def order_pick_list_pdf(request, order_number):
    """
    Generate and return a pick list PDF for the specified order.
    """
    try:
        order = Order.objects.prefetch_related("items", "items__warehouse").get(
            order_number=order_number
        )
    except Order.DoesNotExist:
        return Response(
            {
                "success": False,
                "error": {
                    "code": 404,
                    "message": _("Order not found."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        pdf_bytes = _generate_pick_list_pdf(order)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="pick_list_{order.order_number}.pdf"'
        )
        return response

    except Exception as e:
        logger.error(
            f"Pick list PDF generation failed for order {order_number}: {e}", exc_info=True
        )
        return Response(
            {
                "success": False,
                "error": {
                    "code": 500,
                    "message": _("Failed to generate pick list PDF."),
                    "reference": generate_error_reference(),
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema(
    tags=["Admin - Documents"],
    summary=_("Batch generate documents as ZIP"),
    description=_("""
    Generate multiple document types for multiple orders and package them as a ZIP file.

    **Rate Limit:** 300 requests per minute

    Maximum 50 orders per request. Available document types:
    - invoice: Full invoice with pricing
    - packing_slip: Items and quantities without pricing
    - pick_list: Warehouse pick list organized by location

    Returns a ZIP file containing all generated PDFs, organized by order number.
    """),
    request=BatchDocumentsSerializer,
    responses={
        200: OpenApiResponse(description=_("ZIP file download")),
        400: ErrorResponseSerializer,
        401: OpenApiResponse(description=AUTH_REQUIRED),
        403: OpenApiResponse(description=PERMISSION_DENIED),
        429: OpenApiResponse(description=RATE_LIMIT_EXCEEDED),
    },
)
@api_view(["POST"])
@permission_classes([category_permission("orders", "view")])
@throttle_classes([AdminAPIThrottle])
def batch_documents(request):
    """
    Generate batch documents for multiple orders as a ZIP download.
    """
    serializer = BatchDocumentsSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("Invalid batch document request."),
                    "reference": generate_error_reference(),
                    "details": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    order_numbers = serializer.validated_data["order_numbers"]
    document_types = serializer.validated_data["document_types"]

    # Pre-fetch site settings once for all documents
    site_settings = _get_site_settings()

    # Generator function map
    generators = {
        "invoice": _generate_invoice_pdf,
        "packing_slip": _generate_packing_slip_pdf,
        "pick_list": _generate_pick_list_pdf,
    }

    # Create ZIP in memory
    zip_buffer = BytesIO()
    errors = []

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for order_number in order_numbers:
            try:
                order = Order.objects.prefetch_related("items", "items__warehouse").get(
                    order_number=order_number
                )

                for doc_type in document_types:
                    try:
                        generator = generators[doc_type]
                        pdf_bytes = generator(order, site_settings=site_settings)

                        filename = f"{order_number}/{doc_type}_{order_number}.pdf"
                        zip_file.writestr(filename, pdf_bytes)

                    except Exception as e:
                        logger.error(
                            f"Batch document generation failed for {order_number}/{doc_type}: {e}",
                            exc_info=True,
                        )
                        errors.append(
                            {
                                "order_number": order_number,
                                "document_type": doc_type,
                                "error": str(e),
                            }
                        )

            except Order.DoesNotExist:
                errors.append(
                    {
                        "order_number": order_number,
                        "document_type": "all",
                        "error": _("Order not found."),
                    }
                )

    zip_buffer.seek(0)
    zip_bytes = zip_buffer.getvalue()
    zip_buffer.close()

    if not zip_bytes or len(zip_bytes) <= 22:
        # Empty ZIP file (22 bytes = empty zip header)
        return Response(
            {
                "success": False,
                "error": {
                    "code": 400,
                    "message": _("No documents could be generated."),
                    "reference": generate_error_reference(),
                    "details": errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    response = HttpResponse(zip_bytes, content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="order_documents.zip"'
    return response
