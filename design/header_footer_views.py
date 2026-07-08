"""
Views for header, footer, and menu management
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from .header_footer_models import (
    HeaderTemplate, FooterTemplate, Widget,
    Menu, MenuItem
)


@method_decorator(staff_member_required, name='dispatch')
class PreviewHeaderView(View):
    """Preview header template"""

    def get(self, request, header_id):
        from .theme_models import Theme, ThemeBranding

        header = get_object_or_404(HeaderTemplate, pk=header_id)

        # Get widgets for this header
        widget_placements = header.widget_placements.filter(
            is_active=True
        ).select_related('widget').order_by('zone', 'order')

        # Group widgets by zone
        # Convert zone names with hyphens to underscores for template compatibility
        zones = {}
        for placement in widget_placements:
            # Convert "top-bar_full" to "top_bar_full" for template access
            zone_key = placement.zone.replace('-', '_')
            if zone_key not in zones:
                zones[zone_key] = []
            zones[zone_key].append(placement)

        # Get theme CSS URLs
        theme_css_url = None
        brand_css_url = None

        active_theme = Theme.objects.filter(is_default=True).first()
        if active_theme:
            theme_css_url = active_theme.css_url

        branding = ThemeBranding.objects.first()
        if branding:
            brand_css_url = branding.get_css_url()

        context = {
            'header': header,
            'zones': zones,
            'zone_overrides': header.zone_overrides or {},
            'preview_mode': True,
            'theme_css_url': theme_css_url,
            'brand_css_url': brand_css_url,
        }

        return render(request, 'design/preview/header.html', context)


@method_decorator(staff_member_required, name='dispatch')
class PreviewFooterView(View):
    """Preview footer template"""

    def get(self, request, footer_id):
        from .theme_models import Theme, ThemeBranding

        footer = get_object_or_404(FooterTemplate, pk=footer_id)

        # Get widgets for this footer
        widget_placements = footer.widget_placements.filter(
            is_active=True
        ).select_related('widget').order_by('zone', 'order')

        # Group widgets by zone
        # Convert zone names with hyphens to underscores for template compatibility
        zones = {}
        for placement in widget_placements:
            # Convert "top-bar_full" to "top_bar_full" for template access
            zone_key = placement.zone.replace('-', '_')
            if zone_key not in zones:
                zones[zone_key] = []
            zones[zone_key].append(placement)

        # Get theme CSS URLs
        theme_css_url = None
        brand_css_url = None

        active_theme = Theme.objects.filter(is_default=True).first()
        if active_theme:
            theme_css_url = active_theme.css_url

        branding = ThemeBranding.objects.first()
        if branding:
            brand_css_url = branding.get_css_url()

        context = {
            'footer': footer,
            'zones': zones,
            'preview_mode': True,
            'theme_css_url': theme_css_url,
            'brand_css_url': brand_css_url,
        }

        return render(request, 'design/preview/footer.html', context)


@method_decorator(staff_member_required, name='dispatch')
class MenuBuilderView(View):
    """Enhanced visual menu builder interface with drag-and-drop support"""

    def get(self, request, menu_id=None):
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        from .theme_models import ThemeBranding
        from .theme_utils import get_active_theme

        # If no menu_id provided, get the first menu or create a default
        if menu_id is None:
            menu = Menu.objects.filter(is_active=True).first()
            if not menu:
                # Create a default menu if none exists
                menu = Menu.objects.create(
                    name='Main Menu',
                    slug='main-menu',
                    location='header',
                    display_type='horizontal',
                    is_active=True,
                )

            # Redirect to builder with the menu ID
            return HttpResponseRedirect(
                reverse('design:menu_builder', args=[menu.id])
            )

        # Load the specific menu
        menu = get_object_or_404(Menu, pk=menu_id)

        # Get all menus for the dropdown selector
        all_menus = Menu.objects.filter(is_active=True).order_by('location', 'name')

        # Get menu items as nested tree structure
        items_tree = menu.get_all_items_tree() if hasattr(menu, 'get_all_items_tree') else self._get_items_tree(menu)

        # Threshold for switching to AJAX-based search
        # Below this, embed all data; above this, use search API
        AJAX_THRESHOLD = 10

        # Get counts for pages and categories to determine loading mode
        from page_builder.models import Page
        from catalog.models import Category
        pages_count = Page.objects.filter(status='published').count()
        categories_count = Category.objects.filter(is_active=True).count()

        # Only load full data if below threshold (for small stores)
        # Large stores will use AJAX search instead
        pages_use_ajax = pages_count > AJAX_THRESHOLD
        categories_use_ajax = categories_count > AJAX_THRESHOLD

        available_pages = [] if pages_use_ajax else self.get_available_pages()
        available_categories = [] if categories_use_ajax else self.get_available_categories()

        # Get theme CSS URLs for preview
        theme_css_url = None
        brand_css_url = None
        base_css_url = f"{settings.STATIC_URL}css/base.css"

        # Get theme default menu tokens from active theme manifest
        active_theme = get_active_theme()
        theme_menu_tokens = {}
        if active_theme:
            theme_css_url = active_theme.get_css_url()
            # Load menu tokens from theme manifest
            if active_theme.manifest:
                theme_tokens = active_theme.manifest.get('tokens', {})
                theme_menu_tokens = theme_tokens.get('menu', {})

        # Get custom overrides from ThemeBranding
        branding = ThemeBranding.objects.first()
        custom_menu_tokens = {}
        branding_id = None
        if branding:
            brand_css_url = branding.get_css_url()
            branding_id = branding.id
            # Extract custom menu tokens from component_overrides
            overrides = branding.component_overrides or {}
            custom_menu_tokens = overrides.get('menu', {})

        # Merge: theme defaults + custom overrides (custom wins)
        menu_tokens = {**theme_menu_tokens, **custom_menu_tokens}

        # Item type choices for the builder
        item_type_choices = [
            {'value': 'link', 'label': 'Standard Link', 'icon': 'fa-link'},
            {'value': 'page', 'label': 'Page Link', 'icon': 'fa-file'},
            {'value': 'category', 'label': 'Category Link', 'icon': 'fa-folder'},
            {'value': 'category_tree', 'label': 'Dynamic Categories', 'icon': 'fa-sitemap'},
            {'value': 'custom_url', 'label': 'Custom URL', 'icon': 'fa-external-link-alt'},
            {'value': 'divider', 'label': 'Divider', 'icon': 'fa-minus'},
            {'value': 'header', 'label': 'Section Header', 'icon': 'fa-heading'},
            {'value': 'widget', 'label': 'Widget Item', 'icon': 'fa-puzzle-piece'},
        ]

        # Widget type choices for widget items
        widget_type_choices = [
            {'value': 'login_toggle', 'label': 'Login/Logout', 'icon': 'fa-sign-in-alt'},
            {'value': 'cart', 'label': 'Shopping Cart', 'icon': 'fa-shopping-cart'},
            {'value': 'account', 'label': 'My Account', 'icon': 'fa-user'},
            {'value': 'wishlist', 'label': 'Wishlist', 'icon': 'fa-heart'},
            {'value': 'search', 'label': 'Search', 'icon': 'fa-search'},
        ]

        # Location choices for menu
        location_choices = [
            {'value': 'header', 'label': 'Header'},
            {'value': 'footer', 'label': 'Footer'},
            {'value': 'sidebar', 'label': 'Sidebar'},
            {'value': 'mobile', 'label': 'Mobile Only'},
            {'value': 'other', 'label': 'Other'},
        ]

        # Display type choices
        display_type_choices = [
            {'value': 'horizontal', 'label': 'Horizontal'},
            {'value': 'vertical', 'label': 'Vertical'},
            {'value': 'dropdown', 'label': 'Dropdown'},
            {'value': 'mega_menu', 'label': 'Mega Menu'},
        ]

        context = {
            'menu': menu,
            'all_menus': all_menus,
            'items_tree': json.dumps(items_tree),
            'available_pages': json.dumps(available_pages),
            'available_categories': json.dumps(available_categories),
            'item_type_choices': item_type_choices,
            'widget_type_choices': widget_type_choices,
            'location_choices': location_choices,
            'display_type_choices': display_type_choices,
            'builder_type': 'menu',
            # API URLs for JavaScript
            'api_base_url': '/api/menu/',
            'api_menu_url': f'/api/menu/{menu.id}/',
            'api_items_url': '/api/menu/items/',
            'api_reorder_url': '/api/menu/items/reorder/',
            'api_sources_url': '/api/menu/sources/',
            'api_preview_url': f'/api/menu/{menu.id}/preview/',
            'api_save_structure_url': f'/api/menu/{menu.id}/save-structure/',
            # Theme CSS URLs for preview styling
            'theme_css_url': theme_css_url,
            'brand_css_url': brand_css_url,
            'base_css_url': base_css_url,
            # Menu widget CSS for accurate preview (same CSS as frontend)
            'menu_widget_css_url': f"{settings.STATIC_URL}design/css/widgets/menu.css",
            # AJAX-based search flags for large stores
            'pages_count': pages_count,
            'categories_count': categories_count,
            'pages_use_ajax': pages_use_ajax,
            'categories_use_ajax': categories_use_ajax,
            'ajax_threshold': AJAX_THRESHOLD,
            # Menu tokens for menu-level styling (syncs with ThemeBranding)
            'branding_id': branding_id,
            'menu_tokens': json.dumps(menu_tokens),              # Merged effective values
            'menu_tokens_custom': json.dumps(custom_menu_tokens),    # Custom overrides only
            'menu_tokens_defaults': json.dumps(theme_menu_tokens),   # Theme defaults
            'api_menu_tokens_url': '/api/menu/tokens/',
        }

        return render(request, 'design/menu_builder/builder.html', context)

    def _get_items_tree(self, menu):
        """Fallback method to build items tree if model method not available"""
        def build_tree(parent=None):
            items = menu.items.filter(parent=parent, is_active=True).order_by('order')
            tree = []
            for item in items:
                node = {
                    'id': item.id,
                    'title': item.title,
                    'url': item.url,
                    'target': item.target,
                    'icon': item.icon,
                    'badge_text': item.badge_text,
                    'badge_color': item.badge_color,
                    'css_classes': item.css_classes,
                    'mega_menu_content': item.mega_menu_content,
                    'order': item.order,
                    'is_active': item.is_active,
                    # New fields
                    'item_type': getattr(item, 'item_type', 'link'),
                    'page_reference_id': getattr(item, 'page_reference_id', None),
                    'category_reference_id': getattr(item, 'category_reference_id', None),
                    'style_config': getattr(item, 'style_config', {}),
                    'widget_config': getattr(item, 'widget_config', {}),
                    'tree_config': getattr(item, 'tree_config', {}),
                    'visibility_rules': getattr(item, 'visibility_rules', []),
                    'translations': getattr(item, 'translations', {}),
                    'children': build_tree(item),
                }
                tree.append(node)
            return tree
        return build_tree()

    def get_available_pages(self):
        """Get list of available pages from Page model"""
        try:
            from page_builder.models import Page
            # Page model uses status='published' instead of is_active
            pages = Page.objects.filter(status='published').values('id', 'title', 'slug')
            return [
                {
                    'id': p['id'],
                    'title': p['title'],
                    'slug': p['slug'],
                    'url': f"/{p['slug']}/" if p['slug'] else '/',
                }
                for p in pages
            ]
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error fetching pages: {e}")
            return []

    def get_available_categories(self):
        """Get list of available categories from Category model"""
        try:
            from catalog.models import Category
            categories = Category.objects.filter(is_active=True).values('id', 'name', 'slug')
            return [
                {
                    'id': c['id'],
                    'name': c['name'],
                    'slug': c['slug'],
                    'url': f"/category/{c['slug']}/",
                }
                for c in categories
            ]
        except Exception:
            return []


@method_decorator(staff_member_required, name='dispatch')
class BrandingPreviewView(View):
    """Live preview of branding changes"""

    def get(self, request):
        from .theme_models import ThemeBranding

        branding = ThemeBranding.objects.first()
        if not branding:
            branding = ThemeBranding.objects.create()

        context = {
            'branding': branding,
            'preview_mode': True,
        }

        return render(request, 'design/preview/branding.html', context)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class WidgetConfigView(View):
    """AJAX endpoint for widget configuration"""

    def post(self, request, widget_id):
        """Update widget configuration"""
        widget = get_object_or_404(Widget, pk=widget_id)

        try:
            data = json.loads(request.body)
            widget.config = data.get('config', {})
            widget.save()

            return JsonResponse({'success': True, 'message': 'Widget configuration saved'})

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    def get(self, request, widget_id):
        """Get widget configuration"""
        widget = get_object_or_404(Widget, pk=widget_id)

        return JsonResponse({
            'id': widget.id,
            'name': widget.name,
            'type': widget.widget_type,
            'config': widget.config,
            'content': widget.content,
        })