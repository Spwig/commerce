/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Affiliate Admin JavaScript
 * Handles status toggles and list filter initialization for affiliate admin pages.
 * Uses event delegation -- no inline onclick handlers required.
 */
(function () {
  'use strict';

  function getCsrfToken() {
    return AdminUtils.getCsrfToken();
  }

  function postStatusChange(url) {
    fetch(url, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': getCsrfToken(),
      },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.success) {
          if (window.AdminListFilters) {
            window.AdminListFilters.apply();
          } else {
            window.location.reload();
          }
        } else {
          AdminModal.alert({ message: data.error || 'An error occurred.', type: 'error' });
        }
      })
      .catch(function () {
        AdminModal.alert({ message: 'An error occurred. Please try again.', type: 'error' });
      });
  }

  // Show Django default table view (commission list)
  function showAdminTable() {
    const main = document.getElementById('content-main');
    const table = document.getElementById('admin-table-view');
    if (main) main.style.display = 'none';
    if (table) table.style.display = 'block';
  }

  // Event delegation for all affiliate admin actions
  document.addEventListener('click', async function (e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;
    const lang = document.documentElement.lang || 'en';

    if (action === 'toggle-affiliate-status') {
      var confirmMsg = btn.dataset.confirm || 'Are you sure?';
      if (!(await AdminModal.confirm(confirmMsg))) return;
      var pk = btn.dataset.pk;
      var status = btn.dataset.status;
      postStatusChange('/' + lang + '/admin/affiliate/affiliates/' + pk + '/' + status + '/');
    } else if (action === 'toggle-program-status') {
      var confirmMsg = btn.dataset.confirm || 'Are you sure?';
      if (!(await AdminModal.confirm(confirmMsg))) return;
      var pk = btn.dataset.pk;
      const activate = btn.dataset.activate === 'true';
      const statusAction = activate ? 'activate' : 'pause';
      postStatusChange('/' + lang + '/admin/affiliate/programs/' + pk + '/' + statusAction + '/');
    } else if (action === 'toggle-membership-status') {
      var confirmMsg = btn.dataset.confirm || 'Are you sure?';
      if (!(await AdminModal.confirm(confirmMsg))) return;
      var pk = btn.dataset.pk;
      var status = btn.dataset.status;
      postStatusChange('/' + lang + '/admin/affiliate/memberships/' + pk + '/' + status + '/');
    } else if (action === 'show-admin-table') {
      e.preventDefault();
      showAdminTable();
    }

    // Generic status change: data-url required, data-confirm optional
    else if (action === 'status-change') {
      var confirmMsg = btn.dataset.confirm || 'Are you sure?';
      if (!(await AdminModal.confirm(confirmMsg))) return;
      postStatusChange(btn.dataset.url);
    }

    // Confirm and navigate: data-url required, data-confirm optional
    else if (action === 'confirm-navigate') {
      e.preventDefault();
      var confirmMsg = btn.dataset.confirm || 'Are you sure?';
      if (!(await AdminModal.confirm(confirmMsg))) return;
      window.location.href = btn.dataset.url;
    }
  });

  // Initialize AdminListFilters from config element
  document.addEventListener('DOMContentLoaded', function () {
    const config = document.getElementById('affiliate-list-config');
    if (config && window.AdminListFilters) {
      const lang = document.documentElement.lang || 'en';
      const filterPath = config.dataset.filterPath;
      window.AdminListFilters.init({
        url: '/' + lang + filterPath,
        resultsContainer: config.dataset.resultsContainer,
        resultsCount: config.dataset.resultsCount,
      });
    }
  });
})();
