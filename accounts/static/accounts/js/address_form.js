/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const radios = document.querySelectorAll('input[name="address_type"]');

    radios.forEach(function (radio) {
      radio.addEventListener('change', function () {
        radios.forEach(function (r) {
          r.closest('label').classList.remove('border-blue-500', 'bg-blue-50');
        });
        this.closest('label').classList.add('border-blue-500', 'bg-blue-50');
      });

      if (radio.checked) {
        radio.closest('label').classList.add('border-blue-500', 'bg-blue-50');
      }
    });
  });
})();
