/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Visibility Rule Wizard
 * Handles the 4-step wizard for creating visibility rules.
 * Reads rule type config, operator labels, and translations from
 * the #visibility-rule-wizard-i18n JSON data island.
 */
(function () {
    'use strict';

    var currentStep = 1;
    var totalSteps = 4;
    var selectedRuleType = null;
    var selectedOperator = null;
    var ruleTypeConfig = {};
    var operatorLabels = {};
    var geoipWarnings = {};
    var ui = {};
    var deviceOptions = {};

    function init() {
        var el = document.getElementById('visibility-rule-wizard-i18n');
        if (el) {
            try {
                var data = JSON.parse(el.textContent);
                ruleTypeConfig = data.ruleTypeConfig || {};
                operatorLabels = data.operatorLabels || {};
                geoipWarnings = data.geoipWarnings || {};
                ui = data.ui || {};
                deviceOptions = data.deviceOptions || {};
                if (ruleTypeConfig.device_type && deviceOptions) {
                    ruleTypeConfig.device_type.options = [
                        { value: 'mobile', label: deviceOptions.mobile || 'Mobile' },
                        { value: 'tablet', label: deviceOptions.tablet || 'Tablet' },
                        { value: 'desktop', label: deviceOptions.desktop || 'Desktop' }
                    ];
                }
            } catch (e) {
                console.error('Failed to parse visibility-rule-wizard-i18n:', e);
            }
        }
        initRuleTypeSelection();
        initNavigation();
        initDaySelector();
        initBooleanToggle();
    }

    function initRuleTypeSelection() {
        var ruleTypeItems = document.querySelectorAll('.rule-type-item');
        ruleTypeItems.forEach(function (item) {
            item.addEventListener('click', function () {
                ruleTypeItems.forEach(function (i) { i.classList.remove('selected'); });
                this.classList.add('selected');
                var radio = this.querySelector('input[type="radio"]');
                radio.checked = true;
                selectedRuleType = radio.value;
            });
        });
    }

    function initNavigation() {
        var prevBtn = document.getElementById('prev-btn');
        var nextBtn = document.getElementById('next-btn');
        prevBtn.addEventListener('click', function () { goToStep(currentStep - 1); });
        nextBtn.addEventListener('click', function () {
            if (validateStep(currentStep)) { goToStep(currentStep + 1); }
        });
    }

    function initDaySelector() {
        document.querySelectorAll('.day-option').forEach(function (option) {
            option.addEventListener('click', function (e) {
                e.preventDefault();
                var checkbox = this.querySelector('input[type="checkbox"]');
                checkbox.checked = !checkbox.checked;
                this.classList.toggle('selected', checkbox.checked);
            });
        });
    }

    function initBooleanToggle() {
        var booleanOptions = document.querySelectorAll('.boolean-option');
        booleanOptions.forEach(function (option) {
            option.addEventListener('click', function () {
                booleanOptions.forEach(function (o) { o.classList.remove('selected'); });
                this.classList.add('selected');
                this.querySelector('input[type="radio"]').checked = true;
            });
        });
    }

    function goToStep(step) {
        if (step < 1 || step > totalSteps) { return; }
        document.getElementById('step-' + currentStep).classList.add('hidden');
        document.querySelector('.step[data-step="' + currentStep + '"]').classList.remove('active');
        for (var i = 1; i < step; i++) {
            document.querySelector('.step[data-step="' + i + '"]').classList.add('completed');
        }
        currentStep = step;
        document.getElementById('step-' + currentStep).classList.remove('hidden');
        document.querySelector('.step[data-step="' + currentStep + '"]').classList.add('active');
        updateNavigationButtons();
        if (currentStep === 2) { setupStep2(); }
        else if (currentStep === 4) { populateReview(); }
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function setupStep2() {
        if (!selectedRuleType || !ruleTypeConfig[selectedRuleType]) { return; }
        var config = ruleTypeConfig[selectedRuleType];
        document.getElementById('rule-help-title').textContent = config.label;
        document.getElementById('rule-help-text').textContent = config.help;
        var geoipWarning = document.getElementById('geoip-warning');
        var geoipDetail = document.getElementById('geoip-warning-detail');
        var geoRuleTypes = ['geo_country', 'geo_region', 'geo_city', 'geo_timezone'];
        if (geoRuleTypes.indexOf(selectedRuleType) !== -1) {
            geoipWarning.classList.remove('hidden');
            if (selectedRuleType === 'geo_country') {
                geoipDetail.textContent = geoipWarnings.country || '';
            } else if (selectedRuleType === 'geo_region' || selectedRuleType === 'geo_city') {
                geoipDetail.textContent = geoipWarnings.regionCity || '';
            } else {
                geoipDetail.textContent = geoipWarnings.timezone || '';
            }
        } else {
            geoipWarning.classList.add('hidden');
        }
        var operatorGrid = document.getElementById('operator-grid');
        operatorGrid.innerHTML = '';
        config.operators.forEach(function (op, index) {
            var opInfo = operatorLabels[op] || { label: op, symbol: op };
            var div = document.createElement('div');
            div.className = 'operator-item' + (index === 0 ? ' selected' : '');
            div.dataset.operator = op;
            div.innerHTML =
                '<input type="radio" name="operator" value="' + op + '" id="op-' + op + '"' + (index === 0 ? ' checked' : '') + '>' +
                '<span class="symbol">' + opInfo.symbol + '</span>' +
                '<label for="op-' + op + '">' + opInfo.label + '</label>';
            div.addEventListener('click', (function (opValue) {
                return function () {
                    document.querySelectorAll('.operator-item').forEach(function (i) { i.classList.remove('selected'); });
                    this.classList.add('selected');
                    this.querySelector('input[type="radio"]').checked = true;
                    selectedOperator = opValue;
                    updateValueInput();
                };
            }(op)));
            operatorGrid.appendChild(div);
        });
        selectedOperator = config.operators[0];
        updateValueInput();
    }

    function updateValueInput() {
        if (!selectedRuleType || !ruleTypeConfig[selectedRuleType]) { return; }
        var config = ruleTypeConfig[selectedRuleType];
        ['text-value-group', 'boolean-value-group', 'number-value-group', 'range-value-group',
         'date-range-group', 'time-range-group', 'day-selector-group', 'select-value-group'
        ].forEach(function (id) {
            document.getElementById(id).classList.add('hidden');
        });
        var valueType = config.valueType;
        if (valueType === 'boolean' || selectedOperator === 'is_true' || selectedOperator === 'is_false') {
            document.getElementById('boolean-value-group').classList.remove('hidden');
            if (selectedOperator === 'is_true') {
                document.querySelector('.boolean-option[data-value="true"]').click();
            } else if (selectedOperator === 'is_false') {
                document.querySelector('.boolean-option[data-value="false"]').click();
            }
        } else if (valueType === 'number') {
            if (selectedOperator === 'between') {
                document.getElementById('range-value-group').classList.remove('hidden');
                document.querySelector('#range-value-group input:first-of-type').type = 'number';
                document.querySelector('#range-value-group input:last-of-type').type = 'number';
            } else {
                document.getElementById('number-value-group').classList.remove('hidden');
                document.getElementById('number-help-text').textContent = config.help;
            }
        } else if (valueType === 'date_range') {
            document.getElementById('date-range-group').classList.remove('hidden');
        } else if (valueType === 'time_range') {
            document.getElementById('time-range-group').classList.remove('hidden');
        } else if (valueType === 'day_selector') {
            document.getElementById('day-selector-group').classList.remove('hidden');
        } else if (valueType === 'select') {
            document.getElementById('select-value-group').classList.remove('hidden');
            var select = document.getElementById('rule-value-select');
            select.innerHTML = '';
            (config.options || []).forEach(function (opt) {
                var option = document.createElement('option');
                option.value = opt.value;
                option.textContent = opt.label;
                select.appendChild(option);
            });
        } else {
            document.getElementById('text-value-group').classList.remove('hidden');
            var input = document.getElementById('rule-value');
            input.placeholder = config.valuePlaceholder || (ui.enterValue || 'Enter value...');
            document.getElementById('value-help-text').textContent = config.help;
        }
        document.getElementById('value-config-label').textContent =
            config.label + ' ' + (ui.valueSuffix || 'Value');
    }

    function updateNavigationButtons() {
        var prevBtn = document.getElementById('prev-btn');
        var nextBtn = document.getElementById('next-btn');
        var submitBtn = document.getElementById('submit-btn');
        var cancelBtn = document.getElementById('cancel-btn');
        prevBtn.style.display = currentStep === 1 ? 'none' : 'inline-flex';
        cancelBtn.style.display = currentStep === 1 ? 'inline-flex' : 'none';
        nextBtn.style.display = currentStep === totalSteps ? 'none' : 'inline-flex';
        submitBtn.style.display = currentStep === totalSteps ? 'inline-flex' : 'none';
    }

    function validateStep(step) {
        var errors = [];
        if (step === 1) {
            if (!selectedRuleType) { errors.push(ui.selectRuleType || 'Please select a rule type'); }
        }
        if (step === 2) {
            var value = getValue();
            if (!selectedOperator) { errors.push(ui.selectOperator || 'Please select an operator'); }
            if (value === null || value === '' || (Array.isArray(value) && value.length === 0)) {
                if (selectedOperator !== 'is_true' && selectedOperator !== 'is_false') {
                    errors.push(ui.enterValueError || 'Please enter a value');
                }
            }
        }
        if (step === 3) {
            var name = document.getElementById('rule-name').value.trim();
            if (!name) { errors.push(ui.enterRuleName || 'Please enter a rule name'); }
        }
        if (errors.length > 0) { AdminModal.alert({message: errors.join('\n'), type: 'warning'}); return false; }
        return true;
    }

    function getValue() {
        if (!selectedRuleType || !ruleTypeConfig[selectedRuleType]) { return null; }
        var config = ruleTypeConfig[selectedRuleType];
        var valueType = config.valueType;
        if (valueType === 'boolean' || selectedOperator === 'is_true' || selectedOperator === 'is_false') {
            var selected = document.querySelector('.boolean-option.selected');
            return selected ? selected.dataset.value === 'true' : null;
        }
        if (valueType === 'number') {
            if (selectedOperator === 'between') {
                var from = document.getElementById('range-from').value;
                var to = document.getElementById('range-to').value;
                return { from: parseFloat(from), to: parseFloat(to) };
            }
            return parseFloat(document.getElementById('rule-value-number').value);
        }
        if (valueType === 'date_range') {
            return { from: document.getElementById('date-from').value, to: document.getElementById('date-to').value };
        }
        if (valueType === 'time_range') {
            return { from: document.getElementById('time-from').value, to: document.getElementById('time-to').value };
        }
        if (valueType === 'day_selector') {
            var selDays = [];
            document.querySelectorAll('.day-option.selected').forEach(function (day) {
                selDays.push(parseInt(day.dataset.day));
            });
            return selDays;
        }
        if (valueType === 'select') {
            var sel = document.getElementById('rule-value-select');
            var selOpts = Array.from(sel.selectedOptions).map(function (o) { return o.value; });
            return selOpts.length === 1 ? selOpts[0] : selOpts;
        }
        return document.getElementById('rule-value').value.trim();
    }

    function populateReview() {
        var config = ruleTypeConfig[selectedRuleType];
        var opInfo = operatorLabels[selectedOperator] || { label: selectedOperator };
        var value = getValue();
        document.getElementById('review-rule-name').textContent =
            document.getElementById('rule-name').value || (ui.unnamedRule || 'Unnamed Rule');
        document.getElementById('review-rule-type').textContent = config.label;
        document.getElementById('review-operator').textContent = opInfo.label;
        var valueDisplay = value;
        if (typeof value === 'boolean') {
            valueDisplay = value ? (ui.trueLabel || 'True') : (ui.falseLabel || 'False');
        } else if (typeof value === 'object' && value !== null) {
            if (value.from !== undefined && value.to !== undefined) {
                valueDisplay = value.from + ' \u2192 ' + value.to;
            } else if (Array.isArray(value)) {
                valueDisplay = value.join(', ');
            } else {
                valueDisplay = JSON.stringify(value);
            }
        }
        document.getElementById('review-value').textContent = valueDisplay;
        var isActive = document.getElementById('rule-active').checked;
        document.getElementById('review-status').innerHTML = isActive
            ? '<span class="status-badge active"><i class="fas fa-check-circle"></i> ' + (ui.activeStatus || 'Active') + '</span>'
            : '<span class="status-badge inactive"><i class="fas fa-times-circle"></i> ' + (ui.inactiveStatus || 'Inactive') + '</span>';
        var description = document.getElementById('rule-description').value;
        var descGroup = document.getElementById('review-description-group');
        if (description) {
            descGroup.classList.remove('hidden');
            document.getElementById('review-description').textContent = description;
        } else {
            descGroup.classList.add('hidden');
        }
        document.getElementById('rule-value-json').value = JSON.stringify(value);
    }

    document.addEventListener('DOMContentLoaded', init);
}());
