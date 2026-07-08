/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Promotion Wizard Step 3: Geographic & Method Restrictions
 * Adds Select All / Select None buttons to checkbox groups.
 */

(function() {
    'use strict';

    var configEl = document.getElementById('promotion-wizard-step3-config');
    var i18n = {};
    if (configEl) {
        try {
            var config = JSON.parse(configEl.textContent);
            i18n = config.i18n || {};
        } catch (e) {
            // fall back to empty strings
        }
    }

    function addSelectButtons(container, fieldName) {
        var buttonsDiv = document.createElement('div');
        buttonsDiv.className = 'select-buttons';
        buttonsDiv.style.marginBottom = '15px';
        buttonsDiv.innerHTML =
            '<button type="button" class="btn-select-all" data-field="' + fieldName + '">' +
            '<i class="fas fa-check-double"></i> ' + (i18n.selectAll || 'Select All') +
            '</button>' +
            '<button type="button" class="btn-select-none" data-field="' + fieldName + '">' +
            '<i class="fas fa-times"></i> ' + (i18n.selectNone || 'Select None') +
            '</button>';

        container.parentNode.insertBefore(buttonsDiv, container);

        buttonsDiv.querySelector('.btn-select-all').addEventListener('click', function() {
            var checkboxes = document.querySelectorAll('input[name="' + fieldName + '"]');
            checkboxes.forEach(function(cb) { cb.checked = true; });
        });

        buttonsDiv.querySelector('.btn-select-none').addEventListener('click', function() {
            var checkboxes = document.querySelectorAll('input[name="' + fieldName + '"]');
            checkboxes.forEach(function(cb) { cb.checked = false; });
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        // Add helper buttons for zones if there are any
        var zoneCheckboxGroup = document.querySelector('.form-section:nth-of-type(2) .checkbox-group');
        if (zoneCheckboxGroup) {
            addSelectButtons(zoneCheckboxGroup, 'zones');
        }

        // Add helper buttons for methods if there are any
        var methodCheckboxGroup = document.querySelector('.form-section:nth-of-type(3) .checkbox-group');
        if (methodCheckboxGroup) {
            addSelectButtons(methodCheckboxGroup, 'shipping_methods');
        }
    });

}());
