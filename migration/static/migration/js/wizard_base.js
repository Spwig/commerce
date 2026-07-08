/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var copiedText = '';

    function init() {
        var tEl = document.getElementById('wizard-base-translations');
        if (tEl) {
            try {
                var t = JSON.parse(tEl.textContent);
                copiedText = t.copied || 'Copied!';
            } catch (e) {}
        }

        document.addEventListener('click', function (e) {
            var btn = e.target.closest('[data-action="copy-to-clipboard"]');
            if (!btn) return;
            var text = btn.dataset.copyText || '';
            if (!text) return;
            navigator.clipboard.writeText(text).then(function () {
                var originalHTML = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> ' + copiedText;
                setTimeout(function () {
                    btn.innerHTML = originalHTML;
                }, 2000);
            });
        });
    }

    /* Exported utility for step templates */
    window.MigrationWizard = {
        validateForm: function (formId) {
            var form = document.getElementById(formId);
            if (!form) return true;
            var requiredFields = form.querySelectorAll('[required]');
            var isValid = true;
            requiredFields.forEach(function (field) {
                if (!field.value.trim()) {
                    field.style.borderColor = 'var(--error-fg)';
                    isValid = false;
                } else {
                    field.style.borderColor = 'var(--hairline-color)';
                }
            });
            return isValid;
        }
    };

    document.addEventListener('DOMContentLoaded', init);
}());
