/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Shipping Method Admin List View JavaScript
 * Handles card selection, bulk actions, filtering, and method management
 */

(function () {
  'use strict';

  // State management
  const state = {
    selectedMethods: new Set(),
    allMethods: [],
    filteredMethods: [],
    currentFilters: {
      status: '',
      type: '',
      search: '',
    },
  };

  // DOM elements
  const elements = {};

  /**
   * Initialize the application
   */
  function init() {
    // Wait for DOM to be fully loaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initializeApp);
    } else {
      initializeApp();
    }
  }

  /**
   * Initialize app after DOM is ready
   */
  function initializeApp() {
    cacheElements();
    if (!elements.methodsContainer) {
      console.warn('Shipping methods container not found');
      return;
    }
    collectMethodData();
    attachEventListeners();
  }

  /**
   * Cache frequently accessed DOM elements
   */
  function cacheElements() {
    elements.methodsContainer = document.querySelector('.methods-container');
    elements.methodCards = document.querySelectorAll('.method-card');
    elements.selectAllCheckbox = document.getElementById('select-all-methods');
    elements.bulkActionSelect = document.getElementById('bulk-action-select');
    elements.applyBulkActionBtn = document.getElementById('apply-bulk-action');
    elements.selectedCount = document.getElementById('selected-count');
    elements.selectedNumber = document.getElementById('selected-number');
    elements.statusFilter = document.getElementById('status-filter');
    elements.typeFilter = document.getElementById('type-filter');
    elements.clearFiltersBtn = document.getElementById('clear-filters-btn');
    elements.searchInput = document.getElementById('method-search');
    elements.loadingOverlay = document.getElementById('loading-overlay');
    elements.notificationContainer = document.getElementById('notification-container');
  }

  /**
   * Collect method data from cards
   */
  function collectMethodData() {
    state.allMethods = Array.from(elements.methodCards).map(card => ({
      id: card.dataset.methodId,
      name: card.dataset.name,
      type: card.dataset.type,
      isActive: card.dataset.isActive === 'true',
      element: card,
    }));
    state.filteredMethods = [...state.allMethods];
  }

  /**
   * Attach event listeners
   */
  function attachEventListeners() {
    // Select all checkbox
    if (elements.selectAllCheckbox) {
      elements.selectAllCheckbox.addEventListener('change', handleSelectAll);
    }

    // Individual method checkboxes
    elements.methodCards.forEach(card => {
      const checkbox = card.querySelector('.method-select');
      if (checkbox) {
        checkbox.addEventListener('change', () => handleMethodSelect(card, checkbox));
      }

      // Toggle button
      const toggleBtn = card.querySelector('.method-toggle-btn');
      if (toggleBtn) {
        toggleBtn.addEventListener('click', e => {
          e.preventDefault();
          handleToggleMethod(toggleBtn);
        });
      }

      // Delete button
      const deleteBtn = card.querySelector('.delete-btn');
      if (deleteBtn) {
        deleteBtn.addEventListener('click', e => {
          e.preventDefault();
          handleDeleteMethod(deleteBtn);
        });
      }
    });

    // Bulk action button
    if (elements.applyBulkActionBtn) {
      elements.applyBulkActionBtn.addEventListener('click', handleBulkAction);
    }

    // Filters
    if (elements.statusFilter) {
      elements.statusFilter.addEventListener('change', handleFilterChange);
    }
    if (elements.typeFilter) {
      elements.typeFilter.addEventListener('change', handleFilterChange);
    }
    if (elements.clearFiltersBtn) {
      elements.clearFiltersBtn.addEventListener('click', clearFilters);
    }

    // Search with debounce
    if (elements.searchInput) {
      let searchTimeout;
      elements.searchInput.addEventListener('input', e => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          state.currentFilters.search = e.target.value.toLowerCase();
          applyFilters();
        }, 300);
      });
    }
  }

  /**
   * Handle select all checkbox
   */
  function handleSelectAll(e) {
    const checked = e.target.checked;
    elements.methodCards.forEach(card => {
      const checkbox = card.querySelector('.method-select');
      if (checkbox && card.style.display !== 'none') {
        checkbox.checked = checked;
        if (checked) {
          state.selectedMethods.add(card.dataset.methodId);
          card.classList.add('selected');
        } else {
          state.selectedMethods.delete(card.dataset.methodId);
          card.classList.remove('selected');
        }
      }
    });
    updateSelectionUI();
  }

  /**
   * Handle individual method selection
   */
  function handleMethodSelect(card, checkbox) {
    if (checkbox.checked) {
      state.selectedMethods.add(card.dataset.methodId);
      card.classList.add('selected');
    } else {
      state.selectedMethods.delete(card.dataset.methodId);
      card.classList.remove('selected');
    }
    updateSelectionUI();
  }

  /**
   * Update selection UI
   */
  function updateSelectionUI() {
    const count = state.selectedMethods.size;

    // Update selected count
    if (elements.selectedNumber) {
      elements.selectedNumber.textContent = count;
    }
    if (elements.selectedCount) {
      elements.selectedCount.style.display = count > 0 ? 'inline' : 'none';
    }

    // Update bulk action button
    if (elements.applyBulkActionBtn) {
      elements.applyBulkActionBtn.disabled = count === 0;
    }

    // Update select all checkbox
    if (elements.selectAllCheckbox) {
      const visibleMethods = state.filteredMethods.length;
      elements.selectAllCheckbox.checked = count > 0 && count === visibleMethods;
      elements.selectAllCheckbox.indeterminate = count > 0 && count < visibleMethods;
    }
  }

  /**
   * Handle bulk action execution
   */
  function handleBulkAction() {
    const action = elements.bulkActionSelect.value;
    if (!action || state.selectedMethods.size === 0) return;

    const methodIds = Array.from(state.selectedMethods);

    switch (action) {
      case 'enable':
        confirmBulkAction('Enable', methodIds, performBulkEnable);
        break;
      case 'disable':
        confirmBulkAction('Disable', methodIds, performBulkDisable);
        break;
      case 'delete':
        confirmBulkAction('Delete', methodIds, performBulkDelete);
        break;
    }
  }

  /**
   * Confirm bulk action
   */
  async function confirmBulkAction(action, methodIds, callback) {
    const count = methodIds.length;
    const message = `Are you sure you want to ${action.toLowerCase()} ${count} shipping method${count !== 1 ? 's' : ''}?`;

    if (await AdminModal.confirm(message)) {
      callback(methodIds);
    }
  }

  /**
   * Perform bulk enable
   */
  function performBulkEnable(methodIds) {
    executeBulkMethodAction('enable', methodIds);
  }

  /**
   * Perform bulk disable
   */
  function performBulkDisable(methodIds) {
    executeBulkMethodAction('disable', methodIds);
  }

  /**
   * Perform bulk delete
   */
  function performBulkDelete(methodIds) {
    executeBulkMethodAction('delete', methodIds);
  }

  /**
   * Execute bulk action via AJAX
   */
  function executeBulkMethodAction(action, methodIds) {
    showLoading();

    const csrfToken =
      document.querySelector('meta[name="csrf-token"]')?.content ||
      document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    fetch(window.location.pathname + 'bulk-action/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        action: action,
        method_ids: methodIds,
      }),
    })
      .then(response => response.json())
      .then(data => {
        hideLoading();
        if (data.success) {
          showNotification(data.message || 'Action completed successfully', 'success');
          setTimeout(() => window.location.reload(), 1000);
        } else {
          showNotification(data.message || 'Action failed', 'error');
        }
        clearSelection();
      })
      .catch(error => {
        hideLoading();
        showNotification('An error occurred: ' + error.message, 'error');
        clearSelection();
      });
  }

  /**
   * Handle toggle method active/inactive
   */
  function handleToggleMethod(button) {
    const methodId = button.dataset.methodId;
    const isActive = button.dataset.isActive === 'true';
    const newStatus = !isActive;

    const card = button.closest('.method-card');
    showLoading();

    // Simulate AJAX call
    setTimeout(() => {
      updateMethodStatus(card, newStatus);
      button.dataset.isActive = newStatus.toString();

      hideLoading();
      showNotification(`Method ${newStatus ? 'enabled' : 'disabled'} successfully`, 'success');
    }, 300);
  }

  /**
   * Update method status in UI
   */
  function updateMethodStatus(card, isActive) {
    card.dataset.isActive = isActive.toString();

    // Update status badge
    const statusBadge = card.querySelector('.status-badge');
    if (statusBadge) {
      statusBadge.className = isActive
        ? 'status-badge status-active'
        : 'status-badge status-inactive';
      statusBadge.innerHTML = isActive
        ? '<i class="fas fa-check-circle"></i> Active'
        : '<i class="fas fa-times-circle"></i> Inactive';
    }

    // Update toggle button
    const toggleBtn = card.querySelector('.method-toggle-btn');
    if (toggleBtn) {
      toggleBtn.innerHTML = `<i class="fas fa-toggle-${isActive ? 'on' : 'off'}"></i>`;
      toggleBtn.dataset.isActive = isActive.toString();
    }
  }

  /**
   * Handle delete method
   */
  async function handleDeleteMethod(button) {
    const methodId = button.dataset.methodId;
    const methodName = button.dataset.methodName;

    if (
      !(await AdminModal.confirm({
        message: `Are you sure you want to delete "${methodName}"?`,
        danger: true,
        confirmText: 'Delete',
      }))
    ) {
      return;
    }

    showLoading();

    // Simulate AJAX call
    setTimeout(() => {
      const card = button.closest('.method-card');
      card.remove();

      // Update state
      state.allMethods = state.allMethods.filter(m => m.id !== methodId);
      state.selectedMethods.delete(methodId);
      collectMethodData();
      updateSelectionUI();

      hideLoading();
      showNotification('Method deleted successfully', 'success');
    }, 300);
  }

  /**
   * Handle filter change
   */
  function handleFilterChange() {
    state.currentFilters.status = elements.statusFilter?.value || '';
    state.currentFilters.type = elements.typeFilter?.value || '';
    applyFilters();
  }

  /**
   * Apply all filters
   */
  function applyFilters() {
    state.filteredMethods = state.allMethods.filter(method => {
      // Status filter
      if (state.currentFilters.status) {
        const isActive = state.currentFilters.status === 'active';
        if (method.isActive !== isActive) return false;
      }

      // Type filter
      if (state.currentFilters.type && method.type !== state.currentFilters.type) {
        return false;
      }

      // Search filter
      if (
        state.currentFilters.search &&
        !method.name.toLowerCase().includes(state.currentFilters.search)
      ) {
        return false;
      }

      return true;
    });

    updateCardVisibility();
  }

  /**
   * Update card visibility based on filters
   */
  function updateCardVisibility() {
    const filteredIds = new Set(state.filteredMethods.map(m => m.id));

    elements.methodCards.forEach(card => {
      if (filteredIds.has(card.dataset.methodId)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  }

  /**
   * Clear all filters
   */
  function clearFilters() {
    if (elements.statusFilter) elements.statusFilter.value = '';
    if (elements.typeFilter) elements.typeFilter.value = '';
    if (elements.searchInput) elements.searchInput.value = '';

    state.currentFilters = {
      status: '',
      type: '',
      search: '',
    };

    applyFilters();
  }

  /**
   * Clear selection
   */
  function clearSelection() {
    state.selectedMethods.clear();
    elements.methodCards.forEach(card => {
      const checkbox = card.querySelector('.method-select');
      if (checkbox) checkbox.checked = false;
      card.classList.remove('selected');
    });
    if (elements.selectAllCheckbox) elements.selectAllCheckbox.checked = false;
    if (elements.bulkActionSelect) elements.bulkActionSelect.value = '';
    updateSelectionUI();
  }

  /**
   * Show loading overlay
   */
  function showLoading() {
    if (elements.loadingOverlay) {
      elements.loadingOverlay.style.display = 'flex';
    }
  }

  /**
   * Hide loading overlay
   */
  function hideLoading() {
    if (elements.loadingOverlay) {
      elements.loadingOverlay.style.display = 'none';
    }
  }

  /**
   * Show notification
   */
  function showNotification(message, type = 'success') {
    AdminModal.toast(message, type);
  }

  // Initialize on load
  init();
})();
