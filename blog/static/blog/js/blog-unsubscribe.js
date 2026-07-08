/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Blog Unsubscribe Confirm Page
 * Appends the optional reason query parameter to the unsubscribe link.
 * Replaces inline <script> block in unsubscribe_confirm.html.
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        var btn = document.getElementById('confirm-unsubscribe-btn');
        var textarea = document.getElementById('unsubscribe-reason');
        if (!btn || !textarea) return;

        btn.addEventListener('click', function(e) {
            var reason = textarea.value.trim();
            if (reason) {
                e.preventDefault();
                window.location.href = btn.href + '&reason=' + encodeURIComponent(reason);
            }
        });
    });
})();
