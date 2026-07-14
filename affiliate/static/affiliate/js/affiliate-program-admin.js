/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Affiliate Program Admin - Member Filtering
 * Handles member search/filter on the program change form.
 */
(function () {
  'use strict';

  function filterMembers() {
    const searchEl = document.getElementById('member-search');
    const statusEl = document.getElementById('member-status-filter');
    const formEl = document.querySelector('.program-change-form');
    if (!formEl) return;

    const search = searchEl ? searchEl.value : '';
    const status = statusEl ? statusEl.value : '';
    const programId = formEl.dataset.programId;
    const lang = document.documentElement.lang || 'en';

    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (status) params.append('status', status);

    const url =
      '/' +
      lang +
      '/admin/affiliate/programs/' +
      programId +
      '/members/filter/?' +
      params.toString();

    fetch(url, { method: 'GET', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        const container = document.getElementById('members-container');
        if (container) container.innerHTML = data.html;
      })
      .catch(function (err) {
        console.error('Member filter error:', err);
      });
  }

  document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('member-search');
    const statusFilter = document.getElementById('member-status-filter');

    if (searchInput) {
      let searchTimeout;
      searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(filterMembers, 300);
      });
    }

    if (statusFilter) {
      statusFilter.addEventListener('change', filterMembers);
    }
  });
})();
