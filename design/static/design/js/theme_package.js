/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Theme Packager JavaScript
 * Handles validation and packaging UI interactions
 */

(function () {
  'use strict';

  // Read translation strings from JSON island (CSP-compliant)
  const msgEl = document.getElementById('package-messages');
  if (msgEl) {
    try {
      window.PackageMessages = JSON.parse(msgEl.textContent);
    } catch (e) {}
  }
  window.PackageMessages = window.PackageMessages || {};

  const csrftoken = AdminUtils.getCsrfToken();

  // DOM Elements
  const themeSelect = document.getElementById('theme-select');
  const themePathInput = document.getElementById('theme-path-input');
  const validateBtn = document.getElementById('validate-btn');
  const packageBtn = document.getElementById('package-btn');
  const revalidateBtn = document.getElementById('revalidate-btn');
  const packageAnotherBtn = document.getElementById('package-another-btn');
  const downloadLink = document.getElementById('download-link');

  const validationSection = document.getElementById('validation-section');
  const packageSection = document.getElementById('package-section');
  const loadingOverlay = document.getElementById('loading-overlay');
  const loadingMessage = document.getElementById('loading-message');

  const themeInfoCard = document.getElementById('theme-info-card');
  const validationStatus = document.getElementById('validation-status');
  const errorsContainer = document.getElementById('errors-container');
  const warningsContainer = document.getElementById('warnings-container');
  const validationActions = document.getElementById('validation-actions');

  let currentThemePath = '';

  // Event Listeners
  if (themeSelect) {
    themeSelect.addEventListener('change', function () {
      if (this.value) {
        themePathInput.value = this.value;
        currentThemePath = this.value;
        validateBtn.disabled = false;
      } else {
        currentThemePath = '';
        validateBtn.disabled = true;
      }
    });
  }

  if (themePathInput) {
    themePathInput.addEventListener('input', function () {
      if (this.value.trim()) {
        currentThemePath = this.value.trim();
        validateBtn.disabled = false;
        if (themeSelect) themeSelect.value = '';
      } else {
        currentThemePath = '';
        validateBtn.disabled = true;
      }
    });
  }

  if (validateBtn) {
    validateBtn.addEventListener('click', validateTheme);
  }

  if (packageBtn) {
    packageBtn.addEventListener('click', packageTheme);
  }

  if (revalidateBtn) {
    revalidateBtn.addEventListener('click', validateTheme);
  }

  if (packageAnotherBtn) {
    packageAnotherBtn.addEventListener('click', resetForm);
  }

  // Validate Theme
  function validateTheme() {
    if (!currentThemePath) {
      AdminModal.alert({ message: window.PackageMessages.selectTheme, type: 'warning' });
      return;
    }

    showLoading(window.PackageMessages.validating);

    fetch('/design/themes/validate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrftoken,
      },
      body: `theme_path=${encodeURIComponent(currentThemePath)}`,
    })
      .then(response => response.json())
      .then(data => {
        hideLoading();

        if (!data.success) {
          AdminModal.alert({
            message: `${window.PackageMessages.error}: ${data.error}`,
            type: 'error',
          });
          return;
        }

        displayValidationResults(data);
      })
      .catch(error => {
        hideLoading();
        console.error('Validation error:', error);
        AdminModal.alert({
          message: `${window.PackageMessages.error}: ${error.message}`,
          type: 'error',
        });
      });
  }

  // Display Validation Results
  function displayValidationResults(data) {
    // Show validation section
    validationSection.style.display = 'block';
    packageSection.style.display = 'none';

    // Display theme info
    if (data.theme_info) {
      themeInfoCard.style.display = 'block';
      document.getElementById('theme-info-name').textContent = data.theme_info.display_name;
      document.getElementById('theme-info-version').textContent = `v${data.theme_info.version}`;
      document.getElementById('theme-info-author').innerHTML =
        `<i class="fas fa-user"></i> ${data.theme_info.author}`;
      document.getElementById('theme-info-description').textContent = data.theme_info.description;
    }

    // Display validation status
    validationStatus.className = `validation-status ${data.is_valid ? 'success' : 'error'}`;
    validationStatus.innerHTML = data.is_valid
      ? `<i class="fas fa-check-circle"></i> <span>${window.PackageMessages.validationPassed}</span>`
      : `<i class="fas fa-times-circle"></i> <span>${window.PackageMessages.validationFailed}</span>`;

    // Display errors
    if (data.errors && data.errors.length > 0) {
      errorsContainer.style.display = 'block';
      document.getElementById('errors-count').textContent = data.errors.length;
      document.getElementById('errors-plural').textContent = data.errors.length > 1 ? 's' : '';

      const errorsList = document.getElementById('errors-list');
      errorsList.innerHTML = '';
      data.errors.forEach(error => {
        const li = document.createElement('li');
        li.innerHTML = `<i class="fas fa-times-circle"></i> <span>${error}</span>`;
        errorsList.appendChild(li);
      });
    } else {
      errorsContainer.style.display = 'none';
    }

    // Display warnings
    if (data.warnings && data.warnings.length > 0) {
      warningsContainer.style.display = 'block';
      document.getElementById('warnings-count').textContent = data.warnings.length;
      document.getElementById('warnings-plural').textContent = data.warnings.length > 1 ? 's' : '';

      const warningsList = document.getElementById('warnings-list');
      warningsList.innerHTML = '';
      data.warnings.forEach(warning => {
        const li = document.createElement('li');
        li.innerHTML = `<i class="fas fa-exclamation-triangle"></i> <span>${warning}</span>`;
        warningsList.appendChild(li);
      });
    } else {
      warningsContainer.style.display = 'none';
    }

    // Show actions
    validationActions.style.display = 'flex';
    packageBtn.disabled = !data.is_valid;

    // Scroll to validation section
    validationSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Package Theme
  function packageTheme() {
    if (!currentThemePath) {
      AdminModal.alert({ message: window.PackageMessages.selectTheme, type: 'warning' });
      return;
    }

    showLoading(window.PackageMessages.packaging);

    fetch('/design/themes/create-package/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': csrftoken,
      },
      body: `theme_path=${encodeURIComponent(currentThemePath)}`,
    })
      .then(response => response.json())
      .then(data => {
        hideLoading();

        if (!data.success) {
          AdminModal.alert({
            message: `${window.PackageMessages.packagingFailed}: ${data.error}`,
            type: 'error',
          });
          return;
        }

        displayPackageResults(data);
      })
      .catch(error => {
        hideLoading();
        console.error('Packaging error:', error);
        AdminModal.alert({
          message: `${window.PackageMessages.error}: ${error.message}`,
          type: 'error',
        });
      });
  }

  // Display Package Results
  function displayPackageResults(data) {
    // Hide validation section, show package section
    validationSection.style.display = 'none';
    packageSection.style.display = 'block';

    // Display package info
    document.getElementById('package-filename').textContent = data.package_filename;
    document.getElementById('package-file-count').textContent = data.package_info.file_count;
    document.getElementById('package-size').textContent = formatBytes(
      data.package_info.package_size
    );
    document.getElementById('package-checksum').textContent =
      data.package_info.package_checksum.substring(0, 16) + '...';

    // Set download link
    downloadLink.href = data.download_url;
    downloadLink.download = data.package_filename;

    // Scroll to package section
    packageSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Reset Form
  function resetForm() {
    // Reset selections
    if (themeSelect) themeSelect.value = '';
    if (themePathInput) themePathInput.value = '';
    currentThemePath = '';
    validateBtn.disabled = true;

    // Hide sections
    validationSection.style.display = 'none';
    packageSection.style.display = 'none';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Show Loading
  function showLoading(message) {
    loadingMessage.textContent = message;
    loadingOverlay.style.display = 'flex';
  }

  // Hide Loading
  function hideLoading() {
    loadingOverlay.style.display = 'none';
  }

  // Format Bytes
  function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
  }
})();
