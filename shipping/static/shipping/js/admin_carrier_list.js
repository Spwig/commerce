/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Carrier List Admin JavaScript
 * Handles filtering, bulk actions, and quick actions for carrier management
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
     * Get selected carrier IDs
     */
    function getSelectedCarriers() {
        const checkboxes = document.querySelectorAll('.carrier-select:checked');
        return Array.from(checkboxes).map(cb => cb.value);
    }

    /**
     * Update selected count display
     */
    function updateSelectedCount() {
        const count = getSelectedCarriers().length;
        const countDisplay = document.getElementById('selected-count');
        const numberDisplay = document.getElementById('selected-number');
        const applyButton = document.getElementById('apply-bulk-action');

        if (numberDisplay) numberDisplay.textContent = count;
        if (countDisplay) countDisplay.style.display = count > 0 ? 'inline' : 'none';
        if (applyButton) applyButton.disabled = count === 0;
    }

    // ========================================================================
    // Filter Handling (Client-Side)
    // ========================================================================

    /**
     * Apply filters to carrier cards (client-side, no page reload)
     */
    function applyFilters() {
        const countryFilter = document.getElementById('country-filter');
        const statusFilter = document.getElementById('status-filter');
        const typeFilter = document.getElementById('type-filter');
        const searchInput = document.getElementById('carrier-search');

        const selectedCountry = countryFilter ? countryFilter.value : '';
        const selectedStatus = statusFilter ? statusFilter.value : '';
        const selectedType = typeFilter ? typeFilter.value : '';
        const searchTerm = searchInput ? searchInput.value.toLowerCase().trim() : '';

        const carrierCards = document.querySelectorAll('.carrier-card');
        let visibleCount = 0;

        carrierCards.forEach(card => {
            let show = true;

            // Country filter
            if (selectedCountry) {
                const countryCode = card.dataset.country || 'NONE';
                if (countryCode !== selectedCountry) {
                    show = false;
                }
            }

            // Status filter
            if (selectedStatus && show) {
                const isActive = card.dataset.isActive === 'true';
                if (selectedStatus === 'active' && !isActive) {
                    show = false;
                } else if (selectedStatus === 'inactive' && isActive) {
                    show = false;
                }
            }

            // Type filter
            if (selectedType && show) {
                const isSystem = card.dataset.isSystem === 'true';
                if (selectedType === 'system' && !isSystem) {
                    show = false;
                } else if (selectedType === 'custom' && isSystem) {
                    show = false;
                }
            }

            // Search filter
            if (searchTerm && show) {
                const carrierName = (card.dataset.name || '').toLowerCase();
                const carrierSlug = (card.dataset.slug || '').toLowerCase();
                if (!carrierName.includes(searchTerm) && !carrierSlug.includes(searchTerm)) {
                    show = false;
                }
            }

            // Show/hide card with animation
            if (show) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Update results count if available
        updateResultsCount(visibleCount, carrierCards.length);
    }

    /**
     * Update results count display
     */
    function updateResultsCount(visible, total) {
        // You can add a results count element to the template if desired
        // For now, we'll just log it
        console.log(`Showing ${visible} of ${total} carriers`);
    }

    /**
     * Clear all filters
     */
    function clearAllFilters() {
        const countryFilter = document.getElementById('country-filter');
        const statusFilter = document.getElementById('status-filter');
        const typeFilter = document.getElementById('type-filter');
        const searchInput = document.getElementById('carrier-search');

        // Reset all filter values
        if (countryFilter) {
            countryFilter.value = '';
            // For searchable-select, we need to update both the select and the instance
            // Find the searchable-select instance by looking for the wrapper
            const wrapper = countryFilter.closest('.searchable-select-wrapper');
            if (wrapper) {
                // Update the hidden input that searchable-select uses
                const hiddenInput = wrapper.querySelector('input[type="hidden"]');
                if (hiddenInput) {
                    hiddenInput.value = '';
                }
                // Update the display text
                const valueText = wrapper.querySelector('.searchable-select-value-text');
                if (valueText) {
                    valueText.textContent = countryFilter.getAttribute('data-placeholder') || 'Search countries...';
                }
                // Clear the icon
                const valueIcon = wrapper.querySelector('.searchable-select-value-icon');
                if (valueIcon) {
                    valueIcon.innerHTML = '';
                }
            }
        }
        if (statusFilter) statusFilter.value = '';
        if (typeFilter) typeFilter.value = '';
        if (searchInput) searchInput.value = '';

        // Reapply filters (will show all)
        applyFilters();
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
    // Bulk Actions
    // ========================================================================

    /**
     * Handle bulk action execution
     */
    async function executeBulkAction(action) {
        const selectedIds = getSelectedCarriers();

        if (selectedIds.length === 0) {
            showNotification('Please select at least one carrier', 'warning');
            return;
        }

        // Confirm destructive actions
        if (action === 'delete') {
            if (!await AdminModal.confirm({ message: `Are you sure you want to delete ${selectedIds.length} carrier(s)?`, danger: true, confirmText: 'Delete' })) {
                return;
            }
        } else if (action === 'set_default') {
            if (selectedIds.length > 1) {
                showNotification('Please select only one carrier to set as default', 'warning');
                return;
            }
        }

        setLoading(true);

        try {
            const response = await fetch(AdminUtils.buildAdminUrl('/admin/shipping/carrierpreset/bulk-action/'), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': AdminUtils.getCsrfToken(),
                },
                body: JSON.stringify({
                    action: action,
                    carrier_ids: selectedIds
                })
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message, 'success');
                // Reload page to reflect changes
                setTimeout(() => window.location.reload(), 1000);
            } else {
                showNotification(data.message || 'Action failed', 'error');
            }
        } catch (error) {
            console.error('Bulk action error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        } finally {
            setLoading(false);
        }
    }

    // ========================================================================
    // Quick Actions
    // ========================================================================

    /**
     * Toggle carrier active status
     */
    async function toggleCarrierActive(carrierId, button) {
        const isActive = button.dataset.isActive === 'true';

        setLoading(true);

        try {
            const response = await fetch(AdminUtils.buildAdminUrl(`/admin/shipping/carrierpreset/${carrierId}/toggle-active/`), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': AdminUtils.getCsrfToken(),
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message, 'success');

                // Update button state
                button.dataset.isActive = data.is_active ? 'true' : 'false';
                button.title = data.is_active ? 'Disable' : 'Enable';
                button.classList.toggle('active', data.is_active);
                button.classList.toggle('inactive', !data.is_active);
                button.innerHTML = data.is_active ?
                    '<i class="fas fa-toggle-on"></i>' :
                    '<i class="fas fa-toggle-off"></i>';

                // Update badge
                const card = button.closest('.carrier-card');
                const statusBadge = card.querySelector('.badge-status');
                if (statusBadge) {
                    statusBadge.className = data.is_active ? 'badge badge-status badge-active' : 'badge badge-status badge-inactive';
                    statusBadge.innerHTML = data.is_active ?
                        '<i class="fas fa-check-circle"></i> Active' :
                        '<i class="fas fa-times-circle"></i> Inactive';
                }
            } else {
                showNotification(data.message || 'Failed to toggle status', 'error');
            }
        } catch (error) {
            console.error('Toggle error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        } finally {
            setLoading(false);
        }
    }

    /**
     * Set carrier as default
     */
    async function setCarrierDefault(carrierId, button) {
        if (!await AdminModal.confirm('Set this carrier as the default?')) {
            return;
        }

        setLoading(true);

        try {
            const response = await fetch(AdminUtils.buildAdminUrl(`/admin/shipping/carrierpreset/${carrierId}/set-default/`), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': AdminUtils.getCsrfToken(),
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message, 'success');
                // Reload to update all default badges
                setTimeout(() => window.location.reload(), 1000);
            } else {
                showNotification(data.message || 'Failed to set as default', 'error');
            }
        } catch (error) {
            console.error('Set default error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        } finally {
            setLoading(false);
        }
    }

    /**
     * Delete carrier
     */
    async function deleteCarrier(carrierId, button) {
        const card = button.closest('.carrier-card');
        const carrierName = card.querySelector('.carrier-name a').textContent;

        if (!await AdminModal.confirm({ message: `Are you sure you want to delete "${carrierName}"?`, danger: true, confirmText: 'Delete' })) {
            return;
        }

        setLoading(true);

        try {
            const response = await fetch(AdminUtils.buildAdminUrl(`/admin/shipping/carrierpreset/${carrierId}/delete/`), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': AdminUtils.getCsrfToken(),
                }
            });

            const data = await response.json();

            if (data.success) {
                showNotification(data.message, 'success');

                // Animate card removal
                card.style.opacity = '0';
                card.style.transform = 'scale(0.8)';
                setTimeout(() => card.remove(), 300);
            } else {
                showNotification(data.message || 'Failed to delete carrier', 'error');
            }
        } catch (error) {
            console.error('Delete error:', error);
            showNotification('An error occurred. Please try again.', 'error');
        } finally {
            setLoading(false);
        }
    }

    // ========================================================================
    // Event Listeners
    // ========================================================================

    document.addEventListener('DOMContentLoaded', function() {

        // Country filter
        const countryFilter = document.getElementById('country-filter');
        if (countryFilter) {
            countryFilter.addEventListener('change', applyFilters);
        }

        // Status filter
        const statusFilter = document.getElementById('status-filter');
        if (statusFilter) {
            statusFilter.addEventListener('change', applyFilters);
        }

        // Type filter
        const typeFilter = document.getElementById('type-filter');
        if (typeFilter) {
            typeFilter.addEventListener('change', applyFilters);
        }

        // Search with debounce
        const searchInput = document.getElementById('carrier-search');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(applyFilters, 500));
        }

        // Clear filters button
        const clearFiltersBtn = document.getElementById('clear-filters-btn');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', clearAllFilters);
        }

        // Select all checkbox
        const selectAllCheckbox = document.getElementById('select-all-carriers');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', function() {
                const checkboxes = document.querySelectorAll('.carrier-select');
                checkboxes.forEach(cb => cb.checked = this.checked);
                updateSelectedCount();
            });
        }

        // Individual carrier checkboxes
        document.addEventListener('change', function(e) {
            if (e.target.classList.contains('carrier-select')) {
                updateSelectedCount();

                // Update select-all checkbox state
                const allCheckboxes = document.querySelectorAll('.carrier-select');
                const checkedCheckboxes = document.querySelectorAll('.carrier-select:checked');
                if (selectAllCheckbox) {
                    selectAllCheckbox.checked = allCheckboxes.length === checkedCheckboxes.length && allCheckboxes.length > 0;
                }
            }
        });

        // Bulk action apply button
        const applyBulkButton = document.getElementById('apply-bulk-action');
        if (applyBulkButton) {
            applyBulkButton.addEventListener('click', function() {
                const actionSelect = document.getElementById('bulk-action-select');
                const action = actionSelect.value;

                if (!action) {
                    showNotification('Please select an action', 'warning');
                    return;
                }

                executeBulkAction(action);
            });
        }

        // Quick action buttons - using event delegation
        document.addEventListener('click', function(e) {
            const button = e.target.closest('.action-btn');
            if (!button) return;

            const carrierId = button.dataset.carrierId;

            // Toggle active/inactive
            if (button.classList.contains('carrier-toggle-btn')) {
                e.preventDefault();
                toggleCarrierActive(carrierId, button);
            }

            // Set as default
            if (button.classList.contains('default-btn')) {
                e.preventDefault();
                setCarrierDefault(carrierId, button);
            }

            // Delete carrier
            if (button.classList.contains('delete-btn')) {
                e.preventDefault();
                deleteCarrier(carrierId, button);
            }
        });

        // Initialize selected count on page load
        updateSelectedCount();
    });

})();
