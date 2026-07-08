/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Shop Dashboard JavaScript
 * Handles chart rendering, filters, and dynamic data updates
 */

(function() {
    'use strict';

    // Dashboard state
    let salesChart = null;
    let viewsChart = null;
    let channelRevenueChart = null;
    let channelOrdersChart = null;
    let conversionFunnelChart = null;
    let trafficTypeChart = null;
    let trafficTrendsChart = null;
    let currentPeriod = 'this_year';
    let compareEnabled = true;
    let currentGrouping = 'day';

    /**
     * Initialize dashboard on page load
     */
    function initDashboard() {
        // Parse dashboard data from template
        const dataElement = document.getElementById('dashboard-data');
        if (!dataElement) {
            console.error('Dashboard data not found');
            return;
        }

        let dashboardData;
        try {
            dashboardData = JSON.parse(dataElement.textContent);
        } catch (e) {
            console.error('Failed to parse dashboard data:', e);
            return;
        }

        // Store API URL and current grouping
        window.dashboardApiUrl = dashboardData.api_url;
        currentPeriod = document.getElementById('period-select').value;
        compareEnabled = document.getElementById('compare-toggle').checked;
        currentGrouping = dashboardData.current_grouping || 'day';

        // Initialize charts
        initSalesChart(dashboardData.sales_over_time, dashboardData.compare_enabled);
        initViewsChart(dashboardData.views_over_time, dashboardData.compare_enabled);

        // Initialize sales channel charts
        if (dashboardData.sales_channel_performance) {
            initChannelRevenueChart(dashboardData.sales_channel_performance);
            initChannelOrdersChart(dashboardData.sales_channel_performance);
        }

        // Initialize conversion funnel chart
        if (dashboardData.conversion_funnel && dashboardData.conversion_funnel.stages) {
            initConversionFunnelChart(dashboardData.conversion_funnel);
        }

        // Initialize traffic source analytics charts
        if (dashboardData.traffic_source_analytics) {
            initTrafficTypeChart(dashboardData.traffic_source_analytics);
            initTrafficTrendsChart(dashboardData.traffic_source_analytics);
        }

        // Attach event listeners
        attachEventListeners();
        attachGeographyListeners();
    }

    /**
     * Initialize the sales revenue chart (PRIMARY CHART)
     */
    function initSalesChart(data, compare) {
        const canvas = document.getElementById('sales-chart');
        if (!canvas) return;

        // Destroy existing chart if it exists
        if (salesChart) {
            salesChart.destroy();
            salesChart = null;
        }

        const ctx = canvas.getContext('2d');

        // Prepare datasets for revenue
        const datasets = [
            {
                label: gettext('Revenue'),
                data: data.current.revenue,
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3,
                yAxisID: 'y'
            },
            {
                label: gettext('Orders'),
                data: data.current.orders,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: false,
                tension: 0.3,
                yAxisID: 'y1'
            }
        ];

        if (compare && data.previous) {
            datasets.push({
                label: gettext('Revenue (Previous)'),
                data: data.previous.revenue,
                borderColor: '#90ee90',
                backgroundColor: 'rgba(144, 238, 144, 0.05)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
                tension: 0.3,
                yAxisID: 'y'
            });
            datasets.push({
                label: gettext('Orders (Previous)'),
                data: data.previous.orders,
                borderColor: '#cbd5e0',
                backgroundColor: 'transparent',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
                tension: 0.3,
                yAxisID: 'y1'
            });
        }

        // Create chart
        salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.current.labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 15
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                const label = context.dataset.label || '';
                                if (label.includes('Revenue')) {
                                    return label + ': $' + context.parsed.y.toLocaleString(undefined, {
                                        minimumFractionDigits: 2,
                                        maximumFractionDigits: 2
                                    });
                                } else {
                                    return label + ': ' + context.parsed.y.toLocaleString();
                                }
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toLocaleString();
                            }
                        },
                        title: {
                            display: true,
                            text: gettext('Revenue'),
                            color: '#28a745',
                            font: {
                                weight: 'bold'
                            }
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        beginAtZero: true,
                        grid: {
                            drawOnChartArea: false
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        },
                        title: {
                            display: true,
                            text: gettext('Orders'),
                            color: '#667eea',
                            font: {
                                weight: 'bold'
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize the page views chart
     */
    function initViewsChart(data, compare) {
        const canvas = document.getElementById('views-chart');
        if (!canvas) return;

        // Destroy existing chart if it exists
        if (viewsChart) {
            viewsChart.destroy();
            viewsChart = null;
        }

        const ctx = canvas.getContext('2d');

        // Prepare datasets
        const datasets = [
            {
                label: gettext('Current Period'),
                data: data.current.data,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.3
            }
        ];

        if (compare && data.previous) {
            datasets.push({
                label: gettext('Previous Period'),
                data: data.previous.data,
                borderColor: '#cbd5e0',
                backgroundColor: 'rgba(203, 213, 224, 0.1)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
                tension: 0.3
            });
        }

        // Create chart
        viewsChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.current.labels.map(label => formatChartDate(label)),
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: compare,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 15
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y.toLocaleString() + ' views';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize the channel revenue pie chart
     */
    function initChannelRevenueChart(data) {
        const canvas = document.getElementById('channelRevenueChart');
        if (!canvas || !data.by_channel || data.by_channel.length === 0) return;

        // Destroy existing chart if it exists
        if (channelRevenueChart) {
            channelRevenueChart.destroy();
            channelRevenueChart = null;
        }

        const ctx = canvas.getContext('2d');

        // Define colors for each channel
        const channelColors = {
            'email': '#3498db',      // Blue
            'referral': '#9b59b6',   // Purple
            'social': '#e74c3c',     // Red
            'direct': '#2ecc71',     // Green
            'organic': '#f39c12',    // Orange
            'loyalty': '#e67e22',    // Dark Orange
            'utm_tracked': '#1abc9c', // Teal
            'web': '#3498db',        // Blue
            'mobile': '#e91e63',     // Pink
            'unknown': '#95a5a6'     // Gray
        };

        // Prepare chart data - ensure numeric values
        const labels = data.by_channel.map(channel => channel.source_display);
        const revenues = data.by_channel.map(channel => parseFloat(channel.revenue) || 0);
        const colors = data.by_channel.map(channel => channelColors[channel.source] || '#95a5a6');

        // Create chart
        channelRevenueChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: revenues,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 15,
                            font: {
                                size: 11
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const totalRevenue = parseFloat(data.total_revenue) || 0;
                                const percentage = totalRevenue > 0 ? ((value / totalRevenue) * 100).toFixed(1) : 0;
                                return label + ': $' + value.toLocaleString(undefined, {
                                    minimumFractionDigits: 2,
                                    maximumFractionDigits: 2
                                }) + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize the channel orders bar chart
     */
    function initChannelOrdersChart(data) {
        const canvas = document.getElementById('channelOrdersChart');
        if (!canvas || !data.by_channel || data.by_channel.length === 0) return;

        // Destroy existing chart if it exists
        if (channelOrdersChart) {
            channelOrdersChart.destroy();
            channelOrdersChart = null;
        }

        const ctx = canvas.getContext('2d');

        // Define colors for each channel
        const channelColors = {
            'email': '#3498db',      // Blue
            'referral': '#9b59b6',   // Purple
            'social': '#e74c3c',     // Red
            'direct': '#2ecc71',     // Green
            'organic': '#f39c12',    // Orange
            'loyalty': '#e67e22',    // Dark Orange
            'utm_tracked': '#1abc9c', // Teal
            'web': '#3498db',        // Blue
            'mobile': '#e91e63',     // Pink
            'unknown': '#95a5a6'     // Gray
        };

        // Prepare chart data - ensure numeric values
        const labels = data.by_channel.map(channel => channel.source_display);
        const orders = data.by_channel.map(channel => parseFloat(channel.orders) || 0);
        const colors = data.by_channel.map(channel => channelColors[channel.source] || '#95a5a6');

        // Create chart
        channelOrdersChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: gettext('Orders'),
                    data: orders,
                    backgroundColor: colors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                return gettext('Orders') + ': ' + context.parsed.y.toLocaleString();
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize the conversion funnel chart
     */
    function initConversionFunnelChart(data) {
        const canvas = document.getElementById('conversionFunnelChart');
        if (!canvas || !data.stages || data.stages.length === 0) return;

        // Destroy existing chart if it exists
        if (conversionFunnelChart) {
            conversionFunnelChart.destroy();
            conversionFunnelChart = null;
        }

        const ctx = canvas.getContext('2d');

        // Prepare data for horizontal bar chart (funnel)
        const labels = data.stages.map(stage => stage.name);
        const counts = data.stages.map(stage => parseFloat(stage.count) || 0);

        // Color gradient for funnel stages
        const colors = [
            '#3498db',  // Product Views - Blue
            '#9b59b6',  // Add to Cart - Purple
            '#f39c12',  // Checkout Started - Orange
            '#e67e22',  // Payment - Dark Orange
            '#27ae60'   // Order Complete - Green
        ];

        // Create chart
        conversionFunnelChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: gettext('Count'),
                    data: counts,
                    backgroundColor: colors,
                    borderWidth: 0,
                    barPercentage: 0.8,
                    categoryPercentage: 0.9
                }]
            },
            options: {
                indexAxis: 'y',  // Horizontal bars
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                const index = context.dataIndex;
                                const stage = data.stages[index];
                                const count = context.parsed.x.toLocaleString();
                                const percentage = stage.percentage.toFixed(1);
                                const dropOff = stage.drop_off > 0 ? ` (${stage.drop_off.toFixed(1)}% drop-off)` : '';
                                return [
                                    `Count: ${count}`,
                                    `${percentage}% of total${dropOff}`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            font: {
                                size: 12,
                                weight: '500'
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize the traffic type pie chart
     */
    function initTrafficTypeChart(data) {
        const canvas = document.getElementById('traffic-type-chart');
        if (!canvas || !data || !data.traffic_by_type) return;

        // Destroy existing chart if it exists
        if (trafficTypeChart) {
            trafficTypeChart.destroy();
            trafficTypeChart = null;
        }

        const ctx = canvas.getContext('2d');

        // Prepare data for pie chart
        const labels = data.traffic_by_type.map(item => item.type);
        const counts = data.traffic_by_type.map(item => item.count);
        const colors = data.traffic_by_type.map(item => item.color);

        trafficTypeChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: counts,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: 'var(--body-bg)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            font: {
                                size: 13
                            },
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                const index = context.dataIndex;
                                const item = data.traffic_by_type[index];
                                const count = item.count.toLocaleString();
                                const percentage = item.percentage.toFixed(1);
                                return [
                                    `${context.label}: ${count} visitors`,
                                    `${percentage}% of total traffic`
                                ];
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize the traffic trends line chart
     */
    function initTrafficTrendsChart(data) {
        const canvas = document.getElementById('traffic-trends-chart');
        if (!canvas || !data || !data.traffic_trends) return;

        // Destroy existing chart if it exists
        if (trafficTrendsChart) {
            trafficTrendsChart.destroy();
            trafficTrendsChart = null;
        }

        const ctx = canvas.getContext('2d');

        // Prepare data for line chart
        const labels = data.traffic_trends.map(item => item.date);
        const visitors = data.traffic_trends.map(item => item.visitors);

        trafficTrendsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Visitors',
                    data: visitors,
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderColor: '#3498db',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                    pointHoverRadius: 6,
                    pointBackgroundColor: '#3498db',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: {
                            size: 14
                        },
                        bodyFont: {
                            size: 13
                        },
                        callbacks: {
                            label: function(context) {
                                return `Visitors: ${context.parsed.y.toLocaleString()}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 0,
                            autoSkip: true,
                            maxTicksLimit: 10,
                            font: {
                                size: 11
                            }
                        }
                    },
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Format date for chart labels
     */
    function formatChartDate(dateString) {
        const date = new Date(dateString);
        const period = currentPeriod;

        // Show different formats based on period
        if (period === 'today' || period === 'yesterday') {
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        } else if (period === 'last_7_days' || period === 'last_30_days') {
            return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
        } else {
            return date.toLocaleDateString([], { month: 'short', day: 'numeric' });
        }
    }

    /**
     * Attach event listeners to dashboard controls
     */
    function attachEventListeners() {
        // Period selector
        const periodSelect = document.getElementById('period-select');
        if (periodSelect) {
            periodSelect.addEventListener('change', function() {
                currentPeriod = this.value;
                toggleCustomDateRange(this.value === 'custom');
                // Auto-refresh dashboard when period changes
                if (this.value !== 'custom') {
                    refreshDashboard();
                }
            });
        }

        // Compare toggle
        const compareToggle = document.getElementById('compare-toggle');
        if (compareToggle) {
            compareToggle.addEventListener('change', function() {
                compareEnabled = this.checked;
                // Auto-refresh dashboard when compare toggle changes
                refreshDashboard();
            });
        }

        // Refresh button
        const refreshButton = document.getElementById('refresh-dashboard');
        if (refreshButton) {
            refreshButton.addEventListener('click', refreshDashboard);
        }

        // Custom date inputs
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');
        if (startDateInput && endDateInput) {
            startDateInput.addEventListener('change', validateDateRange);
            endDateInput.addEventListener('change', validateDateRange);
        }

        // Grouping buttons
        const groupingButtons = document.querySelectorAll('.grouping-btn');
        groupingButtons.forEach(button => {
            button.addEventListener('click', function() {
                const grouping = this.getAttribute('data-grouping');
                if (grouping !== currentGrouping) {
                    currentGrouping = grouping;
                    // Update active state
                    groupingButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    // Refresh with new grouping
                    refreshDashboard();
                }
            });
        });

        // Jump to navigation
        const jumpToSelect = document.getElementById('jump-to-select');
        if (jumpToSelect) {
            jumpToSelect.addEventListener('change', function() {
                const sectionId = this.value;
                if (sectionId) {
                    const targetSection = document.getElementById(sectionId);
                    if (targetSection) {
                        // Smooth scroll to section
                        targetSection.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                        // Reset select to placeholder
                        setTimeout(() => {
                            this.value = '';
                        }, 300);
                    }
                }
            });
        }
    }

    /**
     * Toggle visibility of custom date range inputs
     */
    function toggleCustomDateRange(show) {
        const customDateRange = document.querySelector('.custom-date-range');
        if (customDateRange) {
            customDateRange.classList.toggle('mgmt-hidden', !show);
        }
    }

    /**
     * Validate custom date range
     */
    function validateDateRange() {
        const startDate = document.getElementById('start-date');
        const endDate = document.getElementById('end-date');

        if (!startDate || !endDate) return;

        const start = new Date(startDate.value);
        const end = new Date(endDate.value);

        if (start > end) {
            AdminModal.alert({message: gettext('Start date must be before end date'), type: 'warning'});
            endDate.value = startDate.value;
        }
    }

    /**
     * Refresh dashboard data via API
     */
    function refreshDashboard() {
        const periodSelect = document.getElementById('period-select');
        const compareToggle = document.getElementById('compare-toggle');
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');

        if (!periodSelect || !compareToggle) return;

        const period = periodSelect.value;
        const compare = compareToggle.checked;

        // Build API URL
        let apiUrl = window.dashboardApiUrl + '?period=' + period + '&compare=' + compare + '&grouping=' + currentGrouping;

        if (period === 'custom' && startDateInput && endDateInput) {
            const startDate = startDateInput.value;
            const endDate = endDateInput.value;

            if (!startDate || !endDate) {
                AdminModal.alert({message: gettext('Please select both start and end dates'), type: 'warning'});
                return;
            }

            apiUrl += '&start_date=' + startDate + 'T00:00:00&end_date=' + endDate + 'T23:59:59';
        }

        // Show loading state
        const dashboard = document.querySelector('.shop-dashboard');
        if (dashboard) {
            dashboard.classList.add('dashboard-loading');
        }

        // Fetch updated data
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                updateDashboard(data);
                if (dashboard) {
                    dashboard.classList.remove('dashboard-loading');
                }
            })
            .catch(error => {
                console.error('Error refreshing dashboard:', error);
                AdminModal.alert({message: gettext('Failed to refresh dashboard. Please try again.'), type: 'error'});
                if (dashboard) {
                    dashboard.classList.remove('dashboard-loading');
                }
            });
    }

    /**
     * Update dashboard with new data
     */
    function updateDashboard(data) {
        // Update grouping if returned
        if (data.grouping) {
            currentGrouping = data.grouping;
            // Update active button state
            document.querySelectorAll('.grouping-btn').forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-grouping') === currentGrouping);
            });
        }

        // Update action cards
        updateActionCards(data.action_cards);

        // Update sales performance
        updateSalesPerformance(data.sales_performance);

        // Update profit metrics
        if (data.profit_metrics) {
            updateProfitMetrics(data.profit_metrics);
        }

        // Update PRIMARY CHART: Sales over time
        updateSalesChart(data.sales_over_time, compareEnabled);

        // Update top products
        updateTopProducts(data.top_products);

        // Update visitor analytics
        updateVisitorAnalytics(data.visitor_analytics);

        // Update views chart
        updateViewsChart(data.views_over_time, compareEnabled);

        // Update most viewed products
        updateMostViewedProducts(data.most_viewed_products);

        // Update visitor geography
        updateVisitorGeography(data.visitor_geography);

        // Update referrer stats if available
        if (data.referrer_stats && data.referrer_stats.length > 0) {
            updateReferrerStats(data.referrer_stats);
        }

        // Update sales channel performance charts
        if (data.sales_channel_performance) {
            updateChannelCharts(data.sales_channel_performance);
        }

        // Update conversion funnel chart
        if (data.conversion_funnel && data.conversion_funnel.stages) {
            updateConversionFunnelChart(data.conversion_funnel);
        }

        // Update traffic source analytics charts
        if (data.traffic_source_analytics) {
            // Reinitialize the charts with new data
            initTrafficTypeChart(data.traffic_source_analytics);
            initTrafficTrendsChart(data.traffic_source_analytics);
        }
    }

    /**
     * Update action cards
     */
    function updateActionCards(data) {
        const cards = document.querySelectorAll('.action-card-value');
        if (cards.length >= 4) {
            cards[0].textContent = data.incomplete_orders;
            cards[1].textContent = data.abandoned_carts;
            cards[2].textContent = data.low_stock_products;
            cards[3].textContent = data.out_of_stock_products;
        }
    }

    /**
     * Update sales performance metrics
     */
    function updateSalesPerformance(data) {
        const metricCards = document.querySelectorAll('.metrics-grid .metric-card');

        // Revenue
        if (metricCards[0]) {
            const valueEl = metricCards[0].querySelector('.metric-value');
            const changeEl = metricCards[0].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = '$' + parseFloat(data.current.revenue).toFixed(2);
            if (changeEl && data.changes && data.changes.revenue !== null) {
                updateChangeIndicator(changeEl, data.changes.revenue);
            }
        }

        // Orders
        if (metricCards[1]) {
            const valueEl = metricCards[1].querySelector('.metric-value');
            const changeEl = metricCards[1].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = data.current.orders;
            if (changeEl && data.changes && data.changes.orders !== null) {
                updateChangeIndicator(changeEl, data.changes.orders);
            }
        }

        // AOV
        if (metricCards[2]) {
            const valueEl = metricCards[2].querySelector('.metric-value');
            const changeEl = metricCards[2].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = '$' + parseFloat(data.current.aov).toFixed(2);
            if (changeEl && data.changes && data.changes.aov !== null) {
                updateChangeIndicator(changeEl, data.changes.aov);
            }
        }
    }

    /**
     * Update profit metrics
     */
    function updateProfitMetrics(data) {
        // Find the Profit Analysis section by its heading
        const profitSection = Array.from(document.querySelectorAll('.section-header h2'))
            .find(h => h.textContent.includes('Profit Analysis') || h.textContent.includes(gettext('Profit Analysis')));

        if (!profitSection) return;

        // Get the metrics grid within the profit section
        const metricsGrid = profitSection.closest('.dashboard-section').querySelector('.metrics-grid');
        if (!metricsGrid) return;

        const metricCards = metricsGrid.querySelectorAll('.metric-card');

        // Helper to format currency (will use the same format as backend)
        const formatCurrency = (value) => {
            // For now, using simple $ format - backend handles locale-aware formatting on page load
            return '$' + parseFloat(value).toFixed(2);
        };

        // 1. Gross Profit
        if (metricCards[0]) {
            const valueEl = metricCards[0].querySelector('.metric-value');
            const changeEl = metricCards[0].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = formatCurrency(data.current.profit);
            if (changeEl && data.changes && data.changes.profit !== null) {
                updateChangeIndicator(changeEl, data.changes.profit);
            }
        }

        // 2. Profit Margin
        if (metricCards[1]) {
            const valueEl = metricCards[1].querySelector('.metric-value');
            const changeEl = metricCards[1].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = parseFloat(data.current.margin_percentage).toFixed(1) + '%';
            if (changeEl && data.changes && data.changes.margin_percentage !== null) {
                // For margin, lower is worse (red), higher is better (green)
                const change = data.changes.margin_percentage;
                const isPositive = change >= 0;
                changeEl.className = 'metric-change ' + (isPositive ? 'positive' : 'negative');
                const icon = changeEl.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-arrow-' + (isPositive ? 'up' : 'down');
                }
                const textNode = Array.from(changeEl.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
                if (textNode) {
                    textNode.textContent = Math.abs(change).toFixed(1) + 'pp';
                } else {
                    changeEl.innerHTML += Math.abs(change).toFixed(1) + 'pp';
                }
            }
        }

        // 3. Cost of Goods Sold
        if (metricCards[2]) {
            const valueEl = metricCards[2].querySelector('.metric-value');
            const changeEl = metricCards[2].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = formatCurrency(data.current.cogs);
            if (changeEl && data.changes && data.changes.cogs !== null) {
                // For COGS, lower is better (green), higher is worse (red) - reversed logic
                const change = data.changes.cogs;
                const isPositive = change <= 0;  // Reversed: decrease is positive
                changeEl.className = 'metric-change ' + (isPositive ? 'positive' : 'negative');
                const icon = changeEl.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-arrow-' + (change <= 0 ? 'down' : 'up');
                }
                const textNode = Array.from(changeEl.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
                if (textNode) {
                    textNode.textContent = Math.abs(change).toFixed(1) + '%';
                } else {
                    changeEl.innerHTML += Math.abs(change).toFixed(1) + '%';
                }
            }
        }

        // 4. Refunds
        if (metricCards[3]) {
            const valueEl = metricCards[3].querySelector('.metric-value');
            const changeEl = metricCards[3].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = formatCurrency(data.current.refunds);
            if (changeEl && data.changes && data.changes.refunds !== null) {
                // For refunds, lower is better (green), higher is worse (red) - reversed logic
                const change = data.changes.refunds;
                const isPositive = change <= 0;  // Reversed: decrease is positive
                changeEl.className = 'metric-change ' + (isPositive ? 'positive' : 'negative');
                const icon = changeEl.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-arrow-' + (change <= 0 ? 'down' : 'up');
                }
                const textNode = Array.from(changeEl.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
                if (textNode) {
                    textNode.textContent = Math.abs(change).toFixed(1) + '%';
                } else {
                    changeEl.innerHTML += Math.abs(change).toFixed(1) + '%';
                }
            }
        }

        // Update product profits table if available
        if (data.products && data.products.length > 0) {
            const profitTable = profitSection.closest('.dashboard-section').querySelector('.profit-table tbody');
            if (profitTable) {
                profitTable.innerHTML = data.products.map(product => `
                    <tr>
                        <td class="table-td-left-light">
                            <span class="table-rank">${product.rank || ''}</span>
                            ${product.product_name}
                        </td>
                        <td class="table-td-right-light">
                            ${product.units_sold}
                        </td>
                        <td class="table-td-right-light">
                            ${formatCurrency(product.revenue)}
                        </td>
                        <td class="table-td-right-light text-quiet">
                            ${formatCurrency(product.cogs)}
                        </td>
                        <td class="table-td-right text-bold text-success-fg">
                            ${formatCurrency(product.profit)}
                        </td>
                        <td class="table-td-right text-bold text-success-fg">
                            ${parseFloat(product.margin_pct).toFixed(1)}%
                        </td>
                    </tr>
                `).join('');
            }
        }
    }

    /**
     * Update change indicator
     */
    function updateChangeIndicator(element, change) {
        const isPositive = change >= 0;
        element.className = 'metric-change ' + (isPositive ? 'positive' : 'negative');

        const icon = element.querySelector('i');
        if (icon) {
            icon.className = 'fas fa-arrow-' + (isPositive ? 'up' : 'down');
        }

        const textNode = Array.from(element.childNodes).find(node => node.nodeType === Node.TEXT_NODE);
        if (textNode) {
            textNode.textContent = Math.abs(change).toFixed(1) + '%';
        } else {
            element.innerHTML += Math.abs(change).toFixed(1) + '%';
        }
    }

    /**
     * Update top products table
     */
    function updateTopProducts(products) {
        const tbody = document.querySelector('.products-table tbody');
        if (!tbody) return;

        if (products.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="empty-state"><i class="fas fa-inbox"></i>' +
                gettext('No sales data for this period') + '</td></tr>';
            return;
        }

        tbody.innerHTML = products.map(product => {
            const imageHtml = product.image_url
                ? `<img src="${product.image_url}" alt="${product.name}" class="product-image">`
                : '<div class="product-image-placeholder"><i class="fas fa-image"></i></div>';

            return `<tr>
                <td>
                    <div class="product-info">
                        ${imageHtml}
                        <span class="product-name">${product.name}</span>
                    </div>
                </td>
                <td class="text-right">${product.units_sold}</td>
                <td class="text-right">$${parseFloat(product.revenue).toFixed(2)}</td>
            </tr>`;
        }).join('');
    }

    /**
     * Update visitor analytics
     */
    function updateVisitorAnalytics(data) {
        // Find visitor analytics section (second metrics-grid)
        const metricGrids = document.querySelectorAll('.metrics-grid');
        if (metricGrids.length < 2) return;

        const visitorMetrics = metricGrids[1].querySelectorAll('.metric-card');

        // Unique visitors
        if (visitorMetrics[0]) {
            const valueEl = visitorMetrics[0].querySelector('.metric-value');
            const changeEl = visitorMetrics[0].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = data.current.unique_visitors;
            if (changeEl && data.changes && data.changes.unique_visitors !== null) {
                updateChangeIndicator(changeEl, data.changes.unique_visitors);
            }
        }

        // Conversion rate
        if (visitorMetrics[1]) {
            const valueEl = visitorMetrics[1].querySelector('.metric-value');
            const changeEl = visitorMetrics[1].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = data.current.conversion_rate + '%';
            if (changeEl && data.changes && data.changes.conversion_rate !== null) {
                updateChangeIndicator(changeEl, data.changes.conversion_rate);
            }
        }

        // New customers
        if (visitorMetrics[2]) {
            const valueEl = visitorMetrics[2].querySelector('.metric-value');
            const changeEl = visitorMetrics[2].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = data.current.new_customers;
            if (changeEl && data.changes && data.changes.new_customers !== null) {
                updateChangeIndicator(changeEl, data.changes.new_customers);
            }
        }

        // Page views
        if (visitorMetrics[3]) {
            const valueEl = visitorMetrics[3].querySelector('.metric-value');
            const changeEl = visitorMetrics[3].querySelector('.metric-change');
            if (valueEl) valueEl.textContent = data.current.page_views;
            if (changeEl && data.changes && data.changes.page_views !== null) {
                updateChangeIndicator(changeEl, data.changes.page_views);
            }
        }
    }

    /**
     * Update sales chart
     */
    function updateSalesChart(data, compare) {
        if (!salesChart) return;

        salesChart.data.labels = data.current.labels;
        salesChart.data.datasets[0].data = data.current.revenue;
        salesChart.data.datasets[1].data = data.current.orders;

        if (compare && data.previous) {
            if (salesChart.data.datasets.length === 2) {
                // Add previous period datasets
                salesChart.data.datasets.push({
                    label: gettext('Revenue (Previous)'),
                    data: data.previous.revenue,
                    borderColor: '#90ee90',
                    backgroundColor: 'rgba(144, 238, 144, 0.05)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.3,
                    yAxisID: 'y'
                });
                salesChart.data.datasets.push({
                    label: gettext('Orders (Previous)'),
                    data: data.previous.orders,
                    borderColor: '#cbd5e0',
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.3,
                    yAxisID: 'y1'
                });
            } else {
                salesChart.data.datasets[2].data = data.previous.revenue;
                salesChart.data.datasets[3].data = data.previous.orders;
            }
        } else {
            // Remove previous period datasets
            if (salesChart.data.datasets.length > 2) {
                salesChart.data.datasets.splice(2, 2);
            }
        }

        salesChart.update();
    }

    /**
     * Update views chart
     */
    function updateViewsChart(data, compare) {
        if (!viewsChart) return;

        viewsChart.data.labels = data.current.labels.map(label => formatChartDate(label));
        viewsChart.data.datasets[0].data = data.current.data;

        if (compare && data.previous) {
            if (viewsChart.data.datasets.length === 1) {
                // Add previous period dataset
                viewsChart.data.datasets.push({
                    label: gettext('Previous Period'),
                    data: data.previous.data,
                    borderColor: '#cbd5e0',
                    backgroundColor: 'rgba(203, 213, 224, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.3
                });
            } else {
                viewsChart.data.datasets[1].data = data.previous.data;
            }
            viewsChart.options.plugins.legend.display = true;
        } else {
            // Remove previous period dataset
            if (viewsChart.data.datasets.length > 1) {
                viewsChart.data.datasets.pop();
            }
            viewsChart.options.plugins.legend.display = false;
        }

        viewsChart.update();
    }

    /**
     * Update most viewed products list
     */
    function updateMostViewedProducts(products) {
        const lists = document.querySelectorAll('.data-list');
        if (lists.length < 1) return;

        const productList = lists[0];
        if (products.length === 0) {
            productList.innerHTML = '<li class="empty-state"><i class="fas fa-inbox"></i>' +
                gettext('No view data available') + '</li>';
            return;
        }

        productList.innerHTML = products.map(product => {
            const imageHtml = product.image_url
                ? `<img src="${product.image_url}" alt="${product.name}" class="list-item-image">`
                : '<div class="list-item-image-placeholder"><i class="fas fa-image"></i></div>';

            return `<li class="data-list-item">
                <div class="list-item-content">
                    ${imageHtml}
                    <span class="list-item-label">${product.name}</span>
                </div>
                <span class="list-item-value">${product.views}</span>
            </li>`;
        }).join('');
    }

    /**
     * Update visitor geography list
     */
    function updateVisitorGeography(geography) {
        const lists = document.querySelectorAll('.data-list');
        if (lists.length < 2) return;

        const geoList = lists[1];
        if (geography.length === 0) {
            geoList.innerHTML = '<li class="empty-state"><i class="fas fa-inbox"></i>' +
                gettext('No geography data available') + '</li>';
            return;
        }

        geoList.innerHTML = geography.map(item => {
            // Check if this is country-level or drill-down (city-level) data
            if (item.country_name) {
                // Country view with flags and drill-down
                return `<li class="data-list-item geography-country" data-country-code="${item.country_code}">
                    <div class="list-item-content">
                        <span class="country-flag" style="font-size: 24px; margin-right: 10px;">${item.flag}</span>
                        <span class="list-item-label" style="font-weight: 500;">
                            ${item.country_name}
                            <span style="color: #999; font-size: 12px; margin-left: 5px;">(${item.country_code})</span>
                        </span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span class="list-item-value">${item.visitors}</span>
                        <i class="fas fa-chevron-right" style="color: #999; font-size: 12px;"></i>
                    </div>
                </li>`;
            } else {
                // City drill-down view
                return `<li class="data-list-item">
                    <div class="list-item-content">
                        <i class="fas fa-map-marker-alt" style="color: #667eea; margin-right: 8px;"></i>
                        <span class="list-item-label">
                            ${item.city}${item.region ? ', ' + item.region : ''}
                        </span>
                    </div>
                    <span class="list-item-value">${item.visitors}</span>
                </li>`;
            }
        }).join('');

        // Re-attach drill-down listeners after updating
        attachGeographyListeners();
    }

    /**
     * Attach accordion listeners to geography items
     */
    function attachGeographyListeners() {
        const countryHeaders = document.querySelectorAll('.geography-country-header');

        countryHeaders.forEach(header => {
            header.addEventListener('click', function() {
                const countryItem = this.closest('.geography-country-item');
                const countryCode = countryItem.getAttribute('data-country-code');
                const citiesList = countryItem.querySelector('.geography-cities-list');
                const isExpanded = countryItem.classList.contains('expanded');

                if (isExpanded) {
                    // Collapse
                    countryItem.classList.remove('expanded');
                    citiesList.classList.add('mgmt-hidden');
                } else {
                    // Collapse all other countries first
                    document.querySelectorAll('.geography-country-item.expanded').forEach(item => {
                        item.classList.remove('expanded');
                        item.querySelector('.geography-cities-list').classList.add('mgmt-hidden');
                    });

                    // Expand this country
                    countryItem.classList.add('expanded');
                    citiesList.classList.remove('mgmt-hidden');

                    // Load cities if not already loaded
                    if (citiesList.querySelector('.loading-cities')) {
                        loadCountryCities(countryCode, citiesList);
                    }
                }
            });
        });
    }

    /**
     * Load cities for a specific country via AJAX
     */
    function loadCountryCities(countryCode, citiesList) {
        const periodSelect = document.getElementById('period-select');
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');

        if (!periodSelect) return;

        const period = periodSelect.value;

        // Build API URL for cities
        let apiUrl = `/admin/management/systemmetrics/shop-dashboard/geography-cities/${countryCode}/?period=${period}`;

        if (period === 'custom' && startDateInput && endDateInput) {
            const startDate = startDateInput.value;
            const endDate = endDateInput.value;
            if (startDate && endDate) {
                apiUrl += `&start_date=${startDate}T00:00:00&end_date=${endDate}T23:59:59`;
            }
        }

        // Fetch cities data
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                if (data.cities && data.cities.length > 0) {
                    citiesList.innerHTML = data.cities.map(city => {
                        return `<li class="geography-city-item">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <i class="fas fa-map-marker-alt" style="color: #667eea; font-size: 12px;"></i>
                                <span class="city-name">${city.city}${city.region ? ', ' + city.region : ''}</span>
                            </div>
                            <span class="city-visitors">${city.visitors}</span>
                        </li>`;
                    }).join('');
                } else {
                    citiesList.innerHTML = '<li style="padding: 10px; color: #999; font-size: 13px; text-align: center;">No city data available</li>';
                }
            })
            .catch(error => {
                console.error('Error loading cities:', error);
                citiesList.innerHTML = '<li style="padding: 10px; color: #dc3545; font-size: 13px; text-align: center;">Failed to load cities</li>';
            });
    }

    /**
     * Drill down into specific country or back to countries
     */
    function drillDownGeography(countryCode) {
        const periodSelect = document.getElementById('period-select');
        const compareToggle = document.getElementById('compare-toggle');
        const startDateInput = document.getElementById('start-date');
        const endDateInput = document.getElementById('end-date');

        if (!periodSelect || !compareToggle) return;

        const period = periodSelect.value;
        const compare = compareToggle.checked;

        // Build API URL with country parameter
        let apiUrl = window.dashboardApiUrl + '?period=' + period + '&compare=' + compare + '&grouping=' + currentGrouping;

        if (countryCode) {
            apiUrl += '&country=' + countryCode;
        }

        if (period === 'custom' && startDateInput && endDateInput) {
            const startDate = startDateInput.value;
            const endDate = endDateInput.value;
            if (startDate && endDate) {
                apiUrl += '&start_date=' + startDate + 'T00:00:00&end_date=' + endDate + 'T23:59:59';
            }
        }

        // Fetch drill-down data
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                updateVisitorGeography(data.visitor_geography);
            })
            .catch(error => {
                console.error('Error drilling down geography:', error);
            });
    }

    /**
     * Update referrer stats list
     */
    function updateReferrerStats(referrers) {
        const lists = document.querySelectorAll('.data-list');
        if (lists.length < 3) return;

        const referrerList = lists[2];
        referrerList.innerHTML = referrers.map(referrer => {
            return `<li class="data-list-item">
                <span class="list-item-label">${referrer.source}</span>
                <span class="list-item-value">${referrer.visitors}</span>
            </li>`;
        }).join('');
    }

    /**
     * Update sales channel performance charts
     */
    function updateChannelCharts(data) {
        if (!data.by_channel || data.by_channel.length === 0) return;

        // Define colors for each channel
        const channelColors = {
            'email': '#3498db',      // Blue
            'referral': '#9b59b6',   // Purple
            'social': '#e74c3c',     // Red
            'direct': '#2ecc71',     // Green
            'organic': '#f39c12',    // Orange
            'loyalty': '#e67e22',    // Dark Orange
            'utm_tracked': '#1abc9c', // Teal
            'web': '#3498db',        // Blue
            'mobile': '#e91e63',     // Pink
            'unknown': '#95a5a6'     // Gray
        };

        // Update revenue chart
        if (channelRevenueChart) {
            channelRevenueChart.data.labels = data.by_channel.map(channel => channel.source_display);
            channelRevenueChart.data.datasets[0].data = data.by_channel.map(channel => parseFloat(channel.revenue) || 0);
            channelRevenueChart.data.datasets[0].backgroundColor = data.by_channel.map(channel =>
                channelColors[channel.source] || '#95a5a6'
            );
            channelRevenueChart.update();
        }

        // Update orders chart
        if (channelOrdersChart) {
            channelOrdersChart.data.labels = data.by_channel.map(channel => channel.source_display);
            channelOrdersChart.data.datasets[0].data = data.by_channel.map(channel => parseFloat(channel.orders) || 0);
            channelOrdersChart.data.datasets[0].backgroundColor = data.by_channel.map(channel =>
                channelColors[channel.source] || '#95a5a6'
            );
            channelOrdersChart.update();
        }
    }

    /**
     * Update conversion funnel chart
     */
    function updateConversionFunnelChart(data) {
        if (!conversionFunnelChart || !data.stages || data.stages.length === 0) return;

        const labels = data.stages.map(stage => stage.name);
        const counts = data.stages.map(stage => parseFloat(stage.count) || 0);

        // Update chart data
        conversionFunnelChart.data.labels = labels;
        conversionFunnelChart.data.datasets[0].data = counts;
        conversionFunnelChart.update();
    }

    /**
     * Polyfill for gettext (if not available)
     */
    function gettext(str) {
        if (typeof window.gettext === 'function') {
            return window.gettext(str);
        }
        return str;
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDashboard);
    } else {
        initDashboard();
    }

})();
