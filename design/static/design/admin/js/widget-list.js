/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const config = document.getElementById('widget-list-config');
    if (!config) return;

    const lang = document.documentElement.lang || 'en';
    const rawUrl = config.dataset.filterUrl;
    const url = rawUrl.charAt(0) === '/' ? rawUrl : '/' + lang + '/' + rawUrl;

    window.AdminListFilters.init({
      url: url,
      resultsContainer: config.dataset.resultsContainer || 'widget-results',
      resultsCount: config.dataset.resultsCount || 'widget-count',
    });

    const refreshBtn = document.getElementById('refresh-updates-btn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', function () {
        const actionSelect = document.querySelector('select[name=action]');
        const submitBtn = document.querySelector('.actions button[type=submit]');
        if (actionSelect && submitBtn) {
          actionSelect.value = 'check_for_updates_action';
          submitBtn.click();
        }
      });
    }
  });
})();
