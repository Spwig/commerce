/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Command Classes for Undo/Redo Operations
 * All commands now support DOM snapshots for instant undo/redo
 */

/**
 * Base Command Class
 */
class BaseCommand {
  constructor() {
    this.timestamp = Date.now();
    this.beforeSnapshot = null;
    this.afterSnapshot = null;
  }

  /**
   * Get command description for UI
   */
  getDescription() {
    return 'Action';
  }

  /**
   * Serialize command for storage
   */
  serialize() {
    return {
      type: this.constructor.name,
      timestamp: this.timestamp,
    };
  }

  /**
   * Execute command
   * @param {boolean} skipDOM - Skip DOM updates (used when restoring from snapshot)
   */
  async execute(skipDOM = false) {
    throw new Error('Execute method must be implemented');
  }

  /**
   * Undo command
   * @param {boolean} skipDOM - Skip DOM updates (used when restoring from snapshot)
   */
  async undo(skipDOM = false) {
    throw new Error('Undo method must be implemented');
  }
}

/**
 * Add Element Command
 */
class AddElementCommand extends BaseCommand {
  constructor(elementData, parentId, beforeElement = null) {
    super();
    this.elementData = elementData;
    this.parentId = parentId;
    this.beforeElement = beforeElement;
    this.createdElementId = null;
    this.createdElementHTML = null;
  }

  getDescription() {
    const elementType = this.elementData.element_type || 'element';
    return `Add ${elementType}`;
  }

  async execute(skipDOM = false) {
    // Create element via API
    const response = await window.apiClient.createElement(this.elementData);

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to add element: ${error}`);
    }

    const data = await response.json();
    this.createdElementId = data.element?.id;
    this.createdElementHTML = data.element?.html;

    // Update DOM if not skipping
    if (!skipDOM && this.createdElementHTML) {
      this.insertElementInDOM();
    }

    // Mark draft as dirty
    if (window.markDraftDirty) {
      window.markDraftDirty();
    }

    return data;
  }

  insertElementInDOM() {
    if (!this.createdElementHTML) return;

    // Find parent container
    let targetContainer = null;

    if (this.parentId !== null && this.parentId !== undefined) {
      // Try to find container by ID
      const parentElement = document.querySelector(`[data-element-id="${this.parentId}"]`);
      if (parentElement) {
        // Check for different container content areas (regular container, modal popup, etc.)
        targetContainer =
          parentElement.querySelector('.pb-container-content') ||
          parentElement.querySelector('.pb-modal-builder__inner') ||
          parentElement;
      }
    } else {
      // Add to page sections
      targetContainer = document.getElementById('page-elements');
    }

    if (targetContainer) {
      // Remove the empty zone drop indicator if this is the first element added
      // IMPORTANT: Use :scope > to only find DIRECT child empty zones, not nested ones
      const emptyZone = targetContainer.querySelector(':scope > .container-empty-zone');
      if (emptyZone) {
        emptyZone.remove();
      }

      // Create temporary div to hold HTML
      const temp = document.createElement('div');
      temp.innerHTML = this.createdElementHTML;
      const newElement = temp.firstElementChild;

      if (this.beforeElement) {
        const beforeEl = document.querySelector(`[data-element-id="${this.beforeElement}"]`);
        if (beforeEl && beforeEl.parentNode === targetContainer) {
          targetContainer.insertBefore(newElement, beforeEl);
        } else {
          targetContainer.appendChild(newElement);
        }
      } else {
        targetContainer.appendChild(newElement);
      }

      // Register the new element with StateManager
      if (window.pageStateManager && newElement) {
        // Extract element data from the DOM
        const elementData = window.pageStateManager.extractElementFromDOM(newElement);
        if (elementData) {
          // Determine the index where it was inserted
          let index = null;
          const parent = newElement.parentElement;
          if (parent) {
            const siblings = parent.querySelectorAll(
              ':scope > .element-wrapper, :scope > .container-child-wrapper > .element-wrapper'
            );
            index = Array.from(siblings).indexOf(newElement);

            // If element is wrapped in container-child-wrapper, get the actual element
            if (
              index === -1 &&
              newElement.parentElement?.classList.contains('container-child-wrapper')
            ) {
              const wrapper = newElement.parentElement;
              const wrapperSiblings = parent.querySelectorAll(':scope > .container-child-wrapper');
              index = Array.from(wrapperSiblings).indexOf(wrapper);
            }
          }

          // Add to StateManager
          window.pageStateManager.addElement(
            elementData,
            this.parentId || null,
            index >= 0 ? index : null
          );

          // Update ContentManager if available
          if (window.contentManager) {
            window.contentManager.loadElementContent(this.createdElementId);
          }
        }
      }

      // Reinitialize sortables if needed
      if (window.builderInstance) {
        window.builderInstance.initializePreviewSortables();
        // Structure view will be refreshed by the ELEMENT_ADDED event from StateManager
      }
    }
  }

  async undo(skipDOM = false) {
    if (!this.createdElementId) return;

    // Delete element via API
    const response = await window.apiClient.deleteElement(this.createdElementId);

    if (!response.ok) {
      throw new Error('Failed to delete element');
    }

    // Remove from DOM if not skipping
    if (!skipDOM) {
      this.removeElementFromDOM();
    }

    // Refresh structure view
    if (window.builderInstance) {
      window.builderInstance.refreshStructureView();
    }
  }

  removeElementFromDOM() {
    if (!this.createdElementId) return;

    const element = document.querySelector(`[data-element-id="${this.createdElementId}"]`);
    if (element) {
      element.remove();
    }
  }

  serialize() {
    return {
      ...super.serialize(),
      elementData: this.elementData,
      parentId: this.parentId,
      beforeElement: this.beforeElement,
      createdElementId: this.createdElementId,
    };
  }
}

/**
 * Delete Element Command
 */
class DeleteElementCommand extends BaseCommand {
  constructor(elementId) {
    super();
    this.elementId = elementId;
    this.elementSnapshot = null;
    this.parentId = null;
    this.elementHTML = null;
    this.elementPosition = null;
  }

  getDescription() {
    const elementType = this.elementSnapshot?.element_type || 'element';
    return `Delete ${elementType}`;
  }

  async execute(skipDOM = false) {
    // Check if DOM is already removed by StateManager
    if (this.domAlreadyRemoved) {
      skipDOM = true;
    }

    // Capture element data before deletion
    if (!skipDOM) {
      this.captureElementData();
    }

    // Get element data from API first
    const getResponse = await window.apiClient.getElement(this.elementId);
    if (getResponse.ok) {
      this.elementSnapshot = await getResponse.json();
    }

    // Delete element via API
    const response = await window.apiClient.deleteElement(this.elementId);

    if (!response.ok) {
      throw new Error('Failed to delete element');
    }

    // Remove from DOM if not skipping
    if (!skipDOM) {
      this.removeElementFromDOM();
    }

    // StateManager will handle structure view updates through subscriptions
    // No need to manually refresh structure view
  }

  captureElementData() {
    const element = document.querySelector(`[data-element-id="${this.elementId}"]`);
    if (element) {
      // Capture HTML
      this.elementHTML = element.outerHTML;

      // Capture position info
      const parent = element.parentElement;
      const siblings = parent ? Array.from(parent.children) : [];
      const index = siblings.indexOf(element);

      this.elementPosition = {
        parentId: parent?.closest('[data-element-id]')?.dataset?.elementId,
        parentClass: parent?.className,
        index: index,
        nextSiblingId: element.nextElementSibling?.dataset?.elementId,
        previousSiblingId: element.previousElementSibling?.dataset?.elementId,
      };

      // Capture parent ID (check regular container and modal popup)
      const parentWrapper =
        element.closest('.pb-container-content')?.closest('[data-element-id]') ||
        element.closest('.pb-modal-builder__inner')?.closest('[data-element-id]');
      this.parentId = parentWrapper?.dataset?.elementId;
    }
  }

  removeElementFromDOM() {
    const element = document.querySelector(`[data-element-id="${this.elementId}"]`);
    if (element) {
      // Check if this is the last element in a container
      const containerContent = element.closest('.pb-container-content');
      const parentContainer = containerContent?.closest('[data-element-id]');

      // Check if element is wrapped in container-child-wrapper (elements in containers are wrapped)
      const childWrapper = element.closest('.container-child-wrapper');
      if (childWrapper && childWrapper.parentElement === containerContent) {
        // Remove the wrapper instead of just the element
        childWrapper.remove();
      } else {
        element.remove();
      }

      // If container is now empty, add back the empty zone
      if (containerContent && parentContainer) {
        const remainingElements = containerContent.querySelectorAll(
          ':scope > .element-wrapper, :scope > .container-child-wrapper'
        );
        if (remainingElements.length === 0) {
          const containerId = parentContainer.dataset.elementId;
          const emptyZoneHTML = `
                        <div class="container-drop-zone container-empty-zone"
                             data-container-id="${containerId}"
                             style="
                               min-height: 80px;
                               border: 2px dashed var(--primary, #3b82f6);
                               border-radius: 8px;
                               display: flex;
                               align-items: center;
                               justify-content: center;
                               color: var(--primary, #3b82f6);
                               font-size: 14px;
                               background: rgba(59, 130, 246, 0.05);
                               transition: all 0.2s ease;
                               width: 100%;
                             ">
                          <div style="text-align: center; pointer-events: none;">
                            <i class="fas fa-plus-circle" style="font-size: 20px; margin-bottom: 4px; display: block;"></i>
                            Drop elements here
                          </div>
                        </div>
                    `;
          containerContent.insertAdjacentHTML('beforeend', emptyZoneHTML);

          // Setup drop zone for the new empty zone
          if (window.builderInstance) {
            const newZone = containerContent.querySelector('.container-empty-zone');
            if (newZone) {
              window.builderInstance.setupDropZone(
                newZone,
                window.builderInstance.handleDropElement.bind(window.builderInstance)
              );
              newZone.style.cursor = 'pointer';
              newZone.onclick = event => {
                window.builderInstance.showQuickAddMenu(event, 'container', containerId);
              };
            }
          }
        }
      }
    }
  }

  async undo(skipDOM = false) {
    if (!this.elementSnapshot) return;

    // Recreate element via API
    const elementData = {
      ...this.elementSnapshot,
      parent_element_id: this.parentId,
    };

    const response = await window.apiClient.createElement(elementData);

    if (!response.ok) {
      throw new Error('Failed to recreate element');
    }

    const data = await response.json();

    // Restore element in DOM if not skipping
    if (!skipDOM && this.elementHTML) {
      this.restoreElementInDOM();
    }

    // Refresh UI
    if (window.builderInstance) {
      window.builderInstance.refreshStructureView();
      window.builderInstance.initializePreviewSortables();
    }
  }

  restoreElementInDOM() {
    if (!this.elementHTML || !this.elementPosition) return;

    // Find parent
    let parent = null;
    if (this.elementPosition.parentId !== null && this.elementPosition.parentId !== undefined) {
      const parentElement = document.querySelector(
        `[data-element-id="${this.elementPosition.parentId}"]`
      );
      // Check for different container content areas (regular container, modal popup, etc.)
      parent =
        parentElement?.querySelector('.pb-container-content') ||
        parentElement?.querySelector('.pb-modal-builder__inner') ||
        parentElement;
    } else if (this.elementPosition.parentClass) {
      parent = document.querySelector(`.${this.elementPosition.parentClass.split(' ')[0]}`);
    }

    if (!parent) {
      parent = document.getElementById('page-elements');
    }

    if (parent) {
      // Remove empty zone if present (we're restoring an element)
      // IMPORTANT: Use :scope > to only find DIRECT child empty zones, not nested ones
      const emptyZone = parent.querySelector(':scope > .container-empty-zone');
      if (emptyZone) {
        emptyZone.remove();
      }

      // Create element from HTML
      const temp = document.createElement('div');
      temp.innerHTML = this.elementHTML;
      const element = temp.firstElementChild;

      // Insert at correct position
      if (this.elementPosition.nextSiblingId) {
        const nextSibling = parent.querySelector(
          `[data-element-id="${this.elementPosition.nextSiblingId}"]`
        );
        if (nextSibling) {
          parent.insertBefore(element, nextSibling);
        } else {
          parent.appendChild(element);
        }
      } else if (this.elementPosition.index >= 0) {
        const children = Array.from(parent.children);
        if (this.elementPosition.index < children.length) {
          parent.insertBefore(element, children[this.elementPosition.index]);
        } else {
          parent.appendChild(element);
        }
      } else {
        parent.appendChild(element);
      }
    }
  }

  serialize() {
    return {
      ...super.serialize(),
      elementId: this.elementId,
      elementSnapshot: this.elementSnapshot,
      parentId: this.parentId,
    };
  }
}

/**
 * Update Element Command
 */
class UpdateElementCommand extends BaseCommand {
  constructor(elementId, oldData, newData) {
    super();
    this.elementId = elementId;
    this.oldData = oldData;
    this.newData = newData;
    this.oldHTML = null;
    this.newHTML = null;
  }

  getDescription() {
    // Try to provide a meaningful description based on what changed
    if (this.newData.content?.text !== undefined) {
      return 'Update text';
    } else if (this.newData.style_overrides) {
      return 'Update styles';
    } else if (this.newData.layout_config) {
      return 'Update layout';
    }
    return 'Update element';
  }

  async execute(skipDOM = false) {
    // Capture old HTML
    if (!skipDOM && !this.oldHTML) {
      const element = document.querySelector(`[data-element-id="${this.elementId}"]`);
      if (element) {
        this.oldHTML = element.outerHTML;
      }
    }

    // Update element via API
    const response = await window.apiClient.updateElement(this.elementId, this.newData);

    if (!response.ok) {
      throw new Error('Failed to update element');
    }

    const data = await response.json();
    this.newHTML = data.element?.html;

    // Update DOM if not skipping
    if (!skipDOM && this.newHTML) {
      this.updateElementInDOM(this.newHTML);
    }

    return data;
  }

  async undo(skipDOM = false) {
    // Restore old data via API
    const response = await window.apiClient.updateElement(this.elementId, this.oldData);

    if (!response.ok) {
      throw new Error('Failed to restore element');
    }

    // Update DOM if not skipping
    if (!skipDOM && this.oldHTML) {
      this.updateElementInDOM(this.oldHTML);
    }
  }

  updateElementInDOM(html) {
    const element = document.querySelector(`[data-element-id="${this.elementId}"]`);
    if (element && html) {
      // Create new element from HTML
      const temp = document.createElement('div');
      temp.innerHTML = html;
      const newElement = temp.firstElementChild;

      // Replace old element
      element.parentNode.replaceChild(newElement, element);

      // Re-attach event handlers if needed
      if (window.builderInstance) {
        window.builderInstance.attachElementEventHandlers(newElement);
      }
    }
  }

  serialize() {
    return {
      ...super.serialize(),
      elementId: this.elementId,
      oldData: this.oldData,
      newData: this.newData,
    };
  }
}

/**
 * Move Element Command
 */
class MoveElementCommand extends BaseCommand {
  constructor(elementId, oldParentId, newParentId, oldIndex, newIndex, elementOrders) {
    super();
    this.elementId = elementId;
    this.oldParentId = oldParentId;
    this.newParentId = newParentId;
    this.oldIndex = oldIndex;
    this.newIndex = newIndex;
    this.elementOrders = elementOrders;
    this.previousOrders = null;
    this.parentChanged = false;
    this.actualNewParentId = null;
    this.actualNewParentType = null;
    this.oldPositionData = null;
    this.newPositionData = null;
  }

  getDescription() {
    if (this.parentChanged || this.oldParentId !== this.newParentId) {
      return 'Move element to new container';
    }
    return 'Reorder element';
  }

  async execute(skipDOM = false) {
    // Check if DOM was already moved by Sortable.js
    if (this.domAlreadyMoved) {
      skipDOM = true;
    }

    // Only capture state if not already captured (pre-captured in visual-builder.js)
    if (!this.stateSnapshot && window.pageStateManager) {
      this.stateSnapshot = window.pageStateManager.captureState();
    }
    if (window.contentManager) {
      this.contentSnapshot = window.contentManager.captureContent(this.elementId);
    }

    // Capture old position
    if (!skipDOM && !this.oldPositionData) {
      this.captureElementPosition(true);
    }

    // Store current orders before moving (for undo)
    if (!this.previousOrders && this.oldParentId) {
      const oldParentResponse = await window.apiClient.getElement(this.oldParentId);
      if (oldParentResponse.ok) {
        const oldParentData = await oldParentResponse.json();
        this.previousOrders = oldParentData.child_elements || [];
      }
    }

    // Build request body
    const requestBody = {
      element_orders: this.elementOrders,
    };

    // Add parent change info if applicable
    if (this.parentChanged) {
      requestBody.element_id = this.elementId;
      requestBody.new_parent_id = this.actualNewParentId || this.newParentId;
      requestBody.new_parent_type = this.actualNewParentType || 'container';
    } else if (this.newParentId) {
      requestBody.element_id = this.elementId;
      requestBody.new_parent_id = this.newParentId;
      requestBody.new_parent_type = 'container';
    }

    // Call the reorder API
    const response = await window.apiClient.reorderElements(requestBody);

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Failed to move element: ${error}`);
    }

    // Move element in DOM if not skipping
    if (!skipDOM) {
      this.moveElementInDOM();
      this.captureElementPosition(false);
    }

    // Mark draft as dirty
    if (window.markDraftDirty) {
      window.markDraftDirty();
    }

    // Clear the flag after execution
    this.domAlreadyMoved = false;

    return true;
  }

  captureElementPosition(isOld = true) {
    const element = document.querySelector(`[data-element-id="${this.elementId}"]`);
    if (!element) return;

    const parent = element.parentElement;
    const data = {
      parentElement: parent,
      parentId: parent?.closest('[data-element-id]')?.dataset?.elementId,
      siblings: parent ? Array.from(parent.children) : [],
      index: parent ? Array.from(parent.children).indexOf(element) : -1,
      nextSibling: element.nextElementSibling,
      previousSibling: element.previousElementSibling,
    };

    if (isOld) {
      this.oldPositionData = data;
    } else {
      this.newPositionData = data;
    }
  }

  moveElementInDOM() {
    const element = document.querySelector(`[data-element-id="${this.elementId}"]`);
    if (!element) return;

    let targetContainer = null;

    // Find target container
    if (this.newParentId || this.actualNewParentId) {
      const parentId = this.actualNewParentId || this.newParentId;
      const parentElement = document.querySelector(`[data-element-id="${parentId}"]`);
      if (parentElement) {
        // Check for different container content areas (regular container, modal popup, etc.)
        targetContainer =
          parentElement.querySelector('.pb-container-content') ||
          parentElement.querySelector('.pb-modal-builder__inner') ||
          parentElement;
      }
    } else {
      // Root level - moving to page-elements container
      targetContainer = document.getElementById('page-elements');
    }

    // Fallback to old position parent if no target found
    if (!targetContainer && this.oldPositionData?.parentElement) {
      targetContainer = this.oldPositionData.parentElement;
    }

    if (targetContainer && element.parentNode !== targetContainer) {
      // Move to new container
      const children = Array.from(targetContainer.children);
      if (this.newIndex < children.length) {
        targetContainer.insertBefore(element, children[this.newIndex]);
      } else {
        targetContainer.appendChild(element);
      }
    } else if (targetContainer) {
      // Reorder within same container
      const children = Array.from(targetContainer.children);
      const currentIndex = children.indexOf(element);

      if (currentIndex !== this.newIndex) {
        // Calculate the actual element to insert before
        let insertBeforeElement = null;

        if (this.newIndex > currentIndex) {
          // Moving down - since the element is still in the array,
          // we use newIndex directly (not +1) because when we move the element,
          // all indices shift
          if (this.newIndex < children.length) {
            insertBeforeElement = children[this.newIndex];
          }
        } else {
          // Moving up - straightforward
          insertBeforeElement = children[this.newIndex];
        }

        // Perform the move
        if (insertBeforeElement && insertBeforeElement !== element) {
          targetContainer.insertBefore(element, insertBeforeElement);
        } else if (!insertBeforeElement && currentIndex !== children.length - 1) {
          // Moving to the end
          targetContainer.appendChild(element);
        }
      }
    }

    // Reinitialize sortables
    if (window.builderInstance) {
      window.builderInstance.initializePreviewSortables();
    }
  }

  async undo(skipDOM = false) {
    // Restore state snapshots
    if (this.stateSnapshot && window.pageStateManager) {
      window.pageStateManager.restoreState(this.stateSnapshot);
      // State restore will trigger DOM updates via subscribers
      skipDOM = true;
    }
    if (this.contentSnapshot && window.contentManager) {
      window.contentManager.restoreContent(this.elementId, this.contentSnapshot);
    }

    // Build request to restore original position
    const requestBody = {
      element_orders: [],
    };

    // If we have previous orders, use them
    if (this.previousOrders && this.previousOrders.length > 0) {
      requestBody.element_orders = this.previousOrders;
    }

    // If parent changed, specify where to move back
    if (this.parentChanged && this.oldParentId) {
      requestBody.element_id = this.elementId;
      requestBody.new_parent_id = this.oldParentId;
      requestBody.new_parent_type = 'container';
    }

    // Make API call
    const response = await window.apiClient.reorderElements(requestBody);

    if (!response.ok) {
      throw new Error('Failed to undo element move');
    }

    // Restore position in DOM if not skipping
    if (!skipDOM && this.oldPositionData) {
      this.restoreElementPosition();
    }
  }

  restoreElementPosition() {
    if (!this.oldPositionData) return;

    const element = document.querySelector(`[data-element-id="${this.elementId}"]`);
    if (!element) return;

    const { parentElement, index, nextSibling } = this.oldPositionData;

    if (parentElement && element.parentNode !== parentElement) {
      // Move back to original parent
      if (nextSibling && nextSibling.parentNode === parentElement) {
        parentElement.insertBefore(element, nextSibling);
      } else if (index >= 0) {
        const children = Array.from(parentElement.children);
        if (index < children.length) {
          parentElement.insertBefore(element, children[index]);
        } else {
          parentElement.appendChild(element);
        }
      } else {
        parentElement.appendChild(element);
      }
    }

    // Reinitialize sortables
    if (window.builderInstance) {
      window.builderInstance.initializePreviewSortables();
    }
  }

  serialize() {
    return {
      ...super.serialize(),
      elementId: this.elementId,
      oldParentId: this.oldParentId,
      newParentId: this.newParentId,
      oldIndex: this.oldIndex,
      newIndex: this.newIndex,
      elementOrders: this.elementOrders,
      parentChanged: this.parentChanged,
    };
  }
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    BaseCommand,
    AddElementCommand,
    DeleteElementCommand,
    UpdateElementCommand,
    MoveElementCommand,
  };
}

// Make available globally
window.BaseCommand = BaseCommand;
window.AddElementCommand = AddElementCommand;
window.DeleteElementCommand = DeleteElementCommand;
window.UpdateElementCommand = UpdateElementCommand;
window.MoveElementCommand = MoveElementCommand;
