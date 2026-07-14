/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let translations = {};
  let cfg = {};
  let updateInterval = null;
  let logsExpanded = false;

  function init() {
    const tEl = document.getElementById('step5-data');
    if (tEl) {
      try {
        const data = JSON.parse(tEl.textContent);
        translations = data.translations || {};
        cfg = data.config || {};
      } catch (e) {}
    }

    document.addEventListener('click', handleActions);

    window.addEventListener('beforeunload', function () {
      if (updateInterval) {
        clearInterval(updateInterval);
      }
    });

    updateProgress();
    updateInterval = setInterval(updateProgress, 2000);
  }

  function handleActions(e) {
    const btn = e.target.closest('[data-action="toggle-logs"]');
    if (!btn) {
      return;
    }
    toggleLogs();
  }

  function toggleLogs() {
    const logsContainer = document.getElementById('logs-container');
    const toggleIcon = document.getElementById('logs-toggle-icon');
    const toggleText = document.getElementById('logs-toggle-text');

    logsExpanded = !logsExpanded;

    if (logsExpanded) {
      if (logsContainer) {
        logsContainer.style.display = 'block';
      }
      if (toggleIcon) {
        toggleIcon.className = 'fas fa-chevron-up';
      }
      if (toggleText) {
        toggleText.textContent = translations.hideDetails || 'Hide Details';
      }
    } else {
      if (logsContainer) {
        logsContainer.style.display = 'none';
      }
      if (toggleIcon) {
        toggleIcon.className = 'fas fa-chevron-down';
      }
      if (toggleText) {
        toggleText.textContent = translations.showDetails || 'Show Details';
      }
    }
  }

  function updateProgress() {
    if (!cfg.progressUrl) {
      return;
    }

    fetch(cfg.progressUrl)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        const pctEl = document.getElementById('overall-percentage');
        const barEl = document.getElementById('overall-progress-bar');
        const statusEl = document.getElementById('overall-status');
        const statsEl = document.getElementById('overall-stats');

        if (pctEl) {
          pctEl.textContent = Math.round(data.overall_progress);
        }
        if (barEl) {
          barEl.style.width = data.overall_progress + '%';
        }
        if (statusEl) {
          statusEl.textContent = data.status_display;
        }
        if (statsEl) {
          const totalProcessed = data.total_imported + data.total_skipped + data.total_failed;
          statsEl.textContent =
            totalProcessed +
            ' of ' +
            data.total_items +
            ' items: ' +
            data.total_imported +
            ' imported, ' +
            data.total_skipped +
            ' skipped, ' +
            data.total_failed +
            ' failed';
        }

        if (data.steps) {
          data.steps.forEach(function (step) {
            const stepEl = document.querySelector('.step-item[data-step="' + step.step_type + '"]');
            if (!stepEl) {
              return;
            }
            stepEl.style.display = 'block';

            const progressBar = stepEl.querySelector('.step-progress-bar');
            const percentage = stepEl.querySelector('.step-percentage');
            const stats = stepEl.querySelector('.step-stats');
            const icon = stepEl.querySelector('.step-icon');

            if (progressBar) {
              progressBar.style.width = step.progress + '%';
            }
            if (percentage) {
              percentage.textContent = Math.round(step.progress) + '%';
            }
            if (stats) {
              let stepText =
                step.imported +
                ' imported, ' +
                step.skipped +
                ' skipped, ' +
                step.failed +
                ' failed of ' +
                step.total;
              if (step.current_item && step.status === 'running') {
                stepText = step.current_item;
              }
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
          const logsContainer = document.getElementById('logs-container');
          if (logsContainer) {
            logsContainer.innerHTML = '';
            data.recent_logs.forEach(function (log) {
              const logEntry = document.createElement('div');
              logEntry.style.marginBottom = '8px';
              let logColor = 'var(--body-fg)';
              if (log.level === 'error' || log.level === 'critical') {
                logColor = 'var(--error-fg, #f44336)';
              } else if (log.level === 'warning') {
                logColor = 'var(--warning-color, #ff9800)';
              } else if (log.level === 'info') {
                logColor = 'var(--primary)';
              }
              logEntry.innerHTML =
                '<span style="color: ' +
                logColor +
                ';">[' +
                log.timestamp +
                '] ' +
                log.message +
                '</span>';
              logsContainer.appendChild(logEntry);
            });
            if (logsExpanded) {
              logsContainer.scrollTop = logsContainer.scrollHeight;
            }
          }
        }

        if (data.status === 'completed' || data.status === 'failed') {
          clearInterval(updateInterval);
          const actionButtons = document.getElementById('action-buttons');
          if (actionButtons) {
            actionButtons.style.display = 'flex';
          }

          if (data.status === 'failed') {
            if (statusEl) {
              statusEl.style.color = 'var(--error-fg, #f44336)';
            }
            const completeBtn = document.getElementById('complete-button');
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
})();
