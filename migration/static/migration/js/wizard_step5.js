/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var translations = {};
    var cfg = {};
    var updateInterval = null;
    var logsExpanded = false;

    function init() {
        var tEl = document.getElementById('step5-data');
        if (tEl) {
            try {
                var data = JSON.parse(tEl.textContent);
                translations = data.translations || {};
                cfg = data.config || {};
            } catch (e) {}
        }

        document.addEventListener('click', handleActions);

        window.addEventListener('beforeunload', function () {
            if (updateInterval) { clearInterval(updateInterval); }
        });

        updateProgress();
        updateInterval = setInterval(updateProgress, 2000);
    }

    function handleActions(e) {
        var btn = e.target.closest('[data-action="toggle-logs"]');
        if (!btn) { return; }
        toggleLogs();
    }

    function toggleLogs() {
        var logsContainer = document.getElementById('logs-container');
        var toggleIcon = document.getElementById('logs-toggle-icon');
        var toggleText = document.getElementById('logs-toggle-text');

        logsExpanded = !logsExpanded;

        if (logsExpanded) {
            if (logsContainer) { logsContainer.style.display = 'block'; }
            if (toggleIcon) { toggleIcon.className = 'fas fa-chevron-up'; }
            if (toggleText) { toggleText.textContent = translations.hideDetails || 'Hide Details'; }
        } else {
            if (logsContainer) { logsContainer.style.display = 'none'; }
            if (toggleIcon) { toggleIcon.className = 'fas fa-chevron-down'; }
            if (toggleText) { toggleText.textContent = translations.showDetails || 'Show Details'; }
        }
    }

    function updateProgress() {
        if (!cfg.progressUrl) { return; }

        fetch(cfg.progressUrl)
            .then(function (response) { return response.json(); })
            .then(function (data) {
                var pctEl = document.getElementById('overall-percentage');
                var barEl = document.getElementById('overall-progress-bar');
                var statusEl = document.getElementById('overall-status');
                var statsEl = document.getElementById('overall-stats');

                if (pctEl) { pctEl.textContent = Math.round(data.overall_progress); }
                if (barEl) { barEl.style.width = data.overall_progress + '%'; }
                if (statusEl) { statusEl.textContent = data.status_display; }
                if (statsEl) {
                    var totalProcessed = data.total_imported + data.total_skipped + data.total_failed;
                    statsEl.textContent = totalProcessed + ' of ' + data.total_items + ' items: ' +
                        data.total_imported + ' imported, ' +
                        data.total_skipped + ' skipped, ' +
                        data.total_failed + ' failed';
                }

                if (data.steps) {
                    data.steps.forEach(function (step) {
                        var stepEl = document.querySelector('.step-item[data-step="' + step.step_type + '"]');
                        if (!stepEl) { return; }
                        stepEl.style.display = 'block';

                        var progressBar = stepEl.querySelector('.step-progress-bar');
                        var percentage = stepEl.querySelector('.step-percentage');
                        var stats = stepEl.querySelector('.step-stats');
                        var icon = stepEl.querySelector('.step-icon');

                        if (progressBar) { progressBar.style.width = step.progress + '%'; }
                        if (percentage) { percentage.textContent = Math.round(step.progress) + '%'; }
                        if (stats) {
                            var stepText = step.imported + ' imported, ' + step.skipped + ' skipped, ' + step.failed + ' failed of ' + step.total;
                            if (step.current_item && step.status === 'running') { stepText = step.current_item; }
                            stats.textContent = stepText;
                        }
                        if (icon) {
                            if (step.status === 'completed') {
                                icon.style.background = 'var(--success-fg, #28a745)';
                                icon.style.color = '#fff';
                            } else if (step.status === 'failed') {
                                icon.style.background = 'var(--error-fg, #f44336)';
                                icon.style.color = '#fff';
                            } else if (step.status === 'running') {
                                icon.style.background = 'var(--primary)';
                                icon.style.color = '#fff';
                            }
                        }
                    });
                }

                if (data.recent_logs) {
                    var logsContainer = document.getElementById('logs-container');
                    if (logsContainer) {
                        logsContainer.innerHTML = '';
                        data.recent_logs.forEach(function (log) {
                            var logEntry = document.createElement('div');
                            logEntry.style.marginBottom = '8px';
                            var logColor = 'var(--body-fg)';
                            if (log.level === 'error' || log.level === 'critical') {
                                logColor = 'var(--error-fg, #f44336)';
                            } else if (log.level === 'warning') {
                                logColor = 'var(--warning-color, #ff9800)';
                            } else if (log.level === 'info') {
                                logColor = 'var(--primary)';
                            }
                            logEntry.innerHTML = '<span style="color: ' + logColor + ';">[' + log.timestamp + '] ' + log.message + '</span>';
                            logsContainer.appendChild(logEntry);
                        });
                        if (logsExpanded) {
                            logsContainer.scrollTop = logsContainer.scrollHeight;
                        }
                    }
                }

                if (data.status === 'completed' || data.status === 'failed') {
                    clearInterval(updateInterval);
                    var actionButtons = document.getElementById('action-buttons');
                    if (actionButtons) { actionButtons.style.display = 'flex'; }

                    if (data.status === 'failed') {
                        if (statusEl) { statusEl.style.color = 'var(--error-fg, #f44336)'; }
                        var completeBtn = document.getElementById('complete-button');
                        if (completeBtn) {
                            completeBtn.textContent = translations.viewErrorReport || 'View Error Report';
                            completeBtn.classList.remove('success');
                            completeBtn.classList.add('danger');
                        }
                    }
                }
            })
            .catch(function (error) {
                console.error('Error fetching progress:', error);
            });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
