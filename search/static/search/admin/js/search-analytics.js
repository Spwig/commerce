/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Search Analytics Dashboard
 *
 * Provides analytics filtering and dashboard stats for search query performance.
 * Displays total searches, unique queries, zero result rate, response time, and click-through rate.
 */

(function() {
    'use strict';

    /**
     * Initialize search analytics dashboard
     * @param {object} config - Configuration object
     * @param {string} config.dashboardDataUrl - URL endpoint for dashboard stats
     * @param {string} config.analyticsFilterUrl - URL endpoint for analytics query cards
     */
    function initSearchAnalytics(config) {
        const form = document.getElementById('analytics-filters');
        const resultsContainer = document.getElementById('query-results');
        const statsContainer = document.getElementById('dashboard-stats');

        if (!form || !resultsContainer || !statsContainer) {
            console.error('Required elements not found for search analytics');
            return;
        }

        // Set default date range (last 30 days)
        const today = new Date();
        const thirtyDaysAgo = new Date(today);
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

        const dateToInput = document.getElementById('date_to');
        const dateFromInput = document.getElementById('date_from');

        if (dateToInput) dateToInput.value = today.toISOString().split('T')[0];
        if (dateFromInput) dateFromInput.value = thirtyDaysAgo.toISOString().split('T')[0];

        /**
         * Load dashboard statistics and query cards
         */
        function loadDashboardData() {
            const formData = new FormData(form);
            const params = new URLSearchParams(formData);

            const headers = {'X-Requested-With': 'XMLHttpRequest'};

            // Load dashboard stats
            fetch(`${config.dashboardDataUrl}?${params}`, {headers})
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    updateStat('total_searches', data.total_searches.toLocaleString());
                    updateStat('unique_queries', data.unique_queries.toLocaleString());
                    updateStat('zero_result_rate', data.zero_result_rate + '%');
                    updateStat('avg_response_time_ms', Math.round(data.avg_response_time_ms) + 'ms');
                    updateStat('click_through_rate', data.click_through_rate + '%');
                })
                .catch(error => {
                    console.error('Failed to load dashboard stats:', error);
                });

            // Load query cards
            resultsContainer.innerHTML = '<div class="loading-indicator"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';

            fetch(`${config.analyticsFilterUrl}?${params}`, {headers})
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    resultsContainer.innerHTML = data.html || '';
                })
                .catch(error => {
                    console.error('Failed to load analytics results:', error);
                    resultsContainer.innerHTML = '<div class="error">Failed to load results. Please try again.</div>';
                });
        }

        /**
         * Update a stat value in the dashboard
         */
        function updateStat(statName, value) {
            const element = document.querySelector(`[data-stat="${statName}"]`);
            if (element) {
                element.textContent = value;
            }
        }

        // Initial load
        loadDashboardData();

        // Form submit handler
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            loadDashboardData();
        });

        // Debounced search input
        let searchTimeout;
        const searchInput = document.getElementById('search');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(loadDashboardData, 300);
            });
        }
    }

    // Export to global scope
    window.SearchAnalytics = {
        init: initSearchAnalytics
    };

})();

// Auto-initialize from data island if present
document.addEventListener('DOMContentLoaded', function() {
    var dataEl = document.getElementById('search-analytics-data');
    if (dataEl) {
        var cfg = JSON.parse(dataEl.textContent);
        window.SearchAnalytics.init(cfg);
    }
});
