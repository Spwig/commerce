/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Upload Queue Manager for Media Library
 * Handles file uploads with progress tracking and job monitoring
 */

class UploadQueueManager {
    constructor(options = {}) {
        this.options = {
            maxConcurrent: 2,
            pollInterval: 2000,  // Poll job status every 2 seconds
            apiBase: this.getApiBaseUrl(),
            ...options
        };

        this.queue = [];
        this.activeUploads = new Map();
        this.processingJobs = new Map();
        this.isProcessing = false;
        this.pollTimer = null;
        this.completionCallbacks = [];

        this.init();
    }

    init() {
        // Create queue UI container
        this.createQueueUI();

        // Start polling for job updates
        this.startJobPolling();
    }

    createQueueUI() {
        // Remove existing queue UI if present
        const existingUI = document.querySelector('.upload-queue-container');
        if (existingUI) {
            existingUI.remove();
        }

        // Create queue container using utility-popup classes
        // Start hidden - will be shown when files are added to queue
        const container = document.createElement('div');
        container.className = 'upload-queue-container utility-popup hidden';
        container.innerHTML = `
            <div class="utility-header" style="cursor: grab;">
                <span class="utility-title"><i class="fas fa-upload"></i> Upload Queue</span>
                <div class="utility-tools">
                    <button class="util-btn util-btn-small queue-minimize" type="button" title="Minimize">
                        <i class="fas fa-minus"></i>
                    </button>
                    <button class="util-btn util-btn-small utility-close queue-close" type="button" title="Close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
            <div class="upload-queue-items utility-body"></div>
            <div class="upload-queue-summary utility-footer">
                <span class="queue-count">0 files</span>
                <button class="util-btn util-btn-small queue-clear-completed" type="button" title="Clear completed">
                    <i class="fas fa-redo"></i>
                </button>
            </div>
        `;

        document.body.appendChild(container);

        // Set initial state based on screen size
        if (window.innerWidth <= 640) {
            // Start minimized on mobile
            container.classList.add('minimized');
            container.querySelector('.queue-minimize i').className = 'fas fa-plus';
        }

        // Setup event listeners
        container.querySelector('.queue-minimize').addEventListener('click', () => {
            const isMinimized = container.classList.contains('minimized');
            const icon = container.querySelector('.queue-minimize i');

            if (isMinimized) {
                // Currently minimized, so expand
                container.classList.remove('minimized');
                container.classList.add('user-expanded');
                icon.className = 'fas fa-minus';
            } else {
                // Currently expanded, so minimize
                container.classList.add('minimized');
                container.classList.remove('user-expanded');
                icon.className = 'fas fa-plus';
            }
        });

        container.querySelector('.queue-close').addEventListener('click', async () => {
            if (this.hasActiveUploads()) {
                if (!await AdminModal.confirm('There are active uploads. Are you sure you want to close?')) {
                    return;
                }
            }
            this.destroy();
        });

        container.querySelector('.queue-clear-completed').addEventListener('click', () => {
            this.clearCompleted();
        });

        // Make the popup draggable
        this.makeDraggable(container);

        this.container = container;
        this.itemsContainer = container.querySelector('.upload-queue-items');
    }

    addToQueue(files) {
        const container = document.querySelector('.upload-queue-container');
        if (container) {
            container.classList.remove('hidden');
            container.classList.remove('minimized');
        }

        for (const file of files) {
            const queueItem = {
                id: this.generateId(),
                file: file,
                status: 'pending',
                progress: 0,
                jobId: null
            };

            this.queue.push(queueItem);
            this.createQueueItemUI(queueItem);
        }

        this.updateSummary();

        if (!this.isProcessing) {
            this.processQueue();
        }
    }

    createQueueItemUI(item) {
        const element = document.createElement('div');
        element.className = 'queue-item';
        element.dataset.itemId = item.id;

        const isVideo = item.file.type.startsWith('video/');
        const icon = isVideo ? '<i class="fas fa-video"></i>' : '<i class="fas fa-image"></i>';

        element.innerHTML = `
            <div class="queue-item-info">
                <span class="queue-item-icon">${icon}</span>
                <div class="queue-item-details">
                    <div class="queue-item-name">${this.truncateFilename(item.file.name, 30)}</div>
                    <div class="queue-item-size">${this.formatFileSize(item.file.size)}</div>
                </div>
            </div>
            <div class="queue-item-progress">
                <div class="progress-bar">
                    <div class="progress-fill" style="width: 0%"></div>
                </div>
                <span class="progress-text">Waiting...</span>
            </div>
            <div class="queue-item-actions">
                <button class="queue-item-cancel" title="Cancel">×</button>
            </div>
        `;

        // Add cancel handler
        element.querySelector('.queue-item-cancel').addEventListener('click', () => {
            this.cancelItem(item);
        });

        this.itemsContainer.appendChild(element);
    }

    async processQueue() {
        if (this.queue.length === 0 || this.activeUploads.size >= this.options.maxConcurrent) {
            this.isProcessing = false;
            return;
        }

        this.isProcessing = true;

        // Get next pending item
        const item = this.queue.find(i => i.status === 'pending');
        if (!item) {
            this.isProcessing = false;
            return;
        }

        // Start upload
        item.status = 'uploading';
        this.updateItemUI(item, 'Uploading...', 0);

        try {
            const jobId = await this.uploadFile(item);

            if (jobId) {
                // Async processing - track the job
                item.jobId = jobId;
                item.status = 'processing';
                this.processingJobs.set(jobId, item);
                this.updateItemUI(item, 'Processing...', 50);
            } else {
                // If no jobId, the file was already marked as completed in uploadFile
                // Trigger completion callbacks to refresh the gallery
                this.triggerCompletionCallbacks();
            }

        } catch (error) {
            item.status = 'failed';
            this.updateItemUI(item, `Failed: ${error.message}`, 0, 'error');
        } finally {
            this.activeUploads.delete(item.id);
        }

        // Process next item
        setTimeout(() => this.processQueue(), 100);
    }

    async uploadFile(item) {
        const formData = new FormData();
        formData.append('original_file', item.file);
        formData.append('title', item.file.name.split('.')[0]);

        // Track upload progress using XMLHttpRequest
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();

            // Track upload progress
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percentComplete = Math.round((e.loaded / e.total) * 100);
                    this.updateItemUI(item, `Uploading... ${percentComplete}%`, percentComplete * 0.5);
                }
            });

            xhr.addEventListener('load', () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        console.log('Upload response:', response); // Debug logging

                        // Check if we have a job_id for async processing
                        if (response.job_id) {
                            // Check if the job is already completed
                            if (response.job_status === 'completed') {
                                // Job completed synchronously
                                item.status = 'completed';
                                item.asset = response;
                                this.updateItemUI(item, 'Completed', 100, 'success');
                                this.triggerUploadComplete(item, response);
                                resolve(null);
                            } else {
                                // Job needs polling
                                resolve(response.job_id);
                            }
                        } else {
                            // No job ID means processing completed synchronously
                            item.status = 'completed';
                            item.asset = response;
                            this.updateItemUI(item, 'Completed', 100, 'success');
                            this.triggerUploadComplete(item, response);
                            resolve(null);
                        }
                    } catch (error) {
                        console.error('Error parsing response:', error);
                        // If JSON parsing fails, mark as completed
                        item.status = 'completed';
                        this.updateItemUI(item, 'Completed', 100, 'success');
                        resolve(null);
                    }
                } else {
                    reject(new Error(`Upload failed: ${xhr.statusText}`));
                }
            });

            xhr.addEventListener('error', () => {
                reject(new Error('Network error during upload'));
            });

            xhr.open('POST', `${this.options.apiBase}/assets/`);
            xhr.setRequestHeader('X-CSRFToken', this.getCSRFToken());

            this.activeUploads.set(item.id, xhr);
            xhr.send(formData);
        });
    }

    async pollJobStatus() {
        if (this.processingJobs.size === 0) return;

        console.log('Polling for jobs:', Array.from(this.processingJobs.keys()));

        try {
            const response = await fetch(`${this.options.apiBase}/jobs/active/`, {
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (!response.ok) {
                console.error('Failed to poll jobs:', response.status);
                return;
            }

            const data = await response.json();
            console.log('Active jobs response:', data);

            for (const job of data.jobs) {
                const item = this.processingJobs.get(job.id);
                if (!item) continue;

                // Update item based on job status
                if (job.status === 'completed') {
                    item.status = 'completed';
                    item.asset = job;
                    this.updateItemUI(item, 'Completed', 100, 'success');
                    this.processingJobs.delete(job.id);
                    // Trigger individual upload completion
                    this.triggerUploadComplete(item, job);
                    // Trigger completion callbacks
                    this.triggerCompletionCallbacks();
                } else if (job.status === 'failed') {
                    item.status = 'failed';
                    this.updateItemUI(item, 'Failed', 0, 'error');
                    this.processingJobs.delete(job.id);
                } else {
                    // Update progress
                    let statusText = job.status_message || job.status;
                    if (job.status === 'converting') {
                        statusText = `Converting to WebM/AV1... ${job.progress}%`;
                    } else if (job.status === 'generating_thumbnails') {
                        statusText = `Generating thumbnails... ${job.progress}%`;
                    }

                    const progress = 50 + (job.progress * 0.5);
                    this.updateItemUI(item, statusText, progress);
                }
            }
        } catch (error) {
            console.error('Error polling job status:', error);
        }
    }

    updateItemUI(item, statusText, progress, statusClass = null) {
        const element = this.itemsContainer.querySelector(`[data-item-id="${item.id}"]`);
        if (!element) return;

        const progressFill = element.querySelector('.progress-fill');
        const progressText = element.querySelector('.progress-text');

        progressFill.style.width = `${progress}%`;
        progressText.textContent = statusText;

        // Update status class
        element.className = 'queue-item';
        if (statusClass) {
            element.classList.add(`queue-item-${statusClass}`);
        } else if (item.status) {
            element.classList.add(`queue-item-${item.status}`);
        }

        // Hide cancel button for completed/failed items
        if (item.status === 'completed' || item.status === 'failed') {
            element.querySelector('.queue-item-cancel').style.display = 'none';
        }

        this.updateSummary();
    }

    cancelItem(item) {
        if (item.status === 'uploading') {
            const xhr = this.activeUploads.get(item.id);
            if (xhr) {
                xhr.abort();
                this.activeUploads.delete(item.id);
            }
        } else if (item.status === 'processing' && item.jobId) {
            // Cancel processing job
            this.cancelJob(item.jobId);
            this.processingJobs.delete(item.jobId);
        }

        item.status = 'cancelled';
        this.updateItemUI(item, 'Cancelled', 0, 'cancelled');
    }

    async cancelJob(jobId) {
        try {
            await fetch(`${this.options.apiBase}/jobs/${jobId}/cancel/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });
        } catch (error) {
            console.error('Error cancelling job:', error);
        }
    }

    clearCompleted() {
        const completedItems = this.queue.filter(
            item => item.status === 'completed' || item.status === 'failed' || item.status === 'cancelled'
        );

        completedItems.forEach(item => {
            const element = this.itemsContainer.querySelector(`[data-item-id="${item.id}"]`);
            if (element) {
                element.remove();
            }

            const index = this.queue.indexOf(item);
            if (index > -1) {
                this.queue.splice(index, 1);
            }
        });

        this.updateSummary();
    }

    updateSummary() {
        const summary = this.container.querySelector('.queue-count');
        const active = this.queue.filter(i =>
            i.status === 'pending' || i.status === 'uploading' || i.status === 'processing'
        ).length;

        const completed = this.queue.filter(i => i.status === 'completed').length;
        const failed = this.queue.filter(i => i.status === 'failed').length;

        let text = '';
        if (active > 0) text += `${active} active`;
        if (completed > 0) text += (text ? ', ' : '') + `${completed} completed`;
        if (failed > 0) text += (text ? ', ' : '') + `${failed} failed`;

        summary.textContent = text || 'No files';
    }

    startJobPolling() {
        if (this.pollTimer) return;

        this.pollTimer = setInterval(() => {
            this.pollJobStatus();
        }, this.options.pollInterval);
    }

    stopJobPolling() {
        if (this.pollTimer) {
            clearInterval(this.pollTimer);
            this.pollTimer = null;
        }
    }

    hasActiveUploads() {
        return this.queue.some(item =>
            item.status === 'pending' || item.status === 'uploading' || item.status === 'processing'
        );
    }

    makeDraggable(container) {
        const header = container.querySelector('.utility-header');
        let isDragging = false;
        let currentX;
        let currentY;
        let initialX;
        let initialY;
        let xOffset = 0;
        let yOffset = 0;

        const dragStart = (e) => {
            if (e.type === "touchstart") {
                initialX = e.touches[0].clientX - xOffset;
                initialY = e.touches[0].clientY - yOffset;
            } else {
                initialX = e.clientX - xOffset;
                initialY = e.clientY - yOffset;
            }

            if (e.target === header || header.contains(e.target)) {
                isDragging = true;
                container.style.transition = 'none';
            }
        };

        const dragEnd = (e) => {
            initialX = currentX;
            initialY = currentY;
            isDragging = false;
            container.style.transition = '';
        };

        const drag = (e) => {
            if (!isDragging) return;

            e.preventDefault();

            if (e.type === "touchmove") {
                currentX = e.touches[0].clientX - initialX;
                currentY = e.touches[0].clientY - initialY;
            } else {
                currentX = e.clientX - initialX;
                currentY = e.clientY - initialY;
            }

            xOffset = currentX;
            yOffset = currentY;

            // Apply transform to move the container
            container.style.transform = `translate(${currentX}px, ${currentY}px)`;
        };

        // Add event listeners
        header.addEventListener('mousedown', dragStart);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', dragEnd);

        // Touch events for mobile
        header.addEventListener('touchstart', dragStart);
        document.addEventListener('touchmove', drag);
        document.addEventListener('touchend', dragEnd);
    }

    destroy() {
        this.stopJobPolling();

        // Cancel all active uploads
        this.activeUploads.forEach((xhr) => {
            xhr.abort();
        });

        if (this.container) {
            this.container.remove();
        }
    }

    // Utility methods
    generateId() {
        return `upload-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    }

    getCSRFToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }

    getApiBaseUrl() {
        // API is outside i18n_patterns, no language prefix needed
        return '/api/media';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
    }

    truncateFilename(filename, maxLength) {
        if (filename.length <= maxLength) return filename;

        const ext = filename.split('.').pop();
        const nameWithoutExt = filename.slice(0, -(ext.length + 1));
        const truncatedName = nameWithoutExt.slice(0, maxLength - ext.length - 4) + '...';

        return `${truncatedName}.${ext}`;
    }

    // Event handling methods
    onComplete(callback) {
        if (typeof callback === 'function') {
            this.completionCallbacks.push(callback);
        }
    }

    triggerUploadComplete(item, asset) {
        // Call the individual upload complete callback if it exists
        if (this.onUploadComplete && typeof this.onUploadComplete === 'function') {
            try {
                this.onUploadComplete(asset);
            } catch (error) {
                console.error('Error in onUploadComplete callback:', error);
            }
        }
    }

    triggerCompletionCallbacks() {
        // Check if all jobs are complete
        const hasActiveJobs = this.queue.some(item =>
            item.status === 'pending' || item.status === 'uploading' || item.status === 'processing'
        );

        if (!hasActiveJobs && this.completionCallbacks.length > 0) {
            // Trigger all callbacks
            this.completionCallbacks.forEach(callback => {
                try {
                    callback();
                } catch (error) {
                    console.error('Error in completion callback:', error);
                }
            });
        }
    }
}

// Export for use
window.UploadQueueManager = UploadQueueManager;