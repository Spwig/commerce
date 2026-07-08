/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Form Builder - Frontend Form Renderer
 * Handles form submission, multi-step navigation, validation, and interactive fields
 */

(function() {
    'use strict';

    /**
     * FormRenderer Class
     * Main controller for form functionality
     */
    class FormRenderer {
        constructor(formElement) {
            this.form = formElement;
            this.formSlug = this.form.id.replace('form-', '');
            this.isMultiStep = this.form.classList.contains('multi-step');
            this.currentStep = 0;
            this.steps = [];
            this.formData = {};
            this.responseId = null;

            this.init();
        }

        init() {
            this.bindFormSubmit();
            this.initStarRatings();
            this.initFileUploads();
            this.initProductSelects();

            if (this.isMultiStep) {
                this.initMultiStep();
            }
        }

        /**
         * Form Submission
         */
        bindFormSubmit() {
            this.form.addEventListener('submit', async (e) => {
                e.preventDefault();

                if (!this.validateCurrentStep()) {
                    return;
                }

                const submitBtn = this.form.querySelector('button[type="submit"]');
                const originalText = submitBtn.textContent;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

                try {
                    const formData = new FormData(this.form);
                    const response = await fetch(this.form.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': this.getCSRFToken()
                        }
                    });

                    const result = await response.json();

                    if (response.ok && result.success) {
                        this.showSuccess(result.message);
                    } else {
                        this.showErrors(result.errors || { general: result.error });
                    }
                } catch (error) {
                    console.error('Form submission error:', error);
                    this.showErrors({ general: 'An error occurred. Please try again.' });
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = originalText;
                }
            });
        }

        getCSRFToken() {
            const input = this.form.querySelector('input[name="csrfmiddlewaretoken"]');
            return input ? input.value : '';
        }

        showSuccess(message) {
            this.form.style.display = 'none';
            const messagesContainer = this.form.closest('.form-container').querySelector('.form-messages');
            if (messagesContainer) {
                messagesContainer.style.display = 'block';
                messagesContainer.classList.add('success');
                messagesContainer.querySelector('.success-message').textContent = message;
            }
        }

        showErrors(errors) {
            // Clear previous errors
            this.form.querySelectorAll('.field-error').forEach(el => {
                el.style.display = 'none';
                el.textContent = '';
            });
            this.form.querySelectorAll('.form-input.error, .form-textarea.error, .form-select.error').forEach(el => {
                el.classList.remove('error');
            });

            // Show new errors
            for (const [fieldName, message] of Object.entries(errors)) {
                if (fieldName === 'general') {
                    const messagesContainer = this.form.closest('.form-container').querySelector('.form-messages');
                    if (messagesContainer) {
                        messagesContainer.style.display = 'block';
                        messagesContainer.classList.add('error');
                        messagesContainer.querySelector('.error-message').textContent = message;
                    }
                } else {
                    const field = this.form.querySelector(`[data-field-name="${fieldName}"]`);
                    if (field) {
                        const errorEl = field.querySelector('.field-error');
                        const input = field.querySelector('.form-input, .form-textarea, .form-select');
                        if (errorEl) {
                            errorEl.textContent = message;
                            errorEl.style.display = 'block';
                        }
                        if (input) {
                            input.classList.add('error');
                        }
                    }
                }
            }
        }

        /**
         * Multi-Step Navigation
         */
        initMultiStep() {
            this.steps = Array.from(this.form.querySelectorAll('.form-step'));
            this.progressSteps = Array.from(this.form.querySelectorAll('.progress-step'));

            // Bind next buttons
            this.form.querySelectorAll('.next-step').forEach(btn => {
                btn.addEventListener('click', () => this.nextStep());
            });

            // Bind back buttons
            this.form.querySelectorAll('.prev-step').forEach(btn => {
                btn.addEventListener('click', () => this.prevStep());
            });

            this.updateStepDisplay();
        }

        nextStep() {
            if (!this.validateCurrentStep()) {
                return;
            }

            if (this.currentStep < this.steps.length - 1) {
                this.savePartialResponse();
                this.currentStep++;
                this.updateStepDisplay();
            }
        }

        prevStep() {
            if (this.currentStep > 0) {
                this.currentStep--;
                this.updateStepDisplay();
            }
        }

        updateStepDisplay() {
            // Update step visibility
            this.steps.forEach((step, index) => {
                step.classList.toggle('active', index === this.currentStep);
            });

            // Update progress indicator
            this.progressSteps.forEach((step, index) => {
                step.classList.remove('active', 'completed');
                if (index === this.currentStep) {
                    step.classList.add('active');
                } else if (index < this.currentStep) {
                    step.classList.add('completed');
                }
            });

            // Scroll to top of form
            this.form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        async savePartialResponse() {
            const formData = new FormData(this.form);
            const data = {};
            formData.forEach((value, key) => {
                if (key !== 'csrfmiddlewaretoken') {
                    data[key] = value;
                }
            });

            try {
                const response = await fetch(`/api/form-builder/forms/${this.formSlug}/partial/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify({
                        response_id: this.responseId,
                        current_step: this.currentStep + 1,
                        data: data
                    })
                });

                const result = await response.json();
                if (result.success) {
                    this.responseId = result.response_id;
                }
            } catch (error) {
                console.error('Failed to save partial response:', error);
            }
        }

        /**
         * Validation
         */
        validateCurrentStep() {
            let isValid = true;
            const stepElement = this.isMultiStep ? this.steps[this.currentStep] : this.form;
            const fields = stepElement.querySelectorAll('.form-field');

            fields.forEach(field => {
                const fieldName = field.dataset.fieldName;
                const isRequired = field.dataset.required === 'true';
                const input = field.querySelector('input, textarea, select');

                if (!input) return;

                // Clear previous error
                const errorEl = field.querySelector('.field-error');
                if (errorEl) {
                    errorEl.style.display = 'none';
                }
                input.classList.remove('error');

                // Check required
                if (isRequired) {
                    let value = input.value;

                    // Handle special field types
                    if (input.type === 'checkbox') {
                        value = input.checked ? '1' : '';
                    } else if (input.type === 'hidden' && field.classList.contains('field-rating_stars')) {
                        value = field.querySelector('input[type="hidden"]').value;
                    }

                    if (!value || value.trim() === '') {
                        isValid = false;
                        if (errorEl) {
                            errorEl.textContent = 'This field is required';
                            errorEl.style.display = 'block';
                        }
                        input.classList.add('error');
                    }
                }

                // Additional validation
                if (input.value && !input.checkValidity()) {
                    isValid = false;
                    if (errorEl) {
                        errorEl.textContent = input.validationMessage;
                        errorEl.style.display = 'block';
                    }
                    input.classList.add('error');
                }
            });

            return isValid;
        }

        /**
         * Star Ratings
         */
        initStarRatings() {
            this.form.querySelectorAll('.rating-stars-wrapper').forEach(wrapper => {
                const hiddenInput = wrapper.querySelector('input[type="hidden"]');
                const starBtns = wrapper.querySelectorAll('.star-btn');
                const valueDisplay = wrapper.querySelector('.rating-value-display');

                starBtns.forEach(btn => {
                    btn.addEventListener('click', () => {
                        const value = btn.dataset.value;
                        hiddenInput.value = value;

                        // Update visual state
                        starBtns.forEach((b, index) => {
                            b.classList.toggle('active', index < parseInt(value));
                        });

                        // Update display
                        if (valueDisplay) {
                            valueDisplay.textContent = `${value} / ${starBtns.length}`;
                        }
                    });

                    // Hover effects
                    btn.addEventListener('mouseenter', () => {
                        const value = parseInt(btn.dataset.value);
                        starBtns.forEach((b, index) => {
                            b.classList.toggle('hover', index < value);
                        });
                    });

                    btn.addEventListener('mouseleave', () => {
                        starBtns.forEach(b => b.classList.remove('hover'));
                    });
                });
            });
        }

        /**
         * File Uploads
         */
        initFileUploads() {
            this.form.querySelectorAll('.file-upload-wrapper').forEach(wrapper => {
                const dropzone = wrapper.querySelector('.file-dropzone');
                const input = wrapper.querySelector('.file-input');
                const fileList = wrapper.querySelector('.file-list');
                const maxSize = parseInt(wrapper.dataset.maxSize) || 5;
                const maxFiles = parseInt(wrapper.dataset.maxFiles) || 1;
                const allowedTypes = wrapper.dataset.allowedTypes?.split(',') || [];

                // Drag and drop events
                ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
                    dropzone.addEventListener(event, (e) => {
                        e.preventDefault();
                        e.stopPropagation();
                    });
                });

                ['dragenter', 'dragover'].forEach(event => {
                    dropzone.addEventListener(event, () => {
                        dropzone.classList.add('dragover');
                    });
                });

                ['dragleave', 'drop'].forEach(event => {
                    dropzone.addEventListener(event, () => {
                        dropzone.classList.remove('dragover');
                    });
                });

                dropzone.addEventListener('drop', (e) => {
                    const files = e.dataTransfer.files;
                    this.handleFiles(files, wrapper, maxSize, maxFiles, allowedTypes);
                });

                input.addEventListener('change', () => {
                    this.handleFiles(input.files, wrapper, maxSize, maxFiles, allowedTypes);
                });
            });
        }

        handleFiles(files, wrapper, maxSize, maxFiles, allowedTypes) {
            const fileList = wrapper.querySelector('.file-list');
            const existingFiles = fileList.querySelectorAll('.file-item').length;

            Array.from(files).forEach((file, index) => {
                if (existingFiles + index >= maxFiles) {
                    AdminModal.alert({message: `Maximum ${maxFiles} file(s) allowed`, type: 'warning'});
                    return;
                }

                // Validate size
                if (file.size > maxSize * 1024 * 1024) {
                    AdminModal.alert({message: `File "${file.name}" exceeds ${maxSize}MB limit`, type: 'warning'});
                    return;
                }

                // Validate type
                if (allowedTypes.length > 0) {
                    const ext = file.name.split('.').pop().toLowerCase();
                    if (!allowedTypes.includes(ext)) {
                        AdminModal.alert({message: `File type .${ext} is not allowed`, type: 'warning'});
                        return;
                    }
                }

                // Add file to list
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item';
                fileItem.innerHTML = `
                    <i class="fas fa-file file-item-icon"></i>
                    <div class="file-item-info">
                        <div class="file-item-name">${file.name}</div>
                        <div class="file-item-size">${this.formatFileSize(file.size)}</div>
                    </div>
                    <button type="button" class="file-item-remove">
                        <i class="fas fa-times"></i>
                    </button>
                `;

                fileItem.querySelector('.file-item-remove').addEventListener('click', () => {
                    fileItem.remove();
                });

                fileList.appendChild(fileItem);
            });
        }

        formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        }

        /**
         * Product Select
         */
        initProductSelects() {
            this.form.querySelectorAll('.product-select-wrapper').forEach(wrapper => {
                const searchInput = wrapper.querySelector('.product-search-input');
                const resultsContainer = wrapper.querySelector('.product-results');
                const resultsList = wrapper.querySelector('.product-results-list');
                const selectedContainer = wrapper.querySelector('.selected-products');
                const hiddenInput = wrapper.querySelector('input[type="hidden"]');
                const maxSelections = parseInt(wrapper.dataset.maxSelections) || 1;
                const showPrice = wrapper.dataset.showPrice === 'true';

                let debounceTimer;
                const selectedProducts = new Set();

                searchInput.addEventListener('input', () => {
                    clearTimeout(debounceTimer);
                    debounceTimer = setTimeout(() => {
                        this.searchProducts(searchInput.value, wrapper, showPrice);
                    }, 300);
                });

                searchInput.addEventListener('focus', () => {
                    if (searchInput.value.length >= 2) {
                        resultsContainer.style.display = 'block';
                    }
                });

                // Close results on outside click
                document.addEventListener('click', (e) => {
                    if (!wrapper.contains(e.target)) {
                        resultsContainer.style.display = 'none';
                    }
                });
            });
        }

        async searchProducts(query, wrapper, showPrice) {
            if (query.length < 2) {
                wrapper.querySelector('.product-results').style.display = 'none';
                return;
            }

            const resultsContainer = wrapper.querySelector('.product-results');
            const resultsList = wrapper.querySelector('.product-results-list');
            const loadingEl = wrapper.querySelector('.product-results-loading');
            const emptyEl = wrapper.querySelector('.product-results-empty');

            resultsContainer.style.display = 'block';
            loadingEl.style.display = 'block';
            resultsList.innerHTML = '';
            emptyEl.style.display = 'none';

            try {
                const categories = wrapper.dataset.categories;
                const url = new URL('/api/form-builder/products/search/', window.location.origin);
                url.searchParams.set('q', query);
                if (categories) {
                    url.searchParams.set('categories', categories);
                }

                const response = await fetch(url);
                const products = await response.json();

                loadingEl.style.display = 'none';

                if (products.length === 0) {
                    emptyEl.style.display = 'block';
                    return;
                }

                products.forEach(product => {
                    const item = document.createElement('div');
                    item.className = 'product-result-item';
                    item.innerHTML = `
                        <img src="${product.image || '/static/placeholder.png'}" alt="${product.name}" class="product-result-image">
                        <div>
                            <div class="product-result-name">${product.name}</div>
                            ${showPrice ? `<div class="product-result-price">${product.price}</div>` : ''}
                        </div>
                    `;

                    item.addEventListener('click', () => {
                        this.selectProduct(product, wrapper);
                    });

                    resultsList.appendChild(item);
                });
            } catch (error) {
                console.error('Product search error:', error);
                loadingEl.style.display = 'none';
            }
        }

        selectProduct(product, wrapper) {
            const hiddenInput = wrapper.querySelector('input[type="hidden"]');
            const selectedContainer = wrapper.querySelector('.selected-products');
            const maxSelections = parseInt(wrapper.dataset.maxSelections) || 1;

            // Check max selections
            const currentSelections = selectedContainer.querySelectorAll('.selected-product').length;
            if (currentSelections >= maxSelections) {
                return;
            }

            // Add to selected
            const selectedEl = document.createElement('div');
            selectedEl.className = 'selected-product';
            selectedEl.dataset.productId = product.id;
            selectedEl.innerHTML = `
                <span>${product.name}</span>
                <button type="button" class="selected-product-remove">
                    <i class="fas fa-times"></i>
                </button>
            `;

            selectedEl.querySelector('.selected-product-remove').addEventListener('click', () => {
                selectedEl.remove();
                this.updateProductInput(wrapper);
            });

            selectedContainer.appendChild(selectedEl);
            this.updateProductInput(wrapper);

            // Hide results
            wrapper.querySelector('.product-results').style.display = 'none';
            wrapper.querySelector('.product-search-input').value = '';
        }

        updateProductInput(wrapper) {
            const hiddenInput = wrapper.querySelector('input[type="hidden"]');
            const selectedProducts = wrapper.querySelectorAll('.selected-product');
            const ids = Array.from(selectedProducts).map(el => el.dataset.productId);
            hiddenInput.value = ids.join(',');
        }
    }

    /**
     * Initialize all forms on page
     */
    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.spwig-form').forEach(form => {
            new FormRenderer(form);
        });
    });

})();
