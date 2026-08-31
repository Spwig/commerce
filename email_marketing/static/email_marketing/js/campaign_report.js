/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* Per-campaign engagement time-series (sends / unique opens / unique clicks).
   Reads the json_script payload emitted by the report page; CSP-safe (no inline JS). */
(function () {
  'use strict';

  var el = document.getElementById('em-report-series');
  var canvas = document.getElementById('emReportChart');
  if (!el || !canvas || typeof Chart === 'undefined') return;

  var data;
  try {
    data = JSON.parse(el.textContent);
  } catch (e) {
    return;
  }
  if (!data.labels || !data.labels.length) return;

  var css = getComputedStyle(document.documentElement);
  var accent = (css.getPropertyValue('--link-fg') || '#417690').trim();
  var muted = (css.getPropertyValue('--body-quiet-color') || '#8a8a8a').trim();
  var grid = (css.getPropertyValue('--border-color') || 'rgba(128,128,128,0.2)').trim();
  var body = (css.getPropertyValue('--body-fg') || '#333').trim();

  var SENDS = '#8a8a8a'; // grey
  var OPENS = accent; // theme accent
  var CLICKS = '#2e7d32'; // success green

  function series(label, values, color) {
    return {
      label: label,
      data: values,
      borderColor: color,
      backgroundColor: color,
      fill: false,
      tension: 0.35,
      pointRadius: 0,
      borderWidth: 2,
    };
  }

  var legend = data.legend || {};
  new Chart(canvas, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [
        series(legend.sends || 'Sent', data.sends, SENDS),
        series(legend.opens || 'Opened', data.opens, OPENS),
        series(legend.clicks || 'Clicked', data.clicks, CLICKS),
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: true, position: 'bottom', labels: { color: body, boxWidth: 12 } },
      },
      scales: {
        x: {
          ticks: { color: muted, maxRotation: 0, autoSkip: true, maxTicksLimit: 8 },
          grid: { display: false },
        },
        y: { beginAtZero: true, ticks: { color: muted, precision: 0 }, grid: { color: grid } },
      },
    },
  });
})();
