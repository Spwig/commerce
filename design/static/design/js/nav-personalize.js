/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/*
 * Resolves deferred (per-visitor) navigation placeholders left in the cacheable
 * header/footer shell. Each `[data-pb-defer-nav-widget]` marker is a header or
 * footer widget whose visibility depends on per-visitor rules (auth, cart,
 * device, precise geo) that must never be evaluated into the shared/cached HTML.
 * We ask the server — once, for all placeholders — which the visitor should
 * actually see, and swap them in. Fail-closed: anything we can't confirm is
 * removed, never shown.
 */
(function () {
  'use strict';

  var ENDPOINT = '/api/design/personalize-nav/';
  // Bounds re-resolution if a personalized widget inserts its own markers.
  var MAX_PASSES = 3;

  function resolve(pass) {
    pass = pass || 0;
    var placeholders = Array.prototype.slice.call(
      document.querySelectorAll('[data-pb-defer-nav-widget]')
    );
    if (!placeholders.length || pass >= MAX_PASSES) {
      return;
    }

    var ids = placeholders
      .map(function (el) {
        return parseInt(el.getAttribute('data-pb-defer-nav-widget'), 10);
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

    // The market is URL-authoritative; the placeholders carry it so the server
    // evaluates shell region/language rules against the current market, not the
    // default (the POST URL has no /nz/ prefix). Server re-validates it.
    var market = placeholders[0].getAttribute('data-pb-market') || '';

    // Endpoint is CSRF-exempt (read-only); same-origin credentials carry the
    // session so per-visitor rules evaluate against the real visitor.
    fetch(ENDPOINT, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify({ widget_placement_ids: ids, market_slug: market }),
    })
      .then(function (r) {
        return r.ok ? r.json() : Promise.reject(r.status);
      })
      .then(function (data) {
        var widgets = (data && data.widgets) || {};
        placeholders.forEach(function (ph) {
          var id = ph.getAttribute('data-pb-defer-nav-widget');
          var html = Object.prototype.hasOwnProperty.call(widgets, id) ? widgets[id] : null;
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
        if (document.querySelector('[data-pb-defer-nav-widget]')) {
          resolve(pass + 1);
        }
      })
      .catch(function () {
        removeAll();
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      resolve(0);
    });
  } else {
    resolve(0);
  }
})();
