/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Search Results Page
 *
 * Auto-submits the filter form when filter controls change.
 */

(function () {
  'use strict';

  function initSearchFilters() {
    const form = document.getElementById('search-filters-form');
    if (!form) return;

    form
      .querySelectorAll('input[type="radio"], input[type="checkbox"], select')
      .forEach(function (input) {
        input.addEventListener('change', function () {
          form.submit();
        });
      });
  }

  document.addEventListener('DOMContentLoaded', initSearchFilters);
})();
