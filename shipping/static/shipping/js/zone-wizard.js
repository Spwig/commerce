/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Zone Wizard - Interactive Controls
 * Handles country chip selection, validation, and form assistance
 */

(function () {
  'use strict';

  // =========================================================================
  // Initialization
  // =========================================================================

  function init() {
    console.log('🌐 Initializing Zone Wizard...');

    setupCountryChips();
    setupJSONValidation();
    setupFormValidation();

    console.log('✅ Zone Wizard initialized');
  }

  // =========================================================================
  // Country Chip Selection (Step 2)
  // =========================================================================

  function setupCountryChips() {
    const countryInput = document.getElementById('id_countries');
    const chipButtons = document.querySelectorAll('.chip-btn');

    if (!countryInput || chipButtons.length === 0) return;

    chipButtons.forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        const code = btn.dataset.code;
        const name = btn.dataset.name;

        // Get current value
        const currentValue = countryInput.value.trim();
        const countries = currentValue
          ? currentValue.split(',').map(c => c.trim().toUpperCase())
          : [];

        // Check if already added
        if (countries.includes(code)) {
          showNotification('info', `${name} (${code}) is already added`);
          return;
        }

        // Add country
        countries.push(code);
        countryInput.value = countries.join(', ');

        // Visual feedback
        btn.style.animation = 'pulse 0.3s ease';
        setTimeout(() => {
          btn.style.animation = '';
        }, 300);

        showNotification('success', `Added ${name} (${code})`);
      });
    });
  }

  // =========================================================================
  // JSON Validation (Step 2 - States)
  // =========================================================================

  function setupJSONValidation() {
    const statesInput = document.getElementById('id_states');

    if (!statesInput) return;

    statesInput.addEventListener('blur', () => {
      const value = statesInput.value.trim();

      if (!value) return; // Empty is valid

      try {
        const parsed = JSON.parse(value);

        // Validate structure
        if (typeof parsed !== 'object' || Array.isArray(parsed)) {
          throw new Error('States must be a JSON object');
        }

        // Validate each country has array of states
        for (const [country, states] of Object.entries(parsed)) {
          if (!Array.isArray(states)) {
            throw new Error(`States for ${country} must be an array`);
          }
        }

        // Pretty print the JSON
        statesInput.value = JSON.stringify(parsed, null, 2);

        // Remove error styling
        statesInput.style.borderColor = '';
      } catch (error) {
        statesInput.style.borderColor = 'var(--error-fg)';
        showNotification('error', `Invalid JSON: ${error.message}`);
      }
    });
  }

  // =========================================================================
  // Form Validation
  // =========================================================================

  function setupFormValidation() {
    // Step 1 - Basic Information
    const basicForm = document.getElementById('zone-basic-form');
    if (basicForm) {
      basicForm.addEventListener('submit', e => {
        const name = document.getElementById('id_name').value.trim();

        if (!name) {
          e.preventDefault();
          showNotification('error', 'Zone name is required');
          document.getElementById('id_name').focus();
          return false;
        }
      });
    }

    // Step 2 - Coverage
    const coverageForm = document.getElementById('zone-coverage-form');
    if (coverageForm) {
      coverageForm.addEventListener('submit', e => {
        const statesInput = document.getElementById('id_states');
        const statesValue = statesInput.value.trim();

        // Validate JSON if provided
        if (statesValue) {
          try {
            const parsed = JSON.parse(statesValue);

            if (typeof parsed !== 'object' || Array.isArray(parsed)) {
              e.preventDefault();
              showNotification('error', 'States must be a valid JSON object');
              statesInput.focus();
              return false;
            }
          } catch (error) {
            e.preventDefault();
            showNotification('error', `Invalid JSON in states field: ${error.message}`);
            statesInput.focus();
            return false;
          }
        }
      });
    }

    // Step 3 - Review (No validation needed, just confirmation)
    const createForm = document.getElementById('zone-create-form');
    if (createForm) {
      createForm.addEventListener('submit', e => {
        // Optional: Add confirmation dialog
        // if (!confirm('Create this shipping zone?')) {
        //     e.preventDefault();
        //     return false;
        // }
      });
    }
  }

  // =========================================================================
  // Notification Helper
  // =========================================================================

  function showNotification(type, message) {
    AdminModal.toast(message, type || 'info');
  }

  // =========================================================================
  // Animations
  // =========================================================================

  // Add CSS animations dynamically
  const style = document.createElement('style');
  style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }

        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }
    `;
  document.head.appendChild(style);

  // =========================================================================
  // Initialize on DOM Ready
  // =========================================================================

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
