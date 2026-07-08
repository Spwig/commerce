/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function() {
    'use strict';

    var configEl = document.getElementById('wizard-step1-config');
    var config = configEl ? JSON.parse(configEl.textContent) : {};

    document.addEventListener('DOMContentLoaded', function() {
        // Auto-select provider if there's only one available
        var providerRadios = document.querySelectorAll('input[name="component_id"]');

        if (providerRadios.length === 1) {
            providerRadios[0].checked = true;
            // Visually highlight the selected card
            var card = providerRadios[0].closest('.provider-card');
            if (card) {
                card.classList.add('selected');
            }

            // Show a helpful message
            var stepDescription = document.querySelector('.step-description');
            if (stepDescription) {
                var autoSelectNote = document.createElement('p');
                autoSelectNote.className = 'auto-select-note';
                var icon = document.createElement('i');
                icon.className = 'fas fa-info-circle';
                autoSelectNote.appendChild(icon);
                autoSelectNote.appendChild(document.createTextNode(' ' + (config.autoSelectMsg || '')));
                stepDescription.after(autoSelectNote);
            }
        }

        // Add visual feedback for selected provider
        providerRadios.forEach(function(radio) {
            radio.addEventListener('change', function() {
                document.querySelectorAll('.provider-card').forEach(function(c) {
                    c.classList.remove('selected');
                });
                if (this.checked) {
                    var c = this.closest('.provider-card');
                    if (c) {
                        c.classList.add('selected');
                    }
                }
            });
        });
    });
})();
