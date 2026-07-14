/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Gift card promo element: denomination selection.
 * Auto-initializes all .gift-card-promo sections on the page.
 */
(function () {
  'use strict';

  function initGiftCardPromo(section) {
    const denomBtns = section.querySelectorAll(
      '.gift-card-promo__denom-btn, .gift-card-promo__denom-card'
    );
    denomBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        denomBtns.forEach(function (b) {
          b.classList.remove(
            'gift-card-promo__denom-btn--selected',
            'gift-card-promo__denom-card--selected'
          );
        });
        btn.classList.add(
          btn.classList.contains('gift-card-promo__denom-btn')
            ? 'gift-card-promo__denom-btn--selected'
            : 'gift-card-promo__denom-card--selected'
        );
      });
    });
  }

  function init() {
    document.querySelectorAll('.gift-card-promo').forEach(initGiftCardPromo);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
