/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin Base JavaScript
 * =====================================
 * Reusable components and utilities for Django admin interface
 *
 * Components:
 * - SearchableSelect: Searchable dropdown with Font Awesome icon support
 * ===================================== */

/**
 * SearchableSelect Component
 *
 * Converts a standard HTML select element into a searchable dropdown with:
 * - Live search filtering
 * - Font Awesome icon support (from data-icon attributes)
 * - Optgroup support with sticky headers
 * - Keyboard navigation
 * - Theme-aware styling
 * - Clean single-element UI (replaces original select entirely)
 *
 * Usage:
 *   <select data-searchable-select data-placeholder="Search...">
 *     <optgroup label="Popular">
 *       <option value="USD" data-icon="fa-dollar-sign" data-icon-style="fas">US Dollar (USD)</option>
 *     </optgroup>
 *   </select>
 *
 * Or initialize programmatically:
 *   new SearchableSelect('#my-select', {
 *       placeholder: 'Search...',
 *       noResultsText: 'No matches found'
 *   });
 */
class SearchableSelect {
    constructor(selectElement, options = {}) {
        this.selectElement = typeof selectElement === 'string'
            ? document.querySelector(selectElement)
            : selectElement;

        if (!this.selectElement) {
            console.error('SearchableSelect: Element not found');
            return;
        }

        this.options = {
            placeholder: options.placeholder || selectElement.getAttribute('data-placeholder') || 'Search...',
            noResultsText: options.noResultsText || 'No results found',
            onChange: options.onChange || null
        };

        this.isOpen = false;
        this.selectedValue = this.selectElement.value;
        this.selectedIcon = null;
        this.selectedIconStyle = 'fas';
        this.allOptions = [];

        this.init();
    }

    init() {
        // Parse options from original select (including icon data)
        this.parseOptions();

        // Create wrapper structure and replace original select
        this.createWrapper();

        // Bind events
        this.bindEvents();

        // Set initial value
        this.updateDisplay();
    }

    parseOptions() {
        const select = this.selectElement;
        this.allOptions = [];

        // Handle optgroups
        const optgroups = select.querySelectorAll('optgroup');
        if (optgroups.length > 0) {
            optgroups.forEach(optgroup => {
                const groupLabel = optgroup.label;
                const options = [];

                optgroup.querySelectorAll('option').forEach(option => {
                    options.push({
                        value: option.value,
                        text: option.textContent.trim(),
                        selected: option.selected,
                        group: groupLabel,
                        icon: option.getAttribute('data-icon') || null,
                        iconStyle: option.getAttribute('data-icon-style') || 'fas'
                    });

                    // Store selected option icon
                    if (option.selected && option.getAttribute('data-icon')) {
                        this.selectedIcon = option.getAttribute('data-icon');
                        this.selectedIconStyle = option.getAttribute('data-icon-style') || 'fas';
                    }
                });

                this.allOptions.push({
                    isGroup: true,
                    label: groupLabel,
                    options: options
                });
            });
        } else {
            // Handle flat options
            const options = [];
            select.querySelectorAll('option').forEach(option => {
                if (option.value) {  // Skip empty options
                    options.push({
                        value: option.value,
                        text: option.textContent.trim(),
                        selected: option.selected,
                        icon: option.getAttribute('data-icon') || null,
                        iconStyle: option.getAttribute('data-icon-style') || 'fas'
                    });

                    // Store selected option icon
                    if (option.selected && option.getAttribute('data-icon')) {
                        this.selectedIcon = option.getAttribute('data-icon');
                        this.selectedIconStyle = option.getAttribute('data-icon-style') || 'fas';
                    }
                }
            });

            this.allOptions.push({
                isGroup: false,
                options: options
            });
        }
    }

    createWrapper() {
        // Create hidden input to replace original select (for form submission)
        this.hiddenInput = document.createElement('input');
        this.hiddenInput.type = 'hidden';
        this.hiddenInput.name = this.selectElement.name;
        this.hiddenInput.id = this.selectElement.id;
        this.hiddenInput.value = this.selectedValue;

        // Create wrapper div
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'searchable-select-wrapper';

        // Create value display (main clickable button showing current selection)
        this.createValueDisplay();

        // Create search input (shown when dropdown is open)
        this.searchInput = document.createElement('input');
        this.searchInput.type = 'text';
        this.searchInput.className = 'searchable-select-search';
        this.searchInput.placeholder = this.options.placeholder;
        this.searchInput.autocomplete = 'off';
        this.searchInput.style.display = 'none';

        // Create dropdown (appended to body to avoid overflow issues)
        this.dropdown = document.createElement('div');
        this.dropdown.className = 'searchable-select-dropdown';

        // Assemble wrapper (without dropdown - it goes to body)
        this.wrapper.appendChild(this.hiddenInput);
        this.wrapper.appendChild(this.valueDisplay);
        this.wrapper.appendChild(this.searchInput);

        // Replace original select entirely
        const parent = this.selectElement.parentNode;
        parent.replaceChild(this.wrapper, this.selectElement);

        // Append dropdown to body to avoid overflow constraints
        document.body.appendChild(this.dropdown);
    }

    createValueDisplay() {
        // Main button showing current selected value
        this.valueDisplay = document.createElement('div');
        this.valueDisplay.className = 'searchable-select-value-display';
        this.valueDisplay.tabIndex = 0; // Make focusable

        // Icon container
        this.valueIcon = document.createElement('span');
        this.valueIcon.className = 'searchable-select-value-icon';

        // Text container
        this.valueText = document.createElement('span');
        this.valueText.className = 'searchable-select-value-text';

        // Chevron indicator
        this.chevron = document.createElement('span');
        this.chevron.className = 'searchable-select-chevron';
        const chevronIcon = document.createElement('i');
        chevronIcon.className = 'fas fa-chevron-down';
        this.chevron.appendChild(chevronIcon);

        // Assemble value display
        this.valueDisplay.appendChild(this.valueIcon);
        this.valueDisplay.appendChild(this.valueText);
        this.valueDisplay.appendChild(this.chevron);
    }

    bindEvents() {
        // Value display click - toggle dropdown
        this.valueDisplay.addEventListener('click', (e) => {
            e.preventDefault();
            this.toggle();
        });

        // Value display keyboard - open on Enter or Space
        this.valueDisplay.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.toggle();
            }
        });

        // Search input typing
        this.searchInput.addEventListener('input', (e) => {
            this.filter(e.target.value);
        });

        // Search input keyboard navigation
        this.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.close();
            }
        });

        // Close on outside click
        this.outsideClickHandler = (e) => {
            if (!this.wrapper.contains(e.target) && !this.dropdown.contains(e.target)) {
                this.close();
            }
        };
        document.addEventListener('click', this.outsideClickHandler);

        // Reposition dropdown on scroll/resize
        this.repositionHandler = () => {
            if (this.isOpen) {
                this.positionDropdown();
            }
        };
        window.addEventListener('scroll', this.repositionHandler, true);
        window.addEventListener('resize', this.repositionHandler);
    }

    toggle() {
        if (this.isOpen) {
            this.close();
        } else {
            this.open();
        }
    }

    open() {
        this.isOpen = true;
        this.wrapper.classList.add('open');
        this.valueDisplay.style.display = 'none';
        this.searchInput.style.display = 'block';
        this.searchInput.focus();
        this.renderOptions();
        this.positionDropdown();
    }

    close() {
        this.isOpen = false;
        this.wrapper.classList.remove('open');
        this.searchInput.style.display = 'none';
        this.searchInput.value = '';
        this.valueDisplay.style.display = 'flex';
        this.dropdown.style.display = 'none';
    }

    positionDropdown() {
        // Position dropdown using fixed positioning to break out of overflow constraints
        const rect = this.wrapper.getBoundingClientRect();

        this.dropdown.style.position = 'fixed';
        this.dropdown.style.top = `${rect.bottom + 6}px`;
        this.dropdown.style.left = `${rect.left}px`;
        this.dropdown.style.width = `${rect.width}px`;
        this.dropdown.style.display = 'block';
    }

    filter(searchTerm) {
        this.renderOptions(searchTerm);
    }

    renderOptions(searchTerm = '') {
        this.dropdown.innerHTML = '';
        const term = searchTerm.toLowerCase();
        let hasResults = false;

        this.allOptions.forEach(group => {
            const filteredOptions = group.options.filter(opt =>
                opt.text.toLowerCase().includes(term) ||
                opt.value.toLowerCase().includes(term)
            );

            if (filteredOptions.length === 0) return;
            hasResults = true;

            // Add group label if exists
            if (group.isGroup) {
                const groupLabel = document.createElement('div');
                groupLabel.className = 'searchable-select-group-label';
                groupLabel.textContent = group.label;
                this.dropdown.appendChild(groupLabel);
            }

            // Add options with icons
            filteredOptions.forEach(option => {
                const optionDiv = document.createElement('div');
                optionDiv.className = 'searchable-select-option';
                optionDiv.dataset.value = option.value;

                // Add icon if present (supports both Font Awesome icons and image URLs)
                if (option.icon) {
                    const iconSpan = document.createElement('span');
                    iconSpan.className = 'searchable-select-option-icon';

                    // Check if icon is an image URL (starts with / or http)
                    if (option.icon.startsWith('/') || option.icon.startsWith('http')) {
                        const img = document.createElement('img');
                        img.src = option.icon;
                        img.alt = '';
                        img.style.width = '20px';
                        img.style.height = '15px';
                        img.style.objectFit = 'contain';
                        iconSpan.appendChild(img);
                    } else {
                        // Font Awesome icon
                        const icon = document.createElement('i');
                        icon.className = `${option.iconStyle} ${option.icon}`;
                        iconSpan.appendChild(icon);
                    }

                    optionDiv.appendChild(iconSpan);
                }

                // Add text
                const textSpan = document.createElement('span');
                textSpan.className = 'searchable-select-option-text';
                textSpan.textContent = option.text;
                optionDiv.appendChild(textSpan);

                // Mark as selected
                if (option.value === this.selectedValue) {
                    optionDiv.classList.add('selected');
                }

                // Click handler
                optionDiv.addEventListener('click', () => {
                    this.selectOption(option.value, option.text, option.icon, option.iconStyle);
                });

                this.dropdown.appendChild(optionDiv);
            });
        });

        // Show "no results" if nothing found
        if (!hasResults) {
            const noResults = document.createElement('div');
            noResults.className = 'searchable-select-no-results';
            noResults.textContent = this.options.noResultsText;
            this.dropdown.appendChild(noResults);
        }
    }

    selectOption(value, text, icon, iconStyle) {
        this.selectedValue = value;
        this.selectedIcon = icon;
        this.selectedIconStyle = iconStyle || 'fas';

        // Update hidden input
        this.hiddenInput.value = value;

        // Trigger change event for Django admin
        const event = new Event('change', { bubbles: true });
        this.hiddenInput.dispatchEvent(event);

        // Update display
        this.updateDisplay();

        // Call custom onChange if provided
        if (this.options.onChange) {
            this.options.onChange(value, text);
        }

        this.close();
    }

    updateDisplay() {
        // Update value display with selected option
        const selectedOption = this.getSelectedOption();

        if (selectedOption) {
            // Update icon (supports both Font Awesome icons and image URLs)
            this.valueIcon.innerHTML = '';
            if (selectedOption.icon) {
                // Check if icon is an image URL (starts with / or http)
                if (selectedOption.icon.startsWith('/') || selectedOption.icon.startsWith('http')) {
                    const img = document.createElement('img');
                    img.src = selectedOption.icon;
                    img.alt = '';
                    img.style.width = '20px';
                    img.style.height = '15px';
                    img.style.objectFit = 'contain';
                    this.valueIcon.appendChild(img);
                } else {
                    // Font Awesome icon
                    const icon = document.createElement('i');
                    icon.className = `${selectedOption.iconStyle} ${selectedOption.icon}`;
                    this.valueIcon.appendChild(icon);
                }
            }

            // Update text
            this.valueText.textContent = selectedOption.text;
        } else {
            // No selection
            this.valueIcon.innerHTML = '';
            this.valueText.textContent = this.options.placeholder;
        }
    }

    getSelectedOption() {
        for (const group of this.allOptions) {
            for (const option of group.options) {
                if (option.value === this.selectedValue) {
                    return option;
                }
            }
        }
        return null;
    }

    destroy() {
        // Clean up event listeners
        document.removeEventListener('click', this.outsideClickHandler);
        window.removeEventListener('scroll', this.repositionHandler, true);
        window.removeEventListener('resize', this.repositionHandler);

        // Remove DOM elements
        this.dropdown.remove();
        this.wrapper.remove();
    }
}

/**
 * SlugGenerator Component
 * =====================================
 * Automatically generates URL-friendly slugs from name/title fields
 *
 * Features:
 * - Live slug generation as user types
 * - Lock/unlock mechanism (manual override)
 * - Visual indicators for auto vs manual mode
 * - Progressive enhancement (works with Django's prepopulated_fields)
 * - Supports international characters with transliteration
 *
 * Usage:
 *   Auto-initialized on DOMContentLoaded for all fields with name ending in 'slug'
 *
 *   Or initialize manually:
 *   new SlugGenerator('#id_slug', '#id_name');
 */
class SlugGenerator {
    constructor(slugFieldSelector, sourceFieldSelector = null) {
        this.slugField = typeof slugFieldSelector === 'string'
            ? document.querySelector(slugFieldSelector)
            : slugFieldSelector;

        if (!this.slugField) {
            console.error('SlugGenerator: Slug field not found');
            return;
        }

        // Auto-detect source field if not provided
        if (!sourceFieldSelector) {
            this.sourceField = this.detectSourceField();
        } else {
            this.sourceField = typeof sourceFieldSelector === 'string'
                ? document.querySelector(sourceFieldSelector)
                : sourceFieldSelector;
        }

        if (!this.sourceField) {
            console.warn('SlugGenerator: Source field not found, auto-generation disabled');
            return;
        }

        // State
        this.isLocked = false;  // false = auto-generate, true = manual mode
        this.hasUserEdit = false;  // Track if user has manually edited slug

        this.init();
    }

    init() {
        // Check if slug field already has a value
        if (this.slugField.value.trim()) {
            // Assume user wants manual control if editing existing record
            this.isLocked = true;
            this.hasUserEdit = true;
        }

        // Create UI elements
        this.createToggleButton();
        this.updateVisualState();

        // Bind events
        this.bindEvents();
    }

    detectSourceField() {
        // Look for common field names: name, title
        const possibleSelectors = ['#id_name', '#id_title', '[name="name"]', '[name="title"]'];

        for (const selector of possibleSelectors) {
            const field = document.querySelector(selector);
            if (field) {
                return field;
            }
        }

        return null;
    }

    createToggleButton() {
        // Create toggle button container
        this.toggleContainer = document.createElement('div');
        this.toggleContainer.className = 'slug-generator-toggle';
        this.toggleContainer.title = 'Toggle auto-generation';

        // Create lock icon
        this.lockIcon = document.createElement('i');
        this.updateLockIcon();

        // Create status text
        this.statusText = document.createElement('span');
        this.statusText.className = 'slug-generator-status-text';

        this.toggleContainer.appendChild(this.lockIcon);
        this.toggleContainer.appendChild(this.statusText);

        // Insert after slug field
        const slugFieldParent = this.slugField.parentElement;
        slugFieldParent.style.position = 'relative';
        slugFieldParent.appendChild(this.toggleContainer);
    }

    updateLockIcon() {
        if (this.isLocked) {
            this.lockIcon.className = 'fas fa-lock slug-generator-icon locked';
        } else {
            this.lockIcon.className = 'fas fa-magic slug-generator-icon unlocked';
        }
    }

    updateVisualState() {
        this.updateLockIcon();

        if (this.isLocked) {
            this.statusText.textContent = 'Manual';
            this.toggleContainer.classList.add('locked');
            this.toggleContainer.classList.remove('unlocked');
            this.slugField.classList.add('slug-manual');
            this.slugField.classList.remove('slug-auto');
        } else {
            this.statusText.textContent = 'Auto';
            this.toggleContainer.classList.add('unlocked');
            this.toggleContainer.classList.remove('locked');
            this.slugField.classList.add('slug-auto');
            this.slugField.classList.remove('slug-manual');
        }
    }

    bindEvents() {
        // Source field input - generate slug if not locked
        this.sourceField.addEventListener('input', () => {
            if (!this.isLocked) {
                this.generateSlug();
            }
        });

        // Slug field input - detect manual edit
        this.slugField.addEventListener('input', () => {
            if (!this.hasUserEdit) {
                // User is manually editing, switch to locked mode
                this.isLocked = true;
                this.hasUserEdit = true;
                this.updateVisualState();
            }
        });

        // Toggle button click - switch between auto/manual
        this.toggleContainer.addEventListener('click', () => {
            this.isLocked = !this.isLocked;

            // If switching to auto mode, generate slug immediately
            if (!this.isLocked) {
                this.generateSlug();
            }

            this.updateVisualState();
        });

        // Keyboard support for toggle
        this.toggleContainer.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.isLocked = !this.isLocked;

                if (!this.isLocked) {
                    this.generateSlug();
                }

                this.updateVisualState();
            }
        });
    }

    generateSlug() {
        const sourceValue = this.sourceField.value;

        if (!sourceValue) {
            this.slugField.value = '';
            return;
        }

        // Use Django's URLify if available (loaded in Django admin)
        if (typeof URLify !== 'undefined') {
            this.slugField.value = URLify(sourceValue, 255, true);
        } else {
            // Fallback slugify implementation
            this.slugField.value = this.slugify(sourceValue);
        }

        // Trigger change event for any listeners
        const event = new Event('change', { bubbles: true });
        this.slugField.dispatchEvent(event);
    }

    slugify(text) {
        // Fallback slugify implementation if Django's URLify is not available
        return text
            .toString()
            .toLowerCase()
            .trim()
            // Replace spaces with hyphens
            .replace(/\s+/g, '-')
            // Remove all non-word chars (keep letters, numbers, hyphens)
            .replace(/[^\w\-]+/g, '')
            // Replace multiple hyphens with single hyphen
            .replace(/\-\-+/g, '-')
            // Remove leading/trailing hyphens
            .replace(/^-+/, '')
            .replace(/-+$/, '');
    }

    destroy() {
        // Clean up
        if (this.toggleContainer) {
            this.toggleContainer.remove();
        }
    }
}

/**
 * Auto-initialize SlugGenerator for all slug fields
 */
function initializeSlugGenerators() {
    // Find all input fields ending with 'slug' in their name
    const slugFields = document.querySelectorAll('input[type="text"][name$="slug"]');

    slugFields.forEach(slugField => {
        // Skip if already initialized
        if (slugField.dataset.slugGeneratorInitialized) {
            return;
        }

        // Mark as initialized
        slugField.dataset.slugGeneratorInitialized = 'true';

        // Create slug generator
        new SlugGenerator(slugField);
    });
}

/**
 * Submenu Toggle Functions
 * =====================================
 * Handles collapsible sub-menus in the admin sidebar
 */

/**
 * Initialize all collapsible sub-menus
 */
function initializeSubMenus() {
    const toggleButtons = document.querySelectorAll('.submenu-toggle');

    toggleButtons.forEach(button => {
        // Get the submenu ID from aria-controls
        const submenuId = button.getAttribute('aria-controls');
        const submenuContainer = document.getElementById(submenuId);
        const parentLink = button.previousElementSibling;
        const menuId = parentLink?.getAttribute('data-submenu-id');

        if (!submenuContainer) return;

        // Restore saved state from localStorage
        const savedState = getSubMenuState(menuId);
        if (savedState === 'expanded') {
            expandSubMenu(button, submenuContainer);
        }

        // Attach click event listener
        button.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation(); // Prevent parent link from being triggered
            toggleSubMenu(button, submenuContainer, menuId);
        });

        // Keyboard support
        button.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                e.stopPropagation();
                toggleSubMenu(button, submenuContainer, menuId);
            }
        });

        // Touch support (prevent double-tap delay)
        let touchStartTime = 0;
        button.addEventListener('touchstart', (e) => {
            touchStartTime = Date.now();
        });

        button.addEventListener('touchend', (e) => {
            const touchDuration = Date.now() - touchStartTime;
            // Only trigger if it's a quick tap (not a scroll)
            if (touchDuration < 200) {
                e.preventDefault();
                e.stopPropagation();
                toggleSubMenu(button, submenuContainer, menuId);
            }
        });
    });
}

/**
 * Toggle a submenu (expand/collapse)
 */
function toggleSubMenu(button, submenuContainer, menuId) {
    const isExpanded = button.getAttribute('aria-expanded') === 'true';

    if (isExpanded) {
        collapseSubMenu(button, submenuContainer, menuId);
    } else {
        expandSubMenu(button, submenuContainer, menuId);
    }
}

/**
 * Expand a submenu
 */
function expandSubMenu(button, submenuContainer, menuId) {
    button.setAttribute('aria-expanded', 'true');
    submenuContainer.classList.remove('collapsed');
    submenuContainer.classList.add('expanded');

    // Rotate chevron icon
    const icon = button.querySelector('i');
    if (icon) {
        icon.style.transform = 'rotate(90deg)';
    }

    // Save state to localStorage if menuId provided
    if (menuId) {
        saveSubMenuState(menuId, 'expanded');
    }
}

/**
 * Collapse a submenu
 */
function collapseSubMenu(button, submenuContainer, menuId) {
    button.setAttribute('aria-expanded', 'false');
    submenuContainer.classList.remove('expanded');
    submenuContainer.classList.add('collapsed');

    // Reset chevron icon rotation
    const icon = button.querySelector('i');
    if (icon) {
        icon.style.transform = 'rotate(0deg)';
    }

    // Save state to localStorage if menuId provided
    if (menuId) {
        saveSubMenuState(menuId, 'collapsed');
    }
}

/**
 * Save submenu state to localStorage
 */
function saveSubMenuState(menuId, state) {
    try {
        const key = `submenu_${menuId}_state`;
        localStorage.setItem(key, state);
    } catch (e) {
        // localStorage might be disabled
        console.warn('Could not save submenu state:', e);
    }
}

/**
 * Get submenu state from localStorage
 */
function getSubMenuState(menuId) {
    try {
        const key = `submenu_${menuId}_state`;
        return localStorage.getItem(key);
    } catch (e) {
        // localStorage might be disabled
        return null;
    }
}

/**
 * Badge Rollup
 * =====================================
 * When a submenu is collapsed, aggregate child badge counts onto the parent.
 * Uses the highest-severity color among children.
 */
const BADGE_SEVERITY_ORDER = ['danger', 'warning', 'primary', 'info', 'success'];

function initializeBadgeRollup() {
    document.querySelectorAll('.menu-item-group').forEach(function(group) {
        const parentItem = group.querySelector('.menu-item-parent .menu-item');
        const submenuContainer = group.querySelector('.submenu-container');
        if (!parentItem || !submenuContainer) return;

        const childBadges = submenuContainer.querySelectorAll('.menu-badge');
        if (childBadges.length === 0) return;

        // Remove any existing rollup badge
        const existingRollup = parentItem.querySelector('[data-rollup]');
        if (existingRollup) existingRollup.remove();

        // Create rollup badge element
        const rollupBadge = document.createElement('span');
        rollupBadge.setAttribute('data-rollup', 'true');
        parentItem.appendChild(rollupBadge);

        function updateRollup() {
            let total = 0;
            let highestSeverity = null;

            childBadges.forEach(function(badge) {
                // Skip hidden badges
                if (badge.style.display === 'none') return;

                const count = parseInt(badge.textContent.trim(), 10);
                if (!isNaN(count) && count > 0) {
                    total += count;
                }

                // Determine severity from class
                for (let i = 0; i < BADGE_SEVERITY_ORDER.length; i++) {
                    if (badge.classList.contains('menu-badge-' + BADGE_SEVERITY_ORDER[i])) {
                        if (!highestSeverity ||
                            BADGE_SEVERITY_ORDER.indexOf(BADGE_SEVERITY_ORDER[i]) < BADGE_SEVERITY_ORDER.indexOf(highestSeverity)) {
                            highestSeverity = BADGE_SEVERITY_ORDER[i];
                        }
                        break;
                    }
                }
            });

            // Only show rollup when submenu is collapsed and there are counts
            const isCollapsed = submenuContainer.classList.contains('collapsed');
            // Check if parent already has its own (non-rollup) badge
            const parentOwnBadge = parentItem.querySelector('.menu-badge:not([data-rollup])');

            if (total > 0 && isCollapsed && !parentOwnBadge) {
                rollupBadge.textContent = total > 99 ? '99+' : total;
                rollupBadge.className = 'menu-badge menu-badge-' + (highestSeverity || 'primary');
                rollupBadge.setAttribute('data-rollup', 'true');
                rollupBadge.style.display = '';
            } else if (total > 0 && isCollapsed && parentOwnBadge) {
                // Parent has its own badge - show rollup as additional indicator
                rollupBadge.textContent = total > 99 ? '99+' : total;
                rollupBadge.className = 'menu-badge menu-badge-' + (highestSeverity || 'primary');
                rollupBadge.setAttribute('data-rollup', 'true');
                rollupBadge.style.display = '';
            } else {
                rollupBadge.style.display = 'none';
            }
        }

        // Initial computation
        updateRollup();

        // Re-compute when submenu expanded/collapsed
        var observer = new MutationObserver(updateRollup);
        observer.observe(submenuContainer, { attributes: true, attributeFilter: ['class'] });
    });
}

/**
 * Sidebar Management Functions
 * =====================================
 * Handles sidebar toggle, active menu items, accordions, and scroll position
 */

/**
 * Toggle sidebar collapsed/expanded state
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');

    if (sidebar) {
        sidebar.classList.toggle('collapsed');

        // Store state in localStorage
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
    }
}

/**
 * Set active menu item based on current URL
 */
function setActiveMenuItem() {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(item => {
        const itemPath = new URL(item.href).pathname;
        if (currentPath.startsWith(itemPath) || currentPath === itemPath) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

/**
 * Initialize all accordion menus
 */
function initializeAccordions() {
    const accordions = document.querySelectorAll('.menu-accordion');

    accordions.forEach(accordion => {
        const toggle = accordion.querySelector('.menu-accordion-toggle');
        const accordionId = accordion.getAttribute('data-accordion-id');

        // Restore accordion state from localStorage
        const isExpanded = localStorage.getItem(`accordion_${accordionId}`) === 'true';
        if (isExpanded) {
            accordion.classList.add('expanded');
        }

        // Add click handler
        if (toggle) {
            toggle.addEventListener('click', function() {
                toggleAccordion(accordion, accordionId);
            });
        }
    });
}

/**
 * Toggle accordion expanded/collapsed state
 */
function toggleAccordion(accordion, accordionId) {
    const isExpanded = accordion.classList.toggle('expanded');

    // Save state to localStorage
    localStorage.setItem(`accordion_${accordionId}`, isExpanded);
}

/**
 * Save sidebar scroll position to localStorage
 */
function saveSidebarScrollPosition() {
    const sidebarMenu = document.querySelector('.sidebar-menu');
    if (sidebarMenu) {
        localStorage.setItem('sidebarScrollPosition', sidebarMenu.scrollTop);
    }
}

/**
 * Restore sidebar scroll position from localStorage
 */
function restoreSidebarScrollPosition() {
    const sidebarMenu = document.querySelector('.sidebar-menu');
    const savedPosition = localStorage.getItem('sidebarScrollPosition');

    if (sidebarMenu && savedPosition) {
        sidebarMenu.scrollTop = parseInt(savedPosition, 10);
    }
}

/**
 * Mobile Sidebar Management
 * =====================================
 * Handles mobile-specific sidebar behavior
 */

/**
 * Check if current viewport is mobile
 */
function isMobileView() {
    return window.matchMedia('(max-width: 768px)').matches;
}

/**
 * Initialize mobile sidebar behavior
 */
function initializeMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;

    // Set sidebar to collapsed by default on mobile
    if (isMobileView()) {
        sidebar.classList.add('collapsed');
    }

    // Add click handlers to menu items for mobile slide-up
    const menuLinks = document.querySelectorAll('.menu-item');
    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Only apply on mobile view
            if (isMobileView()) {
                // Don't interfere with submenu parent items that have toggles
                const hasSubmenu = link.getAttribute('data-has-submenu') === 'true';

                // If it's a regular menu link (not a submenu parent), slide up
                if (!hasSubmenu) {
                    sidebar.classList.add('sliding-up');

                    // After animation completes, collapse sidebar for next page load
                    setTimeout(() => {
                        sidebar.classList.add('collapsed');
                        sidebar.classList.remove('sliding-up');
                    }, 200);
                }
            }
        });
    });

    // Handle window resize - collapse sidebar when switching to mobile
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            if (isMobileView() && sidebar && !sidebar.classList.contains('collapsed')) {
                // Auto-collapse when resizing to mobile
                sidebar.classList.add('collapsed');
            }
        }, 100);
    });
}

// Auto-initialize all admin components
document.addEventListener('DOMContentLoaded', function() {
    // Initialize searchable selects
    document.querySelectorAll('[data-searchable-select]').forEach(select => {
        const options = {
            placeholder: select.getAttribute('data-placeholder') || 'Search...'
        };
        new SearchableSelect(select, options);
    });

    // Initialize slug generators for all slug fields
    initializeSlugGenerators();

    // Initialize collapsible sub-menus
    initializeSubMenus();

    // Initialize badge rollup (aggregate child badges onto collapsed parent items)
    initializeBadgeRollup();

    // Initialize sidebar
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    const sidebar = document.getElementById('sidebar');

    if (sidebar && isCollapsed) {
        sidebar.classList.add('collapsed');
    }

    // Set active menu item
    setActiveMenuItem();

    // Initialize accordions
    initializeAccordions();

    // Initialize mobile sidebar behavior
    initializeMobileSidebar();

    // Apply dynamic colors from data-color attributes (CSP-compliant)
    document.querySelectorAll('[data-color]').forEach(function(el) {
        var color = el.dataset.color;
        if (color) { el.style.backgroundColor = color; }
    });

    // Apply tier colors as CSS custom properties (CSP-compliant)
    document.querySelectorAll('[data-tier-color]').forEach(function(el) {
        var color = el.dataset.tierColor;
        if (color) { el.style.setProperty('--tier-color', color); }
    });

    // Restore scroll position
    restoreSidebarScrollPosition();

    // Save scroll position on scroll
    const sidebarMenu = document.querySelector('.sidebar-menu');
    if (sidebarMenu) {
        sidebarMenu.addEventListener('scroll', saveSidebarScrollPosition);
    }
});

/**
 * Dismiss the update notice banner for the current session.
 * Uses sessionStorage so the banner reappears on new sessions.
 */
function dismissUpdateBanner() {
    const banner = document.querySelector('.update-notice-banner');
    if (banner) {
        banner.style.animation = 'updateBannerSlideOut 0.2s ease-in forwards';
        setTimeout(() => {
            banner.style.display = 'none';
        }, 200);
        // Store dismissal in sessionStorage (reappears on new session)
        sessionStorage.setItem('update_banner_dismissed', 'true');
    }
}

// Check if update banner should be hidden on page load
document.addEventListener('DOMContentLoaded', function() {
    if (sessionStorage.getItem('update_banner_dismissed') === 'true') {
        const banner = document.querySelector('.update-notice-banner');
        if (banner) {
            banner.style.display = 'none';
        }
    }
});


// Image fallback: hide broken images and show next sibling, or replace with fallback src
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('img[data-img-fallback="hide"]').forEach(function (img) {
        function handleError() {
            img.style.display = 'none';
            if (img.nextElementSibling) img.nextElementSibling.style.display = 'flex';
        }
        img.addEventListener('error', handleError);
        if (img.complete && img.naturalWidth === 0) handleError();
    });
    document.querySelectorAll('img[data-img-fallback-src]').forEach(function (img) {
        var fallbackSrc = img.dataset.imgFallbackSrc;
        function handleFallback() {
            if (img.src !== fallbackSrc) { img.src = fallbackSrc; }
        }
        img.addEventListener('error', handleFallback);
        if (img.complete && img.naturalWidth === 0 && img.src !== fallbackSrc) { handleFallback(); }
    });
});

// Export for use in other scripts and template onclick handlers
window.SearchableSelect = SearchableSelect;
window.SlugGenerator = SlugGenerator;
window.initializeSlugGenerators = initializeSlugGenerators;
window.initializeSubMenus = initializeSubMenus;
window.initializeBadgeRollup = initializeBadgeRollup;
window.toggleSidebar = toggleSidebar;
window.setActiveMenuItem = setActiveMenuItem;
window.initializeAccordions = initializeAccordions;
window.toggleAccordion = toggleAccordion;
window.initializeMobileSidebar = initializeMobileSidebar;
window.saveSidebarScrollPosition = saveSidebarScrollPosition;
window.restoreSidebarScrollPosition = restoreSidebarScrollPosition;
window.dismissUpdateBanner = dismissUpdateBanner;
