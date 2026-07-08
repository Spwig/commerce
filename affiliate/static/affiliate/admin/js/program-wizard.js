/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Affiliate Program Wizard
 * Multi-step form for creating affiliate programs with live preview and validation.
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('wizard-form');
        if (!form) return; // Not on wizard page

        // Get translations from data island
        const translationsEl = document.getElementById('wizard-translations');
        const t = translationsEl ? JSON.parse(translationsEl.textContent) : {};

        const steps = document.querySelectorAll('.wizard-step');
        const stepIndicators = document.querySelectorAll('.wizard-steps .step');
        const btnPrev = document.getElementById('btn-prev');
        const btnNext = document.getElementById('btn-next');
        const btnCreate = document.getElementById('btn-create');

        let currentStep = 1;
        const totalSteps = 5;

        // Show specific step
        function showStep(step) {
            steps.forEach(s => s.style.display = 'none');
            document.querySelector(`.wizard-step[data-step="${step}"]`).style.display = 'block';

            // Update step indicators
            stepIndicators.forEach((indicator, index) => {
                indicator.classList.remove('active', 'completed');
                if (index + 1 < step) {
                    indicator.classList.add('completed');
                } else if (index + 1 === step) {
                    indicator.classList.add('active');
                }
            });

            // Update buttons
            btnPrev.style.display = step > 1 ? 'inline-flex' : 'none';
            btnNext.style.display = step < totalSteps ? 'inline-flex' : 'none';
            btnCreate.style.display = step === totalSteps ? 'inline-flex' : 'none';

            // Update review if on last step
            if (step === totalSteps) {
                updateReview();
            }
        }

        // Validate current step
        function validateStep(step) {
            let isValid = true;

            if (step === 1) {
                const name = document.getElementById('name').value.trim();
                if (!name) {
                    showError('name', t.programNameRequired || 'Program name is required.');
                    isValid = false;
                } else {
                    clearError('name');
                }
            }

            if (step === 2) {
                const commissionValue = document.getElementById('commission_value').value;
                const commissionType = document.querySelector('input[name="commission_type"]:checked').value;

                if (!commissionValue || parseFloat(commissionValue) <= 0) {
                    showError('commission_value', t.validCommissionValue || 'Please enter a valid commission value.');
                    isValid = false;
                } else if (commissionType === 'percentage' && parseFloat(commissionValue) > 100) {
                    showError('commission_value', t.percentageMax100 || 'Percentage cannot exceed 100%.');
                    isValid = false;
                } else {
                    clearError('commission_value');
                }
            }

            return isValid;
        }

        function showError(field, message) {
            const errorEl = document.getElementById(`${field}-error`);
            if (errorEl) {
                errorEl.textContent = message;
                errorEl.style.display = 'block';
            }
            const input = document.getElementById(field);
            if (input) {
                input.classList.add('error');
            }
        }

        function clearError(field) {
            const errorEl = document.getElementById(`${field}-error`);
            if (errorEl) {
                errorEl.textContent = '';
                errorEl.style.display = 'none';
            }
            const input = document.getElementById(field);
            if (input) {
                input.classList.remove('error');
            }
        }

        // Navigation
        btnNext.addEventListener('click', function() {
            if (validateStep(currentStep)) {
                currentStep++;
                showStep(currentStep);
            }
        });

        btnPrev.addEventListener('click', function() {
            currentStep--;
            showStep(currentStep);
        });

        // Commission type switching
        const commissionCards = document.querySelectorAll('.commission-type-card');
        commissionCards.forEach(card => {
            card.addEventListener('click', function() {
                commissionCards.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                this.querySelector('input[type="radio"]').checked = true;
                updateCommissionUI();
            });
        });

        function updateCommissionUI() {
            const type = document.querySelector('input[name="commission_type"]:checked').value;
            const input = document.getElementById('commission_value');
            const label = document.getElementById('commission-value-label');
            const prefix = document.getElementById('commission-prefix');
            const suffix = document.getElementById('commission-suffix');
            const help = document.getElementById('commission-help');

            if (type === 'percentage') {
                label.textContent = t.commissionPercentage || 'Commission Percentage';
                prefix.style.display = 'none';
                suffix.style.display = 'inline-flex';
                suffix.textContent = '%';
                input.max = 100;
                input.placeholder = '10';
                help.textContent = t.enter0to100 || 'Enter a value between 0 and 100.';
            } else {
                label.textContent = t.commissionAmount || 'Commission Amount';
                prefix.style.display = 'inline-flex';
                suffix.style.display = 'none';
                input.removeAttribute('max');
                input.placeholder = '5.00';
                help.textContent = t.enterFixedAmount || 'Enter the fixed amount per sale.';
            }
            updateCommissionPreview();
        }

        // Commission preview
        function updateCommissionPreview() {
            const type = document.querySelector('input[name="commission_type"]:checked').value;
            const value = parseFloat(document.getElementById('commission_value').value) || 0;
            const previewEl = document.getElementById('preview-commission');

            let commission;
            if (type === 'percentage') {
                commission = (100 * value / 100).toFixed(2);
            } else {
                commission = value.toFixed(2);
            }
            previewEl.textContent = '$' + commission;
        }

        document.getElementById('commission_value').addEventListener('input', updateCommissionPreview);

        // Cookie lifetime slider
        const slider = document.getElementById('cookie_lifetime_slider');
        const cookieInput = document.getElementById('cookie_lifetime_days');

        slider.addEventListener('input', function() {
            cookieInput.value = this.value;
        });

        cookieInput.addEventListener('input', function() {
            slider.value = this.value;
        });

        // Auto-approve toggle
        const autoApproveCheckbox = document.getElementById('auto_approve_affiliates');
        const approvalMessage = document.getElementById('approval-message');

        autoApproveCheckbox.addEventListener('change', function() {
            if (this.checked) {
                approvalMessage.textContent = t.autoApproveOn || 'New affiliates will be automatically approved.';
            } else {
                approvalMessage.textContent = t.autoApproveOff || 'You will manually review and approve each affiliate application.';
            }
        });

        // Update review summary
        function updateReview() {
            document.getElementById('review-name').textContent = document.getElementById('name').value || '-';

            const status = document.getElementById('status').value;
            const statusText = status === 'active' ? (t.active || 'Active') : (t.paused || 'Paused');
            document.getElementById('review-status').textContent = statusText;

            const commissionType = document.querySelector('input[name="commission_type"]:checked').value;
            const commissionTypeText = commissionType === 'percentage' ? (t.percentage || 'Percentage') : (t.fixedAmount || 'Fixed Amount');
            document.getElementById('review-commission-type').textContent = commissionTypeText;

            const commissionValue = document.getElementById('commission_value').value;
            const commissionDisplay = commissionType === 'percentage' ? commissionValue + '%' : '$' + commissionValue;
            document.getElementById('review-commission-value').textContent = commissionDisplay;

            document.getElementById('review-cookie').textContent = document.getElementById('cookie_lifetime_days').value + ' ' + (t.days || 'days');

            const autoApprove = document.getElementById('auto_approve_affiliates').checked;
            document.getElementById('review-auto-approve').textContent = autoApprove ? (t.yes || 'Yes') : (t.no || 'No');

            document.getElementById('review-min-payout').textContent = '$' + document.getElementById('minimum_payout').value;
        }

        // Form submission
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(form);

            btnCreate.disabled = true;
            btnCreate.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + (t.creating || 'Creating...');

            fetch(form.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = data.redirect_url;
                } else {
                    btnCreate.disabled = false;
                    btnCreate.innerHTML = '<i class="fas fa-check"></i> ' + (t.createProgram || 'Create Program');

                    const errorsDiv = document.getElementById('form-errors');
                    const errorsMsg = document.getElementById('form-errors-message');

                    if (data.errors) {
                        const errorMessages = Object.values(data.errors).join('<br>');
                        errorsMsg.innerHTML = errorMessages;
                        errorsDiv.style.display = 'flex';
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                btnCreate.disabled = false;
                btnCreate.innerHTML = '<i class="fas fa-check"></i> ' + (t.createProgram || 'Create Program');

                const errorsDiv = document.getElementById('form-errors');
                const errorsMsg = document.getElementById('form-errors-message');
                errorsMsg.textContent = t.errorOccurred || 'An error occurred. Please try again.';
                errorsDiv.style.display = 'flex';
            });
        });

        // Auto-generate slug from name
        document.getElementById('name').addEventListener('blur', function() {
            const slugField = document.getElementById('slug');
            if (!slugField.value) {
                const slug = this.value
                    .toLowerCase()
                    .replace(/[^\w\s-]/g, '')
                    .replace(/\s+/g, '-')
                    .replace(/-+/g, '-')
                    .trim();
                slugField.value = slug;
            }
        });

        // Initialize
        showStep(1);
        updateCommissionUI();
    });

})();
