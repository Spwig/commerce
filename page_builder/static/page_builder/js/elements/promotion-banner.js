/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Promotion banner element: dismiss persistence and countdown timer.
 * Auto-initializes all .promo-banner elements on the page.
 */
(function () {
  'use strict';

  function initPromoBanner(banner) {
    const elementId = banner.dataset.elementId;
    const dismissKey = 'promo_dismissed_' + elementId;

    // Check if dismissed
    if (banner.dataset.dismissible === 'true' && localStorage.getItem(dismissKey)) {
      banner.dataset.dismissed = 'true';
      return;
    }

    // Close button
    const closeBtn = banner.querySelector('.promo-banner__close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        banner.dataset.dismissed = 'true';
        localStorage.setItem(dismissKey, 'true');
      });
    }

    // Countdown
    const countdown = banner.querySelector('.promo-banner__countdown');
    if (countdown && countdown.dataset.ends) {
      const endDate = new Date(countdown.dataset.ends).getTime();
      const daysEl = countdown.querySelector('[data-days]');
      const hoursEl = countdown.querySelector('[data-hours]');
      const minsEl = countdown.querySelector('[data-mins]');
      const secsEl = countdown.querySelector('[data-secs]');

      function update() {
        const now = Date.now();
        const diff = endDate - now;

        if (diff <= 0) {
          if (banner.dataset.autoHide === 'true') {
            banner.dataset.dismissed = 'true';
          }
          return;
        }

        const d = Math.floor(diff / (1000 * 60 * 60 * 24));
        const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const s = Math.floor((diff % (1000 * 60)) / 1000);

        if (daysEl) daysEl.textContent = String(d).padStart(2, '0');
        if (hoursEl) hoursEl.textContent = String(h).padStart(2, '0');
        if (minsEl) minsEl.textContent = String(m).padStart(2, '0');
        if (secsEl) secsEl.textContent = String(s).padStart(2, '0');
      }

      update();
      setInterval(update, 1000);
    }
  }

  function init() {
    document.querySelectorAll('.promo-banner').forEach(initPromoBanner);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
