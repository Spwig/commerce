/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Referrals Dashboard
 *
 * Renders Chart.js charts for referrals trend, conversion funnel, and reward distribution.
 * Reads data from the #referrals-dashboard-data JSON island.
 */

(function () {
  'use strict';

  function initReferralsDashboard() {
    const dataEl = document.getElementById('referrals-dashboard-data');
    if (!dataEl) return;

    const cfg = JSON.parse(dataEl.textContent);
    const referralsTrendData = cfg.referralsTrendData;
    const funnelData = cfg.funnelData;
    const rewardDistributionData = cfg.rewardDistributionData;
    const i18n = cfg.i18n;

    if (typeof Chart === 'undefined') {
      console.error('Chart.js is not loaded!');
      return;
    }

    // Theme detection
    const isDarkTheme = document.body.getAttribute('data-theme') === 'dark';
    const textColor = isDarkTheme ? '#e8e8e8' : '#333333';
    const gridColor = isDarkTheme ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';

    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;

    // 1. Referrals Trend Chart (Line Chart)
    const referralsTrendCtx = document.getElementById('referralsTrendChart');
    if (referralsTrendCtx && referralsTrendData && referralsTrendData.length > 0) {
      new Chart(referralsTrendCtx, {
        type: 'line',
        data: {
          labels: referralsTrendData.map(function (d) {
            return new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          }),
          datasets: [
            {
              label: i18n.referrals,
              data: referralsTrendData.map(function (d) {
                return d.count;
              }),
              borderColor: '#667eea',
              backgroundColor: 'rgba(102, 126, 234, 0.1)',
              fill: true,
              tension: 0.4,
              pointRadius: 3,
              pointHoverRadius: 6,
              pointBackgroundColor: '#667eea',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointHoverBackgroundColor: '#667eea',
              pointHoverBorderColor: '#fff',
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: '#667eea',
              borderWidth: 1,
              padding: 12,
              displayColors: false,
              callbacks: {
                label: function (context) {
                  const word =
                    context.parsed.y !== 1
                      ? i18n.referral_plural || 'referrals'
                      : i18n.referral_singular || 'referral';
                  return context.parsed.y + ' ' + word;
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { precision: 0, color: textColor },
              grid: { color: gridColor },
            },
            x: {
              ticks: { color: textColor, maxRotation: 45, minRotation: 45 },
              grid: { display: false },
            },
          },
        },
      });
    }

    // 2. Conversion Funnel Chart (Bar Chart)
    const funnelCtx = document.getElementById('conversionFunnelChart');
    if (funnelCtx && funnelData) {
      new Chart(funnelCtx, {
        type: 'bar',
        data: {
          labels: [i18n.clicks, i18n.signups, i18n.orders, i18n.approved],
          datasets: [
            {
              label: i18n.count,
              data: [
                funnelData.clicks || 0,
                funnelData.signups || 0,
                funnelData.orders || 0,
                funnelData.approved || 0,
              ],
              backgroundColor: [
                'rgba(102, 126, 234, 0.8)',
                'rgba(118, 75, 162, 0.8)',
                'rgba(237, 100, 166, 0.8)',
                'rgba(52, 211, 153, 0.8)',
              ],
              borderColor: ['#667eea', '#764ba2', '#ed64a6', '#34d399'],
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderWidth: 1,
              padding: 12,
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { precision: 0, color: textColor },
              grid: { color: gridColor },
            },
            x: {
              ticks: { color: textColor },
              grid: { display: false },
            },
          },
        },
      });
    }

    // 3. Reward Distribution Chart (Doughnut Chart)
    const rewardDistCtx = document.getElementById('rewardDistributionChart');
    if (rewardDistCtx && rewardDistributionData && rewardDistributionData.length > 0) {
      new Chart(rewardDistCtx, {
        type: 'doughnut',
        data: {
          labels: rewardDistributionData.map(function (d) {
            return d.name;
          }),
          datasets: [
            {
              data: rewardDistributionData.map(function (d) {
                return d.count;
              }),
              backgroundColor: rewardDistributionData.map(function (d) {
                return d.color;
              }),
              borderColor: isDarkTheme ? '#1f1f1f' : '#ffffff',
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              display: true,
              position: 'right',
              labels: {
                usePointStyle: true,
                padding: 15,
                color: textColor,
                font: { size: 12 },
              },
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderWidth: 1,
              padding: 12,
              callbacks: {
                label: function (context) {
                  const total = context.dataset.data.reduce(function (a, b) {
                    return a + b;
                  }, 0);
                  const percentage = ((context.parsed / total) * 100).toFixed(1);
                  return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                },
              },
            },
          },
        },
      });
    }

    // Smooth scroll for settings link
    document.querySelectorAll('.scroll-link').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', initReferralsDashboard);
})();
