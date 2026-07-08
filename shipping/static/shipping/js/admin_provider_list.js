/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Provider Account List Admin JavaScript
 * Handles filtering, bulk actions, and quick actions for provider account management
 */

(function() {
    'use strict';

    // ========================================================================
    // Helper Functions
    // ========================================================================
    // Note: CSRF token and i18n URL handling now use global AdminUtils module

    /**
     * Show notification message
     */
    function showNotification(message, type = 'success') {
        AdminModal.toast(message, type);
    }

    /**
     * Show/hide loading overlay
     */
    function setLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = show ? 'flex' : 'none';
        }
    }

    /**
     * Get selected provider IDs
     */
    function getSelectedProviders() {
        const checkboxes = document.querySelectorAll('.provider-select:checked');
        return Array.from(checkboxes).map(cb => cb.value);
    }

    /**
     * Update selected count display
     */
    function updateSelectedCount() {
        const count = getSelectedProviders().length;
        const countDisplay = document.getElementById('selected-count');
        const numberDisplay = document.getElementById('selected-number');
        const applyButton = document.getElementById('apply-bulk-action');

        if (numberDisplay) numberDisplay.textContent = count;
        if (countDisplay) countDisplay.style.display = count > 0 ? 'inline' : 'none';
        if (applyButton) applyButton.disabled = count === 0;
    }

    // ========================================================================
    // Filter Handling
    // ========================================================================

    /**
     * Apply filters and reload provider list
     */
    function applyFilters() {
        const statusFilter = document.getElementById('status-filter');
        const activeFilter = document.getElementById('active-filter');
        const componentFilter = document.getElementById('component-filter');
        const searchInput = document.getElementById('provider-search');

        const params = new URLSearchParams(window.location.search);

        // Connection status filter
        if (statusFilter && statusFilter.value) {
            params.set('connection_status', statusFilter.value);
        } else {
            params.delete('connection_status');
        }

        // Active filter
        if (activeFilter && activeFilter.value) {
            if (activeFilter.value === 'active') {
                params.set('is_active', '1');
            } else if (activeFilter.value === 'inactive') {
                params.set('is_active', '0');
            }
        } else {
            params.delete('is_active');
        }

        // Component filter
        if (componentFilter && componentFilter.value) {
            params.set('component', componentFilter.value);
        } else {
            params.delete('component');
        }

        // Search
        if (searchInput && searchInput.value) {
            params.set('q', searchInput.value);
        } else {
            params.delete('q');
        }

        // Reload page with new filters
        window.location.search = params.toString();
    }

    /**
     * Debounce function for search
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ========================================================================
    // AJAX Actions
    // ========================================================================

    /**
     * Toggle provider active status
     */
    function toggleProviderActive(providerId, button) {
        const isActive = button.dataset.isActive === 'true';
        const card = button.closest('.provider-card');

        setLoading(true);

        fetch(AdminUtils.buildAdminUrl(`/admin/shipping/provideraccount/${providerId}/toggle-active/`), {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');

                // Update UI
                button.dataset.isActive = data.is_active;
                button.classList.toggle('active', data.is_active);
                button.classList.toggle('inactive', !data.is_active);
                button.title = data.is_active ? 'Disable' : 'Enable';
                button.innerHTML = data.is_active ? '<i class="fas fa-toggle-on"></i>' : '<i class="fas fa-toggle-off"></i>';

                // Update badge
                const badge = card.querySelector('.badge-status');
                if (badge) {
                    badge.className = `badge badge-status ${data.is_active ? 'badge-active' : 'badge-inactive'}`;
                    badge.innerHTML = data.is_active ? '<i class="fas fa-check-circle"></i> Active' : '<i class="fas fa-times-circle"></i> Inactive';
                }
            } else {
                showNotification(data.message || 'Failed to toggle provider status', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            setLoading(false);
        });
    }

    /**
     * Set provider as default
     */
    function setProviderDefault(providerId, button) {
        setLoading(true);

        fetch(AdminUtils.buildAdminUrl(`/admin/shipping/provideraccount/${providerId}/set-default/`), {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                // Reload page to update all default badges
                setTimeout(() => window.location.reload(), 500);
            } else {
                showNotification(data.message || 'Failed to set default provider', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            setLoading(false);
        });
    }

    /**
     * Test provider connection
     */
    function testProviderConnection(providerId, button) {
        const originalHtml = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        button.disabled = true;

        fetch(AdminUtils.buildAdminUrl(`/admin/shipping/provideraccount/${providerId}/test-connection/`), {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message || 'Connection test successful!', 'success');
                // Reload page to update connection status
                setTimeout(() => window.location.reload(), 1000);
            } else {
                showNotification(data.message || data.error || 'Connection test failed', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred during connection test.', 'error');
        })
        .finally(() => {
            button.innerHTML = originalHtml;
            button.disabled = false;
        });
    }

    /**
     * Delete provider
     */
    async function deleteProvider(providerId, button) {
        if (!await AdminModal.confirm({ message: 'Are you sure you want to delete this provider? This action cannot be undone.', danger: true, confirmText: 'Delete' })) {
            return;
        }

        setLoading(true);

        fetch(AdminUtils.buildAdminUrl(`/admin/shipping/provideraccount/${providerId}/delete/`), {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                // Remove card from UI
                const card = button.closest('.provider-card');
                if (card) {
                    card.style.opacity = '0';
                    setTimeout(() => card.remove(), 300);
                }
            } else {
                showNotification(data.message || 'Failed to delete provider', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        })
        .finally(() => {
            setLoading(false);
        });
    }

    /**
     * Handle bulk actions
     */
    async function applyBulkAction() {
        const action = document.getElementById('bulk-action-select').value;
        const providerIds = getSelectedProviders();

        if (!action || providerIds.length === 0) {
            showNotification('Please select an action and at least one provider', 'warning');
            return;
        }

        // Confirm for delete action
        if (action === 'delete') {
            if (!await AdminModal.confirm({ message: `Are you sure you want to delete ${providerIds.length} provider(s)? This action cannot be undone.`, danger: true, confirmText: 'Delete' })) {
                return;
            }
        }

        // Confirm for set_default action
        if (action === 'set_default' && providerIds.length !== 1) {
            showNotification('Please select exactly one provider to set as default', 'warning');
            return;
        }

        setLoading(true);

        fetch(AdminUtils.buildAdminUrl('/admin/shipping/provideraccount/bulk-action/'), {
            method: 'POST',
            headers: {
                'X-CSRFToken': AdminUtils.getCsrfToken(),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                action: action,
                provider_ids: providerIds,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                // Reload page after a short delay
                setTimeout(() => window.location.reload(), 500);
            } else {
                showNotification(data.message || 'Bulk action failed', 'error');
                setLoading(false);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('An error occurred. Please try again.', 'error');
            setLoading(false);
        });
    }

    // ========================================================================
    // Event Listeners
    // ========================================================================

    document.addEventListener('DOMContentLoaded', function() {
        // Select All functionality
        const selectAllCheckbox = document.getElementById('select-all-providers');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function() {
                const checkboxes = document.querySelectorAll('.provider-select');
                checkboxes.forEach(cb => cb.checked = this.checked);
                updateSelectedCount();
            });
        }

        // Individual checkbox selection
        document.addEventListener('change', function(e) {
            if (e.target.classList.contains('provider-select')) {
                updateSelectedCount();

                // Update select all checkbox
                const selectAll = document.getElementById('select-all-providers');
                const checkboxes = document.querySelectorAll('.provider-select');
                const checkedBoxes = document.querySelectorAll('.provider-select:checked');
                if (selectAll) {
                    selectAll.checked = checkboxes.length === checkedBoxes.length;
                }
            }
        });

        // Filter change handlers
        const statusFilter = document.getElementById('status-filter');
        const activeFilter = document.getElementById('active-filter');
        const componentFilter = document.getElementById('component-filter');

        if (statusFilter) statusFilter.addEventListener('change', applyFilters);
        if (activeFilter) activeFilter.addEventListener('change', applyFilters);
        if (componentFilter) componentFilter.addEventListener('change', applyFilters);

        // Search with debounce
        const searchInput = document.getElementById('provider-search');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(applyFilters, 500));
        }

        // Bulk action apply button
        const applyButton = document.getElementById('apply-bulk-action');
        if (applyButton) {
            applyButton.addEventListener('click', applyBulkAction);
        }

        // Quick action buttons
        document.addEventListener('click', function(e) {
            const button = e.target.closest('button');
            if (!button) return;

            const providerId = button.dataset.providerId;
            if (!providerId) return;

            if (button.classList.contains('provider-toggle-btn')) {
                e.preventDefault();
                toggleProviderActive(providerId, button);
            } else if (button.classList.contains('default-btn')) {
                e.preventDefault();
                setProviderDefault(providerId, button);
            } else if (button.classList.contains('test-btn')) {
                e.preventDefault();
                testProviderConnection(providerId, button);
            } else if (button.classList.contains('delete-btn')) {
                e.preventDefault();
                deleteProvider(providerId, button);
            }
        });
    });

})();
