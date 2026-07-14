/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Affiliate merchant dashboard — Chart.js initialisation.
 * Chart data is passed via <script type="application/json" id="revenue-chart-data">.
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initRevenueChart();
  });

  function initRevenueChart() {
    const canvas = document.getElementById('revenueChart');
    if (!canvas) return;

    const dataEl = document.getElementById('revenue-chart-data');
    if (!dataEl) return;

    let config;
    try {
      config = JSON.parse(dataEl.textContent);
    } catch (e) {
      return;
    }

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: config.labels,
        datasets: [
          {
            label: config.label,
            data: config.data,
            borderColor: '#28a745',
            backgroundColor: 'rgba(40, 167, 69, 0.1)',
            borderWidth: 2,
            fill: true,
            tension: 0.4,
            pointRadius: 4,
            pointHoverRadius: 6,
            pointBackgroundColor: '#28a745',
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            titleFont: { size: 14, weight: 'bold' },
            bodyFont: { size: 13 },
            callbacks: {
              label: function (context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                label += '$' + context.parsed.y.toFixed(2);
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
                return '$' + value.toFixed(0);
              },
            },
            grid: { color: 'rgba(0, 0, 0, 0.05)' },
          },
          x: {
            grid: { display: false },
          },
        },
      },
    });
  }
})();
