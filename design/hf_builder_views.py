"""
Header/Footer Visual Builder Views
Provides the main builder interface for creating and editing headers/footers
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponseRedirect

from .header_footer_models import HeaderTemplate, FooterTemplate
from .theme_models import Theme, ThemeBranding
from .theme_utils import get_active_theme


@method_decorator(staff_member_required, name='dispatch')
class HeaderBuilderView(View):
    """Visual builder for header templates"""

    def get(self, request, header_id=None):
        # If no header_id provided, get the default or create one
        if header_id is None:
            header = HeaderTemplate.objects.filter(is_default=True).first()
            if not header:
                header = HeaderTemplate.objects.filter(is_active=True).first()

            if not header:
                # Create a default header if none exists
                header = HeaderTemplate.objects.create(
                    name='Default Header',
                    slug='default-header',
                    layout_type='classic',
                    is_default=True,
                    is_active=True,
                    created_by=request.user,
                )

            # Redirect to builder with the header ID
            return HttpResponseRedirect(
                reverse('design:header_builder', args=[header.id])
            )

        # Load the specific header
        header = get_object_or_404(HeaderTemplate, pk=header_id)

        # Get all headers for the dropdown
        all_headers = HeaderTemplate.objects.filter(is_active=True).order_by('name')

        # Get theme CSS URLs
        theme_css_url = None
        brand_css_url = None

        active_theme = get_active_theme()
        if active_theme:
            theme_css_url = active_theme.get_css_url()

        branding = ThemeBranding.objects.first()
        if branding:
            brand_css_url = branding.get_css_url()

        context = {
            'header': header,
            'all_headers': all_headers,
            'builder_type': 'header',
            'api_url': reverse('hf_api:header_builder', args=[header.id]),
            'widget_library_url': reverse('hf_api:widget_library'),
            'preset_gallery_url': reverse('hf_api:preset_gallery', args=['header']),
            'theme_css_url': theme_css_url,
            'brand_css_url': brand_css_url,
        }

        return render(request, 'design/header_footer_builder.html', context)


@method_decorator(staff_member_required, name='dispatch')
class FooterBuilderView(View):
    """Visual builder for footer templates"""

    def get(self, request, footer_id=None):
        # If no footer_id provided, get the default or create one
        if footer_id is None:
            footer = FooterTemplate.objects.filter(is_default=True).first()
            if not footer:
                footer = FooterTemplate.objects.filter(is_active=True).first()

            if not footer:
                # Create a default footer if none exists
                footer = FooterTemplate.objects.create(
                    name='Default Footer',
                    slug='default-footer',
                    layout_type='columns',
                    column_count=4,
                    is_default=True,
                    is_active=True,
                    created_by=request.user,
                )

            # Redirect to builder with the footer ID
            return HttpResponseRedirect(
                reverse('design:footer_builder', args=[footer.id])
            )

        # Load the specific footer
        footer = get_object_or_404(FooterTemplate, pk=footer_id)

        # Get all footers for the dropdown
        all_footers = FooterTemplate.objects.filter(is_active=True).order_by('name')

        # Get theme CSS URLs
        theme_css_url = None
        brand_css_url = None

        active_theme = get_active_theme()
        if active_theme:
            theme_css_url = active_theme.get_css_url()

        branding = ThemeBranding.objects.first()
        if branding:
            brand_css_url = branding.get_css_url()

        context = {
            'footer': footer,
            'all_footers': all_footers,
            'builder_type': 'footer',
            'api_url': reverse('hf_api:footer_builder', args=[footer.id]),
            'widget_library_url': reverse('hf_api:widget_library'),
            'preset_gallery_url': reverse('hf_api:preset_gallery', args=['footer']),
            'theme_css_url': theme_css_url,
            'brand_css_url': brand_css_url,
        }

        return render(request, 'design/header_footer_builder.html', context)
