/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    function init() {
        var methodTypeSelect = document.getElementById('id_method_type');
        if (!methodTypeSelect) { return; }
        methodTypeSelect.addEventListener('change', updateConditionalFields);
        updateConditionalFields();
    }

    function updateConditionalFields() {
        var methodTypeSelect = document.getElementById('id_method_type');
        var flatRateSection = document.getElementById('flat-rate-section');
        var flatRateCostInput = document.getElementById('id_flat_rate_cost');
        var carrierSection = document.getElementById('carrier-section');
        var carrierInput = document.getElementById('id_carrier');

        if (!methodTypeSelect) { return; }
        var methodType = methodTypeSelect.value;

        if (flatRateSection && flatRateCostInput) {
            if (methodType === 'flat_rate') {
                flatRateSection.style.display = 'block';
                flatRateCostInput.setAttribute('required', 'required');
            } else {
                flatRateSection.style.display = 'none';
                flatRateCostInput.removeAttribute('required');
            }
        }

        if (carrierSection) {
            if (methodType === 'real_time') {
                carrierSection.style.display = 'block';
                if (carrierInput) { carrierInput.setAttribute('required', 'required'); }
            } else {
                carrierSection.style.display = 'none';
                if (carrierInput) { carrierInput.removeAttribute('required'); }
            }
        }
    }

    document.addEventListener('DOMContentLoaded', init);
}());
