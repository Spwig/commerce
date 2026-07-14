/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let cfg = {};
  let translations = {};
  let cohortComparisonChart;
  let retentionCurveChart;
  let chartData = null;

  function init() {
    const dataEl = document.getElementById('cohort-dashboard-data');
    if (dataEl) {
      try {
        const data = JSON.parse(dataEl.textContent);
        cfg = data.config || {};
        translations = data.translations || {};
      } catch (e) {
        // silently ignore parse errors
      }
    }
    loadCohortData();
    setupEventListeners();
  }

  function t(key) {
    return translations[key] || key;
  }

  function loadCohortData() {
    fetch(cfg.cohortDataApiUrl, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          chartData = data;
          renderComparisonChart('ltv');
        } else {
          console.error('Failed to load cohort data:', data.message);
        }
      })
      .catch(function (error) {
        console.error('Error loading cohort data:', error);
      });
  }

  function renderComparisonChart(chartType) {
    if (!chartData) {
      return;
    }

    const ctx = document.getElementById('cohortComparisonChart').getContext('2d');

    if (cohortComparisonChart) {
      cohortComparisonChart.destroy();
    }

    let dataset;
    let label;
    let yAxisLabel;

    if (chartType === 'ltv') {
      dataset = chartData.datasets.ltv_values;
      label = t('averageLtv');
      yAxisLabel = t('lifetimeValue');
    } else if (chartType === 'retention') {
      dataset = chartData.datasets.retention_rates;
      label = t('retentionRate3m');
      yAxisLabel = t('retentionPercent');
    } else {
      dataset = chartData.datasets.customer_counts;
      label = t('cohortSize');
      yAxisLabel = t('numberOfCustomers');
    }

    cohortComparisonChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: chartData.labels,
        datasets: [
          {
            label: label,
            data: dataset,
            backgroundColor: 'rgba(0, 124, 186, 0.7)',
            borderColor: 'rgba(0, 124, 186, 1)',
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: yAxisLabel,
            },
          },
          x: {
            title: {
              display: true,
              text: t('cohortMonth'),
            },
          },
        },
      },
    });
  }

  function setupEventListeners() {
    // Chart tabs
    document.querySelectorAll('.chart-tab').forEach(function (tab) {
      tab.addEventListener('click', function () {
        document.querySelectorAll('.chart-tab').forEach(function (t) {
          t.classList.remove('active');
        });
        this.classList.add('active');
        renderComparisonChart(this.dataset.chart);
      });
    });

    // View cohort details buttons
    document.querySelectorAll('.view-cohort-details').forEach(function (button) {
      button.addEventListener('click', function () {
        const cohortId = this.dataset.cohortId;
        const cohortName = this.dataset.cohortName;
        showRetentionCurve(cohortId, cohortName);
      });
    });

    // Rebuild cohorts button
    const rebuildBtn = document.getElementById('rebuildCohortsButton');
    if (rebuildBtn) {
      rebuildBtn.addEventListener('click', async function () {
        if (await AdminModal.confirm(t('rebuildConfirm'))) {
          rebuildCohorts();
        }
      });
    }

    // Modal close button (data-action pattern)
    document.addEventListener('click', function (event) {
      if (event.target.closest('[data-action="close-retention-modal"]')) {
        closeRetentionModal();
      }
    });

    // Close modal when clicking outside
    window.addEventListener('click', function (event) {
      const modal = document.getElementById('retentionModal');
      if (event.target === modal) {
        closeRetentionModal();
      }
    });
  }

  function showRetentionCurve(cohortId, cohortName) {
    document.getElementById('modalCohortName').textContent =
      cohortName + ' - ' + t('retentionCurve');
    document.getElementById('retentionModal').classList.add('active');
    document.body.classList.add('admin-modal-body-locked');

    fetch(cfg.cohortDataApiUrl + '?cohort_id=' + cohortId, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          renderRetentionCurve(data);
        }
      })
      .catch(function (error) {
        console.error('Error loading retention curve:', error);
      });
  }

  function renderRetentionCurve(data) {
    const ctx = document.getElementById('retentionCurveChart').getContext('2d');

    if (retentionCurveChart) {
      retentionCurveChart.destroy();
    }

    if (!data.retention_curve || data.retention_curve.length === 0) {
      document.getElementById('retentionStats').innerHTML =
        '<p class="text-center">' + t('notEnoughData') + '</p>';
      return;
    }

    const labels = data.retention_curve.map(function (point) {
      return t('month') + ' ' + point.month;
    });
    const retentionRates = data.retention_curve.map(function (point) {
      return point.retention_rate;
    });

    retentionCurveChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: t('retentionRate'),
            data: retentionRates,
            borderColor: '#007cba',
            backgroundColor: 'rgba(0, 124, 186, 0.1)',
            fill: true,
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            title: {
              display: true,
              text: t('retentionPercent'),
            },
          },
          x: {
            title: {
              display: true,
              text: t('monthsSinceFirstPurchase'),
            },
          },
        },
      },
    });

    const statsHTML =
      '<div class="stats-grid">' +
      '<div class="stat-item">' +
      '<span class="stat-label">' +
      t('cohortSizeLabel') +
      '</span>' +
      '<span class="stat-value">' +
      data.cohort.customer_count +
      '</span>' +
      '</div>' +
      '<div class="stat-item">' +
      '<span class="stat-label">' +
      t('totalRevenueLabel') +
      '</span>' +
      '<span class="stat-value">$' +
      data.cohort.total_revenue.toFixed(2) +
      '</span>' +
      '</div>' +
      '<div class="stat-item">' +
      '<span class="stat-label">' +
      t('avgLtvLabel') +
      '</span>' +
      '<span class="stat-value">$' +
      data.cohort.average_ltv.toFixed(2) +
      '</span>' +
      '</div>' +
      '</div>';
    document.getElementById('retentionStats').innerHTML = statsHTML;
  }

  function closeRetentionModal() {
    document.getElementById('retentionModal').classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
    if (retentionCurveChart) {
      retentionCurveChart.destroy();
    }
  }

  function rebuildCohorts() {
    const button = document.getElementById('rebuildCohortsButton');
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + t('rebuilding');

    fetch(cfg.recalculateLtvUrl, {
      method: 'POST',
      headers: {
        'X-CSRFToken': cfg.csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'scope=all&async=true',
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          AdminModal.toast(t('rebuildQueued'), 'success');
          setTimeout(function () {
            window.location.reload();
          }, 2000);
        } else {
          AdminModal.alert({ message: data.message || t('errorRebuilding'), type: 'error' });
          button.disabled = false;
          button.innerHTML = '<i class="fas fa-arrow-right"></i> ' + t('rebuildLabel');
        }
      })
      .catch(function () {
        AdminModal.alert({ message: t('networkError'), type: 'error' });
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-arrow-right"></i> ' + t('rebuildLabel');
      });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
