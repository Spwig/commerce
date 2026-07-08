/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Account Dashboard Page
 * Handles referral code copy-to-clipboard.
 * Replaces inline onclick="copyReferralCode('...')".
 *
 * Usage: <button data-action="copy-referral-code" data-code="ABC123" data-success-msg="Copied!">
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        // Copy referral/affiliate code
        document.addEventListener('click', function(e) {
            var btn = e.target.closest('[data-action="copy-referral-code"]');
            if (!btn) return;

            var code = btn.dataset.code || '';
            var successMsg = btn.dataset.successMsg || 'Referral code copied to clipboard!';

            navigator.clipboard.writeText(code).then(function() {
                AdminModal.toast(successMsg, 'success');
            }).catch(function(err) {
                console.error('Failed to copy:', err);
            });
        });

        // Apply dynamic background colors from data-color attributes
        document.querySelectorAll('[data-color]').forEach(function(el) {
            var color = el.dataset.color;
            if (color) {
                el.style.backgroundColor = color;
            }
        });
    });
})();
