/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Shipping Zone Admin - Interactive Controls
 * Handles filtering, search, bulk actions, and AJAX operations
 */

(function() {
    'use strict';

    // =========================================================================
    // State Management
    // =========================================================================

    const state = {
        selectedZones: new Set(),
        filters: {
            status: '',
            priority: '',
            hasMethods: '',
            search: ''
        }
    };

    // =========================================================================
    // DOM Elements
    // =========================================================================

    const elements = {
        selectAllCheckbox: document.getElementById('select-all-zones'),
        zoneSelects: document.querySelectorAll('.zone-select'),
        bulkActionSelect: document.getElementById('bulk-action-select'),
        applyBulkActionBtn: document.getElementById('apply-bulk-action'),
        selectedCountDisplay: document.getElementById('selected-count'),
        selectedNumberDisplay: document.getElementById('selected-number'),
        statusFilter: document.getElementById('status-filter'),
        priorityFilter: document.getElementById('priority-filter'),
        methodsFilter: document.getElementById('methods-filter'),
        clearFiltersBtn: document.getElementById('clear-filters-btn'),
        searchInput: document.getElementById('zone-search'),
        loadingOverlay: document.getElementById('loading-overlay'),
        notificationContainer: document.getElementById('notification-container')
    };

    // =========================================================================
    // Initialization
    // =========================================================================

    function init() {
        console.log('🌐 Initializing Shipping Zone Admin...');

        setupEventListeners();
        updateSelectedCount();

        console.log('✅ Shipping Zone Admin initialized');
    }

    // =========================================================================
    // Event Listeners
    // =========================================================================

    function setupEventListeners() {
        // Selection
        if (elements.selectAllCheckbox) {
            elements.selectAllCheckbox.addEventListener('change', handleSelectAll);
        }

        elements.zoneSelects.forEach(checkbox => {
            checkbox.addEventListener('change', handleZoneSelect);
        });

        // Bulk Actions
        if (elements.applyBulkActionBtn) {
            elements.applyBulkActionBtn.addEventListener('click', handleBulkAction);
        }

        // Filters
        if (elements.statusFilter) {
            elements.statusFilter.addEventListener('change', handleStatusFilter);
        }

        if (elements.priorityFilter) {
            elements.priorityFilter.addEventListener('change', handlePriorityFilter);
        }

        if (elements.methodsFilter) {
            elements.methodsFilter.addEventListener('change', handleMethodsFilter);
        }

        if (elements.clearFiltersBtn) {
            elements.clearFiltersBtn.addEventListener('click', handleClearFilters);
        }

        // Search
        if (elements.searchInput) {
            let searchTimeout;
            elements.searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    handleSearch(e.target.value);
                }, 300);
            });
        }

        // Zone Actions
        document.querySelectorAll('.zone-toggle-btn').forEach(btn => {
            btn.addEventListener('click', handleToggleZone);
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', handleDeleteZone);
        });
    }

    // =========================================================================
    // Selection Handlers
    // =========================================================================

    function handleSelectAll(e) {
        const isChecked = e.target.checked;

        elements.zoneSelects.forEach(checkbox => {
            checkbox.checked = isChecked;
            const zoneId = checkbox.value;

            if (isChecked) {
                state.selectedZones.add(zoneId);
            } else {
                state.selectedZones.delete(zoneId);
            }
        });

        updateSelectedCount();
    }

    function handleZoneSelect(e) {
        const zoneId = e.target.value;

        if (e.target.checked) {
            state.selectedZones.add(zoneId);
        } else {
            state.selectedZones.delete(zoneId);
            if (elements.selectAllCheckbox) {
                elements.selectAllCheckbox.checked = false;
            }
        }

        updateSelectedCount();
    }

    function updateSelectedCount() {
        const count = state.selectedZones.size;

        if (elements.selectedCountDisplay) {
            elements.selectedCountDisplay.style.display = count > 0 ? 'inline' : 'none';
        }

        if (elements.selectedNumberDisplay) {
            elements.selectedNumberDisplay.textContent = count;
        }

        if (elements.applyBulkActionBtn) {
            elements.applyBulkActionBtn.disabled = count === 0;
        }
    }

    // =========================================================================
    // Bulk Actions
    // =========================================================================

    async function handleBulkAction() {
        const action = elements.bulkActionSelect.value;
        const count = state.selectedZones.size;

        if (!action || count === 0) return;

        const confirmMessages = {
            'enable': `Enable ${count} zone(s)?`,
            'disable': `Disable ${count} zone(s)?`,
            'delete': `Delete ${count} zone(s)? This action cannot be undone.`
        };

        const isDeleteAction = action === 'delete';
        const confirmed = isDeleteAction
            ? await AdminModal.confirm({ message: confirmMessages[action], danger: true, confirmText: 'Delete' })
            : await AdminModal.confirm(confirmMessages[action]);
        if (!confirmed) return;

        showLoading(true);

        try {
            const zoneIds = Array.from(state.selectedZones);

            switch (action) {
                case 'enable':
                    await bulkUpdateStatus(zoneIds, true);
                    showNotification('success', `${count} zone(s) enabled successfully`);
                    break;
                case 'disable':
                    await bulkUpdateStatus(zoneIds, false);
                    showNotification('success', `${count} zone(s) disabled successfully`);
                    break;
                case 'delete':
                    await bulkDelete(zoneIds);
                    showNotification('success', `${count} zone(s) deleted successfully`);
                    break;
            }

            // Reload page after action
            setTimeout(() => {
                window.location.reload();
            }, 1000);

        } catch (error) {
            console.error('Bulk action failed:', error);
            showNotification('error', `Failed to ${action}: ${error.message}`);
        } finally {
            showLoading(false);
        }
    }

    async function bulkUpdateStatus(zoneIds, isActive) {
        const response = await fetch(AdminUtils.buildAdminUrl('/admin/shipping/admin/shippingzone/bulk-action/'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': AdminUtils.getCsrfToken(),
            },
            body: JSON.stringify({
                action: isActive ? 'enable' : 'disable',
                zone_ids: zoneIds
            })
        });
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.message || 'Failed to update zones');
        }
    }

    async function bulkDelete(zoneIds) {
        const response = await fetch(AdminUtils.buildAdminUrl('/admin/shipping/admin/shippingzone/bulk-action/'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': AdminUtils.getCsrfToken(),
            },
            body: JSON.stringify({
                action: 'delete',
                zone_ids: zoneIds
            })
        });
        const data = await response.json();
        if (!data.success) {
            throw new Error(data.message || 'Failed to delete zones');
        }
    }

    // =========================================================================
    // Filter Handlers
    // =========================================================================

    function handleStatusFilter(e) {
        const value = e.target.value;
        state.filters.status = value;
        applyFilters();
    }

    function handlePriorityFilter(e) {
        const value = e.target.value;
        state.filters.priority = value;
        applyFilters();
    }

    function handleMethodsFilter(e) {
        const value = e.target.value;
        state.filters.hasMethods = value;
        applyFilters();
    }

    function handleSearch(value) {
        state.filters.search = value;
        applyFilters();
    }

    function handleClearFilters() {
        // Reset all filters
        state.filters = {
            status: '',
            priority: '',
            hasMethods: '',
            search: ''
        };

        // Reset UI
        if (elements.statusFilter) elements.statusFilter.value = '';
        if (elements.priorityFilter) elements.priorityFilter.value = '';
        if (elements.methodsFilter) elements.methodsFilter.value = '';
        if (elements.searchInput) elements.searchInput.value = '';

        // Apply filters (which will reload without filters)
        applyFilters();
    }

    function applyFilters() {
        const params = new URLSearchParams();

        // Status filter
        if (state.filters.status === 'active') {
            params.append('is_active', '1');
        } else if (state.filters.status === 'inactive') {
            params.append('is_active', '0');
        }

        // Priority filter
        if (state.filters.priority) {
            params.append('priority', state.filters.priority);
        }

        // Methods filter
        if (state.filters.hasMethods === 'with-methods') {
            params.append('has_methods', '1');
        } else if (state.filters.hasMethods === 'without-methods') {
            params.append('has_methods', '0');
        }

        // Search
        if (state.filters.search) {
            params.append('q', state.filters.search);
        }

        // Navigate to filtered URL
        const url = params.toString() ? `?${params.toString()}` : window.location.pathname;
        window.location.href = url;
    }

    // =========================================================================
    // Zone Actions
    // =========================================================================

    async function handleToggleZone(e) {
        e.preventDefault();
        const btn = e.currentTarget;
        const zoneId = btn.dataset.zoneId;
        const isActive = btn.dataset.isActive === 'true';

        if (!await AdminModal.confirm(`${isActive ? 'Disable' : 'Enable'} this zone?`)) return;

        showLoading(true);

        try {
            await toggleZoneStatus(zoneId, !isActive);
            showNotification('success', `Zone ${isActive ? 'disabled' : 'enabled'} successfully`);

            setTimeout(() => {
                window.location.reload();
            }, 1000);

        } catch (error) {
            console.error('Toggle zone failed:', error);
            showNotification('error', `Failed to toggle zone: ${error.message}`);
        } finally {
            showLoading(false);
        }
    }

    async function handleDeleteZone(e) {
        e.preventDefault();
        const btn = e.currentTarget;
        const zoneId = btn.dataset.zoneId;

        if (!await AdminModal.confirm({ message: 'Delete this zone? This action cannot be undone.', danger: true, confirmText: 'Delete' })) return;

        showLoading(true);

        try {
            await deleteZone(zoneId);
            showNotification('success', 'Zone deleted successfully');

            setTimeout(() => {
                window.location.reload();
            }, 1000);

        } catch (error) {
            console.error('Delete zone failed:', error);
            showNotification('error', `Failed to delete zone: ${error.message}`);
        } finally {
            showLoading(false);
        }
    }

    async function toggleZoneStatus(zoneId, isActive) {
        // TODO: Implement toggle status API call
        console.log('Toggle zone status:', zoneId, isActive);
        return new Promise(resolve => setTimeout(resolve, 500));
    }

    async function deleteZone(zoneId) {
        // TODO: Implement delete API call
        console.log('Delete zone:', zoneId);
        return new Promise(resolve => setTimeout(resolve, 500));
    }

    // =========================================================================
    // UI Helpers
    // =========================================================================

    function showLoading(show) {
        if (elements.loadingOverlay) {
            elements.loadingOverlay.style.display = show ? 'flex' : 'none';
        }
    }

    function showNotification(type, message) {
        AdminModal.toast(message, type || 'info');
    }

    // =========================================================================
    // Initialize on DOM Ready
    // =========================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
