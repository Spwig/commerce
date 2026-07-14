/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  if (window._widgetSearchInit) {
    return;
  }
  window._widgetSearchInit = true;

  function initWidget(widget) {
    if (widget.dataset.searchInitialized) {
      return;
    }
    widget.dataset.searchInitialized = 'true';

    const trigger = widget.querySelector('.search-mobile-trigger');
    const closeBtn = widget.querySelector('.search-mobile-close');
    const backdrop = widget.querySelector('.search-mobile-backdrop');
    const input = widget.querySelector('.search-input');

    if (!trigger) {
      return;
    }

    function openSearch() {
      widget.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      if (input) {
        setTimeout(function () {
          input.focus();
        }, 100);
      }
    }

    function closeSearch() {
      widget.classList.remove('is-open');
      document.body.style.overflow = '';
    }

    trigger.addEventListener('click', openSearch);

    if (closeBtn) {
      closeBtn.addEventListener('click', closeSearch);
    }
    if (backdrop) {
      backdrop.addEventListener('click', closeSearch);
    }

    widget.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && widget.classList.contains('is-open')) {
        closeSearch();
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.widget-search').forEach(initWidget);
  });
})();
