/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // Initialize progress bar widths from data attributes (CSP-compliant)
    document.querySelectorAll('.migration-progress-bar[data-width]').forEach(function (bar) {
      bar.style.width = bar.dataset.width + '%';
    });
  });

  // Confirm-then-navigate, for actions whose target renders its own confirmation
  // page on GET (Rollback). Do not use this for state-changing endpoints.
  document.addEventListener('click', async function (e) {
    const link = e.target.closest('[data-action="confirm-navigate"]');
    if (!link) return;
    e.preventDefault();
    const msg = link.dataset.confirmMsg || 'Are you sure?';
    if (await AdminModal.confirm(msg)) {
      window.location.href = link.href;
    }
  });

  // Confirm-then-submit, for state-changing actions posted as CSRF-protected
  // forms (Retry, Cancel, Delete).
  document.addEventListener('click', async function (e) {
    const button = e.target.closest('[data-action="confirm-submit"]');
    if (!button) return;
    const form = button.closest('form');
    if (!form || form.dataset.confirmed === 'true') return;
    e.preventDefault();
    const msg = button.dataset.confirmMsg || 'Are you sure?';
    if (await AdminModal.confirm(msg)) {
      form.dataset.confirmed = 'true';
      button.disabled = true;
      form.submit();
    }
  });
})();
