/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  function toggleLanguageDropdown() {
    const switcher = document.querySelector('.language-switcher');
    const dropdown = document.getElementById('languageDropdown');
    if (!switcher || !dropdown) return;

    const isOpen = switcher.classList.contains('open');

    if (isOpen) {
      switcher.classList.remove('open');
      dropdown.setAttribute('aria-expanded', 'false');
    } else {
      document.querySelectorAll('.language-switcher.open').forEach(function (el) {
        el.classList.remove('open');
        const btn = el.querySelector('[aria-expanded]');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      });
      switcher.classList.add('open');
      dropdown.setAttribute('aria-expanded', 'true');
    }
  }

  function setLanguageAndRedirect(languageCode) {
    const expires = new Date();
    expires.setTime(expires.getTime() + 365 * 24 * 60 * 60 * 1000);
    document.cookie =
      'lang=' + languageCode + '; expires=' + expires.toUTCString() + '; path=/; SameSite=Lax';

    const urlObj = new URL(window.location.href);
    const pathParts = urlObj.pathname.split('/').filter(function (p) {
      return p;
    });
    const languages = [
      'en',
      'es',
      'fr',
      'de',
      'pt',
      'zh-hans',
      'zh-hant',
      'ja',
      'ar',
      'ru',
      'hi',
      'id',
      'ko',
      'tr',
      'vi',
      'it',
      'th',
    ];

    if (pathParts.length > 0 && languages.indexOf(pathParts[0]) !== -1) {
      pathParts[0] = languageCode;
    } else {
      pathParts.unshift(languageCode);
    }

    window.location.href =
      urlObj.protocol +
      '//' +
      urlObj.host +
      '/' +
      pathParts.join('/') +
      urlObj.search +
      urlObj.hash;
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Toggle button via event delegation
    document.addEventListener('click', function (e) {
      const btn = e.target.closest('[data-action="toggle-language-dropdown"]');
      if (btn) {
        toggleLanguageDropdown();
        return;
      }
      // Close on outside click
      const switcher = document.querySelector('.language-switcher');
      if (switcher && !switcher.contains(e.target)) {
        switcher.classList.remove('open');
        const toggle = switcher.querySelector('[aria-expanded]');
        if (toggle) toggle.setAttribute('aria-expanded', 'false');
      }
    });

    // Language form submission
    document.querySelectorAll('.language-form').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        const langInput = form.querySelector('input[name="language"]');
        if (langInput) setLanguageAndRedirect(langInput.value);
      });
    });

    // Close on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        const openSwitcher = document.querySelector('.language-switcher.open');
        if (openSwitcher) {
          openSwitcher.classList.remove('open');
          const toggle = openSwitcher.querySelector('[aria-expanded]');
          if (toggle) toggle.setAttribute('aria-expanded', 'false');
        }
      }
    });
  });
})();
