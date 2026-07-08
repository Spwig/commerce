/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Language Selector Widget - Mobile Enhancement
 *
 * On mobile (<=768px), the desktop <select> form is hidden via CSS and replaced
 * with a globe-icon trigger button that opens a bottom-positioned dropdown.
 * Selecting a language sets the hidden <select> value and submits the form,
 * preserving the CSRF-protected POST to Django's set_language view.
 */
(function () {
    'use strict';

    if (window._widgetLanguageInit) { return; }
    window._widgetLanguageInit = true;

    function initWidget(widget) {
        if (widget.dataset.languageInitialized) { return; }
        widget.dataset.languageInitialized = 'true';

        var trigger = widget.querySelector('.language-mobile-trigger');
        var dropdown = widget.querySelector('.language-mobile-dropdown');
        var backdrop = widget.querySelector('.language-mobile-backdrop');
        var form = widget.querySelector('.language-form');
        var select = widget.querySelector('.language-select');
        var options = dropdown ? dropdown.querySelectorAll('.language-mobile-option') : [];

        if (!trigger || !dropdown || !form || !select) { return; }

        function openDropdown() {
            widget.classList.add('is-open');
            dropdown.hidden = false;
            trigger.setAttribute('aria-expanded', 'true');
        }

        function closeDropdown() {
            widget.classList.remove('is-open');
            dropdown.hidden = true;
            trigger.setAttribute('aria-expanded', 'false');
        }

        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            if (widget.classList.contains('is-open')) {
                closeDropdown();
            } else {
                openDropdown();
            }
        });

        if (backdrop) {
            backdrop.addEventListener('click', closeDropdown);
        }

        // Language option selection -- set select value and submit form
        Array.prototype.forEach.call(options, function (option) {
            option.addEventListener('click', function () {
                var langCode = option.dataset.langCode;
                if (langCode && select) {
                    select.value = langCode;
                    form.submit();
                }
            });
        });

        // Close on outside click
        document.addEventListener('click', function (e) {
            if (!widget.contains(e.target)) {
                closeDropdown();
            }
        });

        // Close on Escape
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && widget.classList.contains('is-open')) {
                closeDropdown();
                trigger.focus();
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        var widgets = document.querySelectorAll('.widget-language');
        for (var i = 0; i < widgets.length; i++) {
            initWidget(widgets[i]);
        }
    });
}());
