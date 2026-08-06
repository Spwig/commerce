/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Provider-agnostic capture of a reusable (off-session) payment method for
 * subscriptions.
 *
 * This helper names NO payment gateway. It asks the backend "begin-setup"
 * endpoint for a manifest-driven bundle {provider_key, handler_url,
 * sdk_dependencies, client_params} for whichever provider the merchant
 * configured, loads that provider's SDK + handler, and dispatches through the
 * SAME `window.PaymentHandlers[provider_key]` registry the checkout already uses
 * for charging — calling the handler's `initializeSetup(...)` entry (tokenize
 * without charging). It then finalises a PaymentToken via the generic
 * /api/subscriptions/tokens/ endpoint and attaches it to the subscription cart
 * items.
 *
 * Adding/removing a provider is entirely a component concern: ship a
 * checkout-handler.js that registers `window.PaymentHandlers[<slug>] = {
 * initialize(...), initializeSetup(...) }`. No edit to this file is ever needed.
 */
(function () {
  'use strict';

  var ENDPOINTS = {
    beginSetup: '/api/subscriptions/tokens/begin-setup/',
    createToken: '/api/subscriptions/tokens/',
    attachToken: function (itemId) {
      return '/api/cart/items/' + encodeURIComponent(itemId) + '/attach-subscription-token/';
    },
  };

  var _loaded = {}; // src -> Promise, so each SDK/handler loads at most once

  function loadScript(src) {
    if (!src) return Promise.resolve();
    if (_loaded[src]) return _loaded[src];
    _loaded[src] = new Promise(function (resolve, reject) {
      var existing = document.querySelector('script[data-sps-src="' + src + '"]');
      if (existing && existing.dataset.spsLoaded === 'true') {
        resolve();
        return;
      }
      var el = document.createElement('script');
      el.src = src;
      el.async = true;
      el.dataset.spsSrc = src;
      el.addEventListener('load', function () {
        el.dataset.spsLoaded = 'true';
        resolve();
      });
      el.addEventListener('error', function () {
        reject(new Error('Failed to load script: ' + src));
      });
      document.head.appendChild(el);
    });
    return _loaded[src];
  }

  function getCsrfToken() {
    // Reuse the checkout's helper when present; fall back to the cookie.
    if (window.SpwigCheckout && typeof window.SpwigCheckout.getCSRFToken === 'function') {
      return window.SpwigCheckout.getCSRFToken();
    }
    var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : '';
  }

  function postJson(url, body) {
    return fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify(body || {}),
    }).then(function (resp) {
      return resp.json().then(function (data) {
        return { ok: resp.ok, status: resp.status, data: data };
      });
    });
  }

  /**
   * Capture a reusable payment method and bind it to the subscription cart
   * items.
   *
   * @param {Object} opts
   * @param {string} opts.providerAccountId  The merchant's selected provider account id.
   * @param {Array<number|string>} opts.itemIds  Subscription cart item ids to attach the token to.
   * @param {HTMLElement} opts.container  Mount point for the provider's setup UI.
   * @returns {Promise<Object>} resolves to one of:
   *   { supported: false, providerKey }                        // gateway has no setup handler yet
   *   { supported: true, success: true, tokenId }              // captured + attached
   *   { supported: true, success: false, error }               // capture/attach failed
   */
  function capture(opts) {
    opts = opts || {};
    var providerAccountId = opts.providerAccountId;
    var itemIds = opts.itemIds || [];
    var container = opts.container;

    if (!providerAccountId) {
      return Promise.reject(new Error('providerAccountId is required'));
    }

    return postJson(ENDPOINTS.beginSetup, { provider_account_id: providerAccountId }).then(
      function (res) {
        if (!res.ok) {
          throw new Error((res.data && res.data.error) || 'begin-setup failed');
        }
        var bundle = res.data || {};
        if (!bundle.supported) {
          // Gateway hasn't shipped a setup handler — caller falls back to saved
          // tokens or shows a clear message. Never a hard failure.
          return { supported: false, providerKey: bundle.provider_key };
        }

        var deps = bundle.sdk_dependencies || [];
        var chain = Promise.resolve();
        deps.forEach(function (sdkUrl) {
          chain = chain.then(function () {
            return loadScript(sdkUrl);
          });
        });
        return chain
          .then(function () {
            return loadScript(bundle.handler_url);
          })
          .then(function () {
            var handler = window.PaymentHandlers && window.PaymentHandlers[bundle.provider_key];
            if (!handler || typeof handler.initializeSetup !== 'function') {
              // Handler script loaded but exposes no setup entry point — treat
              // as unsupported so the caller degrades gracefully.
              return { supported: false, providerKey: bundle.provider_key };
            }
            return new Promise(function (resolve) {
              var onToken = function (paymentMethodData) {
                finalizeToken(providerAccountId, paymentMethodData, itemIds)
                  .then(function (out) {
                    resolve(Object.assign({ supported: true }, out));
                  })
                  .catch(function (err) {
                    resolve({ supported: true, success: false, error: err.message });
                  });
              };
              var onError = function (message) {
                resolve({ supported: true, success: false, error: message || 'setup failed' });
              };
              // The provider-specific handler tokenizes WITHOUT charging and
              // hands back opaque provider payment_method_data via onToken.
              handler.initializeSetup(bundle, container, onToken, onError);
            });
          });
      }
    );
  }

  function finalizeToken(providerAccountId, paymentMethodData, itemIds) {
    return postJson(ENDPOINTS.createToken, {
      provider_account_id: providerAccountId,
      payment_method_data: paymentMethodData,
      set_as_default: true,
    }).then(function (res) {
      if (!res.ok) {
        throw new Error((res.data && res.data.error) || 'Could not save payment method');
      }
      var tokenId = res.data && res.data.token_id;
      if (!tokenId) {
        throw new Error('No token returned');
      }
      // Attach the reusable token to each subscription cart item so checkout's
      // server-side gate passes and renewals have a method to charge.
      var chain = Promise.resolve();
      (itemIds || []).forEach(function (itemId) {
        chain = chain.then(function () {
          return postJson(ENDPOINTS.attachToken(itemId), { payment_token_id: tokenId });
        });
      });
      return chain.then(function () {
        return { success: true, tokenId: tokenId };
      });
    });
  }

  window.SubscriptionPaymentSetup = { capture: capture, loadScript: loadScript };
})();
