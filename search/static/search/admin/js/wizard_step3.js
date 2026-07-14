/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Search Engine Wizard Step 3 - Relevance Weights
 * Handles weight slider sync and custom weights toggle.
 */

(function () {
  'use strict';

  function init() {
    const checkbox = document.getElementById('use-custom-weights');
    if (checkbox) {
      checkbox.addEventListener('change', toggleWeightSliders);
    }

    // Sync range sliders with number inputs
    document.querySelectorAll('input[type="range"][data-target]').forEach(function (slider) {
      slider.addEventListener('input', function () {
        const target = document.getElementById(slider.dataset.target);
        if (target) target.value = slider.value;
      });
    });

    // Sync number inputs back to sliders
    document.querySelectorAll('input[type="number"][id]').forEach(function (input) {
      input.addEventListener('input', function () {
        const slider = document.getElementById(input.id + '_slider');
        if (slider) slider.value = input.value;
      });
    });
  }

  function toggleWeightSliders() {
    const checkbox = document.getElementById('use-custom-weights');
    const sliders = document.getElementById('weight-sliders');
    if (!checkbox || !sliders) return;

    if (checkbox.checked) {
      sliders.classList.remove('wizard-weights-disabled');
    } else {
      sliders.classList.add('wizard-weights-disabled');
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
