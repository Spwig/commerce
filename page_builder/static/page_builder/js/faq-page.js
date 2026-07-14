/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * FAQ page functionality: accordion expand/collapse and smooth scroll navigation.
 * Used by page_builder/templates/page_builder/pages/faq.html
 */
(function () {
  'use strict';

  function initFaqPage() {
    // Accordion functionality
    document.querySelectorAll('.accordion__trigger').forEach(function (trigger) {
      trigger.addEventListener('click', function () {
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', String(!expanded));
      });
    });

    // Smooth scroll to sections
    document.querySelectorAll('.faq-nav__link').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').slice(1);
        const target = document.getElementById(targetId);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          document.querySelectorAll('.faq-nav__link').forEach(function (l) {
            l.classList.remove('faq-nav__link--active');
          });
          link.classList.add('faq-nav__link--active');
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initFaqPage);
  } else {
    initFaqPage();
  }
})();
