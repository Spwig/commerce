/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Blog Subscription Form
 * Handles AJAX subscription for blog sidebar and post detail CTA forms.
 * Replaces inline onsubmit="return false;" + inline <script> blocks.
 *
 * Usage: add data-subscribe-url="<url>" and data-message-el="<id>" to the form.
 */
(function () {
  'use strict';

  function initSubscribeForm(form) {
    const url = form.dataset.subscribeUrl;
    const msgEl = document.getElementById(form.dataset.messageEl || '');

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const emailInput = form.querySelector('[name="email"]');
      const btn = form.querySelector('button[type="submit"]');
      const email = emailInput ? emailInput.value : '';

      if (btn) btn.disabled = true;
      if (msgEl) {
        msgEl.className = 'blog-sidebar__subscribe-msg';
        msgEl.style.display = 'none';
      }

      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email }),
      })
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          if (msgEl) {
            if (data.success) {
              msgEl.textContent = data.message;
              msgEl.className = 'blog-sidebar__subscribe-msg blog-sidebar__subscribe-msg--success';
              if (emailInput) emailInput.value = '';
            } else {
              msgEl.textContent = data.error || 'Something went wrong.';
              msgEl.className = 'blog-sidebar__subscribe-msg blog-sidebar__subscribe-msg--error';
            }
            msgEl.style.display = 'block';
          }
          if (btn) btn.disabled = false;
        })
        .catch(function () {
          if (msgEl) {
            msgEl.textContent = 'Network error. Please try again.';
            msgEl.className = 'blog-sidebar__subscribe-msg blog-sidebar__subscribe-msg--error';
            msgEl.style.display = 'block';
          }
          if (btn) btn.disabled = false;
        });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form[data-subscribe-url]').forEach(initSubscribeForm);
  });
})();
