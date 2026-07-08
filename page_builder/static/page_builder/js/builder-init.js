/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
/* Page Builder Init — reads config from #page-builder-config JSON data island */
(function () {
    'use strict';

    // ---------- Admin theme ----------
    function initializeAdminTheme(theme) {
        console.log('Page Builder Admin Theme:', theme);
        document.documentElement.setAttribute('data-theme', theme);
        document.body.setAttribute('data-theme', theme);
    }

    // Listen for theme changes from admin storage (runtime switching)
    window.addEventListener('storage', function (e) {
        if (e.key === 'admin_theme' && e.newValue) {
            var newTheme = e.newValue || 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            document.body.setAttribute('data-theme', newTheme);
            console.log('Admin theme changed to:', newTheme);
        }
    });

    // Listen for custom theme-changed events
    window.addEventListener('theme-changed', function (e) {
        if (e.detail && e.detail.theme) {
            document.body.setAttribute('data-theme', e.detail.theme);
            document.documentElement.setAttribute('data-theme', e.detail.theme);
        }
    });

    // ---------- URL resolution ----------
    function resolveUrl(relativeUrl, baseUrl) {
        try {
            if (baseUrl.startsWith('/') && !baseUrl.startsWith('//')) {
                baseUrl = window.location.origin + baseUrl;
            }
            return new URL(relativeUrl, baseUrl).href;
        } catch (e) {
            console.warn('URL resolution failed:', e, 'relative:', relativeUrl, 'base:', baseUrl);
            return relativeUrl;
        }
    }

    // ---------- Shared CSS scoping helper ----------
    // Scopes CSS selectors under .pb-content-preview using an indexOf-based parser.
    // This avoids the O(n) regex backtracking of the previous ([^{}]+)\{ approach
    // which took ~2.3s on 162KB theme CSS files. The indexOf parser runs in <1ms.
    var SCOPE_PREFIX = '.pb-content-preview';

    function applyScopeToCSS(rawCSS) {
        // Strip comments (not needed in injected <style> elements)
        var css = rawCSS.replace(/\/\*[\s\S]*?\*\//g, '');
        return _scopeBlock(css);
    }

    function _scopeBlock(css) {
        var chunks = [];
        var pos = 0;
        var len = css.length;

        while (pos < len) {
            var openIdx = css.indexOf('{', pos);
            if (openIdx === -1) {
                chunks.push(css.substring(pos));
                break;
            }

            // Everything from pos to openIdx is the selector
            var selector = css.substring(pos, openIdx);

            // Find matching } via depth counting
            var depth = 1;
            var scanPos = openIdx + 1;
            while (scanPos < len && depth > 0) {
                var c = css.charCodeAt(scanPos);
                if (c === 123) depth++;      // {
                else if (c === 125) depth--; // }
                scanPos++;
            }

            var body = css.substring(openIdx + 1, scanPos - 1);
            var trimSel = selector.trim();

            if (!trimSel) {
                // Whitespace-only selector (shouldn't happen, but be safe)
                chunks.push(selector, '{', body, '}');
            } else if (trimSel.charCodeAt(0) === 64) { // '@'
                // @-rule: check if it contains inner rules that need scoping
                if (trimSel.length > 6 && (
                    trimSel.startsWith('@media') ||
                    trimSel.startsWith('@supports') ||
                    trimSel.startsWith('@layer') ||
                    trimSel.startsWith('@container') ||
                    trimSel.startsWith('@scope') ||
                    trimSel.startsWith('@document')
                )) {
                    chunks.push(selector, '{', _scopeBlock(body), '}');
                } else {
                    // @font-face, @keyframes, @charset, @import, etc. — pass through
                    chunks.push(selector, '{', body, '}');
                }
            } else {
                // Regular CSS rule — scope the selector
                chunks.push(_scopeSelectors(trimSel), '{', body, '}');
            }

            pos = scanPos;
        }

        return chunks.join('');
    }

    function _scopeSelectors(selectorText) {
        // Fast path: single selector (no comma) — most common case
        if (selectorText.indexOf(',') === -1) {
            return _scopeOne(selectorText);
        }
        var parts = selectorText.split(',');
        for (var i = 0; i < parts.length; i++) {
            parts[i] = _scopeOne(parts[i].trim());
        }
        return parts.join(', ');
    }

    function _scopeOne(sel) {
        if (!sel || sel.startsWith(SCOPE_PREFIX)) return sel;
        if (sel === 'html' || sel === 'body') return SCOPE_PREFIX;
        if (sel.indexOf(':root') !== -1) return sel.replace(':root', SCOPE_PREFIX);
        if (sel.startsWith('html ')) return SCOPE_PREFIX + sel.substring(4);
        if (sel.startsWith('body ')) return SCOPE_PREFIX + sel.substring(4);
        if (sel.charCodeAt(0) === 91 && sel.startsWith('[data-theme')) return SCOPE_PREFIX + sel;
        return SCOPE_PREFIX + ' ' + sel;
    }

    // ---------- fetchAndScopeCSS ----------
    async function fetchAndScopeCSS(url, layerName) {
        // Check sessionStorage cache (keyed by full URL including version hash)
        var cacheKey = 'scopedCSS:' + layerName + ':' + url;
        try {
            var cached = sessionStorage.getItem(cacheKey);
            if (cached) {
                return cached;
            }
        } catch (e) { /* sessionStorage unavailable */ }

        var response = await fetch(url);
        var css = await response.text();

        // Inline @import statements in parallel
        var importRegex = /@import\s+url\(['"]?([^'")\s]+)['"]?\)\s*;?/gi;
        var imports = [];
        var m;
        while ((m = importRegex.exec(css)) !== null) {
            // Skip external @imports (http/https URLs) — preserve them as-is
            if (/^https?:\/\//.test(m[1])) continue;
            imports.push({ fullMatch: m[0], importUrl: m[1] });
        }

        if (imports.length > 0) {
            var importResults = await Promise.all(imports.map(async function (imp) {
                var abs = resolveUrl(imp.importUrl, url);
                try {
                    var r = await fetch(abs);
                    return { imp: imp, content: r.ok ? await r.text() : '/* Failed to load: ' + imp.importUrl + ' */' };
                } catch (e) {
                    return { imp: imp, content: '/* Error loading: ' + imp.importUrl + ' */' };
                }
            }));
            importResults.forEach(function (r) { css = css.replace(r.imp.fullMatch, r.content); });
        }

        var scopedCSS = applyScopeToCSS(css);

        if (layerName) {
            scopedCSS = '@layer ' + layerName + ' {\n' + scopedCSS + '\n}';
        }

        // Cache in sessionStorage for subsequent loads
        try { sessionStorage.setItem(cacheKey, scopedCSS); } catch (e) { /* quota exceeded or unavailable */ }

        return scopedCSS;
    }

    // ---------- loadAndScopeCSS (legacy, kept for backward compatibility) ----------
    // Note: Kept for compatibility. New code should use fetchAndScopeCSS + loadThemeSystemCSS.
    async function loadAndScopeCSS(url, id) {
        try {
            var response = await fetch(url);
            var css = await response.text();

            var importRegex = /@import\s+url\(['"]?([^'")\s]+)['"]?\)\s*;?/gi;
            var imports = [];
            var m;
            while ((m = importRegex.exec(css)) !== null) {
                imports.push({ fullMatch: m[0], importUrl: m[1] });
            }
            for (var i = 0; i < imports.length; i++) {
                var imp = imports[i];
                var abs = resolveUrl(imp.importUrl, url);
                try {
                    var r = await fetch(abs);
                    if (r.ok) {
                        css = css.replace(imp.fullMatch, await r.text());
                    } else {
                        console.warn('Failed to fetch @import (' + r.status + '): ' + abs);
                        css = css.replace(imp.fullMatch, '/* Failed to load: ' + imp.importUrl + ' */');
                    }
                } catch (e) {
                    console.warn('Could not load @import from ' + abs + ':', e);
                    css = css.replace(imp.fullMatch, '/* Error loading: ' + imp.importUrl + ' */');
                }
            }

            var scopedCSS = applyScopeToCSS(css);
            var el = document.getElementById('scoped-' + id);
            if (!el) {
                el = document.createElement('style');
                el.id = 'scoped-' + id;
                document.head.appendChild(el);
            }
            el.textContent = scopedCSS;
        } catch (err) {
            console.warn('Could not load CSS from ' + url + ':', err);
        }
    }

    // ---------- loadThemeSystemCSS ----------
    // Loads theme CSS with proper @layer declarations. Uses parallel fetching for performance.
    async function loadThemeSystemCSS(cssConfig) {
        var cssToLoad = [
            { url: cssConfig.baseCss, id: 'base-css', layer: 'canvas-base' },
            { url: cssConfig.themeCss, id: cssConfig.themeId || 'theme-css', layer: 'canvas-theme' }
        ];
        if (cssConfig.brandCss) {
            cssToLoad.push({ url: cssConfig.brandCss, id: 'brand-css', layer: 'canvas-brand' });
        }
        cssToLoad.push({ url: cssConfig.formBuilderCss, id: 'form-builder-css', layer: 'canvas-theme' });

        // Pre-create style elements in correct cascade order (DOM order matters for CSS)
        var styleElements = {};
        cssToLoad.forEach(function (item) {
            var el = document.getElementById('scoped-' + item.id);
            if (!el) {
                el = document.createElement('style');
                el.id = 'scoped-' + item.id;
                document.head.appendChild(el);
            }
            styleElements[item.id] = el;
        });

        // Fetch all CSS in parallel, then apply in order
        var results = await Promise.all(cssToLoad.map(async function (item) {
            try {
                var css = await fetchAndScopeCSS(item.url, item.layer);
                return { id: item.id, css: css, ok: true };
            } catch (e) {
                console.warn('Could not load CSS from ' + item.url + ':', e);
                return { id: item.id, css: '', ok: false };
            }
        }));

        results.forEach(function (r) {
            if (styleElements[r.id]) { styleElements[r.id].textContent = r.css; }
        });
    }

    // Deprecated: kept for compatibility, delegates to loadThemeSystemCSS
    function loadTemplateCSSScoped(cssConfig) {
        loadThemeSystemCSS(cssConfig);
    }

    // ---------- Main DOMContentLoaded ----------
    document.addEventListener('DOMContentLoaded', function () {
        var configEl = document.getElementById('page-builder-config');
        var config = {};
        if (configEl) {
            try {
                config = JSON.parse(configEl.textContent);
            } catch (e) {
                console.error('Failed to parse #page-builder-config:', e);
            }
        }

        // Expose translations for color picker utility
        window.ColorPickerTranslations = config.colorPickerTranslations || {};

        // Expose available languages for translation editor utility
        window.PAGE_BUILDER_LANGUAGES = config.languages || [];

        // Expose element metadata (icons, defaults, names) for data-driven element handling
        window.elementMetadata = config.elementMetadata || {};

        // Expose all elements data for LivePreviewManager style initialization (eliminates per-element API calls)
        window.allElementsData = config.allElementsData || {};

        // Expose admin page builder URL prefix for AJAX and preview paths
        window.adminPageBuilderPrefix = config.adminPrefix || '';

        // Set up CSRF token for AJAX requests (prefer config, then meta tag)
        var csrf = config.csrfToken
            || (document.querySelector('meta[name="csrf-token"]') || {}).content
            || '';
        if (csrf) { window.csrfToken = csrf; }

        // Initialize admin theme
        initializeAdminTheme(config.adminTheme || 'light');

        // Apply force light mode to canvas preview (honors merchant's theme setting)
        if (config.forceLightMode) {
            var preview = document.querySelector('.pb-content-preview');
            if (preview) { preview.setAttribute('data-theme', 'light'); }
        }

        // Load theme system CSS
        loadThemeSystemCSS(config.cssConfig || {});

        // Initialize the visual builder with page data
        initVisualBuilder(config.pageData || {});

        // Canvas background click opens page settings panel
        var canvasFrame = document.getElementById('page-canvas');
        if (canvasFrame) {
            canvasFrame.addEventListener('click', function (e) {
                var target = e.target;
                if (target.id === 'page-canvas' || target.id === 'page-elements') {
                    if (!target.closest('.element-wrapper, .page-drop-zone, .empty-drop-zone, .empty-message')) {
                        openPageSettings();
                    }
                }
            });
        }
    });

})();
