/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Element Builder Live Preview Manager
 *
 * Provides real-time CSS preview updates for element properties.
 * Simplified version of page_builder's LivePreviewManager.
 */

class ElementBuilderLivePreview {
    constructor() {
        // Map of element IDs to their dynamically injected style elements
        this.styleElements = new Map();

        // CSS property mapping from content properties to CSS properties
        this.cssPropertyMap = {
            // Colors
            'color': 'color',
            'text_color': 'color',
            'background_color': 'background-color',
            'backgroundColor': 'background-color',

            // Typography
            'font_size': 'font-size',
            'fontSize': 'font-size',
            'font_weight': 'font-weight',
            'fontWeight': 'font-weight',
            'font_family': 'font-family',
            'fontFamily': 'font-family',
            'line_height': 'line-height',
            'lineHeight': 'line-height',
            'letter_spacing': 'letter-spacing',
            'letterSpacing': 'letter-spacing',
            'text_align': 'text-align',
            'textAlign': 'text-align',
            'text_transform': 'text-transform',
            'textTransform': 'text-transform',
            'text_decoration': 'text-decoration',
            'textDecoration': 'text-decoration',

            // Spacing
            'padding': 'padding',
            'padding_top': 'padding-top',
            'padding_right': 'padding-right',
            'padding_bottom': 'padding-bottom',
            'padding_left': 'padding-left',
            'margin': 'margin',
            'margin_top': 'margin-top',
            'margin_right': 'margin-right',
            'margin_bottom': 'margin-bottom',
            'margin_left': 'margin-left',

            // Layout
            'width': 'width',
            'height': 'height',
            'max_width': 'max-width',
            'maxWidth': 'max-width',
            'min_width': 'min-width',
            'minWidth': 'min-width',
            'display': 'display',
            'flex_direction': 'flex-direction',
            'flexDirection': 'flex-direction',
            'justify_content': 'justify-content',
            'justifyContent': 'justify-content',
            'align_items': 'align-items',
            'alignItems': 'align-items',
            'gap': 'gap',

            // Appearance
            'border': 'border',
            'border_radius': 'border-radius',
            'borderRadius': 'border-radius',
            'box_shadow': 'box-shadow',
            'boxShadow': 'box-shadow',
            'opacity': 'opacity',
            'background': 'background',

            // Grid
            'grid_template_columns': 'grid-template-columns',
            'gridTemplateColumns': 'grid-template-columns',
        };
    }

    /**
     * Apply CSS styles to an element in the preview
     * @param {number|string} elementId - Element ID
     * @param {Object} properties - Properties to apply as CSS
     */
    applyStyles(elementId, properties) {
        // Find element in preview
        const element = document.querySelector(
            `.eb-preview-element[data-element-id="${elementId}"]`
        );

        if (!element) {
            // Element not in preview, skip
            return;
        }

        // Build CSS rules from properties
        const cssRules = [];

        for (const [key, value] of Object.entries(properties)) {
            if (value === undefined || value === null || value === '') continue;

            const cssProperty = this.cssPropertyMap[key];
            if (cssProperty) {
                cssRules.push(`${cssProperty}: ${value}`);
            }
        }

        if (cssRules.length === 0) return;

        // Apply inline styles for immediate feedback
        // This is faster than injecting style elements for real-time preview
        for (const [key, value] of Object.entries(properties)) {
            const cssProperty = this.cssPropertyMap[key];
            if (cssProperty && value !== undefined && value !== null && value !== '') {
                // Convert CSS property to camelCase for style object
                const jsProperty = cssProperty.replace(/-([a-z])/g, (g) => g[1].toUpperCase());
                element.style[jsProperty] = value;
            }
        }
    }

    /**
     * Remove all applied styles from an element
     * @param {number|string} elementId - Element ID
     */
    clearStyles(elementId) {
        const element = document.querySelector(
            `.eb-preview-element[data-element-id="${elementId}"]`
        );

        if (element) {
            element.removeAttribute('style');
        }

        // Also remove any injected style elements
        const styleEl = this.styleElements.get(elementId);
        if (styleEl && styleEl.parentNode) {
            styleEl.parentNode.removeChild(styleEl);
            this.styleElements.delete(elementId);
        }
    }

    /**
     * Refresh the entire preview (called after saving)
     */
    refresh() {
        // Clear all cached style elements
        this.styleElements.forEach((styleEl) => {
            if (styleEl.parentNode) {
                styleEl.parentNode.removeChild(styleEl);
            }
        });
        this.styleElements.clear();
    }

    /**
     * Update text content in the preview
     * @param {number|string} elementId - Element ID
     * @param {string} text - New text content
     */
    updateText(elementId, text) {
        const element = document.querySelector(
            `.eb-preview-element[data-element-id="${elementId}"]`
        );

        if (element) {
            // Find the text content area within the element
            const textContent = element.querySelector('.element-content, .text-element, p, span, h1, h2, h3, h4, h5, h6');
            if (textContent) {
                textContent.textContent = text;
            }
        }
    }

    /**
     * Update image source in the preview
     * @param {number|string} elementId - Element ID
     * @param {string} src - New image source URL
     */
    updateImage(elementId, src) {
        const element = document.querySelector(
            `.eb-preview-element[data-element-id="${elementId}"]`
        );

        if (element) {
            const img = element.querySelector('img');
            if (img) {
                img.src = src;
            }
        }
    }
}

// Create global instance for PropertyRenderer to use
window.livePreview = new ElementBuilderLivePreview();
