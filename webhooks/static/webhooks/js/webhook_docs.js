/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initTabSwitching();
    initSmoothScrolling();
  });

  function initTabSwitching() {
    document.querySelectorAll('.tab-header').forEach(function (header) {
      header.addEventListener('click', function () {
        const tab = header.dataset.tab;

        // Update header states
        document.querySelectorAll('.tab-header').forEach(function (h) {
          h.classList.remove('active');
        });
        header.classList.add('active');

        // Update content states
        document.querySelectorAll('.tab-content').forEach(function (c) {
          c.classList.remove('active');
        });
        const target = document.getElementById('tab-' + tab);
        if (target) {
          target.classList.add('active');
        }
      });
    });
  }

  function initSmoothScrolling() {
    document.querySelectorAll('.docs-nav .nav-item').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }
})();
