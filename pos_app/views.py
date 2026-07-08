import os
from decimal import Decimal

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from core.models import SiteSettings
from core.utils.currency_helpers import format_money


# Directory where built POS frontend assets live after running the build script.
# In production this is populated by: pos_app/build.sh
POS_DIST_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'frontend_build'
)


class POSAppView(TemplateView):
    """
    Serve the POS Single Page Application.

    This is a catch-all: any /pos/* route (except /pos/assets/ and
    /pos/display/) renders the same index.html and lets React Router
    handle client-side routing.
    """
    template_name = 'pos/index.html'


class POSCustomerDisplayView(TemplateView):
    """Serve the customer-facing display page (no login required)."""
    template_name = 'pos/index.html'


class POSAssetView(View):
    """
    Serve built POS frontend assets (JS, CSS, images, SW, manifest).

    In production Nginx should serve /pos/assets/ directly from the dist
    folder for better performance, but this view works as a zero-config
    fallback so merchants don't need to touch their Nginx config.
    """

    def get(self, request, path='', prefix=''):
        # Reconstruct full relative path within dist/ (e.g., 'assets/index-abc.js')
        rel_path = os.path.join(prefix, path) if prefix else path
        file_path = os.path.normpath(os.path.join(POS_DIST_DIR, rel_path))

        # Prevent directory traversal
        if not file_path.startswith(os.path.normpath(POS_DIST_DIR)):
            raise Http404

        if not os.path.isfile(file_path):
            raise Http404

        response = FileResponse(open(file_path, 'rb'))

        # Set correct content types for common POS assets
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.js': 'application/javascript',
            '.css': 'text/css',
            '.json': 'application/json',
            '.webmanifest': 'application/manifest+json',
            '.png': 'image/png',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.woff2': 'font/woff2',
            '.woff': 'font/woff',
            '.ttf': 'font/ttf',
        }
        if ext in content_types:
            response['Content-Type'] = content_types[ext]

        # Cache built assets aggressively (filenames contain hashes)
        if 'assets/' in rel_path:
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
        else:
            response['Cache-Control'] = 'public, max-age=3600'

        # Service worker needs this header to control /pos/ scope
        if rel_path.endswith('sw.js'):
            response['Service-Worker-Allowed'] = '/pos/'

        return response


class PublicReceiptView(View):
    """
    Public receipt view accessible via unique token.

    No authentication required - security through token obscurity.
    Allows customers to view their receipt via link from email/SMS.
    """

    def get(self, request, token):
        from orders.models import Order

        # Find order by token
        order = get_object_or_404(
            Order.objects.prefetch_related(
                'items', 'pos_payments'
            ).select_related(
                'cashier', 'pos_terminal'
            ),
            receipt_token=token,
            channel='pos',
        )

        site_settings = SiteSettings.get_settings()
        currency = str(order.total_amount.currency)

        # Build context
        store_name = site_settings.site_name if site_settings else 'Store'
        store_address_parts = []
        if site_settings:
            for part in [
                getattr(site_settings, 'address_line_1', ''),
                getattr(site_settings, 'city', ''),
                getattr(site_settings, 'state_province', ''),
                getattr(site_settings, 'postal_code', ''),
                getattr(site_settings, 'country', ''),
            ]:
                if part:
                    store_address_parts.append(str(part))
        store_address = ', '.join(store_address_parts)
        store_phone = str(getattr(site_settings, 'phone_number', '')) if site_settings else ''

        # Store logo URL
        store_logo_url = ''
        if site_settings and site_settings.site_logo:
            try:
                logo = site_settings.site_logo
                if logo.file:
                    store_logo_url = request.build_absolute_uri(logo.file.url)
            except Exception:
                pass

        # Order items
        items = []
        for item in order.items.all():
            unit_price = item.unit_price.amount if hasattr(item.unit_price, 'amount') else Decimal(str(item.unit_price))
            line_total = item.total_price.amount if hasattr(item.total_price, 'amount') else Decimal(str(item.total_price))

            items.append({
                'name': f"{item.product_name}{' - ' + item.variant_name if item.variant_name else ''}",
                'sku': item.sku,
                'quantity': item.quantity,
                'unit_price': format_money(unit_price, currency),
                'line_total': format_money(line_total, currency),
            })

        # Payments
        payments = []
        total_change = Decimal('0')

        for p in order.pos_payments.all():
            change = Decimal('0')
            if p.change_given:
                change = p.change_given.amount if hasattr(p.change_given, 'amount') else Decimal(str(p.change_given))
                total_change += change

            amount = p.amount.amount if hasattr(p.amount, 'amount') else Decimal(str(p.amount))

            payments.append({
                'method': p.get_method_display(),
                'amount': format_money(amount, currency),
                'card_last4': p.card_last_four or '',
            })

        # Totals
        subtotal = order.subtotal.amount if hasattr(order.subtotal, 'amount') else Decimal(str(order.subtotal))
        tax_amount = order.tax_amount.amount if hasattr(order.tax_amount, 'amount') else Decimal('0')
        discount_amount = order.discount_amount.amount if hasattr(order.discount_amount, 'amount') else Decimal('0')
        total = order.total_amount.amount if hasattr(order.total_amount, 'amount') else Decimal(str(order.total_amount))

        context = {
            'order': order,
            'store_name': store_name,
            'store_address': store_address,
            'store_phone': store_phone,
            'store_logo_url': store_logo_url,
            'order_number': order.order_number,
            'order_date': order.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'cashier_name': order.cashier.get_full_name() if order.cashier else '',
            'terminal_name': order.pos_terminal.name if order.pos_terminal else '',
            'items': items,
            'subtotal': format_money(subtotal, currency),
            'discount_amount': format_money(discount_amount, currency) if discount_amount else None,
            'tax_amount': format_money(tax_amount, currency) if tax_amount else None,
            'total': format_money(total, currency),
            'currency': currency,
            'payments': payments,
            'change_given': format_money(total_change, currency) if total_change else None,
        }

        return render(request, 'pos/public_receipt.html', context)
