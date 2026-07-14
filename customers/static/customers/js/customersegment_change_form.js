/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initSaveButtons();
    initColorDots();
  });

  function initSaveButtons() {
    const form = document.getElementById('customersegment_form');
    const saveContinueBtn = document.getElementById('seg-save-continue-btn');
    const saveBtn = document.getElementById('seg-save-btn');

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

  function initColorDots() {
    const dots = document.querySelectorAll('.segment-color-dot[data-color]');
    dots.forEach(function (dot) {
      dot.style.backgroundColor = dot.getAttribute('data-color');
    });
  }
})();
