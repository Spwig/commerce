"""
Analytics Export Service for Admin API

Generates CSV and PDF exports for analytics reports.
Uses ReportLab for PDF generation (same pattern as shipping/services/document_service.py).
"""
import csv
import logging
from io import BytesIO, StringIO
from decimal import Decimal
from datetime import date, datetime

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from admin_api.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)


class AnalyticsExportService:
    """
    Service for exporting analytics data as CSV or PDF files.
    """

    # ------------------------------------------------------------------ #
    #  PDF helpers (mirrors DocumentService pattern)
    # ------------------------------------------------------------------ #
    @staticmethod
    def _create_pdf_buffer(title: str, pagesize=letter):
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

    @staticmethod
    def _get_styles():
        """Get common text styles for reports."""
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
        ))

        styles.add(ParagraphStyle(
            name='ReportSubtitle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
        ))

        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading3'],
            fontSize=11,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            spaceBefore=12,
        ))

        styles.add(ParagraphStyle(
            name='Normal_Right',
            parent=styles['Normal'],
            alignment=TA_RIGHT,
        ))

        styles.add(ParagraphStyle(
            name='SmallText',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7f8c8d'),
        ))

        return styles

    @staticmethod
    def _format_decimal(value):
        """Format a Decimal or numeric value for display."""
        if value is None:
            return '0.00'
        if isinstance(value, Decimal):
            return f'{value:,.2f}'
        return f'{float(value):,.2f}'

    @staticmethod
    def _build_table(header_row, data_rows, col_widths=None):
        """Build a styled ReportLab Table with standard analytics styling."""
        all_rows = [header_row] + data_rows

        table = Table(all_rows, colWidths=col_widths)
        style_commands = [
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 6),
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        # Alternate row shading
        for i in range(1, len(all_rows)):
            if i % 2 == 0:
                style_commands.append(
                    ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8f9fa'))
                )

        table.setStyle(TableStyle(style_commands))
        return table

    # ================================================================== #
    #  CSV Export
    # ================================================================== #
    @classmethod
    def export_csv(cls, report_type: str, start_date: date, end_date: date) -> str:
        """
        Export analytics data as a CSV string.

        Args:
            report_type: One of 'products', 'customers', 'categories', 'brands',
                        'orders', 'summary'
            start_date: Start date for the report range
            end_date: End date for the report range

        Returns:
            CSV content as a string
        """
        output = StringIO()
        writer = csv.writer(output)

        if report_type == 'products':
            cls._csv_products(writer, start_date, end_date)
        elif report_type == 'customers':
            cls._csv_customers(writer, start_date, end_date)
        elif report_type == 'categories':
            cls._csv_categories(writer, start_date, end_date)
        elif report_type == 'brands':
            cls._csv_brands(writer, start_date, end_date)
        elif report_type == 'orders':
            cls._csv_orders(writer, start_date, end_date)
        elif report_type == 'summary':
            cls._csv_summary(writer, start_date, end_date)
        else:
            writer.writerow(['Error', f'Unknown report type: {report_type}'])

        return output.getvalue()

    @classmethod
    def _csv_products(cls, writer, start_date, end_date):
        """Write product analytics CSV rows."""
        data = AnalyticsService.get_product_analytics(
            start_date, end_date, page_size=10000
        )
        currency = data['currency']

        writer.writerow([
            f'Product Analytics Report ({start_date} to {end_date})'
        ])
        writer.writerow([
            f'Currency: {currency}',
            f'Total Revenue: {cls._format_decimal(data["summary"]["total_revenue"])}',
            f'Total Units: {data["summary"]["total_units"]}',
            f'Products Sold: {data["summary"]["total_products_sold"]}',
        ])
        writer.writerow([])

        writer.writerow([
            'Product Name', 'SKU', 'Category', 'Brand',
            'Units Sold', f'Revenue ({currency})', 'Orders',
            'Returns', 'Return Rate (%)', f'Avg Price ({currency})',
        ])

        for product in data['products']:
            writer.writerow([
                product['product_name'],
                product['sku'],
                product['category_name'],
                product['brand_name'],
                product['units_sold'],
                cls._format_decimal(product['revenue']),
                product['orders_count'],
                product['returns_count'],
                cls._format_decimal(product['return_rate']),
                cls._format_decimal(product['average_selling_price']),
            ])

    @classmethod
    def _csv_customers(cls, writer, start_date, end_date):
        """Write customer analytics CSV rows."""
        data = AnalyticsService.get_customer_analytics(
            start_date, end_date, page_size=10000
        )
        currency = data['currency']
        summary = data['summary']

        writer.writerow([
            f'Customer Analytics Report ({start_date} to {end_date})'
        ])
        writer.writerow([
            f'Total Customers: {summary["total_customers"]}',
            f'New: {summary["new_customers"]}',
            f'Returning: {summary["returning_customers"]}',
            f'Avg LTV: {cls._format_decimal(summary["average_ltv"])} {currency}',
        ])
        writer.writerow([])

        # Top customers
        writer.writerow([
            'Customer Name', 'Email', 'Segment', f'Total Spent ({currency})',
            'Total Orders', f'Period Spent ({currency})', 'Period Orders', 'Joined',
        ])

        for customer in data['top_customers']:
            writer.writerow([
                customer['name'],
                customer['email'],
                customer['segment'],
                cls._format_decimal(customer['total_spent']),
                customer['total_orders'],
                cls._format_decimal(customer['range_spent']),
                customer['range_orders'],
                customer.get('joined', ''),
            ])

        # Geo breakdown
        writer.writerow([])
        writer.writerow(['--- Geographic Breakdown ---'])
        writer.writerow(['Country', 'Orders', f'Revenue ({currency})', 'Customers'])
        for geo in data['geo_breakdown']:
            writer.writerow([
                geo['country'],
                geo['order_count'],
                cls._format_decimal(geo['revenue']),
                geo['customer_count'],
            ])

    @classmethod
    def _csv_categories(cls, writer, start_date, end_date):
        """Write category analytics CSV rows."""
        data = AnalyticsService.get_category_analytics(start_date, end_date)
        currency = data['currency']

        writer.writerow([
            f'Category Analytics Report ({start_date} to {end_date})'
        ])
        writer.writerow([
            f'Currency: {currency}',
            f'Total Revenue: {cls._format_decimal(data["summary"]["total_revenue"])}',
            f'Total Units: {data["summary"]["total_units"]}',
            f'Categories: {data["summary"]["total_categories"]}',
        ])
        writer.writerow([])

        writer.writerow([
            'Category', f'Revenue ({currency})', 'Revenue %',
            'Units Sold', 'Orders', 'Products',
        ])

        for cat in data['categories']:
            writer.writerow([
                cat['category_name'],
                cls._format_decimal(cat['revenue']),
                cls._format_decimal(cat['revenue_percentage']),
                cat['units_sold'],
                cat['orders_count'],
                cat['products_count'],
            ])

    @classmethod
    def _csv_brands(cls, writer, start_date, end_date):
        """Write brand analytics CSV rows."""
        data = AnalyticsService.get_brand_analytics(start_date, end_date)
        currency = data['currency']

        writer.writerow([
            f'Brand Analytics Report ({start_date} to {end_date})'
        ])
        writer.writerow([
            f'Currency: {currency}',
            f'Total Revenue: {cls._format_decimal(data["summary"]["total_revenue"])}',
            f'Total Units: {data["summary"]["total_units"]}',
            f'Brands: {data["summary"]["total_brands"]}',
        ])
        writer.writerow([])

        writer.writerow([
            'Brand', f'Revenue ({currency})', 'Revenue %',
            'Units Sold', 'Orders', 'Products',
        ])

        for brand in data['brands']:
            writer.writerow([
                brand['brand_name'],
                cls._format_decimal(brand['revenue']),
                cls._format_decimal(brand['revenue_percentage']),
                brand['units_sold'],
                brand['orders_count'],
                brand['products_count'],
            ])

    @classmethod
    def _csv_orders(cls, writer, start_date, end_date):
        """Write order-level CSV data for the date range."""
        from orders.models import Order

        start_dt = AnalyticsService._date_to_aware_dt(start_date)
        end_dt = AnalyticsService._date_to_aware_dt(end_date, end_of_day=True)
        currency = AnalyticsService._get_currency()

        orders = Order.objects.filter(
            created_at__gte=start_dt,
            created_at__lte=end_dt,
            payment_status='paid',
        ).exclude(
            status__in=['cancelled', 'refunded']
        ).select_related('user').order_by('-created_at')

        writer.writerow([
            f'Orders Report ({start_date} to {end_date})'
        ])
        writer.writerow([f'Currency: {currency}'])
        writer.writerow([])

        writer.writerow([
            'Order Number', 'Date', 'Customer', 'Email', 'Status',
            f'Total ({currency})', 'Items', 'Country',
        ])

        for order in orders:
            customer_name = ''
            if order.user:
                customer_name = (
                    f"{order.user.first_name} {order.user.last_name}".strip()
                    or order.user.email
                )
            item_count = order.items.count()

            writer.writerow([
                order.order_number,
                order.created_at.strftime('%Y-%m-%d %H:%M'),
                customer_name,
                order.email,
                order.status,
                cls._format_decimal(order.total_amount_base),
                item_count,
                order.shipping_country,
            ])

    @classmethod
    def _csv_summary(cls, writer, start_date, end_date):
        """Write summary analytics CSV."""
        currency = AnalyticsService._get_currency()
        kpi = AnalyticsService.get_sales_kpi(
            period='custom', start_date=start_date, end_date=end_date
        )
        cat_data = AnalyticsService.get_category_analytics(start_date, end_date)
        brand_data = AnalyticsService.get_brand_analytics(start_date, end_date)

        writer.writerow([
            f'Analytics Summary ({start_date} to {end_date})'
        ])
        writer.writerow([f'Currency: {currency}'])
        writer.writerow([])

        writer.writerow(['--- Sales KPIs ---'])
        writer.writerow(['Total Sales', cls._format_decimal(kpi['total_sales'])])
        writer.writerow(['Order Count', kpi['order_count']])
        writer.writerow(['Average Order Value', cls._format_decimal(kpi['average_order_value'])])
        writer.writerow([])

        writer.writerow(['--- Top Categories ---'])
        writer.writerow(['Category', f'Revenue ({currency})', 'Units Sold'])
        for cat in cat_data['categories'][:10]:
            writer.writerow([
                cat['category_name'],
                cls._format_decimal(cat['revenue']),
                cat['units_sold'],
            ])
        writer.writerow([])

        writer.writerow(['--- Top Brands ---'])
        writer.writerow(['Brand', f'Revenue ({currency})', 'Units Sold'])
        for brand in brand_data['brands'][:10]:
            writer.writerow([
                brand['brand_name'],
                cls._format_decimal(brand['revenue']),
                brand['units_sold'],
            ])

    # ================================================================== #
    #  PDF Export
    # ================================================================== #
    @classmethod
    def export_pdf(cls, report_type: str, start_date: date, end_date: date) -> BytesIO:
        """
        Export analytics data as a PDF.

        Args:
            report_type: One of 'products', 'customers', 'categories', 'brands',
                        'orders', 'summary'
            start_date: Start date for the report range
            end_date: End date for the report range

        Returns:
            BytesIO containing the PDF data
        """
        title_map = {
            'products': 'Product Analytics Report',
            'customers': 'Customer Analytics Report',
            'categories': 'Category Analytics Report',
            'brands': 'Brand Analytics Report',
            'orders': 'Orders Report',
            'summary': 'Analytics Summary Report',
        }
        title = title_map.get(report_type, 'Analytics Report')
        buffer, doc = cls._create_pdf_buffer(title)
        styles = cls._get_styles()
        story = []

        # Header
        from django.conf import settings as django_settings
        site_name = getattr(django_settings, 'SITE_NAME', 'Shop')
        story.append(Paragraph(site_name, styles['ReportTitle']))
        story.append(Paragraph(title, styles['ReportSubtitle']))
        story.append(Paragraph(
            f'{start_date.isoformat()} to {end_date.isoformat()}',
            styles['SmallText']
        ))
        story.append(Spacer(1, 0.3 * inch))

        if report_type == 'products':
            cls._pdf_products(story, styles, start_date, end_date)
        elif report_type == 'customers':
            cls._pdf_customers(story, styles, start_date, end_date)
        elif report_type == 'categories':
            cls._pdf_categories(story, styles, start_date, end_date)
        elif report_type == 'brands':
            cls._pdf_brands(story, styles, start_date, end_date)
        elif report_type == 'orders':
            cls._pdf_orders(story, styles, start_date, end_date)
        elif report_type == 'summary':
            cls._pdf_summary(story, styles, start_date, end_date)

        # Footer
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(
            f'Generated by Spwig Analytics',
            styles['SmallText']
        ))

        doc.build(story)
        buffer.seek(0)
        return buffer

    @classmethod
    def _pdf_products(cls, story, styles, start_date, end_date):
        """Add product analytics content to PDF story."""
        data = AnalyticsService.get_product_analytics(
            start_date, end_date, page_size=100
        )
        currency = data['currency']
        summary = data['summary']

        # Summary section
        story.append(Paragraph('Summary', styles['SectionHeader']))
        summary_rows = [
            ['Metric', 'Value'],
            ['Total Revenue', f'{currency} {cls._format_decimal(summary["total_revenue"])}'],
            ['Total Units Sold', str(summary['total_units'])],
            ['Products Sold', str(summary['total_products_sold'])],
        ]
        story.append(cls._build_table(
            summary_rows[0], summary_rows[1:],
            col_widths=[2.5 * inch, 3.5 * inch]
        ))
        story.append(Spacer(1, 0.2 * inch))

        # Product table
        story.append(Paragraph('Product Performance', styles['SectionHeader']))
        header = ['Product', 'SKU', 'Units', f'Revenue ({currency})', 'Orders', 'Avg Price']
        rows = []
        for p in data['products']:
            rows.append([
                Paragraph(p['product_name'][:40], styles['Normal']),
                p['sku'][:15],
                str(p['units_sold']),
                cls._format_decimal(p['revenue']),
                str(p['orders_count']),
                cls._format_decimal(p['average_selling_price']),
            ])

        if rows:
            story.append(cls._build_table(
                header, rows,
                col_widths=[2 * inch, 1 * inch, 0.6 * inch, 1.2 * inch, 0.7 * inch, 1 * inch]
            ))
        else:
            story.append(Paragraph('No product data for this period.', styles['Normal']))

    @classmethod
    def _pdf_customers(cls, story, styles, start_date, end_date):
        """Add customer analytics content to PDF story."""
        data = AnalyticsService.get_customer_analytics(
            start_date, end_date, page_size=50
        )
        currency = data['currency']
        summary = data['summary']

        # Summary
        story.append(Paragraph('Summary', styles['SectionHeader']))
        summary_rows = [
            ['Metric', 'Value'],
            ['Total Customers', str(summary['total_customers'])],
            ['New Customers', str(summary['new_customers'])],
            ['Returning Customers', str(summary['returning_customers'])],
            ['Average LTV', f'{currency} {cls._format_decimal(summary["average_ltv"])}'],
            ['Avg Orders per Customer', str(summary['average_orders_per_customer'])],
        ]
        story.append(cls._build_table(
            summary_rows[0], summary_rows[1:],
            col_widths=[2.5 * inch, 3.5 * inch]
        ))
        story.append(Spacer(1, 0.2 * inch))

        # LTV Distribution
        story.append(Paragraph('LTV Distribution', styles['SectionHeader']))
        ltv_header = ['Range', 'Customers']
        ltv_rows = [
            [b['label'], str(b['count'])]
            for b in data['ltv_distribution']
        ]
        if ltv_rows:
            story.append(cls._build_table(
                ltv_header, ltv_rows,
                col_widths=[3 * inch, 3 * inch]
            ))
        story.append(Spacer(1, 0.2 * inch))

        # Top customers
        story.append(Paragraph('Top Customers', styles['SectionHeader']))
        header = ['Name', 'Email', 'Segment', f'Total Spent ({currency})', 'Orders']
        rows = []
        for c in data['top_customers'][:20]:
            rows.append([
                Paragraph(c['name'][:30], styles['Normal']),
                c['email'][:30],
                c['segment'],
                cls._format_decimal(c['total_spent']),
                str(c['total_orders']),
            ])

        if rows:
            story.append(cls._build_table(
                header, rows,
                col_widths=[1.5 * inch, 1.8 * inch, 0.8 * inch, 1.2 * inch, 0.7 * inch]
            ))

        # Geo breakdown
        if data['geo_breakdown']:
            story.append(Spacer(1, 0.2 * inch))
            story.append(Paragraph('Geographic Breakdown', styles['SectionHeader']))
            geo_header = ['Country', 'Orders', f'Revenue ({currency})', 'Customers']
            geo_rows = [
                [
                    g['country'],
                    str(g['order_count']),
                    cls._format_decimal(g['revenue']),
                    str(g['customer_count']),
                ]
                for g in data['geo_breakdown'][:15]
            ]
            story.append(cls._build_table(
                geo_header, geo_rows,
                col_widths=[2 * inch, 1 * inch, 1.5 * inch, 1 * inch]
            ))

    @classmethod
    def _pdf_categories(cls, story, styles, start_date, end_date):
        """Add category analytics content to PDF story."""
        data = AnalyticsService.get_category_analytics(start_date, end_date)
        currency = data['currency']
        summary = data['summary']

        # Summary
        story.append(Paragraph('Summary', styles['SectionHeader']))
        summary_rows = [
            ['Metric', 'Value'],
            ['Total Revenue', f'{currency} {cls._format_decimal(summary["total_revenue"])}'],
            ['Total Units', str(summary['total_units'])],
            ['Categories', str(summary['total_categories'])],
        ]
        story.append(cls._build_table(
            summary_rows[0], summary_rows[1:],
            col_widths=[2.5 * inch, 3.5 * inch]
        ))
        story.append(Spacer(1, 0.2 * inch))

        # Categories table
        story.append(Paragraph('Category Breakdown', styles['SectionHeader']))
        header = ['Category', f'Revenue ({currency})', '%', 'Units', 'Orders', 'Products']
        rows = []
        for cat in data['categories']:
            rows.append([
                Paragraph(cat['category_name'][:35], styles['Normal']),
                cls._format_decimal(cat['revenue']),
                cls._format_decimal(cat['revenue_percentage']),
                str(cat['units_sold']),
                str(cat['orders_count']),
                str(cat['products_count']),
            ])

        if rows:
            story.append(cls._build_table(
                header, rows,
                col_widths=[2 * inch, 1.2 * inch, 0.5 * inch, 0.7 * inch, 0.7 * inch, 0.8 * inch]
            ))
        else:
            story.append(Paragraph('No category data for this period.', styles['Normal']))

    @classmethod
    def _pdf_brands(cls, story, styles, start_date, end_date):
        """Add brand analytics content to PDF story."""
        data = AnalyticsService.get_brand_analytics(start_date, end_date)
        currency = data['currency']
        summary = data['summary']

        # Summary
        story.append(Paragraph('Summary', styles['SectionHeader']))
        summary_rows = [
            ['Metric', 'Value'],
            ['Total Revenue', f'{currency} {cls._format_decimal(summary["total_revenue"])}'],
            ['Total Units', str(summary['total_units'])],
            ['Brands', str(summary['total_brands'])],
        ]
        story.append(cls._build_table(
            summary_rows[0], summary_rows[1:],
            col_widths=[2.5 * inch, 3.5 * inch]
        ))
        story.append(Spacer(1, 0.2 * inch))

        # Brands table
        story.append(Paragraph('Brand Breakdown', styles['SectionHeader']))
        header = ['Brand', f'Revenue ({currency})', '%', 'Units', 'Orders', 'Products']
        rows = []
        for brand in data['brands']:
            rows.append([
                Paragraph(brand['brand_name'][:35], styles['Normal']),
                cls._format_decimal(brand['revenue']),
                cls._format_decimal(brand['revenue_percentage']),
                str(brand['units_sold']),
                str(brand['orders_count']),
                str(brand['products_count']),
            ])

        if rows:
            story.append(cls._build_table(
                header, rows,
                col_widths=[2 * inch, 1.2 * inch, 0.5 * inch, 0.7 * inch, 0.7 * inch, 0.8 * inch]
            ))
        else:
            story.append(Paragraph('No brand data for this period.', styles['Normal']))

    @classmethod
    def _pdf_orders(cls, story, styles, start_date, end_date):
        """Add order list content to PDF story."""
        from orders.models import Order

        start_dt = AnalyticsService._date_to_aware_dt(start_date)
        end_dt = AnalyticsService._date_to_aware_dt(end_date, end_of_day=True)
        currency = AnalyticsService._get_currency()

        orders = Order.objects.filter(
            created_at__gte=start_dt,
            created_at__lte=end_dt,
            payment_status='paid',
        ).exclude(
            status__in=['cancelled', 'refunded']
        ).select_related('user').order_by('-created_at')[:200]

        # Summary
        total_count = Order.objects.filter(
            created_at__gte=start_dt,
            created_at__lte=end_dt,
            payment_status='paid',
        ).exclude(
            status__in=['cancelled', 'refunded']
        ).count()

        story.append(Paragraph(
            f'Showing {min(200, total_count)} of {total_count} orders',
            styles['Normal']
        ))
        story.append(Spacer(1, 0.2 * inch))

        header = ['Order #', 'Date', 'Customer', 'Status', f'Total ({currency})']
        rows = []
        for order in orders:
            customer_name = ''
            if order.user:
                customer_name = (
                    f"{order.user.first_name} {order.user.last_name}".strip()
                    or order.user.email
                )
            rows.append([
                order.order_number,
                order.created_at.strftime('%Y-%m-%d'),
                Paragraph(customer_name[:25], styles['Normal']),
                order.status.title(),
                cls._format_decimal(order.total_amount_base),
            ])

        if rows:
            story.append(cls._build_table(
                header, rows,
                col_widths=[1.2 * inch, 0.9 * inch, 1.8 * inch, 0.9 * inch, 1.2 * inch]
            ))
        else:
            story.append(Paragraph('No orders found for this period.', styles['Normal']))

    @classmethod
    def _pdf_summary(cls, story, styles, start_date, end_date):
        """Add summary analytics content to PDF story."""
        currency = AnalyticsService._get_currency()
        kpi = AnalyticsService.get_sales_kpi(
            period='custom', start_date=start_date, end_date=end_date
        )

        # KPIs
        story.append(Paragraph('Sales KPIs', styles['SectionHeader']))
        kpi_rows = [
            ['Metric', 'Value'],
            ['Total Sales', f'{currency} {cls._format_decimal(kpi["total_sales"])}'],
            ['Order Count', str(kpi['order_count'])],
            ['Average Order Value', f'{currency} {cls._format_decimal(kpi["average_order_value"])}'],
        ]
        story.append(cls._build_table(
            kpi_rows[0], kpi_rows[1:],
            col_widths=[2.5 * inch, 3.5 * inch]
        ))
        story.append(Spacer(1, 0.2 * inch))

        # Top categories
        cat_data = AnalyticsService.get_category_analytics(start_date, end_date)
        story.append(Paragraph('Top Categories', styles['SectionHeader']))
        cat_header = ['Category', f'Revenue ({currency})', 'Units', 'Revenue %']
        cat_rows = []
        for cat in cat_data['categories'][:10]:
            cat_rows.append([
                Paragraph(cat['category_name'][:30], styles['Normal']),
                cls._format_decimal(cat['revenue']),
                str(cat['units_sold']),
                f"{cls._format_decimal(cat['revenue_percentage'])}%",
            ])

        if cat_rows:
            story.append(cls._build_table(
                cat_header, cat_rows,
                col_widths=[2 * inch, 1.5 * inch, 1 * inch, 1 * inch]
            ))
        story.append(Spacer(1, 0.2 * inch))

        # Top brands
        brand_data = AnalyticsService.get_brand_analytics(start_date, end_date)
        story.append(Paragraph('Top Brands', styles['SectionHeader']))
        brand_header = ['Brand', f'Revenue ({currency})', 'Units', 'Revenue %']
        brand_rows = []
        for brand in brand_data['brands'][:10]:
            brand_rows.append([
                Paragraph(brand['brand_name'][:30], styles['Normal']),
                cls._format_decimal(brand['revenue']),
                str(brand['units_sold']),
                f"{cls._format_decimal(brand['revenue_percentage'])}%",
            ])

        if brand_rows:
            story.append(cls._build_table(
                brand_header, brand_rows,
                col_widths=[2 * inch, 1.5 * inch, 1 * inch, 1 * inch]
            ))
