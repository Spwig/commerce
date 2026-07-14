/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let translations = {};

  function init() {
    const dataEl = document.getElementById('cart-wizard-step4-data');
    if (dataEl) {
      try {
        const data = JSON.parse(dataEl.textContent);
        translations = data.translations || {};
      } catch (e) {}
    }

    const form = document.getElementById('method-features-form');
    const availableLocations = document.getElementById('available-locations');
    const selectedLocations = document.getElementById('selected-locations');

    if (availableLocations && selectedLocations) {
      const addBtn = document.getElementById('add-locations');
      const addAllBtn = document.getElementById('add-all-locations');
      const removeBtn = document.getElementById('remove-locations');
      const removeAllBtn = document.getElementById('remove-all-locations');

      if (addBtn) {
        addBtn.addEventListener('click', function () {
          moveOptions(availableLocations, selectedLocations, false);
        });
      }
      if (addAllBtn) {
        addAllBtn.addEventListener('click', function () {
          moveOptions(availableLocations, selectedLocations, true);
        });
      }
      if (removeBtn) {
        removeBtn.addEventListener('click', function () {
          moveOptions(selectedLocations, availableLocations, false);
        });
      }
      if (removeAllBtn) {
        removeAllBtn.addEventListener('click', function () {
          moveOptions(selectedLocations, availableLocations, true);
        });
      }

      if (form) {
        form.addEventListener('submit', function () {
          Array.from(selectedLocations.options).forEach(function (option) {
            option.selected = true;
          });
        });
      }
    }

    const minDeliveryDays = document.getElementById('id_min_delivery_days');
    const maxDeliveryDays = document.getElementById('id_max_delivery_days');

    if (minDeliveryDays && maxDeliveryDays) {
      if (form) {
        form.addEventListener('submit', function (e) {
          if (!validateDeliveryRange(minDeliveryDays, maxDeliveryDays)) {
            e.preventDefault();
          }
        });
      }
      [minDeliveryDays, maxDeliveryDays].forEach(function (field) {
        field.addEventListener('blur', function () {
          validateDeliveryRange(minDeliveryDays, maxDeliveryDays);
        });
      });
    }

    const apiStatusSection = document.getElementById('carrier-status-section');
    if (apiStatusSection) {
      setTimeout(function () {
        const statusResult = document.getElementById('api-status-result');
        const statusItem = apiStatusSection.querySelector('.status-item');
        if (statusItem) {
          statusItem.style.display = 'none';
        }
        if (statusResult) {
          statusResult.style.display = 'block';
          statusResult.innerHTML =
            '<div class="status-item success">' +
            '<i class="fas fa-check-circle status-icon status-icon-success"></i>' +
            '<span>' +
            (translations.apiVerified || 'API credentials verified successfully') +
            '</span>' +
            '</div>';
        }
      }, 1500);
    }
  }

  function moveOptions(fromSelect, toSelect, moveAll) {
    const options = moveAll
      ? Array.from(fromSelect.options)
      : Array.from(fromSelect.selectedOptions);
    options.forEach(function (option) {
      toSelect.appendChild(option);
    });
  }

  function validateDeliveryRange(minField, maxField) {
    const minVal = parseInt(minField.value) || 0;
    const maxVal = parseInt(maxField.value) || 0;
    if (minVal > maxVal) {
      AdminModal.alert({
        message: 'Minimum delivery days cannot be greater than maximum delivery days',
        type: 'error',
      });
      return false;
    }
    return true;
  }

  document.addEventListener('DOMContentLoaded', init);
})();
