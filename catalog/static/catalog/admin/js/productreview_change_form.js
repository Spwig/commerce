/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * ProductReview Change Form JavaScript
 * Wires the header save buttons to the form.
 * Tab switching is handled by the global AdminTabs utility (admin-tabs.js).
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('productreview_form');
    if (!form) return;

    // Mark/unmark review images for deletion (applied on save).
    form.querySelectorAll('.review-image-delete').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const thumb = btn.closest('.review-image-thumb');
        const input = thumb ? thumb.querySelector('.review-image-delete-input') : null;
        if (!input) return;
        input.checked = !input.checked;
        thumb.classList.toggle('marked', input.checked);
      });
    });

    const saveContinueBtn = document.getElementById('pr-save-continue-btn');
    if (saveContinueBtn) {
      saveContinueBtn.addEventListener('click', function () {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = '_continue';
        input.value = '1';
        form.appendChild(input);
        form.submit();
      });
    }

    const saveBtn = document.getElementById('pr-save-btn');
    if (saveBtn) {
      saveBtn.addEventListener('click', function () {
        form.submit();
      });
    }
  });
})();
