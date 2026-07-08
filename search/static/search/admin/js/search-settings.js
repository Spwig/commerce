/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Search Settings Form
 *
 * Handles slider synchronization for relevance weight fields.
 */

(function() {
    'use strict';

    function initSearchSettings() {
        // Slider synchronization
        document.querySelectorAll('input[type="range"]').forEach(function(slider) {
            var targetId = slider.dataset.target;
            var targetInput = document.getElementById(targetId);
            var valueDisplay = slider.parentNode.querySelector('.slider-value');

            if (!targetInput || !valueDisplay) return;

            slider.addEventListener('input', function() {
                targetInput.value = this.value;
                valueDisplay.textContent = this.value;
            });

            targetInput.addEventListener('input', function() {
                slider.value = this.value;
                valueDisplay.textContent = this.value;
            });
        });
    }

    document.addEventListener('DOMContentLoaded', initSearchSettings);

})();
