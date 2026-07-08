/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * FaqAccordion - Collapsible FAQ section handler
 * Handles expand/collapse behavior with optional animations
 */
class FaqAccordion {
    constructor(element) {
        this.element = element;
        this.config = this.parseConfig();
        this.items = element.querySelectorAll('.faq-accordion__item');

        if (this.items.length === 0) {
            return;
        }

        this.init();
    }

    parseConfig() {
        return {
            behavior: this.element.dataset.behavior || 'single',
            animate: this.element.dataset.animate !== 'false'
        };
    }

    init() {
        this.items.forEach(item => {
            const button = item.querySelector('.faq-accordion__question');

            if (button) {
                button.addEventListener('click', () => this.handleItemClick(item));
            }
        });
    }

    handleItemClick(item) {
        const isOpen = item.classList.contains('faq-accordion__item--open');

        // Close others if single behavior
        if (this.config.behavior === 'single' && !isOpen) {
            this.items.forEach(otherItem => {
                if (otherItem !== item && otherItem.classList.contains('faq-accordion__item--open')) {
                    this.closeItem(otherItem);
                }
            });
        }

        // Toggle current
        if (isOpen) {
            this.closeItem(item);
        } else {
            this.openItem(item);
        }
    }

    openItem(item) {
        const button = item.querySelector('.faq-accordion__question');
        const answer = item.querySelector('.faq-accordion__answer');

        if (!answer) return;

        item.classList.add('faq-accordion__item--open');
        button.setAttribute('aria-expanded', 'true');
        answer.hidden = false;

        if (this.config.animate) {
            answer.style.maxHeight = '0';
            answer.style.opacity = '0';
            requestAnimationFrame(() => {
                answer.style.maxHeight = answer.scrollHeight + 'px';
                answer.style.opacity = '1';
            });
        }
    }

    closeItem(item) {
        const button = item.querySelector('.faq-accordion__question');
        const answer = item.querySelector('.faq-accordion__answer');

        if (!answer) return;

        item.classList.remove('faq-accordion__item--open');
        button.setAttribute('aria-expanded', 'false');

        if (this.config.animate) {
            answer.style.maxHeight = answer.scrollHeight + 'px';
            requestAnimationFrame(() => {
                answer.style.maxHeight = '0';
                answer.style.opacity = '0';
                setTimeout(() => {
                    answer.hidden = true;
                    answer.style.maxHeight = '';
                    answer.style.opacity = '';
                }, 300);
            });
        } else {
            answer.hidden = true;
        }
    }
}

// Self-initialize: Find all FAQ accordion elements and create instances
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-faq-accordion]').forEach(element => {
        new FaqAccordion(element);
    });
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FaqAccordion;
}
