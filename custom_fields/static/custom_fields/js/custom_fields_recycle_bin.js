/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Custom Fields Recycle Bin - Admin JavaScript
 *
 * Handles restore and permanent delete actions for deleted custom field
 * groups and definitions.
 */
(function () {
  'use strict';

  const BASE_URL = AdminUtils.buildAdminUrl('/admin/custom-fields');

  const i18nEl = document.getElementById('cf-i18n');
  const i18n = i18nEl ? i18nEl.dataset : {};

  function showMessage(message, type) {
    let messagesDiv = document.querySelector('.messagelist');
    if (!messagesDiv) {
      messagesDiv = document.createElement('ul');
      messagesDiv.className = 'messagelist';
      const content = document.getElementById('content-main');
      if (content && content.parentNode) {
        content.parentNode.insertBefore(messagesDiv, content);
      }
    }
    const li = document.createElement('li');
    li.className = type || 'info';
    li.textContent = message;
    messagesDiv.appendChild(li);
    setTimeout(function () {
      li.remove();
    }, 5000);
  }

  function apiRequest(url, method, data) {
    const options = AdminUtils.buildFetchOptions(method, data, {
      'X-Requested-With': 'XMLHttpRequest',
    });
    return fetch(url, options).then(function (r) {
      return r.json();
    });
  }

  // Restore Group
  document.querySelectorAll('.cf-btn-restore-group').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const groupId = this.dataset.groupId;
      apiRequest(BASE_URL + '/groups/' + groupId + '/restore/', 'POST').then(function (resp) {
        if (resp.success) {
          showMessage(i18n.successRestored || 'Item restored.', 'success');
          location.reload();
        } else {
          showMessage(resp.error || i18n.errorGeneric, 'error');
        }
      });
    });
  });

  // Permanent Delete Group
  document.querySelectorAll('.cf-btn-permanent-delete-group').forEach(function (btn) {
    btn.addEventListener('click', async function () {
      const confirmMsg =
        i18n.confirmPermanentDelete || 'Permanently delete? This cannot be undone.';
      if (
        !(await AdminModal.confirm({
          message: confirmMsg,
          danger: true,
          confirmText: 'Delete',
        }))
      )
        return;

      const groupId = this.dataset.groupId;
      apiRequest(BASE_URL + '/groups/' + groupId + '/permanent-delete/', 'POST').then(
        function (resp) {
          if (resp.success) {
            showMessage(i18n.successDeleted || 'Item permanently deleted.', 'success');
            location.reload();
          } else {
            showMessage(resp.error || i18n.errorGeneric, 'error');
          }
        }
      );
    });
  });

  // Restore Field
  document.querySelectorAll('.cf-btn-restore-field').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const fieldId = this.dataset.fieldId;
      apiRequest(BASE_URL + '/fields/' + fieldId + '/restore/', 'POST').then(function (resp) {
        if (resp.success) {
          showMessage(i18n.successRestored || 'Item restored.', 'success');
          location.reload();
        } else {
          showMessage(resp.error || i18n.errorGeneric, 'error');
        }
      });
    });
  });

  // Permanent Delete Field
  document.querySelectorAll('.cf-btn-permanent-delete-field').forEach(function (btn) {
    btn.addEventListener('click', async function () {
      const confirmMsg =
        i18n.confirmPermanentDelete || 'Permanently delete? This cannot be undone.';
      if (
        !(await AdminModal.confirm({
          message: confirmMsg,
          danger: true,
          confirmText: 'Delete',
        }))
      )
        return;

      const fieldId = this.dataset.fieldId;
      apiRequest(BASE_URL + '/fields/' + fieldId + '/permanent-delete/', 'POST').then(
        function (resp) {
          if (resp.success) {
            showMessage(i18n.successDeleted || 'Item permanently deleted.', 'success');
            location.reload();
          } else {
            showMessage(resp.error || i18n.errorGeneric, 'error');
          }
        }
      );
    });
  });
})();
