/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    if (window._widgetAccountInit) { return; }
    window._widgetAccountInit = true;

    function initWidget(widget) {
        if (widget.dataset.accountInitialized) { return; }
        widget.dataset.accountInitialized = 'true';

        var button = widget.querySelector('.widget-account-button');
        var menu = widget.querySelector('.widget-account-menu');

        if (!button || !menu) { return; }

        button.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            var isOpen = widget.classList.contains('is-open');

            document.querySelectorAll('.widget-account.is-open').forEach(function (w) {
                w.classList.remove('is-open');
                var btn = w.querySelector('.widget-account-button');
                if (btn) { btn.setAttribute('aria-expanded', 'false'); }
            });

            if (!isOpen) {
                widget.classList.add('is-open');
                button.setAttribute('aria-expanded', 'true');
            }
        });

        document.addEventListener('click', function (e) {
            if (!widget.contains(e.target)) {
                widget.classList.remove('is-open');
                button.setAttribute('aria-expanded', 'false');
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && widget.classList.contains('is-open')) {
                widget.classList.remove('is-open');
                button.setAttribute('aria-expanded', 'false');
                button.focus();
            }
        });

        menu.addEventListener('keydown', function (e) {
            var links = menu.querySelectorAll('.widget-account-link');
            var currentIndex = Array.prototype.indexOf.call(links, document.activeElement);

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                var nextIndex = (currentIndex + 1) % links.length;
                if (links[nextIndex]) { links[nextIndex].focus(); }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                var prevIndex = currentIndex <= 0 ? links.length - 1 : currentIndex - 1;
                if (links[prevIndex]) { links[prevIndex].focus(); }
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('.widget-account').forEach(initWidget);
    });
}());
