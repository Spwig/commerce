/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Translation Provider Setup Wizard
 * Multi-step wizard for configuring external translation providers
 */

(function() {
    'use strict';

    // Escape HTML entities to prevent XSS in dynamic content
    function escapeHtml(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    // Wizard navigation
    let currentStep = 1;
    const totalSteps = 4;

    function showStep(step) {
        // Hide all steps
        document.querySelectorAll('.wizard-step').forEach(s => s.classList.remove('active'));
        document.querySelectorAll('.progress-step').forEach(s => s.classList.remove('active'));

        // Show current step
        document.getElementById(`step-${step}`).classList.add('active');

        // Update progress
        for (let i = 1; i <= step; i++) {
            document.querySelector(`.progress-step[data-step="${i}"]`).classList.add('active');
        }

        currentStep = step;
    }

    function nextStep() {
        if (currentStep < totalSteps) {
            // Update summary on last step
            if (currentStep === 3) {
                updateSummary();
            }
            showStep(currentStep + 1);
        }
    }

    function previousStep() {
        if (currentStep > 1) {
            showStep(currentStep - 1);
        }
    }

    function updateSummary() {
        const providerName = document.getElementById('provider_name');
        const rateLimit = document.getElementById('rate_limit');

        if (providerName) {
            const summaryProvider = document.getElementById('summary-provider');
            const defaultName = summaryProvider?.dataset.defaultName || '';
            summaryProvider.textContent = providerName.value || defaultName;
        }

        // Build credential summary from all password/text fields in the provider form
        const summaryCredentials = document.getElementById('summary-credentials');
        if (summaryCredentials) {
            const form = document.getElementById('provider-form');
            const credFields = form?.querySelectorAll('input[type="password"], input[type="text"]') || [];
            const parts = [];
            credFields.forEach(field => {
                if (field.name === 'name' || field.name === 'provider_type' || field.type === 'hidden') return;
                if (field.value) {
                    const val = field.value;
                    const masked = val.length > 6
                        ? val.substring(0, 3) + '***' + val.substring(val.length - 3)
                        : '***';
                    parts.push(masked);
                }
            });
            summaryCredentials.textContent = parts.length > 0 ? parts.join(' | ') : '***************';
        }

        const rateLimitValue = rateLimit?.value || '100';
        const summaryRateLimit = document.getElementById('summary-rate-limit');
        if (summaryRateLimit) {
            summaryRateLimit.textContent = rateLimitValue + ' requests/min';
        }
    }

    function testConnection() {
        const resultDiv = document.getElementById('test-result');
        resultDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Testing connection...</div>';

        const formData = new FormData(document.getElementById('provider-form'));
        const testUrl = (document.getElementById('translations-config') || document.body).dataset.testProviderUrl;

        fetch(testUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resultDiv.innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i>
                        <strong>Connection successful!</strong><br>
                        ${escapeHtml(data.message || 'Provider is accessible and authenticated.')}
                    </div>`;
            } else {
                resultDiv.innerHTML = `
                    <div class="alert alert-error">
                        <i class="fas fa-times-circle"></i>
                        <strong>Connection failed:</strong><br>
                        ${escapeHtml(data.error || 'Unknown error')}
                    </div>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `
                <div class="alert alert-error">
                    <i class="fas fa-times-circle"></i>
                    <strong>Request failed:</strong><br>
                    ${escapeHtml(error.message)}
                </div>`;
        });
    }

    function testTranslation() {
        const resultDiv = document.getElementById('test-translation-result');
        const text = document.getElementById('test-text')?.value?.trim();
        const targetLang = document.getElementById('test-target')?.value;

        if (!text) {
            resultDiv.innerHTML = '<div class="alert alert-error"><i class="fas fa-exclamation-circle"></i> Please enter text to translate.</div>';
            return;
        }

        resultDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Translating...</div>';

        const formData = new FormData(document.getElementById('provider-form'));
        formData.append('text', text);
        formData.append('target_lang', targetLang);
        formData.append('source_lang', 'en');

        const testUrl = (document.getElementById('translations-config') || document.body).dataset.testTranslationUrl;

        fetch(testUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resultDiv.innerHTML = `
                    <div class="alert alert-success">
                        <strong>Translation Result:</strong><br>
                        ${escapeHtml(data.translated_text)}
                    </div>`;
            } else {
                resultDiv.innerHTML = `
                    <div class="alert alert-error">
                        <i class="fas fa-times-circle"></i>
                        <strong>Translation failed:</strong><br>
                        ${escapeHtml(data.error || 'Unknown error')}
                    </div>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `
                <div class="alert alert-error">
                    <i class="fas fa-times-circle"></i>
                    <strong>Request failed:</strong><br>
                    ${escapeHtml(error.message)}
                </div>`;
        });
    }

    function saveConfiguration() {
        const configForm = document.getElementById('provider-form');
        const settingsForm = document.getElementById('settings-form');
        const saveUrl = (document.getElementById('translations-config') || document.body).dataset.saveProviderUrl;
        const providersUrl = (document.getElementById('translations-config') || document.body).dataset.providersUrl;

        const formData = new FormData(configForm);

        // Add settings form data
        if (settingsForm) {
            for (let [key, value] of new FormData(settingsForm).entries()) {
                formData.append(key, value);
            }
        }

        fetch(saveUrl, {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                AdminModal.toast(data.message, 'success');
                window.location.href = providersUrl;
            } else {
                AdminModal.alert({message: 'Error: ' + (data.error || 'Failed to save configuration'), type: 'error'});
            }
        })
        .catch(error => {
            AdminModal.alert({message: 'Request failed: ' + error.message, type: 'error'});
        });
    }

    /**
     * Handle wizard actions via delegation
     */
    function handleWizardActions(e) {
        const actionElement = e.target.closest('[data-action]');
        if (!actionElement) return;

        const action = actionElement.dataset.action;

        switch (action) {
            case 'next-step':
                e.preventDefault();
                nextStep();
                break;
            case 'previous-step':
                e.preventDefault();
                previousStep();
                break;
            case 'test-connection':
                e.preventDefault();
                testConnection();
                break;
            case 'test-translation':
                e.preventDefault();
                testTranslation();
                break;
            case 'save-configuration':
                e.preventDefault();
                saveConfiguration();
                break;
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            // Show first step
            showStep(1);
            // Event delegation
            document.addEventListener('click', handleWizardActions);
        });
    } else {
        showStep(1);
        document.addEventListener('click', handleWizardActions);
    }

})();
