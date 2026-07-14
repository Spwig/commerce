/**
 * Visitor Analytics Dashboard — Chart.js initialization and AJAX data loading.
 */
(function () {
  'use strict';

  // Read configuration from JSON data island (CSP-compliant, no inline scripts)
  const configEl = document.getElementById('analytics-config');
  const config = configEl ? JSON.parse(configEl.textContent) : {};

  // Chart instances (for destroy/rebuild on data refresh)
  let trafficChart = null;
  let deviceChart = null;
  let newReturningChart = null;

  // Read chart colors from CSS custom properties (theme-aware for dark mode)
  function getCSSVar(name, fallback) {
    const val = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return val || fallback;
  }

  function hexToRgba(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return 'rgba(' + r + ',' + g + ',' + b + ',' + alpha + ')';
  }

  const primary = getCSSVar('--primary', '#417690');
  const success = getCSSVar('--success-fg', '#28a745');
  const warning = getCSSVar('--warning-fg', '#ffc107');
  const danger = getCSSVar('--error-fg', '#dc3545');
  const muted = getCSSVar('--body-quiet-color', '#999');

  const chartColors = {
    primary: primary,
    primaryLight: hexToRgba(primary, 0.15),
    success: success,
    successLight: hexToRgba(success, 0.15),
    warning: warning,
    danger: danger,
    muted: muted,
    desktop: primary,
    mobile: success,
    tablet: warning,
    unknown: getCSSVar('--border-color', '#ccc'),
  };

  /**
   * Initialize all charts with initial data.
   */
  function initCharts() {
    // Device distribution doughnut
    const devices = config.devices || {};
    initDeviceChart(devices);

    // New vs returning doughnut
    const nvr = config.new_vs_returning || {};
    initNewReturningChart(nvr);

    // Traffic trend — load via AJAX to get time-series data
    loadData(getCurrentPeriod());
  }

  function getCurrentPeriod() {
    const active = document.querySelector('.va-period-btn.active');
    return active ? active.dataset.period : '30_days';
  }

  /**
   * Traffic trend line chart.
   */
  function initTrafficChart(data) {
    const ctx = document.getElementById('trafficTrendChart');
    if (!ctx) return;

    if (trafficChart) trafficChart.destroy();

    trafficChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels || [],
        datasets: [
          {
            label: 'Page Views',
            data: data.views || [],
            borderColor: chartColors.primary,
            backgroundColor: chartColors.primaryLight,
            fill: true,
            tension: 0.3,
            pointRadius: 2,
          },
          {
            label: 'Unique Visitors',
            data: data.visitors || [],
            borderColor: chartColors.success,
            backgroundColor: chartColors.successLight,
            fill: true,
            tension: 0.3,
            pointRadius: 2,
          },
          {
            label: 'Bot Views',
            data: data.bot_views || [],
            borderColor: chartColors.danger,
            backgroundColor: 'transparent',
            borderDash: [5, 5],
            tension: 0.3,
            pointRadius: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: 'index', intersect: false },
        plugins: {
          legend: { position: 'top' },
        },
        scales: {
          y: { beginAtZero: true, ticks: { precision: 0 } },
        },
      },
    });
  }

  /**
   * Device distribution doughnut chart.
   */
  function initDeviceChart(devices) {
    const ctx = document.getElementById('deviceChart');
    if (!ctx) return;

    if (deviceChart) deviceChart.destroy();

    deviceChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Desktop', 'Mobile', 'Tablet', 'Unknown'],
        datasets: [
          {
            data: [
              devices.desktop || 0,
              devices.mobile || 0,
              devices.tablet || 0,
              devices.unknown || 0,
            ],
            backgroundColor: [
              chartColors.desktop,
              chartColors.mobile,
              chartColors.tablet,
              chartColors.unknown,
            ],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' },
        },
      },
    });
  }

  /**
   * New vs returning doughnut chart.
   */
  function initNewReturningChart(data) {
    const ctx = document.getElementById('newReturningChart');
    if (!ctx) return;

    if (newReturningChart) newReturningChart.destroy();

    newReturningChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['New Visitors', 'Returning Visitors'],
        datasets: [
          {
            data: [data.new_visitors || 0, data.returning_visitors || 0],
            backgroundColor: [chartColors.primary, chartColors.success],
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom' },
        },
      },
    });
  }

  /**
   * Fetch fresh data for the selected period and update all charts/tables.
   */
  function loadData(period) {
    const url = config.data_url + '?period=' + encodeURIComponent(period);

    fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      credentials: 'same-origin',
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        // Update KPI cards
        updateKPI('kpi-total-views', data.overview.total_views);
        updateKPI('kpi-unique-visitors', data.overview.unique_visitors);
        updateKPI('kpi-bounce-rate', data.overview.bounce_rate + '%');
        updateKPI('kpi-avg-pages', data.overview.avg_pages_per_session);
        updateKPI('kpi-bot-pct', data.bot_summary.bot_pct + '%');

        // Update charts
        if (data.traffic_trends) initTrafficChart(data.traffic_trends);
        if (data.devices) initDeviceChart(data.devices);
        if (data.new_vs_returning) initNewReturningChart(data.new_vs_returning);

        // Update tables
        if (data.top_pages)
          updateTable('top-pages-table', data.top_pages, [
            'url_path',
            'views',
            'unique_visitors',
            'entries',
          ]);
        if (data.campaigns)
          updateTable('campaigns-table', data.campaigns, [
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'visitors',
          ]);
        if (data.geographic)
          updateTable('geo-table', data.geographic, ['resolved_country', 'visitors', 'page_views']);
        if (data.referrers) updateTable('referrers-table', data.referrers, ['referrer', 'count']);
        if (data.landing_pages)
          updateTable('landing-pages-table', data.landing_pages, [
            'url_path',
            'entries',
            'unique_visitors',
          ]);
      })
      .catch(function (err) {
        console.error('Analytics data load failed:', err);
      });
  }

  function updateKPI(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
  }

  function updateTable(tableId, rows, columns) {
    const table = document.getElementById(tableId);
    if (!table) return;
    const tbody = table.querySelector('tbody');
    if (!tbody) return;

    if (!rows.length) {
      tbody.innerHTML =
        '<tr><td colspan="' +
        columns.length +
        '" class="va-empty">No data for this period</td></tr>';
      return;
    }

    tbody.innerHTML = rows
      .map(function (row) {
        return (
          '<tr>' +
          columns
            .map(function (col) {
              const val = row[col] !== null && row[col] !== undefined ? row[col] : '-';
              const cls =
                col === 'url_path' || col === 'referrer'
                  ? ' class="font-monospace va-url-cell"'
                  : '';
              return '<td' + cls + '>' + escapeHtml(String(val)) + '</td>';
            })
            .join('') +
          '</tr>'
        );
      })
      .join('');
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  /**
   * Period selector click handler.
   */
  function bindPeriodSelector() {
    document.querySelectorAll('.va-period-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.va-period-btn').forEach(function (b) {
          b.classList.remove('active');
        });
        btn.classList.add('active');
        loadData(btn.dataset.period);
      });
    });
  }

  // Init on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      initCharts();
      bindPeriodSelector();
    });
  } else {
    initCharts();
    bindPeriodSelector();
  }
})();
