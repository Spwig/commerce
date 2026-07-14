/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Cart Page Module
 * Handles shopping cart display, quantity updates, item removal, and voucher management
 */
(function () {
  'use strict';

  const CartPage = {
    endpoints: {
      cart: '/api/cart/',
      updateItem: '/api/cart/items/',
      applyVoucher: '/api/cart/apply-voucher/',
      removeVoucher: '/api/cart/remove-voucher/',
    },

    els: {},

    init() {
      this.cacheElements();
      this.bindEvents();
      this.fetchCart();
    },

    cacheElements() {
      this.els.loading = document.getElementById('cart-loading');
      this.els.empty = document.getElementById('cart-empty');
      this.els.list = document.getElementById('cart-list');
      this.els.summary = document.getElementById('cart-summary');
      this.els.subtotal = document.getElementById('cart-subtotal');
      this.els.discount = document.getElementById('cart-discount');
      this.els.discountRow = document.getElementById('cart-discount-row');
      this.els.shipping = document.getElementById('cart-shipping');
      this.els.total = document.getElementById('cart-total');
      this.els.voucherInput = document.getElementById('voucher-code');
      this.els.voucherBtn = document.getElementById('apply-voucher');
      this.els.voucherMessage = document.getElementById('voucher-message');
      this.els.appliedVouchers = document.getElementById('applied-vouchers');
    },

    bindEvents() {
      if (this.els.voucherBtn) {
        this.els.voucherBtn.addEventListener('click', () => this.applyVoucher());
      }
      if (this.els.voucherInput) {
        this.els.voucherInput.addEventListener('keydown', e => {
          if (e.key === 'Enter') {
            e.preventDefault();
            this.applyVoucher();
          }
        });
      }

      // Event delegation for dynamically generated cart items
      document.addEventListener('click', e => {
        // Quantity decrease button
        const decreaseBtn = e.target.closest('[data-action="decrease-quantity"]');
        if (decreaseBtn) {
          e.preventDefault();
          const itemId = parseInt(decreaseBtn.dataset.itemId, 10);
          const newQty = parseInt(decreaseBtn.dataset.newQuantity, 10);
          this.updateQuantity(itemId, newQty);
          return;
        }

        // Quantity increase button
        const increaseBtn = e.target.closest('[data-action="increase-quantity"]');
        if (increaseBtn) {
          e.preventDefault();
          const itemId = parseInt(increaseBtn.dataset.itemId, 10);
          const newQty = parseInt(increaseBtn.dataset.newQuantity, 10);
          this.updateQuantity(itemId, newQty);
          return;
        }

        // Remove item button
        const removeBtn = e.target.closest('[data-action="remove-item"]');
        if (removeBtn) {
          e.preventDefault();
          const itemId = parseInt(removeBtn.dataset.itemId, 10);
          this.removeItem(itemId);
          return;
        }

        // Remove voucher button
        const removeVoucherBtn = e.target.closest('[data-action="remove-voucher"]');
        if (removeVoucherBtn) {
          e.preventDefault();
          const code = removeVoucherBtn.dataset.code;
          this.removeVoucher(code);
          return;
        }
      });

      // Event delegation for quantity input changes
      document.addEventListener('change', e => {
        if (e.target.matches('[data-action="change-quantity"]')) {
          e.preventDefault();
          const itemId = parseInt(e.target.dataset.itemId, 10);
          const newQty = parseInt(e.target.value, 10);
          if (!isNaN(newQty) && newQty > 0) {
            this.updateQuantity(itemId, newQty);
          }
        }
      });
    },

    async fetchCart() {
      try {
        const response = await fetch(this.endpoints.cart, {
          headers: { Accept: 'application/json' },
        });
        if (!response.ok) throw new Error('Failed to load cart');
        const data = await response.json();
        this.render(data);
      } catch (error) {
        console.error('Error fetching cart:', error);
        this.showEmpty();
      }
    },

    render(data) {
      this.els.loading.hidden = true;
      const items = data.items || [];

      if (items.length === 0) {
        this.showEmpty();
        return;
      }

      this.els.empty.hidden = true;
      this.els.list.hidden = false;
      this.els.summary.hidden = false;

      this.renderItems(items);
      this.renderSummary(data);
      this.renderVouchers(data.applied_vouchers || []);
      this.syncBadges(data.total_items || items.length);
    },

    showEmpty() {
      this.els.loading.hidden = true;
      this.els.empty.hidden = false;
      this.els.list.hidden = true;
      this.els.summary.hidden = true;
      this.syncBadges(0);
    },

    renderItems(items) {
      this.els.list.innerHTML = items
        .map(item => {
          const product = item.product || {};
          const variant = item.variant;
          const name = product.name || 'Product';
          const imageUrl =
            product.images && product.images.length > 0
              ? product.images[0].thumbnail_url ||
                product.images[0].image_url ||
                product.images[0].url ||
                ''
              : '/static/img/placeholder-product-thumb.png';
          const productUrl = product.url || product.slug ? `/product/${product.slug}/` : '#';
          const variantName = variant ? variant.name || '' : '';
          const unitPrice = item.product
            ? product.effective_price_formatted || product.price_formatted || item.total_price
            : item.total_price;
          const lineTotal = item.total_price || '0.00';

          // Nested components for configurable/bundle products
          const bundleComps = item.bundle_components;
          let componentsHtml = '';
          if (bundleComps) {
            const allComps = [...(bundleComps.shipping || []), ...(bundleComps.instant || [])];
            if (allComps.length > 0) {
              componentsHtml = `
                            <div class="cart-item__components">
                                ${allComps
                                  .map(comp => {
                                    const compName = comp.product ? comp.product.name : 'Component';
                                    const compVariant = comp.variant ? comp.variant.name : '';
                                    const compImage =
                                      comp.product &&
                                      comp.product.images &&
                                      comp.product.images.length > 0
                                        ? comp.product.images[0].thumbnail_url ||
                                          comp.product.images[0].image_url ||
                                          comp.product.images[0].url ||
                                          ''
                                        : '';
                                    const compImageHtml = compImage
                                      ? `<img src="${this.escapeAttr(compImage)}" alt="" class="cart-item__component-image" loading="lazy">`
                                      : '<div class="cart-item__component-image cart-item__component-image--placeholder"><i class="fas fa-box"></i></div>';
                                    return `
                                        <div class="cart-item__component">
                                            ${compImageHtml}
                                            <div class="cart-item__component-info">
                                                <span class="cart-item__component-name">${this.escapeHtml(compName)}</span>
                                                ${compVariant ? `<span class="cart-item__component-variant">${this.escapeHtml(compVariant)}</span>` : ''}
                                            </div>
                                            <span class="cart-item__component-qty">&times;${comp.quantity}</span>
                                        </div>
                                    `;
                                  })
                                  .join('')}
                            </div>
                        `;
            }
          }

          return `
                    <div class="cart-item" data-item-id="${item.id}">
                        <img src="${this.escapeAttr(imageUrl)}"
                             alt="${this.escapeAttr(name)}"
                             class="cart-item__image"
                             loading="lazy">
                        <div class="cart-item__details">
                            <a href="${this.escapeAttr(productUrl)}" class="cart-item__name">${this.escapeHtml(name)}</a>
                            ${variantName ? `<p class="cart-item__variant">${this.escapeHtml(variantName)}</p>` : ''}
                            ${componentsHtml}
                            <div class="cart-item__actions">
                                <div class="cart-item__quantity">
                                    <button type="button" aria-label="Decrease quantity"
                                            data-action="decrease-quantity"
                                            data-item-id="${item.id}"
                                            data-new-quantity="${item.quantity - 1}">
                                        <i class="fas fa-minus"></i>
                                    </button>
                                    <input type="number" value="${item.quantity}" min="1"
                                           aria-label="Quantity"
                                           data-action="change-quantity"
                                           data-item-id="${item.id}">
                                    <button type="button" aria-label="Increase quantity"
                                            data-action="increase-quantity"
                                            data-item-id="${item.id}"
                                            data-new-quantity="${item.quantity + 1}">
                                        <i class="fas fa-plus"></i>
                                    </button>
                                </div>
                                <button type="button" class="cart-item__remove" aria-label="Remove item"
                                        data-action="remove-item"
                                        data-item-id="${item.id}">
                                    <i class="fas fa-trash-alt"></i>
                                </button>
                            </div>
                        </div>
                        <div class="cart-item__line-total">${this.formatCurrency(lineTotal)}</div>
                    </div>
                `;
        })
        .join('');
    },

    renderSummary(data) {
      const subtotal = data.total_amount || '0.00';
      const discount = data.voucher_discount_amount || '0.00';
      const total = data.grand_total || data.final_amount || subtotal;

      this.els.subtotal.textContent = this.formatCurrency(subtotal);
      this.els.total.textContent = this.formatCurrency(total);

      if (parseFloat(discount) > 0) {
        this.els.discountRow.hidden = false;
        this.els.discount.textContent = '-' + this.formatCurrency(discount);
      } else {
        this.els.discountRow.hidden = true;
      }

      // Display-only mode: show dual-currency info
      this.renderDisplayOnlyNotice(data);
    },

    renderDisplayOnlyNotice(data) {
      // Remove existing notice if any
      const existing = document.getElementById('cart-display-only-notice');
      if (existing) existing.remove();

      if (!data.display_only_mode || !data.display_exchange_rate) return;

      const rate = data.display_exchange_rate;
      const displayCurrency = data.display_currency;
      const chargeCurrency = data.charge_currency;

      // Convert total to display currency for reference
      const totalNum = parseFloat(
        data.grand_total || data.final_amount || data.total_amount || '0'
      );
      const displayTotal = totalNum * rate;

      const formattedDisplay = new Intl.NumberFormat(undefined, {
        style: 'currency',
        currency: displayCurrency,
        minimumFractionDigits: 2,
      }).format(displayTotal);

      const notice = document.createElement('div');
      notice.id = 'cart-display-only-notice';
      notice.className = 'cart-conversion-notice';
      notice.innerHTML =
        '<i class="fas fa-info-circle"></i> ' +
        '<span>Approximate total in ' +
        this.escapeHtml(displayCurrency) +
        ': <strong>' +
        formattedDisplay +
        '</strong>. ' +
        'Your payment will be processed in ' +
        this.escapeHtml(chargeCurrency) +
        '.</span>';

      // Insert after the summary section
      if (this.els.summary) {
        this.els.summary.appendChild(notice);
      }
    },

    renderVouchers(vouchers) {
      if (!this.els.appliedVouchers) return;
      if (!vouchers || vouchers.length === 0) {
        this.els.appliedVouchers.innerHTML = '';
        return;
      }
      this.els.appliedVouchers.innerHTML = vouchers
        .map(v => {
          const code = this.escapeHtml(v.voucher_code || v.code || '');
          const codeAttr = this.escapeAttr(v.voucher_code || v.code || '');
          return `
                    <div class="cart-voucher__success">
                        <span><i class="fas fa-tag"></i> ${code}</span>
                        <button type="button" class="cart-voucher__remove" aria-label="Remove voucher"
                                data-action="remove-voucher"
                                data-code="${codeAttr}">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `;
        })
        .join('');
    },

    async updateQuantity(itemId, newQty) {
      if (newQty < 1) {
        this.removeItem(itemId);
        return;
      }
      try {
        const response = await fetch(`${this.endpoints.updateItem}${itemId}/`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken(),
          },
          body: JSON.stringify({ quantity: newQty }),
        });
        if (!response.ok) throw new Error('Update failed');
        await this.fetchCart();
      } catch (error) {
        console.error('Error updating quantity:', error);
      }
    },

    async removeItem(itemId) {
      try {
        const response = await fetch(`${this.endpoints.updateItem}${itemId}/`, {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': this.getCsrfToken(),
          },
        });
        if (!response.ok) throw new Error('Remove failed');
        await this.fetchCart();
      } catch (error) {
        console.error('Error removing item:', error);
      }
    },

    async applyVoucher() {
      const code = this.els.voucherInput?.value.trim();
      if (!code) return;

      this.els.voucherMessage.innerHTML = '';
      try {
        const response = await fetch(this.endpoints.applyVoucher, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCsrfToken(),
          },
          body: JSON.stringify({ code }),
        });
        const data = await response.json();
        if (response.ok && data.success !== false) {
          this.els.voucherInput.value = '';
          await this.fetchCart();
        } else {
          this.els.voucherMessage.innerHTML = `<div class="cart-voucher__error">${this.escapeHtml(data.message || data.detail || 'Invalid voucher code')}</div>`;
        }
      } catch (error) {
        console.error('Error applying voucher:', error);
        this.els.voucherMessage.innerHTML =
          '<div class="cart-voucher__error">Failed to apply voucher. Please try again.</div>';
      }
    },

    async removeVoucher(code) {
      try {
        const response = await fetch(
          `${this.endpoints.removeVoucher}${encodeURIComponent(code)}/`,
          {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': this.getCsrfToken(),
            },
          }
        );
        if (!response.ok) throw new Error('Remove voucher failed');
        await this.fetchCart();
      } catch (error) {
        console.error('Error removing voucher:', error);
      }
    },

    formatCurrency(amount) {
      const num = typeof amount === 'string' ? parseFloat(amount) : amount;
      const currency = window.__shopCurrency || 'USD';
      if (isNaN(num))
        return new Intl.NumberFormat(undefined, {
          style: 'currency',
          currency,
          minimumFractionDigits: 2,
        }).format(0);
      return new Intl.NumberFormat(undefined, {
        style: 'currency',
        currency,
        minimumFractionDigits: 2,
      }).format(num);
    },

    syncBadges(count) {
      if (window.MiniCart && typeof window.MiniCart.updateBadges === 'function') {
        window.MiniCart.updateBadges(count);
      }
    },

    getCsrfToken() {
      const meta = document.querySelector('meta[name="csrf-token"]');
      if (meta && meta.content) return meta.content;
      const input = document.querySelector('[name=csrfmiddlewaretoken]');
      if (input) return input.value;
      return '';
    },

    escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text || '';
      return div.innerHTML;
    },

    escapeAttr(text) {
      return (text || '')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    },
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => CartPage.init());
  } else {
    CartPage.init();
  }

  window.CartPage = CartPage;
})();
