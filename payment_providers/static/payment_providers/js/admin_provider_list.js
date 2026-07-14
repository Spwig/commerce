/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Payment Provider Admin - List View JavaScript
 * Uses AdminUtils for CSRF tokens and language-aware URLs.
 */

(function () {
  'use strict';

  // Load i18n strings from template config
  let i18n = {};
  const configEl = document.getElementById('pp-list-config');
  if (configEl) {
    try {
      const config = JSON.parse(configEl.textContent);
      i18n = config.i18n || {};
    } catch (e) {
      // fall back to empty strings
    }
  }

  // Wait for DOM to be ready
  document.addEventListener('DOMContentLoaded', function () {
    initializeFilters();
    initializeSearch();
    initializeActionButtons();
  });

  /**
   * Initialize filter dropdowns
   */
  function initializeFilters() {
    const statusFilter = document.getElementById('status-filter');
    const activeFilter = document.getElementById('active-filter');
    const checkoutModeFilter = document.getElementById('checkout-mode-filter');
    const providerTypeFilter = document.getElementById('provider-type-filter');

    if (statusFilter) {
      statusFilter.addEventListener('change', function () {
        updateURL('connection_status', this.value);
      });
    }

    if (activeFilter) {
      activeFilter.addEventListener('change', function () {
        updateURL('is_active', this.value);
      });
    }

    if (checkoutModeFilter) {
      checkoutModeFilter.addEventListener('change', function () {
        updateURL('checkout_mode', this.value);
      });
    }

    if (providerTypeFilter) {
      providerTypeFilter.addEventListener('change', function () {
        updateURL('component', this.value);
      });
    }
  }

  /**
   * Initialize search functionality
   */
  function initializeSearch() {
    const searchInput = document.getElementById('provider-search');

    if (searchInput) {
      let searchTimeout;

      searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        const input = searchInput;
        searchTimeout = setTimeout(function () {
          updateURL('q', input.value);
        }, 500);
      });
    }
  }

  /**
   * Initialize action buttons
   */
  function initializeActionButtons() {
    document.querySelectorAll('.test-btn, .action-test').forEach(function (button) {
      button.addEventListener('click', function (e) {
        e.preventDefault();
        const accountId = this.dataset.accountId;
        testConnection(accountId, this);
      });
    });

    document.querySelectorAll('.default-btn, .action-set-default').forEach(function (button) {
      button.addEventListener('click', function (e) {
        e.preventDefault();
        const accountId = this.dataset.accountId;
        setDefaultProvider(accountId, this);
      });
    });

    document.querySelectorAll('.provider-toggle-btn').forEach(function (button) {
      button.addEventListener('click', function (e) {
        e.preventDefault();
        const accountId = this.dataset.accountId;
        toggleActive(accountId, this);
      });
    });

    document.querySelectorAll('.delete-btn, .action-delete').forEach(function (button) {
      button.addEventListener('click', function (e) {
        e.preventDefault();
        const accountId = this.dataset.accountId;
        deleteProvider(accountId, this);
      });
    });
  }

  /**
   * Update URL with new query parameter
   */
  function updateURL(param, value) {
    const url = new URL(window.location);

    if (value) {
      url.searchParams.set(param, value);
    } else {
      url.searchParams.delete(param);
    }

    window.location = url.toString();
  }

  /**
   * Build admin AJAX URL with language prefix
   */
  function buildAdminURL(accountId, action) {
    const langPrefix = window.AdminUtils ? AdminUtils.getLanguagePrefix() : '';
    return (
      langPrefix +
      '/admin/payment_providers/paymentprovideraccount/' +
      accountId +
      '/' +
      action +
      '/'
    );
  }

  /**
   * Get CSRF token (AdminUtils preferred, cookie fallback)
   */
  function getCsrf() {
    if (window.AdminUtils) {
      return AdminUtils.getCsrfToken();
    }
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return null;
  }

  /**
   * Test provider connection
   */
  function testConnection(accountId, button) {
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;

    fetch(buildAdminURL(accountId, 'test'), {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrf(),
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showMessage('success', data.message);
          setTimeout(function () {
            window.location.reload();
          }, 1000);
        } else {
          showMessage('error', data.message);
          button.innerHTML = originalHTML;
          button.disabled = false;
        }
      })
      .catch(function (error) {
        showMessage(
          'error',
          (i18n.connectionTestFailed || 'Connection test failed') + ': ' + error
        );
        button.innerHTML = originalHTML;
        button.disabled = false;
      });
  }

  /**
   * Toggle provider active status
   */
  function toggleActive(accountId, button) {
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;

    fetch(buildAdminURL(accountId, 'toggle-active'), {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrf(),
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showMessage('success', data.message);
          button.dataset.isActive = data.is_active ? 'true' : 'false';
          if (data.is_active) {
            button.className = 'action-btn provider-toggle-btn active';
            button.innerHTML = '<i class="fas fa-toggle-on"></i>';
            button.title = i18n.disable || 'Disable';
          } else {
            button.className = 'action-btn provider-toggle-btn inactive';
            button.innerHTML = '<i class="fas fa-toggle-off"></i>';
            button.title = i18n.enable || 'Enable';
          }
          const card = button.closest('.provider-card');
          if (card) {
            const badge = card.querySelector('.badge-active, .badge-inactive');
            if (badge) {
              badge.className = data.is_active
                ? 'badge badge-status badge-active'
                : 'badge badge-status badge-inactive';
              badge.innerHTML = data.is_active
                ? '<i class="fas fa-check-circle"></i> ' + (i18n.active || 'Active')
                : '<i class="fas fa-times-circle"></i> ' + (i18n.inactive || 'Inactive');
            }
          }
          button.disabled = false;
        } else {
          showMessage('error', data.message);
          button.innerHTML = originalHTML;
          button.disabled = false;
        }
      })
      .catch(function (error) {
        showMessage('error', (i18n.failedToggle || 'Failed to toggle provider') + ': ' + error);
        button.innerHTML = originalHTML;
        button.disabled = false;
      });
  }

  /**
   * Set provider as default
   */
  async function setDefaultProvider(accountId, button) {
    if (
      !(await AdminModal.confirm(
        i18n.confirmSetDefault || 'Set this provider as the default payment provider?'
      ))
    ) {
      return;
    }

    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;

    fetch(buildAdminURL(accountId, 'set-default'), {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrf(),
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showMessage('success', data.message);
          setTimeout(function () {
            window.location.reload();
          }, 1000);
        } else {
          showMessage('error', data.message);
          button.innerHTML = originalHTML;
          button.disabled = false;
        }
      })
      .catch(function (error) {
        showMessage('error', (i18n.failedSetDefault || 'Failed to set default') + ': ' + error);
        button.innerHTML = originalHTML;
        button.disabled = false;
      });
  }

  /**
   * Delete provider
   */
  async function deleteProvider(accountId, button) {
    if (
      !(await AdminModal.confirm({
        message:
          i18n.confirmDelete ||
          'Are you sure you want to delete this payment provider? This action cannot be undone.',
        danger: true,
        confirmText: 'Delete',
      }))
    ) {
      return;
    }

    const card = button.closest('.provider-card');
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;

    fetch(buildAdminURL(accountId, 'delete'), {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrf(),
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showMessage('success', i18n.providerDeletedSuccess || 'Provider deleted successfully');
          if (card) {
            card.style.opacity = '0';
            setTimeout(function () {
              card.remove();
            }, 500);
          }
        } else {
          showMessage('error', data.message);
          button.innerHTML = originalHTML;
          button.disabled = false;
        }
      })
      .catch(function (error) {
        showMessage('error', (i18n.failedDelete || 'Failed to delete') + ': ' + error);
        button.innerHTML = originalHTML;
        button.disabled = false;
      });
  }

  /**
   * Show message to user (XSS-safe: uses textContent)
   */
  function showMessage(type, message) {
    const messageContainer = document.createElement('div');
    messageContainer.className = 'messagelist';

    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    messageContainer.appendChild(messageDiv);

    const container = document.getElementById('content-main');
    if (container) {
      container.insertBefore(messageContainer, container.firstChild);
      setTimeout(function () {
        messageContainer.remove();
      }, 5000);
    }
  }
})();
