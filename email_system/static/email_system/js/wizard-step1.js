/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  const configEl = document.getElementById('wizard-step1-config');
  const config = configEl ? JSON.parse(configEl.textContent) : {};

  document.addEventListener('DOMContentLoaded', function () {
    // Auto-select provider if there's only one available
    const providerRadios = document.querySelectorAll('input[name="component_id"]');

    if (providerRadios.length === 1) {
      providerRadios[0].checked = true;
      // Visually highlight the selected card
      const card = providerRadios[0].closest('.provider-card');
      if (card) {
        card.classList.add('selected');
      }

      // Show a helpful message
      const stepDescription = document.querySelector('.step-description');
      if (stepDescription) {
        const autoSelectNote = document.createElement('p');
        autoSelectNote.className = 'auto-select-note';
        const icon = document.createElement('i');
        icon.className = 'fas fa-info-circle';
        autoSelectNote.appendChild(icon);
        autoSelectNote.appendChild(document.createTextNode(' ' + (config.autoSelectMsg || '')));
        stepDescription.after(autoSelectNote);
      }
    }

    // Add visual feedback for selected provider
    providerRadios.forEach(function (radio) {
      radio.addEventListener('change', function () {
        document.querySelectorAll('.provider-card').forEach(function (c) {
          c.classList.remove('selected');
        });
        if (this.checked) {
          const c = this.closest('.provider-card');
          if (c) {
            c.classList.add('selected');
          }
        }
      });
    });
  });
})();
