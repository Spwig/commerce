/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  function init() {
    // Handle card selection visual feedback for any card with a radio input
    const cards = document.querySelectorAll('.page-card, .org-card');
    cards.forEach(function (card) {
      card.addEventListener('click', function () {
        // Remove selected from all sibling cards of same type
        const allCards = document.querySelectorAll('.page-card, .org-card');
        allCards.forEach(function (c) {
          c.classList.remove('selected');
        });
        // Add selected to clicked card
        card.classList.add('selected');
        // Check the radio button
        const radio = card.querySelector('input[type="radio"]');
        if (radio) {
          radio.checked = true;
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
