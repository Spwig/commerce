/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Frontend Utilities
 * Core JavaScript utilities for the frontend: lazy loading, notifications, cart, express checkout
 */
(function () {
  'use strict';

  // === Shop Currency (from CSP-safe JSON island) ===
  const currencyEl = document.getElementById('shop-currency-config');
  if (currencyEl) {
    try {
      window.__shopCurrency = JSON.parse(currencyEl.textContent).currency;
    } catch (e) {
      /* ignore parse errors */
    }
  }

  // === Shop Default Country (from CSP-safe JSON island) ===
  const countryEl = document.getElementById('shop-country-config');
  if (countryEl) {
    try {
      window.shopDefaultCountry = JSON.parse(countryEl.textContent).country;
    } catch (e) {
      /* ignore parse errors */
    }
  }

  // === Lazy Loading for Images ===
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove('lazy');
          imageObserver.unobserve(img);
        }
      });
    });

    // Initialize when DOM is ready
    function initLazyImages() {
      document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
      });
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initLazyImages);
    } else {
      initLazyImages();
    }
  }

  // === CSRF Token Helper ===
  // With CSRF_COOKIE_HTTPONLY=True, JS cannot read the csrftoken cookie.
  // Prefer meta tag (set in base.html) → hidden form input → cookie fallback.
  window.getCSRFToken = function () {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input) return input.value;
    return window.getCookie('csrftoken') || '';
  };

  window.getCookie = function (name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  // === Merchant Translation Helper ===
  // Reads translations from JSON script tag if available
  let uiTranslations = {};
  const translationsElement = document.getElementById('ui-translations');
  if (translationsElement) {
    try {
      uiTranslations = JSON.parse(translationsElement.textContent);
    } catch (e) {
      console.warn('Failed to parse UI translations:', e);
    }
  }

  window._mt = function (key, fallback) {
    return uiTranslations[key] || fallback || key;
  };

  // === Notification System ===
  // Storefront-only toast. Uses `.toast` / `.toast--{type}` styles from
  // page_builder/css/frontend-base.css. Do NOT delegate to AdminModal —
  // that helper is only loaded in the admin bundle.
  window.showNotification = function (message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `toast toast--${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    requestAnimationFrame(() => {
      notification.classList.add('toast--visible');
    });

    setTimeout(() => {
      notification.classList.remove('toast--visible');
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  };

  // === Add to Cart Functionality ===
  window.addToCart = function (productId, quantity = 1, variantId = null) {
    const csrfToken = window.getCSRFToken();

    fetch('/api/cart/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        product_id: productId,
        variant_id: variantId,
        quantity: quantity,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Open mini cart with updated data (MiniCart provided by mini-cart.js)
          if (window.MiniCart) {
            window.MiniCart.open(data);
          }
          window.showNotification(
            window._mt('product_added_to_cart', 'Product added to cart!'),
            'success'
          );
        } else {
          window.showNotification(
            data.message || window._mt('error_adding_to_cart', 'Error adding to cart'),
            'error'
          );
        }
      })
      .catch(error => {
        window.showNotification(
          window._mt('error_adding_to_cart', 'Error adding to cart'),
          'error'
        );
      });
  };

  // === Performance: Preload on Hover ===
  document.addEventListener(
    'mouseover',
    function (e) {
      if (e.target.tagName === 'A' && e.target.href) {
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = e.target.href;
        document.head.appendChild(link);
      }
    },
    { once: true }
  );

  // === Express Checkout ===
  window.expressCheckout = function (providerSlug, methodSlug) {
    const csrfToken = window.getCSRFToken();

    // Show loading state
    window.showNotification(
      window._mt('initializing_express_checkout', 'Initializing express checkout...'),
      'info'
    );

    // Build the express checkout URL dynamically based on provider
    const expressCheckoutUrl = `/api/payment/providers/${providerSlug}/express-checkout/`;

    // Initiate express checkout session
    fetch(expressCheckoutUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        method: methodSlug,
        cart_token: window.getCookie('cart_token') || null,
      }),
    })
      .then(response => {
        // Handle 404 gracefully - express checkout not yet implemented for this provider
        if (response.status === 404) {
          // Fallback to standard checkout
          window.showNotification(
            window._mt('redirecting_to_checkout', 'Redirecting to checkout...'),
            'info'
          );
          window.location.href = '/checkout/';
          return null;
        }
        return response.json();
      })
      .then(data => {
        if (!data) return; // Already handled 404 redirect

        if (data.success) {
          // Handle based on checkout type
          if (data.redirect_url) {
            // Redirect to hosted checkout
            window.location.href = data.redirect_url;
          } else if (data.client_secret) {
            // Integrated checkout - init payment sheet
            window.initPaymentSheet(providerSlug, methodSlug, data);
          }
        } else {
          window.showNotification(
            data.message || window._mt('express_checkout_failed', 'Express checkout failed'),
            'error'
          );
        }
      })
      .catch(error => {
        console.error('Express checkout error:', error);
        // Fallback to standard checkout on error
        window.showNotification(
          window._mt('redirecting_to_checkout', 'Redirecting to checkout...'),
          'info'
        );
        window.location.href = '/checkout/';
      });
  };

  // === Initialize Payment Sheet (provider-specific implementation) ===
  window.initPaymentSheet = function (provider, method, data) {
    // This will be implemented per-provider
    // For now, redirect to standard checkout
    console.log('Payment sheet init:', provider, method, data);
    window.location.href = '/checkout/';
  };

  // === Auto-Submit Form Selects ===
  // Replaces inline onchange="this.form.submit()" on <select data-auto-submit>
  document.addEventListener('change', e => {
    const select = e.target.closest('select[data-auto-submit]');
    if (select && select.form) {
      select.form.submit();
    }
  });

  // === Event Delegation for Express Checkout Buttons ===
  document.addEventListener('click', e => {
    const expressBtn = e.target.closest('[data-action="express-checkout"]');
    if (expressBtn) {
      e.preventDefault();
      const provider = expressBtn.dataset.provider;
      const method = expressBtn.dataset.method;
      if (provider && method) {
        window.expressCheckout(provider, method);
      }
    }

    // Handle data-onclick attributes (CSP-safe alternative to inline onclick)
    const onclickBtn = e.target.closest('[data-onclick]');
    if (onclickBtn) {
      const onclick = onclickBtn.dataset.onclick.trim();

      // Only allow safe, common patterns
      if (onclick === 'location.reload()' || onclick === 'window.location.reload()') {
        e.preventDefault();
        window.location.reload();
      } else if (onclick === 'history.back()' || onclick === 'window.history.back()') {
        e.preventDefault();
        window.history.back();
      } else if (onclick.match(/^window\.scrollTo\(0,\s*0\)$/)) {
        e.preventDefault();
        window.scrollTo(0, 0);
      } else if (onclick === 'window.print()') {
        e.preventDefault();
        window.print();
      } else {
        // Unsupported pattern - log warning
        console.warn('Unsupported data-onclick pattern:', onclick);
        console.warn('For security reasons, only common navigation patterns are supported.');
      }
    }
  });
})();
