/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Media Asset Admin
 * Tab switching handled by global AdminTabs utility.
 */

(function() {
    // Ensure translation adapter initializes
    window.addEventListener('load', function() {
        if (window.MediaTranslationAdapter) {
            // Translation adapter already initialized
        } else if (window.initializeMediaTranslations) {
            window.initializeMediaTranslations();
        }
    });
})();
