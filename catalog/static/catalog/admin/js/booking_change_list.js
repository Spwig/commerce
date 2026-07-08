/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var configEl = document.getElementById('booking-calendar-config');
        if (!configEl) return;

        var config;
        try {
            config = JSON.parse(configEl.textContent);
        } catch (e) {
            return;
        }

        document.querySelectorAll('[data-action="calendar-filter"]').forEach(function (el) {
            el.addEventListener('change', function () {
                var statusEl = document.getElementById('filter-status');
                var productEl = document.getElementById('filter-product');
                var status = statusEl ? statusEl.value : '';
                var product = productEl ? productEl.value : '';

                var viewMode = config.viewMode || 'calendar';
                var url = '?view=' + viewMode;

                if (viewMode === 'calendar') {
                    url += '&year=' + config.calendarYear + '&month=' + config.calendarMonth;
                } else if (viewMode === 'week' || viewMode === 'day') {
                    url += '&year=' + config.calendarYear + '&month=' + config.calendarMonth + '&day=' + config.calendarDay;
                }

                if (status) url += '&status__exact=' + status;
                if (product) url += '&product__id__exact=' + product;
                window.location.href = url;
            });
        });
    });
})();
