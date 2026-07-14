/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Category Accordion - Interactive expandable image panels.
 * Handles click-to-expand behavior, keyboard navigation,
 * and responsive adjustments.
 */
(function () {
  'use strict';

  document.querySelectorAll('.cat-accordion').forEach(initAccordion);

  function initAccordion(accordion) {
    const panels = accordion.querySelectorAll('.cat-accordion__panel');
    if (panels.length === 0) return;

    const config = {
      height: accordion.dataset.height || 'lg',
      expandRatio: parseInt(accordion.dataset.expandRatio) || 3,
      transitionSpeed: parseInt(accordion.dataset.transitionSpeed) || 400,
    };

    // Apply height class
    accordion.classList.add('cat-accordion--height-' + config.height);

    // Set CSS custom property for expand ratio
    accordion.style.setProperty('--accordion-expand-ratio', config.expandRatio);
    accordion.style.setProperty('--accordion-transition-speed', config.transitionSpeed + 'ms');

    // Click to expand (toggle on mobile, expand on desktop)
    panels.forEach(function (panel) {
      panel.addEventListener('click', function (e) {
        // On mobile (stacked layout), don't interfere - let the link navigate
        if (window.innerWidth <= 768) return;

        // If panel is already active, let the link navigate
        if (panel.classList.contains('cat-accordion__panel--active')) return;

        // Otherwise, expand this panel first (prevent navigation)
        e.preventDefault();
        panels.forEach(function (p) {
          p.classList.remove('cat-accordion__panel--active');
        });
        panel.classList.add('cat-accordion__panel--active');
      });
    });

    // Keyboard navigation
    accordion.addEventListener('keydown', function (e) {
      const activePanel = accordion.querySelector('.cat-accordion__panel--active');
      const index = activePanel ? Array.from(panels).indexOf(activePanel) : -1;

      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIndex = (index + 1) % panels.length;
        panels.forEach(function (p) {
          p.classList.remove('cat-accordion__panel--active');
        });
        panels[nextIndex].classList.add('cat-accordion__panel--active');
        panels[nextIndex].focus();
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        const prevIndex = index <= 0 ? panels.length - 1 : index - 1;
        panels.forEach(function (p) {
          p.classList.remove('cat-accordion__panel--active');
        });
        panels[prevIndex].classList.add('cat-accordion__panel--active');
        panels[prevIndex].focus();
      } else if (e.key === 'Enter' || e.key === ' ') {
        // Navigate to the category
        if (activePanel) {
          const link = activePanel.getAttribute('href');
          if (link) {
            window.location.href = link;
          }
        }
      }
    });

    // Set first panel as active on load
    if (!accordion.querySelector('.cat-accordion__panel--active') && panels.length > 0) {
      panels[0].classList.add('cat-accordion__panel--active');
    }
  }
})();
