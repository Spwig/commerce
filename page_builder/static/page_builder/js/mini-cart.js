/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Mini-Cart Module
 *
 * Handles the slide-out cart panel functionality.
 * Provides cart operations: open/close, fetch, update quantity, remove items.
 *
 * Usage:
 * - Add `data-open-mini-cart` attribute to any element to trigger opening
 * - Add `data-cart-count` attribute to badges that should show cart count
 * - Call MiniCart.open(data) directly to open with cart data
 * - Call window.openMiniCart(data) for backward compatibility
 */
(function () {
  'use strict';

  const MiniCart = {
    // DOM element references
    overlay: null,
    panel: null,
    itemsContainer: null,
    emptyState: null,
    footer: null,
    countEl: null,
    subtotalEl: null,

    // API endpoints (no language prefix per rules_llm.md)
    endpoints: {
      get: '/api/cart/get/',
      update: '/api/cart/update/',
      remove: '/api/cart/remove/',
      summary: '/api/cart/summary/',
      add: '/api/cart/add/',
      recommendations: '/api/cart/empty-recommendations/',
    },

    /**
     * Initialize the mini-cart
     */
    init() {
      this.cacheElements();
      this.bindEvents();
      this.fetchInitialCount();
      this.initExpressCheckoutButtons();
    },

    /**
     * Cache DOM element references
     */
    cacheElements() {
      this.overlay = document.getElementById('mini-cart-overlay');
      this.panel = document.getElementById('mini-cart');
      this.itemsContainer = document.getElementById('mini-cart-items');
      this.emptyState = document.getElementById('mini-cart-empty');
      this.footer = document.getElementById('mini-cart-footer');
      this.countEl = document.getElementById('mini-cart-count');
      this.subtotalEl = document.getElementById('mini-cart-subtotal');
    },

    /**
     * Bind event listeners
     */
    bindEvents() {
      // Overlay click to close
      if (this.overlay) {
        this.overlay.addEventListener('click', () => this.close());
      }

      // Close button
      const closeBtn = document.getElementById('mini-cart-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => this.close());
      }

      // Escape key to close
      document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && this.isOpen()) {
          this.close();
        }
      });

      // Cart widget clicks (delegate to document for dynamic elements)
      document.addEventListener('click', e => {
        const cartTrigger = e.target.closest('[data-open-mini-cart]');
        if (cartTrigger) {
          e.preventDefault();
          this.open();
        }
      });

      // Load recommendations for empty cart
      this.loadRecommendations();
    },

    /**
     * Check if mini-cart is currently open
     */
    isOpen() {
      return this.panel?.classList.contains('open');
    },

    /**
     * Open the mini-cart panel
     * @param {Object|null} cartData - Optional cart data to display immediately
     */
    open(cartData = null) {
      if (!this.panel || !this.overlay) return;

      this.panel.classList.add('open');
      this.panel.setAttribute('aria-hidden', 'false');
      this.overlay.classList.add('active');
      document.body.style.overflow = 'hidden';

      if (cartData) {
        this.update(cartData);
      } else {
        this.fetch();
      }
    },

    /**
     * Close the mini-cart panel
     */
    close() {
      if (!this.panel || !this.overlay) return;

      this.panel.classList.remove('open');
      this.panel.setAttribute('aria-hidden', 'true');
      this.overlay.classList.remove('active');
      document.body.style.overflow = '';
    },

    /**
     * Fetch cart data from API
     */
    fetch() {
      fetch(this.endpoints.get, {
        headers: { Accept: 'application/json' },
      })
        .then(response => response.json())
        .then(data => this.update(data))
        .catch(error => console.error('Error fetching cart:', error));
    },

    /**
     * Fetch initial cart count on page load (lightweight endpoint)
     */
    fetchInitialCount() {
      fetch(this.endpoints.summary, {
        headers: { Accept: 'application/json' },
      })
        .then(response => response.json())
        .then(data => {
          const count = data.item_count || data.cart_count || 0;
          this.updateBadges(count);
        })
        .catch(() => {
          // Silently fail - badge will show 0
        });
    },

    /**
     * Update the mini-cart display with cart data
     * @param {Object} data - Cart data from API
     */
    update(data) {
      if (!data) return;

      const count = data.item_count || data.cart_count || 0;

      // Update count badges
      this.updateBadges(count);

      // Update panel count
      if (this.countEl) {
        this.countEl.textContent = count;
      }

      // Toggle empty/filled state
      if (count === 0) {
        if (this.emptyState) this.emptyState.style.display = 'block';
        if (this.itemsContainer) this.itemsContainer.style.display = 'none';
        if (this.footer) this.footer.style.display = 'none';
      } else {
        if (this.emptyState) this.emptyState.style.display = 'none';
        if (this.itemsContainer) this.itemsContainer.style.display = 'block';
        if (this.footer) this.footer.style.display = 'block';

        // Render items
        this.renderItems(data.items || []);

        // Update subtotal
        if (this.subtotalEl) {
          this.subtotalEl.textContent = data.subtotal_formatted || data.subtotal || '0.00';
        }
      }

      // Notify other components (e.g. checkout) that the cart changed
      document.dispatchEvent(new CustomEvent('cart:updated', { detail: data }));
    },

    /**
     * Update all cart count badges on the page
     * @param {number} count - Current cart item count
     */
    updateBadges(count) {
      // Header cart count badges using data attribute (preferred)
      document.querySelectorAll('[data-cart-count]').forEach(badge => {
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
      });

      // Legacy class-based badges (backward compatibility)
      document
        .querySelectorAll('.header__cart-count, .cart-count, .widget-cart-count')
        .forEach(badge => {
          badge.textContent = count;
          badge.style.display = count > 0 ? 'flex' : 'none';
        });
    },

    /**
     * Render cart items with intelligent DOM diffing to prevent image reload
     * @param {Array} items - Array of cart items
     */
    renderItems(items) {
      if (!this.itemsContainer) return;

      // Build a map of current items by ID for quick lookup
      const currentItems = new Map();
      this.itemsContainer.querySelectorAll('.cart-item').forEach(el => {
        const itemId = el.getAttribute('data-item-id');
        if (itemId) currentItems.set(itemId, el);
      });

      // Build a map of new items
      const newItemIds = new Set(items.map(item => String(item.id)));

      // Remove items that no longer exist
      currentItems.forEach((el, itemId) => {
        if (!newItemIds.has(itemId)) {
          el.remove();
          currentItems.delete(itemId);
        }
      });

      // Update existing items or add new ones
      items.forEach((item, index) => {
        const itemId = String(item.id);
        const existingEl = currentItems.get(itemId);

        if (existingEl) {
          // Update existing item - preserve image element
          this.updateItemElement(existingEl, item);

          // Ensure correct order
          const currentIndex = Array.from(this.itemsContainer.children).indexOf(existingEl);
          if (currentIndex !== index) {
            if (index >= this.itemsContainer.children.length) {
              this.itemsContainer.appendChild(existingEl);
            } else {
              this.itemsContainer.insertBefore(existingEl, this.itemsContainer.children[index]);
            }
          }
        } else {
          // Create new item
          const newEl = this.createItemElement(item);
          if (index >= this.itemsContainer.children.length) {
            this.itemsContainer.appendChild(newEl);
          } else {
            this.itemsContainer.insertBefore(newEl, this.itemsContainer.children[index]);
          }
        }
      });

      // Rebind event handlers
      this.bindItemActions();
    },

    /**
     * Update an existing cart item element (preserves images)
     * @param {HTMLElement} element - Existing cart item element
     * @param {Object} item - Item data
     */
    updateItemElement(element, item) {
      // Update image src only if changed
      const img = element.querySelector('.cart-item__image');
      const newSrc = item.image_url || '/static/img/placeholder-product-thumb.png';
      if (img && img.src !== newSrc) {
        img.src = newSrc;
        img.alt = this.escapeHtml(item.name);
      }

      // Update quantity
      const qtyValue = element.querySelector('.cart-item__qty-value');
      if (qtyValue) qtyValue.textContent = item.quantity;

      // Update quantity button data attributes
      const decreaseBtn = element.querySelector('[data-action="decrease"]');
      if (decreaseBtn) decreaseBtn.setAttribute('data-quantity', item.quantity - 1);

      const increaseBtn = element.querySelector('[data-action="increase"]');
      if (increaseBtn) increaseBtn.setAttribute('data-quantity', item.quantity + 1);

      // Update price (use item total)
      const priceEl = element.querySelector('.cart-item__price');
      if (priceEl) {
        priceEl.textContent = item.item_total_formatted || item.price_formatted || item.price;
      }

      // Update just_added class
      if (item.just_added) {
        element.classList.add('cart-item--added');
      } else {
        element.classList.remove('cart-item--added');
      }

      // Update variant name if it exists
      const variantEl = element.querySelector('.cart-item__variant');
      if (item.variant_name) {
        if (variantEl) {
          variantEl.textContent = this.escapeHtml(item.variant_name);
        } else {
          const detailsDiv = element.querySelector('.cart-item__details');
          const nameLink = detailsDiv?.querySelector('.cart-item__name');
          if (nameLink && detailsDiv) {
            const variantP = document.createElement('p');
            variantP.className = 'cart-item__variant';
            variantP.textContent = this.escapeHtml(item.variant_name);
            nameLink.insertAdjacentElement('afterend', variantP);
          }
        }
      } else if (variantEl) {
        variantEl.remove();
      }
    },

    /**
     * Create a new cart item element
     * @param {Object} item - Item data
     * @returns {HTMLElement} - New cart item element
     */
    createItemElement(item) {
      // Nested components HTML for configurable/bundle products
      let componentsHtml = '';
      if (item.is_configurable && item.components && item.components.length > 0) {
        componentsHtml = `
                    <div class="cart-item__components">
                        ${item.components
                          .map(comp => {
                            const compImage = comp.image_url || '';
                            const compImageHtml = compImage
                              ? `<img src="${compImage}" alt="" class="cart-item__component-image" loading="lazy">`
                              : '<div class="cart-item__component-image cart-item__component-image--placeholder"><i class="fas fa-box"></i></div>';
                            return `
                            <div class="cart-item__component">
                                ${compImageHtml}
                                <div class="cart-item__component-info">
                                    <span class="cart-item__component-name">${this.escapeHtml(comp.name)}</span>
                                    ${comp.variant_name ? `<span class="cart-item__component-variant">${this.escapeHtml(comp.variant_name)}</span>` : ''}
                                </div>
                                <span class="cart-item__component-qty">&times;${comp.quantity}</span>
                            </div>`;
                          })
                          .join('')}
                    </div>
                `;
      }

      const template = `
                <div class="cart-item ${item.just_added ? 'cart-item--added' : ''}" data-item-id="${item.id}">
                    <img src="${item.image_url || '/static/img/placeholder-product-thumb.png'}"
                         alt="${this.escapeHtml(item.name)}"
                         class="cart-item__image">
                    <div class="cart-item__details">
                        <a href="${item.url || '#'}" class="cart-item__name">${this.escapeHtml(item.name)}</a>
                        ${item.variant_name ? `<p class="cart-item__variant">${this.escapeHtml(item.variant_name)}</p>` : ''}
                        ${componentsHtml}
                        <p class="cart-item__price">${item.item_total_formatted || item.price_formatted || item.price}</p>
                        <div class="cart-item__actions">
                            <div class="cart-item__quantity">
                                <button type="button"
                                        class="cart-item__qty-btn"
                                        data-action="decrease"
                                        data-item-id="${item.id}"
                                        data-quantity="${item.quantity - 1}"
                                        aria-label="Decrease quantity">
                                    <i class="fas fa-minus"></i>
                                </button>
                                <span class="cart-item__qty-value">${item.quantity}</span>
                                <button type="button"
                                        class="cart-item__qty-btn"
                                        data-action="increase"
                                        data-item-id="${item.id}"
                                        data-quantity="${item.quantity + 1}"
                                        aria-label="Increase quantity">
                                    <i class="fas fa-plus"></i>
                                </button>
                            </div>
                            <button type="button"
                                    class="cart-item__remove"
                                    data-action="remove"
                                    data-item-id="${item.id}"
                                    aria-label="Remove item">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `;

      const div = document.createElement('div');
      div.innerHTML = template;
      return div.firstElementChild;
    },

    /**
     * Bind actions on cart items (quantity buttons, remove)
     */
    bindItemActions() {
      if (!this.itemsContainer) return;

      this.itemsContainer.querySelectorAll('[data-action]').forEach(btn => {
        btn.addEventListener('click', e => {
          e.preventDefault();
          const action = btn.dataset.action;
          const itemId = parseInt(btn.dataset.itemId, 10);
          const quantity = parseInt(btn.dataset.quantity, 10);

          if (action === 'remove' || quantity < 1) {
            this.removeItem(itemId);
          } else {
            this.updateQuantity(itemId, quantity);
          }
        });
      });
    },

    /**
     * Update item quantity
     * @param {number} itemId - Cart item ID
     * @param {number} newQuantity - New quantity value
     */
    updateQuantity(itemId, newQuantity) {
      if (newQuantity < 1) {
        this.removeItem(itemId);
        return;
      }

      fetch(this.endpoints.update, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken(),
        },
        body: JSON.stringify({
          item_id: itemId,
          quantity: newQuantity,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            this.update(data);
          }
        })
        .catch(error => console.error('Error updating quantity:', error));
    },

    /**
     * Remove item from cart
     * @param {number} itemId - Cart item ID to remove
     */
    removeItem(itemId) {
      fetch(this.endpoints.remove, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken(),
        },
        body: JSON.stringify({ item_id: itemId }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            this.update(data);
          }
        })
        .catch(error => console.error('Error removing item:', error));
    },

    /**
     * Load intelligent product recommendations for empty cart state
     * Renders labeled sections: Recently Viewed, On Sale, Trending
     */
    loadRecommendations() {
      const container = document.getElementById('recommendations-list');
      if (!container) return;

      // Show loading state
      container.innerHTML =
        '<div class="mini-cart__recommendations-loading"><div class="mini-cart__spinner"></div></div>';

      fetch(this.endpoints.recommendations + '?limit=6')
        .then(response => response.json())
        .then(data => {
          if (data.sections && data.sections.length > 0) {
            // Render sections with labels
            container.innerHTML = data.sections
              .map(
                section => `
                        <div class="mini-cart__recommendation-section" data-type="${section.type}">
                            <h4 class="mini-cart__section-title">${this.escapeHtml(section.label)}</h4>
                            <div class="mini-cart__recommendations-list">
                                ${section.products.map(product => this.renderRecommendationItem(product)).join('')}
                            </div>
                        </div>
                    `
              )
              .join('');

            // Bind quick-add buttons
            this.bindQuickAddButtons();
          } else {
            // No recommendations available
            container.innerHTML = '';
          }
        })
        .catch(() => {
          // Silently fail - recommendations are optional
          container.innerHTML = '';
        });
    },

    /**
     * Render a single recommendation item with quick-add button
     * @param {Object} product - Product data
     * @returns {string} HTML string
     */
    renderRecommendationItem(product) {
      const saleTag = product.on_sale ? '<span class="recommendation-item__badge">Sale</span>' : '';

      const priceDisplay =
        product.on_sale && product.sale_price_formatted
          ? `<span class="recommendation-item__price recommendation-item__price--sale">${product.sale_price_formatted}</span>
                   <span class="recommendation-item__price recommendation-item__price--original">${product.price_formatted}</span>`
          : `<span class="recommendation-item__price">${product.price_formatted}</span>`;

      return `
                <div class="recommendation-item" data-product-id="${product.id}">
                    <a href="${product.url}" class="recommendation-item__link">
                        <img src="${product.image_url || '/static/img/placeholder-product-thumb.png'}"
                             alt="${this.escapeHtml(product.name)}"
                             class="recommendation-item__image"
                             loading="lazy">
                        <div class="recommendation-item__info">
                            <span class="recommendation-item__name">${this.escapeHtml(product.name)}</span>
                            <div class="recommendation-item__prices">
                                ${priceDisplay}
                                ${saleTag}
                            </div>
                        </div>
                    </a>
                    <button type="button"
                            class="recommendation-item__quick-add"
                            data-product-id="${product.id}"
                            aria-label="Add to cart"
                            title="Add to cart">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
            `;
    },

    /**
     * Bind click handlers for quick-add buttons
     */
    bindQuickAddButtons() {
      const container = document.getElementById('recommendations-list');
      if (!container) return;

      container.querySelectorAll('.recommendation-item__quick-add').forEach(btn => {
        btn.addEventListener('click', e => {
          e.preventDefault();
          e.stopPropagation();
          const productId = parseInt(btn.dataset.productId, 10);
          if (productId) {
            this.quickAddToCart(productId, btn);
          }
        });
      });
    },

    /**
     * Quick add product to cart from recommendations
     * @param {number} productId - Product ID to add
     * @param {HTMLElement} button - The button element
     */
    quickAddToCart(productId, button) {
      // Show loading state
      button.classList.add('loading');
      button.disabled = true;

      fetch(this.endpoints.add, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCsrfToken(),
        },
        body: JSON.stringify({
          product_id: productId,
          quantity: 1,
        }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Update cart display
            this.update(data);

            // Show success feedback
            button.innerHTML = '<i class="fas fa-check"></i>';
            button.classList.add('success');

            // Reset button after delay
            setTimeout(() => {
              button.innerHTML = '<i class="fas fa-plus"></i>';
              button.classList.remove('success', 'loading');
              button.disabled = false;
            }, 1500);
          } else {
            // Show error
            button.classList.remove('loading');
            button.disabled = false;
            console.error('Add to cart failed:', data.message);
          }
        })
        .catch(error => {
          button.classList.remove('loading');
          button.disabled = false;
          console.error('Error adding to cart:', error);
        });
    },

    /**
     * Initialize express checkout buttons (check JS-based availability)
     */
    initExpressCheckoutButtons() {
      // CSP-safe feature check registry (no eval)
      const FEATURE_CHECKS = {
        'apple-pay': () => window.ApplePaySession && ApplePaySession.canMakePayments(),
      };

      // Check for Apple Pay (direct)
      if (FEATURE_CHECKS['apple-pay']()) {
        const applePayBtn = document.getElementById('mc-apple-pay');
        if (applePayBtn) applePayBtn.style.display = 'flex';
      }

      // Find all buttons with data-js-check attribute
      const buttons = document.querySelectorAll('[data-js-check]');
      buttons.forEach(button => {
        const checkName = button.dataset.jsCheck;
        const checker = FEATURE_CHECKS[checkName];
        try {
          if (checker && checker()) {
            button.style.display = '';
          }
        } catch (e) {
          console.debug('Express checkout check failed:', checkName, e);
        }
      });
    },

    /**
     * Get CSRF token from cookie
     * @returns {string|null} CSRF token value
     */
    getCsrfToken() {
      const meta = document.querySelector('meta[name="csrf-token"]');
      if (meta && meta.content) return meta.content;
      const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
      const cookieValue = tokenElement ? tokenElement.value : null;

      return cookieValue;
    },

    /**
     * Escape HTML to prevent XSS
     * @param {string} text - Text to escape
     * @returns {string} Escaped HTML string
     */
    escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    },
  };

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => MiniCart.init());
  } else {
    MiniCart.init();
  }

  // Expose to global scope for addToCart and other integrations
  window.MiniCart = MiniCart;

  // Legacy function for backward compatibility
  window.openMiniCart = function (data) {
    MiniCart.open(data);
  };
})();
