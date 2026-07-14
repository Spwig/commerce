/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Product admin page initializer — runs before admin_product_form.js.
 * Reads window.PRODUCT_ADMIN_CONFIG from the JSON data island
 * and zeros AJAX-managed formset management forms.
 */
(function () {
  'use strict';

  // ----------------------------------------------------------------
  // 1. Read PRODUCT_ADMIN_CONFIG from JSON data island
  // ----------------------------------------------------------------
  const dataEl = document.getElementById('product-admin-config');
  if (dataEl) {
    try {
      window.PRODUCT_ADMIN_CONFIG = JSON.parse(dataEl.textContent);
    } catch (e) {
      window.PRODUCT_ADMIN_CONFIG = {};
    }
  } else {
    window.PRODUCT_ADMIN_CONFIG = {};
  }

  // ----------------------------------------------------------------
  // 2. Zero AJAX-managed formset management forms on DOMContentLoaded
  // ----------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-zero-formset]').forEach(function (el) {
      const prefix = el.dataset.zeroFormset;
      const tf = document.querySelector('input[name="' + prefix + '-TOTAL_FORMS"]');
      const inf = document.querySelector('input[name="' + prefix + '-INITIAL_FORMS"]');
      if (tf) {
        tf.value = '0';
      }
      if (inf) {
        inf.value = '0';
      }
    });

    // Formset sanity check (development aid)
    const prefixes = [];
    document.querySelectorAll('.js-inline-admin-formset').forEach(function (formset) {
      const id = formset.id;
      if (id && id.endsWith('-group')) {
        prefixes.push(id.replace('-group', ''));
      }
    });
    prefixes.forEach(function (prefix) {
      const totalForms = document.querySelector('input[name="' + prefix + '-TOTAL_FORMS"]');
      const initialForms = document.querySelector('input[name="' + prefix + '-INITIAL_FORMS"]');
      if (!totalForms || !initialForms) {
        console.error('[Formset Check] MISSING management form fields for ' + prefix);
      } else {
        console.log(
          '[Formset Check] OK ' +
            prefix +
            ' (TOTAL=' +
            totalForms.value +
            ', INITIAL=' +
            initialForms.value +
            ')'
        );
      }
    });
  });
})();
