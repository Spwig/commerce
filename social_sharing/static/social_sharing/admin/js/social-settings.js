/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Social Sharing Settings Form
 *
 * Handles the save-and-continue button for the settings form.
 */

(function () {
  'use strict';

  function initSaveButtons() {
    const form = document.getElementById('settings-form');
    const saveContinueBtn = document.getElementById('save-continue-btn');

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
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Tab switching handled by global AdminTabs utility
    initSaveButtons();
  });
})();
