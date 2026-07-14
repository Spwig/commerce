/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';
  function init() {
    document.querySelectorAll('[data-webhook-path]').forEach(function (el) {
      el.textContent = window.location.origin + el.dataset.webhookPath;
    });
    const cards = document.querySelectorAll('.account-card');
    if (cards.length > 0) {
      cards.forEach(function (card) {
        card.addEventListener('click', function () {
          cards.forEach(function (c) {
            c.classList.remove('selected');
          });
          this.classList.add('selected');
          const radio = this.querySelector('input[type="radio"]');
          if (radio) radio.checked = true;
        });
      });
    }
    const domain = window.location.hostname;
    document.querySelectorAll('.merchant-domain').forEach(function (el) {
      el.textContent = domain;
    });
  }
  document.addEventListener('click', function (e) {
    let b = e.target.closest('[data-action="copy-to-clipboard"][data-copy-id]');
    if (b) {
      const el = document.getElementById(b.dataset.copyId);
      var text = el ? el.textContent.trim() : '';
      navigator.clipboard.writeText(text).then(function () {
        const orig = b.textContent;
        b.textContent = 'Copied!';
        b.classList.add('success');
        setTimeout(function () {
          b.textContent = orig;
          b.classList.remove('success');
        }, 2000);
      });
      return;
    }
    b = e.target.closest('[data-action="copy-to-clipboard"][data-copy-value]');
    if (b) {
      navigator.clipboard.writeText(b.dataset.copyValue || '').then(function () {
        const orig = b.textContent;
        b.textContent = 'Copied!';
        b.classList.add('copied');
        setTimeout(function () {
          b.textContent = orig;
          b.classList.remove('copied');
        }, 2000);
      });
      return;
    }
    b = e.target.closest('[data-action="copy-text"]');
    if (b && b.dataset.copyValue !== undefined) {
      navigator.clipboard.writeText(b.dataset.copyValue || '').then(function () {
        const orig = b.textContent;
        b.textContent = 'Copied!';
        setTimeout(function () {
          b.textContent = orig;
        }, 2000);
      });
      return;
    }
    b = e.target.closest('.copy-btn[data-copy-target]');
    if (b) {
      const target = b.getAttribute('data-copy-target');
      const targetEl = document.querySelector(target);
      var text = targetEl ? targetEl.textContent.trim() : '';
      navigator.clipboard.writeText(text).then(function () {
        const orig = b.innerHTML;
        b.innerHTML = '<i class="fas fa-check"></i> Copied!';
        setTimeout(function () {
          b.innerHTML = orig;
        }, 2000);
      });
      return;
    }
    b = e.target.closest('[data-action="switch-tab"]');
    if (b) {
      const tab = b.dataset.tab;
      const container = b.closest('.provider-tabs, .tabs, .registrar-tabs');
      if (container) {
        const section = container.parentElement || document;
        section.querySelectorAll('.provider-content, .tab-content').forEach(function (el) {
          el.classList.remove('active');
        });
        container.querySelectorAll('[data-action="switch-tab"]').forEach(function (el) {
          el.classList.remove('active');
        });
      } else {
        document.querySelectorAll('.provider-content, .tab-content').forEach(function (el) {
          el.classList.remove('active');
        });
        document.querySelectorAll('[data-action="switch-tab"]').forEach(function (el) {
          el.classList.remove('active');
        });
      }
      const content =
        document.getElementById(tab + '-content') ||
        document.getElementById(tab + '-tab') ||
        document.getElementById(tab);
      if (content) content.classList.add('active');
      b.classList.add('active');
    }
  });
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
