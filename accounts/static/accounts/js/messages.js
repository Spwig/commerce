/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Customer Messages Portal
 * Provides character counter for message and follow-up textareas.
 * Uses data-char-counter and data-max-chars attributes.
 */
(function () {
    'use strict';

    function initCharCounters() {
        document.querySelectorAll('[data-char-counter="true"]').forEach(function (textarea) {
            var max = parseInt(textarea.dataset.maxChars || '5000', 10);
            var formGroup = textarea.closest('.form-group');
            var counter = formGroup ? formGroup.querySelector('.char-count') : null;

            if (!counter) return;

            function update() {
                var len = textarea.value.length;
                counter.textContent = len.toLocaleString();
                if (len > max * 0.9) {
                    counter.classList.add('char-count--warning');
                } else {
                    counter.classList.remove('char-count--warning');
                }
            }

            textarea.addEventListener('input', update);
            update();
        });
    }

    document.addEventListener('DOMContentLoaded', initCharCounters);
})();
