/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Order Change Form - Admin actions and interactions
 */
(function () {
  'use strict';

  function togglePaymentForm() {
    const form = document.getElementById('mark-paid-form');
    const btn = document.getElementById('show-payment-form-btn');
    if (form.classList.contains('d-none')) {
      form.classList.remove('d-none');
      btn.classList.add('d-none');
    } else {
      form.classList.add('d-none');
      btn.classList.remove('d-none');
    }
  }

  // Event delegation
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const action = btn.dataset.action;

    if (action === 'toggle-payment-form') {
      e.preventDefault();
      togglePaymentForm();
    }
  });

  // Handle form submissions with confirmation
  document.addEventListener('submit', async function (e) {
    const form = e.target;
    const submitBtn = document.activeElement;

    if (submitBtn && submitBtn.dataset.confirm) {
      e.preventDefault();
      if (await AdminModal.confirm(submitBtn.dataset.confirm)) {
        form.submit();
      }
    }
  });

  // Initialize on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function () {
    // Handle quick action forms
    const actionForms = document.querySelectorAll('.quick-actions form');
    actionForms.forEach(form => {
      form.addEventListener('submit', function (e) {
        const action = this.querySelector('input[name="action"]').value;
        const actionName = this.querySelector('button').textContent.trim();

        // Show loading state
        const button = this.querySelector('button');
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        button.disabled = true;
      });
    });
  });
})();
