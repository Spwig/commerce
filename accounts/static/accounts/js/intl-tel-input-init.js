/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * International Telephone Input Initialization
 * Integrates intl-tel-input library with GeoIP auto-detection
 */

(function () {
  'use strict';

  function initPhoneInputs() {
    // Get country from GeoIP (set by backend via meta tag)
    const geoCountry = document.querySelector('meta[name="geo-country"]')?.content || 'US';

    // Initialize all phone inputs
    const phoneInputs = document.querySelectorAll('input[type="tel"]');

    phoneInputs.forEach(input => {
      const iti = window.intlTelInput(input, {
        initialCountry: geoCountry,
        preferredCountries: ['us', 'gb', 'ca', 'au'],
        utilsScript:
          document.querySelector('meta[name="intl-tel-utils-url"]')?.content ||
          '/static/core/vendor/intl-tel-input/js/utils.js',
        nationalMode: false, // Show country code
        formatOnDisplay: true,
        separateDialCode: true,
        autoPlaceholder: 'aggressive',
        customPlaceholder: function (selectedCountryPlaceholder) {
          return selectedCountryPlaceholder;
        },
      });

      // Store instance on element for validation
      input.intlTelInputInstance = iti;

      // Validation on blur
      input.addEventListener('blur', function () {
        if (input.value.trim()) {
          if (iti.isValidNumber()) {
            input.classList.remove('error');
            input.classList.add('valid');
            // Store E.164 format in hidden field if it exists
            const hiddenField = document.getElementById(input.id + '_e164');
            if (hiddenField) {
              hiddenField.value = iti.getNumber();
            }
          } else {
            input.classList.add('error');
            input.classList.remove('valid');
          }
        }
      });

      // Clear validation state on input
      input.addEventListener('input', function () {
        input.classList.remove('error', 'valid');
      });
    });
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPhoneInputs);
  } else {
    initPhoneInputs();
  }
})();
