/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    'use strict';

    var msgs = {
        confirmActivate: 'Are you sure you want to activate this rule?',
        confirmDeactivate: 'Are you sure you want to deactivate this rule?',
        errorOccurred: 'An error occurred.',
        retryError: 'An error occurred. Please try again.'
    };

    document.addEventListener('DOMContentLoaded', function () {
        var island = document.getElementById('loyalty-rule-i18n');
        if (island) {
            try { msgs = JSON.parse(island.textContent); } catch (e) { }
        }
    });

    async function toggleRuleStatus(ruleId, activate) {
        var action = activate ? 'activate' : 'deactivate';
        var message = activate ? msgs.confirmActivate : msgs.confirmDeactivate;

        if (!await AdminModal.confirm(message)) {
            return;
        }

        var languageCode = document.documentElement.lang || 'en';
        var url = '/' + languageCode + '/admin/loyalty/rules/' + ruleId + '/' + action + '/';
        var csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfEl ? csrfEl.value : ''
            }
        })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            if (data.success) {
                window.AdminListFilters.apply();
            } else {
                AdminModal.alert({message: data.error || msgs.errorOccurred, type: 'error'});
            }
        })
        .catch(function (error) {
            console.error('Toggle error:', error);
            AdminModal.alert({message: msgs.retryError, type: 'error'});
        });
    }

    window.toggleRuleStatus = toggleRuleStatus;

})();
