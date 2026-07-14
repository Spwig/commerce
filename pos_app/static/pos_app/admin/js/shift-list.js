/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  const lang = document.documentElement.lang || 'en';

  document.addEventListener('DOMContentLoaded', function () {
    window.AdminListFilters.init({
      url: '/' + lang + '/admin/pos/shifts/filter/',
      resultsContainer: 'shift-results',
      resultsCount: 'shift-count',
      onUpdate: function (data) {
        if (data.counts) {
          const all = document.getElementById('count-all');
          const open = document.getElementById('count-open');
          const closed = document.getElementById('count-closed');
          if (all) all.textContent = data.counts.all;
          if (open) open.textContent = data.counts.open;
          if (closed) closed.textContent = data.counts.closed;
        }
      },
    });
  });

  document.addEventListener('click', function (e) {
    const tab = e.target.closest('[data-action="set-shift-tab"]');
    if (!tab) return;
    e.preventDefault();

    document.querySelectorAll('.pos-filter-tab').forEach(function (t) {
      t.classList.remove('active');
    });
    tab.classList.add('active');

    const statusInput = document.getElementById('filter-shift_status');
    if (statusInput) statusInput.value = tab.dataset.status || '';

    window.AdminListFilters.apply();
  });
})();
