/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var translations = {};

    function init() {
        var dataEl = document.getElementById('cart-wizard-step5-data');
        if (dataEl) {
            try {
                var data = JSON.parse(dataEl.textContent);
                translations = data.translations || {};
            } catch (e) {}
        }

        var form = document.getElementById('method-review-form');
        if (!form) { return; }

        form.addEventListener('submit', function () {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (!submitBtn) { return; }
            var originalContent = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + (translations.creating || 'Creating...');
            setTimeout(function () {
                if (submitBtn.disabled) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalContent;
                }
            }, 10000);
        });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
