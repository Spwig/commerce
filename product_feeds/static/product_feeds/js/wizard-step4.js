/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
/* Product Feeds Wizard Step 4 - Test Connection */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // Read configuration from data island
    const configEl = document.getElementById('wizard-step4-config');
    if (!configEl) {
      console.error('wizard-step4-config data island not found');
      return;
    }
    let config;
    try {
      config = JSON.parse(configEl.textContent);
    } catch (e) {
      console.error('Failed to parse wizard-step4-config:', e);
      return;
    }

    const i18n = config.i18n;
    const urls = config.urls;

    const testBtn = document.getElementById('test-connection-btn');
    const testStatus = document.getElementById('test-status');
    const testButtonContainer = document.getElementById('test-button-container');
    const testConnectionArea = document.querySelector('.test-connection-area');
    const testResults = document.getElementById('test-results');
    const saveBtn = document.getElementById('save-btn');
    const testResultTitle = document.getElementById('test-result-title');
    const testResultMessage = document.getElementById('test-result-message');
    const testDetails = document.getElementById('test-details');
    const testDetailsBody = document.getElementById('test-details-body');
    const testResultIcon = testResults.querySelector('.test-result-icon i');
    const feedPreview = document.getElementById('feed-preview');

    if (!testBtn) {
      console.error('Test button not found!');
      return;
    }

    testBtn.addEventListener('click', async function () {
      // Show testing status
      testButtonContainer.classList.add('hidden');
      testStatus.classList.remove('hidden');
      testResults.classList.add('hidden');
      if (feedPreview) feedPreview.classList.add('hidden');
      saveBtn.classList.add('hidden');

      try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');

        const formData = new FormData();
        formData.append('action', 'test');
        if (csrfToken) {
          formData.append('csrfmiddlewaretoken', csrfToken.value);
        }

        const response = await fetch(urls.step4, {
          method: 'POST',
          body: formData,
        });

        const result = await response.json();

        // Hide testing status and test area
        testStatus.classList.add('hidden');
        testConnectionArea.classList.add('hidden');

        // Show results
        testResults.classList.remove('hidden');

        if (result.success) {
          // Success
          testResultIcon.className = 'fas fa-check-circle';
          testResults.className = 'test-results success';
          testResultTitle.textContent = i18n.success;
          testResultMessage.textContent = result.message || i18n.successMsg;

          // Show details if available
          if (result.details) {
            testDetails.removeAttribute('hidden');
            testDetailsBody.innerHTML = '';
            for (const [key, value] of Object.entries(result.details)) {
              const row = document.createElement('tr');
              row.innerHTML = `<th>${key}</th><td>${value}</td>`;
              testDetailsBody.appendChild(row);
            }
          }

          // Show feed preview if available
          if (result.preview && feedPreview) {
            feedPreview.classList.remove('hidden');
            document.getElementById('preview-product-count').textContent =
              result.preview.product_count || 0;
            document.getElementById('preview-category-count').textContent =
              result.preview.category_count || 0;
            document.getElementById('preview-format').textContent = result.preview.format || 'XML';
          }

          // Show save button
          saveBtn.classList.remove('hidden');
        } else {
          // Failure
          testResultIcon.className = 'fas fa-times-circle';
          testResults.className = 'test-results error';
          testResultTitle.textContent = i18n.failed;
          testResultMessage.textContent = result.error || result.message || i18n.failedMsg;

          // Show retry button - bring back the test area
          testConnectionArea.classList.remove('hidden');
          testButtonContainer.classList.remove('hidden');
        }
      } catch (error) {
        // Error
        testStatus.classList.add('hidden');
        testConnectionArea.classList.add('hidden');
        testResults.classList.remove('hidden');
        testResultIcon.className = 'fas fa-exclamation-triangle';
        testResults.className = 'test-results error';
        testResultTitle.textContent = i18n.error;
        testResultMessage.textContent = error.message || i18n.errorMsg;

        // Show retry button - bring back the test area
        testConnectionArea.classList.remove('hidden');
        testButtonContainer.classList.remove('hidden');
      }
    });

    // Save button handler
    saveBtn.addEventListener('click', async function () {
      saveBtn.disabled = true;
      saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + i18n.saving;

      try {
        const formData = new FormData();
        formData.append('action', 'save');
        formData.append('csrfmiddlewaretoken', AdminUtils.getCsrfToken());

        const response = await fetch(urls.step4, {
          method: 'POST',
          body: formData,
        });

        const result = await response.json();

        if (result.success) {
          // Redirect to provider account list
          window.location.href = urls.changelist;
        } else {
          AdminModal.alert({ message: result.error || i18n.saveFailed, type: 'error' });
          saveBtn.disabled = false;
          saveBtn.innerHTML = '<i class="fas fa-save"></i> ' + i18n.saveFinish;
        }
      } catch (error) {
        AdminModal.alert({ message: error.message || i18n.saveError, type: 'error' });
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i class="fas fa-save"></i> ' + i18n.saveFinish;
      }
    });
  });
})();
