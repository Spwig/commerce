/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('change', function (e) {
        var el = e.target.closest('[data-action]');
        if (!el) return;

        if (el.dataset.autoSubmit === 'true') {
            var form = el.closest('form');
            if (form) form.submit();
            return;
        }

        if (el.dataset.action === 'preview-logo') {
            var preview = document.getElementById('logo-preview');
            if (!preview) return;
            if (el.files && el.files[0]) {
                var reader = new FileReader();
                reader.onload = function (ev) {
                    preview.innerHTML = '<img src="' + ev.target.result + '" alt="Logo preview">';
                };
                reader.readAsDataURL(el.files[0]);
            }
        }
    });

    document.addEventListener('click', async function (e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) return;

        switch (btn.dataset.action) {
            case 'dismiss-alert':
                btn.closest('.dev-alert')?.remove();
                break;

            case 'copy-api-key': {
                var targetEl = document.getElementById(btn.dataset.target);
                if (targetEl) {
                    navigator.clipboard.writeText(targetEl.textContent.trim()).catch(function () {});
                }
                break;
            }

            case 'confirm-before-submit': {
                e.preventDefault();
                var msg = btn.dataset.confirmMessage || '';
                if (await AdminModal.confirm(msg)) {
                    var form = btn.closest('form');
                    if (form) form.submit();
                }
                break;
            }
        }
    });

}());
