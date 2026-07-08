/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * SEO Generator Admin Integration
 *
 * Adds "Regenerate SEO" button to admin change forms for models with SEO fields.
 * Provides real-time Google-style preview of SEO content.
 */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        // Only run on change forms (not add forms or list views)
        var saveButton = document.querySelector(
            'button[name="_save"], input[name="_save"], ' +
            'button[name="_continue"], input[name="_continue"]'
        );

        if (!saveButton) {
            return;
        }

        var form = saveButton.closest('form');
        if (!form) {
            return;
        }

        // Check if this model has SEO fields
        var metaTitleField = document.querySelector('#id_meta_title');
        var metaDescriptionField = document.querySelector('#id_meta_description');

        if (!metaTitleField && !metaDescriptionField) {
            return;
        }

        // Get object ID from URL
        var urlMatch = window.location.pathname.match(/\/(\d+)\/change\//);
        if (!urlMatch) {
            return;
        }
        var objectId = urlMatch[1];

        // Determine model type from URL
        var modelType = detectModelType();
        if (!modelType) {
            return;
        }

        // Create the "Regenerate SEO" button
        createSEOButton(modelType, objectId, metaTitleField, metaDescriptionField);

        // Initialize SEO preview
        initializeSEOPreview(metaTitleField, metaDescriptionField);
    });

    /**
     * Detect model type from current URL path.
     */
    function detectModelType() {
        var path = window.location.pathname;
        if (path.includes('/product/')) return 'product';
        if (path.includes('/category/') && !path.includes('/blogcategory/')) return 'category';
        if (path.includes('/brand/')) return 'brand';
        if (path.includes('/page/')) return 'page';
        if (path.includes('/blogpost/')) return 'blogpost';
        if (path.includes('/blogcategory/')) return 'blogcategory';
        return null;
    }

    /**
     * Read i18n labels from data attributes on the config element, with English fallbacks.
     */
    function getLabels() {
        var configEl = document.querySelector('#seo-generator-container, [data-seo-labels]');
        return {
            regenerate: (configEl && configEl.dataset.seoLabelRegenerate) || 'Regenerate SEO',
            regenerateTitle: (configEl && configEl.dataset.seoLabelRegenerateTitle) || 'Generate meta title and description from content',
            generating: (configEl && configEl.dataset.seoLabelGenerating) || 'Generating...',
            success: (configEl && configEl.dataset.seoLabelSuccess) || 'SEO generated successfully!',
            failed: (configEl && configEl.dataset.seoLabelFailed) || 'SEO generation failed. Please try again.',
            noTitle: (configEl && configEl.dataset.seoLabelNoTitle) || 'No title set',
            noDescription: (configEl && configEl.dataset.seoLabelNoDescription) || 'No description set'
        };
    }

    function createSEOButton(modelType, objectId, metaTitleField, metaDescriptionField) {
        var labels = getLabels();

        // Create button container
        var buttonContainer = document.createElement('div');
        buttonContainer.className = 'seo-generator-button-container';

        // Create button
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'button seo-generate-btn';
        button.innerHTML = '<i class="fas fa-magic"></i> ' + escapeHTML(labels.regenerate);
        button.title = labels.regenerateTitle;

        // Create loading indicator (hidden by default via CSS class)
        var loadingSpinner = document.createElement('span');
        loadingSpinner.className = 'seo-loading seo-hidden';
        loadingSpinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + escapeHTML(labels.generating);

        // Create result message (hidden by default via CSS class)
        var resultMessage = document.createElement('span');
        resultMessage.className = 'seo-result-message seo-hidden';

        buttonContainer.appendChild(button);
        buttonContainer.appendChild(loadingSpinner);
        buttonContainer.appendChild(resultMessage);

        // Check if there's a custom SEO generator container (for custom templates like Product)
        var customContainer = document.querySelector('#seo-generator-container');

        if (customContainer) {
            customContainer.appendChild(buttonContainer);
        } else {
            // Standard Django admin template - find the SEO fieldset
            var seoFieldset = null;
            document.querySelectorAll('.module h2').forEach(function(header) {
                if (header.textContent.includes('SEO')) {
                    seoFieldset = header.closest('.module');
                }
            });

            if (!seoFieldset) {
                return;
            }

            // Insert button after the SEO fieldset header
            var fieldsetContent = seoFieldset.querySelector('.module');
            if (fieldsetContent) {
                fieldsetContent.insertBefore(buttonContainer, fieldsetContent.firstChild);
            } else {
                seoFieldset.appendChild(buttonContainer);
            }
        }

        // Add click handler
        button.addEventListener('click', function() {
            generateSEO(modelType, objectId, button, loadingSpinner, resultMessage, metaTitleField, metaDescriptionField);
        });
    }

    function generateSEO(modelType, objectId, button, loadingSpinner, resultMessage, metaTitleField, metaDescriptionField) {
        var labels = getLabels();

        // Show loading state
        button.disabled = true;
        loadingSpinner.classList.remove('seo-hidden');
        resultMessage.classList.add('seo-hidden');

        // Get CSRF token using AdminUtils
        var csrfToken = (typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken)
            ? AdminUtils.getCsrfToken()
            : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

        // Call SEO generation API
        fetch('/api/seo/generate/' + modelType + '/' + objectId + '/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({})
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            if (data.success) {
                // Update fields
                if (metaTitleField && data.meta_title) {
                    metaTitleField.value = data.meta_title;
                }
                if (metaDescriptionField && data.meta_description) {
                    metaDescriptionField.value = data.meta_description;
                }

                // Update SEO preview
                var previewContainer = document.querySelector('#seo-preview-content');
                if (previewContainer) {
                    updateSEOPreview(metaTitleField, metaDescriptionField, previewContainer);
                }

                // Show success message
                showMessage(resultMessage, labels.success, 'success');

                // Mark fields as changed
                if (metaTitleField) metaTitleField.dispatchEvent(new Event('input'));
                if (metaDescriptionField) metaDescriptionField.dispatchEvent(new Event('input'));
            } else {
                showMessage(resultMessage, data.error || labels.failed, 'error');
            }
        })
        .catch(function() {
            showMessage(resultMessage, labels.failed, 'error');
        })
        .finally(function() {
            button.disabled = false;
            loadingSpinner.classList.add('seo-hidden');
        });
    }

    function showMessage(element, message, type) {
        element.textContent = message;
        element.classList.remove('seo-hidden');
        element.className = 'seo-result-message seo-result-' + type;

        // Auto-hide after 5 seconds
        setTimeout(function() {
            element.classList.add('seo-hidden');
        }, 5000);
    }

    function initializeSEOPreview(metaTitleField, metaDescriptionField) {
        var previewContainer = document.querySelector('#seo-preview-content');

        if (!previewContainer) {
            return;
        }

        // Update preview immediately with current values
        updateSEOPreview(metaTitleField, metaDescriptionField, previewContainer);

        // Add event listeners for real-time updates
        if (metaTitleField) {
            metaTitleField.addEventListener('input', function() {
                updateSEOPreview(metaTitleField, metaDescriptionField, previewContainer);
            });
            metaTitleField.addEventListener('change', function() {
                updateSEOPreview(metaTitleField, metaDescriptionField, previewContainer);
            });
        }

        if (metaDescriptionField) {
            metaDescriptionField.addEventListener('input', function() {
                updateSEOPreview(metaTitleField, metaDescriptionField, previewContainer);
            });
            metaDescriptionField.addEventListener('change', function() {
                updateSEOPreview(metaTitleField, metaDescriptionField, previewContainer);
            });
        }
    }

    function updateSEOPreview(metaTitleField, metaDescriptionField, previewContainer) {
        var labels = getLabels();
        var title = metaTitleField ? metaTitleField.value : '';
        var description = metaDescriptionField ? metaDescriptionField.value : '';

        // Get site domain and build breadcrumb
        var domain = window.location.hostname;
        var breadcrumb = buildBreadcrumb();

        // Get product image if available
        var productImage = getProductImage();

        var titleHTML = escapeHTML(title) || '<span class="seo-preview-empty">' + escapeHTML(labels.noTitle) + '</span>';
        var descHTML = escapeHTML(description) || '<span class="seo-preview-empty">' + escapeHTML(labels.noDescription) + '</span>';

        // Create preview HTML (no inline styles - all styling via CSS classes)
        var previewHTML =
            '<div class="seo-preview-google">' +
                '<div class="seo-preview-header">' +
                    '<div class="seo-preview-favicon">' +
                        '<svg width="24" height="24" viewBox="0 0 24 24">' +
                            '<circle cx="12" cy="12" r="10"/>' +
                            '<text x="12" y="16" font-size="12" text-anchor="middle">' + domain.charAt(0).toUpperCase() + '</text>' +
                        '</svg>' +
                    '</div>' +
                    '<div class="seo-preview-domain-info">' +
                        '<div class="seo-preview-domain">' + escapeHTML(domain) + '</div>' +
                        '<div class="seo-preview-breadcrumb">' + escapeHTML(breadcrumb) + '</div>' +
                    '</div>' +
                '</div>' +
                '<div class="seo-preview-content">' +
                    '<div class="seo-preview-text">' +
                        '<div class="seo-preview-title">' + titleHTML + '</div>' +
                        '<div class="seo-preview-description">' + descHTML + '</div>' +
                    '</div>' +
                    (productImage ? '<div class="seo-preview-image"><img src="' + escapeHTML(productImage) + '" alt=""></div>' : '') +
                '</div>' +
            '</div>';

        previewContainer.innerHTML = previewHTML;
    }

    function buildBreadcrumb() {
        var domain = window.location.hostname;
        var breadcrumb = domain;

        var categorySelect = document.querySelector('#id_category');
        if (categorySelect && categorySelect.selectedOptions.length > 0) {
            var categoryName = categorySelect.selectedOptions[0].text;
            if (categoryName && categoryName !== '---------') {
                breadcrumb += ' \u203A ' + categoryName;
            }
        }

        return breadcrumb;
    }

    function getProductImage() {
        var headerThumbnail = document.querySelector('.header-thumbnail');
        if (headerThumbnail && headerThumbnail.src) {
            return headerThumbnail.src;
        }

        var imageCardPreview = document.querySelector('.image-card-preview img');
        if (imageCardPreview && imageCardPreview.src) {
            return imageCardPreview.src;
        }

        var mediaLibraryImage = document.querySelector('.media-item img, .media-gallery img');
        if (mediaLibraryImage && mediaLibraryImage.src) {
            return mediaLibraryImage.src;
        }

        return null;
    }

    function escapeHTML(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

})();
