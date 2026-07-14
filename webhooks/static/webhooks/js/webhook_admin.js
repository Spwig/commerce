/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Webhook Admin JavaScript
 * Handles filtering, testing, and other interactions
 */

(function () {
  'use strict';

  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', function () {
    initInfoCardToggle();
    initFilters();
    initTestButtons();
    initResetButtons();
    initAdminListFilters();
  });

  /**
   * Info Card Toggle
   */
  function initInfoCardToggle() {
    const infoCard = document.getElementById('webhookInfoCard');
    if (!infoCard) return;

    const toggle = infoCard.querySelector('.collapse-toggle');
    if (!toggle) return;

    // Check localStorage for collapsed state
    const isCollapsed = localStorage.getItem('webhookInfoCardCollapsed') === 'true';
    if (isCollapsed) {
      infoCard.classList.add('collapsed');
    }

    toggle.addEventListener('click', function () {
      infoCard.classList.toggle('collapsed');
      localStorage.setItem('webhookInfoCardCollapsed', infoCard.classList.contains('collapsed'));
    });
  }

  /**
   * Filter Functions
   */
  let searchTimeout;

  function initFilters() {
    const searchInput = document.getElementById('filter-search');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(applyFilters, 300);
      });
    }

    const statusSelect = document.getElementById('filter-status');
    if (statusSelect) {
      statusSelect.addEventListener('change', applyFilters);
    }

    const healthSelect = document.getElementById('filter-health');
    if (healthSelect) {
      healthSelect.addEventListener('change', applyFilters);
    }
  }

  function applyFilters() {
    const panel = document.getElementById('filters-panel');
    if (panel) {
      panel.classList.add('loading');
    }

    const params = new URLSearchParams();
    const search = document.getElementById('filter-search')?.value || '';
    const status = document.getElementById('filter-status')?.value || '';
    const health = document.getElementById('filter-health')?.value || '';

    if (search) params.append('search', search);
    if (status) params.append('status', status);
    if (health) params.append('health', health);

    const lang = document.documentElement.lang || 'en';
    const url = `/${lang}/admin/webhooks/endpoints/filter/?${params.toString()}`;

    fetch(url, {
      method: 'GET',
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(response => response.json())
      .then(data => {
        const resultsContainer = document.getElementById('endpoint-results');
        if (resultsContainer) {
          resultsContainer.innerHTML = data.html;
        }

        const countEl = document.getElementById('endpoint-count');
        if (countEl) {
          countEl.textContent = data.count;
        }

        updateActiveFilters();

        // Re-initialize test and reset buttons after AJAX load
        initTestButtons();
        initResetButtons();

        if (panel) {
          panel.classList.remove('loading');
        }
      })
      .catch(error => {
        console.error('Filter error:', error);
        if (panel) {
          panel.classList.remove('loading');
        }
        showNotification('error', 'Failed to apply filters. Please try again.');
      });
  }

  function clearFilters() {
    const searchInput = document.getElementById('filter-search');
    const statusSelect = document.getElementById('filter-status');
    const healthSelect = document.getElementById('filter-health');

    if (searchInput) searchInput.value = '';
    if (statusSelect) statusSelect.value = '';
    if (healthSelect) healthSelect.value = '';

    applyFilters();
  }

  function toggleFilters() {
    const fields = document.getElementById('filters-panel-fields');
    const footer = document.querySelector('.filters-panel-footer');
    const toggle = document.querySelector('.filters-toggle i');

    if (fields) {
      const isHidden = fields.style.display === 'none';
      fields.style.display = isHidden ? 'grid' : 'none';
      if (footer) footer.style.display = isHidden ? 'flex' : 'none';
      if (toggle) {
        toggle.classList.toggle('fa-chevron-down', isHidden);
        toggle.classList.toggle('fa-chevron-up', !isHidden);
      }
    }
  }

  function updateActiveFilters() {
    const container = document.getElementById('active-filters');
    if (!container) return;

    const search = document.getElementById('filter-search')?.value || '';
    const status = document.getElementById('filter-status')?.value || '';
    const health = document.getElementById('filter-health')?.value || '';

    let html = '<span class="active-filters-label">Active:</span>';
    let hasFilters = false;

    if (search) {
      hasFilters = true;
      html += `<span class="active-filter-tag">Search: ${escapeHtml(search)}
                <button type="button" class="active-filter-remove" data-action="clear-single-filter" data-field-id="filter-search"><i class="fas fa-times"></i></button>
            </span>`;
    }
    if (status) {
      hasFilters = true;
      const statusLabel =
        document.querySelector('#filter-status option:checked')?.textContent || status;
      html += `<span class="active-filter-tag">Status: ${escapeHtml(statusLabel)}
                <button type="button" class="active-filter-remove" data-action="clear-single-filter" data-field-id="filter-status"><i class="fas fa-times"></i></button>
            </span>`;
    }
    if (health) {
      hasFilters = true;
      const healthLabel =
        document.querySelector('#filter-health option:checked')?.textContent || health;
      html += `<span class="active-filter-tag">Health: ${escapeHtml(healthLabel)}
                <button type="button" class="active-filter-remove" data-action="clear-single-filter" data-field-id="filter-health"><i class="fas fa-times"></i></button>
            </span>`;
    }

    container.innerHTML = hasFilters ? html : '';
  }

  /**
   * Test Endpoint Functions
   */
  function initTestButtons() {
    document.querySelectorAll('.test-endpoint-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const endpointId = this.dataset.endpointId;
        testEndpoint(endpointId);
      });
    });
  }

  function testEndpoint(endpointId) {
    const modal = document.getElementById('test-webhook-modal');
    const resultContainer = document.getElementById('test-result');
    const loadingContainer = document.getElementById('test-loading');

    if (!modal) return;

    // Show modal with loading
    modal.style.display = 'flex';
    if (resultContainer) resultContainer.style.display = 'none';
    if (loadingContainer) loadingContainer.style.display = 'block';

    // Make API request
    fetch(`/api/webhooks/endpoints/${endpointId}/test/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    })
      .then(response => response.json())
      .then(data => {
        if (loadingContainer) loadingContainer.style.display = 'none';
        if (resultContainer) {
          resultContainer.style.display = 'flex';
          resultContainer.className = 'test-result ' + (data.success ? 'success' : 'failed');

          const statusEl = resultContainer.querySelector('.test-result-status');
          const codeEl = resultContainer.querySelector('.test-result-code');
          const timeEl = resultContainer.querySelector('.test-result-time');
          const errorEl = resultContainer.querySelector('.test-result-error');

          if (statusEl) {
            statusEl.textContent = data.success ? 'Test Successful!' : 'Test Failed';
          }
          if (codeEl) {
            codeEl.textContent = data.status_code ? `Response Code: ${data.status_code}` : '';
          }
          if (timeEl) {
            timeEl.textContent = data.response_time_ms
              ? `Response Time: ${data.response_time_ms}ms`
              : '';
          }
          if (errorEl) {
            errorEl.textContent = data.error || '';
            errorEl.style.display = data.error ? 'block' : 'none';
          }
        }
      })
      .catch(error => {
        console.error('Test error:', error);
        if (loadingContainer) loadingContainer.style.display = 'none';
        if (resultContainer) {
          resultContainer.style.display = 'flex';
          resultContainer.className = 'test-result failed';

          const statusEl = resultContainer.querySelector('.test-result-status');
          const errorEl = resultContainer.querySelector('.test-result-error');

          if (statusEl) statusEl.textContent = 'Test Failed';
          if (errorEl) {
            errorEl.textContent = 'Network error occurred';
            errorEl.style.display = 'block';
          }
        }
      });
  }

  function closeTestModal() {
    const modal = document.getElementById('test-webhook-modal');
    if (modal) {
      modal.style.display = 'none';
    }
  }

  // Close modal on background click
  document.addEventListener('click', function (e) {
    if (e.target.classList.contains('webhook-modal')) {
      closeTestModal();
    }
  });

  // Close modal on Escape key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      closeTestModal();
    }
  });

  /**
   * Event delegation for data-action buttons
   */
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;

    switch (btn.dataset.action) {
      case 'apply-filters':
        applyFilters();
        break;
      case 'clear-filters':
        clearFilters();
        break;
      case 'toggle-filters':
        toggleFilters();
        break;
      case 'close-test-modal':
        closeTestModal();
        break;
      case 'dismiss-notification':
        btn.closest('.notification')?.remove();
        break;
      case 'clear-single-filter': {
        const fieldEl = document.getElementById(btn.dataset.fieldId);
        if (fieldEl) fieldEl.value = '';
        applyFilters();
        break;
      }
    }
  });

  /**
   * Reset Endpoint Functions
   */
  function initResetButtons() {
    document.querySelectorAll('.reset-endpoint-btn').forEach(btn => {
      btn.addEventListener('click', function () {
        const endpointId = this.dataset.endpointId;
        resetEndpoint(endpointId);
      });
    });
  }

  async function resetEndpoint(endpointId) {
    if (
      !(await AdminModal.confirm({
        message:
          'Reset failure count for this endpoint? This will re-enable it if it was disabled.',
        danger: true,
        confirmText: 'Reset',
      }))
    ) {
      return;
    }

    fetch(`/api/webhooks/endpoints/${endpointId}/reset-failures/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showNotification('success', data.message || 'Endpoint reset successfully');
          // Refresh the list
          applyFilters();
        } else {
          showNotification('error', data.error || 'Failed to reset endpoint');
        }
      })
      .catch(error => {
        console.error('Reset error:', error);
        showNotification('error', 'Network error occurred');
      });
  }

  /**
   * Notification Functions
   */
  function showNotification(type, message) {
    AdminModal.toast(message, type || 'info');
  }

  /**
   * Initialize AdminListFilters integration
   */
  function initAdminListFilters() {
    const lang = document.documentElement.lang || 'en';
    if (window.AdminListFilters) {
      window.AdminListFilters.init({
        url: `/${lang}/admin/webhooks/webhookendpoint/filter/`,
        resultsContainer: 'endpoint-results',
        resultsCount: 'endpoint-count',
      });
    }
  }

  /**
   * Utility Functions
   */
  function getCsrfToken() {
    return AdminUtils.getCsrfToken();
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
})();
