/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Preview Market Switcher
 * Re-renders the preview iframe as a visitor in a chosen market by setting the
 * `preview_market` query param on the preview URL (staff-only preview view).
 */
(function () {
  'use strict';

  const MarketSwitcher = {
    init() {
      document.addEventListener('click', e => {
        const toggleBtn = e.target.closest('[data-action="toggle-market-dropdown"]');
        if (toggleBtn) {
          e.preventDefault();
          this.toggleDropdown();
          return;
        }

        const switchBtn = e.target.closest('[data-action="switch-preview-market"]');
        if (switchBtn) {
          e.preventDefault();
          this.switchMarket(switchBtn);
          return;
        }

        const switcher = document.querySelector('#preview-market-switcher');
        if (switcher && !switcher.contains(e.target)) {
          this.closeDropdown();
        }
      });

      document.addEventListener('keydown', e => {
        if (e.key === 'Escape') {
          this.closeDropdown();
        }
      });
    },

    toggleDropdown() {
      const switcher = document.querySelector('#preview-market-switcher');
      if (!switcher) return;
      switcher.classList.toggle('open');
      const toggle = switcher.querySelector('[aria-expanded]');
      if (toggle) {
        toggle.setAttribute(
          'aria-expanded',
          switcher.classList.contains('open') ? 'true' : 'false'
        );
      }
    },

    closeDropdown() {
      const switcher = document.querySelector('#preview-market-switcher');
      if (switcher && switcher.classList.contains('open')) {
        switcher.classList.remove('open');
        const toggle = switcher.querySelector('[aria-expanded]');
        if (toggle) {
          toggle.setAttribute('aria-expanded', 'false');
        }
      }
    },

    switchMarket(btn) {
      const slug = btn.dataset.market || '';
      const iframe = document.getElementById('preview');
      if (!iframe) return;

      const urlObj = new URL(iframe.src, window.location.origin);
      if (slug) {
        urlObj.searchParams.set('preview_market', slug);
      } else {
        urlObj.searchParams.delete('preview_market');
      }

      const loading = document.querySelector('.loading-indicator');
      if (loading) {
        loading.classList.add('active');
      }
      iframe.src = urlObj.toString();

      // Update the toggle label + active state.
      const label = document.querySelector('#preview-market-switcher .current-market-code');
      if (label) {
        label.textContent = slug ? slug.toUpperCase() : 'Default';
      }
      document.querySelectorAll('#preview-market-switcher .language-option').forEach(option => {
        const isActive = (option.dataset.market || '') === slug;
        option.classList.toggle('active', isActive);
        let checkmark = option.querySelector('.checkmark');
        if (isActive && !checkmark) {
          checkmark = document.createElement('span');
          checkmark.className = 'checkmark';
          checkmark.textContent = '✓';
          option.appendChild(checkmark);
        } else if (!isActive && checkmark) {
          checkmark.remove();
        }
      });

      this.closeDropdown();
    },
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => MarketSwitcher.init());
  } else {
    MarketSwitcher.init();
  }

  window.PreviewMarketSwitcher = MarketSwitcher;
})();
