/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Reviews Dashboard charts (Chart.js).
 * Reads data from the #reviews-dashboard-data JSON block (CSP-safe, no inline JS).
 */
(function () {
  'use strict';

  const PALETTE = [
    '#667eea',
    '#10b981',
    '#f59e0b',
    '#ef4444',
    '#3498db',
    '#9b59b6',
    '#1abc9c',
    '#e67e22',
  ];

  function init() {
    const dataEl = document.getElementById('reviews-dashboard-data');
    if (!dataEl) return;

    let data;
    try {
      data = JSON.parse(dataEl.textContent);
    } catch (e) {
      console.error('Error parsing reviews dashboard data:', e);
      return;
    }

    if (typeof Chart === 'undefined') {
      console.error('Chart.js is not loaded!');
      return;
    }

    const isDark = document.body.getAttribute('data-theme') === 'dark';
    const textColor = isDark ? '#e8e8e8' : '#333333';
    const gridColor = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;

    initRatingDist(data.ratingDistribution || [], textColor, gridColor);
    initReviewsSeries(data.reviewsSeries || [], data.translations || {}, textColor, gridColor);
    initChannel(data.channelBreakdown || []);
  }

  function initRatingDist(rows, textColor, gridColor) {
    const el = document.getElementById('ratingDistChart');
    if (!el || !rows.length) return;
    new Chart(el, {
      type: 'bar',
      data: {
        labels: rows.map(function (r) {
          return r.rating + '★';
        }),
        datasets: [
          {
            data: rows.map(function (r) {
              return r.count;
            }),
            backgroundColor: ['#ef4444', '#f59e0b', '#eab308', '#84cc16', '#10b981'],
            borderRadius: 6,
            borderSkipped: false,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { precision: 0, color: textColor },
            grid: { color: gridColor },
          },
          x: { grid: { display: false }, ticks: { color: textColor } },
        },
      },
    });
  }

  function initReviewsSeries(rows, translations, textColor, gridColor) {
    const el = document.getElementById('reviewsSeriesChart');
    if (!el || !rows.length) return;
    new Chart(el, {
      type: 'line',
      data: {
        labels: rows.map(function (d) {
          return new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        }),
        datasets: [
          {
            label: translations.reviews || 'Reviews',
            data: rows.map(function (d) {
              return d.count;
            }),
            borderColor: '#667eea',
            backgroundColor: 'rgba(102,126,234,0.1)',
            fill: true,
            tension: 0.4,
            pointRadius: 3,
            pointHoverRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { precision: 0, color: textColor },
            grid: { color: gridColor },
          },
          x: {
            grid: { display: false },
            ticks: { color: textColor, maxRotation: 45, minRotation: 45 },
          },
        },
      },
    });
  }

  function initChannel(rows) {
    const el = document.getElementById('channelChart');
    if (!el || !rows.length) return;
    new Chart(el, {
      type: 'doughnut',
      data: {
        labels: rows.map(function (r) {
          return r.label || r.channel;
        }),
        datasets: [
          {
            data: rows.map(function (r) {
              return r.count;
            }),
            backgroundColor: rows.map(function (r, i) {
              return PALETTE[i % PALETTE.length];
            }),
            borderWidth: 0,
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

  document.addEventListener('DOMContentLoaded', init);
})();
