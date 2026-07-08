/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initSaveButtons();
    });

    function initSaveButtons() {
        var form = document.getElementById('shippingpromotion_form');
        var saveContinueBtn = document.getElementById('sr-save-continue-btn');
        var saveBtn = document.getElementById('sr-save-btn');

        if (saveContinueBtn && form) {
            saveContinueBtn.addEventListener('click', function() {
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = '_continue';
                input.value = '1';
                form.appendChild(input);
                form.submit();
            });
        }

        if (saveBtn && form) {
            saveBtn.addEventListener('click', function() {
                form.submit();
            });
        }
    }
})();
