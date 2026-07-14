/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  let updateInfo = null;
  let currentUpdateId = null;
  let pollInterval = null;
  let hotfixPollInterval = null;
  let hotfixPollErrors = 0;
  let pollErrors = 0;
  const cfg = {};
  let msgs = {
    errorChecking: 'Error checking for updates:',
    noUpdateAvailable: 'No update available',
    errorStarting: 'Error starting update:',
    andMore: '... and more',
    noChangelog: 'No changelog available',
    starting: 'Starting...',
    updateNow: 'Update Now',
    updateCompleted: 'Update completed successfully!',
    updateFailed: 'Update failed:',
    unknownError: 'Unknown error',
    estTimeRemaining: 'Estimated time remaining:',
    seconds: 'seconds',
    confirmRollback: 'Are you sure you want to rollback to the previous version?',
    rollbackWarning:
      'This will revert to previous application code and may cause brief service interruption (~30 seconds). This cannot be undone.',
    rollbackNotReady: 'Rollback functionality will be implemented in Phase 3',
    noHotfixAvailable: 'No new hotfixes available for your platform version.',
    hotfixConfirm: 'Applying hotfixes will restart your store briefly (~30-60 seconds). Continue?',
    hotfixApplying: 'Applying Hotfixes',
    hotfixRollingBack: 'Rolling Back Hotfixes',
    hotfixCompleted: 'Hotfixes applied and verified successfully!',
    hotfixFailed: 'Hotfix apply failed:',
    hotfixRolledBackAuto: 'Verification failed — hotfixes were automatically rolled back.',
    hotfixRestarting: 'Restarting services... please wait',
    confirmHotfixRollback:
      'Are you sure you want to rollback all hotfixes? This will restart your store briefly (~30-60 seconds).',
    upgradeRestarting: 'Upgrading platform... services restarting, please wait',
  };

  function show(el) {
    if (el) el.classList.remove('platform-update-hidden');
  }

  function hide(el) {
    if (el) el.classList.add('platform-update-hidden');
  }

  function getCsrfToken() {
    if (typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken) {
      return AdminUtils.getCsrfToken();
    }
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : '';
  }

  function checkForUpdates() {
    const btn = document.getElementById('checkUpdatesBtn');
    btn.classList.add('loading');
    btn.disabled = true;

    fetch(cfg.checkUrl)
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        btn.classList.remove('loading');
        btn.disabled = false;

        if (data.error) {
          AdminModal.alert({ message: msgs.errorChecking + ' ' + data.error, type: 'error' });
          return;
        }

        updateInfo = data;

        if (data.update_available) {
          showUpdateAvailable(data);
        } else {
          showNoUpdates();
        }
      })
      .catch(function (error) {
        btn.classList.remove('loading');
        btn.disabled = false;
        AdminModal.alert({ message: msgs.errorChecking + ' ' + error, type: 'error' });
      });
  }

  function showUpdateAvailable(data) {
    hide(document.getElementById('noUpdatesCard'));
    show(document.getElementById('updateAvailableCard'));

    document.getElementById('newVersionDisplay').textContent = 'v' + data.latest_version;
    document.getElementById('currentVersionDisplay').textContent = 'v' + data.current_version;

    const sizeBytes = data.package_size_bytes || 0;
    const sizeMB = (sizeBytes / 1024 / 1024).toFixed(1);
    document.getElementById('packageSize').textContent = sizeMB + ' MB';

    const channel = data.channel || 'stable';
    document.getElementById('channelDisplay').textContent =
      channel.charAt(0).toUpperCase() + channel.slice(1);
    document.getElementById('updateChannel').textContent = channel.toUpperCase();
    document.getElementById('updateChannel').className = 'channel-badge channel-' + channel;

    const migrationWarning = document.getElementById('migrationWarning');
    if (data.requires_migration) {
      show(migrationWarning);
      document.getElementById('migrationTime').textContent = data.migration_estimate_seconds || 30;
    } else {
      hide(migrationWarning);
    }

    const securityBadge = document.getElementById('securityBadge');
    if (data.security_update) {
      show(securityBadge);
    } else {
      hide(securityBadge);
    }

    const changelogList = document.getElementById('changelogList');
    changelogList.innerHTML = '';

    if (data.changelog) {
      const lines = data.changelog.split('\n').filter(function (l) {
        return l.trim();
      });
      lines.slice(0, 5).forEach(function (line) {
        const li = document.createElement('li');
        li.textContent = line.replace(/^[-*]\s*/, '');
        changelogList.appendChild(li);
      });
      if (lines.length > 5) {
        var li = document.createElement('li');
        const em = document.createElement('em');
        em.textContent = msgs.andMore;
        li.appendChild(em);
        changelogList.appendChild(li);
      }
    } else {
      var li = document.createElement('li');
      li.textContent = msgs.noChangelog;
      changelogList.appendChild(li);
    }
  }

  function showNoUpdates() {
    hide(document.getElementById('updateAvailableCard'));
    show(document.getElementById('noUpdatesCard'));
  }

  function hideUpdateCard() {
    hide(document.getElementById('updateAvailableCard'));
  }

  function startUpdate() {
    if (!updateInfo || !updateInfo.update_available) {
      AdminModal.alert(msgs.noUpdateAvailable);
      return;
    }

    const btn = document.getElementById('startUpdateBtn');
    btn.disabled = true;
    btn.classList.add('loading');

    fetch(cfg.startUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.error) {
          AdminModal.alert({ message: msgs.errorStarting + ' ' + data.error, type: 'error' });
          btn.disabled = false;
          btn.classList.remove('loading');
          return;
        }
        currentUpdateId = data.update_id;
        document.getElementById('progressVersion').textContent = 'v' + updateInfo.latest_version;
        showProgressModal();
        startPolling();
      })
      .catch(function (error) {
        AdminModal.alert({ message: msgs.errorStarting + ' ' + error, type: 'error' });
        btn.disabled = false;
        btn.classList.remove('loading');
      });
  }

  function showProgressModal() {
    document.getElementById('progressOverlay').classList.add('active');
    hide(document.getElementById('updateAvailableCard'));
  }

  function hideProgressModal() {
    document.getElementById('progressOverlay').classList.remove('active');
  }

  function startPolling() {
    pollErrors = 0;
    pollInterval = setInterval(pollStatus, 2000);
    pollStatus();
  }

  function stopPolling() {
    if (pollInterval) {
      clearInterval(pollInterval);
      pollInterval = null;
    }
  }

  function pollStatus() {
    if (!currentUpdateId) return;

    const statusUrl = cfg.statusUrlTemplate + currentUpdateId + '/status/';

    fetch(statusUrl)
      .then(function (r) {
        if (r.redirected) {
          location.reload();
          return;
        }
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        if (!data) return;
        pollErrors = 0;
        updateProgressUI(data);

        if (
          data.status === 'completed' ||
          data.status === 'failed' ||
          data.status === 'rolled_back'
        ) {
          stopPolling();

          if (data.status === 'completed') {
            setTimeout(function () {
              hideProgressModal();
              location.reload();
            }, 2000);
          } else {
            // Show close button and hide "DO NOT CLOSE" on failure/rollback
            show(document.getElementById('closeProgressBtn'));
            hide(document.getElementById('doNotCloseLabel'));
          }
        }
      })
      .catch(function () {
        // Network error — shop is restarting during upgrade.
        // Show restarting message and keep polling (matches hotfix pattern).
        pollErrors++;
        if (pollErrors >= 2) {
          const estEl = document.getElementById('progressEstimate');
          estEl.textContent = '\u23F3 ' + msgs.upgradeRestarting;
          estEl.className = 'progress-estimate';
        }
        // Don't stop polling — the shop will come back
      });
  }

  function updateProgressUI(data) {
    const progressFill = document.getElementById('progressBarFill');
    progressFill.style.setProperty('--progress-width', data.progress_percent + '%');
    document.getElementById('progressPercent').textContent = data.progress_percent;

    const stepsContainer = document.getElementById('progressSteps');
    stepsContainer.innerHTML = '';

    (data.steps || []).forEach(function (step) {
      const stepEl = document.createElement('div');
      stepEl.className = 'progress-step ' + step.status;

      let icon = '\u2B1C';
      if (step.status === 'completed') icon = '\u2705';
      if (step.status === 'in_progress') icon = '\u23F3';

      const iconSpan = document.createElement('span');
      iconSpan.className = 'progress-step-icon';
      iconSpan.textContent = icon;

      const nameSpan = document.createElement('span');
      nameSpan.className = 'progress-step-name';
      nameSpan.textContent = step.name;

      const detailSpan = document.createElement('span');
      detailSpan.className = 'progress-step-detail';
      detailSpan.textContent = step.detail || '';

      stepEl.appendChild(iconSpan);
      stepEl.appendChild(nameSpan);
      stepEl.appendChild(detailSpan);
      stepsContainer.appendChild(stepEl);
    });

    const logContainer = document.getElementById('progressLog');
    logContainer.innerHTML = '';

    (data.log_lines || []).slice(-20).forEach(function (line) {
      const lineEl = document.createElement('div');
      lineEl.className = 'progress-log-line';
      lineEl.textContent = line;
      logContainer.appendChild(lineEl);
    });

    logContainer.scrollTop = logContainer.scrollHeight;

    const estEl = document.getElementById('progressEstimate');
    if (data.status === 'completed') {
      estEl.textContent = '\u2705 ' + msgs.updateCompleted;
      estEl.className = 'progress-estimate success';
    } else if (data.status === 'failed') {
      estEl.textContent =
        '\u274C ' + msgs.updateFailed + ' ' + (data.error_message || msgs.unknownError);
      estEl.className = 'progress-estimate error';
    } else if (data.estimated_seconds_remaining) {
      estEl.textContent =
        msgs.estTimeRemaining + ' ~' + data.estimated_seconds_remaining + ' ' + msgs.seconds;
      estEl.className = 'progress-estimate';
    }
  }

  async function confirmRollback() {
    if (
      await AdminModal.confirm({
        message: msgs.confirmRollback + '\n\n' + msgs.rollbackWarning,
        danger: true,
        confirmText: 'Rollback',
      })
    ) {
      AdminModal.alert(msgs.rollbackNotReady);
    }
  }

  // --- Hotfix Functions ---

  function checkForHotfix() {
    const btn = document.getElementById('checkHotfixBtn');
    btn.classList.add('loading');
    btn.disabled = true;

    fetch(cfg.checkHotfixUrl)
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        btn.classList.remove('loading');
        btn.disabled = false;

        if (data.error) {
          AdminModal.alert({ message: msgs.errorChecking + ' ' + data.error, type: 'error' });
          return;
        }

        if (data.hotfix_available) {
          location.reload();
        } else {
          AdminModal.alert(msgs.noHotfixAvailable);
        }
      })
      .catch(function (error) {
        btn.classList.remove('loading');
        btn.disabled = false;
        AdminModal.alert({ message: msgs.errorChecking + ' ' + error, type: 'error' });
      });
  }

  async function applyHotfix(btn) {
    const version = btn.dataset.version;
    let hotfixNumbers = [];

    if (btn.dataset.hotfixNumbers) {
      try {
        hotfixNumbers = JSON.parse(btn.dataset.hotfixNumbers);
      } catch (e) {
        /* ignore parse errors */
      }
    }
    if (!hotfixNumbers.length && btn.dataset.hotfixNumber) {
      hotfixNumbers = [parseInt(btn.dataset.hotfixNumber, 10)];
    }

    // Confirmation with restart warning
    if (
      !(await AdminModal.confirm({
        message: msgs.hotfixConfirm,
        confirmText: 'Apply Hotfixes',
      }))
    )
      return;

    btn.disabled = true;

    fetch(cfg.applyHotfixUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({
        version: version,
        hotfix_numbers: hotfixNumbers,
      }),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.success) {
          document.getElementById('progressVersion').textContent =
            msgs.hotfixApplying + ' — v' + version;
          hide(document.getElementById('closeProgressBtn'));
          show(document.getElementById('doNotCloseLabel'));
          showProgressModal();
          startHotfixPolling();
        } else {
          AdminModal.alert({ message: data.error || msgs.unknownError, type: 'error' });
          btn.disabled = false;
        }
      })
      .catch(function (error) {
        AdminModal.alert({ message: msgs.errorStarting + ' ' + error, type: 'error' });
        btn.disabled = false;
      });
  }

  async function rollbackHotfix() {
    if (
      !(await AdminModal.confirm({
        message: msgs.confirmHotfixRollback,
        danger: true,
        confirmText: 'Rollback',
      }))
    )
      return;

    fetch(cfg.rollbackHotfixUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.success) {
          document.getElementById('progressVersion').textContent = msgs.hotfixRollingBack;
          hide(document.getElementById('closeProgressBtn'));
          show(document.getElementById('doNotCloseLabel'));
          showProgressModal();
          startHotfixPolling();
        } else {
          AdminModal.alert({ message: data.error || msgs.unknownError, type: 'error' });
        }
      })
      .catch(function (error) {
        AdminModal.alert({ message: error, type: 'error' });
      });
  }

  // --- Hotfix Progress Polling ---

  function startHotfixPolling() {
    hotfixPollErrors = 0;
    hotfixPollInterval = setInterval(pollHotfixStatus, 2000);
    pollHotfixStatus();
  }

  function stopHotfixPolling() {
    if (hotfixPollInterval) {
      clearInterval(hotfixPollInterval);
      hotfixPollInterval = null;
    }
  }

  function pollHotfixStatus() {
    fetch(cfg.hotfixStatusUrl)
      .then(function (r) {
        if (r.redirected) {
          location.reload();
          return;
        }
        return r.json();
      })
      .then(function (data) {
        if (!data) return;
        hotfixPollErrors = 0;
        updateHotfixProgressUI(data);

        if (data.status === 'completed') {
          stopHotfixPolling();
          var estEl = document.getElementById('progressEstimate');
          estEl.textContent = '\u2705 ' + msgs.hotfixCompleted;
          estEl.className = 'progress-estimate success';
          setTimeout(function () {
            hideProgressModal();
            location.reload();
          }, 2000);
        } else if (data.status === 'failed') {
          stopHotfixPolling();
          var estEl = document.getElementById('progressEstimate');
          const errMsg = data.error_message || msgs.unknownError;
          estEl.textContent = '\u274C ' + msgs.hotfixFailed + ' ' + errMsg;
          estEl.className = 'progress-estimate error';
          show(document.getElementById('closeProgressBtn'));
          hide(document.getElementById('doNotCloseLabel'));
        } else if (data.status === 'idle') {
          // Operation finished before we started polling — reload
          stopHotfixPolling();
          location.reload();
        }
      })
      .catch(function () {
        // Network error — shop is restarting. Show restarting message
        // and continue polling. The proxy endpoint returns a safe
        // fallback when the upgrader is unreachable.
        hotfixPollErrors++;
        if (hotfixPollErrors >= 2) {
          const estEl = document.getElementById('progressEstimate');
          estEl.textContent = '\u23F3 ' + msgs.hotfixRestarting;
          estEl.className = 'progress-estimate';
        }
      });
  }

  function updateHotfixProgressUI(data) {
    // Reuse the same progress UI elements as platform upgrades
    const progressFill = document.getElementById('progressBarFill');
    progressFill.style.setProperty('--progress-width', data.progress_percent + '%');
    document.getElementById('progressPercent').textContent = data.progress_percent;

    const stepsContainer = document.getElementById('progressSteps');
    stepsContainer.innerHTML = '';

    (data.steps || []).forEach(function (step) {
      const stepEl = document.createElement('div');
      stepEl.className = 'progress-step ' + step.status;

      let icon = '\u2B1C';
      if (step.status === 'completed') icon = '\u2705';
      if (step.status === 'in_progress') icon = '\u23F3';
      if (step.status === 'failed') icon = '\u274C';

      const iconSpan = document.createElement('span');
      iconSpan.className = 'progress-step-icon';
      iconSpan.textContent = icon;

      const nameSpan = document.createElement('span');
      nameSpan.className = 'progress-step-name';
      nameSpan.textContent = step.name;

      const detailSpan = document.createElement('span');
      detailSpan.className = 'progress-step-detail';
      detailSpan.textContent = step.detail || '';

      stepEl.appendChild(iconSpan);
      stepEl.appendChild(nameSpan);
      stepEl.appendChild(detailSpan);
      stepsContainer.appendChild(stepEl);
    });

    const logContainer = document.getElementById('progressLog');
    logContainer.innerHTML = '';

    (data.log_lines || []).slice(-20).forEach(function (line) {
      const lineEl = document.createElement('div');
      lineEl.className = 'progress-log-line';
      lineEl.textContent = line;
      logContainer.appendChild(lineEl);
    });

    logContainer.scrollTop = logContainer.scrollHeight;

    const estEl = document.getElementById('progressEstimate');
    if (data.current_step && data.status === 'in_progress') {
      estEl.textContent = data.current_step;
      estEl.className = 'progress-estimate';
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Load i18n strings
    const i18nIsland = document.getElementById('platform-update-i18n');
    if (i18nIsland) {
      try {
        msgs = JSON.parse(i18nIsland.textContent);
      } catch (e) {}
    }

    const configEl = document.getElementById('platform-update-config');
    if (!configEl) return;

    cfg.checkUrl = configEl.dataset.checkUrl;
    cfg.startUrl = configEl.dataset.startUrl;
    cfg.statusUrlTemplate = configEl.dataset.statusUrlTemplate;
    cfg.checkHotfixUrl = configEl.dataset.checkHotfixUrl;
    cfg.applyHotfixUrl = configEl.dataset.applyHotfixUrl;
    cfg.rollbackHotfixUrl = configEl.dataset.rollbackHotfixUrl;
    cfg.hotfixStatusUrl = configEl.dataset.hotfixStatusUrl;

    // Event delegation
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      const action = btn.dataset.action;

      if (action === 'check-for-updates') {
        checkForUpdates();
      } else if (action === 'start-update') {
        startUpdate();
      } else if (action === 'hide-update-card') {
        hideUpdateCard();
      } else if (action === 'confirm-rollback') {
        confirmRollback();
      } else if (action === 'check-hotfix') {
        checkForHotfix();
      } else if (action === 'apply-hotfix') {
        applyHotfix(btn);
      } else if (action === 'rollback-hotfix') {
        rollbackHotfix();
      } else if (action === 'close-progress') {
        hideProgressModal();
        location.reload();
      }
    });

    // Resume in-progress update
    if (configEl.dataset.hasCurrentUpdate === 'true') {
      currentUpdateId = configEl.dataset.currentUpdateId;
      const progressVersionEl = document.getElementById('progressVersion');
      if (progressVersionEl) {
        progressVersionEl.textContent = 'v' + configEl.dataset.currentUpdateVersion;
      }
      showProgressModal();
      startPolling();
    }

    // Resume in-progress hotfix operation
    if (configEl.dataset.hotfixInProgress === 'true') {
      const hotfixVersion = configEl.dataset.hotfixTargetVersion || '';
      document.getElementById('progressVersion').textContent =
        msgs.hotfixApplying + (hotfixVersion ? ' — ' + hotfixVersion : '');
      hide(document.getElementById('closeProgressBtn'));
      show(document.getElementById('doNotCloseLabel'));
      showProgressModal();
      startHotfixPolling();
    }

    // Show cached update info
    if (configEl.dataset.updateAvailable === 'true') {
      try {
        updateInfo = JSON.parse(configEl.dataset.updateInfoJson || '{}');
        if (updateInfo && updateInfo.update_available) {
          showUpdateAvailable(updateInfo);
        }
      } catch (e) {
        console.error('Failed to parse cached update info:', e);
      }
    }
  });
})();
