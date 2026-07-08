/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
/* Payout Providers Wizard Step 4 - Test Connection */
(function () {
    'use strict';

    /**
     * Helper: show an element by removing payout-hidden class
     */
    function showEl(el) {
        if (el) el.classList.remove('payout-hidden');
    }

    /**
     * Helper: hide an element by adding payout-hidden class
     */
    function hideEl(el) {
        if (el) el.classList.add('payout-hidden');
    }

    /**
     * Helper: create a table row with th + td (XSS-safe via textContent)
     */
    function createDetailRow(label, value) {
        var row = document.createElement('tr');
        var th = document.createElement('th');
        th.textContent = label;
        var td = document.createElement('td');
        td.textContent = value;
        row.appendChild(th);
        row.appendChild(td);
        return row;
    }

    /**
     * Helper: set button content with icon + text (XSS-safe via DOM creation)
     */
    function setButtonContent(btn, iconClass, text) {
        btn.textContent = '';
        var icon = document.createElement('i');
        icon.className = iconClass;
        btn.appendChild(icon);
        btn.appendChild(document.createTextNode(' ' + text));
    }

    /**
     * Show inline error notification (replaces alert())
     */
    function showSaveError(container, message) {
        var existing = container.querySelector('.save-error-msg');
        if (existing) existing.remove();

        var errorDiv = document.createElement('div');
        errorDiv.className = 'save-error-msg test-results error';

        var iconDiv = document.createElement('div');
        iconDiv.className = 'test-result-icon';
        var icon = document.createElement('i');
        icon.className = 'fas fa-exclamation-triangle';
        iconDiv.appendChild(icon);

        var title = document.createElement('h3');
        title.textContent = message;

        errorDiv.appendChild(iconDiv);
        errorDiv.appendChild(title);
        container.appendChild(errorDiv);

        setTimeout(function () {
            if (errorDiv.parentNode) errorDiv.remove();
        }, 8000);
    }

    document.addEventListener('DOMContentLoaded', function () {
        // Read configuration from data island
        var configEl = document.getElementById('wizard-step4-config');
        if (!configEl) {
            console.error('wizard-step4-config data island not found');
            return;
        }
        var config;
        try {
            config = JSON.parse(configEl.textContent);
        } catch (e) {
            console.error('Failed to parse wizard-step4-config:', e);
            return;
        }

        var i18n = config.i18n;
        var urls = config.urls;

        var testBtn = document.getElementById('test-connection-btn');
        var testStatus = document.getElementById('test-status');
        var testButtonContainer = document.getElementById('test-button-container');
        var testConnectionArea = document.querySelector('.test-connection-area');
        var testResults = document.getElementById('test-results');
        var saveBtn = document.getElementById('save-btn');
        var testResultTitle = document.getElementById('test-result-title');
        var testResultMessage = document.getElementById('test-result-message');
        var testDetails = document.getElementById('test-details');
        var testDetailsBody = document.getElementById('test-details-body');
        var testResultIcon = testResults.querySelector('.test-result-icon i');
        var wizardContent = document.querySelector('.wizard-step-content');

        if (!testBtn) {
            console.error('Test button not found!');
            return;
        }

        testBtn.addEventListener('click', async function () {
            // Show testing status
            hideEl(testButtonContainer);
            showEl(testStatus);
            hideEl(testResults);
            hideEl(saveBtn);

            try {
                var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');

                var formData = new FormData();
                formData.append('action', 'test');
                if (csrfToken) {
                    formData.append('csrfmiddlewaretoken', csrfToken.value);
                }

                var response = await fetch(urls.step4, {
                    method: 'POST',
                    body: formData
                });

                var result = await response.json();

                // Hide testing status and test area
                hideEl(testStatus);
                hideEl(testConnectionArea);

                // Show results
                showEl(testResults);

                if (result.success) {
                    // Success
                    testResultIcon.className = 'fas fa-check-circle';
                    testResults.className = 'test-results success';
                    testResultTitle.textContent = i18n.success;
                    testResultMessage.textContent = result.message || i18n.successMsg;

                    // Show details if available
                    if (result.account_id || result.account_name || result.environment) {
                        showEl(testDetails);
                        testDetailsBody.textContent = '';
                        if (result.environment) {
                            testDetailsBody.appendChild(createDetailRow(i18n.environment, result.environment));
                        }
                        if (result.account_id) {
                            testDetailsBody.appendChild(createDetailRow(i18n.accountId, result.account_id));
                        }
                        if (result.account_name) {
                            testDetailsBody.appendChild(createDetailRow(i18n.accountName, result.account_name));
                        }
                    }

                    // Show save button
                    showEl(saveBtn);
                } else {
                    // Failure
                    testResultIcon.className = 'fas fa-times-circle';
                    testResults.className = 'test-results error';
                    testResultTitle.textContent = i18n.failed;
                    testResultMessage.textContent = result.error || result.message || i18n.failedMsg;

                    // Show retry button - bring back the test area
                    showEl(testConnectionArea);
                    showEl(testButtonContainer);
                }
            } catch (error) {
                // Error
                hideEl(testStatus);
                hideEl(testConnectionArea);
                showEl(testResults);
                testResultIcon.className = 'fas fa-exclamation-triangle';
                testResults.className = 'test-results error';
                testResultTitle.textContent = i18n.error;
                testResultMessage.textContent = error.message || i18n.errorMsg;

                // Show retry button - bring back the test area
                showEl(testConnectionArea);
                showEl(testButtonContainer);
            }
        });

        // Save button handler
        saveBtn.addEventListener('click', async function () {
            saveBtn.disabled = true;
            setButtonContent(saveBtn, 'fas fa-spinner fa-spin', i18n.saving);

            try {
                var formData = new FormData();
                formData.append('action', 'save');
                formData.append('csrfmiddlewaretoken', AdminUtils.getCsrfToken());

                var response = await fetch(urls.step4, {
                    method: 'POST',
                    body: formData
                });

                var result = await response.json();

                if (result.success) {
                    // Redirect to provider account page or list
                    if (result.redirect_url) {
                        window.location.href = result.redirect_url;
                    } else {
                        window.location.href = urls.changelist;
                    }
                } else {
                    showSaveError(wizardContent, result.error || i18n.saveFailed);
                    saveBtn.disabled = false;
                    setButtonContent(saveBtn, 'fas fa-save', i18n.saveFinish);
                }
            } catch (error) {
                showSaveError(wizardContent, error.message || i18n.saveError);
                saveBtn.disabled = false;
                setButtonContent(saveBtn, 'fas fa-save', i18n.saveFinish);
            }
        });
    });
})();
