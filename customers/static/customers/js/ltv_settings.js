/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var i18n = {};

    function t(key) {
        return i18n[key] || key;
    }

    function init() {
        var dataEl = document.getElementById('ltv-settings-i18n');
        if (dataEl) {
            try { i18n = JSON.parse(dataEl.textContent); } catch (e) {}
        }

        var form = document.getElementById('ltvSettingsForm');
        var saveButton = document.getElementById('saveButton');
        var saveAndRecalculateButton = document.getElementById('saveAndRecalculateButton');

        if (!form || !saveButton || !saveAndRecalculateButton) { return; }

        // Method card selection
        var methodCards = document.querySelectorAll('.ltv-method-card');
        methodCards.forEach(function (card) {
            card.addEventListener('click', function () {
                methodCards.forEach(function (c) { c.classList.remove('selected'); });
                this.classList.add('selected');
                this.querySelector('input[type="radio"]').checked = true;
            });
        });

        saveButton.addEventListener('click', function (e) {
            e.preventDefault();
            saveSettings(form, saveButton, saveAndRecalculateButton, false);
        });

        saveAndRecalculateButton.addEventListener('click', async function (e) {
            e.preventDefault();
            if (await AdminModal.confirm(t('confirmRecalculate'))) {
                saveSettings(form, saveButton, saveAndRecalculateButton, true);
            }
        });
    }

    function saveSettings(form, saveButton, saveAndRecalculateButton, triggerRecalculation) {
        var formData = new FormData(form);

        if (triggerRecalculation) {
            formData.append('trigger_recalculation', 'true');
        }

        saveButton.disabled = true;
        saveAndRecalculateButton.disabled = true;
        saveButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + t('saving');

        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            if (data.success) {
                showMessage(data.message, 'success');
                setTimeout(function () {
                    window.location.reload();
                }, 2000);
            } else {
                showMessage(data.message || t('errorSaving'), 'error');
                saveButton.disabled = false;
                saveAndRecalculateButton.disabled = false;
                saveButton.innerHTML = '<i class="fas fa-save"></i> ' + t('saveSettings');
            }
        })
        .catch(function () {
            showMessage(t('networkError'), 'error');
            saveButton.disabled = false;
            saveAndRecalculateButton.disabled = false;
            saveButton.innerHTML = '<i class="fas fa-save"></i> ' + t('saveSettings');
        });
    }

    function showMessage(message, type) {
        var messageDiv = document.createElement('div');
        messageDiv.className = 'message-toast ' + type;
        var icon = type === 'success' ? 'check-circle' : 'exclamation-circle';
        messageDiv.innerHTML = '<i class="fas fa-' + icon + '"></i><span>' + message + '</span>';

        document.body.appendChild(messageDiv);

        setTimeout(function () {
            messageDiv.classList.add('show');
        }, 10);

        setTimeout(function () {
            messageDiv.classList.remove('show');
            setTimeout(function () {
                messageDiv.remove();
            }, 300);
        }, 3000);
    }

    document.addEventListener('DOMContentLoaded', init);
}());
