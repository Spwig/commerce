/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let urls = {};
  let csrfToken = '';
  let translations = {};
  let headerToDelete = null;

  function init() {
    const dataEl = document.getElementById('headertemplate-management-data');
    if (dataEl) {
      try {
        const data = JSON.parse(dataEl.textContent);
        urls = data.urls || {};
        csrfToken = data.csrfToken || '';
        translations = data.translations || {};
      } catch (e) {}
    }

    document.addEventListener('click', handleActions);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        hideDeleteModal();
      }
    });
  }

  function handleActions(e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) {
      return;
    }
    const action = btn.dataset.action;

    if (action === 'set-default') {
      setAsDefault(btn.dataset.headerId, btn.dataset.headerName);
    } else if (action === 'duplicate-header') {
      duplicateHeader(btn.dataset.headerId, btn.dataset.headerName);
    } else if (action === 'show-delete-modal') {
      const isDefault = btn.dataset.isDefault === 'true';
      const pageCount = parseInt(btn.dataset.pageCount, 10) || 0;
      showDeleteModal(btn.dataset.headerId, btn.dataset.headerName, isDefault, pageCount);
    } else if (action === 'hide-delete-modal') {
      hideDeleteModal();
    } else if (action === 'confirm-delete') {
      confirmDelete();
    }
  }

  async function duplicateHeader(headerId, headerName) {
    const msg = (translations.createCopyOf || 'Create a copy of') + ' "' + headerName + '"?';
    if (!(await AdminModal.confirm(msg))) {
      return;
    }

    const url = (urls.duplicateHeader || '').replace('0', headerId);
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
    })
      .then(function (response) {
        if (!response.ok) {
          return response.json().then(function (data) {
            throw data;
          });
        }
        return response.json();
      })
      .then(function () {
        window.location.reload();
      })
      .catch(function (error) {
        AdminModal.alert({
          message:
            (translations.errorDuplicating || 'Error duplicating header:') +
            ' ' +
            (error.error || error.message || error),
          type: 'error',
        });
      });
  }

  async function setAsDefault(headerId, headerName) {
    const msg =
      (translations.setWith || 'Set') +
      ' "' +
      headerName +
      '" ' +
      (translations.setAsDefaultConfirm || 'as the default header for your site?');
    if (!(await AdminModal.confirm(msg))) {
      return;
    }

    const url = (urls.setDefaultHeader || '').replace('0', headerId);
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
    })
      .then(function (response) {
        if (!response.ok) {
          return response.json().then(function (data) {
            throw data;
          });
        }
        return response.json();
      })
      .then(function () {
        window.location.reload();
      })
      .catch(function (error) {
        AdminModal.alert({
          message:
            (translations.errorSettingDefault || 'Error setting default:') +
            ' ' +
            (error.error || error.message || error),
          type: 'error',
        });
      });
  }

  function showDeleteModal(headerId, headerName, isDefault, pageCount) {
    headerToDelete = headerId;
    const modal = document.getElementById('deleteModal');
    const message = document.getElementById('deleteModalMessage');
    const warning = document.getElementById('deleteModalWarning');
    const confirmBtn = document.getElementById('confirmDeleteBtn');

    if (!modal) {
      return;
    }

    message.textContent =
      (translations.areYouSureDelete || 'Are you sure you want to delete the header') +
      ' "' +
      headerName +
      '"?';

    warning.style.display = 'none';
    warning.textContent = '';
    confirmBtn.disabled = false;

    if (isDefault) {
      setWarning(
        warning,
        'fas fa-star',
        translations.cannotDeleteDefault || 'Cannot delete default header',
        translations.defaultHeaderWarning ||
          'This is the default header for your site. Please set another header as default before deleting this one.'
      );
      warning.style.display = 'block';
      confirmBtn.disabled = true;
    } else if (pageCount > 0) {
      setWarning(
        warning,
        'fas fa-file-alt',
        translations.headerInUse || 'Header in use',
        (translations.headerUsedBy || 'This header is used by') +
          ' ' +
          pageCount +
          ' ' +
          (translations.pagesPleaseAssign ||
            'page(s). Please assign a different header to these pages before deleting.')
      );
      warning.style.display = 'block';
      confirmBtn.disabled = true;
    }

    modal.style.display = 'flex';
  }

  function setWarning(container, iconClass, title, body) {
    container.textContent = '';

    const icon = document.createElement('i');
    icon.className = iconClass;

    const strong = document.createElement('strong');
    strong.textContent = title;

    const br = document.createElement('br');

    container.appendChild(icon);
    container.appendChild(document.createTextNode(' '));
    container.appendChild(strong);
    container.appendChild(br);
    container.appendChild(document.createTextNode(body));
  }

  function hideDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
      modal.style.display = 'none';
    }
    headerToDelete = null;
  }

  function confirmDelete() {
    if (!headerToDelete) {
      return;
    }

    const confirmBtn = document.getElementById('confirmDeleteBtn');
    confirmBtn.disabled = true;

    const spinner = document.createElement('i');
    spinner.className = 'fas fa-spinner fa-spin';
    confirmBtn.textContent = ' ' + (translations.deleting || 'Deleting...');
    confirmBtn.insertBefore(spinner, confirmBtn.firstChild);

    const url = (urls.deleteHeader || '').replace('0', headerToDelete);
    fetch(url, {
      method: 'DELETE',
      headers: { 'X-CSRFToken': csrfToken },
    })
      .then(function (response) {
        if (!response.ok) {
          return response.json().then(function (data) {
            throw data;
          });
        }
        return response.json();
      })
      .then(function () {
        window.location.reload();
      })
      .catch(function (error) {
        const warning = document.getElementById('deleteModalWarning');
        if (warning) {
          const icon = document.createElement('i');
          icon.className = 'fas fa-exclamation-circle';
          warning.textContent =
            ' ' + (error.message || error.error || translations.deleteFailed || 'Delete failed');
          warning.insertBefore(icon, warning.firstChild);
          warning.style.display = 'block';
        }
        confirmBtn.disabled = true;
        const trashIcon = document.createElement('i');
        trashIcon.className = 'fas fa-trash';
        confirmBtn.textContent = ' ' + (translations.deleteHeader || 'Delete Header');
        confirmBtn.insertBefore(trashIcon, confirmBtn.firstChild);
      });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
