"""
Design Dashboard - Central hub for all design and theme management
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Q
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .models import (
    DesignToken, ComponentStyle,
    GlobalDesignSettings, CustomCSS
)
from .theme_models import (
    Theme, ThemeBranding, ThemeInstallation, ThemeAsset
)
from .header_footer_models import (
    HeaderTemplate, FooterTemplate, Widget,
    WidgetPlacement, Menu, MenuItem
)


@method_decorator(staff_member_required, name='dispatch')
class DesignDashboardView(View):
    """Main dashboard for design and theme management"""

    def get(self, request):
        print("=" * 100)
        print("DASHBOARD VIEW GET METHOD CALLED")
        print("=" * 100)

        active_theme_result = self.get_active_theme()
        print(f"DASHBOARD: active_theme_result = {active_theme_result}")
        print(f"DASHBOARD: active_theme_result type = {type(active_theme_result)}")

        # Get design settings
        design_settings = GlobalDesignSettings.get_settings()

        context = {
            'title': 'Design & Theme Dashboard',

            # Statistics
            'stats': self.get_statistics(),

            # Quick access items
            'active_theme': active_theme_result,
            'recent_activity': self.get_recent_activity(),

            # Component counts
            'components': self.get_component_counts(),

            # Quick actions URLs
            'urls': self.get_quick_action_urls(),

            # Workflow sections
            'workflow_sections': self.get_workflow_sections(),

            # Dark mode setting
            'force_light_mode': design_settings.force_light_mode,
            'theme_supports_dark_mode': (
                active_theme_result['theme'].supports_dark_mode
                if active_theme_result and active_theme_result.get('theme')
                else False
            ),
        }

        print(f"DASHBOARD: context['active_theme'] = {context['active_theme']}")
        print("=" * 100)

        return render(request, 'design/dashboard.html', context)

    def get_statistics(self):
        """Get dashboard statistics"""
        return {
            'themes_installed': Theme.objects.count(),
            'active_widgets': Widget.objects.filter(is_active=True).count(),
            'total_menus': Menu.objects.count(),
            'menu_items': MenuItem.objects.filter(is_active=True).count(),
            'headers': HeaderTemplate.objects.filter(is_active=True).count(),
            'footers': FooterTemplate.objects.filter(is_active=True).count(),
            'design_tokens': DesignToken.objects.filter(is_active=True).count(),
            'custom_css_rules': CustomCSS.objects.filter(is_active=True).count(),
        }

    def get_active_theme(self):
        """Get currently active theme information from authoritative sources"""
        import os
        import logging
        from .theme_utils import get_active_theme_with_metadata
        from .models import GlobalDesignSettings

        logger = logging.getLogger(__name__)

        logger.info("=" * 80)
        logger.info("DEBUG: get_active_theme() called")

        # Get theme with metadata from ComponentRegistry
        try:
            theme_data = get_active_theme_with_metadata()
            logger.info(f"DEBUG: theme_data = {theme_data}")
        except Exception as e:
            logger.error(f"DEBUG: Error getting theme_data: {e}", exc_info=True)
            return None

        branding = ThemeBranding.objects.first()
        logger.info(f"DEBUG: branding = {branding}")

        if theme_data:
            theme = theme_data['theme']
            logger.info(f"DEBUG: theme = {theme}")
            logger.info(f"DEBUG: theme.name = {theme.name if theme else 'None'}")
            logger.info(f"DEBUG: theme.slug = {theme.slug if theme else 'None'}")

            # Get theme CSS file size
            css_size = 0
            if theme.extracted_path:
                css_file = os.path.join(theme.extracted_path, 'theme', 'css', 'theme.css')
                logger.info(f"DEBUG: Looking for CSS at: {css_file}")
                if os.path.exists(css_file):
                    css_size = os.path.getsize(css_file)
                    logger.info(f"DEBUG: CSS size: {css_size}")

            result = {
                'theme': theme,
                'name': theme_data['name'],
                'version': theme_data['version'],
                'author': theme_data['author'],  # From ComponentRegistry (Spwig)
                'branding': branding,
                'css_size': css_size,
                'last_update': theme.updated_at,
            }
            logger.info(f"DEBUG: Returning active_theme dict: {result}")
            logger.info("=" * 80)
            return result
        else:
            logger.warning("DEBUG: theme_data is None/False, returning None")
            logger.info("=" * 80)
            return None

    def get_recent_activity(self):
        """Get recent design-related activities"""
        activities = []

        # Recent theme installations
        recent_installations = ThemeInstallation.objects.select_related('theme', 'installed_by').order_by('-installed_at')[:3]
        for install in recent_installations:
            activities.append({
                'type': 'theme_install',
                'icon': 'fa-download',
                'color': 'success',
                'title': f'Theme "{install.theme.name}" installed',
                'user': install.installed_by,
                'timestamp': install.installed_at,
            })

        # Recent widget updates
        recent_widgets = Widget.objects.order_by('-updated_at')[:3]
        for widget in recent_widgets:
            activities.append({
                'type': 'widget_update',
                'icon': 'fa-puzzle-piece',
                'color': 'info',
                'title': f'Widget "{widget.name}" updated',
                'user': widget.created_by,
                'timestamp': widget.updated_at,
            })

        # Recent menu changes
        recent_menus = Menu.objects.order_by('-updated_at')[:3]
        for menu in recent_menus:
            activities.append({
                'type': 'menu_update',
                'icon': 'fa-bars',
                'color': 'warning',
                'title': f'Menu "{menu.name}" modified',
                'user': menu.created_by,
                'timestamp': menu.updated_at,
            })

        # Sort by timestamp and return top 5
        activities.sort(key=lambda x: x['timestamp'] if x['timestamp'] else timezone.now() - timedelta(days=365), reverse=True)
        return activities[:5]

    def get_component_counts(self):
        """Get counts for different component types"""
        return {
            'headers': {
                'total': HeaderTemplate.objects.count(),
                'active': HeaderTemplate.objects.filter(is_active=True).count(),
                'default': HeaderTemplate.objects.filter(is_default=True).count(),
            },
            'footers': {
                'total': FooterTemplate.objects.count(),
                'active': FooterTemplate.objects.filter(is_active=True).count(),
                'default': FooterTemplate.objects.filter(is_default=True).count(),
            },
            'widgets': {
                'total': Widget.objects.count(),
                'active': Widget.objects.filter(is_active=True).count(),
                'by_type': Widget.objects.values('widget_type').annotate(count=Count('id')),
            },
            'menus': {
                'total': Menu.objects.count(),
                'active': Menu.objects.filter(is_active=True).count(),
                'by_location': Menu.objects.values('location').annotate(count=Count('id')),
            },
        }

    def get_quick_action_urls(self):
        """Get URLs for quick actions"""
        return {
            # Theme management (unified interface)
            'install_theme': reverse('admin:unified_theme_management'),
            'manage_themes': reverse('admin:unified_theme_management'),
            'branding': self.get_branding_url(),

            # Structure
            'headers': reverse('admin:design_headertemplate_changelist'),
            'footers': reverse('admin:design_footertemplate_changelist'),
            'menus': reverse('admin:design_menu_changelist'),

            # Components
            'widgets': reverse('admin:design_widget_changelist'),
            'component_styles': reverse('admin:design_componentstyle_changelist'),
            'design_tokens': reverse('admin:design_designtoken_changelist'),

            # Content
            'pages': reverse('admin:page_builder_page_changelist'),
            'page_templates': reverse('admin:page_builder_pagetemplate_changelist'),
            'custom_css': reverse('admin:design_customcss_changelist'),

            # Tools
            'regenerate_css': reverse('design:regenerate_css') if self.url_exists('design:regenerate_css') else '#',
            'clear_cache': reverse('design:clear_theme_cache') if self.url_exists('design:clear_theme_cache') else '#',
            'preview_site': '/',
        }

    def get_branding_url(self):
        """Get URL for branding configuration"""
        branding = ThemeBranding.objects.first()
        if not branding:
            # Auto-create branding linked to the active theme
            active_theme = Theme.objects.filter(is_active=True).first()
            branding = ThemeBranding.objects.create(theme=active_theme)
        return reverse('design:branding_builder', args=[branding.pk])

    def url_exists(self, url_name):
        """Check if a URL name exists"""
        try:
            reverse(url_name)
            return True
        except:
            return False

    def get_workflow_sections(self):
        """Get organized workflow sections"""
        return [
            {
                'id': 'theme_foundation',
                'title': 'Theme Foundation',
                'icon': 'fa-paint-brush',
                'description': 'Core theme setup and branding',
                'color': 'primary',
                'items': [
                    {
                        'title': 'Theme Packages',
                        'description': 'Install and manage theme packages',
                        'url': reverse('admin:unified_theme_management'),
                        'icon': 'fa-download',
                        'badge': Theme.objects.count(),
                    },
                    {
                        'title': 'Branding',
                        'description': 'Colors, typography, spacing',
                        'url': self.get_branding_url(),
                        'icon': 'fa-palette',
                        'badge': 'Configure',
                    },
                    {
                        'title': 'Page Templates',
                        'description': 'Choose checkout, product, and category page layouts',
                        'url': reverse('design:template_config'),
                        'icon': 'fa-columns',
                        'badge': 'Configure',
                    },
                    {
                        'title': 'Design Tokens',
                        'description': 'Advanced token management',
                        'url': reverse('admin:design_designtoken_changelist'),
                        'icon': 'fa-coins',
                        'badge': DesignToken.objects.filter(is_active=True).count(),
                    },
                    {
                        'title': 'Image Processing',
                        'description': 'Thumbnail sizes, regeneration, and image optimization',
                        'url': reverse('media_library_admin:image_processing'),
                        'icon': 'fa-images',
                        'badge': 'Manage',
                    },
                ]
            },
            {
                'id': 'site_structure',
                'title': 'Site Structure',
                'icon': 'fa-sitemap',
                'description': 'Headers, footers, and navigation',
                'color': 'success',
                'items': [
                    {
                        'title': 'Header Builder',
                        'description': 'Visual header builder (drag & drop)',
                        'url': reverse('design:header_builder_default'),
                        'icon': 'fa-paint-brush',
                        'badge': 'Build',
                        'highlight': True,
                    },
                    {
                        'title': 'Footer Builder',
                        'description': 'Visual footer builder (drag & drop)',
                        'url': reverse('design:footer_builder_default'),
                        'icon': 'fa-paint-brush',
                        'badge': 'Build',
                        'highlight': True,
                    },
                    {
                        'title': 'Menu Builder',
                        'description': 'Visual menu builder (drag & drop)',
                        'url': reverse('design:menu_builder_default'),
                        'icon': 'fa-bars',
                        'badge': 'Build',
                        'highlight': True,
                    },
                    {
                        'title': 'Manage Headers',
                        'description': 'List and configure headers',
                        'url': reverse('admin:design_headertemplate_changelist'),
                        'icon': 'fa-heading',
                        'badge': HeaderTemplate.objects.count(),
                    },
                    {
                        'title': 'Manage Footers',
                        'description': 'List and configure footers',
                        'url': reverse('admin:design_footertemplate_changelist'),
                        'icon': 'fa-shoe-prints',
                        'badge': FooterTemplate.objects.count(),
                    },
                    {
                        'title': 'Menus',
                        'description': 'Navigation menus',
                        'url': reverse('admin:design_menu_changelist'),
                        'icon': 'fa-bars',
                        'badge': Menu.objects.count(),
                    },
                    {
                        'title': 'Widgets',
                        'description': 'Manage header/footer widgets',
                        'url': reverse('admin:design_widget_changelist'),
                        'icon': 'fa-puzzle-piece',
                        'badge': Widget.objects.count(),
                    },
                ]
            },
            {
                'id': 'components_widgets',
                'title': 'Components & Widgets',
                'icon': 'fa-puzzle-piece',
                'description': 'Reusable components and widgets',
                'color': 'info',
                'items': [
                    {
                        'title': 'Component Styles',
                        'description': 'Component style presets',
                        'url': reverse('admin:design_componentstyle_changelist'),
                        'icon': 'fa-layer-group',
                        'badge': ComponentStyle.objects.count(),
                    },
                    {
                        'title': 'Themes',
                        'description': 'Manage shop themes',
                        'url': reverse('admin:unified_theme_management'),
                        'icon': 'fa-swatchbook',
                        'badge': Theme.objects.count(),
                    },
                ]
            },
            {
                'id': 'content_management',
                'title': 'Content Management',
                'icon': 'fa-file-alt',
                'description': 'Pages and content templates',
                'color': 'warning',
                'items': [
                    {
                        'title': 'Pages',
                        'description': 'Site pages and content',
                        'url': reverse('admin:page_builder_page_changelist'),
                        'icon': 'fa-file',
                        'badge': self.get_page_count(),
                    },
                    {
                        'title': 'Page Templates',
                        'description': 'Reusable page layouts',
                        'url': reverse('admin:page_builder_pagetemplate_changelist'),
                        'icon': 'fa-clipboard',
                        'badge': self.get_page_template_count(),
                    },
                    {
                        'title': 'Custom CSS',
                        'description': 'Custom style rules',
                        'url': reverse('admin:design_customcss_changelist'),
                        'icon': 'fa-code',
                        'badge': CustomCSS.objects.count(),
                    },
                    {
                        'title': 'Custom Elements',
                        'description': 'Data-bound UI components',
                        'url': reverse('admin:element_builder_customelement_changelist'),
                        'icon': 'fa-puzzle-piece',
                        'badge': self.get_custom_element_count(),
                    },
                ]
            },
            {
                'id': 'visibility_rules',
                'title': 'Visibility Rules',
                'icon': 'fa-eye',
                'description': 'Conditional display rules for elements',
                'color': 'danger',
                'items': [
                    {
                        'title': 'Visibility Rules',
                        'description': 'Create individual visibility conditions',
                        'url': reverse('admin:page_builder_visibilityrule_changelist'),
                        'icon': 'fa-filter',
                        'badge': self.get_visibility_rule_count(),
                    },
                    {
                        'title': 'Rule Groups',
                        'description': 'Combine rules with AND/OR logic',
                        'url': reverse('admin:page_builder_rulegroup_changelist'),
                        'icon': 'fa-layer-group',
                        'badge': self.get_rule_group_count(),
                    },
                    {
                        'title': 'Elements',
                        'description': 'Manage page elements with visibility',
                        'url': reverse('admin:page_builder_element_changelist'),
                        'icon': 'fa-shapes',
                        'badge': self.get_element_count(),
                    },
                ]
            },
            {
                'id': 'email_templates',
                'title': 'Email Templates',
                'icon': 'fa-envelope',
                'description': 'Transactional email templates with multi-language support',
                'color': 'warning',
                'items': [
                    {
                        'title': 'Manage Templates',
                        'description': 'Edit email templates with MJML editor',
                        'url': reverse('email_system:template_list'),
                        'icon': 'fa-envelope',
                        'badge': self._get_email_template_stats()['active'],
                        'highlight': True,
                    },
                    {
                        'title': 'Translations',
                        'description': 'Translate templates to multiple languages',
                        'url': reverse('email_system:translation_manager'),
                        'icon': 'fa-language',
                        'badge': self._get_email_template_stats()['coverage'],
                    },
                    {
                        'title': 'Preview & Test',
                        'description': 'Preview templates with sample data',
                        'url': reverse('email_system:template_list'),
                        'icon': 'fa-eye',
                        'badge': 'Test',
                    },
                ]
            },
        ]

    def get_page_count(self):
        """Get page count if page_builder is installed"""
        try:
            from page_builder.models import Page
            return Page.objects.count()
        except:
            return 0

    def get_page_template_count(self):
        """Get page template count if page_builder is installed"""
        try:
            from page_builder.models import PageTemplate
            return PageTemplate.objects.count()
        except:
            return 0

    def get_visibility_rule_count(self):
        """Get visibility rule count"""
        try:
            from page_builder.models import VisibilityRule
            return VisibilityRule.objects.filter(is_active=True).count()
        except:
            return 0

    def get_rule_group_count(self):
        """Get rule group count"""
        try:
            from page_builder.models import RuleGroup
            return RuleGroup.objects.filter(is_active=True).count()
        except:
            return 0

    def get_element_count(self):
        """Get element count"""
        try:
            from page_builder.models import Element
            return Element.objects.filter(is_active=True).count()
        except:
            return 0

    def get_custom_element_count(self):
        """Get custom element count from element_builder"""
        try:
            from element_builder.models import CustomElement
            return CustomElement.objects.filter(is_active=True).count()
        except:
            return 0

    def _get_email_template_stats(self):
        """Get email template statistics for dashboard"""
        try:
            from email_system.models import EmailTemplate, EmailTemplateTranslation

            total_templates = EmailTemplate.objects.count()
            active_templates = EmailTemplate.objects.filter(is_active=True).count()
            total_translations = EmailTemplateTranslation.objects.count()

            # Calculate translation coverage (6 languages excluding English)
            system_templates = EmailTemplate.objects.filter(is_system=True, language_code='en').count()
            max_translations = system_templates * 6 if system_templates > 0 else 0
            coverage_percentage = (total_translations / max_translations * 100) if max_translations > 0 else 0

            return {
                'total': total_templates,
                'active': active_templates,
                'translations': total_translations,
                'coverage': f"{coverage_percentage:.0f}%",
            }
        except Exception:
            # If email_system is not installed or has errors
            return {
                'total': 0,
                'active': 0,
                'translations': 0,
                'coverage': '0%',
            }


@method_decorator(staff_member_required, name='dispatch')
class RegenerateCSSView(View):
    """Regenerate theme CSS"""

    def post(self, request):
        from .theme_models import ThemeBranding

        branding = ThemeBranding.objects.first()
        if branding:
            branding.generate_css()
            cache.delete_pattern('theme_*')
            cache.delete_pattern('active_theme*')

        return redirect('design:dashboard')


@method_decorator(staff_member_required, name='dispatch')
class ClearThemeCacheView(View):
    """Clear all theme-related caches"""

    def post(self, request):
        cache.delete_pattern('theme_*')
        cache.delete_pattern('active_theme*')
        cache.delete('current_theme')

        return redirect('design:dashboard')


@method_decorator(staff_member_required, name='dispatch')
class ToggleForceLightModeView(View):
    """Toggle force light mode setting"""

    def post(self, request):
        """Toggle the force_light_mode setting"""
        import json

        try:
            data = json.loads(request.body)
            force_light = data.get('force_light_mode', False)

            settings = GlobalDesignSettings.get_settings()
            settings.force_light_mode = force_light
            settings.save(update_fields=['force_light_mode'])

            return JsonResponse({
                'success': True,
                'force_light_mode': settings.force_light_mode
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)