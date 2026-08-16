/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Preview Visitor-State controls
 * Reloads the preview iframe with `preview_auth` / `preview_cart` query params so
 * the staff-only preview renders deferred (per-visitor) content as that visitor
 * would see it.
 */
(function () {
  'use strict';

  function setParam(name, value) {
    var iframe = document.getElementById('preview');
    if (!iframe) {
      return;
    }
    var url = new URL(iframe.src, window.location.origin);
    if (value) {
      url.searchParams.set(name, value);
    } else {
      url.searchParams.delete(name);
    }
    var loading = document.querySelector('.loading-indicator');
    if (loading) {
      loading.classList.add('active');
    }
    iframe.src = url.toString();
  }

  document.addEventListener('click', function (e) {
    var authBtn = e.target.closest('[data-action="set-preview-auth"]');
    if (!authBtn) {
      return;
    }
    e.preventDefault();
    setParam('preview_auth', authBtn.dataset.auth || '');
    document.querySelectorAll('#preview-visitor-state .pvs-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn === authBtn);
    });
  });

  var cartTimer = null;
  document.addEventListener('input', function (e) {
    var cartInput = e.target.closest('[data-action="set-preview-cart"]');
    if (!cartInput) {
      return;
    }
    clearTimeout(cartTimer); // debounce so we don't reload on every keystroke
    cartTimer = setTimeout(function () {
      setParam('preview_cart', cartInput.value);
    }, 500);
  });
})();
