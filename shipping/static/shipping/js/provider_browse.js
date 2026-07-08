/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Provider Browse Page JavaScript
 * Handles provider installation and UI interactions
 */

(function() {
    'use strict';

    var i18n = {};

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

            // Auto-remove after duration
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

                const response = await fetch(AdminUtils.buildAdminUrl(`/admin/shipping/providers/install/${providerSlug}/`), {
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

            // Get current language from URL
            const currentPath = window.location.pathname;
            const langMatch = currentPath.match(/^\/([a-z]{2})\//);
            const langCode = langMatch ? langMatch[1] : 'en';

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
                configureBtn.href = `/${langCode}/admin/shipping/wizard/step1/`;
                configureBtn.className = 'button btn-primary';
                configureBtn.innerHTML = '<i class="fas fa-cog"></i> Configure';
                installBtn.parentNode.replaceChild(configureBtn, installBtn);
            }
        }
    }

    // Information card collapse functionality
    const InfoCardManager = {
        STORAGE_KEY: 'provider_info_card_collapsed',

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

    // Provider update handler
    class ProviderUpdater {
        constructor() {
            this.csrfToken = AdminUtils.getCsrfToken();
        }

        async update(providerSlug, providerVersion) {
            try {
                LoadingOverlay.show(`Updating ${providerSlug} to v${providerVersion}...`);

                const response = await fetch(AdminUtils.buildAdminUrl(`/admin/shipping/providers/update/${providerSlug}/`), {
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
            // Create message element
            const messageDiv = document.createElement('div');
            messageDiv.className = `update-message update-message-${type}`;
            messageDiv.innerHTML = `
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                ${message}
            `;

            // Insert at top of container
            const container = document.querySelector('.provider-browse-container');
            if (container) {
                container.insertBefore(messageDiv, container.firstChild);

                // Remove after 5 seconds
                setTimeout(() => {
                    messageDiv.remove();
                }, 5000);
            }
        }
    }

    // Make install and update functions globally available for modal
    window.installProvider = function(slug, name) {
        const installer = new ProviderInstaller();
        return installer.install(slug, name);
    };

    window.updateProvider = async function(slug, version, name) {
        const confirmed = await ProviderConfirm.show({
            title: i18n.updateTitle || 'Update Provider',
            message: ((i18n.confirmUpdate || 'Update {name} to version {version}?').replace('{name}', name || slug).replace('{version}', version)),
            confirmText: i18n.updateBtn || 'Update',
            cancelText: i18n.cancelBtn || 'Cancel'
        });
        if (!confirmed) return false;
        const updater = new ProviderUpdater();
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
        const installButtons = document.querySelectorAll('.btn-install');

        installButtons.forEach(button => {
            button.addEventListener('click', async function(e) {
                e.preventDefault();

                const providerSlug = this.dataset.providerSlug;
                const providerName = this.dataset.providerName;

                if (!providerSlug) {
                    NotificationManager.error('Invalid provider. Please refresh the page and try again.');
                    return;
                }

                // Disable button during installation
                this.disabled = true;
                const originalHTML = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Installing...';

                const success = await installer.install(providerSlug, providerName);

                // Re-enable button if installation failed
                if (!success) {
                    this.disabled = false;
                    this.innerHTML = originalHTML;
                }
            });
        });

        // Attach event listeners to update buttons
        const updateButtons = document.querySelectorAll('.btn-update');

        updateButtons.forEach(button => {
            button.addEventListener('click', async function(e) {
                e.preventDefault();

                const slug = this.dataset.slug;
                const version = this.dataset.version;
                const name = this.dataset.name || slug;

                if (!slug || !version) {
                    return;
                }

                const confirmed = await ProviderConfirm.show({
                    title: i18n.updateTitle || 'Update Provider',
                    message: (i18n.confirmUpdate || 'Update {name} to version {version}?').replace('{name}', name).replace('{version}', version),
                    confirmText: i18n.updateBtn || 'Update',
                    cancelText: i18n.cancelBtn || 'Cancel'
                });
                if (!confirmed) {
                    return;
                }

                // Disable button and show loading
                this.disabled = true;
                const originalHTML = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Updating...';

                const success = await updater.update(slug, version);

                // Re-enable button if update failed
                if (!success) {
                    this.disabled = false;
                    this.innerHTML = originalHTML;
                }
            });
        });

        // Handle learn more links (open in new tab)
        const learnMoreLinks = document.querySelectorAll('.provider-learn-more[target="_blank"]');
        learnMoreLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // Allow default behavior, but track if needed
                console.log('Opening documentation:', this.href);
            });
        });

        // Handle "View Details" button clicks
        const detailsButtons = document.querySelectorAll('.provider-details-link');
        detailsButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();

                // Get provider data from script tag
                const providerDataScript = document.getElementById('provider-data');
                if (!providerDataScript) {
                    console.error('Provider data not found');
                    return;
                }

                try {
                    const providersData = JSON.parse(providerDataScript.textContent);
                    const card = this.closest('.provider-card');
                    const providerSlug = card ? card.dataset.providerSlug : null;

                    if (!providerSlug) {
                        console.error('Provider slug not found');
                        return;
                    }

                    // Find provider in data
                    const providerData = providersData.find(p => p.slug === providerSlug);

                    if (!providerData) {
                        console.error('Provider data not found for slug:', providerSlug);
                        return;
                    }

                    // Add provider type for modal
                    providerData.provider_type = 'shipping';

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

    // Auto-submit selects (replaces onchange="this.form.submit()")
    document.addEventListener('change', function (e) {
        var el = e.target;
        if (el && el.dataset && el.dataset.autoSubmit === 'true') {
            var form = el.closest('form');
            if (form) form.submit();
        }
    });

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
