/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var config = document.getElementById('feed-sync-log-config');
        if (!config) return;

        var lang = document.documentElement.lang || 'en';
        var rawUrl = config.dataset.filterUrl;
        var url = rawUrl.charAt(0) === '/' ? rawUrl : '/' + lang + '/' + rawUrl;
        var runningCount = parseInt(config.dataset.runningCount, 10) || 0;

        window.AdminListFilters.init({
            url: url,
            resultsContainer: config.dataset.resultsContainer || 'log-results',
            resultsCount: config.dataset.resultsCount || 'log-count'
        });

        if (runningCount > 0) {
            setTimeout(function () {
                window.AdminListFilters.apply();
            }, 5000);
        }
    });

})();
