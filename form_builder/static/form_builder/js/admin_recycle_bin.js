/* Form Builder Recycle Bin JS */
/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var selectAll = document.getElementById('select-all');
        var checkboxes = document.querySelectorAll('input[name="form_ids"]');

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
                if (await AdminModal.confirm({
                    message: msg,
                    danger: true,
                    confirmText: 'Delete'
                })) {
                    var form = btn.closest('form');
                    if (form) form.submit();
                }
            }
        });
    });
})();
