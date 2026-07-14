/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * License Key Template Admin JavaScript
 * Interactive features for the license key template admin interface
 */

(function ($) {
  'use strict';

  $(document).ready(function () {
    // Live preview functionality
    function updateLivePreview() {
      const pattern = $('#id_pattern').val();
      const prefix = $('#id_prefix').val();
      const suffix = $('#id_suffix').val();

      if (!pattern) return;

      // Simple client-side preview (actual generation happens server-side)
      let previewText = pattern;
      if (prefix) {
        previewText = previewText.replace(/{PREFIX}/g, '<strong>' + prefix + '</strong>');
      }
      if (suffix) {
        previewText = previewText.replace(/{SUFFIX}/g, '<strong>' + suffix + '</strong>');
      }

      // Highlight placeholders
      previewText = previewText.replace(
        /\{([A-Z_:]+)\}/g,
        '<span style="color: #0066cc; font-weight: bold;">{$1}</span>'
      );

      // Update preview if it exists
      const $preview = $('.license-template-preview code');
      if ($preview.length) {
        $preview.html(previewText);
      }
    }

    // Attach live preview to pattern field changes
    $('#id_pattern, #id_prefix, #id_suffix').on('input', function () {
      updateLivePreview();
    });

    // Initialize preview on page load
    updateLivePreview();

    // Character set helper
    $('#id_character_set').on('blur', function () {
      const charset = $(this).val();
      const unique = [...new Set(charset)].join('');
      if (charset !== unique) {
        $(this).val(unique);
        AdminModal.alert('Duplicate characters were removed from the character set.');
      }
    });

    // Pattern validation helper
    $('#id_pattern').on('blur', function () {
      const pattern = $(this).val();
      const validPlaceholders = [
        'RANDOM',
        'CHECKSUM',
        'PREFIX',
        'SUFFIX',
        'ORDER_ID',
        'PRODUCT_SKU',
        'DATE',
      ];
      const placeholders = pattern.match(/\{([A-Z_]+)(?::\w+)?\}/g) || [];

      const invalid = [];
      placeholders.forEach(function (placeholder) {
        const name = placeholder.replace(/[{}:].*/g, '');
        if (!validPlaceholders.includes(name)) {
          invalid.push(placeholder);
        }
      });

      if (invalid.length > 0) {
        AdminModal.alert({
          message:
            'Warning: Invalid placeholders detected: ' +
            invalid.join(', ') +
            '\n\nValid placeholders are: ' +
            validPlaceholders.join(', '),
          type: 'warning',
        });
      }
    });
  });
})(django.jQuery);
