/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  function init() {
    applyProviderColors();
  }

  function applyProviderColors() {
    document.querySelectorAll('.provider-icon[data-color]').forEach(function (el) {
      const color = el.dataset.color;
      if (color) {
        el.style.backgroundColor = color + '20';
        el.style.color = color;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
