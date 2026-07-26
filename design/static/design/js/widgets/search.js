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
    const form = widget.querySelector('.search-form');

    if (!trigger) {
      return;
    }

    // Matches the overlay breakpoint in widgets/search.css. Above it the search
    // is an inline header field and must not be relocated.
    const overlayQuery = window.matchMedia('(max-width: 767.98px)');
    let portalHandle = null;

    function openSearch() {
      widget.classList.add('is-open');

      // The overlay is position:fixed but lives inside <header>, which is a
      // stacking context and may be a containing block. Portal it to body level
      // so it covers the viewport rather than the header strip.
      if (overlayQuery.matches && window.SpwigPortal && !portalHandle) {
        // Host carries the widget's classes so `.widget-search .search-*`
        // selectors in search.css keep matching after the move.
        portalHandle = window.SpwigPortal.mount(
          [backdrop, form].filter(Boolean),
          'widget-search is-open',
          { lockScroll: true }
        );
      }

      if (input) {
        setTimeout(function () {
          input.focus();
        }, 100);
      }
    }

    function closeSearch() {
      if (portalHandle) {
        window.SpwigPortal.unmount(portalHandle);
        portalHandle = null;
      }
      widget.classList.remove('is-open');
    }

    trigger.addEventListener('click', openSearch);

    if (closeBtn) {
      closeBtn.addEventListener('click', closeSearch);
    }
    if (backdrop) {
      backdrop.addEventListener('click', closeSearch);
    }

    // Bound on document, not the widget: once portaled, the focused input is no
    // longer a descendant of `widget`, so keydown would never reach it.
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && widget.classList.contains('is-open')) {
        closeSearch();
      }
    });

    // Crossing back to desktop width while open would leave the form stranded
    // in the portal, where the inline layout rules don't apply.
    const onBreakpointChange = function () {
      if (!overlayQuery.matches && portalHandle) {
        closeSearch();
      }
    };
    if (overlayQuery.addEventListener) {
      overlayQuery.addEventListener('change', onBreakpointChange);
    } else if (overlayQuery.addListener) {
      overlayQuery.addListener(onBreakpointChange);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.widget-search').forEach(initWidget);
  });
})();
