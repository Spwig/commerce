/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Translation Admin Theme Detector
 * Automatically detects Django Admin dark mode and applies appropriate theme
 */

(function() {
    'use strict';

    function detectAndApplyTheme() {
        // Check various dark mode indicators in Django Admin
        const isDarkMode =
            // Django 4.2+ dark mode class
            document.body.classList.contains('dark') ||
            document.body.classList.contains('dark-mode') ||
            // Check for dark mode in Django admin's theme preference
            (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ||
            // Check if Django admin container has dark class
            document.querySelector('#container.dark') !== null ||
            // Check localStorage for theme preference
            localStorage.getItem('theme') === 'dark' ||
            localStorage.getItem('django-admin-theme') === 'dark';

        // Apply dark mode class to body if detected
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
            // Also add to dashboard container if it exists
            const dashboardContainer = document.querySelector('.dashboard-container');
            if (dashboardContainer) {
                dashboardContainer.classList.add('dark-mode');
            }
        }

        // Listen for theme changes
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
                if (e.matches) {
                    document.body.classList.add('dark-mode');
                } else {
                    document.body.classList.remove('dark-mode');
                }
            });
        }

        // Watch for Django admin theme toggle if it exists
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                    const target = mutation.target;
                    if (target === document.body || target.id === 'container') {
                        if (target.classList.contains('dark')) {
                            document.body.classList.add('dark-mode');
                        } else {
                            document.body.classList.remove('dark-mode');
                        }
                    }
                }
            });
        });

        // Start observing
        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['class']
        });

        const container = document.getElementById('container');
        if (container) {
            observer.observe(container, {
                attributes: true,
                attributeFilter: ['class']
            });
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', detectAndApplyTheme);
    } else {
        detectAndApplyTheme();
    }
})();