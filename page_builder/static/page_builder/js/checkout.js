/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Checkout Module
 *
 * Single-page accordion checkout flow with multi-provider payment support.
 * Steps: Contact → Shipping Address → Shipping Method → Payment → Review & Place Order
 */
(function() {
    'use strict';

    const Checkout = {
        // API endpoints (no language prefix)
        endpoints: {
            cart: '/api/cart/',
            session: '/api/checkout/',
            shippingAddress: '/api/checkout/shipping-address/',
            billingAddress: '/api/checkout/billing-address/',
            shippingMethods: '/api/checkout/shipping-methods/',
            shippingMethod: '/api/checkout/shipping-method/',
            paymentProviders: '/api/checkout/payment-providers/',
            paymentMethod: '/api/checkout/payment-method/',
            validate: '/api/checkout/validate/',
            complete: '/api/checkout/complete/',
            createIntent: '/api/payments/intents/',
            intentDetail: '/api/payments/intents/',
        },

        // State
        config: {},
        cartData: null,
        sessionData: null,
        selectedShippingMethod: null,
        selectedProvider: null,
        steps: ['contact', 'shipping', 'shipping-method', 'payment', 'review'],
        completedSteps: new Set(),

        init() {
            // Read config from JSON script tag
            const configElement = document.getElementById('checkout-config');
            this.config = configElement ? JSON.parse(configElement.textContent) : {};
            // Add lang from document
            this.config.lang = document.documentElement.lang || 'en';

            this.cacheElements();
            this.bindEvents();
            this.initAccountCreationUI();
            this.loadCheckout();
        },

        cacheElements() {
            this.els = {
                steps: document.getElementById('checkout-steps'),
                loading: document.getElementById('checkout-loading'),
                // Summaries
                contactSummary: document.getElementById('contact-summary'),
                shippingSummary: document.getElementById('shipping-summary'),
                shippingMethodSummary: document.getElementById('shipping-method-summary'),
                paymentSummary: document.getElementById('payment-summary'),
                // Order summary sidebar
                summaryItems: document.getElementById('summary-items'),
                summarySubtotal: document.getElementById('summary-subtotal'),
                summaryShipping: document.getElementById('summary-shipping'),
                summaryShippingRow: document.getElementById('summary-shipping-row'),
                summaryDiscount: document.getElementById('summary-discount'),
                summaryDiscountRow: document.getElementById('summary-discount-row'),
                summaryTax: document.getElementById('summary-tax'),
                summaryTaxRow: document.getElementById('summary-tax-row'),
                summaryTotal: document.getElementById('summary-total'),
                // Shipping methods
                shippingMethodsList: document.getElementById('shipping-methods-list'),
                // Payment
                paymentProvidersList: document.getElementById('payment-providers-list'),
                billingSameAsShipping: document.getElementById('billing-same-as-shipping'),
                billingForm: document.getElementById('billing-address-form'),
                // Review
                reviewContact: document.getElementById('review-contact'),
                reviewShipping: document.getElementById('review-shipping'),
                reviewShippingMethod: document.getElementById('review-shipping-method'),
                reviewPayment: document.getElementById('review-payment'),
                reviewItems: document.getElementById('review-items'),
                // Review totals
                reviewSubtotal: document.getElementById('review-subtotal'),
                reviewShippingCost: document.getElementById('review-shipping-cost'),
                reviewDiscount: document.getElementById('review-discount'),
                reviewDiscountRow: document.getElementById('review-discount-row'),
                reviewTax: document.getElementById('review-tax'),
                reviewTaxRow: document.getElementById('review-tax-row'),
                reviewTotal: document.getElementById('review-total'),
            };
        },

        bindEvents() {
            // Step header clicks for navigation
            document.querySelectorAll('.checkout-step__header').forEach(header => {
                header.addEventListener('click', () => {
                    const step = header.closest('.checkout-step');
                    const stepName = step.dataset.step;
                    if (this.completedSteps.has(stepName) || step.classList.contains('checkout-step--active')) {
                        this.openStep(stepName);
                        if (stepName === 'shipping-method') this.fetchShippingMethods();
                        if (stepName === 'payment') this.fetchPaymentProviders();
                    }
                });
                header.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        header.click();
                    }
                });
            });

            // Listen for mini-cart changes (item removed/quantity changed)
            document.addEventListener('cart:updated', (e) => {
                this.handleCartUpdate(e.detail);
            });

            // Continue buttons and express checkout
            document.querySelectorAll('[data-action]').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const action = e.currentTarget.dataset.action;
                    switch (action) {
                        case 'continue-contact': this.submitContact(); break;
                        case 'continue-shipping': this.submitShippingAddress(); break;
                        case 'continue-shipping-method': this.submitShippingMethod(); break;
                        case 'continue-payment': this.submitPaymentMethod(); break;
                        case 'express-checkout':
                            const provider = e.currentTarget.dataset.provider;
                            const method = e.currentTarget.dataset.method;
                            if (provider && method) {
                                this.expressCheckout(provider, method);
                            }
                            break;
                    }
                });
            });

            // New address toggle
            const toggle = document.getElementById('new-address-toggle');
            if (toggle) {
                toggle.addEventListener('click', () => {
                    const form = document.getElementById('new-address-form');
                    const savedAddresses = document.getElementById('saved-addresses');
                    if (form.hidden) {
                        form.hidden = false;
                        toggle.innerHTML = '<i class="fas fa-arrow-left"></i> Use saved address';
                        // Deselect saved addresses
                        savedAddresses.querySelectorAll('input[type="radio"]').forEach(r => {
                            r.checked = false;
                            r.closest('.saved-address-card').classList.remove('saved-address-card--selected');
                        });
                    } else {
                        form.hidden = true;
                        toggle.innerHTML = '<i class="fas fa-plus"></i> Use a different address';
                    }
                });
            }

            // Saved address selection styling
            document.querySelectorAll('.saved-address-card input[type="radio"]').forEach(radio => {
                radio.addEventListener('change', () => {
                    document.querySelectorAll('.saved-address-card').forEach(card => {
                        card.classList.toggle('saved-address-card--selected', card.querySelector('input').checked);
                    });
                    // Hide new address form
                    const form = document.getElementById('new-address-form');
                    if (form) form.hidden = true;
                    const toggleBtn = document.getElementById('new-address-toggle');
                    if (toggleBtn) toggleBtn.innerHTML = '<i class="fas fa-plus"></i> Use a different address';
                });
            });

            // Billing toggle
            if (this.els.billingSameAsShipping) {
                this.els.billingSameAsShipping.addEventListener('change', () => {
                    this.els.billingForm.hidden = this.els.billingSameAsShipping.checked;
                });
            }
        },

        initAccountCreationUI() {
            // Handle account creation UI based on timing mode
            const accountTiming = this.config.accountCreationTiming || 'post_purchase';

            if (accountTiming === 'during_checkout') {
                // Toggle password field when checkbox changes
                const checkbox = document.getElementById('create-account-checkbox');
                const accountFields = document.getElementById('account-fields');
                const passwordInput = document.getElementById('checkout-password');

                if (checkbox && accountFields) {
                    checkbox.addEventListener('change', (e) => {
                        accountFields.hidden = !e.target.checked;
                        if (passwordInput) {
                            passwordInput.required = e.target.checked;
                        }
                    });
                }
            }
        },

        async loadCheckout() {
            this.showLoading(true);
            try {
                // Fetch cart and checkout session in parallel
                const [cartResp, sessionResp] = await Promise.all([
                    this.api(this.endpoints.cart),
                    this.api(this.endpoints.session),
                ]);
                this.cartData = cartResp;
                this.sessionData = sessionResp.session || sessionResp;
                this.renderSummary();
                this.initAddressAutocomplete();

                // Restore form fields from session data
                this.restoreFormFields();

                // Resume from last completed step if session has data
                if (this.sessionData.shipping_address || this.sessionData.shipping_address_data) {
                    this.completedSteps.add('contact');
                    this.completedSteps.add('shipping');
                    this.updateStepUI('contact', 'completed');
                    this.updateStepUI('shipping', 'completed');
                    this.updateSummaryText('contact', this.config.userEmail);
                    this.updateShippingSummary();

                    // Always fetch shipping methods when address exists so they
                    // are available on page reload (especially for single-page
                    // checkout where all sections are visible at once)
                    this.fetchShippingMethods();

                    if (this.sessionData.selected_shipping_method) {
                        this.completedSteps.add('shipping-method');
                        this.updateStepUI('shipping-method', 'completed');
                        this.updateShippingMethodSummary();

                        // Always fetch payment providers when shipping method
                        // is selected so they are populated on reload
                        this.fetchPaymentProviders();

                        if (this.sessionData.payment_provider) {
                            this.completedSteps.add('payment');
                            this.updateStepUI('payment', 'completed');
                            this.updateSummaryText('payment', this.sessionData.payment_provider_name || '');
                            this.openStep('review');
                            this.renderReview();

                            // Recover payment handler if we have a stored intent
                            const storedIntentId = sessionStorage.getItem('payment_intent_id');
                            if (storedIntentId) {
                                this.recoverPaymentHandler(storedIntentId);
                            }
                        } else {
                            this.openStep('payment');
                        }
                    } else {
                        this.openStep('shipping-method');
                    }
                } else {
                    // Auto-complete contact if email is pre-filled
                    if (this.config.userEmail) {
                        this.openStep('contact');
                    }
                }
            } catch (err) {
                console.error('Checkout load error:', err);
                this.showAlert('Failed to load checkout. Please try again.', 'error');
            } finally {
                this.showLoading(false);
            }
        },

        // === Step Logic ===

        openStep(stepName) {
            this.steps.forEach(name => {
                const el = document.getElementById(`step-${name}`);
                if (!el) return;
                if (name === stepName) {
                    el.classList.remove('checkout-step--disabled');
                    el.classList.add('checkout-step--active');
                    el.querySelector('.checkout-step__header').setAttribute('aria-expanded', 'true');
                } else if (this.completedSteps.has(name)) {
                    el.classList.remove('checkout-step--active', 'checkout-step--disabled');
                    el.classList.add('checkout-step--completed');
                    el.querySelector('.checkout-step__header').setAttribute('aria-expanded', 'false');
                } else {
                    el.classList.remove('checkout-step--active', 'checkout-step--completed');
                    el.classList.add('checkout-step--disabled');
                    el.querySelector('.checkout-step__header').setAttribute('aria-expanded', 'false');
                }
            });

            // Scroll to step
            const stepEl = document.getElementById(`step-${stepName}`);
            if (stepEl) {
                stepEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        },

        updateStepUI(stepName, state) {
            const el = document.getElementById(`step-${stepName}`);
            if (!el) return;
            el.classList.remove('checkout-step--active', 'checkout-step--completed', 'checkout-step--disabled');
            if (state === 'completed') {
                el.classList.add('checkout-step--completed');
            } else if (state === 'active') {
                el.classList.add('checkout-step--active');
            } else {
                el.classList.add('checkout-step--disabled');
            }
        },

        updateSummaryText(stepName, text) {
            const el = document.getElementById(`${stepName}-summary`);
            if (el) el.textContent = text || '';
        },

        // === Contact ===

        async submitContact() {
            const email = document.getElementById('checkout-email').value.trim();
            if (!email || !this.isValidEmail(email)) {
                this.showFieldError('checkout-email', 'Please enter a valid email address.');
                this.scrollToFirstError();
                return;
            }

            // Handle password field based on account creation timing
            const accountTiming = this.config.accountCreationTiming || 'post_purchase';
            const passwordInput = document.getElementById('checkout-password');
            let password = '';

            if (passwordInput && !passwordInput.hidden) {
                password = passwordInput.value.trim();

                // Validate password if required (before_checkout mode)
                if (accountTiming === 'before_checkout' && !password) {
                    this.showFieldError('checkout-password', 'Password is required to continue.');
                    this.scrollToFirstError();
                    return;
                }

                // Validate password if provided (during_checkout mode with checkbox checked)
                if (password && password.length < 8) {
                    this.showFieldError('checkout-password', 'Password must be at least 8 characters.');
                    this.scrollToFirstError();
                    return;
                }
            }

            this.clearFieldErrors();

            // Store contact info locally (will be submitted with order at completion)
            // Following e-commerce best practice: collect data client-side, submit atomically on order placement
            this.sessionData = this.sessionData || {};
            this.sessionData.email = email;
            this.sessionData.first_name = this.config.userFirstName || '';
            this.sessionData.last_name = this.config.userLastName || '';

            // Store password if provided (for account creation)
            if (password) {
                this.sessionData.password = password;
            }

            // Mark step as complete
            this.completedSteps.add('contact');
            this.updateSummaryText('contact', email);

            // Invalidate downstream steps when contact info changes
            ['shipping', 'shipping-method', 'payment', 'review'].forEach(s => {
                this.completedSteps.delete(s);
                this.updateStepUI(s, 'disabled');
                this.updateSummaryText(s, '');
            });

            // Proceed to shipping
            this.openStep('shipping');
        },

        // === Shipping Address ===

        async submitShippingAddress() {
            this.showLoading(true);
            try {
                let body;
                const savedRadio = document.querySelector('input[name="saved_address"]:checked');
                const newForm = document.getElementById('new-address-form');

                if (savedRadio && newForm.hidden) {
                    body = { address_id: parseInt(savedRadio.value, 10) };
                } else {
                    // Validate required fields
                    const fields = {
                        name: document.getElementById('shipping-name').value.trim(),
                        address1: document.getElementById('shipping-address1').value.trim(),
                        city: document.getElementById('shipping-city').value.trim(),
                        state: document.getElementById('shipping-state').value.trim(),
                        postal_code: document.getElementById('shipping-postal-code').value.trim(),
                        country: document.getElementById('shipping-country').value.trim(),
                    };

                    const missing = Object.entries(fields).filter(([, v]) => !v);
                    if (missing.length > 0) {
                        missing.forEach(([key]) => {
                            this.showFieldError(`shipping-${key.replace('_', '-')}`, 'This field is required.');
                        });
                        this.scrollToFirstError();
                        return;
                    }

                    body = {
                        ...fields,
                        company: document.getElementById('shipping-company').value.trim(),
                        address2: document.getElementById('shipping-address2').value.trim(),
                        phone: document.getElementById('shipping-phone').value.trim(),
                    };
                }

                // Include email with shipping address (for guest checkout email persistence)
                const emailField = document.getElementById('checkout-email');
                const email = (this.sessionData && this.sessionData.email) ||
                             (emailField && emailField.value.trim()) ||
                             this.config.userEmail || '';
                if (email) {
                    body.email = email;
                }

                this.clearFieldErrors();
                const resp = await this.api(this.endpoints.shippingAddress, 'POST', body);

                if (resp.success) {
                    this.sessionData = resp.session;
                    this.completedSteps.add('shipping');
                    // Invalidate downstream steps (backend cleared shipping method)
                    ['shipping-method', 'payment', 'review'].forEach(s => {
                        this.completedSteps.delete(s);
                        this.updateStepUI(s, 'disabled');
                        this.updateSummaryText(s, '');
                    });
                    this.selectedShippingMethod = null;
                    this.updateShippingSummary();
                    this.renderSummary();
                    this.openStep('shipping-method');
                    this.fetchShippingMethods();
                } else {
                    this.showAlert(resp.message || 'Failed to set shipping address.', 'error');
                }
            } catch (err) {
                console.error('Shipping address error:', err);
                this.showAlert('Failed to save address. Please try again.', 'error');
            } finally {
                this.showLoading(false);
            }
        },

        updateShippingSummary() {
            if (!this.sessionData || !this.sessionData.shipping_address) return;
            const addr = this.sessionData.shipping_address;
            const text = addr.city ? `${addr.city}, ${addr.country || addr.state}` : '';
            this.updateSummaryText('shipping', text);
        },

        // === Shipping Methods ===

        async fetchShippingMethods() {
            const container = this.els.shippingMethodsList;
            container.innerHTML = '<div class="checkout-empty-state"><i class="fas fa-spinner fa-spin"></i><p>Loading shipping methods...</p></div>';

            try {
                const resp = await this.api(this.endpoints.shippingMethods);
                const methods = resp.shipping_methods || [];

                if (methods.length === 0) {
                    container.innerHTML = `
                        <div class="checkout-empty-state">
                            <i class="fas fa-exclamation-circle"></i>
                            <p><strong>No shipping methods available for this address.</strong></p>
                            <p style="font-size: 0.875rem; color: var(--theme-color-text-muted, #6b7280); margin-top: 0.5rem;">
                                Please try a different shipping address or contact us for assistance.
                            </p>
                        </div>
                    `;
                    // Disable the continue button
                    const continueBtn = document.querySelector('[data-action="continue-shipping-method"]');
                    if (continueBtn) {
                        continueBtn.disabled = true;
                        continueBtn.style.opacity = '0.5';
                        continueBtn.style.cursor = 'not-allowed';
                    }
                    return;
                }

                container.innerHTML = methods.map(m => `
                    <label class="shipping-method-card" data-method-id="${this.escAttr(m.id)}">
                        <input type="radio" name="shipping_method" value="${this.escAttr(m.id)}">
                        <div class="shipping-method-card__info">
                            <div class="shipping-method-card__name">${this.esc(m.name)}</div>
                            <div class="shipping-method-card__desc">${this.esc(m.estimated_delivery || m.description || '')}</div>
                        </div>
                        <div class="shipping-method-card__price">
                            ${parseFloat(m.final_cost) === 0 ? 'Free' : this.formatCurrency(m.final_cost)}
                        </div>
                    </label>
                `).join('');

                // Re-enable the continue button (in case it was disabled before)
                const continueBtn = document.querySelector('[data-action="continue-shipping-method"]');
                if (continueBtn) {
                    continueBtn.disabled = false;
                    continueBtn.style.opacity = '';
                    continueBtn.style.cursor = '';
                }

                // Bind selection styling
                container.querySelectorAll('.shipping-method-card').forEach(card => {
                    card.querySelector('input').addEventListener('change', () => {
                        container.querySelectorAll('.shipping-method-card').forEach(c => {
                            c.classList.toggle('shipping-method-card--selected', c.querySelector('input').checked);
                        });
                    });
                });

                // Auto-select first if session has one or default to first
                if (this.sessionData && this.sessionData.selected_shipping_method) {
                    const radio = container.querySelector(`input[value="${this.sessionData.selected_shipping_method?.id || this.sessionData.selected_shipping_method}"]`);
                    if (radio) {
                        radio.checked = true;
                        radio.closest('.shipping-method-card').classList.add('shipping-method-card--selected');
                    }
                } else if (methods.length === 1) {
                    const radio = container.querySelector('input[type="radio"]');
                    if (radio) {
                        radio.checked = true;
                        radio.closest('.shipping-method-card').classList.add('shipping-method-card--selected');
                    }
                }
            } catch (err) {
                console.error('Shipping methods error:', err);
                container.innerHTML = '<div class="checkout-empty-state"><i class="fas fa-exclamation-triangle"></i><p>Failed to load shipping methods.</p></div>';
            }
        },

        async submitShippingMethod() {
            const selected = document.querySelector('input[name="shipping_method"]:checked');
            if (!selected) {
                this.showAlert('Please select a shipping method.', 'error');
                return;
            }

            this.showLoading(true);
            try {
                const resp = await this.api(this.endpoints.shippingMethod, 'POST', {
                    shipping_method_id: parseInt(selected.value, 10)
                });

                if (resp.success) {
                    this.sessionData = resp.session;
                    this.selectedShippingMethod = selected.closest('.shipping-method-card');
                    this.completedSteps.add('shipping-method');
                    // Invalidate downstream steps
                    ['payment', 'review'].forEach(s => {
                        this.completedSteps.delete(s);
                        this.updateStepUI(s, 'disabled');
                        this.updateSummaryText(s, '');
                    });
                    this.updateShippingMethodSummary();
                    this.renderSummary();
                    this.openStep('payment');
                    this.fetchPaymentProviders();
                } else {
                    this.showAlert(resp.message || 'Failed to set shipping method.', 'error');
                }
            } catch (err) {
                console.error('Shipping method error:', err);
                this.showAlert('Failed to save shipping method. Please try again.', 'error');
            } finally {
                this.showLoading(false);
            }
        },

        updateShippingMethodSummary() {
            if (!this.selectedShippingMethod) {
                const sel = document.querySelector('input[name="shipping_method"]:checked');
                if (sel) this.selectedShippingMethod = sel.closest('.shipping-method-card');
            }
            if (this.selectedShippingMethod) {
                const name = this.selectedShippingMethod.querySelector('.shipping-method-card__name');
                this.updateSummaryText('shipping-method', name ? name.textContent : '');
            } else if (this.sessionData?.selected_shipping_method?.name) {
                this.updateSummaryText('shipping-method', this.sessionData.selected_shipping_method.name);
            }
        },

        // === Payment Providers ===

        async fetchPaymentProviders() {
            const container = this.els.paymentProvidersList;
            container.innerHTML = '<div class="checkout-empty-state"><i class="fas fa-spinner fa-spin"></i><p>Loading payment methods...</p></div>';

            try {
                const resp = await this.api(this.endpoints.paymentProviders);
                const providers = resp.payment_providers || [];

                if (providers.length === 0) {
                    container.innerHTML = '<div class="checkout-empty-state"><i class="fas fa-credit-card"></i><p>No payment methods available.</p></div>';
                    return;
                }

                container.innerHTML = providers.map(p => `
                    <label class="payment-provider-card" data-provider-id="${this.escAttr(p.id)}">
                        <input type="radio" name="payment_provider" value="${this.escAttr(p.id)}">
                        <div class="payment-provider-card__info">
                            <div class="payment-provider-card__name">${this.esc(p.display_name || p.provider_name)}</div>
                            <div class="payment-provider-card__methods">
                                ${(p.available_methods || []).map(m => this.paymentMethodBadge(m)).join('')}
                            </div>
                        </div>
                    </label>
                `).join('');

                // Bind selection styling
                container.querySelectorAll('.payment-provider-card').forEach(card => {
                    card.querySelector('input').addEventListener('change', () => {
                        container.querySelectorAll('.payment-provider-card').forEach(c => {
                            c.classList.toggle('payment-provider-card--selected', c.querySelector('input').checked);
                        });
                    });
                });

                // Auto-select if only one provider
                if (providers.length === 1) {
                    const radio = container.querySelector('input[type="radio"]');
                    if (radio) {
                        radio.checked = true;
                        radio.closest('.payment-provider-card').classList.add('payment-provider-card--selected');
                    }
                }
            } catch (err) {
                console.error('Payment providers error:', err);
                container.innerHTML = '<div class="checkout-empty-state"><i class="fas fa-exclamation-triangle"></i><p>Failed to load payment methods.</p></div>';
            }
        },

        async submitPaymentMethod() {
            const selected = document.querySelector('input[name="payment_provider"]:checked');
            if (!selected) {
                this.showAlert('Please select a payment method.', 'error');
                return;
            }

            this.showLoading(true);
            try {
                // 1. Submit payment provider selection
                const resp = await this.api(this.endpoints.paymentMethod, 'POST', {
                    payment_provider_id: selected.value
                });

                if (!resp.success) {
                    this.showAlert(resp.message || 'Failed to set payment method.', 'error');
                    return;
                }

                this.sessionData = resp.session;
                this.selectedProvider = selected.closest('.payment-provider-card');

                // 2. Create payment intent immediately (NEW FLOW)
                await this.createPaymentIntent();

            } catch (err) {
                console.error('Payment method error:', err);
                this.showAlert('Failed to save payment method. Please try again.', 'error');
            } finally {
                this.showLoading(false);
            }
        },

        async createPaymentIntent() {
            try {
                // 1. Set billing address
                const billingSame = this.els.billingSameAsShipping?.checked !== false;
                const billingBody = billingSame
                    ? { same_as_shipping: true }
                    : {
                        same_as_shipping: false,
                        name: document.getElementById('billing-name')?.value.trim() || '',
                        company: document.getElementById('billing-company')?.value.trim() || '',
                        address1: document.getElementById('billing-address1')?.value.trim() || '',
                        address2: document.getElementById('billing-address2')?.value.trim() || '',
                        city: document.getElementById('billing-city')?.value.trim() || '',
                        state: document.getElementById('billing-state')?.value.trim() || '',
                        postal_code: document.getElementById('billing-postal-code')?.value.trim() || '',
                        country: document.getElementById('billing-country')?.value.trim() || '',
                        phone: document.getElementById('billing-phone')?.value.trim() || '',
                    };

                const billingResp = await this.api(this.endpoints.billingAddress, 'POST', billingBody);
                if (!billingResp.success) {
                    this.showAlert(billingResp.message || 'Failed to set billing address.', 'error');
                    return;
                }
                this.sessionData = billingResp.session;

                // 2. Validate checkout
                const validation = await this.api(this.endpoints.validate, 'POST');
                if (!validation.is_valid) {
                    const errorMsg = (validation.errors || []).join('. ') || 'Checkout validation failed.';
                    this.showAlert(errorMsg, 'error');
                    return;
                }

                // 3. Create payment intent
                const lang = this.config.lang || document.documentElement.lang || 'en';
                const origin = window.location.origin;
                const emailField = document.getElementById('checkout-email');
                const email = (this.sessionData && this.sessionData.email) ||
                             (emailField && emailField.value.trim()) ||
                             this.config.userEmail || '';

                const intentResp = await this.api(this.endpoints.createIntent, 'POST', {
                    return_url: `${origin}/${lang}/checkout/return/`,
                    cancel_url: `${origin}/${lang}/checkout/`,
                    metadata: { email: email }
                });

                if (!intentResp.success) {
                    this.showAlert(intentResp.message || 'Failed to create payment. Please try again.', 'error');
                    return;
                }

                // 4. Mark payment step complete
                this.completedSteps.add('payment');
                const providerName = this.selectedProvider?.querySelector('.payment-provider-card__name')?.textContent || '';
                this.updateSummaryText('payment', providerName);

                // 5. Render review and advance to review step
                this.renderSummary();
                this.renderReview();
                this.openStep('review');

                // 6. Route payment based on checkout type
                console.log('[Checkout] Payment intent response:', intentResp);

                if (intentResp.checkout_url) {
                    // HOSTED: Redirect to provider's checkout page
                    console.log('[Checkout] Routing to hosted checkout');
                    sessionStorage.setItem('payment_intent_id', intentResp.intent_id);
                    sessionStorage.setItem('order_number', intentResp.order_number);
                    window.location.href = intentResp.checkout_url;
                } else if (intentResp.handler_url) {
                    // PLUGIN HANDLER: Load provider's checkout handler in review step
                    console.log('[Checkout] Routing to plugin handler:', intentResp.handler_url);
                    sessionStorage.setItem('payment_intent_id', intentResp.intent_id);
                    sessionStorage.setItem('order_number', intentResp.order_number);
                    await this.initPluginHandlerInReview(intentResp);
                } else if (intentResp.client_secret) {
                    // LEGACY EMBEDDED: Direct embedded payment
                    console.log('[Checkout] Routing to legacy embedded');
                    this.initEmbeddedPaymentInReview(intentResp);
                } else {
                    // OFFLINE (COD, bank transfer): Order created, go to confirmation
                    console.log('[Checkout] Routing to confirmation (offline payment)');
                    sessionStorage.removeItem('payment_intent_id');
                    sessionStorage.removeItem('order_number');
                    window.location.href = `/${lang}/checkout/confirmation/${intentResp.order_number}/`;
                }

            } catch (err) {
                console.error('Create payment intent error:', err);
                this.showAlert(err.message || 'Something went wrong. Please try again.', 'error');
            }
        },

        // === Review & Place Order ===

        renderReview() {
            // Contact
            const emailEl = document.getElementById('checkout-email');
            const email = (emailEl && emailEl.value.trim()) || this.config.userEmail || '';
            if (this.els.reviewContact) {
                this.els.reviewContact.textContent = email;
            }

            // Shipping address
            if (this.els.reviewShipping && this.sessionData && this.sessionData.shipping_address) {
                const addr = this.sessionData.shipping_address;
                // Clear previous content
                this.els.reviewShipping.textContent = '';
                // Build address lines safely using DOM elements
                const lines = [
                    addr.name,
                    addr.address1,
                    addr.address2,
                    `${addr.city}, ${addr.state} ${addr.postal_code}`,
                    addr.country,
                    addr.phone ? `Phone: ${addr.phone}` : ''
                ].filter(Boolean);

                lines.forEach((line, index) => {
                    const p = document.createElement('p');
                    p.textContent = line; // Auto-escaped, XSS-safe
                    p.style.margin = '0';
                    this.els.reviewShipping.appendChild(p);
                });
            }

            // Shipping method
            if (this.els.reviewShippingMethod) {
                const sel = document.querySelector('input[name="shipping_method"]:checked');
                if (sel) {
                    const card = sel.closest('.shipping-method-card');
                    const name = card.querySelector('.shipping-method-card__name')?.textContent || '';
                    const price = card.querySelector('.shipping-method-card__price')?.textContent || '';
                    this.els.reviewShippingMethod.textContent = `${name} — ${price}`;
                } else if (this.sessionData?.selected_shipping_method) {
                    const sm = this.sessionData.selected_shipping_method;
                    this.els.reviewShippingMethod.textContent = `${sm.name} — ${this.formatCurrency(this.sessionData.shipping_cost || sm.flat_rate_cost)}`;
                }
            }

            // Payment
            if (this.els.reviewPayment) {
                const sel = document.querySelector('input[name="payment_provider"]:checked');
                if (sel) {
                    const card = sel.closest('.payment-provider-card');
                    const name = card.querySelector('.payment-provider-card__name')?.textContent || '';
                    this.els.reviewPayment.textContent = name;
                } else if (this.sessionData?.payment_provider_name) {
                    this.els.reviewPayment.textContent = this.sessionData.payment_provider_name;
                }
            }

            // Items
            if (this.els.reviewItems && this.cartData) {
                const items = this.cartData.items || [];
                this.els.reviewItems.innerHTML = items.map(item => {
                    const product = item.product || {};
                    const name = product.name || 'Product';
                    const imageUrl = (product.images && product.images.length > 0)
                        ? (product.images[0].thumbnail_url || product.images[0].image_url || product.images[0].url || '')
                        : '/static/img/placeholder-product-thumb.png';
                    return `
                        <div class="review-item">
                            ${imageUrl ? `<img src="${this.escAttr(imageUrl)}" alt="${this.escAttr(name)}" class="review-item__image">` : ''}
                            <div class="review-item__info">
                                <div class="review-item__name">${this.esc(name)}</div>
                                <div class="review-item__qty">Qty: ${item.quantity}</div>
                            </div>
                            <div class="review-item__price">${this.formatCurrency(item.total_price)}</div>
                        </div>
                    `;
                }).join('');
            }

            // Order totals (mirrors renderSummary logic)
            const session = this.sessionData || {};
            const subtotal = this.cartData.total_amount || session.subtotal || '0.00';
            const discount = this.cartData.voucher_discount_amount || session.discount_amount || '0.00';
            const shipping = session.shipping_cost;
            const tax = session.tax_amount || '0.00';
            const sessionHasTotal = session.total_amount && parseFloat(session.total_amount) > 0;
            const total = sessionHasTotal ? session.total_amount : (this.cartData.final_amount || subtotal);

            if (this.els.reviewSubtotal) this.els.reviewSubtotal.textContent = this.formatCurrency(subtotal);
            if (this.els.reviewTotal) this.els.reviewTotal.textContent = this.formatCurrency(total);

            // Shipping
            if (this.els.reviewShippingCost) {
                if (shipping !== null && shipping !== undefined) {
                    this.els.reviewShippingCost.textContent = parseFloat(shipping) === 0 ? 'Free' : this.formatCurrency(shipping);
                } else {
                    this.els.reviewShippingCost.textContent = '\u2014';
                }
            }

            // Discount (conditionally shown)
            if (this.els.reviewDiscountRow) {
                if (parseFloat(discount) > 0) {
                    this.els.reviewDiscountRow.hidden = false;
                    if (this.els.reviewDiscount) this.els.reviewDiscount.textContent = '-' + this.formatCurrency(discount);
                } else {
                    this.els.reviewDiscountRow.hidden = true;
                }
            }

            // Tax (conditionally shown)
            if (this.els.reviewTaxRow) {
                if (parseFloat(tax) > 0) {
                    this.els.reviewTaxRow.hidden = false;
                    if (this.els.reviewTax) this.els.reviewTax.textContent = this.formatCurrency(tax);
                } else {
                    this.els.reviewTaxRow.hidden = true;
                }
            }
        },

        // === Express Checkout ===

        expressCheckout(providerSlug, methodSlug) {
            const csrfToken = this.getCsrfToken();

            // Show loading state
            this.showAlert('Initializing express checkout...', 'info');

            // Build the express checkout URL dynamically based on provider
            const expressCheckoutUrl = `/api/payment/providers/${providerSlug}/express-checkout/`;

            // Initiate express checkout session
            fetch(expressCheckoutUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({
                    method: methodSlug,
                    cart_token: this.getCookie('cart_token') || null
                })
            })
            .then(response => {
                // Handle 404 gracefully - express checkout not yet implemented for this provider
                if (response.status === 404) {
                    // Fallback to standard checkout
                    this.showAlert('Redirecting to checkout...', 'info');
                    window.location.href = '/checkout/';
                    return null;
                }
                return response.json();
            })
            .then(data => {
                if (!data) return; // Already handled 404 redirect

                if (data.success) {
                    // Handle based on checkout type
                    if (data.redirect_url) {
                        // Redirect to hosted checkout
                        window.location.href = data.redirect_url;
                    } else if (data.client_secret) {
                        // Integrated checkout - init payment sheet
                        this.initPaymentSheet(providerSlug, methodSlug, data);
                    }
                } else {
                    this.showAlert(data.message || 'Express checkout failed', 'error');
                }
            })
            .catch(error => {
                console.error('Express checkout error:', error);
                // Fallback to standard checkout on error
                this.showAlert('Redirecting to checkout...', 'info');
                window.location.href = '/checkout/';
            });
        },

        initPaymentSheet(providerSlug, methodSlug, data) {
            // Provider-specific payment sheet initialization
            // This would integrate with payment provider SDKs (Stripe, PayPal, etc.)
            console.log('Payment sheet init:', providerSlug, methodSlug, data);
            this.showAlert('Payment sheet initialization not yet implemented', 'error');
        },

        getCookie(name) {
            const value = `; ${document.cookie}`;
            const parts = value.split(`; ${name}=`);
            if (parts.length === 2) return parts.pop().split(';').shift();
            return null;
        },

        // === Embedded Payment ===

        initEmbeddedPayment(intentData) {
            const container = document.getElementById('embedded-payment-container');
            if (!container) return;

            // Show a message for embedded payment - provider SDK integration point
            container.innerHTML = `
                <div class="checkout-alert checkout-alert--info">
                    <p>Embedded payment for this provider is being processed. If you are not redirected automatically, please wait...</p>
                </div>
            `;

            // Provider-specific SDK loading would go here.
            // For now, check if the intent already succeeded (some offline providers)
            // or poll for completion.
            if (intentData.status === 'succeeded' && intentData.order_number) {
                const lang = this.config.lang || 'en';
                window.location.href = `/${lang}/checkout/confirmation/${intentData.order_number}/`;
                return;
            }

            // Start polling for intent completion
            this.pollIntentStatus(intentData.intent_id, intentData.order_number);
        },

        async pollIntentStatus(intentId, orderNumber) {
            const maxAttempts = 30;
            let attempt = 0;

            const poll = async () => {
                attempt++;
                try {
                    const resp = await this.api(`${this.endpoints.intentDetail}${intentId}/`);
                    if (resp.status === 'succeeded') {
                        const lang = this.config.lang || 'en';
                        const num = resp.order_number || orderNumber;
                        window.location.href = `/${lang}/checkout/confirmation/${num}/`;
                        return;
                    }
                    if (resp.status === 'failed' || resp.status === 'canceled') {
                        this.showAlert('Payment was not completed. Please try a different payment method.', 'error');
                        this.showLoading(false);
                        return;
                    }
                } catch (err) {
                    console.error('Poll error:', err);
                }

                if (attempt < maxAttempts) {
                    setTimeout(poll, 2000);
                } else {
                    this.showAlert('Payment is still processing. You will receive an email confirmation once complete.', 'info');
                    this.showLoading(false);
                }
            };

            poll();
        },

        /**
         * Initialize payment using provider's plugin handler
         * @param {object} intentData - Payment intent response with handler info
         */
        async initPluginHandler(intentData) {
            console.log('[Plugin Handler] Initializing with data:', intentData);
            try {
                // Navigate back to payment step and make it visible
                const paymentStepEl = document.querySelector('[data-step="payment"]');
                if (paymentStepEl) {
                    // Collapse all other steps
                    document.querySelectorAll('.checkout-step').forEach(step => {
                        step.classList.remove('checkout-step--active');
                    });

                    // Activate payment step
                    paymentStepEl.classList.remove('checkout-step--disabled');
                    paymentStepEl.classList.add('checkout-step--active');

                    // Scroll into view
                    paymentStepEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }

                // Load SDK dependencies first
                if (intentData.sdk_dependencies && intentData.sdk_dependencies.length > 0) {
                    console.log('[Plugin Handler] Loading SDK dependencies:', intentData.sdk_dependencies);
                    for (const sdkUrl of intentData.sdk_dependencies) {
                        await this.loadScript(sdkUrl);
                        console.log('[Plugin Handler] Loaded SDK:', sdkUrl);
                    }
                    // Note: Handler is responsible for waiting for SDK readiness
                }

                // Load provider's handler
                console.log('[Plugin Handler] Loading handler script:', intentData.handler_url);
                await this.loadScript(intentData.handler_url);
                console.log('[Plugin Handler] Handler script loaded');

                // Get handler from global registry
                const providerKey = intentData.provider_key || 'unknown';
                console.log('[Plugin Handler] Looking for handler:', providerKey);
                console.log('[Plugin Handler] Available handlers:', Object.keys(window.PaymentHandlers || {}));
                const handler = window.PaymentHandlers?.[providerKey];

                if (!handler || typeof handler.initialize !== 'function') {
                    console.error('[Plugin Handler] Handler not found or invalid:', providerKey, handler);
                    throw new Error(`Payment handler not found for provider: ${providerKey}`);
                }

                console.log('[Plugin Handler] Found valid handler for:', providerKey);

                // Get the embedded payment container (it should exist in _step_payment.html)
                const container = document.getElementById('embedded-payment-container');
                if (!container) {
                    console.error('[Plugin Handler] embedded-payment-container not found in DOM');
                    throw new Error('Payment container not found on page');
                }

                // Clear any previous content
                container.innerHTML = '';

                // Hide payment providers list (loading spinner) since we're showing embedded form
                const paymentProvidersList = document.getElementById('payment-providers-list');
                if (paymentProvidersList) {
                    paymentProvidersList.style.display = 'none';
                }

                // Hide "Continue to Review" button since payment is handled by embedded form
                const continueButton = paymentStepEl.querySelector('[data-action="continue-payment"]');
                if (continueButton) {
                    continueButton.style.display = 'none';
                }

                // Initialize handler
                const lang = document.documentElement.lang || 'en';
                await handler.initialize(
                    intentData,
                    container,
                    // Success callback
                    (orderNumber) => {
                        sessionStorage.removeItem('payment_intent_id');
                        sessionStorage.removeItem('order_number');
                        window.location.href = `/${lang}/checkout/confirmation/${orderNumber}/`;
                    },
                    // Error callback - show persistent error in payment container
                    (errorMessage) => {
                        console.error('[Plugin Handler] Handler error callback:', errorMessage);
                        this.showPaymentError(intentData);
                        this.showLoading(false);
                    }
                );

                this.showLoading(false);
            } catch (err) {
                console.error('[Plugin Handler] Outer catch:', err);
                this.showPaymentError(intentData);
                this.showLoading(false);
            }
        },

        /**
         * Initialize payment handler in review step (NEW FLOW)
         * @param {object} intentData - Payment intent response with handler info
         */
        async initPluginHandlerInReview(intentData) {
            console.log('[Plugin Handler] Initializing in review step with data:', intentData);
            try {
                // Review step is already active at this point
                // Load SDK dependencies first
                if (intentData.sdk_dependencies && intentData.sdk_dependencies.length > 0) {
                    console.log('[Plugin Handler] Loading SDK dependencies:', intentData.sdk_dependencies);
                    for (const sdkUrl of intentData.sdk_dependencies) {
                        await this.loadScript(sdkUrl);
                        console.log('[Plugin Handler] Loaded SDK:', sdkUrl);
                    }
                }

                // Load provider's handler script
                console.log('[Plugin Handler] Loading handler script:', intentData.handler_url);
                await this.loadScript(intentData.handler_url);
                console.log('[Plugin Handler] Handler script loaded');

                // Get handler from global registry
                const providerKey = intentData.provider_key || 'unknown';
                console.log('[Plugin Handler] Looking for handler:', providerKey);
                const handler = window.PaymentHandlers?.[providerKey];

                if (!handler || typeof handler.initialize !== 'function') {
                    console.error('[Plugin Handler] Handler not found or invalid:', providerKey, handler);
                    throw new Error(`Payment handler not found for provider: ${providerKey}`);
                }

                console.log('[Plugin Handler] Found valid handler for:', providerKey);

                // Get the review payment container
                const container = document.getElementById('review-payment-container');
                if (!container) {
                    console.error('[Plugin Handler] review-payment-container not found in DOM');
                    throw new Error('Payment container not found in review step');
                }

                // Show the payment section
                const paymentSection = document.getElementById('review-payment-section');
                if (paymentSection) {
                    paymentSection.style.display = 'block';
                }

                // Clear any previous content
                container.innerHTML = '';

                // Initialize handler
                const lang = document.documentElement.lang || 'en';
                await handler.initialize(
                    intentData,
                    container,
                    // Success callback
                    (orderNumber) => {
                        sessionStorage.removeItem('payment_intent_id');
                        sessionStorage.removeItem('order_number');
                        window.location.href = `/${lang}/checkout/confirmation/${orderNumber}/`;
                    },
                    // Error callback - show persistent error in payment container
                    (errorMessage) => {
                        console.error('[Plugin Handler] Review handler error callback:', errorMessage);
                        this.showPaymentError(intentData);
                        this.showLoading(false);
                    }
                );

                this.showLoading(false);
            } catch (err) {
                console.error('[Plugin Handler] Review outer catch:', err);
                this.showPaymentError(intentData);
                this.showLoading(false);
            }
        },

        /**
         * Recover payment handler after page refresh.
         * Fetches intent data from API and re-initializes the plugin handler.
         * @param {string} intentId - Payment intent UUID from sessionStorage
         */
        async recoverPaymentHandler(intentId) {
            console.log('[Checkout] Recovering payment handler for intent:', intentId);
            try {
                const intentData = await this.api(`${this.endpoints.intentDetail}${intentId}/`);

                if (intentData.handler_url) {
                    await this.initPluginHandlerInReview(intentData);
                } else if (intentData.client_secret) {
                    this.initEmbeddedPaymentInReview(intentData);
                } else if (intentData.status === 'succeeded') {
                    // Payment already completed — redirect to confirmation
                    const lang = document.documentElement.lang || 'en';
                    const orderNumber = intentData.order_number || sessionStorage.getItem('order_number');
                    if (orderNumber) {
                        sessionStorage.removeItem('payment_intent_id');
                        sessionStorage.removeItem('order_number');
                        window.location.href = `/${lang}/checkout/confirmation/${orderNumber}/`;
                    }
                } else {
                    console.warn('[Checkout] Cannot recover handler — no handler_url or client_secret');
                    sessionStorage.removeItem('payment_intent_id');
                }
            } catch (err) {
                console.error('[Checkout] Failed to recover payment handler:', err);
                // Don't block checkout — user can re-select payment method
                sessionStorage.removeItem('payment_intent_id');
            }
        },

        /**
         * Initialize embedded payment in review step (legacy providers)
         * @param {object} intentData - Payment intent response
         */
        initEmbeddedPaymentInReview(intentData) {
            const container = document.getElementById('review-payment-container');
            if (!container) return;

            // Show the payment section
            const paymentSection = document.getElementById('review-payment-section');
            if (paymentSection) {
                paymentSection.style.display = 'block';
            }

            // Show message for embedded payment
            container.innerHTML = `
                <div class="checkout-alert checkout-alert--info">
                    <p>Processing your payment. Please wait...</p>
                </div>
            `;

            // Check if intent already succeeded (offline providers)
            if (intentData.status === 'succeeded' && intentData.order_number) {
                const lang = this.config.lang || 'en';
                window.location.href = `/${lang}/checkout/confirmation/${intentData.order_number}/`;
                return;
            }

            // Poll for intent completion (if needed)
            if (intentData.intent_id && intentData.order_number) {
                this.pollIntentStatus(intentData.intent_id, intentData.order_number);
            }
        },

        // === Cart ↔ Checkout Sync ===

        /**
         * Handle cart changes from mini-cart (item removed, quantity changed).
         * Re-fetches full cart data so prices, totals, and session stay consistent,
         * then re-renders the order summary. Redirects to cart if empty.
         */
        async handleCartUpdate(miniCartData) {
            const count = miniCartData ? (miniCartData.item_count || miniCartData.cart_count || 0) : 0;
            if (count === 0) {
                window.location.href = this.config.cartUrl || '/en/cart/';
                return;
            }
            try {
                const [cartResp, sessionResp] = await Promise.all([
                    this.api(this.endpoints.cart),
                    this.api(this.endpoints.session),
                ]);
                this.cartData = cartResp;
                this.sessionData = sessionResp.session || sessionResp;
                this.renderSummary();
                // If on review step, re-render review items too
                const activeStep = document.querySelector('.checkout-step--active');
                if (activeStep && activeStep.dataset.step === 'review') {
                    this.renderReview();
                }
            } catch (err) {
                console.error('Failed to refresh checkout after cart change:', err);
            }
        },

        // === Order Summary Sidebar ===

        renderSummary() {
            if (!this.cartData) return;
            const items = this.cartData.items || [];

            // Items
            if (this.els.summaryItems) {
                this.els.summaryItems.innerHTML = items.map(item => {
                    const product = item.product || {};
                    const name = product.name || 'Product';
                    const imageUrl = (product.images && product.images.length > 0)
                        ? (product.images[0].thumbnail_url || product.images[0].image_url || product.images[0].url || '')
                        : '/static/img/placeholder-product-thumb.png';

                    // Calculate unit price from total_price / quantity
                    const unitPrice = item.quantity > 0 ? (parseFloat(item.total_price) / item.quantity) : 0;

                    // Show unit price × quantity = total (like mini cart)
                    const priceBreakdown = item.quantity > 1
                        ? `${this.formatCurrency(unitPrice)} × ${item.quantity}`
                        : this.formatCurrency(item.total_price);

                    return `
                        <div class="checkout-summary__item">
                            ${imageUrl ? `<img src="${this.escAttr(imageUrl)}" alt="${this.escAttr(name)}" class="checkout-summary__item-image">` : ''}
                            <div class="checkout-summary__item-info">
                                <div class="checkout-summary__item-name">${this.esc(name)}</div>
                                <div class="checkout-summary__item-qty">${priceBreakdown}</div>
                            </div>
                            <div class="checkout-summary__item-price">${this.formatCurrency(item.total_price)}</div>
                        </div>
                    `;
                }).join('');
            }

            // Cart data is always live-calculated; session data adds shipping + tax
            const session = this.sessionData || {};
            const subtotal = this.cartData.total_amount || session.subtotal || '0.00';
            const discount = this.cartData.voucher_discount_amount || session.discount_amount || '0.00';
            const shipping = session.shipping_cost;
            const tax = session.tax_amount || '0.00';
            // Use session total if it includes shipping/tax, otherwise derive from cart
            const sessionHasTotal = session.total_amount && parseFloat(session.total_amount) > 0;
            const total = sessionHasTotal ? session.total_amount : (this.cartData.final_amount || subtotal);

            if (this.els.summarySubtotal) this.els.summarySubtotal.textContent = this.formatCurrency(subtotal);
            if (this.els.summaryTotal) this.els.summaryTotal.textContent = this.formatCurrency(total);

            // Shipping
            if (this.els.summaryShipping) {
                if (shipping !== null && shipping !== undefined) {
                    this.els.summaryShipping.textContent = parseFloat(shipping) === 0 ? 'Free' : this.formatCurrency(shipping);
                }
            }

            // Discount
            if (this.els.summaryDiscountRow) {
                if (parseFloat(discount) > 0) {
                    this.els.summaryDiscountRow.hidden = false;
                    if (this.els.summaryDiscount) this.els.summaryDiscount.textContent = '-' + this.formatCurrency(discount);
                } else {
                    this.els.summaryDiscountRow.hidden = true;
                }
            }

            // Tax
            if (this.els.summaryTaxRow) {
                if (parseFloat(tax) > 0) {
                    this.els.summaryTaxRow.hidden = false;
                    if (this.els.summaryTax) this.els.summaryTax.textContent = this.formatCurrency(tax);
                } else {
                    this.els.summaryTaxRow.hidden = true;
                }
            }

            // Dispatch event for mobile summary toggle
            document.dispatchEvent(new CustomEvent('checkout:summary-updated', {
                detail: { total: total }
            }));
        },

        // === Form Field Restoration ===

        restoreFormFields() {
            if (!this.sessionData) return;

            // Restore contact email from multiple sources
            const emailField = document.getElementById('checkout-email');
            if (emailField) {
                // Priority: 1) config.userEmail (logged in), 2) cart.user.email (guest user created), 3) metadata
                const email = this.config.userEmail ||
                             (this.cartData && this.cartData.user && this.cartData.user.email) ||
                             (this.sessionData.metadata && this.sessionData.metadata.email) || '';
                if (email) {
                    emailField.value = email;
                }
            }

            // Restore shipping address from shipping_address_data (JSONField)
            const shippingData = this.sessionData.shipping_address_data;
            if (shippingData) {
                this.fillAddressFields('shipping', shippingData);
            }

            // Restore billing address if different from shipping
            if (!this.sessionData.billing_same_as_shipping && this.sessionData.billing_address_data) {
                const checkbox = document.getElementById('billing-same-as-shipping');
                if (checkbox) {
                    checkbox.checked = false;
                    // Show billing form
                    const billingForm = document.getElementById('billing-address-form');
                    if (billingForm) billingForm.hidden = false;
                }
                this.fillAddressFields('billing', this.sessionData.billing_address_data);
            }
        },

        fillAddressFields(prefix, addressData) {
            if (!addressData) return;

            const fieldMap = {
                name: `${prefix}-name`,
                company: `${prefix}-company`,
                address1: `${prefix}-address1`,
                address2: `${prefix}-address2`,
                city: `${prefix}-city`,
                state: `${prefix}-state`,
                postal_code: `${prefix}-postal-code`,
                country: `${prefix}-country`,
                phone: `${prefix}-phone`
            };

            Object.entries(fieldMap).forEach(([dataKey, fieldId]) => {
                const field = document.getElementById(fieldId);
                if (field && addressData[dataKey]) {
                    field.value = addressData[dataKey];
                }
            });
        },

        // === Address Autocomplete ===

        initAddressAutocomplete() {
            if (typeof AddressAutocomplete === 'undefined') return;

            // Shipping address autocomplete
            const shippingSearch = document.getElementById('address-search');
            if (shippingSearch) {
                try {
                    new AddressAutocomplete('#address-search', {
                        apiUrl: '/api/address/autocomplete',
                        normalizeUrl: '/api/address/normalize',
                        validateUrl: '/api/address/validate',
                        fieldMapping: {
                            address1: '#shipping-address1',
                            address2: '#shipping-address2',
                            city: '#shipping-city',
                            state: '#shipping-state',
                            postal_code: '#shipping-postal-code',
                            country: '#shipping-country',
                        },
                        countryBias: this.config.geoCountry || '',
                    });
                } catch (e) {
                    console.warn('Address autocomplete init failed:', e);
                }
            }

            // Billing address autocomplete
            const billingSearch = document.getElementById('billing-address-search');
            if (billingSearch) {
                try {
                    new AddressAutocomplete('#billing-address-search', {
                        apiUrl: '/api/address/autocomplete',
                        normalizeUrl: '/api/address/normalize',
                        validateUrl: '/api/address/validate',
                        fieldMapping: {
                            address1: '#billing-address1',
                            address2: '#billing-address2',
                            city: '#billing-city',
                            state: '#billing-state',
                            postal_code: '#billing-postal-code',
                            country: '#billing-country',
                        },
                        countryBias: this.config.geoCountry || '',
                    });
                } catch (e) {
                    console.warn('Billing address autocomplete init failed:', e);
                }
            }
        },

        // === Utilities ===

        async api(url, method, body) {
            const opts = {
                method: method || 'GET',
                headers: { 'Accept': 'application/json' },
                credentials: 'same-origin',  // Include cookies for authentication
            };
            if (body) {
                opts.headers['Content-Type'] = 'application/json';
                opts.headers['X-CSRFToken'] = this.getCsrfToken();
                opts.body = JSON.stringify(body);
            }
            if (method && method !== 'GET') {
                opts.headers['X-CSRFToken'] = this.getCsrfToken();
            }
            const response = await fetch(url, opts);
            if (!response.ok) {
                let data;
                try { data = await response.json(); } catch { data = {}; }
                if (data.message || data.detail) {
                    throw new Error(data.message || data.detail);
                }
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        },

        /**
         * Load external script dynamically with retry support
         * @param {string} url - Script URL
         * @param {number} retries - Number of retry attempts (default: 2, so 3 total attempts)
         * @returns {Promise} - Resolves when loaded
         */
        loadScript(url, retries = 2) {
            return new Promise((resolve, reject) => {
                // Check if already loaded
                const existing = document.querySelector(`script[src="${url}"]`);
                if (existing) {
                    resolve();
                    return;
                }

                const attempt = (remainingRetries) => {
                    const script = document.createElement('script');
                    script.src = url;
                    script.async = false;  // Load in order to ensure dependencies
                    script.onload = () => {
                        // Add small delay to ensure script initialization
                        setTimeout(resolve, 100);
                    };
                    script.onerror = () => {
                        // Remove failed script tag so retry creates a fresh one
                        script.remove();
                        if (remainingRetries > 0) {
                            console.warn(`[Checkout] Script load failed, retrying (${remainingRetries} left): ${url}`);
                            setTimeout(() => attempt(remainingRetries - 1), 1000);
                        } else {
                            reject(new Error(`Failed to load: ${url}`));
                        }
                    };
                    document.head.appendChild(script);
                };

                attempt(retries);
            });
        },

        getCsrfToken() {
            const meta = document.querySelector('meta[name="csrf-token"]');
            if (meta && meta.content) return meta.content;
            const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
            if (tokenElement) return tokenElement.value;
            return '';
        },

        formatCurrency(amount) {
            const num = typeof amount === 'string' ? parseFloat(amount) : amount;
            const currency = this.config?.currency || window.__shopCurrency || 'USD';
            if (isNaN(num)) return new Intl.NumberFormat(undefined, {
                style: 'currency', currency, minimumFractionDigits: 2,
            }).format(0);
            return new Intl.NumberFormat(undefined, {
                style: 'currency',
                currency,
                minimumFractionDigits: 2,
            }).format(num);
        },

        isValidEmail(email) {
            return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        },

        // Payment method slug → image path(s) under /static/providers_common/images/brands/payment_methods/
        // "card" expands to top 4 card network logos; all others map to a single SVG
        paymentMethodIcons: {
            // Card networks (generic "card" slug expands to multiple brands)
            card: [
                { name: 'Visa', img: 'cards/visa.svg' },
                { name: 'Mastercard', img: 'cards/mastercard.svg' },
                { name: 'American Express', img: 'cards/american-express.svg' },
                { name: 'Discover', img: 'cards/discover.svg' },
            ],
            // Individual card brands (if returned individually by provider)
            visa:           { name: 'Visa', img: 'cards/visa.svg' },
            mastercard:     { name: 'Mastercard', img: 'cards/mastercard.svg' },
            amex:           { name: 'American Express', img: 'cards/american-express.svg' },
            american_express: { name: 'American Express', img: 'cards/american-express.svg' },
            discover:       { name: 'Discover', img: 'cards/discover.svg' },
            jcb:            { name: 'JCB', img: 'cards/jcb.svg' },
            unionpay:       { name: 'UnionPay', img: 'cards/unionpay.svg' },
            diners:         { name: 'Diners Club', img: 'cards/diners.svg' },
            maestro:        { name: 'Maestro', img: 'cards/maestro.svg' },
            // Wallets
            apple_pay:      { name: 'Apple Pay', img: 'wallets/apple-pay.svg' },
            google_pay:     { name: 'Google Pay', img: 'wallets/google-pay.svg' },
            samsung_pay:    { name: 'Samsung Pay', img: 'wallets/samsung-pay.svg' },
            // Major alternative methods
            paypal:         { name: 'PayPal', img: 'alternative/paypal.svg' },
            ideal:          { name: 'iDEAL', img: 'alternative/ideal.svg' },
            bancontact:     { name: 'Bancontact', img: 'alternative/bancontact.svg' },
            klarna:         { name: 'Klarna', img: 'alternative/klarna.svg' },
            giropay:        { name: 'Giropay', img: 'alternative/giropay.svg' },
            eps:            { name: 'EPS', img: 'alternative/eps.svg' },
            sofort:         { name: 'Sofort', img: 'alternative/klarna.svg' },
            przelewy24:     { name: 'Przelewy24', img: 'alternative/przelewy24.svg' },
            blik:           { name: 'BLIK', img: 'alternative/blik.svg' },
            // SEPA
            sepa_debit:     { name: 'SEPA Debit', img: 'alternative/sepa.svg' },
            sepa:           { name: 'SEPA', img: 'alternative/sepa.svg' },
            // Asian payment methods
            alipay:         { name: 'Alipay', img: 'alternative/alipay.svg' },
            alipay_plus:    { name: 'Alipay+', img: 'alternative/alipay-plus.svg' },
            wechat_pay:     { name: 'WeChat Pay', img: 'alternative/wechat-pay.svg' },
            // Other
            amazon_pay:     { name: 'Amazon Pay', img: 'alternative/amazon-pay.svg' },
            paysafecard:    { name: 'Paysafecard', img: 'alternative/paysafecard.svg' },
            skrill:         { name: 'Skrill', img: 'alternative/skrill.svg' },
            swish:          { name: 'Swish', img: 'alternative/swish.svg' },
            mobilepay:      { name: 'MobilePay', img: 'alternative/mobilepay.svg' },
            vipps:          { name: 'Vipps', img: 'alternative/vipps.svg' },
            twint:          { name: 'TWINT', img: 'alternative/twint.svg' },
        },

        /** Base URL for payment method brand SVGs */
        pmIconBase: '/static/providers_common/images/brands/payment_methods/',

        /**
         * Get the display badge HTML for a payment method slug.
         * Returns <img> icon(s) from the providers_common SVG library.
         * "card" expands to top 4 card brand logos; all others show a single icon.
         * Falls back to a text pill if the method is unknown.
         */
        paymentMethodBadge(slug) {
            const raw = typeof slug === 'string' ? slug : (slug.name || slug.method_type || '');
            const entry = this.paymentMethodIcons[raw];
            if (entry) {
                // "card" maps to an array of brands
                const items = Array.isArray(entry) ? entry : [entry];
                return items.map(item =>
                    `<span class="pm-badge" title="${this.escAttr(item.name)}"><img src="${this.pmIconBase}${item.img}" alt="${this.escAttr(item.name)}" loading="lazy"></span>`
                ).join('');
            }
            // Fallback: humanise slug ("some_method" → "Some Method") with text pill
            const label = raw.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
            return `<span class="pm-badge pm-badge--text" title="${this.escAttr(label)}">${this.esc(label)}</span>`;
        },

        esc(text) {
            const div = document.createElement('div');
            div.textContent = text || '';
            return div.innerHTML;
        },

        escAttr(text) {
            return (text || '').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        },

        showLoading(show) {
            if (this.els.loading) this.els.loading.hidden = !show;
        },

        showAlert(message, type) {
            // Remove existing alerts
            document.querySelectorAll('.checkout-alert--dynamic').forEach(a => a.remove());

            const alertEl = document.createElement('div');
            alertEl.className = `checkout-alert checkout-alert--${type || 'error'} checkout-alert--dynamic`;
            alertEl.textContent = message;
            const steps = this.els.steps;
            if (steps) {
                steps.insertBefore(alertEl, steps.firstChild);
                alertEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                // Auto-dismiss after 8 seconds
                setTimeout(() => alertEl.remove(), 8000);
            }
        },

        /**
         * Show persistent payment error in the payment container with retry button.
         * Unlike showAlert, this does NOT auto-dismiss.
         * @param {object} intentData - The original intent data for retry
         */
        showPaymentError(intentData) {
            const container = document.getElementById('review-payment-container')
                || document.getElementById('embedded-payment-container');
            if (!container) return;

            // Make sure payment section is visible
            const paymentSection = document.getElementById('review-payment-section');
            if (paymentSection) {
                paymentSection.style.display = 'block';
            }

            container.innerHTML = '';

            const errorDiv = document.createElement('div');
            errorDiv.className = 'checkout-payment-error';
            errorDiv.setAttribute('role', 'alert');

            const icon = document.createElement('i');
            icon.className = 'fas fa-exclamation-triangle checkout-payment-error__icon';
            errorDiv.appendChild(icon);

            const title = document.createElement('div');
            title.className = 'checkout-payment-error__title';
            title.textContent = window.UI_STRINGS?.['js.payment_form_unavailable'] || 'Unable to load payment form';
            errorDiv.appendChild(title);

            const message = document.createElement('div');
            message.className = 'checkout-payment-error__message';
            message.textContent = window.UI_STRINGS?.['js.payment_form_error_message'] || 'We could not connect to the payment service. This may be a temporary issue. Please try again or choose a different payment method.';
            errorDiv.appendChild(message);

            const actions = document.createElement('div');
            actions.className = 'checkout-payment-error__actions';

            const retryBtn = document.createElement('button');
            retryBtn.type = 'button';
            retryBtn.className = 'checkout-payment-error__retry-btn';
            retryBtn.innerHTML = '<i class="fas fa-redo"></i> ' + (window.UI_STRINGS?.['js.payment_form_try_again'] || 'Try Again');
            retryBtn.addEventListener('click', () => {
                // Remove previously loaded SDK scripts to force fresh reload
                if (intentData.sdk_dependencies) {
                    intentData.sdk_dependencies.forEach(url => {
                        const existing = document.querySelector(`script[src="${url}"]`);
                        if (existing) existing.remove();
                    });
                }
                if (intentData.handler_url) {
                    const existing = document.querySelector(`script[src="${intentData.handler_url}"]`);
                    if (existing) existing.remove();
                }
                container.innerHTML = '';
                this.showLoading(true);
                this.initPluginHandlerInReview(intentData);
            });
            actions.appendChild(retryBtn);

            const altText = document.createElement('div');
            altText.className = 'checkout-payment-error__alt-text';
            altText.textContent = window.UI_STRINGS?.['js.payment_form_choose_different'] || 'Or go back to select a different payment method';
            actions.appendChild(altText);

            errorDiv.appendChild(actions);
            container.appendChild(errorDiv);

            // Report failure to backend for merchant notification
            this.reportPaymentSDKFailure(intentData.provider_key || 'unknown');
        },

        /**
         * Report payment SDK failure to backend for merchant notification.
         * Fire-and-forget - failures here should not affect customer experience.
         * @param {string} providerKey - The provider slug (e.g., 'airwallex', 'stripe')
         */
        reportPaymentSDKFailure(providerKey) {
            try {
                fetch('/api/payments/report-sdk-failure/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken(),
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify({
                        provider_key: providerKey,
                        error_type: 'sdk_load_failure',
                        page_url: window.location.href,
                        user_agent: navigator.userAgent,
                    }),
                }).catch(() => {
                    // Silently fail - merchant notification must not affect customer UX
                });
            } catch (e) {
                // Silently fail
            }
        },

        showFieldError(fieldId, message) {
            const field = document.getElementById(fieldId);
            if (!field) return;
            field.classList.add('checkout-input--error');
            // Add or update error message
            let errEl = field.nextElementSibling;
            if (!errEl || !errEl.classList.contains('checkout-form-error')) {
                errEl = document.createElement('div');
                errEl.className = 'checkout-form-error';
                field.parentNode.insertBefore(errEl, field.nextSibling);
            }
            errEl.textContent = message;
        },

        clearFieldErrors() {
            document.querySelectorAll('.checkout-input--error').forEach(el => el.classList.remove('checkout-input--error'));
            document.querySelectorAll('.checkout-form-error').forEach(el => el.remove());
        },

        scrollToFirstError() {
            // Find all error fields
            const errorFields = document.querySelectorAll('.checkout-input--error');
            if (errorFields.length === 0) return;

            // Get the first error field (topmost in DOM)
            const firstError = errorFields[0];

            // Get header height for offset
            const header = document.querySelector('header, .site-header, .header, .navbar');
            const headerHeight = header ? header.offsetHeight : 0;
            const offset = headerHeight + 20; // Header height + 20px spacing

            // Scroll to the error field
            const y = firstError.getBoundingClientRect().top + window.pageYOffset - offset;
            window.scrollTo({ top: y, behavior: 'smooth' });

            // Focus the field for accessibility
            firstError.focus();
        },
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => Checkout.init());
    } else {
        Checkout.init();
    }

    window.Checkout = Checkout;
})();
