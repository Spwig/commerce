/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Checkout Single Page UI
 *
 * All checkout sections visible at once. Overrides the step-based navigation
 * with section-based validation and progressive disclosure.
 * Loaded AFTER checkout.js.
 */
(function () {
  'use strict';

  function initSinglePage() {
    const C = window.Checkout;
    if (!C) {
      console.error('Checkout base not loaded');
      return;
    }

    // Override openStep - single page doesn't navigate, just enables/disables sections
    C.openStep = function (stepName) {
      // Enable all sections up to and including this step
      const idx = C.steps.indexOf(stepName);
      C.steps.forEach((name, i) => {
        const section = document.querySelector(`.single-page__section[data-step="${name}"]`);
        if (!section) return;

        if (i <= idx || C.completedSteps.has(name)) {
          section.classList.remove('single-page__section--disabled');
        } else {
          section.classList.add('single-page__section--disabled');
        }
      });

      // Scroll to the section
      const targetSection = document.querySelector(
        `.single-page__section[data-step="${stepName}"]`
      );
      if (targetSection) {
        targetSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    };

    // Override updateStepUI - single page uses section-level styling
    C.updateStepUI = function (stepName, state) {
      const section = document.querySelector(`.single-page__section[data-step="${stepName}"]`);
      if (!section) return;

      section.classList.remove('single-page__section--disabled');
      if (state === 'disabled') {
        section.classList.add('single-page__section--disabled');
      }

      // Update section number badge to checkmark
      const number = section.querySelector('.single-page__section-number');
      if (number && state === 'completed') {
        number.innerHTML = '<i class="fas fa-check" style="font-size: 0.625rem;"></i>';
        number.style.background = 'var(--theme-color-success, #059669)';
      }
    };

    // Auto-submit contact on blur if valid
    const emailInput = document.getElementById('checkout-email');
    if (emailInput) {
      emailInput.addEventListener('blur', function () {
        const email = this.value.trim();
        if (email && C.isValidEmail(email) && !C.completedSteps.has('contact')) {
          C.completedSteps.add('contact');
          C.updateSummaryText('contact', email);
          C.updateStepUI('contact', 'completed');
          C.openStep('shipping');
        }
      });
    }

    // Initial section states - enable contact, disable the rest
    C.steps.forEach((name, i) => {
      const section = document.querySelector(`.single-page__section[data-step="${name}"]`);
      if (!section) return;
      if (i > 0 && !C.completedSteps.has(name)) {
        section.classList.add('single-page__section--disabled');
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(initSinglePage, 10);
    });
  } else {
    setTimeout(initSinglePage, 10);
  }
})();
