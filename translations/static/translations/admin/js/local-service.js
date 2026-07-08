/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Local Translation Service Management
 * Handles AI model installation, activation, and quality settings
 */

(function() {
    'use strict';

    let currentModelTab = 'm2m100_418m';

    /**
     * Progressive loading with AJAX
     */
    function initializeService() {
        // Initialize dynamic widths from data attributes (CSP-safe)
        document.querySelectorAll('[data-width]').forEach(function(el) {
            el.style.width = el.dataset.width + '%';
        });

        const loadingMessage = document.getElementById('loading-message');

        // Update loading message
        if (loadingMessage) {
            loadingMessage.innerHTML = document.documentElement.lang === 'en' ?
                'Connecting to translation service...' : loadingMessage.innerHTML;
        }

        // Get data URL from template
        const serviceDataUrl = (document.getElementById('translations-config') || document.body).dataset.serviceDataUrl;
        if (!serviceDataUrl) {
            console.error('Service data URL not configured');
            return;
        }

        // Fetch the service data
        fetch(serviceDataUrl, {
            credentials: 'same-origin',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Failed to load service data');
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);

            try {
                // Update the page with received data
                updatePageContent(data);
            } catch (updateError) {
                console.error('Error updating page content:', updateError);
            }

            // Always hide loading overlay and show content, even if update fails
            const loadingOverlay = document.getElementById('loading-overlay');
            const serviceContainer = document.getElementById('service-container');
            const loadingStyle = document.getElementById('loading-overlay-style');

            // Remove the style element that forces display: flex !important
            if (loadingStyle) {
                loadingStyle.remove();
                console.log('Removed loading overlay style');
            }

            if (loadingOverlay) {
                console.log('Hiding loading overlay');
                loadingOverlay.style.display = 'none';
            }
            if (serviceContainer) {
                console.log('Showing service container');
                serviceContainer.classList.add('loaded');
            }
        })
        .catch(error => {
            console.error('Error loading service data:', error);
            const loadingOverlay = document.getElementById('loading-overlay');
            if (loadingOverlay) {
                loadingOverlay.innerHTML = `
                    <div class="error-display">
                        <i class="fas fa-exclamation-triangle"></i>
                        <h3>Failed to Load Service Data</h3>
                        <p>${error.message}</p>
                        <button class="button default" data-action="reload">
                            <i class="fas fa-refresh"></i> Retry
                        </button>
                    </div>
                `;
            }
        });
    }

    /**
     * Function to update page content with AJAX data
     */
    function updatePageContent(data) {
        try {
            // Update service status box
            const serviceStatus = document.querySelector('.service-status');
            if (serviceStatus && data.service_status) {
                serviceStatus.className = 'service-status ' + data.service_status.class;
                serviceStatus.innerHTML = data.service_status.html;
            }

            // Update quality cards for each model
            if (data.quality_settings) {
                Object.keys(data.quality_settings).forEach(modelId => {
                    const settingsDiv = document.getElementById(modelId + '-settings');
                    if (settingsDiv) {
                        const qualityGrid = settingsDiv.querySelector('.quality-grid');
                        if (qualityGrid) {
                            try {
                                qualityGrid.innerHTML = data.quality_settings[modelId].map(quality =>
                                    generateQualityCard(modelId, quality)
                                ).join('');
                            } catch (e) {
                                console.error('Error generating quality cards for', modelId, e);
                            }
                        }
                    }
                });
            }

            // Update disk usage
            if (data.disk_usage) {
                const diskUsage = document.querySelector('.disk-usage');
                if (diskUsage) {
                    try {
                        diskUsage.innerHTML = generateDiskUsage(data.disk_usage);
                        // Apply dynamic widths from data attributes (CSP-safe)
                        diskUsage.querySelectorAll('[data-width]').forEach(function(el) {
                            el.style.width = el.dataset.width + '%';
                        });
                    } catch (e) {
                        console.error('Error updating disk usage:', e);
                    }
                }
            }
        } catch (e) {
            console.error('Error in updatePageContent:', e);
        }
    }

    /**
     * Generate quality metrics HTML
     */
    function generateQualityMetrics(quant, modelId) {
        const speedIcon = quant === 'int8' ? 'rocket' : quant === 'int16' ? 'plane' : quant === 'float16' ? 'walking' : 'turtle';
        const starCount = quant === 'int8' ? 2 : quant === 'int16' ? 3 : quant === 'float16' ? 4 : 5;
        const memSize = quant === 'float32' ? 1.6 : (quant === 'float16' || quant === 'int16') ? 0.8 : 0.4;

        // Adjust memory size based on model
        let adjustedMemSize = memSize;
        if (modelId === 'm2m100_1.2b') {
            adjustedMemSize = memSize * 3; // 1.2B model uses 3x more memory
        } else if (modelId === 'nllb_200') {
            adjustedMemSize = memSize * 1.5; // NLLB uses 1.5x more memory
        }

        let stars = '';
        for (let i = 0; i < starCount; i++) {
            stars += '<i class="fas fa-star"></i>';
        }

        return `
            <div class="metric">
                <span class="metric-icon"><i class="fas fa-${speedIcon}"></i></span>
                <span class="metric-label">Speed</span>
            </div>
            <div class="metric">
                <span class="metric-icon">${stars}</span>
                <span class="metric-label">Quality</span>
            </div>
            <div class="metric">
                <span class="metric-icon"><i class="fas fa-hdd"></i></span>
                <span class="metric-label">~${adjustedMemSize.toFixed(1)}GB</span>
            </div>
        `;
    }

    /**
     * Generate quality card HTML
     */
    function generateQualityCard(modelId, quality) {
        const icons = {
            'int8': 'fas fa-bolt',
            'int16': 'fas fa-balance-scale',
            'float16': 'fas fa-bullseye',
            'float32': 'fas fa-trophy'
        };

        const titles = {
            'int8': 'Speed Priority',
            'int16': 'Balanced',
            'float16': 'Quality Focus',
            'float32': 'Maximum Quality'
        };

        return `
            <div class="quality-card ${quality.is_active ? 'active' : (quality.is_available ? 'available' : '')} ${!quality.is_supported ? 'hardware-unsupported' : ''}"
                 data-model="${modelId}" data-quant="${quality.name}"
                 ${!quality.is_supported ? 'data-unsupported-message="⚠️ Hardware incompatible"' : ''}>
                ${quality.is_active ? '<span class="available-badge active"><i class="fas fa-play-circle"></i> Active</span>' :
                  quality.is_available ? '<span class="available-badge"><i class="fas fa-check"></i> Available</span>' : ''}
                <h4 class="quality-title"><i class="${icons[quality.name]}"></i> ${titles[quality.name]}</h4>
                <p class="quality-subtitle">${quality.subtitle}</p>
                <div class="quality-metrics">
                    ${generateQualityMetrics(quality.name, modelId)}
                </div>
                <p class="quality-size">${quality.description}</p>
                ${!quality.is_supported ? '<p class="quality-error"><i class="fas fa-exclamation-triangle"></i> ' + quality.error_message + '</p>' : ''}
                ${quality.is_active ?
                    '<button class="deletelink" data-action="unload-model"><i class="fas fa-power-off"></i> Deactivate</button>' :
                  quality.is_available ?
                    `<button class="button default" data-action="activate-quality" data-model-id="${modelId}" data-quality="${quality.name}">Activate</button>` :
                    `<button class="button default" data-action="install-and-activate" data-model-id="${modelId}" data-quality="${quality.name}">
                        <i class="${quality.model_downloaded ? 'fas fa-cog' : 'fas fa-download'}"></i>
                        ${quality.model_downloaded ? 'Install & Activate' : 'Install & Activate'}
                    </button>`}
            </div>
        `;
    }

    /**
     * Generate disk usage HTML
     */
    function generateDiskUsage(disk) {
        const modelsPercent = disk.disk_total_gb > 0 ? Math.round((disk.disk_usage_gb / disk.disk_total_gb) * 100) : 0;
        const otherPercent = disk.disk_total_gb > 0 ? Math.round((disk.system_used_gb / disk.disk_total_gb) * 100) : 0;
        const displayPercent = disk.disk_usage_gb > 0 && modelsPercent === 0 ? 1 : modelsPercent;

        return `
            <h3><i class="fas fa-hdd"></i> Storage Usage</h3>
            <div>
                <strong>Models:</strong> ${disk.disk_usage_gb.toFixed(1)} GB
                | <strong>Free Space:</strong> ${disk.disk_free_gb.toFixed(1)} GB
                | <strong>Total:</strong> ${disk.disk_total_gb.toFixed(1)} GB
            </div>
            <div class="disk-bar">
                ${disk.disk_total_gb > 0 ? `
                    <div class="disk-segment disk-other" data-width="${otherPercent}" title="Other files: ${disk.system_used_gb.toFixed(1)}GB"></div>
                    <div class="disk-segment disk-models" data-width="${displayPercent}" title="Translation models: ${disk.disk_usage_gb.toFixed(1)}GB"></div>
                    <div class="disk-segment disk-free" title="Free space: ${disk.disk_free_gb.toFixed(1)}GB"></div>
                ` : '<div class="disk-segment disk-free disk-free--full"></div>'}
            </div>
            <small>
                ${disk.disk_free_gb < 3 ?
                    '<span class="status-warning"><i class="fas fa-exclamation-triangle"></i> Low disk space! Consider removing unused models.</span>' :
                    '<span class="status-check"><i class="fas fa-check-circle"></i> Sufficient disk space available.</span>'}
            </small>
        `;
    }

    /**
     * Get CSRF token via AdminUtils
     */
    function getCsrfToken() {
        return AdminUtils.getCsrfToken();
    }

    /**
     * Model tab switching
     */
    function switchModelTab(modelId) {
        // Update tab buttons
        document.querySelectorAll('.admin-tab-btn').forEach(btn => {
            if (btn.dataset.model === modelId) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });

        // Update content
        document.querySelectorAll('.admin-tab-content').forEach(content => {
            content.classList.remove('active');
        });

        const targetContent = document.getElementById(modelId + '-settings');
        if (targetContent) {
            targetContent.classList.add('active');
        }

        currentModelTab = modelId;
    }

    /**
     * Unload current model
     */
    async function unloadModel() {
        if (!await AdminModal.confirm('Deactivate the current translation model?')) return;

        const btn = event.target;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deactivating...';

        fetch('/translator-api/model/unload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'unloaded') {
                location.reload();
            } else {
                AdminModal.alert({message: 'Failed to unload model', type: 'error'});
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-power-off"></i> Deactivate';
            }
        })
        .catch(error => {
            AdminModal.alert({message: 'Error: ' + error, type: 'error'});
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-power-off"></i> Deactivate';
        });
    }

    /**
     * Activate an already installed quantization
     */
    function activateQuality(modelId, quality) {
        const btn = event.target;
        const card = btn.closest('.quality-card');

        // Check if hardware supports this quantization
        if (card && card.classList.contains('hardware-unsupported')) {
            AdminModal.alert({message: 'This quality setting is not supported on your current hardware.', type: 'warning'});
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Activating...';

        const quantizationSetUrl = (document.getElementById('translations-config') || document.body).dataset.quantizationSetUrl;
        if (!quantizationSetUrl) {
            console.error('Quantization set URL not configured');
            return;
        }

        // This would call an endpoint to load the model
        fetch(quantizationSetUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'quantization=' + quality + '&model=' + modelId
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                AdminModal.alert({message: data.error || 'Failed to activate', type: 'error'});
                btn.disabled = false;
                btn.innerHTML = 'Activate';
            }
        })
        .catch(error => {
            AdminModal.alert({message: 'Error: ' + error, type: 'error'});
            btn.disabled = false;
            btn.innerHTML = 'Activate';
        });
    }

    /**
     * Install and activate a model/quantization
     */
    async function installAndActivate(modelId, quality) {
        const btn = event.target;
        const card = btn.closest('.quality-card');

        // Check if hardware supports this quantization
        if (card && card.classList.contains('hardware-unsupported')) {
            AdminModal.alert({message: 'This quality setting is not supported on your current hardware.', type: 'warning'});
            return;
        }

        if (!await AdminModal.confirm('Install and activate this translation model?')) return;
        const originalContent = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Installing...';
        card.classList.add('downloading');

        // Create progress element using theme styles
        const progressDiv = document.createElement('div');
        progressDiv.className = 'progress-wrapper';
        progressDiv.innerHTML = `
            <div class="progress-label">
                <span class="progress-message">Starting download...</span>
                <span class="progress-value">0%</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar active" data-width="0" id="progress-${modelId}-${quality}">
                    <span class="progress-text"></span>
                </div>
            </div>
        `;
        card.appendChild(progressDiv);

        const startDownloadUrl = (document.getElementById('translations-config') || document.body).dataset.startDownloadUrl;
        if (!startDownloadUrl) {
            console.error('Start download URL not configured');
            return;
        }

        // Start download
        fetch(startDownloadUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'model=' + modelId + '&quantization=' + quality
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Poll for download completion
                progressDiv.querySelector('.progress-message').textContent = 'Downloading model...';
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Downloading...';
                pollDownloadStatus(modelId, quality, btn, originalContent, progressDiv, card);
            } else {
                AdminModal.alert({message: data.error || 'Failed to start download', type: 'error'});
                btn.disabled = false;
                btn.innerHTML = originalContent;
                card.classList.remove('downloading');
                card.removeChild(progressDiv);
            }
        })
        .catch(error => {
            AdminModal.alert({message: 'Error: ' + error, type: 'error'});
            btn.disabled = false;
            btn.innerHTML = originalContent;
            card.classList.remove('downloading');
            if (progressDiv.parentNode === card) {
                card.removeChild(progressDiv);
            }
        });
    }

    /**
     * Poll download status
     */
    function pollDownloadStatus(modelId, quality, btn, originalContent, progressDiv, card) {
        const downloadStatusUrl = (document.getElementById('translations-config') || document.body).dataset.downloadStatusUrl;
        const quantizationSetUrl = (document.getElementById('translations-config') || document.body).dataset.quantizationSetUrl;

        const interval = setInterval(() => {
            fetch(downloadStatusUrl + '?model=' + modelId, {
                credentials: 'same-origin',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
                .then(response => {
                    if (!response.ok) {
                        console.error('Download status response not OK:', response.status);
                        throw new Error('Status response not OK');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Download status data:', data);

                    // Handle error responses from Django
                    if (data.error) {
                        console.error('Download status error:', data.error);
                        return;
                    }

                    if (data.status === 'completed' || data.status === 'complete') {
                        clearInterval(interval);
                        // Update progress to 100%
                        progressDiv.querySelector('.progress-message').textContent = 'Download complete! Activating...';
                        progressDiv.querySelector('.progress-bar').style.width = '100%';
                        progressDiv.querySelector('.progress-bar').classList.remove('warning');
                        progressDiv.querySelector('.progress-bar').classList.add('success');
                        progressDiv.querySelector('.progress-value').textContent = '100%';

                        // Now activate it
                        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Activating...';

                        // Activate the quality setting
                        fetch(quantizationSetUrl, {
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': getCsrfToken(),
                                'Content-Type': 'application/x-www-form-urlencoded'
                            },
                            body: 'quantization=' + quality + '&model=' + modelId
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                progressDiv.querySelector('.progress-message').textContent = 'Success! Reloading...';
                                setTimeout(() => location.reload(), 1500);
                            } else {
                                throw new Error(data.error || 'Activation failed');
                            }
                        })
                        .catch(error => {
                            AdminModal.alert({message: 'Error: ' + error, type: 'error'});
                            btn.disabled = false;
                            btn.innerHTML = originalContent;
                            card.classList.remove('downloading');
                            card.removeChild(progressDiv);
                        });
                    } else if (data.status === 'failed') {
                        clearInterval(interval);
                        AdminModal.alert({message: 'Download failed', type: 'error'});
                        btn.disabled = false;
                        btn.innerHTML = originalContent;
                        card.classList.remove('downloading');
                        card.removeChild(progressDiv);
                    } else if (data.progress !== undefined && data.progress !== null) {
                        // Update progress bar
                        const progress = Math.round(data.progress);
                        console.log('Updating progress to:', progress + '%');

                        const progressBar = progressDiv.querySelector('.progress-bar');
                        const progressValue = progressDiv.querySelector('.progress-value');

                        if (progressBar) {
                            progressBar.style.width = progress + '%';
                            console.log('Progress bar width set to:', progress + '%');
                        } else {
                            console.error('Progress bar element not found');
                        }

                        if (progressValue) {
                            progressValue.textContent = progress + '%';
                        } else {
                            console.error('Progress value element not found');
                        }

                        // Update message based on status
                        if (data.status === 'converting') {
                            progressDiv.querySelector('.progress-message').textContent = 'Converting model...';
                            progressDiv.querySelector('.progress-bar').classList.add('warning');
                            btn.innerHTML = '<i class="fas fa-cog fa-spin"></i> Converting...';
                        } else {
                            progressDiv.querySelector('.progress-message').textContent = 'Downloading model...';
                            btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Downloading... ${progress}%`;
                        }
                    } else if (data.status === 'idle') {
                        // Download might have completed very quickly (cached model)
                        console.log('Download status is idle - checking if model exists');
                    }
                })
                .catch((error) => {
                    console.error('Error polling download status:', error);
                    clearInterval(interval);
                    btn.disabled = false;
                    btn.innerHTML = originalContent;
                    card.classList.remove('downloading');
                    if (progressDiv.parentNode === card) {
                        card.removeChild(progressDiv);
                    }
                });
        }, 2000);
    }

    /**
     * Handle local service actions via delegation
     */
    function handleLocalServiceActions(e) {
        const actionElement = e.target.closest('[data-action]');
        if (!actionElement) return;

        const action = actionElement.dataset.action;

        switch (action) {
            case 'reload':
                e.preventDefault();
                location.reload();
                break;
            case 'switch-model-tab':
                e.preventDefault();
                const modelId = actionElement.dataset.model;
                if (modelId) switchModelTab(modelId);
                break;
            case 'unload-model':
                e.preventDefault();
                unloadModel();
                break;
            case 'activate-quality':
                e.preventDefault();
                const activateModelId = actionElement.dataset.modelId;
                const activateQuality = actionElement.dataset.quality;
                if (activateModelId && activateQuality) {
                    activateQuality(activateModelId, activateQuality);
                }
                break;
            case 'install-and-activate':
                e.preventDefault();
                const iaaModelId = actionElement.dataset.modelId;
                const iaaQuality = actionElement.dataset.quality;
                if (iaaModelId && iaaQuality) {
                    installAndActivate(iaaModelId, iaaQuality);
                }
                break;
        }
    }

    // Show loading overlay immediately (before DOM ready)
    (function() {
        const style = document.createElement('style');
        style.textContent = '#loading-overlay { display: flex !important; }';
        style.id = 'loading-overlay-style';
        document.head.appendChild(style);
    })();

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initializeService();
            document.addEventListener('click', handleLocalServiceActions);
        });
    } else {
        initializeService();
        document.addEventListener('click', handleLocalServiceActions);
    }

})();
