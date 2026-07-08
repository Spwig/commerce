/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Shipping Promotion Admin - List View Interactions
 */

(function() {
    'use strict';

    // ========================================================================
    // State Management
    // ========================================================================

    const state = {
        selectedPromotions: new Set(),
        allPromotions: [],
        filteredPromotions: [],
        currentFilters: {
            status: '',
            type: '',
            priority: '',
            search: ''
        }
    };

    // ========================================================================
    // DOM Elements
    // ========================================================================

    let elements = {};

    function initElements() {
        elements = {
            // Bulk actions
            selectAllCheckbox: document.getElementById('select-all-promotions'),
            promotionCheckboxes: document.querySelectorAll('.rule-select'),
            bulkActionSelect: document.getElementById('bulk-action-select'),
            applyBulkActionBtn: document.getElementById('apply-bulk-action'),
            selectedCountDisplay: document.getElementById('selected-count'),
            selectedNumberDisplay: document.getElementById('selected-number'),

            // Filters
            statusFilter: document.getElementById('status-filter'),
            typeFilter: document.getElementById('type-filter'),
            priorityFilter: document.getElementById('priority-filter'),
            clearFiltersBtn: document.getElementById('clear-filters-btn'),
            promotionSearch: document.getElementById('promotion-search'),

            // Cards
            promotionCards: document.querySelectorAll('.rule-card'),
            toggleButtons: document.querySelectorAll('.rule-toggle-btn'),
            deleteButtons: document.querySelectorAll('.delete-btn'),

            // Overlays
            loadingOverlay: document.getElementById('loading-overlay'),
            notificationContainer: document.getElementById('notification-container')
        };
    }

    // ========================================================================
    // Initialization
    // ========================================================================

    function init() {
        initElements();
        collectPromotionData();
        attachEventListeners();
    }

    function collectPromotionData() {
        state.allPromotions = Array.from(elements.promotionCards).map(card => ({
            id: card.dataset.ruleId,
            name: card.dataset.name,
            type: card.dataset.type,
            priority: parseInt(card.dataset.priority),
            isActive: card.dataset.isActive === 'true',
            element: card
        }));
        state.filteredPromotions = [...state.allPromotions];
    }

    // ========================================================================
    // Event Listeners
    // ========================================================================

    function attachEventListeners() {
        // Select all checkbox
        if (elements.selectAllCheckbox) {
            elements.selectAllCheckbox.addEventListener('change', handleSelectAll);
        }

        // Individual rule checkboxes
        elements.promotionCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', handlePromotionSelect);
        });

        // Bulk actions
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
        if (elements.priorityFilter) {
            elements.priorityFilter.addEventListener('change', handleFilterChange);
        }
        if (elements.clearFiltersBtn) {
            elements.clearFiltersBtn.addEventListener('click', clearFilters);
        }

        // Search
        if (elements.promotionSearch) {
            let searchTimeout;
            elements.promotionSearch.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    state.currentFilters.search = e.target.value.toLowerCase();
                    applyFilters();
                }, 300);
            });
        }

        // Toggle buttons
        elements.toggleButtons.forEach(btn => {
            btn.addEventListener('click', handleTogglePromotion);
        });

        // Delete buttons
        elements.deleteButtons.forEach(btn => {
            btn.addEventListener('click', handleDeletePromotion);
        });
    }

    // ========================================================================
    // Selection Handlers
    // ========================================================================

    function handleSelectAll(e) {
        const isChecked = e.target.checked;

        elements.promotionCheckboxes.forEach(checkbox => {
            const card = checkbox.closest('.rule-card');
            if (!card.style.display || card.style.display !== 'none') {
                checkbox.checked = isChecked;
                if (isChecked) {
                    state.selectedPromotions.add(checkbox.value);
                    card.classList.add('selected');
                } else {
                    state.selectedPromotions.delete(checkbox.value);
                    card.classList.remove('selected');
                }
            }
        });

        updateSelectionUI();
    }

    function handlePromotionSelect(e) {
        const ruleId = e.target.value;
        const card = e.target.closest('.rule-card');

        if (e.target.checked) {
            state.selectedPromotions.add(ruleId);
            card.classList.add('selected');
        } else {
            state.selectedPromotions.delete(ruleId);
            card.classList.remove('selected');
        }

        updateSelectionUI();
    }

    function updateSelectionUI() {
        const count = state.selectedPromotions.size;

        // Update select all checkbox
        if (elements.selectAllCheckbox) {
            const visibleCheckboxes = Array.from(elements.promotionCheckboxes).filter(cb => {
                const card = cb.closest('.rule-card');
                return !card.style.display || card.style.display !== 'none';
            });
            elements.selectAllCheckbox.checked = count > 0 && count === visibleCheckboxes.length;
        }

        // Update selected count display
        if (elements.selectedCountDisplay && elements.selectedNumberDisplay) {
            elements.selectedNumberDisplay.textContent = count;
            elements.selectedCountDisplay.style.display = count > 0 ? 'inline' : 'none';
        }

        // Enable/disable bulk action button
        if (elements.applyBulkActionBtn) {
            elements.applyBulkActionBtn.disabled = count === 0;
        }
    }

    // ========================================================================
    // Bulk Actions
    // ========================================================================

    function handleBulkAction() {
        const action = elements.bulkActionSelect.value;
        if (!action || state.selectedPromotions.size === 0) return;

        const ruleIds = Array.from(state.selectedPromotions);

        switch (action) {
            case 'enable':
                confirmBulkAction('Enable', ruleIds, performBulkEnable);
                break;
            case 'disable':
                confirmBulkAction('Disable', ruleIds, performBulkDisable);
                break;
            case 'delete':
                confirmBulkAction('Delete', ruleIds, performBulkDelete);
                break;
        }
    }

    async function confirmBulkAction(actionName, ruleIds, callback) {
        const count = ruleIds.length;
        const message = `Are you sure you want to ${actionName.toLowerCase()} ${count} promotion${count !== 1 ? 's' : ''}?`;
        const isDangerous = actionName.toLowerCase() === 'delete';

        const confirmed = isDangerous
            ? await AdminModal.confirm({ message: message, danger: true, confirmText: actionName })
            : await AdminModal.confirm(message);

        if (confirmed) {
            callback(ruleIds);
        }
    }

    function performBulkEnable(ruleIds) {
        executeBulkPromotionAction('enable', ruleIds);
    }

    function performBulkDisable(ruleIds) {
        executeBulkPromotionAction('disable', ruleIds);
    }

    function performBulkDelete(ruleIds) {
        executeBulkPromotionAction('delete', ruleIds);
    }

    function executeBulkPromotionAction(action, ruleIds) {
        showLoading();
        fetch(AdminUtils.buildAdminUrl('/admin/shipping/admin/shippingpromotion/bulk-action/'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': AdminUtils.getCsrfToken(),
            },
            body: JSON.stringify({
                action: action,
                promotion_ids: ruleIds
            })
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

    function clearSelection() {
        state.selectedPromotions.clear();
        elements.promotionCheckboxes.forEach(checkbox => {
            checkbox.checked = false;
            checkbox.closest('.rule-card')?.classList.remove('selected');
        });
        updateSelectionUI();
        if (elements.bulkActionSelect) {
            elements.bulkActionSelect.value = '';
        }
    }

    // ========================================================================
    // Filter Handlers
    // ========================================================================

    function handleFilterChange(e) {
        const filterType = e.target.id.replace('-filter', '');
        state.currentFilters[filterType] = e.target.value;
        applyFilters();
    }

    function applyFilters() {
        state.filteredPromotions = state.allPromotions.filter(rule => {
            // Status filter
            if (state.currentFilters.status) {
                const isActive = state.currentFilters.status === 'active';
                if (rule.isActive !== isActive) return false;
            }

            // Type filter
            if (state.currentFilters.type && rule.type !== state.currentFilters.type) {
                return false;
            }

            // Priority filter
            if (state.currentFilters.priority) {
                const priority = rule.priority;
                if (state.currentFilters.priority === 'high' && priority < 50) return false;
                if (state.currentFilters.priority === 'medium' && (priority < 0 || priority >= 50)) return false;
                if (state.currentFilters.priority === 'low' && priority >= 0) return false;
            }

            // Search filter
            if (state.currentFilters.search && !rule.name.toLowerCase().includes(state.currentFilters.search)) {
                return false;
            }

            return true;
        });

        updateCardVisibility();
    }

    function updateCardVisibility() {
        const visibleIds = new Set(state.filteredPromotions.map(r => r.id));

        state.allPromotions.forEach(rule => {
            if (visibleIds.has(rule.id)) {
                rule.element.style.display = '';
            } else {
                rule.element.style.display = 'none';
            }
        });

        // Clear selection for hidden cards
        state.selectedPromotions.forEach(id => {
            if (!visibleIds.has(id)) {
                state.selectedPromotions.delete(id);
                const checkbox = document.querySelector(`.rule-select[value="${id}"]`);
                if (checkbox) checkbox.checked = false;
            }
        });

        updateSelectionUI();
    }

    function clearFilters() {
        // Reset filter selects
        if (elements.statusFilter) elements.statusFilter.value = '';
        if (elements.typeFilter) elements.typeFilter.value = '';
        if (elements.priorityFilter) elements.priorityFilter.value = '';
        if (elements.promotionSearch) elements.promotionSearch.value = '';

        // Reset state
        state.currentFilters = {
            status: '',
            type: '',
            priority: '',
            search: ''
        };

        // Reapply (which will show all)
        applyFilters();
    }

    // ========================================================================
    // Rule Actions
    // ========================================================================

    async function handleTogglePromotion(e) {
        e.preventDefault();
        const btn = e.currentTarget;
        const ruleId = btn.dataset.ruleId;
        const isActive = btn.dataset.isActive === 'true';
        const card = btn.closest('.rule-card');

        const action = isActive ? 'disable' : 'enable';
        if (await AdminModal.confirm(`Are you sure you want to ${actionName.toLowerCase()} ${count} promotion?`)) {
            showLoading();

            // Simulate AJAX call
            setTimeout(() => {
                const newState = !isActive;
                btn.dataset.isActive = newState;
                card.dataset.isActive = newState;
                updatePromotionCard(card, newState);
                hideLoading();
                showNotification(`Promotion ${action}d successfully`, 'success');
            }, 300);
        }
    }

    function updatePromotionCard(card, isActive) {
        const toggleBtn = card.querySelector('.rule-toggle-btn');
        const statusBadge = card.querySelector('.badge-status');

        if (toggleBtn) {
            toggleBtn.classList.toggle('active', isActive);
            toggleBtn.classList.toggle('inactive', !isActive);
            toggleBtn.title = isActive ? 'Disable' : 'Enable';
            toggleBtn.innerHTML = isActive
                ? '<i class="fas fa-toggle-on"></i>'
                : '<i class="fas fa-toggle-off"></i>';
        }

        if (statusBadge) {
            statusBadge.classList.toggle('badge-active', isActive);
            statusBadge.classList.toggle('badge-inactive', !isActive);
            statusBadge.innerHTML = isActive
                ? '<i class="fas fa-check-circle"></i> Active'
                : '<i class="fas fa-times-circle"></i> Inactive';
        }

        // Update rule in state
        const rule = state.allPromotions.find(r => r.id === card.dataset.ruleId);
        if (rule) {
            rule.isActive = isActive;
        }
    }

    async function handleDeletePromotion(e) {
        e.preventDefault();
        const btn = e.currentTarget;
        const ruleId = btn.dataset.ruleId;
        const card = btn.closest('.rule-card');
        const ruleName = card.dataset.name;

        if (await AdminModal.confirm({ message: `Are you sure you want to ${actionName.toLowerCase()} ${count} promotionName}"? This action cannot be undone.`, danger: true, confirmText: 'Delete' })) {
            showLoading();

            // Simulate AJAX call
            setTimeout(() => {
                card.remove();
                state.selectedPromotions.delete(ruleId);
                hideLoading();
                showNotification('Promotion deleted successfully', 'success');
                collectPromotionData();
                updateSelectionUI();
            }, 300);
        }
    }

    // ========================================================================
    // UI Helpers
    // ========================================================================

    function showLoading() {
        if (elements.loadingOverlay) {
            elements.loadingOverlay.style.display = 'flex';
        }
    }

    function hideLoading() {
        if (elements.loadingOverlay) {
            elements.loadingOverlay.style.display = 'none';
        }
    }

    function showNotification(message, type = 'info') {
        AdminModal.toast(message, type);
    }

    // ========================================================================
    // Initialize on DOM ready
    // ========================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
