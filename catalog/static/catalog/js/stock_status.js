/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Stock Status Component JavaScript
 * Handles fetching product availability and the Notify Me form
 */

class StockStatusManager {
    constructor(containerSelector = '#stock-status') {
        this.container = document.querySelector(containerSelector);
        if (!this.container) return;

        this.productSlug = this.container.dataset.productSlug;
        this.currentVariantId = null;

        this.elements = {
            badge: document.getElementById('stock-badge'),
            lowStockWarning: document.getElementById('low-stock-warning'),
            lowStockMessage: document.getElementById('low-stock-message'),
            shipsFrom: document.getElementById('ships-from'),
            shipsFromText: document.getElementById('ships-from-text'),
            estimatedDelivery: document.getElementById('estimated-delivery'),
            deliveryText: document.getElementById('delivery-text'),
            preorderInfo: document.getElementById('preorder-info'),
            preorderText: document.getElementById('preorder-text'),
            notifyContainer: document.getElementById('notify-me-container'),
            notifyForm: document.getElementById('notify-me-form'),
            notifyEmail: document.getElementById('notify-email'),
            notifySuccess: document.getElementById('notify-success'),
            notifyDisclaimer: document.getElementById('notify-disclaimer'),
        };

        this.addToCartBtn = document.getElementById('add-to-cart');

        this.init();
    }

    init() {
        // Fetch initial availability
        this.fetchAvailability();

        // Set up Notify Me form handler
        if (this.elements.notifyForm) {
            this.elements.notifyForm.addEventListener('submit', (e) => this.handleNotifySubmit(e));
        }

        // Listen for variant changes
        this.setupVariantListener();
    }

    setupVariantListener() {
        // Watch for variant selection changes
        const variantSwatches = document.querySelectorAll('.variant-swatch');
        variantSwatches.forEach(swatch => {
            swatch.addEventListener('click', () => {
                // Wait a tick for the variant ID to be set on the add to cart button
                setTimeout(() => {
                    const newVariantId = this.addToCartBtn?.dataset.variantId;
                    if (newVariantId !== this.currentVariantId) {
                        this.currentVariantId = newVariantId;
                        this.container.dataset.variantId = newVariantId || '';
                        this.fetchAvailability(newVariantId);
                    }
                }, 50);
            });
        });
    }

    async fetchAvailability(variantId = null) {
        if (!this.productSlug) return;

        // Show loading state
        this.showLoading();

        let url = `/api/catalog/products/${this.productSlug}/availability/`;
        if (variantId) {
            url += `?variant_id=${variantId}`;
        }

        try {
            const response = await fetch(url);
            const data = await response.json();

            if (response.ok) {
                this.updateDisplay(data);
            } else {
                console.error('Failed to fetch availability:', data);
                this.showError();
            }
        } catch (error) {
            console.error('Error fetching availability:', error);
            this.showError();
        }
    }

    showLoading() {
        if (this.elements.badge) {
            this.elements.badge.innerHTML = `
                <span class="stock-status__loading">
                    <i class="fas fa-spinner fa-spin"></i> Checking availability...
                </span>
            `;
            this.elements.badge.className = 'stock-status__badge';
        }
    }

    showError() {
        if (this.elements.badge) {
            this.elements.badge.innerHTML = `<span>Unable to check availability</span>`;
            this.elements.badge.className = 'stock-status__badge';
        }
    }

    updateDisplay(data) {
        // Hide all optional elements first
        this.hideAllOptionalElements();

        // Update stock badge
        this.updateBadge(data);

        // Show low stock warning if applicable
        if (data.show_low_stock_warning && data.low_stock_quantity) {
            this.showLowStockWarning(data.low_stock_quantity);
        }

        // Show ships from location if applicable
        if (data.show_ships_from && data.ships_from) {
            this.showShipsFrom(data.ships_from);
        }

        // Show estimated delivery if applicable
        if (data.show_estimated_delivery && data.estimated_delivery) {
            this.showEstimatedDelivery(data.estimated_delivery);
        }

        // Show pre-order info if applicable
        if (data.is_preorder) {
            this.showPreorderInfo(data.preorder_message, data.preorder_release_date);
        }

        // Show Notify Me form if applicable
        if (data.show_notify_me) {
            this.showNotifyMe();
        }

        // Update add to cart button state
        this.updateAddToCartButton(data);
    }

    updateBadge(data) {
        if (!this.elements.badge) return;

        let badgeClass = 'stock-status__badge';
        let badgeText = '';
        let badgeIcon = '';

        if (data.is_preorder) {
            badgeClass += ' stock-status__badge--preorder';
            badgeText = data.preorder_message || 'Pre-Order';
            badgeIcon = '<i class="fas fa-calendar-alt"></i>';
        } else if (data.in_stock) {
            if (data.show_low_stock_warning && data.low_stock_quantity) {
                badgeClass += ' stock-status__badge--low-stock';
                if (data.show_exact_quantity) {
                    badgeText = `Only ${data.low_stock_quantity} left!`;
                } else {
                    badgeText = 'Low Stock';
                }
                badgeIcon = '<i class="fas fa-exclamation-triangle"></i>';
            } else {
                badgeClass += ' stock-status__badge--in-stock';
                badgeText = 'In Stock';
            }
        } else {
            // Out of stock
            if (data.allow_backorders) {
                badgeClass += ' stock-status__badge--backorder';
                badgeText = data.backorder_message || 'Available on Backorder';
                badgeIcon = '<i class="fas fa-clock"></i>';
            } else {
                badgeClass += ' stock-status__badge--out-of-stock';
                badgeText = data.out_of_stock_message || 'Out of Stock';
                badgeIcon = '<i class="fas fa-times-circle"></i>';
            }
        }

        this.elements.badge.className = badgeClass;
        this.elements.badge.innerHTML = badgeIcon ? `${badgeIcon} <span>${badgeText}</span>` : `<span>${badgeText}</span>`;
    }

    hideAllOptionalElements() {
        const optionalElements = [
            'lowStockWarning', 'shipsFrom', 'estimatedDelivery',
            'preorderInfo', 'notifyContainer'
        ];

        optionalElements.forEach(key => {
            if (this.elements[key]) {
                this.elements[key].style.display = 'none';
            }
        });

        // Reset notify form state
        if (this.elements.notifySuccess) {
            this.elements.notifySuccess.style.display = 'none';
        }
        if (this.elements.notifyForm) {
            this.elements.notifyForm.style.display = 'flex';
        }
        if (this.elements.notifyDisclaimer) {
            this.elements.notifyDisclaimer.style.display = 'block';
        }
    }

    showLowStockWarning(quantity) {
        if (this.elements.lowStockWarning && this.elements.lowStockMessage) {
            this.elements.lowStockMessage.textContent = `Only ${quantity} left in stock - order soon!`;
            this.elements.lowStockWarning.style.display = 'flex';
        }
    }

    showShipsFrom(location) {
        if (this.elements.shipsFrom && this.elements.shipsFromText) {
            this.elements.shipsFromText.textContent = `Ships from ${location}`;
            this.elements.shipsFrom.style.display = 'flex';
        }
    }

    showEstimatedDelivery(delivery) {
        if (this.elements.estimatedDelivery && this.elements.deliveryText) {
            this.elements.deliveryText.textContent = `${delivery}`;
            this.elements.estimatedDelivery.style.display = 'flex';
        }
    }

    showPreorderInfo(message, releaseDate) {
        if (this.elements.preorderInfo && this.elements.preorderText) {
            let text = message || 'Pre-Order Available';
            if (releaseDate && !message) {
                text = `Pre-Order - Available ${releaseDate}`;
            }
            this.elements.preorderText.textContent = text;
            this.elements.preorderInfo.style.display = 'flex';
        }
    }

    showNotifyMe() {
        if (this.elements.notifyContainer) {
            this.elements.notifyContainer.style.display = 'block';
        }
    }

    updateAddToCartButton(data) {
        if (!this.addToCartBtn) return;

        const buttonText = this.addToCartBtn.querySelector('span');

        if (data.is_preorder) {
            // Enable button for pre-order
            this.addToCartBtn.disabled = false;
            if (buttonText) buttonText.textContent = 'Pre-Order';
        } else if (data.in_stock || data.allow_backorders) {
            // Enable button for in-stock or backorder
            this.addToCartBtn.disabled = false;
            if (buttonText) {
                buttonText.textContent = data.allow_backorders && !data.in_stock
                    ? 'Backorder'
                    : 'Add to Cart';
            }
        } else {
            // Disable button for out of stock (no backorder)
            this.addToCartBtn.disabled = true;
            if (buttonText) buttonText.textContent = 'Out of Stock';
        }
    }

    async handleNotifySubmit(e) {
        e.preventDefault();

        const email = this.elements.notifyEmail?.value?.trim();
        if (!email) return;

        const submitBtn = this.elements.notifyForm.querySelector('button');
        const btnText = submitBtn?.querySelector('.btn-text');
        const btnLoading = submitBtn?.querySelector('.btn-loading');

        // Show loading state
        if (btnText) btnText.style.display = 'none';
        if (btnLoading) btnLoading.style.display = 'inline';
        if (submitBtn) submitBtn.disabled = true;

        const variantId = this.container.dataset.variantId || null;

        try {
            const response = await fetch(`/api/catalog/products/${this.productSlug}/notify-me/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    email: email,
                    variant_id: variantId
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Show success message
                if (this.elements.notifyForm) {
                    this.elements.notifyForm.style.display = 'none';
                }
                if (this.elements.notifyDisclaimer) {
                    this.elements.notifyDisclaimer.style.display = 'none';
                }
                if (this.elements.notifySuccess) {
                    this.elements.notifySuccess.style.display = 'flex';
                }
            } else {
                // Show error
                this.showNotifyError(data.error || 'Unable to subscribe. Please try again.');
            }
        } catch (error) {
            console.error('Notify Me error:', error);
            this.showNotifyError('Network error. Please try again.');
        } finally {
            // Reset button state
            if (btnText) btnText.style.display = 'inline';
            if (btnLoading) btnLoading.style.display = 'none';
            if (submitBtn) submitBtn.disabled = false;
        }
    }

    showNotifyError(message) {
        // Remove any existing error
        const existingError = this.elements.notifyContainer?.querySelector('.stock-status__notify-error');
        if (existingError) existingError.remove();

        // Add new error message
        const errorEl = document.createElement('div');
        errorEl.className = 'stock-status__notify-error';
        errorEl.innerHTML = `<i class="fas fa-exclamation-circle"></i> <span>${message}</span>`;
        this.elements.notifyForm?.after(errorEl);

        // Auto-remove after 5 seconds
        setTimeout(() => errorEl.remove(), 5000);
    }

    getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input) return input.value;
        return '';
    }
}

// Initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-initialize if stock-status container exists
    if (document.getElementById('stock-status')) {
        window.stockStatusManager = new StockStatusManager();
    }
});
