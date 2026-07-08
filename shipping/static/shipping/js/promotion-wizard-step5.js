/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Promotion Wizard Step 5: Advanced Settings & Review
 * Validates that end date is after start date.
 */

(function() {
    'use strict';

    var configEl = document.getElementById('promotion-wizard-step5-config');
    var i18n = {};
    if (configEl) {
        try {
            var config = JSON.parse(configEl.textContent);
            i18n = config.i18n || {};
        } catch (e) {
            // fall back to empty strings
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        var form = document.getElementById('rule-review-form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            var startDate = document.getElementById('id_start_date').value;
            var endDate = document.getElementById('id_end_date').value;

            if (startDate && endDate && new Date(startDate) >= new Date(endDate)) {
                AdminModal.alert({message: i18n.endDateError || 'End date must be after start date', type: 'error'});
                e.preventDefault();
                return;
            }
        });
    });

}());
