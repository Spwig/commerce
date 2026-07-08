/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Image Processing - Thumbnail Configuration and Regeneration
 * Standalone page for managing thumbnail sizes, image stats, and regeneration.
 */
(function() {
    'use strict';

    // Read URL configuration from data island
    const dataEl = document.getElementById('image-processing-data');
    let urls = {};
    if (dataEl) {
        try {
            const config = JSON.parse(dataEl.textContent);
            urls = config.urls || {};
        } catch (e) {
            console.error('[Image Processing] Failed to parse config:', e);
        }
    }

    // Store sizes data globally for editing
    let thumbnailSizesData = [];

    // Global polling interval
    let statusPollInterval = null;

    document.addEventListener('DOMContentLoaded', function() {
        loadThumbnailConfiguration();
        loadImageStats();
        checkRegenerationStatus();
        loadLastRegenerationInfo();
    });

    function buildUrl(path) {
        // URLs are already absolute from the data island
        return path;
    }

    function getCsrfToken() {
        if (typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken) {
            return AdminUtils.getCsrfToken();
        }
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input) return input.value;
        return '';
    }

    // Load and display configured thumbnail sizes
    function loadThumbnailConfiguration() {
        const container = document.getElementById('thumbnail-sizes-display');
        const noteEl = document.getElementById('thumbnail-config-note');
        const manageSection = document.getElementById('manage-sizes-section');

        if (!container) return;

        fetch(buildUrl(urls.thumbnailSizes))
            .then(response => response.json())
            .then(data => {
                const sizes = data.thumbnail_sizes || {};
                const entries = Object.entries(sizes);
                thumbnailSizesData = data.sizes_detail || [];

                if (data.has_db_sizes) {
                    noteEl.innerHTML = '<i class="fas fa-database"></i> Sizes are managed in the database. <a href="#" class="toggle-manage-link">Edit sizes below</a>';
                    noteEl.querySelector('.toggle-manage-link').addEventListener('click', function(e) {
                        e.preventDefault();
                        toggleManageSizes();
                    });
                    if (manageSection) manageSection.style.display = 'block';
                    loadThumbnailEditor();
                } else {
                    noteEl.innerHTML = '<i class="fas fa-file-code"></i> These sizes are configured in <code>settings.py</code>';
                }

                if (entries.length === 0) {
                    container.innerHTML = '<div class="images-empty-state">No thumbnail sizes configured</div>';
                    return;
                }

                container.innerHTML = entries.map(([name, [width, height]]) => `
                    <div class="thumbnail-size-card">
                        <div class="thumbnail-size-icon">
                            <i class="fas fa-image"></i>
                        </div>
                        <div class="thumbnail-size-name">
                            ${name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                        </div>
                        <div class="thumbnail-size-dimensions">
                            ${width} × ${height}px
                        </div>
                    </div>
                `).join('');
            })
            .catch(error => {
                console.error('Error loading thumbnail sizes:', error);
                container.innerHTML = '<div class="images-empty-state images-error">Error loading thumbnail configuration</div>';
            });
    }

    // Load thumbnail editor
    function loadThumbnailEditor() {
        const editor = document.getElementById('thumbnail-sizes-editor');
        if (!editor || thumbnailSizesData.length === 0) return;

        editor.innerHTML = `
            <div class="thumbnail-editor-wrapper">
                <table class="thumbnail-editor-table">
                    <thead>
                        <tr>
                            <th>Type</th>
                            <th>Active</th>
                            <th>Display Name</th>
                            <th>Name (Key)</th>
                            <th>Width</th>
                            <th>Height</th>
                            <th>Description</th>
                            <th>Order</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${thumbnailSizesData.map(size => {
                            const isSystemPreset = size.is_system_preset || false;
                            const readonlyAttr = isSystemPreset ? 'readonly class="system-preset-field"' : '';
                            const deleteButtonHtml = isSystemPreset
                                ? '<span class="system-lock-icon" title="System presets cannot be deleted"><i class="fas fa-lock"></i></span>'
                                : `<button type="button" class="delete-size-btn" data-size-id="${size.id}" title="Delete"><i class="fas fa-trash"></i></button>`;
                            const typeLabel = isSystemPreset
                                ? '<span class="preset-badge preset-badge-system"><i class="fas fa-lock"></i> System</span>'
                                : '<span class="preset-badge preset-badge-custom">Custom</span>';

                            return `
                            <tr data-size-id="${size.id}" ${isSystemPreset ? 'data-system-preset="true"' : ''}>
                                <td>${typeLabel}</td>
                                <td><input type="checkbox" ${size.is_active ? 'checked' : ''} data-field="is_active"></td>
                                <td><input type="text" value="${size.display_name}" data-field="display_name" ${readonlyAttr}></td>
                                <td><input type="text" value="${size.name}" data-field="name" ${readonlyAttr}></td>
                                <td><input type="number" value="${size.width}" data-field="width" min="1"></td>
                                <td><input type="number" value="${size.height}" data-field="height" min="1"></td>
                                <td><input type="text" value="${size.description || ''}" data-field="description"></td>
                                <td><input type="number" value="${size.sort_order}" data-field="sort_order" min="0"></td>
                                <td>${deleteButtonHtml}</td>
                            </tr>
                        `;
                        }).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    // Toggle manage sizes section
    function toggleManageSizes() {
        const section = document.getElementById('manage-sizes-section');
        if (section) {
            section.style.display = section.style.display === 'none' ? 'block' : 'none';
        }
    }

    // Add new thumbnail size
    function showAddSizeForm() {
        const tbody = document.querySelector('#thumbnail-sizes-editor tbody');
        if (!tbody) return;

        const newRow = document.createElement('tr');
        newRow.className = 'new-size-row';
        newRow.setAttribute('data-size-id', 'new');
        newRow.innerHTML = `
            <td><span class="preset-badge preset-badge-custom">Custom</span></td>
            <td><input type="checkbox" checked data-field="is_active"></td>
            <td><input type="text" value="" placeholder="Display Name" data-field="display_name" required></td>
            <td><input type="text" value="" placeholder="internal_name" data-field="name" required></td>
            <td><input type="number" value="300" data-field="width" min="1"></td>
            <td><input type="number" value="300" data-field="height" min="1"></td>
            <td><input type="text" value="" placeholder="Description" data-field="description"></td>
            <td><input type="number" value="${thumbnailSizesData.length * 10 + 10}" data-field="sort_order" min="0"></td>
            <td>
                <button type="button" class="delete-size-btn cancel-new-btn" title="Cancel">
                    <i class="fas fa-times"></i>
                </button>
            </td>
        `;

        tbody.appendChild(newRow);

        // Cancel button removes the row
        newRow.querySelector('.cancel-new-btn').addEventListener('click', function() {
            newRow.remove();
        });

        const displayNameInput = newRow.querySelector('[data-field="display_name"]');
        if (displayNameInput) {
            displayNameInput.focus();
        }
    }

    // Save thumbnail sizes
    function saveThumbnailSizes(btn) {
        const tbody = document.querySelector('#thumbnail-sizes-editor tbody');
        if (!tbody) return;

        const rows = tbody.querySelectorAll('tr');
        const updates = [];
        const creates = [];

        rows.forEach(row => {
            const sizeId = row.getAttribute('data-size-id');
            const isNew = sizeId === 'new';

            const data = {
                name: row.querySelector('[data-field="name"]').value.trim(),
                display_name: row.querySelector('[data-field="display_name"]').value.trim(),
                width: parseInt(row.querySelector('[data-field="width"]').value),
                height: parseInt(row.querySelector('[data-field="height"]').value),
                description: row.querySelector('[data-field="description"]').value.trim(),
                is_active: row.querySelector('[data-field="is_active"]').checked,
                sort_order: parseInt(row.querySelector('[data-field="sort_order"]').value)
            };

            if (!data.name || !data.display_name || !data.width || !data.height) {
                AdminModal.alert({message: 'Please fill in all required fields (Name, Display Name, Width, Height)', type: 'warning'});
                return;
            }

            if (isNew) {
                creates.push(data);
            } else {
                updates.push({
                    id: parseInt(sizeId),
                    ...data
                });
            }
        });

        const originalText = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

        fetch(buildUrl(urls.saveThumbnailSizes), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ updates, creates })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                AdminModal.toast('Thumbnail sizes saved successfully!', 'success');
                loadThumbnailConfiguration();
            } else {
                throw new Error(data.error || 'Failed to save');
            }
        })
        .catch(error => {
            console.error('Error saving thumbnail sizes:', error);
            AdminModal.alert({message: 'Error saving thumbnail sizes: ' + error.message, type: 'error'});
        })
        .finally(() => {
            btn.disabled = false;
            btn.innerHTML = originalText;
        });
    }

    // Delete thumbnail size
    function deleteThumbnailSize(sizeId) {
        if (!confirm('Are you sure you want to delete this thumbnail size? This action cannot be undone.')) {
            return;
        }

        const deleteUrl = urls.deleteThumbnailSize.replace('/0/', '/' + sizeId + '/');

        fetch(buildUrl(deleteUrl), {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                AdminModal.toast('Thumbnail size deleted successfully!', 'success');
                loadThumbnailConfiguration();
            } else {
                throw new Error(data.error || 'Failed to delete');
            }
        })
        .catch(error => {
            console.error('Error deleting thumbnail size:', error);
            AdminModal.alert({message: 'Error deleting thumbnail size: ' + error.message, type: 'error'});
        });
    }

    // Load and display image statistics
    function loadImageStats() {
        const container = document.getElementById('image-stats-display');
        if (!container) return;

        fetch(buildUrl(urls.imageStats))
            .then(response => response.json())
            .then(data => {
                const stats = [
                    { label: 'Total Images', value: data.total_images || 0, icon: 'fa-images' },
                    { label: 'Product Images', value: data.product_images || 0, icon: 'fa-shopping-bag' },
                    { label: 'Total Thumbnails', value: data.total_thumbnails || 0, icon: 'fa-th' },
                    { label: 'WebP Images', value: data.webp_images || 0, icon: 'fa-bolt' }
                ];

                container.innerHTML = stats.map(stat => `
                    <div class="image-stat-card">
                        <div class="image-stat-icon">
                            <i class="fas ${stat.icon}"></i>
                        </div>
                        <div class="image-stat-value">
                            ${stat.value.toLocaleString()}
                        </div>
                        <div class="image-stat-label">
                            ${stat.label}
                        </div>
                    </div>
                `).join('');
            })
            .catch(error => {
                console.error('Error loading image stats:', error);
                container.innerHTML = '<div class="images-empty-state images-error">Error loading statistics</div>';
            });
    }

    // Load and display last regeneration info
    function loadLastRegenerationInfo() {
        fetch(buildUrl(urls.regenerateThumbnailsStatus))
            .then(response => response.json())
            .then(data => {
                updateLastRegenerationDisplay(data.last_regeneration);
            })
            .catch(error => {
                console.error('Error loading last regeneration info:', error);
            });
    }

    // Update the last regeneration display
    function updateLastRegenerationDisplay(lastRegeneration) {
        const infoDiv = document.getElementById('last-regeneration-info');
        const textSpan = document.getElementById('last-regeneration-text');

        if (!infoDiv || !textSpan) return;

        if (lastRegeneration && lastRegeneration.timestamp) {
            const timestamp = new Date(lastRegeneration.timestamp);
            const now = new Date();
            const diffMs = now - timestamp;
            const diffMins = Math.floor(diffMs / 60000);
            const diffHours = Math.floor(diffMs / 3600000);
            const diffDays = Math.floor(diffMs / 86400000);

            let timeAgo;
            if (diffMins < 1) {
                timeAgo = 'just now';
            } else if (diffMins < 60) {
                timeAgo = `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
            } else if (diffHours < 24) {
                timeAgo = `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
            } else if (diffDays < 30) {
                timeAgo = `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
            } else {
                timeAgo = `on ${timestamp.toLocaleDateString()}`;
            }

            textSpan.textContent = `Last regenerated ${timeAgo} (${lastRegeneration.processed} images)`;
            infoDiv.style.display = 'flex';
        } else {
            infoDiv.style.display = 'none';
        }
    }

    // Check regeneration status on page load
    function checkRegenerationStatus() {
        fetch(buildUrl(urls.regenerateThumbnailsStatus))
            .then(response => response.json())
            .then(data => {
                if (!data.complete && data.total > 0) {
                    showRegenerationBanner(data);
                    startStatusPolling();
                }
            })
            .catch(error => {
                console.error('Error checking regeneration status:', error);
            });
    }

    // Show the persistent banner
    function showRegenerationBanner(statusData) {
        const banner = document.getElementById('regeneration-status-banner');
        const message = document.getElementById('banner-status-message');
        const progressFill = document.getElementById('banner-progress-fill');

        if (banner) {
            banner.style.display = 'block';

            if (message) {
                message.textContent = statusData.message || `Processing ${statusData.processed || 0} of ${statusData.total || 0} images...`;
            }

            if (progressFill) {
                progressFill.style.width = (statusData.progress || 0) + '%';
            }
        }
    }

    // Hide the banner
    function hideRegenerationBanner() {
        const banner = document.getElementById('regeneration-status-banner');
        if (banner) {
            banner.style.display = 'none';
        }
    }

    // Start polling for status updates
    function startStatusPolling() {
        if (statusPollInterval) {
            clearInterval(statusPollInterval);
        }

        statusPollInterval = setInterval(() => {
            fetch(buildUrl(urls.regenerateThumbnailsStatus))
                .then(response => response.json())
                .then(data => {
                    if (data.complete) {
                        clearInterval(statusPollInterval);
                        statusPollInterval = null;

                        const banner = document.getElementById('regeneration-status-banner');
                        const icon = banner ? banner.querySelector('.regeneration-status-icon i') : null;
                        const title = banner ? banner.querySelector('.regeneration-status-title') : null;
                        const message = document.getElementById('banner-status-message');
                        const progressFill = document.getElementById('banner-progress-fill');

                        if (icon) icon.className = 'fas fa-check-circle';
                        if (title) title.textContent = 'Regeneration Complete!';
                        if (message) message.textContent = data.message || `Successfully regenerated ${data.processed} images!`;
                        if (progressFill) progressFill.style.width = '100%';

                        loadImageStats();
                        updateLastRegenerationDisplay(data.last_regeneration);

                        setTimeout(() => {
                            hideRegenerationBanner();
                        }, 5000);
                    } else {
                        showRegenerationBanner(data);
                    }
                })
                .catch(error => {
                    console.error('Error polling regeneration status:', error);
                    clearInterval(statusPollInterval);
                    statusPollInterval = null;
                });
        }, 2000);
    }

    // Regenerate thumbnails
    function regenerateThumbnails() {
        const btn = document.getElementById('regenerate-thumbnails-btn');
        const status = document.getElementById('regenerate-status');
        const progressContainer = document.getElementById('regenerate-progress');
        const progressBar = document.getElementById('regenerate-progress-bar');
        const progressText = document.getElementById('regenerate-progress-text');

        if (!confirm('This will regenerate all product image thumbnails. This process may take several minutes depending on the number of images. Continue?')) {
            return;
        }

        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        status.textContent = 'Starting regeneration...';
        progressContainer.classList.add('active');
        progressBar.style.width = '0%';

        showRegenerationBanner({
            complete: false,
            progress: 0,
            processed: 0,
            total: 0,
            message: 'Starting regeneration...'
        });

        fetch(buildUrl(urls.regenerateThumbnails), {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({}),
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                startStatusPolling();

                const pollInterval = setInterval(() => {
                    fetch(buildUrl(urls.regenerateThumbnailsStatus))
                        .then(response => response.json())
                        .then(statusData => {
                            const percent = statusData.progress || 0;
                            progressBar.style.width = percent + '%';
                            progressText.textContent = statusData.message || `Processing ${statusData.processed || 0} of ${statusData.total || 0} images...`;

                            if (statusData.complete) {
                                clearInterval(pollInterval);
                                btn.disabled = false;
                                btn.innerHTML = '<i class="fas fa-check"></i> Completed!';
                                status.textContent = `Successfully regenerated ${statusData.processed} thumbnails!`;

                                loadImageStats();
                                updateLastRegenerationDisplay(statusData.last_regeneration);

                                setTimeout(() => {
                                    btn.innerHTML = '<i class="fas fa-sync-alt"></i> Regenerate All Product Thumbnails';
                                    status.textContent = '';
                                    progressContainer.classList.remove('active');
                                }, 3000);
                            }
                        });
                }, 1000);
            } else {
                throw new Error(data.error || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error regenerating thumbnails:', error);
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sync-alt"></i> Regenerate All Product Thumbnails';
            status.textContent = '';
            progressContainer.classList.remove('active');
            hideRegenerationBanner();
            AdminModal.alert({message: 'Error regenerating thumbnails: ' + error.message, type: 'error'});
        });
    }

    // Event delegation for data-action buttons
    document.addEventListener('click', function(e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) return;
        var action = btn.dataset.action;

        if (action === 'dismiss-banner') {
            hideRegenerationBanner();
        } else if (action === 'show-add-size-form') {
            showAddSizeForm();
        } else if (action === 'save-thumbnail-sizes') {
            saveThumbnailSizes(btn);
        } else if (action === 'regenerate-thumbnails') {
            regenerateThumbnails();
        }

        // Handle delete buttons
        var deleteBtn = e.target.closest('.delete-size-btn[data-size-id]');
        if (deleteBtn) {
            deleteThumbnailSize(parseInt(deleteBtn.dataset.sizeId));
        }
    });

})();
