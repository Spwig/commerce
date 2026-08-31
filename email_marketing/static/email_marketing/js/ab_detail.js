/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* A/B test results — a per-variant open/click-rate comparison bar chart.
   Mirrors dashboard.js: json_script data-in, theme-token colours, CSP-safe. */
(function () {
  'use strict';

  var el = document.getElementById('ab-chart-data');
  var canvas = document.getElementById('ab-compare-chart');
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

  function rgba(hex, a) {
    var m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (!m) return 'rgba(65,118,144,' + a + ')';
    return (
      'rgba(' +
      parseInt(m[1], 16) +
      ',' +
      parseInt(m[2], 16) +
      ',' +
      parseInt(m[3], 16) +
      ',' +
      a +
      ')'
    );
  }

  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: data.labels.map(function (l) {
        return 'Variant ' + l;
      }),
      datasets: [
        {
          label: 'Open rate',
          data: data.open_rate,
          backgroundColor: rgba(accent, 0.65),
          borderRadius: 3,
        },
        {
          label: 'Click rate',
          data: data.click_rate,
          backgroundColor: rgba('#16a34a', 0.65),
          borderRadius: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: true, labels: { color: muted } } },
      scales: {
        x: { ticks: { color: muted }, grid: { display: false } },
        y: {
          beginAtZero: true,
          ticks: {
            color: muted,
            callback: function (v) {
              return v + '%';
            },
          },
          grid: { color: grid },
        },
      },
    },
  });
})();
