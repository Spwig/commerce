/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var T = {};
    var lang = document.documentElement.lang || 'en';

    /* ---- Store Location Enable ---- */
    function initEnableStore() {
        var enableBtn = document.getElementById('enable-store-btn');
        if (!enableBtn) return;

        enableBtn.addEventListener('click', function () {
            var warehouseId = this.dataset.warehouseId;
            var displayName = document.getElementById('store-display-name').value.trim();
            var btn = this;
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + (T.enabling || 'Enabling...');

            var formData = new FormData();
            formData.append('warehouse_id', warehouseId);
            formData.append('pos_display_name', displayName);

            fetch('/' + lang + '/admin/pos/store-location/enable/', {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': AdminUtils.getCsrfToken()
                },
                body: formData
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                if (data.success) {
                    window.location.reload();
                } else {
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fas fa-check"></i> ' + (T.enableStoreLocation || 'Enable as Store Location');
                    AdminModal.alert({message: data.error || (T.somethingWentWrong || 'Something went wrong. Please try again.'), type: 'error'});
                }
            })
            .catch(function () {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-check"></i> ' + (T.enableStoreLocation || 'Enable as Store Location');
                AdminModal.alert({message: T.somethingWentWrong || 'Something went wrong. Please try again.', type: 'error'});
            });
        });
    }

    /* ---- Remote Unlock ---- */
    async function handleUnlock(btn) {
        var terminalId = btn.dataset.terminalId;
        if (!await AdminModal.confirm(T.confirmUnlock || 'Send remote unlock signal to this terminal?')) return;

        btn.disabled = true;
        var icon = btn.querySelector('i');
        icon.className = 'fas fa-spinner fa-spin';

        var formData = new FormData();
        formData.append('terminal_id', terminalId);

        fetch('/' + lang + '/admin/pos/terminals/unlock/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            },
            body: formData
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            btn.disabled = false;
            icon.className = 'fas fa-unlock';
            if (data.success) {
                icon.className = 'fas fa-check unlock-success-icon';
                setTimeout(function () { icon.className = 'fas fa-unlock'; }, 2000);
            } else {
                AdminModal.alert({message: data.error || (T.failedUnlock || 'Failed to unlock terminal.'), type: 'error'});
            }
        })
        .catch(function () {
            btn.disabled = false;
            icon.className = 'fas fa-unlock';
            AdminModal.alert({message: T.failedUnlock || 'Failed to unlock terminal.', type: 'error'});
        });
    }

    /* ---- Event delegation for unlock buttons ---- */
    document.addEventListener('click', function (e) {
        var unlockBtn = e.target.closest('.terminal-unlock-btn');
        if (unlockBtn) {
            e.preventDefault();
            handleUnlock(unlockBtn);
        }
    });

    /* ---- Init ---- */
    document.addEventListener('DOMContentLoaded', function () {
        var el = document.getElementById('terminal-list-translations');
        if (el) { try { T = JSON.parse(el.textContent); } catch (err) {} }

        initEnableStore();

        // Only init filters if the filters panel exists (not shown on store setup page)
        if (document.getElementById('filters-panel')) {
            window.AdminListFilters.init({
                url: '/' + lang + '/admin/pos/terminals/filter/',
                resultsContainer: 'terminal-results',
                resultsCount: 'terminal-count'
            });
        }
    });
}());
