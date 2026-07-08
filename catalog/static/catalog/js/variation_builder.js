/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Variation Builder - Interactive Functionality
 * Provides live preview, SKU generation, and combination counting
 */

(function() {
    'use strict';

    // State management
    const state = {
        selectedAttributes: {},
        skuPattern: '',
        priceStrategy: 'none',
        priceAmount: 0,
        productSku: '',
        attributeData: {}
    };

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeVariationBuilder();
    });

    function initializeVariationBuilder() {
        // Cache DOM elements
        const form = document.getElementById('variation-form');
        if (!form) return; // Exit if not on variation builder page

        const skuInput = document.getElementById('sku_pattern');
        const generateBtn = document.getElementById('generate-btn');
        const checkboxes = document.querySelectorAll('.attr-checkbox');
        const priceStrategyInputs = document.querySelectorAll('input[name="price_strategy"]');
        const priceAmountInputs = document.querySelectorAll('input[name="price_amount"]');

        // Extract product SKU from pattern default
        if (skuInput) {
            state.skuPattern = skuInput.value;
            // Extract product SKU from the pattern (everything before first -)
            const match = state.skuPattern.match(/^([^-{]+)/);
            if (match) {
                state.productSku = match[1];
            }
        }

        // Build attribute data structure
        buildAttributeData();

        // Event Listeners
        if (checkboxes.length > 0) {
            checkboxes.forEach(checkbox => {
                checkbox.addEventListener('change', handleAttributeChange);
            });
        }

        if (skuInput) {
            skuInput.addEventListener('input', handleSkuPatternChange);
        }

        if (priceStrategyInputs.length > 0) {
            priceStrategyInputs.forEach(input => {
                input.addEventListener('change', handlePriceStrategyChange);
            });
        }

        if (priceAmountInputs.length > 0) {
            priceAmountInputs.forEach(input => {
                input.addEventListener('input', handlePriceAmountChange);
            });
        }

        // Select All / Deselect All buttons
        const selectAllBtns = document.querySelectorAll('.select-all-btn');
        const deselectAllBtns = document.querySelectorAll('.deselect-all-btn');

        selectAllBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const attrId = this.dataset.attrId;
                selectAllValues(attrId);
            });
        });

        deselectAllBtns.forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const attrId = this.dataset.attrId;
                deselectAllValues(attrId);
            });
        });

        // Form submission validation
        if (form) {
            form.addEventListener('submit', handleFormSubmit);
        }

        // Initial update
        updatePreview();
    }

    /**
     * Build attribute data structure from DOM
     */
    function buildAttributeData() {
        const checkboxes = document.querySelectorAll('.attr-checkbox');

        checkboxes.forEach(checkbox => {
            const attrId = checkbox.dataset.attrId;
            const attrName = checkbox.dataset.attrName;
            const valueName = checkbox.dataset.valueName;
            const valueId = checkbox.value;

            if (!state.attributeData[attrId]) {
                state.attributeData[attrId] = {
                    name: attrName,
                    values: {}
                };
            }

            state.attributeData[attrId].values[valueId] = valueName;
        });
    }

    /**
     * Handle attribute checkbox change
     */
    function handleAttributeChange(e) {
        const checkbox = e.target;
        const attrId = checkbox.dataset.attrId;
        const valueId = checkbox.value;

        if (!state.selectedAttributes[attrId]) {
            state.selectedAttributes[attrId] = [];
        }

        if (checkbox.checked) {
            if (!state.selectedAttributes[attrId].includes(valueId)) {
                state.selectedAttributes[attrId].push(valueId);
            }
        } else {
            state.selectedAttributes[attrId] = state.selectedAttributes[attrId].filter(id => id !== valueId);
            if (state.selectedAttributes[attrId].length === 0) {
                delete state.selectedAttributes[attrId];
            }
        }

        updatePreview();
    }

    /**
     * Handle SKU pattern input change
     */
    function handleSkuPatternChange(e) {
        state.skuPattern = e.target.value;
        updatePreview();
    }

    /**
     * Handle price strategy change
     */
    function handlePriceStrategyChange(e) {
        state.priceStrategy = e.target.value;
        updatePreview();
    }

    /**
     * Handle price amount change
     */
    function handlePriceAmountChange(e) {
        state.priceAmount = parseFloat(e.target.value) || 0;
        updatePreview();
    }

    /**
     * Select all values for an attribute
     */
    function selectAllValues(attrId) {
        const checkboxes = document.querySelectorAll(`.attr-checkbox[data-attr-id="${attrId}"]`);
        checkboxes.forEach(checkbox => {
            if (!checkbox.checked) {
                checkbox.checked = true;
                checkbox.dispatchEvent(new Event('change'));
            }
        });
    }

    /**
     * Deselect all values for an attribute
     */
    function deselectAllValues(attrId) {
        const checkboxes = document.querySelectorAll(`.attr-checkbox[data-attr-id="${attrId}"]`);
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                checkbox.checked = false;
                checkbox.dispatchEvent(new Event('change'));
            }
        });
    }

    /**
     * Generate all combinations from selected attributes
     */
    function generateCombinations() {
        const attributeIds = Object.keys(state.selectedAttributes);

        if (attributeIds.length === 0) {
            return [];
        }

        // Get all value arrays
        const valueArrays = attributeIds.map(attrId => {
            return state.selectedAttributes[attrId].map(valueId => ({
                attrId: attrId,
                attrName: state.attributeData[attrId].name,
                valueId: valueId,
                valueName: state.attributeData[attrId].values[valueId]
            }));
        });

        // Generate cartesian product
        return cartesianProduct(valueArrays);
    }

    /**
     * Cartesian product of arrays
     */
    function cartesianProduct(arrays) {
        if (arrays.length === 0) return [];
        if (arrays.length === 1) return arrays[0].map(item => [item]);

        const result = [];
        const restProduct = cartesianProduct(arrays.slice(1));

        for (let i = 0; i < arrays[0].length; i++) {
            for (let j = 0; j < restProduct.length; j++) {
                result.push([arrays[0][i]].concat(restProduct[j]));
            }
        }

        return result;
    }

    /**
     * Generate SKU from pattern for a combination
     */
    function generateSkuForCombination(combination) {
        let sku = state.skuPattern;

        // Replace {product_sku} or {sku}
        sku = sku.replace(/\{product_sku\}/gi, state.productSku);
        sku = sku.replace(/\{sku\}/gi, state.productSku);

        // Replace attribute placeholders
        combination.forEach(attr => {
            const placeholder = `{${attr.attrName}}`;
            const regex = new RegExp(placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
            sku = sku.replace(regex, attr.valueName.toUpperCase());
        });

        return sku;
    }

    /**
     * Get attribute display string for combination
     */
    function getAttributeString(combination) {
        return combination.map(attr => {
            return `${attr.attrName}: ${attr.valueName}`;
        }).join(' • ');
    }

    /**
     * Update all preview sections
     */
    function updatePreview() {
        const combinations = generateCombinations();
        const totalCount = combinations.length;

        // Update total combinations count
        const countElement = document.getElementById('total-combinations');
        if (countElement) {
            countElement.textContent = totalCount;
        }

        // Update SKU preview
        updateSkuPreview(combinations);

        // Update combinations preview
        updateCombinationsPreview(combinations);

        // Enable/disable generate button
        const generateBtn = document.getElementById('generate-btn');
        if (generateBtn) {
            generateBtn.disabled = totalCount === 0;
        }
    }

    /**
     * Update SKU preview section
     */
    function updateSkuPreview(combinations) {
        const previewOutput = document.getElementById('sku-preview-output');
        if (!previewOutput) return;

        if (combinations.length === 0) {
            previewOutput.textContent = 'Select attribute values to see SKU preview';
            previewOutput.classList.remove('populated');
            return;
        }

        // Show first 3 SKU examples
        const examples = combinations.slice(0, 3).map(combination => {
            return generateSkuForCombination(combination);
        });

        let html = examples.join('<br>');
        if (combinations.length > 3) {
            html += `<br><em>... and ${combinations.length - 3} more</em>`;
        }

        previewOutput.innerHTML = html;
        previewOutput.classList.add('populated');
    }

    /**
     * Update combinations preview list
     */
    function updateCombinationsPreview(combinations) {
        const previewContainer = document.getElementById('combinations-preview');
        if (!previewContainer) return;

        if (combinations.length === 0) {
            previewContainer.innerHTML = 'Select attribute values to preview combinations';
            return;
        }

        // Limit preview to first 50 combinations for performance
        const displayLimit = 50;
        const displayCombinations = combinations.slice(0, displayLimit);

        let html = '';
        displayCombinations.forEach(combination => {
            const sku = generateSkuForCombination(combination);
            const attrs = getAttributeString(combination);

            html += `
                <div class="combination-item">
                    <div class="combination-sku">${escapeHtml(sku)}</div>
                    <div class="combination-attrs">${escapeHtml(attrs)}</div>
                </div>
            `;
        });

        if (combinations.length > displayLimit) {
            html += `
                <div class="combination-item" style="text-align: center; border-left-color: #999;">
                    <em>... and ${combinations.length - displayLimit} more combinations</em>
                </div>
            `;
        }

        previewContainer.innerHTML = html;
    }

    /**
     * Handle form submission validation
     */
    async function handleFormSubmit(e) {
        e.preventDefault();
        const combinations = generateCombinations();

        if (combinations.length === 0) {
            AdminModal.alert({message: 'Please select at least one value for each attribute to generate variations.', type: 'warning'});
            return false;
        }

        // Check SKU pattern
        if (!state.skuPattern.trim()) {
            AdminModal.alert({message: 'Please provide a SKU pattern.', type: 'warning'});
            return false;
        }

        // Validate price amount for strategies that require it
        if (['fixed_add', 'fixed_subtract', 'percentage_add'].includes(state.priceStrategy)) {
            if (!state.priceAmount || state.priceAmount <= 0) {
                AdminModal.alert({message: 'Please enter a valid price amount for the selected pricing strategy.', type: 'warning'});
                return false;
            }
        }

        // Confirm large batch generation
        if (combinations.length > 100) {
            const confirmed = await AdminModal.confirm(
                `You are about to generate ${combinations.length} variations. This may take a few moments. Continue?`
            );
            if (!confirmed) {
                return false;
            }
        }

        e.target.submit();
        return true;
    }

    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

})();
