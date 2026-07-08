/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var selectAll = document.getElementById('select-all');
        var checkboxes = document.querySelectorAll('input[name="product_ids"]');

        if (selectAll) {
            selectAll.addEventListener('change', function (e) {
                checkboxes.forEach(function (cb) { cb.checked = e.target.checked; });
            });
        }

        checkboxes.forEach(function (cb) {
            cb.addEventListener('change', function () {
                var allChecked = Array.from(checkboxes).every(function (c) { return c.checked; });
                var someChecked = Array.from(checkboxes).some(function (c) { return c.checked; });
                if (selectAll) {
                    selectAll.checked = allChecked;
                    selectAll.indeterminate = someChecked && !allChecked;
                }
            });
        });

        // Handle data-confirm buttons
        document.addEventListener('click', async function (e) {
            var btn = e.target.closest('[data-confirm]');
            if (!btn) return;
            var msg = btn.getAttribute('data-confirm');
            if (msg) {
                e.preventDefault();
                if (!await AdminModal.confirm({ message: msg, danger: true, confirmText: 'Confirm' })) {
                    return;
                }
                // Re-trigger the action after confirmation
                if (btn.tagName === 'A') {
                    window.location.href = btn.href;
                } else if (btn.form) {
                    if (btn.name) {
                        var hidden = document.createElement('input');
                        hidden.type = 'hidden';
                        hidden.name = btn.name;
                        hidden.value = btn.value || '';
                        btn.form.appendChild(hidden);
                    }
                    btn.form.submit();
                } else {
                    btn.removeAttribute('data-confirm');
                    btn.click();
                }
            }
        });
    });
})();
