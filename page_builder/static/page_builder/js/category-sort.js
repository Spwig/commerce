/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Category Sort Select
 * Handles the sort-by select on category/collection pages.
 * Replaces inline onchange="window.location.href=..." handler.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('change', function (e) {
      const select = e.target.closest('[data-sort-select]');
      if (!select) return;

      const selected = select.options[select.selectedIndex];
      const url = selected && selected.dataset.url;
      if (url) {
        window.location.href = url;
      }
    });
  });
})();
