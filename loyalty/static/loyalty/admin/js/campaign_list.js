/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var translations = {};

    function init() {
        var tEl = document.getElementById('loyalty-campaign-i18n');
        if (tEl) {
            try { translations = JSON.parse(tEl.textContent); } catch (e) {}
        }
        document.addEventListener('click', handleActions);
    }

    function handleActions(e) {
        var btn = e.target.closest('[data-action="toggle-campaign-status"]');
        if (!btn) return;
        e.preventDefault();
        toggleCampaignStatus(btn.dataset.pk, btn.dataset.activate === 'true');
    }

    async function toggleCampaignStatus(campaignId, activate) {
        var action = activate ? 'activate' : 'pause';
        var message = activate
            ? (translations.confirmActivate || 'Are you sure you want to activate this campaign?')
            : (translations.confirmPause || 'Are you sure you want to pause this campaign?');

        if (!await AdminModal.confirm(message)) { return; }

        var lang = document.documentElement.lang || 'en';
        var url = '/' + lang + '/admin/loyalty/campaigns/' + campaignId + '/' + action + '/';
        var csrf = document.querySelector('[name=csrfmiddlewaretoken]');

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf ? csrf.value : ''
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                window.AdminListFilters.apply();
            } else {
                AdminModal.alert({message: data.error || translations.errorOccurred || 'An error occurred.', type: 'error'});
            }
        })
        .catch(function () {
            AdminModal.alert({message: translations.retryError || 'An error occurred. Please try again.', type: 'error'});
        });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
