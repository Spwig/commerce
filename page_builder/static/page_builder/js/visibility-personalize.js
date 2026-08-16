/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/*
 * Resolves deferred (per-visitor) visibility placeholders left in the cacheable
 * page shell. Each `[data-pb-defer]` marker is an element whose visibility
 * depends on per-visitor rules (auth, cart, device, precise geo) that must never
 * be evaluated into the shared/cached HTML. We ask the server — once, for all
 * placeholders — which the visitor should actually see, and swap them in.
 * Fail-closed: anything we can't confirm is removed, never shown.
 */
(function () {
  'use strict';

  // Bounds re-resolution when a personalized container inserts its own deferred
  // children (which arrive as fresh placeholders after the first pass).
  var MAX_PASSES = 5;

  function resolve(pass) {
    pass = pass || 0;
    var placeholders = Array.prototype.slice.call(document.querySelectorAll('[data-pb-defer]'));
    if (!placeholders.length || pass >= MAX_PASSES) {
      return;
    }

    var root = document.querySelector('[data-pb-page-id]');
    var pageId = root ? parseInt(root.getAttribute('data-pb-page-id'), 10) : NaN;
    if (isNaN(pageId)) {
      return;
    }

    var url =
      (root && root.getAttribute('data-pb-personalize-url')) || '/api/page-builder/personalize/';

    var ids = placeholders
      .map(function (el) {
        return parseInt(el.getAttribute('data-pb-defer'), 10);
      })
      .filter(function (n) {
        return !isNaN(n);
      });
    if (!ids.length) {
      return;
    }

    function removeAll() {
      placeholders.forEach(function (ph) {
        ph.remove();
      });
    }

    // Route slugs (present on category/product pages) let the server rebuild the
    // page-type context for deferred elements that need it.
    var body = { page_id: pageId, element_ids: ids };
    var categorySlug = root.getAttribute('data-pb-category-slug');
    var productSlug = root.getAttribute('data-pb-product-slug');
    if (categorySlug) {
      body.category_slug = categorySlug;
    }
    if (productSlug) {
      body.product_slug = productSlug;
    }

    // Endpoint is CSRF-exempt (read-only); the JSON body + same-origin
    // credentials are what it relies on. No CSRF token needed (and the cookie is
    // HttpOnly anyway, so JS can't read it).
    fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify(body),
    })
      .then(function (r) {
        return r.ok ? r.json() : Promise.reject(r.status);
      })
      .then(function (data) {
        var elements = (data && data.elements) || {};
        placeholders.forEach(function (ph) {
          var id = ph.getAttribute('data-pb-defer');
          var html = Object.prototype.hasOwnProperty.call(elements, id) ? elements[id] : null;
          if (html) {
            var tmp = document.createElement('div');
            tmp.innerHTML = html;
            var node = tmp.firstElementChild;
            if (node) {
              ph.replaceWith(node);
            } else {
              ph.remove();
            }
          } else {
            ph.remove();
          }
        });
        // A personalized container may have inserted its own deferred children
        // (new placeholders); resolve those too, bounded by MAX_PASSES.
        if (document.querySelector('[data-pb-defer]')) {
          resolve(pass + 1);
        }
      })
      .catch(function () {
        removeAll();
      });
  }

  // Wrap so the DOMContentLoaded event object isn't passed as `pass` (which would
  // break the MAX_PASSES bound on nested re-resolution).
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      resolve(0);
    });
  } else {
    resolve(0);
  }
})();
