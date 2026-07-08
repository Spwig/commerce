/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Site Settings Admin JavaScript
 * Enhances the site settings admin interface with validation and UX improvements
 */

(function() {
    'use strict';

    // Wait for Django admin to load
    document.addEventListener('DOMContentLoaded', function() {
        // Use Django's jQuery
        var $ = django.jQuery;
        
        // Character count for meta fields
        function addCharacterCount(fieldId, maxLength) {
            const field = $('#' + fieldId);
            if (field.length) {
                const helpText = field.closest('.form-row').find('.help');
                const counter = $('<div class="char-counter"></div>');
                helpText.after(counter);
                
                function updateCount() {
                    const remaining = maxLength - field.val().length;
                    const color = remaining < 10 ? '#dc3545' : remaining < 30 ? '#ffc107' : '#28a745';
                    counter.html(`<span style="color: ${color}">${field.val().length}/${maxLength} characters</span>`);
                }
                
                field.on('input', updateCount);
                updateCount();
            }
        }
        
        // Add character counters for meta fields
        addCharacterCount('id_meta_title', 60);
        addCharacterCount('id_meta_description', 160);
        
        // Email validation feedback
        function validateEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }
        
        function addEmailValidation(fieldId) {
            const field = $('#' + fieldId);
            if (field.length) {
                const validationDiv = $('<div class="email-validation"></div>');
                field.after(validationDiv);
                
                field.on('blur', function() {
                    const email = field.val().trim();
                    if (email && !validateEmail(email)) {
                        validationDiv.html('<span style="color: #dc3545;">⚠ Please enter a valid email address</span>');
                    } else {
                        validationDiv.empty();
                    }
                });
            }
        }
        
        // Add email validation for email fields
        addEmailValidation('id_admin_email');
        addEmailValidation('id_support_email');
        
        // URL validation
        function validateURL(url) {
            try {
                new URL(url);
                return true;
            } catch {
                return false;
            }
        }
        
        function addURLValidation(fieldId) {
            const field = $('#' + fieldId);
            if (field.length) {
                const validationDiv = $('<div class="url-validation"></div>');
                field.after(validationDiv);
                
                field.on('blur', function() {
                    const url = field.val().trim();
                    if (url && !validateURL(url)) {
                        validationDiv.html('<span style="color: #dc3545;">⚠ Please enter a valid URL (including http:// or https://)</span>');
                    } else {
                        validationDiv.empty();
                    }
                });
            }
        }
        
        // Add URL validation for URL fields
        addURLValidation('id_site_url');
        addURLValidation('id_facebook_url');
        addURLValidation('id_twitter_url');
        addURLValidation('id_instagram_url');
        addURLValidation('id_linkedin_url');
        
        // Maintenance mode warning
        const maintenanceField = $('#id_maintenance_mode');
        if (maintenanceField.length) {
            maintenanceField.on('change', function() {
                if (this.checked) {
                    const warning = $('<div class="maintenance-warning" style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 4px;"><strong>⚠ Warning:</strong> Enabling maintenance mode will make your site inaccessible to visitors. Only staff members will be able to access the site.</div>');
                    maintenanceField.closest('.form-row').after(warning);
                } else {
                    $('.maintenance-warning').remove();
                }
            });
        }
        
        // Auto-fill support email with admin email if empty
        const adminEmailField = $('#id_admin_email');
        const supportEmailField = $('#id_support_email');
        
        if (adminEmailField.length && supportEmailField.length) {
            adminEmailField.on('blur', async function() {
                if (!supportEmailField.val().trim() && validateEmail(adminEmailField.val())) {
                    if (await AdminModal.confirm('Would you like to use the same email for customer support?')) {
                        supportEmailField.val(adminEmailField.val());
                    }
                }
            });
        }
        
        // Currency and timezone help
        const currencyField = $('#id_default_currency');
        const timezoneField = $('#id_default_timezone');
        
        if (currencyField.length) {
            const currencyHelp = $('<div class="field-help" style="font-size: 11px; color: #666; margin-top: 5px;">This will be the default currency for all product prices. You can still set individual product prices in different currencies.</div>');
            currencyField.after(currencyHelp);
        }
        
        if (timezoneField.length) {
            const timezoneHelp = $('<div class="field-help" style="font-size: 11px; color: #666; margin-top: 5px;">This affects order timestamps, scheduled tasks, and email notifications.</div>');
            timezoneField.after(timezoneHelp);
        }
        
        // Form submission validation
        $('form').on('submit', function(e) {
            let hasErrors = false;
            
            // Check required email fields
            $('.required input[type="email"]').each(function() {
                const email = $(this).val().trim();
                if (email && !validateEmail(email)) {
                    hasErrors = true;
                    $(this).focus();
                    AdminModal.alert({message: 'Please correct the email address: ' + $(this).closest('.form-row').find('label').text(), type: 'error'});
                    return false;
                }
            });
            
            // Check required URL fields
            $('.required input[type="url"]').each(function() {
                const url = $(this).val().trim();
                if (url && !validateURL(url)) {
                    hasErrors = true;
                    $(this).focus();
                    AdminModal.alert({message: 'Please correct the URL: ' + $(this).closest('.form-row').find('label').text(), type: 'error'});
                    return false;
                }
            });
            
            if (hasErrors) {
                e.preventDefault();
            }
        });
        
        // Add save reminder for maintenance mode
        if (maintenanceField.length && maintenanceField.prop('checked')) {
            const warning = $('<div class="maintenance-active" style="background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 15px; margin: 15px 0; border-radius: 4px; font-weight: bold;"><strong>🚧 Maintenance Mode is Currently Active</strong><br>Your site is in maintenance mode. Visitors will see a maintenance page.</div>');
            $('.form-row').first().before(warning);
        }

    });

})();

/**
 * License Status Widget
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var dataEl = document.getElementById('site-settings-license-data');
        if (!dataEl) { return; }

        var data;
        try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }

        var t = data.translations || {};
        var apiUrl = data.apiUrl || '';

        fetch(apiUrl)
            .then(function (r) { return r.json(); })
            .then(function (d) {
                var badge = document.getElementById('license-badge');
                var typeEl = document.getElementById('license-type');
                var featuresEl = document.getElementById('license-features');

                if (d.is_valid) {
                    if (badge) {
                        badge.textContent = '\u2713 ' + (t.licensed || 'Licensed');
                        badge.style.background = 'var(--success-color)';
                        badge.style.color = 'white';
                    }
                    if (typeEl) {
                        typeEl.textContent = d.license_type.charAt(0).toUpperCase() + d.license_type.slice(1);
                    }
                    if (featuresEl) {
                        featuresEl.style.display = 'block';
                        setFeature('feature-payment', d.features.payment_processing, t.paymentProcessing || 'Payment Processing', t);
                        setFeature('feature-support', d.features.priority_support, t.prioritySupport || 'Priority Support', t);
                    }
                } else {
                    if (badge) {
                        badge.textContent = '\u26a0 ' + (t.trialMode || 'Trial Mode');
                        badge.style.background = 'var(--warning-color)';
                        badge.style.color = 'white';
                    }
                    if (typeEl) {
                        typeEl.textContent = t.paymentDisabled || 'Payment processing disabled';
                    }
                }
            })
            .catch(function () {
                var badge = document.getElementById('license-badge');
                if (badge) { badge.textContent = '? ' + (t.unknown || 'Unknown'); }
            });
    });

    function setFeature(id, enabled, label, t) {
        var el = document.getElementById(id);
        if (!el) { return; }
        var icon = document.createElement('span');
        if (enabled) {
            icon.style.color = 'var(--success-fg)';
            icon.textContent = '\u2713';
        } else {
            icon.className = 'text-error';
            icon.textContent = '\u2717';
        }
        el.textContent = '';
        el.appendChild(icon);
        el.appendChild(document.createTextNode(' ' + label));
    }
}());