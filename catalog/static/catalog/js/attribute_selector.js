/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Attribute Selector Widget
 * Handles variant selection based on product attributes
 * Supports text, color swatches, images, and button display types
 */

(function() {
    'use strict';

    class AttributeSelector {
        constructor(widgetElement, options = {}) {
            this.widget = widgetElement;
            this.options = {
                onVariantChange: options.onVariantChange || null,
                onAttributeChange: options.onAttributeChange || null,
                autoSelectSingle: options.autoSelectSingle !== false, // Default true
                ...options
            };

            // Parse variants data from dataset or options
            this.variants = options.variants || [];
            this.productId = this.widget.dataset.productId;
            this.productType = this.widget.dataset.productType;

            // State
            this.selectedAttributes = {}; // { attributeId: valueId }
            this.selectedVariant = null;

            // DOM elements
            this.attributeGroups = this.widget.querySelectorAll('.attribute-group');
            this.hiddenInput = this.widget.querySelector('#selected-variant-id');
            this.availabilityMessage = this.widget.querySelector('.availability-message');
            this.variantInfo = this.widget.querySelector('.selected-variant-info');

            this.init();
        }

        init() {
            // Bind event listeners
            this.bindEvents();

            // Auto-select if only one option available
            if (this.options.autoSelectSingle) {
                this.autoSelectSingleOptions();
            }

            // Initialize availability states
            this.updateAvailability();
        }

        bindEvents() {
            // Handle attribute option clicks
            this.widget.addEventListener('click', (e) => {
                const option = e.target.closest('.attribute-option');
                if (option) {
                    e.preventDefault();
                    this.handleAttributeClick(option);
                }
            });
        }

        handleAttributeClick(option) {
            const group = option.closest('.attribute-group');
            const attributeId = group.dataset.attributeId;
            const attributeSlug = group.dataset.attributeSlug;
            const valueId = option.dataset.valueId;
            const valueName = option.dataset.valueName;

            // Check if option is disabled
            if (option.disabled || option.classList.contains('disabled')) {
                return;
            }

            // Toggle selection
            if (this.selectedAttributes[attributeId] === valueId) {
                // Deselect
                delete this.selectedAttributes[attributeId];
                this.updateOptionState(group, null);
            } else {
                // Select
                this.selectedAttributes[attributeId] = valueId;
                this.updateOptionState(group, option);
            }

            // Update selected value label
            this.updateSelectedLabel(group, valueName);

            // Find matching variant
            this.findMatchingVariant();

            // Update availability of other options
            this.updateAvailability();

            // Callback
            if (this.options.onAttributeChange) {
                this.options.onAttributeChange({
                    attributeId,
                    attributeSlug,
                    valueId,
                    valueName,
                    selectedAttributes: this.selectedAttributes
                });
            }
        }

        updateOptionState(group, selectedOption) {
            const options = group.querySelectorAll('.attribute-option');

            options.forEach(option => {
                option.classList.remove('selected', 'bg-blue-50', 'border-blue-500');

                if (option === selectedOption) {
                    option.classList.add('selected', 'border-blue-500');

                    // Show checkmark for color/image types
                    const checkmark = option.querySelector('.color-checkmark, .image-checkmark');
                    if (checkmark) {
                        checkmark.classList.remove('hidden');
                    }

                    // Highlight button types
                    if (option.classList.contains('attribute-option-button') ||
                        option.classList.contains('attribute-option-text')) {
                        option.classList.add('bg-blue-50', 'text-blue-600');
                    }
                } else {
                    // Hide checkmark
                    const checkmark = option.querySelector('.color-checkmark, .image-checkmark');
                    if (checkmark) {
                        checkmark.classList.add('hidden');
                    }

                    // Remove highlight
                    option.classList.remove('bg-blue-50', 'text-blue-600');
                }
            });
        }

        updateSelectedLabel(group, valueName) {
            const label = group.querySelector('.selected-value');
            if (label) {
                if (valueName) {
                    label.textContent = `(${valueName})`;
                    label.classList.remove('hidden');
                } else {
                    label.textContent = '';
                    label.classList.add('hidden');
                }
            }
        }

        findMatchingVariant() {
            if (!this.variants || this.variants.length === 0) {
                return;
            }

            // Get selected attribute value IDs
            const selectedValueIds = Object.values(this.selectedAttributes);

            // Find variant that matches ALL selected attributes
            const matchingVariant = this.variants.find(variant => {
                if (!variant.attributes_structured) return false;

                const variantValueIds = variant.attributes_structured.map(attr => attr.id.toString());

                // Check if all selected attributes match this variant
                return selectedValueIds.every(valueId =>
                    variantValueIds.includes(valueId.toString())
                );
            });

            if (matchingVariant) {
                this.selectVariant(matchingVariant);
            } else {
                this.clearVariantSelection();
            }
        }

        selectVariant(variant) {
            this.selectedVariant = variant;

            // Update hidden input
            if (this.hiddenInput) {
                this.hiddenInput.value = variant.id;
            }

            // Update variant info display
            this.displayVariantInfo(variant);

            // Clear any error messages
            this.clearMessages();

            // Callback
            if (this.options.onVariantChange) {
                this.options.onVariantChange(variant);
            }
        }

        clearVariantSelection() {
            this.selectedVariant = null;

            if (this.hiddenInput) {
                this.hiddenInput.value = '';
            }

            if (this.variantInfo) {
                this.variantInfo.classList.add('hidden');
            }

            // Show message if attributes are selected but no match found
            const selectedCount = Object.keys(this.selectedAttributes).length;
            if (selectedCount > 0) {
                this.showMessage('This combination is not available. Please try a different selection.', 'warning');
            } else {
                this.clearMessages();
            }
        }

        displayVariantInfo(variant) {
            if (!this.variantInfo) return;

            // Update variant details
            const nameEl = this.variantInfo.querySelector('.variant-name');
            const skuEl = this.variantInfo.querySelector('.variant-sku');
            const priceEl = this.variantInfo.querySelector('.variant-price');
            const stockEl = this.variantInfo.querySelector('.variant-stock');

            if (nameEl) nameEl.textContent = variant.name || 'Variant';
            if (skuEl) skuEl.textContent = `SKU: ${variant.sku || 'N/A'}`;

            if (priceEl && variant.effective_price) {
                const price = variant.effective_price;
                priceEl.textContent = `${price.currency} ${price.amount}`;
            }

            if (stockEl) {
                const stockQty = variant.stock_quantity || 0;
                if (stockQty > 0) {
                    stockEl.innerHTML = `<span class="text-green-600 dark:text-green-400">✓ In Stock (${stockQty} available)</span>`;
                } else {
                    stockEl.innerHTML = `<span class="text-red-600 dark:text-red-400">✗ Out of Stock</span>`;
                }
            }

            this.variantInfo.classList.remove('hidden');
        }

        updateAvailability() {
            // If no variants data, skip availability check
            if (!this.variants || this.variants.length === 0) return;

            // For each attribute group, check which options are available
            this.attributeGroups.forEach(group => {
                const attributeId = group.dataset.attributeId;
                const options = group.querySelectorAll('.attribute-option');

                options.forEach(option => {
                    const valueId = option.dataset.valueId;

                    // Build test selection with this value
                    const testSelection = { ...this.selectedAttributes, [attributeId]: valueId };
                    const testValueIds = Object.values(testSelection);

                    // Check if any variant matches this combination
                    const hasMatch = this.variants.some(variant => {
                        if (!variant.attributes_structured) return false;
                        const variantValueIds = variant.attributes_structured.map(attr => attr.id.toString());
                        return testValueIds.every(id => variantValueIds.includes(id.toString()));
                    });

                    // Disable/enable option based on availability
                    if (hasMatch) {
                        option.disabled = false;
                        option.classList.remove('disabled', 'opacity-50', 'cursor-not-allowed');
                    } else {
                        option.disabled = true;
                        option.classList.add('disabled', 'opacity-50', 'cursor-not-allowed');
                    }
                });
            });
        }

        autoSelectSingleOptions() {
            this.attributeGroups.forEach(group => {
                const options = group.querySelectorAll('.attribute-option:not(.disabled)');
                if (options.length === 1) {
                    // Auto-select the only available option
                    this.handleAttributeClick(options[0]);
                }
            });
        }

        validate() {
            const errors = [];
            const requiredCount = this.widget.querySelectorAll('.attribute-group').length;
            const selectedCount = Object.keys(this.selectedAttributes).length;

            // Check if all required attributes are selected
            this.attributeGroups.forEach(group => {
                const attributeName = group.querySelector('.attribute-label').textContent.trim();
                const isRequired = attributeName.includes('*');
                const attributeId = group.dataset.attributeId;

                if (isRequired && !this.selectedAttributes[attributeId]) {
                    errors.push(`Please select ${attributeName.replace('*', '').trim()}`);
                    this.showAttributeError(group, `Please select a value`);
                } else {
                    this.clearAttributeError(group);
                }
            });

            // Check if a valid variant is selected
            if (selectedCount > 0 && !this.selectedVariant) {
                errors.push('The selected combination is not available');
            }

            return {
                valid: errors.length === 0,
                errors: errors
            };
        }

        showAttributeError(group, message) {
            const errorEl = group.querySelector('.attribute-error');
            if (errorEl) {
                errorEl.textContent = message;
                errorEl.classList.remove('hidden');
            }
        }

        clearAttributeError(group) {
            const errorEl = group.querySelector('.attribute-error');
            if (errorEl) {
                errorEl.textContent = '';
                errorEl.classList.add('hidden');
            }
        }

        showMessage(message, type = 'info') {
            if (!this.availabilityMessage) return;

            const messageText = this.availabilityMessage.querySelector('.message-text');
            if (messageText) {
                messageText.textContent = message;
            }

            // Reset classes
            this.availabilityMessage.classList.remove(
                'hidden',
                'bg-blue-50', 'text-blue-800', 'border-blue-200',
                'bg-yellow-50', 'text-yellow-800', 'border-yellow-200',
                'bg-red-50', 'text-red-800', 'border-red-200',
                'bg-green-50', 'text-green-800', 'border-green-200'
            );

            // Add appropriate classes based on type
            const typeClasses = {
                'info': ['bg-blue-50', 'text-blue-800', 'border-blue-200'],
                'warning': ['bg-yellow-50', 'text-yellow-800', 'border-yellow-200'],
                'error': ['bg-red-50', 'text-red-800', 'border-red-200'],
                'success': ['bg-green-50', 'text-green-800', 'border-green-200']
            };

            this.availabilityMessage.classList.add(...(typeClasses[type] || typeClasses.info));
            this.availabilityMessage.classList.add('border');
        }

        clearMessages() {
            if (this.availabilityMessage) {
                this.availabilityMessage.classList.add('hidden');
            }
            this.attributeGroups.forEach(group => this.clearAttributeError(group));
        }

        // Public API
        getSelectedVariant() {
            return this.selectedVariant;
        }

        getSelectedAttributes() {
            return this.selectedAttributes;
        }

        reset() {
            this.selectedAttributes = {};
            this.selectedVariant = null;

            this.attributeGroups.forEach(group => {
                this.updateOptionState(group, null);
                this.updateSelectedLabel(group, null);
                this.clearAttributeError(group);
            });

            this.clearMessages();

            if (this.hiddenInput) {
                this.hiddenInput.value = '';
            }

            if (this.variantInfo) {
                this.variantInfo.classList.add('hidden');
            }
        }

        setVariants(variants) {
            this.variants = variants;
            this.updateAvailability();
        }
    }

    // Auto-initialize on page load
    document.addEventListener('DOMContentLoaded', function() {
        const widgets = document.querySelectorAll('.attribute-selector-widget');

        widgets.forEach(widgetEl => {
            // Check if variants data is embedded in the page
            const variantsData = widgetEl.dataset.variants;
            const variants = variantsData ? JSON.parse(variantsData) : [];

            // Initialize widget
            const selector = new AttributeSelector(widgetEl, {
                variants: variants,
                onVariantChange: function(variant) {
                    console.log('Variant selected:', variant);
                    // Trigger custom event for integration
                    widgetEl.dispatchEvent(new CustomEvent('variantChange', {
                        detail: { variant },
                        bubbles: true
                    }));
                },
                onAttributeChange: function(data) {
                    console.log('Attribute changed:', data);
                    // Trigger custom event for integration
                    widgetEl.dispatchEvent(new CustomEvent('attributeChange', {
                        detail: data,
                        bubbles: true
                    }));
                }
            });

            // Store instance on element for external access
            widgetEl.attributeSelector = selector;
        });
    });

    // Export for module systems
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = AttributeSelector;
    } else if (typeof define === 'function' && define.amd) {
        define([], function() { return AttributeSelector; });
    } else {
        window.AttributeSelector = AttributeSelector;
    }
})();
