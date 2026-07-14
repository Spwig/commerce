/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Collection Change Form JavaScript
 * Handles save buttons and conditional visibility.
 * Tab switching is handled by the global AdminTabs utility (admin-tabs.js).
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initSaveButtons();
    initConditionalVisibility();
  });

  /* =============================================
       SAVE BUTTONS
       ============================================= */

  function initSaveButtons() {
    const form = document.getElementById('collection_form');
    if (!form) return;

    const saveContinueBtn = document.getElementById('collection-save-continue-btn');
    if (saveContinueBtn) {
      saveContinueBtn.addEventListener('click', function () {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = '_continue';
        input.value = '1';
        form.appendChild(input);
        form.submit();
      });
    }

    const saveBtn = document.getElementById('collection-save-btn');
    if (saveBtn) {
      saveBtn.addEventListener('click', function () {
        form.submit();
      });
    }
  }

  /* =============================================
       CONDITIONAL VISIBILITY
       ============================================= */

  function initConditionalVisibility() {
    const typeSelect = document.getElementById('id_collection_type');
    if (!typeSelect) return;

    typeSelect.addEventListener('change', function () {
      updateVisibility(this.value);
    });

    updateVisibility(typeSelect.value);
  }

  function updateVisibility(collectionType) {
    const autoCriteria = document.getElementById('auto-criteria-section');
    const manualInfo = document.getElementById('products-info-manual');
    const autoInfo = document.getElementById('products-info-auto');

    if (autoCriteria) {
      autoCriteria.classList.toggle('hidden', collectionType !== 'auto');
    }
    if (manualInfo) {
      manualInfo.classList.toggle('hidden', collectionType === 'auto');
    }
    if (autoInfo) {
      autoInfo.classList.toggle('hidden', collectionType !== 'auto');
    }
  }
})();
