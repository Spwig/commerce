/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Loyalty Admin AJAX Filters
 * Shared filtering functionality for all loyalty change_list templates
 *
 * Usage:
 * Add data-filter-endpoint attribute to #filters-panel element with the filter URL
 * Example: <div id="filters-panel" class="filters-panel" data-filter-endpoint="/en/admin/loyalty/tiers/filter/">
 */

(function () {
  'use strict';

  // Debounce helper
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Get filter endpoint from data attribute
  function getFilterEndpoint() {
    const panel = document.getElementById('filters-panel');
    const endpoint = panel?.dataset.filterEndpoint;

    if (!endpoint) {
      console.error('Filter endpoint not configured. Add data-filter-endpoint to #filters-panel');
      return null;
    }

    return endpoint;
  }

  // Apply filters with AJAX
  window.applyFilters = function () {
    const panel = document.getElementById('filters-panel');
    const container = document.getElementById('results-container');
    const endpoint = getFilterEndpoint();

    if (!endpoint) return;

    panel.classList.add('loading');

    // Collect all filter values
    const filters = {};
    const filterInputs = panel.querySelectorAll('[id^="filter-"]');

    filterInputs.forEach(input => {
      const key = input.id.replace('filter-', '');
      const value = input.value;
      if (value) {
        filters[key] = value;
      }
    });

    // Build URL with filters
    const params = new URLSearchParams();
    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        params.append(key, filters[key]);
      }
    });

    const url = params.toString() ? `${endpoint}?${params.toString()}` : endpoint;

    fetch(url, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        container.innerHTML = data.html;

        const resultsCount = document.getElementById('results-count');
        if (resultsCount) {
          resultsCount.textContent = data.count;
        }

        updateActiveFilters(filters);
        panel.classList.remove('loading');
      })
      .catch(error => {
        console.error('Filter error:', error);
        panel.classList.remove('loading');

        // Get translated error message from panel data attribute or use default
        const errorMsg =
          panel.dataset.errorMessage || 'An error occurred while filtering. Please try again.';
        AdminModal.alert({ message: errorMsg, type: 'error' });
      });
  };

  // Clear all filters
  window.clearFilters = function () {
    const panel = document.getElementById('filters-panel');
    const filterInputs = panel.querySelectorAll('[id^="filter-"]');

    filterInputs.forEach(input => {
      if (input.tagName === 'SELECT') {
        // Reset to first option or data-default value
        const defaultValue = input.dataset.default || '';
        input.value = defaultValue;
      } else {
        input.value = '';
      }
    });

    const activeFiltersContainer = document.getElementById('active-filters');
    if (activeFiltersContainer) {
      activeFiltersContainer.innerHTML = '';
    }

    applyFilters();
  };

  // Update active filter tags
  function updateActiveFilters(filters) {
    const container = document.getElementById('active-filters');
    if (!container) return;

    container.innerHTML = '';

    Object.keys(filters).forEach(key => {
      if (filters[key]) {
        const label = key.charAt(0).toUpperCase() + key.slice(1);
        let value = filters[key];

        // Get readable value for select fields
        const filterElement = document.getElementById('filter-' + key);
        if (filterElement && filterElement.tagName === 'SELECT') {
          const selectedOption = filterElement.options[filterElement.selectedIndex];
          if (selectedOption) {
            value = selectedOption.text;
          }
        }

        const tag = document.createElement('span');
        tag.className = 'active-filter-tag';
        tag.innerHTML = `${label}: ${value} <i class="fas fa-times" onclick="removeFilter('${key}')"></i>`;
        container.appendChild(tag);
      }
    });
  }

  // Remove individual filter
  window.removeFilter = function (filterKey) {
    const filterElement = document.getElementById('filter-' + filterKey);
    if (filterElement) {
      if (filterElement.tagName === 'SELECT') {
        const defaultValue = filterElement.dataset.default || '';
        filterElement.value = defaultValue;
      } else {
        filterElement.value = '';
      }
    }
    applyFilters();
  };

  // Toggle filters on mobile
  window.toggleFilters = function () {
    const panel = document.getElementById('filters-panel');
    if (!panel) return;

    panel.classList.toggle('expanded');

    const icon = document.querySelector('.filters-toggle i');
    if (icon) {
      if (panel.classList.contains('expanded')) {
        icon.className = 'fas fa-chevron-up';
      } else {
        icon.className = 'fas fa-chevron-down';
      }
    }
  };

  // Initialize when DOM is ready
  function initFilters() {
    // Debounced search on all text inputs
    const searchInputs = document.querySelectorAll('#filters-panel input[type="text"]');
    const debouncedApplyFilters = debounce(applyFilters, 300);

    searchInputs.forEach(input => {
      input.addEventListener('input', debouncedApplyFilters);
    });

    // Apply filters on select change
    const selectInputs = document.querySelectorAll('#filters-panel select');
    selectInputs.forEach(select => {
      select.addEventListener('change', applyFilters);
    });
  }

  // Auto-initialize when DOM is loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFilters);
  } else {
    initFilters();
  }
})();
