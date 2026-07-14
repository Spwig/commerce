/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let cfg = {};
  let translations = {};

  // Cohort tab chart instances
  let cohortComparisonChart;
  let retentionCurveChart;
  let ltvByChannelChart;
  let ltvByCategoryChart;
  let revenueCurveChart;
  let chartData = null;

  function init() {
    const dataEl = document.getElementById('customer-dashboard-data');
    if (dataEl) {
      try {
        const data = JSON.parse(dataEl.textContent);
        cfg = data.config || {};
        translations = data.translations || {};
      } catch (e) {
        // silently ignore parse errors
      }
    }

    setupTabSwitching();
    setupOverviewTab();
    setupModalListeners();

    // Check for tab parameter in URL
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');
    if (tabParam === 'cohorts') {
      switchTab('cohorts');
    }

    // Initialize cohort data if already on cohorts tab
    if (tabParam === 'cohorts') {
      initializeCohortTab();
    }
  }

  function t(key) {
    return translations[key] || key;
  }

  // ----------------------------------------------------------------
  // Tab switching
  // ----------------------------------------------------------------

  function setupTabSwitching() {
    document.querySelectorAll('.dashboard-tab').forEach(function (tab) {
      tab.addEventListener('click', function () {
        switchTab(this.dataset.tab);
      });
    });

    document.querySelectorAll('.dashboard-tab-switch').forEach(function (button) {
      button.addEventListener('click', function () {
        switchTab(this.dataset.tab);
      });
    });
  }

  function switchTab(tabName) {
    document.querySelectorAll('.dashboard-tab').forEach(function (tab) {
      tab.classList.toggle('active', tab.dataset.tab === tabName);
    });

    document.querySelectorAll('.dashboard-tab-content').forEach(function (content) {
      content.style.display = 'none';
      content.classList.remove('active');
    });

    const targetContent = document.getElementById(tabName + '-tab');
    if (targetContent) {
      targetContent.style.display = 'block';
      targetContent.classList.add('active');

      if (tabName === 'cohorts' && !window.cohortTabInitialized) {
        initializeCohortTab();
        window.cohortTabInitialized = true;
      }
    }

    const url = new URL(window.location);
    url.searchParams.set('tab', tabName);
    window.history.pushState({}, '', url);
  }

  // ----------------------------------------------------------------
  // Overview Tab
  // ----------------------------------------------------------------

  function setupOverviewTab() {
    fetch(cfg.analyticsApiUrl)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        renderGrowthChart(data);
        renderSegmentsChart(data);

        if (data.segment_revenue_data && data.segment_revenue_data.segments) {
          renderRevenueBySegmentChart(data.segment_revenue_data);
        }
        if (data.segment_insights && data.segment_insights.length > 0) {
          displaySegmentInsights(data.segment_insights);
        }
        if (data.churn_risk_data && data.churn_risk_data.buckets) {
          renderChurnRiskChart(data.churn_risk_data);
        }
        if (data.churn_risk_insights && data.churn_risk_insights.length > 0) {
          displayInsights(
            data.churn_risk_insights,
            'churnRiskInsightsPanel',
            'churnRiskInsightsList'
          );
        }
        if (data.frequency_histogram_data && data.frequency_histogram_data.histogram) {
          renderFrequencyHistogram(data.frequency_histogram_data);
        }
        if (data.frequency_histogram_insights && data.frequency_histogram_insights.length > 0) {
          displayInsights(
            data.frequency_histogram_insights,
            'frequencyInsightsPanel',
            'frequencyInsightsList'
          );
        }
        if (data.prediction_data) {
          renderPredictionAccuracyChart(data.prediction_data);
        }
        if (data.prediction_insights && data.prediction_insights.length > 0) {
          displayInsights(
            data.prediction_insights,
            'predictionInsightsPanel',
            'predictionInsightsList'
          );
        }
      });

    const refreshBtn = document.getElementById('refreshMetrics');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', function () {
        this.disabled = true;
        this.textContent = t('refreshing');

        const self = this;
        fetch(cfg.refreshMetricsUrl, {
          method: 'POST',
          headers: {
            'X-CSRFToken': cfg.csrfToken,
            'Content-Type': 'application/json',
          },
        })
          .then(function (response) {
            return response.json();
          })
          .then(function (data) {
            AdminModal.alert(data.message);
            location.reload();
          })
          .catch(function () {
            AdminModal.alert({ message: t('errorRefreshing'), type: 'error' });
            self.disabled = false;
            self.textContent = t('refreshMetrics');
          });
      });
    }
  }

  function renderGrowthChart(data) {
    const growthCtx = document.getElementById('growthChart').getContext('2d');
    new Chart(growthCtx, {
      type: 'line',
      data: {
        labels: data.customer_growth.months,
        datasets: [
          {
            label: t('newCustomers'),
            data: data.customer_growth.data,
            borderColor: '#007cba',
            backgroundColor: 'rgba(0, 124, 186, 0.1)',
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }

  function renderSegmentsChart(data) {
    const segmentsCtx = document.getElementById('segmentsChart').getContext('2d');
    new Chart(segmentsCtx, {
      type: 'doughnut',
      data: {
        labels: data.segment_revenue.map(function (s) {
          return s.name;
        }),
        datasets: [
          {
            data: data.segment_revenue.map(function (s) {
              return s.revenue;
            }),
            backgroundColor: data.segment_revenue.map(function (s) {
              return s.color;
            }),
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
        },
      },
    });
  }

  function renderRevenueBySegmentChart(segmentData) {
    const revenueChartCtx = document.getElementById('revenueBySegmentChart').getContext('2d');
    const segments = segmentData.segments;
    const labels = segments.map(function (s) {
      return s.name;
    });
    const revenues = segments.map(function (s) {
      return s.revenue;
    });
    const colors = segments.map(function (s) {
      return s.color;
    });

    new Chart(revenueChartCtx, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: t('revenue'),
            data: revenues,
            backgroundColor: colors,
            borderColor: colors.map(function (c) {
              return c.replace('0.8', '1');
            }),
            borderWidth: 1,
          },
        ],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const segment = segments[context.dataIndex];
                return [
                  t('revenue') +
                    ': ' +
                    segmentData.currency +
                    context.raw.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    }),
                  t('customers') + ': ' + segment.customer_count,
                  t('share') + ': ' + segment.percentage.toFixed(1) + '%',
                ];
              },
            },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            title: {
              display: true,
              text: t('revenue') + ' (' + segmentData.currency + ')',
            },
          },
          y: {
            title: {
              display: true,
              text: t('customerSegment'),
            },
          },
        },
      },
    });
  }

  function displaySegmentInsights(insights) {
    const panel = document.getElementById('segmentInsightsPanel');
    const list = document.getElementById('segmentInsightsList');

    if (!insights || insights.length === 0) {
      panel.style.display = 'none';
      return;
    }

    insights.sort(function (a, b) {
      return a.priority - b.priority;
    });

    let html = '';
    insights.forEach(function (insight) {
      const typeClass = 'insight-' + insight.type;
      html +=
        '<div class="insight-card ' +
        typeClass +
        '">' +
        '<div class="insight-icon"><i class="' +
        insight.icon +
        '"></i></div>' +
        '<div class="insight-content">' +
        '<h4>' +
        insight.title +
        '</h4>' +
        '<p>' +
        insight.description +
        '</p>' +
        '</div>' +
        '</div>';
    });

    list.innerHTML = html;
    panel.style.display = 'block';
  }

  function displayInsights(insights, panelId, listId) {
    const panel = document.getElementById(panelId);
    const list = document.getElementById(listId);

    if (!insights || insights.length === 0) {
      panel.style.display = 'none';
      return;
    }

    insights.sort(function (a, b) {
      return a.priority - b.priority;
    });

    let html = '';
    insights.forEach(function (insight) {
      const typeClass = 'insight-' + insight.type;
      html +=
        '<div class="insight-card ' +
        typeClass +
        '">' +
        '<div class="insight-icon"><i class="' +
        insight.icon +
        '"></i></div>' +
        '<div class="insight-content">' +
        '<h4>' +
        insight.title +
        '</h4>' +
        '<p>' +
        insight.description +
        '</p>' +
        '</div>' +
        '</div>';
    });

    list.innerHTML = html;
    panel.style.display = 'block';
  }

  function renderChurnRiskChart(data) {
    const ctx = document.getElementById('churnRiskChart').getContext('2d');
    const buckets = data.buckets;

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: buckets.map(function (b) {
          return b.label;
        }),
        datasets: [
          {
            label: t('customers'),
            data: buckets.map(function (b) {
              return b.count;
            }),
            backgroundColor: buckets.map(function (b) {
              return b.color;
            }),
            borderColor: buckets.map(function (b) {
              return b.color.replace('0.8', '1');
            }),
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
          tooltip: {
            callbacks: {
              label: function (context) {
                const bucket = buckets[context.dataIndex];
                return [
                  t('customers') + ': ' + bucket.count,
                  t('percentage') + ': ' + bucket.percentage.toFixed(1) + '%',
                ];
              },
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: t('numberOfCustomers'),
            },
          },
          x: {
            title: {
              display: true,
              text: t('probabilityOfReturn'),
            },
          },
        },
      },
    });
  }

  function renderFrequencyHistogram(data) {
    const ctx = document.getElementById('frequencyHistogramChart').getContext('2d');
    const histogram = data.histogram;

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: histogram.map(function (h) {
          return h.label;
        }),
        datasets: [
          {
            label: t('customers'),
            data: histogram.map(function (h) {
              return h.count;
            }),
            backgroundColor: histogram.map(function (h) {
              return h.color;
            }),
            borderColor: histogram.map(function (h) {
              return h.color.replace('0.7', '1');
            }),
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
          tooltip: {
            callbacks: {
              label: function (context) {
                const bucket = histogram[context.dataIndex];
                return [
                  t('customers') + ': ' + bucket.count,
                  t('percentage') + ': ' + bucket.percentage.toFixed(1) + '%',
                ];
              },
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: t('numberOfCustomers'),
            },
          },
          x: {
            title: {
              display: true,
              text: t('totalOrders'),
            },
          },
        },
      },
    });
  }

  function renderPredictionAccuracyChart(data) {
    const ctx = document.getElementById('predictionAccuracyChart').getContext('2d');
    const scatterData = data.scatter_data || [];

    const accuracyLabel =
      t('accuracy') +
      ': ' +
      (data.accuracy_percentage ? data.accuracy_percentage.toFixed(1) : 'N/A') +
      '% | ' +
      t('sample') +
      ': ' +
      (data.sample_size || 0) +
      ' ' +
      t('customersLower');

    new Chart(ctx, {
      type: 'scatter',
      data: {
        datasets: [
          {
            label: t('customers'),
            data: scatterData.map(function (d) {
              return { x: d.predicted, y: d.actual };
            }),
            backgroundColor: 'rgba(0, 124, 186, 0.5)',
            borderColor: 'rgba(0, 124, 186, 1)',
            pointRadius: 5,
          },
          {
            label: t('perfectPredictionLine'),
            data: [
              { x: 0, y: 0 },
              { x: data.max_value || 10, y: data.max_value || 10 },
            ],
            type: 'line',
            borderColor: 'rgba(40, 167, 69, 0.7)',
            borderDash: [5, 5],
            borderWidth: 2,
            fill: false,
            pointRadius: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                if (context.dataset.label === t('customers')) {
                  return (
                    t('predicted') +
                    ': ' +
                    context.parsed.x.toFixed(1) +
                    ', ' +
                    t('actual') +
                    ': ' +
                    context.parsed.y.toFixed(0)
                  );
                }
                return context.dataset.label;
              },
            },
          },
          title: {
            display: true,
            text: accuracyLabel,
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: t('predictedPurchases'),
            },
            min: 0,
          },
          y: {
            title: {
              display: true,
              text: t('actualPurchases'),
            },
            min: 0,
          },
        },
      },
    });
  }

  // ----------------------------------------------------------------
  // Cohort Tab
  // ----------------------------------------------------------------

  function initializeCohortTab() {
    loadCohortData();
    setupCohortEventListeners();
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
          if (data.heatmap_data) {
            renderRetentionHeatmap(data.heatmap_data);
          }
          if (data.retention_insights && data.retention_insights.length > 0) {
            displayRetentionInsights(data.retention_insights);
          }
          if (data.channel_data && data.channel_data.channels) {
            renderLTVByChannelChart(data.channel_data);
          }
          if (data.channel_insights && data.channel_insights.length > 0) {
            displayInsights(data.channel_insights, 'channelInsightsPanel', 'channelInsightsList');
          }
          if (data.category_data && data.category_data.categories) {
            renderLTVByCategoryChart(data.category_data);
          }
          if (data.category_insights && data.category_insights.length > 0) {
            displayInsights(
              data.category_insights,
              'categoryInsightsPanel',
              'categoryInsightsList'
            );
          }
          if (data.revenue_curve_data && data.revenue_curve_data.curves) {
            renderRevenueCurveChart(data.revenue_curve_data);
          }
          if (data.revenue_curve_insights && data.revenue_curve_insights.length > 0) {
            displayInsights(
              data.revenue_curve_insights,
              'revenueCurveInsightsPanel',
              'revenueCurveInsightsList'
            );
          }
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

  function renderRetentionHeatmap(heatmapData) {
    const container = document.getElementById('retentionHeatmapContainer');

    if (!heatmapData || !heatmapData.cohorts || heatmapData.cohorts.length === 0) {
      container.innerHTML =
        '<div class="empty-state"><i class="fas fa-inbox"></i><p>' +
        t('noRetentionData') +
        '</p></div>';
      return;
    }

    let html = '<div class="table-responsive"><table class="table heatmap-table"><thead><tr>';
    html += '<th>' + t('cohortLabel') + '</th>';

    for (let i = 0; i < heatmapData.months.length; i++) {
      html += '<th class="heatmap-header">M' + i + '</th>';
    }
    html += '</tr></thead><tbody>';

    heatmapData.cohorts.forEach(function (cohort, rowIndex) {
      html += '<tr><td class="cohort-label">' + cohort + '</td>';

      heatmapData.data[rowIndex].forEach(function (value) {
        if (value !== null) {
          const colorClass = getHeatmapColor(value);
          const textColor = value > 50 ? '#fff' : '#333';
          html +=
            '<td class="heatmap-cell ' +
            colorClass +
            '" style="color: ' +
            textColor +
            '">' +
            value.toFixed(0) +
            '%</td>';
        } else {
          html += '<td class="heatmap-cell heatmap-null">-</td>';
        }
      });

      html += '</tr>';
    });

    html += '</tbody></table></div>';

    html +=
      '<div class="heatmap-legend">' +
      '<span class="legend-label">' +
      t('low') +
      '</span>' +
      '<div class="legend-gradient"></div>' +
      '<span class="legend-label">' +
      t('high') +
      '</span>' +
      '</div>';

    container.innerHTML = html;
  }

  function getHeatmapColor(value) {
    if (value >= 80) {
      return 'heatmap-excellent';
    }
    if (value >= 60) {
      return 'heatmap-good';
    }
    if (value >= 40) {
      return 'heatmap-moderate';
    }
    if (value >= 20) {
      return 'heatmap-low';
    }
    return 'heatmap-critical';
  }

  function displayRetentionInsights(insights) {
    const panel = document.getElementById('retentionInsightsPanel');
    const list = document.getElementById('retentionInsightsList');

    if (!insights || insights.length === 0) {
      panel.style.display = 'none';
      return;
    }

    insights.sort(function (a, b) {
      return a.priority - b.priority;
    });

    let html = '';
    insights.forEach(function (insight) {
      const typeClass = 'insight-' + insight.type;
      html +=
        '<div class="insight-card ' +
        typeClass +
        '">' +
        '<div class="insight-icon"><i class="' +
        insight.icon +
        '"></i></div>' +
        '<div class="insight-content">' +
        '<h4>' +
        insight.title +
        '</h4>' +
        '<p>' +
        insight.description +
        '</p>' +
        '</div>' +
        '</div>';
    });

    list.innerHTML = html;
    panel.style.display = 'block';
  }

  function renderLTVByChannelChart(data) {
    const ctx = document.getElementById('ltvByChannelChart').getContext('2d');
    const channels = data.channels;

    if (ltvByChannelChart) {
      ltvByChannelChart.destroy();
    }

    if (!channels || channels.length === 0) {
      document.getElementById('ltvByChannelChart').parentElement.innerHTML =
        '<div class="empty-state"><i class="fas fa-inbox"></i><p>' +
        t('noChannelData') +
        '</p></div>';
      return;
    }

    ltvByChannelChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: channels.map(function (c) {
          return c.display_name;
        }),
        datasets: [
          {
            label: t('averageLtv'),
            data: channels.map(function (c) {
              return c.average_ltv;
            }),
            backgroundColor: channels.map(function (c) {
              return c.color;
            }),
            borderColor: channels.map(function (c) {
              return c.color.replace('0.8', '1');
            }),
            borderWidth: 1,
          },
        ],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const channel = channels[context.dataIndex];
                return [
                  t('averageLtv') + ': $' + channel.average_ltv.toFixed(2),
                  t('customers') + ': ' + channel.customer_count,
                  t('totalRevenue') +
                    ': $' +
                    channel.total_revenue.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    }),
                ];
              },
            },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            title: {
              display: true,
              text: t('averageLifetimeValue'),
            },
          },
          y: {
            title: {
              display: true,
              text: t('acquisitionChannel'),
            },
          },
        },
      },
    });
  }

  function renderLTVByCategoryChart(data) {
    const ctx = document.getElementById('ltvByCategoryChart').getContext('2d');
    const categories = data.categories;

    if (ltvByCategoryChart) {
      ltvByCategoryChart.destroy();
    }

    if (!categories || categories.length === 0) {
      document.getElementById('ltvByCategoryChart').parentElement.innerHTML =
        '<div class="empty-state"><i class="fas fa-inbox"></i><p>' +
        t('noCategoryData') +
        '</p></div>';
      return;
    }

    ltvByCategoryChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: categories.map(function (c) {
          return c.display_name;
        }),
        datasets: [
          {
            label: t('averageLtv'),
            data: categories.map(function (c) {
              return c.average_ltv;
            }),
            backgroundColor: categories.map(function (c) {
              return c.color;
            }),
            borderColor: categories.map(function (c) {
              return c.color.replace('0.7', '1');
            }),
            borderWidth: 1,
          },
        ],
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                const category = categories[context.dataIndex];
                return [
                  t('averageLtv') + ': $' + category.average_ltv.toFixed(2),
                  t('customers') + ': ' + category.customer_count,
                  t('totalRevenue') +
                    ': $' +
                    category.total_revenue.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    }),
                ];
              },
            },
          },
        },
        scales: {
          x: {
            beginAtZero: true,
            title: {
              display: true,
              text: t('averageLifetimeValue'),
            },
          },
          y: {
            title: {
              display: true,
              text: t('firstProductCategory'),
            },
          },
        },
      },
    });
  }

  function renderRevenueCurveChart(data) {
    const ctx = document.getElementById('revenueCurveChart').getContext('2d');
    const curves = data.curves;

    if (revenueCurveChart) {
      revenueCurveChart.destroy();
    }

    if (!curves || curves.length === 0) {
      document.getElementById('revenueCurveChart').parentElement.innerHTML =
        '<div class="empty-state"><i class="fas fa-inbox"></i><p>' +
        t('noRevenueCurveData') +
        '</p></div>';
      return;
    }

    const datasets = curves.map(function (curve) {
      return {
        label: curve.cohort,
        data: curve.data.map(function (d) {
          return d.revenue;
        }),
        borderColor: curve.color,
        backgroundColor: curve.color.replace('1)', '0.1)'),
        fill: false,
        tension: 0.3,
      };
    });

    revenueCurveChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.months,
        datasets: datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return (
                  context.dataset.label +
                  ': $' +
                  context.raw.toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                );
              },
            },
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: t('monthsSinceFirstPurchase'),
            },
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: t('cumulativeRevenue'),
            },
          },
        },
      },
    });
  }

  function setupCohortEventListeners() {
    document.querySelectorAll('.chart-tab').forEach(function (tab) {
      tab.addEventListener('click', function () {
        document.querySelectorAll('.chart-tab').forEach(function (t) {
          t.classList.remove('active');
        });
        this.classList.add('active');
        renderComparisonChart(this.dataset.chart);
      });
    });

    document.querySelectorAll('.view-cohort-details').forEach(function (button) {
      button.addEventListener('click', function () {
        const cohortId = this.dataset.cohortId;
        const cohortName = this.dataset.cohortName;
        showRetentionCurve(cohortId, cohortName);
      });
    });

    const rebuildButton = document.getElementById('rebuildCohortsButton');
    if (rebuildButton) {
      rebuildButton.addEventListener('click', async function () {
        if (await AdminModal.confirm(t('rebuildConfirm'))) {
          rebuildCohorts();
        }
      });
    }
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

  function setupModalListeners() {
    // Modal close button via data-action delegation
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

  document.addEventListener('DOMContentLoaded', init);
})();
