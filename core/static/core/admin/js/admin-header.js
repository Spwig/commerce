/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin Header - User menu, theme switching, and help drawer functionality
 *
 * Provides interactive features for the admin header:
 * - User dropdown menu with outside click detection
 * - Theme switching (light/dark) with API persistence
 * - Help drawer toggle
 * - Keyboard accessibility (Escape to close)
 */

(function() {
    'use strict';

    /**
     * Dismiss a notification banner with animation and session persistence.
     */
    function dismissBanner(selector, storageKey) {
        var banner = document.querySelector(selector);
        if (banner) {
            banner.style.animation = 'licenseBannerSlideOut 0.2s ease-in forwards';
            setTimeout(function() { banner.style.display = 'none'; }, 200);
            if (storageKey) {
                sessionStorage.setItem(storageKey, 'true');
            }
        }
    }

    // Restore dismissed banner state on page load
    document.addEventListener('DOMContentLoaded', function() {
        var banners = [
            { key: 'license_banner_dismissed', selector: '.license-notice-banner' },
            { key: 'mfa_banner_dismissed', selector: '.mfa-grace-banner' },
            { key: 'update_banner_dismissed', selector: '.update-notice-banner' }
        ];
        banners.forEach(function(item) {
            if (sessionStorage.getItem(item.key) === 'true') {
                var el = document.querySelector(item.selector);
                if (el) { el.style.display = 'none'; }
            }
        });
    });

    /**
     * Toggle user dropdown menu
     */
    function toggleUserMenu() {
        const userMenu = document.getElementById('userMenu');
        const dropdown = document.getElementById('userDropdown');
        const toggle = userMenu ? userMenu.querySelector('.user-menu-toggle') : null;

        if (!userMenu || !toggle) return;

        const isOpen = userMenu.classList.contains('open');

        if (isOpen) {
            userMenu.classList.remove('open');
            toggle.setAttribute('aria-expanded', 'false');
        } else {
            userMenu.classList.add('open');
            toggle.setAttribute('aria-expanded', 'true');
        }
    }

    /**
     * Close user menu when clicking outside
     */
    function handleOutsideClick(event) {
        const userMenu = document.getElementById('userMenu');
        if (!userMenu) return;

        const toggle = userMenu.querySelector('.user-menu-toggle');

        if (!userMenu.contains(event.target)) {
            userMenu.classList.remove('open');
            if (toggle) {
                toggle.setAttribute('aria-expanded', 'false');
            }
        }
    }

    /**
     * Close user menu on Escape key
     */
    function handleEscapeKey(event) {
        if (event.key === 'Escape') {
            const userMenu = document.getElementById('userMenu');
            if (!userMenu) return;

            const toggle = userMenu.querySelector('.user-menu-toggle');

            userMenu.classList.remove('open');
            if (toggle) {
                toggle.setAttribute('aria-expanded', 'false');
            }
        }
    }

    /**
     * Load theme CSS file
     */
    function loadThemeCSS(theme) {
        const existingLink = document.querySelector('link[href*="/themes/"]');
        if (existingLink) {
            existingLink.href = `/static/core/admin/css/themes/${theme}.css`;
        } else {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = `/static/core/admin/css/themes/${theme}.css`;
            document.head.appendChild(link);
        }
    }

    /**
     * Update theme button active state
     */
    function updateThemeButton(theme, buttons) {
        buttons.forEach(btn => {
            const btnTheme = btn.getAttribute('data-theme');
            if (btnTheme === theme) {
                btn.style.background = '#28a745';
                btn.style.transform = 'scale(0.95)';
            } else {
                btn.style.background = 'var(--primary, #417690)';
                btn.style.transform = 'scale(1)';
            }
        });
    }

    /**
     * Initialize theme toggle functionality
     */
    function initThemeToggle() {
        const themeButtons = document.querySelectorAll('.theme-toggle-btn');
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';

        // Set initial state
        updateThemeButton(currentTheme, themeButtons);

        // Add click handlers
        themeButtons.forEach(btn => {
            btn.addEventListener('click', function() {
                const theme = this.getAttribute('data-theme');

                // Get CSRF token
                const csrfToken = AdminUtils.getCsrfToken();

                // Make API call to switch theme - include language prefix in URL
                const langCode = document.documentElement.lang || 'en';
                const url = `/${langCode}/admin/switch-theme/`;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    body: JSON.stringify({ theme: theme })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Update document theme
                        document.documentElement.setAttribute('data-theme', theme);

                        // Update active button
                        updateThemeButton(theme, themeButtons);

                        // Load theme CSS if needed
                        loadThemeCSS(theme);
                    }
                })
                .catch(error => {
                    console.error('Theme switch error:', error);
                    // Fallback: still apply theme locally
                    document.documentElement.setAttribute('data-theme', theme);
                    updateThemeButton(theme, themeButtons);
                    loadThemeCSS(theme);
                    // Store in localStorage as backup
                    localStorage.setItem('admin_theme', theme);
                });
            });

            // Add hover effects
            btn.addEventListener('mouseenter', function() {
                if (this.style.background !== 'rgb(40, 167, 69)') { // Not active
                    this.style.background = '#5a9bc4';
                }
            });

            btn.addEventListener('mouseleave', function() {
                if (this.style.background !== 'rgb(40, 167, 69)') { // Not active
                    this.style.background = 'var(--primary, #417690)';
                }
            });
        });
    }

    /**
     * Toggle help drawer open/closed
     */
    function toggleHelpDrawer() {
        const drawer = document.getElementById('helpDrawer');
        const overlay = document.getElementById('helpDrawerOverlay');

        if (!drawer || !overlay) return;

        const isOpen = drawer.classList.contains('open');

        if (isOpen) {
            drawer.classList.remove('open');
            overlay.classList.remove('active');
            drawer.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        } else {
            drawer.classList.add('open');
            overlay.classList.add('active');
            drawer.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';

            // Initialize help system if not already done
            if (typeof HelpSystem !== 'undefined' && typeof HelpSystem.init === 'function') {
                HelpSystem.init();
            }
        }
    }

    /**
     * Handle all header click events via delegation
     */
    function handleHeaderActions(e) {
        // Find the nearest element with data-action
        const actionElement = e.target.closest('[data-action]');
        if (!actionElement) return;

        const action = actionElement.dataset.action;
        if (!action) return;

        switch (action) {
            case 'toggle-user-menu':
                e.preventDefault();
                toggleUserMenu();
                break;
            case 'toggle-help-drawer':
                e.preventDefault();
                toggleHelpDrawer();
                break;
            case 'toggle-sidebar':
                e.preventDefault();
                if (typeof window.toggleSidebar === 'function') {
                    window.toggleSidebar();
                }
                break;
            case 'help-show-categories':
                e.preventDefault();
                if (typeof window.HelpSystem !== 'undefined' && typeof window.HelpSystem.showCategories === 'function') {
                    window.HelpSystem.showCategories();
                }
                break;
            case 'help-submit-feedback':
                e.preventDefault();
                const helpful = actionElement.dataset.helpful === 'true';
                if (typeof window.HelpSystem !== 'undefined' && typeof window.HelpSystem.submitFeedback === 'function') {
                    window.HelpSystem.submitFeedback(helpful);
                }
                break;
            case 'help-submit-feedback-comment':
                e.preventDefault();
                if (typeof window.HelpSystem !== 'undefined' && typeof window.HelpSystem.submitFeedbackComment === 'function') {
                    window.HelpSystem.submitFeedbackComment();
                }
                break;
            case 'open-bug-report':
                e.preventDefault();
                if (typeof window.BugReportWizard !== 'undefined') {
                    window.BugReportWizard.open();
                }
                break;
            case 'close-bug-report':
                e.preventDefault();
                if (typeof window.BugReportWizard !== 'undefined') {
                    window.BugReportWizard.close();
                }
                break;
            case 'bug-report-next':
                e.preventDefault();
                if (typeof window.BugReportWizard !== 'undefined') {
                    window.BugReportWizard.next();
                }
                break;
            case 'bug-report-back':
                e.preventDefault();
                if (typeof window.BugReportWizard !== 'undefined') {
                    window.BugReportWizard.back();
                }
                break;
            case 'bug-report-skip':
                e.preventDefault();
                if (typeof window.BugReportWizard !== 'undefined') {
                    window.BugReportWizard.skip();
                }
                break;
            case 'bug-report-submit':
                e.preventDefault();
                if (typeof window.BugReportWizard !== 'undefined') {
                    window.BugReportWizard.submit();
                }
                break;
            case 'dismiss-license-banner':
                e.preventDefault();
                dismissBanner('.license-notice-banner', 'license_banner_dismissed');
                break;
            case 'dismiss-mfa-banner':
                e.preventDefault();
                dismissBanner('.mfa-grace-banner', 'mfa_banner_dismissed');
                break;
            case 'dismiss-update-banner':
                e.preventDefault();
                dismissBanner('.update-notice-banner', 'update_banner_dismissed');
                break;
        }
    }

    /**
     * Initialize admin header functionality
     */
    function init() {
        // Add body class for proper spacing
        document.body.classList.add('has-admin-header');

        // Event delegation for all header actions
        document.addEventListener('click', handleHeaderActions);

        // User menu: close on outside click
        document.addEventListener('click', handleOutsideClick);

        // User menu: close on Escape key
        document.addEventListener('keydown', handleEscapeKey);

        // Initialize theme toggle
        initThemeToggle();
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for external access if needed
    window.AdminHeader = {
        toggleUserMenu: toggleUserMenu,
        toggleHelpDrawer: toggleHelpDrawer
    };

})();
