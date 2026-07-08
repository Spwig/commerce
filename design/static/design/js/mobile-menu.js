/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Mobile Menu Toggle
 * Reusable module for mobile menu functionality
 *
 * Usage: Auto-initializes on DOMContentLoaded
 * Manual: new MobileMenuToggle(toggleButton, menuElement)
 *
 * Follows rules_llm.md: Class-based, no inline JS
 */
class MobileMenuToggle {
    constructor(toggle, menu) {
        this.toggle = toggle;
        this.menu = menu;
        this.closeBtn = menu.querySelector('[data-menu-close]');
        this.isOpen = false;

        this.init();
    }

    init() {
        // Toggle button click
        this.toggle.addEventListener('click', () => this.toggleMenu());

        // Close button click
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }

        // Escape key closes menu
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen) {
                this.close();
                this.toggle.focus();
            }
        });

        // Click on backdrop closes menu
        this.menu.addEventListener('click', (e) => {
            if (e.target === this.menu) {
                this.close();
            }
        });
    }

    open() {
        this.isOpen = true;
        this.menu.classList.add('is-open');
        this.menu.setAttribute('aria-hidden', 'false');
        this.toggle.setAttribute('aria-expanded', 'true');
        document.body.classList.add('menu-open');
    }

    close() {
        this.isOpen = false;
        this.menu.classList.remove('is-open');
        this.menu.setAttribute('aria-hidden', 'true');
        this.toggle.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('menu-open');
    }

    toggleMenu() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }
}

// Auto-initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.querySelector('[data-menu-toggle]');
    const menu = document.querySelector('[data-mobile-menu]') || document.getElementById('mobile-menu');

    if (toggle && menu) {
        new MobileMenuToggle(toggle, menu);
    }
});
