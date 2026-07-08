"""
LayoutRenderer Demo View - Integration Example

This demonstrates how LayoutRenderer integrates with existing builders,
showing CSS isolation and preview mode working correctly.

This view can be used as a reference for integrating LayoutRenderer into:
- Brand Builder preview
- Page Editor preview
- Production page rendering
"""

from django.shortcuts import render
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from core.decorators import allow_iframe_sameorigin

from .layout_renderer import LayoutRenderer
from .theme_models import ThemeBranding


@method_decorator([staff_member_required, allow_iframe_sameorigin], name='dispatch')
class LayoutRendererDemoView(View):
    """
    Demonstration view showing LayoutRenderer integration.

    Shows how to:
    1. Use LayoutRenderer to generate HTML
    2. Apply CSS isolation for preview mode
    3. Integrate with branding system
    4. Handle different page types and tiers
    """

    def get(self, request):
        """Render a demo page showing LayoutRenderer features."""
        # Get page parameters from query string
        page_type = request.GET.get('page_type', 'home')
        tier = request.GET.get('tier', 'C')
        preview_mode = request.GET.get('preview', 'true') == 'true'
        isolation_type = request.GET.get('isolation', 'page_editor')

        # Get branding if available
        branding = None
        css_content = ''
        try:
            branding = ThemeBranding.objects.first()
            if branding:
                css_content = branding.generate_css()
        except Exception:
            pass

        # Initialize LayoutRenderer
        renderer = LayoutRenderer(
            page_type=page_type,
            tier=tier,
            context={
                'branding': branding,
                'preview_mode': preview_mode,
                'isolation_type': isolation_type,  # 'brand_builder' or 'page_editor'
            }
        )

        # Render the layout
        html_content = renderer.render()

        # Get CSS isolation class for reference
        isolation_class = renderer.get_css_isolation_class()

        context = {
            'page_type': page_type,
            'tier': tier,
            'preview_mode': preview_mode,
            'isolation_type': isolation_type,
            'isolation_class': isolation_class,
            'html_content': html_content,
            'css_content': css_content,
            'renderer_info': {
                'cache_enabled': not preview_mode,
                'regions_rendered': len(renderer.page_tier.schema.get('regions', {})),
                'schema': renderer.page_tier.schema,
            }
        }

        return render(request, 'design/layout_renderer_demo.html', context)


@method_decorator([staff_member_required, allow_iframe_sameorigin], name='dispatch')
class BrandingPreviewWithRendererView(View):
    """
    Example of integrating LayoutRenderer with Brand Builder.

    This shows how to use LayoutRenderer for branding previews while
    maintaining existing CSS isolation and sample content display.
    """

    def get(self, request, branding_id):
        """Render branding preview using LayoutRenderer."""
        from .theme_models import ThemeBranding
        from django.shortcuts import get_object_or_404

        branding = get_object_or_404(ThemeBranding, pk=branding_id)

        # Option 1: Use LayoutRenderer to generate page structure
        renderer = LayoutRenderer(
            page_type='home',
            tier='C',
            context={
                'branding': branding,
                'preview_mode': True,
                'isolation_type': 'brand_builder',
            }
        )

        html_content = renderer.render()
        css_content = branding.generate_css()

        context = {
            'branding': branding,
            'html_content': html_content,
            'css_content': css_content,
            'isolation_class': renderer.get_css_isolation_class(),
        }

        return render(request, 'design/branding_preview_with_renderer.html', context)


@method_decorator([staff_member_required, allow_iframe_sameorigin], name='dispatch')
class PageBuilderPreviewWithRendererView(View):
    """
    Example of integrating LayoutRenderer with Page Editor.

    This shows how to use LayoutRenderer for page previews with
    proper CSS isolation and context passing.
    """

    def get(self, request, page_id):
        """Render page preview using LayoutRenderer."""
        from page_builder.models import Page
        from django.shortcuts import get_object_or_404

        page = get_object_or_404(Page, pk=page_id)

        # Use LayoutRenderer to render the page
        renderer = LayoutRenderer(
            page_type=page.page_type if hasattr(page, 'page_type') else 'home',
            tier='C',  # Could be determined from page settings
            context={
                'page': page,
                'preview_mode': True,
                'isolation_type': 'page_editor',
            }
        )

        html_content = renderer.render()

        context = {
            'page': page,
            'html_content': html_content,
            'isolation_class': renderer.get_css_isolation_class(),
        }

        return render(request, 'design/page_preview_with_renderer.html', context)
