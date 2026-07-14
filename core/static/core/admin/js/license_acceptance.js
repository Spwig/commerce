/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * License Acceptance - Scroll detection and form validation
 *
 * Ensures the merchant scrolls through the license text and
 * checks the acceptance checkbox before the submit button is enabled.
 * Fully CSP-compliant: no inline handlers, uses addEventListener.
 */

(function () {
  'use strict';

  let hasScrolledToBottom = false;

  /**
   * Check if the license text has been scrolled to the bottom.
   */
  function checkScrollPosition() {
    const licenseText = document.getElementById('license-text');
    if (!licenseText) return;

    const atBottom =
      licenseText.scrollHeight - licenseText.scrollTop <= licenseText.clientHeight + 20;

    if (atBottom && !hasScrolledToBottom) {
      hasScrolledToBottom = true;
      updateScrollHint();
      updateSubmitButton();
    }
  }

  /**
   * Hide the scroll hint once the user has scrolled to the bottom.
   */
  function updateScrollHint() {
    const hint = document.getElementById('scroll-hint');
    if (hint && hasScrolledToBottom) {
      hint.classList.add('hidden');
    }
  }

  /**
   * Enable or disable the submit button based on scroll + checkbox state.
   */
  function updateSubmitButton() {
    const submitBtn = document.getElementById('accept-btn');
    const checkbox = document.getElementById('accept-checkbox');
    if (!submitBtn || !checkbox) return;

    submitBtn.disabled = !(hasScrolledToBottom && checkbox.checked);
  }

  /**
   * Handle checkbox change.
   */
  function handleCheckboxChange() {
    updateSubmitButton();
  }

  /**
   * Initialize license acceptance page.
   */
  function init() {
    const licenseText = document.getElementById('license-text');
    const checkbox = document.getElementById('accept-checkbox');

    if (!licenseText) return;

    // Listen for scroll events on the license text container
    licenseText.addEventListener('scroll', checkScrollPosition);

    // Check if content is short enough that no scrolling is needed
    if (licenseText.scrollHeight <= licenseText.clientHeight + 20) {
      hasScrolledToBottom = true;
      updateScrollHint();
    }

    // Listen for checkbox changes
    if (checkbox) {
      checkbox.addEventListener('change', handleCheckboxChange);
    }

    // Initial state
    updateSubmitButton();
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
