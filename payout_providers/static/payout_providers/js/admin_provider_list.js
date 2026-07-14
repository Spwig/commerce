/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Payout Provider Account List Admin JavaScript
 * Handles bulk actions and quick actions for payout provider management.
 * Filtering is handled by admin-list-filters.js (AdminListFilters.init()).
 */

(function () {
  'use strict';

  // ========================================================================
  // i18n Loading
  // ========================================================================

  let i18n = {};

  function loadI18n() {
    const el = document.getElementById('payout-providers-i18n');
    if (el) {
      try {
        i18n = JSON.parse(el.textContent);
      } catch (e) {
        console.error('Failed to parse payout-providers-i18n:', e);
      }
    }
  }

  // ========================================================================
  // Helper Functions
  // ========================================================================

  /**
   * Show notification message
   */
  function showNotification(message, type) {
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
    return Array.from(checkboxes).map(function (cb) {
      return cb.value;
    });
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
        countDisplay.classList.remove('payout-hidden');
      } else {
        countDisplay.classList.add('payout-hidden');
      }
    }
    if (applyButton) applyButton.disabled = count === 0;
  }

  /**
   * Helper: set button content with icon + text (XSS-safe via DOM creation)
   */
  function setButtonContent(btn, iconClass, text) {
    btn.textContent = '';
    const icon = document.createElement('i');
    icon.className = iconClass;
    btn.appendChild(icon);
    btn.appendChild(document.createTextNode(' ' + text));
  }

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
        '/admin/payout_providers/payoutprovideraccount/' + providerId + '/toggle-active/'
      ),
      {
        method: 'POST',
        headers: {
          'X-CSRFToken': AdminUtils.getCsrfToken(),
          'Content-Type': 'application/json',
        },
      }
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showNotification(data.message, 'success');

          // Update UI
          button.dataset.isActive = data.is_active;
          button.classList.toggle('active', data.is_active);
          button.classList.toggle('inactive', !data.is_active);
          button.title = data.is_active ? i18n.disable || 'Disable' : i18n.enable || 'Enable';
          setButtonContent(button, data.is_active ? 'fas fa-toggle-on' : 'fas fa-toggle-off', '');
          // Quick action buttons only show icon, remove trailing text
          button.textContent = '';
          const icon = document.createElement('i');
          icon.className = data.is_active ? 'fas fa-toggle-on' : 'fas fa-toggle-off';
          button.appendChild(icon);

          // Update badge
          const badge = card.querySelector('.badge-active, .badge-inactive');
          if (badge) {
            badge.className = 'badge ' + (data.is_active ? 'badge-active' : 'badge-inactive');
            badge.textContent = '';
            const badgeIcon = document.createElement('i');
            badgeIcon.className = data.is_active ? 'fas fa-check-circle' : 'fas fa-times-circle';
            badge.appendChild(badgeIcon);
            badge.appendChild(
              document.createTextNode(
                ' ' + (data.is_active ? i18n.active || 'Active' : i18n.inactive || 'Inactive')
              )
            );
          }
        } else {
          showNotification(
            data.message || i18n.toggleFailed || 'Failed to toggle provider status',
            'error'
          );
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
        showNotification(i18n.genericError || 'An error occurred. Please try again.', 'error');
      })
      .finally(function () {
        setLoading(false);
      });
  }

  /**
   * Set provider as default
   */
  function setProviderDefault(providerId, button) {
    setLoading(true);

    fetch(
      AdminUtils.buildAdminUrl(
        '/admin/payout_providers/payoutprovideraccount/' + providerId + '/set-default/'
      ),
      {
        method: 'POST',
        headers: {
          'X-CSRFToken': AdminUtils.getCsrfToken(),
          'Content-Type': 'application/json',
        },
      }
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showNotification(data.message, 'success');
          // Reload page to update all default badges
          setTimeout(function () {
            window.location.reload();
          }, 500);
        } else {
          showNotification(
            data.message || i18n.defaultFailed || 'Failed to set default provider',
            'error'
          );
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
        showNotification(i18n.genericError || 'An error occurred. Please try again.', 'error');
      })
      .finally(function () {
        setLoading(false);
      });
  }

  /**
   * Test provider connection
   */
  function testProviderConnection(providerId, button) {
    const originalIcon = button.querySelector('i');
    const originalIconClass = originalIcon ? originalIcon.className : 'fas fa-plug';
    button.textContent = '';
    const spinIcon = document.createElement('i');
    spinIcon.className = 'fas fa-spinner fa-spin';
    button.appendChild(spinIcon);
    button.disabled = true;

    fetch(
      AdminUtils.buildAdminUrl(
        '/admin/payout_providers/payoutprovideraccount/' + providerId + '/test-connection/'
      ),
      {
        method: 'POST',
        headers: {
          'X-CSRFToken': AdminUtils.getCsrfToken(),
          'Content-Type': 'application/json',
        },
      }
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showNotification(
            data.message || i18n.testSuccess || 'Connection test successful!',
            'success'
          );
          // Reload page to update connection status
          setTimeout(function () {
            window.location.reload();
          }, 1000);
        } else {
          showNotification(
            data.message || data.error || i18n.testFailed || 'Connection test failed',
            'error'
          );
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
        showNotification(i18n.testError || 'An error occurred during connection test.', 'error');
      })
      .finally(function () {
        button.textContent = '';
        const restoreIcon = document.createElement('i');
        restoreIcon.className = originalIconClass;
        button.appendChild(restoreIcon);
        button.disabled = false;
      });
  }

  /**
   * Handle bulk actions
   */
  async function applyBulkAction() {
    const actionSelect = document.getElementById('bulk-action-select');
    const action = actionSelect ? actionSelect.value : '';
    const providerIds = getSelectedProviders();

    if (!action || providerIds.length === 0) {
      showNotification(
        i18n.selectActionWarning || 'Please select an action and at least one provider',
        'warning'
      );
      return;
    }

    // Confirm for delete action
    if (action === 'delete') {
      const deleteMsg = (
        i18n.confirmDelete ||
        'Are you sure you want to delete {count} provider(s)? This action cannot be undone.'
      ).replace('{count}', providerIds.length);
      if (
        !(await AdminModal.confirm({ message: deleteMsg, danger: true, confirmText: 'Delete' }))
      ) {
        return;
      }
    }

    // Confirm for set_default action
    if (action === 'set_default' && providerIds.length !== 1) {
      showNotification(
        i18n.selectOneDefault || 'Please select exactly one provider to set as default',
        'warning'
      );
      return;
    }

    setLoading(true);

    fetch(AdminUtils.buildAdminUrl('/admin/payout_providers/payoutprovideraccount/bulk-action/'), {
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
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showNotification(data.message, 'success');
          // Reload page after a short delay
          setTimeout(function () {
            window.location.reload();
          }, 500);
        } else {
          showNotification(data.message || i18n.bulkFailed || 'Bulk action failed', 'error');
          setLoading(false);
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
        showNotification(i18n.genericError || 'An error occurred. Please try again.', 'error');
        setLoading(false);
      });
  }

  // ========================================================================
  // Event Listeners
  // ========================================================================

  document.addEventListener('DOMContentLoaded', function () {
    loadI18n();

    // Select All functionality
    const selectAllCheckbox = document.getElementById('select-all-providers');
    if (selectAllCheckbox) {
      selectAllCheckbox.addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('.provider-select');
        const checked = this.checked;
        checkboxes.forEach(function (cb) {
          cb.checked = checked;
        });
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

      if (button.classList.contains('toggle-btn')) {
        e.preventDefault();
        toggleProviderActive(providerId, button);
      } else if (button.classList.contains('default-btn')) {
        e.preventDefault();
        setProviderDefault(providerId, button);
      } else if (button.classList.contains('test-btn')) {
        e.preventDefault();
        testProviderConnection(providerId, button);
      }
    });
  });
})();
