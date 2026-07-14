/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Return Request Admin List - Filter and search functionality
 */
(function () {
  'use strict';

  // Get translations from data island
  let t = {};
  let searchTimeout;

  function toggleFilters() {
    const fields = document.getElementById('filters-panel-fields');
    const toggle = document.querySelector('.filters-toggle i');
    if (fields.classList.contains('d-none')) {
      fields.classList.remove('d-none');
      toggle.classList.replace('fa-chevron-right', 'fa-chevron-down');
    } else {
      fields.classList.add('d-none');
      toggle.classList.replace('fa-chevron-down', 'fa-chevron-right');
    }
  }

  function applyFilters() {
    const params = new URLSearchParams();
    const search = document.getElementById('filter-search').value.trim();
    const status = document.getElementById('filter-status').value;
    const reason = document.getElementById('filter-reason').value;

    if (search) params.append('q', search);
    if (status) params.append('status__exact', status);
    if (reason) params.append('reason__exact', reason);

    const queryString = params.toString();
    window.location.href = window.location.pathname + (queryString ? '?' + queryString : '');
  }

  function clearFilters() {
    document.getElementById('filter-search').value = '';
    document.getElementById('filter-status').value = '';
    document.getElementById('filter-reason').value = '';
    window.location.href = window.location.pathname;
  }

  function clearSingleFilter(filterId) {
    document.getElementById(filterId).value = '';
    applyFilters();
  }

  function updateActiveFilters() {
    const container = document.getElementById('active-filters');
    const search = document.getElementById('filter-search').value.trim();
    const status = document.getElementById('filter-status').value;
    const reason = document.getElementById('filter-reason').value;

    let html = '';
    let hasFilters = false;

    if (search) {
      hasFilters = true;
      html += `<span class="active-filter-tag">${t.search || 'Search'}: ${search}
                <i class="fas fa-times" data-action="clear-single-filter" data-filter-id="filter-search"></i>
            </span>`;
    }
    if (status) {
      hasFilters = true;
      const label = document.getElementById('filter-status').selectedOptions[0].text;
      html += `<span class="active-filter-tag">${t.status || 'Status'}: ${label}
                <i class="fas fa-times" data-action="clear-single-filter" data-filter-id="filter-status"></i>
            </span>`;
    }
    if (reason) {
      hasFilters = true;
      const label = document.getElementById('filter-reason').selectedOptions[0].text;
      html += `<span class="active-filter-tag">${t.reason || 'Reason'}: ${label}
                <i class="fas fa-times" data-action="clear-single-filter" data-filter-id="filter-reason"></i>
            </span>`;
    }

    if (hasFilters) {
      html = `<span class="active-filters-label">${t.active || 'Active:'}}</span>` + html;
    }
    container.innerHTML = html;
  }

  // Event delegation
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const action = btn.dataset.action;

    if (action === 'toggle-filters') {
      e.preventDefault();
      toggleFilters();
    } else if (action === 'apply-filters') {
      e.preventDefault();
      applyFilters();
    } else if (action === 'clear-filters') {
      e.preventDefault();
      clearFilters();
    } else if (action === 'clear-single-filter') {
      e.preventDefault();
      clearSingleFilter(btn.dataset.filterId);
    }
  });

  // Initialize on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', function () {
    // Load translations from data island
    const translationsEl = document.getElementById('return-request-translations');
    if (translationsEl) {
      try {
        t = JSON.parse(translationsEl.textContent);
      } catch (e) {
        console.error('Failed to parse translations:', e);
      }
    }

    // Search input with debounce
    const searchInput = document.getElementById('filter-search');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(applyFilters, 300);
      });
    }

    // Filter inputs
    ['filter-status', 'filter-reason'].forEach(function (id) {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('change', applyFilters);
      }
    });

    updateActiveFilters();
  });
})();
