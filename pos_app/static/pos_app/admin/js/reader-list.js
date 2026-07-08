/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var T = {};
    var lang = document.documentElement.lang || 'en';

    function showMessage(text, type) {
        var messageList = document.querySelector('.messagelist');
        if (!messageList) {
            messageList = document.createElement('div');
            messageList.className = 'messagelist';
            var header = document.querySelector('.change-list-header');
            if (!header) return;
            header.parentNode.insertBefore(messageList, header.nextSibling);
        }
        var msg = document.createElement('div');
        msg.className = type;
        msg.textContent = text;
        messageList.appendChild(msg);
        setTimeout(function () {
            msg.remove();
            if (messageList.children.length === 0) { messageList.remove(); }
        }, 5000);
    }

    function syncReaders() {
        var btn = document.getElementById('sync-readers-btn');
        if (!btn) return;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-sync fa-spin"></i> ' + (T.syncing || 'Syncing...');

        fetch('/' + lang + '/admin/pos/readers/sync/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            btn.innerHTML = '<i class="fas fa-sync"></i> ' + (T.syncReaders || 'Sync Readers');
            btn.disabled = false;
            if (data.success) {
                showMessage((T.synced || 'Synced') + ' ' + data.synced + ' ' + (T.readers || 'readers'), 'success');
            } else if (data.errors && data.errors.length > 0) {
                showMessage((T.syncWithErrors || 'Sync completed with errors:') + ' ' + data.errors.join(', '), 'warning');
            }
            if (window.AdminListFilters) { window.AdminListFilters.applyFilters(); }
        })
        .catch(function (error) {
            btn.innerHTML = '<i class="fas fa-sync"></i> ' + (T.syncReaders || 'Sync Readers');
            btn.disabled = false;
            console.error('Sync error:', error);
            showMessage((T.syncFailed || 'Sync failed:') + ' ' + error.message, 'error');
        });
    }

    function quickAssignTerminal(select) {
        var readerId = select.dataset.readerId;
        var terminalId = select.value;
        select.disabled = true;

        fetch('/' + lang + '/admin/pos/readers/quick-assign/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: 'reader_id=' + readerId + '&terminal_id=' + terminalId
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            select.disabled = false;
            if (data.success) {
                showMessage(data.message, 'success');
            } else {
                showMessage(data.error || (T.failedAssign || 'Failed to assign'), 'error');
                if (window.AdminListFilters) { window.AdminListFilters.applyFilters(); }
            }
        })
        .catch(function (error) {
            select.disabled = false;
            console.error('Assign error:', error);
            showMessage(T.failedAssignReader || 'Failed to assign reader', 'error');
        });
    }

    function refreshReaderStatus(readerId, btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-sync fa-spin"></i>';

        fetch('/' + lang + '/admin/pos/readers/' + readerId + '/refresh-status/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sync"></i>';

            if (data.success) {
                var card = btn.closest('.list-row-card');
                var statusBadge = card.querySelector('.reader-status-badge');
                statusBadge.className = 'list-row-card-badge reader-status-badge';

                if (data.status === 'online') {
                    statusBadge.classList.add('list-row-card-badge-success');
                    statusBadge.innerHTML = '<span class="terminal-status-dot online"></span> ' + (T.online || 'Online');
                } else if (data.status === 'busy') {
                    statusBadge.classList.add('list-row-card-badge-warning');
                    statusBadge.innerHTML = '<span class="terminal-status-dot busy"></span> ' + (T.busy || 'Busy');
                } else {
                    statusBadge.innerHTML = '<span class="terminal-status-dot offline"></span> ' + (T.offline || 'Offline');
                }

                if (data.status === 'offline') {
                    card.classList.add('disabled');
                } else {
                    card.classList.remove('disabled');
                }

                var lastSeenEl = card.querySelector('.reader-last-seen');
                if (lastSeenEl) { lastSeenEl.textContent = T.justNow || 'Just now'; }
            } else {
                showMessage(data.error || (T.failedRefresh || 'Failed to refresh status'), 'error');
            }
        })
        .catch(function (error) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sync"></i>';
            console.error('Refresh error:', error);
            showMessage(T.failedRefresh || 'Failed to refresh status', 'error');
        });
    }

    document.addEventListener('click', function (e) {
        if (e.target.closest('[data-action="sync-readers"]')) {
            e.preventDefault();
            syncReaders();
        } else {
            var refreshBtn = e.target.closest('[data-action="refresh-reader-status"]');
            if (refreshBtn) {
                e.preventDefault();
                refreshReaderStatus(refreshBtn.dataset.readerId, refreshBtn);
            }
        }
    });

    document.addEventListener('change', function (e) {
        var select = e.target.closest('[data-action="quick-assign-terminal"]');
        if (select) { quickAssignTerminal(select); }
    });

    document.addEventListener('DOMContentLoaded', function () {
        var el = document.getElementById('reader-list-translations');
        if (el) { try { T = JSON.parse(el.textContent); } catch (err) {} }

        if (window.AdminListFilters) {
            window.AdminListFilters.init({
                url: '/' + lang + '/admin/pos/terminal-readers/filter/',
                resultsContainer: 'reader-results',
                resultsCount: 'reader-count'
            });
        }
    });
}());
