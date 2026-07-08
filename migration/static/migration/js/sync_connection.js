/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Sync Connection JS
 * Handles connection card selection and AJAX connection testing
 * for both Settings Sync and Full Migration wizard step 1.
 */
(function() {
    'use strict';

    // Parse config
    const configEl = document.getElementById('sync-step1-config');
    if (!configEl) return;
    const config = JSON.parse(configEl.textContent);

    // Elements
    const form = document.getElementById('connection-form');
    const connectionIdField = document.getElementById('connection_id');
    const nameField = document.getElementById('name');
    const urlField = document.getElementById('remote_url');
    const tokenField = document.getElementById('auth_token');
    const roleField = document.getElementById('role');
    const testBtn = document.getElementById('test-connection-btn');
    const testResult = document.getElementById('connection-test-result');

    // Connection card selection
    document.querySelectorAll('.connection-card').forEach(card => {
        card.addEventListener('click', function() {
            // Deselect all
            document.querySelectorAll('.connection-card').forEach(c => c.classList.remove('selected'));
            // Select this one
            this.classList.add('selected');

            // Fill form fields from saved connection
            connectionIdField.value = this.dataset.connectionId;
            nameField.value = this.dataset.name;
            urlField.value = this.dataset.url;
            // Token is not exposed in HTML — server uses connection_id to look it up
            tokenField.value = '';
            tokenField.placeholder = 'Using saved token';
            tokenField.removeAttribute('required');
            if (roleField && this.dataset.role) {
                roleField.value = this.dataset.role;
            }
        });
    });

    // Clear selection when typing in form fields
    [nameField, urlField, tokenField].forEach(field => {
        if (field) {
            field.addEventListener('input', function() {
                if (connectionIdField.value) {
                    connectionIdField.value = '';
                    tokenField.placeholder = '';
                    tokenField.setAttribute('required', '');
                    document.querySelectorAll('.connection-card').forEach(c => c.classList.remove('selected'));
                }
            });
        }
    });

    // Test connection
    if (testBtn) {
        testBtn.addEventListener('click', async function() {
            const url = urlField.value.trim();
            const token = tokenField.value.trim();
            const connId = connectionIdField.value.trim();

            // For saved connections, URL is required but token can come from server
            if (!url && !connId) {
                showTestResult(false, 'Please enter a URL or select a saved connection.');
                return;
            }
            if (!token && !connId) {
                showTestResult(false, 'Please enter a token or select a saved connection.');
                return;
            }

            testBtn.disabled = true;
            testBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + config.translations.testing;
            testResult.classList.add('sync-hidden');

            try {
                const formData = new FormData();
                formData.append('remote_url', url);
                formData.append('auth_token', token);
                if (connId) {
                    formData.append('connection_id', connId);
                }

                const response = await fetch(config.testConnectionUrl, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': config.csrfToken,
                    },
                    body: formData,
                });

                const data = await response.json();

                if (data.success) {
                    showTestResult(true, config.translations.success, {
                        [config.translations.siteName]: data.site_name,
                        [config.translations.version]: data.version,
                        [config.translations.categories]: data.categories + ' available',
                    });
                } else {
                    showTestResult(false, data.error || config.translations.failed);
                }
            } catch (err) {
                showTestResult(false, config.translations.failed + ': ' + err.message);
            }

            testBtn.disabled = false;
            testBtn.innerHTML = '<i class="fas fa-plug"></i> Test Connection';
        });
    }

    function showTestResult(success, message, info) {
        testResult.classList.remove('sync-hidden');
        testResult.className = 'connection-test-result ' + (success ? 'success' : 'error');
        testResult.textContent = '';

        const msgDiv = document.createElement('div');
        const icon = document.createElement('i');
        icon.className = success ? 'fas fa-check-circle' : 'fas fa-times-circle';
        msgDiv.appendChild(icon);
        msgDiv.appendChild(document.createTextNode(' '));
        const strong = document.createElement('strong');
        strong.textContent = message;
        msgDiv.appendChild(strong);
        testResult.appendChild(msgDiv);

        if (info) {
            const dl = document.createElement('dl');
            dl.className = 'test-info';
            for (const [key, value] of Object.entries(info)) {
                const dt = document.createElement('dt');
                dt.textContent = key;
                const dd = document.createElement('dd');
                dd.textContent = value;
                dl.appendChild(dt);
                dl.appendChild(dd);
            }
            testResult.appendChild(dl);
        }
    }
})();
