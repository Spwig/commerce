/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * GeoIP Location Widget JavaScript
 * Extracted from inline onchange handlers in geoip/location_widget.html
 * for CSP compliance.
 */

(function () {
  'use strict';

  function initLocationWidget() {
    document.querySelectorAll('.geoip-location-widget').forEach(function (widget) {
      const currencySelector = widget.querySelector('.currency-selector');
      const languageSelector = widget.querySelector('.language-selector');

      if (currencySelector) {
        currencySelector.addEventListener('change', function () {
          if (window.GeoIP && typeof window.GeoIP.setPreference === 'function') {
            window.GeoIP.setPreference('currency', this.value);
          }
        });
      }

      if (languageSelector) {
        languageSelector.addEventListener('change', function () {
          if (window.GeoIP && typeof window.GeoIP.setPreference === 'function') {
            window.GeoIP.setPreference('language', this.value);
          }
        });
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLocationWidget);
  } else {
    initLocationWidget();
  }
})();
