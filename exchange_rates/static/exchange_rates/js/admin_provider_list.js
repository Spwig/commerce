/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Provider Account List Admin JavaScript
 * Handles filtering, bulk actions, and quick actions for provider account management
 */

(function () {
  'use strict';

  // ========================================================================
  // Helper Functions
  // ========================================================================
  // Note: CSRF token and i18n URL handling now use global AdminUtils module

  /**
   * Show notification message
   */
  function showNotification(message, type = 'success') {
    AdminModal.toast(message, type || 'info');
  }

  /**
   * Show/hide loading overlay
   */
  function setLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
      overlay.style.display = show ? 'flex' : 'none';
    }
  }

  /**
   * Get selected provider IDs
   */
  function getSelectedProviders() {
    const checkboxes = document.querySelectorAll('.provider-select:checked');
    return Array.from(checkboxes).map(cb => cb.value);
  }

  /**
   * Update selected count display
   */
  function updateSelectedCount() {
    const count = getSelectedProviders().length;
    const countDisplay = document.getElementById('selected-count');
    const numberDisplay = document.getElementById('selected-number');
    const applyButton = document.getElementById('apply-bulk-action');

    if (numberDisplay) numberDisplay.textContent = count;
    if (countDisplay) {
      if (count > 0) {
        countDisplay.classList.remove('exchange-rates-hidden');
      } else {
        countDisplay.classList.add('exchange-rates-hidden');
      }
    }
    if (applyButton) applyButton.disabled = count === 0;
  }

  // ========================================================================
  // Filter Handling
  // ========================================================================
  // NOTE: Filtering is now handled by AdminListFilters module (admin-list-filters.js)
  // Custom AJAX actions (toggle, sync, delete, bulk) remain below

  // ========================================================================
  // AJAX Actions
  // ========================================================================

  /**
   * Toggle provider active status
   */
  function toggleProviderActive(providerId, button) {
    const isActive = button.dataset.isActive === 'true';
    const card = button.closest('.provider-card');

    setLoading(true);

    fetch(
      AdminUtils.buildAdminUrl(
        `/admin/exchange-rates/admin/provideraccount/${providerId}/toggle-active/`
      ),
      {
        method: 'POST',
        headers: {
          'X-CSRFToken': AdminUtils.getCsrfToken(),
          'Content-Type': 'application/json',
        },
      }
    )
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showNotification(data.message, 'success');

          // Update UI
          button.dataset.isActive = data.is_active;
          button.classList.toggle('active', data.is_active);
          button.classList.toggle('inactive', !data.is_active);
          button.title = data.is_active ? 'Disable' : 'Enable';
          button.innerHTML = data.is_active
            ? '<i class="fas fa-toggle-on"></i>'
            : '<i class="fas fa-toggle-off"></i>';

          // Update badge
          const badge = card.querySelector('.badge-status');
          if (badge) {
            badge.className = `badge badge-status ${data.is_active ? 'badge-active' : 'badge-inactive'}`;
            badge.innerHTML = data.is_active
              ? '<i class="fas fa-check-circle"></i> Active'
              : '<i class="fas fa-times-circle"></i> Inactive';
          }
        } else {
          showNotification(data.message || 'Failed to toggle provider status', 'error');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
      })
      .finally(() => {
        setLoading(false);
      });
  }

  /**
   * Set provider as primary
   */
  function setProviderPrimary(providerId, button) {
    setLoading(true);

    fetch(
      AdminUtils.buildAdminUrl(
        `/admin/exchange-rates/admin/provideraccount/${providerId}/set-primary/`
      ),
      {
        method: 'POST',
        headers: {
          'X-CSRFToken': AdminUtils.getCsrfToken(),
          'Content-Type': 'application/json',
        },
      }
    )
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showNotification(data.message, 'success');
          // Reload page to update all primary badges
          setTimeout(() => window.location.reload(), 500);
        } else {
          showNotification(data.message || 'Failed to set primary provider', 'error');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
      })
      .finally(() => {
        setLoading(false);
      });
  }

  /**
   * Sync provider exchange rates
   */
  function syncProviderRates(providerId, button) {
    const originalHtml = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;
    const card = button.closest('.provider-card');

    fetch(
      AdminUtils.buildAdminUrl(
        `/admin/exchange-rates/admin/provideraccount/${providerId}/sync-rates/`
      ),
      {
        method: 'POST',
        headers: {
          'X-CSRFToken': AdminUtils.getCsrfToken(),
          'Content-Type': 'application/json',
        },
      }
    )
      .then(response => response.json())
      .then(data => {
        console.log('=== Exchange Rate Sync Complete ===');
        console.log('Response:', data);

        if (data.stats) {
          console.log('Statistics:');
          console.table({
            Provider: data.stats.provider,
            'Base Currency': data.stats.base_currency,
            'Rates Received': data.stats.rates_received,
            'Rates Saved': data.stats.rates_saved,
            'Success Rate': `${((data.stats.rates_saved / data.stats.rates_received) * 100).toFixed(1)}%`,
          });
        }
        console.log('===================================');

        if (data.success) {
          showNotification(data.message || 'Exchange rates synced successfully!', 'success');

          // Update UI without page reload
          if (card) {
            // Update sync status badge
            const syncBadge = card.querySelector('.status-badge');
            if (syncBadge) {
              syncBadge.className = 'status-badge status-success';
              syncBadge.innerHTML = '<i class="fas fa-check-circle"></i> Success';
            }

            // Update last sync time
            const syncTimeElement = card.querySelector('.sync-time');
            if (syncTimeElement) {
              syncTimeElement.innerHTML = 'Last synced: <strong>Just now</strong>';
            }
          }
        } else {
          showNotification(data.message || data.error || 'Sync failed', 'error');

          // Update sync status to error if available
          if (card) {
            const syncBadge = card.querySelector('.status-badge');
            if (syncBadge) {
              syncBadge.className = 'status-badge status-error';
              syncBadge.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
            }
          }
        }
      })
      .catch(error => {
        console.error('Sync error:', error);
        showNotification('An error occurred during sync.', 'error');

        // Update sync status to error
        if (card) {
          const syncBadge = card.querySelector('.status-badge');
          if (syncBadge) {
            syncBadge.className = 'status-badge status-error';
            syncBadge.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error';
          }
        }
      })
      .finally(() => {
        button.innerHTML = originalHtml;
        button.disabled = false;
      });
  }

  /**
   * Delete provider
   */
  async function deleteProvider(providerId, button) {
    if (
      !(await AdminModal.confirm({
        message: 'Are you sure you want to delete this provider? This action cannot be undone.',
        danger: true,
        confirmText: 'Delete',
      }))
    ) {
      return;
    }

    setLoading(true);

    fetch(
      AdminUtils.buildAdminUrl(`/admin/exchange-rates/admin/provideraccount/${providerId}/delete/`),
      {
        method: 'POST',
        headers: {
          'X-CSRFToken': AdminUtils.getCsrfToken(),
          'Content-Type': 'application/json',
        },
      }
    )
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showNotification(data.message, 'success');
          // Remove card from UI
          const card = button.closest('.provider-card');
          if (card) {
            card.style.opacity = '0';
            setTimeout(() => card.remove(), 300);
          }
        } else {
          showNotification(data.message || 'Failed to delete provider', 'error');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
      })
      .finally(() => {
        setLoading(false);
      });
  }

  /**
   * Handle bulk actions
   */
  async function applyBulkAction() {
    const action = document.getElementById('bulk-action-select').value;
    const providerIds = getSelectedProviders();

    if (!action || providerIds.length === 0) {
      showNotification('Please select an action and at least one provider', 'warning');
      return;
    }

    // Confirm for delete action
    if (action === 'delete') {
      if (
        !(await AdminModal.confirm({
          message: `Are you sure you want to delete ${providerIds.length} provider(s)? This action cannot be undone.`,
          danger: true,
          confirmText: 'Delete',
        }))
      ) {
        return;
      }
    }

    // Confirm for set_primary action
    if (action === 'set_primary' && providerIds.length !== 1) {
      showNotification('Please select exactly one provider to set as default', 'warning');
      return;
    }

    setLoading(true);

    fetch(AdminUtils.buildAdminUrl('/admin/exchange-rates/admin/provideraccount/bulk-action/'), {
      method: 'POST',
      headers: {
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: action,
        provider_ids: providerIds,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showNotification(data.message, 'success');
          // Reload page after a short delay
          setTimeout(() => window.location.reload(), 500);
        } else {
          showNotification(data.message || 'Bulk action failed', 'error');
          setLoading(false);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
        setLoading(false);
      });
  }

  // ========================================================================
  // Event Listeners
  // ========================================================================

  document.addEventListener('DOMContentLoaded', function () {
    // Select All functionality
    const selectAllCheckbox = document.getElementById('select-all-providers');
    if (selectAllCheckbox) {
      selectAllCheckbox.addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('.provider-select');
        checkboxes.forEach(cb => (cb.checked = this.checked));
        updateSelectedCount();
      });
    }

    // Individual checkbox selection
    document.addEventListener('change', function (e) {
      if (e.target.classList.contains('provider-select')) {
        updateSelectedCount();

        // Update select all checkbox
        const selectAll = document.getElementById('select-all-providers');
        const checkboxes = document.querySelectorAll('.provider-select');
        const checkedBoxes = document.querySelectorAll('.provider-select:checked');
        if (selectAll) {
          selectAll.checked = checkboxes.length === checkedBoxes.length;
        }
      }
    });

    // NOTE: Filter change handlers removed - now handled by AdminListFilters module

    // Bulk action apply button
    const applyButton = document.getElementById('apply-bulk-action');
    if (applyButton) {
      applyButton.addEventListener('click', applyBulkAction);
    }

    // Quick action buttons
    document.addEventListener('click', function (e) {
      const button = e.target.closest('button');
      if (!button) return;

      const providerId = button.dataset.providerId;
      if (!providerId) return;

      if (button.classList.contains('provider-toggle-btn')) {
        e.preventDefault();
        toggleProviderActive(providerId, button);
      } else if (button.classList.contains('primary-btn')) {
        e.preventDefault();
        setProviderPrimary(providerId, button);
      } else if (button.classList.contains('sync-btn')) {
        e.preventDefault();
        syncProviderRates(providerId, button);
      } else if (button.classList.contains('delete-btn')) {
        e.preventDefault();
        deleteProvider(providerId, button);
      }
    });
  });
})();
