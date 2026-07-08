/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var configEl = document.getElementById('licenseprovider-step4-config');
        if (!configEl) return;
        var config = JSON.parse(configEl.textContent);

        var testBtn = document.getElementById('test-connection-btn');
        var saveBtn = document.getElementById('save-provider-btn');
        var testIcon = document.getElementById('test-icon');
        var testMessage = document.getElementById('test-message');
        var testDetails = document.getElementById('test-details');

        // Test Connection
        testBtn.addEventListener('click', function () {
            testConnection();
        });

        // Save Provider
        saveBtn.addEventListener('click', function () {
            saveProvider();
        });

        function testConnection() {
            // Update UI to testing state
            testIcon.className = 'test-result-icon testing';
            testIcon.innerHTML = '<i class="fas fa-spinner"></i>';
            testMessage.textContent = config.strings.testingConnection;
            testDetails.textContent = config.strings.pleaseWait;
            testBtn.disabled = true;
            saveBtn.disabled = true;

            // Make AJAX request
            fetch(config.step4Url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': AdminUtils.getCsrfToken()
                },
                body: 'action=test'
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success) {
                    testIcon.className = 'test-result-icon success';
                    testIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
                    testMessage.textContent = config.strings.connectionSuccessful;
                    testDetails.textContent = data.message || config.strings.credentialsValid;
                    saveBtn.disabled = false;
                } else {
                    testIcon.className = 'test-result-icon error';
                    testIcon.innerHTML = '<i class="fas fa-times-circle"></i>';
                    testMessage.textContent = config.strings.connectionFailed;
                    testDetails.textContent = data.error || config.strings.checkCredentials;
                    testBtn.disabled = false;
                }
            })
            .catch(function (error) {
                testIcon.className = 'test-result-icon error';
                testIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
                testMessage.textContent = config.strings.error;
                testDetails.textContent = error.message || config.strings.unexpectedError;
                testBtn.disabled = false;
            });
        }

        function saveProvider() {
            saveBtn.disabled = true;
            saveBtn.textContent = config.strings.saving;

            fetch(config.step4Url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': AdminUtils.getCsrfToken()
                },
                body: 'action=save'
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    AdminModal.alert({message: data.error || config.strings.failedToSave, type: 'error'});
                    saveBtn.disabled = false;
                    saveBtn.textContent = config.strings.completeSetup;
                }
            })
            .catch(function (error) {
                AdminModal.alert({message: error.message || config.strings.unexpectedError, type: 'error'});
                saveBtn.disabled = false;
                saveBtn.textContent = config.strings.completeSetup;
            });
        }

    });
})();
