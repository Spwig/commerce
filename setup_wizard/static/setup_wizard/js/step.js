/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Setup Wizard - Step Page JavaScript
 *
 * Description: Handles progress bar rendering and form submission
 * Template: setup_wizard/templates/setup_wizard/step.html
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // Set progress bar width from data attribute
    const progressFills = document.querySelectorAll('.setup-progress-fill[data-progress]');
    progressFills.forEach(function (fill) {
      const progress = fill.getAttribute('data-progress');
      if (progress) {
        fill.style.width = progress + '%';
      }
    });
  });
})();
