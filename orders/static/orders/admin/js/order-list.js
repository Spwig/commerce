/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Order List Admin
 * Initializes flatpickr date pickers and admin table toggle for the order change list.
 */
(function () {
    'use strict';

    function init() {
        // Initialize date pickers
        if (typeof flatpickr !== 'undefined') {
            var dateFrom = document.getElementById('date-from');
            var dateTo = document.getElementById('date-to');
            if (dateFrom) flatpickr(dateFrom, { dateFormat: 'Y-m-d' });
            if (dateTo) flatpickr(dateTo, { dateFormat: 'Y-m-d' });
        }

        // Show admin table view
        var showAdminTableBtn = document.getElementById('show-admin-table-btn');
        if (showAdminTableBtn) {
            showAdminTableBtn.addEventListener('click', function () {
                var container = document.querySelector('.orders-management-container');
                var tableView = document.getElementById('admin-table-view');
                if (container) container.classList.add('hidden');
                if (tableView) tableView.classList.add('visible');
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}());
