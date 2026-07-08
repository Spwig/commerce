/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * VoucherCodeDisplay - Voucher copy-to-clipboard functionality
 * Handles clipboard operations and toast notifications for voucher codes
 */
class VoucherCodeDisplay {
    constructor(element) {
        this.element = element;
        this.toast = element.querySelector('.voucher-display__toast');
        this.copyButtons = element.querySelectorAll('.voucher-display__copy');

        if (this.copyButtons.length === 0) {
            return;
        }

        this.init();
    }

    /**
     * Initialize copy functionality for all buttons
     */
    init() {
        this.copyButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleCopy(e, btn));
        });
    }

    /**
     * Handle copy button click
     */
    async handleCopy(e, btn) {
        e.preventDefault();
        const code = btn.dataset.code;

        if (!code) return;

        try {
            await navigator.clipboard.writeText(code);
            this.showCopySuccess(btn);
        } catch (err) {
            // Fallback for older browsers
            this.fallbackCopy(code);
            this.showCopySuccess(btn);
        }
    }

    /**
     * Fallback copy method for browsers without clipboard API
     */
    fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }

    /**
     * Show copy success feedback
     */
    showCopySuccess(btn) {
        btn.classList.add('copied');

        if (this.toast) {
            this.toast.classList.add('show');
        }

        setTimeout(() => {
            btn.classList.remove('copied');
            if (this.toast) {
                this.toast.classList.remove('show');
            }
        }, 2000);
    }
}

/**
 * Initialize all voucher code display elements on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-voucher-code-display]').forEach(element => {
        new VoucherCodeDisplay(element);
    });
});

// Export for manual initialization
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoucherCodeDisplay;
}
