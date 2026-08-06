/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Product Subscription Options
 *
 * Wires the buy-box subscription selector: one-time vs subscribe toggle, plan
 * switching, and per-tier price swap when a variant is chosen. Every displayed
 * price is a string the server already formatted (variantsData.subscription_prices
 * and the server-rendered tier labels) — this module never does money maths.
 *
 * Exposes window.SubscriptionOptions.getSelection() for product-base.js so the
 * add-to-cart request can carry the chosen plan + tier.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const root = document.querySelector('[data-subscription-options]');
    if (!root) return;

    // Variant → per-tier price strings (formatted server-side).
    let variantsData = [];
    try {
      const el = document.getElementById('variants-data');
      variantsData = el ? JSON.parse(el.textContent || '[]') : [];
    } catch (e) {
      variantsData = [];
    }

    const fields = root.querySelector('[data-subscription-fields]');

    // --- Purchase mode (one-time vs subscription) ---
    function currentMode() {
      const checked = root.querySelector('input[name="purchase-mode"]:checked');
      if (checked) return checked.value;
      // No radio present → one-time not allowed → subscription is forced.
      return root.dataset.allowOneTime === 'false' ? 'subscription' : 'one_time';
    }

    function applyMode() {
      const isSub = currentMode() === 'subscription';
      if (fields) fields.hidden = !isSub;
    }

    root.querySelectorAll('input[name="purchase-mode"]').forEach(function (radio) {
      radio.addEventListener('change', applyMode);
    });

    // --- Plan switching ---
    function showPlan(planId) {
      root.querySelectorAll('[data-plan-panel]').forEach(function (panel) {
        panel.hidden = panel.dataset.planPanel !== planId;
      });
      root.querySelectorAll('[data-plan-meta]').forEach(function (meta) {
        meta.hidden = meta.dataset.planMeta !== planId;
      });
      // Radios share the name "pricing-tier", so switching plans leaves the new
      // plan with no checked tier — preselect its default (or first) tier.
      const panel = root.querySelector('[data-plan-panel="' + planId + '"]');
      if (panel && !panel.querySelector('input[name="pricing-tier"]:checked')) {
        const preferred =
          panel.querySelector('input[name="pricing-tier"][data-tier-default="true"]') ||
          panel.querySelector('input[name="pricing-tier"]');
        if (preferred) preferred.checked = true;
      }
    }

    root.querySelectorAll('input[name="subscription-plan"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        showPlan(this.value || this.dataset.planId);
      });
    });

    // --- Per-tier price swap on variant change ---
    // product-base.js always writes the resolved variant id onto #add-to-cart's
    // data-variant-id, so watching that attribute captures both selection modes
    // (direct swatches and attribute matching) without touching that module.
    function applyVariantPrices(variantId) {
      if (variantId == null || variantId === '') return;
      const variant = variantsData.find(function (v) {
        return String(v.id) === String(variantId);
      });
      if (!variant || !variant.subscription_prices) return;
      Object.keys(variant.subscription_prices).forEach(function (tierId) {
        const priceEl = root.querySelector('[data-tier-price="' + tierId + '"]');
        if (priceEl) priceEl.textContent = variant.subscription_prices[tierId];
      });
    }

    const addBtn = document.getElementById('add-to-cart');
    if (addBtn && typeof MutationObserver !== 'undefined') {
      const observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (m) {
          if (m.attributeName === 'data-variant-id') {
            applyVariantPrices(addBtn.dataset.variantId);
          }
        });
      });
      observer.observe(addBtn, { attributes: true, attributeFilter: ['data-variant-id'] });
      if (addBtn.dataset.variantId) applyVariantPrices(addBtn.dataset.variantId);
    }

    // Reflect the server-rendered initial state.
    applyMode();

    // --- Public API for product-base.js ---
    function getSelection() {
      if (currentMode() !== 'subscription') {
        return { is_subscription: false };
      }
      const planInput =
        root.querySelector('input[name="subscription-plan"]:checked') ||
        root.querySelector('input[name="subscription-plan"]');
      const planId = planInput ? planInput.value || planInput.dataset.planId : null;

      // Read the checked tier inside the visible plan panel first — tier radios
      // share a name across plans, so a hidden plan could hold the browser's
      // "checked" state otherwise.
      let tierInput = null;
      if (planId) {
        const panel = root.querySelector('[data-plan-panel="' + planId + '"]');
        if (panel) tierInput = panel.querySelector('input[name="pricing-tier"]:checked');
      }
      if (!tierInput) tierInput = root.querySelector('input[name="pricing-tier"]:checked');
      const tierId = tierInput ? tierInput.value || tierInput.dataset.tierId : null;

      return {
        is_subscription: true,
        subscription_plan_id: planId,
        pricing_tier_id: tierId,
      };
    }

    window.SubscriptionOptions = { getSelection: getSelection };
  });
})();
