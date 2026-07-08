/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Sync Progress JS
 * AJAX polling for sync/migration job progress.
 * Used by Settings Sync step 4 and Full Migration step 4.
 *
 * Features:
 * - Real-time progress bars and stats
 * - Elapsed time and ETA display
 * - Live activity log with cursor-based streaming
 * - Media transfer stats (bytes/files) for full migration
 * - Connection status indicator with reconnect detection
 * - Safe-to-leave notice management
 */
(function() {
    'use strict';

    const configEl = document.getElementById('sync-progress-config');
    if (!configEl) return;
    const config = JSON.parse(configEl.textContent);

    const POLL_INTERVAL = 2000; // 2 seconds
    let pollTimer = null;
    let logCursor = 0;
    let consecutiveErrors = 0;
    let startedAtMs = null; // Server start time in ms (from first poll)

    // Initialize progress bar widths from data attributes
    initProgressWidths();

    // Start the sync if status is pending/awaiting_confirmation
    if (config.status === 'pending' || config.status === 'awaiting_confirmation') {
        startSync();
    } else if (config.status === 'running') {
        startPolling();
    }

    // Activity log toggle
    const logToggle = document.getElementById('log-toggle');
    if (logToggle) {
        logToggle.addEventListener('click', function() {
            const logContainer = document.getElementById('activity-log');
            if (logContainer) {
                const isHidden = logContainer.classList.contains('sync-hidden');
                logContainer.classList.toggle('sync-hidden', !isHidden);
                logToggle.classList.toggle('open', isHidden);
            }
        });
    }

    async function startSync() {
        try {
            const response = await fetch(config.startUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': config.csrfToken,
                    'Content-Type': 'application/json',
                },
            });
            const data = await response.json();
            if (data.status === 'started') {
                startPolling();
            }
        } catch (err) {
            console.error('Failed to start sync:', err);
        }
    }

    function startPolling() {
        pollTimer = setInterval(pollProgress, POLL_INTERVAL);
        pollProgress(); // immediate first poll
    }

    async function pollProgress() {
        try {
            const url = config.progressUrl + '?log_cursor=' + logCursor;
            const response = await fetch(url);
            const data = await response.json();

            // Reset error counter on success
            if (consecutiveErrors > 0) {
                updateConnectionStatus('restored');
                consecutiveErrors = 0;
            }

            // Capture server start time on first poll
            if (data.started_at && !startedAtMs) {
                startedAtMs = new Date(data.started_at).getTime();
            }

            updateOverallProgress(data);
            updateTimeInfo(data);
            updateStepItems(data.steps || []);
            updateActivityLog(data.activity_log || [], data.log_cursor);
            updateSafeToLeave(data.status);

            // Stop polling when complete or failed
            if (['completed', 'failed', 'rolled_back', 'cancelled'].includes(data.status)) {
                clearInterval(pollTimer);
                updateStatusText(data);
                updateActions(data);
                updateConnectionStatus('');
            }
        } catch (err) {
            console.error('Progress poll error:', err);
            consecutiveErrors++;
            if (consecutiveErrors >= 2) {
                updateConnectionStatus('lost');
            }
        }
    }

    function updateOverallProgress(data) {
        const progressBar = document.getElementById('overall-progress-bar');
        const progressLabel = document.getElementById('progress-label');
        const progressPercent = document.getElementById('progress-percent');

        if (progressBar) progressBar.style.width = data.progress_percent + '%';
        if (progressLabel) progressLabel.textContent = data.current_step || '';
        if (progressPercent) progressPercent.textContent = data.progress_percent + '%';

        // Stats
        const statSynced = document.getElementById('stat-synced');
        const statSkipped = document.getElementById('stat-skipped');
        const statFailed = document.getElementById('stat-failed');
        const statTotal = document.getElementById('stat-total');

        if (statSynced) statSynced.textContent = data.items_synced;
        if (statSkipped) statSkipped.textContent = data.items_skipped;
        if (statFailed) statFailed.textContent = data.items_failed;
        if (statTotal) statTotal.textContent = data.items_total;
    }

    function updateTimeInfo(data) {
        const timeInfo = document.getElementById('progress-time-info');
        const elapsedEl = document.getElementById('elapsed-time');
        const etaEl = document.getElementById('eta-time');

        if (!timeInfo || !elapsedEl || !etaEl) return;

        const elapsed = data.elapsed_seconds;
        if (elapsed === null || elapsed === undefined) return;

        // Show the time info row
        timeInfo.classList.remove('sync-hidden');

        // Update elapsed
        const t = config.translations;
        setTextWithIcon(elapsedEl, 'fas fa-clock',
            (t.elapsed || 'Elapsed:') + ' ' + formatDuration(elapsed));

        // Calculate and show ETA (only when running and progress > 5%)
        const isRunning = !['completed', 'failed', 'rolled_back', 'cancelled'].includes(data.status);
        if (isRunning && data.progress_percent > 5) {
            const totalEstimate = elapsed / (data.progress_percent / 100);
            const remaining = Math.max(0, Math.round(totalEstimate - elapsed));
            setTextWithIcon(etaEl, 'fas fa-hourglass-half',
                (t.remaining || 'Remaining:') + ' ~' + formatDuration(remaining));
            etaEl.classList.remove('eta-calculating');
        } else if (isRunning) {
            etaEl.textContent = '';
            etaEl.appendChild(makeIcon('fas fa-hourglass-half'));
            etaEl.appendChild(document.createTextNode(' ' + (t.remaining || 'Remaining:') + ' '));
            var calcSpan = document.createElement('span');
            calcSpan.className = 'eta-calculating';
            calcSpan.textContent = t.calculating || 'calculating...';
            etaEl.appendChild(calcSpan);
        } else {
            // Completed/failed: just show total elapsed
            etaEl.classList.add('sync-hidden');
        }
    }

    function updateStepItems(steps) {
        const container = document.getElementById('step-items-container');
        if (!container) return;

        steps.forEach(step => {
            const el = document.getElementById('step-' + step.category);
            if (!el) return;

            // Update icon
            const icon = el.querySelector('.step-icon-circle');
            if (icon) {
                icon.className = 'step-icon-circle step-icon-' + step.status;
                if (step.status === 'completed') {
                    setIconContent(icon, 'fas fa-check');
                } else if (step.status === 'running') {
                    setIconContent(icon, 'fas fa-spinner fa-spin');
                } else if (step.status === 'failed') {
                    setIconContent(icon, 'fas fa-times');
                } else {
                    setIconContent(icon, 'fas fa-circle');
                }
            }

            // Update label
            const label = el.querySelector('.step-item-label');
            if (label) label.textContent = step.label;

            // Update percentage
            const pct = el.querySelector('.step-percentage-text');
            if (pct) {
                if (step.status === 'completed') pct.textContent = '100%';
                else if (step.status === 'running') pct.textContent = step.progress + '%';
                else pct.textContent = '';
            }

            // Update progress bar
            let progressContainer = el.querySelector('.step-progress-bar-container');
            if (step.status === 'running' || step.status === 'completed') {
                if (!progressContainer) {
                    const content = el.querySelector('.step-item-content');
                    if (content) {
                        const headerRow = content.querySelector('.step-header-row');
                        if (headerRow) {
                            progressContainer = document.createElement('div');
                            progressContainer.className = 'step-progress-bar-container';
                            var fill = document.createElement('div');
                            fill.className = 'step-progress-bar-fill';
                            progressContainer.appendChild(fill);
                            headerRow.insertAdjacentElement('afterend', progressContainer);
                        }
                    }
                }
                if (progressContainer) {
                    const fill = progressContainer.querySelector('.step-progress-bar-fill');
                    if (fill) {
                        fill.style.width = (step.status === 'completed' ? 100 : step.progress) + '%';
                    }
                }
            }

            // Update stats text
            const statsText = el.querySelector('.step-stats-text');
            if (statsText && step.items_total > 0) {
                const t = config.translations;
                let text = step.items_synced + ' ' + t.synced +
                    ' / ' + step.items_failed + ' ' + t.failed +
                    ' / ' + step.items_total + ' ' + t.total;

                statsText.textContent = text;

                if (step.error_message) {
                    const errorSpan = document.createElement('span');
                    errorSpan.className = 'step-error-text';
                    errorSpan.textContent = ' ' + step.error_message;
                    statsText.appendChild(errorSpan);
                }
            }

            // Media transfer stats (extra_data)
            if (step.extra_data && step.category === 'media') {
                let mediaStats = el.querySelector('.step-media-stats');
                if (!mediaStats) {
                    const content = el.querySelector('.step-item-content');
                    if (content) {
                        mediaStats = document.createElement('div');
                        mediaStats.className = 'step-media-stats';
                        content.appendChild(mediaStats);
                    }
                }
                if (mediaStats) {
                    const ed = step.extra_data;
                    const filesText = (ed.files_transferred || 0) + ' of ' +
                        (ed.files_total || 0) + ' files';
                    const bytesText = formatBytes(ed.bytes_transferred || 0) + ' of ' +
                        formatBytes(ed.bytes_total || 0);
                    setTextWithIcon(mediaStats, 'fas fa-hdd',
                        filesText + ' (' + bytesText + ')');
                }
            }
        });
    }

    function updateActivityLog(newEntries, newCursor) {
        if (!newEntries.length) return;

        const entriesContainer = document.getElementById('log-entries');
        if (!entriesContainer) return;

        // Remove empty placeholder
        const emptyEl = document.getElementById('log-empty');
        if (emptyEl) emptyEl.remove();

        // Append new entries
        newEntries.forEach(entry => {
            const div = document.createElement('div');
            div.className = 'log-entry';

            const timeSpan = document.createElement('span');
            timeSpan.className = 'log-entry-time';
            timeSpan.textContent = entry.ts || '';

            const msgSpan = document.createElement('span');
            msgSpan.className = 'log-entry-msg';
            msgSpan.textContent = entry.msg || '';

            div.appendChild(timeSpan);
            div.appendChild(msgSpan);
            entriesContainer.appendChild(div);
        });

        // Auto-scroll to bottom
        const logContainer = document.getElementById('activity-log');
        if (logContainer && !logContainer.classList.contains('sync-hidden')) {
            logContainer.scrollTop = logContainer.scrollHeight;
        }

        // Update cursor
        if (newCursor !== undefined) {
            logCursor = newCursor;
        }
    }

    function updateSafeToLeave(status) {
        const notice = document.getElementById('safe-to-leave');
        if (!notice) return;

        notice.classList.toggle('sync-hidden', status !== 'running');
    }

    function updateConnectionStatus(state) {
        const statusEl = document.getElementById('connection-status');
        if (!statusEl) return;

        statusEl.className = 'progress-connection-status';

        if (state === 'lost') {
            statusEl.className += ' connection-lost';
            statusEl.textContent = config.translations.connectionLost || 'Connection lost, retrying...';
        } else if (state === 'restored') {
            statusEl.className += ' connection-restored';
            statusEl.textContent = config.translations.reconnected || 'Reconnected';
            // Clear after 3 seconds
            setTimeout(() => {
                if (statusEl.textContent === (config.translations.reconnected || 'Reconnected')) {
                    statusEl.textContent = '';
                    statusEl.className = 'progress-connection-status';
                }
            }, 3000);
        } else {
            statusEl.textContent = '';
        }
    }

    function updateStatusText(data) {
        const statusText = document.getElementById('progress-status-text');
        if (!statusText) return;

        const t = config.translations;
        if (data.status === 'completed') {
            statusText.textContent = t.completed;
        } else if (data.status === 'failed') {
            statusText.textContent = t.failedMsg;
        }
    }

    function updateActions(data) {
        const actionsEl = document.getElementById('progress-actions');
        if (!actionsEl) return;

        // For full migration, redirect to results on completion
        if (config.wizardType === 'fullmig' && data.status === 'completed' && config.resultsUrl) {
            window.location.href = config.resultsUrl;
            return;
        }

        // Rebuild actions for completion
        if (data.status === 'completed' || data.status === 'failed') {
            actionsEl.textContent = '';

            const backLink = document.createElement('a');
            backLink.href = document.querySelector('.back-link')?.href || '#';
            backLink.className = 'btn btn-secondary';
            const backIcon = document.createElement('i');
            backIcon.className = 'fas fa-arrow-left';
            backLink.appendChild(backIcon);
            backLink.appendChild(document.createTextNode(' ' + config.translations.backToDashboard));
            actionsEl.appendChild(backLink);

            if (data.is_rollbackable && config.translations.rollback) {
                const rollbackBtn = document.createElement('button');
                rollbackBtn.type = 'button';
                rollbackBtn.className = 'btn btn-secondary';
                rollbackBtn.addEventListener('click', handleRollback);
                const rollbackIcon = document.createElement('i');
                rollbackIcon.className = 'fas fa-undo';
                rollbackBtn.appendChild(rollbackIcon);
                rollbackBtn.appendChild(document.createTextNode(' ' + config.translations.rollback));
                actionsEl.appendChild(document.createTextNode(' '));
                actionsEl.appendChild(rollbackBtn);
            }
        }
    }

    // Rollback handler
    async function handleRollback() {
        var confirmed = await AdminModal.confirm({
            message: config.translations.confirmRollback,
            danger: true,
            confirmText: config.translations.rollback || 'Rollback'
        });
        if (!confirmed) return;

        try {
            const rollbackBtn = document.getElementById('rollback-btn');
            const url = (rollbackBtn && rollbackBtn.dataset.rollbackUrl) ||
                        config.progressUrl.replace('/sync-progress/', '/rollback/');

            await fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': config.csrfToken },
            });
            location.reload();
        } catch (err) {
            console.error('Rollback failed:', err);
        }
    }

    // -- Utility functions --

    function makeIcon(classes) {
        var i = document.createElement('i');
        i.className = classes;
        return i;
    }

    function setIconContent(container, iconClasses) {
        container.textContent = '';
        container.appendChild(makeIcon(iconClasses));
    }

    function setTextWithIcon(container, iconClasses, text) {
        container.textContent = '';
        container.appendChild(makeIcon(iconClasses));
        container.appendChild(document.createTextNode(' ' + text));
    }

    function formatDuration(seconds) {
        if (seconds < 60) return seconds + 's';
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        if (mins < 60) {
            return secs > 0 ? mins + 'm ' + secs + 's' : mins + 'm';
        }
        const hours = Math.floor(mins / 60);
        const remainMins = mins % 60;
        return remainMins > 0 ? hours + 'h ' + remainMins + 'm' : hours + 'h';
    }

    function formatBytes(bytes) {
        if (bytes === 0) return '0 B';
        const units = ['B', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        const value = bytes / Math.pow(1024, i);
        return value.toFixed(i > 0 ? 1 : 0) + ' ' + units[i];
    }

    function initProgressWidths() {
        document.querySelectorAll('[data-initial-width]').forEach(function(el) {
            el.style.width = el.dataset.initialWidth + '%';
        });
    }
})();
