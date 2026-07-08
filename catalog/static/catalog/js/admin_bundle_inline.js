/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin Bundle Inline JavaScript
 * Handles dynamic filtering of variants, price updates, and card UI updates
 */

(function($) {
    'use strict';

    // Get language from HTML for URL building
    const LANG = document.documentElement.lang || 'en';

    /**
     * Get the custom autocomplete URL for component products (excludes bundles)
     */
    function getComponentAutocompleteUrl() {
        const container = $('.bundle-inline-group');
        return container.data('component-autocomplete-url') || null;
    }

    /**
     * Build the variants URL for a product
     */
    function buildVariantsUrl(productId) {
        return `/${LANG}/admin/catalog/product/${productId}/variants/`;
    }

    /**
     * Get card element from any child element
     */
    function getCard(element) {
        return $(element).closest('.bundle-item-card');
    }

    /**
     * Get the variant select for a card
     */
    function getVariantSelect(card) {
        return card.find('select[name$="-component_variant"]');
    }

    /**
     * Get the "allow variant selection" checkbox for a card
     */
    function getCustomerSelectsCheckbox(card) {
        return card.find('input[name$="-allow_variant_selection"]');
    }

    /**
     * Get the variant wrapper element
     */
    function getVariantWrapper(card) {
        return card.find('[data-variant-wrapper]');
    }

    /**
     * Update variant section visibility based on "customer selects" checkbox
     */
    function updateVariantVisibility(card) {
        const checkbox = getCustomerSelectsCheckbox(card);
        const variantWrapper = getVariantWrapper(card);
        const variantSelect = getVariantSelect(card);
        const productInfo = card.data('productInfo');

        if (!variantWrapper.length) return;

        const customerChooses = checkbox.prop('checked');

        if (customerChooses) {
            // Customer chooses - hide dropdown, show message
            variantWrapper.addClass('customer-chooses');
            variantSelect.val('').prop('disabled', true);
        } else {
            // Merchant pre-selects - show dropdown
            variantWrapper.removeClass('customer-chooses');
            // Only enable if product is variable and has variants
            if (productInfo && productInfo.product_type === 'variable' && productInfo.variants && productInfo.variants.length > 0) {
                variantSelect.prop('disabled', false);
            }
        }
    }

    /**
     * Update "customer selects" checkbox visibility based on product type
     * Only show for variable products
     */
    function updateCustomerSelectsVisibility(card, productInfo) {
        const checkbox = getCustomerSelectsCheckbox(card);

        if (productInfo && productInfo.product_type === 'variable') {
            // Add class to card - CSS rules show variant fields
            card.addClass('product-variable');
        } else {
            // Remove class - CSS rules hide variant fields
            card.removeClass('product-variable');
            checkbox.prop('checked', false);
        }

        updateVariantVisibility(card);
    }

    /**
     * Get the product select/input for a card (handles select2)
     */
    function getProductInput(card) {
        // Select2 creates a hidden input with the actual value
        return card.find('select[name$="-component_product"], input[name$="-component_product"]').first();
    }

    /**
     * Get the product ID from a card
     */
    function getProductId(card) {
        const input = getProductInput(card);
        return input.val() || null;
    }

    /**
     * Clear and reset variant select
     */
    function clearVariantSelect(variantSelect, message) {
        const emptyText = message || '---------';
        variantSelect.empty();
        variantSelect.append($('<option>', {
            value: '',
            text: emptyText
        }));
        variantSelect.prop('disabled', !message ? false : message !== '---------');
    }

    /**
     * Populate variant select with options
     */
    function populateVariantSelect(variantSelect, variants, currentValue) {
        variantSelect.empty();
        variantSelect.append($('<option>', {
            value: '',
            text: '---------'
        }));

        variants.forEach(function(variant) {
            const option = $('<option>', {
                value: variant.id,
                text: variant.display
            });
            if (currentValue && String(variant.id) === String(currentValue)) {
                option.prop('selected', true);
            }
            variantSelect.append(option);
        });

        variantSelect.prop('disabled', false);
    }

    /**
     * Update card UI with product info
     */
    function updateCardUI(card, productInfo) {
        // Update thumbnail
        const thumbnailContainer = card.find('.bundle-item-thumbnail');
        if (productInfo && productInfo.thumbnail) {
            thumbnailContainer.html(
                `<img src="${productInfo.thumbnail}" alt="${productInfo.name}" class="bundle-product-image">`
            );
        } else {
            thumbnailContainer.html(
                '<div class="bundle-product-placeholder"><i class="fas fa-box"></i></div>'
            );
        }

        // Update product name display
        const nameContainer = card.find('.bundle-item-product-name');
        if (productInfo) {
            nameContainer.html(`
                <span class="product-name-text">${productInfo.name}</span>
                <span class="product-sku-text">${productInfo.sku || ''}</span>
            `);
        } else {
            nameContainer.html(
                '<span class="product-name-text placeholder">Select a product...</span>'
            );
        }

        // Update unit price
        const unitPriceEl = card.find('[data-field="unit-price"]');
        if (productInfo && productInfo.price) {
            unitPriceEl.text(productInfo.price);
        } else {
            unitPriceEl.text('-');
        }

        // Calculate and update line total
        updateLineTotal(card, productInfo);

        // Update "customer selects" checkbox visibility based on product type
        updateCustomerSelectsVisibility(card, productInfo);
    }

    /**
     * Update line total based on quantity and unit price
     */
    function updateLineTotal(card, productInfo) {
        const lineTotalEl = card.find('[data-field="line-total"]');
        const quantityInput = card.find('input[name$="-quantity"]');
        const quantity = parseInt(quantityInput.val()) || 1;

        if (productInfo && productInfo.price_amount) {
            const total = (productInfo.price_amount * quantity).toFixed(2);
            const currency = productInfo.currency || window.__shopCurrency || 'USD';
            // Format with currency symbol (simplified)
            lineTotalEl.text(`${currency} ${total}`);
        } else {
            lineTotalEl.text('-');
        }
    }

    /**
     * Fetch product info and variants, then update UI
     */
    function fetchProductAndUpdateCard(card, preserveVariant) {
        const productId = getProductId(card);
        const variantSelect = getVariantSelect(card);
        const currentVariant = preserveVariant ? variantSelect.val() : null;

        if (!productId) {
            clearVariantSelect(variantSelect, '---------');
            updateCardUI(card, null);
            updateBundleSummary();
            return;
        }

        card.addClass('loading');

        $.ajax({
            url: buildVariantsUrl(productId),
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                card.removeClass('loading');

                if (data.success) {
                    // Update card with product info
                    updateCardUI(card, data.product);

                    // Store product info on card for line total calculations
                    // Include variants for price lookup when variant is selected
                    const productInfoWithVariants = {
                        ...data.product,
                        variants: data.variants || []
                    };
                    card.data('productInfo', productInfoWithVariants);

                    // Update variants dropdown
                    if (data.has_variants && data.variants.length > 0) {
                        populateVariantSelect(variantSelect, data.variants, currentVariant);
                    } else {
                        const message = data.product.product_type !== 'variable'
                            ? '(Not a variable product)'
                            : '(No variants available)';
                        clearVariantSelect(variantSelect, message);
                    }

                    updateBundleSummary();
                } else {
                    console.error('Failed to fetch product info:', data.error);
                    clearVariantSelect(variantSelect, '---------');
                    updateCardUI(card, null);
                }
            },
            error: function(xhr, status, error) {
                card.removeClass('loading');
                console.error('Error fetching product info:', error);
                clearVariantSelect(variantSelect, '---------');
                updateCardUI(card, null);
            }
        });
    }

    /**
     * Update bundle summary (total items and value)
     */
    function updateBundleSummary() {
        const container = $('.bundle-items-container');
        let totalItems = 0;
        let totalValue = 0;
        let currency = window.__shopCurrency || 'USD';

        container.find('.bundle-item-card:not(.empty-form)').each(function() {
            const card = $(this);
            const deleteCheckbox = card.find('input[type="checkbox"][name$="-DELETE"]');

            // Skip deleted items
            if (deleteCheckbox.length && deleteCheckbox.prop('checked')) {
                return;
            }

            const productId = getProductId(card);
            if (!productId) {
                return;
            }

            const productInfo = card.data('productInfo');
            const quantity = parseInt(card.find('input[name$="-quantity"]').val()) || 1;

            totalItems += quantity;

            if (productInfo && productInfo.price_amount) {
                totalValue += productInfo.price_amount * quantity;
                currency = productInfo.currency || currency;
            }
        });

        $('#bundle-total-items').text(totalItems);
        $('#bundle-total-value').text(totalValue > 0 ? `${currency} ${totalValue.toFixed(2)}` : '-');
    }

    /**
     * Handle variant change - update line total with variant price
     */
    function handleVariantChange(card) {
        const variantSelect = getVariantSelect(card);
        const variantId = variantSelect.val();
        const productInfo = card.data('productInfo');

        if (!productInfo) return;

        // Find variant price if selected
        let priceToUse = productInfo;

        if (variantId && productInfo.variants) {
            const variant = productInfo.variants.find(v => String(v.id) === String(variantId));
            if (variant && variant.price_amount) {
                priceToUse = {
                    ...productInfo,
                    price: variant.price,
                    price_amount: variant.price_amount
                };
            }
        }

        // Update unit price display
        const unitPriceEl = card.find('[data-field="unit-price"]');
        unitPriceEl.text(priceToUse.price || '-');

        updateLineTotal(card, priceToUse);
        updateBundleSummary();
    }

    /**
     * Initialize a single bundle item card
     */
    function initCard(card) {
        if (card.data('bundle-initialized')) {
            return;
        }
        card.data('bundle-initialized', true);

        const productInput = getProductInput(card);
        const variantSelect = getVariantSelect(card);
        const quantityInput = card.find('input[name$="-quantity"]');
        const removeBtn = card.find('.bundle-item-remove');
        const customerSelectsCheckbox = getCustomerSelectsCheckbox(card);

        // Check if this card already has a product selected (existing record)
        const productId = getProductId(card);
        if (productId) {
            // Fetch product info to populate the card
            fetchProductAndUpdateCard(card, true);
        } else {
            // No product selected - hide variant options until a product is chosen
            updateCustomerSelectsVisibility(card, null);
        }

        // Listen for select2 changes on product field
        // Select2 triggers 'change' event when selection changes
        productInput.on('change.bundleInline', function() {
            fetchProductAndUpdateCard(card, false);
        });

        // Also try to bind to select2:select for more reliable detection
        productInput.on('select2:select select2:clear', function() {
            fetchProductAndUpdateCard(card, false);
        });

        // Listen for "customer selects variant" checkbox changes
        customerSelectsCheckbox.on('change.bundleInline', function() {
            updateVariantVisibility(card);
        });

        // Listen for variant changes
        variantSelect.on('change.bundleInline', function() {
            handleVariantChange(card);
        });

        // Listen for quantity changes
        quantityInput.on('change.bundleInline input.bundleInline', function() {
            const productInfo = card.data('productInfo');
            if (productInfo) {
                updateLineTotal(card, productInfo);
                updateBundleSummary();
            }
        });

        // Handle remove button
        removeBtn.on('click.bundleInline', function(e) {
            e.preventDefault();
            const deleteCheckbox = card.find('input[type="checkbox"][name$="-DELETE"]');

            // Animate out then hide
            card.css({
                overflow: 'hidden',
                transition: 'opacity 0.2s ease, max-height 0.3s ease, margin 0.3s ease, padding 0.3s ease'
            });
            card.css({ opacity: 0, maxHeight: card.outerHeight() + 'px' });

            setTimeout(function() {
                card.css({ maxHeight: 0, margin: 0, padding: 0, border: 'none' });
            }, 50);

            setTimeout(function() {
                if (deleteCheckbox.length) {
                    // Existing item - mark for deletion (Django needs this on save)
                    deleteCheckbox.prop('checked', true);
                    card.addClass('marked-for-delete');
                } else {
                    // New item - remove from DOM
                    card.remove();
                }
                updateBundleSummary();
            }, 350);
        });

        // Initialize variant visibility state based on current checkbox value
        updateVariantVisibility(card);
    }

    /**
     * Initialize all existing cards
     */
    function initAllCards() {
        $('.bundle-item-card:not(.empty-form)').each(function() {
            initCard($(this));
        });

        updateBundleSummary();
    }

    /**
     * Handle adding new rows
     */
    function setupAddButton() {
        const container = $('.bundle-inline-group');
        const addBtn = container.find('.bundle-add-btn');
        const emptyForm = container.find('.bundle-item-card.empty-form');
        const formsetPrefix = container.attr('id').replace('-group', '');

        if (!addBtn.length || !emptyForm.length) {
            return;
        }

        addBtn.on('click', function(e) {
            e.preventDefault();

            // Get current form count
            const totalForms = $(`#id_${formsetPrefix}-TOTAL_FORMS`);
            const formCount = parseInt(totalForms.val());

            // Clone empty form WITHOUT events to avoid select2 issues
            const newForm = emptyForm.clone(false);
            newForm.removeClass('empty-form last-related');
            newForm.attr('id', `${formsetPrefix}-${formCount}`);
            newForm.attr('data-index', formCount);

            // Remove any cloned select2 containers (they'll be reinitialized)
            newForm.find('.select2-container').remove();

            // Update form field names and IDs
            newForm.find('input, select, textarea').each(function() {
                const el = $(this);
                const name = el.attr('name');
                const id = el.attr('id');

                if (name) {
                    el.attr('name', name.replace(/__prefix__/g, formCount));
                }
                if (id) {
                    el.attr('id', id.replace(/__prefix__/g, formCount));
                }

                // Clean up select2 state from cloned selects
                el.removeClass('select2-hidden-accessible');
                el.removeAttr('data-select2-id');
                el.removeAttr('aria-hidden');
                el.removeAttr('tabindex');
            });

            // Update labels
            newForm.find('label').each(function() {
                const el = $(this);
                const forAttr = el.attr('for');
                if (forAttr) {
                    el.attr('for', forAttr.replace(/__prefix__/g, formCount));
                }
            });

            // Update any other elements with __prefix__ in data attributes
            newForm.find('[data-select2-id]').removeAttr('data-select2-id');

            // Insert before the empty form
            newForm.insertBefore(emptyForm);

            // Update total forms count
            totalForms.val(formCount + 1);

            // Show the new form
            newForm.show();

            // Initialize Django admin's autocomplete (select2) on the new form
            // Use our custom autocomplete URL that filters out bundle products
            const productSelect = newForm.find('select[name$="-component_product"]');
            if (productSelect.length && $.fn.select2 && window.django && window.django.jQuery) {
                // Use custom autocomplete URL that excludes bundles
                const autocompleteUrl = getComponentAutocompleteUrl() || productSelect.data('ajax--url');
                if (autocompleteUrl) {
                    // Initialize with Django admin's autocomplete configuration
                    productSelect.select2({
                        ajax: {
                            url: autocompleteUrl,
                            dataType: 'json',
                            delay: 250,
                            data: function(params) {
                                return {
                                    term: params.term,
                                    page: params.page
                                };
                            },
                            processResults: function(data) {
                                return {
                                    results: data.results,
                                    pagination: data.pagination
                                };
                            },
                            cache: true
                        },
                        allowClear: productSelect.data('allow-clear') !== false,
                        placeholder: '',
                        minimumInputLength: 0,
                        theme: 'admin-autocomplete'
                    });
                }
            }

            // Initialize the card
            initCard(newForm);

            // Trigger Django's formset:added event for other handlers
            $(document).trigger('formset:added', [newForm[0], formsetPrefix]);

            updateBundleSummary();
        });
    }

    /**
     * Watch for dynamically added rows (e.g., from Django's default add mechanism)
     */
    function watchForNewRows() {
        $(document).on('formset:added', function(event, row, prefix) {
            if (prefix && prefix.indexOf('bundleitem') !== -1) {
                const card = $(row);
                if (card.hasClass('bundle-item-card')) {
                    setTimeout(function() {
                        initCard(card);
                    }, 100);
                }
            }
        });
    }

    /**
     * Initialize on DOM ready
     */
    function init() {
        $(document).ready(function() {
            // Small delay to ensure select2 is initialized by Django admin
            setTimeout(function() {
                initAllCards();
                setupAddButton();
                watchForNewRows();
            }, 300);
        });
    }

    // Start initialization
    init();

})(django.jQuery || jQuery);
