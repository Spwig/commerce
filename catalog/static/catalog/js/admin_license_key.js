/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * License Key Admin JavaScript
 * Adds copy-to-clipboard functionality for license keys
 */

(function() {
    'use strict';

    /**
     * Initialize copy-to-clipboard for license keys
     */
    function initCopyButtons() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    }

    function init() {
        // Find all copy buttons
        const copyButtons = document.querySelectorAll('.copy-license-key');

        copyButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                const licenseKey = this.getAttribute('data-key');
                copyToClipboard(licenseKey, this);
            });
        });
    }

    /**
     * Copy text to clipboard
     */
    function copyToClipboard(text, button) {
        // Modern approach using Clipboard API
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(() => {
                showCopyFeedback(button, true);
            }).catch(err => {
                console.error('Failed to copy:', err);
                // Fallback to legacy method
                fallbackCopyToClipboard(text, button);
            });
        } else {
            // Fallback for older browsers
            fallbackCopyToClipboard(text, button);
        }
    }

    /**
     * Fallback copy method for older browsers
     */
    function fallbackCopyToClipboard(text, button) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            const successful = document.execCommand('copy');
            showCopyFeedback(button, successful);
        } catch (err) {
            console.error('Fallback: Failed to copy:', err);
            showCopyFeedback(button, false);
        }

        document.body.removeChild(textArea);
    }

    /**
     * Show visual feedback when copy is successful or fails
     */
    function showCopyFeedback(button, success) {
        const originalText = button.textContent;
        const originalBg = button.style.backgroundColor;

        if (success) {
            button.textContent = '✓';
            button.style.backgroundColor = '#28a745';
            button.style.color = 'white';

            // Restore after 2 seconds
            setTimeout(() => {
                button.textContent = originalText;
                button.style.backgroundColor = originalBg;
                button.style.color = '';
            }, 2000);
        } else {
            button.textContent = '✗';
            button.style.backgroundColor = '#dc3545';
            button.style.color = 'white';

            // Restore after 2 seconds
            setTimeout(() => {
                button.textContent = originalText;
                button.style.backgroundColor = originalBg;
                button.style.color = '';
            }, 2000);

            // Show alert as fallback
            AdminModal.alert({message: 'Failed to copy to clipboard. Please copy manually:\n\n' + button.getAttribute('data-key'), type: 'error'});
        }
    }

    // Initialize when script loads
    initCopyButtons();

})();
