/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Payment Provider Admin - Change Form JavaScript
 * Handles multiselect helpers using admin-base.css classes.
 * Tab switching handled by global AdminTabs utility.
 *
 *  */

(function() {
    'use strict';

    // Load i18n strings from template config
    var i18n = {};
    var configEl = document.getElementById('pp-form-config');
    if (configEl) {
        try {
            var config = JSON.parse(configEl.textContent);
            i18n = config.i18n || {};
        } catch (e) {
            // fall back to empty strings
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        initializeMultiselectHelpers();
        initializeCopyButtons();
    });

    /**
     * Add select all / deselect all buttons for payment methods multiselect
     */
    function initializeMultiselectHelpers() {
        var paymentMethodsSelect = document.querySelector('#id_payment_method_types');

        if (paymentMethodsSelect) {
            var wrapper = paymentMethodsSelect.parentElement;
            var buttonContainer = document.createElement('div');
            buttonContainer.className = 'pp-multiselect-helpers';

            var selectAllBtn = document.createElement('button');
            selectAllBtn.type = 'button';
            selectAllBtn.className = 'button';
            selectAllBtn.dataset.action = 'selectall';
            var selectIcon = document.createElement('i');
            selectIcon.className = 'fas fa-check-double';
            selectAllBtn.appendChild(selectIcon);
            selectAllBtn.appendChild(document.createTextNode(' ' + (i18n.selectAll || 'Select All')));

            var clearAllBtn = document.createElement('button');
            clearAllBtn.type = 'button';
            clearAllBtn.className = 'button';
            clearAllBtn.dataset.action = 'deselectall';
            var clearIcon = document.createElement('i');
            clearIcon.className = 'fas fa-times';
            clearAllBtn.appendChild(clearIcon);
            clearAllBtn.appendChild(document.createTextNode(' ' + (i18n.clearAll || 'Clear All')));

            buttonContainer.appendChild(selectAllBtn);
            buttonContainer.appendChild(clearAllBtn);

            wrapper.insertBefore(buttonContainer, paymentMethodsSelect);

            buttonContainer.addEventListener('click', function(e) {
                var target = e.target.closest('[data-action]');
                if (!target) return;
                var action = target.dataset.action;

                var options = paymentMethodsSelect.options;
                for (var idx = 0; idx < options.length; idx++) {
                    options[idx].selected = (action === 'selectall');
                }
            });
        }
    }

    /**
     * Initialize copy-to-clipboard buttons
     */
    function initializeCopyButtons() {
        document.querySelectorAll('.pp-copy-btn').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var targetId = btn.dataset.copyTarget;
                var target = document.getElementById(targetId);
                if (!target) return;

                var text = target.textContent.trim();
                navigator.clipboard.writeText(text).then(function() {
                    btn.classList.add('copied');
                    var icon = btn.querySelector('i');
                    if (icon) {
                        icon.className = 'fas fa-check';
                        setTimeout(function() {
                            icon.className = 'fas fa-copy';
                            btn.classList.remove('copied');
                        }, 2000);
                    }
                });
            });
        });
    }

})();
