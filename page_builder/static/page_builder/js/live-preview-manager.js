/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Live Preview Manager
 * Version 2.0.3
 * Centralized system for handling real-time preview updates in the page builder
 *
 * This manager provides:
 * - Instant visual updates without server round-trips
 * - Intelligent element selection based on element type
 * - Debounced server synchronization
 * - Unified API for all utilities
 */
class LivePreviewManager {
    constructor() {
        console.log('[LivePreviewManager] Initializing...');
        this.pendingUpdates = new Map();
        this.updateTimeout = null;
        this.updateDelay = 500; // Delay for server sync

        // Element selector mappings
        this.elementSelectors = {
            'text': '.pb-text, .text-element',
            'heading': 'h1, h2, h3, h4, h5, h6',
            'button': 'button, .btn, .button-element',
            'image': 'img, .image-element',
            'video': 'video, .video-element',
            'container': '.pb-container',
            'spacer': '.pb-spacer',
            'divider': '.pb-divider',
            'icon': '.icon-element',
            'social': '.social-element',
            'form': '.fb-form-section, section.fb-form-section',
            'hero': '.hero, section.hero',
            'cta_banner': '.cta-banner, section.cta-banner',
            'testimonials': '.testimonials, section.testimonials',
            'gallery': '.gallery, section.gallery',
            'newsletter': '.newsletter, section.newsletter',
            'product_carousel': '.product-carousel, section.product-carousel',
            'product_grid': '.product-grid, section.product-grid',
            'search': '.search, section.search',
            'image_accordion': '.image-accordion, section.image-accordion',
            'default': ':first-child'
        };

        // CSS property mappings
        this.propertyMap = {
            // Colors
            'background': 'background',
            'background_color': 'backgroundColor',
            'backgroundColor': 'backgroundColor',
            'background-color': 'backgroundColor',
            'text_color': 'color',
            'textColor': 'color',
            'color': 'color',
            'border_color': 'borderColor',
            'borderColor': 'borderColor',
            'border-color': 'borderColor',

            // Typography
            'font_size': 'fontSize',
            'fontSize': 'fontSize',
            'font-size': 'fontSize',
            'font_weight': 'fontWeight',
            'fontWeight': 'fontWeight',
            'font-weight': 'fontWeight',
            'font_family': 'fontFamily',
            'fontFamily': 'fontFamily',
            'font-family': 'fontFamily',
            'line_height': 'lineHeight',
            'lineHeight': 'lineHeight',
            'line-height': 'lineHeight',
            'letter_spacing': 'letterSpacing',
            'letterSpacing': 'letterSpacing',
            'letter-spacing': 'letterSpacing',
            'text_align': 'textAlign',
            'textAlign': 'textAlign',
            'text-align': 'textAlign',

            // Spacing
            'padding': 'padding',
            'padding_top': 'paddingTop',
            'paddingTop': 'paddingTop',
            'padding-top': 'paddingTop',
            'padding_right': 'paddingRight',
            'paddingRight': 'paddingRight',
            'padding-right': 'paddingRight',
            'padding_bottom': 'paddingBottom',
            'paddingBottom': 'paddingBottom',
            'padding-bottom': 'paddingBottom',
            'padding_left': 'paddingLeft',
            'paddingLeft': 'paddingLeft',
            'padding-left': 'paddingLeft',
            'margin': 'margin',
            'margin_top': 'marginTop',
            'marginTop': 'marginTop',
            'margin-top': 'marginTop',
            'margin_right': 'marginRight',
            'marginRight': 'marginRight',
            'margin-right': 'marginRight',
            'margin_bottom': 'marginBottom',
            'marginBottom': 'marginBottom',
            'margin-bottom': 'marginBottom',
            'margin_left': 'marginLeft',
            'marginLeft': 'marginLeft',
            'margin-left': 'marginLeft',

            // Borders
            'border': 'border',
            'border_width': 'borderWidth',
            'borderWidth': 'borderWidth',
            'border-width': 'borderWidth',
            'border_style': 'borderStyle',
            'borderStyle': 'borderStyle',
            'border-style': 'borderStyle',
            'border_radius': 'borderRadius',
            'borderRadius': 'borderRadius',
            'border-radius': 'borderRadius',

            // Layout
            'width': 'width',
            'height': 'height',
            'min_width': 'minWidth',
            'minWidth': 'minWidth',
            'min-width': 'minWidth',
            'max_width': 'maxWidth',
            'maxWidth': 'maxWidth',
            'max-width': 'maxWidth',
            'min_height': 'minHeight',
            'minHeight': 'minHeight',
            'min-height': 'minHeight',
            'max_height': 'maxHeight',
            'maxHeight': 'maxHeight',
            'max-height': 'maxHeight',

            // Effects
            'opacity': 'opacity',
            'box_shadow': 'boxShadow',
            'boxShadow': 'boxShadow',
            'box-shadow': 'boxShadow',
            'text_shadow': 'textShadow',
            'textShadow': 'textShadow',
            'text-shadow': 'textShadow',
            'transform': 'transform',
            'transition': 'transition',
            'filter': 'filter'
        };

        // Bind methods
        this.updateElement = this.updateElement.bind(this);
        this.applyStyles = this.applyStyles.bind(this);
        this.syncToServer = this.syncToServer.bind(this);

        // Make globally available
        window.livePreview = this;
        console.log('[LivePreviewManager] Set window.livePreview');

        // Initialize saved styles on page load
        this.initializeSavedStyles();

        // Note: Hover backgrounds are now rendered by templates via <style> blocks
        // No need to initialize from data attributes

        console.log('[LivePreviewManager] Initialization complete');
    }

    /**
     * Initialize saved styles from element data on page load.
     * Uses pre-loaded data from the config JSON data island (zero network requests).
     * Falls back to sequential API calls if pre-loaded data is unavailable.
     */
    initializeSavedStyles() {
        // Small delay to ensure DOM and builder-init.js have run
        setTimeout(() => {
            // Try to get pre-loaded element data (set by builder-init.js from config)
            let allElementsData = window.allElementsData;

            // Fallback: read directly from config data island
            if (!allElementsData || Object.keys(allElementsData).length === 0) {
                try {
                    const configEl = document.getElementById('page-builder-config');
                    if (configEl) {
                        const config = JSON.parse(configEl.textContent);
                        allElementsData = config.allElementsData || {};
                    }
                } catch (e) {
                    allElementsData = {};
                }
            }

            const elements = document.querySelectorAll('.element-wrapper[data-element-id]');
            const hasPreloadedData = allElementsData && Object.keys(allElementsData).length > 0;

            if (hasPreloadedData) {
                // Fast path: use pre-loaded data (zero network requests)
                for (const element of elements) {
                    const elementId = element.dataset.elementId;
                    if (!elementId) continue;

                    const data = allElementsData[elementId];
                    if (data && data.content) {
                        this._applyElementStyles(element, elementId, data.content, data.element_type);
                    }
                }
            } else {
                // Slow fallback: sequential API calls (original behavior)
                console.warn('[LivePreviewManager] allElementsData not available, falling back to API calls');
                this._initializeSavedStylesViaApi(elements);
            }
        }, 100);
    }

    /**
     * Apply saved styles to a single element from its content data.
     * Shared by both the fast path (pre-loaded data) and fallback (API calls).
     */
    _applyElementStyles(element, elementId, content, elementType) {
        const hasTypography = content.typography &&
                             content.typography !== 'inherit' &&
                             content.typography.trim() !== '';

        if (hasTypography) {
            const typographyStyles = this.parseTypographyString(content.typography);
            if (typographyStyles && Object.keys(typographyStyles).length > 0) {
                this.applyStyles(elementId, typographyStyles);
            }
        }

        const resolvedType = element.dataset.elementType || elementType || 'default';
        this.applyElementSpecificStyles(element, resolvedType, content);

        const styleProperties = {};
        const propertyMappings = {
            'text_color': 'color',
            'background_color': 'backgroundColor',
            'background': 'background',
            'border': 'border',
            'shadow': 'boxShadow',
            'box_shadow': 'boxShadow'
        };
        const typographyManagedProps = ['fontSize', 'fontWeight', 'textAlign', 'lineHeight', 'letterSpacing'];

        for (const [contentKey, cssProperty] of Object.entries(propertyMappings)) {
            if (hasTypography && typographyManagedProps.includes(cssProperty)) {
                continue;
            }
            if (content[contentKey]) {
                styleProperties[cssProperty] = content[contentKey];
            }
        }

        if (Object.keys(styleProperties).length > 0) {
            this.applyStyles(elementId, styleProperties);
        }

        if (content.hover_background) {
            this.applyHoverBackground(element, content.hover_background);
        }
    }

    /**
     * Fallback: sequential API calls for style initialization (original behavior).
     */
    async _initializeSavedStylesViaApi(elements) {
        for (const element of elements) {
            const elementId = element.dataset.elementId;
            if (!elementId) continue;

            try {
                let apiBaseUrl;
                if (window.builderInstance?.getApiBaseUrl) {
                    apiBaseUrl = window.builderInstance.getApiBaseUrl();
                } else {
                    apiBaseUrl = '/api/page-builder';
                }
                const response = await fetch(`${apiBaseUrl}/elements/${elementId}/`, {
                    headers: { 'Accept': 'application/json' }
                });

                if (response.status === 404 || !response.ok) continue;

                const data = await response.json();
                if (data && data.content) {
                    this._applyElementStyles(element, elementId, data.content, data.element_type);
                }
            } catch (error) {
                console.warn(`Failed to load styles for element ${elementId}:`, error);
            }
        }
    }

    /**
     * Apply element-specific styles for complex elements with multiple text components
     * @param {HTMLElement} elementWrapper - The element wrapper
     * @param {string} elementType - The type of element
     * @param {Object} content - The element content data
     */
    applyElementSpecificStyles(elementWrapper, elementType, content) {
        // Define mappings for elements with multiple text components
        const elementStyleMappings = {
            'hero': {
                'title': { selector: '.hero__title', typography: 'title_typography', color: 'title_color', shadow: 'title_shadow' },
                'subtitle': { selector: '.hero__subtitle', typography: 'subtitle_typography', color: 'subtitle_color', shadow: 'subtitle_shadow' },
                'description': { selector: '.hero__description', typography: 'description_typography', color: 'description_color', shadow: 'description_shadow' }
            },
            'cta_banner': {
                'title': { selector: '.cta-banner__title', typography: 'title_typography', color: 'title_color', shadow: 'title_shadow' },
                'subtitle': { selector: '.cta-banner__subtitle', typography: 'subtitle_typography', color: 'subtitle_color', shadow: 'subtitle_shadow' }
            },
            'testimonials': {
                'title': { selector: '.testimonials__title', typography: 'title_typography', color: 'title_color', shadow: 'title_shadow' }
            }
        };

        // Get mappings for this element type
        const mappings = elementStyleMappings[elementType];
        if (!mappings) return;

        const elementContent = elementWrapper.querySelector('.element-content');
        if (!elementContent) return;

        // Apply styles to each mapped component
        for (const [componentKey, mapping] of Object.entries(mappings)) {
            const targetElement = elementContent.querySelector(mapping.selector);
            if (!targetElement) continue;

            // Apply typography styles (CSS string from typography editor)
            if (mapping.typography && content[mapping.typography]) {
                const typographyValue = content[mapping.typography];
                if (typographyValue && typographyValue !== 'inherit') {
                    const styles = this.parseTypographyString(typographyValue);
                    for (const [prop, value] of Object.entries(styles)) {
                        targetElement.style[prop] = value;
                    }
                }
            }

            // Apply color
            if (mapping.color && content[mapping.color]) {
                targetElement.style.color = content[mapping.color];
            }

            // Apply text shadow
            if (mapping.shadow && content[mapping.shadow]) {
                targetElement.style.textShadow = content[mapping.shadow];
            }
        }
    }

    /**
     * Apply element-specific styles from a properties object (used during editing)
     * This handles properties like title_typography, title_color passed individually
     * @param {HTMLElement} elementWrapper - The element wrapper
     * @param {string} elementType - The type of element
     * @param {Object} properties - Properties being updated
     */
    applyElementSpecificStylesFromProperties(elementWrapper, elementType, properties) {
        // Define mappings for element-specific properties
        const propertyMappings = {
            'hero': {
                'title_typography': { selector: '.hero__title', type: 'typography' },
                'title_color': { selector: '.hero__title', type: 'color' },
                'title_shadow': { selector: '.hero__title', type: 'textShadow' },
                'subtitle_typography': { selector: '.hero__subtitle', type: 'typography' },
                'subtitle_color': { selector: '.hero__subtitle', type: 'color' },
                'subtitle_shadow': { selector: '.hero__subtitle', type: 'textShadow' },
                'description_typography': { selector: '.hero__description', type: 'typography' },
                'description_color': { selector: '.hero__description', type: 'color' },
                'description_shadow': { selector: '.hero__description', type: 'textShadow' },
                // Primary button mappings
                'button_background': { selector: '.hero__actions .btn:first-child', type: 'background' },
                'button_text_color': { selector: '.hero__actions .btn:first-child', type: 'color' },
                'button_border': { selector: '.hero__actions .btn:first-child', type: 'border' },
                'button_typography': { selector: '.hero__actions .btn:first-child', type: 'typography' },
                'button_padding': { selector: '.hero__actions .btn:first-child', type: 'padding' },
                'button_shadow': { selector: '.hero__actions .btn:first-child', type: 'boxShadow' },
                // Secondary button mappings
                'secondary_button_background': { selector: '.hero__actions .btn:nth-child(2)', type: 'background' },
                'secondary_button_text_color': { selector: '.hero__actions .btn:nth-child(2)', type: 'color' },
                'secondary_button_border': { selector: '.hero__actions .btn:nth-child(2)', type: 'border' },
                'secondary_button_typography': { selector: '.hero__actions .btn:nth-child(2)', type: 'typography' },
                'secondary_button_padding': { selector: '.hero__actions .btn:nth-child(2)', type: 'padding' },
                'secondary_button_shadow': { selector: '.hero__actions .btn:nth-child(2)', type: 'boxShadow' }
            },
            'cta_banner': {
                'title_typography': { selector: '.cta-banner__title', type: 'typography' },
                'title_color': { selector: '.cta-banner__title', type: 'color' },
                'title_shadow': { selector: '.cta-banner__title', type: 'textShadow' },
                'subtitle_typography': { selector: '.cta-banner__subtitle', type: 'typography' },
                'subtitle_color': { selector: '.cta-banner__subtitle', type: 'color' },
                'subtitle_shadow': { selector: '.cta-banner__subtitle', type: 'textShadow' }
            },
            'testimonials': {
                'title_typography': { selector: '.testimonials__title', type: 'typography' },
                'title_color': { selector: '.testimonials__title', type: 'color' },
                'title_shadow': { selector: '.testimonials__title', type: 'textShadow' }
            }
        };

        // Get mappings for this element type
        const mappings = propertyMappings[elementType];
        if (!mappings) return;

        const elementContent = elementWrapper.querySelector('.element-content');
        if (!elementContent) return;

        // Process each property
        for (const [propKey, propValue] of Object.entries(properties)) {
            const mapping = mappings[propKey];
            if (!mapping) continue;

            const targetElement = elementContent.querySelector(mapping.selector);
            if (!targetElement) continue;

            // Handle clearing (empty value) - reset styles to inherit/default
            const isEmpty = propValue === '' || propValue === null || propValue === undefined;

            if (mapping.type === 'typography') {
                if (isEmpty) {
                    // Clear all typography-related inline styles
                    const typographyProps = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle',
                        'lineHeight', 'letterSpacing', 'wordSpacing', 'textTransform',
                        'textDecoration', 'textDecorationStyle', 'textIndent', 'textAlign',
                        'verticalAlign', 'direction', 'fontVariant'];
                    typographyProps.forEach(prop => targetElement.style[prop] = '');
                } else {
                    // Parse and apply typography CSS string
                    const styles = this.parseTypographyString(propValue);
                    for (const [cssProp, cssValue] of Object.entries(styles)) {
                        targetElement.style[cssProp] = cssValue;
                    }
                }
            } else if (mapping.type === 'color') {
                targetElement.style.color = isEmpty ? '' : propValue;
            } else if (mapping.type === 'textShadow') {
                targetElement.style.textShadow = isEmpty ? '' : propValue;
            } else if (mapping.type === 'background') {
                if (isEmpty) {
                    targetElement.style.background = '';
                    targetElement.style.backgroundColor = '';
                } else if (propValue.includes('gradient') || propValue.includes('url(')) {
                    targetElement.style.background = propValue;
                } else {
                    targetElement.style.backgroundColor = propValue;
                }
            } else if (mapping.type === 'border') {
                if (isEmpty) {
                    // Clear all border-related inline styles
                    const borderProps = ['border', 'borderWidth', 'borderStyle', 'borderColor',
                        'borderRadius', 'borderTop', 'borderRight', 'borderBottom', 'borderLeft',
                        'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
                        'borderTopStyle', 'borderRightStyle', 'borderBottomStyle', 'borderLeftStyle',
                        'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor',
                        'borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomLeftRadius', 'borderBottomRightRadius'];
                    borderProps.forEach(prop => targetElement.style[prop] = '');
                } else {
                    // Border CSS string from border_editor
                    const styles = this.parseCSSString(propValue);
                    for (const [cssProp, cssValue] of Object.entries(styles)) {
                        targetElement.style[cssProp] = cssValue;
                    }
                }
            } else if (mapping.type === 'padding') {
                if (isEmpty) {
                    // Clear all padding-related inline styles
                    const paddingProps = ['padding', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'];
                    paddingProps.forEach(prop => targetElement.style[prop] = '');
                } else {
                    // Padding CSS string from spacing_editor
                    const styles = this.parseCSSString(propValue);
                    for (const [cssProp, cssValue] of Object.entries(styles)) {
                        targetElement.style[cssProp] = cssValue;
                    }
                }
            } else if (mapping.type === 'boxShadow') {
                targetElement.style.boxShadow = isEmpty ? '' : propValue;
            }
        }
    }

    /**
     * Apply text content updates to element preview
     * Maps text property names to their target DOM selectors
     * @param {HTMLElement} elementWrapper - The element wrapper
     * @param {string} elementType - Type of element (hero, text, heading, etc.)
     * @param {Object} properties - Properties being updated
     */
    applyTextContentFromProperties(elementWrapper, elementType, properties) {
        // Define text content mappings for each element type
        // Maps property name -> { selector, allowHtml, hideWhenEmpty }
        // hideWhenEmpty: true will hide the element when text is empty (for optional elements like secondary buttons)
        const textMappings = {
            'hero': {
                'title': { selector: '.hero__title', allowHtml: false },
                'subtitle': { selector: '.hero__subtitle', allowHtml: false },
                'description': { selector: '.hero__description', allowHtml: false },
                'button_text': { selector: '.hero__actions .btn:first-child', allowHtml: false },
                'secondary_button_text': { selector: '.hero__actions .btn:nth-child(2)', allowHtml: false, hideWhenEmpty: true }
            },
            'heading': {
                'text': { selector: '.pb-heading', allowHtml: false }
            },
            'text': {
                'text': { selector: '.pb-text', allowHtml: true }
            },
            'cta_banner': {
                'title': { selector: '.cta-banner__title', allowHtml: false },
                'subtitle': { selector: '.cta-banner__subtitle', allowHtml: false },
                'cta_text': { selector: '.cta-banner__actions .btn:first-child', allowHtml: false },
                'secondary_cta_text': { selector: '.cta-banner__actions .btn:nth-child(2)', allowHtml: false, hideWhenEmpty: true }
            },
            'testimonials': {
                'title': { selector: '.testimonials__title', allowHtml: false },
                'subtitle': { selector: '.testimonials__subtitle', allowHtml: false }
            },
            'newsletter': {
                'title': { selector: '.newsletter__title', allowHtml: false },
                'subtitle': { selector: '.newsletter__subtitle', allowHtml: false },
                'button_text': { selector: '.newsletter__submit, .newsletter .btn', allowHtml: false }
            },
            'contact_form': {
                'title': { selector: '.section-header__title', allowHtml: false },
                'description': { selector: '.section-header__subtitle', allowHtml: false },
                'submit_text': { selector: '.btn--primary', allowHtml: false }
            },
            'button': {
                'text': { selector: '.btn span, .btn', allowHtml: false }
            },
            'image': {
                'caption': { selector: '.pb-image__caption', allowHtml: false, toggleVisibility: 'show_caption' },
                'alt': { selector: 'img', attribute: 'alt' },
                'show_caption': { selector: '.pb-image__caption', toggleElement: true }
            },
            'gallery': {
                'title': { selector: '.gallery__title', allowHtml: false }
            },
            'product_grid': {
                'title': { selector: '.product-grid__title', allowHtml: false }
            },
            'product_carousel': {
                'title': { selector: '.product-carousel__title', allowHtml: false }
            },
            'promotion_banner': {
                'title': { selector: '.promotion-banner__title', allowHtml: false },
                'subtitle': { selector: '.promotion-banner__subtitle', allowHtml: false },
                'button_text': { selector: '.promotion-banner .btn', allowHtml: false }
            },
            'faq_accordion': {
                'title': { selector: '.faq-accordion__title', allowHtml: false },
                'subtitle': { selector: '.faq-accordion__subtitle', allowHtml: false }
            },
            'countdown_timer': {
                'title': { selector: '.countdown-timer__title', allowHtml: false },
                'subtitle': { selector: '.countdown-timer__subtitle', allowHtml: false }
            }
        };

        // Get mappings for this element type
        const mappings = textMappings[elementType];
        if (!mappings) return;

        const elementContent = elementWrapper.querySelector('.element-content');
        if (!elementContent) return;

        // Process each property
        for (const [propKey, propValue] of Object.entries(properties)) {
            const mapping = mappings[propKey];
            if (!mapping) continue;

            // Find target element
            const targetElement = elementContent.querySelector(mapping.selector);
            if (!targetElement) continue;

            // Handle toggle element visibility (like show_caption)
            if (mapping.toggleElement) {
                if (propValue) {
                    targetElement.style.display = '';
                } else {
                    targetElement.style.display = 'none';
                }
                continue;
            }

            // Handle attribute updates (like alt text for images)
            if (mapping.attribute) {
                if (propValue) {
                    targetElement.setAttribute(mapping.attribute, propValue);
                } else {
                    targetElement.removeAttribute(mapping.attribute);
                }
                continue;
            }

            // Check if element should be hidden when empty
            const isEmpty = propValue === undefined || propValue === null || propValue === '';

            // Check if visibility is controlled by another property (e.g., show_caption)
            if (mapping.toggleVisibility) {
                const toggleProp = mapping.toggleVisibility;
                const showElement = properties[toggleProp];
                if (showElement === false) {
                    targetElement.style.display = 'none';
                    continue;
                } else if (showElement === true) {
                    targetElement.style.display = '';
                }
            }

            if (mapping.hideWhenEmpty) {
                // Toggle visibility based on whether text is empty
                if (isEmpty) {
                    targetElement.style.display = 'none';
                } else {
                    targetElement.style.display = '';
                }
            }

            // Update text content
            if (!isEmpty) {
                if (mapping.allowHtml) {
                    // For elements that allow HTML, use innerHTML
                    // Convert line breaks to <br> for plain text with newlines
                    const htmlContent = propValue.replace(/\n/g, '<br>');
                    targetElement.innerHTML = htmlContent;
                } else {
                    // For plain text elements, use textContent
                    targetElement.textContent = propValue;
                }
            }
        }
    }

    /**
     * Apply class-based property changes for form elements
     * Form elements use CSS class modifiers rather than inline styles
     * @param {HTMLElement} elementWrapper - The element wrapper
     * @param {Object} properties - Properties being updated
     */
    applyFormElementClasses(elementWrapper, properties) {
        const formElement = elementWrapper.querySelector('.fb-form');
        const formActions = elementWrapper.querySelectorAll('.fb-form__actions');
        const formButtons = elementWrapper.querySelectorAll('.fb-form__btn--submit, .fb-form__btn--next');

        // Class mappings: property -> { target/targets, prefix, values }
        const classMappings = {
            field_style: { target: formElement, prefix: 'fb-form--', values: ['outlined', 'filled', 'underlined'] },
            label_position: { target: formElement, prefix: 'fb-form--labels-', values: ['above', 'floating', 'inline'] },
            field_size: { target: formElement, prefix: 'fb-form--size-', values: ['sm', 'md', 'lg'] },
            field_spacing: { target: formElement, prefix: 'fb-form--spacing-', values: ['compact', 'normal', 'spacious'] },
            button_style: { targets: formButtons, prefix: 'btn--', values: ['primary', 'secondary', 'outline'] },
            button_size: { targets: formButtons, prefix: 'btn--', values: ['sm', 'md', 'lg'] },
            button_alignment: { targets: formActions, prefix: 'fb-form__actions--', values: ['left', 'center', 'right', 'space-between'] }
        };

        // Apply class-based property changes
        for (const [propKey, propValue] of Object.entries(properties)) {
            const mapping = classMappings[propKey];
            if (!mapping || propValue === undefined) continue;

            const targets = mapping.targets || (mapping.target ? [mapping.target] : []);
            targets.forEach(target => {
                if (!target) return;
                // Remove all possible values for this property
                mapping.values.forEach(v => target.classList.remove(mapping.prefix + v));
                // Add the new value
                target.classList.add(mapping.prefix + propValue);
            });
        }

        // Handle button_width separately (add/remove single class)
        if (properties.button_width !== undefined) {
            formButtons.forEach(btn => {
                if (!btn) return;
                if (properties.button_width === 'full') {
                    btn.classList.add('btn--full');
                } else {
                    btn.classList.remove('btn--full');
                }
            });
        }

        // Handle step indicator style switching
        if (properties.step_indicator_style !== undefined) {
            const indicatorContainer = elementWrapper.querySelector('.fb-form__step-indicator');
            if (indicatorContainer) {
                // Update the indicator type class
                const styles = ['progress_bar', 'numbered_circles', 'breadcrumb', 'steps_text', 'none'];
                styles.forEach(s => indicatorContainer.classList.remove(`fb-form__step-indicator--${s}`));
                indicatorContainer.classList.add(`fb-form__step-indicator--${properties.step_indicator_style}`);

                // Show/hide the container based on 'none' selection
                indicatorContainer.style.display = properties.step_indicator_style === 'none' ? 'none' : '';

                // Show/hide individual indicator types
                const progressBar = indicatorContainer.querySelector('.fb-progress-bar');
                const progressBarText = indicatorContainer.querySelector('.fb-progress-bar__text');
                const circles = indicatorContainer.querySelector('.fb-step-circles');
                const breadcrumb = indicatorContainer.querySelector('.fb-breadcrumb');
                const stepsText = indicatorContainer.querySelector('.fb-steps-text');

                if (progressBar) progressBar.style.display = properties.step_indicator_style === 'progress_bar' ? '' : 'none';
                if (progressBarText) progressBarText.style.display = properties.step_indicator_style === 'progress_bar' ? '' : 'none';
                if (circles) circles.style.display = properties.step_indicator_style === 'numbered_circles' ? '' : 'none';
                if (breadcrumb) breadcrumb.style.display = properties.step_indicator_style === 'breadcrumb' ? '' : 'none';
                if (stepsText) stepsText.style.display = properties.step_indicator_style === 'steps_text' ? '' : 'none';
            }
        }

        // Handle validation display mode
        if (properties.validation_display !== undefined) {
            if (formElement) {
                const modes = ['below_field', 'tooltip', 'summary'];
                modes.forEach(m => formElement.classList.remove(`fb-form--validation-${m}`));
                formElement.classList.add(`fb-form--validation-${properties.validation_display}`);
            }

            // Update error summary container mode
            const errorSummary = elementWrapper.querySelector('.fb-form__error-summary');
            if (errorSummary) {
                errorSummary.dataset.mode = properties.validation_display;
            }
        }

        // Handle visibility toggles
        this.applyFormVisibilityToggles(elementWrapper, properties);
    }

    /**
     * Apply visibility toggles for form elements
     * @param {HTMLElement} elementWrapper - The element wrapper
     * @param {Object} properties - Properties being updated
     */
    applyFormVisibilityToggles(elementWrapper, properties) {
        const visibilityMappings = {
            show_title: '.fb-form__title',
            show_description: '.fb-form__description',
            show_step_titles: '.fb-step-circle__label, .fb-form__step-title',
            show_step_descriptions: '.fb-form__step-description'
        };

        for (const [propKey, propValue] of Object.entries(properties)) {
            const selector = visibilityMappings[propKey];
            if (selector === undefined) continue;

            const elements = elementWrapper.querySelectorAll(selector);
            elements.forEach(el => {
                el.style.display = propValue ? '' : 'none';
            });
        }

        // Handle title styling (typography, color, shadow)
        const titleEl = elementWrapper.querySelector('.fb-form__title');
        if (titleEl) {
            if (properties.title_typography !== undefined) {
                const styles = this.parseTypographyString(properties.title_typography);
                for (const [prop, value] of Object.entries(styles)) {
                    titleEl.style[prop] = value;
                }
            }
            if (properties.title_color !== undefined) {
                titleEl.style.color = properties.title_color || '';
            }
            if (properties.title_shadow !== undefined) {
                titleEl.style.textShadow = properties.title_shadow || '';
            }
        }

        // Handle description styling (typography, color, shadow)
        const descEl = elementWrapper.querySelector('.fb-form__description');
        if (descEl) {
            if (properties.description_typography !== undefined) {
                const styles = this.parseTypographyString(properties.description_typography);
                for (const [prop, value] of Object.entries(styles)) {
                    descEl.style[prop] = value;
                }
            }
            if (properties.description_color !== undefined) {
                descEl.style.color = properties.description_color || '';
            }
            if (properties.description_shadow !== undefined) {
                descEl.style.textShadow = properties.description_shadow || '';
            }
        }

        // Handle required indicator visibility via CSS class
        if (properties.show_required_indicator !== undefined) {
            const formElement = elementWrapper.querySelector('.fb-form');
            if (formElement) {
                if (properties.show_required_indicator) {
                    formElement.classList.remove('fb-form--hide-required');
                } else {
                    formElement.classList.add('fb-form--hide-required');
                }
            }
        }

        // Handle help text visibility via CSS class
        if (properties.show_help_text !== undefined) {
            const formElement = elementWrapper.querySelector('.fb-form');
            if (formElement) {
                if (properties.show_help_text) {
                    formElement.classList.remove('fb-form--hide-help');
                } else {
                    formElement.classList.add('fb-form--hide-help');
                }
            }
        }

        // Apply step indicator inline styles
        this.applyFormStepIndicatorStyles(elementWrapper, properties);
    }

    /**
     * Apply inline styles for form step indicator customization
     * @param {HTMLElement} elementWrapper - The element wrapper
     * @param {Object} properties - Properties being updated
     */
    applyFormStepIndicatorStyles(elementWrapper, properties) {
        // Progress bar styles
        const progressBar = elementWrapper.querySelector('.fb-progress-bar');
        if (progressBar) {
            if (properties.progress_bar_height) {
                progressBar.style.height = properties.progress_bar_height;
            }
            if (properties.progress_bar_bg_color) {
                progressBar.style.backgroundColor = properties.progress_bar_bg_color;
            }
            if (properties.progress_bar_radius) {
                progressBar.style.borderRadius = properties.progress_bar_radius;
            }
        }

        const progressBarFill = elementWrapper.querySelector('.fb-progress-bar__fill');
        if (progressBarFill) {
            if (properties.progress_bar_fill_color) {
                progressBarFill.style.backgroundColor = properties.progress_bar_fill_color;
            }
            if (properties.progress_bar_radius) {
                progressBarFill.style.borderRadius = properties.progress_bar_radius;
            }
        }

        // Numbered circles styles
        const stepCircles = elementWrapper.querySelectorAll('.fb-step-circle');
        stepCircles.forEach(circle => {
            if (properties.circle_size) {
                circle.style.width = properties.circle_size;
                circle.style.height = properties.circle_size;
                circle.style.minWidth = properties.circle_size;
            }

            // Apply colors based on state (active or inactive)
            const isActive = circle.classList.contains('fb-step-circle--active');
            const isCompleted = circle.classList.contains('fb-step-circle--completed');

            if (isCompleted && properties.circle_completed_bg) {
                circle.style.backgroundColor = properties.circle_completed_bg;
                if (properties.circle_active_text) {
                    circle.style.color = properties.circle_active_text;
                }
            } else if (isActive) {
                if (properties.circle_active_bg) {
                    circle.style.backgroundColor = properties.circle_active_bg;
                }
                if (properties.circle_active_text) {
                    circle.style.color = properties.circle_active_text;
                }
            } else {
                if (properties.circle_inactive_bg) {
                    circle.style.backgroundColor = properties.circle_inactive_bg;
                }
                if (properties.circle_inactive_text) {
                    circle.style.color = properties.circle_inactive_text;
                }
            }

            // Store colors as data attributes for JS step navigation
            if (properties.circle_inactive_bg) {
                circle.dataset.inactiveBg = properties.circle_inactive_bg;
            }
            if (properties.circle_inactive_text) {
                circle.dataset.inactiveText = properties.circle_inactive_text;
            }
            if (properties.circle_active_bg) {
                circle.dataset.activeBg = properties.circle_active_bg;
            }
            if (properties.circle_active_text) {
                circle.dataset.activeText = properties.circle_active_text;
            }
            if (properties.circle_completed_bg) {
                circle.dataset.completedBg = properties.circle_completed_bg;
            }
        });

        // Circle number typography
        const circleNumbers = elementWrapper.querySelectorAll('.fb-step-circle__number');
        if (properties.circle_number_typography) {
            const styles = this.parseTypographyString(properties.circle_number_typography);
            circleNumbers.forEach(num => {
                for (const [prop, value] of Object.entries(styles)) {
                    num.style[prop] = value;
                }
            });
        }

        // Circle label typography
        const circleLabels = elementWrapper.querySelectorAll('.fb-step-circle__label');
        if (properties.circle_label_typography) {
            const styles = this.parseTypographyString(properties.circle_label_typography);
            circleLabels.forEach(label => {
                for (const [prop, value] of Object.entries(styles)) {
                    label.style[prop] = value;
                }
            });
        }

        // Connector styles
        const connectors = elementWrapper.querySelectorAll('.fb-step-connector');
        connectors.forEach(connector => {
            if (properties.connector_color) {
                connector.style.backgroundColor = properties.connector_color;
            }
            if (properties.connector_width) {
                connector.style.height = properties.connector_width;
            }
        });

        // Breadcrumb styles
        const breadcrumb = elementWrapper.querySelector('.fb-breadcrumb');
        if (breadcrumb) {
            if (properties.breadcrumb_bg_color) {
                breadcrumb.style.backgroundColor = properties.breadcrumb_bg_color;
            }
        }

        const breadcrumbItems = elementWrapper.querySelectorAll('.fb-breadcrumb__item');
        if (properties.breadcrumb_typography) {
            const styles = this.parseTypographyString(properties.breadcrumb_typography);
            breadcrumbItems.forEach(item => {
                for (const [prop, value] of Object.entries(styles)) {
                    item.style[prop] = value;
                }
            });
        }
        breadcrumbItems.forEach(item => {
            const isActive = item.classList.contains('fb-breadcrumb__item--active');
            if (isActive && properties.breadcrumb_active_color) {
                item.style.color = properties.breadcrumb_active_color;
                item.dataset.activeColor = properties.breadcrumb_active_color;
            }
        });

        const breadcrumbSeparators = elementWrapper.querySelectorAll('.fb-breadcrumb__separator');
        breadcrumbSeparators.forEach(sep => {
            if (properties.breadcrumb_separator_color) {
                sep.style.color = properties.breadcrumb_separator_color;
            }
        });

        // Steps text styles
        const stepsText = elementWrapper.querySelector('.fb-steps-text');
        if (stepsText) {
            if (properties.steps_text_color) {
                stepsText.style.color = properties.steps_text_color;
            }
            if (properties.steps_text_typography) {
                const styles = this.parseTypographyString(properties.steps_text_typography);
                for (const [prop, value] of Object.entries(styles)) {
                    stepsText.style[prop] = value;
                }
            }
        }
    }

    /**
     * Apply class-based property changes for button elements in hero and cta_banner
     * Button style and size use CSS class modifiers rather than inline styles
     * @param {HTMLElement} elementWrapper - The element wrapper
     * @param {string} elementType - Type of element (hero, cta_banner)
     * @param {Object} properties - Properties being updated
     */
    applyButtonClasses(elementWrapper, elementType, properties) {
        const elementContent = elementWrapper.querySelector('.element-content');
        if (!elementContent) return;

        // Define button selectors and class mappings per element type
        const buttonConfigs = {
            'hero': {
                primary: {
                    selector: '.hero__actions .btn:first-child',
                    styleProperty: 'button_style',
                    sizeProperty: 'button_size',
                    styleClasses: { 'primary': 'btn--primary', 'outline': 'btn--outline', 'ghost': 'btn--ghost' },
                    sizeClasses: { 'sm': 'btn--sm', 'md': '', 'lg': 'btn--lg' }
                },
                secondary: {
                    selector: '.hero__actions .btn:nth-child(2)',
                    styleProperty: 'secondary_button_style',
                    sizeProperty: 'secondary_button_size',
                    // Secondary button: solid maps to primary, default is outline
                    styleClasses: { 'solid': 'btn--primary', 'outline': 'btn--outline', 'ghost': 'btn--ghost' },
                    sizeClasses: { 'sm': 'btn--sm', 'md': '', 'lg': 'btn--lg' }
                }
            },
            'cta_banner': {
                primary: {
                    selector: '.cta-banner__actions .btn:first-child',
                    styleProperty: 'cta_style',
                    sizeProperty: 'cta_size',
                    styleClasses: { 'primary': 'btn--primary', 'outline': 'btn--outline', 'ghost': 'btn--ghost' },
                    sizeClasses: { 'sm': 'btn--sm', 'md': '', 'lg': 'btn--lg' }
                },
                secondary: {
                    selector: '.cta-banner__actions .btn:nth-child(2)',
                    styleProperty: 'secondary_cta_style',
                    sizeProperty: 'secondary_cta_size',
                    styleClasses: { 'solid': 'btn--primary', 'outline': 'btn--outline', 'ghost': 'btn--ghost' },
                    sizeClasses: { 'sm': 'btn--sm', 'md': '', 'lg': 'btn--lg' }
                }
            }
        };

        const config = buttonConfigs[elementType];
        if (!config) return;

        // Process each button (primary and secondary)
        for (const buttonConfig of Object.values(config)) {
            const buttonElement = elementContent.querySelector(buttonConfig.selector);
            if (!buttonElement) continue;

            // Handle style property
            const styleValue = properties[buttonConfig.styleProperty];
            if (styleValue !== undefined) {
                // Remove all style classes
                Object.values(buttonConfig.styleClasses).forEach(cls => {
                    if (cls) buttonElement.classList.remove(cls);
                });
                // Add the new style class
                const newStyleClass = buttonConfig.styleClasses[styleValue];
                if (newStyleClass) {
                    buttonElement.classList.add(newStyleClass);
                } else if (!styleValue || styleValue === 'primary') {
                    // Default to primary for primary button
                    buttonElement.classList.add('btn--primary');
                } else {
                    // Default to outline for secondary button
                    buttonElement.classList.add('btn--outline');
                }
            }

            // Handle size property
            const sizeValue = properties[buttonConfig.sizeProperty];
            if (sizeValue !== undefined) {
                // Remove all size classes
                Object.values(buttonConfig.sizeClasses).forEach(cls => {
                    if (cls) buttonElement.classList.remove(cls);
                });
                // Add the new size class
                const newSizeClass = buttonConfig.sizeClasses[sizeValue];
                if (newSizeClass) {
                    buttonElement.classList.add(newSizeClass);
                }
            }
        }
    }

    /**
     * Apply image filter effects (presets and custom sliders)
     * @param {HTMLElement} elementWrapper - The element wrapper
     * @param {Object} properties - Properties being updated
     */
    applyImageFilters(elementWrapper, properties) {
        const imgElement = elementWrapper.querySelector('img');
        if (!imgElement) return;

        // Check if any filter-related property is being updated
        const filterProps = ['filter_preset', 'filter_grayscale', 'filter_brightness',
                            'filter_contrast', 'filter_saturate', 'filter_blur'];
        const hasFilterUpdate = filterProps.some(prop => properties[prop] !== undefined);

        if (!hasFilterUpdate) return;

        // Get stored content for this element to merge with updated properties
        const elementId = elementWrapper.dataset.elementId;
        let storedContent = {};
        if (window.contentManager && elementId) {
            storedContent = window.contentManager.getContent(elementId) || {};
        }

        // Also check the property panel form for current values (more reliable for live updates)
        const propertyForm = document.querySelector(`form.element-properties-form[data-element-id="${elementId}"]`);
        let formValues = {};
        if (propertyForm) {
            filterProps.forEach(prop => {
                const input = propertyForm.querySelector(`[name="${prop}"]`);
                if (input) {
                    formValues[prop] = input.type === 'range' ? parseFloat(input.value) : input.value;
                }
            });
        }

        // Merge: storedContent < formValues < properties (properties takes highest precedence)
        const mergedProps = { ...storedContent, ...formValues, ...properties };

        // Get current filter preset
        const filterPreset = mergedProps.filter_preset;

        // Define filter presets
        const presets = {
            'none': '',
            'grayscale': 'grayscale(100%)',
            'sepia': 'sepia(80%)',
            'vintage': 'sepia(40%) contrast(90%) brightness(90%)',
            'high-contrast': 'contrast(150%) saturate(120%)',
            'soft': 'brightness(105%) contrast(95%) saturate(90%)',
            'dramatic': 'contrast(130%) brightness(90%) saturate(110%)'
        };

        // If preset is not custom, use the preset value
        if (filterPreset && filterPreset !== 'custom') {
            imgElement.style.filter = presets[filterPreset] || '';
            return;
        }

        // For custom preset, use individual slider values
        if (filterPreset === 'custom') {
            // Get values from merged properties or use defaults
            const grayscale = mergedProps.filter_grayscale ?? 0;
            const brightness = mergedProps.filter_brightness ?? 100;
            const contrast = mergedProps.filter_contrast ?? 100;
            const saturate = mergedProps.filter_saturate ?? 100;
            const blur = mergedProps.filter_blur ?? 0;

            // Build the filter string
            const filterValue = `grayscale(${grayscale}%) brightness(${brightness}%) contrast(${contrast}%) saturate(${saturate}%) blur(${blur}px)`;
            imgElement.style.filter = filterValue;
        }
    }

    /**
     * Parse typography CSS string into individual properties
     * @param {string} typographyString - CSS string from typography editor
     * @returns {Object} Parsed CSS properties
     */
    parseTypographyString(typographyString) {
        if (!typographyString || typographyString === 'inherit') return {};

        const properties = {};

        try {
            const styles = typographyString.split(';').map(s => s.trim()).filter(s => s);

            styles.forEach(style => {
                const [property, value] = style.split(':').map(s => s.trim());

                // Map CSS property names to JavaScript style property names
                const propertyMap = {
                    'font-family': 'fontFamily',
                    'font-size': 'fontSize',
                    'font-weight': 'fontWeight',
                    'font-style': 'fontStyle',
                    'line-height': 'lineHeight',
                    'letter-spacing': 'letterSpacing',
                    'word-spacing': 'wordSpacing',
                    'text-transform': 'textTransform',
                    'text-align': 'textAlign',
                    'text-decoration': 'textDecoration',
                    'text-decoration-style': 'textDecorationStyle',
                    'text-indent': 'textIndent',
                    'vertical-align': 'verticalAlign',
                    'direction': 'direction',
                    'color': 'color',
                    'text-shadow': 'textShadow'
                };

                const jsProperty = propertyMap[property] || property;
                if (value && value !== 'inherit' && value !== 'normal') {
                    properties[jsProperty] = value;
                }
            });
        } catch (e) {
            console.warn('Could not parse typography value:', typographyString);
        }

        return properties;
    }

    /**
     * Parse a CSS string into individual properties
     * @param {string} cssString - CSS properties as string (e.g., "border: 1px solid red; border-radius: 4px;")
     * @returns {Object} - Object with camelCase CSS property names and values
     */
    parseCSSString(cssString) {
        const styles = {};
        if (!cssString) return styles;

        const declarations = cssString.split(';').filter(d => d.trim());
        for (const declaration of declarations) {
            const [property, ...valueParts] = declaration.split(':');
            if (property && valueParts.length) {
                const propName = this.toCamelCase(property.trim());
                const propValue = valueParts.join(':').trim();
                styles[propName] = propValue;
            }
        }
        return styles;
    }

    /**
     * Update element with new properties
     * @param {string|number} elementId - Element ID
     * @param {Object} properties - Properties to update
     * @param {Object} options - Update options
     */
    updateElement(elementId, properties, options = {}) {
        console.log('[LivePreviewManager] updateElement called:', {
            elementId: elementId,
            propertyKeys: Object.keys(properties),
            hasHoverBg: 'data-hover-background' in properties,
            options: options
        });

        const defaults = {
            instant: true,      // Apply visual changes immediately
            sync: true,         // Sync to server
            debounce: true      // Debounce server sync
        };

        const settings = { ...defaults, ...options };

        // Apply instant visual updates
        if (settings.instant) {
            console.log('[LivePreviewManager] Calling applyStyles for element:', elementId);
            this.applyStyles(elementId, properties);
        }

        // Queue server sync
        if (settings.sync) {
            this.queueServerSync(elementId, properties, settings.debounce);
        }
    }

    /**
     * Apply styles immediately to element
     * @param {string|number} elementId - Element ID
     * @param {Object} properties - Style properties
     */
    applyStyles(elementId, properties) {
        // Skip page settings - they don't have a DOM element in the canvas
        // Page design settings are applied at the page level, not element level
        if (typeof elementId === 'string' && elementId.startsWith('page-')) {
            return;
        }

        console.log('[LivePreviewManager] applyStyles called:', {
            elementId: elementId,
            propertyKeys: Object.keys(properties)
        });

        // Find element wrapper - use specific selector to target only visual elements
        // (not the form panel which also has data-element-id)
        const elementWrapper = document.querySelector(`.element-wrapper[data-element-id="${elementId}"]`);
        console.log('[LivePreviewManager] Element wrapper found:', !!elementWrapper, elementWrapper?.className);
        if (!elementWrapper) {
            console.warn(`[LivePreviewManager] Element ${elementId} not found in DOM`);
            return;
        }

        // Get element type
        const elementType = elementWrapper.dataset.elementType || 'default';

        // Handle element-specific style properties (e.g., title_typography, title_color)
        this.applyElementSpecificStylesFromProperties(elementWrapper, elementType, properties);

        // Handle text content updates (e.g., title, subtitle, description, button_text)
        this.applyTextContentFromProperties(elementWrapper, elementType, properties);

        // Handle form element class-based properties
        if (elementType === 'form') {
            this.applyFormElementClasses(elementWrapper, properties);
        }

        // Handle button class-based properties (style, size) for hero and cta_banner
        if (elementType === 'hero' || elementType === 'cta_banner') {
            this.applyButtonClasses(elementWrapper, elementType, properties);
        }

        // Handle image src attribute updates
        if (elementType === 'image' && properties.src !== undefined) {
            const imgElement = elementWrapper.querySelector('img');
            if (imgElement && properties.src) {
                imgElement.src = properties.src;
                console.log('[LivePreviewManager] Updated image src:', properties.src);
            }
        }

        // Handle image filter updates
        if (elementType === 'image') {
            this.applyImageFilters(elementWrapper, properties);
        }

        // Find target element for styles
        const targetElement = this.findTargetElement(elementWrapper, elementType);
        if (!targetElement) {
            console.warn(`Target element not found for ${elementType}`);
            return;
        }

        // Apply entrance animation if any animation properties are present
        if (properties.animation_type || properties.animation_duration ||
            properties.animation_delay || properties.animation_timing ||
            properties.animation_repeat) {
            this.applyAnimation(targetElement, properties);
        }

        // Apply hover animation if any hover animation properties are present
        if (properties.hover_animation_type || properties.hover_animation_duration ||
            properties.hover_animation_timing || properties.hover_animation_intensity) {
            this.applyHoverAnimation(targetElement, properties);
        }

        // Handle divider element properties via CSS custom properties (CSS-only implementation)
        if (elementType === 'divider') {
            this.applyDividerStyles(elementWrapper, targetElement, properties);
            this.dispatchUpdateEvent(elementWrapper, properties);
            return;
        }

        // Handle spacer element height with unit
        if (elementType === 'spacer') {
            if (properties.height !== undefined || properties.height_unit !== undefined) {
                // Get current height from inline style
                const currentHeight = targetElement.style.height || '40px';
                const heightMatch = currentHeight.match(/^(\d+(?:\.\d+)?)/);
                const unitMatch = currentHeight.match(/[a-z%]+$/);

                // Use new values if provided, otherwise keep current
                const height = properties.height !== undefined ? properties.height : (heightMatch ? heightMatch[1] : '40');
                const unit = properties.height_unit !== undefined ? properties.height_unit : (unitMatch ? unitMatch[0] : 'px');

                targetElement.style.height = `${height}${unit}`;
                console.log('[LivePreviewManager] Updated spacer height:', `${height}${unit}`);
            }
            // Continue to apply other properties (like background from base_styles)
        }

        // Apply each property
        for (const [key, value] of Object.entries(properties)) {
            // Handle hover_background property - inject CSS rule for hover effects
            // This is sent by BackgroundEditor and should apply to the target element, not the wrapper
            if (key === 'hover_background') {
                console.log('[LivePreviewManager] applyStyles detected hover_background:', {
                    elementId: elementId,
                    elementType: elementWrapper.dataset.elementType,
                    valueLength: value ? value.length : 0
                });
                this.applyHoverBackground(elementWrapper, value);
                continue;
            }

            // Handle data attributes (including video overlay settings)
            // Skip data-hover-background as we now use hover_background instead
            if (key.startsWith('data-')) {
                // Skip deprecated data-hover-background (use hover_background instead)
                if (key === 'data-hover-background') {
                    continue;
                }

                // Apply data attributes to the element wrapper (not the target element)
                // This ensures data attributes are available for templates to use
                const attrName = key.substring(5); // Remove 'data-' prefix
                if (value !== undefined && value !== null && value !== '') {
                    elementWrapper.setAttribute(`data-${attrName}`, value);
                } else {
                    // Remove the attribute if value is empty
                    elementWrapper.removeAttribute(`data-${attrName}`);
                }
                continue;
            }

            // Skip non-style properties and animation properties (handled separately)
            if (this.isNonStyleProperty(key) || key.startsWith('animation_') || key.startsWith('hover_animation_')) {
                continue;
            }

            // Determine if value is empty (should trigger clearing)
            const isEmpty = value === '' || value === null || value === undefined;

            // Special handling for typography property
            if (key === 'typography') {
                if (isEmpty) {
                    // Clear all typography-related inline styles
                    const typographyProps = ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle',
                        'lineHeight', 'letterSpacing', 'wordSpacing', 'textTransform',
                        'textDecoration', 'textDecorationStyle', 'textIndent', 'textAlign',
                        'verticalAlign', 'direction', 'fontVariant'];
                    typographyProps.forEach(prop => targetElement.style[prop] = '');
                } else {
                    // Parse and apply typography CSS string
                    const styles = this.parseTypographyString(value);
                    for (const [cssProp, cssValue] of Object.entries(styles)) {
                        targetElement.style[cssProp] = cssValue;
                    }
                }
                continue;
            }

            // Special handling for border property with CSS string
            if (key === 'border') {
                if (isEmpty) {
                    // Clear all border-related inline styles
                    const borderProps = ['border', 'borderWidth', 'borderStyle', 'borderColor',
                        'borderRadius', 'borderTop', 'borderRight', 'borderBottom', 'borderLeft',
                        'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
                        'borderTopStyle', 'borderRightStyle', 'borderBottomStyle', 'borderLeftStyle',
                        'borderTopColor', 'borderRightColor', 'borderBottomColor', 'borderLeftColor',
                        'borderTopLeftRadius', 'borderTopRightRadius', 'borderBottomLeftRadius', 'borderBottomRightRadius',
                        'animationName', 'animationDuration', 'animationTimingFunction', 'animationIterationCount'];
                    borderProps.forEach(prop => targetElement.style[prop] = '');
                } else {
                    // Apply border CSS styles
                    this.applyBorderFromCSS(targetElement, value);
                }
                continue;
            }

            // Special handling for background property
            if (key === 'background') {
                if (isEmpty) {
                    // Clear background styles
                    targetElement.style.background = '';
                    targetElement.style.backgroundColor = '';
                } else {
                    // Apply background styles
                    targetElement.style.background = value;

                    // If background includes video, create/update video element
                    if (elementWrapper.hasAttribute('data-video-url') && elementWrapper.getAttribute('data-video-url')) {
                        this.updateVideoBackground(elementWrapper, targetElement);
                    }
                }
                continue;
            }

            // Special handling for spacing property (CSS string from spacing_editor)
            if (key === 'spacing') {
                if (isEmpty) {
                    // Clear all spacing-related inline styles
                    const spacingProps = ['margin', 'marginTop', 'marginRight', 'marginBottom', 'marginLeft',
                        'padding', 'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'];
                    spacingProps.forEach(prop => targetElement.style[prop] = '');
                } else {
                    // Parse and apply spacing CSS (margin and padding properties)
                    const spacingProps = value.split(';').map(p => p.trim()).filter(p => p);
                    spacingProps.forEach(prop => {
                        const colonIndex = prop.indexOf(':');
                        if (colonIndex === -1) return;
                        const cssPropName = prop.substring(0, colonIndex).trim();
                        const cssValue = prop.substring(colonIndex + 1).trim();
                        const camelCase = cssPropName.replace(/-([a-z])/g, (_, letter) => letter.toUpperCase());
                        try {
                            targetElement.style[camelCase] = cssValue;
                        } catch (e) {
                            console.warn(`Failed to apply spacing ${cssPropName}: ${cssValue}`, e);
                        }
                    });
                }
                continue;
            }

            // Special handling for shadow properties (box_shadow, boxShadow, shadow, text_shadow, textShadow)
            // The shadow_editor may save values as "box-shadow: ..." which works in templates
            // but needs to be parsed for JavaScript's style.boxShadow property
            if (key === 'box_shadow' || key === 'boxShadow' || key === 'shadow') {
                if (isEmpty) {
                    targetElement.style.boxShadow = '';
                } else {
                    let shadowValue = value;
                    // Extract just the value if the full CSS property is included
                    if (typeof value === 'string' && value.toLowerCase().startsWith('box-shadow:')) {
                        shadowValue = value.substring(11).trim().replace(/;$/, '');
                    }
                    targetElement.style.boxShadow = shadowValue;
                }
                continue;
            }
            if (key === 'text_shadow' || key === 'textShadow') {
                targetElement.style.textShadow = isEmpty ? '' : value;
                continue;
            }

            // Map property name to CSS property
            const cssProperty = this.propertyMap[key] || this.toCamelCase(key);

            // Apply the style (including empty values to clear styles)
            try {
                targetElement.style[cssProperty] = isEmpty ? '' : value;
            } catch (e) {
                console.warn(`Failed to apply ${cssProperty}: ${value}`, e);
            }
        }

        // Trigger custom event
        this.dispatchUpdateEvent(elementWrapper, properties);
    }

    /**
     * Apply border styles from CSS string
     * @param {HTMLElement} element - Target element
     * @param {string} borderCSS - Border CSS string
     */
    applyBorderFromCSS(element, borderCSS) {
        // Parse CSS string (semicolon-separated properties)
        const properties = borderCSS.split(';').map(p => p.trim()).filter(p => p);

        let hasAnimation = false;
        let animType = null;

        properties.forEach(prop => {
            const colonIndex = prop.indexOf(':');
            if (colonIndex === -1) return;

            const key = prop.substring(0, colonIndex).trim();
            const val = prop.substring(colonIndex + 1).trim();

            // Skip comments
            if (val.startsWith('/*') && val.endsWith('*/')) return;

            // Check if this is an animation property
            if (key === 'animation-name' && val.startsWith('border-')) {
                hasAnimation = true;
                animType = val.replace('border-', '');
            }

            // Convert CSS property name to camelCase for style object
            const cssProp = key.replace(/-([a-z])/g, (match, letter) => letter.toUpperCase());

            try {
                element.style[cssProp] = val;
            } catch (e) {
                console.warn(`Failed to apply border style ${key}: ${val}`, e);
            }
        });

        // Animation properties are now applied via inline styles above
        // We don't add classes because inline animation-name directly references @keyframes

        // Check for legacy animation in comments (backward compatibility)
        if (!hasAnimation) {
            const animMatch = borderCSS.match(/\/\*\s*animation:\s*border-(\w+)\s+([\d.]+s)\s+(\w+(?:-\w+)?)\s+(\w+|\d+)\s*\*\//);
            if (animMatch) {
                const [, legacyAnimType, speed, timing, iterations] = animMatch;
                // Apply legacy animation as inline styles
                element.style.animationName = `border-${legacyAnimType}`;
                element.style.animationDuration = speed || '2s';
                element.style.animationTimingFunction = timing || 'ease-in-out';
                element.style.animationIterationCount = iterations || 'infinite';
            }
        }
    }

    /**
     * Apply divider-specific styles
     * Properties like thickness, width, and color need to target the child .pb-divider__line element
     * to match how the template renders inline styles
     * @param {HTMLElement} _wrapper - Element wrapper (unused, kept for consistency)
     * @param {HTMLElement} target - Target .pb-divider element
     * @param {Object} properties - Properties to apply
     */
    applyDividerStyles(_wrapper, target, properties) {
        // Find the line element inside the divider
        const lineElement = target.querySelector('.pb-divider__line');
        if (!lineElement) {
            console.warn('[LivePreviewManager] No .pb-divider__line found in divider');
            return;
        }

        for (const [key, value] of Object.entries(properties)) {
            const isEmpty = value === '' || value === null || value === undefined;

            switch (key) {
                case 'line_color':
                    // Apply as CSS variable on the line element (used by gradient styles in CSS)
                    if (isEmpty) {
                        lineElement.style.removeProperty('--divider-color');
                    } else {
                        lineElement.style.setProperty('--divider-color', value);
                    }
                    break;

                case 'thickness':
                    // Apply as direct inline height on the line element (matches template)
                    lineElement.style.height = isEmpty ? '' : `${value}px`;
                    break;

                case 'width':
                    // Apply as direct inline width on the line element (matches template)
                    lineElement.style.width = isEmpty ? '' : value;
                    break;

                case 'margin_top':
                    // Applied to the parent container
                    target.style.marginTop = isEmpty ? '' : `${value}px`;
                    break;

                case 'margin_bottom':
                    // Applied to the parent container
                    target.style.marginBottom = isEmpty ? '' : `${value}px`;
                    break;

                case 'alignment':
                    // Transform alignment to flexbox justify-content on parent
                    const alignMap = { left: 'flex-start', center: 'center', right: 'flex-end' };
                    target.style.justifyContent = isEmpty ? '' : (alignMap[value] || 'center');
                    break;

                case 'style':
                    // Swap divider style class on parent
                    if (!isEmpty) {
                        // Remove existing style classes
                        target.className = target.className.replace(/pb-divider--\w+/g, '').trim();
                        // Add new style class
                        target.classList.add(`pb-divider--${value}`);
                    }
                    break;

                case 'opacity':
                    // Applied to the parent container
                    target.style.opacity = isEmpty ? '' : value;
                    break;

                case 'box_shadow':
                case 'boxShadow':
                    // Apply shadow directly to the line element
                    let shadowValue = value;
                    if (typeof value === 'string' && value.toLowerCase().startsWith('box-shadow:')) {
                        shadowValue = value.substring(11).trim().replace(/;$/, '');
                    }
                    lineElement.style.boxShadow = isEmpty ? '' : shadowValue;
                    break;

                // Skip animation properties - handled by base applyStyles
                default:
                    if (key.startsWith('hover_animation_') || key.startsWith('animation_')) {
                        // These are handled by applyHoverAnimation/applyAnimation
                    }
                    break;
            }
        }

        console.log('[LivePreviewManager] Applied divider styles:', {
            thickness: properties.thickness,
            width: properties.width,
            line_color: properties.line_color
        });
    }

    /**
     * Apply border styles from JSON data (backward compatibility)
     * @param {HTMLElement} element - Target element
     * @param {Object} borderData - Border configuration data
     */
    applyBorderStyles(element, borderData) {
        // Apply border style
        if (borderData.style === 'none') {
            element.style.border = 'none';
            return;
        }

        // Apply border width
        if (borderData.sidesLinked) {
            element.style.borderWidth = `${borderData.width}${borderData.widthUnit || 'px'}`;
        } else {
            const top = borderData.topWidth || borderData.width;
            const right = borderData.rightWidth || borderData.width;
            const bottom = borderData.bottomWidth || borderData.width;
            const left = borderData.leftWidth || borderData.width;
            const unit = borderData.widthUnit || 'px';
            element.style.borderWidth = `${top}${unit} ${right}${unit} ${bottom}${unit} ${left}${unit}`;
        }

        // Apply border style and color
        element.style.borderStyle = borderData.style || 'solid';
        element.style.borderColor = borderData.color || '#000000';

        // Apply border radius
        if (borderData.cornersLinked) {
            element.style.borderRadius = `${borderData.radius}${borderData.radiusUnit || 'px'}`;
        } else {
            const tl = borderData.topLeftRadius || borderData.radius;
            const tr = borderData.topRightRadius || borderData.radius;
            const br = borderData.bottomRightRadius || borderData.radius;
            const bl = borderData.bottomLeftRadius || borderData.radius;
            const unit = borderData.radiusUnit || 'px';
            element.style.borderRadius = `${tl}${unit} ${tr}${unit} ${br}${unit} ${bl}${unit}`;
        }

        // Apply animation if present
        if (borderData.animation && borderData.animation.enabled && borderData.animation.type) {
            const animType = borderData.animation.type;
            const speed = borderData.animation.speed || '2s';
            const timing = borderData.animation.timing || 'ease-in-out';
            const iterations = borderData.animation.infinite ? 'infinite' : '1';

            // Set animation properties inline (no need for classes)
            element.style.animationName = `border-${animType}`;
            element.style.animationDuration = speed;
            element.style.animationTimingFunction = timing;
            element.style.animationIterationCount = iterations;
        } else {
            // Clear animation styles if disabled
            element.style.animationName = '';
            element.style.animationDuration = '';
            element.style.animationTimingFunction = '';
            element.style.animationIterationCount = '';
        }
    }

    /**
     * Update video background element
     * @param {HTMLElement} elementWrapper - Element wrapper with data attributes
     * @param {HTMLElement} targetElement - Target element for background
     */
    updateVideoBackground(elementWrapper, targetElement) {
        const videoUrl = elementWrapper.getAttribute('data-video-url');
        if (!videoUrl) return;

        // Check if video container already exists
        let videoContainer = targetElement.querySelector('.video-background-container');

        if (!videoContainer) {
            // Create video background structure
            videoContainer = document.createElement('div');
            videoContainer.className = 'video-background-container';
            videoContainer.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                z-index: -1;
            `;

            // Create video element
            const video = document.createElement('video');
            video.className = 'background-video';
            video.style.cssText = `
                position: absolute;
                top: 50%;
                left: 50%;
                min-width: 100%;
                min-height: 100%;
                width: auto;
                height: auto;
                transform: translate(-50%, -50%);
                object-fit: cover;
            `;

            // Set video attributes
            video.src = videoUrl;
            video.autoplay = elementWrapper.getAttribute('data-video-autoplay') === 'true';
            video.loop = elementWrapper.getAttribute('data-video-loop') === 'true';
            video.muted = elementWrapper.getAttribute('data-video-muted') === 'true';
            video.playsInline = true;

            const poster = elementWrapper.getAttribute('data-video-poster');
            if (poster) {
                video.poster = poster;
            }

            videoContainer.appendChild(video);

            // Create overlay if enabled
            if (elementWrapper.getAttribute('data-video-overlay-enabled') === 'true') {
                const overlay = document.createElement('div');
                overlay.className = 'video-overlay';
                const overlayColor = elementWrapper.getAttribute('data-video-overlay-color') || '#000000';
                const overlayOpacity = elementWrapper.getAttribute('data-video-overlay-opacity') || '0.5';
                overlay.style.cssText = `
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: ${overlayColor};
                    opacity: ${overlayOpacity};
                    pointer-events: none;
                `;
                videoContainer.appendChild(overlay);
            }

            // Ensure target element has relative positioning
            if (getComputedStyle(targetElement).position === 'static') {
                targetElement.style.position = 'relative';
            }

            // Add to target element
            targetElement.insertBefore(videoContainer, targetElement.firstChild);

            // Start playing if autoplay
            if (video.autoplay) {
                video.play().catch(err => {
                    console.warn('Video autoplay failed:', err);
                });
            }
        } else {
            // Update existing video
            const video = videoContainer.querySelector('video');
            if (video) {
                video.src = videoUrl;
                video.autoplay = elementWrapper.getAttribute('data-video-autoplay') === 'true';
                video.loop = elementWrapper.getAttribute('data-video-loop') === 'true';
                video.muted = elementWrapper.getAttribute('data-video-muted') === 'true';

                const poster = elementWrapper.getAttribute('data-video-poster');
                if (poster) {
                    video.poster = poster;
                } else {
                    video.removeAttribute('poster');
                }
            }

            // Update or create overlay
            let overlay = videoContainer.querySelector('.video-overlay');
            if (elementWrapper.getAttribute('data-video-overlay-enabled') === 'true') {
                const overlayColor = elementWrapper.getAttribute('data-video-overlay-color') || '#000000';
                const overlayOpacity = elementWrapper.getAttribute('data-video-overlay-opacity') || '0.5';

                if (!overlay) {
                    overlay = document.createElement('div');
                    overlay.className = 'video-overlay';
                    overlay.style.cssText = `
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background-color: ${overlayColor};
                        opacity: ${overlayOpacity};
                        pointer-events: none;
                    `;
                    videoContainer.appendChild(overlay);
                } else {
                    overlay.style.backgroundColor = overlayColor;
                    overlay.style.opacity = overlayOpacity;
                }
            } else if (overlay) {
                // Remove overlay if disabled
                overlay.remove();
            }
        }
    }

    /**
     * Apply animation class and properties to element
     * @param {HTMLElement} element - Target element
     * @param {Object} properties - Properties including animation settings
     */
    applyAnimation(element, properties) {
        const animationType = properties.animation_type;

        // Remove all existing animation classes
        const animationClasses = [
            'animate-fadeIn', 'animate-slideInUp', 'animate-slideInDown', 'animate-slideInLeft', 'animate-slideInRight',
            'animate-zoomIn', 'animate-bounceIn', 'animate-fadeOut', 'animate-slideOutUp', 'animate-slideOutDown',
            'animate-slideOutLeft', 'animate-slideOutRight', 'animate-zoomOut', 'animate-pulse', 'animate-shake',
            'animate-bounce', 'animate-flash', 'animate-spin'
        ];
        element.classList.remove(...animationClasses);

        // If no animation type selected, we might still need to update other animation properties
        if (!animationType) {
            // Check if element has an existing animation class
            let hasExistingAnimation = false;
            for (const className of element.classList) {
                if (className.startsWith('animate-')) {
                    hasExistingAnimation = true;
                    break;
                }
            }

            // If no existing animation and no new animation type, clear all animation styles
            if (!hasExistingAnimation) {
                element.style.animationDuration = '';
                element.style.animationDelay = '';
                element.style.animationTimingFunction = '';
                element.style.animationIterationCount = '';
                return;
            }
        } else {
            // Add the new animation class
            element.classList.add(`animate-${animationType}`);

            // Force animation restart by triggering a reflow
            void element.offsetWidth;
        }

        // Apply custom animation properties as inline styles to override defaults
        // These will update even if animation_type is not changed
        if (properties.animation_duration !== undefined) {
            element.style.animationDuration = properties.animation_duration || '';
        }
        if (properties.animation_delay !== undefined) {
            element.style.animationDelay = properties.animation_delay || '';
        }
        if (properties.animation_timing !== undefined) {
            element.style.animationTimingFunction = properties.animation_timing || '';
        }
        if (properties.animation_repeat !== undefined) {
            element.style.animationIterationCount = properties.animation_repeat || '';
        }

        // Set animation fill mode to keep the final state
        if (animationType) {
            element.style.animationFillMode = 'both';
        }
    }

    /**
     * Apply hover animation settings to element
     * Uses data attributes and CSS-based hover effects via transitions
     * @param {HTMLElement} element - Target element
     * @param {Object} properties - Properties including hover animation settings
     */
    applyHoverAnimation(element, properties) {
        const hoverType = properties.hover_animation_type;
        const hoverDuration = properties.hover_animation_duration || '0.3s';
        const hoverTiming = properties.hover_animation_timing || 'ease-out';
        const hoverIntensity = properties.hover_animation_intensity || 'normal';

        // Clear existing hover animation attributes and styles
        element.removeAttribute('data-hover-animation');
        element.removeAttribute('data-hover-intensity');
        element.style.transitionDuration = '';
        element.style.transitionTimingFunction = '';
        element.style.transitionProperty = '';

        // If no hover animation type, we're done
        if (!hoverType) {
            return;
        }

        // Set data attributes for CSS-based hover effects
        element.setAttribute('data-hover-animation', hoverType);

        // Set intensity if applicable (not all effects use it)
        const intensityEffects = ['scale-up', 'scale-down', 'lift', 'rotate-cw', 'rotate-ccw',
                                  'shadow-grow', 'lift-shadow', 'zoom-brighten', 'skew'];
        if (intensityEffects.includes(hoverType)) {
            element.setAttribute('data-hover-intensity', hoverIntensity);
        }

        // Apply transition timing via inline styles
        element.style.transitionDuration = hoverDuration;
        element.style.transitionTimingFunction = hoverTiming;
        element.style.transitionProperty = 'transform, opacity, filter, box-shadow, border-color';

        console.log('[LivePreviewManager] Applied hover animation:', {
            type: hoverType,
            duration: hoverDuration,
            timing: hoverTiming,
            intensity: hoverIntensity
        });
    }

    /**
     * Find the target element for applying styles
     * @param {HTMLElement} wrapper - Element wrapper
     * @param {string} elementType - Type of element
     * @returns {HTMLElement|null} Target element
     */
    findTargetElement(wrapper, elementType) {
        const elementContent = wrapper.querySelector('.element-content');
        if (!elementContent) {
            console.log('[LivePreviewManager] findTargetElement: No .element-content found in wrapper');
            return null;
        }

        // Get selector for this element type
        const selector = this.elementSelectors[elementType] || this.elementSelectors.default;
        console.log('[LivePreviewManager] findTargetElement using selector:', selector, 'for type:', elementType);

        // Try to find element with selector
        let target = elementContent.querySelector(selector);
        console.log('[LivePreviewManager] findTargetElement querySelector result:', target?.tagName, target?.className);

        // If not found, check if content itself matches
        if (!target && elementContent.matches(selector)) {
            target = elementContent;
            console.log('[LivePreviewManager] findTargetElement: elementContent itself matches selector');
        }

        // Fallback to first child element
        if (!target) {
            target = elementContent.firstElementChild || elementContent;
            console.log('[LivePreviewManager] findTargetElement: Using fallback - firstElementChild:', target?.tagName, target?.className);
        }

        return target;
    }

    /**
     * Queue server synchronization
     * @param {string|number} elementId - Element ID
     * @param {Object} properties - Properties to sync
     * @param {boolean} debounce - Whether to debounce
     */
    queueServerSync(elementId, properties, debounce = true) {
        // Store pending updates
        const existing = this.pendingUpdates.get(elementId) || {};
        this.pendingUpdates.set(elementId, { ...existing, ...properties });

        // Clear existing timeout
        if (this.updateTimeout) {
            clearTimeout(this.updateTimeout);
        }

        // Schedule sync
        if (debounce) {
            this.updateTimeout = setTimeout(() => {
                this.syncToServer();
            }, this.updateDelay);
        } else {
            this.syncToServer();
        }
    }

    /**
     * Sync pending updates to server
     */
    async syncToServer() {
        if (this.pendingUpdates.size === 0) return;

        // Get all pending updates
        const updates = new Map(this.pendingUpdates);
        this.pendingUpdates.clear();

        // Process each element update
        for (const [elementId, properties] of updates) {
            try {
                await this.sendUpdateToServer(elementId, properties);
            } catch (error) {
                console.error(`Failed to sync element ${elementId}:`, error);
                // Re-queue failed update
                const existing = this.pendingUpdates.get(elementId) || {};
                this.pendingUpdates.set(elementId, { ...existing, ...properties });
            }
        }
    }

    /**
     * Send update to server
     * @param {string|number} elementId - Element ID
     * @param {Object} properties - Properties to update
     */
    async sendUpdateToServer(elementId, properties) {
        console.log('[LivePreviewManager] sendUpdateToServer called:', {
            elementId: elementId,
            propertyKeys: Object.keys(properties),
            hasHoverBackground: 'hover_background' in properties,
            hoverBackgroundValue: properties.hover_background ? properties.hover_background.substring(0, 50) + '...' : null
        });

        // Get current element state for comparison (to detect actual changes)
        const wrapper = document.querySelector(`.element-wrapper[data-element-id="${elementId}"]`);
        const currentTagElement = wrapper?.querySelector('h1, h2, h3, h4, h5, h6');
        const currentTag = currentTagElement?.tagName.toLowerCase();

        // Get form to extract all current values
        const form = document.querySelector(`.element-properties-form[data-element-id="${elementId}"]`);
        let allProperties = { ...properties };

        if (form) {
            // Get all form values
            const formData = new FormData(form);
            for (const [key, value] of formData.entries()) {
                if (!(key in allProperties)) {
                    allProperties[key] = value;
                }
            }

            // Get checkboxes
            form.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
                if (!(checkbox.name in allProperties)) {
                    allProperties[checkbox.name] = checkbox.checked;
                }
            });
        }

        // Send to server
        const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/api/page-builder';
        console.log('[LivePreviewManager] Sending to server:', {
            url: `${apiBaseUrl}/elements/${elementId}/`,
            hasHoverBackground: 'hover_background' in allProperties,
            hoverBackgroundValue: allProperties.hover_background ? allProperties.hover_background.substring(0, 80) + '...' : null,
            allPropertyKeys: Object.keys(allProperties)
        });
        const response = await fetch(`${apiBaseUrl}/elements/${elementId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({ content: allProperties })
        });

        if (!response.ok) {
            throw new Error(`Server update failed: ${response.status}`);
        }

        const data = await response.json();

        // Get element type for element-specific property handling
        const elementWrapper = document.querySelector(`.element-wrapper[data-element-id="${elementId}"]`);
        const elementType = elementWrapper?.dataset?.elementType || null;

        // Check if any content properties were updated that need HTML re-render
        // These are properties that can add/remove DOM elements (like button text)
        // For 'tag' property, only trigger refresh if the tag actually CHANGED
        const rerenderProps = Object.keys(properties).filter(key => {
            if (key === 'tag') {
                // Only include 'tag' if it actually changed from current DOM state
                const newTag = properties[key];
                const tagChanged = currentTag && newTag && newTag !== currentTag;
                console.log('[LivePreviewManager] Tag comparison:', { currentTag, newTag, tagChanged });
                return tagChanged;
            }
            return this.isContentProperty(key, elementType);
        });
        const needsHtmlRefresh = rerenderProps.length > 0;

        console.log('[LivePreviewManager] Checking HTML refresh:', {
            needsHtmlRefresh,
            rerenderProps,
            hasHtml: !!data.element?.html,
            currentTag
        });

        if (needsHtmlRefresh && data.element?.html) {
            console.log('[LivePreviewManager] Calling refreshElementHtml for element:', elementId);
            this.refreshElementHtml(elementId, data.element.html);
        }

        return data;
    }

    /**
     * Check if property is a content property that needs HTML refresh
     * These properties can add/remove DOM elements, not just change styles
     * @param {string} key - Property key
     * @param {string} elementType - Optional element type for element-specific handling
     * @returns {boolean}
     */
    isContentProperty(key, _elementType = null) {
        // Properties that require full HTML refresh from server
        const fullRefreshProps = [
            'form_slug',  // Form element - selecting different form requires full re-render
            'tag',        // Heading element - changing HTML tag requires full re-render
            'frames',     // Image accordion - array of frames needs full re-render
            'images',     // Gallery - array of images needs full re-render
            'testimonials', // Testimonials - array needs full re-render
            'items',        // FAQ accordion - array of items needs full re-render
            'text_align',   // CTA banner / hero - alignment changes CSS class, needs re-render
            'platforms',    // Social links - array of platform links needs full re-render
            'reviews'       // Reviews display - array of static reviews needs full re-render
        ];

        // Element-specific properties that require full HTML refresh
        // These are properties that control template inline styles/conditionals
        const elementSpecificRefresh = {
            'social_links': ['style', 'size', 'color_scheme', 'custom_color', 'alignment', 'gap'],
            'contact_form': ['show_first_name', 'show_last_name', 'show_phone', 'show_subject',
                'show_privacy_checkbox', 'required_first_name', 'required_last_name',
                'required_phone', 'required_subject', 'required_privacy', 'message_rows',
                'placeholder_first_name', 'placeholder_last_name', 'placeholder_email',
                'placeholder_phone', 'placeholder_subject', 'placeholder_message',
                'privacy_text', 'privacy_url', 'terms_url',
                'show_success_message', 'show_error_message', 'success_message', 'error_message'],
            'reviews_display': [
                'data_source', 'source_type', 'product_id', 'min_rating', 'max_reviews',
                'show_verified_only', 'layout', 'columns', 'card_style',
                'show_summary', 'summary_position', 'show_rating', 'show_date',
                'show_verified_badge', 'show_images', 'show_helpful_votes',
                'show_avatar', 'show_product_name', 'star_color', 'verified_color',
                'show_carousel_arrows', 'show_carousel_dots', 'carousel_autoplay', 'carousel_interval',
                'show_write_review', 'write_review_text', 'write_review_login_text'
            ],
            'product_grid': [
                'data_source', 'source_type', 'category_id', 'collection_id',
                'max_products', 'sort_order', 'product_ids', 'layout',
                'columns', 'slides_per_view', 'featured_count', 'hero_layout',
                'show_badges', 'show_quick_actions', 'show_add_to_cart',
                'image_position', 'show_description', 'masonry_columns', 'gap_size',
                'hide_out_of_stock', 'hide_gift_cards', 'hide_digital',
                'hide_booking', 'hide_bundles', 'min_price', 'max_price'
            ],
            'category_showcase': [
                'data_source', 'source_type', 'parent_category_id', 'category_ids',
                'max_categories', 'show_product_count', 'show_description', 'show_image',
                'style', 'columns', 'image_ratio', 'hide_empty', 'spacing'
            ]
        };

        if (_elementType && elementSpecificRefresh[_elementType]) {
            if (elementSpecificRefresh[_elementType].includes(key)) {
                return true;
            }
        }

        // Check for exact matches first (full refresh required)
        if (fullRefreshProps.includes(key)) {
            return true;
        }

        const contentProps = [
            'button_text', 'secondary_button_text',
            'show_scroll_indicator', 'show_',
            '_text', '_url', '_target',
            // Button styling properties - applied inline in template, need HTML refresh
            'button_background', 'button_text_color', 'button_border',
            'button_typography', 'button_padding', 'button_shadow',
            'secondary_button_background', 'secondary_button_text_color',
            'secondary_button_border', 'secondary_button_typography',
            'secondary_button_padding', 'secondary_button_shadow',
            // Overlay and style properties that affect template output
            'overlay_style', 'content_align'
        ];
        return contentProps.some(prop => key.includes(prop));
    }

    /**
     * Refresh element HTML in the DOM
     * @param {string|number} elementId - Element ID
     * @param {string} html - New HTML content
     */
    refreshElementHtml(elementId, html) {
        const wrapper = document.querySelector(`.element-wrapper[data-element-id="${elementId}"]`);
        if (wrapper && html) {
            console.log('[LivePreviewManager] Refreshing element HTML:', elementId);
            wrapper.outerHTML = html;
        }
    }

    /**
     * Get CSRF token
     */
    getCSRFToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        if (token) return token.value;
        return '';
    }

    /**
     * Check if property is non-style
     * @param {string} key - Property key
     * @returns {boolean}
     */
    isNonStyleProperty(key) {
        // These are valid CSS style properties that start with 'text' - don't filter them out
        const validTextStyleProps = [
            'text_color', 'textColor', 'text_shadow', 'textShadow',
            'text_align', 'textAlign', 'text_transform', 'textTransform',
            'text_decoration', 'textDecoration', 'text_indent', 'textIndent'
        ];

        // If it's a valid text style property, don't filter it out
        if (validTextStyleProps.includes(key)) {
            return false;
        }

        const nonStyleProps = [
            'text', 'content', 'href', 'src', 'alt', 'title',
            'placeholder', 'value', 'name', 'id', 'class',
            'data', 'aria', 'role', 'tabindex',
            // Sub-element properties - handled via applyElementSpecificStylesFromProperties()
            'button_', 'secondary_button_',
            // Element layout/content properties that map to CSS classes in templates
            // (applying 'columns' directly would set the CSS multi-column 'columns' property,
            // collapsing grid layouts — it must be handled via full refresh instead)
            'columns'
        ];

        return nonStyleProps.some(prop => key.startsWith(prop));
    }

    /**
     * Convert string to camelCase
     * @param {string} str - String to convert
     * @returns {string}
     */
    toCamelCase(str) {
        return str.replace(/[-_]([a-z])/g, (match, letter) => letter.toUpperCase());
    }

    /**
     * Dispatch update event
     * @param {HTMLElement} element - Element that was updated
     * @param {Object} properties - Properties that were updated
     */
    dispatchUpdateEvent(element, properties) {
        const event = new CustomEvent('livePreviewUpdate', {
            detail: { properties },
            bubbles: true
        });
        element.dispatchEvent(event);
    }

    /**
     * Register a utility with the preview manager
     * @param {Object} utility - Utility instance
     * @param {string|number} elementId - Associated element ID
     */
    registerUtility(utility, elementId) {
        // Store utility reference if needed
        if (!this.utilities) {
            this.utilities = new Map();
        }
        this.utilities.set(elementId, utility);
    }

    /**
     * Set update delay
     * @param {number} delay - Delay in milliseconds
     */
    setUpdateDelay(delay) {
        this.updateDelay = delay;
    }

    /**
     * Apply hover background by injecting a CSS rule with :hover selector
     * @param {HTMLElement} elementWrapper - The element wrapper (has data-element-id)
     * @param {string} hoverCSS - The CSS background value for hover state
     */
    applyHoverBackground(elementWrapper, hoverCSS) {
        console.log('[LivePreviewManager] applyHoverBackground called with:', {
            elementWrapper: elementWrapper,
            elementWrapperExists: !!elementWrapper,
            elementWrapperClass: elementWrapper?.className,
            elementWrapperTag: elementWrapper?.tagName,
            hoverCSS: hoverCSS ? hoverCSS.substring(0, 80) + '...' : null
        });

        if (!elementWrapper) {
            console.warn('[LivePreviewManager] applyHoverBackground: No element wrapper provided');
            return;
        }

        // Verify this is actually an element wrapper, not an input field
        if (elementWrapper.tagName === 'INPUT' || elementWrapper.tagName === 'TEXTAREA') {
            console.warn('[LivePreviewManager] applyHoverBackground: Received input element instead of wrapper, skipping');
            return;
        }

        // Find the actual target element inside the wrapper (same as where normal background is applied)
        const elementType = elementWrapper.dataset.elementType || 'default';
        let targetElement = this.findTargetElement(elementWrapper, elementType);

        console.log('[LivePreviewManager] findTargetElement result:', {
            elementType: elementType,
            targetElement: targetElement,
            targetElementTag: targetElement?.tagName,
            targetElementClass: targetElement?.className
        });

        // Fallback: if findTargetElement fails, try to find element directly
        if (!targetElement) {
            console.log('[LivePreviewManager] findTargetElement failed, trying fallback selectors');
            const elementContent = elementWrapper.querySelector('.element-content');
            if (elementContent) {
                // Try common element patterns
                targetElement = elementContent.querySelector('section, .hero, .cta-banner, .testimonials, .gallery, .newsletter, .product-carousel, .product-grid');
                if (!targetElement) {
                    // Last resort: first child element
                    targetElement = elementContent.firstElementChild;
                }
                console.log('[LivePreviewManager] Fallback found:', targetElement?.tagName, targetElement?.className);
            }
        }

        if (!targetElement) {
            console.warn('[LivePreviewManager] Could not find target element for hover background after fallbacks');
            return;
        }

        // Ensure target element has an ID for CSS targeting
        const elementId = elementWrapper.dataset.elementId || Math.random().toString(36).substr(2, 9);
        if (!targetElement.id) {
            targetElement.id = 'pb-target-' + elementId;
            console.log('[LivePreviewManager] Assigned new ID to target element:', targetElement.id);
        } else {
            console.log('[LivePreviewManager] Target element already has ID:', targetElement.id);
        }

        // Find or create the hover styles container
        let styleEl = document.getElementById('pb-hover-styles');
        if (!styleEl) {
            styleEl = document.createElement('style');
            styleEl.id = 'pb-hover-styles';
            document.head.appendChild(styleEl);
            console.log('[LivePreviewManager] Created new style element for hover styles');
        }

        // Remove existing rule for this element (if any)
        const selector = `#${targetElement.id}`;
        const existingRules = styleEl.textContent || '';
        const ruleRegex = new RegExp(`\\s*${selector.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}:hover\\s*\\{[^}]*\\}`, 'g');
        styleEl.textContent = existingRules.replace(ruleRegex, '');

        // Add new hover rule if value provided
        if (hoverCSS && hoverCSS.trim()) {
            const rule = `\n${selector}:hover { background: ${hoverCSS} !important; transition: background 0.3s ease; }`;
            styleEl.textContent += rule;
            console.log('[LivePreviewManager] Applied hover background for', selector, '- Rule:', rule.substring(0, 100) + '...');
            console.log('[LivePreviewManager] Full style element content:', styleEl.textContent);
        } else {
            console.log('[LivePreviewManager] Removed hover background for', selector, '(hoverCSS was empty/null)');
        }
    }

    // Note: initializeHoverBackgrounds() removed - templates now render hover styles via <style> blocks
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    new LivePreviewManager();
});

// Also initialize immediately if DOM already loaded
if (document.readyState !== 'loading') {
    new LivePreviewManager();
}
