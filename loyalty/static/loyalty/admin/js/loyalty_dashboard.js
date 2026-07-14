/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let enrollmentData = [];
  let pointsTrendData = [];
  let tierDistributionData = [];
  let translations = {};

  function init() {
    const dataEl = document.getElementById('loyalty-dashboard-data');
    if (dataEl) {
      try {
        const data = JSON.parse(dataEl.textContent);
        enrollmentData = data.enrollmentData || [];
        pointsTrendData = data.pointsTrendData || [];
        tierDistributionData = data.tierDistributionData || [];
        translations = data.translations || {};
      } catch (e) {
        console.error('Error parsing loyalty dashboard data:', e);
      }
    }

    if (typeof Chart === 'undefined') {
      console.error('Chart.js is not loaded!');
      return;
    }

    const isDarkTheme = document.body.getAttribute('data-theme') === 'dark';
    const textColor = isDarkTheme ? '#e8e8e8' : '#333333';
    const gridColor = isDarkTheme ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';

    Chart.defaults.color = textColor;
    Chart.defaults.borderColor = gridColor;

    initEnrollmentChart(textColor, gridColor);
    initPointsTrendChart(textColor, gridColor);
    initTierDistributionChart(gridColor);
  }

  function initEnrollmentChart(textColor, gridColor) {
    const enrollmentCtx = document.getElementById('enrollmentChart');
    if (!enrollmentCtx || !enrollmentData || enrollmentData.length === 0) {
      return;
    }

    try {
      new Chart(enrollmentCtx, {
        type: 'line',
        data: {
          labels: enrollmentData.map(function (d) {
            return new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          }),
          datasets: [
            {
              label: translations.newMembers || 'New Members',
              data: enrollmentData.map(function (d) {
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
                  return context.parsed.y + ' new member' + (context.parsed.y !== 1 ? 's' : '');
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
    } catch (error) {
      console.error('Error creating enrollment chart:', error);
    }
  }

  function initPointsTrendChart(textColor, gridColor) {
    const pointsTrendCtx = document.getElementById('pointsTrendChart');
    if (!pointsTrendCtx || !pointsTrendData || pointsTrendData.length === 0) {
      return;
    }

    try {
      new Chart(pointsTrendCtx, {
        type: 'line',
        data: {
          labels: pointsTrendData.map(function (d) {
            return new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
          }),
          datasets: [
            {
              label: translations.earned || 'Earned',
              data: pointsTrendData.map(function (d) {
                return d.earned;
              }),
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              fill: true,
              tension: 0.4,
              pointRadius: 3,
              pointHoverRadius: 6,
              pointBackgroundColor: '#10b981',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointHoverBackgroundColor: '#10b981',
              pointHoverBorderColor: '#fff',
            },
            {
              label: translations.redeemed || 'Redeemed',
              data: pointsTrendData.map(function (d) {
                return d.redeemed;
              }),
              borderColor: '#ef4444',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              fill: true,
              tension: 0.4,
              pointRadius: 3,
              pointHoverRadius: 6,
              pointBackgroundColor: '#ef4444',
              pointBorderColor: '#fff',
              pointBorderWidth: 2,
              pointHoverBackgroundColor: '#ef4444',
              pointHoverBorderColor: '#fff',
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: {
              display: true,
              position: 'top',
              labels: { usePointStyle: true, padding: 15, color: textColor },
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleColor: '#fff',
              bodyColor: '#fff',
              borderColor: '#667eea',
              borderWidth: 1,
              padding: 12,
              usePointStyle: true,
              callbacks: {
                label: function (context) {
                  const value = context.parsed.y.toLocaleString();
                  return context.dataset.label + ': ' + value + ' pts';
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0,
                color: textColor,
                callback: function (value) {
                  return value.toLocaleString();
                },
              },
              grid: { color: gridColor },
            },
            x: {
              ticks: { color: textColor, maxRotation: 45, minRotation: 45 },
              grid: { display: false },
            },
          },
        },
      });
    } catch (error) {
      console.error('Error creating points trend chart:', error);
    }
  }

  function initTierDistributionChart(gridColor) {
    const tierDistCtx = document.getElementById('tierDistributionChart');
    if (!tierDistCtx || !tierDistributionData || tierDistributionData.length === 0) {
      return;
    }

    try {
      new Chart(tierDistCtx, {
        type: 'bar',
        data: {
          labels: tierDistributionData.map(function (d) {
            return d.name;
          }),
          datasets: [
            {
              label: translations.members || 'Members',
              data: tierDistributionData.map(function (d) {
                return d.count;
              }),
              backgroundColor: tierDistributionData.map(function (d) {
                return d.color;
              }),
              borderColor: tierDistributionData.map(function (d) {
                return d.color;
              }),
              borderWidth: 2,
              borderRadius: 6,
              borderSkipped: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: { display: false },
            tooltip: {
              callbacks: {
                label: function (context) {
                  return context.dataset.label + ': ' + context.parsed.y + ' members';
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { precision: 0 },
              grid: { color: gridColor },
            },
            x: {
              grid: { display: false },
            },
          },
        },
      });
    } catch (error) {
      console.error('Error creating tier distribution chart:', error);
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
