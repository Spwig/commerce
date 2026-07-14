/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Payment Provider Wizard Step 4: Test Connection
 * Auto-submits the test form after a short delay.
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    // Auto-submit form to start test
    setTimeout(function () {
      const form = document.getElementById('test-form');
      if (form) {
        form.submit();
      }
    }, 500);
  });
})();
