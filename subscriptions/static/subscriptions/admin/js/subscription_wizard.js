/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    'use strict';

    var i18n = {
        pricingTier: 'Pricing Tier',
        setDefault: 'Set Default',
        remove: 'Remove',
        tierName: 'Tier Name',
        tierNamePlaceholder: 'e.g., Monthly, Annual',
        billingCycle: 'Billing Cycle',
        daily: 'Daily',
        weekly: 'Weekly',
        monthly: 'Monthly',
        quarterly: 'Quarterly',
        semiannual: 'Semi-Annual',
        annual: 'Annual',
        billingInterval: 'Billing Interval',
        billingIntervalHelp: "e.g., 2 for 'every 2 months'",
        discountPct: 'Discount %',
        discountHelp: 'Discount off product price',
        noTiersMsg: "No pricing tiers yet. Click 'Add Pricing Tier' to get started.",
        planNameRequired: 'Plan name is required',
        tierRequired: 'At least one pricing tier is required',
        tierNameRequired: 'All tiers must have a name',
        tieredPricing: 'Tiered Pricing',
        quantityBased: 'Quantity-Based',
        flatRate: 'Flat Rate',
        defaultLabel: 'Default',
        every: 'Every',
        discount: 'discount',
        days: 'days',
        noTrial: 'No trial',
        free: 'Free',
        yes: 'Yes',
        no: 'No',
        unlimited: 'Unlimited',
        cancelAnytime: 'Cancel Anytime',
        cancelAtPeriodEnd: 'Cancel at Period End',
        minimumCommitment: 'Minimum Commitment Required',
        cycles: 'cycles',
        none: 'None',
        disabled: 'Disabled'
    };

    // State
    var currentStep = 1;
    var totalSteps = 7;
    var tiersData = [];
    var tierCounter = 0;

    // Initialize
    document.addEventListener('DOMContentLoaded', function () {
        var island = document.getElementById('subscription-wizard-i18n');
        if (island) {
            try { i18n = JSON.parse(island.textContent); } catch (e) {}
        }

        initPricingModelCards();
        initCancellationPolicyCards();
        initTierManagement();
        initQuantitySettings();
        initCommitmentSettings();
        initNavigation();
    });

    function initPricingModelCards() {
        var cards = document.querySelectorAll('.model-card');
        var input = document.getElementById('pricing-model');

        cards.forEach(function (card) {
            card.addEventListener('click', function () {
                cards.forEach(function (c) { c.classList.remove('selected'); });
                card.classList.add('selected');
                input.value = card.dataset.model;
            });
        });

        var defaultCard = document.querySelector('.model-card[data-model="tiered"]');
        if (defaultCard) defaultCard.click();
    }

    function initCancellationPolicyCards() {
        var cards = document.querySelectorAll('.policy-card');
        var input = document.getElementById('cancellation-policy');
        var commitmentSettings = document.getElementById('commitment-settings');

        cards.forEach(function (card) {
            card.addEventListener('click', function () {
                cards.forEach(function (c) { c.classList.remove('selected'); });
                card.classList.add('selected');
                input.value = card.dataset.policy;

                if (card.dataset.policy === 'minimum_commitment') {
                    commitmentSettings.classList.remove('hidden');
                } else {
                    commitmentSettings.classList.add('hidden');
                }
            });
        });

        var defaultCard = document.querySelector('.policy-card[data-policy="end_of_period"]');
        if (defaultCard) defaultCard.click();
    }

    function initTierManagement() {
        var addBtn = document.getElementById('add-tier-btn');
        addBtn.addEventListener('click', addTier);
    }

    function addTier() {
        tierCounter++;
        var container = document.getElementById('pricing-tiers-container');
        var noTiersMsg = document.getElementById('no-tiers-message');

        if (noTiersMsg) noTiersMsg.remove();

        var tierCard = document.createElement('div');
        tierCard.className = 'tier-card';
        tierCard.dataset.tierId = tierCounter;

        tierCard.innerHTML =
            '<div class="tier-header">' +
                '<h4 class="tier-header-title">' +
                    '<i class="fas fa-tag"></i> ' + i18n.pricingTier + ' #' + tierCounter +
                '</h4>' +
                '<div class="tier-actions">' +
                    '<button type="button" class="util-btn" data-action="set-default-tier" data-tier-id="' + tierCounter + '" title="' + i18n.setDefault + '">' +
                        '<i class="fas fa-star"></i>' +
                    '</button>' +
                    '<button type="button" class="util-btn danger" data-action="remove-tier" data-tier-id="' + tierCounter + '" title="' + i18n.remove + '">' +
                        '<i class="fas fa-trash"></i>' +
                    '</button>' +
                '</div>' +
            '</div>' +
            '<div class="tier-fields">' +
                '<div class="form-group">' +
                    '<label>' + i18n.tierName + '</label>' +
                    '<input type="text" class="form-control tier-name" placeholder="' + i18n.tierNamePlaceholder + '" required>' +
                '</div>' +
                '<div class="form-group">' +
                    '<label>' + i18n.billingCycle + '</label>' +
                    '<select class="form-control tier-cycle" required>' +
                        '<option value="daily">' + i18n.daily + '</option>' +
                        '<option value="weekly">' + i18n.weekly + '</option>' +
                        '<option value="monthly" selected>' + i18n.monthly + '</option>' +
                        '<option value="quarterly">' + i18n.quarterly + '</option>' +
                        '<option value="semiannual">' + i18n.semiannual + '</option>' +
                        '<option value="annual">' + i18n.annual + '</option>' +
                    '</select>' +
                '</div>' +
                '<div class="form-group">' +
                    '<label>' + i18n.billingInterval + '</label>' +
                    '<input type="number" class="form-control tier-interval" value="1" min="1" max="24" required>' +
                    '<div class="form-help">' + i18n.billingIntervalHelp + '</div>' +
                '</div>' +
                '<div class="form-group">' +
                    '<label>' + i18n.discountPct + '</label>' +
                    '<input type="number" class="form-control tier-discount" value="0" min="0" max="100" step="0.01" required>' +
                    '<div class="form-help">' + i18n.discountHelp + '</div>' +
                '</div>' +
            '</div>';

        container.appendChild(tierCard);

        tiersData.push({ id: tierCounter, isDefault: tiersData.length === 0 });

        if (tiersData.length === 1) tierCard.classList.add('default');
    }

    window.removeTier = function (tierId) {
        tierId = parseInt(tierId, 10);
        var tierCard = document.querySelector('.tier-card[data-tier-id="' + tierId + '"]');
        if (!tierCard) return;

        var wasDefault = tierCard.classList.contains('default');
        tierCard.remove();

        tiersData = tiersData.filter(function (t) { return t.id !== tierId; });

        if (wasDefault && tiersData.length > 0) {
            var firstTierCard = document.querySelector('.tier-card');
            if (firstTierCard) {
                firstTierCard.classList.add('default');
                tiersData[0].isDefault = true;
            }
        }

        if (tiersData.length === 0) {
            var container = document.getElementById('pricing-tiers-container');
            var noTiersMsg = document.createElement('div');
            noTiersMsg.id = 'no-tiers-message';
            noTiersMsg.className = 'no-tiers-message';
            noTiersMsg.innerHTML =
                '<i class="fas fa-plus-circle no-tiers-icon"></i>' +
                '<p>' + i18n.noTiersMsg + '</p>';
            container.appendChild(noTiersMsg);
        }
    };

    window.setDefaultTier = function (tierId) {
        tierId = parseInt(tierId, 10);
        document.querySelectorAll('.tier-card').forEach(function (card) {
            card.classList.remove('default');
        });

        var tierCard = document.querySelector('.tier-card[data-tier-id="' + tierId + '"]');
        if (tierCard) tierCard.classList.add('default');

        tiersData.forEach(function (tier) {
            tier.isDefault = tier.id === tierId;
        });
    };

    function initQuantitySettings() {
        var checkbox = document.getElementById('allow-quantity');
        var settings = document.getElementById('quantity-settings');

        checkbox.addEventListener('change', function () {
            if (checkbox.checked) {
                settings.classList.remove('hidden');
            } else {
                settings.classList.add('hidden');
            }
        });
    }

    function initCommitmentSettings() {
        // Handled in initCancellationPolicyCards
    }

    function initNavigation() {
        var prevBtn = document.getElementById('prev-btn');
        var nextBtn = document.getElementById('next-btn');

        prevBtn.addEventListener('click', function () { goToStep(currentStep - 1); });
        nextBtn.addEventListener('click', function () {
            if (validateStep(currentStep)) goToStep(currentStep + 1);
        });

        document.getElementById('wizard-form').addEventListener('submit', handleSubmit);
    }

    function goToStep(step) {
        if (step < 1 || step > totalSteps) return;

        document.getElementById('step-' + currentStep).classList.add('hidden');
        document.querySelector('.step[data-step="' + currentStep + '"]').classList.remove('active', 'completed');

        if (step > currentStep) {
            document.querySelector('.step[data-step="' + currentStep + '"]').classList.add('completed');
        }

        currentStep = step;

        document.getElementById('step-' + currentStep).classList.remove('hidden');
        document.querySelector('.step[data-step="' + currentStep + '"]').classList.add('active');

        updateNavigationButtons();

        if (currentStep === 7) populateReview();

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function updateNavigationButtons() {
        var prevBtn = document.getElementById('prev-btn');
        var nextBtn = document.getElementById('next-btn');
        var submitBtn = document.getElementById('submit-btn');

        prevBtn.classList.toggle('wizard-btn-hidden', currentStep === 1);
        nextBtn.classList.toggle('wizard-btn-hidden', currentStep === totalSteps);
        submitBtn.classList.toggle('wizard-btn-hidden', currentStep !== totalSteps);
    }

    function validateStep(step) {
        var errors = [];

        if (step === 1) {
            var name = document.getElementById('plan-name').value.trim();
            if (!name) errors.push(i18n.planNameRequired);
        }

        if (step === 2) {
            if (tiersData.length === 0) {
                errors.push(i18n.tierRequired);
            } else {
                document.querySelectorAll('.tier-card').forEach(function (card) {
                    var tierName = card.querySelector('.tier-name').value.trim();
                    if (!tierName) errors.push(i18n.tierNameRequired);
                });
            }
        }

        if (errors.length > 0) {
            AdminModal.alert({message: errors.join('\n'), type: 'warning'});
            return false;
        }
        return true;
    }

    function populateReview() {
        document.getElementById('review-name').textContent = document.getElementById('plan-name').value || '-';
        document.getElementById('review-description').textContent = document.getElementById('plan-description').value || '-';

        var pricingModel = document.getElementById('pricing-model').value;
        var modelLabels = {
            'tiered': i18n.tieredPricing,
            'quantity_based': i18n.quantityBased,
            'flat': i18n.flatRate
        };
        document.getElementById('review-pricing-model').textContent = modelLabels[pricingModel] || '-';

        var tiersHtml = [];
        document.querySelectorAll('.tier-card').forEach(function (card) {
            var name = card.querySelector('.tier-name').value;
            var cycle = card.querySelector('.tier-cycle').selectedOptions[0].textContent;
            var interval = card.querySelector('.tier-interval').value;
            var discountVal = card.querySelector('.tier-discount').value;
            var isDefault = card.classList.contains('default');

            tiersHtml.push(
                '<div class="review-tier-item">' +
                    '<strong>' + name + '</strong>' +
                    (isDefault ? '<span class="review-badge review-badge-inline">' + i18n.defaultLabel + '</span>' : '') +
                    '<div class="review-tier-detail">' +
                        (interval > 1 ? i18n.every + ' ' + interval + ' ' : '') + cycle + ' \u2022 ' + discountVal + '% ' + i18n.discount +
                    '</div>' +
                '</div>'
            );
        });
        document.getElementById('review-tiers').innerHTML = tiersHtml.join('') || '-';

        var trialDays = document.getElementById('trial-period-days').value;
        document.getElementById('review-trial').textContent = trialDays > 0 ? trialDays + ' ' + i18n.days : i18n.noTrial;

        var trialPrice = document.getElementById('trial-price').value;
        document.getElementById('review-trial-price').textContent = trialPrice ? '$' + trialPrice : i18n.free;

        var setupFee = document.getElementById('setup-fee').value;
        document.getElementById('review-setup-fee').textContent = '$' + (setupFee || '0.00');

        var allowQty = document.getElementById('allow-quantity').checked;
        document.getElementById('review-allow-quantity').innerHTML = allowQty
            ? '<span class="review-badge">' + i18n.yes + '</span>'
            : i18n.no;

        document.getElementById('review-min-quantity').textContent = document.getElementById('minimum-quantity').value || '-';
        document.getElementById('review-max-quantity').textContent = document.getElementById('maximum-quantity').value || i18n.unlimited;
        document.getElementById('review-max-cycles').textContent = document.getElementById('max-billing-cycles').value || i18n.unlimited;

        var cancellationPolicy = document.getElementById('cancellation-policy').value;
        var policyLabels = {
            'anytime': i18n.cancelAnytime,
            'end_of_period': i18n.cancelAtPeriodEnd,
            'minimum_commitment': i18n.minimumCommitment
        };
        document.getElementById('review-cancellation').textContent = policyLabels[cancellationPolicy] || '-';

        var minCommitment = document.getElementById('minimum-commitment-cycles').value;
        document.getElementById('review-commitment').textContent = minCommitment > 0 ? minCommitment + ' ' + i18n.cycles : i18n.none;

        var graceDays = document.getElementById('grace-period-days').value;
        document.getElementById('review-grace').textContent = graceDays > 0 ? graceDays + ' ' + i18n.days : i18n.none;

        var reactivationDays = document.getElementById('reactivation-period-days').value;
        document.getElementById('review-reactivation').textContent = reactivationDays > 0 ? reactivationDays + ' ' + i18n.days : i18n.disabled;

        var isActive = document.getElementById('is-active').checked;
        document.getElementById('review-active').innerHTML = isActive
            ? '<span class="review-badge">' + i18n.yes + '</span>'
            : i18n.no;

        var isPublic = document.getElementById('is-public').checked;
        document.getElementById('review-public').innerHTML = isPublic
            ? '<span class="review-badge">' + i18n.yes + '</span>'
            : i18n.no;

        document.getElementById('review-sort').textContent = document.getElementById('sort-order').value || '0';
    }

    function handleSubmit(e) {
        e.preventDefault();

        var tiers = [];
        document.querySelectorAll('.tier-card').forEach(function (card) {
            tiers.push({
                tier_name: card.querySelector('.tier-name').value,
                billing_cycle: card.querySelector('.tier-cycle').value,
                billing_interval: card.querySelector('.tier-interval').value,
                discount_percentage: card.querySelector('.tier-discount').value,
                is_default: card.classList.contains('default')
            });
        });

        document.getElementById('tiers-data').value = JSON.stringify(tiers);
        e.target.submit();
    }

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) return;
        var action = btn.dataset.action;
        var tierId = btn.dataset.tierId;
        if (action === 'set-default-tier' && tierId) {
            window.setDefaultTier(tierId);
        } else if (action === 'remove-tier' && tierId) {
            window.removeTier(tierId);
        }
    });

}());
