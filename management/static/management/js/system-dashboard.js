/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  let autoRefreshInterval;
  let cpuChart, memoryChart, diskChart, sessionsChart;

  function readConfig() {
    const el = document.getElementById('system-dashboard-config');
    return el ? el.dataset : {};
  }

  function initializeCharts() {
    const config = readConfig();
    function makeChart(id, label, color) {
      const el = document.getElementById(id);
      if (!el) return null;
      const rgba = color.replace('rgb', 'rgba').replace(')', ', 0.1)');
      return new Chart(el.getContext('2d'), {
        type: 'line',
        data: {
          labels: [],
          datasets: [
            {
              label: label,
              data: [],
              borderColor: color,
              backgroundColor: rgba,
              tension: 0.1,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: { y: { beginAtZero: true, max: id !== 'sessionsChart' ? 100 : undefined } },
        },
      });
    }
    cpuChart = makeChart('cpuChart', config.labelCpu || 'CPU Usage (%)', 'rgb(255, 107, 107)');
    memoryChart = makeChart(
      'memoryChart',
      config.labelMemory || 'Memory Usage (%)',
      'rgb(78, 205, 196)'
    );
    diskChart = makeChart('diskChart', config.labelDisk || 'Disk Usage (%)', 'rgb(69, 183, 209)');
    sessionsChart = makeChart(
      'sessionsChart',
      config.labelSessions || 'Active Sessions',
      'rgb(247, 183, 49)'
    );
  }

  function updateCharts(historyData) {
    const labels = historyData.map(function (item) {
      const date = new Date(item.timestamp);
      return date.getHours() + ':' + date.getMinutes().toString().padStart(2, '0');
    });
    function updateChart(chart, key) {
      if (!chart) return;
      chart.data.labels = labels;
      chart.data.datasets[0].data = historyData.map(function (i) {
        return i[key];
      });
      chart.update();
    }
    updateChart(cpuChart, 'cpu_percent');
    updateChart(memoryChart, 'memory_percent');
    updateChart(diskChart, 'disk_percent');
    updateChart(sessionsChart, 'active_sessions');
  }

  function loadChartData() {
    const config = readConfig();
    if (!config.metricsApiUrl) return;
    fetch(config.metricsApiUrl + '?hours=24')
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.history && data.history.length > 0) {
          updateCharts(data.history);
        }
      })
      .catch(function (error) {
        console.error('Error loading chart data:', error);
      });
  }

  function refreshMetrics() {
    location.reload();
  }

  function collectMetrics() {
    const config = readConfig();
    fetch(config.collectMetricsUrl, {
      method: 'POST',
      headers: { 'X-CSRFToken': AdminUtils.getCsrfToken() },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.success) {
          setTimeout(refreshMetrics, 1000);
        }
      })
      .catch(function (error) {
        console.error('Error collecting metrics:', error);
      });
  }

  function toggleAutoRefresh() {
    const checkbox = document.getElementById('auto-refresh');
    if (checkbox.checked) {
      autoRefreshInterval = setInterval(function () {
        loadChartData();
        updateLastUpdated();
      }, 30000);
      updateLastUpdated();
    } else {
      clearInterval(autoRefreshInterval);
      document.getElementById('last-updated').innerHTML = '';
    }
  }

  function updateLastUpdated() {
    const config = readConfig();
    const now = new Date();
    const el = document.getElementById('last-updated');
    if (el)
      el.innerHTML = (config.labelLastUpdated || 'Last updated') + ': ' + now.toLocaleTimeString();
  }

  async function toggleMaintenanceMode(enabled) {
    const config = readConfig();
    let reason = '';
    if (enabled) {
      reason = await AdminModal.prompt({
        message: config.msgMaintenanceReason || 'Enter maintenance reason (optional):',
        defaultValue: '',
      });
      if (reason === null) return;
    }
    fetch(config.toggleMaintenanceUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': AdminUtils.getCsrfToken() },
      body: JSON.stringify({ enabled: enabled, reason: reason || '' }),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.success) {
          location.reload();
        } else {
          AdminModal.alert({
            message:
              (config.msgFailedMaintenance || 'Failed to toggle maintenance mode') +
              ': ' +
              (data.error || config.msgUnknown || 'Unknown error'),
            type: 'error',
          });
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
        AdminModal.alert({
          message: config.msgFailedMaintenance || 'Failed to toggle maintenance mode',
          type: 'error',
        });
      });
  }

  async function checkForUpdates(btn) {
    const config = readConfig();
    const originalContent = btn.innerHTML;
    btn.innerHTML =
      '<i class="fas fa-spinner fa-spin"></i><span>' +
      (config.msgChecking || 'Checking...') +
      '</span>';
    btn.disabled = true;
    fetch(config.checkUpdatesUrl, {
      method: 'POST',
      headers: { 'X-CSRFToken': AdminUtils.getCsrfToken() },
    })
      .then(function (r) {
        return r.json();
      })
      .then(async function (data) {
        if (data.update_available) {
          const msg =
            (config.msgUpdateAvailable || 'Update available') +
            ': ' +
            data.available_version +
            '\n\n' +
            (config.msgViewUpgrade || 'Would you like to view upgrade options?');
          if (await AdminModal.confirm(msg)) {
            window.location.href = config.upgradeUrl;
          } else {
            location.reload();
          }
        } else {
          AdminModal.alert(
            (config.msgLatestVersion || 'You are running the latest version') +
              ': ' +
              data.current_version
          );
          btn.innerHTML = originalContent;
          btn.disabled = false;
        }
      })
      .catch(function (error) {
        console.error('Error:', error);
        AdminModal.alert({
          message: config.msgFailedCheck || 'Failed to check for updates',
          type: 'error',
        });
        btn.innerHTML = originalContent;
        btn.disabled = false;
      });
  }

  function runDiagnostics(btn) {
    const config = readConfig();
    const originalContent = btn.innerHTML;
    btn.innerHTML =
      "<i class='fas fa-spinner fa-spin'></i><span>" +
      (config.msgRunning || 'Running...') +
      '</span>';
    btn.disabled = true;
    fetch(config.runDiagnosticsUrl, {
      method: 'POST',
      headers: { 'X-CSRFToken': AdminUtils.getCsrfToken() },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.success) {
          showDiagnosticsResults(data.results, config);
        } else {
          AdminModal.alert({
            message:
              (config.msgDiagnosticsFailed || 'Diagnostics failed') +
              ': ' +
              (data.error || config.msgUnknown || 'Unknown error'),
            type: 'error',
          });
        }
        btn.innerHTML = originalContent;
        btn.disabled = false;
      })
      .catch(function (error) {
        console.error('Error:', error);
        AdminModal.alert({
          message: config.msgFailedDiagnostics || 'Failed to run diagnostics',
          type: 'error',
        });
        btn.innerHTML = originalContent;
        btn.disabled = false;
      });
  }

  function showDiagnosticsResults(results, config) {
    const modal = document.createElement('div');
    modal.className = 'admin-modal-overlay active';
    modal.innerHTML =
      "<div class='admin-modal'>" +
      "<div class='admin-modal-header'><h2 class='admin-modal-title'><i class='fas fa-stethoscope'></i> " +
      (config.labelDiagResults || 'Diagnostics Results') +
      '</h2>' +
      "<button data-action='close-modal' class='admin-modal-close'><i class='fas fa-times'></i></button></div>" +
      "<div class='admin-modal-body'>" +
      formatDiagnosticsResults(results, config) +
      '</div>' +
      "<div class='admin-modal-footer'><button data-action='close-modal' class='button'>" +
      (config.labelClose || 'Close') +
      '</button></div>' +
      '</div>';
    document.body.appendChild(modal);
    document.body.classList.add('admin-modal-body-locked');
  }

  function formatDiagnosticsResults(results, config) {
    if (!results) return '<p>' + (config.msgNoResults || 'No results available') + '</p>';
    let html = "<div class='diagnostics-grid'>";
    function addCheck(key, icon, label) {
      if (!results[key]) return;
      const r = results[key];
      const ok = r.healthy !== undefined ? r.healthy : r.valid;
      html +=
        '<div class="diagnostics-item ' +
        (ok ? 'healthy' : 'unhealthy') +
        '">' +
        '<i class="fas ' +
        icon +
        '"></i>' +
        "<span class='check-name'>" +
        label +
        '</span>' +
        "<span class='check-status'>" +
        (ok ? '✓' : '✗') +
        '</span>' +
        (r.error ? "<span class='check-error'>" + r.error + '</span>' : '') +
        '</div>';
    }
    addCheck('database', 'fa-database', config.labelDatabase || 'Database');
    addCheck('redis', 'fa-bolt', config.labelRedis || 'Redis');
    addCheck('celery', 'fa-cogs', config.labelCelery || 'Celery Workers');
    if (results.ssl) {
      const ssl = results.ssl;
      html +=
        '<div class="diagnostics-item ' +
        (ssl.valid ? 'healthy' : 'unhealthy') +
        '">' +
        "<i class='fas fa-lock'></i>" +
        "<span class='check-name'>" +
        (config.labelSSL || 'SSL Certificate') +
        '</span>' +
        "<span class='check-status'>" +
        (ssl.valid ? '✓' : '✗') +
        '</span>' +
        (ssl.days_remaining !== null && ssl.days_remaining !== undefined
          ? "<span class='check-detail'>" +
            (config.labelDaysRemaining || 'Days remaining') +
            ': ' +
            ssl.days_remaining +
            '</span>'
          : '') +
        (ssl.error ? "<span class='check-error'>" + ssl.error + '</span>' : '') +
        '</div>';
    }
    if (results.disk) {
      const disk = results.disk;
      const diskWarning = disk.percent > 80;
      html +=
        '<div class="diagnostics-item ' +
        (diskWarning ? 'warning' : 'healthy') +
        '">' +
        "<i class='fas fa-hdd'></i>" +
        "<span class='check-name'>" +
        (config.labelDisk || 'Disk Space') +
        '</span>' +
        "<span class='check-status'>" +
        (diskWarning ? '⚠' : '✓') +
        '</span>' +
        "<span class='check-detail'>" +
        disk.percent +
        '% ' +
        (config.labelUsed || 'used') +
        ' (' +
        disk.free_display +
        ' ' +
        (config.labelFree || 'free') +
        ')</span>' +
        '</div>';
    }
    html += '</div>';
    return html;
  }

  // Progress polling
  let progressPollingInterval = null;

  function startProgressPolling() {
    if (progressPollingInterval) return;
    progressPollingInterval = setInterval(function () {
      pollBackupProgress();
      pollRestoreProgress();
      pollUpgradeProgress();
    }, 2000);
  }

  function stopProgressPolling() {
    if (progressPollingInterval) {
      clearInterval(progressPollingInterval);
      progressPollingInterval = null;
    }
  }

  function pollBackupProgress() {
    const card = document.getElementById('backup-progress-card');
    if (!card) return;
    const config = readConfig();
    const backupId = card.dataset.backupId;
    fetch(config.backupProgressUrl.replace('0', backupId))
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.status === 'completed' || data.status === 'failed') {
          location.reload();
        } else {
          card.querySelector('.progress-bar').style.width = data.progress_percent + '%';
          card.querySelector('.progress-percent').textContent = data.progress_percent + '%';
          card.querySelector('.current-step').textContent = data.current_step || '';
        }
      })
      .catch(function (error) {
        console.error('Error polling backup:', error);
      });
  }

  function pollRestoreProgress() {
    const card = document.getElementById('restore-progress-card');
    if (!card) return;
    const config = readConfig();
    const restoreId = card.dataset.restoreId;
    fetch(config.restoreProgressUrl.replace('0', restoreId))
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.status === 'completed' || data.status === 'failed') {
          location.reload();
        } else {
          card.querySelector('.progress-bar').style.width = data.progress_percent + '%';
          card.querySelector('.progress-percent').textContent = data.progress_percent + '%';
          card.querySelector('.current-step').textContent = data.current_step || '';
        }
      })
      .catch(function (error) {
        console.error('Error polling restore:', error);
      });
  }

  function pollUpgradeProgress() {
    const card = document.getElementById('upgrade-progress-card');
    if (!card) return;
    const config = readConfig();
    const upgradeId = card.dataset.upgradeId;
    fetch(config.upgradeProgressUrl.replace('0', upgradeId))
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (
          data.status === 'completed' ||
          data.status === 'failed' ||
          data.status === 'rolled_back'
        ) {
          location.reload();
        } else {
          card.querySelector('.progress-bar').style.width = data.progress_percent + '%';
          card.querySelector('.progress-percent').textContent = data.progress_percent + '%';
          card.querySelector('.current-step').textContent = data.current_step || '';
        }
      })
      .catch(function (error) {
        console.error('Error polling upgrade:', error);
      });
  }

  document.addEventListener('click', function (e) {
    const el = e.target.closest('[data-action]');
    if (!el) return;
    switch (el.dataset.action) {
      case 'refresh-metrics':
        refreshMetrics();
        break;
      case 'collect-metrics':
        collectMetrics();
        break;
      case 'toggle-maintenance':
        toggleMaintenanceMode(el.dataset.value === 'true');
        break;
      case 'check-for-updates':
        checkForUpdates(el.closest('.quick-action-btn') || el);
        break;
      case 'run-diagnostics':
        runDiagnostics(el.closest('.quick-action-btn') || el);
        break;
      case 'close-modal':
        var modal = el.closest('.admin-modal-overlay');
        if (modal) {
          modal.remove();
          document.body.classList.remove('admin-modal-body-locked');
        }
        break;
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    initializeCharts();
    loadChartData();

    const autoRefreshEl = document.getElementById('auto-refresh');
    if (autoRefreshEl) {
      autoRefreshEl.addEventListener('change', toggleAutoRefresh);
    }

    const operationsSection = document.getElementById('operations-progress');
    if (operationsSection && !operationsSection.classList.contains('mgmt-hidden')) {
      startProgressPolling();
    }

    setInterval(function () {
      const checkbox = document.getElementById('auto-refresh');
      if (checkbox && checkbox.checked) {
        updateLastUpdated();
      }
    }, 1000);
    updateLastUpdated();
  });
})();
