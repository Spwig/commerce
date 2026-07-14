/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Provider Account Change Form
 * Adds security hint text to encrypted credential fields.
 */

(function () {
  'use strict';

  const configEl = document.getElementById('provider-account-config');
  let i18n = {};
  if (configEl) {
    try {
      const config = JSON.parse(configEl.textContent);
      i18n = config.i18n || {};
    } catch (e) {
      // fall back to empty strings
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const secretFields = document.querySelectorAll('input[data-secret="true"]');
    secretFields.forEach(function (field) {
      const fieldRow = field.closest('.form-row');
      if (fieldRow && !fieldRow.querySelector('.shipping-credential-help')) {
        const helpText = document.createElement('div');
        helpText.className = 'help shipping-credential-help';
        helpText.innerHTML =
          '<i class="fas fa-lock" style="color: var(--warning-color); margin-right: 5px;"></i>' +
          (i18n.encryptedField || 'This field is encrypted and stored securely.');

        const fieldContainer = field.closest('div');
        if (fieldContainer) {
          fieldContainer.appendChild(helpText);
        }
      }
    });
  });
})();
