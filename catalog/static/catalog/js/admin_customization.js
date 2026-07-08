/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Django Admin Customization Option JavaScript
 * Provides dynamic UI enhancements for managing product customization options
 */

(function($) {
    'use strict';

    /**
     * CustomizationOptionManager - Handles customization option UI logic
     */
    class CustomizationOptionManager {
        constructor() {
            this.init();
        }

        init() {
            $(document).ready(() => {
                this.setupFieldVisibility();
                this.setupChoicesHelper();
                this.setupPricingHelper();
                this.observeDynamicForms();
            });
        }

        /**
         * Show/hide fields based on option_type selection
         */
        setupFieldVisibility() {
            const updateFieldVisibility = ($row) => {
                const optionType = $row.find('select[name*="option_type"]').val();

                // Hide all conditional fields first
                $row.find('.field-max_length').hide();
                $row.find('.field-allowed_file_types').hide();
                $row.find('.field-max_file_size_mb').hide();
                $row.find('.field-min_value').hide();
                $row.find('.field-max_value').hide();

                // Show relevant fields based on option type
                switch(optionType) {
                    case 'text':
                    case 'textarea':
                        $row.find('.field-max_length').show();
                        break;
                    case 'file':
                        $row.find('.field-allowed_file_types').show();
                        $row.find('.field-max_file_size_mb').show();
                        break;
                    case 'number':
                        $row.find('.field-min_value').show();
                        $row.find('.field-max_value').show();
                        break;
                    case 'select':
                    case 'color':
                        // Choices are always visible for these types
                        break;
                }
            };

            // Apply to existing rows
            $('.inline-related:has([name*="option_type"])').each(function() {
                updateFieldVisibility($(this));
            });

            // Apply to new rows (dynamically added)
            $(document).on('change', 'select[name*="option_type"]', function() {
                updateFieldVisibility($(this).closest('.inline-related'));
            });

            // Also trigger on formset:added for Django's inline formsets
            $(document).on('formset:added', function(event, $row, formsetName) {
                if (formsetName === 'customizationoption_set') {
                    updateFieldVisibility($row);
                }
            });
        }

        /**
         * Add JSON formatting helper for choices field
         */
        setupChoicesHelper() {
            $('textarea[name*="choices"]').each(function() {
                const $textarea = $(this);
                const $fieldBox = $textarea.closest('.form-row, .field-choices');

                // Don't add helper if it already exists
                if ($fieldBox.find('.choices-helper').length > 0) {
                    return;
                }

                const helper = $('<div class="choices-helper"></div>').css({
                    'margin-top': '10px',
                    'padding': '12px',
                    'background': '#f0f8ff',
                    'border-left': '3px solid #0066cc',
                    'border-radius': '4px',
                    'font-size': '12px'
                });

                const exampleHtml = `
                    <strong>Choices Format (JSON):</strong>
                    <pre style="background: #fff; padding: 10px; border-radius: 3px; margin-top: 8px; overflow-x: auto;">[
  {
    "value": "oak",
    "label": "Oak Wood",
    "price_modifier": 0
  },
  {
    "value": "walnut",
    "label": "Walnut Wood",
    "price_modifier": 25.00
  }
]</pre>
                    <div style="margin-top: 8px; color: #666;">
                        <strong>Tips:</strong>
                        <ul style="margin: 4px 0 0 20px; padding: 0;">
                            <li><code>value</code>: Internal identifier (required)</li>
                            <li><code>label</code>: Display name (required)</li>
                            <li><code>price_modifier</code>: Additional cost (optional, default: 0)</li>
                            <li><code>color</code>: Hex color for color picker type (optional)</li>
                        </ul>
                    </div>
                `;

                helper.html(exampleHtml);
                $fieldBox.append(helper);

                // Add format validation button
                const formatBtn = $('<button type="button" class="button">Format JSON</button>').css({
                    'margin-top': '8px'
                });

                formatBtn.on('click', () => {
                    try {
                        const json = JSON.parse($textarea.val() || '[]');
                        $textarea.val(JSON.stringify(json, null, 2));
                        this.showMessage('JSON formatted successfully!', 'success');
                    } catch (e) {
                        this.showMessage('Invalid JSON: ' + e.message, 'error');
                    }
                });

                $fieldBox.append(formatBtn);
            });
        }

        /**
         * Add pricing helper tooltips
         */
        setupPricingHelper() {
            $('select[name*="pricing_type"]').each(function() {
                const $select = $(this);
                const $fieldBox = $select.closest('.form-row, .field-pricing_type');

                // Don't add helper if it already exists
                if ($fieldBox.find('.pricing-helper').length > 0) {
                    return;
                }

                const updateHelper = () => {
                    const pricingType = $select.val();
                    let helperText = '';

                    switch(pricingType) {
                        case 'free':
                            helperText = 'No additional charge for this customization';
                            break;
                        case 'fixed':
                            helperText = 'Fixed fee added to product price';
                            break;
                        case 'percentage':
                            helperText = 'Percentage of product base price (e.g., 10 = 10%)';
                            break;
                        case 'per_unit':
                            helperText = 'Price per character (text) or per unit (number)';
                            break;
                    }

                    $fieldBox.find('.pricing-helper').remove();

                    if (helperText) {
                        const helper = $('<div class="pricing-helper"></div>').css({
                            'margin-top': '6px',
                            'padding': '8px 12px',
                            'background': '#fff3e0',
                            'border-left': '3px solid #ff9800',
                            'border-radius': '3px',
                            'font-size': '12px',
                            'color': '#666'
                        }).text(helperText);

                        $fieldBox.append(helper);
                    }
                };

                updateHelper();
                $select.on('change', updateHelper);
            });
        }

        /**
         * Observe for dynamically added forms (Django inline formsets)
         */
        observeDynamicForms() {
            // Watch for new inline forms being added
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === 1 && $(node).hasClass('inline-related')) {
                            this.setupFieldVisibility();
                            this.setupChoicesHelper();
                            this.setupPricingHelper();
                        }
                    });
                });
            });

            // Start observing
            const inlineGroups = document.querySelectorAll('.inline-group');
            inlineGroups.forEach((group) => {
                observer.observe(group, {
                    childList: true,
                    subtree: true
                });
            });
        }

        /**
         * Show temporary message to user
         */
        showMessage(message, type = 'info') {
            const $message = $('<div class="custom-message"></div>').css({
                'position': 'fixed',
                'top': '100px',
                'right': '20px',
                'padding': '12px 20px',
                'background': type === 'success' ? '#28a745' : '#dc3545',
                'color': 'white',
                'border-radius': '4px',
                'box-shadow': '0 2px 8px rgba(0,0,0,0.2)',
                'z-index': '10000',
                'animation': 'slideInRight 0.3s ease'
            }).text(message);

            $('body').append($message);

            setTimeout(() => {
                $message.fadeOut(300, function() {
                    $(this).remove();
                });
            }, 3000);
        }
    }

    /**
     * Initialize when DOM is ready
     */
    if (typeof django !== 'undefined' && django.jQuery) {
        new CustomizationOptionManager();
    }

})(django.jQuery || jQuery);
