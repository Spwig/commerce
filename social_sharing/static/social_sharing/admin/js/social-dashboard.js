/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Social Sharing Dashboard
 *
 * Renders Chart.js charts for shares trend and platform distribution.
 * Reads data from json_script tags for XSS-safe data injection.
 */

(function() {
    'use strict';

    function initSocialDashboard() {
        // Read data from json_script tags (XSS-safe)
        var trendEl = document.getElementById('shares-trend-data');
        var distEl = document.getElementById('platform-dist-data');
        var i18nEl = document.getElementById('social-dashboard-i18n');

        var sharesTrendData = trendEl ? JSON.parse(trendEl.textContent) : [];
        var platformDistributionData = distEl ? JSON.parse(distEl.textContent) : [];
        var i18n = i18nEl ? JSON.parse(i18nEl.textContent) : {};

        if (typeof Chart === 'undefined') {
            console.error('Chart.js is not loaded!');
            return;
        }

        // Theme detection
        var isDarkTheme = document.body.getAttribute('data-theme') === 'dark';
        var textColor = isDarkTheme ? '#e8e8e8' : '#333333';
        var gridColor = isDarkTheme ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';

        Chart.defaults.color = textColor;
        Chart.defaults.borderColor = gridColor;

        // 1. Shares Trend Chart (Line Chart)
        var sharesTrendCtx = document.getElementById('sharesTrendChart');
        if (sharesTrendCtx && sharesTrendData && sharesTrendData.length > 0) {
            new Chart(sharesTrendCtx, {
                type: 'line',
                data: {
                    labels: sharesTrendData.map(function(d) {
                        return new Date(d.date).toLocaleDateString('en-US', {month: 'short', day: 'numeric'});
                    }),
                    datasets: [{
                        label: i18n.shares || 'Shares',
                        data: sharesTrendData.map(function(d) { return d.count; }),
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
                        pointHoverBorderColor: '#fff'
                    }]
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
                                label: function(context) {
                                    var n = context.parsed.y;
                                    return n + ' ' + (n !== 1 ? (i18n.shares_plural || 'shares') : (i18n.share_singular || 'share'));
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { precision: 0, color: textColor },
                            grid: { color: gridColor }
                        },
                        x: {
                            ticks: { color: textColor, maxRotation: 45, minRotation: 45 },
                            grid: { display: false }
                        }
                    }
                }
            });
        }

        // 2. Platform Distribution Chart (Doughnut Chart)
        var platformDistCtx = document.getElementById('platformDistributionChart');
        if (platformDistCtx && platformDistributionData && platformDistributionData.length > 0) {
            new Chart(platformDistCtx, {
                type: 'doughnut',
                data: {
                    labels: platformDistributionData.map(function(d) { return d.name; }),
                    datasets: [{
                        data: platformDistributionData.map(function(d) { return d.count; }),
                        backgroundColor: platformDistributionData.map(function(d) { return d.color; }),
                        borderColor: isDarkTheme ? '#1f1f1f' : '#ffffff',
                        borderWidth: 2
                    }]
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
                                font: { size: 12 }
                            }
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            borderWidth: 1,
                            padding: 12,
                            callbacks: {
                                label: function(context) {
                                    var total = context.dataset.data.reduce(function(a, b) { return a + b; }, 0);
                                    var percentage = ((context.parsed / total) * 100).toFixed(1);
                                    return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                                }
                            }
                        }
                    }
                }
            });
        }

        // Smooth scroll for settings link
        document.querySelectorAll('.scroll-link').forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                var target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
    }

    document.addEventListener('DOMContentLoaded', initSocialDashboard);

})();
