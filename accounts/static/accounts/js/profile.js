/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Account Profile Page
 * Handles business account toggle visibility.
 * Replaces inline onchange="toggleBusinessFields(this.checked)".
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // Business account toggle
    document.addEventListener('change', function (e) {
      const checkbox = e.target.closest('[data-action="toggle-business-fields"]');
      if (!checkbox) return;

      const businessFields = document.getElementById('business-fields');
      if (businessFields) {
        businessFields.classList.toggle('hidden', !checkbox.checked);
      }
    });
  });
})();
