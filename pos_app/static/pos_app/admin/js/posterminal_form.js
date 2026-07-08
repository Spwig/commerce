/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * POS Terminal Change Form - Save Button Handlers
 * Wires header save buttons to the hidden Django submit inputs.
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        var form = document.getElementById('posterminal_form');
        if (!form) return;

        var saveContinueBtn = document.getElementById('term-save-continue-btn');
        var saveBtn = document.getElementById('term-save-btn');

        if (saveContinueBtn) {
            saveContinueBtn.addEventListener('click', function() {
                var continueInput = form.querySelector('input[name="_continue"]');
                if (continueInput) {
                    continueInput.click();
                }
            });
        }

        if (saveBtn) {
            saveBtn.addEventListener('click', function() {
                var saveInput = form.querySelector('input[name="_save"]');
                if (saveInput) {
                    saveInput.click();
                }
            });
        }
    });
})();
