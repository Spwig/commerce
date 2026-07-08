/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var urls = {};
    var csrfToken = '';
    var translations = {};
    var headerToDelete = null;

    function init() {
        var dataEl = document.getElementById('headertemplate-management-data');
        if (dataEl) {
            try {
                var data = JSON.parse(dataEl.textContent);
                urls = data.urls || {};
                csrfToken = data.csrfToken || '';
                translations = data.translations || {};
            } catch (e) {}
        }

        document.addEventListener('click', handleActions);

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { hideDeleteModal(); }
        });
    }

    function handleActions(e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) { return; }
        var action = btn.dataset.action;

        if (action === 'set-default') {
            setAsDefault(btn.dataset.headerId, btn.dataset.headerName);
        } else if (action === 'duplicate-header') {
            duplicateHeader(btn.dataset.headerId, btn.dataset.headerName);
        } else if (action === 'show-delete-modal') {
            var isDefault = btn.dataset.isDefault === 'true';
            var pageCount = parseInt(btn.dataset.pageCount, 10) || 0;
            showDeleteModal(btn.dataset.headerId, btn.dataset.headerName, isDefault, pageCount);
        } else if (action === 'hide-delete-modal') {
            hideDeleteModal();
        } else if (action === 'confirm-delete') {
            confirmDelete();
        }
    }

    async function duplicateHeader(headerId, headerName) {
        var msg = (translations.createCopyOf || 'Create a copy of') + ' "' + headerName + '"?';
        if (!await AdminModal.confirm(msg)) { return; }

        var url = (urls.duplicateHeader || '').replace('0', headerId);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(function (response) {
            if (!response.ok) {
                return response.json().then(function (data) { throw data; });
            }
            return response.json();
        })
        .then(function () {
            window.location.reload();
        })
        .catch(function (error) {
            AdminModal.alert({message: (translations.errorDuplicating || 'Error duplicating header:') + ' ' +
                  (error.error || error.message || error), type: 'error'});
        });
    }

    async function setAsDefault(headerId, headerName) {
        var msg = (translations.setWith || 'Set') + ' "' + headerName + '" ' +
                  (translations.setAsDefaultConfirm || 'as the default header for your site?');
        if (!await AdminModal.confirm(msg)) { return; }

        var url = (urls.setDefaultHeader || '').replace('0', headerId);
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            }
        })
        .then(function (response) {
            if (!response.ok) {
                return response.json().then(function (data) { throw data; });
            }
            return response.json();
        })
        .then(function () {
            window.location.reload();
        })
        .catch(function (error) {
            AdminModal.alert({message: (translations.errorSettingDefault || 'Error setting default:') + ' ' +
                  (error.error || error.message || error), type: 'error'});
        });
    }

    function showDeleteModal(headerId, headerName, isDefault, pageCount) {
        headerToDelete = headerId;
        var modal = document.getElementById('deleteModal');
        var message = document.getElementById('deleteModalMessage');
        var warning = document.getElementById('deleteModalWarning');
        var confirmBtn = document.getElementById('confirmDeleteBtn');

        if (!modal) { return; }

        message.textContent = (translations.areYouSureDelete || 'Are you sure you want to delete the header') +
                               ' "' + headerName + '"?';

        warning.style.display = 'none';
        warning.textContent = '';
        confirmBtn.disabled = false;

        if (isDefault) {
            setWarning(warning,
                'fas fa-star',
                translations.cannotDeleteDefault || 'Cannot delete default header',
                translations.defaultHeaderWarning || 'This is the default header for your site. Please set another header as default before deleting this one.');
            warning.style.display = 'block';
            confirmBtn.disabled = true;
        } else if (pageCount > 0) {
            setWarning(warning,
                'fas fa-file-alt',
                translations.headerInUse || 'Header in use',
                (translations.headerUsedBy || 'This header is used by') + ' ' + pageCount + ' ' +
                (translations.pagesPleaseAssign || 'page(s). Please assign a different header to these pages before deleting.'));
            warning.style.display = 'block';
            confirmBtn.disabled = true;
        }

        modal.style.display = 'flex';
    }

    function setWarning(container, iconClass, title, body) {
        container.textContent = '';

        var icon = document.createElement('i');
        icon.className = iconClass;

        var strong = document.createElement('strong');
        strong.textContent = title;

        var br = document.createElement('br');

        container.appendChild(icon);
        container.appendChild(document.createTextNode(' '));
        container.appendChild(strong);
        container.appendChild(br);
        container.appendChild(document.createTextNode(body));
    }

    function hideDeleteModal() {
        var modal = document.getElementById('deleteModal');
        if (modal) { modal.style.display = 'none'; }
        headerToDelete = null;
    }

    function confirmDelete() {
        if (!headerToDelete) { return; }

        var confirmBtn = document.getElementById('confirmDeleteBtn');
        confirmBtn.disabled = true;

        var spinner = document.createElement('i');
        spinner.className = 'fas fa-spinner fa-spin';
        confirmBtn.textContent = ' ' + (translations.deleting || 'Deleting...');
        confirmBtn.insertBefore(spinner, confirmBtn.firstChild);

        var url = (urls.deleteHeader || '').replace('0', headerToDelete);
        fetch(url, {
            method: 'DELETE',
            headers: { 'X-CSRFToken': csrfToken }
        })
        .then(function (response) {
            if (!response.ok) {
                return response.json().then(function (data) { throw data; });
            }
            return response.json();
        })
        .then(function () {
            window.location.reload();
        })
        .catch(function (error) {
            var warning = document.getElementById('deleteModalWarning');
            if (warning) {
                var icon = document.createElement('i');
                icon.className = 'fas fa-exclamation-circle';
                warning.textContent = ' ' + (error.message || error.error || (translations.deleteFailed || 'Delete failed'));
                warning.insertBefore(icon, warning.firstChild);
                warning.style.display = 'block';
            }
            confirmBtn.disabled = true;
            var trashIcon = document.createElement('i');
            trashIcon.className = 'fas fa-trash';
            confirmBtn.textContent = ' ' + (translations.deleteHeader || 'Delete Header');
            confirmBtn.insertBefore(trashIcon, confirmBtn.firstChild);
        });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
