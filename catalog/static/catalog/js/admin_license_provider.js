/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * License Provider Admin JavaScript
 * Handles interactions for license provider list and cards
 */

(function() {
    'use strict';

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        initFilters();
        initSearch();
        initBulkActions();
        initTestConnection();
        initSyncNow();
    });

    /**
     * Initialize filter dropdowns
     */
    function initFilters() {
        const filters = {
            'connection-status-filter': 'connection_status',
            'active-filter': 'is_active',
            'provider-type-filter': 'provider_type'
        };

        Object.entries(filters).forEach(([elementId, paramName]) => {
            const filterElement = document.getElementById(elementId);
            if (filterElement) {
                filterElement.addEventListener('change', function() {
                    updateURLParameter(paramName, this.value);
                });
            }
        });
    }

    /**
     * Initialize search functionality
     */
    function initSearch() {
        const searchInput = document.getElementById('provider-search');
        if (!searchInput) return;

        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                updateURLParameter('q', this.value);
            }, 500);
        });
    }

    /**
     * Initialize bulk actions
     */
    function initBulkActions() {
        const selectAllCheckbox = document.getElementById('select-all-providers');
        const providerCheckboxes = document.querySelectorAll('.provider-checkbox');
        const selectedCount = document.getElementById('selected-count');
        const selectedNumber = document.getElementById('selected-number');
        const applyButton = document.getElementById('apply-bulk-action');

        if (!selectAllCheckbox) return;

        // Select all functionality
        selectAllCheckbox.addEventListener('change', function() {
            providerCheckboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateSelectedCount();
        });

        // Individual checkbox change
        providerCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateSelectedCount);
        });

        function updateSelectedCount() {
            const checkedCount = document.querySelectorAll('.provider-checkbox:checked').length;

            if (checkedCount > 0) {
                selectedCount.style.display = 'inline-block';
                selectedNumber.textContent = checkedCount;
                if (applyButton) applyButton.disabled = false;
            } else {
                selectedCount.style.display = 'none';
                if (applyButton) applyButton.disabled = true;
            }

            // Update select-all state
            selectAllCheckbox.checked = checkedCount === providerCheckboxes.length;
            selectAllCheckbox.indeterminate = checkedCount > 0 && checkedCount < providerCheckboxes.length;
        }
    }

    /**
     * Initialize test connection buttons
     */
    function initTestConnection() {
        const testButtons = document.querySelectorAll('.test-connection-btn');

        testButtons.forEach(button => {
            button.addEventListener('click', function() {
                const providerId = this.dataset.providerId;
                const providerName = this.dataset.providerName;

                testProviderConnection(providerId, providerName, this);
            });
        });
    }

    /**
     * Test provider connection via AJAX
     */
    function testProviderConnection(providerId, providerName, button) {
        const originalHTML = button.innerHTML;
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';

        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            },
            body: new URLSearchParams({
                'action': 'test_provider_connections',
                '_selected_action': providerId,
                'index': '0'
            })
        })
        .then(response => {
            if (response.ok) {
                showNotification(`Testing connection for ${providerName}...`, 'info');
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                throw new Error('Failed to test connection');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Failed to test connection', 'error');
            button.disabled = false;
            button.innerHTML = originalHTML;
        });
    }

    /**
     * Initialize sync now buttons
     */
    function initSyncNow() {
        const syncButtons = document.querySelectorAll('.sync-now-btn');

        syncButtons.forEach(button => {
            button.addEventListener('click', function() {
                const providerId = this.dataset.providerId;
                showNotification('Sync functionality coming soon', 'info');
            });
        });
    }

    /**
     * Update URL parameter and reload
     */
    function updateURLParameter(param, value) {
        const url = new URL(window.location);

        if (value) {
            url.searchParams.set(param, value);
        } else {
            url.searchParams.delete(param);
        }

        // Keep page parameter if it exists
        if (!url.searchParams.has('p')) {
            url.searchParams.delete('p');
        }

        window.location.href = url.toString();
    }

    /**
     * Show notification
     */
    function showNotification(message, type = 'info') {
        AdminModal.toast(message, type);
    }

})();
