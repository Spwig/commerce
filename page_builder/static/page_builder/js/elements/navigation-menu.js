/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Navigation menu element: mobile toggle and dropdown hover/click interactions.
 * Auto-initializes all .pb-nav-menu elements on the page.
 */
(function () {
  'use strict';

  function initNavMenu(nav) {
    const toggle = nav.querySelector('.pb-nav-menu__toggle');
    const list = nav.querySelector('.pb-nav-menu__list');

    if (toggle && list) {
      toggle.addEventListener('click', function () {
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', String(!expanded));
        list.classList.toggle('pb-nav-menu__list--open');
      });
    }

    const itemsWithChildren = nav.querySelectorAll('.pb-nav-menu__item--has-children');
    itemsWithChildren.forEach(function (item) {
      const link = item.querySelector('.pb-nav-menu__link');
      const mobileBreakpoint = parseInt(nav.dataset.mobileBreakpoint || 768, 10);

      item.addEventListener('mouseenter', function () {
        if (window.innerWidth > mobileBreakpoint) {
          item.classList.add('pb-nav-menu__item--open');
        }
      });

      item.addEventListener('mouseleave', function () {
        if (window.innerWidth > mobileBreakpoint) {
          item.classList.remove('pb-nav-menu__item--open');
        }
      });

      if (link) {
        link.addEventListener('click', function (e) {
          if (window.innerWidth <= mobileBreakpoint) {
            e.preventDefault();
            item.classList.toggle('pb-nav-menu__item--open');
          }
        });
      }
    });
  }

  function init() {
    document.querySelectorAll('.pb-nav-menu').forEach(initNavMenu);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
