/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        initFileUpload();
        initPricingToggle();
    });

    function initFileUpload() {
        var fileInput = document.getElementById('package_file');
        if (!fileInput) return;

        var fileSelected = document.getElementById('file-selected');
        var uploadContent = document.querySelector('.dev-file-upload-content');
        var fileName = document.getElementById('file-name');
        var fileSize = document.getElementById('file-size');
        var configEl = document.getElementById('create-submission-config');
        var validateUrl = configEl ? configEl.dataset.validateUrl : '';

        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                var file = this.files[0];
                if (fileName) fileName.textContent = file.name;
                if (fileSize) fileSize.textContent = '(' + (file.size / 1024 / 1024).toFixed(1) + ' MB)';
                if (fileSelected) fileSelected.style.display = 'flex';
                if (uploadContent) uploadContent.style.display = 'none';

                if (!validateUrl) return;

                var formData = new FormData();
                formData.append('package_file', file);
                var typeEl = document.getElementById('component_type');
                if (typeEl) formData.append('component_type', typeEl.value);
                formData.append('csrfmiddlewaretoken', AdminUtils.getCsrfToken());

                var resultsDiv = document.getElementById('validation-results');
                var statusDiv = document.getElementById('validation-status');
                var detailsDiv = document.getElementById('validation-details');

                if (resultsDiv) resultsDiv.style.display = 'block';
                if (statusDiv) {
                    statusDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Validating package...';
                    statusDiv.className = 'dev-validation-status validating';
                }
                if (detailsDiv) detailsDiv.innerHTML = '';

                fetch(validateUrl, { method: 'POST', body: formData })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    if (data.valid) {
                        var m = data.manifest;
                        if (statusDiv) {
                            statusDiv.innerHTML = '<i class="fas fa-check-circle"></i> Package valid';
                            statusDiv.className = 'dev-validation-status valid';
                        }
                        if (detailsDiv) {
                            detailsDiv.innerHTML =
                                '<div class="dev-manifest-preview">' +
                                    '<strong>' + (m.display_name || m.name) + '</strong> v' + m.version + '<br>' +
                                    '<small>Author: ' + m.author + ' | License: ' + (m.license || 'N/A') + '</small>' +
                                '</div>';
                        }
                    } else {
                        if (statusDiv) {
                            statusDiv.innerHTML = '<i class="fas fa-times-circle"></i> Validation failed';
                            statusDiv.className = 'dev-validation-status invalid';
                        }
                        if (detailsDiv) {
                            detailsDiv.innerHTML = '<ul>' + data.errors.map(function (e) {
                                return '<li>' + e + '</li>';
                            }).join('') + '</ul>';
                        }
                    }
                    if (data.warnings && data.warnings.length && detailsDiv) {
                        detailsDiv.innerHTML += '<div class="dev-warnings"><strong>Warnings:</strong><ul>' +
                            data.warnings.map(function (w) { return '<li>' + w + '</li>'; }).join('') +
                            '</ul></div>';
                    }
                })
                .catch(function () {
                    if (statusDiv) {
                        statusDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Could not validate';
                        statusDiv.className = 'dev-validation-status warning';
                    }
                });
            } else {
                if (fileSelected) fileSelected.style.display = 'none';
                if (uploadContent) uploadContent.style.display = 'flex';
            }
        });
    }

    function initPricingToggle() {
        document.addEventListener('change', function (e) {
            if (e.target.name === 'pricing_model') {
                var priceField = document.getElementById('price-field');
                if (priceField) {
                    priceField.style.display = e.target.value === 'paid' ? 'block' : 'none';
                }
            }
        });
    }

}());
