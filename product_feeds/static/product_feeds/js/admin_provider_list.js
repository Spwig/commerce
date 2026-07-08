/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Product Feed Provider Account List Admin JavaScript
 * Handles bulk actions, filtering, and AJAX operations
 */

(function() {
    'use strict';

    // CSRF Token (via AdminUtils global)
    const csrfToken = AdminUtils.getCsrfToken();

    // Notification System
    function showNotification(message, type = 'info') {
        AdminModal.toast(message, type || 'info');
    }

    // Loading Overlay
    function showLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.classList.remove('hidden');
    }

    function hideLoading() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.classList.add('hidden');
    }

    // Selection Management
    let selectedProviders = new Set();

    function updateSelectedCount() {
        const countEl = document.getElementById('selected-count');
        const numberEl = document.getElementById('selected-number');
        const applyBtn = document.getElementById('apply-bulk-action');

        if (countEl && numberEl) {
            numberEl.textContent = selectedProviders.size;
            countEl.classList.toggle('hidden', selectedProviders.size === 0);
        }

        if (applyBtn) {
            applyBtn.disabled = selectedProviders.size === 0;
        }
    }

    function initCheckboxes() {
        // Individual checkboxes
        document.querySelectorAll('.provider-select').forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    selectedProviders.add(this.value);
                } else {
                    selectedProviders.delete(this.value);
                }
                updateSelectedCount();
            });
        });

        // Select all checkbox
        const selectAllCheckbox = document.getElementById('select-all-providers');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function() {
                const checkboxes = document.querySelectorAll('.provider-select');
                checkboxes.forEach(checkbox => {
                    checkbox.checked = this.checked;
                    if (this.checked) {
                        selectedProviders.add(checkbox.value);
                    } else {
                        selectedProviders.delete(checkbox.value);
                    }
                });
                updateSelectedCount();
            });
        }
    }

    // Filter Handlers
    function initFilters() {
        // Sync status filter
        const syncFilter = document.getElementById('sync-status-filter');
        if (syncFilter) {
            syncFilter.addEventListener('change', applyFilters);
        }

        // Active filter
        const activeFilter = document.getElementById('active-filter');
        if (activeFilter) {
            activeFilter.addEventListener('change', applyFilters);
        }

        // Component filter
        const componentFilter = document.getElementById('component-filter');
        if (componentFilter) {
            componentFilter.addEventListener('change', applyFilters);
        }

        // Search input
        const searchInput = document.getElementById('provider-search');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(applyFilters, 300);
            });
        }
    }

    function applyFilters() {
        const params = new URLSearchParams();

        const syncFilter = document.getElementById('sync-status-filter');
        const activeFilter = document.getElementById('active-filter');
        const componentFilter = document.getElementById('component-filter');
        const searchInput = document.getElementById('provider-search');

        if (syncFilter && syncFilter.value) {
            params.set('sync_status', syncFilter.value);
        }

        if (activeFilter && activeFilter.value) {
            params.set('is_active', activeFilter.value === 'active' ? '1' : '0');
        }

        if (componentFilter && componentFilter.value) {
            params.set('component', componentFilter.value);
        }

        if (searchInput && searchInput.value.trim()) {
            params.set('q', searchInput.value.trim());
        }

        const queryString = params.toString();
        window.location.href = window.location.pathname + (queryString ? '?' + queryString : '');
    }

    // Bulk Actions
    function initBulkActions() {
        const applyBtn = document.getElementById('apply-bulk-action');
        if (applyBtn) {
            applyBtn.addEventListener('click', handleBulkAction);
        }
    }

    async function handleBulkAction() {
        const select = document.getElementById('bulk-action-select');
        const action = select ? select.value : '';

        if (!action || selectedProviders.size === 0) {
            showNotification('Please select an action and at least one provider', 'warning');
            return;
        }

        const providerIds = Array.from(selectedProviders);

        if (action === 'delete') {
            if (!await AdminModal.confirm({ message: `Are you sure you want to delete ${providerIds.length} provider(s)?`, danger: true, confirmText: 'Delete' })) {
                return;
            }
        }

        showLoading();

        try {
            const response = await fetch(AdminUtils.buildAdminUrl('/admin/product-feeds/admin/bulk-action/'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    action: action,
                    provider_ids: providerIds
                })
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message || 'Action completed successfully', 'success');
                setTimeout(() => window.location.reload(), 1000);
            } else {
                showNotification(data.message || 'Action failed', 'error');
            }
        } catch (error) {
            console.error('Bulk action error:', error);
            showNotification('An error occurred while performing the action', 'error');
        } finally {
            hideLoading();
        }
    }

    // Quick Action Handlers
    function initQuickActions() {
        // Sync buttons
        document.querySelectorAll('.sync-btn').forEach(btn => {
            btn.addEventListener('click', handleSync);
        });

        // Toggle buttons
        document.querySelectorAll('.provider-toggle-btn').forEach(btn => {
            btn.addEventListener('click', handleToggle);
        });

        // Primary buttons
        document.querySelectorAll('.primary-btn').forEach(btn => {
            btn.addEventListener('click', handleSetPrimary);
        });

        // Delete buttons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', handleDelete);
        });
    }

    async function handleSync(e) {
        const providerId = e.currentTarget.dataset.providerId;
        const btn = e.currentTarget;
        const icon = btn.querySelector('i');

        // Add spinning animation
        icon.classList.add('fa-spin');

        try {
            const response = await fetch(AdminUtils.buildAdminUrl(`/admin/product-feeds/admin/${providerId}/sync/`), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message || 'Feed sync started', 'success');
                // Reload to show updated status
                setTimeout(() => window.location.reload(), 2000);
            } else {
                showNotification(data.message || 'Failed to start feed sync', 'error');
            }
        } catch (error) {
            console.error('Sync error:', error);
            showNotification('An error occurred while syncing the feed', 'error');
        } finally {
            icon.classList.remove('fa-spin');
        }
    }

    async function handleToggle(e) {
        const btn = e.currentTarget;
        const providerId = btn.dataset.providerId;
        const isActive = btn.dataset.isActive === 'true';

        try {
            const response = await fetch(AdminUtils.buildAdminUrl(`/admin/product-feeds/admin/${providerId}/toggle/`), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ is_active: !isActive })
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message || `Provider ${isActive ? 'disabled' : 'enabled'}`, 'success');
                setTimeout(() => window.location.reload(), 500);
            } else {
                showNotification(data.message || 'Failed to toggle provider', 'error');
            }
        } catch (error) {
            console.error('Toggle error:', error);
            showNotification('An error occurred while toggling the provider', 'error');
        }
    }

    async function handleSetPrimary(e) {
        const btn = e.currentTarget;
        const providerId = btn.dataset.providerId;
        const isPrimary = btn.dataset.isPrimary === 'true';

        if (isPrimary) {
            showNotification('This provider is already set as primary', 'info');
            return;
        }

        try {
            const response = await fetch(AdminUtils.buildAdminUrl(`/admin/product-feeds/admin/${providerId}/set-primary/`), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message || 'Provider set as primary', 'success');
                setTimeout(() => window.location.reload(), 500);
            } else {
                showNotification(data.message || 'Failed to set provider as primary', 'error');
            }
        } catch (error) {
            console.error('Set primary error:', error);
            showNotification('An error occurred', 'error');
        }
    }

    async function handleDelete(e) {
        const btn = e.currentTarget;
        const providerId = btn.dataset.providerId;
        const card = btn.closest('.provider-card');
        const providerName = card ? card.querySelector('.provider-name a')?.textContent?.trim() : 'this provider';

        if (!await AdminModal.confirm({ message: `Are you sure you want to delete "${providerName}"?`, danger: true, confirmText: 'Delete' })) {
            return;
        }

        showLoading();

        try {
            const response = await fetch(AdminUtils.buildAdminUrl(`/admin/product-feeds/admin/${providerId}/delete/`), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message || 'Provider deleted successfully', 'success');
                if (card) {
                    card.remove();
                } else {
                    setTimeout(() => window.location.reload(), 500);
                }
            } else {
                showNotification(data.message || 'Failed to delete provider', 'error');
            }
        } catch (error) {
            console.error('Delete error:', error);
            showNotification('An error occurred while deleting the provider', 'error');
        } finally {
            hideLoading();
        }
    }

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
        initCheckboxes();
        initFilters();
        initBulkActions();
        initQuickActions();
    });

})();
