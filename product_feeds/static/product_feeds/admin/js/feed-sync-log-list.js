/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const config = document.getElementById('feed-sync-log-config');
    if (!config) return;

    const lang = document.documentElement.lang || 'en';
    const rawUrl = config.dataset.filterUrl;
    const url = rawUrl.charAt(0) === '/' ? rawUrl : '/' + lang + '/' + rawUrl;
    const runningCount = parseInt(config.dataset.runningCount, 10) || 0;

    window.AdminListFilters.init({
      url: url,
      resultsContainer: config.dataset.resultsContainer || 'log-results',
      resultsCount: config.dataset.resultsCount || 'log-count',
    });

    if (runningCount > 0) {
      setTimeout(function () {
        window.AdminListFilters.apply();
      }, 5000);
    }
  });
})();
