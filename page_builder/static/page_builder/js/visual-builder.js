/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Visual Page Builder JavaScript
 * Main builder class that coordinates all page building functionality
 * Uses modular components for history, commands, DOM snapshots, and API calls
 */

// Initialize global instances from modules
const historyManager = new HistoryManager({ maxSize: 50 });

// The API client is already initialized as window.apiClient in api-client.js

class VisualPageBuilder {
    constructor(pageData) {
        this.pageData = pageData;
        this.selectedElement = null;
        this.isDragging = false;
        this.lastDropTime = null; // For preventing duplicate drops
        this.structureViewVisible = false;
        this.expandedNodes = new Set(); // Track expanded nodes in structure view
        this.init();
    }

    init() {
        this.initializeStateManager();
        this.setupDragAndDrop();
        this.setupEventListeners();
        this.setupSortableSections();
        this.initializePreviewSortables();
        this.initializeStructureView();
        console.log('Visual Page Builder initialized');
    }

    initializeStateManager() {
        // Initialize the state manager with API client
        pageStateManager.init(window.apiClient);

        // Subscribe to state changes for preview updates
        this.stateUnsubscribe = pageStateManager.subscribe((change, state) => {
            this.handleStateChange(change, state);
        });

        console.log('StateManager initialized and subscribed');

        // Initialize ContentManager
        if (window.contentManager) {
            contentManager.init();
            console.log('ContentManager initialized');
        }
    }

    handleStateChange(change, state) {
        console.log('State change received:', change);
        
        // DOM already moved by sortable guard
        //if (window.__suppressNextPreviewDOMUpdate) {
        //    window.__suppressNextPreviewDOMUpdate = false;
        //    console.log('Skipping DOM update due to sortable guard');
        //    return;
        //}

        // Skip DOM updates if the change was from a command with skipDOM flag
        if (change.skipDOM) {
            console.log('Skipping DOM update due to skipDOM flag');
            return;
        }

        // Handle different types of state changes
        switch (change.type) {
            case 'ELEMENT_MOVED':
                // Preview DOM update
                // Check if this is from structure view (domAlreadyMoved would be set on the command, not the change)
                this.updatePreviewAfterMove(change);

                // Update structure view more efficiently
                if (this.structureViewVisible) {
                    this.updateStructureAfterMove(change);
                }
                break;
            case 'ELEMENT_ADDED':
                this.updatePreviewAfterAdd(change);
                // Refresh structure to show new element
                if (this.structureViewVisible) {
                    this._refreshStructureIfVisible();
                }
                // Refresh insert zones for the new element
                this.setupElementInsertZones();
                break;
            case 'ELEMENT_REMOVED':
                this.updatePreviewAfterRemove(change);
                // Refresh structure to remove element
                if (this.structureViewVisible) {
                    this._refreshStructureIfVisible();
                }
                // Refresh insert zones after removal
                this.setupElementInsertZones();
                break;
            case 'ELEMENT_UPDATED':
                this.updatePreviewAfterUpdate(change);
                // Update structure node if properties changed
                if (this.structureViewVisible) {
                    this.updateStructureNode(change.elementId, change.changes);
                }
                break;
            case 'ELEMENT_SELECTED':
                this.updatePreviewSelection(change.elementId);
                // Update structure selection
                if (this.structureViewVisible) {
                    this.updateStructureSelection(change.elementId);
                }
                break;
            case 'BATCH_UPDATE':
                // Handle multiple changes at once
                change.changes.forEach(c => this.handleStateChange(c, state));
                break;
            case 'STATE_RESTORED':
                // Skip DOM rebuilds during bulk operations (undoMultiple/redoMultiple)
                if (historyManager && historyManager.isBulkOperation) {
                    console.log('Skipping STATE_RESTORED handling during bulk operation');
                    return;
                }
                // Full state was restored, refresh everything
                console.log('State restored, refreshing views');
                this._refreshStructureIfVisible();
                // Reinitialize preview from restored state
                this.rebuildPreviewFromState(state);
                break;
        }
    }

    async rebuildPreviewFromState(state) {
        console.log('Rebuilding preview from state:', state);

        try {
            const pageElements = document.getElementById('page-elements');
            if (!pageElements || !state) {
                console.error('Missing page elements or state');
                return;
            }

            // Don't fetch from server - work with current DOM
            // Reorder elements based on restored state
            if (state.parentChildMap) {
                // IMPORTANT: Save the page-drop-zone before reordering
                const pageDropZone = pageElements.querySelector('.page-drop-zone');

                // First, handle root level elements
                const rootChildren = state.parentChildMap['root'] || state.structure || [];
                console.log('Restoring root order:', rootChildren);

                // Collect root elements in correct order
                const rootElements = [];
                rootChildren.forEach(childId => {
                    const element = document.querySelector(`[data-element-id="${childId}"]`);
                    if (element) {
                        // Root elements are direct .element-wrapper elements
                        rootElements.push(element);
                        // Temporarily remove from DOM
                        element.remove();
                    }
                });

                // Re-add in correct order to root
                rootElements.forEach(element => {
                    pageElements.appendChild(element);
                });

                // IMPORTANT: Always ensure page-drop-zone is at the end
                if (pageDropZone) {
                    pageDropZone.remove();
                    pageElements.appendChild(pageDropZone);
                }

                // Then handle container children
                for (const [parentId, childIds] of Object.entries(state.parentChildMap)) {
                    if (parentId === 'root') continue;

                    const parentElement = document.querySelector(`[data-element-id="${parentId}"]`);
                    if (!parentElement) {
                        console.warn(`Parent element ${parentId} not found`);
                        continue;
                    }

                    // Find container content area - try multiple selectors (regular container, modal popup, etc.)
                    const containerContent = parentElement.querySelector('.container-content') ||
                                          parentElement.querySelector('.pb-container-content') ||
                                          parentElement.querySelector('.pb-modal-builder__inner');

                    if (!containerContent) {
                        console.warn(`No container content found for ${parentId}`);
                        continue;
                    }

                    console.log(`Restoring children for container ${parentId}:`, childIds);

                    // IMPORTANT: Save the container's drop zone before reordering
                    const containerDropZone = containerContent.querySelector('.container-drop-zone');

                    // Collect elements with their wrappers
                    const wrappedElements = [];
                    childIds.forEach(childId => {
                        const childElement = document.querySelector(`[data-element-id="${childId}"]`);
                        if (childElement) {
                            // Check if element has a container-child-wrapper parent
                            let elementToMove = childElement;
                            const wrapper = childElement.closest('.container-child-wrapper');

                            // Only use wrapper if it's a direct child of our container
                            if (wrapper && wrapper.parentElement === containerContent) {
                                elementToMove = wrapper;
                                console.log(`Using wrapper for element ${childId}`);
                            } else {
                                console.log(`Using element directly for ${childId}`);
                            }

                            wrappedElements.push(elementToMove);
                            // Temporarily remove from DOM
                            if (elementToMove.parentElement) {
                                elementToMove.remove();
                            }
                        } else {
                            console.warn(`Could not find element ${childId}`);
                        }
                    });

                    // Re-add in correct order
                    wrappedElements.forEach((element, index) => {
                        console.log(`Adding element at position ${index}:`,
                            element.querySelector?.('.element-wrapper')?.dataset.elementId ||
                            element.dataset?.elementId);
                        containerContent.appendChild(element);
                    });

                    // IMPORTANT: Always ensure container-drop-zone is at the end
                    if (containerDropZone) {
                        containerDropZone.remove();
                        containerContent.appendChild(containerDropZone);
                    }
                }
            }

            // Refresh structure view to match restored state
            this._refreshStructureIfVisible();

            // Reinitialize sortables
            this.initializePreviewSortables();

            // Reattach event handlers
            this.setupElementClickHandlers();

            console.log('Preview rebuilt successfully from state');

            // Show visual feedback
            this.showNotification('State restored', 'success');
        } catch (error) {
            console.error('Error rebuilding preview from state:', error);
            // Fallback: reinitialize sortables
            this.initializePreviewSortables();
        }
    }

    updatePreviewAfterMove(change) {
        console.log(`🎯 Updating preview after move:`, {
            elementId: change.elementId,
            oldParent: change.oldParentId,
            newParent: change.newParentId,
            newIndex: change.newIndex
        });

        // Find the element in preview - it might be wrapped in container-child-wrapper
        const element = document.querySelector(`[data-element-id="${change.elementId}"]`);
        if (!element) {
            console.error(`Element ${change.elementId} not found in preview`);
            return;
        }

        console.log(`Found element in preview:`, element.className);


        // Check if element is wrapped and get the actual movable element
        //let elementToMove = element;
        //if (element.parentElement?.classList.contains('container-child-wrapper')) {
        //    elementToMove = element.parentElement;
        //    console.log('Element is wrapped in container-child-wrapper, moving wrapper');
        //}

        // Determine target container
        let targetContainer;
        if (!change.newParentId) {
            // Moving to root level
            targetContainer = document.getElementById('page-elements');
        } else {
            // Find parent element
            const parentElement = document.querySelector(`[data-element-id="${change.newParentId}"]`);
            if (parentElement) {
                const elementType = parentElement.dataset.elementType;
                if (elementType === 'container') {
                    targetContainer = parentElement.querySelector('.pb-container-content');
                } else if (elementType === 'modal_popup') {
                    targetContainer = parentElement.querySelector('.pb-modal-builder__inner');
                } else {
                    targetContainer = parentElement.parentElement;
                }
            }
        }
        if (!targetContainer) {
            console.error(`Target container not found for element ${change.elementId}`);
            return;
        }

        // Determine what unit we're working with based on container type
        // In containers: we move .container-child-wrapper elements
        // At root level: we move .element-wrapper elements
        const isInContainer = targetContainer.classList.contains('pb-container-content') ||
                              targetContainer.classList.contains('pb-modal-builder__inner');
        const draggableSelector = isInContainer ? ':scope > .container-child-wrapper' : '.element-wrapper';

        console.log(`Target container type: ${isInContainer ? 'container' : 'root'}, draggable unit: ${draggableSelector}`);

        const currentWrapper = element.closest('.container-child-wrapper');
        let elementToMove = element;

        if (isInContainer) {
            // we need to move the wrapper into a container
            elementToMove = currentWrapper || element; //if not wrapped yet, we'll wrap after insertion
        } else {
            // we need to move the element directly at root level
            elementToMove = currentWrapper ? currentWrapper : element; // if wrapped, move wrapper, else move element
        }

        const currentParent = elementToMove.parentElement;
        const isSameParent = currentParent === targetContainer;

        // figure out the current index of ONLY the draggable sibling of the target container
        const siblings = Array.from(targetContainer.querySelectorAll(draggableSelector));
        const currentIndex = siblings.indexOf(elementToMove);
        const requestedIndex = change.newIndex;

        console.log(`Current index: ${currentIndex}, requested index: ${requestedIndex}, same parent: ${isSameParent}`);

        // Don't skip if the element is at the wrong position
        // The state has been updated, we need to move the DOM to match
        if (isSameParent && currentIndex === requestedIndex) {
            console.log('✅ Element already in correct position');
            return;
        }

        // remove element from current position
        let oldWrapperToClean = null;
        if (!isInContainer && elementToMove.classList.contains('container-child-wrapper')) {
            oldWrapperToClean = elementToMove;
            elementToMove = element; // switch to inner .element-wrapper for moving to root
        }

        elementToMove.remove();
        if (oldWrapperToClean) {
            oldWrapperToClean.remove();
        }

        // recompute siblings after removal
        const updatedSiblings = Array.from(targetContainer.querySelectorAll(draggableSelector));

        // The StateManager has already given us the correct final index
        // No adjustment needed - just use the index as provided
        let targetIndex = requestedIndex;

        // clamp just in case
        if (targetIndex < 0) targetIndex = 0;
        if (targetIndex > updatedSiblings.length) targetIndex = updatedSiblings.length;

        // insert at the adjusted location
        if (targetIndex >= updatedSiblings.length) {
            targetContainer.appendChild(elementToMove);
            console.log('Appended to end of container');
        } else {
            targetContainer.insertBefore(elementToMove, updatedSiblings[targetIndex]);
            console.log(`Inserted before sibling at index ${targetIndex} (requested ${requestedIndex}, current ${currentIndex})`);
        }

        // If moving to a container and element isn't wrapped, wrap it
        if (isInContainer && !elementToMove.classList.contains('container-child-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'container-child-wrapper';
            elementToMove.parentNode.insertBefore(wrapper, elementToMove);
            wrapper.appendChild(elementToMove);
            console.log('Wrapped element in container-child-wrapper');
        }

        // if moving to root and was wrapped, unwrap it
        if (!isInContainer && elementToMove.classList.contains('container-child-wrapper')) {
            const wrapper = elementToMove.parentNode;
            wrapper.parentNode.insertBefore(elementToMove, wrapper);
            wrapper.remove();
            console.log('Unwrapped element from container-child-wrapper');
        }
        console.log('✅ Preview updated successfully');
        
    }

    updatePreviewAfterAdd(change) {
        // Add element to preview if not already there
        const element = pageStateManager.getElement(change.elementId);
        if (element && !document.querySelector(`[data-element-id="${change.elementId}"]`)) {
            this.addElementToPreview(element, change.parentId, null);
        }
    }

    updatePreviewAfterRemove(change) {
        // Remove element from preview if it exists
        this.removeElementFromPreview(change.elementId);
    }

    updatePreviewAfterUpdate(change) {
        // Update element content in preview
        const element = pageStateManager.getElement(change.elementId);
        if (element) {
            this.updateElementInPreview(change.elementId, element.content);
        }
    }

    updatePreviewSelection(elementId) {
        // Update visual selection in preview
        document.querySelectorAll('.element-wrapper.selected').forEach(el => {
            el.classList.remove('selected');
        });

        if (elementId) {
            const element = document.querySelector(`[data-element-id="${elementId}"]`);
            if (element) {
                element.classList.add('selected');
            }
        }
    }

    // Structure view update methods for StateManager integration
    updateStructureAfterMove(change) {
        // Efficiently update structure view after element move
        console.log(`Updating structure after move: ${change.elementId}`);

        // For now, refresh the entire structure view
        // TODO: Implement incremental DOM updates for better performance
        this._refreshStructureIfVisible();
    }

    updateStructureNode(elementId, changes) {
        // Update structure node when element properties change
        const structureNode = document.querySelector(`.structure-node[data-element-id="${elementId}"]`);
        if (structureNode && changes) {
            // Update node label if content changed
            const label = structureNode.querySelector('.structure-node-label');
            if (label && (changes.content || changes.type)) {
                // Refresh to get updated label
                this._refreshStructureIfVisible();
            }
        }
    }

    updateStructureSelection(elementId) {
        // Update selection in structure view
        document.querySelectorAll('.structure-node.selected').forEach(node => {
            node.classList.remove('selected');
        });

        if (elementId) {
            const node = document.querySelector(`.structure-node[data-element-id="${elementId}"]`);
            if (node) {
                node.classList.add('selected');
                // Ensure node is visible
                this.ensureStructureNodeVisible(node);
            }
        }
    }

    ensureStructureNodeVisible(node) {
        // Ensure the node is visible in the structure view
        const structureWindow = document.querySelector('.structure-window');
        if (structureWindow && node) {
            const content = structureWindow.querySelector('.structure-content');
            if (content) {
                // Expand parent nodes if needed
                let parent = node.parentElement;
                while (parent && parent !== content) {
                    if (parent.classList.contains('structure-node')) {
                        parent.classList.add('expanded');
                        const children = parent.querySelector('.structure-children');
                        if (children) {
                            children.style.display = 'block';
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
    }

    getApiBaseUrl() {
        // API routes are registered at /api/page-builder/ outside i18n_patterns
        // No language prefix needed
        return '/api/page-builder';
    }

    setupDragAndDrop() {
        // Setup draggable components from the library
        const componentItems = document.querySelectorAll('.component-item');
        componentItems.forEach(item => {
            // Ensure draggable is set
            item.draggable = true;
            // Use arrow functions to maintain 'this' context
            item.ondragstart = (e) => this.handleDragStart(e);
            item.ondragend = (e) => this.handleDragEnd(e);
        });

        // Setup drop zones
        this.setupDropZones();
    }

    setupDropZones() {
        // Main drop zone for empty page
        const mainDropZone = document.getElementById('main-drop-zone');
        if (mainDropZone) {
            this.setupDropZone(mainDropZone, this.handleDropOnPage.bind(this));
        }

        // Page drop zone (persistent drop zone for adding elements to page)
        const pageDropZones = document.querySelectorAll('.page-drop-zone');
        pageDropZones.forEach(zone => {
            this.setupDropZone(zone, this.handleDropOnPage.bind(this));
        });

        // Element drop zones
        const elementDropZones = document.querySelectorAll('.element-drop-zone');
        elementDropZones.forEach(zone => {
            this.setupDropZone(zone, this.handleDropElement.bind(this));
        });

        // Container drop zones
        const containerDropZones = document.querySelectorAll('.container-drop-zone');
        containerDropZones.forEach(zone => {
            this.setupDropZone(zone, this.handleDropElement.bind(this));
            // Add click handler for quick add menu
            zone.style.cursor = 'pointer';
            zone.onclick = (event) => {
                const containerId = zone.dataset.containerId;
                this.showQuickAddMenu(event, 'container', containerId);
            };
        });

        // Section drop zones (between sections)
        this.setupSectionDropZones();

        // Element insert zones (between elements for dropping new elements)
        this.setupElementInsertZones();

        // Page-level sortable is now handled in initializePreviewSortables()
        // to ensure it's properly recreated when needed

        // Setup element wrapper click handlers to prevent bubbling
        this.setupElementClickHandlers();
    }

    setupDropZone(element, dropHandler) {
        // Remove existing event listeners to prevent duplicates
        element.removeEventListener('dragover', this.handleDragOver);
        element.removeEventListener('dragenter', this.handleDragEnter);
        element.removeEventListener('dragleave', this.handleDragLeave);

        // Remove existing drop handler if it exists
        if (element._dropHandler) {
            element.removeEventListener('drop', element._dropHandler);
        }

        // Add new event listeners
        element.addEventListener('dragover', this.handleDragOver);
        element.addEventListener('dragenter', this.handleDragEnter);
        element.addEventListener('dragleave', this.handleDragLeave);
        element.addEventListener('drop', dropHandler);

        // Store reference to drop handler for future removal
        element._dropHandler = dropHandler;
    }

    setupSortableSections() {
        const sectionsContainer = document.getElementById('page-elements');
        if (sectionsContainer) {
            new Sortable(sectionsContainer, {
                group: 'sections',
                animation: 150,
                ghostClass: 'sortable-ghost',
                chosenClass: 'sortable-chosen',
                handle: '.move-btn',
                onEnd: (evt) => {
                    this.updateSectionOrder(evt);
                }
            });
        }
    }

    // Helper function to get the correct draggable elements based on container type
    getDraggableElements(container) {
        // In containers: Sortable moves .container-child-wrapper elements
        // At root level: Sortable moves .element-wrapper elements directly
        const isContainer = container.classList.contains('pb-container-content') ||
                           container.classList.contains('pb-modal-builder__inner');

        if (isContainer) {
            // In containers (regular or modal popup), get the wrapper elements
            return Array.from(container.querySelectorAll(':scope > .container-child-wrapper'));
        } else {
            // At root level (page-elements), get direct element-wrapper children
            return Array.from(container.querySelectorAll(':scope > .element-wrapper'));
        }
    }

    // Helper to get element ID from a draggable unit
    getElementIdFromDraggable(draggable) {
        // If it's a container-child-wrapper, look inside for the element
        if (draggable.classList.contains('container-child-wrapper')) {
            const element = draggable.querySelector('.element-wrapper');
            return element ? element.dataset.elementId : null;
        }
        // If it's directly an element-wrapper
        if (draggable.classList.contains('element-wrapper')) {
            return draggable.dataset.elementId;
        }
        return null;
    }

    // New clean preview sortables implementation
    initializePreviewSortables() {
        // Clean up any existing preview sortables
        if (!this.previewSortables) {
            this.previewSortables = [];
        }

        // Destroy existing sortables with better error handling
        this.previewSortables.forEach(sortable => {
            try {
                // Check if sortable is valid and has an element reference
                if (sortable && sortable.destroy && sortable.el) {
                    // Additional check to ensure the element is still in the DOM
                    if (document.body.contains(sortable.el)) {
                        sortable.destroy();
                    }
                }
            } catch (error) {
                // Only log if it's not the expected null reference error
                if (!error.message?.includes("can't access property")) {
                    console.warn('Error destroying sortable:', error);
                }
            }
        });
        this.previewSortables = [];

        // Also clean up the page-level sortable if it exists
        if (this.pageLevelSortable) {
            try {
                // Check if sortable is valid and has an element reference
                if (this.pageLevelSortable.destroy && this.pageLevelSortable.el) {
                    // Additional check to ensure the element is still in the DOM
                    if (document.body.contains(this.pageLevelSortable.el)) {
                        this.pageLevelSortable.destroy();
                    }
                }
            } catch (error) {
                // Only log if it's not the expected null reference error
                if (!error.message?.includes("can't access property")) {
                    console.warn('Error destroying page-level sortable:', error);
                }
            }
            this.pageLevelSortable = null;
        }

        // Recreate page-level sortable for root elements
        const pageElements = document.getElementById('page-elements');
        if (pageElements && typeof Sortable !== 'undefined') {
            this.pageLevelSortable = new Sortable(pageElements, {
                animation: 150,
                ghostClass: 'sortable-ghost',
                chosenClass: 'sortable-chosen',
                dragClass: 'sortable-drag',
                filter: '.page-drop-zone', // Don't drag the drop zone
                draggable: '.element-wrapper', // Drag elements directly
                forceFallback: false,
                onStart: (evt) => {
                    document.body.classList.add('is-dragging-element');
                },
                onEnd: (evt) => {
                    document.body.classList.remove('is-dragging-element');
                    // Handle reordering of page elements
                    const elementId = evt.item.dataset.elementId;
                    const oldIndex = evt.oldIndex;
                    const newIndex = evt.newIndex;

                    if (oldIndex !== newIndex && elementId) {
                        // Send reorder request to server
                        this.reorderPageElements(elementId, newIndex);
                    }
                }
            });
        }

        // Setup sortables for all containers (including modal popups)
        const containers = document.querySelectorAll('.pb-container-content, .pb-modal-builder__inner');
        console.log(`Initializing preview sortables for ${containers.length} containers`);

        containers.forEach((container, index) => {
            try {
                const sortable = new Sortable(container, {
                    group: 'preview-elements', // Shared group for all containers
                    animation: 150,
                    draggable: '.container-child-wrapper', // Drag entire wrapper
                    ghostClass: 'sortable-ghost',
                    chosenClass: 'sortable-chosen',
                    dragClass: 'sortable-drag',
                    filter: '.container-drop-zone', // Don't drag drop zones
                    preventOnFilter: false,
                    swapThreshold: 0.65,
                    forceFallback: false,  // Use native drag for better index detection
                    onStart: (evt) => {
                        console.log(`🎯 Drag start: index ${evt.oldIndex} in container`);
                        // Capture state BEFORE any DOM changes for undo
                        if (window.pageStateManager) {
                            evt.item._preDropStateSnapshot = window.pageStateManager.captureState();
                            console.log('📸 Captured pre-move state snapshot');
                        }
                        // Also capture DOM snapshot before the move
                        if (window.historyManager && window.historyManager.domSnapshot) {
                            evt.item._preMoveSnapshot = window.historyManager.domSnapshot.capture();
                            console.log('📸 Captured pre-move DOM snapshot');
                        }
                    },
                    onEnd: async (evt) => {
                        console.log(`🎯 Drag end: from ${evt.oldIndex} to ${evt.newIndex}`);
                        await this.updateContainerElementOrder(evt);
                    }
                });

                this.previewSortables.push(sortable);
                console.log(`Container ${index} sortable initialized`);
            } catch (error) {
                console.error(`Failed to create sortable for container ${index}:`, error);
            }
        });
    }

    setupSectionDropZones() {
        // Create drop zones between sections for inserting new sections
        const sectionsContainer = document.getElementById('page-elements');
        if (sectionsContainer) {
            // Clear existing section drop zones first
            const existingDropZones = sectionsContainer.querySelectorAll('.section-drop-zone');
            existingDropZones.forEach(zone => zone.remove());
            
            const sections = sectionsContainer.querySelectorAll('.section-wrapper');
            
            if (sections.length > 0) {
                // Add drop zone before first section (position 0)
                this.createSectionDropZone(sectionsContainer, 0);
                
                // Add drop zones between sections
                sections.forEach((section, index) => {
                    this.createSectionDropZone(sectionsContainer, index + 1, section);
                });
                
                // Always add a final drop zone at the end for adding new sections
                // Use sections.length + 1 to match getNextSectionOrder()
                const lastSection = sections[sections.length - 1];
                this.createSectionDropZone(sectionsContainer, sections.length + 1, lastSection, true);
            }
            // If there are no sections, the main-drop-zone will handle section drops
        }
    }

    setupElementInsertZones() {
        // Create insert zones between elements at root level (page-elements)
        const pageElements = document.getElementById('page-elements');
        if (pageElements) {
            this.createInsertZonesForContainer(pageElements, 'root');
        }

        // Create insert zones inside each container (including modal popups)
        const containers = document.querySelectorAll('.pb-container-content, .pb-modal-builder__inner');
        containers.forEach(container => {
            const containerId = container.closest('[data-element-id]')?.dataset.elementId;
            if (containerId) {
                this.createInsertZonesForContainer(container, containerId);
            }
        });
    }

    createInsertZonesForContainer(container, containerId) {
        // Clear existing insert zones in this container
        const existingZones = container.querySelectorAll(':scope > .element-insert-zone');
        existingZones.forEach(zone => zone.remove());

        // Get direct child elements (excluding drop zones and insert zones)
        const elements = Array.from(container.children).filter(child =>
            child.classList.contains('element-wrapper') ||
            child.classList.contains('container-child-wrapper')
        );

        if (elements.length === 0) return;

        // Create insert zone before first element (position 0)
        this.createElementInsertZone(container, containerId, 0, elements[0]);

        // Create insert zones after each element
        elements.forEach((element, index) => {
            this.createElementInsertZone(container, containerId, index + 1, element, true);
        });
    }

    createElementInsertZone(container, containerId, position, referenceElement, insertAfter = false) {
        const insertZone = document.createElement('div');
        insertZone.className = 'element-insert-zone';
        insertZone.dataset.containerId = containerId;
        insertZone.dataset.position = position;

        insertZone.innerHTML = '<span class="insert-indicator">Drop element here</span>';

        // Setup drop functionality
        this.setupDropZone(insertZone, this.handleDropElementInsert.bind(this));

        // Insert the zone
        if (insertAfter) {
            referenceElement.insertAdjacentElement('afterend', insertZone);
        } else {
            container.insertBefore(insertZone, referenceElement);
        }
    }

    setupElementClickHandlers() {
        // Setup click handlers for element wrappers to prevent event bubbling
        const elementWrappers = document.querySelectorAll('.element-wrapper');
        elementWrappers.forEach(wrapper => {
            this.setupElementClickHandler(wrapper);
        });
    }

    setupElementClickHandler(wrapper) {
        // Skip if handler already attached (check for data attribute)
        if (wrapper.dataset.hasClickHandler === 'true') {
            return;
        }

        // Styles (position, z-index, pointer-events) are handled by CSS:
        // .element-wrapper { position: relative; z-index: 1; }
        // .element-wrapper .element-wrapper { z-index: 10 !important; }
        // .element-content { pointer-events: auto; position: relative; }

        // Track if element is being dragged
        let isDragging = false;
        let dragStartX = 0;
        let dragStartY = 0;

        wrapper.addEventListener('mousedown', (event) => {
            isDragging = false;
            dragStartX = event.clientX;
            dragStartY = event.clientY;
        });

        wrapper.addEventListener('mousemove', (event) => {
            // If mouse moved more than 5 pixels, consider it a drag
            const deltaX = Math.abs(event.clientX - dragStartX);
            const deltaY = Math.abs(event.clientY - dragStartY);
            if (deltaX > 5 || deltaY > 5) {
                isDragging = true;
            }
        });

        // Add click handler that stops propagation
        wrapper.addEventListener('click', (event) => {
            // Don't interfere with dragging
            if (isDragging) {
                isDragging = false;
                return;
            }
            // Let control button clicks (edit/delete) propagate to document-level delegation
            if (event.target.closest('.element-controls')) {
                return;
            }
            event.stopPropagation();
            event.stopImmediatePropagation();
            this.handleElementClick(event, wrapper);
        });

        // Mark as having handler attached
        wrapper.dataset.hasClickHandler = 'true';
    }

    handleElementClick(event, wrapper) {
        // Stop propagation to prevent parent elements from being selected
        event.stopPropagation();
        // Don't prevent default - it interferes with dragging

        // Only select this element if we're not clicking on control buttons
        if (!event.target.closest('.element-controls')) {
            const elementId = wrapper.dataset.elementId;
            if (elementId) {
                console.log('Element wrapper clicked:', elementId);

                // Update structure view selection
                this.syncStructureSelection(elementId);

                editElement(elementId, event);
            }
        }
    }

    createSectionDropZone(container, position, afterElement = null, isFinal = false) {
        const dropZone = document.createElement('div');
        dropZone.className = 'section-drop-zone';
        if (isFinal) dropZone.classList.add('section-drop-zone-final');
        dropZone.dataset.position = position;
        
        const dropText = isFinal ? 'Drop elements here to add' : 'Drop elements here'; // Updated: removed section references
        dropZone.innerHTML = `<div class="drop-indicator">${dropText}</div>`;
        
        // Style the drop zone - make final zone more prominent
        const baseStyles = `
            min-height: ${isFinal ? '60px' : '40px'};
            margin: 10px 20px;
            border: 2px dashed ${isFinal ? '#3b82f6' : '#cbd5e1'};
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            opacity: ${isFinal ? '0.7' : '0'};
            transition: all 0.3s ease;
            background: ${isFinal ? '#f0f9ff' : '#f8fafc'};
        `;
        dropZone.style.cssText = baseStyles;
        
        // Setup drop functionality
        this.setupDropZone(dropZone, this.handleDropSection.bind(this));
        
        // Insert the drop zone
        if (afterElement) {
            afterElement.insertAdjacentElement('afterend', dropZone);
        } else {
            container.insertAdjacentElement('afterbegin', dropZone);
        }
    }

    setupEventListeners() {
        // Device preview buttons
        document.querySelectorAll('.device-btn').forEach(btn => {
            btn.addEventListener('click', this.switchDevice.bind(this));
        });

        // Element selection
        document.addEventListener('click', this.handleElementClick.bind(this));

        // Layout picker event delegation
        document.addEventListener('click', (e) => {
            // Apply container layout
            const applyLayoutBtn = e.target.closest('[data-action="apply-container-layout"]');
            if (applyLayoutBtn) {
                e.stopPropagation();
                const containerId = applyLayoutBtn.dataset.containerId;
                const layoutType = applyLayoutBtn.dataset.layoutType;
                if (containerId && layoutType) {
                    applyContainerLayout(containerId, layoutType);
                }
                return;
            }

            // Skip container layout
            const skipLayoutBtn = e.target.closest('[data-action="skip-container-layout"]');
            if (skipLayoutBtn) {
                e.stopPropagation();
                const containerId = skipLayoutBtn.dataset.containerId;
                if (containerId) {
                    skipContainerLayout(containerId);
                }
                return;
            }

            // Edit element
            const editBtn = e.target.closest('[data-action="edit-element"]');
            if (editBtn) {
                const elementId = editBtn.dataset.elementId;
                if (elementId) {
                    this.editElement(parseInt(elementId, 10), e);
                }
                return;
            }

            // Delete element
            const deleteBtn = e.target.closest('[data-action="delete-element"]');
            if (deleteBtn) {
                const elementId = deleteBtn.dataset.elementId;
                if (elementId) {
                    deleteElement(parseInt(elementId, 10), e);
                }
                return;
            }

            // Delete section
            const deleteSectionBtn = e.target.closest('[data-action="delete-section"]');
            if (deleteSectionBtn) {
                const sectionId = deleteSectionBtn.dataset.sectionId;
                if (sectionId) {
                    deleteSection(parseInt(sectionId, 10));
                }
                return;
            }

            // Toolbar actions
            if (e.target.closest('[data-action="open-page-settings"]')) {
                openPageSettings();
                return;
            }
            if (e.target.closest('[data-action="toggle-version-history"]')) {
                toggleVersionHistory();
                return;
            }
            if (e.target.closest('[data-action="refresh-versions"]')) {
                loadVersionHistory();
                return;
            }
            const revertBtn = e.target.closest('[data-action="revert-version"]');
            if (revertBtn) {
                const versionId = revertBtn.dataset.versionId;
                if (versionId) revertToVersion(parseInt(versionId, 10));
                return;
            }
            if (e.target.closest('[data-action="undo"]')) {
                undoAction();
                return;
            }
            if (e.target.closest('[data-action="redo"]')) {
                redoAction();
                return;
            }
            if (e.target.closest('[data-action="toggle-structure-view"]')) {
                this.toggleStructureView();
                return;
            }
            if (e.target.closest('[data-action="preview-page"]')) {
                previewPage();
                return;
            }
            if (e.target.closest('[data-action="save-draft"]')) {
                saveDraft();
                return;
            }
            if (e.target.closest('[data-action="toggle-save-dropdown"]')) {
                toggleSaveDropdown(e);
                return;
            }
            if (e.target.closest('[data-action="publish-page"]')) {
                publishPage();
                return;
            }

            // Quick add menu
            const quickAddBtn = e.target.closest('[data-action="show-quick-add"]');
            if (quickAddBtn) {
                const addTo = quickAddBtn.dataset.addTo;
                if (window.builderInstance) {
                    window.builderInstance.showQuickAddMenu(e, addTo);
                }
                return;
            }

            // Modal actions
            if (e.target.closest('[data-action="close-modal"]')) {
                closeModal();
                return;
            }
            if (e.target.closest('[data-action="save-element"]')) {
                saveElement();
                return;
            }

            // Save element changes (generic)
            const saveChangesBtn = e.target.closest('[data-action="save-element-changes"]');
            if (saveChangesBtn) {
                const elementId = saveChangesBtn.dataset.elementId;
                if (elementId) {
                    saveElementChanges(parseInt(elementId, 10));
                }
                return;
            }

            // Cancel element edit
            if (e.target.closest('[data-action="cancel-element-edit"]')) {
                cancelElementEdit();
                return;
            }

            // Structure view actions
            if (e.target.closest('[data-action="expand-all-structure"]')) {
                this.expandAllStructureNodes();
                return;
            }
            if (e.target.closest('[data-action="collapse-all-structure"]')) {
                this.collapseAllStructureNodes();
                return;
            }
        });

        // Hover effects for drop zone (CSS handles this now, but adding class for reference)
        document.addEventListener('mouseover', (e) => {
            const dropZone = e.target.closest('.page-drop-zone');
            if (dropZone) {
                dropZone.style.opacity = '1';
                dropZone.style.borderColor = '#4a5568';
            }
        });
        document.addEventListener('mouseout', (e) => {
            const dropZone = e.target.closest('.page-drop-zone');
            if (dropZone && !dropZone.contains(e.relatedTarget)) {
                dropZone.style.opacity = '0.7';
                dropZone.style.borderColor = '#cbd5e0';
            }
        });
    }

    // Drag and Drop Handlers
    handleDragStart(e) {
        console.log('Drag start:', e.target);
        this.isDragging = true;
        const componentData = {
            type: 'element', // Everything is now an element
            elementType: e.target.dataset.elementType || e.currentTarget.dataset.elementType
        };
        console.log('Setting drag data:', componentData);
        e.dataTransfer.setData('text/plain', JSON.stringify(componentData));
        e.dataTransfer.effectAllowed = 'copy';

        // Add global dragging state for visual feedback
        document.body.classList.add('is-dragging-element');

        // Create drag preview
        this.createDragPreview(e.target, e);
    }

    handleDragEnd(e) {
        this.isDragging = false;
        this.removeDragPreview();

        // Remove drag over states
        document.querySelectorAll('.drag-over').forEach(el => {
            el.classList.remove('drag-over');
        });

        // Remove all visual feedback classes
        document.querySelectorAll('.drop-target-valid, .drop-target-invalid, .drag-source').forEach(el => {
            el.classList.remove('drop-target-valid', 'drop-target-invalid', 'drag-source');
        });

        // Remove global dragging state
        document.body.classList.remove('is-dragging-element');
    }

    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';

        // Add visual feedback for valid drop target
        if (e.currentTarget.classList.contains('container-drop-zone') ||
            e.currentTarget.classList.contains('empty-drop-zone')) {
            e.currentTarget.classList.add('drop-target-valid');
        }
    }

    handleDragEnter(e) {
        e.preventDefault();
        e.target.classList.add('drag-over');

        // Add visual feedback classes
        if (e.currentTarget.classList.contains('container-drop-zone') ||
            e.currentTarget.classList.contains('empty-drop-zone')) {
            e.currentTarget.classList.add('drop-target-valid');

            // Also highlight parent container if exists (regular container or modal popup)
            const containerWrapper = e.currentTarget.closest('.element-wrapper[data-element-type="container"], .element-wrapper[data-element-type="modal_popup"]');
            if (containerWrapper) {
                containerWrapper.classList.add('drop-target-valid');
            }
        }
    }

    handleDragLeave(e) {
        e.target.classList.remove('drag-over');

        // Remove visual feedback classes
        e.currentTarget.classList.remove('drop-target-valid', 'drop-target-invalid');

        // Also remove from parent container if exists (regular container or modal popup)
        const containerWrapper = e.currentTarget.closest('.element-wrapper[data-element-type="container"], .element-wrapper[data-element-type="modal_popup"]');
        if (containerWrapper) {
            containerWrapper.classList.remove('drop-target-valid', 'drop-target-invalid');
        }
    }

    handleDropOnPage(e) {
        e.preventDefault();
        e.target.classList.remove('drag-over');

        // Remove visual feedback classes
        e.currentTarget.classList.remove('drop-target-valid', 'drop-target-invalid');
        document.querySelectorAll('.drop-target-valid, .drop-target-invalid').forEach(el => {
            el.classList.remove('drop-target-valid', 'drop-target-invalid');
        });

        // Prevent multiple rapid drops with debounce
        const now = Date.now();
        if (this.lastDropTime && (now - this.lastDropTime) < 500) {
            console.log('Preventing duplicate drop on page - too soon after last drop');
            return;
        }
        this.lastDropTime = now;

        // Try to parse the drag data
        let data;
        const dragData = e.dataTransfer.getData('text/plain');

        // If there's no drag data, this is likely a Sortable.js drag of an existing element
        // Drop zones should only handle drops from the element panel (new elements)
        if (!dragData) {
            // This is an existing element being dragged by Sortable.js, ignore it
            return;
        }

        try {
            data = JSON.parse(dragData);
        } catch (error) {
            // If we can't parse the data, it's not a valid element panel drag
            console.log('Invalid or non-JSON drag data, ignoring');
            return;
        }

        if (data && data.type === 'element') {
            // Add the element directly to the page
            this.addElementToPage(data.elementType);
        }
    }

    handleDropElement(e) {
        e.preventDefault();
        e.target.classList.remove('drag-over');

        // Remove visual feedback classes
        e.currentTarget.classList.remove('drop-target-valid', 'drop-target-invalid');
        document.querySelectorAll('.drop-target-valid, .drop-target-invalid').forEach(el => {
            el.classList.remove('drop-target-valid', 'drop-target-invalid');
        });

        // Prevent multiple rapid drops with debounce
        const now = Date.now();
        if (this.lastDropTime && (now - this.lastDropTime) < 500) {
            console.log('Preventing duplicate drop - too soon after last drop');
            return;
        }
        this.lastDropTime = now;

        // Try to parse the drag data
        let data;
        const dragData = e.dataTransfer.getData('text/plain');

        // If there's no drag data, this is likely a Sortable.js drag of an existing element
        // Drop zones should only handle drops from the element panel (new elements)
        if (!dragData) {
            // This is an existing element being dragged by Sortable.js, ignore it
            return;
        }

        try {
            data = JSON.parse(dragData);
        } catch (error) {
            // If we can't parse the data, it's not a valid element panel drag
            console.log('Invalid or non-JSON drag data, ignoring');
            return;
        }

        if (data && data.type === 'element') {
            // Check if this is a container drop zone or if target is inside one
            let dropZone = e.target;
            if (!dropZone.classList.contains('container-drop-zone')) {
                dropZone = e.target.closest('.container-drop-zone');
            }

            if (dropZone && dropZone.classList.contains('container-drop-zone')) {
                const containerId = dropZone.dataset.containerId;
                this.addElementToContainer(containerId, data.elementType);
            } else {
                // Regular section drop zone
                const elementsContainer = e.target.closest('.elements-container');
                if (elementsContainer) {
                    const sectionId = elementsContainer.dataset.sectionId;
                    this.addElement(sectionId, data.elementType);
                } else {
                    console.error('Could not find elements container');
                }
            }
        }
    }

    async handleDropElementInsert(e) {
        e.preventDefault();
        e.stopPropagation();

        // Get the insert zone
        let insertZone = e.target;
        if (!insertZone.classList.contains('element-insert-zone')) {
            insertZone = e.target.closest('.element-insert-zone');
        }

        if (!insertZone) {
            console.error('Insert zone not found');
            return;
        }

        insertZone.classList.remove('drag-over');

        // Prevent duplicate drops
        const now = Date.now();
        if (this.lastDropTime && (now - this.lastDropTime) < 500) {
            console.log('Preventing duplicate drop');
            return;
        }
        this.lastDropTime = now;

        // Parse drag data
        const dragData = e.dataTransfer.getData('text/plain');
        if (!dragData) return;

        let data;
        try {
            data = JSON.parse(dragData);
        } catch (error) {
            console.log('Invalid drag data');
            return;
        }

        if (!data || data.type !== 'element') return;

        const containerId = insertZone.dataset.containerId;
        const position = parseInt(insertZone.dataset.position);

        if (containerId === 'root') {
            // Add to page root level at specific position
            await this.addElementToPageAtPosition(data.elementType, position);
        } else {
            // Add to container at specific position
            await this.addElementToContainerAtPosition(containerId, data.elementType, position);
        }
    }

    async addElementToPageAtPosition(elementType, position) {
        try {
            // Get existing elements BEFORE creating new one (for DOM positioning)
            const pageElements = document.getElementById('page-elements');
            const existingElements = pageElements ?
                Array.from(pageElements.querySelectorAll(':scope > .element-wrapper')) : [];

            const elementData = {
                page_id: this.pageData.id,
                element_type: elementType,
                name: `${elementType.charAt(0).toUpperCase() + elementType.slice(1)} Element`,
                content: this.getDefaultContent(elementType),
                order: position
            };

            const command = new AddElementCommand(elementData, null);
            await historyManager.execute(command);

            if (command.createdElementId) {
                // Reorder existing elements to make room (exclude the newly created element)
                await this.reorderElementsAfterInsert('root', position, command.createdElementId, existingElements);

                // Move the new element to the correct DOM position
                this.moveElementToPosition('root', command.createdElementId, position);

                this.showNotification('Element added successfully!', 'success');
                this._refreshStructureIfVisible();
                this.initializePreviewSortables();
                this.setupElementInsertZones();
            }
        } catch (error) {
            console.error('Error adding element at position:', error);
            this.showNotification('Failed to add element', 'error');
        }
    }

    async addElementToContainerAtPosition(containerId, elementType, position) {
        try {
            // Get existing elements BEFORE creating new one (for DOM positioning)
            const container = document.querySelector(`[data-element-id="${containerId}"] .pb-container-content`);
            const existingElements = container ?
                Array.from(container.querySelectorAll(':scope > .element-wrapper, :scope > .container-child-wrapper > .element-wrapper')) : [];

            const elementData = {
                parent_element_id: containerId,
                element_type: elementType,
                name: `${elementType.charAt(0).toUpperCase() + elementType.slice(1)} Element`,
                content: this.getDefaultContent(elementType),
                order: position
            };

            const command = new AddElementCommand(elementData, containerId);
            await historyManager.execute(command);

            if (command.createdElementId) {
                // Reorder existing elements to make room (exclude the newly created element)
                await this.reorderElementsAfterInsert(containerId, position, command.createdElementId, existingElements);

                // Move the new element to the correct DOM position
                this.moveElementToPosition(containerId, command.createdElementId, position);

                this.showNotification('Element added to container!', 'success');
                this._refreshStructureIfVisible();
                this.initializePreviewSortables();
                this.setupElementInsertZones();
            }
        } catch (error) {
            console.error('Error adding element to container at position:', error);
            this.showNotification('Failed to add element', 'error');
        }
    }

    moveElementToPosition(containerId, elementId, position) {
        // Find the newly created element
        const newElement = document.querySelector(`[data-element-id="${elementId}"]`);
        if (!newElement) return;

        // Get the parent container
        let parentContainer;
        if (containerId === 'root') {
            parentContainer = document.getElementById('page-elements');
        } else {
            parentContainer = document.querySelector(`[data-element-id="${containerId}"] .pb-container-content`);
        }
        if (!parentContainer) return;

        // Get the wrapper (might be wrapped in container-child-wrapper)
        const elementWrapper = newElement.closest('.container-child-wrapper') || newElement;

        // Safety check: verify element is not an ancestor of the parent container
        // This prevents HierarchyRequestError when DOM structure is unexpected
        if (elementWrapper.contains(parentContainer)) {
            console.warn(`[moveElementToPosition] Cannot move element ${elementId}: element contains the parent container`);
            return;
        }

        // Check if element is already in the correct parent container
        if (!parentContainer.contains(elementWrapper)) {
            console.warn(`[moveElementToPosition] Element ${elementId} is not in the expected parent container`);
            return;
        }

        // Get all sibling elements (excluding the new one, insert zones, and non-element children)
        const siblings = Array.from(parentContainer.children).filter(child =>
            (child.classList.contains('element-wrapper') || child.classList.contains('container-child-wrapper')) &&
            child !== elementWrapper &&
            !child.contains(newElement)
        );

        // Check if element is already at the correct position
        const currentSiblings = Array.from(parentContainer.children).filter(child =>
            child.classList.contains('element-wrapper') || child.classList.contains('container-child-wrapper')
        );
        const currentIndex = currentSiblings.indexOf(elementWrapper);
        if (currentIndex === position) {
            // Already at correct position, no need to move
            return;
        }

        // Insert at the correct position
        if (position === 0) {
            // Insert at the beginning
            const firstSibling = siblings[0];
            if (firstSibling) {
                parentContainer.insertBefore(elementWrapper, firstSibling);
            }
        } else if (position >= siblings.length) {
            // Insert at the end (before any drop zones)
            const dropZone = parentContainer.querySelector('.page-drop-zone, .container-drop-zone');
            if (dropZone) {
                parentContainer.insertBefore(elementWrapper, dropZone);
            } else {
                parentContainer.appendChild(elementWrapper);
            }
        } else {
            // Insert after the element at position-1
            const targetSibling = siblings[position];
            if (targetSibling) {
                parentContainer.insertBefore(elementWrapper, targetSibling);
            }
        }
    }

    async reorderElementsAfterInsert(containerId, insertPosition, excludeElementId = null, existingElements = null) {
        // Use pre-captured elements if provided, otherwise query the DOM
        let elements = existingElements;
        if (!elements) {
            if (containerId === 'root') {
                elements = Array.from(document.querySelectorAll('#page-elements > .element-wrapper'));
            } else {
                const container = document.querySelector(`[data-element-id="${containerId}"] .pb-container-content`);
                if (!container) return;
                elements = Array.from(container.querySelectorAll(':scope > .element-wrapper, :scope > .container-child-wrapper > .element-wrapper'));
            }
        }

        // Filter out the newly created element if needed
        const filteredElements = excludeElementId ?
            elements.filter(el => el.dataset.elementId !== String(excludeElementId)) :
            elements;

        // Build reorder data - shift elements at or after insert position up by 1
        const reorderData = [];
        filteredElements.forEach((element, index) => {
            const elementId = element.dataset.elementId;
            // Elements at or after insert position need to shift up by 1
            const newOrder = index >= insertPosition ? index + 1 : index;
            reorderData.push({
                id: parseInt(elementId),
                order: newOrder
            });
        });

        if (reorderData.length > 0) {
            try {
                await window.apiClient.reorderElements({ elements: reorderData });
            } catch (error) {
                console.warn('Reorder after insert failed:', error);
            }
        }
    }

    // Component Creation
    async addElementToPage(elementType) {
        try {
            // Create a container element if this is the first element on the page
            let containerId = null;

            // Check if we need to create a default container first
            if (elementType !== 'container') {
                // Create container using command pattern for undo/redo support
                const containerData = {
                    page_id: this.pageData.id,
                    element_type: 'container',
                    name: 'Main Container',
                    content: {
                        layout: 'flex',
                        direction: 'column',
                        width: '100',
                        width_unit: '%',
                        padding_top: '20',
                        padding_right: '20',
                        padding_bottom: '20',
                        padding_left: '20',
                        padding_unit: 'px',
                        background_type: 'transparent',
                        align_items: 'stretch',
                        justify_content: 'flex-start',
                        gap: '20',
                        gap_unit: 'px',
                        // Mark as initialized since we're adding a child immediately
                        // This prevents the layout picker from showing
                        layout_initialized: true
                    },
                    order: this.getNextElementOrder()
                };

                // Use command pattern for undo/redo support
                const containerCommand = new AddElementCommand(containerData, null);
                await containerCommand.execute();
                containerId = containerCommand.createdElementId;

                // Don't add to history yet - we'll batch it with the element creation
            }

            // Prepare element data
            const elementData = {
                parent_element_id: containerId,  // If we created a container, use it as parent
                page_id: containerId ? null : this.pageData.id,  // Otherwise add directly to page
                element_type: elementType,
                name: `${elementType.charAt(0).toUpperCase() + elementType.slice(1)} Element`,
                content: this.getDefaultContent(elementType),
                order: containerId ? 0 : this.getNextElementOrder()
            };

            // Create element using command pattern for undo/redo support
            const elementCommand = new AddElementCommand(elementData, containerId);

            // Execute through history manager to enable undo/redo
            await historyManager.execute(elementCommand);

            this.showNotification('Element added successfully!', 'success');

            // Reload the content without full page reload
            this._refreshStructureIfVisible();
            this.initializePreviewSortables();
            this.setupElementInsertZones();
        } catch (error) {
            console.error('Error adding element:', error);
            this.showNotification('Failed to add element', 'error');
        }
    }

    async addElement(sectionId, elementType) {
        try {
            const response = await fetch(`${this.getApiBaseUrl()}/elements/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    section_id: sectionId,
                    element_type: elementType,
                    name: `${elementType.charAt(0).toUpperCase() + elementType.slice(1)} Element`,
                    content: this.getDefaultContent(elementType),
                    order: this.getNextElementOrder(sectionId)
                })
            });

            if (response.ok) {
                const elementData = await response.json();
                // Use the server-provided HTML if available, otherwise fallback to client-side rendering
                if (elementData.element && elementData.element.html) {
                    console.log('Using server HTML for:', elementData.element.element_type);
                    this.renderNewElementWithHTML(sectionId, elementData.element.html);
                } else {
                    console.log('Using client rendering for:', elementData.element?.element_type, 'Data:', elementData);
                    this.renderNewElement(sectionId, elementData.element);
                }
                // Re-setup drop zones and event listeners for the new element
                this.setupDropZones();
                this.setupElementClickHandlers();
                this.showNotification('Element added successfully!', 'success');

                // Refresh structure view to show new element
                this._refreshStructureIfVisible();
            } else {
                throw new Error('Failed to add element');
            }
        } catch (error) {
            console.error('Error adding element:', error);
            this.showNotification('Failed to add element', 'error');
        }
    }

    async addContainerWithConfig(containerId, config) {
        try {
            const response = await fetch(`${this.getApiBaseUrl()}/elements/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    parent_element_id: containerId,
                    element_type: 'container',
                    name: config.direction === 'row' ? 'Row Container' : 'Column Container',
                    content: config,
                    order: 0
                })
            });

            if (response.ok) {
                const elementData = await response.json();

                // Find the container element and update it
                const container = document.querySelector(`#container-${containerId}`);
                if (container) {
                    // Find the content area (regular container, modal popup, etc.)
                    const contentArea = container.querySelector('.pb-container-content') ||
                                        container.querySelector('.pb-modal-builder__inner') ||
                                        container;

                    // Find existing drop zone
                    const existingDropZone = contentArea.querySelector('.container-drop-zone');

                    // If drop zone exists, we'll insert before it, otherwise append to content area
                    const insertPosition = existingDropZone ? 'beforebegin' : 'beforeend';
                    const targetElement = existingDropZone || contentArea;
                    
                    // Use server-provided HTML if available
                    if (elementData.element && elementData.element.html) {
                        // Server HTML already includes element-wrapper
                        // Determine wrapper styles based on container type
                        let wrapperStyle = '';
                        if (config.direction === 'column') {
                            // Columns should flex to share space horizontally
                            wrapperStyle = 'flex: 1; min-width: 200px;';
                        } else if (config.direction === 'row') {
                            // Rows should span full width
                            wrapperStyle = 'width: 100%;';
                        } else if (config.flex) {
                            // Custom flex value if specified
                            wrapperStyle = `flex: ${config.flex};`;
                        } else {
                            // Default to full width
                            wrapperStyle = 'width: 100%;';
                        }

                        // Wrap in container-child-wrapper div with appropriate styling
                        const wrapperHTML = `
                            <div class="container-child-wrapper" style="${wrapperStyle}">
                                ${elementData.element.html}
                            </div>
                        `;

                        // Insert before drop zone if it exists, otherwise append
                        if (existingDropZone) {
                            existingDropZone.insertAdjacentHTML('beforebegin', wrapperHTML);
                        } else {
                            contentArea.insertAdjacentHTML('beforeend', wrapperHTML);

                            // Add a drop zone at the end if we don't have one
                            const newDropZone = `
                                <div class="container-drop-zone" data-container-id="${containerId}" style="
                                    min-height: 60px;
                                    border: 2px dashed #e2e8f0;
                                    border-radius: 6px;
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                    color: #94a3b8;
                                    font-size: 12px;
                                    background: rgba(241, 245, 249, 0.5);
                                    margin-top: 10px;
                                    opacity: 0.7;
                                    transition: all 0.3s ease;
                                ">
                                    <div style="text-align: center;">
                                        <i class="fas fa-plus" style="font-size: 16px; margin-bottom: 4px; display: block;"></i>
                                        Add element
                                    </div>
                                </div>
                            `;
                            contentArea.insertAdjacentHTML('beforeend', newDropZone);

                            // Setup click handler for the new drop zone
                            const newZone = contentArea.querySelector('.container-drop-zone:last-child');
                            if (newZone) {
                                newZone.style.cursor = 'pointer';
                                newZone.onclick = (event) => {
                                    this.showQuickAddMenu(event, 'container', containerId);
                                };
                            }
                        }
                    } else {
                        // Create fallback HTML
                        const elementHTML = this.createElementHTML(elementData.element);

                        // Determine wrapper styles based on container type
                        let wrapperStyle = '';
                        if (config.direction === 'column') {
                            // Columns should flex to share space horizontally
                            wrapperStyle = 'flex: 1; min-width: 200px;';
                        } else if (config.direction === 'row') {
                            // Rows should span full width
                            wrapperStyle = 'width: 100%;';
                        } else if (config.flex) {
                            // Custom flex value if specified
                            wrapperStyle = `flex: ${config.flex};`;
                        } else {
                            // Default to full width
                            wrapperStyle = 'width: 100%;';
                        }

                        const wrapperHTML = `
                            <div class="container-child-wrapper" style="${wrapperStyle}">
                                <div class="element-wrapper" data-element-id="${elementData.element.id}" data-element-type="container">
                                    <div class="element-controls">
                                        <button class="control-btn edit-btn" data-action="edit-element" data-element-id="${elementData.element.id}">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="control-btn delete-btn" data-action="delete-element" data-element-id="${elementData.element.id}">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                    <div class="element-content">
                                        ${elementHTML}
                                    </div>
                                </div>
                            </div>
                        `;

                        // Insert before drop zone if it exists, otherwise append
                        if (existingDropZone) {
                            existingDropZone.insertAdjacentHTML('beforebegin', wrapperHTML);
                        } else {
                            contentArea.insertAdjacentHTML('beforeend', wrapperHTML);
                        }
                    }

                    // Only setup click handlers for the new element
                    const newElement = contentArea.querySelector(`[data-element-id="${elementData.element.id}"]`);
                    if (newElement && !newElement.dataset.hasClickHandler) {
                        this.setupElementClickHandler(newElement);
                    }

                    // Force re-apply styles to ensure proper z-index stacking
                    if (newElement) {
                        const wrapper = newElement.classList.contains('element-wrapper') ? newElement : newElement.querySelector('.element-wrapper');
                        if (wrapper) {
                            // Ensure the element is properly styled
                            wrapper.style.position = 'relative';
                            wrapper.style.zIndex = '10';

                            // Ensure content is clickable
                            const elementContent = wrapper.querySelector('.element-content');
                            if (elementContent) {
                                elementContent.style.pointerEvents = 'auto';
                            }

                            // Make sure controls are accessible
                            const controls = wrapper.querySelector('.element-controls');
                            if (controls) {
                                controls.style.zIndex = '100';
                                controls.style.pointerEvents = 'auto';
                            }
                        }
                    }

                    this.showNotification(`${config.direction === 'row' ? 'Row' : 'Column'} added to container!`, 'success');

                    // Setup sortable for the new container's content area
                    // Reinitialize preview sortables to include new container
                    this.initializePreviewSortables();

                    // Refresh structure view to show new container
                    this._refreshStructureIfVisible();
                } else {
                    // Fallback: reload the page if we can't find the container
                    location.reload();
                }
            } else {
                throw new Error('Failed to add container');
            }
        } catch (error) {
            console.error('Error adding container:', error);
            this.showNotification('Failed to add container', 'error');
        }
    }

    async addElementToContainer(containerId, elementType) {
        try {
            // Prepare element data
            const elementData = {
                parent_element_id: containerId,
                element_type: elementType,
                name: `${elementType.charAt(0).toUpperCase() + elementType.slice(1)} Element`,
                content: this.getDefaultContent(elementType),
                order: 0 // Will be managed by the container
            };

            // Use command pattern for undo/redo support
            const command = new AddElementCommand(elementData, containerId);
            await historyManager.execute(command);

            // The command execution will handle the API call and return the created element
            if (command.createdElementId) {
                // Refresh the page content and structure view
                this._refreshStructureIfVisible();
                this.initializePreviewSortables();
                this.setupElementInsertZones();

                this.showNotification('Element added to container successfully!', 'success');
            } else {
                throw new Error('Failed to add element to container');
            }
        } catch (error) {
            console.error('Error adding element to container:', error);
            this.showNotification('Failed to add element to container', 'error');
        }
    }

    // Default Content Templates (data-driven from config.json via window.elementMetadata)
    getDefaultContent(elementType) {
        if (window.elementMetadata && window.elementMetadata[elementType]) {
            return {...(window.elementMetadata[elementType].defaults || {})};
        }
        return {};
    }

    // Rendering Methods
    renderNewSection(section) {
        const sectionsContainer = document.getElementById('page-elements');
        const sectionHTML = this.createSectionHTML(section);
        sectionsContainer.insertAdjacentHTML('beforeend', sectionHTML);
        this.setupDropZones(); // Re-setup drop zones for new section
    }

    renderNewElement(sectionId, element) {
        const elementsContainer = document.querySelector(`[data-section-id="${sectionId}"]`);
        const dropZone = elementsContainer.querySelector('.element-drop-zone');
        const elementHTML = this.createElementHTML(element);
        dropZone.insertAdjacentHTML('beforebegin', elementHTML);
    }

    renderNewElementWithHTML(sectionId, elementHTML) {
        const elementsContainer = document.querySelector(`[data-section-id="${sectionId}"]`);
        const dropZone = elementsContainer.querySelector('.element-drop-zone');

        // Server now always sends properly wrapped HTML, so insert directly
        dropZone.insertAdjacentHTML('beforebegin', elementHTML);
    }

    createSectionHTML(section) {
        // Create elements HTML if there are any
        let elementsHTML = '';
        if (section.elements && section.elements.length > 0) {
            elementsHTML = section.elements.map(element =>
                this.createElementHTML(element)
            ).join('');
        }

        return `
            <div class="section-wrapper" data-section-id="${section.id}">
                <div class="section-controls">
                    <button class="control-btn move-btn">
                        <i class="fas fa-arrows-alt"></i>
                    </button>
                    <button class="control-btn delete-btn" data-action="delete-section" data-section-id="${section.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>

                <div class="section-content">
                    <div class="section-generic">
                        <h4>${section.name}</h4>

                        <div class="elements-container" data-section-id="${section.id}">
                            ${elementsHTML}
                            <div class="element-drop-zone">
                                <i class="fas fa-plus"></i>
                                <span>Drop elements here</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    createElementHTML(element) {
        let contentHTML = '';
        const content = element.content;

        switch (element.element_type) {
            case 'container':
                const layout = content.layout || 'flex';
                const direction = content.direction || 'row';
                const justifyContent = content.justify_content || 'flex-start';
                const alignItems = content.align_items || 'stretch';
                const wrap = content.wrap || 'wrap';
                const gap = content.gap || '16px';
                const backgroundColor = content.background_color || 'transparent';
                const showLayoutPicker = content.layout_initialized === false;

                // Build container styles
                let containerStyles = `
                    display: ${layout};
                    ${layout === 'flex' ? `
                    flex-direction: ${direction};
                    justify-content: ${justifyContent};
                    align-items: ${alignItems};
                    flex-wrap: ${wrap};
                    gap: ${gap};
                    ` : ''}
                    ${layout === 'grid' ? `
                    grid-template-columns: ${content.grid_columns || '1fr'};
                    grid-template-rows: ${content.grid_rows || 'auto'};
                    gap: ${gap};
                    ` : ''}
                    background-color: ${backgroundColor};
                    ${content.spacing || ''}
                    min-height: 100px;
                    width: ${content.width || '100%'};
                    ${content.max_width ? `max-width: ${content.max_width};` : ''}
                    ${content.min_height ? `min-height: ${content.min_height};` : ''}
                    ${content.background || ''}
                `;

                // Inner content - either layout picker or drop zone
                let innerContent = '';
                if (showLayoutPicker) {
                    innerContent = `
                        <div class="container-layout-picker" data-container-id="${element.id}">
                            <div class="layout-picker-header">
                                <i class="fas fa-th-large"></i>
                                <h4>Choose a Layout</h4>
                                <p>Select a preset layout or skip for an empty container</p>
                            </div>
                            <div class="layout-options">
                                <div class="layout-option" data-layout="full-width" title="Single full-width column">
                                    <div class="layout-preview">
                                        <div class="preview-row"><div class="preview-col" style="flex: 1;"></div></div>
                                    </div>
                                    <span>Full Width</span>
                                </div>
                                <div class="layout-option" data-layout="2-equal" title="Two equal columns (50% / 50%)">
                                    <div class="layout-preview">
                                        <div class="preview-row">
                                            <div class="preview-col" style="flex: 1;"></div>
                                            <div class="preview-col" style="flex: 1;"></div>
                                        </div>
                                    </div>
                                    <span>2 Equal</span>
                                </div>
                                <div class="layout-option" data-layout="2-col-33-66" title="Two columns (33% / 66%)">
                                    <div class="layout-preview">
                                        <div class="preview-row">
                                            <div class="preview-col" style="flex: 1;"></div>
                                            <div class="preview-col" style="flex: 2;"></div>
                                        </div>
                                    </div>
                                    <span>33% / 66%</span>
                                </div>
                                <div class="layout-option" data-layout="2-col-66-33" title="Two columns (66% / 33%)">
                                    <div class="layout-preview">
                                        <div class="preview-row">
                                            <div class="preview-col" style="flex: 2;"></div>
                                            <div class="preview-col" style="flex: 1;"></div>
                                        </div>
                                    </div>
                                    <span>66% / 33%</span>
                                </div>
                                <div class="layout-option" data-layout="3-equal" title="Three equal columns">
                                    <div class="layout-preview">
                                        <div class="preview-row">
                                            <div class="preview-col" style="flex: 1;"></div>
                                            <div class="preview-col" style="flex: 1;"></div>
                                            <div class="preview-col" style="flex: 1;"></div>
                                        </div>
                                    </div>
                                    <span>3 Equal</span>
                                </div>
                                <div class="layout-option" data-layout="3-col-25-50-25" title="Three columns (25% / 50% / 25%)">
                                    <div class="layout-preview">
                                        <div class="preview-row">
                                            <div class="preview-col" style="flex: 1;"></div>
                                            <div class="preview-col" style="flex: 2;"></div>
                                            <div class="preview-col" style="flex: 1;"></div>
                                        </div>
                                    </div>
                                    <span>25/50/25</span>
                                </div>
                                <div class="layout-option" data-layout="header-2col" title="One full row with two columns below">
                                    <div class="layout-preview">
                                        <div class="preview-row"><div class="preview-col" style="flex: 1;"></div></div>
                                        <div class="preview-row">
                                            <div class="preview-col" style="flex: 1;"></div>
                                            <div class="preview-col" style="flex: 1;"></div>
                                        </div>
                                    </div>
                                    <span>Header + 2 Col</span>
                                </div>
                            </div>
                            <div class="layout-picker-footer">
                                <button type="button" class="skip-layout-btn" data-container-id="${element.id}">
                                    <i class="fas fa-forward"></i>
                                    Skip - Empty Container
                                </button>
                            </div>
                        </div>
                    `;
                } else {
                    innerContent = `
                        <div class="container-drop-zone" data-container-id="${element.id}">
                            <i class="fas fa-plus"></i> Add element
                        </div>
                    `;
                }

                contentHTML = `
                    <div class="pb-container"
                         id="container-${element.id}"
                         data-element-id="${element.id}"
                         data-element-type="container"
                         style="${containerStyles}">
                      <div class="pb-container-content">
                        ${innerContent}
                      </div>
                    </div>
                `;
                break;
            default: {
                // Generic placeholder - replaced by server-rendered HTML from API
                const meta = window.elementMetadata?.[element.element_type];
                const icon = meta?.icon || 'fas fa-puzzle-piece';
                const name = meta?.name || element.element_type;
                contentHTML = `<div class="element-placeholder"><i class="${icon}"></i> ${name}</div>`;
                break;
            }
        }

        return `
            <div class="element-wrapper" data-element-id="${element.id}" data-element-type="${element.element_type}">
                <div class="element-controls">
                    <button class="control-btn edit-btn" data-action="edit-element" data-element-id="${element.id}">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="control-btn delete-btn" data-action="delete-element" data-element-id="${element.id}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="element-content">
                    ${contentHTML}
                </div>
            </div>
        `;
    }

    // Utility Methods
    hideEmptyDropZone() {
        const emptyDropZone = document.getElementById('main-drop-zone');
        if (emptyDropZone) {
            emptyDropZone.style.display = 'none';
        }
    }

    getNextSectionOrder() {
        const sections = document.querySelectorAll('.section-wrapper');
        return sections.length + 1;
    }

    getNextElementOrder(sectionId = null) {
        if (sectionId) {
            const elements = document.querySelectorAll(`[data-section-id="${sectionId}"] .element-wrapper`);
            return elements.length + 1;
        } else {
            // Get order for page-level elements
            const pageElements = document.querySelectorAll('#page-elements > .element-wrapper, #page-elements > .container-wrapper');
            return pageElements.length + 1;
        }
    }

    getCSRFToken() {
        return window.csrfToken || 
               document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name="csrf-token"]')?.content || '';
    }

    createDragPreview(element, event) {
        const preview = document.createElement('div');
        preview.className = 'drag-preview';
        preview.innerHTML = element.querySelector('.component-info strong').textContent;
        preview.style.left = event.clientX + 'px';
        preview.style.top = event.clientY + 'px';
        document.body.appendChild(preview);

        // Follow mouse
        const followMouse = (e) => {
            preview.style.left = e.clientX + 10 + 'px';
            preview.style.top = e.clientY + 10 + 'px';
        };
        document.addEventListener('dragover', followMouse);
        
        // Clean up
        element.addEventListener('dragend', () => {
            document.removeEventListener('dragover', followMouse);
        });
    }

    removeDragPreview() {
        const preview = document.querySelector('.drag-preview');
        if (preview) {
            preview.remove();
        }
    }

    switchDevice(e) {
        // Get the button element (might be the icon if clicked on it)
        const btn = e.target.closest('.device-btn') || e.currentTarget;
        if (!btn) return;

        // Update active device button
        document.querySelectorAll('.device-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update canvas size
        const canvas = document.querySelector('.canvas-frame');
        const device = btn.dataset.device;

        if (canvas && device) {
            canvas.classList.remove('device-desktop', 'device-tablet', 'device-mobile');
            canvas.classList.add(`device-${device}`);
            console.log(`Switched to ${device} view`);
        }
    }

    handleElementClick(e) {
        // Clear previous selection
        document.querySelectorAll('.selected').forEach(el => el.classList.remove('selected'));

        // Select clicked element
        const elementWrapper = e.target.closest('.element-wrapper');
        if (elementWrapper) {
            // Exit page settings mode if active (only when clicking on an actual element)
            if (pageSettingsManager && pageSettingsManager.isPageSettingsMode) {
                pageSettingsManager.exitPageSettingsMode();
                // Restore default properties header
                const sidebarHeader = document.querySelector('.right-sidebar .sidebar-header h3');
                if (sidebarHeader) {
                    sidebarHeader.innerHTML = '<i class="fas fa-cogs"></i> Properties';
                }
            }

            elementWrapper.classList.add('selected');
            this.selectedElement = elementWrapper;
            this.showElementProperties(elementWrapper);
        }
    }

    async loadElementConfig(elementType) {
        try {
            const response = await fetch(`${this.getApiBaseUrl()}/elements/config/${elementType}/`);
            if (response.ok) {
                return await response.json();
            }
        } catch (error) {
            console.error(`Error loading config for ${elementType}:`, error);
        }
        return null;
    }

    async showElementProperties(elementWrapper) {
        const elementId = elementWrapper.dataset.elementId;
        const elementType = elementWrapper.dataset.elementType;
        
        try {
            // Fetch element data from server
            const response = await fetch(`${this.getApiBaseUrl()}/elements/${elementId}/`, {
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch element data');
            }
            
            const elementData = await response.json();
            
            // Show properties in right sidebar
            const propertiesPanel = document.getElementById('properties-panel');

            if (window.propertyRenderer) {
                // Use the property renderer for elements with config.json
                this.loadElementConfig(elementType).then(config => {
                    if (config) {
                        window.propertyRenderer.renderProperties('properties-panel', config, elementData);
                    } else {
                        // Fallback to basic properties
                        this.showBasicProperties(propertiesPanel, elementData);
                    }
                });
            } else {
                this.showBasicProperties(propertiesPanel, elementData);
            }
            
        } catch (error) {
            console.error('Error loading element properties:', error);
            this.showNotification('Failed to load element properties', 'error');
        }
    }

    // DEPRECATED: showContainerProperties has been removed in favor of config.json-based property rendering.
    // Container elements now use the same propertyRenderer system as all other elements.
    // The properties are defined in: page_builder/templates/page_builder/elements/container/config.json

    showBasicProperties(panel, elementData) {
        panel.innerHTML = `
            <div class="properties-container">
                <div class="properties-header">
                    <h4><i class="fas fa-cube"></i> ${elementData.element_type} Properties</h4>
                </div>
                <p>Basic element properties will be implemented here.</p>
            </div>
        `;
    }

    setupPropertyTabs(panel, activeTab = 'layout') {
        const tabBtns = panel.querySelectorAll('.tab-btn');
        const tabContents = panel.querySelectorAll('.tab-content');
        
        // Set the correct active tab immediately
        tabBtns.forEach(btn => {
            if (btn.dataset.tab === activeTab) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        tabContents.forEach(content => {
            if (content.dataset.tab === activeTab) {
                content.classList.add('active');
            } else {
                content.classList.remove('active');
            }
        });
        
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const tabName = btn.dataset.tab;
                
                // Update active tab button
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Update active tab content
                tabContents.forEach(content => {
                    content.classList.remove('active');
                    if (content.dataset.tab === tabName) {
                        content.classList.add('active');
                    }
                });
                
                // Show/hide layout-specific controls
                if (tabName === 'layout') {
                    const layoutSelect = panel.querySelector('select[name="layout"]');
                    if (layoutSelect) {
                        this.toggleLayoutControls(layoutSelect.value);
                    }
                }
            });
        });
    }

    toggleLayoutControls(layoutType) {
        const flexControls = document.querySelector('.flex-controls');
        const gridControls = document.querySelector('.grid-controls');
        
        if (flexControls) {
            flexControls.style.display = (layoutType === 'flex' || !layoutType) ? 'block' : 'none';
        }
        if (gridControls) {
            gridControls.style.display = (layoutType === 'grid') ? 'block' : 'none';
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    showQuickAddMenu(event, target = 'page', targetId = null) {
        event.preventDefault();
        event.stopPropagation();

        // Remove any existing quick add menu
        const existingMenu = document.querySelector('.quick-add-menu');
        if (existingMenu) {
            existingMenu.remove();
        }

        // Create quick add menu
        const menu = document.createElement('div');
        menu.className = 'quick-add-menu';
        menu.style.cssText = `
            position: absolute;
            left: ${event.pageX}px;
            top: ${event.pageY}px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            padding: 8px;
            z-index: 10000;
            min-width: 200px;
        `;

        // Common elements to add
        const elements = [
            { type: 'container', label: 'Container', icon: 'fas fa-box' },
            { type: 'heading', label: 'Heading', icon: 'fas fa-heading' },
            { type: 'text', label: 'Text', icon: 'fas fa-paragraph' },
            { type: 'button', label: 'Button', icon: 'fas fa-square' },
            { type: 'image', label: 'Image', icon: 'fas fa-image' },
            { type: 'divider', label: 'Divider', icon: 'fas fa-minus' }
        ];

        elements.forEach(elem => {
            const menuItem = document.createElement('div');
            menuItem.style.cssText = `
                padding: 8px 12px;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 10px;
                border-radius: 4px;
                transition: background 0.2s;
                color: #2d3748;
                font-size: 14px;
                font-weight: 500;
            `;
            menuItem.innerHTML = `<i class="${elem.icon}" style="width: 20px; text-align: center; color: #4a5568;"></i> ${elem.label}`;
            menuItem.onmouseover = () => {
                menuItem.style.background = '#edf2f7';
                menuItem.style.color = '#1a202c';
            };
            menuItem.onmouseout = () => {
                menuItem.style.background = 'transparent';
                menuItem.style.color = '#2d3748';
            };
            menuItem.onclick = () => {
                menu.remove();
                if (target === 'page') {
                    this.addElementToPage(elem.type);
                } else if (target === 'container' && targetId) {
                    this.addElementToContainer(targetId, elem.type);
                } else if (target === 'section' && targetId) {
                    this.addElement(targetId, elem.type);
                }
            };
            menu.appendChild(menuItem);
        });

        document.body.appendChild(menu);

        // Auto-close menu when mouse moves away
        let menuRect = menu.getBoundingClientRect();
        const mouseDistanceThreshold = 50; // Distance in pixels before menu closes
        let isOverMenu = false;

        // Track if mouse is over menu
        menu.addEventListener('mouseenter', () => {
            isOverMenu = true;
        });

        menu.addEventListener('mouseleave', () => {
            isOverMenu = false;
            // Update rect when leaving in case menu moved
            menuRect = menu.getBoundingClientRect();
        });

        const checkMouseDistance = (e) => {
            // Don't close if mouse is over the menu
            if (isOverMenu) return;

            // Calculate distance from mouse to menu edges
            const distanceLeft = menuRect.left - e.clientX;
            const distanceRight = e.clientX - menuRect.right;
            const distanceTop = menuRect.top - e.clientY;
            const distanceBottom = e.clientY - menuRect.bottom;

            // Get the minimum distance to any edge
            const horizontalDistance = Math.max(0, Math.max(distanceLeft, distanceRight));
            const verticalDistance = Math.max(0, Math.max(distanceTop, distanceBottom));
            const distance = Math.sqrt(horizontalDistance * horizontalDistance + verticalDistance * verticalDistance);

            // Close menu if mouse is too far away
            if (distance > mouseDistanceThreshold) {
                menu.remove();
                document.removeEventListener('mousemove', checkMouseDistance);
                document.removeEventListener('click', closeMenuOnClick);
            }
        };

        // Also close menu when clicking outside (as fallback)
        const closeMenuOnClick = (e) => {
            if (!menu.contains(e.target)) {
                menu.remove();
                document.removeEventListener('mousemove', checkMouseDistance);
                document.removeEventListener('click', closeMenuOnClick);
            }
        };

        // Start listening after a small delay to prevent immediate closure
        setTimeout(() => {
            document.addEventListener('mousemove', checkMouseDistance);
            document.addEventListener('click', closeMenuOnClick);
        }, 100);
    }

    // DOM Manipulation Helper Methods for Live Updates
    removeElementFromPreview(elementId) {
        const element = document.querySelector(`[data-element-id="${elementId}"]`);
        if (element) {
            // If element is wrapped, remove the wrapper
            const wrapper = element.closest('.container-child-wrapper');
            if (wrapper) {
                wrapper.remove();
            } else {
                element.remove();
            }
            return true;
        }
        return false;
    }

    updateElementInPreview(elementId, content) {
        const element = document.querySelector(`[data-element-id="${elementId}"]`);
        if (!element) return false;

        // Find the element content area
        const contentArea = element.querySelector('.element-content');
        if (!contentArea) return false;

        // Generate new HTML based on element type
        const elementType = element.dataset.elementType;

        // Create a temporary element object to reuse createElementHTML logic
        const tempElement = {
            id: elementId,
            element_type: elementType,
            content: content
        };

        // Get the full HTML and extract just the content part
        const fullHTML = this.createElementHTML(tempElement);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = fullHTML;

        const newContentElement = tempDiv.querySelector('.element-content');
        if (newContentElement) {
            contentArea.innerHTML = newContentElement.innerHTML;
            return true;
        }

        return false;
    }

    addElementToPreview(elementData, parentId = null, afterElementId = null) {
        // Find parent container
        let parentContainer;
        if (parentId !== null && parentId !== undefined) {
            const parentElement = document.querySelector(`[data-element-id="${parentId}"]`);
            if (parentElement) {
                // Check for different container content areas (regular container, modal popup, etc.)
                parentContainer = parentElement.querySelector('.pb-container-content') ||
                                parentElement.querySelector('.pb-modal-builder__inner') ||
                                parentElement.querySelector('.container-drop-zone') ||
                                parentElement;
            }
        } else {
            // Root level
            parentContainer = document.getElementById('page-elements');
        }

        if (!parentContainer) return false;

        // Create element HTML
        const elementHTML = this.createElementHTML(elementData);

        // Wrap if in container
        let fullHTML = elementHTML;
        if (parentContainer.classList.contains('pb-container-content')) {
            fullHTML = `<div class="container-child-wrapper">${elementHTML}</div>`;
        }

        // Insert at correct position
        if (afterElementId) {
            const afterElement = parentContainer.querySelector(`[data-element-id="${afterElementId}"]`);
            if (afterElement) {
                const wrapper = afterElement.closest('.container-child-wrapper') || afterElement;
                wrapper.insertAdjacentHTML('afterend', fullHTML);
            } else {
                parentContainer.insertAdjacentHTML('beforeend', fullHTML);
            }
        } else {
            parentContainer.insertAdjacentHTML('afterbegin', fullHTML);
        }

        // Setup click handlers for new element
        const newElement = parentContainer.querySelector(`[data-element-id="${elementData.id}"]`);
        if (newElement) {
            this.setupElementClickHandler(newElement);
        }

        return true;
    }

    // Order Update Methods
    async reorderPageElements(elementId, newIndex) {
        try {
            // Capture state BEFORE the move for undo
            let stateSnapshot = null;
            if (window.pageStateManager) {
                stateSnapshot = window.pageStateManager.captureState();
            }

            // Update state manager first (single source of truth)
            const moved = pageStateManager.moveElement(elementId, null, newIndex);

            if (moved) {
                // Get all page-level elements for API update
                const pageElements = document.getElementById('page-elements');
                const elements = Array.from(pageElements.querySelectorAll(':scope > .element-wrapper'));

                // Build element orders
                const elementOrders = [];
                elements.forEach((element, index) => {
                    elementOrders.push({
                        id: parseInt(element.dataset.elementId),
                        order: index
                    });
                });

                // Create and execute move command for undo/redo and API sync
                const moveCommand = new MoveElementCommand(
                    parseInt(elementId),
                    null, // old parent (page level)
                    null, // new parent (page level)
                    null, // old index will be determined
                    newIndex,
                    elementOrders
                );

                // Mark that Sortable.js already moved the DOM element
                moveCommand.domAlreadyMoved = true;

                // Store the pre-move state snapshot for undo
                moveCommand.stateSnapshot = stateSnapshot;
                // IMPORTANT: Capture DOM snapshot BEFORE the move (not after!)
                // We need to capture the DOM state before Sortable.js moved the element
                if (evt.item._preMoveSnapshot) {
                    moveCommand.beforeSnapshot = evt.item._preMoveSnapshot;
                    delete evt.item._preMoveSnapshot;
                }
                window.__suppressNextPreviewDOMUpdate = true; // Prevent double DOM update
                await historyManager.execute(moveCommand, false); // Always capture snapshots

                this.showNotification('Element reordered successfully!', 'success');
                // Structure view will be updated automatically via StateManager subscription
            } else {
                console.error('Failed to update state for page element reorder');
                this.showNotification('Failed to reorder element', 'error');
            }
        } catch (error) {
            console.error('Error reordering page elements:', error);
            this.showNotification('Failed to reorder element', 'error');
        }
    }

    updateSectionOrder(evt) {
        const sectionId = evt.item.dataset.sectionId;
        const newIndex = evt.newIndex;

        // Update order on server
        this.updateSectionOrderOnServer(sectionId, newIndex + 1);

        // Refresh structure view to reflect the new order
        if (this.structureViewVisible) {
            this._refreshStructureIfVisible();
        }
    }

    // Removed updateElementOrder - all elements now in containers, handled by updateContainerElementOrder

    async updateContainerElementOrder(evt) {
        // Get the element that was moved
        let movedWrapper = evt.item;
        let elementWrapper;
        let elementId;

        // All elements are now in containers, so they should be wrapped
        if (movedWrapper.classList.contains('container-child-wrapper')) {
            // Standard container element - already wrapped
            elementWrapper = movedWrapper.querySelector('.element-wrapper');
            if (!elementWrapper) return;
            elementId = elementWrapper.dataset.elementId;
        } else {
            console.error('Unexpected element structure in updateContainerElementOrder - all elements should be wrapped');
            return;
        }

        const oldIndex = evt.oldIndex;
        const newIndex = evt.newIndex;

        // Get the new parent container (regular container or modal popup)
        const newContainer = evt.to.closest('.element-wrapper[data-element-type="container"], .element-wrapper[data-element-type="modal_popup"]');
        const newContainerId = newContainer ? newContainer.dataset.elementId : null;

        // Get old parent container (regular container or modal popup)
        const oldContainer = evt.from.closest('.element-wrapper[data-element-type="container"], .element-wrapper[data-element-type="modal_popup"]');
        const oldContainerId = oldContainer ? oldContainer.dataset.elementId : null;

        // Check if parent changed
        const parentChanged = (oldContainerId !== newContainerId);

        try {
            // Special handling for first element moves in containers
            console.log(`🎯 Container move: old=${oldIndex}, new=${newIndex}, same container=${evt.from === evt.to}`);

            // Always check actual DOM position as Sortable sometimes misreports, especially for first element
            let correctedNewIndex = newIndex;  // Use a new variable instead of reassigning const

            // Get the actual current position in DOM after Sortable has moved it
            // Use our helper to get the correct draggable units (wrappers)
            const draggableUnits = this.getDraggableElements(evt.to);
            const actualNewIndex = draggableUnits.findIndex(unit => {
                return this.getElementIdFromDraggable(unit) === elementId;
            });

            console.log(`📍 Actual DOM position: ${actualNewIndex}, Sortable reported: ${newIndex}`);

            // Always prefer the actual index if it differs from what Sortable reported
            if (actualNewIndex !== -1) {
                if (actualNewIndex !== newIndex) {
                    console.log(`⚠️ Sortable misreported! Correcting from ${newIndex} to actual ${actualNewIndex}`);
                    correctedNewIndex = actualNewIndex;
                }

                // Check if this is actually a no-op (element didn't really move)
                if (evt.from === evt.to && actualNewIndex === oldIndex) {
                    console.log('❌ Element position unchanged, ignoring move');
                    return;
                }
            } else {
                console.error(`❌ Could not find element ${elementId} in container after move!`);
                return;
            }

            // Use the state snapshot captured BEFORE the DOM change in onStart
            let stateSnapshot = evt.item._preDropStateSnapshot || null;
            if (!stateSnapshot && window.pageStateManager) {
                // Fallback: capture current state (though DOM is already changed)
                console.warn('⚠️ No pre-move snapshot found, capturing current state');
                stateSnapshot = window.pageStateManager.captureState();
            }
            // Clean up the stored snapshot
            delete evt.item._preDropStateSnapshot;

            // Update state manager first (single source of truth) - use corrected index
            const moved = pageStateManager.moveElement(elementId, newContainerId, correctedNewIndex);

            if (moved) {
                // Get all draggable units in the new container for API update
                const draggableUnits = this.getDraggableElements(evt.to);
                const elementOrders = [];

                draggableUnits.forEach((unit, index) => {
                    const elementId = this.getElementIdFromDraggable(unit);
                    if (elementId) {
                        elementOrders.push({
                            id: parseInt(elementId),
                            order: index
                        });
                    }
                });

                // Create and execute move command for undo/redo support - use corrected index
                const moveCommand = new MoveElementCommand(
                    parseInt(elementId),
                    oldContainerId !== null && oldContainerId !== undefined ? parseInt(oldContainerId) : null,
                    newContainerId !== null && newContainerId !== undefined ? parseInt(newContainerId) : null,
                    oldIndex,
                    correctedNewIndex,  // Use corrected index here
                    elementOrders
                );

                // Mark that Sortable.js already moved the DOM element
                moveCommand.domAlreadyMoved = true;

                // Store the pre-move state snapshot for undo
                moveCommand.stateSnapshot = stateSnapshot;
                // IMPORTANT: Capture DOM snapshot BEFORE the move (not after!)
                // We need to capture the DOM state before Sortable.js moved the element
                if (evt.item._preMoveSnapshot) {
                    moveCommand.beforeSnapshot = evt.item._preMoveSnapshot;
                    delete evt.item._preMoveSnapshot;
                }
                window.__suppressNextPreviewDOMUpdate = true; // Prevent double DOM update
                await historyManager.execute(moveCommand, false); // Always capture snapshots
            } else {
                // State update failed, revert the DOM change
                console.error('Failed to update state for element move');
                evt.from.insertBefore(movedWrapper, evt.from.children[oldIndex]);
                this.showNotification('Failed to move element', 'error');
                return;
            }

            // If the element was moved to a different container, we might need to update styles
            if (oldContainerId !== newContainerId) {
                // Check if the moved element is a container with specific direction
                if (elementWrapper.dataset.elementType === 'container') {
                    const containerEl = elementWrapper.querySelector('.pb-container');
                    if (containerEl) {
                        // Update the wrapper style based on container direction
                        const content = JSON.parse(containerEl.dataset.content || '{}');
                        if (content.direction === 'column') {
                            movedWrapper.style.cssText = 'flex: 1; min-width: 200px;';
                        } else if (content.direction === 'row') {
                            movedWrapper.style.cssText = 'width: 100%;';
                        }
                    }
                }
            }

            this.showNotification('Element moved successfully', 'success');
            // Structure view will be updated automatically via StateManager subscription
        } catch (error) {
            console.error('Error updating element order:', error);
            this.showNotification('Failed to move element', 'error');

            // Revert the move on error
            if (evt.from && evt.oldIndex !== undefined) {
                evt.from.insertBefore(evt.item, evt.from.children[evt.oldIndex]);
            }
        }
    }

    async updateSectionOrderOnServer(sectionId, order) {
        try {
            await fetch(`${this.getApiBaseUrl()}/sections/${sectionId}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ order })
            });
        } catch (error) {
            console.error('Error updating section order:', error);
        }
    }

    async updateElementOrderOnServer(elementId, order) {
        try {
            await fetch(`${this.getApiBaseUrl()}/elements/${elementId}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({ order })
            });
        } catch (error) {
            console.error('Error updating element order:', error);
        }
    }

    async handleDropSection(e) {
        e.preventDefault();
        
        try {
            // Get the actual drop zone element (might be inner div, so find the parent)
            let dropZone = e.target;
            if (!dropZone.classList.contains('section-drop-zone')) {
                dropZone = dropZone.closest('.section-drop-zone');
            }
            
            if (!dropZone || !dropZone.dataset || dropZone.dataset.position === undefined) {
                console.error('Drop zone missing position data:', dropZone);
                return;
            }
            
            // Remove drag-over class from the correct element
            dropZone.classList.remove('drag-over');
            
            const position = parseInt(dropZone.dataset.position);
            const data = JSON.parse(e.dataTransfer.getData('text/plain'));
            
            if (data.type !== 'element') {
                console.error('Invalid drop data type:', data.type);
                return;
            }
            
            // Create generic section first
            const sectionData = {
                page_id: this.pageData.id,
                order: position
            };

            const sectionResponse = await fetch(`${this.getApiBaseUrl()}/sections/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(sectionData)
            });

            if (sectionResponse.ok) {
                const sectionResponseData = await sectionResponse.json();
                
                // Then add the element to the new section
                const elementData = {
                    section_id: sectionResponseData.section.id,
                    element_type: data.elementType,
                    name: `${data.elementType.charAt(0).toUpperCase() + data.elementType.slice(1)} Element`,
                    content: this.getDefaultContent(data.elementType),
                    order: 0
                };

                const elementResponse = await fetch(`${this.getApiBaseUrl()}/elements/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify(elementData)
                });

                if (elementResponse.ok) {
                    const elementData = await elementResponse.json();

                    this.showNotification('Element added successfully!', 'success');

                    // Setup click handlers for any new elements
                    this.setupElementClickHandlers();

                    // Refresh structure view first
                    this._refreshStructureIfVisible();

                    // Add a longer delay to ensure structure view completes update
                    setTimeout(() => {
                        location.reload();
                    }, 500); // Longer delay to let structure view fully update
                } else {
                    throw new Error('Failed to add element to section');
                }
            } else {
                throw new Error('Failed to create section');
            }
        } catch (error) {
            console.error('Error handling section drop:', error);
            this.showNotification('Failed to add section', 'error');
        }
    }

    async reorderSectionsAfterInsert(insertPosition) {
        try {
            const sectionsContainer = document.getElementById('page-elements');
            const sections = sectionsContainer.querySelectorAll('.section-wrapper');
            
            // Update order for sections that come after the insert position
            const updatePromises = [];
            sections.forEach((section, index) => {
                const sectionId = section.dataset.sectionId;
                if (index >= insertPosition) {
                    updatePromises.push(
                        this.updateSectionOrderOnServer(sectionId, index + 2)
                    );
                }
            });
            
            await Promise.all(updatePromises);

            // Refresh structure view after batch reorder
            if (this.structureViewVisible) {
                this._refreshStructureIfVisible();
            }
        } catch (error) {
            console.error('Error reordering sections:', error);
        }
    }

    async refreshPageSections() {
        try {
            const response = await fetch(`${this.getApiBaseUrl()}/page/${this.pageData.id}/`);
            if (response.ok) {
                const sections = await response.json();
                
                // Re-render sections in the canvas
                const sectionsContainer = document.getElementById('page-elements');
                sectionsContainer.innerHTML = '';
                
                sections.forEach(section => {
                    const sectionElement = this.createSectionElement(section);
                    sectionsContainer.appendChild(sectionElement);
                });
                
                // Re-setup sortable and drop zones
                this.setupSortable();
                this.setupSectionDropZones();
            }
        } catch (error) {
            console.error('Error refreshing sections:', error);
        }
    }

    createSectionElement(sectionData) {
        const sectionWrapper = document.createElement('div');
        sectionWrapper.className = 'section-wrapper';
        sectionWrapper.dataset.sectionId = sectionData.id;
        
        sectionWrapper.innerHTML = `
            <div class="section-controls">
                <button data-action="delete-section" data-section-id="${sectionData.id}" title="Delete Section">🗑️</button>
                <span class="drag-handle" title="Drag to reorder">⋮⋮</span>
            </div>
            <div class="section-content">
                <h3>${sectionData.title}</h3>
                <p>Type: ${sectionData.template_type}</p>
                ${sectionData.elements ? sectionData.elements.map(element => 
                    `<div class="element-preview">${element.content || element.type}</div>`
                ).join('') : ''}
            </div>
        `;
        
        return sectionWrapper;
    }

    // Structure View Methods

    /** Refresh structure view if visible, otherwise mark dirty for next open */
    _refreshStructureIfVisible() {
        if (this.structureViewVisible) {
            this.refreshStructureView();
        } else {
            this.structureViewDirty = true;
        }
    }

    initializeStructureView() {
        // Defer the expensive tree build until the panel is actually visible
        this.structureViewDirty = true;

        this.makeStructureViewDraggable();
        this.setupStructureContextMenu();
        this.setupStructureSortable();

        // Restore expanded nodes state from localStorage (needed before any refresh)
        const savedExpandedNodes = localStorage.getItem('structureExpandedNodes');
        if (savedExpandedNodes) {
            try {
                const expandedArray = JSON.parse(savedExpandedNodes);
                this.expandedNodes = new Set(expandedArray);
            } catch (e) {
                console.warn('Failed to restore expanded nodes:', e);
                this.expandedNodes = new Set();
            }
        }

        // Only build the tree if the panel was left open from a previous session
        const savedState = localStorage.getItem('structureViewVisible');
        if (savedState === 'true') {
            const structureWindow = document.getElementById('structure-view-window');
            const toggleBtn = document.getElementById('structure-toggle-btn');

            this.structureViewVisible = true;
            structureWindow.classList.remove('hidden');
            toggleBtn.classList.add('active');
            this._refreshStructureIfVisible();
            this.structureViewDirty = false;
        }
    }

    toggleStructureView() {
        const structureWindow = document.getElementById('structure-view-window');
        const toggleBtn = document.getElementById('structure-toggle-btn');

        this.structureViewVisible = !this.structureViewVisible;

        if (this.structureViewVisible) {
            structureWindow.classList.remove('hidden');
            toggleBtn.classList.add('active');
            // Build tree if it's stale
            if (this.structureViewDirty) {
                this._refreshStructureIfVisible();
                this.structureViewDirty = false;
            } else {
                this._refreshStructureIfVisible();
            }
            // Save state to localStorage
            localStorage.setItem('structureViewVisible', 'true');
        } else {
            structureWindow.classList.add('hidden');
            toggleBtn.classList.remove('active');
            // Save state to localStorage
            localStorage.setItem('structureViewVisible', 'false');
        }
    }

    refreshStructureView() {
        const structureTree = document.getElementById('structure-tree');
        const elementCount = document.getElementById('structure-element-count');

        if (!structureTree) return;

        // Save the scroll position before refresh
        const scrollTop = structureTree.parentElement ? structureTree.parentElement.scrollTop : 0;

        // Get page structure from StateManager if available, otherwise from DOM
        const pageStructure = window.pageStateManager ?
            this.buildPageStructureFromState() :
            this.buildPageStructure();

        // Render structure tree (skip the page node, start with its children)
        let html = '';
        if (pageStructure.children) {
            pageStructure.children.forEach(child => {
                html += this.renderStructureNode(child, 0);
            });
        }
        structureTree.innerHTML = html;

        // Update element count
        const totalElements = this.countTotalElements(pageStructure);
        elementCount.textContent = `${totalElements} elements`;

        // Setup event handlers for structure items
        this.setupStructureEventHandlers();

        // Initialize sortable for the new structure
        this.initializeStructureSortables();

        // Restore scroll position
        if (structureTree.parentElement && scrollTop > 0) {
            structureTree.parentElement.scrollTop = scrollTop;
        }
    }

    buildPageStructureFromState() {
        const structure = {
            type: 'page',
            name: this.pageData.title || 'Page',
            id: 'page',
            children: []
        };

        if (!window.pageStateManager) {
            return this.buildPageStructure();
        }

        const state = window.pageStateManager.getState();
        if (!state || !state.structure) {
            return this.buildPageStructure();
        }

        // Build structure from state
        const buildNode = (elementId) => {
            const element = state.elements[elementId];
            if (!element) return null;

            const node = {
                type: element.type,
                name: this.getElementNameFromState(element),
                id: elementId,
                children: []
            };

            // Add children recursively
            if (element.children && element.children.length > 0) {
                element.children.forEach(childId => {
                    const childNode = buildNode(childId);
                    if (childNode) {
                        node.children.push(childNode);
                    }
                });
            }

            return node;
        };

        // Build from root structure
        state.structure.forEach(rootId => {
            const rootNode = buildNode(rootId);
            if (rootNode) {
                structure.children.push(rootNode);
            }
        });

        return structure;
    }

    getElementNameFromState(element) {
        // Extract display name from element state
        if (element.type === 'container') {
            return element.name || `Container #${element.id}`;
        } else if (element.type === 'text' || element.type === 'heading') {
            // Extract text preview - content might be an object with text/html properties or a string
            let textContent = '';
            if (typeof element.content === 'object' && element.content) {
                textContent = element.content.text || element.content.html || '';
            } else if (typeof element.content === 'string') {
                textContent = element.content;
            }

            // If still no content, try to extract from HTML
            if (!textContent && element.content?.html) {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = element.content.html;
                textContent = tempDiv.textContent || '';
            }

            // Clean up and truncate
            textContent = textContent.trim();
            if (textContent) {
                return textContent.substring(0, 50) + (textContent.length > 50 ? '...' : '');
            }
            return `${element.type} #${element.id}`;
        } else if (element.type === 'image') {
            return element.alt || element.title || `Image #${element.id}`;
        } else if (element.type === 'button') {
            // Button content might also be an object
            let buttonText = '';
            if (typeof element.content === 'object' && element.content) {
                buttonText = element.content.text || element.content.html || '';
            } else if (typeof element.content === 'string') {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = element.content;
                buttonText = tempDiv.textContent || '';
            }
            return buttonText || `Button #${element.id}`;
        } else if (element.type === 'html') {
            return `HTML Block #${element.id}`;
        } else if (element.type === 'video') {
            return element.title || `Video #${element.id}`;
        } else {
            return `${element.type} #${element.id}`;
        }
    }

    buildPageStructure() {
        const structure = {
            type: 'page',
            name: this.pageData.title || 'Page',
            id: 'page',
            children: []
        };

        // First, get direct page elements (new structure without sections)
        const pageElements = document.querySelector('#page-elements');
        if (pageElements) {
            const directElements = pageElements.querySelectorAll(':scope > .element-wrapper');
            directElements.forEach(elementEl => {
                const elementData = this.extractElementData(elementEl);
                if (elementData) {
                    structure.children.push(elementData);
                }
            });
        }

        // Then, get legacy sections if they exist (for backwards compatibility)
        const sections = document.querySelectorAll('.section-wrapper');
        sections.forEach(sectionEl => {
            const sectionId = sectionEl.dataset.sectionId;
            const sectionName = sectionEl.querySelector('h4')?.textContent || `Section ${sectionId}`;

            const section = {
                type: 'section',
                name: sectionName,
                id: sectionId,
                children: []
            };

            // Sections now have a default container - find it
            // Look for the section's container (marked with is_section_container)
            const sectionContainer = sectionEl.querySelector('.element-wrapper[data-element-type="container"]');
            if (sectionContainer) {
                // Add the container's children to the section
                const containerData = this.extractElementData(sectionContainer);
                if (containerData && containerData.children) {
                    // Add container's children directly to section for cleaner view
                    section.children = containerData.children;
                }
            }

            structure.children.push(section);
        });

        return structure;
    }

    extractElementData(elementEl) {
        const elementId = elementEl.dataset.elementId;
        const elementType = elementEl.dataset.elementType;

        if (!elementId || !elementType) return null;

        const elementName = this.getElementDisplayName(elementEl, elementType);

        const elementData = {
            type: elementType,
            name: elementName,
            id: elementId,
            children: []
        };

        // For containers, get DIRECT child elements only
        if (elementType === 'container') {
            const containerContent = elementEl.querySelector('.pb-container-content');
            if (containerContent) {
                // Get direct children - they might be in container-child-wrapper or directly as element-wrapper
                const directChildren = containerContent.querySelectorAll(':scope > .container-child-wrapper, :scope > .element-wrapper');
                directChildren.forEach(child => {
                    let childEl = child;
                    // If it's a wrapper, get the element inside
                    if (child.classList.contains('container-child-wrapper')) {
                        childEl = child.querySelector(':scope > .element-wrapper');
                    }
                    // Only process if it's an element-wrapper
                    if (childEl && childEl.classList.contains('element-wrapper')) {
                        const childData = this.extractElementData(childEl);
                        if (childData) {
                            elementData.children.push(childData);
                        }
                    }
                });
            }
        }

        return elementData;
    }

    getElementDisplayName(elementEl, elementType) {
        let name = `${elementType.charAt(0).toUpperCase() + elementType.slice(1)}`;

        // Try to get more specific names based on content
        try {
            switch (elementType) {
                case 'text':
                case 'heading':
                    const textContent = elementEl.querySelector('.text-element, h1, h2, h3, h4, h5, h6, p')?.textContent?.trim();
                    if (textContent && textContent.length > 0) {
                        name = textContent.length > 30 ? textContent.substring(0, 30) + '...' : textContent;
                    }
                    break;
                case 'button':
                    const buttonText = elementEl.querySelector('button, .btn')?.textContent?.trim();
                    if (buttonText) {
                        name = buttonText;
                    }
                    break;
                case 'image':
                    const img = elementEl.querySelector('img');
                    if (img?.alt) {
                        name = img.alt;
                    }
                    break;
                case 'container':
                    const childCount = elementEl.querySelectorAll('.container-child-wrapper .element-wrapper').length;
                    name = `Container (${childCount} items)`;
                    break;
            }
        } catch (e) {
            // Fallback to default name
            console.warn('Error getting element name:', e);
        }

        return name;
    }

    renderStructureNode(node, level = 0) {
        const hasChildren = node.children && node.children.length > 0;
        const isContainer = node.type === 'container' || node.type === 'section';
        const isExpanded = this.expandedNodes.has(node.id);
        const indent = level * 16;

        let html = `
            <div class="structure-node" data-element-id="${node.id}" data-level="${level}" data-node-type="${node.type}">
                <div class="structure-item" data-element-id="${node.id}" data-node-type="${node.type}">
                    <button class="structure-expand-btn ${(hasChildren || isContainer) ? (isExpanded ? 'expanded' : '') : 'hidden'}"
                            data-node-id="${node.id}">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                    <div class="structure-element-icon ${node.type}">
                        ${this.getElementIcon(node.type)}
                    </div>
                    <div class="structure-element-details">
                        <div class="structure-element-name">${node.name}</div>
                        <div class="structure-element-type">${node.type}</div>
                    </div>
                </div>
        `;

        // For containers and sections, always render a children container (even if empty)
        if (isContainer) {
            html += `<div class="structure-children ${isExpanded ? 'expanded' : ''}">`;

            if (hasChildren) {
                node.children.forEach(child => {
                    html += this.renderStructureNode(child, level + 1);
                });
            } else {
                // Add placeholder for empty containers/sections
                html += `
                    <div class="structure-empty-placeholder" data-parent-id="${node.id}" data-parent-type="${node.type}" data-level="${level + 1}" style="cursor: pointer;">
                        <i class="fas fa-plus-circle"></i>
                        <span>Drop elements here or click to add</span>
                    </div>
                `;
            }

            html += '</div>';
        } else if (hasChildren) {
            // Non-container elements with children
            html += `<div class="structure-children ${isExpanded ? 'expanded' : ''}">`;
            node.children.forEach(child => {
                html += this.renderStructureNode(child, level + 1);
            });
            html += '</div>';
        }

        html += '</div>';
        return html;
    }

    getElementIcon(type) {
        // Structural types (not in element registry)
        if (type === 'page') return '<i class="fas fa-file"></i>';
        if (type === 'section') return '<i class="fas fa-layer-group"></i>';
        // Data-driven from config.json via window.elementMetadata
        if (window.elementMetadata && window.elementMetadata[type]) {
            return `<i class="${window.elementMetadata[type].icon}"></i>`;
        }
        return '<i class="fas fa-puzzle-piece"></i>';
    }

    toggleStructureNode(nodeId) {
        // Prevent toggling during drag operations
        if (this.isDragging) return;

        if (this.expandedNodes.has(nodeId)) {
            this.expandedNodes.delete(nodeId);
        } else {
            this.expandedNodes.add(nodeId);
        }

        // Save expanded nodes to localStorage
        localStorage.setItem('structureExpandedNodes', JSON.stringify([...this.expandedNodes]));

        this._refreshStructureIfVisible();
    }

    expandAllStructureNodes() {
        const allNodes = document.querySelectorAll('.structure-node[data-element-id]');
        allNodes.forEach(node => {
            const nodeId = node.dataset.elementId;
            const hasChildren = node.querySelector('.structure-children');
            if (hasChildren) {
                this.expandedNodes.add(nodeId);
            }
        });

        // Save expanded nodes to localStorage
        localStorage.setItem('structureExpandedNodes', JSON.stringify([...this.expandedNodes]));

        this._refreshStructureIfVisible();
    }

    collapseAllStructureNodes() {
        this.expandedNodes.clear();

        // Save expanded nodes to localStorage
        localStorage.setItem('structureExpandedNodes', JSON.stringify([]));

        this._refreshStructureIfVisible();
    }

    setupStructureEventHandlers() {
        // Setup expand/collapse button handlers
        const expandButtons = document.querySelectorAll('.structure-expand-btn');
        expandButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const nodeId = btn.dataset.nodeId;
                if (nodeId) {
                    this.toggleStructureNode(nodeId);
                }
            });
        });

        const structureItems = document.querySelectorAll('.structure-item');
        let isDragging = false;

        structureItems.forEach(item => {
            // Remove existing listeners
            item.removeEventListener('click', this.handleStructureItemClick);

            // Track drag state
            item.addEventListener('mousedown', () => {
                isDragging = false;
            });

            item.addEventListener('mousemove', () => {
                isDragging = true;
            });

            // Add click listener for selection (only if not dragging)
            item.addEventListener('click', (e) => {
                // Don't trigger if clicking on expand button or if dragging
                if (e.target.closest('.structure-expand-btn') || isDragging) return;

                this.handleStructureItemClick(e, item);
            });

            // Add right-click listener for context menu
            item.addEventListener('contextmenu', (e) => {
                // Don't trigger if clicking on expand button
                if (e.target.closest('.structure-expand-btn')) return;

                const elementId = item.dataset.elementId;
                const nodeType = item.dataset.nodeType;

                // Only show context menu for actual elements (not page or sections)
                // Check if it's an actual element by excluding page and section types
                if (elementId && nodeType !== 'page' && nodeType !== 'section') {
                    this.showContextMenu(e, elementId);
                }
            });
        });

        // Add click handlers for empty placeholders
        const emptyPlaceholders = document.querySelectorAll('.structure-empty-placeholder');
        emptyPlaceholders.forEach(placeholder => {
            placeholder.addEventListener('click', (e) => {
                e.stopPropagation();
                const parentId = placeholder.dataset.parentId;
                const parentType = placeholder.dataset.parentType;

                if (parentType === 'container') {
                    this.showQuickAddMenu(e, 'container', parentId);
                } else if (parentType === 'section') {
                    this.showQuickAddMenu(e, 'section', parentId);
                }
            });
        });
    }

    handleStructureItemClick(event, item) {
        event.stopPropagation();

        const elementId = item.dataset.elementId;

        // Update selection in structure view
        document.querySelectorAll('.structure-item.selected').forEach(el => {
            el.classList.remove('selected');
        });
        item.classList.add('selected');

        // Select element in main builder view
        if (elementId !== 'page') {
            const builderElement = document.querySelector(`[data-element-id="${elementId}"]`);
            if (builderElement) {
                // Clear previous selections
                document.querySelectorAll('.element-wrapper.selected').forEach(el => {
                    el.classList.remove('selected');
                });

                // Select new element
                builderElement.classList.add('selected');
                this.selectedElement = builderElement;

                // Scroll into view
                builderElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });

                // Show properties if needed
                const elementType = builderElement.dataset.elementType;
                if (elementType) {
                    this.showElementProperties(builderElement, elementId, elementType);
                }
            }
        }
    }

    // Update structure view when element is selected in builder
    syncStructureSelection(elementId) {
        if (!this.structureViewVisible) return;

        // Clear previous selections
        document.querySelectorAll('.structure-item.selected').forEach(el => {
            el.classList.remove('selected');
        });

        // Select in structure view
        const structureItem = document.querySelector(`.structure-item[data-element-id="${elementId}"]`);
        if (structureItem) {
            structureItem.classList.add('selected');

            // Scroll into view in structure panel
            structureItem.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest'
            });
        }
    }

    countTotalElements(node) {
        let count = node.type !== 'page' ? 1 : 0;
        if (node.children) {
            node.children.forEach(child => {
                count += this.countTotalElements(child);
            });
        }
        return count;
    }

    makeStructureViewDraggable() {
        const structureWindow = document.getElementById('structure-view-window');
        const header = structureWindow.querySelector('.structure-header');

        let isDragging = false;
        let currentX = 0;
        let currentY = 0;
        let initialX = 0;
        let initialY = 0;

        header.addEventListener('mousedown', (e) => {
            isDragging = true;
            initialX = e.clientX - currentX;
            initialY = e.clientY - currentY;

            document.addEventListener('mousemove', drag);
            document.addEventListener('mouseup', stopDrag);
        });

        function drag(e) {
            if (!isDragging) return;

            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            structureWindow.style.transform = `translate(${currentX}px, ${currentY}px)`;
        }

        function stopDrag() {
            isDragging = false;
            document.removeEventListener('mousemove', drag);
            document.removeEventListener('mouseup', stopDrag);
        }
    }

    // Setup sortable for structure view elements
    setupStructureSortable() {
        // Initialize the sortables array if it doesn't exist
        if (!this.structureSortables) {
            this.structureSortables = [];
        }
    }

    initializeStructureSortables() {
        // Initialize array if it doesn't exist
        if (!this.structureSortables) {
            this.structureSortables = [];
        }

        // Clean up existing sortables with better error handling
        if (this.structureSortables.length > 0) {
            this.structureSortables.forEach(sortable => {
                try {
                    // Check if sortable is valid and has an element reference
                    if (sortable && sortable.destroy && sortable.el) {
                        // Additional check to ensure the element is still in the DOM
                        if (document.body.contains(sortable.el)) {
                            sortable.destroy();
                        }
                    }
                } catch (error) {
                    // Only log if it's not the expected null reference error
                    if (!error.message?.includes("can't access property")) {
                        console.warn('Error destroying structure sortable:', error);
                    }
                }
            });
            this.structureSortables = [];
        }

        // Check if Sortable is available
        if (typeof Sortable === 'undefined') {
            console.error('Sortable.js is not loaded');
            return;
        }

        // Find all structure-children containers (including sections)
        const structureTree = document.getElementById('structure-tree');
        if (!structureTree) return;

        console.log('Initializing structure sortables...');

        // Make the root level sortable for both direct page elements and sections
        try {
            const rootSortable = new Sortable(structureTree, {
                animation: 150,
                draggable: '.structure-node[data-level="0"]',  // All top-level items (elements and sections)
                handle: '.structure-item',  // Use simple handle
                ghostClass: 'structure-item-ghost',
                chosenClass: 'structure-item-chosen',
                dragClass: 'structure-item-drag',
                forceFallback: false,  // Use native HTML5 drag
                onStart: (evt) => {
                    console.log('Top-level drag started:', evt.item.dataset.elementId);
                    this.isDragging = true;
                    evt.item.classList.add('dragging-element');
                    // Hide children while dragging
                    const childrenContainer = evt.item.querySelector('.structure-children');
                    if (childrenContainer) {
                        childrenContainer.style.display = 'none';
                    }
                },
                onEnd: (evt) => {
                    console.log('Top-level drag ended:', evt.item.dataset.elementId);
                    this.isDragging = false;
                    evt.item.classList.remove('dragging-element');
                    // Show children after dragging
                    const childrenContainer = evt.item.querySelector('.structure-children');
                    if (childrenContainer) {
                        childrenContainer.style.display = '';
                    }
                    const nodeType = evt.item.dataset.nodeType;
                    // For root level, parent is null (will be handled as page-elements)
                    this.handleStructureReorder(evt, nodeType === 'section' ? 'section' : 'element', null);
                }
            });
            this.structureSortables.push(rootSortable);
            console.log('Root sortable created for top-level items');
        } catch (error) {
            console.error('Failed to create root sortable:', error);
        }

        // Make each section's children container sortable for elements
        const sectionContainers = structureTree.querySelectorAll('.structure-node[data-node-type="section"] > .structure-children');
        console.log('Found section containers:', sectionContainers.length);

        sectionContainers.forEach((container, index) => {
            // Initialize sortable even for empty containers (they have placeholder)
            const parentNode = container.closest('.structure-node');
            const sectionId = parentNode.dataset.elementId;

            try {
                const sortable = new Sortable(container, {
                    group: 'structure-elements',
                    animation: 150,
                    draggable: '.structure-node[data-level="1"]',  // Only level 1 nodes
                    handle: '.structure-item',  // Simple handle selector
                    filter: '.structure-empty-placeholder',  // Don't drag placeholders
                    ghostClass: 'structure-item-ghost',
                    chosenClass: 'structure-item-chosen',
                    onMove: (evt) => {
                        // Prevent invalid moves
                        const draggedEl = evt.dragged;
                        const relatedEl = evt.related;

                        // Don't allow dropping on placeholders
                        if (relatedEl && relatedEl.classList.contains('structure-empty-placeholder')) {
                            return true; // Allow - placeholder is valid drop target
                        }

                        // Prevent dropping elements on themselves
                        if (draggedEl === relatedEl) {
                            return false;
                        }

                        return true; // Allow the move
                    },
                        onStart: (evt) => {
                            console.log('Element drag started:', evt.item.dataset.elementId);
                            this.isDragging = true;
                            evt.item.classList.add('dragging-element');
                            // Hide children while dragging
                            const childrenContainer = evt.item.querySelector('.structure-children');
                            if (childrenContainer) {
                                childrenContainer.style.display = 'none';
                            }
                        },
                        onEnd: (evt) => {
                            console.log('Element drag ended:', evt.item.dataset.elementId);
                            this.isDragging = false;
                            evt.item.classList.remove('dragging-element');
                            // Show children again after dragging
                            const childrenContainer = evt.item.querySelector('.structure-children');
                            if (childrenContainer) {
                                childrenContainer.style.display = '';
                            }
                            this.handleStructureReorder(evt, 'element', sectionId);
                        }
                    });
                    this.structureSortables.push(sortable);
                    console.log(`Section ${index} sortable created with ${container.children.length} elements`);
                } catch (error) {
                    console.error(`Failed to create sortable for section ${index}:`, error);
                }
        });

        // Make all structure-children containers sortable (containers and page root)
        const allChildrenContainers = structureTree.querySelectorAll('.structure-children');
        console.log('Found all children containers:', allChildrenContainers.length);

        allChildrenContainers.forEach((container, index) => {
            // Initialize sortable even for empty containers (they have placeholder)
            const parentNode = container.closest('.structure-node');
            if (!parentNode) return; // Skip if no parent node

            const containerId = parentNode.dataset.elementId;
            const parentLevel = parseInt(parentNode.dataset.level) || 0;

            try {
                const sortable = new Sortable(container, {
                    group: 'structure-elements',  // Use same group for cross-container dragging
                    animation: 150,
                    draggable: `.structure-node[data-level="${parentLevel + 1}"]`,  // Only direct children at correct level
                    handle: '.structure-item',
                    filter: '.structure-empty-placeholder',  // Don't drag placeholders
                    ghostClass: 'structure-item-ghost',
                    chosenClass: 'structure-item-chosen',
                    dragClass: 'structure-item-drag',
                    forceFallback: false,
                    onMove: (evt) => {
                        // Prevent invalid moves
                        const draggedEl = evt.dragged;
                        const relatedEl = evt.related;

                        // Don't allow dropping on placeholders
                        if (relatedEl && relatedEl.classList.contains('structure-empty-placeholder')) {
                            return true; // Allow - placeholder is valid drop target
                        }

                        // Prevent dropping elements on themselves or their children
                        if (draggedEl === relatedEl || draggedEl.contains(relatedEl)) {
                            return false;
                        }

                        return true; // Allow the move
                    },
                        onStart: (evt) => {
                            console.log('Container element drag started:', evt.item.dataset.elementId);
                            this.isDragging = true;
                            evt.item.classList.add('dragging-element');
                            // Capture state BEFORE any DOM changes for undo
                            if (window.pageStateManager) {
                                evt.item._preDropStateSnapshot = window.pageStateManager.captureState();
                                console.log('📸 Captured pre-move state snapshot (structure view)');
                            }
                            // Also capture DOM snapshot before the move
                            if (window.historyManager && window.historyManager.domSnapshot) {
                                evt.item._preMoveSnapshot = window.historyManager.domSnapshot.capture();
                                console.log('📸 Captured pre-move DOM snapshot (structure view)');
                            }
                            // Hide children while dragging
                            const childrenContainer = evt.item.querySelector('.structure-children');
                            if (childrenContainer) {
                                childrenContainer.style.display = 'none';
                            }
                        },
                        onEnd: (evt) => {
                            console.log('Container element drag ended:', evt.item.dataset.elementId);
                            this.isDragging = false;
                            evt.item.classList.remove('dragging-element');
                            // Show children again after dragging
                            const childrenContainer = evt.item.querySelector('.structure-children');
                            if (childrenContainer) {
                                childrenContainer.style.display = '';
                            }
                            this.handleStructureReorder(evt, 'container-element', containerId);
                        }
                    });
                    this.structureSortables.push(sortable);
                    console.log(`Container ${index} sortable created for level ${parentLevel + 1} with ${container.children.length} elements`);
                } catch (error) {
                    console.error(`Failed to create sortable for container ${index}:`, error);
                }
        });
    }

    syncPreviewFromStructure(elementId, parentId, newIndex, actualParentId = null) {
        // Find the element in the preview
        const element = document.querySelector(`.element-wrapper[data-element-id="${elementId}"]`);
        if (!element) {
            console.error(`Element ${elementId} not found in preview`);
            return;
        }

        // Determine the target container
        let targetContainer = null;
        const targetParentId = actualParentId || parentId;

        if (targetParentId && targetParentId !== 'page') {
            // Find the container element
            const parentElement = document.querySelector(`.element-wrapper[data-element-id="${targetParentId}"]`);
            if (parentElement) {
                // Look for container content area inside the parent (regular container, modal popup, etc.)
                targetContainer = parentElement.querySelector('.pb-container-content') ||
                                  parentElement.querySelector('.pb-modal-builder__inner');
                if (!targetContainer) {
                    console.warn(`Container content not found for parent ${targetParentId}`);
                    targetContainer = parentElement;
                }
            } else {
                console.warn(`Parent element ${targetParentId} not found, using root level`);
                // Try multiple possible root containers
                targetContainer = document.getElementById('page-elements') ||
                                document.getElementById('page-elements') ||
                                document.querySelector('.preview-content');
            }
        } else {
            // Root level - try multiple possible root containers
            targetContainer = document.getElementById('page-elements') ||
                            document.getElementById('page-elements') ||
                            document.querySelector('.preview-content');

            if (!targetContainer) {
                console.error('No root container found. Looking for alternatives...');
                // Try to find any container that has element-wrappers as children
                const possibleContainers = document.querySelectorAll('.element-wrapper');
                if (possibleContainers.length > 0) {
                    targetContainer = possibleContainers[0].parentElement;
                    console.log('Using parent of first element as root container:', targetContainer);
                }
            }
        }

        if (!targetContainer) {
            console.error(`Target container not found. Available IDs:`,
                         Array.from(document.querySelectorAll('[id]')).map(el => el.id).filter(id => id.includes('page')));
            return;
        }

        // The actual DOM manipulation is handled by MoveElementCommand
        // This method now only serves to verify elements exist and reinitialize sortables
        // after the move has been completed by the command

        // Just reinitialize sortables to ensure drag-drop continues to work properly
        this.initializePreviewSortables();
    }

    async handleStructureReorder(evt, type, parentId = null) {
        const itemEl = evt.item;
        const elementId = itemEl.dataset.elementId;
        const oldIndex = evt.oldIndex;
        const newIndex = evt.newIndex;

        // Don't do anything if position hasn't changed
        if (oldIndex === newIndex && evt.from === evt.to) return;

        console.log(`🔧 STRUCTURE REORDER EVENT:`, {
            elementId: elementId,
            type: type,
            sortableOldIndex: oldIndex,
            sortableNewIndex: newIndex,
            fromContainer: evt.from.className,
            toContainer: evt.to.className,
            sameContainer: evt.from === evt.to
        });

        try {
            if (type === 'section') {
                // Get all sections and build new order
                const sections = evt.to.querySelectorAll('.structure-node[data-node-type="section"]');
                const sectionOrders = [];

                sections.forEach((section, index) => {
                    sectionOrders.push({
                        id: parseInt(section.dataset.elementId),
                        order: index + 1
                    });
                });

                const response = await fetch(`${this.getApiBaseUrl()}/reorder-sections/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify({ section_orders: sectionOrders })
                });

                if (response.ok) {
                    this.showNotification('Sections reordered successfully!', 'success');

                    // Update the DOM without reloading
                    // Move the actual section in the builder view
                    const sectionsContainer = document.getElementById('page-elements');
                    const sectionToMove = document.querySelector(`.section-wrapper[data-section-id="${elementId}"]`);

                    if (sectionToMove && sectionsContainer) {
                        // Get all sections
                        const allSections = Array.from(sectionsContainer.querySelectorAll('.section-wrapper'));

                        // Remove the section from DOM
                        sectionToMove.remove();

                        // Insert at new position
                        if (newIndex === 0) {
                            sectionsContainer.insertBefore(sectionToMove, sectionsContainer.firstChild);
                        } else if (newIndex >= allSections.length - 1) {
                            sectionsContainer.appendChild(sectionToMove);
                        } else {
                            const referenceSection = allSections[newIndex];
                            if (oldIndex < newIndex) {
                                referenceSection.insertAdjacentElement('afterend', sectionToMove);
                            } else {
                                referenceSection.insertAdjacentElement('beforebegin', sectionToMove);
                            }
                        }
                    }

                    // Structure view is already updated visually by Sortable
                } else {
                    throw new Error('Failed to reorder sections');
                }
            } else if (type === 'element' || type === 'container-element') {
                // Determine the old parent for tracking
                let oldParentId = null;
                if (evt.from.id === 'structure-tree') {
                    oldParentId = null;
                } else {
                    const oldParentNode = evt.from.parentElement;
                    if (oldParentNode && oldParentNode.classList.contains('structure-node')) {
                        oldParentId = oldParentNode.dataset.elementId;
                    }
                }

                // Determine the new parent container (if element moved between containers)
                let newParentId = null;

                // evt.to is either structure-tree (root) or .structure-children container
                if (evt.to.id === 'structure-tree') {
                    // Root level - no parent
                    newParentId = null;
                    console.log('Moving to root level');
                } else {
                    // evt.to is the .structure-children container that received the element
                    const newParentNode = evt.to.parentElement;
                    if (newParentNode && newParentNode.classList.contains('structure-node')) {
                        newParentId = newParentNode.dataset.elementId;
                        console.log(`Moving to parent ${newParentId}`);
                    }
                }

                // Debug: Log the exact indices from Sortable
                console.log(`🔍 STRUCTURE MOVE DEBUG:`, {
                    elementId,
                    oldIndex: evt.oldIndex,
                    newIndex: evt.newIndex,
                    from: evt.from.id || evt.from.className,
                    to: evt.to.id || evt.to.className,
                    isSameContainer: evt.from === evt.to
                });

                // Always check actual DOM position as Sortable sometimes misreports
                let correctedNewIndex = newIndex;

                // Get the actual position in DOM after Sortable has moved it
                // In structure view, we're moving .structure-node elements
                const allNodes = Array.from(evt.to.querySelectorAll(':scope > .structure-node'));
                const actualPosition = allNodes.findIndex(node =>
                    node.dataset.elementId === elementId
                );

                console.log(`📍 Actual DOM position: ${actualPosition}, Sortable reported: ${newIndex}`);

                // Always prefer the actual index if it differs from what Sortable reported
                if (actualPosition !== -1) {
                    if (actualPosition !== newIndex) {
                        console.log(`⚠️ Sortable misreported! Correcting from ${newIndex} to actual ${actualPosition}`);
                        correctedNewIndex = actualPosition;
                    }

                    // Check if this is actually a no-op (element didn't really move)
                    if (evt.from === evt.to && actualPosition === oldIndex) {
                        console.log('❌ Element position unchanged in structure view, ignoring move');
                        return;
                    }
                } else {
                    console.error(`❌ Could not find element ${elementId} in structure after move!`);
                    return;
                }

                // Use the state snapshot captured BEFORE the DOM change in onStart
                let stateSnapshot = evt.item._preDropStateSnapshot || null;
                if (!stateSnapshot && window.pageStateManager) {
                    // Fallback: capture current state (though DOM is already changed)
                    console.warn('⚠️ No pre-move snapshot found, capturing current state (structure)');
                    stateSnapshot = window.pageStateManager.captureState();
                }
                // Clean up the stored snapshot
                delete evt.item._preDropStateSnapshot;

                // First update StateManager with the corrected index
                console.log(`📤 Calling StateManager.moveElement(${elementId}, ${newParentId}, ${correctedNewIndex})`);
                const moved = pageStateManager.moveElement(elementId, newParentId, correctedNewIndex);
                console.log(`📥 StateManager.moveElement returned: ${moved}`);

                // Force debug panel update if visible
                if (moved && window.debugPanel && window.debugPanel.isVisible) {
                    console.log('🔄 Forcing debug panel update');
                    window.debugPanel.updatePanel(
                        { type: 'ELEMENT_MOVED', elementId, oldParentId, newParentId, newIndex },
                        pageStateManager.getState()
                    );
                }

                // Verify the actual position in state
                if (moved) {
                    const element = pageStateManager.getElement(elementId);
                    const children = newParentId ?
                        pageStateManager.getElement(newParentId)?.children :
                        pageStateManager.state.structure;
                    const actualIndex = children ? children.indexOf(elementId) : -1;
                    console.log(`🔍 VERIFICATION: Element ${elementId} is at index ${actualIndex} in parent ${newParentId || 'root'}`);
                    if (actualIndex !== correctedNewIndex) {
                        console.warn(`⚠️ INDEX MISMATCH: Expected ${correctedNewIndex}, got ${actualIndex}`);
                    }
                }

                if (moved) {
                    // Get all elements in the new container for API sync
                    const elements = evt.to.querySelectorAll(':scope > .structure-node');
                    const elementOrders = [];

                    elements.forEach((element, index) => {
                        elementOrders.push({
                            id: parseInt(element.dataset.elementId),
                            order: index
                        });
                    });

                    // Determine actual parent for API (handle section->container mapping)
                    let actualParentId = newParentId;
                    if (newParentId) {
                        const parentNode = document.querySelector(`.structure-node[data-element-id="${newParentId}"]`);
                        if (parentNode && parentNode.dataset.nodeType === 'section') {
                            // Find the section's default container
                            const sectionEl = document.querySelector(`.section-wrapper[data-section-id="${newParentId}"]`);
                            if (sectionEl) {
                                const container = sectionEl.querySelector('.element-wrapper[data-element-type="container"]');
                                if (container) {
                                    actualParentId = container.dataset.elementId;
                                }
                            }
                        }
                    }

                    // Create and execute move command for API sync - use corrected index
                    const moveCommand = new MoveElementCommand(
                        parseInt(elementId),
                        null, // Old parent will be determined by command
                        actualParentId !== null && actualParentId !== undefined ? parseInt(actualParentId) : null,
                        oldIndex,
                        correctedNewIndex,  // Use the corrected index here
                        elementOrders
                    );

                    // Mark that DOM is already updated by StateManager
                    moveCommand.domAlreadyMoved = true;

                    // Store the pre-move state snapshot for undo
                    moveCommand.stateSnapshot = stateSnapshot;

                    console.log('Executing move command for API sync...');
                    try {
                        // Execute command for API sync
                        window.__suppressNextPreviewDOMUpdate = true; // Prevent double DOM update
                        await historyManager.execute(moveCommand, false); // Always capture snapshots
                        console.log('Move command executed successfully');
                        this.showNotification('Elements reordered successfully!', 'success');
                    } catch (cmdError) {
                        console.error('Move command failed:', cmdError);
                        throw cmdError;
                    }
                } else {
                    throw new Error('Failed to update element order in state');
                }
            }
        } catch (error) {
            console.error('Error reordering:', error);
            this.showNotification('Failed to update order', 'error');

            // Safely revert the move by refreshing the structure view
            // This avoids DOM manipulation errors
            setTimeout(() => {
                this._refreshStructureIfVisible();
            }, 100);
        }
    }

    // Context Menu Methods
    setupStructureContextMenu() {
        this.contextMenu = document.getElementById('structure-context-menu');
        this.contextMenuTarget = null;
        this.copiedStyle = null;

        // Hide context menu when clicking elsewhere
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#structure-context-menu')) {
                this.hideContextMenu();
            }
        });

        // Handle context menu item clicks
        this.contextMenu.addEventListener('click', (e) => {
            const item = e.target.closest('.context-menu-item');
            if (item && !item.classList.contains('disabled')) {
                const action = item.dataset.action;
                this.handleContextMenuAction(action);
                this.hideContextMenu();
            }
        });
    }

    showContextMenu(e, elementId) {
        e.preventDefault();
        e.stopPropagation();

        this.contextMenuTarget = elementId;

        // Update paste style item state
        const pasteStyleItem = document.getElementById('paste-style-item');
        if (this.copiedStyle) {
            pasteStyleItem.classList.remove('disabled');
        } else {
            pasteStyleItem.classList.add('disabled');
        }

        // Position and show context menu
        this.contextMenu.style.left = e.pageX + 'px';
        this.contextMenu.style.top = e.pageY + 'px';
        this.contextMenu.classList.remove('hidden');

        // Adjust position if menu goes off screen
        const rect = this.contextMenu.getBoundingClientRect();
        if (rect.right > window.innerWidth) {
            this.contextMenu.style.left = (e.pageX - rect.width) + 'px';
        }
        if (rect.bottom > window.innerHeight) {
            this.contextMenu.style.top = (e.pageY - rect.height) + 'px';
        }
    }

    hideContextMenu() {
        this.contextMenu.classList.add('hidden');
        this.contextMenuTarget = null;
    }

    async handleContextMenuAction(action) {
        if (!this.contextMenuTarget) return;

        const elementId = this.contextMenuTarget;

        switch (action) {
            case 'edit':
                await this.editElement(elementId);
                break;
            case 'add-same':
                await this.addSameElement(elementId);
                break;
            case 'duplicate':
                await this.duplicateElement(elementId);
                break;
            case 'reset-style':
                await this.resetElementStyle(elementId);
                break;
            case 'copy-style':
                this.copyElementStyle(elementId);
                break;
            case 'paste-style':
                if (this.copiedStyle) {
                    await this.pasteElementStyle(elementId);
                }
                break;
            case 'delete':
                await this.deleteElementWithConfirm(elementId);
                break;
        }
    }

    async editElement(elementId) {
        // Select the element and show properties
        this.selectStructureElement(elementId);
        // Trigger edit mode similar to clicking the element
        const elementWrapper = document.querySelector(`[data-element-id="${elementId}"]`);
        if (elementWrapper) {
            editElement(elementId, null);
        }
    }

    async addSameElement(elementId) {
        try {
            // Get element data to find its type
            const response = await fetch(`${this.getApiBaseUrl()}/elements/${elementId}/`, {
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                const elementData = await response.json();
                const elementType = elementData.element_type;
                const sectionId = elementData.section_id;

                // Add same element type to the section
                await this.addElement(sectionId, elementType);
                this.showNotification(`${elementType} element added successfully!`, 'success');
                this._refreshStructureIfVisible();
            }
        } catch (error) {
            console.error('Error adding same element:', error);
            this.showNotification('Failed to add element', 'error');
        }
    }

    async duplicateElement(elementId) {
        try {
            // Get element data
            const response = await fetch(`${this.getApiBaseUrl()}/elements/${elementId}/`, {
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                const elementData = await response.json();

                // Create duplicate with same content
                const duplicateData = {
                    section_id: elementData.section_id,
                    parent_element_id: elementData.parent_element_id,
                    element_type: elementData.element_type,
                    content: { ...elementData.content },
                    name: elementData.name + ' (Copy)'
                };

                const createResponse = await fetch(`${this.getApiBaseUrl()}/elements/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify(duplicateData)
                });

                if (createResponse.ok) {
                    const newElementData = await createResponse.json();

                    // Add the duplicated element to the preview DOM
                    const parentId = elementData.parent_element_id || null;
                    const success = this.addElementToPreview(
                        newElementData.element || newElementData,
                        parentId,
                        elementId // Insert after original element
                    );

                    if (success) {
                        // Reinitialize sortables to include new element
                        this.initializePreviewSortables();
                        this.showNotification('Element duplicated successfully!', 'success');
                    } else {
                        // Fallback if DOM update fails
                        location.reload();
                    }

                    // Refresh structure view
                    this._refreshStructureIfVisible();
                } else {
                    throw new Error('Failed to duplicate element');
                }
            }
        } catch (error) {
            console.error('Error duplicating element:', error);
            this.showNotification('Failed to duplicate element', 'error');
        }
    }

    async resetElementStyle(elementId) {
        try {
            // Get default content for the element type
            const response = await fetch(`${this.getApiBaseUrl()}/elements/${elementId}/`, {
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                const elementData = await response.json();
                const defaultContent = this.getDefaultContent(elementData.element_type);

                // Reset to default styling
                const updateResponse = await fetch(`${this.getApiBaseUrl()}/elements/${elementId}/`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken()
                    },
                    body: JSON.stringify({
                        content: defaultContent
                    })
                });

                if (updateResponse.ok) {
                    // Update the element in the preview DOM
                    const updated = this.updateElementInPreview(elementId, defaultContent);

                    if (updated) {
                        this.showNotification('Element style reset successfully!', 'success');
                    } else {
                        // Fallback if DOM update fails
                        location.reload();
                    }

                    // Refresh structure view
                    this._refreshStructureIfVisible();
                } else {
                    throw new Error('Failed to reset element style');
                }
            }
        } catch (error) {
            console.error('Error resetting element style:', error);
            this.showNotification('Failed to reset element style', 'error');
        }
    }

    async copyElementStyle(elementId) {
        try {
            const response = await fetch(`${this.getApiBaseUrl()}/elements/${elementId}/`, {
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                const elementData = await response.json();
                this.copiedStyle = { ...elementData.content };
                this.showNotification('Element style copied!', 'success');
            }
        } catch (error) {
            console.error('Error copying element style:', error);
            this.showNotification('Failed to copy element style', 'error');
        }
    }

    async pasteElementStyle(elementId) {
        if (!this.copiedStyle) return;

        try {
            const updateResponse = await fetch(`${this.getApiBaseUrl()}/elements/${elementId}/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    content: this.copiedStyle
                })
            });

            if (updateResponse.ok) {
                // Update the element in the preview DOM
                const updated = this.updateElementInPreview(elementId, this.copiedStyle);

                if (updated) {
                    this.showNotification('Element style pasted successfully!', 'success');
                } else {
                    // Fallback if DOM update fails
                    location.reload();
                }

                // Refresh structure view
                this._refreshStructureIfVisible();
            } else {
                throw new Error('Failed to paste element style');
            }
        } catch (error) {
            console.error('Error pasting element style:', error);
            this.showNotification('Failed to paste element style', 'error');
        }
    }

    async deleteElementWithConfirm(elementId) {
        if (await AdminModal.confirm({ message: 'Are you sure you want to delete this element? This action cannot be undone.', danger: true, confirmText: 'Delete' })) {
            try {
                // First remove from StateManager
                const removed = pageStateManager.removeElement(elementId);

                if (removed) {
                    // Create and execute delete command for API sync
                    const deleteCommand = new DeleteElementCommand(elementId);
                    deleteCommand.domAlreadyRemoved = true; // Mark that DOM will be updated by StateManager

                    // Execute through history manager
                    await historyManager.execute(deleteCommand);

                    this.showNotification('Element deleted successfully!', 'success');
                } else {
                    throw new Error('Failed to delete element from state');
                }
            } catch (error) {
                console.error('Error deleting element:', error);
                this.showNotification('Failed to delete element', 'error');
            }
        }
    }
}

// Global functions for inline event handlers
let builderInstance;
let autoSaveTimer = null;
let isDraftDirty = false;

function initVisualBuilder(pageData) {
    builderInstance = new VisualPageBuilder(pageData);
    window.builderInstance = builderInstance; // Make available globally

    // Initialize auto-save
    startAutoSave();

    // Check page status and update UI
    checkPageStatus();

    // Initialize modern history UI
    initializeModernHistoryUI();

    // Listen for DOM snapshot restoration to refresh structure view
    window.addEventListener('domSnapshotRestored', function(e) {
        console.log('DOM snapshot restored, refreshing structure view');
        // Refresh the structure view to match the restored state
        if (builderInstance && builderInstance.structureViewVisible) {
            builderInstance._refreshStructureIfVisible();
        }
    });
}

// Save/Publish Dropdown Functions
function toggleSaveDropdown(event) {
    event.stopPropagation();
    const menu = document.getElementById('saveDropdownMenu');
    menu.classList.toggle('show');
}

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('saveDropdownMenu');
    const wrapper = document.querySelector('.save-dropdown-wrapper');

    // Close dropdown if click is outside the wrapper
    if (dropdown && !wrapper?.contains(e.target)) {
        dropdown.classList.remove('show');
    }
});

// Draft/Publish Functions
async function saveDraft() {
    try {
        // Show auto-save indicator
        document.getElementById('auto-save-indicator').style.display = 'inline-flex';
        document.querySelector('#auto-save-indicator .save-text').textContent = 'Saving draft...';

        const response = await fetch(`${builderInstance.getApiBaseUrl()}/page/${builderInstance.pageData.id}/save-draft/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': builderInstance.getCSRFToken()
            },
            body: JSON.stringify({
                description: 'Manual draft save'
            })
        });

        if (response.ok) {
            const data = await response.json();

            // Update UI to show saved
            document.querySelector('#auto-save-indicator .save-text').textContent = 'Draft saved';
            setTimeout(() => {
                document.getElementById('auto-save-indicator').style.display = 'none';
            }, 2000);

            isDraftDirty = false;

            // Capture preview thumbnail
            if (builderInstance.pageData.slug) {
                triggerThumbnailCapture(builderInstance.pageData.id, builderInstance.pageData.slug);
            }

            return data;
        } else {
            throw new Error('Failed to save draft');
        }
    } catch (error) {
        console.error('Error saving draft:', error);
        AdminModal.alert({message: 'Failed to save draft. Please try again.', type: 'error'});
        document.getElementById('auto-save-indicator').style.display = 'none';
    }
}

async function publishPage() {
    if (!await AdminModal.confirm('Are you sure you want to publish this page? This will make your changes live.')) {
        return;
    }

    try {
        const notes = await AdminModal.prompt('Add publish notes (optional):') || '';

        const response = await fetch(`${builderInstance.getApiBaseUrl()}/page/${builderInstance.pageData.id}/publish/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': builderInstance.getCSRFToken()
            },
            body: JSON.stringify({
                notes: notes
            })
        });

        if (response.ok) {
            const data = await response.json();

            // Update status badge
            const statusBadge = document.getElementById('page-status-badge');
            statusBadge.classList.remove('status-draft');
            statusBadge.classList.add('status-published');
            statusBadge.querySelector('.status-text').textContent = 'Published';
            statusBadge.querySelector('i').className = 'fas fa-check-circle';

            AdminModal.toast('Page published successfully!', 'success');
            isDraftDirty = false;

            // Capture preview thumbnail
            if (builderInstance.pageData.slug) {
                triggerThumbnailCapture(builderInstance.pageData.id, builderInstance.pageData.slug);
            }
        } else {
            throw new Error('Failed to publish page');
        }
    } catch (error) {
        console.error('Error publishing page:', error);
        AdminModal.alert({message: 'Failed to publish page. Please try again.', type: 'error'});
    }
}

async function checkPageStatus() {
    try {
        const response = await fetch(`${builderInstance.getApiBaseUrl()}/page/${builderInstance.pageData.id}/versions/`);
        if (response.ok) {
            const data = await response.json();

            const statusBadge = document.getElementById('page-status-badge');
            if (data.current_status === 'published') {
                statusBadge.classList.remove('status-draft');
                statusBadge.classList.add('status-published');
                statusBadge.querySelector('.status-text').textContent = 'Published';
                statusBadge.querySelector('i').className = 'fas fa-check-circle';
            }
        }
    } catch (error) {
        console.error('Error checking page status:', error);
    }
}

// Auto-save functionality
function startAutoSave() {
    // Auto-save every 30 seconds if there are changes
    autoSaveTimer = setInterval(() => {
        if (isDraftDirty) {
            autoSaveDraft();
        }
    }, 30000);
}

async function autoSaveDraft() {
    try {
        // Show auto-save indicator
        document.getElementById('auto-save-indicator').style.display = 'inline-flex';

        const response = await fetch(`${builderInstance.getApiBaseUrl()}/page/${builderInstance.pageData.id}/save-draft/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': builderInstance.getCSRFToken()
            },
            body: JSON.stringify({
                description: 'Auto-save'
            })
        });

        if (response.ok) {
            // Hide indicator after a moment
            setTimeout(() => {
                document.getElementById('auto-save-indicator').style.display = 'none';
            }, 2000);
            isDraftDirty = false;
        }
    } catch (error) {
        console.error('Auto-save error:', error);
        document.getElementById('auto-save-indicator').style.display = 'none';
    }
}

// Mark draft as dirty when changes are made
function markDraftDirty() {
    isDraftDirty = true;
}

// Version History Functions
let versionHistoryVisible = false;

async function toggleVersionHistory() {
    const panel = document.getElementById('version-history-window');
    if (!panel) return;

    versionHistoryVisible = !versionHistoryVisible;

    if (versionHistoryVisible) {
        panel.classList.remove('hidden');
        await loadVersionHistory();
    } else {
        panel.classList.add('hidden');
    }
}

async function loadVersionHistory() {
    const listEl = document.getElementById('version-history-list');
    if (!listEl) return;

    listEl.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--pb-text-secondary);"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';

    try {
        const pageId = builderInstance.pageData.id;
        const response = await fetch(`${builderInstance.getApiBaseUrl()}/page/${pageId}/versions/`, {
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) throw new Error('Failed to load versions');

        const data = await response.json();
        renderVersionHistory(data.versions || []);
    } catch (err) {
        listEl.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--pb-text-secondary);">Failed to load version history</div>';
    }
}

function renderVersionHistory(versions) {
    const listEl = document.getElementById('version-history-list');
    if (!listEl) return;

    if (!versions.length) {
        listEl.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--pb-text-secondary);">No versions yet</div>';
        return;
    }

    listEl.innerHTML = versions.map(function(v) {
        const date = new Date(v.created_at);
        const timeAgo = getRelativeTime(date);
        const badges = [];
        if (v.is_published) badges.push('<span class="version-badge version-badge--published">Published</span>');
        if (v.is_current_draft) badges.push('<span class="version-badge version-badge--draft">Current Draft</span>');

        const canRevert = !v.is_current_draft;
        const revertBtn = canRevert
            ? `<button class="version-revert-btn" data-action="revert-version" data-version-id="${v.id}" title="Revert to this version"><i class="fas fa-undo"></i></button>`
            : '';

        return `
            <div class="version-history-item${v.is_current_draft ? ' version-history-item--current' : ''}">
                <div class="version-history-item__header">
                    <span class="version-history-item__number">v${v.version_number}</span>
                    ${badges.join(' ')}
                    ${revertBtn}
                </div>
                <div class="version-history-item__meta">
                    <span title="${date.toLocaleString()}">${timeAgo}</span>
                    ${v.created_by ? ' &middot; ' + escapeHtml(v.created_by) : ''}
                </div>
                ${v.description ? '<div class="version-history-item__desc">' + escapeHtml(v.description) + '</div>' : ''}
            </div>
        `;
    }).join('');
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function getRelativeTime(dateOrTimestamp) {
    if (!dateOrTimestamp) return 'just now';
    const now = Date.now();
    const ts = dateOrTimestamp instanceof Date ? dateOrTimestamp.getTime() : dateOrTimestamp;
    const diff = now - ts;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (seconds < 60) return 'just now';
    if (minutes < 60) return `${minutes} min${minutes > 1 ? 's' : ''} ago`;
    if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (days < 30) return `${days} day${days > 1 ? 's' : ''} ago`;
    return new Date(ts).toLocaleDateString();
}

async function revertToVersion(versionId) {
    if (!await AdminModal.confirm('Revert to this version? Your current draft will be replaced.')) return;

    try {
        const pageId = builderInstance.pageData.id;
        const response = await fetch(`${builderInstance.getApiBaseUrl()}/page/${pageId}/revert/${versionId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': builderInstance.getCSRFToken()
            }
        });

        if (!response.ok) throw new Error('Revert failed');

        const data = await response.json();
        builderInstance.showNotification(data.message || 'Reverted successfully', 'success');

        // Reload the page to reflect the reverted state
        window.location.reload();
    } catch (err) {
        builderInstance.showNotification('Failed to revert version', 'error');
    }
}

// Undo/Redo Functions
async function undoAction() {
    console.log('🔙 Performing undo...');
    const result = await historyManager.undo();
    console.log('🔙 Undo complete:', result, 'isExecuting:', historyManager.isExecuting);
    // Don't need to call updateHistoryButtonStates since history manager already does it
}

async function redoAction() {
    console.log('🔜 Performing redo...');
    const result = await historyManager.redo();
    console.log('🔜 Redo complete:', result, 'isExecuting:', historyManager.isExecuting);
    // Don't need to call updateHistoryButtonStates since history manager already does it
}

// Modern hover-based history dropdowns
let historyHoverTimeout = null;
let isHistoryDropdownHovered = false;

function updateHistoryButtonStates() {
    // Just call the history manager's updateUI which handles button updates
    historyManager.updateUI();
}

function initializeModernHistoryUI() {
    // Initial button state update - history manager's updateUI handles this
    updateHistoryButtonStates();

    // Undo button hover
    const undoWrapper = document.getElementById('undo-wrapper');
    const undoDropdown = document.getElementById('undo-history-dropdown');
    const redoDropdown = document.getElementById('redo-history-dropdown');

    // Make sure dropdowns don't have display:none set
    if (undoDropdown) {
        undoDropdown.style.removeProperty('display');
    }
    if (redoDropdown) {
        redoDropdown.style.removeProperty('display');
    }

    console.log('🔧 Initializing history UI - undo wrapper:', undoWrapper, 'dropdown:', undoDropdown);

    if (undoWrapper && undoDropdown) {
        undoWrapper.addEventListener('mouseenter', () => {
            clearTimeout(historyHoverTimeout);
            const canUndo = historyManager.canUndo();
            console.log('🖱️ Undo hover:', {
                canUndo: canUndo,
                undoStackLength: historyManager.undoStack.length,
                isExecuting: historyManager.isExecuting
            });
            if (canUndo) {
                showHistoryDropdown('undo');
            }
        });

        undoWrapper.addEventListener('mouseleave', (e) => {
            historyHoverTimeout = setTimeout(() => {
                if (!isHistoryDropdownHovered) {
                    hideHistoryDropdown('undo');
                }
            }, 200);
        });

        // Prevent dropdown from closing when hovering over it
        undoDropdown.addEventListener('mouseenter', () => {
            isHistoryDropdownHovered = true;
            clearTimeout(historyHoverTimeout);
        });

        undoDropdown.addEventListener('mouseleave', () => {
            isHistoryDropdownHovered = false;
            historyHoverTimeout = setTimeout(() => {
                hideHistoryDropdown('undo');
            }, 200);
        });
    }

    // Redo button hover
    const redoWrapper = document.getElementById('redo-wrapper');
    // redoDropdown already declared above

    if (redoWrapper && redoDropdown) {
        redoWrapper.addEventListener('mouseenter', () => {
            clearTimeout(historyHoverTimeout);
            if (historyManager.canRedo()) {
                showHistoryDropdown('redo');
            }
        });

        redoWrapper.addEventListener('mouseleave', (e) => {
            historyHoverTimeout = setTimeout(() => {
                if (!isHistoryDropdownHovered) {
                    hideHistoryDropdown('redo');
                }
            }, 200);
        });

        // Prevent dropdown from closing when hovering over it
        redoDropdown.addEventListener('mouseenter', () => {
            isHistoryDropdownHovered = true;
            clearTimeout(historyHoverTimeout);
        });

        redoDropdown.addEventListener('mouseleave', () => {
            isHistoryDropdownHovered = false;
            historyHoverTimeout = setTimeout(() => {
                hideHistoryDropdown('redo');
            }, 200);
        });
    }
}

function showHistoryDropdown(type) {
    const dropdown = document.getElementById(`${type}-history-dropdown`);
    console.log(`🔍 Showing ${type} dropdown:`, dropdown);
    if (dropdown) {
        dropdown.style.display = 'block'; // Make sure display is not none
        dropdown.style.opacity = '1';
        dropdown.style.visibility = 'visible';
        dropdown.style.transform = 'translateX(-50%) scale(1)';
        updateHistoryTimeline(type);
    }
}

function hideHistoryDropdown(type) {
    const dropdown = document.getElementById(`${type}-history-dropdown`);
    if (dropdown) {
        // Don't use display:none, use opacity and visibility for smooth transitions
        dropdown.style.opacity = '0';
        dropdown.style.visibility = 'hidden';
        dropdown.style.transform = 'translateX(-50%) scale(0.95)';
        clearProgressiveHighlight();
    }
}

function updateHistoryTimeline(type) {
    const timeline = document.getElementById(`${type}-history-timeline`);
    if (!timeline) {
        console.warn(`⚠️ Timeline element not found: ${type}-history-timeline`);
        return;
    }

    console.log(`📝 Updating ${type} history timeline`);
    timeline.innerHTML = '';

    if (type === 'undo') {
        const undoHistory = historyManager.getUndoHistory();
        console.log(`📋 Undo history has ${undoHistory.length} items`);
        if (undoHistory.length === 0) {
            timeline.innerHTML = `
                <div class="history-empty">
                    <div class="history-empty-icon"><i class="fas fa-inbox"></i></div>
                    <div class="history-empty-text">No actions to undo</div>
                </div>
            `;
            return;
        }

        undoHistory.forEach((item, index) => {
            console.log(`  Creating undo item ${index}:`, item.description);
            const historyItem = createHistoryItem(item, index, 'undo', undoHistory.length);
            timeline.appendChild(historyItem);
        });
    } else {
        const redoHistory = historyManager.getRedoHistory();
        console.log(`📋 Redo history has ${redoHistory.length} items`);
        if (redoHistory.length === 0) {
            timeline.innerHTML = `
                <div class="history-empty">
                    <div class="history-empty-icon"><i class="fas fa-inbox"></i></div>
                    <div class="history-empty-text">No actions to redo</div>
                </div>
            `;
            return;
        }

        redoHistory.forEach((item, index) => {
            console.log(`  Creating redo item ${index}:`, item.description);
            const historyItem = createHistoryItem(item, index, 'redo', redoHistory.length);
            timeline.appendChild(historyItem);
        });
    }

    // Add progressive highlight listeners
    setupProgressiveHighlight(timeline, type);
    console.log(`✅ ${type} timeline updated with ${timeline.children.length} items`);
}

function createHistoryItem(item, index, type, totalCount) {
    const div = document.createElement('div');
    div.className = 'history-item';
    div.dataset.index = index;
    div.dataset.count = item.index;

    // Format relative time
    const relativeTime = getRelativeTime(item.timestamp);

    // Get action icon
    const icon = getHistoryActionIcon(item.command);

    div.innerHTML = `
        <div class="history-icon">
            <i class="${icon}"></i>
        </div>
        <div class="history-content">
            <div class="history-action">${item.description}</div>
            <div class="history-time">${relativeTime}</div>
        </div>
        <div class="history-meta">
            ${item.index > 1 ? `<span class="history-count-badge">${item.index}</span>` : ''}
            ${item.hasSnapshot ? '<span class="history-snapshot-badge">💾</span>' : ''}
        </div>
    `;

    // Click handler
    div.addEventListener('click', async (e) => {
        e.stopPropagation();
        console.log('🎯 History item clicked:', {
            type: type,
            index: item.index,
            description: item.description,
            hasSnapshot: item.hasSnapshot,
            timestamp: item.timestamp
        });

        try {
            let result;
            if (type === 'undo') {
                console.log(`📤 Calling undoMultiple(${item.index})`);
                result = await historyManager.undoMultiple(item.index);
                console.log(`📥 undoMultiple returned:`, result);
            } else {
                console.log(`📤 Calling redoMultiple(${item.index})`);
                result = await historyManager.redoMultiple(item.index);
                console.log(`📥 redoMultiple returned:`, result);
            }

            if (!result) {
                console.error('❌ Multiple undo/redo failed!');
            }
        } catch (error) {
            console.error('❌ Error in history item click:', error);
        }

        console.log('🔒 Hiding dropdown after history item click');
        hideHistoryDropdown(type);
    });

    return div;
}

function setupProgressiveHighlight(timeline, type) {
    const items = timeline.querySelectorAll('.history-item');

    timeline.addEventListener('mousemove', (e) => {
        const hoveredItem = e.target.closest('.history-item');
        if (!hoveredItem) {
            clearProgressiveHighlight();
            return;
        }

        const hoveredIndex = parseInt(hoveredItem.dataset.index);

        items.forEach((item, index) => {
            item.classList.remove('will-undo', 'will-redo');

            if (index <= hoveredIndex) {
                item.classList.add(type === 'undo' ? 'will-undo' : 'will-redo');
            }
        });
    });

    timeline.addEventListener('mouseleave', () => {
        clearProgressiveHighlight();
    });
}

function clearProgressiveHighlight() {
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('will-undo', 'will-redo');
    });
}

function getHistoryActionIcon(command) {
    if (!command) return 'fas fa-circle';

    const type = command.constructor.name;
    const iconMap = {
        'AddElementCommand': 'fas fa-plus',
        'DeleteElementCommand': 'fas fa-trash',
        'MoveElementCommand': 'fas fa-arrows-alt',
        'UpdateElementCommand': 'fas fa-edit',
        'DuplicateElementCommand': 'fas fa-copy',
        'BatchCommand': 'fas fa-layer-group',
        'StyleCommand': 'fas fa-paint-brush',
        'TextEditCommand': 'fas fa-font',
        'ImageUpdateCommand': 'fas fa-image',
        'ContainerCommand': 'fas fa-box'
    };

    return iconMap[type] || 'fas fa-circle';
}


// Legacy functions for backward compatibility (can be removed later)
function toggleUndoHistory() {
    // No longer needed with hover-based UI
}

function toggleRedoHistory() {
    // No longer needed with hover-based UI
}

function closeHistoryDropdowns() {
    const undoDropdown = document.getElementById('undo-history-dropdown');
    const redoDropdown = document.getElementById('redo-history-dropdown');

    if (undoDropdown) {
        undoDropdown.style.display = 'none';
    }
    if (redoDropdown) {
        redoDropdown.style.display = 'none';
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(e) {
    const isUndoDropdown = e.target.closest('#undo-dropdown-btn') || e.target.closest('#undo-history-dropdown');
    const isRedoDropdown = e.target.closest('#redo-dropdown-btn') || e.target.closest('#redo-history-dropdown');

    if (!isUndoDropdown && !isRedoDropdown) {
        closeHistoryDropdowns();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+Z for undo
    if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        undoAction();
    }
    // Ctrl+Shift+Z for redo
    else if (e.ctrlKey && e.shiftKey && e.key === 'z') {
        e.preventDefault();
        redoAction();
    }
    // Ctrl+S for save draft
    else if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        saveDraft();
    }
});

// ==============================================
// Container Layout Picker
// ==============================================

// Layout configurations - each creates nested child containers
const containerLayoutConfigs = {
    'full-width': [
        { flex: '1 1 100%', minWidth: '100%', name: 'Full Width Column' }
    ],
    '2-equal': [
        { flex: '1 1 0', minWidth: '0', name: 'Left Column' },
        { flex: '1 1 0', minWidth: '0', name: 'Right Column' }
    ],
    '2-col-33-66': [
        { flex: '1 1 0', minWidth: '0', name: 'Narrow Column' },
        { flex: '2 1 0', minWidth: '0', name: 'Wide Column' }
    ],
    '2-col-66-33': [
        { flex: '2 1 0', minWidth: '0', name: 'Wide Column' },
        { flex: '1 1 0', minWidth: '0', name: 'Narrow Column' }
    ],
    '3-equal': [
        { flex: '1 1 0', minWidth: '0', name: 'Left Column' },
        { flex: '1 1 0', minWidth: '0', name: 'Middle Column' },
        { flex: '1 1 0', minWidth: '0', name: 'Right Column' }
    ],
    '3-col-25-50-25': [
        { flex: '1 1 0', minWidth: '0', name: 'Left Sidebar' },
        { flex: '2 1 0', minWidth: '0', name: 'Main Content' },
        { flex: '1 1 0', minWidth: '0', name: 'Right Sidebar' }
    ],
    'header-2col': [
        { flex: '1 1 100%', minWidth: '100%', name: 'Header Row', isFullRow: true },
        { flex: '1 1 0', minWidth: '0', name: 'Left Column' },
        { flex: '1 1 0', minWidth: '0', name: 'Right Column' }
    ]
};

/**
 * Apply a layout preset to a container by creating child containers
 * @param {string} containerId - The ID of the parent container
 * @param {string} layoutType - The layout type key from containerLayoutConfigs
 */
async function applyContainerLayout(containerId, layoutType) {
    const config = containerLayoutConfigs[layoutType];
    if (!config || !builderInstance) {
        console.error('Invalid layout type or builder not initialized:', layoutType);
        return;
    }

    try {
        builderInstance.showNotification('Applying layout...', 'info');

        // Create child containers for each column in the layout
        for (let i = 0; i < config.length; i++) {
            const childConfig = config[i];

            const childContent = {
                layout: 'flex',
                direction: 'column',
                wrap: 'nowrap',
                gap: '16px',
                flex: childConfig.flex,
                min_width: childConfig.minWidth,
                mobile_stack: true,
                layout_initialized: true  // Child containers don't need layout picker
            };

            // Only set width for full-row items (header row in header-2col layout)
            if (childConfig.isFullRow) {
                childContent.width = '100%';
            }

            // Create the child container via API
            const response = await fetch(`${builderInstance.getApiBaseUrl()}/elements/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': builderInstance.getCSRFToken()
                },
                body: JSON.stringify({
                    page_id: builderInstance.pageId,
                    element_type: 'container',
                    parent_element_id: containerId,
                    content: childContent,
                    order: i
                })
            });

            if (!response.ok) {
                throw new Error(`Failed to create child container ${i + 1}`);
            }
        }

        // Update the parent container to mark it as initialized
        // Use nowrap for horizontal layouts to keep columns side-by-side
        // Exception: header-2col needs wrap so header row wraps to next line
        const updateResponse = await fetch(`${builderInstance.getApiBaseUrl()}/elements/${containerId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': builderInstance.getCSRFToken()
            },
            body: JSON.stringify({
                content: {
                    layout: 'flex',
                    direction: 'row',
                    wrap: layoutType === 'header-2col' ? 'wrap' : 'nowrap',
                    gap: '24px',
                    layout_initialized: true
                }
            })
        });

        if (!updateResponse.ok) {
            throw new Error('Failed to update parent container');
        }

        builderInstance.showNotification('Layout applied successfully!', 'success');

        // Refresh structure panel
        builderInstance._refreshStructureIfVisible();

        // AJAX refresh the container instead of full page reload
        await refreshContainerAfterLayout(containerId);

    } catch (error) {
        console.error('Error applying container layout:', error);
        builderInstance.showNotification('Failed to apply layout: ' + error.message, 'error');
    }
}

/**
 * Skip the layout picker and leave the container empty
 * @param {string} containerId - The ID of the container
 */
async function skipContainerLayout(containerId) {
    if (!builderInstance) {
        console.error('Builder not initialized');
        return;
    }

    try {
        // Just mark the container as initialized without creating children
        const response = await fetch(`${builderInstance.getApiBaseUrl()}/elements/${containerId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': builderInstance.getCSRFToken()
            },
            body: JSON.stringify({
                content: {
                    layout_initialized: true
                }
            })
        });

        if (!response.ok) {
            throw new Error('Failed to update container');
        }

        builderInstance.showNotification('Container ready for use', 'success');

        // AJAX refresh the container instead of full page reload
        await refreshContainerAfterLayout(containerId);

    } catch (error) {
        console.error('Error skipping layout:', error);
        builderInstance.showNotification('Failed to update container', 'error');
    }
}

/**
 * Refresh a container's DOM after layout application without page reload
 * @param {string} containerId - The container element ID
 */
async function refreshContainerAfterLayout(containerId) {
    try {
        // Fetch the updated container HTML from AJAX endpoint with visual_builder flag
        const response = await fetch(`${window.adminPageBuilderPrefix}ajax/element/${containerId}/?visual_builder=true`);
        if (!response.ok) {
            throw new Error('Failed to fetch updated container');
        }
        const html = await response.text();

        // Find the container wrapper in DOM
        const elementWrapper = document.querySelector(`.element-wrapper[data-element-id="${containerId}"]`);
        if (!elementWrapper) {
            console.error('Container wrapper not found in DOM');
            location.reload(); // Fallback to reload
            return;
        }

        // Find the element-content div inside the wrapper and replace its contents
        const elementContent = elementWrapper.querySelector('.element-content');
        if (elementContent) {
            elementContent.innerHTML = html;
        } else {
            console.error('element-content not found in wrapper');
            location.reload();
            return;
        }

        // Re-initialize all interactive elements for new child containers
        if (builderInstance) {
            builderInstance.initializePreviewSortables();  // Recreates all sortables
            builderInstance.setupElementInsertZones();     // Recreates insert zones between elements
            builderInstance.setupDropZones();              // Re-attaches drag/drop event handlers on container drop zones
        }

    } catch (error) {
        console.error('Error refreshing container:', error);
        // Fallback to page reload if AJAX refresh fails
        location.reload();
    }
}

// Event delegation for layout picker interactions
document.addEventListener('click', function(e) {
    // Handle layout option click
    const layoutOption = e.target.closest('.layout-option');
    if (layoutOption) {
        const containerId = layoutOption.closest('.container-layout-picker')?.dataset.containerId;
        const layoutType = layoutOption.dataset.layout;
        if (containerId && layoutType) {
            e.preventDefault();
            e.stopPropagation();
            applyContainerLayout(containerId, layoutType);
        }
        return;
    }

    // Handle skip button click
    const skipBtn = e.target.closest('.skip-layout-btn');
    if (skipBtn) {
        const containerId = skipBtn.dataset.containerId;
        if (containerId) {
            e.preventDefault();
            e.stopPropagation();
            skipContainerLayout(containerId);
        }
        return;
    }
});

async function deleteSection(sectionId) {
    if (await AdminModal.confirm({ message: 'Are you sure you want to delete this section? This will also delete all elements within it.', danger: true, confirmText: 'Delete' })) {
        try {
            const response = await fetch(`${builderInstance.getApiBaseUrl()}/sections/${sectionId}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': builderInstance.getCSRFToken()
                }
            });

            if (response.ok) {
                // First, find all element IDs within this section to clean up any orphaned references
                const sectionWrapper = document.querySelector(`[data-section-id="${sectionId}"]`);
                if (sectionWrapper) {
                    // Get all element IDs within this section
                    const elementsToRemove = sectionWrapper.querySelectorAll('[data-element-id]');
                    const elementIds = Array.from(elementsToRemove).map(el => el.dataset.elementId);

                    // Remove the section wrapper
                    sectionWrapper.remove();

                    // Clean up any orphaned element references elsewhere in the DOM
                    // (in case there are duplicates outside the section wrapper)
                    elementIds.forEach(elementId => {
                        const orphanedElements = document.querySelectorAll(`[data-element-id="${elementId}"]`);
                        orphanedElements.forEach(el => {
                            console.log(`Cleaning up orphaned element reference: ${elementId}`);
                            el.remove();
                        });
                    });
                }

                // Check if page is now empty and show empty drop zone if needed
                const remainingSections = document.querySelectorAll('.section-wrapper');
                if (remainingSections.length === 0) {
                    const mainDropZone = document.getElementById('main-drop-zone');
                    if (mainDropZone) {
                        mainDropZone.style.display = 'block';
                    }
                }

                // Refresh structure view
                if (builderInstance) {
                    builderInstance._refreshStructureIfVisible();
                }

                builderInstance.showNotification('Section deleted successfully!', 'success');
            } else {
                throw new Error('Failed to delete section');
            }
        } catch (error) {
            console.error('Error deleting section:', error);
            builderInstance.showNotification('Error deleting section', 'error');
        }
    }
}

function editElement(elementId, event) {
    // Prevent event bubbling to parent elements
    if (event) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
    }

    // Sync structure view selection
    if (builderInstance) {
        builderInstance.syncStructureSelection(elementId);
    }

    // Find the specific element wrapper for this ID
    // Use a more specific selector to avoid conflicts with nested elements
    let elementWrapper = null;
    
    // First, try to find a direct element wrapper with this exact ID
    const allWrappers = document.querySelectorAll(`.element-wrapper[data-element-id="${elementId}"]`);
    
    if (allWrappers.length === 1) {
        elementWrapper = allWrappers[0];
    } else if (allWrappers.length > 1) {
        // Multiple wrappers found - pick the one that's not nested inside another wrapper with the same ID
        for (let wrapper of allWrappers) {
            const parentWrapper = wrapper.parentElement?.closest(`.element-wrapper[data-element-id="${elementId}"]`);
            if (!parentWrapper) {
                elementWrapper = wrapper;
                break;
            }
        }
        // If we still don't have one, use the first one
        if (!elementWrapper) {
            elementWrapper = allWrappers[0];
        }
    }
    
    // If not found, check for container elements
    if (!elementWrapper) {
        // Try to find the container by ID
        const containerEl = document.querySelector(`#container-${elementId}`);
        if (containerEl) {
            // Check if there's a wrapper around it
            const parentWrapper = containerEl.closest('.element-wrapper');
            if (parentWrapper && parentWrapper.dataset.elementId == elementId) {
                elementWrapper = parentWrapper;
            } else {
                // Use the container element itself and ensure it has the right attributes
                elementWrapper = containerEl;
                // Ensure container has proper data attributes
                if (!elementWrapper.dataset.elementId) {
                    elementWrapper.dataset.elementId = elementId;
                }
                if (!elementWrapper.dataset.elementType) {
                    elementWrapper.dataset.elementType = 'container';
                }
            }
        }
    }
    
    if (!elementWrapper) {
        console.error('Element not found:', elementId);
        return;
    }
    
    // Get element type - ensure containers are properly identified
    let elementType = elementWrapper.dataset.elementType;
    if (!elementType) {
        // If no type set but it has container ID pattern, it's a container
        if (elementWrapper.id && elementWrapper.id.startsWith('container-')) {
            elementType = 'container';
            elementWrapper.dataset.elementType = 'container';
        } else {
            elementType = 'text'; // Default fallback
        }
    }
    
    // Remove all previous selections
    document.querySelectorAll('.element-wrapper.selected, .pb-container.selected').forEach(el => {
        el.classList.remove('selected');
    });
    
    // Highlight only this specific element
    elementWrapper.classList.add('selected');
    
    // Show the properties panel for this element
    if (window.builderInstance && window.builderInstance.showElementProperties) {
        window.builderInstance.showElementProperties(elementWrapper);
    } else {
        showElementProperties(elementId, elementType);
    }
}

async function showElementProperties(elementId, elementType) {
    const propertiesPanel = document.getElementById('properties-panel');
    if (!propertiesPanel) return;

    // Use config.json-based property renderer for all element types
    if (window.propertyRenderer && window.builderInstance) {
        try {
            // Fetch element data from API
            const response = await fetch(`${builderInstance.getApiBaseUrl()}/elements/${elementId}/`);
            if (response.ok) {
                const elementData = await response.json();
                // Load element config and render properties
                const config = await builderInstance.loadElementConfig(elementType);
                if (config) {
                    window.propertyRenderer.renderProperties('properties-panel', config, elementData);
                    return;
                }
            }
        } catch (error) {
            console.error('Error loading element properties:', error);
        }
    }

    // PropertyRenderer handles all elements via config.json
    propertiesPanel.innerHTML = '<div class="properties-empty"><p>Unable to load element properties. Please refresh and try again.</p></div>';
}

function cancelElementEdit() {
    const propertiesPanel = document.getElementById('properties-panel');
    if (propertiesPanel) {
        propertiesPanel.innerHTML = `
            <div class="no-selection">
                <i class="fas fa-mouse-pointer"></i>
                <p>Select an element to edit its properties</p>
            </div>
        `;
    }
    
    // Remove selection highlight
    document.querySelectorAll('.element-wrapper').forEach(el => el.classList.remove('selected'));
}

async function saveElementChanges(elementId) {
    const textInput = document.getElementById('element-text');
    if (!textInput) return;
    
    const newText = textInput.value.trim();
    if (!newText) {
        builderInstance.showNotification('Text content cannot be empty', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${builderInstance.getApiBaseUrl()}/elements/${elementId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': builderInstance.getCSRFToken()
            },
            body: JSON.stringify({
                content: { text: newText }
            })
        });

        if (response.ok) {
            // Update the element in the DOM
            const elementWrapper = document.querySelector(`[data-element-id="${elementId}"]`);
            const elementType = elementWrapper.dataset.elementType;
            const elementContent = elementWrapper.querySelector('.element-content');
            
            if (elementType === 'heading') {
                const h3 = elementContent.querySelector('h3');
                if (h3) h3.textContent = newText;
            } else if (elementType === 'text') {
                const p = elementContent.querySelector('p');
                if (p) p.textContent = newText;
            } else if (elementType === 'button') {
                const button = elementContent.querySelector('button');
                if (button) button.textContent = newText;
            }
            
            builderInstance.showNotification('Element updated successfully!', 'success');
            cancelElementEdit(); // Clear the properties panel
        } else {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Failed to update element');
        }
    } catch (error) {
        console.error('Error updating element:', error);
        builderInstance.showNotification('Failed to update element: ' + error.message, 'error');
    }
}

async function deleteElement(elementId, event) {
    // Prevent event bubbling to parent elements
    if (event) {
        event.preventDefault();
        event.stopPropagation();
        event.stopImmediatePropagation();
    }

    if (await AdminModal.confirm({ message: 'Are you sure you want to delete this element?', danger: true, confirmText: 'Delete' })) {
        try {
            // First remove from StateManager
            const removed = pageStateManager.removeElement(elementId);

            if (removed) {
                // Use command pattern for undo/redo support
                const deleteCommand = new DeleteElementCommand(elementId);
                deleteCommand.domAlreadyRemoved = true; // Mark that DOM will be updated by StateManager

                // Execute through history manager to enable undo/redo
                await historyManager.execute(deleteCommand);

                // Show success message
                builderInstance.showNotification('Element deleted successfully!', 'success');
            } else {
                throw new Error('Failed to delete element from state');
            }
        } catch (error) {
            console.error('Error deleting element:', error);
            builderInstance.showNotification('Failed to delete element: ' + error.message, 'error');
        }
    }
}

function previewPage() {
    // Open preview with device toolbar for non-technical users
    window.open(`${window.adminPageBuilderPrefix}builder-preview/${builderInstance.pageData.slug}/`, '_blank');
}

function savePage() {
    builderInstance.showNotification('Page saved successfully!', 'success');
}

function openModal(title, elementId, bodyHtml) {
    const overlay = document.getElementById('modal-overlay');
    const titleEl = document.getElementById('modal-title');
    const bodyEl = document.getElementById('modal-body');
    if (!overlay || !bodyEl) return;

    if (titleEl) titleEl.textContent = title || 'Edit Element';
    overlay.dataset.elementId = elementId || '';
    bodyEl.innerHTML = bodyHtml || '';
    overlay.style.display = 'flex';
}

function closeModal() {
    const overlay = document.getElementById('modal-overlay');
    if (overlay) {
        overlay.style.display = 'none';
        delete overlay.dataset.elementId;
    }
}

async function saveElement() {
    const overlay = document.getElementById('modal-overlay');
    const bodyEl = document.getElementById('modal-body');
    if (!overlay || !bodyEl) return;

    const elementId = overlay.dataset.elementId;
    if (!elementId) {
        builderInstance.showNotification('No element selected', 'error');
        return;
    }

    // Collect all form field values from the modal body
    const content = {};
    bodyEl.querySelectorAll('input, textarea, select').forEach(function(field) {
        if (field.name) {
            if (field.type === 'checkbox') {
                content[field.name] = field.checked;
            } else {
                content[field.name] = field.value;
            }
        }
    });

    try {
        const response = await fetch(`${builderInstance.getApiBaseUrl()}/elements/${elementId}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': builderInstance.getCSRFToken()
            },
            body: JSON.stringify({ content: content })
        });

        if (response.ok) {
            closeModal();
            builderInstance.showNotification('Element updated successfully!', 'success');
            // Refresh the element in the canvas
            if (typeof refreshElement === 'function') {
                refreshElement(parseInt(elementId, 10));
            }
        } else {
            const errorData = await response.json().catch(() => ({}));
            builderInstance.showNotification(errorData.error || 'Failed to save element', 'error');
        }
    } catch (err) {
        builderInstance.showNotification('Failed to save element', 'error');
    }
}

// CSS for device preview
const deviceCSS = `
.canvas-frame.device-mobile {
    max-width: 375px;
    margin: 0 auto;
    transition: max-width 0.3s ease;
}
.canvas-frame.device-tablet {
    max-width: 768px;
    margin: 0 auto;
    transition: max-width 0.3s ease;
}
.canvas-frame.device-desktop {
    max-width: 1200px;
    margin: 0 auto;
    transition: max-width 0.3s ease;
}

.notification {
    position: fixed;
    top: 80px;
    right: 20px;
    padding: 12px 20px;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    gap: 10px;
    z-index: 2000;
    transform: translateX(100%);
    animation: slideIn 0.3s ease forwards;
}

.notification-success {
    border-left: 4px solid #10b981;
    color: #10b981;
}

.notification-error {
    border-left: 4px solid #ef4444;
    color: #ef4444;
}

.notification-info {
    border-left: 4px solid #3b82f6;
    color: #3b82f6;
}

@keyframes slideIn {
    to {
        transform: translateX(0);
    }
}
`;

// Inject CSS
const style = document.createElement('style');
style.textContent = deviceCSS;
document.head.appendChild(style);

// Global functions for container property updates
function updateContainerProperty(input) {
    const form = input.closest('.properties-form');
    const elementId = form.dataset.elementId;

    // Collect all form data
    const formData = new FormData(form);
    const content = {};

    for (let [key, value] of formData.entries()) {
        content[key] = value;
    }

    // Apply live preview immediately
    applyLivePreview(elementId, content);

    // Store the old content for undo (if not already stored)
    if (!window.elementOldContent) {
        window.elementOldContent = {};
    }
    if (!window.elementOldContent[elementId]) {
        // Get current content from the element
        fetch(`${builderInstance.getApiBaseUrl()}/elements/${elementId}/`)
            .then(response => response.json())
            .then(data => {
                window.elementOldContent[elementId] = data.content;
            });
    }

    // Debounce API calls and command creation to avoid too many history entries
    clearTimeout(window.updateTimeout);
    window.updateTimeout = setTimeout(async () => {
        try {
            // Create update command for undo/redo support
            const oldData = { content: window.elementOldContent[elementId] || {} };
            const newData = { content: content };

            const updateCommand = new UpdateElementCommand(elementId, oldData, newData);

            // Execute through history manager
            await historyManager.execute(updateCommand);

            // Update stored old content for next change
            window.elementOldContent[elementId] = content;
        } catch (error) {
            console.error('Error updating container:', error);
            builderInstance.showNotification('Error updating container: ' + error.message, 'error');
        }

        // Maintain selection after update without refreshing properties panel
        const elementWrapper = document.querySelector(`[data-element-id="${elementId}"]`);
        if (elementWrapper && !elementWrapper.classList.contains('selected')) {
            // Clear previous selection
            document.querySelectorAll('.selected').forEach(el => el.classList.remove('selected'));
            // Select the element without calling showElementProperties again
            elementWrapper.classList.add('selected');
            builderInstance.selectedElement = elementWrapper;
        }
    }, 500); // Wait 500ms after last change before saving
}

function applyLivePreview(elementId, content) {
    // Try to find the container element - it could be the pb-container itself or inside an element wrapper
    let container = document.querySelector(`#container-${elementId}`);
    if (!container) {
        container = document.querySelector(`[data-element-id="${elementId}"].pb-container`);
    }
    if (!container) {
        container = document.querySelector(`[data-element-id="${elementId}"] .pb-container`);
    }
    if (!container) {
        // Try to find by element wrapper and look for pb-container inside
        const elementWrapper = document.querySelector(`[data-element-id="${elementId}"][data-element-type="container"]`);
        if (elementWrapper) {
            container = elementWrapper.querySelector('.pb-container');
        }
    }
    if (!container) {
        console.warn(`Container element ${elementId} not found for live preview. Available elements:`, 
                    document.querySelectorAll(`[data-element-id="${elementId}"]`));
        return;
    }
    
    // Build styles object
    const styles = {};
    
    // Layout properties
    if (content.layout) {
        styles.display = content.layout;
        
        if (content.layout === 'flex') {
            styles.flexDirection = content.direction || 'row';
            styles.justifyContent = content.justify_content || 'flex-start';
            styles.alignItems = content.align_items || 'stretch';
            styles.flexWrap = content.wrap || 'nowrap';
            
            const rowGap = content.row_gap || '0';
            const colGap = content.column_gap || '0';
            const gapUnit = content.gap_unit || 'px';
            styles.gap = `${rowGap}${gapUnit} ${colGap}${gapUnit}`;
        } else if (content.layout === 'grid') {
            styles.gridTemplateColumns = content.grid_columns || '1fr';
            styles.gridTemplateRows = content.grid_rows || 'auto';
            
            const rowGap = content.row_gap || '0';
            const colGap = content.column_gap || '0';
            const gapUnit = content.gap_unit || 'px';
            styles.gap = `${rowGap}${gapUnit} ${colGap}${gapUnit}`;
        }
    }
    
    // Size properties
    if (content.width) {
        const widthUnit = content.width_unit || '%';
        styles.width = `${content.width}${widthUnit}`;
    }
    
    if (content.min_height && content.min_height !== 'auto') {
        const minHeightUnit = content.min_height_unit || 'px';
        styles.minHeight = `${content.min_height}${minHeightUnit}`;
    }
    
    if (content.overflow) {
        styles.overflow = content.overflow;
    }
    
    // Background properties
    if (content.background_type === 'color' && content.background_color) {
        styles.backgroundColor = content.background_color;
        styles.backgroundImage = 'none';
    } else if (content.background_type === 'gradient' && content.background_gradient) {
        styles.background = content.background_gradient;
    } else if (content.background_type === 'image' && content.background_image) {
        styles.backgroundImage = `url('${content.background_image}')`;
        styles.backgroundSize = content.background_size || 'cover';
        styles.backgroundPosition = content.background_position || 'center';
        styles.backgroundRepeat = content.background_repeat || 'no-repeat';
    }
    
    // Border properties
    if (content.border_type && content.border_type !== 'none') {
        const borderWidth = content.border_width || '1';
        const borderColor = content.border_color || '#e2e8f0';
        styles.border = `${borderWidth}px ${content.border_type} ${borderColor}`;
    } else {
        styles.border = 'none';
    }
    
    // Border radius
    const topRadius = content.border_radius_top || '0';
    const rightRadius = content.border_radius_right || '0';
    const bottomRadius = content.border_radius_bottom || '0';
    const leftRadius = content.border_radius_left || '0';
    styles.borderRadius = `${topRadius}px ${rightRadius}px ${bottomRadius}px ${leftRadius}px`;
    
    // Box shadow
    if (content.box_shadow) {
        styles.boxShadow = content.box_shadow;
    }
    
    // Spacing
    const marginUnit = content.margin_unit || 'px';
    const marginTop = content.margin_top || '0';
    const marginRight = content.margin_right || '0';
    const marginBottom = content.margin_bottom || '0';
    const marginLeft = content.margin_left || '0';
    styles.margin = `${marginTop}${marginUnit} ${marginRight}${marginUnit} ${marginBottom}${marginUnit} ${marginLeft}${marginUnit}`;
    
    const paddingUnit = content.padding_unit || 'px';
    const paddingTop = content.padding_top || '20';
    const paddingRight = content.padding_right || '20';
    const paddingBottom = content.padding_bottom || '20';
    const paddingLeft = content.padding_left || '20';
    styles.padding = `${paddingTop}${paddingUnit} ${paddingRight}${paddingUnit} ${paddingBottom}${paddingUnit} ${paddingLeft}${paddingUnit}`;
    
    // Advanced properties
    if (content.align_self) {
        styles.alignSelf = content.align_self;
    }
    if (content.order !== null && content.order !== undefined) {
        styles.order = content.order;
    }
    if (content.flex_grow) {
        styles.flexGrow = content.flex_grow;
    }
    if (content.flex_shrink) {
        styles.flexShrink = content.flex_shrink;
    }
    
    // Apply all styles to the container
    Object.assign(container.style, styles);
    
    // Update overlay if present
    const overlay = container.querySelector('.pb-container-overlay');
    if (overlay) {
        if (content.overlay_type === 'color' && content.overlay_color) {
            overlay.style.backgroundColor = content.overlay_color;
        } else if (content.overlay_type === 'gradient' && content.overlay_gradient) {
            overlay.style.background = content.overlay_gradient;
        }
    }
    
    // Apply cell styling to child elements
    if (content.cell_max_width || content.cell_alignment || content.cell_flex_basis) {
        const childElements = container.querySelectorAll('.element-wrapper, .pb-container > *');
        childElements.forEach(child => {
            if (content.cell_max_width) {
                const unit = content.cell_max_width_unit || 'px';
                child.style.maxWidth = `${content.cell_max_width}${unit}`;
            }
            if (content.cell_alignment && content.cell_alignment !== 'auto') {
                child.style.alignSelf = content.cell_alignment;
            }
            if (content.cell_flex_basis && content.cell_flex_basis !== 'auto') {
                child.style.flexBasis = content.cell_flex_basis;
            }
        });
    }
}

// Container structure management functions
function addContainerRow(containerId) {
    // Add a new container configured as a row (horizontal layout)
    // Rows should span full width to be clearly distinguishable
    builderInstance.addContainerWithConfig(containerId, {
        layout: 'flex',
        direction: 'row',
        justify_content: 'flex-start',
        align_items: 'stretch',
        width: '100',
        width_unit: '%',
        min_height: '100',
        min_height_unit: 'px',
        padding_top: '15',
        padding_right: '15', 
        padding_bottom: '15',
        padding_left: '15',
        padding_unit: 'px',
        background_color: 'rgba(248, 249, 250, 0.5)',  // Light background to show row boundaries
        border_type: 'dashed',
        border_width: '1',
        border_color: '#dee2e6'
    });
}

function addContainerColumn(containerId) {
    // Add a new container configured as a column (vertical layout)
    // Columns should be narrower and flex to share space
    builderInstance.addContainerWithConfig(containerId, {
        layout: 'flex',
        direction: 'column',
        justify_content: 'flex-start',
        align_items: 'stretch',
        // Don't set flex here - it will be applied to the wrapper
        min_width: '200',
        min_width_unit: 'px',
        min_height: '100',
        min_height_unit: 'px',
        padding_top: '15',
        padding_right: '15',
        padding_bottom: '15',
        padding_left: '15',
        padding_unit: 'px',
        background_color: 'rgba(255, 255, 255, 0.8)',  // Slightly different background for columns
        border_type: 'dashed',
        border_width: '1',
        border_color: '#cbd5e1'
    });
}

function toggleBackgroundControls(backgroundType) {
    const colorControls = document.querySelector('.background-color-controls');
    const gradientControls = document.querySelector('.background-gradient-controls');
    const imageControls = document.querySelector('.background-image-controls');
    
    if (colorControls) colorControls.style.display = backgroundType === 'color' ? 'block' : 'none';
    if (gradientControls) gradientControls.style.display = backgroundType === 'gradient' ? 'block' : 'none';
    if (imageControls) imageControls.style.display = backgroundType === 'image' ? 'block' : 'none';
}

function toggleOverlayControls(overlayType) {
    const colorControls = document.querySelector('.overlay-color-controls');
    
    if (colorControls) colorControls.style.display = overlayType === 'color' ? 'block' : 'none';
}

function toggleBorderControls(borderType) {
    const borderControls = document.querySelector('.border-controls');
    
    if (borderControls) borderControls.style.display = borderType && borderType !== 'none' ? 'block' : 'none';
}

function toggleLayoutControls(layoutType) {
    const flexControls = document.querySelector('.flex-controls');
    const gridControls = document.querySelector('.grid-controls');
    
    if (flexControls) {
        flexControls.style.display = (layoutType === 'flex' || !layoutType) ? 'block' : 'none';
    }
    if (gridControls) {
        gridControls.style.display = (layoutType === 'grid') ? 'block' : 'none';
    }
}

// Utility: refresh an element's rendered HTML from the server
async function refreshElement(elementId) {
    try {
        const response = await fetch(`${window.adminPageBuilderPrefix}ajax/element/${elementId}/`);
        if (response.ok) {
            const html = await response.text();
            const elementWrapper = document.querySelector(`[data-element-id="${elementId}"]`);
            if (elementWrapper) {
                const elementContent = elementWrapper.querySelector('.element-content');
                if (elementContent) {
                    elementContent.innerHTML = html;
                }
            }
        } else {
            console.error('Failed to refresh element:', response.status, response.statusText);
        }
    } catch (error) {
        console.error('Error refreshing element:', error);
    }
}

// Global notification function for use outside the class
function showNotification(message, type = 'info') {
    AdminModal.toast(message, type || 'info');
}

// Global Structure View Functions
function toggleStructureView() {
    if (builderInstance) {
        builderInstance.toggleStructureView();
    }
}

function expandAllStructureNodes() {
    if (builderInstance) {
        builderInstance.expandAllStructureNodes();
    }
}

function collapseAllStructureNodes() {
    if (builderInstance) {
        builderInstance.collapseAllStructureNodes();
    }
}

/**
 * Update element preview with new properties
 * Called by property renderer when properties change
 */
function updateElementPreview(elementId, properties) {
    // Use LivePreviewManager if available
    if (window.livePreview) {
        window.livePreview.updateElement(elementId, properties, {
            instant: true,
            sync: false  // Property renderer handles server sync
        });
        return;
    }

    // Fallback to direct update if LivePreviewManager not available
    const elementWrapper = document.querySelector(`[data-element-id="${elementId}"]`);
    if (!elementWrapper) return;

    const elementContent = elementWrapper.querySelector('.element-content');
    if (!elementContent) return;

    const elementType = elementWrapper.dataset.elementType;

    // Get the actual content element based on type with improved selectors
    let targetElement = elementContent;

    if (elementType === 'heading') {
        targetElement = elementContent.querySelector('h1, h2, h3, h4, h5, h6') || elementContent;
    } else if (elementType === 'text') {
        // Fixed: Look for .text-element instead of p
        targetElement = elementContent.querySelector('.text-element') || elementContent.querySelector('p') || elementContent;
    } else if (elementType === 'button') {
        targetElement = elementContent.querySelector('button, .btn, .button-element') || elementContent;
    } else if (elementType === 'container') {
        targetElement = elementContent.querySelector('.pb-container') || elementContent;
    } else if (elementType === 'image') {
        targetElement = elementContent.querySelector('img, .image-element') || elementContent;
    } else if (elementType === 'video') {
        targetElement = elementContent.querySelector('video, .video-element') || elementContent;
    }

    // Apply style properties
    for (const [key, value] of Object.entries(properties)) {
        // Skip non-style properties
        if (key === 'text' || key === 'href' || key === 'src' || key === 'alt' ||
            key === 'content' || key === 'placeholder' || key === 'value') {
            continue;
        }

        // Map property names to CSS properties
        const cssProperty = mapPropertyToCss(key);
        if (cssProperty && value !== undefined && value !== null) {
            targetElement.style[cssProperty] = value;
        }
    }
}

/**
 * Map property names to CSS property names
 */
function mapPropertyToCss(property) {
    const propertyMap = {
        // Colors
        'background': 'background',
        'background_color': 'backgroundColor',
        'backgroundColor': 'backgroundColor',
        'background-color': 'backgroundColor',
        'text_color': 'color',
        'textColor': 'color',
        'color': 'color',
        'border_color': 'borderColor',
        'borderColor': 'borderColor',
        'border-color': 'borderColor',

        // Typography
        'font_size': 'fontSize',
        'fontSize': 'fontSize',
        'font-size': 'fontSize',
        'font_weight': 'fontWeight',
        'fontWeight': 'fontWeight',
        'font-weight': 'fontWeight',
        'font_family': 'fontFamily',
        'fontFamily': 'fontFamily',
        'font-family': 'fontFamily',
        'text_align': 'textAlign',
        'textAlign': 'textAlign',
        'text-align': 'textAlign',
        'line_height': 'lineHeight',
        'lineHeight': 'lineHeight',
        'line-height': 'lineHeight',
        'letter_spacing': 'letterSpacing',
        'letterSpacing': 'letterSpacing',
        'letter-spacing': 'letterSpacing',

        // Spacing
        'padding': 'padding',
        'padding_top': 'paddingTop',
        'paddingTop': 'paddingTop',
        'padding-top': 'paddingTop',
        'padding_right': 'paddingRight',
        'paddingRight': 'paddingRight',
        'padding-right': 'paddingRight',
        'padding_bottom': 'paddingBottom',
        'paddingBottom': 'paddingBottom',
        'padding-bottom': 'paddingBottom',
        'padding_left': 'paddingLeft',
        'paddingLeft': 'paddingLeft',
        'padding-left': 'paddingLeft',

        'margin': 'margin',
        'margin_top': 'marginTop',
        'marginTop': 'marginTop',
        'margin-top': 'marginTop',
        'margin_right': 'marginRight',
        'marginRight': 'marginRight',
        'margin-right': 'marginRight',
        'margin_bottom': 'marginBottom',
        'marginBottom': 'marginBottom',
        'margin-bottom': 'marginBottom',
        'margin_left': 'marginLeft',
        'marginLeft': 'marginLeft',
        'margin-left': 'marginLeft',

        // Borders
        'border_width': 'borderWidth',
        'borderWidth': 'borderWidth',
        'border-width': 'borderWidth',
        'border_style': 'borderStyle',
        'borderStyle': 'borderStyle',
        'border-style': 'borderStyle',
        'border_radius': 'borderRadius',
        'borderRadius': 'borderRadius',
        'border-radius': 'borderRadius',

        // Effects
        'box_shadow': 'boxShadow',
        'boxShadow': 'boxShadow',
        'box-shadow': 'boxShadow',
        'text_shadow': 'textShadow',
        'textShadow': 'textShadow',
        'text-shadow': 'textShadow',

        // Layout
        'width': 'width',
        'height': 'height',
        'min_width': 'minWidth',
        'minWidth': 'minWidth',
        'min-width': 'minWidth',
        'max_width': 'maxWidth',
        'maxWidth': 'maxWidth',
        'max-width': 'maxWidth',
        'min_height': 'minHeight',
        'minHeight': 'minHeight',
        'min-height': 'minHeight',
        'max_height': 'maxHeight',
        'maxHeight': 'maxHeight',
        'max-height': 'maxHeight',

        // Display
        'display': 'display',
        'opacity': 'opacity',
        'visibility': 'visibility',
        'overflow': 'overflow'
    };

    return propertyMap[property] || null;
}

// Make functions available globally
window.updateElementPreview = updateElementPreview;
window.initVisualBuilder = initVisualBuilder;
window.undoAction = undoAction;
window.redoAction = redoAction;
window.editElement = editElement;
window.deleteElement = deleteElement;
window.saveDraft = saveDraft;
window.publishPage = publishPage;
window.toggleSaveDropdown = toggleSaveDropdown;
window.openModal = openModal;
window.historyManager = historyManager;
window.refreshElement = refreshElement;
window.applyContainerLayout = applyContainerLayout;
window.skipContainerLayout = skipContainerLayout;

// ===============================================
// Page Settings Manager
// ===============================================

/**
 * PageSettingsManager - Handles page-level configuration in visual builder
 * Manages header/footer selection, design settings, SEO, and page details
 */
class PageSettingsManager {
    constructor(pageId, apiBaseUrl) {
        this.pageId = pageId;
        this.apiBaseUrl = apiBaseUrl || '/api/page-builder/page';
        this.config = null;
        this.currentValues = null;
        this.dynamicOptions = null;
        this.saveTimeout = null;
        this.isPageSettingsMode = false;
    }

    /**
     * Load page settings from the API
     */
    async loadSettings() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/${this.pageId}/settings/`);
            if (!response.ok) {
                throw new Error(`Failed to load page settings: ${response.status}`);
            }
            const data = await response.json();
            this.config = data.config;
            this.currentValues = data.page_data;  // API returns 'page_data'
            this.dynamicOptions = data.config.dynamic_options;  // Dynamic options are in config
            return data;
        } catch (error) {
            console.error('Error loading page settings:', error);
            showNotification('Failed to load page settings', 'error');
            throw error;
        }
    }

    /**
     * Render the page settings panel using PropertyRenderer
     */
    renderSettingsPanel(containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error('Container not found:', containerId);
            return;
        }

        // Update sidebar header to show "Page Settings" with back button
        const sidebarHeader = document.querySelector('.right-sidebar .sidebar-header h3');
        if (sidebarHeader) {
            sidebarHeader.innerHTML = '<button class="page-settings-back-btn" title="Back to Properties"><i class="fas fa-arrow-left"></i></button> <i class="fas fa-file-alt"></i> Page Settings';
            // Add click handler for back button
            const backBtn = sidebarHeader.querySelector('.page-settings-back-btn');
            if (backBtn) {
                backBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.exitPageSettingsMode();
                    sidebarHeader.innerHTML = '<i class="fas fa-cogs"></i> Properties';
                    // Clear properties panel and show default message
                    const propertiesPanel = document.getElementById('properties-panel');
                    if (propertiesPanel) {
                        propertiesPanel.innerHTML = '<p class="no-selection">Select an element to edit its properties</p>';
                    }
                });
            }
        }

        // Check if global PropertyRenderer is available
        if (!window.propertyRenderer) {
            console.error('PropertyRenderer not found');
            container.innerHTML = '<p class="no-selection">PropertyRenderer not available</p>';
            return;
        }

        // Inject dynamic options into config
        const configWithOptions = this.injectDynamicOptions(this.config);

        // Build element data structure expected by PropertyRenderer
        // PropertyRenderer expects: { id, element_type, content: {...} }
        const elementData = {
            id: 'page-' + this.pageId,
            element_type: 'page',
            content: this.currentValues
        };

        // Store reference to this for property change handler
        const self = this;

        // Override the property renderer's change handler for page settings
        window.propertyRenderer.onPropertyChange = function(propertyId, value, propertyConfig) {
            self.handlePropertyChange(propertyId, value, propertyConfig);
        };

        // Render the properties using the global singleton
        window.propertyRenderer.renderProperties(containerId, configWithOptions, elementData);
    }

    /**
     * Inject dynamic options from API into the config
     */
    injectDynamicOptions(config) {
        if (!this.dynamicOptions || !config || !config.tabs) {
            return config;
        }

        // Deep clone the config to avoid mutating the original
        const configCopy = JSON.parse(JSON.stringify(config));

        // Iterate through tabs (object with tab keys) and properties to inject dynamic options
        for (const tab of Object.values(configCopy.tabs)) {
            if (!tab.properties) continue;

            // Tab.properties is an object (property groups), not an array
            for (const prop of Object.values(tab.properties)) {
                if (prop.options_source && this.dynamicOptions[prop.options_source]) {
                    prop.options = this.dynamicOptions[prop.options_source];
                    delete prop.options_source;  // Remove the source reference
                }

                // Handle nested properties in property_groups
                if (prop.properties) {
                    for (const nestedProp of Object.values(prop.properties)) {
                        if (nestedProp.options_source && this.dynamicOptions[nestedProp.options_source]) {
                            nestedProp.options = this.dynamicOptions[nestedProp.options_source];
                            delete nestedProp.options_source;
                        }
                    }
                }
            }
        }

        return configCopy;
    }

    /**
     * Handle property changes with debounced auto-save
     */
    handlePropertyChange(propertyId, value, propertyConfig) {
        // Update local values
        this.currentValues[propertyId] = value;

        // Debounce the save
        if (this.saveTimeout) {
            clearTimeout(this.saveTimeout);
        }

        this.saveTimeout = setTimeout(() => {
            this.saveSettings();
        }, 500);  // 500ms debounce
    }

    /**
     * Save page settings to the API
     */
    async saveSettings() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/${this.pageId}/settings/update/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify(this.currentValues)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to save page settings');
            }

            const data = await response.json();

            // Refresh the preview if header/footer changed
            if (this.currentValues.hide_header !== undefined ||
                this.currentValues.hide_footer !== undefined ||
                this.currentValues.header_template_id !== undefined ||
                this.currentValues.footer_template_id !== undefined) {
                this.refreshHeaderFooterPreview();
            }

            showNotification('Page settings saved', 'success');
            return data;
        } catch (error) {
            console.error('Error saving page settings:', error);
            showNotification('Failed to save page settings: ' + error.message, 'error');
            throw error;
        }
    }

    /**
     * Refresh header/footer in the live preview
     */
    refreshHeaderFooterPreview() {
        // Trigger a preview refresh
        if (window.livePreview && typeof window.livePreview.refresh === 'function') {
            window.livePreview.refresh();
        }
    }

    /**
     * Get CSRF token from cookies
     */
    getCsrfToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /**
     * Enter page settings mode
     */
    enterPageSettingsMode() {
        this.isPageSettingsMode = true;

        // Add visual indicator to canvas
        const canvasFrame = document.querySelector('.canvas-frame');
        if (canvasFrame) {
            canvasFrame.classList.add('page-settings-mode');
        }

        // Deselect any selected elements
        if (typeof deselectAllElements === 'function') {
            deselectAllElements();
        } else if (window.builderInstance && typeof window.builderInstance.deselectElement === 'function') {
            window.builderInstance.deselectElement();
        }
    }

    /**
     * Exit page settings mode
     */
    exitPageSettingsMode() {
        this.isPageSettingsMode = false;

        // Remove visual indicator from canvas
        const canvasFrame = document.querySelector('.canvas-frame');
        if (canvasFrame) {
            canvasFrame.classList.remove('page-settings-mode');
        }
    }
}

// Global page settings manager instance
let pageSettingsManager = null;

/**
 * Open page settings panel
 * Called from toolbar button or canvas click
 */
async function openPageSettings() {
    // Get page ID from the builder
    const pageId = window.builderInstance?.pageId ||
                   document.querySelector('[data-page-id]')?.dataset.pageId ||
                   window.PAGE_ID;

    if (!pageId) {
        console.error('Page ID not found');
        showNotification('Could not determine page ID', 'error');
        return;
    }

    // Initialize page settings manager if needed
    if (!pageSettingsManager || pageSettingsManager.pageId !== pageId) {
        pageSettingsManager = new PageSettingsManager(pageId, '/api/page-builder/page');
    }

    try {
        // Enter page settings mode
        pageSettingsManager.enterPageSettingsMode();

        // Load settings from API
        await pageSettingsManager.loadSettings();

        // Render in properties panel
        pageSettingsManager.renderSettingsPanel('properties-panel');

    } catch (error) {
        console.error('Error opening page settings:', error);
    }
}

/**
 * Setup canvas click handler for opening page settings
 */
function setupCanvasClickHandler() {
    const canvasContent = document.querySelector('.canvas-content');
    if (!canvasContent) return;

    canvasContent.addEventListener('click', (e) => {
        // Check if click was directly on canvas content (not on elements or drop zones)
        if (e.target === canvasContent ||
            e.target.classList.contains('canvas-frame') ||
            e.target.classList.contains('canvas-container')) {
            // Don't trigger if we're dragging
            if (document.body.classList.contains('is-dragging-element')) {
                return;
            }
            openPageSettings();
        }
    });
}

// Initialize canvas click handler when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    setupCanvasClickHandler();
});

// Make page settings functions available globally
window.PageSettingsManager = PageSettingsManager;
window.pageSettingsManager = pageSettingsManager;
window.openPageSettings = openPageSettings;
window.setupCanvasClickHandler = setupCanvasClickHandler;

// --- Page Thumbnail Capture ---
function triggerThumbnailCapture(pageId, slug) {
    if (!slug || !pageId) return;

    var captureFrame = document.createElement('iframe');
    captureFrame.style.cssText = 'position:fixed;left:-9999px;top:-9999px;width:1280px;height:960px;border:none;opacity:0;pointer-events:none;z-index:-1;';
    captureFrame.src = window.adminPageBuilderPrefix + 'preview/' + encodeURIComponent(slug) + '/?capture=1';
    document.body.appendChild(captureFrame);

    var timeout = setTimeout(cleanup, 30000);

    function onMsg(e) {
        if (e.origin !== location.origin) return;
        if (e.data && e.data.type === 'page-thumbnail-captured') {
            fetch(builderInstance.getApiBaseUrl() + '/page/' + pageId + '/capture-thumbnail/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': builderInstance.getCSRFToken()
                },
                body: JSON.stringify({ image_data: e.data.imageData })
            }).catch(function(err) { console.error('[PageThumbnail] Upload failed:', err); });
            cleanup();
        } else if (e.data && e.data.type === 'page-thumbnail-error') {
            cleanup();
        }
    }

    function cleanup() {
        clearTimeout(timeout);
        window.removeEventListener('message', onMsg);
        if (captureFrame.parentNode) captureFrame.remove();
    }

    window.addEventListener('message', onMsg);
}