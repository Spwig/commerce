/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initSaveButtons();
  });

  function initSaveButtons() {
    const form = document.getElementById('loyaltyrule_form');
    const saveContinueBtn = document.getElementById('rule-save-continue-btn');
    const saveBtn = document.getElementById('rule-save-btn');

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
