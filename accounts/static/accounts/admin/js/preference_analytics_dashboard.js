/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let translations = {};
  let chartData = {};
  const charts = {};

  function init() {
    const dataEl = document.getElementById('preference-analytics-data');
    if (dataEl) {
      try {
        const data = JSON.parse(dataEl.textContent);
        translations = data.translations || {};
        chartData = data.chartData || {};
      } catch (e) {}
    }

    const periodSelect = document.getElementById('period');
    if (periodSelect) {
      periodSelect.addEventListener('change', toggleCustomDates);
    }

    initCharts();

    // Re-render charts when the admin theme is switched so their axis/grid/
    // legend colours follow the light/dark tokens. We never track theme state
    // client-side — we only react to the core's admin-theme-changed event.
    document.addEventListener('admin-theme-changed', initCharts);
  }

  function toggleCustomDates() {
    const period = document.getElementById('period');
    const customDates = document.getElementById('custom-dates');
    const customDatesEnd = document.getElementById('custom-dates-end');

    if (!period) {
      return;
    }

    if (period.value === 'custom') {
      if (customDates) {
        customDates.classList.remove('hidden');
      }
      if (customDatesEnd) {
        customDatesEnd.classList.remove('hidden');
      }
    } else {
      if (customDates) {
        customDates.classList.add('hidden');
      }
      if (customDatesEnd) {
        customDatesEnd.classList.add('hidden');
      }
    }
  }

  // Resolve the admin theme tokens to concrete colours for Chart.js, which
  // cannot read CSS custom properties itself.
  function themeColors() {
    const styles = getComputedStyle(document.documentElement);
    const read = function (name, fallback) {
      const value = styles.getPropertyValue(name).trim();
      return value || fallback;
    };
    return {
      text: read('--body-fg', '#1a1a1a'),
      muted: read('--body-quiet-color', '#5f6368'),
      grid: read('--border-color', '#e0e0e0'),
      accent: read('--link-color', '#1a73e8'),
    };
  }

  function initCharts() {
    if (typeof Chart === 'undefined') {
      return;
    }

    const colors = themeColors();

    // Rebuild from scratch so a theme switch fully re-colours the canvas.
    Object.keys(charts).forEach(function (key) {
      if (charts[key]) {
        charts[key].destroy();
        delete charts[key];
      }
    });

    const trendData = chartData.optInTrend || [];
    const trendCtx = document.getElementById('optInTrendChart');
    if (trendCtx && trendData.length > 0) {
      charts.trend = new Chart(trendCtx, {
        type: 'line',
        data: {
          labels: trendData.map(function (item) {
            return item.date;
          }),
          datasets: [
            {
              label: translations.newOptIns || 'New Opt-Ins',
              data: trendData.map(function (item) {
                return item.count;
              }),
              borderColor: colors.accent,
              backgroundColor: 'rgba(26, 115, 232, 0.1)',
              tension: 0.4,
              fill: true,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
          },
          scales: {
            x: {
              ticks: { color: colors.muted },
              grid: { color: colors.grid },
            },
            y: {
              beginAtZero: true,
              ticks: { precision: 0, color: colors.muted },
              grid: { color: colors.grid },
            },
          },
        },
      });
    }

    const appBreakdown = chartData.appBreakdown || {};
    const pieCtx = document.getElementById('appBreakdownChart');
    if (pieCtx) {
      charts.breakdown = new Chart(pieCtx, {
        type: 'doughnut',
        data: {
          labels: [
            translations.blog || 'Blog',
            translations.loyalty || 'Loyalty',
            translations.referrals || 'Referrals',
            translations.affiliate || 'Affiliate',
          ],
          datasets: [
            {
              data: [
                appBreakdown.blog || 0,
                appBreakdown.loyalty || 0,
                appBreakdown.referrals || 0,
                appBreakdown.affiliate || 0,
              ],
              backgroundColor: ['#1a73e8', '#10b981', '#f59e0b', '#8b5cf6'],
              borderColor: colors.grid,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom', labels: { color: colors.text } },
          },
        },
      });
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
