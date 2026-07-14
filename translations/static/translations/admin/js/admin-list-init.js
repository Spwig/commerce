/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin list view initialization
 * Applies dynamic widths from data-width attributes (CSP-safe)
 */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-width]').forEach(function (el) {
    el.style.width = el.dataset.width + '%';
  });
});
