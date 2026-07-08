/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var form = document.getElementById('settings-form');
        var saveContinueBtn = document.getElementById('save-continue-btn');

        if (saveContinueBtn && form) {
            saveContinueBtn.addEventListener('click', function () {
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = '_continue';
                input.value = '1';
                form.appendChild(input);
                form.submit();
            });
        }
    });
}());
