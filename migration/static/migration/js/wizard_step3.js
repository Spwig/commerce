/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let translations = {};
  let progressInterval = null;

  function init() {
    const tEl = document.getElementById('step3-data');
    if (tEl) {
      try {
        const data = JSON.parse(tEl.textContent);
        translations = data.translations || {};
      } catch (e) {}
    }

    const form = document.getElementById('preview-form');
    if (form) {
      form.addEventListener('submit', handleSubmit);
    }

    window.addEventListener('beforeunload', function () {
      if (progressInterval) {
        clearInterval(progressInterval);
      }
    });
  }

  function handleSubmit(e) {
    const checkboxes = document.querySelectorAll('input[name^="import_"]:checked');
    if (checkboxes.length === 0) {
      e.preventDefault();
      AdminModal.alert({
        message: translations.selectAtLeastOne || 'Please select at least one data type to import.',
        type: 'warning',
      });
      return;
    }

    const submitButton = document.getElementById('submit-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> ' + (translations.processing || 'Processing...');
    }
    if (loadingIndicator) {
      loadingIndicator.style.display = 'block';
    }

    let progress = 0;
    progressInterval = setInterval(function () {
      progress += Math.random() * 15;
      if (progress > 90) {
        progress = 90;
      }

      if (progressBar) {
        progressBar.style.width = progress + '%';
      }

      if (progressText) {
        if (progress < 30) {
          progressText.textContent = translations.fetchingSampleData || 'Fetching sample data...';
        } else if (progress < 60) {
          progressText.textContent =
            translations.detectingCustomFields || 'Detecting custom fields...';
        } else {
          progressText.textContent = translations.creatingMappings || 'Creating field mappings...';
        }
      }
    }, 300);
  }

  document.addEventListener('DOMContentLoaded', init);
})();
