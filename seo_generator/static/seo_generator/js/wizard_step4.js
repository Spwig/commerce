/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * SEO Generator Wizard Step 4: Test Connection & Save
 * Pattern follows exchange_rates/js/wizard-step4.js.
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const configEl = document.getElementById('wizard-step4-config');
    if (!configEl) return;

    const config = JSON.parse(configEl.textContent);
    const i18n = config.i18n;
    const urls = config.urls;

    const testBtn = document.getElementById('test-connection-btn');
    const saveBtn = document.getElementById('save-btn');
    const testStatus = document.getElementById('test-status');
    const testResults = document.getElementById('test-results');
    const testButtonContainer = document.getElementById('test-button-container');

    const csrfToken =
      typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken
        ? AdminUtils.getCsrfToken()
        : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    if (testBtn) {
      testBtn.addEventListener('click', function () {
        runTest();
      });
    }

    if (saveBtn) {
      saveBtn.addEventListener('click', function () {
        saveProvider();
      });
    }

    function runTest() {
      // Show testing status
      testStatus.classList.remove('seo-hidden');
      testResults.classList.add('seo-hidden');
      testButtonContainer.classList.add('seo-hidden');
      saveBtn.classList.add('seo-hidden');

      document.getElementById('test-status-title').textContent = i18n.testing;
      document.getElementById('test-status-text').textContent = i18n.pleaseWait;

      const formData = new FormData();
      formData.append('action', 'test');

      fetch(urls.step4, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
        body: formData,
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          testStatus.classList.add('seo-hidden');
          testResults.classList.remove('seo-hidden');

          const resultIcon = testResults.querySelector('.test-result-icon i');
          const resultTitle = document.getElementById('test-result-title');
          const resultMessage = document.getElementById('test-result-message');

          if (data.success) {
            resultIcon.className = 'fas fa-check-circle';
            testResults.className = 'test-results test-success';
            resultTitle.textContent = i18n.success;
            resultMessage.textContent = data.message || i18n.successMsg;
            saveBtn.classList.remove('seo-hidden');
          } else {
            resultIcon.className = 'fas fa-times-circle';
            testResults.className = 'test-results test-failed';
            resultTitle.textContent = i18n.failed;
            resultMessage.textContent = data.error || i18n.failedMsg;
            testButtonContainer.classList.remove('seo-hidden');
          }
        })
        .catch(function () {
          testStatus.classList.add('seo-hidden');
          testResults.classList.remove('seo-hidden');
          testButtonContainer.classList.remove('seo-hidden');

          const resultIcon = testResults.querySelector('.test-result-icon i');
          const resultTitle = document.getElementById('test-result-title');
          const resultMessage = document.getElementById('test-result-message');

          resultIcon.className = 'fas fa-exclamation-triangle';
          testResults.className = 'test-results test-error';
          resultTitle.textContent = i18n.error;
          resultMessage.textContent = i18n.errorMsg;
        });
    }

    function saveProvider() {
      saveBtn.disabled = true;
      saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + i18n.saving;

      const formData = new FormData();
      formData.append('action', 'save');

      fetch(urls.step4, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
        },
        body: formData,
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          if (data.success) {
            window.location.href = data.redirect_url || urls.changelist;
          } else {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save"></i> ' + i18n.saveFinish;

            const resultMessage = document.getElementById('test-result-message');
            resultMessage.textContent = data.error || i18n.saveFailed;
          }
        })
        .catch(function () {
          saveBtn.disabled = false;
          saveBtn.innerHTML = '<i class="fas fa-save"></i> ' + i18n.saveFinish;

          const resultMessage = document.getElementById('test-result-message');
          resultMessage.textContent = i18n.saveError;
        });
    }
  });
})();
