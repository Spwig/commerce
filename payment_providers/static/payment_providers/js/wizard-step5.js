/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Payment Provider Wizard Step 5: Configure
 * Handles webhook URL copying (native Clipboard API), default checkbox
 * confirmation, and form validation.
 */

(function () {
  'use strict';

  const configEl = document.getElementById('wizard-step5-config');
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
    // Initialize copy buttons using native Clipboard API
    initializeCopyButtons();

    // Handle default checkbox - only one can be default
    const defaultCheckbox = document.getElementById('id_is_default');
    if (defaultCheckbox) {
      defaultCheckbox.addEventListener('change', async function () {
        if (this.checked) {
          const confirmMsg =
            i18n.defaultConfirm ||
            'Setting this as the default will remove the default status from any other payment provider. Continue?';
          if (!(await AdminModal.confirm(confirmMsg))) {
            this.checked = false;
          }
        }
      });
    }

    // Validate form before submission
    const form = document.getElementById('configure-form');
    if (form) {
      form.addEventListener('submit', function (e) {
        const isActive = document.getElementById('id_is_active').checked;
        const isDefault = document.getElementById('id_is_default').checked;

        if (isDefault && !isActive) {
          e.preventDefault();
          AdminModal.alert({
            message:
              i18n.cannotSetDefault ||
              'Cannot set as default while inactive. Please enable the provider first.',
            type: 'warning',
          });
          return false;
        }
      });
    }
  });

  /**
   * Initialize copy-to-clipboard buttons using native Clipboard API
   */
  function initializeCopyButtons() {
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const targetSelector = btn.getAttribute('data-clipboard-target');
        if (!targetSelector) return;

        const targetEl = document.querySelector(targetSelector);
        if (!targetEl) return;

        const textToCopy = targetEl.textContent.trim();
        const originalHtml = btn.innerHTML;

        navigator.clipboard
          .writeText(textToCopy)
          .then(function () {
            btn.innerHTML = '<i class="fas fa-check"></i> ' + (i18n.copied || 'Copied!');
            btn.classList.add('copied');

            setTimeout(function () {
              btn.innerHTML = originalHtml;
              btn.classList.remove('copied');
            }, 2000);
          })
          .catch(function () {
            AdminModal.alert({
              message: i18n.copyFailed || 'Failed to copy to clipboard. Please copy manually.',
              type: 'error',
            });
          });
      });
    });
  }
})();
