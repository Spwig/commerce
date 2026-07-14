/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Translation Service Dashboard
 * Handles quick translation tests, model downloads, coverage management, and benchmarks
 */

(function () {
  'use strict';

  let downloadPollInterval = null;

  /**
   * Get CSRF token via AdminUtils
   */
  function getCsrfToken() {
    return AdminUtils.getCsrfToken();
  }

  /**
   * Show/hide download modal
   */
  function showDownloadModal() {
    document.getElementById('downloadModalOverlay').classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
  }

  function closeDownloadModal() {
    document.getElementById('downloadModalOverlay').classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
  }

  /**
   * Start model download
   */
  function startModelDownload(callback) {
    const statusUrl = (document.getElementById('translations-config') || document.body).dataset
      .downloadStatusUrl;
    const startUrl = (document.getElementById('translations-config') || document.body).dataset
      .downloadStartUrl;

    // First check if download is already in progress
    fetch(statusUrl)
      .then(response => response.json())
      .then(statusData => {
        if (statusData.status === 'downloading' || statusData.status === 'converting') {
          // Download already in progress, just start polling
          pollDownloadProgress(callback);
          return;
        } else if (statusData.status === 'complete') {
          // Already downloaded
          if (callback) callback();
          closeDownloadModal();
          return;
        }

        // No download in progress, start a new one
        fetch(startUrl, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        })
          .then(response => response.json())
          .then(data => {
            if (data.success || data.status === 'downloading') {
              pollDownloadProgress(callback);
            } else {
              AdminModal.alert({
                message: 'Failed to start download: ' + (data.error || data.message),
                type: 'error',
              });
              closeDownloadModal();
            }
          });
      });
  }

  /**
   * Poll download progress
   */
  function pollDownloadProgress(callback) {
    const statusUrl = (document.getElementById('translations-config') || document.body).dataset
      .downloadStatusUrl;

    if (downloadPollInterval) {
      clearInterval(downloadPollInterval);
    }

    downloadPollInterval = setInterval(() => {
      fetch(statusUrl)
        .then(response => response.json())
        .then(data => {
          updateProgressDisplay(data);

          if (data.status === 'complete') {
            clearInterval(downloadPollInterval);
            downloadPollInterval = null;
            closeDownloadModal();
            if (callback) callback();
          } else if (data.status === 'error' || data.status === 'idle') {
            clearInterval(downloadPollInterval);
            downloadPollInterval = null;
            closeDownloadModal();
            AdminModal.alert({ message: 'Download failed', type: 'error' });
          }
        });
    }, 2000);
  }

  /**
   * Update progress display
   */
  function updateProgressDisplay(data) {
    const progressBar = document.getElementById('modal-progress-bar');
    const progressPercentage = document.getElementById('modal-progress-percentage');
    const progressStatus = document.getElementById('modal-progress-status');
    const progressMessage = document.getElementById('modal-progress-message');
    const downloadSize = document.getElementById('modal-download-size');
    const downloadSpeed = document.getElementById('modal-download-speed');
    const downloadEta = document.getElementById('modal-download-eta');

    const progress = Math.round(data.progress || 0);
    progressBar.style.width = progress + '%';
    progressPercentage.textContent = progress + '%';

    let statusText = 'Downloading Model';
    if (data.status === 'converting') {
      statusText = 'Converting Model';
    } else if (data.status === 'complete') {
      statusText = '✅ Download Complete';
      progressBar.style.backgroundColor = '#28a745';
    }
    progressStatus.textContent = statusText;

    if (data.message) progressMessage.textContent = data.message;

    if (data.downloaded_mb !== undefined && data.total_size_mb !== undefined) {
      downloadSize.textContent = `${Math.round(data.downloaded_mb)} MB / ${Math.round(data.total_size_mb)} MB`;
    }

    if (data.speed_mbps !== undefined) {
      downloadSpeed.textContent = `${data.speed_mbps.toFixed(1)} MB/s`;
    }

    if (data.eta_seconds !== undefined && data.eta_seconds > 0) {
      const minutes = Math.floor(data.eta_seconds / 60);
      const seconds = Math.floor(data.eta_seconds % 60);
      downloadEta.textContent = `ETA: ${minutes}m ${seconds}s`;
    }
  }

  /**
   * Coverage Manager
   */
  const CoverageManager = {
    _pollInterval: null,
    _jobIds: [],

    refresh: function () {
      const btn = document.querySelector('.coverage-refresh-btn');
      if (btn) {
        const icon = btn.querySelector('i');
        icon.classList.add('fa-spin');
      }
      fetch('/api/translations/service/coverage/refresh/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() },
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            location.reload();
          }
        })
        .catch(() => {})
        .finally(() => {
          if (btn) btn.querySelector('i').classList.remove('fa-spin');
        });
    },

    translateAll: function () {
      const modal = document.getElementById('translate-all-modal');
      modal.classList.add('active');
      document.body.classList.add('admin-modal-body-locked');
      document.getElementById('translate-all-footer').setAttribute('hidden', '');
      document.getElementById('translate-all-body').innerHTML =
        '<div class="translate-all-loading"><i class="fas fa-spinner fa-spin"></i>' +
        '<p>Calculating what needs to be translated...</p></div>';

      fetch('/api/translations/service/translate-all/estimate/')
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            this._renderEstimate(data);
          } else {
            document.getElementById('translate-all-body').innerHTML =
              '<div class="translate-all-error"><i class="fas fa-exclamation-circle"></i>' +
              '<p>' +
              (data.error || 'Failed to calculate estimate') +
              '</p></div>';
          }
        })
        .catch(err => {
          document.getElementById('translate-all-body').innerHTML =
            '<div class="translate-all-error"><i class="fas fa-exclamation-circle"></i>' +
            '<p>Error: ' +
            err.message +
            '</p></div>';
        });
    },

    _renderEstimate: function (data) {
      let html = '<div class="translate-all-estimate">';
      html += '<div class="translate-all-summary">';
      html += '<p><strong>' + data.total_fields + '</strong> fields across ';
      html +=
        '<strong>' + data.content_types.length + '</strong> content types need translation into ';
      html += '<strong>' + data.languages.length + '</strong> languages.</p>';
      html += '<p class="translate-all-jobs-info"><i class="fas fa-tasks"></i> ';
      html += 'This will create <strong>' + data.total_jobs + '</strong> translation jobs.</p>';
      html += '</div>';

      // Content type breakdown
      html += '<table class="translate-all-breakdown"><thead><tr>';
      html += '<th>Content Type</th><th>Missing Fields</th><th>Jobs</th>';
      html += '</tr></thead><tbody>';
      for (let i = 0; i < data.content_types.length; i++) {
        const ct = data.content_types[i];
        html += '<tr><td><i class="' + ct.icon + '"></i> ' + ct.label + '</td>';
        html += '<td>' + ct.missing_fields + '</td>';
        html += '<td>' + ct.jobs + '</td></tr>';
      }
      html += '</tbody></table>';

      // Warning
      if (data.is_large) {
        html += '<div class="translate-all-warning">';
        html += '<i class="fas fa-exclamation-triangle"></i> ';
        html +=
          'Large translation batch. We recommend running during off-peak hours to avoid impacting site performance for your shoppers.';
        html += '</div>';
      }

      html += '</div>';
      document.getElementById('translate-all-body').innerHTML = html;
      document.getElementById('translate-all-footer').removeAttribute('hidden');
    },

    confirmTranslateAll: function () {
      const btn = document.getElementById('translate-all-confirm');
      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Starting...';

      fetch('/api/translations/service/translate-all/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
        body: JSON.stringify({ scope: 'all' }),
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            this._jobIds = data.job_ids || [];
            this._showProgress(data);
          } else {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-play"></i> Start Translation';
            AdminModal.alert({
              message: data.error || 'Failed to start translation',
              type: 'error',
            });
          }
        })
        .catch(err => {
          btn.disabled = false;
          btn.innerHTML = '<i class="fas fa-play"></i> Start Translation';
          AdminModal.alert({ message: 'Error: ' + err.message, type: 'error' });
        });
    },

    _showProgress: function (data) {
      const jobsUrl =
        (document.getElementById('translations-config') || document.body).dataset.jobsUrl ||
        '/admin/translations/translation-jobs/';
      document.getElementById('translate-all-footer').setAttribute('hidden', '');
      let html = '<div class="translate-all-progress">';
      html += '<div class="translate-all-progress__icon"><i class="fas fa-cogs fa-spin"></i></div>';
      html += '<h4>Translation in progress</h4>';
      html += '<p>' + (data.job_ids ? data.job_ids.length : 0) + ' jobs created and queued.</p>';
      html +=
        '<div class="translate-all-progress__bar"><div class="translate-all-progress__fill" id="ta-progress-fill"></div></div>';
      html += '<p class="translate-all-progress__text" id="ta-progress-text">Starting...</p>';
      html +=
        '<p class="translate-all-progress__tip"><i class="fas fa-info-circle"></i> You can close this dialog. Jobs will continue in the background. Monitor progress in <a href="' +
        jobsUrl +
        '">Translation Jobs</a>.</p>';
      html += '</div>';
      document.getElementById('translate-all-body').innerHTML = html;

      // Start polling
      this._pollInterval = setInterval(() => {
        this._pollProgress();
      }, 5000);
    },

    _pollProgress: function () {
      if (!this._jobIds.length) return;
      fetch('/api/translations/service/translate-all/status/?job_ids=' + this._jobIds.join(','))
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            const fill = document.getElementById('ta-progress-fill');
            const text = document.getElementById('ta-progress-text');
            if (fill) fill.style.width = data.overall_progress + '%';
            if (text)
              text.textContent =
                data.completed +
                '/' +
                data.total_jobs +
                ' jobs completed' +
                (data.failed > 0 ? ' (' + data.failed + ' failed)' : '');

            if (data.completed + data.failed >= data.total_jobs) {
              clearInterval(this._pollInterval);
              if (text) text.textContent += ' — Done!';
              if (fill) fill.style.width = '100%';
            }
          }
        })
        .catch(() => {});
    },

    closeModal: function () {
      document.getElementById('translate-all-modal').classList.remove('active');
      document.body.classList.remove('admin-modal-body-locked');
      if (this._pollInterval) {
        clearInterval(this._pollInterval);
        this._pollInterval = null;
      }
      // If jobs were running, refresh the page to update coverage
      if (this._jobIds.length) {
        this._jobIds = [];
        location.reload();
      }
    },
  };

  /**
   * Handle quick translation test form
   */
  function handleQuickTestForm(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const resultDiv = document.getElementById('translation-result');
    const resultText = document.getElementById('translated-text');
    const translateBtn = document.getElementById('translate-btn');
    const translateBtnText = document.getElementById('translate-btn-text');
    const translateBtnIcon = document.getElementById('translate-btn-icon');

    // Show loading state
    translateBtn.disabled = true;
    translateBtnText.textContent = translateBtnText.dataset.translating || 'Translating...';
    translateBtnIcon.className = 'fas fa-spinner fa-spin';

    // Hide previous results
    resultDiv.classList.add('hidden');

    const quickTranslateUrl = (document.getElementById('translations-config') || document.body)
      .dataset.quickTranslateUrl;

    fetch(quickTranslateUrl, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCsrfToken(),
      },
    })
      .then(response => response.json())
      .then(data => {
        // Reset button state
        translateBtn.disabled = false;
        translateBtnText.textContent = translateBtnText.dataset.label || 'Translate';
        translateBtnIcon.className = 'fas fa-language';

        if (data.success) {
          // Show results
          resultDiv.classList.remove('hidden');
          resultText.textContent = data.translated_text;

          // Update stats if elements exist
          const latencyEl = document.getElementById('translation-latency');
          const speedEl = document.getElementById('translation-speed');
          const charsEl = document.getElementById('translation-chars');

          if (latencyEl && data.duration_ms) {
            latencyEl.textContent = data.duration_ms.toFixed(0);
          }
          if (speedEl && data.chars_per_second) {
            speedEl.textContent = data.chars_per_second.toFixed(0);
          }
          if (charsEl && data.translated_text) {
            charsEl.textContent = data.translated_text.length;
          }

          // Smooth scroll to results
          resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
          // Show error
          resultDiv.classList.remove('hidden');
          resultText.innerHTML =
            '<div class="translation-error">❌ ' + (data.error || 'Translation failed') + '</div>';
        }
      })
      .catch(error => {
        console.error('Translation error:', error);
        // Reset button state
        translateBtn.disabled = false;
        translateBtnText.textContent = translateBtnText.dataset.label || 'Translate';
        translateBtnIcon.className = 'fas fa-language';

        // Show error
        resultDiv.classList.remove('hidden');
        resultText.innerHTML =
          '<div class="translation-error">❌ Connection error: ' + error.message + '</div>';
      });
  }

  /**
   * Handle service toggle
   */
  function handleServiceToggle(e) {
    const toggleUrl = (document.getElementById('translations-config') || document.body).dataset
      .toggleServiceUrl;

    fetch(toggleUrl, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'enabled=' + e.target.checked,
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const statusEl = document.getElementById('service-status');
          if (data.enabled) {
            statusEl.innerHTML = '<span class="status-online">● Online</span>';
          } else {
            statusEl.innerHTML = '<span class="status-offline">● Offline</span>';
          }
        }
      });
  }

  /**
   * Handle benchmark run
   */
  async function handleBenchmark(e) {
    const btn = e.target;
    const confirmMsg = btn.dataset.confirmMsg || 'Run performance test? This may take a minute.';

    if (!(await AdminModal.confirm(confirmMsg))) return;

    const benchmarkUrl = (document.getElementById('translations-config') || document.body).dataset
      .benchmarkUrl;

    btn.disabled = true;
    const originalText = btn.textContent;
    btn.textContent = btn.dataset.runningText || 'Running...';

    fetch(benchmarkUrl, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'source_lang=en&target_lang=es&num_samples=10&sample_length=medium',
    })
      .then(response => response.json())
      .then(data => {
        btn.disabled = false;
        btn.textContent = originalText;

        if (data.success) {
          const r = data.results;
          AdminModal.alert(
            `Benchmark Results:\nMedian Latency: ${r.median_latency_ms.toFixed(0)}ms\nTokens/second: ${r.tokens_per_second.toFixed(0)}\nCPU Load: ${r.cpu_load_percent.toFixed(1)}%`
          );
        } else {
          AdminModal.alert({ message: 'Benchmark failed', type: 'error' });
        }
      })
      .catch(error => {
        btn.disabled = false;
        btn.textContent = originalText;
        AdminModal.alert({ message: 'Error: ' + error, type: 'error' });
      });
  }

  /**
   * Handle all dashboard actions via delegation
   */
  function handleDashboardActions(e) {
    const actionElement = e.target.closest('[data-action]');
    if (!actionElement) return;

    const action = actionElement.dataset.action;

    switch (action) {
      case 'close-download-modal':
        e.preventDefault();
        closeDownloadModal();
        break;
      case 'refresh-coverage':
        e.preventDefault();
        CoverageManager.refresh();
        break;
      case 'translate-all':
        e.preventDefault();
        CoverageManager.translateAll();
        break;
      case 'close-translate-modal':
        e.preventDefault();
        CoverageManager.closeModal();
        break;
      case 'confirm-translate-all':
        e.preventDefault();
        CoverageManager.confirmTranslateAll();
        break;
      case 'run-benchmark':
        e.preventDefault();
        handleBenchmark(e);
        break;
    }
  }

  /**
   * Initialize dashboard
   */
  function init() {
    // Initialize dynamic widths from data attributes (CSP-safe)
    document.querySelectorAll('[data-width]').forEach(function (el) {
      el.style.width = el.dataset.width + '%';
    });
    // Initialize SVG coverage rings
    document.querySelectorAll('.coverage-ring__fill[data-percentage]').forEach(function (el) {
      const pct = parseFloat(el.dataset.percentage) || 0;
      el.style.strokeDashoffset = 326.73 - (326.73 * pct) / 100;
    });

    // Event delegation for all dashboard actions
    document.addEventListener('click', handleDashboardActions);

    // Service toggle
    const serviceToggle = document.getElementById('service-toggle');
    if (serviceToggle) {
      serviceToggle.addEventListener('change', handleServiceToggle);
    }

    // Quick test form
    const quickTestForm = document.getElementById('quick-test-form');
    if (quickTestForm) {
      quickTestForm.addEventListener('submit', handleQuickTestForm);
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export for external access
  window.TranslationDashboard = {
    startDownload: startModelDownload,
    closeDownloadModal: closeDownloadModal,
    CoverageManager: CoverageManager,
  };
})();
