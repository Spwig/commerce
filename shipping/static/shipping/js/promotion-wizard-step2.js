/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Promotion Wizard Step 2: Cart Conditions
 * Validates that min <= max for cart value, cart weight, and item count.
 */

(function() {
    'use strict';

    var configEl = document.getElementById('promotion-wizard-step2-config');
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
        var form = document.getElementById('rule-conditions-form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            // Validate cart value
            var minValue = parseFloat(document.getElementById('id_min_cart_value').value) || 0;
            var maxValue = parseFloat(document.getElementById('id_max_cart_value').value) || Infinity;

            if (minValue > 0 && maxValue > 0 && minValue > maxValue) {
                AdminModal.alert({message: i18n.minCartValueError || 'Minimum cart value cannot be greater than maximum cart value', type: 'error'});
                e.preventDefault();
                return;
            }

            // Validate cart weight
            var minWeight = parseFloat(document.getElementById('id_min_cart_weight').value) || 0;
            var maxWeight = parseFloat(document.getElementById('id_max_cart_weight').value) || Infinity;

            if (minWeight > 0 && maxWeight > 0 && minWeight > maxWeight) {
                AdminModal.alert({message: i18n.minCartWeightError || 'Minimum cart weight cannot be greater than maximum cart weight', type: 'error'});
                e.preventDefault();
                return;
            }

            // Validate item count
            var minItems = parseInt(document.getElementById('id_min_item_count').value) || 0;
            var maxItems = parseInt(document.getElementById('id_max_item_count').value) || Infinity;

            if (minItems > 0 && maxItems > 0 && minItems > maxItems) {
                AdminModal.alert({message: i18n.minItemCountError || 'Minimum item count cannot be greater than maximum item count', type: 'error'});
                e.preventDefault();
                return;
            }
        });
    });

}());
