/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Affiliate Program Admin - Member Filtering
 * Handles member search/filter on the program change form.
 */
(function () {
    'use strict';

    function filterMembers() {
        var searchEl = document.getElementById('member-search');
        var statusEl = document.getElementById('member-status-filter');
        var formEl = document.querySelector('.program-change-form');
        if (!formEl) return;

        var search = searchEl ? searchEl.value : '';
        var status = statusEl ? statusEl.value : '';
        var programId = formEl.dataset.programId;
        var lang = document.documentElement.lang || 'en';

        var params = new URLSearchParams();
        if (search) params.append('search', search);
        if (status) params.append('status', status);

        var url = '/' + lang + '/admin/affiliate/programs/' + programId + '/members/filter/?' + params.toString();

        fetch(url, { method: 'GET', headers: { 'X-Requested-With': 'XMLHttpRequest' } })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                var container = document.getElementById('members-container');
                if (container) container.innerHTML = data.html;
            })
            .catch(function (err) { console.error('Member filter error:', err); });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var searchInput = document.getElementById('member-search');
        var statusFilter = document.getElementById('member-status-filter');

        if (searchInput) {
            var searchTimeout;
            searchInput.addEventListener('input', function () {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(filterMembers, 300);
            });
        }

        if (statusFilter) {
            statusFilter.addEventListener('change', filterMembers);
        }
    });

}());
