/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Form Builder Admin JavaScript
 *
 * Handles dynamic functionality in the form builder admin interface.
 */

(function () {
  'use strict';

  // Initialize when DOM is ready
  document.addEventListener('DOMContentLoaded', function () {
    initFieldTypeHandling();
    initFormPreview();
  });

  /**
   * Handle field type changes to show/hide relevant configuration fields
   */
  function initFieldTypeHandling() {
    const fieldTypeSelects = document.querySelectorAll('select[name$="-field_type"]');

    fieldTypeSelects.forEach(function (select) {
      select.addEventListener('change', function () {
        updateFieldConfigVisibility(this);
      });

      // Initial state
      updateFieldConfigVisibility(select);
    });
  }

  /**
   * Update visibility of configuration fields based on field type
   */
  function updateFieldConfigVisibility(select) {
    const row = select.closest('tr') || select.closest('.form-row');
    if (!row) return;

    const fieldType = select.value;

    // Field types that need options
    const needsOptions = ['select', 'radio', 'checkbox_group'];

    // Field types that need rating config
    const needsRatingConfig = ['rating_stars', 'rating_likert', 'rating_nps'];

    // Field types that need file config
    const needsFileConfig = ['file'];

    // Field types that need product config
    const needsProductConfig = ['product_select'];

    // This will be expanded in later phases to show/hide
    // configuration sections in the change form
  }

  /**
   * Initialize form preview functionality
   */
  function initFormPreview() {
    const previewButton = document.querySelector('.form-preview-button');
    if (previewButton) {
      previewButton.addEventListener('click', function (e) {
        e.preventDefault();
        openFormPreview();
      });
    }
  }

  /**
   * Open form preview in a new window
   */
  function openFormPreview() {
    const formId = document.querySelector('input[name="id"]')?.value;
    if (formId) {
      const lang = document.documentElement.lang || 'en';
      const previewUrl = `/${lang}/admin/form_builder/forms/${formId}/preview/`;
      window.open(previewUrl, 'form_preview', 'width=800,height=600,scrollbars=yes');
    }
  }

  /**
   * Utility: Debounce function
   */
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
})();
