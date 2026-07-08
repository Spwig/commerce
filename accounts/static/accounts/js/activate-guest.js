/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Activate Guest Account Page
 * Handles password visibility toggle and client-side password match validation.
 * Replaces inline onclick and inline <script> block.
 */
(function() {
    'use strict';

    /**
     * Toggle password field visibility.
     * Expects button with data-action="toggle-password" and data-field="<input-id>".
     * Each eye icon pair: #<fieldId>-icon-hide and #<fieldId>-icon-show use CSS class "hidden".
     */
    function togglePassword(fieldId) {
        var field = document.getElementById(fieldId);
        var hideIcon = document.getElementById(fieldId + '-icon-hide');
        var showIcon = document.getElementById(fieldId + '-icon-show');

        if (!field) return;

        if (field.type === 'password') {
            field.type = 'text';
            if (hideIcon) hideIcon.classList.add('hidden');
            if (showIcon) showIcon.classList.remove('hidden');
        } else {
            field.type = 'password';
            if (hideIcon) hideIcon.classList.remove('hidden');
            if (showIcon) showIcon.classList.add('hidden');
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Password toggle buttons
        document.addEventListener('click', function(e) {
            var btn = e.target.closest('[data-action="toggle-password"]');
            if (btn) {
                var fieldId = btn.dataset.field;
                if (fieldId) togglePassword(fieldId);
            }
        });

        // Client-side password matching validation
        var form = document.querySelector('form[data-password-form]');
        if (!form) return;

        var mismatchMsg = form.dataset.mismatchMsg || 'Passwords do not match. Please try again.';

        form.addEventListener('submit', function(e) {
            var password = document.getElementById('password');
            var passwordConfirm = document.getElementById('password_confirm');

            if (password && passwordConfirm && password.value !== passwordConfirm.value) {
                e.preventDefault();
                AdminModal.alert({message: mismatchMsg, type: 'warning'});
                passwordConfirm.focus();
            }
        });
    });
})();
