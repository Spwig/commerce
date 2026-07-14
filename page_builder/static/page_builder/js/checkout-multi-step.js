/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Checkout Multi-Step UI
 *
 * Extends the base Checkout object with step navigation, progress bar updates,
 * and slide animations. Loaded AFTER checkout.js.
 */
(function () {
  'use strict';

  // Wait for base Checkout to be available
  function initMultiStep() {
    const C = window.Checkout;
    if (!C) {
      console.error('Checkout base not loaded');
      return;
    }

    const config = C.config || {};
    const opts = config.templateOptions || {};
    const animation = opts.animation || 'slide';

    // === Mobile Order Summary Toggle ===

    const summaryToggle = document.getElementById('summary-toggle');
    const checkoutSummary = document.getElementById('checkout-summary');
    const summaryToggleTotal = document.getElementById('summary-toggle-total');

    if (summaryToggle && checkoutSummary) {
      // Set initial state: expanded on desktop, collapsed on mobile
      const isDesktop = window.innerWidth >= 1024;
      summaryToggle.setAttribute('aria-expanded', isDesktop ? 'true' : 'false');
      checkoutSummary.style.display = isDesktop ? 'block' : 'none';

      // Toggle functionality
      summaryToggle.addEventListener('click', function () {
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', !isExpanded);
        checkoutSummary.style.display = isExpanded ? 'none' : 'block';
      });

      // Update toggle total when cart data changes
      if (window.Checkout && window.Checkout.cartData) {
        const updateToggleTotal = () => {
          const total =
            window.Checkout.cartData.grand_total || window.Checkout.cartData.final_amount || '0.00';
          if (summaryToggleTotal) {
            summaryToggleTotal.textContent = window.Checkout.formatCurrency
              ? window.Checkout.formatCurrency(total)
              : new Intl.NumberFormat(undefined, {
                  style: 'currency',
                  currency: window.__shopCurrency || 'USD',
                  minimumFractionDigits: 2,
                }).format(parseFloat(total) || 0);
          }
        };
        // Update on initial load and when cart changes
        setTimeout(updateToggleTotal, 500);
        document.addEventListener('checkout:summary-updated', updateToggleTotal);
      }

      // Handle window resize
      let resizeTimer;
      window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
          const isDesktop = window.innerWidth >= 1024;
          if (isDesktop) {
            summaryToggle.setAttribute('aria-expanded', 'true');
            checkoutSummary.style.display = 'block';
          }
        }, 250);
      });
    }

    // === Progress Bar ===

    function updateProgressBar(activeStep) {
      const steps = C.steps;
      const activeIdx = steps.indexOf(activeStep);

      // Steps style (support both old and new class names)
      document.querySelectorAll('.progress-step, .multistep__progress-item').forEach((el, i) => {
        el.classList.remove(
          'progress-step--active',
          'progress-step--completed',
          'multistep__progress-item--active',
          'multistep__progress-item--completed'
        );
        if (i < activeIdx || C.completedSteps.has(steps[i])) {
          el.classList.add('progress-step--completed', 'multistep__progress-item--completed');
        } else if (i === activeIdx) {
          el.classList.add('progress-step--active', 'multistep__progress-item--active');
        }
      });

      // Bar style (support both old and new class names)
      const fill = document.querySelector('.progress-bar__fill, .multistep__progress-fill');
      if (fill) {
        const pct = (activeIdx / (steps.length - 1)) * 100;
        fill.style.width = pct + '%';
      }
      const barLabel = document.querySelector('.progress-bar__label, .multistep__progress-label');
      if (barLabel) {
        barLabel.textContent = `Step ${activeIdx + 1} of ${steps.length}`;
      }

      // Dots style (support both old and new class names)
      document.querySelectorAll('.progress-dot, .multistep__dot').forEach((dot, i) => {
        dot.classList.remove(
          'progress-dot--active',
          'progress-dot--completed',
          'multistep__dot--active',
          'multistep__dot--completed'
        );
        if (i < activeIdx || C.completedSteps.has(steps[i])) {
          dot.classList.add('progress-dot--completed', 'multistep__dot--completed');
        } else if (i === activeIdx) {
          dot.classList.add('progress-dot--active', 'multistep__dot--active');
        }
      });
    }

    // === Step Navigation ===

    let currentStepName = 'contact';

    function showStep(stepName, direction) {
      const steps = document.querySelectorAll('.multistep__step');
      steps.forEach(s => {
        s.classList.remove(
          'multistep__step--active',
          'multistep__step--slide-left',
          'multistep__step--fade'
        );
      });

      const target = document.querySelector(`.multistep__step[data-step="${stepName}"]`);
      if (target) {
        target.classList.add('multistep__step--active');

        // Apply animation class
        if (animation === 'slide' && direction === 'back') {
          target.classList.add('multistep__step--slide-left');
        } else if (animation === 'fade') {
          target.classList.add('multistep__step--fade');
        }

        // Scroll to checkout container 20px below page header
        const checkoutContainer = document.querySelector('.checkout-container--multistep');
        if (checkoutContainer) {
          // Get header height (try common header selectors)
          const header = document.querySelector('header, .site-header, .header, .navbar');
          const headerHeight = header ? header.offsetHeight : 0;
          const offset = headerHeight + 20; // Header height + 20px spacing

          const y = checkoutContainer.getBoundingClientRect().top + window.pageYOffset - offset;
          window.scrollTo({ top: y, behavior: 'smooth' });
        }
      }

      currentStepName = stepName;
      updateProgressBar(stepName);
    }

    // Override Checkout.openStep to use multi-step navigation
    const originalOpenStep = C.openStep.bind(C);
    C.openStep = function (stepName) {
      const oldIdx = C.steps.indexOf(currentStepName);
      const newIdx = C.steps.indexOf(stepName);
      const direction = newIdx < oldIdx ? 'back' : 'forward';
      showStep(stepName, direction);
    };

    // Back buttons (match template's data-action names: back-shipping, back-shipping-method, etc.)
    document.querySelectorAll('[data-action^="back-"]').forEach(btn => {
      btn.addEventListener('click', function () {
        const currentIdx = C.steps.indexOf(currentStepName);
        if (currentIdx > 0) {
          showStep(C.steps[currentIdx - 1], 'back');
        }
      });
    });

    // Progress step clicks (go back to completed steps)
    document.querySelectorAll('.progress-step, .multistep__progress-item').forEach((el, i) => {
      el.style.cursor = 'pointer';
      el.addEventListener('click', function () {
        const stepName = C.steps[i];
        if (C.completedSteps.has(stepName) || stepName === currentStepName) {
          showStep(stepName, i < C.steps.indexOf(currentStepName) ? 'back' : 'forward');
        }
      });
    });

    // Override step UI update (multi-step doesn't need accordion UI)
    C.updateStepUI = function () {};

    // Initial state
    showStep('contact', 'forward');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      // Small delay to ensure checkout.js init runs first
      setTimeout(initMultiStep, 10);
    });
  } else {
    setTimeout(initMultiStep, 10);
  }
})();
