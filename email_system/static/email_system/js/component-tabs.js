/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* Component interactions - tab switching & copy-to-clipboard */
/* Used in provider setup instructions and DNS requirements fragments */
(function () {
    'use strict';
    document.addEventListener('click', function (e) {
        /* Tab switching (si-tab pattern) */
        var tabBtn = e.target.closest('[data-action="switch-si-tab"]');
        if (tabBtn) {
            var tab = tabBtn.dataset.tab;
            var container = tabBtn.closest('.setup-instructions, .dns-requirements-iframe-container') || document;
            container.querySelectorAll('.si-tab').forEach(function (el) { el.classList.remove('active'); });
            container.querySelectorAll('.si-tab-content').forEach(function (el) { el.classList.remove('active'); });
            tabBtn.classList.add('active');
            var content = document.getElementById(tab + '-si-tab');
            if (content) content.classList.add('active');
            return;
        }

        /* Copy to clipboard */
        var copyBtn = e.target.closest('[data-action="copy-to-clipboard"]');
        if (copyBtn) {
            var value = copyBtn.dataset.copyValue;
            if (value && navigator.clipboard) {
                navigator.clipboard.writeText(value).then(function () {
                    var originalText = copyBtn.textContent;
                    copyBtn.textContent = '\u2713 Copied';
                    copyBtn.classList.add('copied');
                    setTimeout(function () {
                        copyBtn.textContent = originalText;
                        copyBtn.classList.remove('copied');
                    }, 2000);
                });
            }
        }
    });
}());
