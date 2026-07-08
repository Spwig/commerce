/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * MFA Verification - Auto-focus and code formatting
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const codeInput = document.getElementById('code');
        if (!codeInput) return;

        // Only allow digits
        codeInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/\D/g, '').slice(0, 6);
        });

        // Auto-submit when 6 digits entered
        codeInput.addEventListener('keyup', function(e) {
            if (this.value.length === 6) {
                // Small delay before submit for better UX
                setTimeout(() => {
                    this.form.submit();
                }, 100);
            }
        });
    });
})();
