/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin AttributeValue JavaScript
 * Handles color picker initialization for color_hex field
 */

(function () {
  'use strict';

  /**
   * Initialize color picker for color_hex field
   */
  function initializeColorPicker() {
    // Find the color_hex input field
    const colorInput = document.getElementById('id_color_hex');

    if (!colorInput) {
      console.log('Color hex input not found');
      return;
    }

    // Check if ColorPickerUtility is available
    if (typeof window.ColorPickerUtility === 'undefined') {
      console.error('ColorPickerUtility not loaded');
      return;
    }

    console.log('Initializing color picker for AttributeValue');

    // Create color picker instance
    const colorPicker = new window.ColorPickerUtility({
      showOpacity: false, // Hex colors only, no alpha channel
      onChange: function (color) {
        // Update the input value when color changes
        colorInput.value = color;
      },
    });

    // Get initial value from input
    const initialValue = colorInput.value || '';

    // Attach color picker to the input field
    colorPicker.attach(colorInput, initialValue);

    console.log('Color picker attached successfully');
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeColorPicker);
  } else {
    // DOM already loaded
    initializeColorPicker();
  }
})();
