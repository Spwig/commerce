/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin Badge Refresh
 * Polls the badge API endpoint to keep sidebar badge counts current
 * without requiring a full page reload.
 */
(function() {
    'use strict';

    var REFRESH_INTERVAL = 60000; // 60 seconds
    var BADGE_API_URL = '/api/core/badges/';
    var INITIAL_DELAY = 5000; // 5 seconds after page load

    // Badge key -> CSS severity class mapping
    var BADGE_SEVERITY = {
        orders_new: 'primary',
        carts_abandoned: 'warning',
        shipments_pending: 'info',
        returns_pending: 'danger',
        reviews_pending: 'warning',
        messages_unread: 'primary',
        emails_failed: 'danger',
        payments_failed: 'danger',
        feed_errors: 'danger',
        forms_submitted: 'primary',
        low_stock: 'warning',
        design_updates: 'info',
        component_updates: 'warning',
        hotfix_available: 'danger',
        bookings_pending: 'danger',
        subscriptions_past_due: 'danger',
        loyalty_redemptions_pending: 'warning',
        affiliate_payouts_pending: 'warning',
        sms_failed: 'danger',
        translations_failed: 'danger',
        blog_drafts: 'info'
    };

    function updateBadges(badges) {
        document.querySelectorAll('[data-badge-key]').forEach(function(menuItem) {
            var key = menuItem.getAttribute('data-badge-key');
            var count = badges[key];
            var badgeEl = menuItem.querySelector('.menu-badge:not([data-rollup])');

            if (count && count > 0) {
                if (!badgeEl) {
                    badgeEl = document.createElement('span');
                    var severity = BADGE_SEVERITY[key] || 'primary';
                    badgeEl.className = 'menu-badge menu-badge-' + severity;
                    menuItem.appendChild(badgeEl);
                }
                badgeEl.textContent = count > 99 ? '99+' : count;
                badgeEl.style.display = '';
            } else if (badgeEl) {
                badgeEl.style.display = 'none';
            }
        });

        // Re-trigger badge rollup after updating counts
        if (typeof window.initializeBadgeRollup === 'function') {
            // Remove existing rollup badges first
            document.querySelectorAll('[data-rollup="true"]').forEach(function(el) {
                el.remove();
            });
            window.initializeBadgeRollup();
        }
    }

    function refreshBadges() {
        var headers = { 'X-Requested-With': 'XMLHttpRequest' };

        fetch(BADGE_API_URL, {
            method: 'GET',
            headers: headers,
            credentials: 'same-origin'
        })
        .then(function(response) {
            if (!response.ok) throw new Error('Badge refresh failed');
            return response.json();
        })
        .then(function(data) {
            if (data.badges) {
                updateBadges(data.badges);
            }
        })
        .catch(function() {
            // Silent failure - badges just won't update this cycle
        });
    }

    // Start polling after page load
    document.addEventListener('DOMContentLoaded', function() {
        // Only on admin pages with sidebar
        if (!document.getElementById('sidebar')) return;

        setTimeout(function() {
            setInterval(refreshBadges, REFRESH_INTERVAL);
        }, INITIAL_DELAY);
    });

    // Expose for manual refresh (e.g., after completing an action)
    window.SpwigBadgeRefresh = { refresh: refreshBadges };
})();
