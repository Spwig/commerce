/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * ContactForm - Validation and AJAX submission for the contact form element.
 * Submits to /api/messages/contact/ (or custom action URL) which creates
 * a CustomerMessage record visible in the merchant's admin and mobile app.
 */
class ContactForm {
  constructor(element) {
    this.element = element;
    this.form = element.querySelector('.contact-form');

    if (!this.form) {
      return;
    }

    this.submitBtn = this.form.querySelector('button[type="submit"]');
    this.errorMessage = element.querySelector('#error-message');
    this.successMessage = element.querySelector('#success-message');
    this.submitting = false;
    this.init();
  }

  init() {
    this.form.addEventListener('submit', e => this.handleSubmit(e));

    // Clear error state on input
    this.form.querySelectorAll('.form-input').forEach(input => {
      input.addEventListener('input', () => {
        input.classList.remove('form-input--error');
        if (this.errorMessage) {
          this.errorMessage.classList.add('hidden');
        }
      });
    });
  }

  async handleSubmit(e) {
    e.preventDefault();

    if (this.submitting) return;

    if (!this.validateForm()) {
      this.showError();
      return;
    }

    this.submitting = true;
    if (this.submitBtn) {
      this.submitBtn.disabled = true;
      this.submitBtn.dataset.originalText = this.submitBtn.textContent;
      this.submitBtn.textContent = this.submitBtn.textContent.trim() + '...';
    }

    try {
      const payload = this.buildPayload();
      const actionUrl = this.form.getAttribute('action') || '/api/messages/contact/';
      const meta = document.querySelector('meta[name="csrf-token"]');
      let csrfToken = meta && meta.content ? meta.content : '';
      if (!csrfToken) {
        const csrfInput = this.form.querySelector('[name="csrfmiddlewaretoken"]');
        csrfToken = csrfInput ? csrfInput.value : '';
      }

      const response = await fetch(actionUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(payload),
      });

      if (response.status === 201) {
        this.showSuccess();
        this.form.reset();
      } else if (response.status === 429) {
        this.showError('Too many submissions. Please try again later.');
      } else if (response.status === 400) {
        const data = await response.json();
        const errors = data.errors || {};
        const firstError = Object.values(errors).flat()[0];
        this.showError(firstError || 'Please check your input and try again.');
      } else {
        this.showError();
      }
    } catch {
      this.showError();
    } finally {
      this.submitting = false;
      if (this.submitBtn) {
        this.submitBtn.disabled = false;
        if (this.submitBtn.dataset.originalText) {
          this.submitBtn.textContent = this.submitBtn.dataset.originalText;
        }
      }
    }
  }

  /**
   * Build JSON payload mapping form fields to the API's expected format.
   * API expects: name, email, phone, subject, message, message_type
   */
  buildPayload() {
    const get = name => {
      const el = this.form.querySelector(`[name="${name}"]`);
      return el ? el.value.trim() : '';
    };

    const firstName = get('first_name');
    const lastName = get('last_name');
    let name = [firstName, lastName].filter(Boolean).join(' ');
    if (!name) name = 'Anonymous';

    return {
      name: name,
      email: get('email'),
      phone: get('phone') || undefined,
      subject: get('subject') || 'Contact Form Inquiry',
      message: get('message'),
      message_type: 'general',
    };
  }

  validateForm() {
    let isValid = true;

    // Validate required fields
    this.form.querySelectorAll('[required]').forEach(field => {
      if (field.type === 'checkbox') {
        if (!field.checked) {
          isValid = false;
          field.classList.add('form-input--error');
        } else {
          field.classList.remove('form-input--error');
        }
      } else if (!field.value.trim()) {
        isValid = false;
        field.classList.add('form-input--error');
      } else {
        field.classList.remove('form-input--error');
      }
    });

    // Email validation
    const emailField = this.form.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(emailField.value)) {
        isValid = false;
        emailField.classList.add('form-input--error');
      } else {
        emailField.classList.remove('form-input--error');
      }
    }

    return isValid;
  }

  showSuccess() {
    if (this.successMessage) {
      this.successMessage.classList.remove('hidden');
    }
    if (this.errorMessage) {
      this.errorMessage.classList.add('hidden');
    }
  }

  showError(customMessage) {
    if (this.errorMessage) {
      if (customMessage) {
        this.errorMessage.textContent = customMessage;
      }
      this.errorMessage.classList.remove('hidden');
    }
    if (this.successMessage) {
      this.successMessage.classList.add('hidden');
    }
  }
}

// Self-initialize: Find all contact form elements and create instances
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-contact-form]').forEach(element => {
    new ContactForm(element);
  });
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ContactForm;
}
