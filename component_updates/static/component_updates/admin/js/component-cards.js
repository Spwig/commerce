/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    'use strict';

    var msgs = {
        confirmInstall: 'Are you sure you want to install the update for this component?',
        failedInstall: 'Failed to install update.',
        errorInstall: 'Error installing update. Please try again.',
        confirmLock: 'Are you sure you want to lock this component?',
        confirmUnlock: 'Are you sure you want to unlock this component?',
        failedLock: 'Failed to update lock status.',
        errorLock: 'Error updating lock status. Please try again.'
    };

    document.addEventListener('DOMContentLoaded', function () {
        var island = document.getElementById('component-cards-i18n');
        if (island) {
            try { msgs = JSON.parse(island.textContent); } catch (e) {}
        }
    });

    async function installUpdate(componentId) {
        if (!await AdminModal.confirm(msgs.confirmInstall)) return;

        var langPrefix = AdminUtils.getLanguagePrefix();
        var url = langPrefix + '/admin/component_updates/componentregistry/' + componentId + '/install-update/';

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                window.location.reload();
            } else {
                AdminModal.alert({message: data.error || msgs.failedInstall, type: 'error'});
            }
        })
        .catch(function () {
            AdminModal.alert({message: msgs.errorInstall, type: 'error'});
        });
    }

    async function toggleLock(componentId, lock) {
        if (!await AdminModal.confirm(lock ? msgs.confirmLock : msgs.confirmUnlock)) return;

        var langPrefix = AdminUtils.getLanguagePrefix();
        var url = langPrefix + '/admin/component_updates/componentregistry/' + componentId + '/toggle-lock/';

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ lock: lock })
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                window.location.reload();
            } else {
                AdminModal.alert({message: data.error || msgs.failedLock, type: 'error'});
            }
        })
        .catch(function () {
            AdminModal.alert({message: msgs.errorLock, type: 'error'});
        });
    }

    /* ==========================================================
       Changelog Modal
       ========================================================== */

    function openChangelogModal(slug, name) {
        var overlay = document.getElementById('changelog-modal');
        var body = document.getElementById('changelog-modal-body');
        var title = document.getElementById('changelog-modal-title');
        if (!overlay || !body) return;

        // Set title with component name
        if (title && name) {
            title.textContent = name;
        }

        // Show modal with loading state
        overlay.classList.add('active');
        document.body.classList.add('admin-modal-body-locked');
        body.innerHTML = '<p class="version-history-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</p>';

        // Fetch and render
        if (typeof VersionHistory !== 'undefined') {
            VersionHistory.fetch(slug).then(function (versions) {
                body.innerHTML = '';
                body.appendChild(VersionHistory.render(versions));
            }).catch(function () {
                body.innerHTML = '<p class="version-history-empty">Could not load version history.</p>';
            });
        }
    }

    function closeChangelogModal() {
        var overlay = document.getElementById('changelog-modal');
        if (!overlay) return;
        overlay.classList.remove('active');
        document.body.classList.remove('admin-modal-body-locked');
    }

    /* ==========================================================
       Event delegation
       ========================================================== */

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) return;
        var action = btn.dataset.action;

        if (action === 'install-update') {
            if (btn.dataset.pk) installUpdate(btn.dataset.pk);
        } else if (action === 'toggle-lock') {
            if (btn.dataset.pk) toggleLock(btn.dataset.pk, btn.dataset.lock === 'true');
        } else if (action === 'view-changelog') {
            openChangelogModal(btn.dataset.slug, btn.dataset.name);
        } else if (action === 'close-changelog-modal') {
            closeChangelogModal();
        }
    });

    // Close changelog modal on overlay click
    document.addEventListener('click', function (e) {
        if (e.target && e.target.id === 'changelog-modal') {
            closeChangelogModal();
        }
    });

    // Close changelog modal on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            var overlay = document.getElementById('changelog-modal');
            if (overlay && overlay.classList.contains('active')) {
                closeChangelogModal();
            }
        }
    });

}());
