/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('reply-composer-form');
    if (!form) return;

    const submitBtn = form.querySelector('[data-action="submit-reply"]');
    const textarea = document.getElementById('reply-text');
    const sendEmailCheckbox = document.getElementById('send-email');
    const statusEl = document.getElementById('reply-status');
    const messageId = form.getAttribute('data-message-id');
    const lang = document.documentElement.lang || 'en';
    const replyUrl = '/' + lang + '/admin/admin_api/customermessage/' + messageId + '/reply/';

    submitBtn.addEventListener('click', function (e) {
      e.preventDefault();

      const replyText = textarea.value.trim();
      if (!replyText) {
        textarea.focus();
        return;
      }

      // Disable button and show loading
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
      statusEl.className = 'reply-status';
      statusEl.style.display = 'none';

      const csrfToken = window.AdminUtils
        ? window.AdminUtils.getCsrfToken()
        : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

      fetch(replyUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({
          reply_text: replyText,
          send_email: sendEmailCheckbox.checked,
        }),
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          if (data.success) {
            statusEl.className = 'reply-status success';
            statusEl.textContent = data.message;
            statusEl.style.display = 'block';

            if (data.email_error) {
              statusEl.textContent = data.message + ' (Email warning: ' + data.email_error + ')';
            }

            // Reload page after short delay to show the reply in thread
            setTimeout(function () {
              window.location.reload();
            }, 1000);
          } else {
            statusEl.className = 'reply-status error';
            statusEl.textContent = data.error || 'An error occurred.';
            statusEl.style.display = 'block';
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Reply';
          }
        })
        .catch(function (error) {
          statusEl.className = 'reply-status error';
          statusEl.textContent = 'Network error. Please try again.';
          statusEl.style.display = 'block';
          submitBtn.disabled = false;
          submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send Reply';
        });
    });
  });
})();
