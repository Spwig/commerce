/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Sync Rollback & Init Handler
 * Handles rollback confirmation for sync and migration jobs,
 * and initializes progress bar widths from data attributes.
 * Used by the sync dashboard (change_list) and full migration results (step5).
 *
 * Expected data attributes on .js-rollback-btn:
 *   data-rollback-url   - POST endpoint for the rollback action
 *   data-csrf-token     - CSRF token for the request
 *   data-confirm-msg    - Confirmation message to display
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // Initialize progress bar widths from data attributes
    document.querySelectorAll('[data-initial-width]').forEach(function (el) {
      el.style.width = el.dataset.initialWidth + '%';
    });

    // Delegated rollback handler
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('.js-rollback-btn');
      if (!btn) return;

      e.preventDefault();

      const msg =
        btn.dataset.confirmMsg || 'Rollback this sync? This will restore the previous state.';
      const url = btn.dataset.rollbackUrl;
      const csrfToken = btn.dataset.csrfToken;

      if (!url || !csrfToken) return;

      AdminModal.confirm({
        message: msg,
        danger: true,
        confirmText: 'Rollback',
      }).then(function (confirmed) {
        if (!confirmed) return;
        fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
        }).then(function () {
          location.reload();
        });
      });
    });
  });
})();
