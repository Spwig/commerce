/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        // Handle provider card selection
        var providerCards = document.querySelectorAll('.provider-option');
        var continueBtn = document.getElementById('continue-btn');

        providerCards.forEach(function (card) {
            card.addEventListener('click', function () {
                // Uncheck all
                providerCards.forEach(function (c) {
                    c.classList.remove('selected');
                    var inner = c.querySelector('.provider-option-inner');
                    if (inner) inner.style.borderColor = 'transparent';
                });

                // Check this one
                var radio = this.querySelector('input[type="radio"]');
                if (radio) {
                    radio.checked = true;
                    this.classList.add('selected');
                    var inner = this.querySelector('.provider-option-inner');
                    if (inner) {
                        inner.style.borderColor = 'var(--primary)';
                        inner.style.background = 'var(--primary-lighten)';
                    }
                    continueBtn.disabled = false;
                }
            });
        });
    });
})();
