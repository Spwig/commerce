/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Menu Keyboard Navigation
 * Provides accessible arrow key navigation for menu widgets
 *
 * Usage: Auto-initializes on DOMContentLoaded for all .widget-menu elements
 * Manual: new MenuKeyboardNav(menuElement)
 */
class MenuKeyboardNav {
    constructor(menuElement) {
        this.menu = menuElement;
        this.items = [];
        this.currentIndex = -1;
        this.isHorizontal = false;

        this.init();
    }

    init() {
        // Get all top-level menu links
        this.items = Array.from(this.menu.querySelectorAll('.menu-list > .menu-item > .menu-link'));
        this.isHorizontal = this.menu.querySelector('.menu-horizontal') !== null;

        // Add keyboard event listener
        this.menu.addEventListener('keydown', this.handleKeydown.bind(this));

        // Track focus for current index
        this.items.forEach((item, index) => {
            item.addEventListener('focus', () => {
                this.currentIndex = index;
            });
        });

        // Handle dropdown expansion via click for touch devices
        this.menu.querySelectorAll('.has-dropdown > .menu-link').forEach(link => {
            link.addEventListener('click', (e) => {
                const item = link.closest('.has-dropdown');
                // Only toggle on mobile or when clicking the chevron
                if (window.innerWidth < 768 || e.target.classList.contains('menu-chevron')) {
                    e.preventDefault();
                    this.toggleDropdown(item);
                }
            });
        });
    }

    handleKeydown(e) {
        const target = e.target;
        const isInDropdown = target.closest('.dropdown-menu') !== null;

        switch(e.key) {
            case 'ArrowRight':
                if (this.isHorizontal && !isInDropdown) {
                    e.preventDefault();
                    this.moveFocus(1);
                }
                break;

            case 'ArrowLeft':
                if (this.isHorizontal && !isInDropdown) {
                    e.preventDefault();
                    this.moveFocus(-1);
                }
                break;

            case 'ArrowDown':
                e.preventDefault();
                if (this.isHorizontal && !isInDropdown) {
                    // Open dropdown and focus first item
                    this.openDropdown(target);
                } else {
                    // Move within dropdown or vertical menu
                    this.moveDropdownFocus(target, 1);
                }
                break;

            case 'ArrowUp':
                e.preventDefault();
                if (isInDropdown) {
                    this.moveDropdownFocus(target, -1);
                } else if (!this.isHorizontal) {
                    this.moveFocus(-1);
                }
                break;

            case 'Escape':
                e.preventDefault();
                this.closeAllDropdowns();
                // Return focus to the parent menu item
                if (isInDropdown) {
                    const parentItem = target.closest('.has-dropdown');
                    if (parentItem) {
                        parentItem.querySelector('.menu-link').focus();
                    }
                }
                break;

            case 'Enter':
            case ' ':
                if (target.closest('.has-dropdown') && target.classList.contains('menu-link')) {
                    const item = target.closest('.has-dropdown');
                    const isExpanded = item.classList.contains('expanded');

                    // If has dropdown, toggle it
                    if (!isExpanded) {
                        e.preventDefault();
                        this.toggleDropdown(item);
                    }
                    // If expanded and Enter, allow navigation
                }
                break;

            case 'Tab':
                // Close dropdowns when tabbing away
                if (!e.shiftKey) {
                    const lastItem = this.items[this.items.length - 1];
                    if (target === lastItem || target.closest('.menu-item') === lastItem.closest('.menu-item')) {
                        this.closeAllDropdowns();
                    }
                }
                break;

            case 'Home':
                e.preventDefault();
                this.focusFirst();
                break;

            case 'End':
                e.preventDefault();
                this.focusLast();
                break;
        }
    }

    moveFocus(direction) {
        const newIndex = this.currentIndex + direction;

        if (newIndex >= 0 && newIndex < this.items.length) {
            this.currentIndex = newIndex;
            this.items[this.currentIndex].focus();
        }
    }

    moveDropdownFocus(currentTarget, direction) {
        const dropdown = currentTarget.closest('.dropdown-menu') ||
                        currentTarget.closest('.has-dropdown')?.querySelector('.dropdown-menu');

        if (!dropdown) return;

        const links = Array.from(dropdown.querySelectorAll('a'));
        const currentIdx = links.indexOf(currentTarget);
        const newIdx = currentIdx + direction;

        if (newIdx >= 0 && newIdx < links.length) {
            links[newIdx].focus();
        } else if (direction < 0 && currentIdx === 0) {
            // At top of dropdown, go back to parent
            const parentLink = dropdown.closest('.has-dropdown')?.querySelector('.menu-link');
            if (parentLink) {
                parentLink.focus();
            }
        }
    }

    openDropdown(trigger) {
        const item = trigger.closest('.has-dropdown');
        if (!item) return;

        // Expand the dropdown
        item.classList.add('expanded');

        // Update ARIA
        const link = item.querySelector('.menu-link');
        if (link) {
            link.setAttribute('aria-expanded', 'true');
        }

        // Focus first dropdown link
        const firstDropdownLink = item.querySelector('.dropdown-menu a');
        if (firstDropdownLink) {
            firstDropdownLink.focus();
        }
    }

    toggleDropdown(item) {
        const isExpanded = item.classList.contains('expanded');

        // Close other dropdowns first
        this.menu.querySelectorAll('.has-dropdown.expanded').forEach(openItem => {
            if (openItem !== item) {
                openItem.classList.remove('expanded');
                const link = openItem.querySelector('.menu-link');
                if (link) {
                    link.setAttribute('aria-expanded', 'false');
                }
            }
        });

        // Toggle this dropdown
        item.classList.toggle('expanded');

        // Update ARIA
        const link = item.querySelector('.menu-link');
        if (link) {
            link.setAttribute('aria-expanded', !isExpanded ? 'true' : 'false');
        }

        // Focus first item if opening
        if (!isExpanded) {
            const firstDropdownLink = item.querySelector('.dropdown-menu a');
            if (firstDropdownLink) {
                setTimeout(() => firstDropdownLink.focus(), 10);
            }
        }
    }

    closeAllDropdowns() {
        this.menu.querySelectorAll('.has-dropdown.expanded').forEach(item => {
            item.classList.remove('expanded');
            const link = item.querySelector('.menu-link');
            if (link) {
                link.setAttribute('aria-expanded', 'false');
            }
        });
    }

    focusFirst() {
        if (this.items.length > 0) {
            this.currentIndex = 0;
            this.items[0].focus();
        }
    }

    focusLast() {
        if (this.items.length > 0) {
            this.currentIndex = this.items.length - 1;
            this.items[this.currentIndex].focus();
        }
    }
}

/**
 * Current Page Detection
 * Automatically adds aria-current="page" to menu items matching current URL
 */
function markCurrentPageItems() {
    const currentPath = window.location.pathname;
    const currentUrl = window.location.href;

    document.querySelectorAll('.widget-menu a').forEach(link => {
        const href = link.getAttribute('href');
        if (!href || href === '#') return;

        // Check for exact match or path match
        try {
            const linkUrl = new URL(href, window.location.origin);
            if (linkUrl.pathname === currentPath || linkUrl.href === currentUrl) {
                link.setAttribute('aria-current', 'page');
            }
        } catch (e) {
            // Invalid URL, skip
        }
    });
}

/**
 * Auto-initialize on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize keyboard navigation for all menus
    document.querySelectorAll('.widget-menu').forEach(menu => {
        new MenuKeyboardNav(menu);
    });

    // Mark current page items
    markCurrentPageItems();
});

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { MenuKeyboardNav, markCurrentPageItems };
}
