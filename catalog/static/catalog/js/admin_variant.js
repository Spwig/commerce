/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Enhanced ProductVariant Inline JavaScript
 * Handles dynamic pricing strategy behavior and stock indicators
 */

(function () {
  'use strict';

  // Wait for django.jQuery to be available
  function initWhenReady() {
    if (typeof django !== 'undefined' && typeof django.jQuery !== 'undefined') {
      const $ = django.jQuery;

      $(document).ready(function () {
        initializeVariantInline();

        // Re-initialize when new inline rows are added
        $(document).on('formset:added', function (event, $row, formsetName) {
          if (formsetName === 'productvariant_set') {
            initializeVariantInline();
          }
        });
      });

      return true;
    }
    return false;
  }

  // Try immediately, or wait for DOM ready
  if (!initWhenReady()) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function retry() {
        if (!initWhenReady()) {
          // If still not ready, try again after a short delay
          setTimeout(initWhenReady, 100);
        }
      });
    } else {
      setTimeout(initWhenReady, 100);
    }
  }

  /**
   * Initialize variant inline enhancements
   */
  function initializeVariantInline() {
    if (typeof django === 'undefined' || typeof django.jQuery === 'undefined') {
      return; // jQuery not available yet
    }
    const $ = django.jQuery;

    // Handle pricing strategy changes
    handlePricingStrategyVisibility($);

    // Add stock status color coding
    addStockStatusIndicators($);
  }

  /**
   * Show/hide price field based on pricing strategy
   */
  function handlePricingStrategyVisibility($) {
    $('.inline-group').each(function () {
      const $inline = $(this);
      const $pricingStrategyField = $inline.find('[name*="pricing_strategy"]');
      const $priceField = $inline.find('[name*="-price"]').not('[name*="pricing_strategy"]');
      const $priceContainer = $priceField.closest('td, div');

      if ($pricingStrategyField.length && $priceField.length) {
        // Function to toggle price field visibility
        function togglePriceField() {
          const strategy = $pricingStrategyField.val();
          if (strategy === 'custom') {
            $priceContainer.show();
            $priceField.prop('disabled', false);
          } else {
            $priceContainer.hide();
            $priceField.prop('disabled', true);
          }
        }

        // Initial state
        togglePriceField();

        // Listen for changes
        $pricingStrategyField.on('change', togglePriceField);
      }
    });
  }

  /**
   * Add color coding to stock status indicators
   */
  function addStockStatusIndicators($) {
    $('.field-stock_summary').each(function () {
      const $field = $(this);
      const text = $field.text().toLowerCase();
      const $strong = $field.find('strong');

      if ($strong.length) {
        const totalText = $strong.text();
        const totalMatch = totalText.match(/total:\s*(\d+)/i);

        if (totalMatch) {
          const total = parseInt(totalMatch[1], 10);

          // Add appropriate class based on stock level
          if (total === 0) {
            $strong.addClass('stock-status-out');
            $strong.attr('title', 'Out of stock');
          } else if (total <= 10) {
            $strong.addClass('stock-status-low');
            $strong.attr('title', 'Low stock');
          } else {
            $strong.addClass('stock-status-ok');
            $strong.attr('title', 'In stock');
          }
        }
      }

      // Handle "No stock records" message
      if (text.includes('no stock')) {
        $field.find('em').css('color', '#999');
      }
    });
  }
})();
