/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * SMS Provider Browse Page JavaScript
 * Handles provider installation, updates, info card collapse,
 * detail modal, and notifications.
 */

(function() {
    'use strict';

    // Notification system
    const NotificationManager = {
        container: null,

        init() {
            this.container = document.getElementById('provider-notification-container');
        },

        show(message, type = 'success', duration = 5000) {
            if (!this.container) return;

            const notification = document.createElement('div');
            notification.className = `provider-notification ${type}`;

            const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';

            notification.innerHTML = `
                <i class="fas ${icon}"></i>
                <div class="notification-content">
                    <strong>${type === 'success' ? 'Success' : 'Error'}</strong>
                    <p>${message}</p>
                </div>
            `;

            this.container.appendChild(notification);

            if (duration > 0) {
                setTimeout(() => {
                    notification.style.opacity = '0';
                    setTimeout(() => notification.remove(), 300);
                }, duration);
            }

            return notification;
        },

        success(message, duration = 5000) {
            return this.show(message, 'success', duration);
        },

        error(message, duration = 7000) {
            return this.show(message, 'error', duration);
        }
    };

    // Loading overlay manager
    const LoadingOverlay = {
        overlay: null,

        init() {
            this.overlay = document.getElementById('provider-install-loading');
        },

        show(message = 'Installing provider...') {
            if (!this.overlay) return;

            const messageEl = this.overlay.querySelector('.loading-message');
            if (messageEl) {
                messageEl.textContent = message;
            }

            this.overlay.style.display = 'flex';
        },

        hide() {
            if (!this.overlay) return;
            this.overlay.style.display = 'none';
        }
    };

    // Provider installation handler
    class ProviderInstaller {
        constructor() {
            this.csrfToken = AdminUtils.getCsrfToken();
        }

        async install(providerSlug, providerName) {
            try {
                LoadingOverlay.show(`Installing ${providerName}...`);

                const response = await fetch(AdminUtils.buildAdminUrl(`/admin/sms-system/providers/install/${providerSlug}/`), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.csrfToken,
                    },
                    credentials: 'same-origin',
                });

                // Handle gateway timeout or non-JSON responses (e.g. 504)
                const contentType = response.headers.get('content-type') || '';
                if (!contentType.includes('application/json')) {
                    LoadingOverlay.show('Installation is being processed. Refreshing...');
                    setTimeout(() => window.location.reload(), 3000);
                    return true;
                }

                const data = await response.json();

                LoadingOverlay.hide();

                if (data.success) {
                    NotificationManager.success(data.message || `${providerName} installed successfully!`);

                    // Update UI to show installed state
                    this.updateCardToInstalled(providerSlug);

                    // Redirect to wizard after short delay
                    setTimeout(() => {
                        if (data.redirect_url) {
                            window.location.href = data.redirect_url;
                        }
                    }, 1500);

                    return true;
                } else {
                    NotificationManager.error(data.error || 'Installation failed. Please try again.');
                    return false;
                }

            } catch (error) {
                // Network error or JSON parse failure — install may still be completing
                console.error('Installation error:', error);
                LoadingOverlay.show('Installation is being processed. Refreshing...');
                setTimeout(() => window.location.reload(), 3000);
                return true;
            }
        }

        updateCardToInstalled(providerSlug) {
            const card = document.querySelector(`[data-provider-slug="${providerSlug}"]`);
            if (!card) return;

            // Add installed class
            card.classList.add('configured');

            // Update status badge
            const statusBadge = card.querySelector('.provider-title .status-badge');
            if (statusBadge) {
                statusBadge.className = 'status-badge status-installed';
                statusBadge.innerHTML = '<i class="fas fa-check-circle"></i> Installed';
            }

            // Replace install button with configure button
            const installBtn = card.querySelector('.btn-install');
            if (installBtn) {
                const configureBtn = document.createElement('a');
                configureBtn.href = AdminUtils.buildAdminUrl('/admin/sms-system/wizard/');
                configureBtn.className = 'button btn-primary';
                configureBtn.innerHTML = '<i class="fas fa-cog"></i> Configure';
                installBtn.parentNode.replaceChild(configureBtn, installBtn);
            }
        }
    }

    // Provider update handler
    class ProviderUpdater {
        constructor() {
            this.csrfToken = AdminUtils.getCsrfToken();
        }

        async update(providerSlug, providerVersion) {
            try {
                LoadingOverlay.show(`Updating ${providerSlug} to v${providerVersion}...`);

                const response = await fetch(AdminUtils.buildAdminUrl(`/admin/sms-system/providers/update/${providerSlug}/`), {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.csrfToken,
                        'Content-Type': 'application/json',
                    },
                    credentials: 'same-origin',
                });

                // Handle gateway timeout or non-JSON responses (e.g. 504)
                const contentType = response.headers.get('content-type') || '';
                if (!contentType.includes('application/json')) {
                    LoadingOverlay.show('Update is being processed. Refreshing...');
                    setTimeout(() => window.location.reload(), 3000);
                    return true;
                }

                const data = await response.json();

                LoadingOverlay.hide();

                if (data.success) {
                    NotificationManager.success(data.message || 'Provider updated successfully!');
                    setTimeout(() => window.location.reload(), 1000);
                    return true;
                } else {
                    NotificationManager.error(data.error || 'Update failed.');
                    return false;
                }

            } catch (error) {
                // Network error or JSON parse failure — update may still be completing
                console.error('Update error:', error);
                LoadingOverlay.show('Update is being processed. Refreshing...');
                setTimeout(() => window.location.reload(), 3000);
                return true;
            }
        }

        showMessage(type, message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `update-message update-message-${type}`;
            messageDiv.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                ${message}
            `;

            const container = document.querySelector('.provider-browse-container');
            if (container) {
                container.insertBefore(messageDiv, container.firstChild);

                setTimeout(() => {
                    messageDiv.remove();
                }, 5000);
            }
        }
    }

    // Information card collapse functionality
    const InfoCardManager = {
        STORAGE_KEY: 'sms_provider_info_card_collapsed',

        init() {
            const card = document.getElementById('providerInfoCard');
            if (!card) return;

            const toggleBtn = card.querySelector('.collapse-toggle');
            const cardBody = document.getElementById('cardBody');

            if (!toggleBtn || !cardBody) return;

            // Restore collapse state from localStorage
            const isCollapsed = localStorage.getItem(this.STORAGE_KEY) === 'true';
            if (isCollapsed) {
                cardBody.classList.add('collapsed');
                toggleBtn.setAttribute('aria-expanded', 'false');
                const icon = toggleBtn.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-chevron-down');
                    icon.classList.add('fa-chevron-right');
                }
            }

            // Toggle on click
            toggleBtn.addEventListener('click', () => {
                const isNowCollapsed = cardBody.classList.toggle('collapsed');
                toggleBtn.setAttribute('aria-expanded', !isNowCollapsed);

                const icon = toggleBtn.querySelector('i');
                if (icon) {
                    if (isNowCollapsed) {
                        icon.classList.remove('fa-chevron-down');
                        icon.classList.add('fa-chevron-right');
                    } else {
                        icon.classList.remove('fa-chevron-right');
                        icon.classList.add('fa-chevron-down');
                    }
                }

                // Save state
                localStorage.setItem(this.STORAGE_KEY, isNowCollapsed);
            });
        }
    };

    // Make install and update functions globally available for modal
    window.installProvider = function(slug, name) {
        const installer = new ProviderInstaller();
        return installer.install(slug, name);
    };

    window.updateProvider = async function(slug, version, name) {
        var confirmed = await ProviderConfirm.show({
            title: 'Update Provider',
            message: 'Update ' + (name || slug) + ' to version ' + version + '?',
            confirmText: 'Update',
            cancelText: 'Cancel'
        });
        if (!confirmed) return false;
        var updater = new ProviderUpdater();
        return updater.update(slug, version);
    };

    // Initialize on DOM ready
    function init() {
        // Initialize managers
        NotificationManager.init();
        LoadingOverlay.init();
        InfoCardManager.init();

        const installer = new ProviderInstaller();
        const updater = new ProviderUpdater();

        // Attach event listeners to install buttons
        document.querySelectorAll('.btn-install').forEach(function(button) {
            button.addEventListener('click', async function(e) {
                e.preventDefault();

                var providerSlug = this.dataset.providerSlug;
                var providerName = this.dataset.providerName;

                if (!providerSlug) {
                    NotificationManager.error('Invalid provider. Please refresh the page and try again.');
                    return;
                }

                // Disable button during installation
                this.disabled = true;
                var originalHTML = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Installing...';

                var success = await installer.install(providerSlug, providerName);

                // Re-enable button if installation failed
                if (!success) {
                    this.disabled = false;
                    this.innerHTML = originalHTML;
                }
            });
        });

        // Attach event listeners to update buttons
        document.querySelectorAll('.btn-update').forEach(function(button) {
            button.addEventListener('click', async function(e) {
                e.preventDefault();

                var slug = this.dataset.slug;
                var version = this.dataset.version;
                var name = this.dataset.name || slug;

                if (!slug || !version) return;

                var confirmed = await ProviderConfirm.show({
                    title: 'Update Provider',
                    message: 'Update ' + name + ' to version ' + version + '?',
                    confirmText: 'Update',
                    cancelText: 'Cancel'
                });
                if (!confirmed) {
                    return;
                }

                // Disable button and show loading
                this.disabled = true;
                var originalHTML = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating...';

                var success = await updater.update(slug, version);

                // Re-enable button if update failed
                if (!success) {
                    this.disabled = false;
                    this.innerHTML = originalHTML;
                }
            });
        });

        // Handle learn more links
        document.querySelectorAll('.provider-learn-more[target="_blank"]').forEach(function(link) {
            link.addEventListener('click', function() {
                console.log('Opening documentation:', this.href);
            });
        });

        // Handle "View Details" button clicks
        document.querySelectorAll('.provider-details-link').forEach(function(button) {
            button.addEventListener('click', function(e) {
                e.preventDefault();

                var providerDataScript = document.getElementById('provider-data');
                if (!providerDataScript) {
                    console.error('Provider data not found');
                    return;
                }

                try {
                    var providersData = JSON.parse(providerDataScript.textContent);
                    var providerSlug = this.dataset.providerSlug;

                    if (!providerSlug) {
                        console.error('Provider slug not found');
                        return;
                    }

                    // Find provider in data
                    var providerData = providersData.find(function(p) {
                        return p.slug === providerSlug;
                    });

                    if (!providerData) {
                        console.error('Provider data not found for slug:', providerSlug);
                        return;
                    }

                    // Add provider type for modal
                    providerData.provider_type = 'sms';

                    // Open modal with provider data
                    if (typeof ProviderModal !== 'undefined') {
                        ProviderModal.open(providerData);
                    } else {
                        console.error('ProviderModal not loaded');
                    }
                } catch (error) {
                    console.error('Error parsing provider data:', error);
                }
            });
        });
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
