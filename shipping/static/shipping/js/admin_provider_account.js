/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Provider Account Admin JavaScript
 * Handles credential field masking/unmasking
 * All classes prefixed with 'shipping-' per design rules
 */

(function() {
    'use strict';

    function initializeCredentialFields() {
        // Find all secret credential fields
        const secretFields = document.querySelectorAll('input[data-secret="true"]');

        secretFields.forEach(function(field) {
            // Skip if already initialized
            if (field.parentElement.classList.contains('shipping-password-field-wrapper')) {
                return;
            }

            // Create wrapper
            const wrapper = document.createElement('div');
            wrapper.className = 'shipping-password-field-wrapper shipping-masked';

            // Wrap the input field
            field.parentNode.insertBefore(wrapper, field);
            wrapper.appendChild(field);

            // Create toggle button with Font Awesome eye icon
            const toggleBtn = document.createElement('button');
            toggleBtn.type = 'button';
            toggleBtn.className = 'shipping-password-toggle';
            toggleBtn.innerHTML = '<i class="fas fa-eye"></i>';
            toggleBtn.setAttribute('title', 'Show/Hide');
            toggleBtn.setAttribute('aria-label', 'Toggle password visibility');

            // Add click handler
            toggleBtn.addEventListener('click', function(e) {
                e.preventDefault();
                togglePasswordVisibility(wrapper, field, toggleBtn);
            });

            wrapper.appendChild(toggleBtn);

            // Initially mask the field
            maskField(field);
        });
    }

    function togglePasswordVisibility(wrapper, field, button) {
        const isMasked = wrapper.classList.contains('shipping-masked');

        if (isMasked) {
            // Show password
            wrapper.classList.remove('shipping-masked');
            unmaskField(field);
            button.innerHTML = '<i class="fas fa-eye-slash"></i>';
            button.setAttribute('title', 'Hide');
        } else {
            // Hide password
            wrapper.classList.add('shipping-masked');
            maskField(field);
            button.innerHTML = '<i class="fas fa-eye"></i>';
            button.setAttribute('title', 'Show');
        }
    }

    function maskField(field) {
        // Store original value if not already stored
        if (!field.dataset.originalValue) {
            field.dataset.originalValue = field.value;
        }

        // Apply text-security CSS
        field.style.webkitTextSecurity = 'disc';
        field.style.textSecurity = 'disc';
    }

    function unmaskField(field) {
        // Remove text-security CSS
        field.style.webkitTextSecurity = 'none';
        field.style.textSecurity = 'none';
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeCredentialFields);
    } else {
        initializeCredentialFields();
    }

    // Also initialize after inline formsets are added (for future extensibility)
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).on('formset:added', function() {
            initializeCredentialFields();
        });
    }
})();
