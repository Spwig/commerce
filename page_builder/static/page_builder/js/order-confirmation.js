/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Order confirmation page: account creation form handler.
 * Extracted from page_builder/templates/page_builder/order_confirmation.html
 */
(function () {
    'use strict';

    // Clear checkout state from sessionStorage
    sessionStorage.removeItem('payment_intent_id');
    sessionStorage.removeItem('order_number');

    var form = document.getElementById('account-creation-form');
    var skipBtn = document.getElementById('skip-account');

    if (!form) return;

    function getCSRFToken() {
        var meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        var input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input) return input.value;
        return '';
    }

    function showSuccessMessage(message) {
        var banner = document.querySelector('.confirmation__banner');
        var successDiv = document.createElement('div');
        successDiv.className = 'confirmation__success-message';
        successDiv.innerHTML = '<i class="fas fa-check-circle"></i><span>' + message + '</span>';
        if (banner && banner.parentNode) {
            banner.parentNode.insertBefore(successDiv, banner.nextSibling);
        }
    }

    function showErrorMessage(message) {
        var existingError = form.querySelector('.confirmation__error-message');
        if (existingError) existingError.remove();
        var errorDiv = document.createElement('div');
        errorDiv.className = 'confirmation__error-message';
        errorDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i><span>' + message + '</span>';
        form.insertBefore(errorDiv, form.firstChild);
    }

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        var password = document.getElementById('account-password').value;
        var passwordConfirm = document.getElementById('account-password-confirm').value;
        var submitBtn = document.getElementById('create-account-btn');

        if (password !== passwordConfirm) {
            showErrorMessage('Passwords do not match');
            return;
        }

        if (password.length < 8) {
            showErrorMessage('Password must be at least 8 characters');
            return;
        }

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
        }

        fetch('/api/accounts/convert-guest/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ password: password })
        })
        .then(function (response) {
            return response.json().then(function (data) {
                return { ok: response.ok, data: data };
            });
        })
        .then(function (result) {
            if (result.ok && result.data.success) {
                showSuccessMessage(result.data.message || 'Account created successfully!');
                var card = document.querySelector('.confirmation__card--highlight');
                if (card) {
                    setTimeout(function () {
                        card.style.opacity = '0';
                        card.style.transition = 'opacity 0.3s ease';
                        setTimeout(function () { card.remove(); }, 300);
                    }, 1500);
                }
                var lang2 = document.documentElement.lang || 'en';
                setTimeout(function () {
                    window.location.href = '/' + lang2 + '/accounts/dashboard/';
                }, 2000);
            } else {
                showErrorMessage(result.data.message || 'Failed to create account. Please try again.');
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-check"></i> Create Account';
                }
            }
        })
        .catch(function (err) {
            console.error('Account creation error:', err);
            showErrorMessage('An error occurred. Please try again.');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Create Account';
            }
        });
    });

    if (skipBtn) {
        skipBtn.addEventListener('click', async function () {
            var card = document.querySelector('.confirmation__card--highlight');
            if (card && await AdminModal.confirm('Are you sure you want to skip creating an account? You can always create one later from your email.')) {
                card.style.opacity = '0';
                card.style.transition = 'opacity 0.3s ease';
                setTimeout(function () { card.remove(); }, 300);
            }
        });
    }
})();
