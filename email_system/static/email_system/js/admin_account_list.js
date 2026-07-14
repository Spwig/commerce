/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Email Account List Admin JavaScript
 * Handles filtering, bulk actions, and quick actions for email account management
 */

(function () {
  'use strict';

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
   * Get selected account IDs
   */
  function getSelectedAccounts() {
    const checkboxes = document.querySelectorAll('.account-select:checked');
    return Array.from(checkboxes).map(function (cb) {
      return cb.value;
    });
  }

  /**
   * Update selected count display
   */
  function updateSelectedCount() {
    const count = getSelectedAccounts().length;
    const countDisplay = document.getElementById('selected-count');
    const numberDisplay = document.getElementById('selected-number');
    const applyButton = document.getElementById('apply-bulk-action');

    if (numberDisplay) numberDisplay.textContent = count;
    if (countDisplay) countDisplay.style.display = count > 0 ? 'inline' : 'none';
    if (applyButton) applyButton.disabled = count === 0;
  }

  // ========================================================================
  // Filter Handling
  // ========================================================================

  /**
   * Apply filters and reload page
   */
  function applyFilters() {
    const connectionFilter = document.getElementById('connection-status-filter');
    const activeFilter = document.getElementById('active-filter');
    const componentFilter = document.getElementById('component-filter');
    const searchInput = document.getElementById('provider-search');

    const params = new URLSearchParams(window.location.search);

    // Connection status filter
    if (connectionFilter && connectionFilter.value) {
      params.set('connection_status', connectionFilter.value);
    } else {
      params.delete('connection_status');
    }

    // Active filter
    if (activeFilter && activeFilter.value) {
      if (activeFilter.value === 'active') {
        params.set('is_active', '1');
      } else if (activeFilter.value === 'inactive') {
        params.set('is_active', '0');
      }
    } else {
      params.delete('is_active');
    }

    // Component filter
    if (componentFilter && componentFilter.value) {
      params.set('component', componentFilter.value);
    } else {
      params.delete('component');
    }

    // Search
    if (searchInput && searchInput.value) {
      params.set('q', searchInput.value);
    } else {
      params.delete('q');
    }

    // Reload page with new filters
    window.location.search = params.toString();
  }

  /**
   * Debounce function for search
   */
  function debounce(func, wait) {
    let timeout;
    return function () {
      const args = arguments;
      const context = this;
      clearTimeout(timeout);
      timeout = setTimeout(function () {
        func.apply(context, args);
      }, wait);
    };
  }

  // ========================================================================
  // AJAX Actions
  // ========================================================================

  /**
   * Toggle account active status
   */
  function toggleAccountActive(accountId, button) {
    setLoading(true);

    fetch(
      AdminUtils.buildAdminUrl('/admin/email-system/accounts/' + accountId + '/toggle-active/'),
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
          // Reload to update all UI state
          setTimeout(function () {
            window.location.reload();
          }, 500);
        } else {
          showNotification(data.message || 'Failed to toggle account status', 'error');
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
      })
      .finally(function () {
        setLoading(false);
      });
  }

  /**
   * Test account connection
   */
  function testAccountConnection(accountId, button) {
    const originalHtml = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;

    fetch(
      AdminUtils.buildAdminUrl('/admin/email-system/accounts/' + accountId + '/test-connection/'),
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
          showNotification(data.message || 'Connection test passed', 'success');
        } else {
          showNotification(data.message || 'Connection test failed', 'error');
        }
        // Reload to update connection status badges
        setTimeout(function () {
          window.location.reload();
        }, 1000);
      })
      .catch(function (error) {
        console.error('Error:', error);
        showNotification('An error occurred during connection test.', 'error');
      })
      .finally(function () {
        button.innerHTML = originalHtml;
        button.disabled = false;
      });
  }

  /**
   * Delete account
   */
  async function deleteAccount(accountId, button) {
    if (
      !(await AdminModal.confirm({
        message:
          'Are you sure you want to delete this email account? This action cannot be undone.',
        danger: true,
        confirmText: 'Delete',
      }))
    ) {
      return;
    }

    setLoading(true);

    fetch(AdminUtils.buildAdminUrl('/admin/email-system/accounts/' + accountId + '/delete/'), {
      method: 'POST',
      headers: {
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showNotification(data.message, 'success');
          // Remove card from UI
          const card = button.closest('.provider-card');
          if (card) {
            card.style.opacity = '0';
            setTimeout(function () {
              card.remove();
            }, 300);
          }
        } else {
          showNotification(data.message || 'Failed to delete account', 'error');
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
      })
      .finally(function () {
        setLoading(false);
      });
  }

  /**
   * Handle bulk actions
   */
  async function applyBulkAction() {
    const actionSelect = document.getElementById('bulk-action-select');
    const action = actionSelect ? actionSelect.value : '';
    const accountIds = getSelectedAccounts();

    if (!action || accountIds.length === 0) {
      showNotification('Please select an action and at least one account', 'warning');
      return;
    }

    // Confirm for delete action
    if (action === 'delete') {
      if (
        !(await AdminModal.confirm({
          message:
            'Are you sure you want to delete ' +
            accountIds.length +
            ' account(s)? This action cannot be undone.',
          danger: true,
          confirmText: 'Delete',
        }))
      ) {
        return;
      }
    }

    setLoading(true);

    fetch(AdminUtils.buildAdminUrl('/admin/email-system/accounts/bulk-action/'), {
      method: 'POST',
      headers: {
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: action,
        account_ids: accountIds,
      }),
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showNotification(data.message, 'success');
          setTimeout(function () {
            window.location.reload();
          }, 500);
        } else {
          showNotification(data.message || 'Bulk action failed', 'error');
          setLoading(false);
        }
      })
      .catch(function (error) {
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
    const selectAllCheckbox = document.getElementById('select-all-accounts');
    if (selectAllCheckbox) {
      selectAllCheckbox.addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('.account-select');
        const checked = this.checked;
        checkboxes.forEach(function (cb) {
          cb.checked = checked;
        });
        updateSelectedCount();
      });
    }

    // Individual checkbox selection
    document.addEventListener('change', function (e) {
      if (e.target.classList.contains('account-select')) {
        updateSelectedCount();

        // Update select all checkbox
        const selectAll = document.getElementById('select-all-accounts');
        const checkboxes = document.querySelectorAll('.account-select');
        const checkedBoxes = document.querySelectorAll('.account-select:checked');
        if (selectAll) {
          selectAll.checked = checkboxes.length === checkedBoxes.length;
        }
      }
    });

    // Filter change handlers
    const connectionFilter = document.getElementById('connection-status-filter');
    const activeFilter = document.getElementById('active-filter');
    const componentFilter = document.getElementById('component-filter');

    if (connectionFilter) connectionFilter.addEventListener('change', applyFilters);
    if (activeFilter) activeFilter.addEventListener('change', applyFilters);
    if (componentFilter) componentFilter.addEventListener('change', applyFilters);

    // Search with debounce
    const searchInput = document.getElementById('provider-search');
    if (searchInput) {
      searchInput.addEventListener('input', debounce(applyFilters, 500));
    }

    // Bulk action apply button
    const applyButton = document.getElementById('apply-bulk-action');
    if (applyButton) {
      applyButton.addEventListener('click', applyBulkAction);
    }

    // Quick action buttons (event delegation)
    document.addEventListener('click', function (e) {
      const button = e.target.closest('button');
      if (!button) return;

      const accountId = button.dataset.accountId;
      if (!accountId) return;

      if (button.classList.contains('account-toggle-btn')) {
        e.preventDefault();
        toggleAccountActive(accountId, button);
      } else if (button.classList.contains('test-btn')) {
        e.preventDefault();
        testAccountConnection(accountId, button);
      } else if (button.classList.contains('delete-btn')) {
        e.preventDefault();
        deleteAccount(accountId, button);
      }
    });
  });
})();
