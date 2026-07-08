/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Preview Language Switcher
 * Handles language switching in admin preview mode
 */
(function() {
    'use strict';

    const LanguageSwitcher = {
        init() {
            this.bindEvents();
        },

        bindEvents() {
            // Event delegation for language switcher actions
            document.addEventListener('click', (e) => {
                // Toggle dropdown button
                const toggleBtn = e.target.closest('[data-action="toggle-language-dropdown"]');
                if (toggleBtn) {
                    e.preventDefault();
                    this.toggleDropdown();
                    return;
                }

                // Switch language button
                const switchBtn = e.target.closest('[data-action="switch-preview-language"]');
                if (switchBtn) {
                    e.preventDefault();
                    const langCode = switchBtn.dataset.lang;
                    if (langCode) {
                        this.switchLanguage(langCode);
                    }
                    return;
                }

                // Close dropdown when clicking outside
                const languageSwitcher = document.querySelector('#preview-language-switcher');
                if (languageSwitcher && !languageSwitcher.contains(e.target)) {
                    this.closeDropdown();
                }
            });

            // Close dropdown on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.closeDropdown();
                }
            });
        },

        toggleDropdown() {
            const switcher = document.querySelector('#preview-language-switcher');
            const dropdown = document.getElementById('languageDropdown');

            if (!switcher || !dropdown) return;

            const isOpen = switcher.classList.contains('open');

            if (isOpen) {
                switcher.classList.remove('open');
                dropdown.setAttribute('aria-expanded', 'false');
            } else {
                switcher.classList.add('open');
                dropdown.setAttribute('aria-expanded', 'true');
            }
        },

        closeDropdown() {
            const languageSwitcher = document.querySelector('#preview-language-switcher');
            if (languageSwitcher && languageSwitcher.classList.contains('open')) {
                languageSwitcher.classList.remove('open');
                const dropdown = languageSwitcher.querySelector('[aria-expanded]');
                if (dropdown) {
                    dropdown.setAttribute('aria-expanded', 'false');
                }
            }
        },

        switchLanguage(languageCode) {
            // Map language codes to Django's expected format
            const languageMapping = {
                'zh': 'zh-hans',  // Chinese -> Simplified Chinese
                'en': 'en-us',    // English -> US English
            };

            // Use mapped code if available, otherwise use original
            const djangoLanguageCode = languageMapping[languageCode] || languageCode;

            // Set language cookie with the Django-compatible code
            const expires = new Date();
            expires.setTime(expires.getTime() + (365 * 24 * 60 * 60 * 1000)); // 1 year
            document.cookie = `lang=${djangoLanguageCode}; expires=${expires.toUTCString()}; path=/; SameSite=Lax`;

            // Get the preview iframe
            const iframe = document.getElementById('preview');
            if (iframe) {
                // Get current iframe URL
                const currentUrl = iframe.src;
                const urlObj = new URL(currentUrl, window.location.origin);

                // Update the path with Django-compatible language code
                const pathParts = urlObj.pathname.split('/').filter(part => part);

                // Check if first part is a language code pattern
                if (pathParts.length > 0 && pathParts[0].match(/^[a-z]{2}(-[a-z]{2,4})?$/i)) {
                    // Replace existing language code
                    pathParts[0] = djangoLanguageCode;
                } else {
                    // Add language code at the beginning
                    pathParts.unshift(djangoLanguageCode);
                }

                // Construct new URL
                const newPath = '/' + pathParts.join('/');
                const newUrl = `${urlObj.protocol}//${urlObj.host}${newPath}${urlObj.search}${urlObj.hash}`;

                // Show loading indicator
                const loadingIndicator = document.querySelector('.loading-indicator');
                if (loadingIndicator) {
                    loadingIndicator.classList.add('active');
                }

                // Reload iframe with new language URL
                iframe.src = newUrl;

                // Update the current language display
                const langCodeDisplay = document.querySelector('#preview-language-switcher .current-lang-code');
                if (langCodeDisplay) {
                    langCodeDisplay.textContent = languageCode.toUpperCase();
                }

                // Update active state in dropdown
                document.querySelectorAll('#preview-language-switcher .language-option').forEach(btn => {
                    const isActive = btn.dataset.lang === languageCode;
                    btn.classList.toggle('active', isActive);

                    // Update checkmark
                    let checkmark = btn.querySelector('.checkmark');
                    if (isActive && !checkmark) {
                        checkmark = document.createElement('span');
                        checkmark.className = 'checkmark';
                        checkmark.textContent = '✓';
                        btn.appendChild(checkmark);
                    } else if (!isActive && checkmark) {
                        checkmark.remove();
                    }
                });

                // Close dropdown
                this.closeDropdown();
            }
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => LanguageSwitcher.init());
    } else {
        LanguageSwitcher.init();
    }

    // Expose for debugging
    window.PreviewLanguageSwitcher = LanguageSwitcher;

})();
