/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var configEl = document.getElementById('digital-analytics-config');
    if (!configEl) return;
    var config = JSON.parse(configEl.textContent);

    document.addEventListener('DOMContentLoaded', function () {
        // Download Trends Chart
        var downloadTrendsEl = document.getElementById('downloadTrendsChart');
        if (downloadTrendsEl) {
            new Chart(downloadTrendsEl.getContext('2d'), {
                type: 'line',
                data: {
                    labels: config.downloadTrendsLabels,
                    datasets: [{
                        label: config.strings.downloads,
                        data: config.downloadTrendsCounts,
                        borderColor: 'rgb(65, 118, 144)',
                        backgroundColor: 'rgba(65, 118, 144, 0.1)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        }

        // License Stats Doughnut Chart
        var licenseStatsEl = document.getElementById('licenseStatsChart');
        if (licenseStatsEl) {
            new Chart(licenseStatsEl.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: [config.strings.active, config.strings.expired, config.strings.revoked, config.strings.suspended],
                    datasets: [{
                        data: [
                            config.licenseStats.active,
                            config.licenseStats.expired,
                            config.licenseStats.revoked,
                            config.licenseStats.suspended
                        ],
                        backgroundColor: [
                            'rgb(40, 167, 69)',
                            'rgb(220, 53, 69)',
                            'rgb(108, 117, 125)',
                            'rgb(255, 193, 7)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        }

        // Download Stats Doughnut Chart
        var downloadStatsEl = document.getElementById('downloadStatsChart');
        if (downloadStatsEl) {
            new Chart(downloadStatsEl.getContext('2d'), {
                type: 'doughnut',
                data: {
                    labels: [config.strings.completed, config.strings.failed, config.strings.inProgress, config.strings.pending],
                    datasets: [{
                        data: [
                            config.downloadStats.completed,
                            config.downloadStats.failed,
                            config.downloadStats.inProgress,
                            config.downloadStats.pending
                        ],
                        backgroundColor: [
                            'rgb(40, 167, 69)',
                            'rgb(220, 53, 69)',
                            'rgb(23, 162, 184)',
                            'rgb(255, 193, 7)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        }

        // Top Products Bar Chart
        var topProductsEl = document.getElementById('topProductsChart');
        if (topProductsEl) {
            new Chart(topProductsEl.getContext('2d'), {
                type: 'bar',
                data: {
                    labels: config.topProductsLabels,
                    datasets: [{
                        label: config.strings.downloads,
                        data: config.topProductsCounts,
                        backgroundColor: 'rgba(65, 118, 144, 0.8)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } }
                }
            });
        }
    });
})();
