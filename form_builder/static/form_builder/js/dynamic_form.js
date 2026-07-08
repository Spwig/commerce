/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * DynamicForm - Frontend Form Handler
 *
 * Handles multi-step navigation, conditional logic, validation, and AJAX submission
 * for forms created with the Form Builder.
 */

class DynamicForm {
    constructor(container, formData) {
        this.container = container;
        this.formData = formData;
        this.form = container.querySelector('form');

        if (!this.form) return;

        // State
        this.currentStep = 0;
        this.totalSteps = formData.steps?.length || 1;
        this.formValues = {};
        this.hiddenFields = new Set();
        this.requiredOverrides = new Map();

        // Configuration from data attributes
        this.config = {
            validateOn: this.form.dataset.validateOn || 'blur',
            validationDisplay: this.form.dataset.validationDisplay || 'below_field',
            successAction: this.form.dataset.successAction || 'replace',
            successRedirect: this.form.dataset.successRedirect || '',
            scrollToError: this.form.dataset.scrollToError !== 'false',
        };

        // Initialize
        this.init();
    }

    init() {
        this.bindEvents();
        this.initializeFieldValues();
        this.evaluateAllRules();
        this.updateStepIndicator();
    }

    /**
     * Bind all event listeners
     */
    bindEvents() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Step navigation
        this.container.querySelectorAll('.fb-form__btn--next').forEach(btn => {
            btn.addEventListener('click', () => this.nextStep());
        });

        this.container.querySelectorAll('.fb-form__btn--back').forEach(btn => {
            btn.addEventListener('click', () => this.prevStep());
        });

        // Field change events for conditional logic
        this.form.querySelectorAll('input, select, textarea').forEach(field => {
            field.addEventListener('change', (e) => this.handleFieldChange(e));

            // Validation based on config
            if (this.config.validateOn === 'blur') {
                field.addEventListener('blur', (e) => this.validateField(e.target));
            } else if (this.config.validateOn === 'input') {
                field.addEventListener('input', (e) => this.validateField(e.target));
            }
        });

        // Star rating interactions
        this.initStarRatings();

        // NPS rating interactions
        this.initNPSRatings();

        // File upload interactions
        this.initFileUploads();
    }

    /**
     * Initialize star rating fields
     */
    initStarRatings() {
        this.container.querySelectorAll('.form-star-rating').forEach(rating => {
            const stars = rating.querySelectorAll('.form-star');
            const input = rating.querySelector('input[type="hidden"]');
            const maxStars = parseInt(rating.dataset.max) || 5;

            stars.forEach((star, index) => {
                star.addEventListener('click', () => {
                    const value = index + 1;
                    input.value = value;

                    stars.forEach((s, i) => {
                        const icon = s.querySelector('i');
                        if (i < value) {
                            icon.classList.remove('far');
                            icon.classList.add('fas');
                            s.classList.add('active');
                        } else {
                            icon.classList.add('far');
                            icon.classList.remove('fas');
                            s.classList.remove('active');
                        }
                    });

                    // Trigger change for conditional logic
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                });

                star.addEventListener('mouseenter', () => {
                    stars.forEach((s, i) => {
                        if (i <= index) {
                            s.classList.add('hover');
                        }
                    });
                });

                star.addEventListener('mouseleave', () => {
                    stars.forEach(s => s.classList.remove('hover'));
                });
            });
        });
    }

    /**
     * Initialize NPS rating fields
     */
    initNPSRatings() {
        this.container.querySelectorAll('.form-nps-rating').forEach(rating => {
            const buttons = rating.querySelectorAll('.form-nps-btn');
            const input = rating.querySelector('input[type="hidden"]');

            buttons.forEach(btn => {
                btn.addEventListener('click', () => {
                    const value = btn.dataset.value;
                    input.value = value;

                    buttons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');

                    // Trigger change for conditional logic
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                });
            });
        });
    }

    /**
     * Initialize file upload fields
     */
    initFileUploads() {
        this.container.querySelectorAll('.form-file-upload').forEach(upload => {
            const input = upload.querySelector('.form-file-input');
            const info = upload.querySelector('.form-file-info');

            input.addEventListener('change', () => {
                if (input.files.length > 0) {
                    const fileNames = Array.from(input.files).map(f => f.name).join(', ');
                    info.textContent = fileNames;
                    info.style.display = 'block';
                } else {
                    info.style.display = 'none';
                }
            });
        });
    }

    /**
     * Initialize form field values from DOM
     */
    initializeFieldValues() {
        this.form.querySelectorAll('input, select, textarea').forEach(field => {
            const name = field.name;
            if (!name || name === 'csrfmiddlewaretoken' || name === 'fb_hp_field') return;

            if (field.type === 'checkbox') {
                if (!this.formValues[name]) {
                    this.formValues[name] = [];
                }
                if (field.checked) {
                    this.formValues[name].push(field.value);
                }
            } else if (field.type === 'radio') {
                if (field.checked) {
                    this.formValues[name] = field.value;
                }
            } else {
                this.formValues[name] = field.value;
            }
        });
    }

    /**
     * Handle field change events
     */
    handleFieldChange(e) {
        const field = e.target;
        const name = field.name;

        if (!name || name === 'csrfmiddlewaretoken' || name === 'fb_hp_field') return;

        // Update form values
        if (field.type === 'checkbox') {
            if (!this.formValues[name]) {
                this.formValues[name] = [];
            }
            if (field.checked) {
                if (!this.formValues[name].includes(field.value)) {
                    this.formValues[name].push(field.value);
                }
            } else {
                this.formValues[name] = this.formValues[name].filter(v => v !== field.value);
            }
        } else {
            this.formValues[name] = field.value;
        }

        // Evaluate conditional rules
        this.evaluateAllRules();
    }

    /**
     * Evaluate all conditional rules
     */
    evaluateAllRules() {
        if (!this.formData.rules || this.formData.rules.length === 0) return;

        // Reset hidden fields and required overrides
        this.hiddenFields.clear();
        this.requiredOverrides.clear();

        // Sort rules by priority
        const sortedRules = [...this.formData.rules].sort((a, b) => b.priority - a.priority);

        // Evaluate each rule
        sortedRules.forEach(rule => {
            const result = this.evaluateRule(rule);
            if (result) {
                this.executeRuleAction(rule);
            }
        });

        // Apply visibility changes
        this.applyFieldVisibility();
    }

    /**
     * Evaluate a single rule
     */
    evaluateRule(rule) {
        const fieldValue = this.formValues[rule.source_field_name];
        const comparisonValue = rule.value?.value !== undefined ? rule.value.value : rule.value;

        switch (rule.operator) {
            case 'equals':
                return String(fieldValue).toLowerCase() === String(comparisonValue).toLowerCase();

            case 'not_equals':
                return String(fieldValue).toLowerCase() !== String(comparisonValue).toLowerCase();

            case 'contains':
                return String(fieldValue).toLowerCase().includes(String(comparisonValue).toLowerCase());

            case 'not_contains':
                return !String(fieldValue).toLowerCase().includes(String(comparisonValue).toLowerCase());

            case 'greater_than':
                return parseFloat(fieldValue) > parseFloat(comparisonValue);

            case 'less_than':
                return parseFloat(fieldValue) < parseFloat(comparisonValue);

            case 'greater_than_or_equal':
                return parseFloat(fieldValue) >= parseFloat(comparisonValue);

            case 'less_than_or_equal':
                return parseFloat(fieldValue) <= parseFloat(comparisonValue);

            case 'is_empty':
                return !fieldValue || fieldValue === '' || (Array.isArray(fieldValue) && fieldValue.length === 0);

            case 'is_not_empty':
                return fieldValue && fieldValue !== '' && (!Array.isArray(fieldValue) || fieldValue.length > 0);

            case 'in_list':
                const list = rule.value?.list || [];
                return list.some(v => String(v).toLowerCase() === String(fieldValue).toLowerCase());

            case 'not_in_list':
                const notList = rule.value?.list || [];
                return !notList.some(v => String(v).toLowerCase() === String(fieldValue).toLowerCase());

            case 'starts_with':
                return String(fieldValue).toLowerCase().startsWith(String(comparisonValue).toLowerCase());

            case 'ends_with':
                return String(fieldValue).toLowerCase().endsWith(String(comparisonValue).toLowerCase());

            default:
                return false;
        }
    }

    /**
     * Execute a rule's action
     */
    executeRuleAction(rule) {
        switch (rule.action) {
            case 'show_field':
                // Field will be shown (remove from hidden set if present)
                // This is handled by not adding to hiddenFields
                break;

            case 'hide_field':
                if (rule.target_field_name) {
                    this.hiddenFields.add(rule.target_field_name);
                }
                break;

            case 'require_field':
                if (rule.target_field_name) {
                    this.requiredOverrides.set(rule.target_field_name, true);
                }
                break;

            case 'unrequire_field':
                if (rule.target_field_name) {
                    this.requiredOverrides.set(rule.target_field_name, false);
                }
                break;

            case 'skip_to_step':
                // This is handled during step navigation
                break;

            case 'set_value':
                if (rule.target_field_name && rule.action_value?.value !== undefined) {
                    const field = this.form.querySelector(`[name="${rule.target_field_name}"]`);
                    if (field) {
                        field.value = rule.action_value.value;
                        this.formValues[rule.target_field_name] = rule.action_value.value;
                    }
                }
                break;
        }
    }

    /**
     * Apply field visibility based on rules
     */
    applyFieldVisibility() {
        this.container.querySelectorAll('.fb-field').forEach(fieldWrapper => {
            const fieldName = fieldWrapper.dataset.fieldName;

            if (this.hiddenFields.has(fieldName)) {
                fieldWrapper.style.display = 'none';
                fieldWrapper.classList.add('fb-field--hidden');

                // Clear hidden field values and remove required
                const field = fieldWrapper.querySelector('input, select, textarea');
                if (field) {
                    field.removeAttribute('required');
                }
            } else {
                fieldWrapper.style.display = '';
                fieldWrapper.classList.remove('fb-field--hidden');

                // Restore required attribute based on original config and overrides
                const field = fieldWrapper.querySelector('input, select, textarea');
                if (field) {
                    const fieldData = this.formData.fields.find(f => f.field_name === fieldName);
                    const override = this.requiredOverrides.get(fieldName);

                    if (override !== undefined) {
                        if (override) {
                            field.setAttribute('required', '');
                        } else {
                            field.removeAttribute('required');
                        }
                    } else if (fieldData?.is_required) {
                        field.setAttribute('required', '');
                    }
                }
            }
        });
    }

    /**
     * Navigate to next step
     */
    nextStep() {
        // Validate current step fields
        if (!this.validateCurrentStep()) {
            return;
        }

        // Save partial response if enabled
        if (this.container.dataset.savePartial === 'true') {
            this.savePartialResponse();
        }

        // Check for skip rules
        let targetStep = this.currentStep + 1;
        const skipRule = this.formData.rules?.find(r =>
            r.action === 'skip_to_step' &&
            this.evaluateRule(r) &&
            r.target_step_order > this.currentStep
        );

        if (skipRule) {
            targetStep = skipRule.target_step_order;
        }

        if (targetStep < this.totalSteps) {
            this.goToStep(targetStep);
        }
    }

    /**
     * Navigate to previous step
     */
    prevStep() {
        if (this.currentStep > 0) {
            this.goToStep(this.currentStep - 1);
        }
    }

    /**
     * Go to a specific step
     */
    goToStep(stepIndex) {
        const transition = this.container.dataset.transition || 'slide';
        const currentStepEl = this.container.querySelector(`.fb-form__step[data-step="${this.currentStep}"]`);
        const targetStepEl = this.container.querySelector(`.fb-form__step[data-step="${stepIndex}"]`);

        if (!targetStepEl) return;

        // Apply transition
        if (transition === 'slide') {
            const direction = stepIndex > this.currentStep ? 'left' : 'right';
            currentStepEl.style.transform = `translateX(${direction === 'left' ? '-100%' : '100%'})`;
            currentStepEl.style.opacity = '0';

            setTimeout(() => {
                currentStepEl.style.display = 'none';
                currentStepEl.classList.remove('fb-form__step--active');

                targetStepEl.style.display = '';
                targetStepEl.style.transform = `translateX(${direction === 'left' ? '100%' : '-100%'})`;
                targetStepEl.classList.add('fb-form__step--active');

                requestAnimationFrame(() => {
                    targetStepEl.style.transform = 'translateX(0)';
                    targetStepEl.style.opacity = '1';
                });
            }, 200);

        } else if (transition === 'fade') {
            currentStepEl.style.opacity = '0';

            setTimeout(() => {
                currentStepEl.style.display = 'none';
                currentStepEl.classList.remove('fb-form__step--active');

                targetStepEl.style.display = '';
                targetStepEl.style.opacity = '0';
                targetStepEl.classList.add('fb-form__step--active');

                requestAnimationFrame(() => {
                    targetStepEl.style.opacity = '1';
                });
            }, 200);

        } else {
            // Instant
            currentStepEl.style.display = 'none';
            currentStepEl.classList.remove('fb-form__step--active');
            targetStepEl.style.display = '';
            targetStepEl.classList.add('fb-form__step--active');
        }

        this.currentStep = stepIndex;
        this.updateStepIndicator();

        // Scroll to top of form
        this.container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Update step indicator
     */
    updateStepIndicator() {
        // Update progress bar
        const progressFill = this.container.querySelector('.fb-progress-bar__fill');
        if (progressFill) {
            const progress = ((this.currentStep + 1) / this.totalSteps) * 100;
            progressFill.style.width = `${progress}%`;
        }

        // Update progress text
        const currentText = this.container.querySelector('.fb-progress-bar__current, .fb-steps-text__current');
        if (currentText) {
            currentText.textContent = this.currentStep + 1;
        }

        // Update step circles
        this.container.querySelectorAll('.fb-step-circle').forEach((circle, index) => {
            circle.classList.remove('fb-step-circle--active', 'fb-step-circle--completed');
            if (index < this.currentStep) {
                circle.classList.add('fb-step-circle--completed');
            } else if (index === this.currentStep) {
                circle.classList.add('fb-step-circle--active');
            }
        });

        // Update breadcrumb
        this.container.querySelectorAll('.fb-breadcrumb__item').forEach((item, index) => {
            item.classList.remove('fb-breadcrumb__item--active', 'fb-breadcrumb__item--completed');
            if (index < this.currentStep) {
                item.classList.add('fb-breadcrumb__item--completed');
            } else if (index === this.currentStep) {
                item.classList.add('fb-breadcrumb__item--active');
            }
        });
    }

    /**
     * Validate current step fields
     */
    validateCurrentStep() {
        const stepEl = this.container.querySelector(`.fb-form__step[data-step="${this.currentStep}"]`);
        if (!stepEl) return true;

        let isValid = true;
        const fields = stepEl.querySelectorAll('input, select, textarea');

        fields.forEach(field => {
            const fieldWrapper = field.closest('.fb-field');
            if (fieldWrapper && fieldWrapper.classList.contains('fb-field--hidden')) {
                return; // Skip hidden fields
            }

            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        if (!isValid && this.config.scrollToError) {
            const firstError = stepEl.querySelector('.form-input--error, .form-error:not([style*="display: none"])');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }

        return isValid;
    }

    /**
     * Validate a single field
     */
    validateField(field) {
        const fieldWrapper = field.closest('.fb-field, .form-group');
        const errorEl = fieldWrapper?.querySelector('.form-error');

        // Clear previous error state
        field.classList.remove('form-input--error', 'form-input--success');
        if (errorEl) {
            errorEl.style.display = 'none';
        }

        // Skip validation for hidden fields
        if (fieldWrapper?.classList.contains('fb-field--hidden')) {
            return true;
        }

        let isValid = true;
        let errorMessage = '';

        // Required validation
        if (field.hasAttribute('required')) {
            if (field.type === 'checkbox') {
                if (!field.checked) {
                    isValid = false;
                    errorMessage = 'This field is required.';
                }
            } else if (!field.value.trim()) {
                isValid = false;
                errorMessage = 'This field is required.';
            }
        }

        // Pattern validation
        if (isValid && field.hasAttribute('pattern') && field.value) {
            const pattern = new RegExp(field.pattern);
            if (!pattern.test(field.value)) {
                isValid = false;
                errorMessage = field.dataset.patternMessage || 'Please enter a valid value.';
            }
        }

        // Min/max length validation
        if (isValid && field.value) {
            const minLength = field.getAttribute('minlength');
            const maxLength = field.getAttribute('maxlength');

            if (minLength && field.value.length < parseInt(minLength)) {
                isValid = false;
                errorMessage = `Please enter at least ${minLength} characters.`;
            }

            if (maxLength && field.value.length > parseInt(maxLength)) {
                isValid = false;
                errorMessage = `Please enter no more than ${maxLength} characters.`;
            }
        }

        // Email validation
        if (isValid && field.type === 'email' && field.value) {
            const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailPattern.test(field.value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address.';
            }
        }

        // Apply validation state
        if (!isValid) {
            field.classList.add('form-input--error');
            if (errorEl) {
                errorEl.textContent = errorMessage;
                errorEl.style.display = '';
            }
        } else if (field.value && this.config.showSuccessState) {
            field.classList.add('form-input--success');
        }

        return isValid;
    }

    /**
     * Validate entire form
     */
    validateForm() {
        let isValid = true;
        const fields = this.form.querySelectorAll('input, select, textarea');

        fields.forEach(field => {
            const fieldWrapper = field.closest('.fb-field');
            if (fieldWrapper && fieldWrapper.classList.contains('fb-field--hidden')) {
                return;
            }

            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    /**
     * Handle form submission
     */
    async handleSubmit(e) {
        e.preventDefault();

        // Check honeypot
        const honeypot = this.form.querySelector('[name="fb_hp_field"]');
        if (honeypot && honeypot.value) {
            console.warn('Honeypot triggered');
            return;
        }

        // Validate form
        if (!this.validateForm()) {
            if (this.config.scrollToError) {
                const firstError = this.form.querySelector('.form-input--error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            return;
        }

        // Get submit button and show loading state
        const submitBtn = this.form.querySelector('.fb-form__btn--submit');
        const originalText = submitBtn?.textContent;
        const loadingText = submitBtn?.dataset.loadingText;

        if (submitBtn && loadingText) {
            submitBtn.disabled = true;
            submitBtn.textContent = loadingText;
        }

        try {
            // Prepare form data
            const formData = new FormData(this.form);

            // Remove honeypot and hidden fields
            formData.delete('fb_hp_field');
            this.hiddenFields.forEach(fieldName => {
                formData.delete(fieldName);
            });

            // Submit via AJAX
            const response = await fetch(this.form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });

            const result = await response.json();

            if (response.ok && result.success) {
                this.handleSuccess(result);
            } else {
                this.handleError(result);
            }

        } catch (error) {
            console.error('Form submission error:', error);
            this.handleError({ error: 'An unexpected error occurred. Please try again.' });

        } finally {
            // Restore submit button
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            }
        }
    }

    /**
     * Handle successful submission
     */
    handleSuccess(result) {
        const successEl = this.container.querySelector('.fb-form__success');
        const successMessage = this.container.querySelector('.fb-form__success-message');

        if (result.message && successMessage) {
            successMessage.textContent = result.message;
        }

        switch (this.config.successAction) {
            case 'redirect':
                if (this.config.successRedirect) {
                    window.location.href = this.config.successRedirect;
                }
                break;

            case 'replace':
                this.form.style.display = 'none';
                if (successEl) {
                    successEl.style.display = '';
                }
                break;

            case 'message':
            default:
                if (successEl) {
                    successEl.style.display = '';
                }
                this.form.reset();
                this.initializeFieldValues();
                this.evaluateAllRules();

                // Go back to first step for multi-step forms
                if (this.totalSteps > 1) {
                    this.goToStep(0);
                }
                break;
        }

        // Scroll to success message
        if (successEl && successEl.style.display !== 'none') {
            successEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    /**
     * Handle submission error
     */
    handleError(result) {
        const errorEl = this.container.querySelector('.fb-form__error');
        const errorMessage = this.container.querySelector('.fb-form__error-message');

        // Show field-specific errors
        if (result.errors) {
            Object.entries(result.errors).forEach(([fieldName, message]) => {
                const field = this.form.querySelector(`[name="${fieldName}"]`);
                if (field) {
                    field.classList.add('form-input--error');
                    const fieldWrapper = field.closest('.fb-field, .form-group');
                    const fieldError = fieldWrapper?.querySelector('.form-error');
                    if (fieldError) {
                        fieldError.textContent = message;
                        fieldError.style.display = '';
                    }
                }
            });
        }

        // Show general error message
        if (errorEl) {
            if (result.error && errorMessage) {
                errorMessage.textContent = result.error;
            }
            errorEl.style.display = '';
        }

        // Scroll to error
        if (this.config.scrollToError) {
            const firstError = this.form.querySelector('.form-input--error') || errorEl;
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }

    /**
     * Save partial response for multi-step forms
     */
    async savePartialResponse() {
        const slug = this.container.dataset.formSlug;
        if (!slug) return;

        try {
            const formData = new FormData(this.form);
            const data = {};

            for (const [key, value] of formData.entries()) {
                if (key !== 'csrfmiddlewaretoken' && key !== 'fb_hp_field') {
                    data[key] = value;
                }
            }

            await fetch(`/api/form-builder/forms/${slug}/partial/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken') || (window.getCSRFToken ? window.getCSRFToken() : ''),
                },
                body: JSON.stringify({
                    current_step: this.currentStep + 1,
                    data: data,
                })
            });

        } catch (error) {
            console.error('Failed to save partial response:', error);
        }
    }
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DynamicForm;
}

// Make available globally
window.DynamicForm = DynamicForm;
