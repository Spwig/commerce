/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin Login - Password visibility toggle
 *
 * Provides password show/hide functionality for the admin login form.
 */

(function() {
    'use strict';

    /**
     * Toggle password visibility
     */
    function togglePasswordVisibility() {
        const input = document.getElementById('id_password');
        const icon = document.getElementById('password-toggle-icon');

        if (!input || !icon) return;

        if (input.type === 'password') {
            input.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        } else {
            input.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }

    /**
     * Handle login form actions via delegation
     */
    function handleLoginActions(e) {
        // Find the nearest element with data-action
        const actionElement = e.target.closest('[data-action]');
        if (!actionElement) return;

        const action = actionElement.dataset.action;
        if (!action) return;

        if (action === 'toggle-password') {
            e.preventDefault();
            togglePasswordVisibility();
        }
    }

    // Initialize event delegation
    document.addEventListener('click', handleLoginActions);

    // Export for external access if needed
    window.AdminLogin = {
        togglePasswordVisibility: togglePasswordVisibility
    };

})();
