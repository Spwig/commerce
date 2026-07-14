/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Subscription Admin Interface JavaScript
 * Handles filter panel interactions and AJAX filtering
 * Follows design rules from change_list_rules.md
 */

(function () {
  'use strict';

  // Configuration - auto-detect results container
  const resultsContainer =
    document.getElementById('plan-results') || document.getElementById('subscription-results');
  const resultsContainerId = resultsContainer ? resultsContainer.id : null;

  const CONFIG = {
    debounceDelay: 300, // ms delay for filter input
    filterPanelId: 'filters-panel',
    resultsContainerId: resultsContainerId,
    storageKey: 'subscriptions_filters_collapsed',
  };

  // State
  let filterDebounceTimer = null;
  let currentFilters = {};

  /**
   * Initialize the subscription admin interface
   */
  function init() {
    initFilterPanel();
    initFilterInputs();
    initClearFilters();
    loadFiltersFromURL();
    restoreFilterPanelState();
  }

  /**
   * Initialize filter panel collapse/expand functionality
   */
  function initFilterPanel() {
    const panel = document.getElementById(CONFIG.filterPanelId);
    if (!panel) return;

    const header = panel.querySelector('.filters-panel-header');
    if (!header) return;

    header.addEventListener('click', function () {
      panel.classList.toggle('collapsed');

      // Save state to localStorage
      const isCollapsed = panel.classList.contains('collapsed');
      localStorage.setItem(CONFIG.storageKey, isCollapsed ? '1' : '0');
    });
  }

  /**
   * Restore filter panel collapsed state from localStorage
   */
  function restoreFilterPanelState() {
    const panel = document.getElementById(CONFIG.filterPanelId);
    if (!panel) return;

    const isCollapsed = localStorage.getItem(CONFIG.storageKey) === '1';
    if (isCollapsed) {
      panel.classList.add('collapsed');
    }
  }

  /**
   * Initialize filter input listeners with debouncing
   */
  function initFilterInputs() {
    const panel = document.getElementById(CONFIG.filterPanelId);
    if (!panel) return;

    // Get all filter inputs and selects
    const inputs = panel.querySelectorAll('input[name^="filter_"], select[name^="filter_"]');

    inputs.forEach(input => {
      if (input.tagName === 'SELECT') {
        // Immediate filtering for dropdowns
        input.addEventListener('change', handleFilterChange);
      } else {
        // Debounced filtering for text inputs
        input.addEventListener('input', handleFilterInputDebounced);
      }
    });
  }

  /**
   * Handle filter input change with debouncing
   */
  function handleFilterInputDebounced(event) {
    clearTimeout(filterDebounceTimer);

    filterDebounceTimer = setTimeout(() => {
      handleFilterChange(event);
    }, CONFIG.debounceDelay);
  }

  /**
   * Handle filter change and trigger AJAX request
   */
  function handleFilterChange(event) {
    const input = event.target;
    const filterName = input.name.replace('filter_', '');
    const filterValue = input.value.trim();

    // Update current filters
    if (filterValue) {
      currentFilters[filterName] = filterValue;
    } else {
      delete currentFilters[filterName];
    }

    // Update URL without reload
    updateURL();

    // Fetch filtered results
    fetchFilteredResults();
  }

  /**
   * Load filters from URL parameters
   */
  function loadFiltersFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const panel = document.getElementById(CONFIG.filterPanelId);
    if (!panel) return;

    urlParams.forEach((value, key) => {
      if (key.startsWith('filter_')) {
        const filterName = key.replace('filter_', '');
        currentFilters[filterName] = value;

        // Set input value
        const input = panel.querySelector(`[name="${key}"]`);
        if (input) {
          input.value = value;
        }
      }
    });
  }

  /**
   * Update URL with current filters without page reload
   */
  function updateURL() {
    const url = new URL(window.location);

    // Clear existing filter params
    const params = new URLSearchParams(url.search);
    const keysToDelete = [];
    params.forEach((value, key) => {
      if (key.startsWith('filter_')) {
        keysToDelete.push(key);
      }
    });
    keysToDelete.forEach(key => params.delete(key));

    // Add current filters
    Object.keys(currentFilters).forEach(filterName => {
      params.set(`filter_${filterName}`, currentFilters[filterName]);
    });

    // Update URL
    url.search = params.toString();
    window.history.pushState({}, '', url);
  }

  /**
   * Fetch filtered results via AJAX
   */
  function fetchFilteredResults() {
    const resultsContainer = document.getElementById(CONFIG.resultsContainerId);
    if (!resultsContainer) return;

    // Show loading state
    showLoadingState(resultsContainer);

    // Build query string
    const params = new URLSearchParams();
    Object.keys(currentFilters).forEach(filterName => {
      params.set(`filter_${filterName}`, currentFilters[filterName]);
    });
    params.set('ajax', '1'); // Mark as AJAX request

    // Get current URL path with language prefix
    const currentPath = window.location.pathname;
    const url = `${currentPath}?${params.toString()}`;

    // Fetch results
    fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        Accept: 'text/html',
      },
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
      })
      .then(html => {
        // Update results container
        resultsContainer.innerHTML = html;

        // Re-initialize any event listeners on new content
        initResultsListeners();
      })
      .catch(error => {
        console.error('Error fetching filtered results:', error);
        showErrorState(resultsContainer, error.message);
      });
  }

  /**
   * Show loading state in results container
   */
  function showLoadingState(container) {
    const loadingText =
      CONFIG.resultsContainerId === 'plan-results'
        ? 'Loading subscription plans...'
        : 'Loading subscriptions...';

    container.innerHTML = `
            <div class="loading">
                <i class="fas fa-spinner fa-spin"></i>
                <span>${loadingText}</span>
            </div>
        `;
  }

  /**
   * Show error state in results container
   */
  function showErrorState(container, message) {
    const errorText =
      CONFIG.resultsContainerId === 'plan-results'
        ? 'Error loading subscription plans'
        : 'Error loading subscriptions';

    container.innerHTML = `
            <div class="list-row-card card-empty-state card-error-state">
                <div class="card-empty-state-icon card-error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <p class="card-empty-state-title card-error-title">
                    ${errorText}
                </p>
                <p class="card-empty-state-subtitle">
                    ${escapeHtml(message)}
                </p>
                <button type="button" class="button card-error-reload-btn" data-action="reload-page">
                    <i class="fas fa-redo"></i> Reload Page
                </button>
            </div>
        `;

    // Bind reload button via event delegation (no inline onclick)
    const reloadBtn = container.querySelector('[data-action="reload-page"]');
    if (reloadBtn) {
      reloadBtn.addEventListener('click', function () {
        location.reload();
      });
    }
  }

  /**
   * Initialize event listeners on results (checkboxes, etc.)
   */
  function initResultsListeners() {
    // Re-initialize Django admin select all functionality if present
    if (typeof django !== 'undefined' && django.jQuery && CONFIG.resultsContainerId) {
      const $ = django.jQuery;
      const $results = $(`#${CONFIG.resultsContainerId}`);

      // Reinitialize action checkboxes
      $results
        .find('.action-select')
        .off('click')
        .on('click', function () {
          const $checkbox = $(this);
          const $row = $checkbox.closest('.list-row-card');
          $row.toggleClass('selected', $checkbox.prop('checked'));
        });
    }
  }

  /**
   * Initialize clear filters button
   */
  function initClearFilters() {
    const clearButton = document.querySelector('.clear-filters');
    if (!clearButton) return;

    clearButton.addEventListener('click', function (e) {
      e.preventDefault();
      clearAllFilters();
    });
  }

  /**
   * Clear all filters and reload
   */
  function clearAllFilters() {
    currentFilters = {};

    // Clear all filter inputs
    const panel = document.getElementById(CONFIG.filterPanelId);
    if (panel) {
      const inputs = panel.querySelectorAll('input[name^="filter_"], select[name^="filter_"]');
      inputs.forEach(input => {
        input.value = '';
      });
    }

    // Update URL and fetch results
    updateURL();
    fetchFilteredResults();
  }

  /**
   * Escape HTML to prevent XSS
   */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Handle browser back/forward buttons
   */
  window.addEventListener('popstate', function () {
    loadFiltersFromURL();
    fetchFilteredResults();
  });

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
