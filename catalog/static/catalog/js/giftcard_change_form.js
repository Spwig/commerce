/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * GiftCard Change Form JavaScript
 * Handles save buttons only.
 * Tab switching is handled by the global AdminTabs utility (admin-tabs.js).
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initSaveButtons();
    });

    function initSaveButtons() {
        var form = document.getElementById('giftcard_form');
        if (!form) return;

        var saveContinueBtn = document.getElementById('gc-save-continue-btn');
        if (saveContinueBtn) {
            saveContinueBtn.addEventListener('click', function() {
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = '_continue';
                input.value = '1';
                form.appendChild(input);
                form.submit();
            });
        }

        var saveBtn = document.getElementById('gc-save-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', function() {
                form.submit();
            });
        }
    }

})();
