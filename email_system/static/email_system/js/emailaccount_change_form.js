/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initSaveButtons();
    initClipboardActions();
  });

  function initClipboardActions() {
    document.addEventListener('click', function (e) {
      const button = e.target.closest('[data-action="copy-to-clipboard"]');
      if (!button) return;

      const text = button.getAttribute('data-clipboard-text');
      if (!text) return;

      navigator.clipboard
        .writeText(text)
        .then(function () {
          const originalHtml = button.innerHTML;
          button.innerHTML = '<i class="fas fa-check"></i> Copied!';
          setTimeout(function () {
            button.innerHTML = originalHtml;
          }, 2000);
        })
        .catch(function () {
          // Fallback for older browsers
          const textarea = document.createElement('textarea');
          textarea.value = text;
          textarea.setAttribute('readonly', '');
          textarea.style.position = 'absolute';
          textarea.style.left = '-9999px';
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand('copy');
          document.body.removeChild(textarea);
        });
    });
  }

  function initSaveButtons() {
    const form = document.getElementById('emailaccount_form');
    const saveContinueBtn = document.getElementById('ea-save-continue-btn');
    const saveBtn = document.getElementById('ea-save-btn');

    if (saveContinueBtn && form) {
      saveContinueBtn.addEventListener('click', function () {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = '_continue';
        input.value = '1';
        form.appendChild(input);
        form.submit();
      });
    }

    if (saveBtn && form) {
      saveBtn.addEventListener('click', function () {
        form.submit();
      });
    }
  }
})();
