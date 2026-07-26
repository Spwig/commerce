/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Category Accordion - Interactive expandable image panels.
 * Panels expand on hover (mouse) and every click/tap navigates straight
 * to the category page. Keyboard navigation moves the expanded panel.
 */
(function () {
  'use strict';

  var hoverCapable = window.matchMedia('(hover: hover) and (pointer: fine)');

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

    // Expose merchant options to the stylesheet
    accordion.style.setProperty('--accordion-expand-ratio', config.expandRatio);
    accordion.style.setProperty('--accordion-transition-speed', config.transitionSpeed + 'ms');

    function activate(panel) {
      panels.forEach(function (p) {
        p.classList.toggle('cat-accordion__panel--active', p === panel);
      });
    }

    // Hovering a panel expands it; clicks are left alone so a single
    // click (or tap on touch devices) always follows the link.
    panels.forEach(function (panel) {
      panel.addEventListener('pointerenter', function (e) {
        if (e.pointerType === 'mouse' && hoverCapable.matches) {
          activate(panel);
        }
      });
    });

    // Keyboard navigation
    accordion.addEventListener('keydown', function (e) {
      const activePanel = accordion.querySelector('.cat-accordion__panel--active');
      const index = activePanel ? Array.from(panels).indexOf(activePanel) : -1;

      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIndex = (index + 1) % panels.length;
        activate(panels[nextIndex]);
        panels[nextIndex].focus();
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        const prevIndex = index <= 0 ? panels.length - 1 : index - 1;
        activate(panels[prevIndex]);
        panels[prevIndex].focus();
      } else if (e.key === 'Enter' || e.key === ' ') {
        // Navigate to the expanded category
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
