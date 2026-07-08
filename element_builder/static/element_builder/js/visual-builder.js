/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Element Builder Visual Builder
 * Uses page_builder Elements via API for element tree management
 */

(function() {
    'use strict';

    // Configuration from server (read from data island for CSP compliance)
    var _ebConfigEl = document.getElementById('element-builder-config');
    const config = _ebConfigEl ? JSON.parse(_ebConfigEl.textContent) : (window.ElementBuilderConfig || {});

    // API base URL
    const apiBase = config.apiBaseUrl || '/api/element-builder';

    // State management
    const state = {
        customElementId: config.customElementId,
        elementTree: config.elementTree || null,  // Root Element with children
        selectedElementId: null,
        undoStack: [],
        redoStack: [],
        isDirty: false,
        targetModel: config.targetModel || '',
        bindings: config.bindings || [],
        previewItem: null,
        canvasView: 'preview',  // 'preview' or 'structure'
        sortables: []  // Sortable.js instances for container drag-drop
    };

    // Initialize the builder
    function init() {
        loadPrimitives();
        setupDragAndDrop();
        setupPropertyPanel();
        setupActions();
        setupModelSelector();
        setupPreviewItemSearch();
        setupCanvasViewToggle();
        renderCanvas();
    }

    // Setup canvas view toggle (preview/structure)
    function setupCanvasViewToggle() {
        const toggle = document.getElementById('canvas-view-toggle');
        if (!toggle) return;

        toggle.querySelectorAll('.view-toggle-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const view = btn.dataset.view;
                if (view === state.canvasView) return;

                // Update state
                state.canvasView = view;

                // Update active button
                toggle.querySelectorAll('.view-toggle-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                // Show/hide canvas sections
                const preview = document.getElementById('canvas-preview');
                const tree = document.getElementById('canvas-tree');

                if (view === 'preview') {
                    preview.style.display = 'block';
                    tree.style.display = 'none';
                    renderPreview();
                } else {
                    preview.style.display = 'none';
                    tree.style.display = 'block';
                    renderStructureTree();
                }
            });
        });
    }

    // Load available primitives from API
    async function loadPrimitives() {
        try {
            const response = await fetch(`${apiBase}/primitives/`);
            const primitives = await response.json();
            renderElementLibrary(primitives);
        } catch (err) {
            console.error('Error loading primitives:', err);
        }
    }

    // Render element library with primitives from API, grouped by category
    function renderElementLibrary(primitives) {
        const library = document.getElementById('element-library-items');
        if (!library) return;

        // Group elements by category
        const categories = {};
        const categoryLabels = {
            'layout': 'Layout',
            'basic': 'Basic Elements',
            'content': 'Content',
            'media': 'Media',
            'forms': 'Forms',
            'marketing': 'Marketing',
            'ecommerce': 'E-Commerce',
            'social': 'Social',
            'navigation': 'Navigation',
        };

        primitives.forEach(p => {
            const cat = p.category || 'content';
            if (!categories[cat]) {
                categories[cat] = [];
            }
            categories[cat].push(p);
        });

        // Render categories and items
        let html = '';
        for (const [catKey, items] of Object.entries(categories)) {
            const catLabel = categoryLabels[catKey] || catKey.charAt(0).toUpperCase() + catKey.slice(1);
            html += `
                <div class="element-category">
                    <h4 class="element-category-title">
                        <i class="fas fa-chevron-down"></i>
                        ${catLabel}
                    </h4>
                    <div class="element-category-items">
                        ${items.map(p => `
                            <div class="element-library-item"
                                 draggable="true"
                                 data-type="${p.type}"
                                 data-label="${p.name}"
                                 data-icon="${p.icon}"
                                 title="${p.description || ''}">
                                <i class="${p.icon}"></i>
                                <span>${p.name}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        library.innerHTML = html;

        // Setup category toggle
        library.querySelectorAll('.element-category-title').forEach(title => {
            title.addEventListener('click', () => {
                title.closest('.element-category').classList.toggle('collapsed');
            });
        });

        // Setup drag events for library items
        library.querySelectorAll('.element-library-item').forEach(item => {
            item.addEventListener('dragstart', (e) => {
                e.dataTransfer.setData('text/plain', JSON.stringify({
                    source: 'library',
                    type: item.dataset.type,
                    label: item.dataset.label,
                    icon: item.dataset.icon
                }));
                e.dataTransfer.effectAllowed = 'copy';
            });
        });
    }

    // Drag and Drop from Element Library
    function setupDragAndDrop() {
        const canvas = document.getElementById('builder-canvas');

        // Canvas drop zone
        canvas.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
            canvas.classList.add('drag-over');
        });

        canvas.addEventListener('dragleave', (e) => {
            if (!canvas.contains(e.relatedTarget)) {
                canvas.classList.remove('drag-over');
            }
        });

        canvas.addEventListener('drop', (e) => {
            e.preventDefault();
            canvas.classList.remove('drag-over');

            const rawData = e.dataTransfer.getData('text/plain');
            if (!rawData) {
                // No data available - ignore the drop
                return;
            }

            try {
                const data = JSON.parse(rawData);
                if (data.source === 'library') {
                    addElement(data.type, data.label);
                }
            } catch (err) {
                console.error('Drop error:', err);
            }
        });

        // Category toggle
        document.querySelectorAll('.element-category-title').forEach(title => {
            title.addEventListener('click', () => {
                title.closest('.element-category').classList.toggle('collapsed');
            });
        });
    }

    // Model selector setup
    function setupModelSelector() {
        const modelSelect = document.getElementById('model-selector');
        const previewContainer = document.getElementById('preview-selector-container');

        if (!modelSelect) return;

        modelSelect.addEventListener('change', async (e) => {
            const newModel = e.target.value;
            const previousModel = state.targetModel;

            // Check if there are existing bindings and model is actually changing
            if (state.bindings && state.bindings.length > 0 && previousModel && newModel !== previousModel) {
                const confirmed = await showModelChangeWarning(state.bindings.length);
                if (!confirmed) {
                    // Revert the select to previous value
                    modelSelect.value = previousModel;
                    return;
                }
                // User confirmed - clear all bindings
                await clearAllBindings();
            }

            state.targetModel = newModel;
            state.previewItem = null;

            // Update available binding fields
            updateModelFields();

            // Show/hide preview selector
            if (previewContainer) {
                previewContainer.style.display = state.targetModel ? 'flex' : 'none';
            }

            // Clear preview item selection
            clearPreviewItem();

            // Save target model to server
            await saveCustomElement({ target_model: state.targetModel });
            state.isDirty = false;
            updateStatus('saved');

            // Refresh canvas to update binding badges
            renderCanvas();
        });
    }

    // Update model fields when model selection changes
    function updateModelFields() {
        const allModels = config.allBindableModels || {};
        const modelData = allModels[state.targetModel] || {};
        config.modelFields = modelData.fields || {};

        // Re-render properties panel if element is selected
        if (state.selectedElementId) {
            updatePropertiesPanel();
        }
    }

    // Preview item search setup
    function setupPreviewItemSearch() {
        const searchInput = document.getElementById('preview-item-search');
        const dropdown = document.getElementById('preview-item-dropdown');

        if (!searchInput || !dropdown) return;

        let debounceTimer;

        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                searchModelItems(e.target.value);
            }, 300);
        });

        searchInput.addEventListener('focus', () => {
            if (!searchInput.value) {
                searchModelItems('');
            }
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.preview-item-search-wrapper')) {
                dropdown.innerHTML = '';
            }
        });
    }

    // Search for model items
    async function searchModelItems(query) {
        if (!state.targetModel || !config.searchItemsUrl) return;

        const dropdown = document.getElementById('preview-item-dropdown');
        if (!dropdown) return;

        try {
            const url = new URL(config.searchItemsUrl, window.location.origin);
            url.searchParams.set('model', state.targetModel);
            url.searchParams.set('q', query);

            const response = await fetch(url);
            const data = await response.json();
            renderPreviewItemDropdown(data.items || []);
        } catch (err) {
            console.error('Error searching items:', err);
            dropdown.innerHTML = '<div class="preview-item-option preview-item-error">Error loading items</div>';
        }
    }

    // Render the preview item dropdown
    function renderPreviewItemDropdown(items) {
        const dropdown = document.getElementById('preview-item-dropdown');
        if (!dropdown) return;

        if (items.length === 0) {
            dropdown.innerHTML = '<div class="preview-item-option preview-item-empty">No items found</div>';
            return;
        }

        dropdown.innerHTML = items.map(item => `
            <div class="preview-item-option" data-id="${item.id}" data-label="${item.label.replace(/"/g, '&quot;')}">
                ${item.label}
            </div>
        `).join('');

        dropdown.querySelectorAll('.preview-item-option[data-id]').forEach(option => {
            option.addEventListener('click', () => {
                selectPreviewItem({
                    id: option.dataset.id,
                    label: option.dataset.label
                });
            });
        });
    }

    // Select a preview item
    function selectPreviewItem(item) {
        state.previewItem = item;

        const selectedEl = document.getElementById('preview-item-selected');
        if (selectedEl) {
            selectedEl.innerHTML = `
                <span class="selected-item-label">${item.label}</span>
                <button type="button" class="clear-preview-btn" title="Clear selection">
                    <i class="fas fa-times"></i>
                </button>
            `;
            selectedEl.querySelector('.clear-preview-btn').addEventListener('click', clearPreviewItem);
        }

        const dropdown = document.getElementById('preview-item-dropdown');
        const searchInput = document.getElementById('preview-item-search');
        if (dropdown) dropdown.innerHTML = '';
        if (searchInput) searchInput.value = '';

        // Refresh preview to show data from the selected item
        renderCanvas();
    }

    // Clear preview item selection
    function clearPreviewItem() {
        state.previewItem = null;
        const selectedEl = document.getElementById('preview-item-selected');
        if (selectedEl) {
            selectedEl.innerHTML = '';
        }

        // Refresh preview to show default/placeholder content
        renderCanvas();
    }

    // Add a new element via API
    async function addElement(type, label, parentId = null) {
        saveUndoState();
        updateStatus('saving');

        try {
            const response = await fetch(`${apiBase}/custom-elements/${state.customElementId}/elements/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': config.csrfToken
                },
                body: JSON.stringify({
                    element_type: type,
                    content: getDefaultContent(type),
                    parent_id: parentId,
                    order: getNextOrder(parentId)
                })
            });

            if (!response.ok) {
                throw new Error('Failed to add element');
            }

            const newElement = await response.json();

            // Reload the element tree
            await reloadElementTree();

            state.isDirty = false;
            updateStatus('saved');
            selectElement(newElement.id);
        } catch (err) {
            console.error('Error adding element:', err);
            updateStatus('error');
        }
    }

    // Get next order value for a parent
    function getNextOrder(parentId) {
        if (!state.elementTree) return 0;

        let parent;
        if (parentId) {
            parent = findElement(state.elementTree, parentId);
        } else {
            parent = state.elementTree;
        }

        if (!parent || !parent.children) return 0;
        return parent.children.length;
    }

    // Get default content for element type
    function getDefaultContent(type) {
        const defaults = {
            container: {
                layout: 'flex',
                direction: 'column',
                gap: '16px',
                width: '100%'
            },
            text: { text: 'Text content' },
            heading: { text: 'Heading', level: 'h2' },
            image: { src: '', alt: 'Image' },
            icon: { icon: 'fas fa-star', size: '24px' },
            button: { text: 'Button', style: 'primary' },
            divider: {},
            spacer: { height: '24px' }
        };
        return defaults[type] || {};
    }

    // Find an element by ID in the tree
    function findElement(element, id) {
        if (!element) return null;
        if (element.id === id) return element;
        if (element.children) {
            for (const child of element.children) {
                const found = findElement(child, id);
                if (found) return found;
            }
        }
        return null;
    }

    // Reload element tree from API
    async function reloadElementTree() {
        try {
            const response = await fetch(`${apiBase}/custom-elements/${state.customElementId}/`);
            const data = await response.json();
            state.elementTree = data.element_tree;
            state.bindings = data.bindings || [];
            renderCanvas();
        } catch (err) {
            console.error('Error reloading element tree:', err);
        }
    }

    // Render the canvas based on current view mode
    function renderCanvas() {
        const canvas = document.getElementById('builder-canvas');
        const emptyState = document.getElementById('canvas-empty');

        if (!state.elementTree) {
            canvas.classList.add('empty');
            document.getElementById('canvas-tree').innerHTML = '';
            document.getElementById('canvas-preview-content').innerHTML = '';
            return;
        }

        canvas.classList.remove('empty');

        if (state.canvasView === 'preview') {
            renderPreview();
        } else {
            renderStructureTree();
        }
    }

    // Render visual preview via API
    async function renderPreview() {
        const previewContent = document.getElementById('canvas-preview-content');
        const previewLoading = document.getElementById('canvas-preview-loading');

        if (!state.elementTree) {
            previewContent.innerHTML = '';
            return;
        }

        // Show loading state
        previewLoading.style.display = 'flex';

        try {
            // Build preview URL with cache busting and optional preview item
            const cacheBust = Date.now();
            let url = `${apiBase}/custom-elements/${state.customElementId}/preview/?_=${cacheBust}`;
            if (state.previewItem) {
                url += `&preview_item_id=${state.previewItem.id}`;
            }

            const response = await fetch(url);
            const data = await response.json();

            previewContent.innerHTML = data.html;

            // Setup click handlers for element selection in preview
            setupPreviewClickHandlers();

            // Initialize Sortable.js for container drag-drop reordering
            initializePreviewSortables();
        } catch (err) {
            console.error('Error rendering preview:', err);
            previewContent.innerHTML = '<div class="preview-error">Error loading preview</div>';
        } finally {
            previewLoading.style.display = 'none';
        }
    }

    // Setup click handlers for selecting elements in preview
    function setupPreviewClickHandlers() {
        const previewContent = document.getElementById('canvas-preview-content');
        if (!previewContent) return;

        previewContent.querySelectorAll('.eb-preview-element').forEach(el => {
            el.addEventListener('click', (e) => {
                e.stopPropagation();
                const elementId = parseInt(el.dataset.elementId);
                if (elementId) {
                    selectElement(elementId);

                    // Update selection visual in preview
                    previewContent.querySelectorAll('.eb-preview-element').forEach(p => {
                        p.classList.remove('selected');
                    });
                    el.classList.add('selected');
                }
            });
        });
    }

    // ==========================================================================
    // Container Layout Functions
    // ==========================================================================

    /**
     * Apply a layout preset to a container element.
     * Creates child column containers based on the layout type.
     */
    async function applyContainerLayout(containerId, layoutType) {
        try {
            const response = await fetch(
                `${apiBase}/custom-elements/${state.customElementId}/elements/${containerId}/layout/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': config.csrfToken
                    },
                    body: JSON.stringify({ layout_type: layoutType })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                console.error('Error applying layout:', error);
                return;
            }

            // Reload the element tree and re-render
            await reloadElementTree();
            renderCanvas();

        } catch (err) {
            console.error('Error applying container layout:', err);
        }
    }

    /**
     * Skip the layout picker and mark container as initialized without children.
     * Results in an empty container with a drop zone.
     */
    async function skipContainerLayout(containerId) {
        try {
            // Get current element content
            const element = findElementById(containerId);
            const currentContent = element ? element.content || {} : {};

            const response = await fetch(
                `${apiBase}/custom-elements/${state.customElementId}/elements/${containerId}/`,
                {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': config.csrfToken
                    },
                    body: JSON.stringify({
                        content: {
                            ...currentContent,
                            layout_initialized: true
                        }
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                console.error('Error skipping layout:', error);
                return;
            }

            // Reload the element tree and re-render
            await reloadElementTree();
            renderCanvas();

        } catch (err) {
            console.error('Error skipping container layout:', err);
        }
    }

    /**
     * Find an element by ID in the element tree (recursive).
     */
    function findElementById(elementId, tree = null) {
        if (!tree) tree = state.elementTree;
        if (!tree) return null;

        if (tree.id === parseInt(elementId)) {
            return tree;
        }

        if (tree.children && Array.isArray(tree.children)) {
            for (const child of tree.children) {
                const found = findElementById(elementId, child);
                if (found) return found;
            }
        }

        return null;
    }

    /**
     * Reload the element tree from the server.
     */
    async function reloadElementTree() {
        try {
            const response = await fetch(
                `${apiBase}/custom-elements/${state.customElementId}/`
            );
            const data = await response.json();

            if (data.element_tree) {
                state.elementTree = data.element_tree;
            }
            if (data.bindings) {
                state.bindings = data.bindings;
            }

        } catch (err) {
            console.error('Error reloading element tree:', err);
        }
    }

    // ==========================================================================
    // Sortable.js Integration
    // ==========================================================================

    /**
     * Initialize Sortable.js for container elements.
     * Enables drag-and-drop reordering of elements within and between containers.
     */
    function initializePreviewSortables() {
        // Check if Sortable.js is loaded
        if (typeof Sortable === 'undefined') {
            console.warn('Sortable.js not loaded - drag-drop reordering disabled');
            return;
        }

        // Destroy existing sortables
        if (state.sortables && state.sortables.length > 0) {
            state.sortables.forEach(s => {
                if (s && typeof s.destroy === 'function') {
                    s.destroy();
                }
            });
        }
        state.sortables = [];

        // Setup sortable for each container
        document.querySelectorAll('.eb-container').forEach(container => {
            const sortable = new Sortable(container, {
                group: 'eb-elements',
                animation: 150,
                draggable: '.eb-child-wrapper',
                ghostClass: 'eb-sortable-ghost',
                chosenClass: 'eb-sortable-chosen',
                filter: '.eb-drop-zone, .eb-layout-picker',
                preventOnFilter: false,
                onEnd: async (evt) => {
                    await handleElementReorder(evt);
                }
            });
            state.sortables.push(sortable);
        });

        // Setup drop zone click handlers for adding elements
        setupDropZoneHandlers();
    }

    /**
     * Handle element reorder after drag-drop.
     */
    async function handleElementReorder(evt) {
        const childWrapper = evt.item;
        const previewElement = childWrapper.querySelector('.eb-preview-element');

        if (!previewElement) {
            console.warn('No preview element found in dragged item');
            return;
        }

        const elementId = previewElement.dataset.elementId;
        const newParentId = evt.to.dataset.containerId;
        const newOrder = evt.newIndex;

        if (!elementId) {
            console.warn('No element ID found');
            return;
        }

        try {
            const response = await fetch(
                `${apiBase}/custom-elements/${state.customElementId}/elements/${elementId}/move/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': config.csrfToken
                    },
                    body: JSON.stringify({
                        parent_id: newParentId ? parseInt(newParentId) : null,
                        order: newOrder
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                console.error('Error moving element:', error);
                // Revert by reloading
                await reloadElementTree();
                renderCanvas();
                return;
            }

            // Reload to sync state
            await reloadElementTree();
            renderCanvas();

        } catch (err) {
            console.error('Error reordering element:', err);
            // Revert by reloading
            await reloadElementTree();
            renderCanvas();
        }
    }

    /**
     * Setup click handlers for drop zones.
     * When clicked, show element picker or allow dropping elements.
     */
    function setupDropZoneHandlers() {
        document.querySelectorAll('.eb-drop-zone').forEach(zone => {
            // Highlight on drag over
            zone.addEventListener('dragover', (e) => {
                e.preventDefault();
                zone.classList.add('drag-over');
            });

            zone.addEventListener('dragleave', () => {
                zone.classList.remove('drag-over');
            });

            zone.addEventListener('drop', async (e) => {
                e.preventDefault();
                zone.classList.remove('drag-over');

                // Get element type from drag data
                const elementType = e.dataTransfer.getData('text/plain');
                if (!elementType) return;

                const containerId = zone.dataset.containerId;
                if (!containerId) return;

                // Add element to container
                await addElementToContainer(elementType, containerId);
            });
        });
    }

    /**
     * Add an element to a container via API.
     */
    async function addElementToContainer(elementType, containerId) {
        try {
            const response = await fetch(
                `${apiBase}/custom-elements/${state.customElementId}/elements/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': config.csrfToken
                    },
                    body: JSON.stringify({
                        element_type: elementType,
                        parent_id: parseInt(containerId),
                        content: {},
                        order: 0
                    })
                }
            );

            if (!response.ok) {
                const error = await response.json();
                console.error('Error adding element:', error);
                return;
            }

            // Reload and re-render
            await reloadElementTree();
            renderCanvas();

        } catch (err) {
            console.error('Error adding element to container:', err);
        }
    }

    // Event delegation for layout picker (replaces inline onclick handlers)
    document.addEventListener('click', function(e) {
        const layoutOption = e.target.closest('.layout-option[data-layout]');
        if (layoutOption) {
            const picker = layoutOption.closest('.eb-layout-picker');
            if (picker && picker.dataset.containerId) {
                applyContainerLayout(picker.dataset.containerId, layoutOption.dataset.layout);
            }
            return;
        }
        const skipBtn = e.target.closest('[data-action="skip-layout"]');
        if (skipBtn) {
            const picker = skipBtn.closest('.eb-layout-picker');
            if (picker && picker.dataset.containerId) {
                skipContainerLayout(picker.dataset.containerId);
            }
        }
    });

    // Render the structure tree view
    function renderStructureTree() {
        const canvasTree = document.getElementById('canvas-tree');

        if (!state.elementTree) {
            canvasTree.innerHTML = '';
            return;
        }

        canvasTree.innerHTML = '';
        canvasTree.appendChild(renderElementNode(state.elementTree));
    }

    // Render a single element node
    function renderElementNode(element) {
        const template = document.getElementById('template-canvas-node');
        const el = template.content.cloneNode(true).firstElementChild;

        el.dataset.elementId = element.id;

        // Get icon for element type
        const typeIcons = {
            container: 'fas fa-square',
            text: 'fas fa-font',
            heading: 'fas fa-heading',
            image: 'fas fa-image',
            icon: 'fas fa-star',
            button: 'fas fa-mouse-pointer',
            divider: 'fas fa-minus',
            spacer: 'fas fa-arrows-alt-v'
        };

        el.querySelector('.node-icon').className = 'node-icon ' + (typeIcons[element.element_type] || 'fas fa-cube');
        el.querySelector('.node-label').textContent = element.element_type;

        // Show binding badge if element has binding
        const binding = state.bindings.find(b => b.element === element.id);
        if (binding) {
            const badge = el.querySelector('.node-binding-badge');
            badge.style.display = 'inline-flex';
            badge.querySelector('.binding-field').textContent = binding.model_field;
        }

        if (state.selectedElementId === element.id) {
            el.classList.add('selected');
        }

        // Click to select
        el.addEventListener('click', (e) => {
            e.stopPropagation();
            selectElement(element.id);
        });

        // Drag within canvas for reordering
        el.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', JSON.stringify({
                source: 'canvas',
                elementId: element.id
            }));
            e.dataTransfer.effectAllowed = 'move';
        });

        // Drop target for containers
        if (element.element_type === 'container') {
            el.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.stopPropagation();
                el.classList.add('drag-over');
            });

            el.addEventListener('dragleave', (e) => {
                el.classList.remove('drag-over');
            });

            el.addEventListener('drop', (e) => {
                e.preventDefault();
                e.stopPropagation();
                el.classList.remove('drag-over');

                try {
                    const data = JSON.parse(e.dataTransfer.getData('text/plain'));
                    if (data.source === 'library') {
                        addElement(data.type, data.label, element.id);
                    } else if (data.source === 'canvas' && data.elementId !== element.id) {
                        moveElement(data.elementId, element.id);
                    }
                } catch (err) {
                    console.error('Drop error:', err);
                }
            });
        }

        // Render children
        if (element.children && element.children.length > 0) {
            const childrenContainer = el.querySelector('.canvas-node-children');
            element.children.forEach(child => {
                childrenContainer.appendChild(renderElementNode(child));
            });
        }

        return el;
    }

    // Move element to a new parent container
    async function moveElement(elementId, newParentId) {
        saveUndoState();
        updateStatus('saving');
        try {
            const response = await fetch(
                `${apiBase}/custom-elements/${state.customElementId}/elements/${elementId}/move/`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': config.csrfToken
                    },
                    body: JSON.stringify({
                        parent_id: newParentId ? parseInt(newParentId) : null,
                        order: 0
                    })
                }
            );
            if (!response.ok) {
                console.error('Error moving element:', await response.json());
            }
            await reloadElementTree();
            renderCanvas();
            updateStatus('saved');
        } catch (err) {
            console.error('Error moving element:', err);
            await reloadElementTree();
            renderCanvas();
            updateStatus('error');
        }
    }

    // Select an element
    function selectElement(elementId) {
        state.selectedElementId = elementId;
        renderCanvas();
        updatePropertiesPanel();
    }

    // Active utilities for cleanup
    let activeUtilities = [];

    // Cache for element configs to avoid repeated API calls
    const elementConfigCache = {};

    // Update the properties panel using PropertyRenderer
    async function updatePropertiesPanel() {
        const panel = document.getElementById('properties-panel');

        // Cleanup previous utilities (PropertyRenderer handles its own cleanup)
        activeUtilities.forEach(util => {
            if (util && typeof util.close === 'function') {
                util.close();
            }
        });
        activeUtilities = [];

        if (!state.selectedElementId) {
            panel.innerHTML = `
                <div class="properties-empty-state">
                    <i class="fas fa-mouse-pointer"></i>
                    <p>Select an element to edit its properties</p>
                </div>
            `;
            return;
        }

        const element = findElement(state.elementTree, state.selectedElementId);
        if (!element) return;

        // Fetch element config from API (with caching)
        let elementConfig = elementConfigCache[element.element_type];
        if (!elementConfig) {
            try {
                const configUrl = config.elementConfigUrl || `${apiBase}/element-config/`;
                const response = await fetch(`${configUrl}${element.element_type}/`);
                if (response.ok) {
                    elementConfig = await response.json();
                    elementConfigCache[element.element_type] = elementConfig;
                } else {
                    console.error('Failed to fetch element config:', element.element_type);
                    elementConfig = null;
                }
            } catch (err) {
                console.error('Error fetching element config:', err);
                elementConfig = null;
            }
        }

        // Clear panel and build new content
        panel.innerHTML = '';

        // Add element type header
        const header = document.createElement('div');
        header.className = 'properties-element-header';
        header.innerHTML = `
            <i class="${elementConfig?.icon || 'fas fa-cube'}"></i>
            <span>${elementConfig?.name || element.element_type}</span>
        `;
        panel.appendChild(header);

        // Render binding section (element_builder-specific)
        panel.appendChild(renderBindingSection(element));

        // Use PropertyRenderer if available and config was fetched
        if (window.propertyRenderer && elementConfig) {
            const propsContainer = document.createElement('div');
            propsContainer.id = 'element-props-container';
            propsContainer.className = 'property-renderer-container';
            panel.appendChild(propsContainer);

            // Create element data object for PropertyRenderer
            const elementData = {
                id: element.id,
                element_type: element.element_type,
                content: element.content || {}
            };

            // Use global propertyRenderer instance (created by page_builder)
            window.propertyRenderer.renderProperties('element-props-container', elementConfig, elementData);

            // Setup change listener for property updates
            setupPropertyChangeListener(element.id);
        } else {
            // Fallback: render basic properties without PropertyRenderer
            panel.appendChild(renderBasicPropertiesPanel(element));
        }

        // Add delete button at the bottom
        panel.appendChild(renderDeleteButton());
    }

    // Render the data binding section (element_builder-specific feature)
    function renderBindingSection(element) {
        const section = document.createElement('div');
        section.className = 'properties-section properties-section-binding';
        section.dataset.section = 'binding';

        const modelFields = config.modelFields || {};
        const binding = state.bindings.find(b => b.element === element.id);
        const isImageElement = element.element_type === 'image';
        const isButtonElement = element.element_type === 'button';

        // Determine which field types to show based on element type
        let allowedTypes = ['text'];
        if (isImageElement) {
            allowedTypes = ['image'];
        } else if (isButtonElement) {
            // Buttons can bind text (for label) or url (for href)
            allowedTypes = ['text', 'url'];
        }

        // Group fields by their group property
        const fieldsByGroup = {};
        Object.entries(modelFields).forEach(([fieldName, fieldConfig]) => {
            const fieldType = fieldConfig.type;
            if (!allowedTypes.includes(fieldType)) return;

            const group = fieldConfig.group || 'other';
            if (!fieldsByGroup[group]) {
                fieldsByGroup[group] = [];
            }
            fieldsByGroup[group].push({ name: fieldName, ...fieldConfig });
        });

        // Define group labels and order
        const groupLabels = {
            basic: 'Basic Info',
            images: 'Images',
            pricing: 'Pricing',
            stock: 'Stock & Availability',
            related: 'Related',
            identifiers: 'Identifiers',
            seo: 'SEO',
            stats: 'Statistics',
            urls: 'Links',
            display: 'Display',
            hierarchy: 'Hierarchy',
            author: 'Author',
            taxonomy: 'Category & Tags',
            dates: 'Dates',
            contact: 'Contact',
            other: 'Other'
        };
        const groupOrder = ['basic', 'images', 'pricing', 'stock', 'related', 'author', 'taxonomy', 'dates', 'stats', 'seo', 'urls', 'display', 'hierarchy', 'identifiers', 'contact', 'other'];

        // Build field options with optgroups
        let fieldOptions = '<option value="">None (Static)</option>';
        groupOrder.forEach(group => {
            const fields = fieldsByGroup[group];
            if (!fields || fields.length === 0) return;

            fieldOptions += `<optgroup label="${groupLabels[group] || group}">`;
            fields.forEach(field => {
                const selected = binding && binding.model_field === field.name ? 'selected' : '';
                const title = field.description ? ` title="${field.description}"` : '';
                fieldOptions += `<option value="${field.name}" ${selected}${title}>${field.label || field.name}</option>`;
            });
            fieldOptions += '</optgroup>';
        });

        // Only show if target model is selected and has compatible fields
        const totalFields = Object.values(fieldsByGroup).reduce((sum, arr) => sum + arr.length, 0);
        const hasModel = state.targetModel && totalFields > 0;

        section.innerHTML = `
            <h4 class="properties-section-title">
                <i class="fas fa-link"></i> Field Binding
                ${!hasModel ? '<span class="binding-hint">(Select a model first)</span>' : ''}
            </h4>
            <div class="properties-section-content" ${!hasModel ? 'style="display:none;"' : ''}>
                <div class="property-field">
                    <label for="prop-binding-field">Bind to Field</label>
                    <select id="prop-binding-field" class="property-input">
                        ${fieldOptions}
                    </select>
                </div>
                ${isImageElement ? `
                <div class="property-field binding-thumbnail-field" ${!binding ? 'style="display:none;"' : ''}>
                    <label for="prop-binding-thumbnail">Thumbnail Size</label>
                    <select id="prop-binding-thumbnail" class="property-input">
                        ${renderThumbnailOptions(binding?.thumbnail_preset)}
                    </select>
                </div>
                ` : ''}
            </div>
        `;

        return section;
    }

    // Render thumbnail preset options
    function renderThumbnailOptions(selectedPreset) {
        // Use presets from config if available
        const presets = window.ElementBuilderConfig.thumbnailPresets || [
            { slug: 'small', name: 'Small', width: 150, height: 150 },
            { slug: 'medium', name: 'Medium', width: 300, height: 300 },
            { slug: 'large', name: 'Large', width: 600, height: 600 }
        ];

        return presets.map(p =>
            `<option value="${p.slug}" ${p.slug === selectedPreset ? 'selected' : ''}>${p.name} (${p.width}x${p.height})</option>`
        ).join('');
    }

    // Render delete button
    function renderDeleteButton() {
        const actions = document.createElement('div');
        actions.className = 'properties-actions';
        actions.innerHTML = `
            <button type="button" class="builder-btn danger" id="btn-delete-element">
                <i class="fas fa-trash"></i> Delete Element
            </button>
        `;
        return actions;
    }

    // Fallback: render basic properties without PropertyRenderer
    function renderBasicPropertiesPanel(element) {
        const container = document.createElement('div');
        container.className = 'properties-basic-fallback';

        // Create basic property fields from element content
        const content = element.content || {};

        let html = '<div class="properties-section"><h4 class="properties-section-title"><i class="fas fa-cog"></i> Content</h4><div class="properties-section-content">';

        // Show text/content fields
        if (content.text !== undefined) {
            html += `
                <div class="property-field">
                    <label for="prop-text">Text</label>
                    <textarea id="prop-text" class="property-input" data-prop="text">${content.text || ''}</textarea>
                </div>
            `;
        }

        if (content.src !== undefined) {
            html += `
                <div class="property-field">
                    <label for="prop-src">Source URL</label>
                    <input type="text" id="prop-src" class="property-input" data-prop="src" value="${content.src || ''}">
                </div>
            `;
        }

        html += '</div></div>';
        container.innerHTML = html;

        return container;
    }

    // Handle property changes from PropertyRenderer
    async function handlePropertyChange(elementId, propertyName, value) {
        saveUndoState();
        await updateElementContent(elementId, propertyName, value);
    }

    // Property change listener debounce timer
    let propertyChangeDebounce = null;

    // Setup listener for property changes from PropertyRenderer form
    function setupPropertyChangeListener(elementId) {
        const form = document.querySelector('.element-properties-form');
        if (!form) return;

        // Remove any existing listener to avoid duplicates
        form.removeEventListener('input', handleFormInput);
        form.removeEventListener('change', handleFormChange);

        // Add listeners for both input (real-time) and change (on blur/select)
        form.addEventListener('input', handleFormInput);
        form.addEventListener('change', handleFormChange);

        function handleFormInput(e) {
            // Debounce for text inputs to avoid too many API calls
            if (e.target.type === 'text' || e.target.tagName === 'TEXTAREA') {
                clearTimeout(propertyChangeDebounce);
                propertyChangeDebounce = setTimeout(() => {
                    saveFormChanges(elementId);
                }, 500);
            }
        }

        function handleFormChange(e) {
            // Immediate save for selects, checkboxes, etc.
            if (e.target.type !== 'text' && e.target.tagName !== 'TEXTAREA') {
                saveFormChanges(elementId);
            }
        }
    }

    // Collect and save all form properties
    async function saveFormChanges(elementId) {
        const form = document.querySelector('.element-properties-form');
        if (!form) return;

        const element = findElement(state.elementTree, elementId);
        if (!element) return;

        // Collect all property values from the form
        const content = { ...element.content };
        let hasChanges = false;

        // Get all named inputs/selects/textareas
        form.querySelectorAll('[name]').forEach(input => {
            const name = input.name;
            let value;

            if (input.type === 'checkbox') {
                value = input.checked;
            } else if (input.type === 'number') {
                value = input.value ? parseFloat(input.value) : '';
            } else {
                value = input.value;
            }

            // Only update if value changed
            if (content[name] !== value) {
                content[name] = value;
                hasChanges = true;
            }
        });

        // Also check data-property attributes (used by utility editors)
        form.querySelectorAll('[data-property]').forEach(input => {
            const name = input.dataset.property;
            let value;

            if (input.type === 'checkbox') {
                value = input.checked;
            } else {
                value = input.value;
            }

            if (content[name] !== value) {
                content[name] = value;
                hasChanges = true;
            }
        });

        if (hasChanges) {
            saveUndoState();
            updateStatus('saving');

            try {
                await fetch(`${apiBase}/custom-elements/${state.customElementId}/elements/${elementId}/`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': config.csrfToken
                    },
                    body: JSON.stringify({ content })
                });

                // Update local state
                element.content = content;
                updateStatus('saved');
            } catch (err) {
                console.error('Error saving property changes:', err);
                updateStatus('error');
            }
        }
    }

    // Setup property panel event listeners
    function setupPropertyPanel() {
        const panel = document.getElementById('properties-panel');

        panel.addEventListener('change', async (e) => {
            if (!state.selectedElementId) return;
            const element = findElement(state.elementTree, state.selectedElementId);
            if (!element) return;

            saveUndoState();

            const target = e.target;

            // Handle binding field change
            if (target.id === 'prop-binding-field') {
                await handleBindingChange(element, target.value);
            }

            // Handle thumbnail preset change
            if (target.id === 'prop-binding-thumbnail') {
                await handleBindingChange(element, null, target.value);
            }

            // Handle content property changes
            if (target.dataset.prop) {
                await updateElementContent(element.id, target.dataset.prop, target.value);
            }
        });

        // Delete button
        panel.addEventListener('click', (e) => {
            if (e.target.closest('#btn-delete-element')) {
                deleteSelectedElement();
            }
        });
    }

    // Show warning dialog when changing models with existing bindings
    function showModelChangeWarning(bindingCount) {
        return new Promise((resolve) => {
            // Create modal overlay
            const overlay = document.createElement('div');
            overlay.className = 'eb-modal-overlay';
            overlay.innerHTML = `
                <div class="eb-modal">
                    <div class="eb-modal-header">
                        <i class="fas fa-exclamation-triangle" style="color: var(--warning-color, #f0ad4e);"></i>
                        <h3>Change Target Model?</h3>
                    </div>
                    <div class="eb-modal-body">
                        <p>You have <strong>${bindingCount}</strong> field binding${bindingCount > 1 ? 's' : ''} configured for the current model.</p>
                        <p>Changing the target model will <strong>remove all existing bindings</strong> since the fields are different between models.</p>
                        <p>This action cannot be undone.</p>
                    </div>
                    <div class="eb-modal-actions">
                        <button type="button" class="builder-btn" id="eb-modal-cancel">Cancel</button>
                        <button type="button" class="builder-btn danger" id="eb-modal-confirm">
                            <i class="fas fa-trash"></i> Change Model & Clear Bindings
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(overlay);

            // Focus the cancel button for safety
            setTimeout(() => overlay.querySelector('#eb-modal-cancel').focus(), 50);

            // Handle button clicks
            overlay.querySelector('#eb-modal-cancel').addEventListener('click', () => {
                overlay.remove();
                resolve(false);
            });
            overlay.querySelector('#eb-modal-confirm').addEventListener('click', () => {
                overlay.remove();
                resolve(true);
            });

            // Handle escape key
            overlay.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    overlay.remove();
                    resolve(false);
                }
            });

            // Handle click outside modal
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) {
                    overlay.remove();
                    resolve(false);
                }
            });
        });
    }

    // Clear all bindings for the current custom element
    async function clearAllBindings() {
        if (!state.bindings || state.bindings.length === 0) return;

        updateStatus('saving');

        try {
            // Delete all bindings via API
            await fetch(`${apiBase}/custom-elements/${state.customElementId}/bindings/clear/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': config.csrfToken }
            });

            // Clear local bindings state
            state.bindings = [];

            updateStatus('saved');
        } catch (err) {
            console.error('Error clearing bindings:', err);
            updateStatus('error');
        }
    }

    // Handle binding changes
    async function handleBindingChange(element, modelField = null, thumbnailPreset = null) {
        updateStatus('saving');

        try {
            const binding = state.bindings.find(b => b.element === element.id);

            // Determine content field based on element type
            const contentField = element.element_type === 'image' ? 'src' : 'text';

            if (modelField === '' || modelField === null && !binding) {
                // Delete binding if exists
                if (binding) {
                    await fetch(`${apiBase}/custom-elements/${state.customElementId}/bindings/?element_id=${element.id}&content_field=${contentField}`, {
                        method: 'DELETE',
                        headers: { 'X-CSRFToken': config.csrfToken }
                    });
                }
            } else {
                // Create or update binding
                await fetch(`${apiBase}/custom-elements/${state.customElementId}/bindings/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': config.csrfToken
                    },
                    body: JSON.stringify({
                        element_id: element.id,
                        content_field: contentField,
                        model_field: modelField || (binding ? binding.model_field : ''),
                        thumbnail_preset: thumbnailPreset || (binding ? binding.thumbnail_preset : '')
                    })
                });
            }

            await reloadElementTree();
            updateStatus('saved');
        } catch (err) {
            console.error('Error updating binding:', err);
            updateStatus('error');
        }
    }

    // Update element content via API
    async function updateElementContent(elementId, prop, value) {
        updateStatus('saving');

        try {
            const element = findElement(state.elementTree, elementId);
            const content = { ...element.content, [prop]: value };

            await fetch(`${apiBase}/custom-elements/${state.customElementId}/elements/${elementId}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': config.csrfToken
                },
                body: JSON.stringify({ content })
            });

            await reloadElementTree();
            updateStatus('saved');
        } catch (err) {
            console.error('Error updating element:', err);
            updateStatus('error');
        }
    }

    // Delete the selected element
    async function deleteSelectedElement() {
        if (!state.selectedElementId) return;

        saveUndoState();
        updateStatus('saving');

        try {
            await fetch(`${apiBase}/custom-elements/${state.customElementId}/elements/${state.selectedElementId}/delete/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': config.csrfToken }
            });

            state.selectedElementId = null;
            await reloadElementTree();
            updateStatus('saved');
            updatePropertiesPanel();
        } catch (err) {
            console.error('Error deleting element:', err);
            updateStatus('error');
        }
    }

    // Save custom element metadata
    async function saveCustomElement(data) {
        const response = await fetch(`${apiBase}/custom-elements/${state.customElementId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': config.csrfToken
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error('Failed to save custom element');
        }

        return response.json();
    }

    // Setup action buttons
    function setupActions() {
        document.getElementById('btn-undo')?.addEventListener('click', undo);
        document.getElementById('btn-redo')?.addEventListener('click', redo);
        document.getElementById('btn-preview')?.addEventListener('click', preview);

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'z' && (e.ctrlKey || e.metaKey)) {
                if (e.shiftKey) {
                    redo();
                } else {
                    undo();
                }
                e.preventDefault();
            }
            if (e.key === 'Delete' || e.key === 'Backspace') {
                if (state.selectedElementId && document.activeElement.tagName !== 'INPUT') {
                    deleteSelectedElement();
                    e.preventDefault();
                }
            }
        });
    }

    // Undo/Redo state management
    function saveUndoState() {
        state.undoStack.push({
            elementTree: JSON.parse(JSON.stringify(state.elementTree)),
            bindings: JSON.parse(JSON.stringify(state.bindings))
        });
        state.redoStack = [];
        updateUndoRedoButtons();
    }

    function undo() {
        if (state.undoStack.length === 0) return;
        state.redoStack.push({
            elementTree: JSON.parse(JSON.stringify(state.elementTree)),
            bindings: JSON.parse(JSON.stringify(state.bindings))
        });
        const previous = state.undoStack.pop();
        state.elementTree = previous.elementTree;
        state.bindings = previous.bindings;
        updateUndoRedoButtons();
        renderCanvas();
        updatePropertiesPanel();
        // Note: This is a client-side undo - doesn't sync to server
    }

    function redo() {
        if (state.redoStack.length === 0) return;
        state.undoStack.push({
            elementTree: JSON.parse(JSON.stringify(state.elementTree)),
            bindings: JSON.parse(JSON.stringify(state.bindings))
        });
        const next = state.redoStack.pop();
        state.elementTree = next.elementTree;
        state.bindings = next.bindings;
        updateUndoRedoButtons();
        renderCanvas();
        updatePropertiesPanel();
    }

    function updateUndoRedoButtons() {
        const undoBtn = document.getElementById('btn-undo');
        const redoBtn = document.getElementById('btn-redo');
        if (undoBtn) undoBtn.disabled = state.undoStack.length === 0;
        if (redoBtn) redoBtn.disabled = state.redoStack.length === 0;
    }

    // Preview the element in a modal
    async function preview() {
        const overlay = document.createElement('div');
        overlay.className = 'eb-modal-overlay eb-preview-modal-overlay';
        overlay.innerHTML = `
            <div class="eb-modal eb-preview-modal">
                <div class="eb-modal-header">
                    <i class="fas fa-eye"></i>
                    <h3>Element Preview</h3>
                    <button type="button" class="eb-preview-close" title="Close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="eb-modal-body eb-preview-modal-body">
                    <div class="eb-preview-loading">
                        <i class="fas fa-spinner fa-spin"></i> Loading preview...
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);

        // Close handlers
        const close = () => overlay.remove();
        overlay.querySelector('.eb-preview-close').addEventListener('click', close);
        overlay.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
        overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
        overlay.setAttribute('tabindex', '-1');
        overlay.focus();

        // Fetch preview HTML via existing API
        try {
            let url = `${apiBase}/custom-elements/${state.customElementId}/preview/?_=${Date.now()}`;
            if (state.previewItem) {
                url += `&preview_item_id=${state.previewItem.id}`;
            }
            const response = await fetch(url);
            const data = await response.json();
            overlay.querySelector('.eb-preview-modal-body').innerHTML = data.html;
        } catch (err) {
            console.error('Error loading preview:', err);
            overlay.querySelector('.eb-preview-modal-body').innerHTML =
                '<div class="preview-error">Error loading preview</div>';
        }
    }

    // Update status indicator
    function updateStatus(status) {
        const statusEl = document.getElementById('builder-status');
        if (!statusEl) return;

        statusEl.className = 'builder-status ' + status;

        const icons = {
            saved: 'fas fa-check-circle',
            saving: 'fas fa-spinner fa-spin',
            unsaved: 'fas fa-circle',
            error: 'fas fa-exclamation-circle'
        };

        const labels = {
            saved: 'Saved',
            saving: 'Saving...',
            unsaved: 'Unsaved changes',
            error: 'Save failed'
        };

        statusEl.innerHTML = `<i class="${icons[status]}"></i><span>${labels[status]}</span>`;
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
