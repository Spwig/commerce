"""
Branding Builder View - Visual interface for theme branding customization
"""

from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.decorators import allow_iframe_sameorigin
from django.utils.translation import gettext as _
import json
import hashlib

from .theme_models import ThemeBranding, Theme
from .theme_utils import get_active_theme


@method_decorator(staff_member_required, name='dispatch')
class BrandingBuilderView(View):
    """Main branding builder interface"""

    def get(self, request, branding_id=None):
        """Render the branding builder interface"""

        # Get or create branding
        if branding_id:
            branding = ThemeBranding.objects.filter(pk=branding_id).first()
            if not branding:
                # Requested branding doesn't exist, get or create default
                branding = ThemeBranding.objects.first()
                if not branding:
                    branding = ThemeBranding.objects.create()
        else:
            branding = ThemeBranding.objects.first()
            if not branding:
                branding = ThemeBranding.objects.create()

        # Ensure branding is linked to a theme
        if not branding.theme:
            # Get the active theme from GlobalDesignSettings
            default_theme = get_active_theme()

            # Fall back to starter theme if no active theme is set
            if not default_theme:
                default_theme = Theme.objects.filter(slug='starter', is_active=True).first()

            if default_theme:
                branding.theme = default_theme
                branding.save()

        # Get theme tokens if theme exists
        theme_tokens = {}
        if branding.theme and branding.theme.manifest:
            theme_tokens = branding.theme.manifest.get('tokens', {})

        # Get available themes
        themes = Theme.objects.filter(is_active=True)

        # Prepare branding data for JavaScript (only customizations, not theme defaults)
        element_tokens = branding.element_tokens or {}
        branding_data = {
            'id': branding.id,
            'colors': branding.color_tokens or {},
            'typography': branding.typography_tokens or {},
            'spacing': branding.spacing_tokens or {},
            'borders': branding.border_tokens or {},
            'shadows': branding.shadow_tokens or {},
            'transitions': branding.transition_tokens or {},
            'header': branding.header_tokens or {},
            'footer': branding.footer_tokens or {},
            'menu': branding.menu_tokens or {},
            'search': branding.search_tokens or {},
            'elements': element_tokens,
            'animations': branding.animation_tokens or {},
            'component_overrides': branding.component_overrides or {},
            'custom_css': branding.custom_css or '',
            # Card type tokens (stored in element_tokens with card- prefix)
            'card-default': element_tokens.get('card-default', {}),
            'card-elevated': element_tokens.get('card-elevated', {}),
            'card-bordered': element_tokens.get('card-bordered', {}),
            'card-minimal': element_tokens.get('card-minimal', {}),
        }

        # Prepare theme tokens for JavaScript
        theme_data = {
            'colors': theme_tokens.get('colors', {}),
            'typography': theme_tokens.get('typography', {}),
            'spacing': theme_tokens.get('spacing', {}),
            'borders': theme_tokens.get('borders', {}),
            'shadows': theme_tokens.get('shadows', {}),
            'transitions': theme_tokens.get('transitions', {}),
            'header': theme_tokens.get('header', {}),
            'footer': theme_tokens.get('footer', {}),
            'menu': theme_tokens.get('menu', {}),
            'search': theme_tokens.get('search', {}),
            'elements': theme_tokens.get('elements', {}),
            'animations': theme_tokens.get('animations', {}),
            # Card type tokens (at root level in tokens.json)
            'card-default': theme_tokens.get('card-default', {}),
            'card-elevated': theme_tokens.get('card-elevated', {}),
            'card-bordered': theme_tokens.get('card-bordered', {}),
            'card-minimal': theme_tokens.get('card-minimal', {}),
        }

        # Get theme CSS URL if available
        theme_css_url = None
        if branding.theme:
            theme_css_url = branding.theme.get_css_url() if hasattr(branding.theme, 'get_css_url') else None

        context = {
            'branding': branding,
            'branding_data': json.dumps(branding_data),
            'theme_data': json.dumps(theme_data),
            'theme_css_url': theme_css_url,
            'themes': themes,
            'preview_url': f'/theme/branding/{branding.id}/preview-frame/',
            'title': _('Branding Builder'),
            # admin_theme is provided by context processor, no need to set it here
        }

        return render(request, 'design/branding_builder.html', context)


@method_decorator([staff_member_required, allow_iframe_sameorigin], name='dispatch')
class BrandingPreviewFrameView(View):
    """Isolated preview frame for branding"""

    def get(self, request, branding_id):
        """Render the preview frame without admin styles"""
        branding = get_object_or_404(ThemeBranding, pk=branding_id)

        # Generate CSS for preview
        css_content = branding.generate_css()

        context = {
            'branding': branding,
            'css_content': css_content,
            'show_samples': True,
        }

        return render(request, 'design/branding_preview_frame.html', context)


@method_decorator([staff_member_required, csrf_exempt, allow_iframe_sameorigin], name='dispatch')
class BrandingUpdateView(View):
    """AJAX endpoint for live branding updates"""

    def post(self, request, branding_id):
        """Update branding settings and return new CSS"""
        branding = get_object_or_404(ThemeBranding, pk=branding_id)

        try:
            data = json.loads(request.body)
            update_type = data.get('type')
            values = data.get('values', {})

            # Update the appropriate token set
            if update_type == 'colors':
                if branding.color_tokens is None:
                    branding.color_tokens = {}
                branding.color_tokens.update(values)
            elif update_type == 'typography':
                if branding.typography_tokens is None:
                    branding.typography_tokens = {}
                branding.typography_tokens.update(values)
            elif update_type == 'spacing':
                if branding.spacing_tokens is None:
                    branding.spacing_tokens = {}
                branding.spacing_tokens.update(values)
            elif update_type == 'borders':
                if branding.border_tokens is None:
                    branding.border_tokens = {}
                branding.border_tokens.update(values)
            elif update_type == 'shadows':
                if branding.shadow_tokens is None:
                    branding.shadow_tokens = {}
                branding.shadow_tokens.update(values)
            elif update_type == 'transitions':
                if branding.transition_tokens is None:
                    branding.transition_tokens = {}
                branding.transition_tokens.update(values)
            elif update_type == 'header':
                if branding.header_tokens is None:
                    branding.header_tokens = {}
                branding.header_tokens.update(values)
            elif update_type == 'footer':
                if branding.footer_tokens is None:
                    branding.footer_tokens = {}
                branding.footer_tokens.update(values)
            elif update_type == 'menu':
                if branding.menu_tokens is None:
                    branding.menu_tokens = {}
                branding.menu_tokens.update(values)
            elif update_type == 'search':
                if branding.search_tokens is None:
                    branding.search_tokens = {}
                branding.search_tokens.update(values)
            elif update_type == 'elements':
                if branding.element_tokens is None:
                    branding.element_tokens = {}
                # Handle nested elements structure
                self._update_nested_dict(branding.element_tokens, values)
            elif update_type == 'animations':
                if branding.animation_tokens is None:
                    branding.animation_tokens = {}
                branding.animation_tokens.update(values)
            elif update_type == 'component_overrides':
                if branding.component_overrides is None:
                    branding.component_overrides = {}
                branding.component_overrides.update(values)
            elif update_type == 'custom_css':
                branding.custom_css = values.get('css', '')
            elif update_type in ('card-default', 'card-elevated', 'card-bordered', 'card-minimal'):
                # Card tokens are stored inside element_tokens with their card-* key
                if branding.element_tokens is None:
                    branding.element_tokens = {}
                if update_type not in branding.element_tokens:
                    branding.element_tokens[update_type] = {}
                branding.element_tokens[update_type].update(values)

            # Save and regenerate CSS
            branding.save()
            css_content = branding.generate_css()

            return JsonResponse({
                'success': True,
                'css': css_content,
                'hash': branding.css_hash,
                'message': _('Branding updated successfully')
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

    def _update_nested_dict(self, target, updates):
        """Update nested dictionary with dot-notation keys from values"""
        for key, value in updates.items():
            if '.' in key:
                # Handle dot-notation paths like "elements.button.radius"
                parts = key.split('.')
                current = target
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                target[key] = value


@method_decorator([staff_member_required, csrf_exempt], name='dispatch')
class BrandingSaveView(View):
    """Save all branding changes"""

    def post(self, request, branding_id):
        """Save complete branding configuration"""
        branding = get_object_or_404(ThemeBranding, pk=branding_id)

        try:
            data = json.loads(request.body)

            # Update all token sets
            branding.color_tokens = data.get('colors', {})
            branding.typography_tokens = data.get('typography', {})
            branding.spacing_tokens = data.get('spacing', {})
            branding.border_tokens = data.get('borders', {})
            branding.shadow_tokens = data.get('shadows', {})
            branding.transition_tokens = data.get('transitions', {})
            branding.header_tokens = data.get('header', {})
            branding.footer_tokens = data.get('footer', {})
            branding.menu_tokens = data.get('menu', {})
            branding.search_tokens = data.get('search', {})
            branding.animation_tokens = data.get('animations', {})
            branding.component_overrides = data.get('component_overrides', {})
            branding.custom_css = data.get('custom_css', '')

            # Merge element tokens with card tokens (card tokens are stored in element_tokens)
            element_tokens = data.get('elements', {})
            for card_type in ('card-default', 'card-elevated', 'card-bordered', 'card-minimal'):
                card_data = data.get(card_type, {})
                if card_data:
                    element_tokens[card_type] = card_data
            branding.element_tokens = element_tokens

            # Save and regenerate CSS
            branding.save()
            branding.generate_css()

            return JsonResponse({
                'success': True,
                'message': _('Branding saved successfully'),
                'redirect_url': f'/admin/design/themebranding/{branding.id}/change/'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


@method_decorator(staff_member_required, name='dispatch')
class BrandingExportView(View):
    """Export branding configuration"""

    def get(self, request, branding_id):
        """Export branding as JSON"""
        branding = get_object_or_404(ThemeBranding, pk=branding_id)

        element_tokens = branding.element_tokens or {}
        export_data = {
            'version': '1.2',
            'colors': branding.color_tokens,
            'typography': branding.typography_tokens,
            'spacing': branding.spacing_tokens,
            'borders': branding.border_tokens,
            'shadows': branding.shadow_tokens,
            'transitions': branding.transition_tokens,
            'header': branding.header_tokens,
            'footer': branding.footer_tokens,
            'menu': branding.menu_tokens,
            'search': branding.search_tokens,
            'elements': branding.element_tokens,
            'animations': branding.animation_tokens,
            'component_overrides': branding.component_overrides,
            'custom_css': branding.custom_css,
            # Card type tokens (exported separately for clarity)
            'card-default': element_tokens.get('card-default', {}),
            'card-elevated': element_tokens.get('card-elevated', {}),
            'card-bordered': element_tokens.get('card-bordered', {}),
            'card-minimal': element_tokens.get('card-minimal', {}),
        }

        response = JsonResponse(export_data, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename="branding-{branding.id}.json"'
        return response


@method_decorator([staff_member_required, csrf_exempt], name='dispatch')
class BrandingImportView(View):
    """Import branding configuration"""

    def post(self, request, branding_id):
        """Import branding from JSON"""
        branding = get_object_or_404(ThemeBranding, pk=branding_id)

        try:
            import_file = request.FILES.get('import_file')
            if not import_file:
                raise ValueError(_('No file provided'))

            # Read and parse JSON
            import_data = json.loads(import_file.read())

            # Update branding with imported data
            branding.color_tokens = import_data.get('colors', {})
            branding.typography_tokens = import_data.get('typography', {})
            branding.spacing_tokens = import_data.get('spacing', {})
            branding.border_tokens = import_data.get('borders', {})
            branding.shadow_tokens = import_data.get('shadows', {})
            branding.transition_tokens = import_data.get('transitions', {})
            branding.header_tokens = import_data.get('header', {})
            branding.footer_tokens = import_data.get('footer', {})
            branding.menu_tokens = import_data.get('menu', {})
            branding.search_tokens = import_data.get('search', {})
            branding.animation_tokens = import_data.get('animations', {})
            branding.component_overrides = import_data.get('component_overrides', {})
            branding.custom_css = import_data.get('custom_css', '')

            # Merge element tokens with card tokens (card tokens stored in element_tokens)
            element_tokens = import_data.get('elements', {})
            for card_type in ('card-default', 'card-elevated', 'card-bordered', 'card-minimal'):
                card_data = import_data.get(card_type, {})
                if card_data:
                    element_tokens[card_type] = card_data
            branding.element_tokens = element_tokens

            # Save and regenerate CSS
            branding.save()
            branding.generate_css()

            return JsonResponse({
                'success': True,
                'message': _('Branding imported successfully')
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)