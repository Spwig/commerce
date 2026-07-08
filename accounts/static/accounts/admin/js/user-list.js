/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * User List Filters Initialization
 *
 * Initializes admin-list-filters.js for the user management change_list template.
 * Uses custom container IDs that differ from the standard admin-list-filters pattern.
 */
(function() {
    'use strict';

    function initializeUserListFilters() {
        const lang = document.documentElement.lang || 'en';

        // Initialize admin-list-filters with custom container IDs
        if (window.AdminListFilters) {
            window.AdminListFilters.init({
                url: `/${lang}/admin/users/filter/`,
                resultsContainer: 'user-results',  // Custom: user-results instead of results-container
                resultsCount: 'user-count'          // Custom: user-count instead of results-count
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeUserListFilters);
    } else {
        initializeUserListFilters();
    }
})();
