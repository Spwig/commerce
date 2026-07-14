/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* Gallery-focus: clicking a grid item updates the hero/main image */
(function () {
  'use strict';

  const mainImage = document.getElementById('main-image');
  const gridItems = document.querySelectorAll('.gallery-focus__item');

  gridItems.forEach(function (item) {
    item.addEventListener('click', function () {
      if (!mainImage) return;
      const img = this.querySelector('.gallery-focus__image');
      if (!img) return;

      // Update hero image to show the clicked grid image
      mainImage.src = img.src;
      mainImage.dataset.zoomSrc = img.dataset.zoomSrc || img.src;

      // Scroll hero into view smoothly
      const hero = document.querySelector('.product-gallery__zoom-container');
      if (hero) {
        hero.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      // Update active states
      gridItems.forEach(function (gi) {
        gi.classList.remove('gallery-focus__item--active');
      });
      this.classList.add('gallery-focus__item--active');
    });
  });
})();
