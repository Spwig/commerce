/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var csrfToken = '';
    var jobId = '';
    var apiBase = '';

    function init() {
        var tEl = document.getElementById('step6-data');
        if (tEl) {
            try {
                var data = JSON.parse(tEl.textContent);
                csrfToken = data.csrfToken || '';
                jobId = data.jobId || '';
            } catch (e) {}
        }

        var lang = document.documentElement.lang || 'en';
        apiBase = '/' + lang + '/admin/migration/migrationjob/api/content-links/' + jobId + '/';

        document.addEventListener('click', handleActions);
        document.addEventListener('keydown', handleKeydown);

        updateApprovedCount();
    }

    function handleActions(e) {
        /* Rollback confirm */
        var rollbackBtn = e.target.closest('[data-action="confirm-rollback"]');
        if (rollbackBtn) {
            var msg = rollbackBtn.dataset.confirmMsg || 'Are you sure you want to rollback this migration? This will remove all imported data and cannot be undone.';
            e.preventDefault();
            AdminModal.confirm({ message: msg, danger: true, confirmText: 'Rollback' }).then(function(confirmed) {
                if (confirmed && rollbackBtn.href) { window.location.href = rollbackBtn.href; }
                else if (confirmed) { rollbackBtn.closest('form')?.submit(); }
            });
            return;
        }

        /* Toggle link group */
        var groupHeader = e.target.closest('[data-action="toggle-group"]');
        if (groupHeader) {
            if (e.target.closest('a')) { return; }
            toggleGroup(groupHeader);
            return;
        }

        /* Bulk approve high confidence */
        var bulkBtn = e.target.closest('[data-action="bulk-approve-high-confidence"]');
        if (bulkBtn) {
            bulkApproveHighConfidence();
            return;
        }

        /* Apply approved links */
        var applyBtn = e.target.closest('[data-action="apply-approved-links"]');
        if (applyBtn) {
            applyApprovedLinks();
            return;
        }

        /* Per-link approve/skip */
        var linkBtn = e.target.closest('.btn-link-action');
        if (linkBtn) {
            handleLinkAction(linkBtn);
        }
    }

    function handleKeydown(e) {
        if (e.key !== 'Enter' || !e.target.classList.contains('custom-url-input')) { return; }
        e.preventDefault();
        var linkId = e.target.dataset.linkId;
        var customUrl = e.target.value.trim();
        if (!customUrl) { return; }
        var row = e.target.closest('.link-row');
        var input = e.target;

        fetch(apiBase + 'update/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify({ link_id: parseInt(linkId), action: 'modify', custom_url: customUrl })
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                if (row) { row.dataset.status = 'modified'; }
                input.style.borderColor = 'var(--success-fg, #28a745)';
                input.style.background = '#f0fff0';
                updateApprovedCount();
            }
        });
    }

    function handleLinkAction(btn) {
        var action = btn.dataset.action;
        var linkId = btn.dataset.linkId;
        var row = btn.closest('.link-row');
        var body = { link_id: parseInt(linkId), action: action };

        if (action === 'modify') {
            var input = row ? row.querySelector('.custom-url-input') : null;
            if (input && input.value) { body.custom_url = input.value; }
        }

        fetch(apiBase + 'update/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify(body)
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (!data.success || !row) { return; }
            row.dataset.status = data.status;
            var actionCell = row.querySelector('td:last-child');
            if (data.status === 'approved') {
                if (actionCell) { actionCell.innerHTML = '<span class="status-icon-success"><i class="fas fa-check"></i></span>'; }
                var matchCell = row.querySelectorAll('td')[3];
                if (matchCell) { matchCell.innerHTML = '<span class="status-badge status-badge-approved">Approved</span>'; }
            } else if (data.status === 'skipped') {
                if (actionCell) { actionCell.innerHTML = '<span class="status-icon-muted"><i class="fas fa-forward"></i></span>'; }
                var matchCell2 = row.querySelectorAll('td')[3];
                if (matchCell2) { matchCell2.innerHTML = '<span class="status-badge status-badge-skipped">Skipped</span>'; }
            }
            updateApprovedCount();
        });
    }

    function updateApprovedCount() {
        var rows = document.querySelectorAll('.link-row');
        var count = 0;
        rows.forEach(function (row) {
            if (row.dataset.status === 'approved' || row.dataset.status === 'modified') { count++; }
        });
        var el = document.getElementById('approved-count');
        if (el) { el.textContent = count; }
        var btn = document.getElementById('apply-links-btn');
        if (btn) { btn.disabled = (count === 0); }
    }

    function showLinkStatus(msg, type) {
        var el = document.getElementById('link-status-msg');
        if (!el) { return; }
        el.style.display = 'block';
        el.style.background = type === 'success' ? '#d4edda' : type === 'error' ? '#f8d7da' : '#cce5ff';
        el.style.color = type === 'success' ? '#155724' : type === 'error' ? '#721c24' : '#004085';
        el.innerHTML = '<i class="fas fa-' + (type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle') + '"></i> ' + msg;
        setTimeout(function () { el.style.display = 'none'; }, 5000);
    }

    function toggleGroup(header) {
        var body = header.nextElementSibling;
        var icon = header.querySelector('.fa-chevron-down, .fa-chevron-right');
        if (!body) { return; }
        if (body.style.display === 'none') {
            body.style.display = '';
            if (icon) { icon.classList.remove('fa-chevron-right'); icon.classList.add('fa-chevron-down'); }
        } else {
            body.style.display = 'none';
            if (icon) { icon.classList.remove('fa-chevron-down'); icon.classList.add('fa-chevron-right'); }
        }
    }

    function bulkApproveHighConfidence() {
        fetch(apiBase + 'bulk-approve/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                showLinkStatus(data.approved_count + ' links auto-approved!', 'success');
                setTimeout(function () { location.reload(); }, 1000);
            }
        });
    }

    function applyApprovedLinks() {
        var btn = document.getElementById('apply-links-btn');
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Applying...';
        }

        fetch(apiBase + 'apply/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                showLinkStatus(
                    data.applied + ' links applied successfully' +
                    (data.failed > 0 ? ', ' + data.failed + ' failed' : '') + '.',
                    data.failed > 0 ? 'info' : 'success'
                );
                setTimeout(function () { location.reload(); }, 1500);
            } else {
                showLinkStatus('Error: ' + (data.error || 'Unknown error'), 'error');
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fas fa-play"></i> Apply Approved Links';
                }
            }
        })
        .catch(function (err) {
            showLinkStatus('Network error: ' + err, 'error');
            if (btn) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-play"></i> Apply Approved Links';
            }
        });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
