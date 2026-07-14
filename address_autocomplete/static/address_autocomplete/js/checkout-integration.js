/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  const configEl = document.getElementById('address-autocomplete-config');
  if (!configEl) return;
  const config = JSON.parse(configEl.textContent);
  const shippingPrefix = config.shippingPrefix;
  const billingPrefix = config.billingPrefix;
  const separateBilling = config.separateBilling;

  function buildFieldMapping(prefix) {
    return {
      address1: '#id_' + prefix + 'address1',
      address2: '#id_' + prefix + 'address2',
      city: '#id_' + prefix + 'city',
      state: '#id_' + prefix + 'state',
      postal_code: '#id_' + prefix + 'postal_code',
      country: '#id_' + prefix + 'country',
      latitude: '#' + prefix + 'latitude',
      longitude: '#' + prefix + 'longitude',
    };
  }

  function showValidationErrors(errors, prefix) {
    const input = document.querySelector('#' + prefix + 'search');
    if (!input) return;
    const container = input.parentElement;
    let errorDiv = container.querySelector('.address-validation-errors');
    if (!errorDiv) {
      errorDiv = document.createElement('div');
      errorDiv.className = 'address-validation-errors alert alert-warning mt-2';
      container.appendChild(errorDiv);
    }
    const strong = document.createElement('strong');
    strong.textContent = 'Address validation:';
    errorDiv.innerHTML = '';
    errorDiv.appendChild(strong);
    const ul = document.createElement('ul');
    errors.forEach(function (err) {
      const li = document.createElement('li');
      li.textContent = err;
      ul.appendChild(li);
    });
    errorDiv.appendChild(ul);
  }

  function clearValidationErrors(prefix) {
    const input = document.querySelector('#' + prefix + 'search');
    if (!input) return;
    const container = input.parentElement;
    const errorDiv = container.querySelector('.address-validation-errors');
    if (errorDiv) {
      errorDiv.remove();
    }
  }

  function validateAddress(components, prefix) {
    const params = new URLSearchParams(components);
    fetch('/api/address/validate?' + params.toString())
      .then(function (response) {
        return response.json();
      })
      .then(function (result) {
        if (!result.valid && result.errors && result.errors.length > 0) {
          showValidationErrors(result.errors, prefix);
        } else {
          clearValidationErrors(prefix);
        }
      })
      .catch(function (error) {
        console.error('Validation error:', error);
      });
  }

  function copyAddressFields(fromPrefix, toPrefix) {
    const fields = ['address1', 'address2', 'city', 'state', 'postal_code', 'country'];
    fields.forEach(function (field) {
      const fromField = document.getElementById('id_' + fromPrefix + field);
      const toField = document.getElementById('id_' + toPrefix + field);
      if (fromField && toField) {
        toField.value = fromField.value;
      }
    });
    ['latitude', 'longitude', 'normalized'].forEach(function (field) {
      const fromField = document.getElementById(fromPrefix + field);
      const toField = document.getElementById(toPrefix + field);
      if (fromField && toField) {
        toField.value = fromField.value;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (typeof AddressAutocomplete === 'undefined') return;

    new AddressAutocomplete('#' + shippingPrefix + 'search', {
      apiUrl: '/api/address/autocomplete',
      fieldMapping: buildFieldMapping(shippingPrefix),
      onSelect: function (suggestion) {
        const el = document.getElementById(shippingPrefix + 'normalized');
        if (el) el.value = JSON.stringify(suggestion);
        validateAddress(suggestion.components, shippingPrefix);
      },
    });

    if (separateBilling && billingPrefix) {
      new AddressAutocomplete('#' + billingPrefix + 'search', {
        apiUrl: '/api/address/autocomplete',
        fieldMapping: buildFieldMapping(billingPrefix),
        onSelect: function (suggestion) {
          const el = document.getElementById(billingPrefix + 'normalized');
          if (el) el.value = JSON.stringify(suggestion);
          validateAddress(suggestion.components, billingPrefix);
        },
      });

      const sameAsShipping = document.getElementById('billing_same_as_shipping');
      if (sameAsShipping) {
        sameAsShipping.addEventListener('change', function () {
          const billingSection = document.getElementById('billing-section');
          if (!billingSection) return;
          if (this.checked) {
            billingSection.style.display = 'none';
            copyAddressFields(shippingPrefix, billingPrefix);
          } else {
            billingSection.style.display = 'block';
          }
        });
      }
    }
  });
})();
