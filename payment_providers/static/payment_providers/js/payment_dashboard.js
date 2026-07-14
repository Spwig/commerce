/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Payment Dashboard JavaScript
 * Handles chart rendering, filters, and dashboard interactivity
 */

(function () {
  'use strict';

  // Read dashboard data from JSON data island
  let dashboardData = {};
  const dataIslandEl = document.getElementById('payment-dashboard-data');
  if (dataIslandEl) {
    try {
      dashboardData = JSON.parse(dataIslandEl.textContent);
    } catch (e) {
      console.error('Failed to parse payment-dashboard-data:', e);
    }
  }

  // Get current language for URL building
  const currentLang = document.documentElement.lang || 'en';

  // Chart instances
  let revenueChart = null;
  let statusChart = null;
  let paymentMethodsChart = null;

  /**
   * Initialize the dashboard
   */
  function initDashboard() {
    // Initialize charts
    initRevenueChart();
    initStatusChart();
    initPaymentMethodsChart();

    // Setup event listeners
    setupFilters();
    setupJumpToNav();
    setupGroupingButtons();
  }

  /**
   * Initialize Revenue Over Time Chart
   */
  function initRevenueChart() {
    const ctx = document.getElementById('revenue-chart-canvas');
    if (!ctx) return;

    const data = dashboardData.revenueOverTime;
    const compareEnabled = dashboardData.compareEnabled;

    const datasets = [
      {
        label: 'Revenue',
        data: data.current.revenue,
        borderColor: 'rgb(102, 126, 234)',
        backgroundColor: 'rgba(102, 126, 234, 0.1)',
        tension: 0.4,
        fill: true,
      },
    ];

    if (compareEnabled && data.previous) {
      datasets.push({
        label: 'Previous Period Revenue',
        data: data.previous.revenue,
        borderColor: 'rgb(153, 153, 153)',
        backgroundColor: 'rgba(153, 153, 153, 0.05)',
        borderDash: [5, 5],
        tension: 0.4,
        fill: false,
      });
    }

    revenueChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: compareEnabled,
            position: 'top',
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            callbacks: {
              label: function (context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                label += formatCurrency(context.parsed.y);
                return label;
              },
            },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function (value) {
                return formatCurrency(value);
              },
            },
          },
        },
      },
    });
  }

  /**
   * Initialize Transaction Status Pie Chart
   */
  function initStatusChart() {
    const ctx = document.getElementById('status-chart');
    if (!ctx) return;

    const data = dashboardData.transactionByStatus;
    if (!data || data.length === 0) return;

    const statusColors = {
      succeeded: '#28a745',
      authorized: '#17a2b8',
      failed: '#dc3545',
      pending: '#ffc107',
      refunded: '#6c757d',
    };

    const labels = data.map(item => item.status.charAt(0).toUpperCase() + item.status.slice(1));
    const counts = data.map(item => item.count);
    const colors = data.map(item => statusColors[item.status] || '#6c757d');

    statusChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [
          {
            data: counts,
            backgroundColor: colors,
            borderWidth: 2,
            borderColor: '#fff',
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
                const label = context.label || '';
                const value = context.parsed;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `${label}: ${value} (${percentage}%)`;
              },
            },
          },
        },
      },
    });
  }

  /**
   * Initialize Payment Methods Distribution Chart
   */
  function initPaymentMethodsChart() {
    const ctx = document.getElementById('payment-methods-chart');
    if (!ctx) return;

    const data = dashboardData.paymentMethods;
    if (!data || data.length === 0) return;

    const methodColors = ['#667eea', '#5ee7df', '#ffa751', '#f093fb', '#28a745', '#ff6b6b'];

    const labels = data.map(item => item.payment_method_type || 'Unknown');
    const counts = data.map(item => item.count);
    const colors = data.map((_, index) => methodColors[index % methodColors.length]);

    paymentMethodsChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [
          {
            data: counts,
            backgroundColor: colors,
            borderWidth: 2,
            borderColor: '#fff',
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
                const label = context.label || '';
                const value = context.parsed;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(1);
                return `${label}: ${value} (${percentage}%)`;
              },
            },
          },
        },
      },
    });
  }

  /**
   * Setup filter event listeners
   */
  function setupFilters() {
    const periodSelect = document.getElementById('period-select');
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    const compareToggle = document.getElementById('compare-toggle');
    const refreshButton = document.getElementById('refresh-dashboard');
    const customDateRange = document.querySelector('.custom-date-range');

    // Show/hide custom date range
    if (periodSelect) {
      periodSelect.addEventListener('change', function () {
        if (customDateRange) {
          if (this.value === 'custom') {
            customDateRange.classList.remove('custom-date-display-none');
            customDateRange.classList.add('custom-date-display-flex');
          } else {
            customDateRange.classList.remove('custom-date-display-flex');
            customDateRange.classList.add('custom-date-display-none');
          }
        }
      });
    }

    // Refresh dashboard
    if (refreshButton) {
      refreshButton.addEventListener('click', function () {
        refreshDashboard();
      });
    }

    // Enter key on date inputs
    if (startDate) {
      startDate.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          refreshDashboard();
        }
      });
    }
    if (endDate) {
      endDate.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          refreshDashboard();
        }
      });
    }
  }

  /**
   * Setup jump to navigation
   */
  function setupJumpToNav() {
    const jumpToSelect = document.getElementById('jump-to-select');
    if (!jumpToSelect) return;

    jumpToSelect.addEventListener('change', function () {
      const sectionId = this.value;
      if (!sectionId) return;

      const section = document.getElementById(sectionId);
      if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }

      // Reset select
      this.value = '';
    });
  }

  /**
   * Setup grouping buttons
   */
  function setupGroupingButtons() {
    const groupingButtons = document.querySelectorAll('.grouping-btn');
    groupingButtons.forEach(button => {
      button.addEventListener('click', function () {
        const grouping = this.dataset.grouping;
        refreshDashboard(grouping);
      });
    });
  }

  /**
   * Refresh dashboard with current filter settings
   */
  function refreshDashboard(grouping = null) {
    const periodSelect = document.getElementById('period-select');
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    const compareToggle = document.getElementById('compare-toggle');

    // Build query parameters
    const params = new URLSearchParams();
    if (periodSelect) {
      params.append('period', periodSelect.value);
    }
    if (compareToggle) {
      params.append('compare', compareToggle.checked ? 'true' : 'false');
    }
    if (periodSelect && periodSelect.value === 'custom') {
      if (startDate && startDate.value) {
        params.append('start_date', startDate.value);
      }
      if (endDate && endDate.value) {
        params.append('end_date', endDate.value);
      }
    }
    if (grouping) {
      params.append('grouping', grouping);
    }

    // Show loading state
    const refreshButton = document.getElementById('refresh-dashboard');
    if (refreshButton) {
      refreshButton.disabled = true;
      const originalHTML = refreshButton.innerHTML;
      refreshButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';

      // Reload page with new parameters
      window.location.href = `/${currentLang}/admin/payment-providers/dashboard/?${params.toString()}`;
    } else {
      // Fallback if button not found
      window.location.href = `/${currentLang}/admin/payment-providers/dashboard/?${params.toString()}`;
    }
  }

  /**
   * Format currency value
   */
  function formatCurrency(value) {
    const currency = dashboardData.defaultCurrency || window.__shopCurrency || 'USD';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 2,
    }).format(value);
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
  } else {
    initDashboard();
  }
})();
