/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var config = document.getElementById('widget-list-config');
        if (!config) return;

        var lang = document.documentElement.lang || 'en';
        var rawUrl = config.dataset.filterUrl;
        var url = rawUrl.charAt(0) === '/' ? rawUrl : '/' + lang + '/' + rawUrl;

        window.AdminListFilters.init({
            url: url,
            resultsContainer: config.dataset.resultsContainer || 'widget-results',
            resultsCount: config.dataset.resultsCount || 'widget-count'
        });

        var refreshBtn = document.getElementById('refresh-updates-btn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', function () {
                var actionSelect = document.querySelector('select[name=action]');
                var submitBtn = document.querySelector('.actions button[type=submit]');
                if (actionSelect && submitBtn) {
                    actionSelect.value = 'check_for_updates_action';
                    submitBtn.click();
                }
            });
        }
    });

})();
