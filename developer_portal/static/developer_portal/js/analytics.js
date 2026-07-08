/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var el = document.getElementById('analytics-chart-data');
        if (!el) return;

        var config;
        try { config = JSON.parse(el.textContent); } catch (err) { return; }

        if (!config.labels || !config.labels.length) return;

        var ctx = document.getElementById('downloadsChart');
        if (!ctx || typeof Chart === 'undefined') return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: config.labels.map(function (d) {
                    var dt = new Date(d);
                    return dt.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
                }),
                datasets: [{
                    label: config.downloadsLabel || 'Downloads',
                    data: config.values,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.08)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 2,
                    pointHoverRadius: 5,
                    borderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 },
                        grid: { color: 'rgba(0,0,0,0.06)' },
                    },
                    x: { grid: { display: false } }
                },
                interaction: { intersect: false, mode: 'index' },
            }
        });
    });

}());
