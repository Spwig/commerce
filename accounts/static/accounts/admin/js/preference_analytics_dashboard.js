/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let translations = {};
  let chartData = {};

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

  function initCharts() {
    if (typeof Chart === 'undefined') {
      return;
    }

    const trendData = chartData.optInTrend || [];
    const trendCtx = document.getElementById('optInTrendChart');
    if (trendCtx && trendData.length > 0) {
      new Chart(trendCtx, {
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
              borderColor: '#417690',
              backgroundColor: 'rgba(65, 118, 144, 0.1)',
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
            y: {
              beginAtZero: true,
              ticks: { precision: 0 },
            },
          },
        },
      });
    }

    const appBreakdown = chartData.appBreakdown || {};
    const pieCtx = document.getElementById('appBreakdownChart');
    if (pieCtx) {
      new Chart(pieCtx, {
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
              backgroundColor: ['#417690', '#10b981', '#f59e0b', '#8b5cf6'],
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom' } },
        },
      });
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
