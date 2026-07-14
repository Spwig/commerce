/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  function updateSummaryDashboard(data) {
    if (!data.stats) return;
    const s = data.stats;
    const set = function (id, val) {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };
    set('summary-total-items', s.total_items);
    set('summary-on-hand', Math.round(s.total_on_hand));
    set('summary-allocated', Math.round(s.total_allocated));
    set('summary-available', Math.round(s.total_available));
    set('summary-low-stock', s.low_stock_count);
    set('summary-out-of-stock', s.out_of_stock_count);
  }

  document.addEventListener('DOMContentLoaded', function () {
    const config = document.getElementById('stockitem-list-config');
    if (!config) return;

    const lang = document.documentElement.lang || 'en';
    const rawUrl = config.dataset.filterUrl;
    const url = rawUrl.charAt(0) === '/' ? rawUrl : '/' + lang + '/' + rawUrl;

    window.AdminListFilters.init({
      url: url,
      resultsContainer: config.dataset.resultsContainer || 'stockitem-results',
      resultsCount: config.dataset.resultsCount || 'stockitem-count',
      onUpdate: updateSummaryDashboard,
    });
  });
})();
