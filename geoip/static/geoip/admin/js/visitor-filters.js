/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';
  document.addEventListener('DOMContentLoaded', function () {
    const el = document.getElementById('filter-country');
    if (el) {
      let t;
      el.addEventListener('input', function () {
        clearTimeout(t);
        t = setTimeout(function () {
          window.AdminListFilters.apply();
        }, 300);
      });
    }
  });
})();
