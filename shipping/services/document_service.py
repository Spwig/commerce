# -*- coding: utf-8 -*-
"""
Document Service - Generate shipping documents (packing slips, invoices, customs forms).

This service handles platform-owned document generation that works independently
of provider implementations. Documents are stored as data URIs (base64-encoded PDFs).
"""
import base64
import logging
from io import BytesIO
from datetime import datetime
from decimal import Decimal
from typing import Optional
from django.utils.translation import gettext as _

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for generating shipping-related documents."""

    @staticmethod
    def _create_pdf_buffer(title: str, pagesize=letter):
        """Create a PDF buffer and document template."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=pagesize,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title=title
        )
        return buffer, doc

    @staticmethod
    def _buffer_to_data_uri(buffer: BytesIO) -> str:
        """Convert PDF buffer to data URI."""
        pdf_data = buffer.getvalue()
        b64_data = base64.b64encode(pdf_data).decode('utf-8')
        return f"data:application/pdf;base64,{b64_data}"

    @staticmethod
    def _get_styles():
        """Get common text styles for documents."""
        styles = getSampleStyleSheet()

        # Add custom styles
        styles.add(ParagraphStyle(
            name='CompanyName',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6
        ))

        styles.add(ParagraphStyle(
            name='DocumentTitle',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12
        ))

        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            spaceBefore=12
        ))

        styles.add(ParagraphStyle(
            name='Normal_Right',
            parent=styles['Normal'],
            alignment=TA_RIGHT
        ))

        return styles

    @staticmethod
    def _format_money(money_obj):
        """Format Money object for display."""
        if money_obj:
            return f"{money_obj.currency} {money_obj.amount:,.2f}"
        return ""

    @staticmethod
    def _format_address(name, address1, address2, city, state, postal_code, country):
        """Format address as multi-line string."""
        lines = [name, address1]
        if address2:
            lines.append(address2)
        lines.append(f"{city}, {state} {postal_code}")
        lines.append(country)
        return "<br/>".join(lines)

    @staticmethod
    def generate_packing_slip(shipment) -> str:
        """
        Generate a packing slip PDF for a shipment.

        Args:
            shipment: Shipment instance

        Returns:
            str: Data URI with base64-encoded PDF
        """
        from django.conf import settings

        logger.info(f"Generating packing slip for shipment {shipment.id}")

        # Create PDF
        buffer, doc = DocumentService._create_pdf_buffer(f"Packing Slip - {shipment.tracking_id}")
        styles = DocumentService._get_styles()
        story = []

        # Company header
        story.append(Paragraph(getattr(settings, 'SITE_NAME', 'Shop'), styles['CompanyName']))
        story.append(Spacer(1, 0.2*inch))

        # Document title
        story.append(Paragraph(_("Packing Slip"), styles['DocumentTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Shipment info table
        shipment_data = [
            [_("Order Number:"), str(shipment.order.order_number)],
            [_("Shipment ID:"), str(shipment.id)],
            [_("Tracking Number:"), shipment.tracking_id or _("Not assigned")],
            [_("Ship Date:"), shipment.created_at.strftime("%Y-%m-%d")],
        ]

        if shipment.carrier_preset:
            shipment_data.append([_("Carrier:"), shipment.carrier_preset.name])

        shipment_table = Table(shipment_data, colWidths=[2*inch, 4*inch])
        shipment_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(shipment_table)
        story.append(Spacer(1, 0.3*inch))

        # Shipping address
        story.append(Paragraph(_("Ship To:"), styles['SectionHeader']))
        ship_to_text = DocumentService._format_address(
            shipment.order.shipping_name,
            shipment.order.shipping_address1,
            shipment.order.shipping_address2,
            shipment.order.shipping_city,
            shipment.order.shipping_state,
            shipment.order.shipping_postal_code,
            shipment.order.shipping_country
        )
        story.append(Paragraph(ship_to_text, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))

        # Items table
        story.append(Paragraph(_("Items"), styles['SectionHeader']))

        items_data = [[_("SKU"), _("Product"), _("Quantity")]]
        for item in shipment.order.items.all():
            items_data.append([
                item.sku,
                f"{item.product_name}{' - ' + item.variant_name if item.variant_name else ''}",
                str(item.quantity)
            ])

        items_table = Table(items_data, colWidths=[1.5*inch, 3.5*inch, 1*inch])
        items_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.3*inch))

        # Footer note
        footer_text = _(
            "This packing slip is for internal use only. "
            "Please verify all items are included before shipping."
        )
        story.append(Paragraph(footer_text, styles['Normal']))

        # Build PDF
        doc.build(story)

        # Convert to data URI
        data_uri = DocumentService._buffer_to_data_uri(buffer)
        buffer.close()

        logger.info(f"Packing slip generated for shipment {shipment.id}")
        return data_uri

    @staticmethod
    def generate_commercial_invoice(shipment) -> str:
        """
        Generate a commercial invoice PDF for international shipments.

        Includes product details, customs values, HS codes, and country of origin.

        Args:
            shipment: Shipment instance

        Returns:
            str: Data URI with base64-encoded PDF
        """
        from django.conf import settings

        logger.info(f"Generating commercial invoice for shipment {shipment.id}")

        # Create PDF (A4 for international standard)
        buffer, doc = DocumentService._create_pdf_buffer(
            f"Commercial Invoice - {shipment.tracking_id}",
            pagesize=A4
        )
        styles = DocumentService._get_styles()
        story = []

        # Company header
        story.append(Paragraph(getattr(settings, 'SITE_NAME', 'Shop'), styles['CompanyName']))
        story.append(Spacer(1, 0.1*inch))

        # Document title
        story.append(Paragraph(_("Commercial Invoice"), styles['DocumentTitle']))
        story.append(Spacer(1, 0.2*inch))

        # Invoice info
        invoice_data = [
            [_("Invoice Number:"), str(shipment.order.order_number)],
            [_("Invoice Date:"), shipment.created_at.strftime("%Y-%m-%d")],
            [_("Shipment ID:"), str(shipment.id)],
            [_("Tracking Number:"), shipment.tracking_id or _("Not assigned")],
        ]

        invoice_table = Table(invoice_data, colWidths=[1.5*inch, 3*inch])
        invoice_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(invoice_table)
        story.append(Spacer(1, 0.2*inch))

        # Addresses side by side
        address_data = [
            [
                Paragraph("<b>" + _("From:") + "</b>", styles['Normal']),
                Paragraph("<b>" + _("To:") + "</b>", styles['Normal'])
            ],
            [
                Paragraph(
                    DocumentService._format_address(
                        getattr(settings, 'SITE_NAME', 'Shop'),
                        _("123 Main Street"),  # TODO: Get from store settings
                        "",
                        _("New York"),
                        _("NY"),
                        "10001",
                        shipment.origin_country
                    ),
                    styles['Normal']
                ),
                Paragraph(
                    DocumentService._format_address(
                        shipment.order.shipping_name,
                        shipment.order.shipping_address1,
                        shipment.order.shipping_address2,
                        shipment.order.shipping_city,
                        shipment.order.shipping_state,
                        shipment.order.shipping_postal_code,
                        shipment.order.shipping_country
                    ),
                    styles['Normal']
                )
            ]
        ]

        address_table = Table(address_data, colWidths=[3*inch, 3*inch])
        address_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(address_table)
        story.append(Spacer(1, 0.3*inch))

        # Items with customs data
        story.append(Paragraph(_("Item Details"), styles['SectionHeader']))

        items_data = [[
            _("Description"),
            _("HS Code"),
            _("Origin"),
            _("Qty"),
            _("Unit Value"),
            _("Total Value")
        ]]

        subtotal = Decimal('0.00')

        for item in shipment.order.items.select_related('product').all():
            product = item.product

            # Get customs data
            hs_code = product.hs_code or _("N/A")
            origin = product.country_of_origin or _("N/A")
            unit_value = product.unit_price_for_customs or item.unit_price.amount
            total_value = unit_value * item.quantity
            subtotal += total_value

            items_data.append([
                f"{item.product_name}{' - ' + item.variant_name if item.variant_name else ''}",
                hs_code,
                origin,
                str(item.quantity),
                f"{unit_value:,.2f}",
                f"{total_value:,.2f}"
            ])

        items_table = Table(items_data, colWidths=[2*inch, 0.8*inch, 0.6*inch, 0.5*inch, 0.8*inch, 0.8*inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            # Data
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Align numbers right
            ('ALIGN', (3, 1), (5, -1), 'RIGHT'),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.2*inch))

        # Totals
        totals_data = [
            [_("Subtotal:"), f"{shipment.order.subtotal.currency} {subtotal:,.2f}"],
            [_("Shipping:"), DocumentService._format_money(shipment.order.shipping_cost)],
        ]

        if shipment.order.tax_amount and shipment.order.tax_amount.amount > 0:
            totals_data.append([_("Tax:"), DocumentService._format_money(shipment.order.tax_amount)])

        totals_data.append([
            Paragraph("<b>" + _("Total:") + "</b>", styles['Normal_Right']),
            Paragraph("<b>" + DocumentService._format_money(shipment.order.total_amount) + "</b>", styles['Normal_Right'])
        ])

        totals_table = Table(totals_data, colWidths=[4.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
        ]))
        story.append(totals_table)
        story.append(Spacer(1, 0.3*inch))

        # Declaration
        declaration_text = _(
            "I hereby certify that the information on this invoice is true and correct, "
            "and that the contents of this shipment are as stated above."
        )
        story.append(Paragraph("<b>" + _("Declaration:") + "</b>", styles['Normal']))
        story.append(Paragraph(declaration_text, styles['Normal']))

        # Build PDF
        doc.build(story)

        # Convert to data URI
        data_uri = DocumentService._buffer_to_data_uri(buffer)
        buffer.close()

        logger.info(f"Commercial invoice generated for shipment {shipment.id}")
        return data_uri

    @staticmethod
    def generate_customs_form(shipment, form_type: str = 'CN22') -> str:
        """
        Generate customs declaration form (CN22 or CN23).

        CN22: For items up to 2kg and value <= €425 (small letter format)
        CN23: For items > 2kg or value > €425 (full declaration)

        Args:
            shipment: Shipment instance
            form_type: 'CN22' or 'CN23'

        Returns:
            str: Data URI with base64-encoded PDF
        """
        from django.conf import settings

        logger.info(f"Generating {form_type} customs form for shipment {shipment.id}")

        # Create PDF
        pagesize = letter if form_type == 'CN23' else (4*inch, 6*inch)
        buffer, doc = DocumentService._create_pdf_buffer(
            f"{form_type} - {shipment.tracking_id}",
            pagesize=pagesize
        )
        styles = DocumentService._get_styles()
        story = []

        # Form title
        story.append(Paragraph(f"<b>{form_type}</b> - " + _("Customs Declaration"), styles['DocumentTitle']))
        story.append(Spacer(1, 0.1*inch))

        # Sender/Recipient
        address_data = [
            [_("From:"), _("To:")],
            [
                getattr(settings, 'SITE_NAME', 'Shop') + f"<br/>{shipment.origin_country}",
                f"{shipment.order.shipping_name}<br/>{shipment.dest_country}"
            ]
        ]

        address_table = Table(address_data, colWidths=[2*inch, 2*inch])
        address_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(address_table)
        story.append(Spacer(1, 0.2*inch))

        # Contents
        story.append(Paragraph(_("Contents:"), styles['SectionHeader']))

        items_data = [[_("Description"), _("Qty"), _("Weight (g)"), _("Value"), _("Origin"), _("HS Code")]]

        total_weight = 0
        total_value = Decimal('0.00')

        for item in shipment.order.items.select_related('product').all():
            product = item.product

            # Get weight from packages or estimate
            item_weight = 0
            if shipment.packages:
                # Distribute total weight across items proportionally by quantity
                total_qty = sum(i.quantity for i in shipment.order.items.all())
                pkg_weight = sum(pkg.get('weight', 0) for pkg in shipment.packages)
                item_weight = int((pkg_weight / total_qty) * item.quantity) if total_qty > 0 else 0

            unit_value = product.unit_price_for_customs or item.unit_price.amount
            item_total = unit_value * item.quantity

            total_weight += item_weight
            total_value += item_total

            items_data.append([
                f"{item.product_name}",
                str(item.quantity),
                str(item_weight),
                f"{unit_value:,.2f}",
                product.country_of_origin or "N/A",
                product.hs_code or "N/A"
            ])

        items_table = Table(items_data, colWidths=[1.5*inch, 0.5*inch, 0.7*inch, 0.6*inch, 0.6*inch, 0.8*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.2*inch))

        # Summary
        summary_data = [
            [_("Total Weight:"), f"{total_weight}g"],
            [_("Total Value:"), f"{shipment.order.total_amount.currency} {total_value:,.2f}"],
            [_("Category:"), _("Merchandise")],  # TODO: Allow configuration
        ]

        summary_table = Table(summary_data, colWidths=[1.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.2*inch))

        # Declaration
        declaration_text = _(
            "I certify that the particulars given in this declaration are correct and "
            "that this item does not contain any dangerous article prohibited by legislation "
            "or by postal or customs regulations."
        )
        story.append(Paragraph("<i>" + declaration_text + "</i>", styles['Normal']))

        # Build PDF
        doc.build(story)

        # Convert to data URI
        data_uri = DocumentService._buffer_to_data_uri(buffer)
        buffer.close()

        logger.info(f"{form_type} customs form generated for shipment {shipment.id}")
        return data_uri

    @staticmethod
    def generate_return_label(return_request):
        """
        Generate a return shipping label PDF for a return request.

        Phase 7: Returns & RMA Workflow

        Args:
            return_request: ReturnRequest instance

        Returns:
            str: Data URI containing base64-encoded PDF

        Raises:
            ValueError: If return request is missing required data
        """
        from orders.models import ReturnRequest

        if not isinstance(return_request, ReturnRequest):
            raise ValueError("Invalid return_request instance")

        if not return_request.order:
            raise ValueError("Return request must have an associated order")

        logger.info(f"Generating return label for return request {return_request.id}")

        order = return_request.order
        styles = DocumentService._get_styles()

        # Create PDF
        buffer, doc = DocumentService._create_pdf_buffer(
            f"Return_Label_{return_request.id}",
            pagesize=letter
        )

        story = []

        # Title
        title = Paragraph(_("RETURN SHIPPING LABEL"), styles['CompanyName'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))

        # RMA Number (prominent display)
        rma_number = f"RMA-{return_request.id}"
        rma_paragraph = Paragraph(
            f"<b>{_('RMA Number:')} {rma_number}</b>",
            ParagraphStyle(
                name='RMANumber',
                fontSize=16,
                textColor=colors.HexColor('#e74c3c'),
                spaceAfter=12
            )
        )
        story.append(rma_paragraph)
        story.append(Spacer(1, 0.2*inch))

        # Return tracking number (if available)
        if return_request.return_tracking_number:
            tracking_paragraph = Paragraph(
                f"<b>{_('Tracking Number:')} {return_request.return_tracking_number}</b>",
                styles['Heading3']
            )
            story.append(tracking_paragraph)
            story.append(Spacer(1, 0.1*inch))

        # Two-column layout: Return To (merchant) and Ship From (customer)
        addresses_data = []

        # Return To address (merchant/warehouse)
        # TODO: Get from Site Settings or Warehouse Location
        return_to_text = f"""
        <b>{_('RETURN TO:')}</b><br/>
        <b>Your Company Name</b><br/>
        Returns Department<br/>
        123 Warehouse Street<br/>
        City, State 12345<br/>
        United States
        """

        # Ship From address (customer)
        ship_from = DocumentService._format_address(
            order.shipping_name,
            order.shipping_address1,
            order.shipping_address2,
            order.shipping_city,
            order.shipping_state,
            order.shipping_postal_code,
            order.shipping_country
        )
        ship_from_text = f"""
        <b>{_('SHIP FROM:')}</b><br/>
        {ship_from.replace(chr(10), '<br/>')}
        """

        addresses_data.append([
            Paragraph(return_to_text, styles['Normal']),
            Paragraph(ship_from_text, styles['Normal'])
        ])

        addresses_table = Table(addresses_data, colWidths=[3.5*inch, 3.5*inch])
        addresses_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOX', (0, 0), (0, 0), 1, colors.black),
            ('BOX', (1, 0), (1, 0), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(addresses_table)
        story.append(Spacer(1, 0.3*inch))

        # Items being returned
        story.append(Paragraph(_("Items Being Returned"), styles['SectionHeader']))

        items_data = [[_("Item"), _("SKU"), _("Quantity"), _("Reason")]]

        for item_data in return_request.items_json:
            try:
                order_item = order.items.get(id=item_data['order_item_id'])
                items_data.append([
                    order_item.product_name[:40],  # Truncate long names
                    order_item.sku,
                    str(item_data.get('quantity', 0)),
                    item_data.get('reason', '—')[:20]  # Truncate
                ])
            except Exception as e:
                logger.warning(f"Could not retrieve order item {item_data.get('order_item_id')}: {e}")
                continue

        items_table = Table(items_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 2*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(items_table)
        story.append(Spacer(1, 0.3*inch))

        # Return instructions
        story.append(Paragraph(_("Return Instructions"), styles['SectionHeader']))
        instructions_text = _(
            "1. Pack all items securely in their original packaging if possible.<br/>"
            "2. Include this return label inside the package.<br/>"
            "3. Affix the shipping label to the outside of the package.<br/>"
            "4. Drop off at any authorized shipping location.<br/>"
            "5. Keep your tracking number for your records."
        )
        story.append(Paragraph(instructions_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

        # Customer notes (if provided)
        if return_request.customer_notes:
            story.append(Paragraph(_("Customer Notes"), styles['SectionHeader']))
            notes_paragraph = Paragraph(return_request.customer_notes[:500], styles['Normal'])
            story.append(notes_paragraph)
            story.append(Spacer(1, 0.2*inch))

        # Footer with order and request info
        footer_data = [
            [_("Original Order:"), order.order_number],
            [_("Request Date:"), return_request.requested_at.strftime("%Y-%m-%d")],
            [_("Reason:"), return_request.get_reason_display()],
        ]

        footer_table = Table(footer_data, colWidths=[1.5*inch, 3*inch])
        footer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#7f8c8d')),
        ]))
        story.append(footer_table)

        # Build PDF
        doc.build(story)

        # Convert to data URI
        data_uri = DocumentService._buffer_to_data_uri(buffer)
        buffer.close()

        logger.info(f"Return label generated for return request {return_request.id}")
        return data_uri
