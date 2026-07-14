/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Entrance Pages JavaScript (Login/Signup/Logout)
 * CSP-Compliant - No inline handlers
 *
 * Features:
 * - Password visibility toggle
 * - Form validation feedback
 * - Loading states
 * - Social auth button handlers
 * - Focus management
 */

(function () {
  'use strict';

  /**
   * Toggle password field visibility
   * @param {HTMLElement} buttonElement - The toggle button
   */
  function togglePassword(buttonElement) {
    const targetId = buttonElement.dataset.target;
    const input = document.getElementById(targetId);
    const icon = buttonElement.querySelector('i');

    if (!input || !icon) return;

    if (input.type === 'password') {
      input.type = 'text';
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
      buttonElement.setAttribute('aria-label', buttonElement.dataset.labelHide || 'Hide password');
    } else {
      input.type = 'password';
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
      buttonElement.setAttribute('aria-label', buttonElement.dataset.labelShow || 'Show password');
    }
  }

  /**
   * Show loading state on form submission
   * @param {Event} event - Form submit event
   */
  function handleFormSubmit(event) {
    const form = event.target;
    const submitBtn = form.querySelector('[type="submit"]');

    if (!submitBtn) return;

    // Show loading state
    const textSpan = submitBtn.querySelector('.entrance-submit-text');
    const icon = submitBtn.querySelector('.entrance-submit-icon');
    const spinner = submitBtn.querySelector('.entrance-submit-spinner');

    if (textSpan && submitBtn.dataset.loadingText) {
      textSpan.textContent = submitBtn.dataset.loadingText;
    }

    if (icon) icon.style.display = 'none';
    if (spinner) spinner.style.display = 'inline-block';

    submitBtn.disabled = true;
    submitBtn.classList.add('entrance-submit-loading');
  }

  /**
   * Show loading state on social provider click
   * @param {Event} event - Click event
   */
  function handleSocialClick(event) {
    const link = event.currentTarget;
    const providerName = link.dataset.provider;

    // Add loading class
    link.classList.add('social-btn-loading');

    // Change text to "Connecting to {Provider}..."
    const span = link.querySelector('span');
    if (span) {
      span.dataset.originalText = span.textContent;
      span.textContent = link.dataset.loadingText || `Connecting to ${providerName}...`;
    }
  }

  /**
   * Real-time field validation feedback
   * @param {HTMLInputElement} input - The input element
   */
  function validateField(input) {
    const wrapper = input.closest('.entrance-field');
    if (!wrapper) return;

    const errorContainer = wrapper.querySelector('.entrance-field-error');

    // Remove existing client-side error state
    wrapper.classList.remove('entrance-field-invalid');
    if (errorContainer && !errorContainer.classList.contains('server-error')) {
      errorContainer.remove();
    }

    // Check HTML5 validity
    if (!input.validity.valid) {
      wrapper.classList.add('entrance-field-invalid');

      // Only add error message if not already present (avoid duplicating server errors)
      if (!errorContainer || !errorContainer.classList.contains('server-error')) {
        const error = document.createElement('div');
        error.className = 'entrance-field-error client-error';
        error.textContent = input.validationMessage;
        input.parentElement.after(error);
      }
    }
  }

  /**
   * Event delegation handler for all entrance actions
   * @param {Event} event - Click event
   */
  function handleEntranceActions(event) {
    const actionElement = event.target.closest('[data-action]');
    if (!actionElement) return;

    const action = actionElement.dataset.action;

    switch (action) {
      case 'toggle-password':
        event.preventDefault();
        togglePassword(actionElement);
        break;
    }
  }

  /**
   * Initialize entrance page functionality
   */
  function init() {
    // Event delegation for all interactive elements
    document.addEventListener('click', handleEntranceActions);

    // Form submission handling
    const forms = document.querySelectorAll('.entrance-form form');
    forms.forEach(form => {
      form.addEventListener('submit', handleFormSubmit);
    });

    // Social provider click handling
    const socialBtns = document.querySelectorAll('.social-btn');
    socialBtns.forEach(btn => {
      btn.addEventListener('click', handleSocialClick);
    });

    // Real-time validation (optional, on blur)
    const inputs = document.querySelectorAll('.entrance-field input[required]');
    inputs.forEach(input => {
      input.addEventListener('blur', () => validateField(input));
    });

    // Focus first input on desktop (not on mobile to avoid keyboard popup)
    const firstInput = document.querySelector('.entrance-field input');
    if (firstInput && window.innerWidth > 768) {
      firstInput.focus();
    }

    // Handle password confirmation matching (signup page)
    const passwordInput = document.getElementById('id_password1');
    const confirmInput = document.getElementById('id_password2');

    if (passwordInput && confirmInput) {
      confirmInput.addEventListener('blur', function () {
        if (this.value && passwordInput.value !== this.value) {
          this.setCustomValidity('Passwords do not match');
        } else {
          this.setCustomValidity('');
        }
        validateField(this);
      });

      passwordInput.addEventListener('input', function () {
        if (confirmInput.value) {
          if (this.value === confirmInput.value) {
            confirmInput.setCustomValidity('');
          } else {
            confirmInput.setCustomValidity('Passwords do not match');
          }
        }
      });
    }
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export for testing/external access
  window.EntrancePages = {
    togglePassword: togglePassword,
    validateField: validateField,
  };
})();
