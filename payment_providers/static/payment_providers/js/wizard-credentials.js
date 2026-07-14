/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Wizard Step 3 - Credential Mode Toggle
 * Replaces inline script in wizard/step3_credentials.html
 */
(function () {
  'use strict';

  function getTranslations() {
    const el = document.getElementById('wizard-credentials-translations');
    if (el) {
      try {
        return JSON.parse(el.textContent);
      } catch (e) {
        /* ignore */
      }
    }
    return {};
  }

  function toggleCredentialMode(isTestMode) {
    const t = getTranslations();
    const banner = document.getElementById('credential-mode-banner');
    const icon = document.getElementById('mode-icon');
    const title = document.getElementById('mode-title');
    const description = document.getElementById('mode-description');

    const testFields = document.querySelectorAll('[data-group="test_credentials"]');
    const liveFields = document.querySelectorAll('[data-group="live_credentials"]');

    if (isTestMode) {
      banner.classList.remove('banner--production');
      banner.classList.add('banner--test');
      icon.innerHTML = '<i class="fas fa-flask"></i>';
      title.textContent = t.testMode || 'TEST MODE';
      description.textContent = t.testDesc || 'Using test credentials - no real transactions';

      testFields.forEach(function (el) {
        el.classList.remove('credential-field--hidden');
      });
      liveFields.forEach(function (el) {
        el.classList.add('credential-field--hidden');
      });
    } else {
      banner.classList.remove('banner--test');
      banner.classList.add('banner--production');
      icon.innerHTML = '<i class="fas fa-rocket"></i>';
      title.textContent = t.prodMode || 'PRODUCTION MODE';
      description.textContent = t.prodDesc || 'Using live credentials - real transactions!';

      testFields.forEach(function (el) {
        el.classList.add('credential-field--hidden');
      });
      liveFields.forEach(function (el) {
        el.classList.remove('credential-field--hidden');
      });
    }
  }

  // Event delegation for toggle
  document.addEventListener('change', function (e) {
    const el = e.target;
    if (el.id === 'id_test_mode' || el.dataset.action === 'toggle-credential-mode') {
      toggleCredentialMode(el.checked);
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    // Initialize credential mode toggle on page load
    const testModeCheckbox = document.getElementById('id_test_mode');
    if (testModeCheckbox) {
      toggleCredentialMode(testModeCheckbox.checked);
    }

    // Show/hide password fields
    document.querySelectorAll('input[type="password"]').forEach(function (input) {
      const wrapper = document.createElement('div');
      wrapper.className = 'password-field-wrapper';
      input.parentNode.insertBefore(wrapper, input);
      wrapper.appendChild(input);

      const toggleBtn = document.createElement('button');
      toggleBtn.type = 'button';
      toggleBtn.className = 'password-toggle';
      toggleBtn.innerHTML = '<i class="fas fa-eye"></i>';
      toggleBtn.addEventListener('click', function () {
        if (input.type === 'password') {
          input.type = 'text';
          toggleBtn.innerHTML = '<i class="fas fa-eye-slash"></i>';
        } else {
          input.type = 'password';
          toggleBtn.innerHTML = '<i class="fas fa-eye"></i>';
        }
      });
      wrapper.appendChild(toggleBtn);
    });
  });
})();
