/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin Variant Inline JavaScript
 * Handles initialization of media managers, color pickers, and other functionality for variant inlines
 */

(function () {
  'use strict';

  const variantMediaManagers = new Map(); // Store managers by variant index

  /**
   * Initialize media manager for a specific variant inline
   */
  function initVariantMediaManager(variantElement, variantIndex) {
    const gridId = `variant-images-grid-${variantIndex}`;
    const hiddenFieldId = `variant-images-data-${variantIndex}`;
    const addButtonId = `add-variant-media-btn-${variantIndex}`;

    // Check if elements exist
    const grid = document.getElementById(gridId);
    const hiddenField = document.getElementById(hiddenFieldId);
    const addButton = document.getElementById(addButtonId);

    if (!grid || !hiddenField || !addButton) {
      console.log(`[Variant ${variantIndex}] Missing elements, skipping media manager init`);
      return null;
    }

    // Create media manager instance
    const manager = new MediaManager({
      entityType: 'variant',
      entityId: variantIndex,
      gridContainerId: gridId,
      hiddenFieldId: hiddenFieldId,
      addButtonId: addButtonId,
      cardClass: 'variant-image-card',
    });

    variantMediaManagers.set(variantIndex, manager);
    console.log(`[Variant ${variantIndex}] Media manager initialized`);
    return manager;
  }

  /**
   * Initialize color picker for a variant's color_swatch field
   */
  function initColorPicker(variantElement, variantIndex) {
    const colorInput = variantElement.querySelector('[name*="color_swatch"]');
    const colorPickerBtn = variantElement.querySelector('.color-picker-trigger');
    const colorPreview = variantElement.querySelector('.color-preview');

    if (!colorInput) {
      return;
    }

    // Update preview on input change
    function updatePreview() {
      const color = colorInput.value;
      if (colorPreview && color) {
        colorPreview.style.backgroundColor = color;
        colorPreview.style.border = '1px solid #ccc';
      }
    }

    colorInput.addEventListener('input', updatePreview);
    colorInput.addEventListener('change', updatePreview);

    // Initialize preview
    updatePreview();

    // Check if ColorPickerUtility is available
    if (typeof window.ColorPickerUtility !== 'undefined') {
      // Use the advanced color picker utility
      const colorPicker = new window.ColorPickerUtility({
        showOpacity: false, // Hex color only for swatches
        onChange: function (color) {
          colorInput.value = color;
          updatePreview();
        },
      });

      // Remove the manual button if it exists (ColorPickerUtility.attach creates its own)
      if (colorPickerBtn) {
        colorPickerBtn.remove();
      }

      // Attach the color picker to the input
      colorPicker.attach(colorInput, colorInput.value || '');

      console.log(`[Variant ${variantIndex}] Color picker (ColorPickerUtility) initialized`);
    } else if (colorPickerBtn) {
      // Fallback: use native color input with the button we have in the template
      colorPickerBtn.addEventListener('click', function (e) {
        e.preventDefault();

        // Use native color input as fallback
        const tempInput = document.createElement('input');
        tempInput.type = 'color';
        tempInput.value = colorInput.value || '#000000';
        tempInput.style.position = 'absolute';
        tempInput.style.opacity = '0';
        document.body.appendChild(tempInput);

        tempInput.addEventListener('change', function () {
          colorInput.value = tempInput.value;
          updatePreview();
          document.body.removeChild(tempInput);
        });

        tempInput.click();
      });

      console.log(`[Variant ${variantIndex}] Color picker (native fallback) initialized`);
    }
  }

  /**
   * Initialize a single variant inline
   */
  function initVariantInline(variantElement) {
    const variantIndex = variantElement.dataset.variantIndex;

    if (!variantIndex) {
      console.warn('[Variant] No variant index found, skipping initialization');
      return;
    }

    console.log(`[Variant ${variantIndex}] Initializing...`);

    // Initialize media manager
    initVariantMediaManager(variantElement, variantIndex);

    // Initialize color picker
    initColorPicker(variantElement, variantIndex);
  }

  /**
   * Initialize all existing variant inlines
   */
  function initAllVariants() {
    const variantInlines = document.querySelectorAll('.variant-inline-item:not(.empty-form)');
    console.log(`[Variants] Found ${variantInlines.length} variant inline(s) to initialize`);

    variantInlines.forEach(function (variantElement) {
      initVariantInline(variantElement);
    });
  }

  /**
   * Handle dynamically added variants (when user clicks "Add another Variant")
   */
  function observeVariantAddition() {
    const variantInlineGroup = document.querySelector('.variant-inline-group');

    if (!variantInlineGroup) {
      console.log('[Variants] No variant inline group found');
      return;
    }

    // Use MutationObserver to detect new variant inlines
    const observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        mutation.addedNodes.forEach(function (node) {
          if (
            node.nodeType === 1 &&
            node.classList &&
            node.classList.contains('variant-inline-item')
          ) {
            // New variant added, but we need to wait for Django to finish rendering
            setTimeout(function () {
              initVariantInline(node);
            }, 100);
          }
        });
      });
    });

    observer.observe(variantInlineGroup, {
      childList: true,
      subtree: true,
    });

    console.log('[Variants] Mutation observer set up for dynamic variant addition');
  }

  /**
   * Get the product ID from the current URL
   */
  function getProductId() {
    const urlMatch = window.location.pathname.match(/\/admin\/catalog\/product\/(\d+)\//);
    return urlMatch ? urlMatch[1] : 'new';
  }

  /**
   * Get localStorage key for variant collapse state
   */
  function getStorageKey(productId, variantIndex) {
    return `variant_collapse_${productId}_${variantIndex}`;
  }

  /**
   * Save variant collapse state to localStorage
   */
  function saveCollapseState(productId, variantIndex, isOpen) {
    try {
      const key = getStorageKey(productId, variantIndex);
      localStorage.setItem(key, isOpen ? 'open' : 'closed');
    } catch (e) {
      console.warn('[Variants] Could not save collapse state:', e);
    }
  }

  /**
   * Get variant collapse state from localStorage
   */
  function getCollapseState(productId, variantIndex) {
    try {
      const key = getStorageKey(productId, variantIndex);
      return localStorage.getItem(key);
    } catch (e) {
      return null;
    }
  }

  /**
   * Initialize collapse functionality for all variants
   */
  function initializeVariantCollapse() {
    const productId = getProductId();
    const variantDetails = document.querySelectorAll('.variant-inline-item');

    if (variantDetails.length === 0) {
      return;
    }

    console.log(`[Variants] Initializing collapse for ${variantDetails.length} variant(s)`);

    // Restore collapse state from localStorage
    variantDetails.forEach(details => {
      const variantIndex = details.getAttribute('data-variant-index');

      // Skip the empty form template
      if (details.classList.contains('empty-form')) {
        return;
      }

      const state = getCollapseState(productId, variantIndex);

      // Restore saved state
      if (state === 'closed') {
        details.removeAttribute('open');
      } else if (state === 'open') {
        details.setAttribute('open', '');
      }
      // If no saved state, leave as default (open from template)

      // Listen for toggle events
      details.addEventListener('toggle', function () {
        const isOpen = details.hasAttribute('open');
        saveCollapseState(productId, variantIndex, isOpen);
      });
    });
  }

  /**
   * Collapse all variants
   */
  function collapseAllVariants() {
    const productId = getProductId();
    const variantDetails = document.querySelectorAll('.variant-inline-item:not(.empty-form)');

    variantDetails.forEach(details => {
      const variantIndex = details.getAttribute('data-variant-index');
      details.removeAttribute('open');
      saveCollapseState(productId, variantIndex, false);
    });

    console.log('[Variants] Collapsed all variants');
  }

  /**
   * Expand all variants
   */
  function expandAllVariants() {
    const productId = getProductId();
    const variantDetails = document.querySelectorAll('.variant-inline-item:not(.empty-form)');

    variantDetails.forEach(details => {
      const variantIndex = details.getAttribute('data-variant-index');
      details.setAttribute('open', '');
      saveCollapseState(productId, variantIndex, true);
    });

    console.log('[Variants] Expanded all variants');
  }

  /**
   * Add collapse control buttons to the Variations tab
   */
  function addCollapseButtons() {
    // Find the variations tab panel
    const variationsPanel = document.querySelector('[data-panel="variations"]');

    if (!variationsPanel) {
      return;
    }

    // Check if we already added buttons
    if (document.getElementById('variant-collapse-controls')) {
      return;
    }

    // Find the variant inline group
    const variantGroup = variationsPanel.querySelector('.variant-inline-group');

    if (!variantGroup) {
      return;
    }

    // Check if there are actual variants (not just the empty form)
    const realVariants = variantGroup.querySelectorAll('.variant-inline-item:not(.empty-form)');

    if (realVariants.length === 0) {
      return;
    }

    // Create controls container
    const controls = document.createElement('div');
    controls.id = 'variant-collapse-controls';
    controls.className = 'variant-collapse-controls';

    // Create Collapse All button
    const collapseAllBtn = document.createElement('button');
    collapseAllBtn.type = 'button';
    collapseAllBtn.className = 'button variant-collapse-btn';
    collapseAllBtn.innerHTML = '<i class="fas fa-compress-alt"></i> Collapse All';
    collapseAllBtn.addEventListener('click', collapseAllVariants);

    // Create Expand All button
    const expandAllBtn = document.createElement('button');
    expandAllBtn.type = 'button';
    expandAllBtn.className = 'button variant-expand-btn';
    expandAllBtn.innerHTML = '<i class="fas fa-expand-alt"></i> Expand All';
    expandAllBtn.addEventListener('click', expandAllVariants);

    // Add buttons to controls
    controls.appendChild(collapseAllBtn);
    controls.appendChild(expandAllBtn);

    // Insert controls before the variant group
    variantGroup.parentNode.insertBefore(controls, variantGroup);

    console.log('[Variants] Collapse control buttons added');
  }

  /**
   * Initialize everything when DOM is ready
   */
  function init() {
    console.log('[Variants] Initializing variant inline functionality...');

    // Wait for MediaManager to be available
    if (typeof MediaManager === 'undefined') {
      console.error('[Variants] MediaManager not loaded! Waiting...');
      setTimeout(init, 100);
      return;
    }

    initAllVariants();
    observeVariantAddition();
    initializeVariantCollapse();
    addCollapseButtons();
    initializeVariantStockManagement();
    bindStockTotalsUpdate();
    initializeVariantDeletion();

    console.log('[Variants] Initialization complete');
  }

  /**
   * Initialize AJAX deletion functionality for variants
   */
  function initializeVariantDeletion() {
    // Use event delegation for delete buttons
    document.addEventListener('click', function (e) {
      const deleteBtn = e.target.closest('.delete-variant-btn');
      if (!deleteBtn) return;

      // Prevent the click from toggling the details element
      e.preventDefault();
      e.stopPropagation();

      const variantId = deleteBtn.dataset.variantId;
      const variantName = deleteBtn.dataset.variantName || 'this variant';

      if (!variantId) {
        console.warn('[Variants] No variant ID found on delete button');
        return;
      }

      // Show confirmation dialog
      showDeleteConfirmation(variantId, variantName, deleteBtn);
    });

    console.log('[Variants] Delete functionality initialized');
  }

  /**
   * Show confirmation dialog before deleting a variant
   */
  function showDeleteConfirmation(variantId, variantName, deleteBtn) {
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.className = 'variant-delete-modal-overlay';
    overlay.innerHTML = `
            <div class="variant-delete-modal">
                <div class="modal-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3>Delete Variant?</h3>
                <p>Are you sure you want to delete <strong>"${escapeHtml(variantName)}"</strong>?</p>
                <p class="warning-text">This action cannot be undone. All stock records for this variant will also be deleted.</p>
                <div class="modal-actions">
                    <button type="button" class="cancel-btn">
                        <i class="fas fa-times"></i> Cancel
                    </button>
                    <button type="button" class="confirm-btn">
                        <i class="fas fa-trash"></i> Delete Variant
                    </button>
                </div>
            </div>
        `;

    // Add styles for the modal
    addDeleteModalStyles();

    // Add to DOM
    document.body.appendChild(overlay);

    // Focus trap and animation
    setTimeout(() => overlay.classList.add('visible'), 10);

    // Handle cancel
    const cancelBtn = overlay.querySelector('.cancel-btn');
    cancelBtn.addEventListener('click', function () {
      closeDeleteModal(overlay);
    });

    // Handle click outside modal
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) {
        closeDeleteModal(overlay);
      }
    });

    // Handle escape key
    const escapeHandler = function (e) {
      if (e.key === 'Escape') {
        closeDeleteModal(overlay);
        document.removeEventListener('keydown', escapeHandler);
      }
    };
    document.addEventListener('keydown', escapeHandler);

    // Handle confirm
    const confirmBtn = overlay.querySelector('.confirm-btn');
    confirmBtn.addEventListener('click', function () {
      closeDeleteModal(overlay);
      deleteVariant(variantId, deleteBtn);
    });
  }

  /**
   * Close and remove the delete confirmation modal
   */
  function closeDeleteModal(overlay) {
    overlay.classList.remove('visible');
    setTimeout(() => overlay.remove(), 200);
  }

  /**
   * Escape HTML to prevent XSS
   */
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Get the language prefix from the current URL
   */
  function getLanguagePrefix() {
    // Check if URL starts with a language code (e.g., /en/, /de/, /fr/)
    const match = window.location.pathname.match(/^\/([a-z]{2}(?:-[a-z]{2})?)\/admin/);
    return match ? '/' + match[1] : '';
  }

  /**
   * Delete a variant via AJAX
   */
  function deleteVariant(variantId, deleteBtn) {
    const variantItem = deleteBtn.closest('.variant-inline-item');

    // Show loading state
    deleteBtn.classList.add('deleting');
    variantItem.classList.add('deleting');

    // Get CSRF token
    const csrfToken =
      document.querySelector('[name=csrfmiddlewaretoken]')?.value || AdminUtils.getCsrfToken();

    // Build URL with language prefix
    const langPrefix = getLanguagePrefix();
    const deleteUrl = `${langPrefix}/admin/catalog/variant/${variantId}/delete/`;

    // Make AJAX request
    fetch(deleteUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
      },
      credentials: 'same-origin',
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Success - animate out and remove
          variantItem.classList.remove('deleting');
          variantItem.classList.add('deleted');

          // Update variant count badge
          updateVariantCount(-1);

          // Remove element after animation
          setTimeout(() => {
            variantItem.remove();

            // Show success notification
            showNotification(data.message || 'Variant deleted successfully', 'success');
          }, 300);
        } else {
          // Error - show message
          variantItem.classList.remove('deleting');
          deleteBtn.classList.remove('deleting');
          showNotification(data.error || 'Failed to delete variant', 'error');
        }
      })
      .catch(error => {
        console.error('[Variants] Delete error:', error);
        variantItem.classList.remove('deleting');
        deleteBtn.classList.remove('deleting');
        showNotification('Network error. Please try again.', 'error');
      });
  }

  /**
   * Update the variant count badge
   */
  function updateVariantCount(delta) {
    const badge = document.querySelector('.variant-count-badge');
    if (badge) {
      const currentCount = parseInt(badge.textContent) || 0;
      const newCount = Math.max(0, currentCount + delta);
      badge.textContent = newCount;
    }
  }

  /**
   * Show a notification message
   */
  function showNotification(message, type) {
    AdminModal.toast(message, type || 'info');
  }

  /**
   * Add styles for the delete confirmation modal
   */
  function addDeleteModalStyles() {
    if (document.getElementById('variant-delete-modal-styles')) return;

    const styles = document.createElement('style');
    styles.id = 'variant-delete-modal-styles';
    styles.textContent = `
            .variant-delete-modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                opacity: 0;
                transition: opacity 0.2s ease;
            }

            .variant-delete-modal-overlay.visible {
                opacity: 1;
            }

            .variant-delete-modal {
                background: var(--surface-primary, #fff);
                border-radius: 12px;
                padding: 30px;
                max-width: 420px;
                width: 90%;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                transform: scale(0.9);
                transition: transform 0.2s ease;
            }

            .variant-delete-modal-overlay.visible .variant-delete-modal {
                transform: scale(1);
            }

            .variant-delete-modal .modal-icon {
                width: 60px;
                height: 60px;
                background: #fef2f2;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px;
            }

            .variant-delete-modal .modal-icon i {
                font-size: 28px;
                color: #ef4444;
            }

            .variant-delete-modal h3 {
                margin: 0 0 12px;
                font-size: 20px;
                font-weight: 600;
                color: var(--text-primary, #1f2937);
            }

            .variant-delete-modal p {
                margin: 0 0 8px;
                font-size: 14px;
                color: var(--text-secondary, #6b7280);
                line-height: 1.5;
            }

            .variant-delete-modal p strong {
                color: var(--text-primary, #1f2937);
            }

            .variant-delete-modal .warning-text {
                font-size: 13px;
                color: #dc2626;
                background: #fef2f2;
                padding: 10px 14px;
                border-radius: 6px;
                margin-top: 12px;
            }

            .variant-delete-modal .modal-actions {
                display: flex;
                gap: 12px;
                justify-content: center;
                margin-top: 24px;
            }

            .variant-delete-modal button {
                padding: 10px 20px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                transition: all 0.2s ease;
                border: none;
            }

            .variant-delete-modal .cancel-btn {
                background: var(--surface-secondary, #f3f4f6);
                color: var(--text-primary, #374151);
            }

            .variant-delete-modal .cancel-btn:hover {
                background: var(--surface-tertiary, #e5e7eb);
            }

            .variant-delete-modal .confirm-btn {
                background: #ef4444;
                color: #fff;
            }

            .variant-delete-modal .confirm-btn:hover {
                background: #dc2626;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
            }

            /* Notification styles */
            .variant-notification {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 14px 20px;
                border-radius: 8px;
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 14px;
                font-weight: 500;
                z-index: 10001;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                opacity: 0;
                transform: translateY(20px);
                transition: all 0.3s ease;
            }

            .variant-notification.visible {
                opacity: 1;
                transform: translateY(0);
            }

            .variant-notification.success {
                background: #10b981;
                color: #fff;
            }

            .variant-notification.error {
                background: #ef4444;
                color: #fff;
            }

            .variant-notification i {
                font-size: 18px;
            }

            /* Dark theme support */
            [data-theme="dark"] .variant-delete-modal {
                background: #1e1e1e;
                border: 1px solid #333;
            }

            [data-theme="dark"] .variant-delete-modal h3 {
                color: #f3f4f6;
            }

            [data-theme="dark"] .variant-delete-modal p {
                color: #9ca3af;
            }

            [data-theme="dark"] .variant-delete-modal p strong {
                color: #f3f4f6;
            }

            [data-theme="dark"] .variant-delete-modal .warning-text {
                background: #7f1d1d;
                color: #fecaca;
            }

            [data-theme="dark"] .variant-delete-modal .cancel-btn {
                background: #374151;
                color: #f3f4f6;
            }

            [data-theme="dark"] .variant-delete-modal .cancel-btn:hover {
                background: #4b5563;
            }
        `;
    document.head.appendChild(styles);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /**
   * Initialize stock management for variants
   */
  function initializeVariantStockManagement() {
    const stockInputs = document.querySelectorAll('.stock-input');

    if (stockInputs.length === 0) {
      return;
    }

    console.log(
      `[Variants] Initializing stock management for ${stockInputs.length} stock input(s)`
    );

    // Track changes to stock inputs
    stockInputs.forEach(input => {
      input.addEventListener('change', function () {
        // Mark input as changed for visual feedback
        this.classList.add('stock-input-changed');

        // Update available stock display
        updateAvailableStock(this);
      });

      // Real-time input validation
      input.addEventListener('input', function () {
        if (this.value < 0) {
          this.value = 0;
        }
      });
    });

    console.log('[Variants] Stock management initialized');
  }

  /**
   * Update available stock display when on_hand changes
   */
  function updateAvailableStock(input) {
    // Find the row this input belongs to
    const row = input.closest('.stock-item-row');

    if (!row) {
      return;
    }

    // Get stock values
    const onHandInput = row.querySelector('.stock-on-hand');
    const allocatedCell = row.querySelector('.stock-allocated');
    const availableCell = row.querySelector('.stock-available strong');

    if (!onHandInput || !allocatedCell || !availableCell) {
      return;
    }

    const onHand = parseInt(onHandInput.value) || 0;
    const allocated = parseInt(allocatedCell.textContent) || 0;
    const available = onHand - allocated;

    // Update available display
    availableCell.textContent = available;

    // Add visual feedback based on availability
    const thresholdInput = row.querySelector('.stock-threshold');
    const threshold = parseInt(thresholdInput?.value) || 5;

    if (available <= 0) {
      availableCell.style.color = '#ef4444'; // Red
    } else if (threshold > 0 && available <= threshold) {
      availableCell.style.color = '#f59e0b'; // Orange
    } else {
      availableCell.style.color = ''; // Default
    }
  }

  /**
   * Update total stock displays
   */
  function updateStockTotals() {
    // Find all variant stock sections
    document.querySelectorAll('.variant-stock').forEach(stockSection => {
      const rows = stockSection.querySelectorAll('.stock-item-row');
      const totalRow = stockSection.querySelector('.stock-totals');

      if (!totalRow || rows.length === 0) {
        return;
      }

      let totalOnHand = 0;
      let totalAllocated = 0;
      let totalAvailable = 0;

      rows.forEach(row => {
        const onHand = parseInt(row.querySelector('.stock-on-hand')?.value) || 0;
        const allocated = parseInt(row.querySelector('.stock-allocated')?.textContent) || 0;

        totalOnHand += onHand;
        totalAllocated += allocated;
        totalAvailable += onHand - allocated;
      });

      // Update totals
      const totalCells = totalRow.querySelectorAll('td');
      if (totalCells.length >= 4) {
        totalCells[1].querySelector('strong').textContent = totalOnHand;
        totalCells[2].querySelector('strong').textContent = totalAllocated;
        totalCells[3].querySelector('strong').textContent = totalAvailable;
      }
    });
  }

  /**
   * Add stock totals update listener
   */
  function bindStockTotalsUpdate() {
    document.querySelectorAll('.stock-on-hand').forEach(input => {
      input.addEventListener('change', updateStockTotals);
    });
  }

  // Export functions for external use
  window.VariantCollapse = {
    collapseAll: collapseAllVariants,
    expandAll: expandAllVariants,
    init: initializeVariantCollapse,
  };

  window.VariantStock = {
    init: initializeVariantStockManagement,
    updateTotals: updateStockTotals,
  };

  window.VariantDelete = {
    init: initializeVariantDeletion,
    delete: deleteVariant,
    showConfirmation: showDeleteConfirmation,
  };
})();
