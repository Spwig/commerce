/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Translation Jobs Management JavaScript
 */

// Global variables
let currentTab = 'all';
let currentPage = 1;
let jobsPerPage = 20;
let selectedJobs = new Set();
let sortField = 'created_at';
let sortOrder = 'desc';
let refreshInterval = null;

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', function() {
    // Start auto-refresh
    startAutoRefresh();

    // Setup priority slider
    const prioritySlider = document.getElementById('priority');
    if (prioritySlider) {
        prioritySlider.addEventListener('input', function() {
            document.getElementById('priority-value').textContent = this.value;
        });
    }

    // Load initial jobs
    refreshJobList();
});

// Auto-refresh functionality
function startAutoRefresh() {
    // Refresh every 5 seconds for processing jobs
    refreshInterval = setInterval(() => {
        const processingCount = parseInt(document.getElementById('processing-count')?.textContent || 0);
        if (processingCount > 0) {
            refreshJobList(true); // Silent refresh
        }
    }, 5000);
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
    }
}

// Tab switching
function switchTab(tab) {
    currentTab = tab;
    currentPage = 1;

    // Update tab UI
    document.querySelectorAll('.admin-tab-btn').forEach(t => {
        t.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

    // Refresh job list
    refreshJobList();
}

// Refresh job list
async function refreshJobList(silent = false) {
    if (!silent) {
        showLoading();
    }

    try {
        const params = new URLSearchParams({
            page: currentPage,
            per_page: jobsPerPage,
            order_by: (sortOrder === 'desc' ? '-' : '') + sortField
        });

        if (currentTab !== 'all') {
            params.append('status', currentTab === 'queue' ? 'pending' : currentTab);
        }

        const response = await fetch(`/api/translations/service/jobs/?${params}`);
        const data = await response.json();

        if (data.success) {
            updateJobCards(data.jobs);
            updatePagination(data);
            updateStatistics();
        }
    } catch (error) {
        console.error('Failed to refresh jobs:', error);
        if (!silent) {
            showError('Failed to load jobs');
        }
    } finally {
        if (!silent) {
            hideLoading();
        }
    }
}

// Get status icon HTML
function getStatusIcon(status) {
    const icons = {
        'pending': '<i class="fas fa-clock job-icon-pending"></i>',
        'processing': '<i class="fas fa-spinner fa-spin job-icon-processing"></i>',
        'completed': '<i class="fas fa-check-circle job-icon-completed"></i>',
        'failed': '<i class="fas fa-times-circle job-icon-failed"></i>',
        'cancelled': '<i class="fas fa-ban job-icon-cancelled"></i>'
    };
    return icons[status] || '<i class="fas fa-question"></i>';
}

// Get status badge class
function getStatusBadgeClass(status) {
    const classes = {
        'pending': 'list-row-card-badge-warning',
        'processing': 'list-row-card-badge-primary',
        'completed': 'list-row-card-badge-success',
        'failed': 'list-row-card-badge-error',
        'cancelled': ''
    };
    return classes[status] || '';
}

// Get status label
function getStatusLabel(status) {
    const labels = {
        'pending': 'Pending',
        'processing': 'Processing',
        'completed': 'Completed',
        'failed': 'Failed',
        'cancelled': 'Cancelled'
    };
    return labels[status] || status;
}

// Get job type label
function getJobTypeLabel(jobType) {
    const labels = {
        'product': 'Product',
        'category': 'Category',
        'page': 'Page',
        'email': 'Email Template',
        'bulk': 'Bulk Translation',
        'custom': 'Custom'
    };
    return labels[jobType] || jobType;
}

// Get action buttons HTML for a job card
function getCardActionButtons(job) {
    const buttons = [];

    if (job.status === 'pending') {
        buttons.push(`
            <button class="list-row-card-action" onclick="startJob(${job.id})" title="Start">
                <i class="fas fa-play"></i>
            </button>
            <button class="list-row-card-action" onclick="cancelJob(${job.id})" title="Cancel">
                <i class="fas fa-times"></i>
            </button>
        `);
    } else if (job.status === 'processing') {
        buttons.push(`
            <button class="list-row-card-action" onclick="cancelJob(${job.id})" title="Cancel">
                <i class="fas fa-stop"></i>
            </button>
        `);
    } else if (job.status === 'failed') {
        buttons.push(`
            <button class="list-row-card-action" onclick="retryJob(${job.id})" title="Retry">
                <i class="fas fa-redo"></i>
            </button>
        `);
    }

    buttons.push(`
        <button class="list-row-card-action" onclick="viewJobDetails(${job.id})" title="Details">
            <i class="fas fa-info-circle"></i>
        </button>
    `);

    return buttons.join('');
}

// Update job cards
function updateJobCards(jobs) {
    const container = document.getElementById('jobs-container');
    if (!container) return;

    if (jobs.length === 0) {
        container.innerHTML = `
            <div class="list-row-card jobs-empty-state">
                <div class="jobs-empty-icon">
                    <i class="fas fa-inbox"></i>
                </div>
                <p class="jobs-empty-text">No translation jobs found</p>
                <p class="jobs-empty-subtext">
                    Create a job to start translating your content.
                </p>
            </div>
        `;
        return;
    }

    container.innerHTML = jobs.map(job => {
        const targetLangs = job.target_languages.join(', ');
        const priorityBadge = job.priority >= 10
            ? '<span class="list-row-card-badge list-row-card-badge-error"><i class="fas fa-arrow-up"></i> High Priority</span>'
            : '';

        return `
        <div class="list-row-card" data-job-id="${job.id}">
            <div class="list-row-card-checkbox">
                <input type="checkbox" class="job-select" value="${job.id}"
                       ${selectedJobs.has(job.id) ? 'checked' : ''}
                       onchange="toggleJobSelection(${job.id})">
            </div>

            <div class="list-row-card-icon">
                ${getStatusIcon(job.status)}
            </div>

            <div class="list-row-card-content">
                <h3 class="list-row-card-title">
                    ${getJobTypeLabel(job.job_type)} Translation
                </h3>
                <div class="list-row-card-badges">
                    <span class="list-row-card-badge ${getStatusBadgeClass(job.status)}">
                        ${getStatusLabel(job.status)}
                    </span>
                    ${priorityBadge}
                    <span class="list-row-card-badge">
                        <i class="fas fa-language"></i>
                        ${job.source_language} <i class="fas fa-arrow-right"></i> ${targetLangs}
                    </span>
                </div>
                <div class="list-row-card-meta">
                    <div class="list-row-card-meta-item">
                        <i class="fas fa-hashtag"></i>
                        <span>#${job.id}</span>
                    </div>
                    <div class="list-row-card-meta-item">
                        <i class="fas fa-server"></i>
                        <span>${job.provider || 'Auto'}</span>
                    </div>
                    <div class="list-row-card-meta-item">
                        <i class="fas fa-clock"></i>
                        <span>${formatTimeAgo(job.created_at)}</span>
                    </div>
                    ${job.created_by ? `
                    <div class="list-row-card-meta-item">
                        <i class="fas fa-user"></i>
                        <span>${job.created_by}</span>
                    </div>` : ''}
                </div>
            </div>

            <div class="list-row-card-stats">
                <div class="list-row-card-stat">
                    <span class="list-row-card-stat-label">Progress</span>
                    <div class="job-card-progress">
                        <div class="job-card-progress-bar">
                            <div class="job-card-progress-fill" data-width="${job.progress}"></div>
                        </div>
                        <span class="job-card-progress-text">${job.progress}%</span>
                    </div>
                </div>
            </div>

            <div class="list-row-card-actions">
                ${getCardActionButtons(job)}
            </div>
        </div>`;
    }).join('');

    // Apply dynamic widths from data attributes (CSP-safe)
    container.querySelectorAll('[data-width]').forEach(function(el) {
        el.style.width = el.dataset.width + '%';
    });
}

// Format time ago
function formatTimeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return 'just now';
    if (seconds < 3600) return Math.floor(seconds / 60) + ' min ago';
    if (seconds < 86400) return Math.floor(seconds / 3600) + ' hours ago';
    if (seconds < 604800) return Math.floor(seconds / 86400) + ' days ago';
    return date.toLocaleDateString();
}

// Update pagination
function updatePagination(data) {
    document.getElementById('showing-start').textContent = ((data.page - 1) * data.per_page) + 1;
    document.getElementById('showing-end').textContent = Math.min(data.page * data.per_page, data.total);
    document.getElementById('total-jobs').textContent = data.total;
    document.getElementById('current-page').textContent = data.page;
    document.getElementById('total-pages').textContent = data.pages;

    // Update button states
    document.getElementById('prev-btn').disabled = data.page === 1;
    document.getElementById('next-btn').disabled = data.page === data.pages;
}

// Update statistics
async function updateStatistics() {
    try {
        const response = await fetch('/api/translations/service/jobs/queue-status/');
        const data = await response.json();

        if (data.success && data.stats) {
            document.getElementById('pending-count').textContent = data.stats.pending || 0;
            document.getElementById('processing-count').textContent = data.stats.processing || 0;
            document.getElementById('queue-count').textContent = data.stats.pending || 0;
            document.getElementById('processing-tab-count').textContent = data.stats.processing || 0;
            document.getElementById('failed-count').textContent = data.stats.failed || 0;
        }
    } catch (error) {
        console.error('Failed to update statistics:', error);
    }
}

// Pagination controls
function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        refreshJobList();
    }
}

function nextPage() {
    currentPage++;
    refreshJobList();
}

// Sorting
function sortTable(field) {
    if (sortField === field) {
        sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
    } else {
        sortField = field;
        sortOrder = 'desc';
    }
    refreshJobList();
}

// Selection handling
function toggleSelectAll() {
    const selectAll = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.job-select');

    checkboxes.forEach(cb => {
        cb.checked = selectAll.checked;
        const jobId = parseInt(cb.value);
        if (selectAll.checked) {
            selectedJobs.add(jobId);
        } else {
            selectedJobs.delete(jobId);
        }
    });

    updateBulkActionsButton();
}

function toggleJobSelection(jobId) {
    if (selectedJobs.has(jobId)) {
        selectedJobs.delete(jobId);
    } else {
        selectedJobs.add(jobId);
    }
    updateBulkActionsButton();
}

function updateBulkActionsButton() {
    const bulkBtn = document.getElementById('bulk-actions-btn');
    bulkBtn.disabled = selectedJobs.size === 0;
}

// Create Job Modal
function openCreateJobModal() {
    document.getElementById('create-job-modal').classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
}

function closeCreateJobModal() {
    document.getElementById('create-job-modal').classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
    document.getElementById('create-job-form').reset();
}

async function submitCreateJob(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    // Get selected target languages
    const targetLangs = [];
    formData.getAll('target_languages').forEach(lang => {
        targetLangs.push(lang);
    });

    if (targetLangs.length === 0) {
        showError('Please select at least one target language');
        return;
    }

    const jobData = {
        job_type: formData.get('job_type'),
        source_language: formData.get('source_language'),
        target_languages: targetLangs,
        priority: parseInt(formData.get('priority')),
        provider_id: formData.get('provider_id') || null,
        execute_now: formData.get('execute_now') === 'on'
    };

    try {
        const response = await fetch('/api/translations/service/jobs/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            },
            body: JSON.stringify(jobData)
        });

        const data = await response.json();

        if (data.success) {
            showSuccess('Job created successfully');
            closeCreateJobModal();
            refreshJobList();
        } else {
            showError(data.error || 'Failed to create job');
        }
    } catch (error) {
        console.error('Failed to create job:', error);
        showError('Failed to create job');
    }
}

// Job Actions
async function startJob(jobId) {
    try {
        const response = await fetch(`/api/translations/service/jobs/${jobId}/start/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken()
            }
        });

        const data = await response.json();

        if (data.success) {
            showSuccess('Job started');
            refreshJobList();
        } else {
            showError(data.error || 'Failed to start job');
        }
    } catch (error) {
        console.error('Failed to start job:', error);
        showError('Failed to start job');
    }
}

async function cancelJob(jobId) {
    if (!await AdminModal.confirm('Are you sure you want to cancel this job?')) {
        return;
    }

    try {
        const response = await fetch(`/api/translations/service/jobs/${jobId}/cancel/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken()
            }
        });

        const data = await response.json();

        if (data.success) {
            showSuccess('Job cancelled');
            refreshJobList();
        } else {
            showError(data.error || 'Failed to cancel job');
        }
    } catch (error) {
        console.error('Failed to cancel job:', error);
        showError('Failed to cancel job');
    }
}

async function retryJob(jobId) {
    try {
        const response = await fetch(`/api/translations/service/jobs/${jobId}/retry/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            },
            body: JSON.stringify({ execute_now: true })
        });

        const data = await response.json();

        if (data.success) {
            showSuccess('Job queued for retry');
            refreshJobList();
        } else {
            showError(data.error || 'Failed to retry job');
        }
    } catch (error) {
        console.error('Failed to retry job:', error);
        showError('Failed to retry job');
    }
}

// Job Details Modal
async function viewJobDetails(jobId) {
    try {
        const response = await fetch(`/api/translations/service/jobs/${jobId}/`);
        const data = await response.json();

        if (data.success) {
            showJobDetailsModal(data.job);
        } else {
            showError('Failed to load job details');
        }
    } catch (error) {
        console.error('Failed to load job details:', error);
        showError('Failed to load job details');
    }
}

function getStatusBadge(status) {
    const icons = {
        'pending': 'fa-clock',
        'processing': 'fa-spinner fa-spin',
        'completed': 'fa-check',
        'failed': 'fa-times',
        'cancelled': 'fa-ban'
    };

    const labels = {
        'pending': 'Pending',
        'processing': 'Processing',
        'completed': 'Completed',
        'failed': 'Failed',
        'cancelled': 'Cancelled'
    };

    return `
        <span class="status-badge status-${status}">
            <i class="fas ${icons[status] || 'fa-question'}"></i>
            ${labels[status] || status}
        </span>
    `;
}

function showJobDetailsModal(job) {
    const content = document.getElementById('job-details-content');
    content.innerHTML = `
        <div class="job-details">
            <h3>Job #${job.id}</h3>
            <div class="detail-row">
                <strong>Type:</strong> ${job.job_type}
            </div>
            <div class="detail-row">
                <strong>Status:</strong> ${getStatusBadge(job.status)}
            </div>
            <div class="detail-row">
                <strong>Progress:</strong> ${job.progress}%
            </div>
            <div class="detail-row">
                <strong>Languages:</strong> ${job.source_language} → ${job.target_languages.join(', ')}
            </div>
            <div class="detail-row">
                <strong>Provider:</strong> ${job.provider ? job.provider.name : 'Auto'}
            </div>
            <div class="detail-row">
                <strong>Created:</strong> ${new Date(job.created_at).toLocaleString()}
            </div>
            ${job.started_at ? `
                <div class="detail-row">
                    <strong>Started:</strong> ${new Date(job.started_at).toLocaleString()}
                </div>
            ` : ''}
            ${job.completed_at ? `
                <div class="detail-row">
                    <strong>Completed:</strong> ${new Date(job.completed_at).toLocaleString()}
                </div>
            ` : ''}
            ${job.error_message ? `
                <div class="detail-row error">
                    <strong>Error:</strong> ${job.error_message}
                </div>
            ` : ''}
        </div>
    `;

    document.getElementById('job-details-modal').classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
}

function closeJobDetailsModal() {
    document.getElementById('job-details-modal').classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
}

// Bulk Actions
function openBulkActionsMenu() {
    const menu = document.getElementById('bulk-actions-menu');
    const btn = document.getElementById('bulk-actions-btn');

    // Position menu below button
    const rect = btn.getBoundingClientRect();
    menu.style.top = rect.bottom + 'px';
    menu.style.left = rect.left + 'px';
    menu.style.display = 'block';

    // Close on click outside
    setTimeout(() => {
        document.addEventListener('click', closeBulkActionsMenu);
    }, 100);
}

function closeBulkActionsMenu() {
    document.getElementById('bulk-actions-menu').style.display = 'none';
    document.removeEventListener('click', closeBulkActionsMenu);
}

async function bulkCancel() {
    if (!await AdminModal.confirm(`Cancel ${selectedJobs.size} selected jobs?`)) {
        return;
    }
    await executeBulkJobAction('cancel');
}

async function bulkRetry() {
    if (!await AdminModal.confirm(`Retry ${selectedJobs.size} selected jobs?`)) {
        return;
    }
    await executeBulkJobAction('retry');
}

async function bulkDelete() {
    if (!await AdminModal.confirm({ message: `Delete ${selectedJobs.size} selected jobs? This action cannot be undone.`, danger: true, confirmText: 'Delete' })) {
        return;
    }
    await executeBulkJobAction('delete');
}

async function executeBulkJobAction(action) {
    closeBulkActionsMenu();
    showLoading();

    try {
        const response = await fetch('/api/translations/service/jobs/bulk-action/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            },
            body: JSON.stringify({
                action: action,
                job_ids: Array.from(selectedJobs)
            })
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            showSuccess(data.message || 'Action completed successfully');
            selectedJobs.clear();
            updateBulkActionUI();
            refreshJobList();
        } else {
            showError(data.error || 'Action failed');
        }
    } catch (error) {
        hideLoading();
        console.error('Bulk action failed:', error);
        showError('An error occurred while processing the action');
    }
}

// Utility Functions
function showLoading() {
    const container = document.getElementById('jobs-container');
    if (container) {
        container.style.opacity = '0.5';
    }
}

function hideLoading() {
    const container = document.getElementById('jobs-container');
    if (container) {
        container.style.opacity = '1';
    }
}

// Toast notification manager (matches provider_browse.js pattern)
const NotificationManager = {
    container: null,

    init() {
        this.container = document.getElementById('notification-container');
    },

    show(message, type, duration) {
        if (!this.container) this.init();
        if (!this.container) return;

        const notification = document.createElement('div');
        notification.className = 'provider-notification ' + type;

        const icons = { success: 'fa-check-circle', error: 'fa-exclamation-circle', info: 'fa-info-circle' };
        const labels = { success: 'Success', error: 'Error', info: 'Info' };

        const iconEl = document.createElement('i');
        iconEl.className = 'fas ' + (icons[type] || icons.info);

        const contentDiv = document.createElement('div');
        contentDiv.className = 'notification-content';

        const strong = document.createElement('strong');
        strong.textContent = labels[type] || labels.info;

        const p = document.createElement('p');
        p.textContent = message;

        contentDiv.appendChild(strong);
        contentDiv.appendChild(p);
        notification.appendChild(iconEl);
        notification.appendChild(contentDiv);

        this.container.appendChild(notification);

        if (duration > 0) {
            setTimeout(() => {
                notification.classList.add('d-none');
                setTimeout(() => notification.remove(), 300);
            }, duration);
        }
    }
};

function showSuccess(message) {
    NotificationManager.show(message, 'success', 5000);
}

function showError(message) {
    NotificationManager.show(message, 'error', 7000);
}

function showInfo(message) {
    NotificationManager.show(message, 'info', 5000);
}

/**
 * Event delegation handler for translation jobs
 */
function handleTranslationJobsActions(e) {
    const actionElement = e.target.closest('[data-action]');
    if (!actionElement) return;

    const action = actionElement.dataset.action;
    const jobId = actionElement.dataset.jobId ? parseInt(actionElement.dataset.jobId) : null;

    switch (action) {
        case 'open-create-job-modal':
            e.preventDefault();
            openCreateJobModal();
            break;
        case 'refresh-job-list':
            e.preventDefault();
            refreshJobList();
            break;
        case 'open-bulk-actions-menu':
            e.preventDefault();
            openBulkActionsMenu();
            break;
        case 'toggle-select-all':
            toggleSelectAll();
            break;
        case 'switch-tab':
            e.preventDefault();
            const tab = actionElement.dataset.tab;
            if (tab) switchTab(tab);
            break;
        case 'toggle-job-selection':
            if (jobId) toggleJobSelection(jobId);
            break;
        case 'start-job':
            e.preventDefault();
            if (jobId) startJob(jobId);
            break;
        case 'cancel-job':
            e.preventDefault();
            if (jobId) cancelJob(jobId);
            break;
        case 'retry-job':
            e.preventDefault();
            if (jobId) retryJob(jobId);
            break;
        case 'view-job-details':
            e.preventDefault();
            if (jobId) viewJobDetails(jobId);
            break;
        case 'previous-page':
            e.preventDefault();
            previousPage();
            break;
        case 'next-page':
            e.preventDefault();
            nextPage();
            break;
        case 'close-create-job-modal':
            e.preventDefault();
            closeCreateJobModal();
            break;
        case 'close-job-details-modal':
            e.preventDefault();
            closeJobDetailsModal();
            break;
        case 'bulk-cancel':
            e.preventDefault();
            bulkCancel();
            break;
        case 'bulk-retry':
            e.preventDefault();
            bulkRetry();
            break;
        case 'bulk-delete':
            e.preventDefault();
            bulkDelete();
            break;
    }
}

/**
 * Handle form submission
 */
function handleFormSubmit(e) {
    const formElement = e.target.closest('[data-action="submit-create-job"]');
    if (formElement) {
        e.preventDefault();
        submitCreateJob(e);
    }
}

// Set up event delegation when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', handleTranslationJobsActions);
    document.addEventListener('change', handleTranslationJobsActions);
    document.addEventListener('submit', handleFormSubmit);
});
