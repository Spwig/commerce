/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * VoucherCode Change Form JavaScript
 * Handles code generation, conditional visibility, save buttons.
 * Tab switching is handled by the global AdminTabs utility (admin-tabs.js).
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        // AdminTabs auto-handles tab switching — no initTabs() needed
        initSaveButtons();
        initCodeGeneration();
        initConditionalVisibility();
    });

    /* =============================================
       SAVE BUTTONS
       ============================================= */

    function initSaveButtons() {
        var form = document.getElementById('vouchercode_form');
        if (!form) return;

        // Save and continue editing
        var saveContinueBtn = document.getElementById('voucher-save-continue-btn');
        if (saveContinueBtn) {
            saveContinueBtn.addEventListener('click', function() {
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = '_continue';
                input.value = '1';
                form.appendChild(input);
                form.submit();
            });
        }

        // Save and return to list
        var saveBtn = document.getElementById('voucher-save-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', function() {
                form.submit();
            });
        }
    }

    /* =============================================
       CODE GENERATION
       ============================================= */

    function initCodeGeneration() {
        var generateBtn = document.getElementById('generate-code-btn');
        if (!generateBtn) return;

        generateBtn.addEventListener('click', async function() {
            var codeInput = document.getElementById('id_code');
            if (!codeInput) return;

            // Confirm overwrite if code already has a value
            if (codeInput.value.trim()) {
                var confirmed = await AdminModal.confirm(
                    gettext('Replace existing code with a generated one?')
                );
                if (!confirmed) return;
            }

            codeInput.value = generateCode();
        });
    }

    function generateCode() {
        var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
        var segments = [];
        for (var s = 0; s < 2; s++) {
            var segment = '';
            for (var i = 0; i < 4; i++) {
                segment += chars.charAt(Math.floor(Math.random() * chars.length));
            }
            segments.push(segment);
        }
        return segments.join('-');
    }

    /* =============================================
       CONDITIONAL VISIBILITY
       ============================================= */

    function initConditionalVisibility() {
        var discountTypeSelect = document.getElementById('id_discount_type');
        var scopeSelect = document.getElementById('id_application_scope');

        if (discountTypeSelect) {
            discountTypeSelect.addEventListener('change', function() {
                updateDiscountVisibility(this.value);
                updateScopeInfoMessage();
            });
            updateDiscountVisibility(discountTypeSelect.value);
        }

        if (scopeSelect) {
            scopeSelect.addEventListener('change', function() {
                updateScopeVisibility(this.value);
                updateScopeInfoMessage();
            });
            updateScopeVisibility(scopeSelect.value);
        }

        updateScopeInfoMessage();
    }

    function updateDiscountVisibility(discountType) {
        // Max discount amount - only for percentage
        var maxDiscountSection = document.getElementById('max-discount-section');
        if (maxDiscountSection) {
            maxDiscountSection.classList.toggle('hidden', discountType !== 'percentage');
        }

        // Gift card settings - only for gift_card
        var giftCardSection = document.getElementById('gift-card-section');
        if (giftCardSection) {
            giftCardSection.classList.toggle('hidden', discountType !== 'gift_card');
        }
    }

    function updateScopeVisibility(scope) {
        // Eligible items - only for products or categories
        var eligibleSection = document.getElementById('eligible-items-section');
        if (eligibleSection) {
            eligibleSection.classList.toggle('hidden', scope === 'cart');
        }
    }

    function updateScopeInfoMessage() {
        var infoMsg = document.getElementById('scope-info-message');
        if (!infoMsg) return;

        var eligibleSection = document.getElementById('eligible-items-section');
        var giftCardSection = document.getElementById('gift-card-section');

        var eligibleVisible = eligibleSection && !eligibleSection.classList.contains('hidden');
        var giftCardVisible = giftCardSection && !giftCardSection.classList.contains('hidden');

        infoMsg.classList.toggle('hidden', eligibleVisible || giftCardVisible);
    }

})();
