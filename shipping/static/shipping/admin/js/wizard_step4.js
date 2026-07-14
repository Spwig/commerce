/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Shipping Provider Wizard Step 4 - Test Connection
 * Reads config from #wizard-step4-config and translations from #wizard-step4-translations.
 */

(function () {
  'use strict';

  function init() {
    const config = document.getElementById('wizard-step4-config');
    let T = {};
    const island = document.getElementById('wizard-step4-translations');
    if (island) {
      try {
        T = JSON.parse(island.textContent);
      } catch (e) {}
    }

    const testBtn = document.getElementById('test-connection-btn');
    if (!testBtn || !config) return;

    const step4Url = config.dataset.step4Url;
    const step5Url = config.dataset.step5Url;

    const testStatus = document.getElementById('test-status');
    const testButtonContainer = document.getElementById('test-button-container');
    const testResults = document.getElementById('test-results');
    const nextBtn = document.getElementById('next-btn');
    const testResultTitle = document.getElementById('test-result-title');
    const testResultMessage = document.getElementById('test-result-message');
    const testDetails = document.getElementById('test-details');
    const testDetailsBody = document.getElementById('test-details-body');
    const testResultIcon = testResults ? testResults.querySelector('.test-result-icon i') : null;

    const csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');

    testBtn.addEventListener('click', function () {
      if (!csrfEl) return;

      testButtonContainer.style.display = 'none';
      testStatus.style.display = 'flex';
      testResults.style.display = 'none';
      nextBtn.style.display = 'none';

      fetch(step4Url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfEl.value,
        },
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (result) {
          testStatus.style.display = 'none';
          testResults.style.display = 'block';

          if (result.success) {
            if (testResultIcon) testResultIcon.className = 'fas fa-check-circle';
            testResults.className = 'test-results success';
            if (testResultTitle)
              testResultTitle.textContent = T.successTitle || 'Connection Successful!';
            if (testResultMessage)
              testResultMessage.textContent =
                result.message ||
                T.successMessage ||
                'Your credentials were verified successfully.';

            if (result.details && testDetails && testDetailsBody) {
              testDetails.style.display = 'block';
              testDetailsBody.innerHTML = '';
              Object.entries(result.details).forEach(function (entry) {
                const row = document.createElement('tr');
                row.innerHTML = '<th>' + entry[0] + '</th><td>' + entry[1] + '</td>';
                testDetailsBody.appendChild(row);
              });
            }

            nextBtn.style.display = 'inline-block';
            nextBtn.addEventListener(
              'click',
              function () {
                window.location.href = step5Url;
              },
              { once: true }
            );
          } else {
            if (testResultIcon) testResultIcon.className = 'fas fa-times-circle';
            testResults.className = 'test-results error';
            if (testResultTitle) testResultTitle.textContent = T.failTitle || 'Connection Failed';
            if (testResultMessage)
              testResultMessage.textContent =
                result.error ||
                result.message ||
                T.failMessage ||
                'Could not connect to the provider API.';
            testButtonContainer.style.display = 'block';
          }
        })
        .catch(function (error) {
          testStatus.style.display = 'none';
          testResults.style.display = 'block';
          if (testResultIcon) testResultIcon.className = 'fas fa-exclamation-triangle';
          testResults.className = 'test-results error';
          if (testResultTitle) testResultTitle.textContent = T.errorTitle || 'Error';
          if (testResultMessage)
            testResultMessage.textContent =
              error.message || T.errorMessage || 'An unexpected error occurred.';
          testButtonContainer.style.display = 'block';
        });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
