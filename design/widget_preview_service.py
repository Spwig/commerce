"""
Widget Preview Service

Renders widgets server-side for the header/footer builder preview.
Uses the same templates as the storefront to ensure visual consistency.
"""
from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser


class MockWidget:
    """Mock widget object for preview rendering"""
    def __init__(self, widget_type='', css_classes=''):
        self.widget_type = widget_type
        self.css_classes = css_classes


class WidgetPreviewRenderer:
    """Render widgets server-side for builder preview"""

    def render(self, widget_type, config, request=None):
        """
        Render widget as HTML for preview.

        Args:
            widget_type: The type of widget (menu, logo, search, etc.)
            config: Widget configuration dictionary
            request: Optional HTTP request for context

        Returns:
            Rendered HTML string
        """
        context = self._build_context(widget_type, config, request)
        template_path = f"design/widgets/{widget_type}.html"

        try:
            return render_to_string(template_path, context, request=request)
        except Exception as e:
            return f'<div class="widget-preview-error">Preview unavailable: {str(e)}</div>'

    def _build_context(self, widget_type, config, request):
        """
        Build context based on widget type requirements.

        Each widget template expects certain context variables.
        This method builds the appropriate context for each type.
        """
        config = config or {}

        # Base context for all widgets
        context = {
            'config': config,
            'widget': MockWidget(widget_type=widget_type, css_classes=''),
            'is_preview': True,
            # For text/custom widgets, content comes from config.text in preview mode
            'content': config.get('text', ''),
        }

        # Add request-based context
        if request:
            context['request'] = request
            context['user'] = request.user
        else:
            context['user'] = AnonymousUser()

        # Widget-specific context building
        context_builder = getattr(self, f'_build_{widget_type}_context', None)
        if context_builder:
            context_builder(context, config, request)

        return context

    def _build_menu_context(self, context, config, request):
        """Build context for menu widget"""
        from design.header_footer_models import Menu

        menu_id = config.get('menu_id')
        if menu_id:
            try:
                menu = Menu.objects.prefetch_related('items').get(pk=menu_id)
                context['menu'] = menu
                context['menu_items'] = menu.get_items()
            except Menu.DoesNotExist:
                context['menu'] = None
                context['menu_items'] = []
        else:
            context['menu'] = None
            context['menu_items'] = []

    def _build_search_context(self, context, config, request):
        """Build context for search widget"""
        if config.get('show_categories'):
            try:
                from catalog.models import Category
                context['search_categories'] = Category.objects.filter(
                    is_active=True,
                    parent__isnull=True
                ).order_by('name')[:15]
            except Exception:
                context['search_categories'] = []
        else:
            context['search_categories'] = []

    def _build_cart_context(self, context, config, request):
        """Build context for cart widget"""
        # In preview mode, show sample cart data
        context['cart_count'] = 0
        context['cart_total'] = 0

    def _build_account_context(self, context, config, request):
        """Build context for account widget"""
        # Already set user in base context
        pass

    def _build_language_context(self, context, config, request):
        """Build context for language widget"""
        from django.conf import settings
        context['LANGUAGES'] = getattr(settings, 'LANGUAGES', [('en', 'English')])
        context['LANGUAGE_CODE'] = getattr(settings, 'LANGUAGE_CODE', 'en')

    def _build_currency_context(self, context, config, request):
        """Build context for currency widget"""
        try:
            from exchange_rates.models import Currency
            context['currencies'] = Currency.objects.filter(is_active=True)
            context['current_currency'] = Currency.objects.filter(is_default=True).first()
        except Exception:
            context['currencies'] = []
            context['current_currency'] = None

    def _build_logo_context(self, context, config, request):
        """Build context for logo widget"""
        from core.models import SiteSettings
        settings = SiteSettings.get_settings()
        context['site_settings'] = settings

        # If use_site_logo is True (default), and no custom logo_url is set,
        # the template will use site settings logo automatically

    def _build_site_variable_context(self, context, config, request):
        """Build context for site_variable widget"""
        from core.models import SiteSettings
        settings = SiteSettings.get_settings()
        context['site_settings'] = settings
