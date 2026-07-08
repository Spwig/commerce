/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Checkout Express UI
 *
 * Streamlined flow for returning customers with saved details.
 * Shows saved address/payment in compact view with "Change" toggles.
 * Falls back to another template if no saved details.
 * Loaded AFTER checkout.js.
 */
(function() {
    'use strict';

    function initExpress() {
        const C = window.Checkout;
        if (!C) {
            console.error('Checkout base not loaded');
            return;
        }

        const config = C.config || {};
        const container = document.querySelector('.checkout-container--express');
        if (!container) return;

        const fallbackTemplate = container.dataset.fallbackTemplate || 'accordion';

        // === Check for saved details ===

        function checkSavedDetails() {
            const hasSavedAddress = document.querySelectorAll('.saved-address-card').length > 0;
            const hasSession = C.sessionData && (C.sessionData.shipping_address || C.sessionData.shipping_address_data);

            if (!hasSavedAddress && !hasSession) {
                const lang = config.lang || 'en';
                const fallbackUrl = `/${lang}/checkout/?template=${fallbackTemplate}`;
                window.location.href = fallbackUrl;
                return false;
            }
            return true;
        }

        // === Render saved info ===

        function renderSavedAddress() {
            const addressEl = document.getElementById('express-default-address');
            if (!addressEl) return;

            const addr = C.sessionData && (C.sessionData.shipping_address || C.sessionData.shipping_address_data);
            if (addr) {
                addressEl.innerHTML = `<div class="express__saved-card-content">
                    ${[
                        addr.name,
                        addr.address1,
                        addr.address2,
                        `${addr.city || ''}, ${addr.state || ''} ${addr.postal_code || ''}`.trim(),
                        addr.country
                    ].filter(Boolean).map(l => `<p>${C.esc(l)}</p>`).join('')}
                </div>`;
            }
        }

        function renderSavedShippingMethod() {
            const el = document.getElementById('express-selected-shipping-method');
            if (!el) return;

            const method = C.sessionData && C.sessionData.selected_shipping_method;
            const cost = C.sessionData && C.sessionData.shipping_cost;
            if (method) {
                const costDisplay = (cost !== null && cost !== undefined)
                    ? (parseFloat(cost) === 0 ? 'Free' : C.formatCurrency(cost))
                    : '';
                el.innerHTML = `<div class="express__saved-card-content">
                    <p class="express__saved-card-name">${C.esc(method.name)}</p>
                    ${costDisplay ? `<p>${costDisplay}</p>` : ''}
                </div>`;
            }
        }

        function renderSavedPayment() {
            const paymentEl = document.getElementById('express-selected-payment');
            if (!paymentEl) return;

            if (C.sessionData && C.sessionData.payment_provider_name) {
                paymentEl.innerHTML = `<div class="express__saved-card-content">
                    <p class="express__saved-card-name">${C.esc(C.sessionData.payment_provider_name)}</p>
                </div>`;
            }
        }

        function renderExpressItems() {
            const itemsEl = document.getElementById('express-items');
            if (!itemsEl || !C.cartData) return;

            const items = C.cartData.items || [];
            itemsEl.innerHTML = items.map(item => {
                const product = item.product || {};
                const name = product.name || 'Product';
                const imageUrl = (product.images && product.images.length > 0)
                    ? (product.images[0].thumbnail_url || product.images[0].image_url || '')
                    : '/static/img/placeholder-product-thumb.png';
                return `
                    <div class="express__item">
                        ${imageUrl ? `<img src="${C.escAttr(imageUrl)}" alt="${C.escAttr(name)}" class="express__item-image">` : ''}
                        <div class="express__item-info">
                            <div class="express__item-name">${C.esc(name)}</div>
                            <div class="express__item-qty">x${item.quantity}</div>
                        </div>
                        <div class="express__item-price">${C.formatCurrency(item.total_price)}</div>
                    </div>
                `;
            }).join('');
        }

        // === Change toggles ===

        document.querySelectorAll('.express__change-link').forEach(btn => {
            btn.addEventListener('click', function() {
                const section = this.closest('.express__section');
                const targetId = this.dataset.target;
                const panel = targetId ? document.getElementById(targetId) : null;
                const savedCard = section.querySelector('.express__saved-card');

                if (panel) {
                    const isVisible = !panel.hidden;
                    panel.hidden = isVisible;
                    this.textContent = isVisible ? 'Change' : 'Cancel';
                    if (savedCard) savedCard.style.display = isVisible ? '' : 'none';

                    // Fetch fresh data when opening change panels
                    if (!isVisible) {
                        if (targetId === 'express-shipping-method-picker') {
                            C.fetchShippingMethods();
                        } else if (targetId === 'express-payment-picker') {
                            C.fetchPaymentProviders();
                        }
                    }
                }
            });
        });

        // Cancel buttons close the change panel
        document.querySelectorAll('[id^="express-cancel-"]').forEach(btn => {
            btn.addEventListener('click', function() {
                const panel = this.closest('.express__change-panel');
                if (panel) {
                    panel.hidden = true;
                    const section = panel.closest('.express__section');
                    const savedCard = section.querySelector('.express__saved-card');
                    if (savedCard) savedCard.style.display = '';
                    const changeBtn = section.querySelector('.express__change-link');
                    if (changeBtn) changeBtn.textContent = 'Change';
                }
            });
        });

        // Confirm buttons for shipping method and payment
        const confirmShippingBtn = document.getElementById('express-confirm-shipping-method');
        if (confirmShippingBtn) {
            confirmShippingBtn.addEventListener('click', async function() {
                const selected = document.querySelector('#shipping-methods-list input[type="radio"]:checked');
                if (!selected) {
                    C.showAlert('Please select a shipping method.', 'error');
                    return;
                }
                await C.submitShippingMethod();
                // Re-render after submission
                renderSavedShippingMethod();
                const panel = document.getElementById('express-shipping-method-picker');
                if (panel) panel.hidden = true;
                const savedCard = document.getElementById('express-selected-shipping-method');
                if (savedCard) savedCard.style.display = '';
                const changeBtn = document.getElementById('express-change-shipping-method');
                if (changeBtn) changeBtn.textContent = 'Change';
            });
        }

        // === Override Checkout navigation ===

        // Express doesn't use step navigation
        C.openStep = function() {};
        C.updateStepUI = function() {};

        // === Auto-complete flow ===

        // After checkout loads, if we have session data, render express view
        const originalLoadCheckout = C.loadCheckout.bind(C);
        C.loadCheckout = async function() {
            await originalLoadCheckout();

            if (!checkSavedDetails()) return;

            renderSavedAddress();
            renderSavedShippingMethod();
            renderSavedPayment();
            renderExpressItems();
            // Totals are rendered by base renderSummary() using standard summary IDs

            // If session has no address yet, pre-select the default saved address
            if (!C.sessionData.shipping_address && !C.sessionData.shipping_address_data) {
                const defaultRadio = document.querySelector('.saved-address-card--selected input[type="radio"]');
                if (defaultRadio) {
                    C.submitShippingAddress();
                }
            }
        };

        // After load, re-trigger
        C.loadCheckout();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initExpress, 10);
        });
    } else {
        setTimeout(initExpress, 10);
    }
})();
