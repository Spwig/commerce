/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Quick View Modal for Variable Products
 * Fetches product data from API, renders variant selectors,
 * and allows add-to-cart without leaving the listing page.
 *
 * Supports two modes:
 * 1. Attribute-based: variants have attributes_structured populated -> show attribute selectors
 * 2. Direct variant: variants have no attribute mappings -> show variants as selectable options
 */
(function() {
    'use strict';

    var cache = {};
    var currentProduct = null;
    var selectedAttributes = {};
    var selectedVariantId = null;

    var modal, backdrop, loading, body, closeBtn;
    var imgEl, thumbsEl, titleEl, priceCurrent, priceOriginal;
    var descEl, variantsEl, stockEl, addBtn, addBtnText, qtyInput, fullLink;

    function init() {
        modal = document.getElementById('product-quick-view');
        if (!modal) return;

        backdrop = modal.querySelector('.quick-view__backdrop');
        loading = modal.querySelector('.quick-view__loading');
        body = modal.querySelector('.quick-view__body');
        closeBtn = modal.querySelector('.quick-view__close');
        imgEl = modal.querySelector('.quick-view__image');
        thumbsEl = modal.querySelector('.quick-view__thumbs');
        titleEl = modal.querySelector('.quick-view__title');
        priceCurrent = modal.querySelector('.quick-view__price-current');
        priceOriginal = modal.querySelector('.quick-view__price-original');
        descEl = modal.querySelector('.quick-view__description');
        variantsEl = modal.querySelector('.quick-view__variants');
        stockEl = modal.querySelector('.quick-view__stock');
        addBtn = modal.querySelector('.quick-view__add-btn');
        addBtnText = modal.querySelector('.quick-view__add-btn-text');
        qtyInput = modal.querySelector('.quick-view__qty-input');
        fullLink = modal.querySelector('.quick-view__full-link');

        // Close handlers
        closeBtn.addEventListener('click', close);
        backdrop.addEventListener('click', close);
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modal.classList.contains('quick-view--visible')) {
                close();
            }
        });

        // Quantity buttons
        modal.querySelectorAll('.quick-view__qty-btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var action = btn.dataset.action;
                var val = parseInt(qtyInput.value, 10) || 1;
                if (action === 'increase') {
                    qtyInput.value = Math.min(val + 1, parseInt(qtyInput.max, 10) || 99);
                } else if (action === 'decrease') {
                    qtyInput.value = Math.max(val - 1, 1);
                }
            });
        });

        // Add to cart
        addBtn.addEventListener('click', handleAddToCart);
    }

    function open(slug) {
        if (!modal) init();
        if (!modal) return;

        selectedAttributes = {};
        selectedVariantId = null;
        currentProduct = null;
        qtyInput.value = 1;

        // Show modal with loading
        modal.classList.add('quick-view--visible');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        loading.style.display = 'flex';
        body.style.display = 'none';

        // Fetch or use cache
        if (cache[slug]) {
            render(cache[slug]);
        } else {
            fetch('/api/catalog/products/' + slug + '/')
                .then(function(r) {
                    if (!r.ok) throw new Error(r.status);
                    return r.json();
                })
                .then(function(data) {
                    cache[slug] = data;
                    render(data);
                })
                .catch(function() {
                    close();
                    if (typeof showNotification === 'function') {
                        showNotification('Failed to load product', 'error');
                    }
                });
        }
    }

    /** Get image URL from an image object (handles both relative and absolute) */
    function getImageUrl(imgObj) {
        return imgObj.image || imgObj.display_url || imgObj.url || '';
    }

    function render(data) {
        currentProduct = data;

        // Clear previous state
        variantsEl.innerHTML = '';
        thumbsEl.innerHTML = '';
        imgEl.src = '';
        imgEl.alt = '';

        // Title
        titleEl.textContent = data.name;

        // Price
        renderPrice(data.price_amount, data.price_currency, data.compare_at_price_amount);

        // Description
        if (data.short_description) {
            descEl.innerHTML = data.short_description;
            descEl.style.display = '';
        } else {
            descEl.style.display = 'none';
        }

        // Main image
        if (data.images && data.images.length > 0) {
            imgEl.src = getImageUrl(data.images[0]);
            imgEl.alt = data.name;
        }

        // Thumbnails
        renderThumbnails(data.images || []);

        // Determine rendering mode: attribute-based or direct variant
        var variants = data.variants || [];
        var hasAttributeMappings = variants.some(function(v) {
            return v.attributes_structured && v.attributes_structured.length > 0;
        });

        if (hasAttributeMappings) {
            renderAttributeSelectors(data.available_attributes || [], variants);
        } else if (variants.length > 0) {
            renderDirectVariants(variants);
        }

        // Stock
        stockEl.innerHTML = '';

        // Full details link
        var lang = document.documentElement.lang || 'en';
        fullLink.href = '/' + lang + '/product/' + data.slug + '/';

        // Button state
        updateButtonState();

        // Show content
        loading.style.display = 'none';
        body.style.display = '';
    }

    function renderPrice(amount, currency, compareAmount) {
        var symbol = getCurrencySymbol(currency);
        if (compareAmount && parseFloat(compareAmount) > parseFloat(amount)) {
            priceCurrent.textContent = symbol + parseFloat(amount).toFixed(2);
            priceCurrent.classList.add('quick-view__price-current--sale');
            priceOriginal.textContent = symbol + parseFloat(compareAmount).toFixed(2);
            priceOriginal.style.display = '';
        } else {
            priceCurrent.textContent = symbol + parseFloat(amount).toFixed(2);
            priceCurrent.classList.remove('quick-view__price-current--sale');
            priceOriginal.style.display = 'none';
        }
    }

    function renderThumbnails(images) {
        thumbsEl.innerHTML = '';
        if (images.length <= 1) return;

        images.forEach(function(img, idx) {
            var thumb = document.createElement('button');
            thumb.className = 'quick-view__thumb' + (idx === 0 ? ' quick-view__thumb--active' : '');
            thumb.type = 'button';
            thumb.innerHTML = '<img src="' + escapeHtml(getImageUrl(img)) + '" alt="">';
            thumb.addEventListener('click', function() {
                imgEl.src = getImageUrl(img);
                thumbsEl.querySelectorAll('.quick-view__thumb').forEach(function(t) {
                    t.classList.remove('quick-view__thumb--active');
                });
                thumb.classList.add('quick-view__thumb--active');
            });
            thumbsEl.appendChild(thumb);
        });
    }

    /**
     * Mode 1: Attribute-based variant selection
     * Used when variants have attributes_structured populated
     */
    function renderAttributeSelectors(attributes, variants) {
        variantsEl.innerHTML = '';
        if (!attributes.length) return;

        attributes.forEach(function(attr) {
            var group = document.createElement('div');
            group.className = 'quick-view__variant-group';

            var label = document.createElement('div');
            label.className = 'quick-view__variant-label';
            label.innerHTML = escapeHtml(attr.name) + ': <span class="qv-selected-value"></span>';
            group.appendChild(label);

            var options = document.createElement('div');
            options.className = 'quick-view__variant-options';

            if (attr.type === 'select') {
                // Dropdown
                var sel = document.createElement('select');
                sel.className = 'quick-view__select';
                sel.dataset.attributeSlug = attr.slug;
                var placeholder = document.createElement('option');
                placeholder.value = '';
                placeholder.textContent = '\u2014 Choose ' + escapeHtml(attr.name) + ' \u2014';
                sel.appendChild(placeholder);
                attr.values.forEach(function(val) {
                    var opt = document.createElement('option');
                    opt.value = val.slug;
                    opt.textContent = val.value;
                    opt.dataset.valueLabel = val.value;
                    sel.appendChild(opt);
                });
                sel.addEventListener('change', function() {
                    var opt = this.options[this.selectedIndex];
                    if (opt.value) {
                        selectAttribute(attr.slug, opt.value, opt.dataset.valueLabel, variants, options);
                    }
                });
                options.appendChild(sel);

            } else if (attr.type === 'radio') {
                // Radio list
                options.className += ' quick-view__variant-options--radio';
                attr.values.forEach(function(val) {
                    var radioLabel = document.createElement('label');
                    radioLabel.className = 'quick-view__radio';
                    var input = document.createElement('input');
                    input.type = 'radio';
                    input.name = 'qv-attr-' + attr.slug;
                    input.value = val.slug;
                    input.addEventListener('change', function() {
                        selectAttribute(attr.slug, val.slug, val.value, variants, options);
                    });
                    var span = document.createElement('span');
                    span.className = 'quick-view__radio-label';
                    span.textContent = val.value;
                    radioLabel.appendChild(input);
                    radioLabel.appendChild(span);
                    options.appendChild(radioLabel);
                });

            } else if (attr.type === 'color') {
                // Color swatches
                attr.values.forEach(function(val) {
                    var btn = document.createElement('button');
                    btn.type = 'button';
                    if (val.color_hex) {
                        btn.className = 'quick-view__swatch';
                        btn.style.setProperty('--swatch-color', val.color_hex);
                    } else {
                        btn.className = 'quick-view__swatch quick-view__swatch--placeholder';
                        btn.textContent = val.value.charAt(0);
                    }
                    btn.title = val.value;
                    btn.setAttribute('aria-label', val.value);
                    btn.dataset.attributeSlug = attr.slug;
                    btn.dataset.valueSlug = val.slug;
                    btn.dataset.valueLabel = val.value;
                    btn.addEventListener('click', function() {
                        selectAttribute(attr.slug, val.slug, val.value, variants, options);
                    });
                    options.appendChild(btn);
                });

            } else {
                // Default: button pills (type === 'button' or any other)
                attr.values.forEach(function(val) {
                    var btn = document.createElement('button');
                    btn.className = 'quick-view__option';
                    btn.type = 'button';
                    btn.textContent = val.value;
                    btn.dataset.attributeSlug = attr.slug;
                    btn.dataset.valueSlug = val.slug;
                    btn.dataset.valueLabel = val.value;
                    btn.addEventListener('click', function() {
                        selectAttribute(attr.slug, val.slug, val.value, variants, options);
                    });
                    options.appendChild(btn);
                });
            }

            group.appendChild(options);
            variantsEl.appendChild(group);
        });
    }

    /**
     * Mode 2: Direct variant selection
     * Used when variants have no attribute mappings — shows variants as buttons
     */
    function renderDirectVariants(variants) {
        variantsEl.innerHTML = '';

        var group = document.createElement('div');
        group.className = 'quick-view__variant-group';

        var label = document.createElement('div');
        label.className = 'quick-view__variant-label';
        label.innerHTML = 'Variant: <span class="qv-selected-value"></span>';
        group.appendChild(label);

        var options = document.createElement('div');
        options.className = 'quick-view__variant-options';

        variants.forEach(function(variant) {
            if (!variant.is_active) return;

            var btn = document.createElement('button');
            btn.type = 'button';

            // Extract a short display name from variant name
            // e.g. "Product Name - NOIR" -> "NOIR"
            var displayName = variant.name;
            var parentName = currentProduct ? currentProduct.name : '';
            if (parentName && displayName.indexOf(parentName) === 0) {
                var suffix = displayName.substring(parentName.length).replace(/^\s*[-–—]\s*/, '');
                if (suffix) displayName = suffix;
            }

            // Use color swatch if available
            if (variant.color_swatch) {
                btn.className = 'quick-view__swatch';
                btn.style.setProperty('--swatch-color', variant.color_swatch);
                btn.title = displayName;
                btn.setAttribute('aria-label', displayName);
            } else {
                btn.className = 'quick-view__option';
                btn.textContent = displayName;
            }

            btn.dataset.variantId = variant.id;

            btn.addEventListener('click', function() {
                selectDirectVariant(variant, displayName, options);
            });

            options.appendChild(btn);
        });

        group.appendChild(options);
        variantsEl.appendChild(group);
    }

    function selectDirectVariant(variant, displayName, optionsContainer) {
        selectedVariantId = variant.id;

        // Update visual selection
        optionsContainer.querySelectorAll('.quick-view__swatch, .quick-view__option').forEach(function(btn) {
            var isSelected = String(btn.dataset.variantId) === String(variant.id);
            btn.classList.toggle('quick-view__swatch--selected', isSelected && btn.classList.contains('quick-view__swatch'));
            btn.classList.toggle('quick-view__option--selected', isSelected && btn.classList.contains('quick-view__option'));
        });

        // Update label
        var group = optionsContainer.closest('.quick-view__variant-group');
        var selectedSpan = group.querySelector('.qv-selected-value');
        if (selectedSpan) selectedSpan.textContent = displayName;

        // Update price
        if (variant.effective_price) {
            renderPrice(
                variant.effective_price.amount,
                variant.effective_price.currency,
                currentProduct.compare_at_price_amount
            );
        }

        // Swap gallery to variant images (or first image as fallback)
        swapGallery(variant);

        // Update stock
        renderStock(variant.stock_quantity);
        updateButtonState();
    }

    /** Swap the main image and thumbnails to show variant-specific images */
    function swapGallery(variant) {
        var variantImages = variant.images || [];
        if (variantImages.length > 0) {
            // Variant has its own gallery — show those images
            imgEl.src = getImageUrl(variantImages[0]);
            imgEl.alt = variantImages[0].alt_text || variant.name;
            renderThumbnails(variantImages);
        } else if (variant.image_url) {
            // Single variant image
            imgEl.src = variant.image_url;
        }
        // If variant has no images at all, keep the current product images
    }

    function selectAttribute(attrSlug, valueSlug, valueLabel, variants, optionsContainer) {
        selectedAttributes[attrSlug] = valueSlug;

        // Update visual selection
        optionsContainer.querySelectorAll('.quick-view__swatch, .quick-view__option').forEach(function(btn) {
            var isSelected = btn.dataset.valueSlug === valueSlug;
            btn.classList.toggle('quick-view__swatch--selected', isSelected && btn.classList.contains('quick-view__swatch'));
            btn.classList.toggle('quick-view__option--selected', isSelected && btn.classList.contains('quick-view__option'));
        });

        // Update label
        var group = optionsContainer.closest('.quick-view__variant-group');
        var selectedSpan = group.querySelector('.qv-selected-value');
        if (selectedSpan) selectedSpan.textContent = valueLabel;

        // Find matching variant
        matchVariant(variants);
    }

    function matchVariant(variants) {
        selectedVariantId = null;

        for (var i = 0; i < variants.length; i++) {
            var variant = variants[i];
            if (!variant.is_active) continue;

            var attrs = variant.attributes_structured || [];
            var match = true;

            for (var slug in selectedAttributes) {
                var found = false;
                for (var j = 0; j < attrs.length; j++) {
                    if (attrs[j].attribute_slug === slug && attrs[j].value_slug === selectedAttributes[slug]) {
                        found = true;
                        break;
                    }
                }
                if (!found) { match = false; break; }
            }

            if (match && Object.keys(selectedAttributes).length === attrs.length) {
                selectedVariantId = variant.id;

                // Update price
                if (variant.effective_price) {
                    renderPrice(
                        variant.effective_price.amount,
                        variant.effective_price.currency,
                        currentProduct.compare_at_price_amount
                    );
                }

                // Swap gallery to variant images
                swapGallery(variant);

                // Update stock
                renderStock(variant.stock_quantity);
                break;
            }
        }

        updateButtonState();
    }

    function renderStock(qty) {
        stockEl.innerHTML = '';
        if (qty === undefined || qty === null) return;

        var el = document.createElement('span');
        if (qty > 10) {
            el.className = 'quick-view__stock--in-stock';
            el.innerHTML = '<i class="fas fa-check-circle"></i> In stock';
        } else if (qty > 0) {
            el.className = 'quick-view__stock--low-stock';
            el.innerHTML = '<i class="fas fa-exclamation-circle"></i> Only ' + qty + ' left';
        } else {
            el.className = 'quick-view__stock--out-of-stock';
            el.innerHTML = '<i class="fas fa-times-circle"></i> Out of stock';
        }
        stockEl.appendChild(el);
    }

    function updateButtonState() {
        if (selectedVariantId) {
            addBtn.disabled = false;
            addBtnText.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
        } else {
            addBtn.disabled = true;
            addBtnText.textContent = 'Select Options';
        }
    }

    function handleAddToCart() {
        if (!selectedVariantId || !currentProduct) return;

        var qty = parseInt(qtyInput.value, 10) || 1;

        // Show loading
        addBtn.disabled = true;
        addBtnText.style.display = 'none';
        modal.querySelector('.quick-view__add-btn-loading').style.display = '';

        if (typeof addToCart === 'function') {
            addToCart(currentProduct.id, qty, selectedVariantId);
        }

        // Reset after timeout (addToCart doesn't return a promise)
        setTimeout(function() {
            addBtnText.style.display = '';
            modal.querySelector('.quick-view__add-btn-loading').style.display = 'none';
            addBtn.disabled = false;
            close();
        }, 1500);
    }

    function close() {
        if (!modal) return;
        modal.classList.remove('quick-view--visible');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    function getCurrencySymbol(code) {
        var symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥', 'CNY': '¥',
            'AUD': 'A$', 'CAD': 'C$', 'CHF': 'CHF ', 'SEK': 'kr ',
            'NOK': 'kr ', 'DKK': 'kr ', 'NZD': 'NZ$', 'SGD': 'S$',
            'HKD': 'HK$', 'KRW': '₩', 'INR': '₹', 'BRL': 'R$',
            'MXN': 'MX$', 'ZAR': 'R', 'TRY': '₺', 'PLN': 'zł',
            'THB': '฿', 'IDR': 'Rp', 'MYR': 'RM', 'PHP': '₱'
        };
        return symbols[code] || code + ' ';
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose globally
    window.QuickView = { open: open, close: close };

})();
