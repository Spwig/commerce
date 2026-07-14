/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  if (window._widgetNewsletterInit) {
    return;
  }
  window._widgetNewsletterInit = true;

  function initWidget(widget) {
    if (widget.dataset.newsletterInitialized) {
      return;
    }
    widget.dataset.newsletterInitialized = 'true';

    const form = widget.querySelector('.widget-newsletter-form');
    const messageEl = widget.querySelector('.widget-newsletter-message');

    if (!form || !messageEl) {
      return;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const emailInput = form.querySelector('input[name="email"]');
      const submitBtn = form.querySelector('button[type="submit"]');
      if (!emailInput || !submitBtn) {
        return;
      }

      const email = emailInput.value.trim();
      if (!email) {
        return;
      }

      // Disable form during submission
      submitBtn.disabled = true;
      const originalText = submitBtn.textContent;
      submitBtn.textContent = '...';

      const meta = document.querySelector('meta[name="csrf-token"]');
      let csrfTokenValue = meta && meta.content ? meta.content : '';
      if (!csrfTokenValue) {
        const csrfInput = form.querySelector('[name="csrfmiddlewaretoken"]');
        csrfTokenValue = csrfInput ? csrfInput.value : '';
      }
      const headers = {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      };
      if (csrfTokenValue) {
        headers['X-CSRFToken'] = csrfTokenValue;
      }

      fetch(form.action, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ email: email }),
      })
        .then(function (response) {
          return response.json().then(function (data) {
            return { ok: response.ok, data: data };
          });
        })
        .then(function (result) {
          const defaultSuccess = widget.dataset.successMessage || 'Thank you for subscribing!';
          const defaultError =
            widget.dataset.errorMessage || 'Subscription failed. Please try again.';
          if (result.ok && result.data.success !== false) {
            showMessage(messageEl, result.data.message || defaultSuccess, 'success');
            emailInput.value = '';
          } else {
            showMessage(
              messageEl,
              result.data.error || result.data.message || defaultError,
              'error'
            );
          }
        })
        .catch(function () {
          // If fetch fails (network error or non-JSON response), fall back to standard form submit
          form.removeEventListener('submit', arguments.callee);
          form.submit();
          return;
        })
        .finally(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = originalText;
        });
    });
  }

  function showMessage(el, text, type) {
    el.textContent = text;
    el.className = 'widget-newsletter-message widget-newsletter-message--' + type;
    el.style.display = '';

    // Auto-hide after 5 seconds
    clearTimeout(el._hideTimeout);
    el._hideTimeout = setTimeout(function () {
      el.style.display = 'none';
    }, 5000);
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.widget-newsletter').forEach(initWidget);
  });
})();
