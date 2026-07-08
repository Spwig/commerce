"""
Theme system views for CSS generation and theme management
"""

import hashlib
import logging
import os
import re
from pathlib import Path

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
import json

from .theme_models import Theme, ThemeBranding
from .theme_service import theme_service

logger = logging.getLogger(__name__)


class BrandCSSView(View):
    """Serve generated brand CSS with hash-based caching.

    Uses the css_hash as a cache key so changes are served immediately.
    The URL includes ?v={hash} for browser cache busting.
    """

    def get(self, request):
        """Generate and return brand CSS"""
        try:
            branding = ThemeBranding.objects.first()
            if not branding:
                # Return empty CSS if no branding configured
                return HttpResponse(
                    "/* No branding configured */",
                    content_type='text/css'
                )

            # Generate CSS if not already generated or if hash is missing
            if not branding.generated_css or not branding.css_hash:
                branding.generate_css()

            # Use hash-based cache key - new hash = new cache entry
            cache_key = f'brand_css_{branding.css_hash}'
            css_content = cache.get(cache_key)

            if css_content is None:
                css_content = branding.generated_css
                # Cache for 24 hours - hash change creates new key
                cache.set(cache_key, css_content, 86400)

            # Return CSS with cache headers
            # URL includes ?v={hash} for cache busting, safe for long cache
            response = HttpResponse(css_content, content_type='text/css')
            response['Cache-Control'] = 'public, max-age=86400'  # 24h (hash-busted URL)
            response['ETag'] = f'"{branding.css_hash}"'
            response['Vary'] = 'Accept-Encoding'
            response['X-Branding-Hash'] = branding.css_hash  # Debug header

            return response

        except Exception as e:
            return HttpResponse(
                f"/* Error generating CSS: {str(e)} */",
                content_type='text/css',
                status=500
            )


class LayeredCSSView(View):
    """Serve complete layered CSS (base + theme + brand)"""

    def get(self, request):
        """Generate complete CSS stack"""
        css_content = theme_service.generate_layered_css(request)

        response = HttpResponse(css_content, content_type='text/css')
        response['Cache-Control'] = 'public, max-age=3600'  # 1 hour
        response['Vary'] = 'Accept-Encoding'

        return response


class ThemeCSSView(View):
    """Serve theme CSS from database with hash-based caching.

    This view serves compiled theme CSS stored in the database,
    which survives platform updates (unlike filesystem extraction).
    Uses hash-based cache keys so theme changes are served immediately.
    """

    def get(self, request, slug):
        """Serve theme CSS for the given theme slug."""
        from django.core.cache import cache

        theme = get_object_or_404(Theme, slug=slug, is_active=True)

        # If compiled_css is empty, try to extract and populate
        if not theme.compiled_css:
            theme.extract_theme()
            # Refresh from DB after extraction
            theme.refresh_from_db()

        # Still empty? Return error CSS
        if not theme.compiled_css:
            return HttpResponse(
                f"/* Theme '{slug}' has no compiled CSS */",
                content_type='text/css',
                status=404
            )

        # Cache key includes hash - new hash = new cache entry
        cache_key = f'theme_css_{slug}_{theme.css_hash}'
        cached_css = cache.get(cache_key)

        if cached_css:
            css_content = cached_css
        else:
            css_content = theme.compiled_css
            cache.set(cache_key, css_content, 60 * 60)  # 1 hour

        response = HttpResponse(css_content, content_type='text/css')
        response['Cache-Control'] = 'public, max-age=86400'  # 24h (hash-busted URL)
        response['ETag'] = f'"{theme.css_hash}"'
        response['Vary'] = 'Accept-Encoding'

        return response


class ThemePreviewView(View):
    """Preview theme with temporary branding tokens"""

    @method_decorator(staff_member_required)
    def post(self, request, theme_id):
        """Generate preview CSS with temporary tokens"""
        try:
            data = json.loads(request.body)
            branding_tokens = data.get('tokens', {})

            preview_css = theme_service.preview_theme(theme_id, branding_tokens)

            return HttpResponse(preview_css, content_type='text/css')

        except Theme.DoesNotExist:
            return HttpResponse(
                "/* Theme not found */",
                content_type='text/css',
                status=404
            )
        except json.JSONDecodeError:
            return HttpResponse(
                "/* Invalid JSON data */",
                content_type='text/css',
                status=400
            )


class ThemeTokenDiffView(View):
    """Show token differences between theme and current branding"""

    @method_decorator(staff_member_required)
    def get(self, request, theme_id):
        """Get token diff for theme installation"""
        try:
            theme = Theme.objects.get(id=theme_id)
            branding = ThemeBranding.objects.first()

            theme_tokens = theme.get_tokens()
            brand_tokens = {}

            if branding:
                # Collect all brand tokens
                for attr in ['color_tokens', 'typography_tokens',
                             'spacing_tokens', 'border_tokens']:
                    brand_tokens.update(getattr(branding, attr, {}))

            # Calculate differences
            new_tokens = []
            kept_tokens = []
            updated_tokens = []

            for token, value in theme_tokens.items():
                if token not in brand_tokens:
                    new_tokens.append({
                        'token': token,
                        'theme_value': value
                    })
                elif brand_tokens[token] != value:
                    updated_tokens.append({
                        'token': token,
                        'brand_value': brand_tokens[token],
                        'theme_value': value
                    })
                else:
                    kept_tokens.append({
                        'token': token,
                        'value': value
                    })

            return JsonResponse({
                'new_tokens': new_tokens,
                'kept_tokens': kept_tokens,
                'updated_tokens': updated_tokens,
                'summary': {
                    'new': len(new_tokens),
                    'kept': len(kept_tokens),
                    'updated': len(updated_tokens),
                }
            })

        except Theme.DoesNotExist:
            return JsonResponse({
                'error': 'Theme not found'
            }, status=404)


class AdoptThemePaletteView(View):
    """Allow merchant to adopt theme's default palette"""

    @method_decorator(staff_member_required)
    def post(self, request, theme_id):
        """Replace brand tokens with theme defaults"""
        try:
            theme = Theme.objects.get(id=theme_id)
            data = json.loads(request.body)
            token_types = data.get('token_types', ['color'])

            branding, created = ThemeBranding.objects.get_or_create(
                theme=theme
            )

            theme_tokens = theme.get_tokens()

            # Update selected token types
            for token_type in token_types:
                if token_type == 'color':
                    branding.color_tokens = {
                        k: v for k, v in theme_tokens.items()
                        if k.startswith('color-') or k.startswith('brand-')
                    }
                elif token_type == 'typography':
                    branding.typography_tokens = {
                        k: v for k, v in theme_tokens.items()
                        if k.startswith('font-') or k.startswith('text-')
                    }
                elif token_type == 'spacing':
                    branding.spacing_tokens = {
                        k: v for k, v in theme_tokens.items()
                        if k.startswith('spacing-') or k.startswith('gap-')
                    }

            branding.save()
            branding.generate_css()

            return JsonResponse({
                'success': True,
                'message': f"Adopted {', '.join(token_types)} tokens from theme"
            })

        except Theme.DoesNotExist:
            return JsonResponse({
                'error': 'Theme not found'
            }, status=404)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)


# ---------------------------------------------------------------------------
# Editor Content CSS - Typography rules scoped to .ck-content
# Mirrors design/static/design/platform/components.css base styles
# ---------------------------------------------------------------------------

EDITOR_SCOPE = '.ck-content.ck-editor__editable'

EDITOR_TYPOGRAPHY_CSS = f"""
/* Typography rules — mirrors platform components.css */
/* Explicitly overrides Django admin and admin-base.css global element rules */

{EDITOR_SCOPE} {{
  font-family: var(--theme-font-sans, system-ui, -apple-system, sans-serif);
  font-size: var(--theme-font-size-base, 1rem);
  line-height: var(--theme-line-height-normal, 1.6);
  color: var(--theme-color-text, #1a1a1a);
  background-color: var(--theme-color-background, #ffffff);
}}

{EDITOR_SCOPE} h1,
{EDITOR_SCOPE} h2,
{EDITOR_SCOPE} h3,
{EDITOR_SCOPE} h4,
{EDITOR_SCOPE} h5,
{EDITOR_SCOPE} h6 {{
  color: var(--theme-color-text, #1a1a1a) !important;
  font-family: var(--theme-font-family-heading, var(--theme-font-sans, inherit)) !important;
  font-weight: var(--theme-font-weight-bold, 700) !important;
  font-size: inherit !important;
  line-height: var(--theme-line-height-tight, 1.25) !important;
  margin: 1.2em 0 0.4em 0 !important;
  padding: 0 !important;
  background: none !important;
  border: none !important;
  border-radius: 0 !important;
  text-transform: none !important;
  letter-spacing: normal !important;
  text-align: inherit !important;
}}

{EDITOR_SCOPE} h1 {{ font-size: var(--theme-font-size-4xl, 2.25rem) !important; }}
{EDITOR_SCOPE} h2 {{ font-size: var(--theme-font-size-3xl, 1.875rem) !important; }}
{EDITOR_SCOPE} h3 {{ font-size: var(--theme-font-size-2xl, 1.5rem) !important; }}
{EDITOR_SCOPE} h4 {{ font-size: var(--theme-font-size-xl, 1.25rem) !important; }}
{EDITOR_SCOPE} h5 {{ font-size: var(--theme-font-size-lg, 1.125rem) !important; }}
{EDITOR_SCOPE} h6 {{ font-size: var(--theme-font-size-base, 1rem) !important; }}

{EDITOR_SCOPE} p {{
  margin: 0 0 var(--theme-space-4, 1rem) 0;
  padding: 0;
  line-height: var(--theme-line-height-normal, 1.6);
}}

{EDITOR_SCOPE} a,
{EDITOR_SCOPE} a:link,
{EDITOR_SCOPE} a:visited {{
  color: var(--theme-color-primary, #2563eb);
  text-decoration: underline;
}}
{EDITOR_SCOPE} a:hover,
{EDITOR_SCOPE} a:focus {{
  color: var(--theme-color-primary-hover, #1d4ed8);
  text-decoration: underline;
}}

{EDITOR_SCOPE} blockquote {{
  border-left: 4px solid var(--theme-color-primary, #2563eb);
  padding: var(--theme-space-4, 1rem) var(--theme-space-6, 1.5rem);
  color: var(--theme-color-text-muted, #6b7280);
  font-style: italic;
  font-size: var(--theme-font-size-base, 1rem);
  margin: var(--theme-space-4, 1rem) 0;
}}

{EDITOR_SCOPE} ul,
{EDITOR_SCOPE} ol {{
  margin: var(--theme-space-4, 1rem) 0;
  padding-left: var(--theme-space-8, 2rem);
}}

{EDITOR_SCOPE} ul {{ list-style-type: disc; }}
{EDITOR_SCOPE} ol {{ list-style-type: decimal; }}

{EDITOR_SCOPE} li,
{EDITOR_SCOPE} ul > li {{
  font-size: inherit;
  line-height: var(--theme-line-height-normal, 1.6);
  margin-bottom: var(--theme-space-1, 0.25rem);
  padding: 0;
  list-style-type: inherit;
}}

{EDITOR_SCOPE} code {{
  font-family: var(--theme-font-mono, ui-monospace, 'Cascadia Code', monospace);
  color: var(--theme-color-text, #1a1a1a);
  background: var(--theme-color-surface, #f3f4f6);
  padding: 0.15em 0.4em;
  border-radius: var(--theme-radius-sm, 0.25rem);
  font-size: 0.9em;
}}

{EDITOR_SCOPE} pre {{
  font-family: var(--theme-font-mono, ui-monospace, 'Cascadia Code', monospace);
  color: var(--theme-color-text, #1a1a1a);
  background: var(--theme-color-surface, #f3f4f6);
  padding: var(--theme-space-4, 1rem);
  border-radius: var(--theme-radius-md, 0.5rem);
  font-size: var(--theme-font-size-sm, 0.875rem);
  overflow-x: auto;
  margin: var(--theme-space-4, 1rem) 0;
}}

{EDITOR_SCOPE} hr {{
  clear: none;
  border: none;
  border-top: 1px solid var(--theme-color-border, #e5e7eb);
  background-color: transparent;
  height: auto;
  margin: var(--theme-space-6, 1.5rem) 0;
  padding: 0;
  line-height: normal;
}}

{EDITOR_SCOPE} img {{
  max-width: 100%;
  height: auto;
}}

{EDITOR_SCOPE} table {{
  border-collapse: collapse;
  width: 100%;
  margin: var(--theme-space-4, 1rem) 0;
}}

{EDITOR_SCOPE} th,
{EDITOR_SCOPE} td {{
  border: 1px solid var(--theme-color-border, #e5e7eb);
  padding: var(--theme-space-2, 0.5rem) var(--theme-space-3, 0.75rem);
  text-align: left;
  font-size: var(--theme-font-size-base, 1rem);
  line-height: var(--theme-line-height-normal, 1.6);
}}

{EDITOR_SCOPE} th {{
  font-weight: var(--theme-font-weight-semibold, 600);
  background: var(--theme-color-surface, #f3f4f6);
  color: var(--theme-color-text, #1a1a1a);
}}

{EDITOR_SCOPE} figure.image {{
  margin: var(--theme-space-4, 1rem) 0;
}}

{EDITOR_SCOPE} figcaption {{
  font-size: var(--theme-font-size-sm, 0.875rem);
  color: var(--theme-color-text-muted, #6b7280);
  text-align: center;
  margin-top: var(--theme-space-2, 0.5rem);
}}
"""


class EditorContentCSSView(View):
    """Serve theme-aware CSS for CKEditor5 editing areas.

    Generates a self-contained CSS file that:
    1. Scopes theme token variables to .ck-content.ck-editor__editable
    2. Includes brand override variables
    3. Applies typography rules using those variables

    This gives merchants a WYSIWYG preview of storefront styles while editing.
    Loaded automatically on all admin pages with CKEditor via CKEDITOR_5_CUSTOM_CSS.
    """

    def get(self, request):
        from .theme_utils import get_active_theme_cached

        theme = get_active_theme_cached()
        branding = ThemeBranding.objects.first()

        theme_hash = theme.css_hash if theme else ''
        brand_hash = branding.css_hash if branding and branding.css_hash else ''
        combined_hash = hashlib.md5(
            f'{theme_hash}:{brand_hash}'.encode()
        ).hexdigest()[:8]

        cache_key = f'editor_content_css_{combined_hash}'
        css_content = cache.get(cache_key)

        if css_content is None:
            css_content = self._generate_css(theme, branding)
            cache.set(cache_key, css_content, 300)  # 5 min

        response = HttpResponse(css_content, content_type='text/css')
        response['Cache-Control'] = 'private, max-age=300'
        response['ETag'] = f'"{combined_hash}"'
        return response

    def _generate_css(self, theme, branding):
        parts = [
            '/* Editor Content Styles — auto-generated from active theme */',
            '/* Scoped to .ck-content to avoid affecting admin UI */',
            '',
        ]

        # 1. Theme token variables scoped to editor
        token_css = self._get_token_css(theme)
        if token_css:
            scoped = self._scope_root_to_editor(token_css)
            parts.append('/* --- Theme token variables --- */')
            parts.append(scoped)
            parts.append('')

        # 2. Brand override variables
        if branding:
            if not branding.generated_css or not branding.css_hash:
                branding.generate_css()
            if branding.generated_css:
                scoped_brand = self._scope_root_to_editor(branding.generated_css)
                parts.append('/* --- Brand overrides --- */')
                parts.append(scoped_brand)
                parts.append('')

        # 3. Typography rules
        parts.append('/* --- Typography rules --- */')
        parts.append(EDITOR_TYPOGRAPHY_CSS)

        # 4. Background/text overrides matching dark.css specificity
        parts.append(self._generate_background_overrides(theme))

        return '\n'.join(parts)

    def _generate_background_overrides(self, theme):
        """Generate background/text overrides that beat admin dark.css.

        dark.css sets background: #0d0d0d !important on the editor at
        specificity 0,0,4,0. We match that specificity and load later
        so source order wins.

        For themes without dark mode: always show the theme's base
        background regardless of admin mode.
        For themes with dark mode: respond to admin's dark/light toggle.
        """
        S = EDITOR_SCOPE
        lines = [
            '',
            '/* --- Editor background/text — storefront theme match --- */',
        ]

        if theme and theme.supports_dark_mode:
            lines.extend([
                f'[data-theme="dark"] .ck.ck-editor__main > {S} {{',
                '  background: var(--theme-color-bg-primary,'
                ' var(--theme-color-background, #0d0d0d)) !important;',
                '  color: var(--theme-color-text-primary,'
                ' var(--theme-color-text, #e0e0e0)) !important;',
                '}',
                f'[data-theme="light"] .ck.ck-editor__main > {S} {{',
                '  background: var(--theme-color-background,'
                ' #ffffff) !important;',
                '  color: var(--theme-color-text,'
                ' #1a1a1a) !important;',
                '}',
            ])
        else:
            # Theme has no dark mode — always show theme's base colors
            lines.extend([
                f'[data-theme="dark"] .ck.ck-editor__main > {S} {{',
                '  background: var(--theme-color-background,'
                ' #ffffff) !important;',
                '  color: var(--theme-color-text,'
                ' #1a1a1a) !important;',
                '}',
            ])

        return '\n'.join(lines)

    def _get_token_css(self, theme):
        """Get token CSS from theme, preferring tokens.json regeneration."""
        if not theme:
            return ''

        # Primary: regenerate from tokens.json for clean output
        if theme.extracted_path:
            tokens_json = Path(theme.extracted_path) / 'theme' / 'tokens.json'
            if tokens_json.exists():
                try:
                    from .services.token_css_generator import generate_tokens_css
                    return generate_tokens_css(
                        tokens_json,
                        theme.name,
                        dark_mode_enabled=theme.supports_dark_mode,
                    )
                except Exception as e:
                    logger.warning(f"Failed to generate token CSS from tokens.json: {e}")

        # Fallback: extract :root blocks from compiled_css
        if theme.compiled_css:
            return self._extract_root_blocks(theme.compiled_css)

        return ''

    def _extract_root_blocks(self, css_text):
        """Extract :root { ... } blocks from compiled CSS."""
        blocks = []
        pos = 0
        while pos < len(css_text):
            idx = css_text.find(':root', pos)
            if idx == -1:
                break
            # Make sure this is actually a selector, not inside a comment
            brace = css_text.find('{', idx)
            if brace == -1:
                break
            # Find matching closing brace
            depth = 1
            j = brace + 1
            while j < len(css_text) and depth > 0:
                if css_text[j] == '{':
                    depth += 1
                elif css_text[j] == '}':
                    depth -= 1
                j += 1
            blocks.append(css_text[idx:j])
            pos = j
        return '\n\n'.join(blocks)

    def _scope_root_to_editor(self, css_text):
        """Replace :root and [data-theme] selectors with editor-scoped equivalents.

        Handles three selector patterns from the token CSS generator:
        1. :root                    -> EDITOR_SCOPE
        2. [data-theme="dark"] {    -> [data-theme="dark"] EDITOR_SCOPE {
        3. [data-theme="light"] {   -> [data-theme="light"] EDITOR_SCOPE {
        """
        result = re.sub(r':root\b', EDITOR_SCOPE, css_text)
        result = re.sub(
            r'\[data-theme="dark"\]\s*\{',
            f'[data-theme="dark"] {EDITOR_SCOPE} {{',
            result,
        )
        result = re.sub(
            r'\[data-theme="light"\]\s*\{',
            f'[data-theme="light"] {EDITOR_SCOPE} {{',
            result,
        )
        return result
