/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Social connector wizard: card selection for page/organization steps.
 * Auto-initializes any element with [data-card-selector-class] attribute.
 * The value of that attribute is the CSS class of the selectable cards.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const containers = document.querySelectorAll('[data-card-selector-class]');
    containers.forEach(function (container) {
      const cardClass = container.dataset.cardSelectorClass;
      const cards = container.querySelectorAll('.' + cardClass);
      cards.forEach(function (card) {
        card.addEventListener('click', function () {
          cards.forEach(function (c) {
            c.classList.remove('selected');
          });
          this.classList.add('selected');
          const radio = this.querySelector('input[type="radio"]');
          if (radio) {
            radio.checked = true;
          }
        });
      });
    });
  });
})();
