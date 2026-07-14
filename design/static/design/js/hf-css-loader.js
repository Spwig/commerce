/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * HF Builder CSS Loader
 * Loads and scopes CSS files for the Header/Footer builder preview.
 * Reads CSS file URLs from window.HFBuilderConfig.cssFiles (set from JSON data island).
 */
(function () {
  'use strict';

  // Parse config from JSON data island early (this script is loaded after the
  // data island in the HTML, so getElementById works immediately).
  // This ensures window.HFBuilderConfig is available before DOMContentLoaded fires.
  if (!window.HFBuilderConfig) {
    const configEl = document.getElementById('hf-builder-config');
    if (configEl) {
      try {
        window.HFBuilderConfig = JSON.parse(configEl.textContent);
      } catch (e) {}
    }
  }

  /**
   * Load CSS file, scope all selectors to .hf-content-preview, and wrap in @layer
   * This prevents theme CSS from affecting admin UI
   * @param {string} url - The CSS file URL to fetch
   * @param {string} id - Unique identifier for the style element
   * @param {string|null} layerName - Optional layer name to wrap CSS in
   */
  function loadAndScopeCSS(url, id, layerName) {
    if (!url) {
      return Promise.resolve();
    }

    return fetch(url)
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Failed to load CSS: ' + url);
        }
        return response.text();
      })
      .then(function (css) {
        // STEP 1: Extract and protect @keyframes blocks
        const keyframesBlocks = [];
        const keyframesPlaceholder = '___KEYFRAMES_PLACEHOLDER_';
        let keyframesIndex = 0;

        let processedCSS = css.replace(
          /@keyframes\s+[\w-]+\s*\{(?:[^{}]*\{[^}]*\})*[^}]*\}/g,
          function (match) {
            keyframesBlocks.push(match);
            return keyframesPlaceholder + keyframesIndex++ + '___';
          }
        );

        // STEP 2: Rewrite relative url() paths to absolute
        const baseUrl = new URL(url, window.location.origin);
        const basePath = baseUrl.pathname.substring(0, baseUrl.pathname.lastIndexOf('/') + 1);

        processedCSS = processedCSS.replace(
          /url\(['"]?(?!data:)(?!http)([^'")\s]+)['"]?\)/g,
          function (match, relPath) {
            if (relPath.startsWith('data:') || relPath.startsWith('http')) {
              return match;
            }
            const absolutePath = new URL(relPath, baseUrl.origin + basePath).pathname;
            return "url('" + absolutePath + "')";
          }
        );

        // STEP 3: Scope remaining CSS selectors
        let scopedCSS = processedCSS.replace(/([^{}]+){/g, function (match, selector) {
          if (selector.trim().startsWith('@')) {
            return match;
          }
          const selectors = selector.split(',').map(function (s) {
            const trimmed = s.trim();
            if (!trimmed) {
              return trimmed;
            }
            if (trimmed.startsWith('.hf-content-preview')) {
              return trimmed;
            }
            if (trimmed.includes(':root')) {
              return trimmed.replace(':root', '.hf-content-preview');
            }
            if (trimmed === 'html' || trimmed === 'body') {
              return '.hf-content-preview';
            }
            if (trimmed.startsWith('html ') || trimmed.startsWith('body ')) {
              return '.hf-content-preview ' + trimmed.substring(5);
            }
            if (/^\[data-theme/.test(trimmed)) {
              return '.hf-content-preview' + trimmed;
            }
            return '.hf-content-preview ' + trimmed;
          });
          return selectors.join(', ') + ' {';
        });

        // STEP 4: Convert @media responsive queries to device-class selectors.
        // The builder simulates device widths via CSS classes on .canvas-frame
        // (mobile-preview, tablet-preview, desktop-preview) rather than changing
        // the viewport. Real @media queries won't fire, so we convert them to
        // class-based selectors that respond to the device toggle.
        scopedCSS = scopedCSS.replace(
          /@media\s*([^{]+?)\s*\{((?:[^{}]*\{[^}]*\})*[^}]*)\}/g,
          function (fullMatch, condition, innerCSS) {
            const maxMatch = condition.match(/max-width\s*:\s*([\d.]+)/);
            const minMatch = condition.match(/min-width\s*:\s*([\d.]+)/);
            if (!maxMatch && !minMatch) {
              return fullMatch;
            } // not width-based, keep as-is

            const maxW = maxMatch ? parseFloat(maxMatch[1]) : Infinity;
            const minW = minMatch ? parseFloat(minMatch[1]) : 0;

            // Determine which device preview modes this query covers.
            // Simulated widths: mobile ~375px, tablet ~900px, desktop ~1200px
            const devices = [];
            if (375 >= minW && 375 <= maxW) {
              devices.push('mobile-preview');
            }
            if (900 >= minW && 900 <= maxW) {
              devices.push('tablet-preview');
            }
            if (1200 >= minW && 1200 <= maxW) {
              devices.push('desktop-preview');
            }

            if (devices.length === 0) {
              return '';
            }
            if (devices.length === 3) {
              return innerCSS;
            } // unconditional

            let result = '';
            for (let d = 0; d < devices.length; d++) {
              result += innerCSS.replace(
                /\.hf-content-preview/g,
                '.canvas-frame.' + devices[d] + ' .hf-content-preview'
              );
            }
            return result;
          }
        );

        // STEP 5: Restore @keyframes blocks
        scopedCSS = scopedCSS.replace(
          new RegExp(keyframesPlaceholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(\d+)___', 'g'),
          function (match, index) {
            return keyframesBlocks[parseInt(index)];
          }
        );

        // STEP 6: Wrap in @layer if layer name provided
        if (layerName) {
          scopedCSS = '@layer ' + layerName + ' {\n' + scopedCSS + '\n}';
        }

        // STEP 7: Inject scoped CSS into a <style> tag
        let styleElement = document.getElementById('scoped-' + id);
        if (!styleElement) {
          styleElement = document.createElement('style');
          styleElement.id = 'scoped-' + id;
          document.head.appendChild(styleElement);
        }
        styleElement.textContent = scopedCSS;

        console.log(
          '✓ Loaded and scoped CSS: ' + id + (layerName ? ' (layer: ' + layerName + ')' : '')
        );
      })
      .catch(function (error) {
        console.error('Error loading CSS (' + id + '):', error);
      });
  }

  /**
   * Load theme system CSS (base, theme, brand, presetZones, widgets) with scoping and layer wrapping.
   * Reads CSS file URLs from window.HFBuilderConfig.cssFiles.
   * Loads independent CSS files in parallel for faster initial load.
   */
  function loadThemeSystemCSS() {
    const config = window.HFBuilderConfig || {};
    const cssFiles = config.cssFiles || {};

    // Theme → Brand must be sequential (brand overrides theme, same CSS layer)
    const themeBrandChain = (
      config.themeCssUrl
        ? loadAndScopeCSS(config.themeCssUrl, 'theme-css', 'hf-theme')
        : Promise.resolve()
    ).then(function () {
      return config.brandCssUrl
        ? loadAndScopeCSS(config.brandCssUrl, 'brand-css', 'hf-theme')
        : Promise.resolve();
    });

    // Widget CSS files (independent of each other)
    const widgetFiles = cssFiles.widgets || [];
    const widgetLoads = widgetFiles.map(function (url) {
      const id = 'widget-' + url.split('/').pop().replace('.css', '');
      return loadAndScopeCSS(url, id, 'hf-theme');
    });

    // Load everything in parallel (base is in hf-base layer, rest are independent within hf-theme)
    const allLoads = [
      loadAndScopeCSS(cssFiles.base || null, 'base-css', 'hf-base'),
      themeBrandChain,
      loadAndScopeCSS(cssFiles.presetZones || null, 'preset-zones-css', 'hf-theme'),
    ].concat(widgetLoads);

    return Promise.all(allLoads)
      .then(function () {
        console.log('\u2713 All theme system CSS loaded');
      })
      .catch(function (error) {
        console.error('Error loading theme system CSS:', error);
      });
  }

  // Expose for use by header-footer-builder.js if needed
  window.HFCssLoader = {
    loadAndScopeCSS: loadAndScopeCSS,
    loadThemeSystemCSS: loadThemeSystemCSS,
  };

  // Load theme CSS when page loads.
  // Store the promise globally so the builder can await it before rendering.
  document.addEventListener('DOMContentLoaded', function () {
    window.HFCssLoaderReady = loadThemeSystemCSS();
  });
})();
