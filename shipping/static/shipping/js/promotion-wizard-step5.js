/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Promotion Wizard Step 5: Advanced Settings & Review
 * Validates that end date is after start date.
 */

(function () {
  'use strict';

  const configEl = document.getElementById('promotion-wizard-step5-config');
  let i18n = {};
  if (configEl) {
    try {
      const config = JSON.parse(configEl.textContent);
      i18n = config.i18n || {};
    } catch (e) {
      // fall back to empty strings
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('rule-review-form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      const startDate = document.getElementById('id_start_date').value;
      const endDate = document.getElementById('id_end_date').value;

      if (startDate && endDate && new Date(startDate) >= new Date(endDate)) {
        AdminModal.alert({
          message: i18n.endDateError || 'End date must be after start date',
          type: 'error',
        });
        e.preventDefault();
        return;
      }
    });
  });
})();
