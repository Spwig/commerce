/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Token Management
 * Handles revoke confirmation for sync tokens.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('[data-action="revoke-token"]');
      if (!btn) return;

      e.preventDefault();
      const tokenName = btn.getAttribute('data-token-name') || '';
      const form = btn.closest('form');
      if (!form) return;

      const msg = tokenName
        ? 'Revoke token "' + tokenName + '"? Any connections using it will stop working.'
        : 'Revoke this token? Any connections using it will stop working.';

      AdminModal.confirm({
        message: msg,
        danger: true,
        confirmText: 'Revoke',
      }).then(function (confirmed) {
        if (confirmed) {
          form.submit();
        }
      });
    });
  });
})();
