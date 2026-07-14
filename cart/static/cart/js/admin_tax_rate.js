/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Tax Rate Admin - Filtering, Preset Loading, and Interactions
 */
(function () {
  'use strict';

  // Read config from data element
  const configEl = document.getElementById('tax-rate-config');
  const TAX_FILTER_URL = configEl ? configEl.dataset.filterUrl : '';
  const TAX_PRESET_URL = configEl ? configEl.dataset.presetUrl : '';

  let searchTimeout;
  const DEBOUNCE_MS = 300;

  // ==========================================
  // AJAX Filtering
  // ==========================================

  function applyFilters() {
    const panel = document.getElementById('filters-panel');
    panel.classList.add('loading');

    const params = new URLSearchParams();
    const search = document.getElementById('filter-search').value;
    const country = document.getElementById('filter-country').value;
    const taxType = document.getElementById('filter-tax-type').value;
    const status = document.getElementById('filter-status').value;

    if (search) params.append('search', search);
    if (country) params.append('country', country);
    if (taxType) params.append('tax_type', taxType);
    if (status) params.append('status', status);

    fetch(TAX_FILTER_URL + '?' + params.toString(), {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(response => response.json())
      .then(data => {
        document.getElementById('tax-results').innerHTML = data.html;
        document.getElementById('tax-count').textContent = data.count;
        updateActiveFilters();
        panel.classList.remove('loading');
      })
      .catch(error => {
        console.error('Filter error:', error);
        panel.classList.remove('loading');
      });
  }

  function clearFilters() {
    document.getElementById('filter-search').value = '';
    document.getElementById('filter-country').value = '';
    document.getElementById('filter-tax-type').value = '';
    document.getElementById('filter-status').value = '';
    applyFilters();
  }

  function clearSingleFilter(filterId) {
    const el = document.getElementById(filterId);
    if (el) {
      el.value = '';
      applyFilters();
    }
  }

  function updateActiveFilters() {
    const container = document.getElementById('active-filters');
    const search = document.getElementById('filter-search').value;
    const country = document.getElementById('filter-country');
    const taxType = document.getElementById('filter-tax-type');
    const status = document.getElementById('filter-status');

    const tags = [];

    if (search) {
      tags.push(
        '<span class="active-filter-tag">Search: ' +
          search +
          ' <i class="fas fa-times" data-action="clear-single-filter" data-filter-id="filter-search"></i></span>'
      );
    }
    if (country.value) {
      tags.push(
        '<span class="active-filter-tag">Country: ' +
          country.options[country.selectedIndex].text +
          ' <i class="fas fa-times" data-action="clear-single-filter" data-filter-id="filter-country"></i></span>'
      );
    }
    if (taxType.value) {
      tags.push(
        '<span class="active-filter-tag">Type: ' +
          taxType.options[taxType.selectedIndex].text +
          ' <i class="fas fa-times" data-action="clear-single-filter" data-filter-id="filter-tax-type"></i></span>'
      );
    }
    if (status.value) {
      tags.push(
        '<span class="active-filter-tag">Status: ' +
          status.options[status.selectedIndex].text +
          ' <i class="fas fa-times" data-action="clear-single-filter" data-filter-id="filter-status"></i></span>'
      );
    }

    if (tags.length > 0) {
      container.innerHTML = '<span class="active-filters-label">Active:</span> ' + tags.join('');
    } else {
      container.innerHTML = '';
    }
  }

  // ==========================================
  // Event Listeners
  // ==========================================

  document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('filter-search');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(applyFilters, DEBOUNCE_MS);
      });
    }

    const selects = ['filter-country', 'filter-tax-type', 'filter-status'];
    selects.forEach(function (id) {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('change', applyFilters);
      }
    });
  });

  // ==========================================
  // Presets Modal
  // ==========================================

  function showPresetsModal() {
    document.getElementById('presets-modal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }

  function hidePresetsModal() {
    document.getElementById('presets-modal').style.display = 'none';
    document.body.style.overflow = '';
  }

  function loadPreset(groupKey, btnEl) {
    btnEl.disabled = true;
    btnEl.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';

    fetch(TAX_PRESET_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify({ group_key: groupKey }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const card = btnEl.closest('.preset-card');
          card.classList.add('loaded');
          btnEl.innerHTML = '<i class="fas fa-check"></i> Loaded';

          showNotification(
            data.created +
              ' rates added' +
              (data.skipped > 0 ? ', ' + data.skipped + ' already existed' : ''),
            'success'
          );

          // Refresh the list after a short delay
          setTimeout(function () {
            applyFilters();
          }, 500);
        } else {
          btnEl.disabled = false;
          btnEl.innerHTML = '<i class="fas fa-download"></i> Load';
          showNotification(data.error || 'Failed to load preset', 'error');
        }
      })
      .catch(error => {
        console.error('Preset load error:', error);
        btnEl.disabled = false;
        btnEl.innerHTML = '<i class="fas fa-download"></i> Load';
        showNotification('Network error loading preset', 'error');
      });
  }

  // ==========================================
  // Notification
  // ==========================================

  function showNotification(message, type) {
    AdminModal.toast(message, type || 'info');
  }

  // ==========================================
  // Close modal on Escape key or overlay click
  // ==========================================

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      hidePresetsModal();
    }
  });

  document.addEventListener('click', function (e) {
    if (e.target.classList.contains('tax-modal-overlay')) {
      hidePresetsModal();
    }
  });

  // Event delegation for all tax rate actions
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    const action = btn.dataset.action;

    if (action === 'show-presets-modal') {
      e.preventDefault();
      showPresetsModal();
    } else if (action === 'hide-presets-modal') {
      e.preventDefault();
      hidePresetsModal();
    } else if (action === 'load-preset') {
      e.preventDefault();
      loadPreset(btn.dataset.groupKey, btn);
    } else if (action === 'clear-filters') {
      e.preventDefault();
      clearFilters();
    } else if (action === 'clear-single-filter') {
      e.preventDefault();
      clearSingleFilter(btn.dataset.filterId);
    }
  });
})();
