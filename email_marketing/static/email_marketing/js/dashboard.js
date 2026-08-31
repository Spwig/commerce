/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  var el = document.getElementById('em-dash-data');
  if (!el || typeof Chart === 'undefined') return;

  var data;
  try {
    data = JSON.parse(el.textContent);
  } catch (e) {
    return;
  }

  // Read the admin accent colour so charts match the current theme.
  var css = getComputedStyle(document.documentElement);
  var accent = (css.getPropertyValue('--link-fg') || '#417690').trim();
  var muted = (css.getPropertyValue('--body-quiet-color') || '#8a8a8a').trim();
  var grid = (css.getPropertyValue('--border-color') || 'rgba(128,128,128,0.2)').trim();

  function baseOptions() {
    return {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: {
          ticks: { color: muted, maxRotation: 0, autoSkip: true, maxTicksLimit: 8 },
          grid: { display: false },
        },
        y: { beginAtZero: true, ticks: { color: muted, precision: 0 }, grid: { color: grid } },
      },
    };
  }

  function hexToRgba(hex, a) {
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

  var growthCanvas = document.getElementById('emGrowthChart');
  if (growthCanvas && data.growth) {
    new Chart(growthCanvas, {
      type: 'line',
      data: {
        labels: data.growth.labels,
        datasets: [
          {
            data: data.growth.counts,
            borderColor: accent,
            backgroundColor: hexToRgba(accent, 0.12),
            fill: true,
            tension: 0.35,
            pointRadius: 0,
            borderWidth: 2,
          },
        ],
      },
      options: baseOptions(),
    });
  }

  var sendsCanvas = document.getElementById('emSendsChart');
  if (sendsCanvas && data.sends) {
    new Chart(sendsCanvas, {
      type: 'bar',
      data: {
        labels: data.sends.labels,
        datasets: [
          { data: data.sends.counts, backgroundColor: hexToRgba(accent, 0.65), borderRadius: 3 },
        ],
      },
      options: baseOptions(),
    });
  }
})();
