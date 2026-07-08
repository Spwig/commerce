/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        // Initialize progress bar widths from data attributes (CSP-compliant)
        document.querySelectorAll('.migration-progress-bar[data-width]').forEach(function (bar) {
            bar.style.width = bar.dataset.width + '%';
        });
    });

    document.addEventListener('click', async function (e) {
        var link = e.target.closest('[data-action="confirm-navigate"]');
        if (!link) return;
        e.preventDefault();
        var msg = link.dataset.confirmMsg || 'Are you sure?';
        if (await AdminModal.confirm(msg)) {
            window.location.href = link.href;
        }
    });
}());
