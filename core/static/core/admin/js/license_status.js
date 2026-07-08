/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var config = {};

    function init() {
        var configEl = document.getElementById('license-status-config');
        if (configEl) {
            try { config = JSON.parse(configEl.textContent); } catch (e) { config = {}; }
        }

        // Button event delegation
        document.addEventListener('click', function (e) {
            var btn = e.target.closest('[data-action="clear-license-cache"]');
            if (btn) { clearLicenseCache(); return; }

            btn = e.target.closest('[data-action="refresh-license"]');
            if (btn) { refreshLicense(btn); return; }

            btn = e.target.closest('[data-action="activate-pos-license"]');
            if (btn) { activatePOSLicense(); return; }

            btn = e.target.closest('[data-action="activate-license-by-key"]');
            if (btn) { activateLicenseByKey(); return; }

            btn = e.target.closest('[data-action="trigger-file-input"]');
            if (btn) {
                var targetId = btn.dataset.target || 'license-file-input';
                var input = document.getElementById(targetId);
                if (input) input.click();
            }
        });

        // File input change
        var fileInput = document.getElementById('license-file-input');
        if (fileInput) {
            fileInput.addEventListener('change', function () { handleFileUpload(this); });
        }
    }

    function activateLicenseByKey() {
        var licenseKey = document.getElementById('license-key-input').value.trim();
        var environmentType = document.getElementById('environment-type-select').value;
        var resultDiv = document.getElementById('activation-result');

        if (!licenseKey) {
            resultDiv.style.display = 'block';
            resultDiv.style.background = 'var(--error-color)';
            resultDiv.style.color = 'white';
            resultDiv.innerHTML = '<strong>\u2717 ' + (config.i18n.enterLicenseKey || 'Please enter a license key') + '</strong>';
            return;
        }

        resultDiv.style.display = 'block';
        resultDiv.style.background = 'var(--body-quiet-color)';
        resultDiv.style.color = 'var(--body-fg)';
        resultDiv.innerHTML = '\u23F3 ' + (config.i18n.activatingLicense || 'Activating license... Please wait');

        var formData = new FormData();
        formData.append('license_key', licenseKey);
        formData.append('environment_type', environmentType);

        fetch(config.urls.activate, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': AdminUtils.getCsrfToken() }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                resultDiv.style.background = 'var(--success-color)';
                resultDiv.style.color = 'white';
                resultDiv.innerHTML = '<strong>\u2713 ' + data.message + '</strong><br>' +
                    (config.i18n.owner || 'Owner') + ': ' + data.owner_name + '<br>' +
                    (config.i18n.type || 'Type') + ': ' + data.license_type + '<br>' +
                    (config.i18n.environment || 'Environment') + ': ' + data.environment_type + '<br>' +
                    (config.i18n.installations || 'Installations') + ': ' + data.active_installations + '/' + data.max_installations + '<br><br>' +
                    '<em>' + (config.i18n.pageWillReload || 'Page will reload automatically...') + '</em>';
                setTimeout(function () { window.location.reload(); }, 2000);
            } else {
                resultDiv.style.background = 'var(--error-color)';
                resultDiv.style.color = 'white';
                var errorMsg = data.error;
                if (data.error_code) { errorMsg += ' (' + data.error_code + ')'; }
                resultDiv.innerHTML = '<strong>\u2717 ' + (config.i18n.activationFailed || 'Activation Failed') + '</strong><br>' + errorMsg;
            }
        })
        .catch(function (error) {
            resultDiv.style.background = 'var(--error-color)';
            resultDiv.style.color = 'white';
            resultDiv.innerHTML = '<strong>\u2717 ' + (config.i18n.connectionError || 'Connection Error') + '</strong><br>' + error.message;
        });
    }

    function handleFileUpload(input) {
        var file = input.files[0];
        if (!file) return;

        var formData = new FormData();
        formData.append('license_file', file);

        var resultDiv = document.getElementById('upload-result');
        resultDiv.style.display = 'block';
        resultDiv.style.background = 'var(--body-quiet-color)';
        resultDiv.style.color = 'var(--body-fg)';
        resultDiv.innerHTML = '\u23F3 ' + (config.i18n.uploadingLicense || 'Uploading and validating license...');

        fetch(config.urls.upload, {
            method: 'POST',
            body: formData,
            headers: { 'X-CSRFToken': AdminUtils.getCsrfToken() }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                resultDiv.style.background = 'var(--success-color)';
                resultDiv.style.color = 'white';
                resultDiv.innerHTML = '<strong>\u2713 ' + data.message + '</strong><br>' +
                    (config.i18n.licenseKey || 'License Key') + ': ' + data.license_key + '<br>' +
                    (config.i18n.type || 'Type') + ': ' + data.license_type;
                setTimeout(function () { window.location.reload(); }, 2000);
            } else {
                resultDiv.style.background = 'var(--error-color)';
                resultDiv.style.color = 'white';
                resultDiv.innerHTML = '<strong>\u2717 ' + (config.i18n.uploadFailed || 'Upload Failed') + '</strong><br>' + data.error;
            }
        })
        .catch(function (error) {
            resultDiv.style.background = 'var(--error-color)';
            resultDiv.style.color = 'white';
            resultDiv.innerHTML = '<strong>\u2717 ' + (config.i18n.uploadFailed || 'Upload Failed') + '</strong><br>' + error.message;
        });
    }

    function refreshLicense(btn) {
        var originalText = btn.textContent;
        btn.disabled = true;
        btn.textContent = config.i18n.refreshingLicense || 'Refreshing license from server...';

        fetch(config.urls.refreshLicense, {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                AdminModal.toast(data.message, 'success');
                window.location.reload();
            } else {
                AdminModal.alert({message: (config.i18n.refreshFailed || 'License Refresh Failed') + ': ' + data.error, type: 'error'});
                btn.disabled = false;
                btn.textContent = originalText;
            }
        })
        .catch(function (error) {
            AdminModal.alert({message: (config.i18n.error || 'Error') + ': ' + error.message, type: 'error'});
            btn.disabled = false;
            btn.textContent = originalText;
        });
    }

    async function clearLicenseCache() {
        if (!await AdminModal.confirm({
            message: config.i18n.confirmClearCache || 'Are you sure you want to clear the license cache?',
            danger: true,
            confirmText: 'Clear'
        })) {
            return;
        }

        fetch(config.urls.clearCache, {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                AdminModal.toast(data.message, 'success');
                window.location.reload();
            } else {
                AdminModal.alert({message: (config.i18n.error || 'Error') + ': ' + data.error, type: 'error'});
            }
        })
        .catch(function (error) {
            AdminModal.alert({message: (config.i18n.error || 'Error') + ': ' + error.message, type: 'error'});
        });
    }

    function activatePOSLicense() {
        var keyInput = document.getElementById('pos-license-key-input');
        var resultDiv = document.getElementById('pos-activation-result');
        var licenseKey = keyInput.value.trim().toUpperCase();

        if (!licenseKey) {
            resultDiv.className = 'pos-activation-result error';
            resultDiv.textContent = config.i18n.enterPosKey || 'Please enter a POS license key.';
            return;
        }

        if (!/^POS-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(licenseKey)) {
            resultDiv.className = 'pos-activation-result error';
            resultDiv.textContent = config.i18n.invalidPosFormat || 'Invalid format. Expected: POS-XXXX-XXXX-XXXX-XXXX';
            return;
        }

        resultDiv.className = 'pos-activation-result loading';
        resultDiv.textContent = config.i18n.activatingPos || 'Activating POS license...';

        fetch(config.urls.activatePos, {
            method: 'POST',
            body: JSON.stringify({ license_key: licenseKey }),
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                resultDiv.className = 'pos-activation-result success';
                resultDiv.textContent = data.message;
                setTimeout(function () { window.location.reload(); }, 1500);
            } else {
                resultDiv.className = 'pos-activation-result error';
                resultDiv.textContent = data.message || (config.i18n.activationFailed || 'Activation failed.');
            }
        })
        .catch(function (err) {
            resultDiv.className = 'pos-activation-result error';
            resultDiv.textContent = (config.i18n.connectionError || 'Connection error: ') + err.message;
        });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
