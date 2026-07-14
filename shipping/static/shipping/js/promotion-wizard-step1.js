/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Promotion Wizard Step 1: Rule Basics
 * Shows/hides the rule value field based on rule type selection.
 */

(function () {
  'use strict';

  const configEl = document.getElementById('promotion-wizard-step1-config');
  let i18n = {};
  if (configEl) {
    try {
      const config = JSON.parse(configEl.textContent);
      i18n = config.i18n || {};
    } catch (e) {
      // fall back to empty strings
    }
  }

  function updateRuleValueField() {
    const ruleTypeEl = document.getElementById('id_rule_type');
    if (!ruleTypeEl) return;

    const ruleType = ruleTypeEl.value;
    const valueGroup = document.getElementById('rule-value-group');
    const valueInput = document.getElementById('id_rule_value');
    const valueLabel = document.getElementById('rule-value-label');
    const valueHelpText = document.getElementById('rule-value-help-text');

    if (!valueGroup || !valueInput) return;

    if (ruleType === 'free_shipping') {
      valueGroup.style.display = 'none';
      valueInput.removeAttribute('required');
    } else {
      valueGroup.style.display = 'block';
      valueInput.setAttribute('required', 'required');

      if (ruleType === 'discount_percentage' || ruleType === 'surcharge_percentage') {
        if (valueLabel) valueLabel.textContent = i18n.percentage || 'Percentage';
        if (valueHelpText)
          valueHelpText.textContent = i18n.enterPercentage || 'Enter percentage (0-100)';
        valueInput.setAttribute('max', '100');
      } else if (ruleType === 'discount_fixed' || ruleType === 'surcharge_fixed') {
        if (valueLabel) valueLabel.textContent = i18n.amount || 'Amount';
        if (valueHelpText)
          valueHelpText.textContent =
            i18n.enterAmount || 'Enter fixed amount in your default currency';
        valueInput.removeAttribute('max');
      } else if (ruleType === 'set_cost') {
        if (valueLabel) valueLabel.textContent = i18n.shippingCost || 'Shipping Cost';
        if (valueHelpText)
          valueHelpText.textContent = i18n.enterShippingCost || 'Enter the fixed shipping cost';
        valueInput.removeAttribute('max');
      }
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const ruleTypeEl = document.getElementById('id_rule_type');
    if (!ruleTypeEl) return;

    ruleTypeEl.addEventListener('change', updateRuleValueField);

    // Trigger on load to set initial state
    updateRuleValueField();
  });
})();
