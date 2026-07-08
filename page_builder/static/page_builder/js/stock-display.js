/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Stock Availability Display
 * Handles regional stock display and store picker modal for product pages
 */
(function() {
    'use strict';

    // Initialize stock display when DOM is ready
    function init() {
        // Load regional stock for all products on page
        document.querySelectorAll('[data-product-stock]').forEach(el => {
            const productId = el.dataset.productId;
            const productSlug = el.dataset.productSlug;
            if (productSlug) {
                loadRegionalStock(productSlug, productId);
            }
        });

        // Event delegation for store picker buttons
        document.addEventListener('click', (e) => {
            const toggleBtn = e.target.closest('[data-action="toggle-store-picker"]');
            if (toggleBtn) {
                e.preventDefault();
                const productId = toggleBtn.dataset.productId;
                const productSlug = toggleBtn.dataset.productSlug;
                toggleStorePicker(productId, productSlug);
                return;
            }

            // Close modal when clicking backdrop
            if (e.target.classList.contains('modal__backdrop')) {
                const modal = e.target.closest('.modal--store-picker');
                if (modal) {
                    modal.classList.add('hidden');
                    document.body.style.overflow = 'auto';
                }
            }
        });
    }

    function loadRegionalStock(productSlug, productId) {
        fetch(`/api/catalog/products/${productSlug}/`)
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById(`regional-stock-${productId}`);
                if (!container) return;

                const regionalStock = data.regional_stock;
                if (!regionalStock) {
                    container.innerHTML = '';
                    return;
                }

                let statusClass = 'out-of-stock';
                let iconHtml = '<svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>';

                if (regionalStock.available) {
                    statusClass = regionalStock.quantity && regionalStock.quantity <= 5 ? 'low-stock' : 'in-stock';
                    iconHtml = '<svg fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>';
                }

                container.innerHTML = `
                    <div class="stock-status__loading ${statusClass}">
                        ${iconHtml}
                        <span class="stock-status__text" style="font-weight: var(--theme-font-weight-medium);">${escapeHtml(regionalStock.message)}</span>
                    </div>
                `;
            })
            .catch(error => {
                console.error('Error loading regional stock:', error);
                const container = document.getElementById(`regional-stock-${productId}`);
                if (container) {
                    // Note: Translation should be passed from template via data attribute if needed
                    container.innerHTML = '<span class="stock-status__text stock-status__text--muted">Stock information unavailable</span>';
                }
            });
    }

    function toggleStorePicker(productId, productSlug) {
        const modal = document.getElementById(`store-picker-${productId}`);
        if (!modal) return;

        const isHidden = modal.classList.contains('hidden');

        if (isHidden) {
            // Show modal
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';

            // Load pickup locations
            loadPickupLocations(productSlug, productId);
        } else {
            // Hide modal
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    }

    function loadPickupLocations(productSlug, productId) {
        const container = document.getElementById(`store-list-${productId}`);
        if (!container) return;

        // Show loading state
        container.innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
            </div>
        `;

        fetch(`/api/catalog/pickup-locations/?product_slug=${productSlug}`)
            .then(response => response.json())
            .then(data => {
                if (!data.locations || data.locations.length === 0) {
                    container.innerHTML = `
                        <div class="empty-state">
                            <svg class="empty-state__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                            <p class="empty-state__text">No pickup locations available for this product</p>
                        </div>
                    `;
                    return;
                }

                // Render store locations
                let html = '';
                data.locations.forEach(location => {
                    const warehouse = location.warehouse;
                    const inStock = location.in_stock !== false;
                    const qty = location.available_quantity;

                    let badgeHtml = '';
                    if (qty !== undefined && qty !== null) {
                        if (qty > 0) {
                            badgeHtml = `<span class="${qty <= 5 ? 'badge--low-stock' : 'badge--available'}">${qty} in stock</span>`;
                        } else {
                            badgeHtml = '<span class="badge--unavailable">Out of stock</span>';
                        }
                    } else {
                        badgeHtml = '<span class="badge--available">Available</span>';
                    }

                    html += `
                        <div class="store-option">
                            <div class="store-option__layout">
                                <div class="store-option__info">
                                    <h4 class="store-option__name">${escapeHtml(warehouse.name)}</h4>
                                    <p class="store-option__address">
                                        ${escapeHtml(warehouse.address_line1)}<br>
                                        ${escapeHtml(warehouse.city)}, ${escapeHtml(warehouse.state_province || '')} ${escapeHtml(warehouse.postal_code)}
                                    </p>
                                    ${warehouse.contact_phone ? `<p class="store-option__phone">📞 ${escapeHtml(warehouse.contact_phone)}</p>` : ''}
                                </div>
                                <div class="store-option__status">
                                    ${badgeHtml}
                                </div>
                            </div>
                        </div>
                    `;
                });

                container.innerHTML = html;
            })
            .catch(error => {
                console.error('Error loading pickup locations:', error);
                container.innerHTML = `
                    <div class="error-state">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <p>Error loading store information</p>
                    </div>
                `;
            });
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text || '';
        return div.innerHTML;
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for potential external use
    window.StockDisplay = {
        loadRegionalStock,
        toggleStorePicker
    };
})();
