/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let T = {};

  function showResult(resultDiv, type, message) {
    resultDiv.className = 'register-result ' + type;
    resultDiv.querySelector('.result-content').innerHTML = message;
    resultDiv.classList.remove('pos-hidden');
  }

  function initRegisterMode(config) {
    const form = document.getElementById('register-form');
    const registerBtn = document.getElementById('register-btn');
    const resultDiv = document.getElementById('register-result');
    if (!form || !registerBtn || !resultDiv) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const code = document.getElementById('registration_code').value.trim();
      if (!code) {
        showResult(resultDiv, 'error', T.enterCode || 'Please enter a registration code.');
        return;
      }

      registerBtn.disabled = true;
      registerBtn.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> ' + (T.registering || 'Registering...');

      const formData = new FormData(form);
      fetch(form.action || window.location.href, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      })
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          if (data.success) {
            showResult(
              resultDiv,
              'success',
              '<i class="fas fa-check-circle"></i> ' +
                (T.registered || 'Reader registered successfully!') +
                '<br><strong>' +
                data.reader.label +
                '</strong> (' +
                data.reader.type +
                ')'
            );
            setTimeout(function () {
              window.location.href = data.redirect_url || config.step3Url || '';
            }, 1500);
          } else {
            showResult(
              resultDiv,
              'error',
              '<i class="fas fa-times-circle"></i> ' +
                (T.failed || 'Registration failed') +
                ': ' +
                data.error
            );
            registerBtn.disabled = false;
            registerBtn.innerHTML =
              '<i class="fas fa-plug"></i> ' + (T.registerReader || 'Register Reader');
          }
        })
        .catch(function (error) {
          showResult(resultDiv, 'error', '<i class="fas fa-times-circle"></i> ' + error.message);
          registerBtn.disabled = false;
          registerBtn.innerHTML =
            '<i class="fas fa-plug"></i> ' + (T.registerReader || 'Register Reader');
        });
    });
  }

  function initDiscoverMode() {
    const checkboxes = document.querySelectorAll('input[name="selected_readers"]');
    const importBtn = document.getElementById('import-btn');

    function updateImportButton() {
      const checked = document.querySelectorAll('input[name="selected_readers"]:checked');
      if (importBtn) {
        importBtn.disabled = checked.length === 0;
        if (checked.length > 0) {
          importBtn.innerHTML =
            '<i class="fas fa-download"></i> ' +
            (T.import || 'Import') +
            ' (' +
            checked.length +
            ')';
        } else {
          importBtn.innerHTML =
            '<i class="fas fa-download"></i> ' + (T.importSelected || 'Import Selected');
        }
      }
    }

    checkboxes.forEach(function (cb) {
      cb.addEventListener('change', updateImportButton);
    });

    document.addEventListener('click', function (e) {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;
      if (btn.dataset.action === 'select-all') {
        checkboxes.forEach(function (cb) {
          cb.checked = true;
        });
        updateImportButton();
      } else if (btn.dataset.action === 'select-none') {
        checkboxes.forEach(function (cb) {
          cb.checked = false;
        });
        updateImportButton();
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    const el = document.getElementById('reader-wizard-translations');
    if (el) {
      try {
        T = JSON.parse(el.textContent);
      } catch (err) {}
    }

    /* ---- Step 1: Provider & Method Selection ---- */
    const readerSelectForm = document.getElementById('reader-select-form');
    if (readerSelectForm) {
      const methodSection = document.getElementById('method-section');
      const providerRadios = readerSelectForm.querySelectorAll('input[name="provider_id"]');

      function updateMethodVisibility() {
        const selected = readerSelectForm.querySelector('input[name="provider_id"]:checked');
        if (selected && selected.dataset.providerKey === 'manual') {
          if (methodSection) methodSection.classList.add('pos-hidden');
          const registerMethod = readerSelectForm.querySelector(
            'input[name="method"][value="register"]'
          );
          if (registerMethod) registerMethod.checked = true;
        } else {
          if (methodSection) methodSection.classList.remove('pos-hidden');
        }
      }

      providerRadios.forEach(function (radio) {
        radio.addEventListener('change', updateMethodVisibility);
      });

      updateMethodVisibility();
    }

    /* ---- Step 3: Terminal Assignment ---- */
    const step3i18nEl = document.getElementById('reader-step3-i18n');
    let step3T = {};
    if (step3i18nEl) {
      try {
        step3T = JSON.parse(step3i18nEl.textContent);
      } catch (e) {}
    }

    const terminalSelect = document.getElementById('terminal_id');
    const warningDiv = document.getElementById('reassign-warning');
    const addAnotherCheckbox = document.getElementById('add_another');
    const saveBtn = document.getElementById('save-btn');

    if (terminalSelect && warningDiv) {
      terminalSelect.addEventListener('change', function () {
        const selectedOption = this.options[this.selectedIndex];
        if (selectedOption.dataset.hasReader) {
          warningDiv.classList.remove('pos-hidden');
        } else {
          warningDiv.classList.add('pos-hidden');
        }
      });
    }

    if (addAnotherCheckbox && saveBtn) {
      addAnotherCheckbox.addEventListener('change', function () {
        if (this.checked) {
          saveBtn.innerHTML =
            '<i class="fas fa-plus"></i> ' + (step3T.saveAndAddAnother || 'Save & Add Another');
        } else {
          saveBtn.innerHTML =
            '<i class="fas fa-check"></i> ' + (step3T.saveAndFinish || 'Save & Finish');
        }
      });
    }

    const configEl = document.getElementById('reader-wizard-config');
    const config = configEl ? configEl.dataset : {};

    if (config.mode === 'register') {
      initRegisterMode(config);
    } else {
      initDiscoverMode();
    }
  });
})();
