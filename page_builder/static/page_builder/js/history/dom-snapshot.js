/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * DOM Snapshot Manager
 * Captures and restores complete DOM state for undo/redo operations
 */

class DOMSnapshot {
    constructor() {
        this.previewContainer = null;
        this.structureContainer = null;
    }

    /**
     * Initialize containers
     */
    init() {
        this.previewContainer = document.getElementById('page-elements');
        this.structureContainer = document.getElementById('structure-tree');
    }

    /**
     * Capture complete DOM state
     */
    capture() {
        const snapshot = {
            timestamp: Date.now(),
            preview: this.capturePreview(),
            structure: this.captureStructure(),
            elements: this.captureElementsData(),
            selections: this.captureSelections(),
            scrollPositions: this.captureScrollPositions(),
            expandedNodes: this.captureExpandedNodes()
        };

        console.log('DOM Snapshot captured:', snapshot);
        return snapshot;
    }

    /**
     * Capture preview area state
     */
    capturePreview() {
        if (!this.previewContainer) return null;

        return {
            html: this.previewContainer.innerHTML,
            elements: this.captureElementsData()
        };
    }

    /**
     * Capture all elements data
     */
    captureElementsData() {
        const elements = {};
        const elementWrappers = document.querySelectorAll('.element-wrapper');

        elementWrappers.forEach(wrapper => {
            const elementId = wrapper.dataset.elementId;
            if (elementId) {
                elements[elementId] = {
                    id: elementId,
                    type: wrapper.dataset.elementType,
                    parentId: this.getParentElementId(wrapper),
                    order: this.getElementOrder(wrapper),
                    content: this.getElementContent(wrapper),
                    properties: this.getElementProperties(wrapper),
                    position: {
                        parent: wrapper.parentElement?.className,
                        previousSibling: wrapper.previousElementSibling?.dataset?.elementId,
                        nextSibling: wrapper.nextElementSibling?.dataset?.elementId
                    }
                };
            }
        });

        return elements;
    }

    /**
     * Get parent element ID
     */
    getParentElementId(element) {
        let parent = element.parentElement;
        while (parent) {
            if (parent.classList.contains('element-wrapper') && parent.dataset.elementId) {
                return parent.dataset.elementId;
            }
            if (parent.classList.contains('section-wrapper') && parent.dataset.sectionId) {
                return parent.dataset.sectionId;
            }
            parent = parent.parentElement;
        }
        return null;
    }

    /**
     * Get element order within parent
     */
    getElementOrder(element) {
        const parent = element.parentElement;
        if (!parent) return 0;

        const siblings = Array.from(parent.querySelectorAll(':scope > .element-wrapper'));
        return siblings.indexOf(element);
    }

    /**
     * Get element content
     */
    getElementContent(wrapper) {
        const content = {};

        // Text content
        const textElements = wrapper.querySelectorAll('[contenteditable="true"], .element-text, .element-content');
        textElements.forEach(el => {
            if (el.textContent) {
                content.text = el.textContent;
            }
        });

        // Image sources
        const images = wrapper.querySelectorAll('img');
        images.forEach(img => {
            content.imageSrc = img.src;
            content.imageAlt = img.alt;
        });

        // Links
        const links = wrapper.querySelectorAll('a');
        links.forEach(link => {
            content.href = link.href;
            content.linkText = link.textContent;
        });

        return content;
    }

    /**
     * Get element properties (styles, classes, etc.)
     */
    getElementProperties(wrapper) {
        return {
            className: wrapper.className,
            style: wrapper.getAttribute('style'),
            dataset: { ...wrapper.dataset }
        };
    }

    /**
     * Capture structure view state
     */
    captureStructure() {
        if (!this.structureContainer) return null;

        return {
            html: this.structureContainer.innerHTML,
            expandedNodes: this.captureExpandedNodes()
        };
    }

    /**
     * Capture current selections
     */
    captureSelections() {
        const selections = {
            selectedElement: null,
            activeContainer: null
        };

        // Find selected element
        const selected = document.querySelector('.element-wrapper.selected, .element-wrapper.active');
        if (selected) {
            selections.selectedElement = selected.dataset.elementId;
        }

        // Find active container
        const activeContainer = document.querySelector('.pb-container-content.active, .container-drop-zone.active');
        if (activeContainer) {
            const wrapper = activeContainer.closest('.element-wrapper');
            if (wrapper) {
                selections.activeContainer = wrapper.dataset.elementId;
            }
        }

        return selections;
    }

    /**
     * Capture scroll positions
     */
    captureScrollPositions() {
        return {
            window: {
                x: window.scrollX,
                y: window.scrollY
            },
            structureView: this.getStructureScrollPosition()
        };
    }

    /**
     * Get structure view scroll position
     */
    getStructureScrollPosition() {
        const structureWindow = document.querySelector('.structure-window');
        if (structureWindow) {
            const content = structureWindow.querySelector('.structure-content');
            if (content) {
                return {
                    x: content.scrollLeft,
                    y: content.scrollTop
                };
            }
        }
        return { x: 0, y: 0 };
    }

    /**
     * Capture expanded nodes in structure view
     */
    captureExpandedNodes() {
        const expanded = [];
        const expandedNodes = document.querySelectorAll('.structure-node.expanded');

        expandedNodes.forEach(node => {
            const elementId = node.dataset.elementId;
            if (elementId) {
                expanded.push(elementId);
            }
        });

        return expanded;
    }

    /**
     * Restore DOM from snapshot
     */
    async restore(snapshot) {
        if (!snapshot) {
            console.error('No snapshot to restore');
            return false;
        }

        console.log('Restoring DOM from snapshot:', snapshot);

        try {
            // Restore preview
            if (snapshot.preview && this.previewContainer) {
                await this.restorePreview(snapshot.preview);
            }

            // Restore structure view
            if (snapshot.structure && this.structureContainer) {
                await this.restoreStructure(snapshot.structure);
            }

            // Restore selections
            if (snapshot.selections) {
                this.restoreSelections(snapshot.selections);
            }

            // Restore scroll positions
            if (snapshot.scrollPositions) {
                this.restoreScrollPositions(snapshot.scrollPositions);
            }

            // Trigger events to update UI
            this.triggerRestoreEvents();

            return true;
        } catch (error) {
            console.error('Error restoring snapshot:', error);
            return false;
        }
    }

    /**
     * Restore preview area
     */
    async restorePreview(previewData) {
        if (this.previewContainer && previewData.html) {
            // Store current sortables
            const sortables = window.builderInstance?.previewSortables || [];

            // Destroy existing sortables
            sortables.forEach(sortable => {
                if (sortable && sortable.destroy) {
                    sortable.destroy();
                }
            });

            // Restore HTML
            this.previewContainer.innerHTML = previewData.html;

            // Clean up any Sortable.js classes that may have been captured in the snapshot
            const sortableClasses = ['sortable-chosen', 'sortable-ghost', 'sortable-drag'];
            sortableClasses.forEach(className => {
                this.previewContainer.querySelectorAll(`.${className}`).forEach(el => {
                    el.classList.remove(className);
                });
            });

            // Sync StateManager with restored DOM
            if (window.pageStateManager) {
                window.pageStateManager.loadStateFromDOM();
            }

            // Reload ContentManager from restored DOM
            if (window.contentManager) {
                window.contentManager.loadCurrentContent();
            }

            // Reinitialize sortables immediately to prevent race conditions
            if (window.builderInstance) {
                window.builderInstance.initializePreviewSortables();
            }

            // Restore element event handlers
            this.restoreElementEventHandlers();
        }
    }

    /**
     * Restore structure view
     */
    async restoreStructure(structureData) {
        if (this.structureContainer && structureData.html) {
            // Restore HTML
            this.structureContainer.innerHTML = structureData.html;

            // Clean up any Sortable.js classes that may have been captured in the snapshot
            const sortableClasses = ['sortable-chosen', 'sortable-ghost', 'sortable-drag'];
            sortableClasses.forEach(className => {
                this.structureContainer.querySelectorAll(`.${className}`).forEach(el => {
                    el.classList.remove(className);
                });
            });

            // Restore expanded nodes
            if (structureData.expandedNodes) {
                structureData.expandedNodes.forEach(nodeId => {
                    const node = this.structureContainer.querySelector(`[data-element-id="${nodeId}"]`);
                    if (node) {
                        node.classList.add('expanded');
                        const children = node.querySelector('.structure-children');
                        if (children) {
                            children.style.display = 'block';
                        }
                    }
                });
            }

            // Reinitialize structure view sortables immediately to prevent race conditions
            if (window.builderInstance) {
                window.builderInstance.initializeStructureSortables();
            }
        }
    }

    /**
     * Restore element event handlers
     */
    restoreElementEventHandlers() {
        // Use the built-in handler setup instead of trying to restore manually
        if (window.builderInstance && window.builderInstance.setupElementClickHandlers) {
            window.builderInstance.setupElementClickHandlers();
        }
        return;

        // Old code - disabled as it references non-existent methods
        /*
        // Re-attach click handlers for elements
        document.querySelectorAll('.element-wrapper').forEach(element => {
            element.addEventListener('click', function(e) {
                if (window.builderInstance) {
                    window.builderInstance.selectElement(this);
                }
            });
        });

        // Re-attach context menu handlers
        document.querySelectorAll('.element-wrapper').forEach(element => {
            element.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                if (window.builderInstance) {
                    window.builderInstance.showElementContextMenu(e, this);
                }
            });
        });
        */
    }

    /**
     * Restore selections
     */
    restoreSelections(selections) {
        // Restore selected element
        if (selections.selectedElement) {
            const element = document.querySelector(`[data-element-id="${selections.selectedElement}"]`);
            if (element) {
                element.classList.add('selected');
            }
        }

        // Restore active container
        if (selections.activeContainer) {
            const container = document.querySelector(`[data-element-id="${selections.activeContainer}"] .pb-container-content`);
            if (container) {
                container.classList.add('active');
            }
        }
    }

    /**
     * Restore scroll positions
     */
    restoreScrollPositions(positions) {
        // Restore window scroll
        if (positions.window) {
            window.scrollTo(positions.window.x, positions.window.y);
        }

        // Restore structure view scroll
        if (positions.structureView) {
            const structureWindow = document.querySelector('.structure-window');
            if (structureWindow) {
                const content = structureWindow.querySelector('.structure-content');
                if (content) {
                    content.scrollLeft = positions.structureView.x;
                    content.scrollTop = positions.structureView.y;
                }
            }
        }
    }

    /**
     * Trigger restore events
     */
    triggerRestoreEvents() {
        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('domSnapshotRestored', {
            detail: { timestamp: Date.now() }
        }));

        // Update element count in structure view
        const elementCount = document.querySelectorAll('.element-wrapper').length;
        const countDisplay = document.getElementById('structure-element-count');
        if (countDisplay) {
            countDisplay.textContent = elementCount;
        }
    }

    /**
     * Compare two snapshots
     */
    compare(snapshot1, snapshot2) {
        if (!snapshot1 || !snapshot2) return false;

        // Simple comparison based on element count and structure
        const elements1 = Object.keys(snapshot1.elements || {});
        const elements2 = Object.keys(snapshot2.elements || {});

        return elements1.length === elements2.length &&
               elements1.every(id => elements2.includes(id));
    }

    /**
     * Get snapshot size in bytes
     */
    getSize(snapshot) {
        return new Blob([JSON.stringify(snapshot)]).size;
    }

    /**
     * Compress snapshot for storage
     */
    compress(snapshot) {
        // Remove redundant HTML data, keep only essential structure
        const compressed = { ...snapshot };

        if (compressed.preview) {
            delete compressed.preview.html; // We can rebuild from elements data
        }

        if (compressed.structure) {
            delete compressed.structure.html; // We can rebuild from structure
        }

        return compressed;
    }
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DOMSnapshot;
}

// Make available globally
window.DOMSnapshot = DOMSnapshot;