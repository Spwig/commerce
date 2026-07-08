/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin List View Filters - Shared functionality for filterable change lists
 *
 * Provides filter panel UI, AJAX filtering, and active filter tag management
 * for admin list views (gift cards, promotions, license pools, etc.)
 *
 * Usage:
 * 1. Include this script in your change_list template
 * 2. Use data-action attributes instead of onclick
 * 3. Implement a filter endpoint that returns {html, count}
 */

(function() {
    'use strict';

    // Module state
    let searchTimeout = null;
    let filterUrl = null;
    let onUpdateCallback = null;
    let extraParams = null;  // Static params merged into every filter request (e.g. tab state)

    /**
     * Initialize filter panel for a list view
     * @param {string|object} urlOrConfig - Filter endpoint URL or config object
     *   If string: URL only (uses default container IDs)
     *   If object: { url, resultsContainer, resultsCount, onUpdate, filters }
     */
    function initFilters(urlOrConfig) {
        // Support both string URL and config object
        if (typeof urlOrConfig === 'string') {
            filterUrl = urlOrConfig;
        } else {
            filterUrl = urlOrConfig.url;
            if (urlOrConfig.resultsContainer) {
                window.__adminListFilters_resultsContainer = urlOrConfig.resultsContainer;
            }
            if (urlOrConfig.resultsCount) {
                window.__adminListFilters_resultsCount = urlOrConfig.resultsCount;
            }
            if (urlOrConfig.onUpdate && typeof urlOrConfig.onUpdate === 'function') {
                onUpdateCallback = urlOrConfig.onUpdate;
            }
            if (urlOrConfig.extraParams) {
                // Accept a query string like "is_active=1&is_retail=0" or a plain object
                if (typeof urlOrConfig.extraParams === 'string') {
                    extraParams = new URLSearchParams(urlOrConfig.extraParams);
                } else {
                    extraParams = new URLSearchParams(urlOrConfig.extraParams);
                }
            }
        }

        // Event delegation for all filter actions
        document.addEventListener('click', handleFilterActions);

        // Initialize search debouncing
        const searchInput = document.getElementById('filter-search');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(applyFilters, 300);
            });
        }

        // Auto-apply on select change
        document.querySelectorAll('[id^="filter-"]').forEach(function(el) {
            if (el.tagName === 'SELECT') {
                el.addEventListener('change', applyFilters);
            }
        });

        // Initialize checkboxes
        initCheckboxes();
    }

    /**
     * Handle all filter-related click events via delegation
     */
    function handleFilterActions(e) {
        // Find the nearest element with data-action (handles clicks on child elements like icons)
        const actionElement = e.target.closest('[data-action]');
        if (!actionElement) return;

        const action = actionElement.dataset.action;
        if (!action) return;

        switch (action) {
            case 'toggle-filters':
                toggleFilters();
                break;
            case 'apply-filters':
                e.preventDefault();
                applyFilters();
                break;
            case 'clear-filters':
                e.preventDefault();
                clearFilters();
                break;
            case 'remove-filter':
                e.preventDefault();
                removeFilter(actionElement);
                break;
            case 'reload-page':
                location.reload();
                break;
        }
    }

    /**
     * Toggle filters panel visibility
     */
    function toggleFilters() {
        const panel = document.getElementById('filters-panel');
        const fields = document.getElementById('filters-panel-fields');
        const toggle = document.querySelector('[data-action="toggle-filters"]');

        if (!panel || !fields) return;

        const isExpanded = !fields.hidden;
        fields.hidden = isExpanded;
        panel.classList.toggle('filters-panel--collapsed', isExpanded);

        if (toggle) {
            const icon = toggle.querySelector('i');
            if (icon) {
                icon.className = isExpanded ? 'fas fa-chevron-down' : 'fas fa-chevron-up';
            }
        }
    }

    /**
     * Apply current filters via AJAX
     */
    function applyFilters() {
        if (!filterUrl) {
            console.error('Filter URL not configured. Call initFilters(url) first.');
            return;
        }

        const params = collectFilterParams();
        const url = `${filterUrl}?${params.toString()}`;

        // Show loading state
        const containerId = window.__adminListFilters_resultsContainer || 'results-container';
        const summaryId = window.__adminListFilters_resultsCount || 'results-count';
        const container = document.getElementById(containerId);
        const summary = document.getElementById(summaryId);
        if (container) {
            container.classList.add('loading');
        }

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (container) {
                container.innerHTML = data.html || '';
                container.classList.remove('loading');
            }
            if (summary) {
                summary.textContent = data.count || 0;
            }
            updateActiveFilters(params);
            initCheckboxes(); // Re-init checkboxes for new content

            // Call custom update callback if provided
            if (onUpdateCallback) {
                onUpdateCallback(data);
            }
        })
        .catch(error => {
            console.error('Filter error:', error);
            if (container) {
                container.classList.remove('loading');
                container.innerHTML = '<div class="error">Failed to load results. Please try again.</div>';
            }
        });
    }

    /**
     * Collect all filter parameters
     */
    function collectFilterParams() {
        const params = new URLSearchParams();

        // Merge static extra params first (e.g. tab state preserved from page URL)
        if (extraParams) {
            extraParams.forEach(function(value, key) {
                params.append(key, value);
            });
        }

        // Collect all filter inputs
        document.querySelectorAll('[id^="filter-"]').forEach(function(el) {
            const name = el.id.replace('filter-', '');
            const value = el.value.trim();
            if (value) {
                params.append(name, value);
            }
        });

        return params;
    }

    /**
     * Clear all filters
     */
    function clearFilters() {
        // Clear all filter inputs
        document.querySelectorAll('[id^="filter-"]').forEach(function(el) {
            if (el.tagName === 'SELECT') {
                el.selectedIndex = 0;
            } else {
                el.value = '';
            }
        });

        // Clear active filters display
        const activeFilters = document.getElementById('active-filters');
        if (activeFilters) {
            activeFilters.innerHTML = '';
        }

        // Reload with no filters
        applyFilters();
    }

    /**
     * Remove a specific filter tag
     */
    function removeFilter(element) {
        // Get filter ID from data attribute
        const filterId = element.dataset.filterId;
        if (filterId) {
            const filterInput = document.getElementById(filterId);
            if (filterInput) {
                if (filterInput.tagName === 'SELECT') {
                    filterInput.selectedIndex = 0;
                } else {
                    filterInput.value = '';
                }
            }
        }

        // Remove the tag and reapply filters
        element.closest('.active-filter-tag').remove();
        applyFilters();
    }

    /**
     * Update active filter tags display
     */
    function updateActiveFilters(params) {
        const container = document.getElementById('active-filters');
        if (!container) return;

        let html = '';
        const entries = Array.from(params.entries());

        entries.forEach(([key, value]) => {
            const filterId = `filter-${key}`;
            const filterEl = document.getElementById(filterId);
            let displayText = value;

            // For selects, get the selected option text
            if (filterEl && filterEl.tagName === 'SELECT') {
                const selectedOption = filterEl.options[filterEl.selectedIndex];
                if (selectedOption) {
                    displayText = selectedOption.text;
                }
            }

            // Capitalize first letter of key for display
            const label = key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ');

            html += `
                <span class="active-filter-tag">
                    ${label}: ${escapeHtml(displayText)}
                    <i class="fas fa-times" data-action="remove-filter" data-filter-id="${filterId}"></i>
                </span>
            `;
        });

        container.innerHTML = html;
    }

    /**
     * Initialize checkbox selection for bulk actions
     */
    function initCheckboxes() {
        const selectAll = document.querySelector('.action-select-all');
        const checkboxes = document.querySelectorAll('.action-select');

        if (selectAll) {
            // Remove old listener by cloning
            const newSelectAll = selectAll.cloneNode(true);
            selectAll.parentNode.replaceChild(newSelectAll, selectAll);

            newSelectAll.addEventListener('change', function() {
                checkboxes.forEach(cb => cb.checked = this.checked);
                updateActionCounter();
            });
        }

        checkboxes.forEach(cb => {
            cb.addEventListener('change', updateActionCounter);
        });

        updateActionCounter();
    }

    /**
     * Update bulk action counter
     */
    function updateActionCounter() {
        const checked = document.querySelectorAll('.action-select:checked').length;
        const total = document.querySelectorAll('.action-select').length;
        const counter = document.querySelector('.action-counter');

        if (counter) {
            counter.textContent = `${checked} of ${total}`;
        }
    }

    /**
     * Escape HTML to prevent XSS in filter tags
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text || '';
        return div.innerHTML;
    }

    // Export to global scope for template initialization
    window.AdminListFilters = {
        init: initFilters,
        apply: applyFilters,
        clear: clearFilters,
        toggle: toggleFilters
    };


// Auto-initialize from data-div if present
document.addEventListener('DOMContentLoaded', function() {
    var config = document.getElementById('list-filter-config');
    if (config && config.dataset.filterUrl) {
        var lang = document.documentElement.lang || 'en';
        // If data-filter-url starts with '/', it is already an absolute path
        // (e.g. rendered by Django {% url %} tag) — use as-is.
        // Otherwise it is a suffix that needs the language prefix prepended.
        var rawUrl = config.dataset.filterUrl;
        var url = rawUrl.charAt(0) === '/' ? rawUrl : '/' + lang + rawUrl;

        // Build extra params from URL search params listed in data-filter-tab-params,
        // or from a literal query string in data-filter-extra-params.
        var extra = null;
        if (config.dataset.filterTabParams) {
            // data-filter-tab-params="is_active,is_retail" — read these from the current URL
            var urlParams = new URLSearchParams(window.location.search);
            var tabKeys = config.dataset.filterTabParams.split(',');
            var tabParts = [];
            tabKeys.forEach(function(key) {
                key = key.trim();
                var val = urlParams.get(key);
                if (val !== null && val !== '') {
                    tabParts.push(key + '=' + encodeURIComponent(val));
                }
            });
            if (tabParts.length > 0) {
                extra = tabParts.join('&');
            }
        } else if (config.dataset.filterExtraParams) {
            extra = config.dataset.filterExtraParams;
        }

        initFilters({
            url: url,
            resultsContainer: config.dataset.resultsContainer || undefined,
            resultsCount: config.dataset.resultsCount || undefined,
            extraParams: extra || undefined
        });

        // If data-auto-load="true", trigger an initial load on page ready
        if (config.dataset.autoLoad === 'true') {
            applyFilters();
        }
    }
});
})();
