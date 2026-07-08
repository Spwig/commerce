/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var T = {};

    /* ---- Toggle Password (step3) ---- */
    function togglePassword(fieldId) {
        var input = document.getElementById(fieldId);
        if (!input) return;
        var icon = input.parentNode.querySelector('.toggle-password i');
        if (input.type === 'password') {
            input.type = 'text';
            if (icon) { icon.classList.remove('fa-eye'); icon.classList.add('fa-eye-slash'); }
        } else {
            input.type = 'password';
            if (icon) { icon.classList.remove('fa-eye-slash'); icon.classList.add('fa-eye'); }
        }
    }

    /* ---- Run Test (step4) ---- */
    function runTest(config) {
        var statusContainer = document.getElementById('test-status');
        var loadingIcon = document.getElementById('loading-icon');
        var testTitle = document.getElementById('test-title');
        var testMessage = document.getElementById('test-message');

        if (statusContainer) { statusContainer.className = 'test-status pending'; }
        if (loadingIcon) { loadingIcon.innerHTML = '<i class="fas fa-spinner fa-spin"></i>'; }
        if (testTitle) { testTitle.textContent = T.testingConnection || 'Testing Connection...'; }
        if (testMessage) { testMessage.textContent = T.pleaseWait || 'Please wait while we verify your credentials.'; }

        var url = config ? config.step4Url : '';
        var csrfToken = config ? config.csrfToken : '';

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                location.reload();
            } else {
                if (statusContainer) {
                    statusContainer.className = 'test-status error';
                    statusContainer.innerHTML =
                        '<div class="test-icon error"><i class="fas fa-times-circle"></i></div>' +
                        '<h3>' + (T.connectionFailed || 'Connection Failed') + '</h3>' +
                        '<p>' + (data.message || (T.checkCredentials || 'Unable to connect. Please check your credentials.')) + '</p>';
                }
            }
        })
        .catch(function () {
            if (statusContainer) {
                statusContainer.className = 'test-status error';
                statusContainer.innerHTML =
                    '<div class="test-icon error"><i class="fas fa-times-circle"></i></div>' +
                    '<h3>' + (T.connectionFailed || 'Connection Failed') + '</h3>' +
                    '<p>' + (T.unexpectedError || 'An unexpected error occurred. Please try again.') + '</p>';
            }
        });
    }

    /* ---- Event Delegation ---- */
    document.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) return;
        if (btn.dataset.action === 'toggle-password') {
            togglePassword(btn.dataset.fieldId);
        } else if (btn.dataset.action === 'run-test') {
            var configEl = document.getElementById('pos-wizard-config');
            runTest(configEl ? configEl.dataset : {});
        }
    });

    /* ---- Init ---- */
    document.addEventListener('DOMContentLoaded', function () {
        var el = document.getElementById('pos-wizard-translations');
        if (el) { try { T = JSON.parse(el.textContent); } catch (err) {} }


        /* ---- Step 1: Provider Selection ---- */
        var providerForm = document.getElementById('provider-select-form');
        if (providerForm) {
            var continueBtn = document.getElementById('continue-btn');
            var componentIdInput = document.getElementById('selected-component-id');
            providerForm.querySelectorAll('input[name="provider_type"]').forEach(function (radio) {
                radio.addEventListener('change', function () {
                    if (continueBtn) continueBtn.disabled = false;
                    if (componentIdInput) componentIdInput.value = this.dataset.componentId || '';
                });
            });
        }

        var configEl = document.getElementById('pos-wizard-config');
        if (configEl && configEl.dataset.autoRun === 'true') {
            runTest(configEl.dataset);
        }
    });
}());
