/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Menu Builder - Visual Drag-and-Drop Menu Editor
 * Follows rules_llm.md: Modular class-based structure
 */

// Device presets for responsive preview - matches page builder preview
// Read builder configuration from JSON data island (CSP-safe)
(function () {
    var configEl = document.getElementById('menu-builder-config');
    if (configEl) {
        try { window.MenuBuilderConfig = JSON.parse(configEl.textContent); }
        catch (e) { window.MenuBuilderConfig = {}; }
    }
}());

const DEVICE_PRESETS = {
    'desktop': { w: 1200, h: 800, label: 'Desktop (1200×800)' },
    'tablet-portrait': { w: 768, h: 1024, label: 'Tablet Portrait (768×1024)' },
    'tablet-landscape': { w: 1024, h: 768, label: 'Tablet Landscape (1024×768)' },
    'mobile-portrait': { w: 390, h: 844, label: 'Mobile Portrait (390×844)' },
    'mobile-landscape': { w: 844, h: 390, label: 'Mobile Landscape (844×390)' }
};

class MenuBuilder {
    constructor() {
        var configEl = document.getElementById('menu-builder-config');
        if (configEl) {
            try { this.config = JSON.parse(configEl.textContent); } catch (e) { this.config = {}; }
        } else {
            this.config = window.MenuBuilderConfig || {};
        }
        this.menuId = this.config.menuId;
        this.itemsTree = this.config.initialItemsTree || [];
        this.availablePages = this.config.availablePages || [];
        this.availableCategories = this.config.availableCategories || [];
        this.selectedItem = null;
        this.menuSelected = false;  // True when menu root is selected (for menu-level styling)

        // Menu tokens: track merged values, custom overrides, and theme defaults
        this.menuTokens = this.config.menuTokens || {};           // Merged effective values
        this.menuTokensCustom = this.config.menuTokensCustom || {};   // Custom overrides only
        this.menuTokensDefaults = this.config.menuTokensDefaults || {};  // Theme defaults
        this.menuTokensSaveTimer = null;  // Debounce timer for saving tokens

        // Color picker utility instances for menu-level styling
        this.colorPickers = new Map();

        this.sortableInstances = [];

        // Undo/Redo stack
        this.history = [];
        this.historyIndex = -1;
        this.maxHistorySize = 50;

        // Track unsaved changes
        this.hasUnsavedChanges = false;

        // Device preview state - SEPARATE states for canvas and preview panel
        // Canvas device: affects main builder area visibility indicators
        this.currentDevice = 'desktop';
        // Preview panel device: independent state for the preview frame
        this.previewDevice = 'desktop';
        this.previewOrientation = 'portrait';
        this.manualZoom = 75;
        this.previewDebounceTimer = null;
        this.previewDebounceDelay = 300;

        // Cached device frame dimensions for scaling calculations
        // Desktop: 1200 + (16*2) borders = 1232 width, 800 + (16*2) borders = 832 height
        this.currentPresetWidth = 1232;
        this.currentPresetHeight = 832;

        // Legacy device widths for canvas preview (kept for backward compatibility)
        this.deviceWidths = {
            mobile: 375,
            tablet: 768,
            desktop: null  // Full width
        };

        // AJAX-based search configuration for large stores
        this.pagesUseAjax = this.config.pagesUseAjax || false;
        this.categoriesUseAjax = this.config.categoriesUseAjax || false;
        this.apiSourcesUrl = this.config.apiSourcesUrl || '/api/menu/sources/';
        this.searchDebounceTimer = null;
        this.searchDebounceDelay = 300;  // ms

        // Theme CSS loading state for preview styling
        this.themeCssLoaded = false;

        this.init();
    }

    init() {
        this.bindEvents();
        this.renderItemsTree();
        this.populateQuickAddSources();
        this.initSortable();
        this.saveHistoryState();
        this.setupPreviewControls();

        // Load theme CSS early (non-blocking) so it's ready for color picker resolution
        // This ensures CSS variables are available when user opens the Style tab
        this.loadThemeCSS();
    }

    // =========================================
    // Event Binding
    // =========================================

    bindEvents() {
        // Menu selector
        const menuSelector = document.getElementById('menu-selector');
        if (menuSelector) {
            menuSelector.addEventListener('change', (e) => this.switchMenu(e.target.value));
        }

        // Menu tree header - Click to select menu root for menu-level styling
        const menuTreeHeader = document.getElementById('menu-tree-header');
        if (menuTreeHeader) {
            menuTreeHeader.addEventListener('click', () => this.selectMenu());
            menuTreeHeader.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.selectMenu();
                }
            });
        }

        // Save button
        const saveBtn = document.getElementById('save-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveMenu());
        }

        // Undo/Redo buttons
        const undoBtn = document.getElementById('undo-btn');
        const redoBtn = document.getElementById('redo-btn');
        if (undoBtn) undoBtn.addEventListener('click', () => this.undo());
        if (redoBtn) redoBtn.addEventListener('click', () => this.redo());

        // Expand/Collapse all
        const expandAllBtn = document.getElementById('expand-all-btn');
        const collapseAllBtn = document.getElementById('collapse-all-btn');
        if (expandAllBtn) expandAllBtn.addEventListener('click', () => this.expandAllItems());
        if (collapseAllBtn) collapseAllBtn.addEventListener('click', () => this.collapseAllItems());

        // Add item buttons
        const addFirstItemBtn = document.getElementById('add-first-item-btn');
        const addItemBtn = document.getElementById('add-item-btn');
        if (addFirstItemBtn) addFirstItemBtn.addEventListener('click', () => this.showAddItemModal());
        if (addItemBtn) addItemBtn.addEventListener('click', () => this.showAddItemModal());

        // New menu button
        const newMenuBtn = document.getElementById('new-menu-btn');
        if (newMenuBtn) {
            newMenuBtn.addEventListener('click', () => this.showNewMenuModal());
        }

        // Menu settings
        const menuSettingsBtn = document.getElementById('menu-settings-btn');
        if (menuSettingsBtn) {
            menuSettingsBtn.addEventListener('click', () => this.showMenuSettingsModal());
        }

        // Preview toggle
        const togglePreviewBtn = document.getElementById('toggle-preview-btn');
        const closePreviewBtn = document.getElementById('close-preview-btn');
        if (togglePreviewBtn) {
            togglePreviewBtn.addEventListener('click', () => this.togglePreview());
        }
        if (closePreviewBtn) {
            closePreviewBtn.addEventListener('click', () => this.hidePreview());
        }

        // Device toggles
        document.querySelectorAll('.device-toggle').forEach(btn => {
            btn.addEventListener('click', (e) => this.setDevicePreview(e.target.closest('.device-toggle').dataset.device));
        });

        // Library section toggles
        document.querySelectorAll('.library-section-header').forEach(header => {
            header.addEventListener('click', () => this.toggleLibrarySection(header));
        });

        // Library search
        const librarySearch = document.getElementById('library-search');
        if (librarySearch) {
            librarySearch.addEventListener('input', (e) => this.filterLibrary(e.target.value));
        }

        // Tab switching
        document.querySelectorAll('.admin-tab-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
        });

        // Modal events
        this.bindModalEvents();

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));

        // Warn on unsaved changes
        window.addEventListener('beforeunload', (e) => {
            if (this.hasUnsavedChanges) {
                e.preventDefault();
                e.returnValue = '';
            }
        });

        // Draggable library items
        this.bindLibraryDragEvents();
    }

    bindLibraryDragEvents() {
        document.querySelectorAll('.library-item.draggable-item').forEach(item => {
            item.addEventListener('dragstart', (e) => {
                // Use a custom MIME type to avoid conflicts with text selection drags
                const dragData = JSON.stringify({
                    type: item.dataset.type,
                    widgetType: item.dataset.widgetType || null,
                    pageId: item.dataset.pageId || null,
                    categoryId: item.dataset.categoryId || null
                });
                e.dataTransfer.setData('application/x-menu-item', dragData);
                e.dataTransfer.setData('text/plain', dragData);
                e.dataTransfer.effectAllowed = 'copy';
                item.classList.add('dragging');
            });

            item.addEventListener('dragend', () => {
                item.classList.remove('dragging');
            });
        });

        // Drop zone for menu tree
        const menuTree = document.getElementById('menu-tree');
        if (menuTree) {
            menuTree.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'copy';
                menuTree.classList.add('drag-over');
            });

            menuTree.addEventListener('dragleave', () => {
                menuTree.classList.remove('drag-over');
            });

            menuTree.addEventListener('drop', (e) => {
                e.preventDefault();
                menuTree.classList.remove('drag-over');

                // Try custom MIME type first, then fall back to text/plain
                let rawData = e.dataTransfer.getData('application/x-menu-item');
                if (!rawData) {
                    rawData = e.dataTransfer.getData('text/plain');
                }

                // Validate it's JSON before parsing
                if (!rawData || !rawData.startsWith('{')) {
                    console.warn('Invalid drop data - not JSON');
                    return;
                }

                try {
                    const data = JSON.parse(rawData);
                    if (data.type) {
                        this.addItemFromLibrary(data.type, data.widgetType, data.pageId, data.categoryId);
                    }
                } catch (err) {
                    console.error('Drop error:', err);
                }
            });
        }
    }

    bindModalEvents() {
        // Add Item Modal
        const closeAddItemModal = document.getElementById('close-add-item-modal');
        const cancelAddItemBtn = document.getElementById('cancel-add-item-btn');
        const confirmAddItemBtn = document.getElementById('confirm-add-item-btn');
        const newItemType = document.getElementById('new-item-type');

        if (closeAddItemModal) closeAddItemModal.addEventListener('click', () => this.hideAddItemModal());
        if (cancelAddItemBtn) cancelAddItemBtn.addEventListener('click', () => this.hideAddItemModal());
        if (confirmAddItemBtn) confirmAddItemBtn.addEventListener('click', () => this.confirmAddItem());
        if (newItemType) newItemType.addEventListener('change', () => this.updateAddItemForm());

        // Menu Settings Modal
        const closeSettingsModal = document.getElementById('close-settings-modal');
        const cancelSettingsBtn = document.getElementById('cancel-settings-btn');
        const saveSettingsBtn = document.getElementById('save-settings-btn');

        if (closeSettingsModal) closeSettingsModal.addEventListener('click', () => this.hideMenuSettingsModal());
        if (cancelSettingsBtn) cancelSettingsBtn.addEventListener('click', () => this.hideMenuSettingsModal());
        if (saveSettingsBtn) saveSettingsBtn.addEventListener('click', () => this.saveMenuSettings());

        // New Menu Modal
        const closeNewMenuModal = document.getElementById('close-new-menu-modal');
        const cancelNewMenuBtn = document.getElementById('cancel-new-menu-btn');
        const confirmNewMenuBtn = document.getElementById('confirm-new-menu-btn');

        if (closeNewMenuModal) closeNewMenuModal.addEventListener('click', () => this.hideNewMenuModal());
        if (cancelNewMenuBtn) cancelNewMenuBtn.addEventListener('click', () => this.hideNewMenuModal());
        if (confirmNewMenuBtn) confirmNewMenuBtn.addEventListener('click', () => this.createNewMenu());

        // Icon Picker Modal
        const closeIconPicker = document.getElementById('close-icon-picker');
        const cancelIconBtn = document.getElementById('cancel-icon-btn');
        const clearIconBtn = document.getElementById('clear-icon-btn');

        if (closeIconPicker) closeIconPicker.addEventListener('click', () => this.hideIconPicker());
        if (cancelIconBtn) cancelIconBtn.addEventListener('click', () => this.hideIconPicker());
        if (clearIconBtn) clearIconBtn.addEventListener('click', () => this.selectIcon(''));
    }

    // =========================================
    // Menu Tree Rendering
    // =========================================

    renderItemsTree() {
        const container = document.getElementById('menu-tree');
        const emptyState = document.getElementById('menu-tree-empty');
        const addItemFooter = document.getElementById('add-item-footer');

        if (!container) return;

        // Clear existing content (except empty state)
        container.querySelectorAll('.menu-tree-item').forEach(el => el.remove());

        if (this.itemsTree.length === 0) {
            if (emptyState) emptyState.style.display = 'flex';
            if (addItemFooter) addItemFooter.style.display = 'none';
        } else {
            if (emptyState) emptyState.style.display = 'none';
            if (addItemFooter) addItemFooter.style.display = 'block';

            const fragment = document.createDocumentFragment();
            this.itemsTree.forEach((item, index) => {
                fragment.appendChild(this.createItemElement(item, index, 0));
            });
            container.appendChild(fragment);

            // Reinitialize sortable
            this.initSortable();

            // Update device visibility indicators after rendering
            this.updateDeviceVisibilityIndicators(this.currentDevice);
        }
    }

    createItemElement(item, index, depth) {
        const div = document.createElement('div');
        div.className = 'menu-tree-item';
        div.dataset.itemId = item.id || `temp-${Date.now()}-${index}`;
        div.dataset.depth = depth;

        const hasChildren = item.children && item.children.length > 0;
        const itemIcon = this.getItemIcon(item);
        const itemTitle = item.title || this.config.translations.untitled || 'Untitled';
        const typeLabel = this.config.itemTypeLabels[item.item_type] || item.item_type;
        const isDynamic = item.item_type === 'category_tree';

        // Build dynamic indicator for category_tree items
        const dynamicHint = isDynamic ? `
            <span class="dynamic-item-hint" title="Auto-populates with categories at render time">
                <i class="fas fa-bolt"></i> Dynamic
            </span>
        ` : '';

        div.innerHTML = `
            <div class="menu-tree-item-row ${this.selectedItem?.id === item.id ? 'selected' : ''} ${isDynamic ? 'dynamic-item' : ''}">
                <div class="item-drag-handle">
                    <i class="fas fa-grip-vertical"></i>
                </div>
                ${hasChildren ? `
                    <button class="item-expand-toggle expanded" data-item-id="${item.id}">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                ` : '<div class="item-expand-placeholder"></div>'}
                <div class="item-icon">
                    <i class="fas ${itemIcon}"></i>
                </div>
                <div class="item-title">${this.escapeHtml(itemTitle)}</div>
                ${dynamicHint}
                <span class="item-type-badge ${isDynamic ? 'dynamic' : ''}">${typeLabel}</span>
                <div class="item-actions">
                    <button class="item-action-btn add-child" title="Add child">
                        <i class="fas fa-plus"></i>
                    </button>
                    <button class="item-action-btn duplicate" title="Duplicate">
                        <i class="fas fa-copy"></i>
                    </button>
                    <button class="item-action-btn delete" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;

        // Always add children container for nesting support (even if empty)
        // This allows any item to become a parent via drag-and-drop
        const childrenContainer = document.createElement('div');
        childrenContainer.className = 'menu-tree-children' + (hasChildren ? '' : ' empty');
        childrenContainer.dataset.parentId = item.id;

        if (hasChildren) {
            item.children.forEach((child, childIndex) => {
                childrenContainer.appendChild(this.createItemElement(child, childIndex, depth + 1));
            });
        }

        div.appendChild(childrenContainer);

        // Bind item events
        this.bindItemEvents(div, item);

        return div;
    }

    bindItemEvents(element, item) {
        const row = element.querySelector('.menu-tree-item-row');
        const expandToggle = element.querySelector('.item-expand-toggle');
        const addChildBtn = element.querySelector('.item-action-btn.add-child');
        const duplicateBtn = element.querySelector('.item-action-btn.duplicate');
        const deleteBtn = element.querySelector('.item-action-btn.delete');

        // Select item
        row.addEventListener('click', (e) => {
            if (!e.target.closest('.item-action-btn') && !e.target.closest('.item-expand-toggle') && !e.target.closest('.item-drag-handle')) {
                this.selectItem(item);
            }
        });

        // Expand/collapse
        if (expandToggle) {
            expandToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleItemExpand(element, expandToggle);
            });
        }

        // Add child
        if (addChildBtn) {
            addChildBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.showAddItemModal(item.id);
            });
        }

        // Duplicate
        if (duplicateBtn) {
            duplicateBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.duplicateItem(item);
            });
        }

        // Delete
        if (deleteBtn) {
            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.deleteItem(item);
            });
        }
    }

    getItemIcon(item) {
        if (item.icon) return item.icon;

        const iconMap = {
            'link': 'fa-link',
            'page': 'fa-file',
            'category': 'fa-folder',
            'category_tree': 'fa-sitemap',
            'custom_url': 'fa-external-link-alt',
            'divider': 'fa-minus',
            'header': 'fa-heading',
            'widget': 'fa-puzzle-piece'
        };

        return iconMap[item.item_type] || 'fa-link';
    }

    toggleItemExpand(element, toggle) {
        const children = element.querySelector('.menu-tree-children');
        if (children) {
            children.classList.toggle('collapsed');
            toggle.classList.toggle('expanded');
        }
    }

    expandAllItems() {
        document.querySelectorAll('.menu-tree-children').forEach(el => {
            el.classList.remove('collapsed');
        });
        document.querySelectorAll('.item-expand-toggle').forEach(el => {
            el.classList.add('expanded');
        });
    }

    collapseAllItems() {
        document.querySelectorAll('.menu-tree-children').forEach(el => {
            el.classList.add('collapsed');
        });
        document.querySelectorAll('.item-expand-toggle').forEach(el => {
            el.classList.remove('expanded');
        });
    }

    // =========================================
    // Sortable (Drag and Drop)
    // =========================================

    initSortable() {
        // Destroy existing instances
        this.sortableInstances.forEach(instance => instance.destroy());
        this.sortableInstances = [];

        // Initialize for root level
        const menuTree = document.getElementById('menu-tree');
        if (menuTree) {
            this.sortableInstances.push(
                new Sortable(menuTree, this.getSortableOptions(null))
            );
        }

        // Initialize for each children container
        document.querySelectorAll('.menu-tree-children').forEach(container => {
            const parentId = container.dataset.parentId;
            this.sortableInstances.push(
                new Sortable(container, this.getSortableOptions(parentId))
            );
        });
    }

    getSortableOptions(parentId) {
        return {
            group: 'menu-items',
            animation: 150,
            fallbackOnBody: true,
            swapThreshold: 0.65,
            handle: '.item-drag-handle',
            ghostClass: 'dragging',
            dragClass: 'dragging',
            filter: '.menu-tree-empty',
            onStart: () => {
                // Add class to show drop zones
                document.querySelector('.menu-builder-container')?.classList.add('is-dragging');
            },
            onEnd: (evt) => {
                // Remove class when drag ends
                document.querySelector('.menu-builder-container')?.classList.remove('is-dragging');
                this.handleDragEnd(evt);
            }
        };
    }

    handleDragEnd(evt) {
        const itemElement = evt.item;
        const itemId = itemElement.dataset.itemId;
        const newParentContainer = evt.to;
        const newParentId = newParentContainer.dataset.parentId || null;
        const newIndex = evt.newIndex;

        // Update the items tree data structure
        this.moveItem(itemId, newParentId, newIndex);

        // Re-render and save history
        this.renderItemsTree();
        this.saveHistoryState();
        this.markUnsaved();
    }

    moveItem(itemId, newParentId, newIndex) {
        // Find and remove item from current position
        const item = this.findAndRemoveItem(this.itemsTree, itemId);
        if (!item) return;

        // Insert at new position
        if (newParentId) {
            const parent = this.findItemById(this.itemsTree, newParentId);
            if (parent) {
                if (!parent.children) parent.children = [];
                parent.children.splice(newIndex, 0, item);
            }
        } else {
            this.itemsTree.splice(newIndex, 0, item);
        }
    }

    findAndRemoveItem(items, itemId, parentArray = null) {
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            if (String(item.id) === String(itemId)) {
                items.splice(i, 1);
                return item;
            }
            if (item.children && item.children.length > 0) {
                const found = this.findAndRemoveItem(item.children, itemId, items);
                if (found) return found;
            }
        }
        return null;
    }

    findItemById(items, itemId) {
        for (const item of items) {
            if (String(item.id) === String(itemId)) return item;
            if (item.children && item.children.length > 0) {
                const found = this.findItemById(item.children, itemId);
                if (found) return found;
            }
        }
        return null;
    }

    // =========================================
    // Item Selection & Properties
    // =========================================

    selectItem(item) {
        this.selectedItem = item;
        this.menuSelected = false;  // Deselect menu when item is selected

        // Update visual selection - remove from all items and menu header
        document.querySelectorAll('.menu-tree-item-row').forEach(row => {
            row.classList.remove('selected');
        });
        const menuHeader = document.getElementById('menu-tree-header');
        if (menuHeader) {
            menuHeader.classList.remove('selected');
        }

        const itemElement = document.querySelector(`[data-item-id="${item.id}"]`);
        if (itemElement) {
            itemElement.querySelector('.menu-tree-item-row')?.classList.add('selected');
        }

        // Render properties panel
        this.renderPropertiesPanel(item);

        // Switch to properties tab
        this.switchTab('item-props');
    }

    /**
     * Select the menu root (for menu-level styling)
     * Deselects any selected item and shows menu-level properties
     */
    selectMenu() {
        this.selectedItem = null;
        this.menuSelected = true;

        // Update visual selection - deselect all items
        document.querySelectorAll('.menu-tree-item-row').forEach(row => {
            row.classList.remove('selected');
        });

        // Highlight menu header
        const menuHeader = document.getElementById('menu-tree-header');
        if (menuHeader) {
            menuHeader.classList.add('selected');
        }

        // Render menu-level properties
        this.renderMenuPropertiesPanel();

        // Switch to style tab since that's the main use case for selecting menu root
        this.switchTab('style-props');
    }

    /**
     * Deselect any selected item (resets to no selection)
     */
    deselectAll() {
        this.selectedItem = null;
        this.menuSelected = false;

        document.querySelectorAll('.menu-tree-item-row').forEach(row => {
            row.classList.remove('selected');
        });
        const menuHeader = document.getElementById('menu-tree-header');
        if (menuHeader) {
            menuHeader.classList.remove('selected');
        }

        this.renderPropertiesPanel(null);
    }

    renderPropertiesPanel(item) {
        const itemPanel = document.getElementById('item-properties-panel');
        const stylePanel = document.getElementById('style-properties-panel');
        const visibilityPanel = document.getElementById('visibility-properties-panel');

        if (!item) {
            // Show empty states
            [itemPanel, stylePanel, visibilityPanel].forEach(panel => {
                if (panel) panel.innerHTML = this.getEmptyPanelHtml(panel.id);
            });
            return;
        }

        // Item Properties Tab
        if (itemPanel) {
            itemPanel.innerHTML = this.getItemPropertiesHtml(item);
            this.bindPropertyEvents(item);
        }

        // Style Properties Tab
        if (stylePanel) {
            stylePanel.innerHTML = this.getStylePropertiesHtml(item);
            this.bindStyleEvents(item);
        }

        // Visibility Properties Tab
        if (visibilityPanel) {
            visibilityPanel.innerHTML = this.getVisibilityPropertiesHtml(item);
            this.bindVisibilityEvents(item);
        }
    }

    /**
     * Render the properties panel for menu-level styling
     * Shows menu settings and design tokens that sync with ThemeBranding
     */
    renderMenuPropertiesPanel() {
        const itemPanel = document.getElementById('item-properties-panel');
        const stylePanel = document.getElementById('style-properties-panel');
        const visibilityPanel = document.getElementById('visibility-properties-panel');

        // Item tab shows menu settings (name, location, display type)
        if (itemPanel) {
            itemPanel.innerHTML = this.getMenuSettingsHtml();
            this.bindMenuSettingsEvents();
        }

        // Style tab shows menu design tokens
        if (stylePanel) {
            stylePanel.innerHTML = this.getMenuStyleHtml();
            this.bindMenuStyleEvents();

            // Initialize color picker utilities after DOM is ready
            // Uses async/await to ensure theme CSS is loaded before resolving variables
            requestAnimationFrame(async () => {
                await this.initializeColorPickers();
            });
        }

        // Visibility tab - not applicable for menu root
        if (visibilityPanel) {
            visibilityPanel.innerHTML = `
                <div class="properties-empty">
                    <i class="fas fa-info-circle"></i>
                    <p>Visibility rules apply to individual menu items</p>
                </div>
            `;
        }
    }

    /**
     * Get HTML for menu settings (Item tab when menu is selected)
     */
    getMenuSettingsHtml() {
        const menuName = this.config.menuName || 'Menu';
        const menuId = this.config.menuId;

        return `
            <div class="properties-section">
                <div class="properties-section-header">
                    <i class="fas fa-bars"></i>
                    <span>${this.config.translations?.menuStylesTitle || 'Menu Settings'}</span>
                </div>
                <div class="properties-section-content">
                    <div class="form-group">
                        <label for="menu-prop-name">Menu Name</label>
                        <input type="text" id="menu-prop-name" class="form-control" value="${this.escapeHtml(menuName)}">
                    </div>
                    <p class="property-hint">
                        <i class="fas fa-info-circle"></i>
                        Use the Menu Settings button to change location and display type.
                    </p>
                </div>
            </div>
        `;
    }

    /**
     * Get HTML for menu styling (Style tab when menu is selected)
     * These tokens sync with ThemeBranding.component_overrides['menu']
     * Shows merged values (theme defaults + custom overrides) with custom indicators
     */
    getMenuStyleHtml() {
        const tokens = this.menuTokens || {};           // Merged effective values
        const customized = this.menuTokensCustom || {};  // Custom overrides only
        const defaults = this.menuTokensDefaults || {};  // Theme defaults

        // Hardcoded fallback defaults when theme doesn't define menu tokens
        const fallbackDefaults = {
            'text-color': 'var(--color-text)',
            'text-hover-color': 'var(--color-text-inverse)',
            'background-hover': 'var(--color-primary)',
            'dropdown-background': 'var(--color-surface)',
            'item-gap': 'var(--space-1)',
            'link-padding-x': 'var(--space-4)',
            'link-padding-y': 'var(--space-2)',
            'font-size': 'var(--font-size-base)',
            'border-radius': 'var(--radius-md)',
            'animation-duration': 'var(--duration-fast)'
        };

        // Helper to check if a token is customized
        const isCustom = (key) => key in customized;

        // Helper to get custom badge HTML
        const customBadge = (key) => isCustom(key)
            ? '<span class="token-custom-badge">Custom</span>'
            : '';

        // Get current editing device
        const editDevice = this.currentDevice || 'desktop';

        // Helper to get effective value for current device
        // Supports both flat values and device-keyed objects
        const getValue = (key) => {
            const val = tokens[key] || defaults[key] || fallbackDefaults[key] || '';

            // If it's a device-keyed object, get value for current device with inheritance
            if (val && typeof val === 'object' && !Array.isArray(val)) {
                // Check for device-specific value, inherit from larger breakpoints
                if (editDevice === 'mobile') {
                    return val.mobile || val.tablet || val.desktop || '';
                } else if (editDevice === 'tablet') {
                    return val.tablet || val.desktop || '';
                } else {
                    return val.desktop || val.mobile || '';  // Desktop fallback to mobile if no desktop
                }
            }

            return val;
        };

        // Helper to get the CSS variable name that will be updated
        const getCssVarName = (key) => `--menu-${key}`;

        // Helper to generate the variable hint label
        const varHint = (key) => `<span class="token-var-hint">Updates: <code>${getCssVarName(key)}</code></span>`;

        // Helper to check if token has device-specific values
        const hasDeviceValues = (key) => {
            const val = tokens[key];
            return val && typeof val === 'object' && ('mobile' in val || 'tablet' in val || 'desktop' in val);
        };

        // Badge for tokens with device-specific values
        const deviceBadge = (key) => hasDeviceValues(key)
            ? '<span class="token-device-badge" title="Has device-specific values"><i class="fas fa-mobile-alt"></i></span>'
            : '';

        // Get current editing device
        const currentDevice = this.currentDevice || 'desktop';

        return `
            <div class="properties-device-selector">
                <span class="device-selector-label">Editing for:</span>
                <div class="device-selector-buttons">
                    <button type="button" class="device-btn ${currentDevice === 'desktop' ? 'active' : ''}"
                            data-device="desktop" title="Desktop (1024px+)">
                        <i class="fas fa-desktop"></i>
                        <span>Desktop</span>
                    </button>
                    <button type="button" class="device-btn ${currentDevice === 'tablet' ? 'active' : ''}"
                            data-device="tablet" title="Tablet (768px - 1023px)">
                        <i class="fas fa-tablet-alt"></i>
                        <span>Tablet</span>
                    </button>
                    <button type="button" class="device-btn ${currentDevice === 'mobile' ? 'active' : ''}"
                            data-device="mobile" title="Mobile (< 768px)">
                        <i class="fas fa-mobile-alt"></i>
                        <span>Mobile</span>
                    </button>
                </div>
            </div>

            <div class="properties-section menu-style-section">
                <div class="properties-section-header">
                    <i class="fas fa-palette"></i>
                    <span>${this.config.translations?.colorsSection || 'Colors'}</span>
                </div>
                <div class="properties-section-content">
                    <div class="form-group color-property" data-token-group="text-color">
                        <label for="menu-token-text-color">Text Color ${customBadge('text-color')}</label>
                        <div class="color-input-wrapper">
                            <input type="text"
                                   id="menu-token-text-color"
                                   class="form-control color-input"
                                   data-token="text-color"
                                   data-raw-value="${this.escapeHtml(getValue('text-color'))}">
                        </div>
                        ${varHint('text-color')}
                    </div>

                    <div class="form-group color-property" data-token-group="text-hover-color">
                        <label for="menu-token-text-hover-color">Hover Text Color ${customBadge('text-hover-color')}</label>
                        <div class="color-input-wrapper">
                            <input type="text"
                                   id="menu-token-text-hover-color"
                                   class="form-control color-input"
                                   data-token="text-hover-color"
                                   data-raw-value="${this.escapeHtml(getValue('text-hover-color'))}">
                        </div>
                        ${varHint('text-hover-color')}
                    </div>

                    <div class="form-group color-property" data-token-group="background-hover">
                        <label for="menu-token-background-hover">Hover Background ${customBadge('background-hover')}</label>
                        <div class="color-input-wrapper">
                            <input type="text"
                                   id="menu-token-background-hover"
                                   class="form-control color-input"
                                   data-token="background-hover"
                                   data-raw-value="${this.escapeHtml(getValue('background-hover'))}">
                        </div>
                        ${varHint('background-hover')}
                    </div>

                    <div class="form-group color-property" data-token-group="dropdown-background">
                        <label for="menu-token-dropdown-background">Dropdown Background ${customBadge('dropdown-background')}</label>
                        <div class="color-input-wrapper">
                            <input type="text"
                                   id="menu-token-dropdown-background"
                                   class="form-control color-input"
                                   data-token="dropdown-background"
                                   data-raw-value="${this.escapeHtml(getValue('dropdown-background'))}">
                        </div>
                        ${varHint('dropdown-background')}
                    </div>
                </div>
            </div>

            <div class="properties-section menu-style-section">
                <div class="properties-section-header">
                    <i class="fas fa-arrows-alt"></i>
                    <span>${this.config.translations?.spacingSection || 'Spacing'}</span>
                </div>
                <div class="properties-section-content">
                    <div class="form-group" data-token-group="item-gap">
                        <label for="menu-token-item-gap">Item Gap ${customBadge('item-gap')}</label>
                        <input type="text"
                               id="menu-token-item-gap"
                               class="form-control"
                               data-token="item-gap"
                               data-raw-value="${this.escapeHtml(getValue('item-gap'))}">
                        ${varHint('item-gap')}
                    </div>

                    <div class="form-group" data-token-group="link-padding-x">
                        <label for="menu-token-link-padding-x">Link Padding X ${customBadge('link-padding-x')}</label>
                        <input type="text"
                               id="menu-token-link-padding-x"
                               class="form-control"
                               data-token="link-padding-x"
                               data-raw-value="${this.escapeHtml(getValue('link-padding-x'))}">
                        ${varHint('link-padding-x')}
                    </div>

                    <div class="form-group" data-token-group="link-padding-y">
                        <label for="menu-token-link-padding-y">Link Padding Y ${customBadge('link-padding-y')}</label>
                        <input type="text"
                               id="menu-token-link-padding-y"
                               class="form-control"
                               data-token="link-padding-y"
                               data-raw-value="${this.escapeHtml(getValue('link-padding-y'))}">
                        ${varHint('link-padding-y')}
                    </div>
                </div>
            </div>

            <div class="properties-section menu-style-section">
                <div class="properties-section-header">
                    <i class="fas fa-font"></i>
                    <span>${this.config.translations?.typographySection || 'Typography'}</span>
                </div>
                <div class="properties-section-content">
                    <div class="form-group" data-token-group="font-size">
                        <label for="menu-token-font-size">Font Size ${customBadge('font-size')}</label>
                        <input type="text"
                               id="menu-token-font-size"
                               class="form-control"
                               data-token="font-size"
                               data-raw-value="${this.escapeHtml(getValue('font-size'))}">
                        ${varHint('font-size')}
                    </div>

                    <div class="form-group" data-token-group="font-weight">
                        <label for="menu-token-font-weight">Font Weight ${customBadge('font-weight')}</label>
                        <select id="menu-token-font-weight" class="form-control" data-token="font-weight" data-raw-value="${this.escapeHtml(getValue('font-weight'))}">
                            <option value="" ${!getValue('font-weight') ? 'selected' : ''}>Default</option>
                            <option value="400" ${getValue('font-weight') === '400' || getValue('font-weight') === 'var(--font-weight-normal)' ? 'selected' : ''}>Normal (400)</option>
                            <option value="500" ${getValue('font-weight') === '500' || getValue('font-weight') === 'var(--font-weight-medium)' ? 'selected' : ''}>Medium (500)</option>
                            <option value="600" ${getValue('font-weight') === '600' || getValue('font-weight') === 'var(--font-weight-semibold)' ? 'selected' : ''}>Semibold (600)</option>
                            <option value="700" ${getValue('font-weight') === '700' || getValue('font-weight') === 'var(--font-weight-bold)' ? 'selected' : ''}>Bold (700)</option>
                        </select>
                        ${varHint('font-weight')}
                    </div>
                </div>
            </div>

            <div class="properties-section menu-style-section">
                <div class="properties-section-header">
                    <i class="fas fa-border-style"></i>
                    <span>Border & Shape</span>
                </div>
                <div class="properties-section-content">
                    <div class="form-group" data-token-group="border-radius">
                        <label for="menu-token-border-radius">Border Radius ${customBadge('border-radius')}</label>
                        <input type="text"
                               id="menu-token-border-radius"
                               class="form-control"
                               data-token="border-radius"
                               data-raw-value="${this.escapeHtml(getValue('border-radius'))}">
                        ${varHint('border-radius')}
                    </div>
                </div>
            </div>

            <div class="properties-section menu-style-section">
                <div class="properties-section-header">
                    <i class="fas fa-clock"></i>
                    <span>${this.config.translations?.animationSection || 'Animation'}</span>
                </div>
                <div class="properties-section-content">
                    <div class="form-group" data-token-group="animation-duration">
                        <label for="menu-token-animation-duration">Animation Duration ${customBadge('animation-duration')}</label>
                        <input type="text"
                               id="menu-token-animation-duration"
                               class="form-control"
                               data-token="animation-duration"
                               data-raw-value="${this.escapeHtml(getValue('animation-duration'))}">
                        ${varHint('animation-duration')}
                    </div>
                </div>
            </div>

            <div class="properties-section menu-style-actions">
                <button type="button" class="btn-secondary btn-block" id="reset-menu-tokens-btn">
                    <i class="fas fa-undo"></i> Reset to Defaults
                </button>
            </div>
        `;
    }

    /**
     * Bind events for menu settings inputs
     */
    bindMenuSettingsEvents() {
        const nameInput = document.getElementById('menu-prop-name');
        if (nameInput) {
            nameInput.addEventListener('input', (e) => {
                this.config.menuName = e.target.value;
                // Update menu name display
                const menuNameDisplay = document.querySelector('.menu-name-display');
                if (menuNameDisplay) {
                    menuNameDisplay.textContent = e.target.value;
                }
                const menuTreeHeaderName = document.querySelector('.menu-tree-header .menu-name');
                if (menuTreeHeaderName) {
                    menuTreeHeaderName.textContent = e.target.value;
                }
                this.hasUnsavedChanges = true;
            });
        }
    }

    /**
     * Bind events for menu style token inputs
     */
    bindMenuStyleEvents() {
        // Bind device selector buttons
        document.querySelectorAll('.properties-device-selector .device-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const device = btn.dataset.device;
                this.setEditingDevice(device);
            });
        });

        // Bind all token inputs
        document.querySelectorAll('[data-token]').forEach(input => {
            const tokenName = input.dataset.token;

            input.addEventListener('input', (e) => {
                const newValue = e.target.value;

                // Update the raw value data attribute (stores what will be saved)
                input.dataset.rawValue = newValue;

                // Update token for current device and preview
                this.updateMenuTokenForDevice(tokenName, newValue);

                // Update color preview if it's a color input
                const preview = input.closest('.color-input-wrapper')?.querySelector('.color-preview');
                if (preview) {
                    preview.style.background = newValue || 'transparent';
                }
            });

            input.addEventListener('change', (e) => {
                const newValue = e.target.value;
                input.dataset.rawValue = newValue;
                this.updateMenuTokenForDevice(tokenName, newValue);
            });
        });

        // Reset button
        const resetBtn = document.getElementById('reset-menu-tokens-btn');
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetMenuTokens());
        }
    }

    /**
     * Set the editing device and sync with preview
     * @param {string} device - 'desktop', 'tablet', or 'mobile'
     */
    setEditingDevice(device) {
        this.currentDevice = device;

        // Update device selector button states
        document.querySelectorAll('.properties-device-selector .device-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.device === device);
        });

        // Sync with preview panel device
        this.switchDevice(device);

        // Re-render properties panel to show values for new device
        this.renderMenuPropertiesPanel();
    }

    /**
     * Update a menu token for the current editing device
     * Handles device-specific values when editing for tablet/mobile
     * @param {string} tokenName - Token name
     * @param {string} value - New value
     */
    updateMenuTokenForDevice(tokenName, value) {
        const device = this.currentDevice || 'desktop';
        const currentValue = this.menuTokens[tokenName];

        if (device === 'desktop') {
            // For desktop, check if we should keep device structure or flatten
            if (typeof currentValue === 'object' && currentValue !== null) {
                // Already has device-specific values, update desktop
                this.menuTokens[tokenName] = { ...currentValue, desktop: value };
            } else {
                // Flat value, keep it flat for desktop
                this.menuTokens[tokenName] = value;
            }
        } else {
            // For tablet/mobile, create device-specific structure
            if (typeof currentValue === 'object' && currentValue !== null) {
                // Already an object, update the specific device
                this.menuTokens[tokenName] = { ...currentValue, [device]: value };
            } else {
                // Convert flat value to device object
                // Keep desktop as the original value
                this.menuTokens[tokenName] = {
                    desktop: currentValue || value,
                    [device]: value
                };
            }
        }

        // Track as custom
        this.menuTokensCustom[tokenName] = this.menuTokens[tokenName];

        // Mark unsaved changes
        this.hasUnsavedChanges = true;

        // Apply to preview
        this.applyMenuTokensToPreview();
    }

    /**
     * Resolve CSS variable to actual color value
     * Handles chained variables like var(--menu-text-color) → var(--color-text) → #1f2937
     * @param {string} value - CSS value that may contain var(--name)
     * @param {number} maxDepth - Maximum recursion depth to prevent infinite loops
     * @returns {string} - Resolved color or original value
     */
    resolveCssVariable(value, maxDepth = 5) {
        if (!value || typeof value !== 'string') {
            return value;
        }

        // If it's not a CSS variable, return as-is
        const trimmedValue = value.trim();
        if (!trimmedValue.startsWith('var(')) {
            return value;
        }

        // Prevent infinite recursion
        if (maxDepth <= 0) {
            console.warn('CSS variable resolution max depth reached:', value);
            return value;
        }

        // Check if it's a CSS variable - extract name and optional fallback
        const varMatch = trimmedValue.match(/^var\(\s*(--[a-zA-Z0-9-]+)\s*(?:,\s*(.+))?\s*\)$/);
        if (!varMatch) {
            return value;  // Malformed var(), return as-is
        }

        const varName = varMatch[1];
        const fallback = varMatch[2];

        // Get the preview content element where theme CSS is scoped
        const previewContent = document.querySelector('.device-frame .preview-content');

        let computedValue = '';
        if (previewContent) {
            // Get computed style from preview content (has scoped theme CSS)
            computedValue = getComputedStyle(previewContent).getPropertyValue(varName).trim();
        } else {
            // No preview element - try document root
            computedValue = getComputedStyle(document.documentElement).getPropertyValue(varName).trim();
        }

        if (computedValue) {
            // If computed value is ALSO a variable reference, resolve recursively
            // This handles chains like: --menu-text-color: var(--color-text)
            if (computedValue.startsWith('var(')) {
                return this.resolveCssVariable(computedValue, maxDepth - 1);
            }
            return computedValue;
        }

        // Try fallback value if provided
        if (fallback) {
            // Fallback might also be a variable - recursively resolve
            return this.resolveCssVariable(fallback.trim(), maxDepth - 1);
        }

        // Return original value if can't resolve
        return value;
    }

    /**
     * Initialize ColorPickerUtility instances for color inputs
     * Uses the reusable utility from page builder for consistent UX
     */
    async initializeColorPickers() {
        // Ensure theme CSS is loaded before trying to resolve CSS variables
        await this.loadThemeCSS();

        // First, resolve all token values and display them in inputs
        this.resolveAllTokenDisplayValues();

        // Clean up existing color pickers to prevent memory leaks
        this.colorPickers.forEach(picker => {
            if (picker && typeof picker.destroy === 'function') {
                picker.destroy();
            }
        });
        this.colorPickers.clear();

        // Check if ColorPickerUtility is available
        if (typeof ColorPickerUtility === 'undefined') {
            console.warn('ColorPickerUtility not loaded - using fallback color inputs');
            return;
        }

        // Find all color inputs with data-token attribute in color property groups
        const colorInputs = document.querySelectorAll('.color-property [data-token]');

        colorInputs.forEach(input => {
            const tokenName = input.dataset.token;
            if (!tokenName) return;

            // Input value is now the resolved color (set by resolveAllTokenDisplayValues)
            const resolvedColor = input.value || '';

            // Create color picker instance
            const picker = new ColorPickerUtility({
                propertyKey: tokenName,
                showOpacity: true,
                showSwatches: true,
                onChange: (value) => {
                    // Update input value with the new color
                    input.value = value;
                    // Update the raw value data attribute
                    input.dataset.rawValue = value;
                    // Update token and preview
                    this.updateMenuToken(tokenName, value);
                }
            });

            // Attach with resolved color for swatch display
            picker.attach(input, resolvedColor);

            // Store reference for cleanup
            this.colorPickers.set(tokenName, picker);
        });
    }

    /**
     * Resolve all token values from CSS variables to actual values
     * Sets the resolved value in inputs while preserving raw value in data attribute
     */
    resolveAllTokenDisplayValues() {
        // Find all inputs with data-raw-value attribute
        const tokenInputs = document.querySelectorAll('[data-token][data-raw-value]');

        tokenInputs.forEach(input => {
            const rawValue = input.dataset.rawValue || '';

            // Resolve the value (handles chained variables like --menu-text-color → --color-text → #hex)
            const resolvedValue = this.resolveCssVariable(rawValue);

            // Set the resolved value in the input for display
            if (input.tagName === 'SELECT') {
                // For select elements, try to match an option
                const options = input.querySelectorAll('option');
                let matched = false;
                options.forEach(option => {
                    if (option.value === resolvedValue) {
                        option.selected = true;
                        matched = true;
                    }
                });
                // If no match and it's a font-weight, try numeric matching
                if (!matched && input.dataset.token === 'font-weight') {
                    const numericWeight = this.resolveCssVariable(rawValue);
                    options.forEach(option => {
                        if (option.value === numericWeight) {
                            option.selected = true;
                        }
                    });
                }
            } else {
                // For text inputs, set the value directly
                input.value = resolvedValue;
            }
        });
    }

    /**
     * Update a single menu token (with debounced save)
     * Tracks both merged values and custom overrides
     */
    updateMenuToken(tokenName, value) {
        const trimmedValue = value ? value.trim() : '';
        const defaultValue = this.menuTokensDefaults[tokenName] || '';

        if (trimmedValue) {
            // Update merged tokens
            this.menuTokens[tokenName] = trimmedValue;

            // Track as custom if different from default
            if (trimmedValue !== defaultValue) {
                this.menuTokensCustom[tokenName] = trimmedValue;
            } else {
                // Value matches default - remove from custom
                delete this.menuTokensCustom[tokenName];
            }
        } else {
            // Empty value - revert to default
            if (defaultValue) {
                this.menuTokens[tokenName] = defaultValue;
            } else {
                delete this.menuTokens[tokenName];
            }
            delete this.menuTokensCustom[tokenName];
        }

        // Update preview immediately with CSS variable
        this.applyMenuTokensToPreview();

        // Debounced save to backend
        this.debouncedSaveMenuTokens();
    }

    /**
     * Apply current menu tokens to preview CSS variables
     */
    applyMenuTokensToPreview() {
        const previewContent = document.getElementById('menu-preview-content');
        if (!previewContent) return;

        // Map token names to CSS variable names
        const tokenToCssVar = {
            'text-color': '--menu-text-color',
            'text-hover-color': '--menu-text-hover-color',
            'background-hover': '--menu-background-hover',
            'dropdown-background': '--menu-dropdown-background',
            'item-gap': '--menu-item-gap',
            'link-padding-x': '--menu-link-padding-x',
            'link-padding-y': '--menu-link-padding-y',
            'font-size': '--menu-font-size',
            'font-weight': '--menu-font-weight',
            'border-radius': '--menu-border-radius',
            'animation-duration': '--menu-animation-duration',
        };

        for (const [token, cssVar] of Object.entries(tokenToCssVar)) {
            if (this.menuTokens[token]) {
                previewContent.style.setProperty(cssVar, this.menuTokens[token]);
            } else {
                previewContent.style.removeProperty(cssVar);
            }
        }
    }

    /**
     * Debounced save of menu tokens to backend
     */
    debouncedSaveMenuTokens() {
        if (this.menuTokensSaveTimer) {
            clearTimeout(this.menuTokensSaveTimer);
        }

        this.menuTokensSaveTimer = setTimeout(() => {
            this.saveMenuTokens();
        }, 500);  // 500ms debounce
    }

    /**
     * Save menu tokens to ThemeBranding via API
     */
    async saveMenuTokens() {
        const apiUrl = this.config.apiMenuTokensUrl || '/api/menu/tokens/';

        // Only save tokens that differ from theme defaults (custom overrides only)
        // This keeps ThemeBranding.component_overrides['menu'] clean
        const tokensToSave = this.menuTokensCustom || {};

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({ tokens: tokensToSave })
            });

            if (response.ok) {
                this.showToast(this.config.translations?.menuStylesSaved || 'Menu styles saved', 'success');
            } else {
                const data = await response.json();
                throw new Error(data.error || 'Failed to save');
            }
        } catch (error) {
            console.error('Failed to save menu tokens:', error);
            this.showToast('Failed to save menu styles', 'error');
        }
    }

    /**
     * Reset menu tokens to defaults
     */
    async resetMenuTokens() {
        const confirmMsg = this.config.translations?.confirmResetStyles || 'Reset all menu styles to theme defaults?';
        if (!await AdminModal.confirm({
            message: confirmMsg,
            danger: true,
            confirmText: 'Reset'
        })) return;

        // Clear custom overrides, restore theme defaults as effective values
        this.menuTokensCustom = {};
        this.menuTokens = { ...this.menuTokensDefaults };

        // Save empty tokens (clears custom overrides in ThemeBranding)
        await this.saveMenuTokens();

        // Re-render the style panel
        this.renderMenuPropertiesPanel();

        // Update preview CSS variables to use defaults
        this.applyMenuTokensToPreview();

        this.showToast(this.config.translations?.menuStylesReset || 'Menu styles reset to defaults', 'success');
    }

    getEmptyPanelHtml(panelId) {
        const icons = {
            'item-properties-panel': 'fa-hand-pointer',
            'style-properties-panel': 'fa-palette',
            'visibility-properties-panel': 'fa-eye'
        };

        const messages = {
            'item-properties-panel': this.config.translations.selectItem || 'Select a menu item to edit its properties',
            'style-properties-panel': 'Select a menu item to customize its styling',
            'visibility-properties-panel': 'Select a menu item to configure visibility rules'
        };

        return `
            <div class="properties-empty">
                <i class="fas ${icons[panelId] || 'fa-hand-pointer'}"></i>
                <p>${messages[panelId]}</p>
            </div>
        `;
    }

    getItemPropertiesHtml(item) {
        const typeOptions = Object.entries(this.config.itemTypeLabels || {})
            .map(([value, label]) => `<option value="${value}" ${item.item_type === value ? 'selected' : ''}>${label}</option>`)
            .join('');

        let dynamicFields = '';

        if (item.item_type === 'page') {
            // Find the currently selected page title
            const selectedPage = this.availablePages.find(p => p.id === item.page_reference_id);
            const selectedPageTitle = selectedPage ? selectedPage.title : '';

            dynamicFields += `
                <div class="form-group">
                    <label for="prop-page-search">Page</label>
                    <div class="searchable-select" id="page-searchable-select">
                        <input type="hidden" id="prop-page-reference" value="${item.page_reference_id || ''}">
                        <div class="searchable-select-input-wrapper">
                            <input type="text"
                                   id="prop-page-search"
                                   class="form-control searchable-select-input"
                                   placeholder="${this.config.translations?.searchPages || 'Search pages...'}"
                                   value="${this.escapeHtml(selectedPageTitle)}"
                                   autocomplete="off">
                            ${selectedPageTitle ? `<button type="button" class="searchable-select-clear" id="prop-page-clear" title="Clear selection">&times;</button>` : ''}
                        </div>
                        <div class="searchable-select-dropdown" id="prop-page-dropdown"></div>
                    </div>
                </div>
            `;
        }

        if (item.item_type === 'category') {
            // Find the currently selected category name
            const selectedCategory = this.availableCategories.find(c => c.id === item.category_reference_id);
            const selectedCategoryName = selectedCategory ? selectedCategory.name : '';

            dynamicFields += `
                <div class="form-group">
                    <label for="prop-category-search">Category</label>
                    <div class="searchable-select" id="category-searchable-select">
                        <input type="hidden" id="prop-category-reference" value="${item.category_reference_id || ''}">
                        <div class="searchable-select-input-wrapper">
                            <input type="text"
                                   id="prop-category-search"
                                   class="form-control searchable-select-input"
                                   placeholder="${this.config.translations?.searchCategories || 'Search categories...'}"
                                   value="${this.escapeHtml(selectedCategoryName)}"
                                   autocomplete="off">
                            ${selectedCategoryName ? `<button type="button" class="searchable-select-clear" id="prop-category-clear" title="Clear selection">&times;</button>` : ''}
                        </div>
                        <div class="searchable-select-dropdown" id="prop-category-dropdown"></div>
                    </div>
                </div>
            `;
        }

        if (item.item_type === 'widget') {
            const widgetTypes = [
                { value: 'login_toggle', label: 'Login/Logout' },
                { value: 'cart', label: 'Shopping Cart' },
                { value: 'account', label: 'My Account' },
                { value: 'wishlist', label: 'Wishlist' },
                { value: 'search', label: 'Search' }
            ];
            const widgetOptions = widgetTypes
                .map(w => `<option value="${w.value}" ${item.widget_config?.widget_type === w.value ? 'selected' : ''}>${w.label}</option>`)
                .join('');
            dynamicFields += `
                <div class="form-group">
                    <label for="prop-widget-type">Widget Type</label>
                    <select id="prop-widget-type" class="form-control">
                        ${widgetOptions}
                    </select>
                </div>
            `;
        }

        if (item.item_type === 'category_tree') {
            const treeConfig = item.tree_config || {};
            const categoryOptions = this.availableCategories
                .map(c => `<option value="${c.id}" ${treeConfig.root_category_id === c.id ? 'selected' : ''}>${c.name}</option>`)
                .join('');

            const depthOptions = [1, 2, 3, 4, 5].map(d =>
                `<option value="${d}" ${(treeConfig.max_depth || 3) === d ? 'selected' : ''}>${d} level${d > 1 ? 's' : ''}</option>`
            ).join('');

            const sortOptions = [
                { value: 'name', label: 'Name (A-Z)' },
                { value: '-name', label: 'Name (Z-A)' },
                { value: 'order', label: 'Custom Order' },
                { value: 'product_count', label: 'Most Products' }
            ].map(s => `<option value="${s.value}" ${treeConfig.sort_by === s.value ? 'selected' : ''}>${s.label}</option>`).join('');

            dynamicFields += `
                <div class="form-group">
                    <label for="prop-root-category">Starting Category</label>
                    <select id="prop-root-category" class="form-control">
                        <option value="">All Categories (Root Level)</option>
                        ${categoryOptions}
                    </select>
                    <small class="form-hint">Leave empty to show all top-level categories</small>
                </div>
                <div class="form-group">
                    <label for="prop-tree-depth">Maximum Depth</label>
                    <select id="prop-tree-depth" class="form-control">
                        ${depthOptions}
                    </select>
                    <small class="form-hint">How many levels of subcategories to show</small>
                </div>
                <div class="form-group">
                    <label for="prop-tree-sort">Sort Order</label>
                    <select id="prop-tree-sort" class="form-control">
                        ${sortOptions}
                    </select>
                </div>
                <div class="form-group checkbox-wrapper">
                    <input type="checkbox" id="prop-tree-show-empty" ${treeConfig.show_empty !== false ? 'checked' : ''}>
                    <label for="prop-tree-show-empty">Show empty categories</label>
                </div>
                <div class="form-group checkbox-wrapper">
                    <input type="checkbox" id="prop-tree-show-counts" ${treeConfig.show_product_count ? 'checked' : ''}>
                    <label for="prop-tree-show-counts">Show product counts</label>
                </div>
            `;
        }

        const showUrlField = ['link', 'custom_url'].includes(item.item_type);
        const showTitleField = !['divider'].includes(item.item_type);

        return `
            <div class="property-section">
                <h4 class="property-section-title">
                    <i class="fas fa-sliders-h"></i>
                    Basic Settings
                </h4>

                <div class="form-group">
                    <label for="prop-item-type">Item Type</label>
                    <select id="prop-item-type" class="form-control">
                        ${typeOptions}
                    </select>
                </div>

                ${showTitleField ? `
                    <div class="form-group">
                        <label for="prop-title">Title</label>
                        <input type="text" id="prop-title" class="form-control" value="${this.escapeHtml(item.title || '')}">
                    </div>
                ` : ''}

                ${showUrlField ? `
                    <div class="form-group">
                        <label for="prop-url">URL</label>
                        <input type="text" id="prop-url" class="form-control" value="${this.escapeHtml(item.url || '')}" placeholder="https://...">
                    </div>
                ` : ''}

                ${dynamicFields}
            </div>

            <div class="property-section">
                <h4 class="property-section-title">
                    <i class="fas fa-icons"></i>
                    Icon & Badge
                </h4>

                <div class="form-group">
                    <label>Icon</label>
                    <button class="icon-picker-btn" id="prop-icon-btn">
                        <div class="icon-preview">
                            <i class="fas ${item.icon || 'fa-icons'}"></i>
                        </div>
                        <span class="icon-text">${item.icon || 'No icon selected'}</span>
                    </button>
                </div>

                <div class="form-group">
                    <label for="prop-badge-text">Badge Text</label>
                    <input type="text" id="prop-badge-text" class="form-control" value="${this.escapeHtml(item.badge_text || '')}" placeholder="e.g., New">
                </div>

                <div class="form-group">
                    <label for="prop-badge-color">Badge Color</label>
                    <div class="color-picker-wrapper">
                        <input type="color" class="color-swatch" id="prop-badge-color-picker" value="${item.badge_color || '#888888'}">
                        <input type="text" id="prop-badge-color" class="form-control color-input" value="${item.badge_color || ''}" placeholder="Theme default">
                    </div>
                </div>
            </div>

            <div class="property-section">
                <h4 class="property-section-title">
                    <i class="fas fa-cog"></i>
                    Behavior
                </h4>

                <div class="form-group">
                    <label for="prop-target">Open In</label>
                    <select id="prop-target" class="form-control">
                        <option value="_self" ${item.target === '_self' ? 'selected' : ''}>Same Window</option>
                        <option value="_blank" ${item.target === '_blank' ? 'selected' : ''}>New Tab</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="prop-css-classes">CSS Classes</label>
                    <input type="text" id="prop-css-classes" class="form-control" value="${this.escapeHtml(item.css_classes || '')}" placeholder="custom-class">
                </div>

                <div class="form-group checkbox-wrapper">
                    <input type="checkbox" id="prop-is-active" ${item.is_active !== false ? 'checked' : ''}>
                    <label for="prop-is-active">Active</label>
                </div>
            </div>
        `;
    }

    getStylePropertiesHtml(item) {
        const styleConfig = item.style_config || {};

        return `
            <div class="property-section">
                <h4 class="property-section-title">
                    <i class="fas fa-palette"></i>
                    Colors
                </h4>
                <p class="property-section-hint">Leave blank to use theme defaults</p>

                <div class="form-group">
                    <label for="style-text-color">Text Color</label>
                    <div class="color-picker-wrapper">
                        <input type="color" class="color-swatch" id="style-text-color-picker" value="${styleConfig.text_color || '#888888'}">
                        <input type="text" id="style-text-color" class="form-control color-input" value="${styleConfig.text_color || ''}" placeholder="Theme default">
                    </div>
                </div>

                <div class="form-group">
                    <label for="style-hover-color">Hover Color</label>
                    <div class="color-picker-wrapper">
                        <input type="color" class="color-swatch" id="style-hover-color-picker" value="${styleConfig.hover_color || '#888888'}">
                        <input type="text" id="style-hover-color" class="form-control color-input" value="${styleConfig.hover_color || ''}" placeholder="Theme default">
                    </div>
                </div>

                <div class="form-group">
                    <label for="style-bg-color">Background Color</label>
                    <div class="color-picker-wrapper">
                        <input type="color" class="color-swatch" id="style-bg-color-picker" value="${styleConfig.background || '#888888'}">
                        <input type="text" id="style-bg-color" class="form-control color-input" value="${styleConfig.background || ''}" placeholder="Theme default">
                    </div>
                </div>
            </div>

            <div class="property-section">
                <h4 class="property-section-title">
                    <i class="fas fa-font"></i>
                    Typography
                </h4>

                <div class="form-group">
                    <label for="style-font-weight">Font Weight</label>
                    <select id="style-font-weight" class="form-control">
                        <option value="">Default</option>
                        <option value="normal" ${styleConfig.font_weight === 'normal' ? 'selected' : ''}>Normal</option>
                        <option value="500" ${styleConfig.font_weight === '500' ? 'selected' : ''}>Medium</option>
                        <option value="600" ${styleConfig.font_weight === '600' ? 'selected' : ''}>Semi-Bold</option>
                        <option value="bold" ${styleConfig.font_weight === 'bold' ? 'selected' : ''}>Bold</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="style-font-size">Font Size</label>
                    <input type="text" id="style-font-size" class="form-control" value="${styleConfig.font_size || ''}" placeholder="inherit">
                </div>
            </div>

            <div class="property-section">
                <h4 class="property-section-title">
                    <i class="fas fa-expand-arrows-alt"></i>
                    Spacing
                </h4>

                <div class="form-group">
                    <label for="style-padding">Padding</label>
                    <input type="text" id="style-padding" class="form-control" value="${styleConfig.padding || ''}" placeholder="e.g., 8px 16px">
                </div>
            </div>
        `;
    }

    getVisibilityPropertiesHtml(item) {
        const visibilityRules = item.visibility_rules || [];
        const deviceRule = visibilityRules.find(r => r.type === 'device') || { value: ['desktop', 'tablet', 'mobile'] };
        const userRule = visibilityRules.find(r => r.type === 'user_status') || { value: 'all' };

        const devices = deviceRule.value || ['desktop', 'tablet', 'mobile'];

        return `
            <div class="property-section">
                <h4 class="property-section-title">
                    <i class="fas fa-desktop"></i>
                    Device Visibility
                </h4>

                <div class="form-group">
                    <p style="font-size: 0.8125rem; color: var(--mb-text-secondary); margin-bottom: 0.75rem;">
                        Show this item on:
                    </p>
                    <div class="checkbox-wrapper" style="margin-bottom: 0.5rem;">
                        <input type="checkbox" id="vis-desktop" ${devices.includes('desktop') ? 'checked' : ''}>
                        <label for="vis-desktop"><i class="fas fa-desktop"></i> Desktop</label>
                    </div>
                    <div class="checkbox-wrapper" style="margin-bottom: 0.5rem;">
                        <input type="checkbox" id="vis-tablet" ${devices.includes('tablet') ? 'checked' : ''}>
                        <label for="vis-tablet"><i class="fas fa-tablet-alt"></i> Tablet</label>
                    </div>
                    <div class="checkbox-wrapper">
                        <input type="checkbox" id="vis-mobile" ${devices.includes('mobile') ? 'checked' : ''}>
                        <label for="vis-mobile"><i class="fas fa-mobile-alt"></i> Mobile</label>
                    </div>
                </div>
            </div>

            <div class="property-section">
                <h4 class="property-section-title">
                    <i class="fas fa-user"></i>
                    User Visibility
                </h4>

                <div class="form-group">
                    <label for="vis-user-status">Show to:</label>
                    <select id="vis-user-status" class="form-control">
                        <option value="all" ${userRule.value === 'all' ? 'selected' : ''}>All Users</option>
                        <option value="logged_in" ${userRule.value === 'logged_in' ? 'selected' : ''}>Logged In Only</option>
                        <option value="logged_out" ${userRule.value === 'logged_out' ? 'selected' : ''}>Logged Out Only</option>
                    </select>
                </div>
            </div>
        `;
    }

    bindPropertyEvents(item) {
        // Item type change
        const typeSelect = document.getElementById('prop-item-type');
        if (typeSelect) {
            typeSelect.addEventListener('change', (e) => {
                item.item_type = e.target.value;
                this.renderPropertiesPanel(item);
                this.markUnsaved();
            });
        }

        // Title
        const titleInput = document.getElementById('prop-title');
        if (titleInput) {
            titleInput.addEventListener('input', (e) => {
                item.title = e.target.value;
                this.updateItemDisplay(item);
                this.markUnsaved();
            });
        }

        // URL
        const urlInput = document.getElementById('prop-url');
        if (urlInput) {
            urlInput.addEventListener('input', (e) => {
                item.url = e.target.value;
                this.markUnsaved();
            });
        }

        // Page reference - searchable select
        const pageSearchInput = document.getElementById('prop-page-search');
        if (pageSearchInput) {
            this.setupPropertySearchable(pageSearchInput, 'pages', item, 'page_reference_id');
        }

        // Category reference - searchable select
        const categorySearchInput = document.getElementById('prop-category-search');
        if (categorySearchInput) {
            this.setupPropertySearchable(categorySearchInput, 'categories', item, 'category_reference_id');
        }

        // Widget type
        const widgetTypeSelect = document.getElementById('prop-widget-type');
        if (widgetTypeSelect) {
            widgetTypeSelect.addEventListener('change', (e) => {
                if (!item.widget_config) item.widget_config = {};
                item.widget_config.widget_type = e.target.value;
                this.markUnsaved();
            });
        }

        // Category tree configuration
        if (item.item_type === 'category_tree') {
            if (!item.tree_config) item.tree_config = {};

            const rootCategorySelect = document.getElementById('prop-root-category');
            if (rootCategorySelect) {
                rootCategorySelect.addEventListener('change', (e) => {
                    item.tree_config.root_category_id = e.target.value ? parseInt(e.target.value) : null;
                    this.markUnsaved();
                });
            }

            const treeDepthSelect = document.getElementById('prop-tree-depth');
            if (treeDepthSelect) {
                treeDepthSelect.addEventListener('change', (e) => {
                    item.tree_config.max_depth = parseInt(e.target.value);
                    this.markUnsaved();
                });
            }

            const treeSortSelect = document.getElementById('prop-tree-sort');
            if (treeSortSelect) {
                treeSortSelect.addEventListener('change', (e) => {
                    item.tree_config.sort_by = e.target.value;
                    this.markUnsaved();
                });
            }

            const showEmptyCheckbox = document.getElementById('prop-tree-show-empty');
            if (showEmptyCheckbox) {
                showEmptyCheckbox.addEventListener('change', (e) => {
                    item.tree_config.show_empty = e.target.checked;
                    this.markUnsaved();
                });
            }

            const showCountsCheckbox = document.getElementById('prop-tree-show-counts');
            if (showCountsCheckbox) {
                showCountsCheckbox.addEventListener('change', (e) => {
                    item.tree_config.show_product_count = e.target.checked;
                    this.markUnsaved();
                });
            }
        }

        // Icon picker
        const iconBtn = document.getElementById('prop-icon-btn');
        if (iconBtn) {
            iconBtn.addEventListener('click', () => this.showIconPicker(item));
        }

        // Badge text
        const badgeTextInput = document.getElementById('prop-badge-text');
        if (badgeTextInput) {
            badgeTextInput.addEventListener('input', (e) => {
                item.badge_text = e.target.value;
                this.markUnsaved();
            });
        }

        // Badge color
        const badgeColorPicker = document.getElementById('prop-badge-color-picker');
        const badgeColorInput = document.getElementById('prop-badge-color');
        if (badgeColorPicker && badgeColorInput) {
            badgeColorPicker.addEventListener('input', (e) => {
                item.badge_color = e.target.value;
                badgeColorInput.value = e.target.value;
                this.markUnsaved();
            });
            badgeColorInput.addEventListener('input', (e) => {
                item.badge_color = e.target.value;
                if (/^#[0-9A-Fa-f]{6}$/.test(e.target.value)) {
                    badgeColorPicker.value = e.target.value;
                }
                this.markUnsaved();
            });
        }

        // Target
        const targetSelect = document.getElementById('prop-target');
        if (targetSelect) {
            targetSelect.addEventListener('change', (e) => {
                item.target = e.target.value;
                this.markUnsaved();
            });
        }

        // CSS classes
        const cssClassesInput = document.getElementById('prop-css-classes');
        if (cssClassesInput) {
            cssClassesInput.addEventListener('input', (e) => {
                item.css_classes = e.target.value;
                this.markUnsaved();
            });
        }

        // Is active
        const isActiveCheckbox = document.getElementById('prop-is-active');
        if (isActiveCheckbox) {
            isActiveCheckbox.addEventListener('change', (e) => {
                item.is_active = e.target.checked;
                this.markUnsaved();
            });
        }
    }

    bindStyleEvents(item) {
        if (!item.style_config) item.style_config = {};

        const styleFields = [
            { picker: 'style-text-color-picker', input: 'style-text-color', key: 'text_color' },
            { picker: 'style-hover-color-picker', input: 'style-hover-color', key: 'hover_color' },
            { picker: 'style-bg-color-picker', input: 'style-bg-color', key: 'background' }
        ];

        styleFields.forEach(({ picker, input, key }) => {
            const pickerEl = document.getElementById(picker);
            const inputEl = document.getElementById(input);
            if (pickerEl && inputEl) {
                pickerEl.addEventListener('input', (e) => {
                    item.style_config[key] = e.target.value;
                    inputEl.value = e.target.value;
                    this.markUnsaved();
                });
                inputEl.addEventListener('input', (e) => {
                    item.style_config[key] = e.target.value;
                    if (/^#[0-9A-Fa-f]{6}$/.test(e.target.value)) {
                        pickerEl.value = e.target.value;
                    }
                    this.markUnsaved();
                });
            }
        });

        // Font weight
        const fontWeightSelect = document.getElementById('style-font-weight');
        if (fontWeightSelect) {
            fontWeightSelect.addEventListener('change', (e) => {
                item.style_config.font_weight = e.target.value;
                this.markUnsaved();
            });
        }

        // Font size
        const fontSizeInput = document.getElementById('style-font-size');
        if (fontSizeInput) {
            fontSizeInput.addEventListener('input', (e) => {
                item.style_config.font_size = e.target.value;
                this.markUnsaved();
            });
        }

        // Padding
        const paddingInput = document.getElementById('style-padding');
        if (paddingInput) {
            paddingInput.addEventListener('input', (e) => {
                item.style_config.padding = e.target.value;
                this.markUnsaved();
            });
        }
    }

    bindVisibilityEvents(item) {
        if (!item.visibility_rules) item.visibility_rules = [];

        // Device checkboxes
        ['desktop', 'tablet', 'mobile'].forEach(device => {
            const checkbox = document.getElementById(`vis-${device}`);
            if (checkbox) {
                checkbox.addEventListener('change', () => {
                    this.updateDeviceVisibility(item);
                });
            }
        });

        // User status
        const userStatusSelect = document.getElementById('vis-user-status');
        if (userStatusSelect) {
            userStatusSelect.addEventListener('change', (e) => {
                const userRule = item.visibility_rules.find(r => r.type === 'user_status');
                if (userRule) {
                    userRule.value = e.target.value;
                } else {
                    item.visibility_rules.push({ type: 'user_status', value: e.target.value });
                }
                this.markUnsaved();
            });
        }
    }

    updateDeviceVisibility(item) {
        const devices = [];
        if (document.getElementById('vis-desktop')?.checked) devices.push('desktop');
        if (document.getElementById('vis-tablet')?.checked) devices.push('tablet');
        if (document.getElementById('vis-mobile')?.checked) devices.push('mobile');

        const deviceRule = item.visibility_rules.find(r => r.type === 'device');
        if (deviceRule) {
            deviceRule.value = devices;
        } else {
            item.visibility_rules.push({ type: 'device', value: devices });
        }
        this.markUnsaved();
    }

    updateItemDisplay(item) {
        const element = document.querySelector(`[data-item-id="${item.id}"]`);
        if (element) {
            const titleEl = element.querySelector('.item-title');
            if (titleEl) {
                titleEl.textContent = item.title || this.config.translations.untitled || 'Untitled';
            }
        }
    }

    // =========================================
    // Item CRUD Operations
    // =========================================

    addItemFromLibrary(type, widgetType = null, pageId = null, categoryId = null) {
        const newItem = this.createNewItem(type, widgetType, pageId, categoryId);
        this.itemsTree.push(newItem);
        this.renderItemsTree();
        this.selectItem(newItem);
        this.saveHistoryState();
        this.markUnsaved();
        this.showToast(this.config.translations.itemAdded || 'Item added', 'success');
    }

    createNewItem(type, widgetType = null, pageId = null, categoryId = null) {
        // Get title from reference if available
        let title = this.getDefaultTitle(type, widgetType);
        let url = '';

        if (type === 'page' && pageId) {
            const page = this.availablePages.find(p => String(p.id) === String(pageId));
            if (page) {
                title = page.title;
                url = page.url || `/${page.slug}/`;
            }
        } else if (type === 'category' && categoryId) {
            const category = this.availableCategories.find(c => String(c.id) === String(categoryId));
            if (category) {
                title = category.name;
                url = category.url || `/category/${category.slug}/`;
            }
        }

        const item = {
            id: `new-${Date.now()}`,
            item_type: type,
            title: title,
            url: url,
            target: '_self',
            icon: '',
            badge_text: '',
            badge_color: '',
            css_classes: '',
            order: this.itemsTree.length,
            is_active: true,
            page_reference_id: pageId ? parseInt(pageId) : null,
            category_reference_id: categoryId ? parseInt(categoryId) : null,
            style_config: {},
            widget_config: widgetType ? { widget_type: widgetType } : {},
            tree_config: type === 'category_tree' ? {
                root_category_id: null,
                max_depth: 3,
                sort_by: 'name',
                show_empty: true,
                show_product_count: false
            } : {},
            visibility_rules: [],
            translations: {},
            children: []
        };

        return item;
    }

    getDefaultTitle(type, widgetType) {
        const titles = {
            'link': 'New Link',
            'page': 'Page Link',
            'category': 'Category Link',
            'category_tree': 'All Categories',
            'custom_url': 'Custom URL',
            'divider': '',
            'header': 'Section Header',
            'widget': widgetType ? this.getWidgetTitle(widgetType) : 'Widget'
        };
        return titles[type] || 'New Item';
    }

    getWidgetTitle(widgetType) {
        const titles = {
            'login_toggle': 'Login/Logout',
            'cart': 'Shopping Cart',
            'account': 'My Account',
            'wishlist': 'Wishlist',
            'search': 'Search'
        };
        return titles[widgetType] || 'Widget';
    }

    duplicateItem(item) {
        const duplicate = JSON.parse(JSON.stringify(item));
        duplicate.id = `dup-${Date.now()}`;
        duplicate.title = `${item.title} (Copy)`;

        // Reset IDs in children recursively
        const resetIds = (items) => {
            items.forEach(child => {
                child.id = `dup-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
                if (child.children) resetIds(child.children);
            });
        };
        if (duplicate.children) resetIds(duplicate.children);

        // Find parent and insert after original
        const parent = this.findParent(this.itemsTree, item.id);
        if (parent) {
            const index = parent.children.findIndex(i => i.id === item.id);
            parent.children.splice(index + 1, 0, duplicate);
        } else {
            const index = this.itemsTree.findIndex(i => i.id === item.id);
            this.itemsTree.splice(index + 1, 0, duplicate);
        }

        this.renderItemsTree();
        this.selectItem(duplicate);
        this.saveHistoryState();
        this.markUnsaved();
        this.showToast('Item duplicated', 'success');
    }

    async deleteItem(item) {
        if (!await AdminModal.confirm({
            message: this.config.translations.deleteConfirm || 'Are you sure you want to delete this menu item and all its children?',
            danger: true,
            confirmText: 'Delete'
        })) {
            return;
        }

        this.findAndRemoveItem(this.itemsTree, item.id);

        if (this.selectedItem?.id === item.id) {
            this.selectedItem = null;
            this.renderPropertiesPanel(null);
        }

        this.renderItemsTree();
        this.saveHistoryState();
        this.markUnsaved();
        this.showToast(this.config.translations.itemRemoved || 'Item removed', 'success');
    }

    findParent(items, itemId, parent = null) {
        for (const item of items) {
            if (String(item.id) === String(itemId)) return parent;
            if (item.children && item.children.length > 0) {
                const found = this.findParent(item.children, itemId, item);
                if (found !== undefined) return found;
            }
        }
        return undefined;
    }

    // =========================================
    // Modals
    // =========================================

    showAddItemModal(parentId = null) {
        this.addItemParentId = parentId;
        document.getElementById('add-item-modal')?.classList.remove('hidden');
        this.updateAddItemForm();
        document.getElementById('new-item-title')?.focus();
    }

    hideAddItemModal() {
        document.getElementById('add-item-modal')?.classList.add('hidden');
        this.addItemParentId = null;
    }

    updateAddItemForm() {
        const type = document.getElementById('new-item-type')?.value || 'link';

        const titleGroup = document.getElementById('new-item-title-group');
        const urlGroup = document.getElementById('new-item-url-group');
        const pageGroup = document.getElementById('new-item-page-group');
        const categoryGroup = document.getElementById('new-item-category-group');
        const widgetGroup = document.getElementById('new-item-widget-group');

        // Show/hide fields based on type
        if (titleGroup) titleGroup.classList.toggle('hidden', type === 'divider');
        if (urlGroup) urlGroup.classList.toggle('hidden', !['link', 'custom_url'].includes(type));
        if (pageGroup) pageGroup.classList.toggle('hidden', type !== 'page');
        if (categoryGroup) categoryGroup.classList.toggle('hidden', type !== 'category');
        if (widgetGroup) widgetGroup.classList.toggle('hidden', type !== 'widget');

        // Populate page options
        if (type === 'page') {
            const pageSelect = document.getElementById('new-item-page');
            if (pageSelect) {
                pageSelect.innerHTML = '<option value="">-- Select a page --</option>' +
                    this.availablePages.map(p => `<option value="${p.id}">${p.title}</option>`).join('');
            }
        }

        // Populate category options
        if (type === 'category') {
            const categorySelect = document.getElementById('new-item-category');
            if (categorySelect) {
                categorySelect.innerHTML = '<option value="">-- Select a category --</option>' +
                    this.availableCategories.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
            }
        }
    }

    confirmAddItem() {
        const type = document.getElementById('new-item-type')?.value || 'link';
        const title = document.getElementById('new-item-title')?.value || this.getDefaultTitle(type);
        const url = document.getElementById('new-item-url')?.value || '';
        const pageId = document.getElementById('new-item-page')?.value;
        const categoryId = document.getElementById('new-item-category')?.value;
        const widgetType = document.getElementById('new-item-widget-type')?.value;

        const newItem = {
            id: `new-${Date.now()}`,
            item_type: type,
            title: title,
            url: url,
            target: '_self',
            icon: '',
            badge_text: '',
            badge_color: '',
            css_classes: '',
            order: 0,
            is_active: true,
            page_reference_id: pageId ? parseInt(pageId) : null,
            category_reference_id: categoryId ? parseInt(categoryId) : null,
            style_config: {},
            widget_config: type === 'widget' ? { widget_type: widgetType } : {},
            visibility_rules: [],
            translations: {},
            children: []
        };

        // Set title from reference if not provided
        if (type === 'page' && pageId && !title) {
            const page = this.availablePages.find(p => String(p.id) === String(pageId));
            if (page) newItem.title = page.title;
        }
        if (type === 'category' && categoryId && !title) {
            const category = this.availableCategories.find(c => String(c.id) === String(categoryId));
            if (category) newItem.title = category.name;
        }

        // Add to parent or root
        if (this.addItemParentId) {
            const parent = this.findItemById(this.itemsTree, this.addItemParentId);
            if (parent) {
                if (!parent.children) parent.children = [];
                parent.children.push(newItem);
            }
        } else {
            this.itemsTree.push(newItem);
        }

        this.hideAddItemModal();
        this.renderItemsTree();
        this.selectItem(newItem);
        this.saveHistoryState();
        this.markUnsaved();
        this.showToast(this.config.translations.itemAdded || 'Item added', 'success');
    }

    showMenuSettingsModal() {
        document.getElementById('menu-settings-modal')?.classList.remove('hidden');
    }

    hideMenuSettingsModal() {
        document.getElementById('menu-settings-modal')?.classList.add('hidden');
    }

    async saveMenuSettings() {
        const name = document.getElementById('menu-name')?.value;
        const location = document.getElementById('menu-location')?.value;
        const displayType = document.getElementById('menu-display-type')?.value;
        const description = document.getElementById('menu-description')?.value;
        const isActive = document.getElementById('menu-is-active')?.checked;

        try {
            const response = await fetch(this.config.apiMenuUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    name,
                    location,
                    display_type: displayType,
                    description,
                    is_active: isActive
                })
            });

            if (!response.ok) throw new Error('Failed to save menu settings');

            // Update display
            document.querySelector('.menu-name-display').textContent = name;

            this.hideMenuSettingsModal();
            this.showToast(this.config.translations.menuUpdated || 'Menu settings updated', 'success');
        } catch (error) {
            console.error('Error saving menu settings:', error);
            this.showToast('Error saving menu settings', 'error');
        }
    }

    showNewMenuModal() {
        document.getElementById('new-menu-modal')?.classList.remove('hidden');
        document.getElementById('create-menu-name')?.focus();
    }

    hideNewMenuModal() {
        document.getElementById('new-menu-modal')?.classList.add('hidden');
    }

    async createNewMenu() {
        const name = document.getElementById('create-menu-name')?.value;
        const location = document.getElementById('create-menu-location')?.value;
        const displayType = document.getElementById('create-menu-display-type')?.value;

        if (!name) {
            this.showToast('Menu name is required', 'warning');
            return;
        }

        try {
            const response = await fetch(this.config.apiBaseUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    name,
                    location,
                    display_type: displayType
                })
            });

            if (!response.ok) throw new Error('Failed to create menu');

            const data = await response.json();
            this.hideNewMenuModal();
            this.showToast(this.config.translations.menuCreated || 'Menu created', 'success');

            // Redirect to new menu
            window.location.href = `/theme/menu/${data.id}/builder/`;
        } catch (error) {
            console.error('Error creating menu:', error);
            this.showToast('Error creating menu', 'error');
        }
    }

    showIconPicker(item) {
        this.iconPickerTarget = item;
        const modal = document.getElementById('icon-picker-modal');
        if (modal) {
            modal.classList.remove('hidden');
            this.loadIconGrid();
        }
    }

    hideIconPicker() {
        document.getElementById('icon-picker-modal')?.classList.add('hidden');
        this.iconPickerTarget = null;
    }

    loadIconGrid() {
        const grid = document.getElementById('icon-grid');
        if (!grid) return;

        // Common FontAwesome icons
        const icons = [
            'fa-home', 'fa-user', 'fa-cog', 'fa-shopping-cart', 'fa-heart',
            'fa-star', 'fa-search', 'fa-envelope', 'fa-phone', 'fa-map-marker-alt',
            'fa-calendar', 'fa-clock', 'fa-bell', 'fa-bookmark', 'fa-tag',
            'fa-folder', 'fa-file', 'fa-image', 'fa-video', 'fa-music',
            'fa-link', 'fa-external-link-alt', 'fa-download', 'fa-upload', 'fa-share',
            'fa-lock', 'fa-key', 'fa-shield-alt', 'fa-check', 'fa-times',
            'fa-plus', 'fa-minus', 'fa-info-circle', 'fa-question-circle', 'fa-exclamation-circle',
            'fa-arrow-right', 'fa-arrow-left', 'fa-arrow-up', 'fa-arrow-down', 'fa-chevron-right',
            'fa-bars', 'fa-ellipsis-h', 'fa-ellipsis-v', 'fa-grip-vertical', 'fa-list',
            'fa-th', 'fa-th-large', 'fa-table', 'fa-chart-bar', 'fa-chart-pie',
            'fa-gift', 'fa-trophy', 'fa-certificate', 'fa-award', 'fa-medal',
            'fa-truck', 'fa-box', 'fa-shopping-bag', 'fa-credit-card', 'fa-wallet',
            'fa-percent', 'fa-dollar-sign', 'fa-euro-sign', 'fa-pound-sign', 'fa-coins',
            'fa-globe', 'fa-flag', 'fa-map', 'fa-compass', 'fa-location-arrow'
        ];

        grid.innerHTML = icons.map(icon => `
            <button class="icon-grid-item" data-icon="${icon}" title="${icon}">
                <i class="fas ${icon}"></i>
            </button>
        `).join('');

        grid.querySelectorAll('.icon-grid-item').forEach(btn => {
            btn.addEventListener('click', () => {
                this.selectIcon(btn.dataset.icon);
            });
        });
    }

    selectIcon(icon) {
        if (this.iconPickerTarget) {
            this.iconPickerTarget.icon = icon;

            // Update the icon button display
            const iconBtn = document.getElementById('prop-icon-btn');
            if (iconBtn) {
                iconBtn.querySelector('.icon-preview i').className = `fas ${icon || 'fa-icons'}`;
                iconBtn.querySelector('.icon-text').textContent = icon || 'No icon selected';
            }

            // Update tree display
            this.updateItemDisplay(this.iconPickerTarget);
            this.markUnsaved();
        }
        this.hideIconPicker();
    }

    // =========================================
    // Quick Add Sources
    // =========================================

    populateQuickAddSources() {
        // Setup search inputs for AJAX mode
        this.setupSearchInput('pages-search', 'pages');
        this.setupSearchInput('categories-search', 'categories');

        // Populate pages list
        if (this.pagesUseAjax) {
            // AJAX mode: show search prompt, don't load all
            this.showSearchPrompt('pages-list', this.config.translations?.typeToSearch || 'Type to search...');
        } else {
            // Embedded mode: render all pages
            this.renderPagesList(this.availablePages, false);
        }

        // Populate categories list
        if (this.categoriesUseAjax) {
            // AJAX mode: show search prompt, don't load all
            this.showSearchPrompt('categories-list', this.config.translations?.typeToSearch || 'Type to search...');
        } else {
            // Embedded mode: render all categories
            this.renderCategoriesList(this.availableCategories, false);
        }
    }

    /**
     * Setup debounced search input for AJAX mode
     */
    setupSearchInput(inputId, type) {
        const input = document.getElementById(inputId);
        if (!input) return;

        input.addEventListener('input', (e) => {
            clearTimeout(this.searchDebounceTimer);
            const query = e.target.value.trim();

            // Show loading state
            const listId = type === 'pages' ? 'pages-list' : 'categories-list';
            if (query.length > 0) {
                this.showSearchLoading(listId);
            }

            this.searchDebounceTimer = setTimeout(() => {
                if (type === 'pages') {
                    this.searchPages(query);
                } else {
                    this.searchCategories(query);
                }
            }, this.searchDebounceDelay);
        });
    }

    /**
     * Search pages via AJAX or filter locally
     */
    async searchPages(query) {
        const pagesList = document.getElementById('pages-list');
        if (!pagesList) return;

        // Empty query - show prompt for AJAX mode, or all items for embedded mode
        if (!query) {
            if (this.pagesUseAjax) {
                this.showSearchPrompt('pages-list', this.config.translations?.typeToSearch || 'Type to search...');
            } else {
                this.renderPagesList(this.availablePages, false);
            }
            return;
        }

        // For embedded mode with small dataset, filter locally
        if (!this.pagesUseAjax) {
            const filtered = this.availablePages.filter(p =>
                p.title.toLowerCase().includes(query.toLowerCase()) ||
                p.slug.toLowerCase().includes(query.toLowerCase())
            );
            this.renderPagesList(filtered, false);
            return;
        }

        // AJAX search for large datasets
        try {
            const response = await fetch(`${this.apiSourcesUrl}?type=pages&search=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.renderPagesList(data.pages || [], data.pages_has_more || false);
        } catch (error) {
            console.error('Error searching pages:', error);
            pagesList.innerHTML = `<p class="library-error">${this.config.translations?.error || 'Error'}</p>`;
        }
    }

    /**
     * Search categories via AJAX or filter locally
     */
    async searchCategories(query) {
        const categoriesList = document.getElementById('categories-list');
        if (!categoriesList) return;

        // Empty query - show prompt for AJAX mode, or all items for embedded mode
        if (!query) {
            if (this.categoriesUseAjax) {
                this.showSearchPrompt('categories-list', this.config.translations?.typeToSearch || 'Type to search...');
            } else {
                this.renderCategoriesList(this.availableCategories, false);
            }
            return;
        }

        // For embedded mode with small dataset, filter locally
        if (!this.categoriesUseAjax) {
            const filtered = this.availableCategories.filter(c =>
                c.name.toLowerCase().includes(query.toLowerCase()) ||
                c.slug.toLowerCase().includes(query.toLowerCase())
            );
            this.renderCategoriesList(filtered, false);
            return;
        }

        // AJAX search for large datasets
        try {
            const response = await fetch(`${this.apiSourcesUrl}?type=categories&search=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.renderCategoriesList(data.categories || [], data.categories_has_more || false);
        } catch (error) {
            console.error('Error searching categories:', error);
            categoriesList.innerHTML = `<p class="library-error">${this.config.translations?.error || 'Error'}</p>`;
        }
    }

    /**
     * Show search prompt in library section
     */
    showSearchPrompt(listId, message) {
        const list = document.getElementById(listId);
        if (list) {
            list.innerHTML = `<p class="library-prompt">${this.escapeHtml(message)}</p>`;
        }
    }

    /**
     * Show loading state in library section
     */
    showSearchLoading(listId) {
        const list = document.getElementById(listId);
        if (list) {
            list.classList.add('loading');
        }
    }

    /**
     * Render pages list with optional "has more" indicator
     */
    renderPagesList(pages, hasMore) {
        const pagesList = document.getElementById('pages-list');
        const pagesCount = document.getElementById('pages-count');

        if (!pagesList) return;

        pagesList.classList.remove('loading');

        if (pages.length > 0) {
            let html = pages.map(page => `
                <div class="library-item draggable-item" data-type="page" data-page-id="${page.id}" draggable="true">
                    <i class="fas fa-file"></i>
                    <span>${this.escapeHtml(page.title)}</span>
                </div>
            `).join('');

            if (hasMore) {
                html += `<p class="library-has-more">${this.config.translations?.moreResults || 'More results available. Refine your search.'}</p>`;
            }

            pagesList.innerHTML = html;

            // Only update count if not in AJAX mode (AJAX mode shows total from server)
            if (pagesCount && !this.pagesUseAjax) {
                pagesCount.textContent = pages.length;
            }

            // Bind drag and click events
            this.bindLibraryItemEvents(pagesList, 'page');
        } else {
            pagesList.innerHTML = `<p class="library-empty">${this.config.translations?.noResults || 'No results found'}</p>`;
        }
    }

    /**
     * Render categories list with optional "has more" indicator
     */
    renderCategoriesList(categories, hasMore) {
        const categoriesList = document.getElementById('categories-list');
        const categoriesCount = document.getElementById('categories-count');

        if (!categoriesList) return;

        categoriesList.classList.remove('loading');

        if (categories.length > 0) {
            let html = categories.map(cat => `
                <div class="library-item draggable-item" data-type="category" data-category-id="${cat.id}" draggable="true">
                    <i class="fas fa-folder"></i>
                    <span>${this.escapeHtml(cat.name)}</span>
                </div>
            `).join('');

            if (hasMore) {
                html += `<p class="library-has-more">${this.config.translations?.moreResults || 'More results available. Refine your search.'}</p>`;
            }

            categoriesList.innerHTML = html;

            // Only update count if not in AJAX mode (AJAX mode shows total from server)
            if (categoriesCount && !this.categoriesUseAjax) {
                categoriesCount.textContent = categories.length;
            }

            // Bind drag and click events
            this.bindLibraryItemEvents(categoriesList, 'category');
        } else {
            categoriesList.innerHTML = `<p class="library-empty">${this.config.translations?.noResults || 'No results found'}</p>`;
        }
    }

    /**
     * Bind drag and click events to library items
     */
    bindLibraryItemEvents(container, type) {
        container.querySelectorAll('.library-item').forEach(item => {
            item.addEventListener('dragstart', (e) => {
                const dragData = JSON.stringify({
                    type: type,
                    pageId: item.dataset.pageId,
                    categoryId: item.dataset.categoryId
                });
                e.dataTransfer.setData('application/x-menu-item', dragData);
                e.dataTransfer.setData('text/plain', dragData);
                e.dataTransfer.effectAllowed = 'copy';
                item.classList.add('dragging');
            });
            item.addEventListener('dragend', () => item.classList.remove('dragging'));
            item.addEventListener('click', () => {
                if (type === 'page') {
                    // For AJAX mode, we need to fetch or construct the page object
                    const pageId = item.dataset.pageId;
                    const title = item.querySelector('span').textContent;
                    const page = this.availablePages.find(p => String(p.id) === pageId) || {
                        id: parseInt(pageId),
                        title: title,
                        url: ''  // Will be resolved server-side
                    };
                    this.addPageItem(page);
                } else if (type === 'category') {
                    const categoryId = item.dataset.categoryId;
                    const name = item.querySelector('span').textContent;
                    const category = this.availableCategories.find(c => String(c.id) === categoryId) || {
                        id: parseInt(categoryId),
                        name: name,
                        url: ''  // Will be resolved server-side
                    };
                    this.addCategoryItem(category);
                }
            });
        });
    }

    addPageItem(page) {
        const newItem = this.createNewItem('page');
        newItem.title = page.title;
        newItem.page_reference_id = page.id;
        newItem.url = page.url;

        this.itemsTree.push(newItem);
        this.renderItemsTree();
        this.selectItem(newItem);
        this.saveHistoryState();
        this.markUnsaved();
        this.showToast('Page added to menu', 'success');
    }

    addCategoryItem(category) {
        const newItem = this.createNewItem('category');
        newItem.title = category.name;
        newItem.category_reference_id = category.id;
        newItem.url = category.url;

        this.itemsTree.push(newItem);
        this.renderItemsTree();
        this.selectItem(newItem);
        this.saveHistoryState();
        this.markUnsaved();
        this.showToast('Category added to menu', 'success');
    }

    // =========================================
    // Property Panel Searchable Selects
    // =========================================

    /**
     * Setup a searchable select in the properties panel
     * @param {HTMLInputElement} input - The search input element
     * @param {string} type - 'pages' or 'categories'
     * @param {object} item - The menu item being edited
     * @param {string} refField - The reference field name (page_reference_id or category_reference_id)
     */
    setupPropertySearchable(input, type, item, refField) {
        const dropdownId = type === 'pages' ? 'prop-page-dropdown' : 'prop-category-dropdown';
        const hiddenId = type === 'pages' ? 'prop-page-reference' : 'prop-category-reference';
        const clearBtnId = type === 'pages' ? 'prop-page-clear' : 'prop-category-clear';
        const wrapper = input.closest('.searchable-select');

        let debounceTimer = null;

        // Focus handler - show dropdown
        input.addEventListener('focus', () => {
            this.showPropertyDropdown(type, '', dropdownId, item, refField);
            wrapper?.classList.add('focused');
        });

        // Input handler - search with debounce
        input.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            const query = e.target.value.trim();

            debounceTimer = setTimeout(() => {
                this.showPropertyDropdown(type, query, dropdownId, item, refField);
            }, 200);
        });

        // Blur handler - hide dropdown after delay (to allow click on items)
        input.addEventListener('blur', () => {
            setTimeout(() => {
                this.hidePropertyDropdown(dropdownId);
                wrapper?.classList.remove('focused');
            }, 200);
        });

        // Clear button handler
        const clearBtn = document.getElementById(clearBtnId);
        if (clearBtn) {
            clearBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                input.value = '';
                document.getElementById(hiddenId).value = '';
                item[refField] = null;
                this.markUnsaved();
                // Re-render to update clear button visibility
                this.renderPropertiesPanel(item);
            });
        }

        // Keyboard navigation
        input.addEventListener('keydown', (e) => {
            const dropdown = document.getElementById(dropdownId);
            if (!dropdown) return;

            const items = dropdown.querySelectorAll('.searchable-select-item');
            const currentIndex = Array.from(items).findIndex(i => i.classList.contains('highlighted'));

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                const nextIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
                this.highlightDropdownItem(items, nextIndex);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                const prevIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
                this.highlightDropdownItem(items, prevIndex);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                const highlighted = dropdown.querySelector('.searchable-select-item.highlighted');
                if (highlighted) {
                    highlighted.click();
                }
            } else if (e.key === 'Escape') {
                this.hidePropertyDropdown(dropdownId);
                input.blur();
            }
        });
    }

    /**
     * Highlight a dropdown item for keyboard navigation
     */
    highlightDropdownItem(items, index) {
        items.forEach((item, i) => {
            item.classList.toggle('highlighted', i === index);
            if (i === index) {
                item.scrollIntoView({ block: 'nearest' });
            }
        });
    }

    /**
     * Show property dropdown with search results
     */
    async showPropertyDropdown(type, query, dropdownId, item, refField) {
        const dropdown = document.getElementById(dropdownId);
        if (!dropdown) return;

        dropdown.innerHTML = '<div class="searchable-select-loading"><i class="fas fa-spinner fa-spin"></i></div>';
        dropdown.classList.add('visible');

        let results = [];
        let hasMore = false;

        try {
            // Check if we should use AJAX or local filtering
            const useAjax = type === 'pages' ? this.pagesUseAjax : this.categoriesUseAjax;
            const localData = type === 'pages' ? this.availablePages : this.availableCategories;

            if (useAjax || localData.length === 0) {
                // AJAX search
                const response = await fetch(`${this.apiSourcesUrl}?type=${type}&search=${encodeURIComponent(query)}`);
                const data = await response.json();

                if (type === 'pages') {
                    results = data.pages || [];
                    hasMore = data.pages_has_more || false;
                } else {
                    results = data.categories || [];
                    hasMore = data.categories_has_more || false;
                }
            } else {
                // Local filtering
                const searchLower = query.toLowerCase();
                if (type === 'pages') {
                    results = localData.filter(p =>
                        !query || p.title.toLowerCase().includes(searchLower) || p.slug?.toLowerCase().includes(searchLower)
                    );
                } else {
                    results = localData.filter(c =>
                        !query || c.name.toLowerCase().includes(searchLower) || c.slug?.toLowerCase().includes(searchLower)
                    );
                }
            }

            this.renderPropertyDropdown(dropdown, results, type, item, refField, hasMore);
        } catch (error) {
            console.error(`Error searching ${type}:`, error);
            dropdown.innerHTML = `<div class="searchable-select-error">${this.config.translations?.error || 'Error loading results'}</div>`;
        }
    }

    /**
     * Render the property dropdown with results
     */
    renderPropertyDropdown(dropdown, results, type, item, refField, hasMore) {
        if (results.length === 0) {
            dropdown.innerHTML = `<div class="searchable-select-empty">${this.config.translations?.noResults || 'No results found'}</div>`;
            return;
        }

        const inputId = type === 'pages' ? 'prop-page-search' : 'prop-category-search';
        const hiddenId = type === 'pages' ? 'prop-page-reference' : 'prop-category-reference';

        let html = results.map((r, index) => {
            const id = r.id;
            const title = type === 'pages' ? r.title : r.name;
            const isSelected = item[refField] === id;
            const icon = type === 'pages' ? 'fa-file' : 'fa-folder';

            return `
                <div class="searchable-select-item ${isSelected ? 'selected' : ''} ${index === 0 ? 'highlighted' : ''}"
                     data-id="${id}"
                     data-title="${this.escapeHtml(title)}">
                    <i class="fas ${icon}"></i>
                    <span>${this.escapeHtml(title)}</span>
                    ${isSelected ? '<i class="fas fa-check selected-icon"></i>' : ''}
                </div>
            `;
        }).join('');

        if (hasMore) {
            html += `<div class="searchable-select-more">${this.config.translations?.moreResults || 'More results available. Refine your search.'}</div>`;
        }

        dropdown.innerHTML = html;

        // Bind click handlers
        dropdown.querySelectorAll('.searchable-select-item').forEach(el => {
            el.addEventListener('mousedown', (e) => {
                e.preventDefault();  // Prevent blur on input
                const id = parseInt(el.dataset.id);
                const title = el.dataset.title;

                // Update the item
                item[refField] = id;
                this.markUnsaved();

                // Update the input and hidden field
                document.getElementById(inputId).value = title;
                document.getElementById(hiddenId).value = id;

                // Also update item title if it's the default
                const defaultTitles = ['Page Link', 'Category Link', 'New Link'];
                if (!item.title || defaultTitles.includes(item.title)) {
                    item.title = title;
                    this.updateItemDisplay(item);
                }

                // Hide dropdown and re-render panel to show clear button
                this.hidePropertyDropdown(dropdown.id);
                this.renderPropertiesPanel(item);
            });

            // Highlight on hover
            el.addEventListener('mouseenter', () => {
                dropdown.querySelectorAll('.searchable-select-item').forEach(i => i.classList.remove('highlighted'));
                el.classList.add('highlighted');
            });
        });
    }

    /**
     * Hide property dropdown
     */
    hidePropertyDropdown(dropdownId) {
        const dropdown = document.getElementById(dropdownId);
        if (dropdown) {
            dropdown.classList.remove('visible');
        }
    }

    // =========================================
    // API Operations
    // =========================================

    async saveMenu() {
        const saveBtn = document.getElementById('save-btn');
        if (saveBtn) {
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span class="btn-text">Saving...</span>';
        }

        try {
            const response = await fetch(this.config.apiSaveStructureUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({
                    items: this.itemsTree
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to save menu');
            }

            const data = await response.json();

            // Update item IDs with server-assigned IDs
            if (data.items) {
                this.itemsTree = data.items;
                this.renderItemsTree();
            }

            this.hasUnsavedChanges = false;
            this.showToast(this.config.translations.saved || 'Saved!', 'success');
        } catch (error) {
            console.error('Error saving menu:', error);
            this.showToast(error.message || 'Error saving menu', 'error');
        } finally {
            if (saveBtn) {
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fas fa-save"></i> <span class="btn-text">Save</span>';
            }
        }
    }

    async switchMenu(menuId) {
        if (this.hasUnsavedChanges) {
            if (!await AdminModal.confirm('You have unsaved changes. Switch menu anyway?')) {
                document.getElementById('menu-selector').value = this.menuId;
                return;
            }
        }
        window.location.href = `/theme/menu/${menuId}/builder/`;
    }

    // =========================================
    // Preview - Advanced Device Frame System
    // =========================================

    /**
     * Setup preview panel controls - device buttons, zoom, orientation
     */
    setupPreviewControls() {
        // Get DOM references
        this.previewPanel = document.getElementById('preview-panel');
        this.previewContent = document.getElementById('menu-preview-content');
        this.deviceFrame = document.getElementById('device-frame');
        this.frameWrapper = document.getElementById('preview-frame-wrapper');
        this.zoomSlider = document.getElementById('preview-zoom');
        this.zoomValue = document.querySelector('.zoom-value');
        this.deviceLabel = document.querySelector('.device-label');
        this.loadingIndicator = document.querySelector('.loading-indicator');

        // Device buttons in preview panel - use separate previewDevice state
        document.querySelectorAll('.preview-toolbar .device-buttons button[data-device]').forEach(btn => {
            btn.addEventListener('click', () => {
                this.previewDevice = btn.dataset.device;
                if (this.previewDevice !== 'desktop') {
                    this.previewOrientation = 'portrait';
                }
                this.applyDevice();
            });
        });

        // Orientation toggle - uses previewDevice state
        const orientationToggle = document.querySelector('.preview-toolbar .orientation-toggle');
        if (orientationToggle) {
            orientationToggle.addEventListener('click', () => {
                if (this.previewDevice === 'desktop') return;
                this.previewOrientation = this.previewOrientation === 'portrait' ? 'landscape' : 'portrait';
                this.applyDevice();
            });
        }

        // Zoom control
        if (this.zoomSlider) {
            this.zoomSlider.addEventListener('input', () => this.updateZoom());
        }

        // Expand button - opens preview in popup
        const expandBtn = document.getElementById('expand-preview-btn');
        if (expandBtn) {
            expandBtn.addEventListener('click', () => this.openPreviewPopup());
        }

        // Handle window resize for preview panel
        window.addEventListener('resize', () => {
            if (this.previewPanel && !this.previewPanel.classList.contains('hidden')) {
                this.fitToWrapper();
            }
        });
    }

    /**
     * Toggle preview panel visibility
     */
    async togglePreview() {
        const panel = document.getElementById('preview-panel');
        const builderContainer = document.querySelector('.menu-builder-container');

        if (panel) {
            panel.classList.toggle('hidden');
            builderContainer?.classList.toggle('preview-open');

            if (!panel.classList.contains('hidden')) {
                // Show loading state
                if (this.loadingIndicator) {
                    this.loadingIndicator.classList.add('active');
                }

                // Load theme CSS BEFORE rendering preview
                // This ensures styles are available when content is rendered
                await this.loadThemeCSS();

                // Hide loading state
                if (this.loadingIndicator) {
                    this.loadingIndicator.classList.remove('active');
                }

                // Initialize preview after CSS is loaded
                this.applyDevice();
                this.updatePreview();
            }
        }
    }

    /**
     * Hide preview panel
     */
    hidePreview() {
        const panel = document.getElementById('preview-panel');
        const builderContainer = document.querySelector('.menu-builder-container');

        panel?.classList.add('hidden');
        builderContainer?.classList.remove('preview-open');
    }

    /**
     * Get device chrome dimensions (borders, bezels) for each device type
     * These must match the CSS border widths in menu-builder.css
     *
     * Note: Chrome elements (buttons, stand, notch) use negative positioning
     * to appear outside the device frame, so we don't add extra space here.
     * The frame wrapper padding provides space for overflow visibility.
     */
    getDeviceChromeDimensions(device) {
        const chromeMap = {
            'desktop': {
                borderWidth: 16       // CSS: border: 16px solid
            },
            'tablet': {
                borderWidth: 20       // CSS: border: 20px solid
            },
            'mobile': {
                borderWidth: 10       // CSS: border: 10px solid
            }
        };
        return chromeMap[device] || chromeMap['desktop'];
    }

    /**
     * Apply device preset to preview frame
     * Uses previewDevice state (independent from main canvas currentDevice)
     */
    applyDevice() {
        const presetKey = this.previewDevice === 'desktop'
            ? 'desktop'
            : `${this.previewDevice}-${this.previewOrientation}`;

        const preset = DEVICE_PRESETS[presetKey];
        if (!preset || !this.previewContent || !this.deviceFrame) return;

        // Get chrome dimensions for this device
        const chrome = this.getDeviceChromeDimensions(this.previewDevice);

        // Update preview content dimensions (the actual viewport)
        this.previewContent.style.width = preset.w + 'px';
        this.previewContent.style.height = preset.h + 'px';

        // Calculate device frame dimensions: content + borders only
        // Chrome elements (buttons, stand, notch) use negative positioning
        // and overflow outside the frame - wrapper padding provides visibility
        const totalWidth = preset.w + (chrome.borderWidth * 2);
        const totalHeight = preset.h + (chrome.borderWidth * 2);

        // Set explicit dimensions on device frame for proper scaling
        this.deviceFrame.style.width = totalWidth + 'px';
        this.deviceFrame.style.height = totalHeight + 'px';

        // Store current preset dimensions for fitToWrapper
        this.currentPresetWidth = totalWidth;
        this.currentPresetHeight = totalHeight;

        // Update active button state in preview toolbar (uses previewDevice)
        document.querySelectorAll('.preview-toolbar .device-buttons button[data-device]').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.device === this.previewDevice);
        });

        // Update device frame class
        this.deviceFrame.className = 'device-frame ' + this.previewDevice;
        if (this.previewOrientation === 'landscape' && this.previewDevice !== 'desktop') {
            this.deviceFrame.classList.add('landscape');
        }

        // Show/hide orientation toggle
        const orientationToggle = document.querySelector('.preview-toolbar .orientation-toggle');
        if (orientationToggle) {
            orientationToggle.classList.toggle('visible', this.previewDevice !== 'desktop');
            const icon = orientationToggle.querySelector('i');
            if (icon) {
                icon.style.transform = this.previewOrientation === 'landscape' ? 'rotate(90deg)' : 'none';
            }
        }

        // Update device label
        if (this.deviceLabel) {
            this.deviceLabel.textContent = preset.label;
        }

        // Re-render menu with device-appropriate layout
        this.updatePreview();

        // Fit to wrapper after a brief delay for DOM update
        setTimeout(() => this.fitToWrapper(), 10);

        // NOTE: Do NOT update canvas device here - preview is independent
        // Canvas device is controlled separately via setDevicePreviewLegacy()
    }

    /**
     * Legacy device preview for canvas area (kept for backward compatibility)
     */
    setDevicePreviewLegacy(device) {
        // Update toggle button states for canvas toolbar
        document.querySelectorAll('.device-toggle').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.device === device);
        });

        // Update canvas container width
        const container = document.querySelector('.menu-tree-container');
        const canvasArea = document.querySelector('.menu-canvas-area');

        if (container && canvasArea) {
            const width = this.deviceWidths[device];

            if (width) {
                container.style.maxWidth = `${width}px`;
                container.style.margin = '0 auto';
                canvasArea.classList.add('device-preview-mode');
                canvasArea.dataset.device = device;
            } else {
                container.style.maxWidth = '';
                container.style.margin = '';
                canvasArea.classList.remove('device-preview-mode');
                canvasArea.dataset.device = 'desktop';
            }
        }

        // Update visibility indicators on items
        this.updateDeviceVisibilityIndicators(device);
    }

    /**
     * Fit device frame to wrapper with proper aspect-ratio-preserving scaling
     */
    fitToWrapper() {
        if (!this.frameWrapper || !this.deviceFrame || !this.previewContent) return;

        const bounds = this.frameWrapper.getBoundingClientRect();

        // Use consistent padding on all sides for centering
        const padding = 60;

        // Get the total device frame dimensions (set by applyDevice)
        const frameWidth = this.currentPresetWidth || parseInt(this.deviceFrame.style.width) || 1232;
        const frameHeight = this.currentPresetHeight || parseInt(this.deviceFrame.style.height) || 892;

        // Additional vertical space for device label below the frame
        const labelSpace = 80;

        // Available space in the wrapper
        const availableWidth = bounds.width - (padding * 2);
        const availableHeight = bounds.height - (padding * 2) - labelSpace;

        // Calculate uniform scale to fit the device frame while preserving aspect ratio
        const scaleX = availableWidth / frameWidth;
        const scaleY = availableHeight / frameHeight;

        // Use the smaller scale to ensure the entire device fits (uniform scaling preserves aspect ratio)
        const autoScale = Math.min(scaleX, scaleY, 1);

        // Apply manual zoom on top of auto-scale
        const scale = autoScale * (this.manualZoom / 100);

        // Minimum scale to keep the device visible
        const minScale = 0.15;
        const finalScale = Math.max(scale, minScale);

        // Apply transform with uniform scaling
        this.deviceFrame.style.transform = `translate(-50%, -50%) scale(${finalScale})`;
        this.deviceFrame.style.position = 'absolute';
        this.deviceFrame.style.left = '50%';
        this.deviceFrame.style.top = `calc(50% - ${labelSpace / 2}px)`;

        // Update zoom display
        const displayZoom = Math.round(finalScale * 100);
        const isConstrained = autoScale < 1;
        if (this.zoomValue) {
            // Show asterisk if we're constrained by available space
            this.zoomValue.textContent = isConstrained
                ? displayZoom + '%*'
                : this.manualZoom + '%';
        }
    }

    /**
     * Update zoom from slider
     */
    updateZoom() {
        if (!this.zoomSlider) return;

        this.manualZoom = parseInt(this.zoomSlider.value);
        if (this.zoomValue) {
            this.zoomValue.textContent = this.manualZoom + '%';
        }
        this.fitToWrapper();
    }

    /**
     * Update preview content - debounced for performance
     */
    updatePreview() {
        if (!this.previewContent) return;

        // Debounce the preview update
        clearTimeout(this.previewDebounceTimer);
        this.previewDebounceTimer = setTimeout(() => {
            this.renderPreviewContent();
        }, this.previewDebounceDelay);
    }

    /**
     * Render preview content - client-side generation
     */
    renderPreviewContent() {
        if (!this.previewContent) return;

        // Generate preview HTML based on current menu state
        const previewHtml = this.generatePreviewHtml();
        this.previewContent.innerHTML = previewHtml;

        // Setup hover handlers for custom hover colors
        this.setupPreviewHoverHandlers();

        // Only load server-rendered preview if there are NO unsaved changes
        // When there are unsaved changes, the client-side preview shows
        // the current in-memory state which the server doesn't have yet
        if (!this.hasUnsavedChanges) {
            this.loadServerPreview();
        }
    }

    /**
     * Setup hover handlers for preview items with custom hover colors
     * This is needed because inline styles can't use :hover pseudo-selectors
     */
    setupPreviewHoverHandlers() {
        if (!this.previewContent) return;

        // Use same class names as frontend widget
        const links = this.previewContent.querySelectorAll('.menu-link');
        links.forEach(link => {
            const parent = link.closest('.menu-item');
            if (!parent) return;

            // Get hover colors from CSS custom properties or data attributes
            const computedStyle = getComputedStyle(link);
            const hoverColor = computedStyle.getPropertyValue('--item-hover-color').trim();
            const hoverBg = computedStyle.getPropertyValue('--item-hover-bg').trim();

            // Store original styles
            const originalColor = link.style.color;
            const originalBg = link.style.backgroundColor;

            if (hoverColor || hoverBg) {
                link.addEventListener('mouseenter', () => {
                    if (hoverColor) link.style.color = hoverColor;
                    if (hoverBg) link.style.backgroundColor = hoverBg;
                });

                link.addEventListener('mouseleave', () => {
                    link.style.color = originalColor;
                    link.style.backgroundColor = originalBg;
                });
            }
        });
    }

    /**
     * Load preview from server API
     * Uses previewDevice state (independent from main canvas currentDevice)
     */
    async loadServerPreview() {
        if (!this.config.apiPreviewUrl) return;

        // Show loading indicator
        if (this.loadingIndicator) {
            this.loadingIndicator.classList.add('active');
        }

        try {
            const params = new URLSearchParams({
                device: this.previewDevice,
                display_type: this.config.displayType || 'horizontal'
            });

            const response = await fetch(`${this.config.apiPreviewUrl}?${params}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) throw new Error('Failed to load preview');

            const data = await response.json();
            if (data.html && this.previewContent) {
                this.previewContent.innerHTML = data.html;
            }
        } catch (error) {
            console.error('Error loading preview:', error);
            // Keep client-side preview as fallback
        } finally {
            if (this.loadingIndicator) {
                this.loadingIndicator.classList.remove('active');
            }
        }
    }

    /**
     * Generate preview HTML client-side
     * Uses the same class names as the frontend widget for accurate preview
     * Uses previewDevice state (independent from main canvas currentDevice)
     */
    generatePreviewHtml() {
        const items = this.itemsTree;
        const displayType = this.config.displayType || 'horizontal';

        // Build HTML with device class wrapper for CSS cascade
        // Structure: .device-{device} > .menu-preview > .widget-menu > .menu-list
        // Uses previewDevice for independent preview panel device selection
        let html = `<div class="device-${this.previewDevice}">`;
        html += `<div class="menu-preview menu-${displayType}">`;

        if (this.previewDevice === 'mobile' && displayType === 'horizontal') {
            // Show hamburger toggle for mobile
            html += `
                <div class="mobile-menu-header">
                    <button class="hamburger-toggle" onclick="this.closest('.menu-preview').classList.toggle('menu-open')">
                        <i class="fas fa-bars"></i>
                    </button>
                </div>
            `;
        }

        // Use same classes as frontend widget: .widget-menu > .menu-list > .menu-item > .menu-link
        html += `<nav class="widget-menu"><ul class="menu-list menu-${displayType}">`;

        for (const item of items) {
            html += this.renderPreviewItem(item, 0);
        }

        html += `</ul></nav></div></div>`;

        return html;
    }

    /**
     * Render a single preview item recursively
     * Uses the same class names as the frontend widget (menu_items.html partial)
     */
    renderPreviewItem(item, depth) {
        if (item.item_type === 'divider') {
            return '<li class="menu-divider"></li>';
        }

        if (item.item_type === 'header') {
            const headerStyle = this.buildHeaderStyle(item);
            return `<li class="menu-header" ${headerStyle}>${this.escapeHtml(item.title || 'Header')}</li>`;
        }

        const hasChildren = item.children && item.children.length > 0;
        const itemStyleAttr = this.buildItemContainerStyle(item);
        const linkStyleAttr = this.buildLinkStyle(item);

        // Use same classes as frontend widget: .menu-item, .menu-link, .dropdown-menu
        let html = `<li class="menu-item ${hasChildren ? 'has-dropdown' : ''}" ${itemStyleAttr}>`;
        html += `<a href="#" class="menu-link" ${linkStyleAttr} onclick="event.preventDefault()">`;

        if (item.icon) {
            const iconStyle = item.style_config?.icon_color ? `style="color: ${item.style_config.icon_color}"` : '';
            html += `<i class="${item.icon}" aria-hidden="true" ${iconStyle}></i>`;
        }

        html += `<span>${this.escapeHtml(item.title || 'Untitled')}</span>`;

        if (item.badge_text) {
            const badgeStyle = item.badge_color ? `background-color: ${item.badge_color}` : '';
            html += `<span class="menu-badge" style="${badgeStyle}">${this.escapeHtml(item.badge_text)}</span>`;
        }

        if (hasChildren) {
            html += `<i class="menu-chevron fas fa-chevron-down" aria-hidden="true"></i>`;
        }

        html += `</a>`;

        if (hasChildren) {
            html += `<ul class="dropdown-menu" role="menu">`;
            for (const child of item.children) {
                html += this.renderPreviewItem(child, depth + 1);
            }
            html += `</ul>`;
        }

        html += `</li>`;
        return html;
    }

    /**
     * Build inline style for the LI container (CSS custom properties for hover states)
     */
    buildItemContainerStyle(item) {
        const config = item.style_config || {};
        const styles = [];

        // CSS custom properties for hover states (used by CSS)
        if (config.hover_color) styles.push(`--item-hover-color: ${config.hover_color}`);
        if (config.hover_background) styles.push(`--item-hover-bg: ${config.hover_background}`);

        return styles.length ? `style="${styles.join('; ')}"` : '';
    }

    /**
     * Build inline style for the link element (direct styles that override theme)
     * These are applied directly to ensure they override theme CSS
     */
    buildLinkStyle(item) {
        const config = item.style_config || {};
        const styles = [];

        // Direct color styles that override theme
        if (config.text_color) styles.push(`color: ${config.text_color}`);
        if (config.background) styles.push(`background-color: ${config.background}`);
        if (config.font_weight) styles.push(`font-weight: ${config.font_weight}`);
        if (config.font_size) styles.push(`font-size: ${config.font_size}`);

        // Padding
        if (config.padding) {
            const padding = config.padding;
            if (typeof padding === 'object') {
                if (padding.top) styles.push(`padding-top: ${padding.top}`);
                if (padding.right) styles.push(`padding-right: ${padding.right}`);
                if (padding.bottom) styles.push(`padding-bottom: ${padding.bottom}`);
                if (padding.left) styles.push(`padding-left: ${padding.left}`);
            } else if (typeof padding === 'string') {
                styles.push(`padding: ${padding}`);
            }
        }

        // Also set CSS custom properties for CSS-based hover states
        if (config.text_color) styles.push(`--item-color: ${config.text_color}`);
        if (config.hover_color) styles.push(`--item-hover-color: ${config.hover_color}`);
        if (config.background) styles.push(`--item-bg: ${config.background}`);

        return styles.length ? `style="${styles.join('; ')}"` : '';
    }

    /**
     * Build inline style for header items
     */
    buildHeaderStyle(item) {
        const config = item.style_config || {};
        const styles = [];

        if (config.text_color) styles.push(`color: ${config.text_color}`);
        if (config.background) styles.push(`background-color: ${config.background}`);
        if (config.font_weight) styles.push(`font-weight: ${config.font_weight}`);
        if (config.font_size) styles.push(`font-size: ${config.font_size}`);

        return styles.length ? `style="${styles.join('; ')}"` : '';
    }

    /**
     * Build inline style attribute for menu item (legacy - kept for compatibility)
     */
    buildItemStyle(item) {
        return this.buildLinkStyle(item);
    }

    /**
     * Open preview in popup window for full-screen experience
     * Uses previewDevice state (independent from main canvas currentDevice)
     */
    openPreviewPopup() {
        const previewUrl = this.config.apiPreviewUrl || `/api/menu/${this.menuId}/preview/`;
        const popupUrl = `${previewUrl}?popup=1&device=${this.previewDevice}`;
        window.open(popupUrl, 'menuPreview', 'width=1200,height=800,resizable=yes');
    }

    // =========================================
    // Theme CSS Loading and Scoping
    // =========================================

    /**
     * Load and scope theme CSS to prevent it affecting admin UI
     * All selectors get prefixed with .device-frame .preview-content
     * Recursively resolves @import statements to inline imported CSS
     */
    async loadAndScopeCSS(url, styleId) {
        if (!url) return;

        try {
            // Fetch CSS with @import resolution
            const css = await this.fetchCSSWithImports(url);

            // Scope all CSS selectors to preview content
            const scopedCSS = this.scopeCSS(css, '.device-frame .preview-content');

            // Inject into style element
            const styleElement = document.getElementById(styleId);
            if (styleElement) {
                styleElement.textContent = scopedCSS;
            } else {
                console.warn(`[${styleId}] Style element not found`);
            }
        } catch (error) {
            console.warn(`Failed to load CSS from ${url}:`, error);
        }
    }

    /**
     * Fetch CSS and recursively resolve @import statements
     * @param {string} url - The URL of the CSS file
     * @param {Set} visited - URLs already fetched (prevent circular imports)
     * @returns {Promise<string>} - CSS with @imports inlined
     */
    async fetchCSSWithImports(url, visited = new Set()) {
        // Prevent circular imports
        if (visited.has(url)) {
            console.warn(`Circular @import detected, skipping: ${url}`);
            return '';
        }
        visited.add(url);

        try {
            const response = await fetch(url);
            if (!response.ok) {
                console.warn(`Failed to fetch CSS from ${url}: ${response.status}`);
                return '';
            }
            let css = await response.text();

            // Find and resolve @import statements
            // Matches: @import url("path"); @import url('path'); @import "path"; @import 'path';
            const importRegex = /@import\s+(?:url\s*\(\s*['"]?([^'")]+)['"]?\s*\)|['"]([^'"]+)['"]);?/gi;
            const baseUrl = new URL(url, window.location.href);

            // Find all imports and their positions
            const imports = [];
            let match;
            while ((match = importRegex.exec(css)) !== null) {
                const importPath = match[1] || match[2];
                imports.push({
                    fullMatch: match[0],
                    path: importPath,
                    index: match.index
                });
            }

            // Resolve imports in reverse order (to preserve indices)
            for (let i = imports.length - 1; i >= 0; i--) {
                const imp = imports[i];
                try {
                    // Resolve relative URL
                    const importUrl = new URL(imp.path, baseUrl).href;

                    // Recursively fetch imported CSS
                    const importedCss = await this.fetchCSSWithImports(importUrl, visited);

                    // Replace @import with the imported content
                    css = css.substring(0, imp.index) + importedCss + css.substring(imp.index + imp.fullMatch.length);
                } catch (e) {
                    console.warn(`Failed to resolve @import "${imp.path}":`, e);
                }
            }

            return css;
        } catch (error) {
            console.warn(`Failed to fetch CSS from ${url}:`, error);
            return '';
        }
    }

    /**
     * Scope CSS selectors to a container
     * Handles :root, html, body, @-rules, and regular selectors
     */
    scopeCSS(css, scopeSelector) {
        // Process CSS, handling @-rules and regular rulesets
        let result = '';
        let i = 0;

        while (i < css.length) {
            // Skip whitespace
            while (i < css.length && /\s/.test(css[i])) {
                result += css[i];
                i++;
            }

            if (i >= css.length) break;

            // Check for CSS comments /* ... */ and pass through as-is
            if (css[i] === '/' && i + 1 < css.length && css[i + 1] === '*') {
                let commentStart = i;
                i += 2; // Skip /*
                // Find closing */
                while (i < css.length - 1 && !(css[i] === '*' && css[i + 1] === '/')) {
                    i++;
                }
                i += 2; // Skip closing */
                result += css.substring(commentStart, i);
                continue;
            }

            // Check for @-rules
            if (css[i] === '@') {
                // Find the @-rule type
                let ruleStart = i;
                i++;
                let ruleName = '';
                while (i < css.length && /[a-zA-Z-]/.test(css[i])) {
                    ruleName += css[i];
                    i++;
                }

                // Handle different @-rules
                if (ruleName === 'media' || ruleName === 'supports' || ruleName === 'layer') {
                    // Find opening brace
                    while (i < css.length && css[i] !== '{') {
                        i++;
                    }
                    // Find matching closing brace (handle nesting)
                    let braceCount = 1;
                    let ruleContent = css.substring(ruleStart, i + 1);
                    i++;
                    let innerStart = i;

                    while (i < css.length && braceCount > 0) {
                        if (css[i] === '{') braceCount++;
                        else if (css[i] === '}') braceCount--;
                        i++;
                    }

                    // Recursively scope the inner content
                    let innerContent = css.substring(innerStart, i - 1);
                    let scopedInner = this.scopeCSS(innerContent, scopeSelector);
                    result += ruleContent + scopedInner + '}';

                } else if (ruleName === 'keyframes' || ruleName === '-webkit-keyframes') {
                    // Don't scope keyframes content - just copy as-is
                    while (i < css.length && css[i] !== '{') {
                        i++;
                    }
                    let braceCount = 1;
                    let keyframeRule = css.substring(ruleStart, i + 1);
                    i++;

                    while (i < css.length && braceCount > 0) {
                        if (css[i] === '{') braceCount++;
                        else if (css[i] === '}') braceCount--;
                        keyframeRule += css[i];
                        i++;
                    }
                    result += keyframeRule;

                } else {
                    // Other @-rules (font-face, import, etc.) - copy as-is until semicolon or brace
                    while (i < css.length && css[i] !== ';' && css[i] !== '{') {
                        i++;
                    }

                    if (css[i] === '{') {
                        let braceCount = 1;
                        i++;
                        while (i < css.length && braceCount > 0) {
                            if (css[i] === '{') braceCount++;
                            else if (css[i] === '}') braceCount--;
                            i++;
                        }
                    } else if (css[i] === ';') {
                        i++;
                    }
                    result += css.substring(ruleStart, i);
                }
            } else {
                // Regular ruleset - find selector and brace
                let selectorStart = i;
                while (i < css.length && css[i] !== '{') {
                    i++;
                }

                if (i >= css.length) break;

                let selector = css.substring(selectorStart, i).trim();

                // Scope the selector
                let scopedSelector = this.scopeSelectorList(selector, scopeSelector);
                result += scopedSelector + ' {';

                // Find the closing brace
                i++; // Skip opening brace
                let braceCount = 1;
                let declarationStart = i;

                while (i < css.length && braceCount > 0) {
                    if (css[i] === '{') braceCount++;
                    else if (css[i] === '}') braceCount--;
                    i++;
                }

                result += css.substring(declarationStart, i);
            }
        }

        return result;
    }

    /**
     * Scope a selector list (comma-separated selectors)
     */
    scopeSelectorList(selectorList, scopeSelector) {
        return selectorList.split(',').map(sel => {
            const s = sel.trim();

            // Convert :root to scope selector (preserves CSS variables)
            if (s === ':root' || s === ':root:root') {
                return scopeSelector;
            }
            if (s.startsWith(':root ')) {
                return scopeSelector + ' ' + s.substring(6);
            }
            if (s.startsWith(':root')) {
                return s.replace(':root', scopeSelector);
            }

            // Replace html/body with scope selector
            if (s === 'html' || s === 'body') {
                return scopeSelector;
            }
            if (s.startsWith('html ')) {
                return scopeSelector + ' ' + s.substring(5);
            }
            if (s.startsWith('body ')) {
                return scopeSelector + ' ' + s.substring(5);
            }

            // Prefix other selectors with scope
            return `${scopeSelector} ${s}`;
        }).join(', ');
    }

    /**
     * Load all theme CSS files with scoping
     * Load order: base → theme → brand → menu widget (later ones override earlier)
     */
    async loadThemeCSS() {
        if (this.themeCssLoaded) return;

        const config = this.config;

        // Load in order: base → theme → brand (later ones override earlier)
        if (config.baseCssUrl) {
            await this.loadAndScopeCSS(config.baseCssUrl, 'scoped-base-css');
        }

        if (config.themeCssUrl) {
            await this.loadAndScopeCSS(config.themeCssUrl, 'scoped-theme-css');
        }

        if (config.brandCssUrl) {
            await this.loadAndScopeCSS(config.brandCssUrl, 'scoped-brand-css');
        }

        // Load menu widget CSS LAST - this ensures preview uses exact same styles as frontend
        if (config.menuWidgetCssUrl) {
            await this.loadAndScopeCSS(config.menuWidgetCssUrl, 'scoped-menu-widget-css');
        }

        this.themeCssLoaded = true;
    }

    /**
     * Set device preview - legacy method for canvas toolbar
     */
    setDevicePreview(device) {
        this.currentDevice = device;
        if (device !== 'desktop') {
            this.currentOrientation = 'portrait';
        }

        // Update both preview panel and canvas
        if (this.previewPanel && !this.previewPanel.classList.contains('hidden')) {
            this.applyDevice();
        } else {
            this.setDevicePreviewLegacy(device);
        }
    }

    /**
     * Update device visibility indicators on menu items
     */
    updateDeviceVisibilityIndicators(device) {
        const itemRows = document.querySelectorAll('.menu-tree-item-row');

        itemRows.forEach(row => {
            const itemId = row.closest('.menu-tree-item')?.dataset.itemId;
            if (!itemId) return;

            const item = this.findItemById(this.itemsTree, itemId);
            if (!item) return;

            const visibilityRules = item.visibility_rules || [];
            const deviceRule = visibilityRules.find(r => r.type === 'device');

            // If no device rule, item is visible on all devices
            if (!deviceRule) {
                row.classList.remove('hidden-on-device');
                row.removeAttribute('title');
                return;
            }

            const visibleDevices = deviceRule.value || ['desktop', 'tablet', 'mobile'];
            const isHiddenOnDevice = !visibleDevices.includes(device);

            row.classList.toggle('hidden-on-device', isHiddenOnDevice);
            if (isHiddenOnDevice) {
                row.setAttribute('title', `Hidden on ${device}`);
            } else {
                row.removeAttribute('title');
            }
        });
    }

    // =========================================
    // UI Helpers
    // =========================================

    switchTab(tabId) {
        document.querySelectorAll('.admin-tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tabId);
        });

        document.querySelectorAll('.admin-tab-content').forEach(content => {
            content.classList.toggle('active', content.id === `${tabId}-tab`);
        });
    }

    toggleLibrarySection(header) {
        header.classList.toggle('collapsed');
    }

    filterLibrary(query) {
        const lower = query.toLowerCase();
        document.querySelectorAll('.library-item').forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(lower) ? '' : 'none';
        });
    }

    showToast(message, type = 'info') {
        AdminModal.toast(message, type || 'info');
    }

    markUnsaved() {
        this.hasUnsavedChanges = true;
    }

    // =========================================
    // History (Undo/Redo)
    // =========================================

    saveHistoryState() {
        // Remove any future states if we're in the middle of the history
        if (this.historyIndex < this.history.length - 1) {
            this.history = this.history.slice(0, this.historyIndex + 1);
        }

        // Add new state
        this.history.push(JSON.stringify(this.itemsTree));

        // Limit history size
        if (this.history.length > this.maxHistorySize) {
            this.history.shift();
        }

        this.historyIndex = this.history.length - 1;
        this.updateHistoryButtons();
    }

    undo() {
        if (this.historyIndex > 0) {
            this.historyIndex--;
            this.itemsTree = JSON.parse(this.history[this.historyIndex]);
            this.renderItemsTree();
            this.selectedItem = null;
            this.renderPropertiesPanel(null);
            this.updateHistoryButtons();
            this.markUnsaved();
        }
    }

    redo() {
        if (this.historyIndex < this.history.length - 1) {
            this.historyIndex++;
            this.itemsTree = JSON.parse(this.history[this.historyIndex]);
            this.renderItemsTree();
            this.selectedItem = null;
            this.renderPropertiesPanel(null);
            this.updateHistoryButtons();
            this.markUnsaved();
        }
    }

    updateHistoryButtons() {
        const undoBtn = document.getElementById('undo-btn');
        const redoBtn = document.getElementById('redo-btn');

        if (undoBtn) undoBtn.disabled = this.historyIndex <= 0;
        if (redoBtn) redoBtn.disabled = this.historyIndex >= this.history.length - 1;
    }

    handleKeyboard(e) {
        // Ctrl/Cmd + Z = Undo
        if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
            e.preventDefault();
            this.undo();
        }

        // Ctrl/Cmd + Shift + Z or Ctrl/Cmd + Y = Redo
        if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
            e.preventDefault();
            this.redo();
        }

        // Ctrl/Cmd + S = Save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            this.saveMenu();
        }

        // Delete/Backspace = Delete selected item
        if ((e.key === 'Delete' || e.key === 'Backspace') && this.selectedItem && !e.target.matches('input, textarea, select')) {
            e.preventDefault();
            this.deleteItem(this.selectedItem);
        }

        // Escape = Deselect or close preview
        if (e.key === 'Escape') {
            // First check if preview is open - close it
            if (this.previewPanel && !this.previewPanel.classList.contains('hidden')) {
                this.hidePreview();
                return;
            }

            this.selectedItem = null;
            document.querySelectorAll('.menu-tree-item-row.selected').forEach(row => row.classList.remove('selected'));
            this.renderPropertiesPanel(null);

            // Close modals
            document.querySelectorAll('.modal-overlay:not(.hidden)').forEach(modal => {
                modal.classList.add('hidden');
            });
        }

        // Device preview shortcuts (only when not in input fields)
        // These control EITHER the preview panel OR the canvas, depending on which is active
        if (!e.ctrlKey && !e.altKey && !e.metaKey && !e.target.matches('input, textarea, select')) {
            const previewVisible = this.previewPanel && !this.previewPanel.classList.contains('hidden');

            // 1 = Desktop preview
            if (e.key === '1') {
                if (previewVisible) {
                    // Update preview panel device (independent state)
                    this.previewDevice = 'desktop';
                    this.applyDevice();
                } else {
                    // Update canvas device
                    this.currentDevice = 'desktop';
                    this.setDevicePreviewLegacy('desktop');
                }
            }

            // 2 = Tablet preview
            if (e.key === '2') {
                if (previewVisible) {
                    // Update preview panel device (independent state)
                    this.previewDevice = 'tablet';
                    this.previewOrientation = 'portrait';
                    this.applyDevice();
                } else {
                    // Update canvas device
                    this.currentDevice = 'tablet';
                    this.setDevicePreviewLegacy('tablet');
                }
            }

            // 3 = Mobile preview
            if (e.key === '3') {
                if (previewVisible) {
                    // Update preview panel device (independent state)
                    this.previewDevice = 'mobile';
                    this.previewOrientation = 'portrait';
                    this.applyDevice();
                } else {
                    // Update canvas device
                    this.currentDevice = 'mobile';
                    this.setDevicePreviewLegacy('mobile');
                }
            }

            // R = Rotate (toggle orientation for tablet/mobile)
            if (e.key === 'r' || e.key === 'R') {
                if (previewVisible) {
                    // Rotate preview panel device
                    if (this.previewDevice !== 'desktop') {
                        this.previewOrientation = this.previewOrientation === 'portrait' ? 'landscape' : 'portrait';
                        this.applyDevice();
                    }
                }
                // Note: canvas area doesn't have orientation, so R does nothing when preview is hidden
            }

            // P = Toggle preview panel
            if (e.key === 'p' || e.key === 'P') {
                this.togglePreview();
            }
        }
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.menuBuilder = new MenuBuilder();

    // Back button — navigate to URL stored in data-url attribute
    const backBtn = document.getElementById('back-btn');
    if (backBtn && backBtn.dataset.url) {
        backBtn.addEventListener('click', () => {
            window.location.href = backBtn.dataset.url;
        });
    }

    // Hamburger toggle for mobile menu preview panel (data-action="toggle-hamburger")
    document.addEventListener('click', (e) => {
        const hamburger = e.target.closest('[data-action="toggle-hamburger"]');
        if (hamburger) {
            hamburger.closest('.menu-preview')?.classList.toggle('menu-open');
        }
        // Preview-mode links — prevent navigation
        if (e.target.closest('[data-preview-link]')) {
            e.preventDefault();
        }
    });
});
