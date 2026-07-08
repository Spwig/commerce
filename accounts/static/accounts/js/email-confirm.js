/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var removeBtn = document.getElementById('remove-email-btn');
        if (removeBtn) {
            var message = removeBtn.getAttribute('data-confirm') || 'Are you sure?';
            removeBtn.addEventListener('click', async function (e) {
                e.preventDefault();
                if (!await AdminModal.confirm({ message: message, danger: true, confirmText: 'Remove' })) {
                    return;
                }
                removeBtn.closest('form').submit();
            });
        }
    });
}());
