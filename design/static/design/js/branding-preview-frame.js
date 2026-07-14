/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';
  window.addEventListener('message', function (event) {
    if (event.data && event.data.type === 'updateCSS') {
      const styleTag = document.querySelector('style') || document.createElement('style');
      styleTag.textContent = event.data.css;
      if (!styleTag.parentNode) {
        document.head.appendChild(styleTag);
      }
    }
  });
})();
