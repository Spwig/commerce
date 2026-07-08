/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var translations = {};

    function init() {
        var dataEl = document.getElementById('oauth-wizard-data');
        if (dataEl) {
            try {
                var data = JSON.parse(dataEl.textContent);
                translations = data.translations || {};
            } catch (e) {}
        }
        document.addEventListener('click', handleActions);
        applyProviderColors();
    }

    function applyProviderColors() {
        document.querySelectorAll('[data-color]').forEach(function (el) {
            var color = el.dataset.color;
            if (color) {
                el.style.backgroundColor = color + '20';
                el.style.color = color;
            }
        });
    }

    function handleActions(e) {
        var btn = e.target.closest('[data-action="copy-to-clipboard"]');
        if (btn) {
            copyToClipboard(btn);
        }
    }

    function copyToClipboard(btn) {
        var text = btn.dataset.copy || '';
        if (!text) { return; }
        navigator.clipboard.writeText(text).then(function () {
            var originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> ' + (translations.copied || 'Copied!');
            setTimeout(function () {
                btn.innerHTML = originalHTML;
            }, 2000);
        });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
