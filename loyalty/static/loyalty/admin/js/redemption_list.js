/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var translations = {};

    function init() {
        var tEl = document.getElementById('redemption-list-translations');
        if (tEl) {
            try { translations = JSON.parse(tEl.textContent); } catch (e) {}
        }
        document.addEventListener('click', handleActions);
    }

    async function handleActions(e) {
        var btn = e.target.closest('[data-action="confirm-fulfill"]');
        if (!btn) return;
        e.preventDefault();
        var msg = btn.dataset.confirmMsg ||
            translations.confirmFulfill ||
            'Mark this redemption as fulfilled?';
        await AdminModal.confirm(msg);
    }

    document.addEventListener('DOMContentLoaded', init);
}());
