/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Loyalty Customer Dashboard JavaScript
 *
 * Handles interactive features for customer-facing loyalty pages
 */

(function () {
  'use strict';

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    // Apply dynamic colors from data attributes (CSP-compliant)
    applyDynamicColors();

    // Apply tier colors as CSS custom properties (CSP-compliant)
    applyTierColors();

    // Animate progress bars on load
    animateProgressBars();

    // Add smooth scroll for anchor links
    setupSmoothScroll();

    // Setup copy-to-clipboard for redemption codes
    setupCopyToClipboard();

    // Confirmation dialogs for forms with data-confirm-msg
    setupFormConfirm();
  }

  /**
   * Apply dynamic colors from data-color attributes (CSP-compliant).
   * Sets background color via JS instead of inline style="" attributes.
   */
  function applyDynamicColors() {
    const elements = document.querySelectorAll('[data-color]');
    elements.forEach(function (el) {
      const color = el.dataset.color;
      if (color) {
        el.style.backgroundColor = color;
      }
    });
  }

  /**
   * Apply tier colors as CSS custom properties (CSP-compliant).
   * Reads data-tier-color attribute and sets --tier-color CSS custom property.
   * CSS classes then reference var(--tier-color) for backgrounds, borders, text.
   */
  function applyTierColors() {
    const elements = document.querySelectorAll('[data-tier-color]');
    elements.forEach(function (el) {
      const color = el.dataset.tierColor;
      if (color) {
        el.style.setProperty('--tier-color', color);
      }
    });
  }

  /**
   * Animate progress bars with smooth transitions.
   * Reads target width from data-progress attribute.
   */
  function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');

    progressBars.forEach(function (bar) {
      const targetWidth = bar.dataset.progress;
      if (targetWidth) {
        bar.style.width = '0%';
        setTimeout(function () {
          bar.style.width = targetWidth + '%';
        }, 150);
      }
    });
  }

  /**
   * Setup smooth scrolling for anchor links
   */
  function setupSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(function (link) {
      link.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;

        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
          });
        }
      });
    });
  }

  /**
   * Setup copy-to-clipboard functionality for redemption codes
   */
  function setupCopyToClipboard() {
    const codes = document.querySelectorAll('.redemption-code code');

    codes.forEach(function (codeElement) {
      codeElement.style.cursor = 'pointer';
      codeElement.title = 'Click to copy';

      codeElement.addEventListener('click', function () {
        const text = this.textContent;

        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard
            .writeText(text)
            .then(function () {
              showCopyFeedback(codeElement);
            })
            .catch(function (err) {
              console.error('Failed to copy:', err);
            });
        } else {
          // Fallback for older browsers
          const textarea = document.createElement('textarea');
          textarea.value = text;
          textarea.style.position = 'fixed';
          textarea.style.opacity = '0';
          document.body.appendChild(textarea);
          textarea.select();

          try {
            document.execCommand('copy');
            showCopyFeedback(codeElement);
          } catch (err) {
            console.error('Fallback copy failed:', err);
          }

          document.body.removeChild(textarea);
        }
      });
    });
  }

  /**
   * Show visual feedback when code is copied
   */
  function showCopyFeedback(element) {
    const originalText = element.textContent;
    const originalTitle = element.title;

    element.textContent = '✓ Copied!';
    element.title = 'Copied to clipboard';
    element.style.color = 'var(--theme-success, #10B981)';

    setTimeout(function () {
      element.textContent = originalText;
      element.title = originalTitle;
      element.style.color = '';
    }, 2000);
  }

  /**
   * Confirmation dialogs for forms with data-confirm-msg attribute.
   * Replaces onsubmit="return confirm('...')".
   */
  function setupFormConfirm() {
    document.addEventListener('submit', async function (e) {
      const form = e.target.closest('form[data-confirm-msg]');
      if (!form) return;
      const msg = form.dataset.confirmMsg;
      if (msg) {
        e.preventDefault();
        if (await AdminModal.confirm(msg)) {
          form.submit();
        }
      }
    });
  }

  /**
   * Format numbers with thousands separator (optional enhancement)
   */
  function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  // Expose utility functions to global scope if needed
  window.LoyaltyDashboard = {
    formatNumber: formatNumber,
  };
})();
