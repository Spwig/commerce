(function() {
    'use strict';

    // ── Config ──────────────────────────────────────────────────────
    const configEl = document.getElementById('hosted-upgrade-config');
    if (!configEl) return;

    const URLS = {
        check:    configEl.dataset.checkUrl,
        schedule: configEl.dataset.scheduleUrl,
        status:   configEl.dataset.statusUrl,
        snooze:   configEl.dataset.snoozeUrl,
        cancel:   configEl.dataset.cancelUrl,
        directProgress: configEl.dataset.directProgressUrl || '',
    };
    const MSGS = {
        confirmUpgrade: configEl.dataset.msgConfirmUpgrade,
        upgradeStarted: configEl.dataset.msgUpgradeStarted,
        upgradeScheduled: configEl.dataset.msgUpgradeScheduled,
        upgradeCancelled: configEl.dataset.msgUpgradeCancelled,
        snoozed: configEl.dataset.msgSnoozed,
        error: configEl.dataset.msgError,
        restarting: configEl.dataset.msgRestarting,
        upgradeFailed: configEl.dataset.msgUpgradeFailed,
        connectionError: configEl.dataset.msgConnectionError,
        completed: configEl.dataset.msgCompleted,
        starting: configEl.dataset.msgStarting,
    };

    let pollTimer = null;
    let pollInterval = 3000;
    let consecutiveErrors = 0;

    // ── Helpers ─────────────────────────────────────────────────────

    function getCsrfToken() {
        if (typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken) {
            return AdminUtils.getCsrfToken();
        }
        const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }

    function show(el) { if (el) el.style.display = ''; }
    function hide(el) { if (el) el.style.display = 'none'; }

    function toast(msg, type) {
        if (typeof AdminModal !== 'undefined' && AdminModal.toast) {
            AdminModal.toast(msg, type || 'info');
        }
    }

    async function apiFetch(url, options) {
        const defaults = {
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
        };
        const resp = await fetch(url, { ...defaults, ...options });
        let data;
        try {
            data = await resp.json();
        } catch (e) {
            data = { error: 'Unexpected response from server' };
        }
        return { ok: resp.ok, status: resp.status, data: data };
    }

    // ── DOM References ──────────────────────────────────────────────

    const els = {
        loading:       document.getElementById('loading-state'),
        upToDate:      document.getElementById('up-to-date-card'),
        updateCard:    document.getElementById('update-available-card'),
        schedulePicker:document.getElementById('schedule-picker'),
        scheduledCard: document.getElementById('scheduled-card'),
        progressCard:  document.getElementById('progress-card'),
        completedCard: document.getElementById('completed-card'),
        errorCard:     document.getElementById('error-card'),
        snoozedCard:   document.getElementById('snoozed-card'),

        versionTo:     document.getElementById('version-to'),
        badgeSecurity: document.getElementById('badge-security'),
        badgeMigration:document.getElementById('badge-migration'),
        changelogSection: document.getElementById('changelog-section'),
        changelogContent: document.getElementById('changelog-content'),

        btnUpgradeNow: document.getElementById('btn-upgrade-now'),
        btnSchedule:   document.getElementById('btn-schedule'),
        btnSnooze:     document.getElementById('btn-snooze'),
        snoozeMenu:    document.getElementById('snooze-menu'),
        scheduleDatetime: document.getElementById('schedule-datetime'),
        btnConfirmSchedule: document.getElementById('btn-confirm-schedule'),
        btnCancelSchedule: document.getElementById('btn-cancel-schedule'),

        scheduledVersion: document.getElementById('scheduled-version'),
        scheduledDisplay: document.getElementById('scheduled-datetime-display'),
        btnCancelUpgrade: document.getElementById('btn-cancel-upgrade'),

        progressBar:     document.getElementById('progress-bar'),
        progressPercent: document.getElementById('progress-percent'),
        progressStep:    document.getElementById('progress-step'),

        completedMsg:    document.getElementById('completed-message'),
        errorHeading:    document.getElementById('error-heading'),
        errorMsg:        document.getElementById('error-message'),
        errorSupport:    document.getElementById('error-support'),
        btnRetry:        document.getElementById('btn-retry'),
        snoozedUntil:    document.getElementById('snoozed-until-display'),
    };

    // ── State Management ────────────────────────────────────────────

    function hideAll() {
        hide(els.loading);
        hide(els.upToDate);
        hide(els.updateCard);
        hide(els.schedulePicker);
        hide(els.scheduledCard);
        hide(els.progressCard);
        hide(els.completedCard);
        hide(els.errorCard);
        hide(els.snoozedCard);
    }

    // ── Check for Updates ───────────────────────────────────────────

    async function checkForUpdates() {
        show(els.loading);
        try {
            const { ok, data } = await apiFetch(URLS.check);
            hide(els.loading);

            if (!ok) {
                showError(data.error || MSGS.error);
                return;
            }

            // Active upgrade in progress?
            if (data.active_upgrade) {
                const status = data.active_upgrade.status;
                if (status === 'in_progress' || status === 'pending') {
                    showProgress(data.active_upgrade);
                    startPolling();
                    return;
                }
                if (status === 'scheduled') {
                    showScheduled(data.active_upgrade);
                    return;
                }
            }

            // Snoozed?
            if (data.snoozed_until) {
                const snoozedDate = new Date(data.snoozed_until);
                if (snoozedDate > new Date()) {
                    showSnoozed(snoozedDate);
                    return;
                }
            }

            // Update available?
            if (data.update_available && data.latest) {
                showUpdateAvailable(data.latest);
            } else {
                hideAll();
                show(els.upToDate);
            }
        } catch (e) {
            hide(els.loading);
            showError(MSGS.error);
        }
    }

    function showUpdateAvailable(latest) {
        hideAll();
        els.versionTo.textContent = 'v' + latest.version;

        if (latest.security_update) show(els.badgeSecurity);
        else hide(els.badgeSecurity);
        if (latest.requires_migration) show(els.badgeMigration);
        else hide(els.badgeMigration);

        if (latest.changelog) {
            els.changelogContent.textContent = latest.changelog;
            show(els.changelogSection);
        }

        // For security updates, only show the 24h snooze option
        els.snoozeMenu.querySelectorAll('[data-snooze]').forEach(btn => {
            if (latest.security_update && parseInt(btn.dataset.snooze, 10) > 24) {
                btn.style.display = 'none';
            } else {
                btn.style.display = '';
            }
        });

        show(els.updateCard);
    }

    function showScheduled(upgrade) {
        hideAll();
        els.scheduledVersion.textContent = 'v' + upgrade.to_version;
        if (upgrade.scheduled_at) {
            els.scheduledDisplay.textContent = new Date(upgrade.scheduled_at).toLocaleString();
        }
        show(els.scheduledCard);
    }

    function showProgress(upgrade) {
        hideAll();
        els.progressBar.style.width = (upgrade.progress_percent || 0) + '%';
        els.progressPercent.textContent = upgrade.progress_percent || 0;
        els.progressStep.textContent = upgrade.current_step || MSGS.starting || 'Starting...';
        show(els.progressCard);
    }

    function showError(msg, type) {
        hideAll();
        if (type === 'upgrade_failed') {
            els.errorHeading.textContent = MSGS.upgradeFailed || 'Upgrade Failed';
            show(els.errorSupport);
            hide(els.btnRetry);
        } else {
            els.errorHeading.textContent = MSGS.connectionError || 'Connection Error';
            hide(els.errorSupport);
            show(els.btnRetry);
        }
        els.errorMsg.textContent = msg;
        show(els.errorCard);
    }

    function showSnoozed(date) {
        hideAll();
        els.snoozedUntil.textContent = date.toLocaleString();
        show(els.snoozedCard);
    }

    // ── Upgrade Now ─────────────────────────────────────────────────

    async function upgradeNow() {
        const confirmed = typeof AdminModal !== 'undefined' && AdminModal.confirm
            ? await AdminModal.confirm(MSGS.confirmUpgrade)
            : confirm(MSGS.confirmUpgrade);
        if (!confirmed) return;

        try {
            const { ok, data } = await apiFetch(URLS.schedule, {
                method: 'POST',
                body: JSON.stringify({ action: 'now' }),
            });
            if (ok) {
                toast(MSGS.upgradeStarted, 'success');
                showProgress(data);
                startPolling();
            } else {
                toast(data.error || MSGS.error, 'error');
            }
        } catch (e) {
            toast(MSGS.error, 'error');
        }
    }

    // ── Schedule ────────────────────────────────────────────────────

    function openSchedulePicker() {
        // Set min to now, max to 14 days
        const now = new Date();
        const max = new Date(now.getTime() + 14 * 24 * 60 * 60 * 1000);
        els.scheduleDatetime.min = toLocalISO(now);
        els.scheduleDatetime.max = toLocalISO(max);
        els.scheduleDatetime.value = '';
        hide(els.updateCard);
        show(els.schedulePicker);
    }

    function toLocalISO(date) {
        const pad = n => String(n).padStart(2, '0');
        return date.getFullYear() + '-' + pad(date.getMonth()+1) + '-' + pad(date.getDate())
            + 'T' + pad(date.getHours()) + ':' + pad(date.getMinutes());
    }

    async function confirmSchedule() {
        const val = els.scheduleDatetime.value;
        if (!val) {
            els.scheduleDatetime.focus();
            els.scheduleDatetime.classList.add('input-error');
            setTimeout(() => els.scheduleDatetime.classList.remove('input-error'), 2000);
            return;
        }

        const scheduledAt = new Date(val).toISOString();
        try {
            const { ok, data } = await apiFetch(URLS.schedule, {
                method: 'POST',
                body: JSON.stringify({ action: 'schedule', scheduled_at: scheduledAt }),
            });
            if (ok) {
                toast(MSGS.upgradeScheduled || 'Upgrade scheduled', 'success');
                showScheduled(data);
            } else {
                toast(data.error || MSGS.error, 'error');
            }
        } catch (e) {
            toast(MSGS.error, 'error');
        }
    }

    function cancelSchedulePicker() {
        hide(els.schedulePicker);
        checkForUpdates();
    }

    // ── Snooze ──────────────────────────────────────────────────────

    function toggleSnoozeMenu() {
        const menu = els.snoozeMenu;
        menu.style.display = menu.style.display === 'none' ? '' : 'none';
    }

    async function snooze(hours) {
        hide(els.snoozeMenu);
        try {
            const { ok, data } = await apiFetch(URLS.snooze, {
                method: 'POST',
                body: JSON.stringify({ snooze_hours: hours }),
            });
            if (ok) {
                toast(MSGS.snoozed, 'info');
                showSnoozed(new Date(data.snoozed_until));
            } else {
                toast(data.error || MSGS.error, 'error');
            }
        } catch (e) {
            toast(MSGS.error, 'error');
        }
    }

    // ── Cancel Scheduled Upgrade ────────────────────────────────────

    async function cancelUpgrade() {
        try {
            const { ok, data } = await apiFetch(URLS.cancel, { method: 'POST' });
            if (ok) {
                toast(MSGS.upgradeCancelled, 'info');
                checkForUpdates();
            } else {
                toast(data.error || MSGS.error, 'error');
            }
        } catch (e) {
            toast(MSGS.error, 'error');
        }
    }

    // ── Progress Polling ────────────────────────────────────────────
    // Strategy: poll shop proxy first. When the proxy fails (shop is
    // restarting), fall back to polling the update server directly via
    // the public progress endpoint. This gives uninterrupted progress
    // visibility even during container restarts.

    let useDirectPolling = false;

    function startPolling() {
        stopPolling();
        pollInterval = 3000;
        consecutiveErrors = 0;
        useDirectPolling = false;
        pollTimer = setInterval(pollStatus, pollInterval);
    }

    function stopPolling() {
        if (pollTimer) {
            clearInterval(pollTimer);
            pollTimer = null;
        }
    }

    async function pollStatus() {
        let upgrade = null;

        if (!useDirectPolling) {
            // Try shop proxy first
            try {
                const { ok, data } = await apiFetch(URLS.status);
                if (ok && data.upgrade) {
                    consecutiveErrors = 0;
                    upgrade = data.upgrade;
                } else {
                    throw new Error('Proxy unavailable');
                }
            } catch (e) {
                consecutiveErrors++;
                if (consecutiveErrors >= 2 && URLS.directProgress) {
                    // Shop proxy is down — switch to direct polling
                    useDirectPolling = true;
                    els.progressStep.textContent = MSGS.restarting || 'Your store is restarting...';
                }
            }
        }

        // Direct polling to update server (bypasses shop proxy)
        if (useDirectPolling && URLS.directProgress) {
            try {
                const resp = await fetch(URLS.directProgress);
                if (resp.ok) {
                    const data = await resp.json();
                    if (data.upgrade) {
                        upgrade = data.upgrade;
                        // If upgrade is done, check if shop proxy is back
                        if (upgrade.status === 'completed' || upgrade.status === 'failed') {
                            useDirectPolling = false;
                        }
                    }
                }
            } catch (e) {
                // Even direct polling failed — update server might be down too
            }
        }

        if (!upgrade) return;

        // Handle terminal states
        if (upgrade.status === 'completed') {
            stopPolling();
            hideAll();
            els.completedMsg.textContent =
                (MSGS.completed || 'Successfully upgraded to') + ' v' + upgrade.to_version;
            show(els.completedCard);
            // Wait for shop to be reachable before reloading
            waitForShopAndReload();
            return;
        }

        if (upgrade.status === 'failed') {
            stopPolling();
            showError(upgrade.error_message || 'Upgrade failed', 'upgrade_failed');
            return;
        }

        // Update progress display
        els.progressBar.style.width = (upgrade.progress_percent || 0) + '%';
        els.progressPercent.textContent = upgrade.progress_percent || 0;
        if (upgrade.current_step) {
            els.progressStep.textContent = upgrade.current_step;
        }
    }

    async function waitForShopAndReload() {
        // Poll the shop until it's back, then reload
        var attempts = 0;
        var maxAttempts = 30;
        var checkShop = setInterval(async function() {
            attempts++;
            try {
                var resp = await fetch(URLS.check, { method: 'GET' });
                if (resp.ok) {
                    clearInterval(checkShop);
                    location.reload();
                }
            } catch (e) {
                // Shop still down
            }
            if (attempts >= maxAttempts) {
                clearInterval(checkShop);
                location.reload(); // Try reload anyway
            }
        }, 3000);
    }

    // ── Event Listeners ─────────────────────────────────────────────

    els.btnUpgradeNow.addEventListener('click', upgradeNow);
    els.btnSchedule.addEventListener('click', openSchedulePicker);
    els.btnSnooze.addEventListener('click', toggleSnoozeMenu);
    els.btnConfirmSchedule.addEventListener('click', confirmSchedule);
    els.btnCancelSchedule.addEventListener('click', cancelSchedulePicker);
    els.btnCancelUpgrade.addEventListener('click', cancelUpgrade);
    els.btnRetry.addEventListener('click', checkForUpdates);

    var btnViewUpdate = document.getElementById('btn-view-update');
    if (btnViewUpdate) {
        btnViewUpdate.addEventListener('click', async function() {
            // Re-check but skip snooze display
            show(els.loading);
            try {
                var resp = await apiFetch(URLS.check);
                hide(els.loading);
                if (resp.ok && resp.data.update_available && resp.data.latest) {
                    showUpdateAvailable(resp.data.latest);
                } else {
                    hideAll();
                    show(els.upToDate);
                }
            } catch (e) {
                hide(els.loading);
                showError(MSGS.error);
            }
        });
    }

    // Snooze menu buttons
    els.snoozeMenu.querySelectorAll('[data-snooze]').forEach(btn => {
        btn.addEventListener('click', () => snooze(parseInt(btn.dataset.snooze, 10)));
    });

    // Close snooze menu on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.snooze-wrapper')) {
            hide(els.snoozeMenu);
        }
    });

    // ── Init ────────────────────────────────────────────────────────
    checkForUpdates();

})();
