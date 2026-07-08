/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    'use strict';

    var msgs = {
        checking: 'Checking...',
        failedToCheck: 'Failed to check for updates.',
        errorChecking: 'Error checking for updates. Please try again.'
    };

    document.addEventListener('DOMContentLoaded', function () {
        var island = document.getElementById('component-registry-i18n');
        if (island) {
            try { msgs = JSON.parse(island.textContent); } catch (e) { }
        }

        var config = document.getElementById('component-registry-config');
        if (config) {
            var langPrefix = AdminUtils.getLanguagePrefix();
            var rawUrl = config.dataset.filterUrl;
            var url = rawUrl.charAt(0) === '/' ? rawUrl : langPrefix + '/' + rawUrl;

            window.AdminListFilters.init({
                url: url,
                resultsContainer: config.dataset.resultsContainer || 'component-results',
                resultsCount: config.dataset.resultsCount || 'component-count'
            });
        }

        document.addEventListener('click', function (e) {
            var btn = e.target.closest('[data-action="check-all-updates"]');
            if (btn) {
                checkAllForUpdates(btn);
            }
        });
    });

    function checkAllForUpdates(btn) {
        var originalContent = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + msgs.checking;
        btn.disabled = true;

        var langPrefix = AdminUtils.getLanguagePrefix();
        var checkUrl = langPrefix + '/admin/component_updates/componentregistry/check-updates/';

        fetch(checkUrl, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            }
        })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            btn.innerHTML = originalContent;
            btn.disabled = false;

            if (data.success) {
                window.location.reload();
            } else {
                AdminModal.alert({message: data.error || msgs.failedToCheck, type: 'error'});
            }
        })
        .catch(function (error) {
            console.error('Error checking for updates:', error);
            btn.innerHTML = originalContent;
            btn.disabled = false;
            AdminModal.alert({message: msgs.errorChecking, type: 'error'});
        });
    }

})();
