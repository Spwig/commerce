/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Order Editing JavaScript
 * Handles dynamic order editing functionality with HTMX
 */

(function() {
    'use strict';

    // Flags to track if event listeners have been initialized
    let eventListenersInitialized = false;
    let productSearchListenersInitialized = false;

    // Utility function to get CSRF token
    function getCSRFToken() {
        return AdminUtils.getCsrfToken();
    }

    // Utility function to show messages
    function showMessage(message, type = 'success') {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.add('show');
        }, 10);

        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Utility function to make AJAX requests
    async function makeRequest(url, method = 'POST', data = null) {
        const headers = {
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest',
        };

        const options = {
            method,
            headers,
            credentials: 'same-origin',
        };

        if (data) {
            if (data instanceof FormData) {
                options.body = data;
            } else {
                headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(data);
            }
        }

        const response = await fetch(url, options);
        return response.json();
    }

    // ==========================================
    // ORDER STATUS MANAGEMENT
    // ==========================================

    function initStatusSelect() {
        const statusSelect = document.getElementById('order-status-select');
        if (!statusSelect) return;

        statusSelect.addEventListener('change', async function() {
            const orderId = this.dataset.orderId;
            const newStatus = this.value;
            const sendNotification = document.getElementById('status-send-notification')?.checked || false;

            const formData = new FormData();
            formData.append('status', newStatus);
            formData.append('send_notification', sendNotification);
            formData.append('csrfmiddlewaretoken', getCSRFToken());

            try {
                const url = `/api/admin/order/${orderId}/status/update/`;
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'same-origin',
                });

                const result = await response.json();

                if (result.success) {
                    showMessage(result.message, 'success');
                    if (result.header_html) {
                        document.querySelector('.order-header-content').outerHTML = result.header_html;
                        // Re-initialize after update
                        initStatusSelect();
                    }
                } else {
                    showMessage(result.message, 'error');
                    // Revert select
                    statusSelect.value = statusSelect.dataset.originalValue || 'pending';
                }
            } catch (error) {
                console.error('Error updating status:', error);
                showMessage('Error updating status. Please try again.', 'error');
            }
        });

        // Store original value
        statusSelect.dataset.originalValue = statusSelect.value;
    }

    // ==========================================
    // ORDER ITEMS MANAGEMENT
    // ==========================================

    function initItemEditing() {
        // Only initialize event listeners once to prevent duplicates
        if (eventListenersInitialized) {
            return;
        }
        eventListenersInitialized = true;

        // Edit item button
        document.addEventListener('click', function(e) {
            const editBtn = e.target.closest('.btn-edit-item');
            if (!editBtn) return;

            const itemRow = editBtn.closest('.order-item-row');
            enterItemEditMode(itemRow);
        });

        // Save item button
        document.addEventListener('click', async function(e) {
            const saveBtn = e.target.closest('.btn-save-item');
            if (!saveBtn) return;

            const itemRow = saveBtn.closest('.order-item-row');
            await saveItemChanges(itemRow);
        });

        // Cancel item edit button
        document.addEventListener('click', function(e) {
            const cancelBtn = e.target.closest('.btn-cancel-item-edit');
            if (!cancelBtn) return;

            const itemRow = cancelBtn.closest('.order-item-row');
            exitItemEditMode(itemRow);
        });

        // Remove item button
        document.addEventListener('click', async function(e) {
            const removeBtn = e.target.closest('.btn-remove-item');
            if (!removeBtn) return;

            if (!await AdminModal.confirm({ message: 'Are you sure you want to remove this item?', danger: true, confirmText: 'Remove' })) return;

            const itemId = removeBtn.dataset.itemId;
            const orderId = removeBtn.dataset.orderId;

            await removeOrderItem(orderId, itemId);
        });

        // Add item button
        document.addEventListener('click', function(e) {
            const addBtn = e.target.closest('#btn-add-item');
            if (!addBtn) return;

            openProductSearchModal();
        });

        // Discount type change - show/hide discount value input
        document.addEventListener('change', function(e) {
            if (!e.target.classList.contains('discount-type-select')) return;

            const itemRow = e.target.closest('.order-item-row');
            const discountValueField = itemRow.querySelector('.edit-field-discount-value');
            const discountType = e.target.value;

            if (discountType === 'none') {
                discountValueField.classList.add('d-none');
            } else {
                discountValueField.classList.remove('d-none');
            }
        });

        // Price change - auto-calculate discount
        document.addEventListener('input', function(e) {
            if (!e.target.classList.contains('price-input')) return;

            const itemRow = e.target.closest('.order-item-row');
            const priceInput = e.target;
            const basePrice = parseFloat(priceInput.dataset.basePrice);
            const newPrice = parseFloat(priceInput.value);

            const discountTypeSelect = itemRow.querySelector('.discount-type-select');
            const discountValueInput = itemRow.querySelector('.discount-value-input');

            // Auto-calculate percentage discount if price is lower
            if (newPrice < basePrice && basePrice > 0) {
                const discountPercentage = ((basePrice - newPrice) / basePrice) * 100;
                discountTypeSelect.value = 'percentage';
                discountValueInput.value = discountPercentage.toFixed(2);
                itemRow.querySelector('.edit-field-discount-value').classList.remove('d-none');
            }
        });

        // Discount value change - recalculate price
        document.addEventListener('input', function(e) {
            if (!e.target.classList.contains('discount-value-input')) return;

            const itemRow = e.target.closest('.order-item-row');
            const priceInput = itemRow.querySelector('.price-input');
            const basePrice = parseFloat(priceInput.dataset.basePrice);
            const discountValue = parseFloat(e.target.value) || 0;
            const discountType = itemRow.querySelector('.discount-type-select').value;

            if (discountType === 'percentage' && basePrice > 0) {
                const newPrice = basePrice - (basePrice * (discountValue / 100));
                priceInput.value = newPrice.toFixed(2);
            } else if (discountType === 'fixed' && basePrice > 0) {
                const newPrice = basePrice - discountValue;
                priceInput.value = Math.max(0, newPrice).toFixed(2);
            }
        });
    }

    function enterItemEditMode(itemRow) {
        // Show edit panel
        itemRow.classList.add('editing');
        itemRow.querySelector('.item-edit-panel').classList.remove('d-none');

        // Show save/cancel buttons, hide edit/remove buttons
        itemRow.querySelector('.btn-edit-item').classList.add('d-none');
        itemRow.querySelector('.btn-remove-item').classList.add('d-none');
        itemRow.querySelector('.btn-save-item').classList.remove('d-none');
        itemRow.querySelector('.btn-cancel-item-edit').classList.remove('d-none');

        // Store original values
        itemRow.dataset.originalQuantity = itemRow.querySelector('.quantity-input').value;
        itemRow.dataset.originalPrice = itemRow.querySelector('.price-input').value;
    }

    function exitItemEditMode(itemRow) {
        // Restore original values
        if (itemRow.dataset.originalQuantity) {
            itemRow.querySelector('.quantity-input').value = itemRow.dataset.originalQuantity;
        }
        if (itemRow.dataset.originalPrice) {
            itemRow.querySelector('.price-input').value = itemRow.dataset.originalPrice;
        }

        // Hide edit panel
        itemRow.classList.remove('editing');
        itemRow.querySelector('.item-edit-panel').classList.add('d-none');

        // Hide save/cancel buttons, show edit/remove buttons
        itemRow.querySelector('.btn-edit-item').classList.remove('d-none');
        itemRow.querySelector('.btn-remove-item').classList.remove('d-none');
        itemRow.querySelector('.btn-save-item').classList.add('d-none');
        itemRow.querySelector('.btn-cancel-item-edit').classList.add('d-none');
    }

    async function saveItemChanges(itemRow) {
        const itemId = itemRow.dataset.itemId;
        const orderId = itemRow.querySelector('.quantity-input').dataset.orderId;
        const quantity = itemRow.querySelector('.quantity-input').value;
        const unitPrice = itemRow.querySelector('.price-input').value;

        // Get discount fields
        const discountType = itemRow.querySelector('.discount-type-select')?.value || 'none';
        const discountValue = itemRow.querySelector('.discount-value-input')?.value || '0';
        const discountReason = itemRow.querySelector('.discount-reason-input')?.value || '';
        const excludeVouchers = itemRow.querySelector('.exclude-vouchers-checkbox')?.checked || false;

        const formData = new FormData();
        formData.append('quantity', quantity);
        formData.append('unit_price', unitPrice);
        formData.append('discount_type', discountType);
        formData.append('discount_value', discountValue);
        formData.append('discount_reason', discountReason);
        formData.append('exclude_from_vouchers', excludeVouchers);
        formData.append('csrfmiddlewaretoken', getCSRFToken());

        try {
            const url = `/api/admin/order/${orderId}/item/${itemId}/update/`;
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            });

            const result = await response.json();

            if (result.success) {
                showMessage(result.message, 'success');

                // Update items section
                if (result.items_html) {
                    document.querySelector('.order-items-content').outerHTML = result.items_html;
                    initItemEditing(); // Re-initialize item editing
                    initProductSearch(); // Re-initialize modal event listeners
                }

                // Update totals
                if (result.totals_html) {
                    document.querySelector('.order-totals').outerHTML = result.totals_html;
                }
            } else {
                showMessage(result.message, 'error');
            }
        } catch (error) {
            console.error('Error updating item:', error);
            showMessage('Error updating item. Please try again.', 'error');
        }
    }

    async function removeOrderItem(orderId, itemId) {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', getCSRFToken());

        try {
            const url = `/api/admin/order/${orderId}/item/${itemId}/remove/`;
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            });

            const result = await response.json();

            if (result.success) {
                showMessage(result.message, 'success');

                // Update items section
                if (result.items_html) {
                    document.querySelector('.order-items-content').outerHTML = result.items_html;
                    initItemEditing(); // Re-initialize item editing
                    initProductSearch(); // Re-initialize modal event listeners
                }

                // Update totals
                if (result.totals_html) {
                    document.querySelector('.order-totals').outerHTML = result.totals_html;
                }
            } else {
                showMessage(result.message, 'error');
            }
        } catch (error) {
            console.error('Error removing item:', error);
            showMessage('Error removing item. Please try again.', 'error');
        }
    }

    // ==========================================
    // PRODUCT SEARCH & ADD ITEM
    // ==========================================

    function openProductSearchModal() {
        const modal = document.getElementById('product-search-modal');
        if (!modal) return;

        modal.classList.remove('d-none');
        document.getElementById('product-search-input').focus();
    }

    function closeProductSearchModal() {
        const modal = document.getElementById('product-search-modal');
        if (!modal) return;

        modal.classList.add('d-none');
        document.getElementById('product-search-input').value = '';
        document.getElementById('product-search-results').innerHTML = `
            <div class="search-placeholder">
                <i class="fas fa-search"></i>
                <p>Start typing to search for products</p>
            </div>
        `;
    }

    // Expose to window for onclick handlers
    window.closeProductSearchModal = closeProductSearchModal;

    function initProductSearch() {
        // Only initialize document-level event listeners once to prevent duplicates
        if (!productSearchListenersInitialized) {
            productSearchListenersInitialized = true;

            // Close modal on close button click
            document.addEventListener('click', function(e) {
                if (e.target.closest('#product-search-modal .close')) {
                    closeProductSearchModal();
                }
            });

            // Close modal on outside click
            document.addEventListener('click', function(e) {
                const modal = document.getElementById('product-search-modal');
                if (e.target === modal) {
                    closeProductSearchModal();
                }
            });

            // Select product from search results
            document.addEventListener('click', async function(e) {
                const selectBtn = e.target.closest('.btn-select-product');
                if (!selectBtn) return;

                const resultItem = selectBtn.closest('.product-result-item');
                const productId = resultItem.dataset.productId;
                const variantId = resultItem.dataset.variantId || '';
                const price = resultItem.dataset.price;
                const trackInventory = resultItem.dataset.trackInventory === 'True';
                const availableStock = parseInt(resultItem.dataset.availableStock) || 0;

                // Check stock and show warning if out of stock
                if (trackInventory && availableStock === 0) {
                    const productName = resultItem.querySelector('.product-name').textContent;
                    const confirmed = await AdminModal.confirm(`Warning: "${productName}" is currently out of stock (0 available). Do you still want to add this item to the order?`);
                    if (!confirmed) {
                        return; // Don't add the item
                    }
                } else if (trackInventory && availableStock <= 5 && availableStock > 0) {
                    // Optional: Show info toast for low stock (non-blocking)
                    const productName = resultItem.querySelector('.product-name').textContent;
                    console.info(`Low stock warning: "${productName}" has only ${availableStock} units available`);
                }

                await addProductToOrder(productId, variantId, price);
            });
        }

        // Re-initialize search input listener (element may be replaced)
        const searchInput = document.getElementById('product-search-input');
        if (!searchInput) return;

        // Remove old listener if exists
        const oldListener = searchInput._searchListener;
        if (oldListener) {
            searchInput.removeEventListener('input', oldListener);
        }

        let searchTimeout;

        const searchListener = function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();

            if (query.length < 2) {
                document.getElementById('product-search-results').innerHTML = `
                    <div class="search-placeholder">
                        <i class="fas fa-search"></i>
                        <p>Type at least 2 characters to search</p>
                    </div>
                `;
                return;
            }

            searchTimeout = setTimeout(async () => {
                await searchProducts(query);
            }, 300);
        };

        // Add listener and store reference for later removal
        searchInput.addEventListener('input', searchListener);
        searchInput._searchListener = searchListener;
    }

    async function searchProducts(query) {
        try {
            const url = `/api/admin/product-search/?q=${encodeURIComponent(query)}`;
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            });

            const result = await response.json();

            if (result.success && result.results_html) {
                document.getElementById('product-search-results').innerHTML = result.results_html;
            } else {
                document.getElementById('product-search-results').innerHTML = `
                    <div class="no-results">
                        <i class="fas fa-search"></i>
                        <p>No products found</p>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error searching products:', error);
        }
    }

    async function addProductToOrder(productId, variantId, price) {
        const orderId = document.getElementById('btn-add-item')?.dataset.orderId;
        if (!orderId) return;

        const formData = new FormData();
        formData.append('product', productId);

        // Only send variant if it has a valid value (not empty, null, or 'None' string)
        if (variantId && variantId !== '' && variantId !== 'null' && variantId !== 'None') {
            formData.append('variant', variantId);
        }

        formData.append('quantity', '1');
        formData.append('unit_price', price);  // Send as plain value, view will create Money object
        formData.append('csrfmiddlewaretoken', getCSRFToken());

        try {
            const url = `/api/admin/order/${orderId}/item/add/`;
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            });

            const result = await response.json();

            if (result.success) {
                showMessage(result.message, 'success');

                // Update items section
                if (result.items_html) {
                    document.querySelector('.order-items-content').outerHTML = result.items_html;
                    initItemEditing(); // Re-initialize item editing
                    initProductSearch(); // Re-initialize modal event listeners
                }

                // Update totals
                if (result.totals_html) {
                    document.querySelector('.order-totals').outerHTML = result.totals_html;
                }

                // Close modal
                closeProductSearchModal();
            } else {
                showMessage(result.message, 'error');
            }
        } catch (error) {
            console.error('Error adding product:', error);
            showMessage('Error adding product. Please try again.', 'error');
        }
    }

    async function searchCustomers(query) {
        try {
            const url = `/api/admin/customer-search/?q=${encodeURIComponent(query)}`;
            const response = await fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            });

            const result = await response.json();

            const resultsContainer = document.getElementById('customer-search-results');
            if (result.success && result.results_html) {
                resultsContainer.innerHTML = result.results_html;
                resultsContainer.classList.remove('d-none');
            } else {
                resultsContainer.innerHTML = `
                    <div class="no-results">
                        <i class="fas fa-search"></i>
                        <p>No customers found</p>
                    </div>
                `;
                resultsContainer.classList.remove('d-none');
            }
        } catch (error) {
            console.error('Error searching customers:', error);
        }
    }

    // ==========================================
    // VOUCHER MANAGEMENT
    // ==========================================

    function initVoucherManagement() {
        // Apply voucher form
        document.addEventListener('submit', async function(e) {
            if (e.target.id !== 'voucher-apply-form') return;
            e.preventDefault();

            const form = e.target;
            const orderId = form.dataset.orderId;
            const formData = new FormData(form);

            try {
                const url = `/api/admin/order/${orderId}/voucher/apply/`;
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'same-origin',
                });

                const result = await response.json();

                if (result.success) {
                    showMessage(result.message, 'success');

                    // Update discounts section
                    if (result.discounts_html) {
                        document.querySelector('.discounts-content').outerHTML = result.discounts_html;
                        initVoucherManagement(); // Re-initialize
                    }

                    // Update totals
                    if (result.totals_html) {
                        document.querySelector('.order-totals').outerHTML = result.totals_html;
                    }

                    // Clear form
                    form.reset();
                } else {
                    showMessage(result.message, 'error');
                }
            } catch (error) {
                console.error('Error applying voucher:', error);
                showMessage('Error applying voucher. Please try again.', 'error');
            }
        });

        // Remove voucher button
        document.addEventListener('click', async function(e) {
            const removeBtn = e.target.closest('.btn-remove-voucher');
            if (!removeBtn) return;

            if (!await AdminModal.confirm({ message: 'Remove this voucher?', danger: true, confirmText: 'Remove' })) return;

            const voucherId = removeBtn.dataset.voucherId;
            const orderId = removeBtn.dataset.orderId;

            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', getCSRFToken());

            try {
                const url = `/api/admin/order/${orderId}/voucher/${voucherId}/remove/`;
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'same-origin',
                });

                const result = await response.json();

                if (result.success) {
                    showMessage(result.message, 'success');

                    // Update discounts section
                    if (result.discounts_html) {
                        document.querySelector('.discounts-content').outerHTML = result.discounts_html;
                        initVoucherManagement(); // Re-initialize
                    }

                    // Update totals
                    if (result.totals_html) {
                        document.querySelector('.order-totals').outerHTML = result.totals_html;
                    }
                } else {
                    showMessage(result.message, 'error');
                }
            } catch (error) {
                console.error('Error removing voucher:', error);
                showMessage('Error removing voucher. Please try again.', 'error');
            }
        });
    }

    // ==========================================
    // MANUAL DISCOUNT
    // ==========================================

    function initManualDiscount() {
        // Toggle manual discount form
        document.addEventListener('click', function(e) {
            const toggleBtn = e.target.closest('[data-action="toggle-manual-discount"]');
            if (!toggleBtn) return;

            e.preventDefault();
            const discountForm = document.querySelector('.manual-discount-form');
            if (discountForm) {
                if (discountForm.classList.contains('d-none')) {
                    discountForm.classList.remove('d-none');
                    toggleBtn.innerHTML = '<i class="fas fa-times"></i> Cancel discount';
                } else {
                    discountForm.classList.add('d-none');
                    toggleBtn.innerHTML = '<i class="fas fa-percent"></i> Apply manual discount';
                    // Reset form
                    const form = document.getElementById('manual-discount-form');
                    if (form) form.reset();
                }
            }
        });

        // Apply manual discount form
        document.addEventListener('submit', async function(e) {
            if (e.target.id !== 'manual-discount-form') return;
            e.preventDefault();

            const form = e.target;
            const orderId = form.dataset.orderId;
            const formData = new FormData(form);

            try {
                const url = `/api/admin/order/${orderId}/discount/apply/`;
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'same-origin',
                });

                const result = await response.json();

                if (result.success) {
                    showMessage(result.message, 'success');

                    // Update discounts section
                    if (result.discounts_html) {
                        document.querySelector('.discounts-content').outerHTML = result.discounts_html;
                        initManualDiscount(); // Re-initialize
                    }

                    // Update totals
                    if (result.totals_html) {
                        document.querySelector('.order-totals').outerHTML = result.totals_html;
                    }

                    // Clear form and hide it
                    form.reset();
                    const discountForm = document.querySelector('.manual-discount-form');
                    if (discountForm) discountForm.classList.add('d-none');

                    const toggleBtn = document.querySelector('[data-action="toggle-manual-discount"]');
                    if (toggleBtn) {
                        toggleBtn.innerHTML = '<i class="fas fa-percent"></i> Apply manual discount';
                    }
                } else {
                    showMessage(result.message, 'error');
                }
            } catch (error) {
                console.error('Error applying manual discount:', error);
                showMessage('Error applying discount. Please try again.', 'error');
            }
        });
    }

    // ==========================================
    // CUSTOMER MANAGEMENT
    // ==========================================

    async function handleCustomerAddresses(addresses, hasExistingAddresses, orderId, previousOrderAddresses = null) {
        /**
         * Handle customer address population with confirmation dialog or modal
         * Shows modal if previous order addresses exist, otherwise uses confirm dialog for saved addresses
         */

        // If we have previous order addresses, show the modal
        if (previousOrderAddresses && previousOrderAddresses.length > 0) {
            showPreviousAddressesModal(previousOrderAddresses, orderId);
            return;
        }

        // Otherwise, handle saved addresses with confirm dialog (existing behavior)
        if (!addresses || (!addresses.shipping && !addresses.billing)) {
            // No saved addresses and no previous addresses - just info message
            if (!previousOrderAddresses || previousOrderAddresses.length === 0) {
                showMessage('Customer has no saved addresses or previous orders.', 'info');
            }
            return;
        }

        let message = 'This customer has saved addresses. Would you like to populate the order with these addresses?';

        if (hasExistingAddresses) {
            message = 'This order already has addresses. Would you like to replace them with the customer\'s saved addresses?';
        }

        const addressPreview = [];
        if (addresses.shipping) {
            addressPreview.push(`Shipping: ${addresses.shipping.name}, ${addresses.shipping.city}, ${addresses.shipping.state}`);
        }
        if (addresses.billing) {
            addressPreview.push(`Billing: ${addresses.billing.name}, ${addresses.billing.city}, ${addresses.billing.state}`);
        }

        const fullMessage = `${message}\n\n${addressPreview.join('\n')}`;

        if (await AdminModal.confirm(fullMessage)) {
            // User confirmed - populate addresses via API
            await populateAddressesViaAPI(orderId, addresses.shipping, addresses.billing);
        }
    }

    async function populateAddressesViaAPI(orderId, shippingAddress, billingAddress) {
        /**
         * Helper function to populate addresses via API call
         */
        try {
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', getCSRFToken());

            if (shippingAddress) {
                formData.append('shipping_name', shippingAddress.name || '');
                formData.append('shipping_address1', shippingAddress.address1 || '');
                formData.append('shipping_address2', shippingAddress.address2 || '');
                formData.append('shipping_city', shippingAddress.city || '');
                formData.append('shipping_state', shippingAddress.state || '');
                formData.append('shipping_postal_code', shippingAddress.postal_code || '');
                formData.append('shipping_country', shippingAddress.country || '');
                formData.append('shipping_phone', shippingAddress.phone || '');
            }

            if (billingAddress) {
                formData.append('billing_name', billingAddress.name || '');
                formData.append('billing_address1', billingAddress.address1 || '');
                formData.append('billing_address2', billingAddress.address2 || '');
                formData.append('billing_city', billingAddress.city || '');
                formData.append('billing_state', billingAddress.state || '');
                formData.append('billing_postal_code', billingAddress.postal_code || '');
                formData.append('billing_country', billingAddress.country || '');
                formData.append('billing_phone', billingAddress.phone || '');
                formData.append('billing_same_as_shipping', 'false');
            } else {
                // If no separate billing address, mark as same as shipping
                formData.append('billing_same_as_shipping', 'true');
            }

            const url = `/api/admin/order/${orderId}/address/update/`;
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            });

            const result = await response.json();

            if (result.success) {
                showMessage('Customer addresses populated successfully', 'success');

                // Update address sections if returned
                if (result.addresses_html) {
                    const addressesSection = document.querySelector('.addresses-grid');
                    if (addressesSection) {
                        addressesSection.outerHTML = result.addresses_html;
                    } else {
                        console.warn('Address section .addresses-grid not found, trying fallback selectors');
                        // Fallback to legacy selectors
                        const fallbackSection = document.querySelector('.addresses-content, .shipping-billing-wrapper');
                        if (fallbackSection) {
                            fallbackSection.outerHTML = result.addresses_html;
                        }
                    }
                } else {
                    // Fallback to individual sections for backwards compatibility
                    if (result.shipping_html) {
                        const shippingSection = document.querySelector('.shipping-info-content');
                        if (shippingSection) {
                            shippingSection.outerHTML = result.shipping_html;
                        }
                    }

                    if (result.billing_html) {
                        const billingSection = document.querySelector('.billing-info-content');
                        if (billingSection) {
                            billingSection.outerHTML = result.billing_html;
                        }
                    }
                }
            } else {
                showMessage(result.message || 'Error populating addresses', 'error');
            }
        } catch (error) {
            console.error('Error populating addresses:', error);
            showMessage('Error populating addresses. Please try again.', 'error');
        }
    }

    function showPreviousAddressesModal(addresses, orderId) {
        /**
         * Display modal with list of previous order addresses
         */
        const modal = document.getElementById('addressSelectionModal');
        const addressList = document.getElementById('previousAddressesList');
        const noAddresses = document.getElementById('noPreviousAddresses');

        if (!modal || !addressList) {
            console.error('Address selection modal not found in DOM');
            return;
        }

        // Clear previous content
        addressList.innerHTML = '';

        if (!addresses || addresses.length === 0) {
            noAddresses.classList.remove('d-none');
            addressList.classList.add('d-none');
        } else {
            noAddresses.classList.add('d-none');
            addressList.classList.remove('d-none');

            // Populate address cards
            addresses.forEach((address) => {
                const card = createAddressCard(address, orderId);
                addressList.appendChild(card);
            });
        }

        // Show modal
        modal.classList.add('active');
        document.body.classList.add('admin-modal-body-locked');
    }

    function closePreviousAddressesModal() {
        /**
         * Close the previous addresses modal
         */
        const modal = document.getElementById('addressSelectionModal');
        if (modal) {
            modal.classList.remove('active');
            document.body.classList.remove('admin-modal-body-locked');
        }
    }

    function createAddressCard(address, orderId) {
        /**
         * Create a card element for an address
         */
        const card = document.createElement('div');
        card.className = 'address-card';

        // Format last used date
        const lastUsed = new Date(address.last_used);
        const formattedDate = lastUsed.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });

        // Build address lines
        const addressLines = [
            address.address1,
            address.address2,
            `${address.city}, ${address.state} ${address.postal_code}`,
            address.country
        ].filter(line => line && line.trim() !== ''); // Remove empty lines

        // Determine badge class
        const badgeClass = address.address_type === 'shipping' ? 'shipping' : 'billing';

        card.innerHTML = `
            <span class="address-type-badge ${badgeClass}">
                ${address.address_type}
            </span>

            <div class="address-content">
                <div class="address-name">
                    <i class="fas fa-user"></i>
                    ${escapeHtml(address.name)}
                </div>
                ${address.company ? `<div class="address-company">${escapeHtml(address.company)}</div>` : ''}
                <div class="address-lines">
                    ${addressLines.map(line => `<div class="address-line">${escapeHtml(line)}</div>`).join('')}
                </div>
                ${address.phone ? `<div class="address-line"><i class="fas fa-phone"></i> ${escapeHtml(address.phone)}</div>` : ''}
            </div>

            <div class="address-metadata">
                <div class="address-metadata-item">
                    <i class="fas fa-clock"></i>
                    <span>Last used: ${formattedDate}</span>
                </div>
                <div class="address-metadata-item">
                    <i class="fas fa-receipt"></i>
                    <span>Order #${escapeHtml(address.order_number)}</span>
                </div>
            </div>

            <div class="address-actions">
                <button type="button" class="btn btn-use-shipping" onclick="useAddressFor('shipping', ${orderId}, this)">
                    <i class="fas fa-shipping-fast"></i>
                    Shipping
                </button>
                <button type="button" class="btn btn-use-billing" onclick="useAddressFor('billing', ${orderId}, this)">
                    <i class="fas fa-credit-card"></i>
                    Billing
                </button>
                <button type="button" class="btn btn-use-both" onclick="useAddressFor('both', ${orderId}, this)">
                    <i class="fas fa-check-double"></i>
                    Both
                </button>
            </div>
        `;

        // Store address data on the card element
        card.dataset.addressData = JSON.stringify(address);

        return card;
    }

    window.useAddressFor = async function(type, orderId, buttonElement) {
        /**
         * Use selected address for shipping, billing, or both
         */
        const card = buttonElement.closest('.address-card');
        const address = JSON.parse(card.dataset.addressData);

        let shippingAddress = null;
        let billingAddress = null;

        if (type === 'shipping' || type === 'both') {
            shippingAddress = address;
        }

        if (type === 'billing' || type === 'both') {
            billingAddress = address;
        }

        // Close modal
        closePreviousAddressesModal();

        // Populate addresses via API
        await populateAddressesViaAPI(orderId, shippingAddress, billingAddress);
    };

    window.closePreviousAddressesModal = closePreviousAddressesModal;

    function escapeHtml(text) {
        /**
         * Escape HTML to prevent XSS
         */
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function initCustomerManagement() {
        // Edit customer button
        document.addEventListener('click', function(e) {
            const editBtn = e.target.closest('[data-action="edit-customer"]');
            if (!editBtn) return;

            const customerInfo = document.querySelector('.customer-info-content');
            const customerForm = document.querySelector('.customer-change-form');

            // Hide search results when opening the form
            const searchResults = document.getElementById('customer-search-results');
            if (searchResults) {
                searchResults.classList.add('d-none');
                searchResults.innerHTML = ''; // Clear previous results
            }

            customerInfo.classList.add('d-none');
            customerForm.classList.remove('d-none');
        });

        // Cancel customer edit
        document.addEventListener('click', function(e) {
            const cancelBtn = e.target.closest('[data-action="cancel-customer-edit"]');
            if (!cancelBtn) return;

            const customerInfo = document.querySelector('.customer-info-content');
            const customerForm = document.querySelector('.customer-change-form');

            customerInfo.classList.remove('d-none');
            customerForm.classList.add('d-none');
        });

        // Customer type radio change
        document.addEventListener('change', function(e) {
            if (e.target.name !== 'customer_type') return;

            const existingGroup = document.querySelector('.existing-customer-group');
            const guestGroup = document.querySelector('.guest-customer-group');

            // Clear search results when switching types
            const searchResults = document.getElementById('customer-search-results');
            if (searchResults) {
                searchResults.classList.add('d-none');
                searchResults.innerHTML = '';
            }

            if (e.target.value === 'existing') {
                existingGroup.classList.remove('d-none');
                guestGroup.classList.add('d-none');
            } else {
                existingGroup.classList.add('d-none');
                guestGroup.classList.remove('d-none');
            }
        });

        // Customer search input
        let customerSearchTimeout;
        const customerSearchInput = document.getElementById('customer-search-input');
        if (customerSearchInput) {
            customerSearchInput.addEventListener('input', function(e) {
                const query = e.target.value.trim();

                // Clear previous timeout
                clearTimeout(customerSearchTimeout);

                if (query.length < 2) {
                    document.getElementById('customer-search-results').classList.add('d-none');
                    return;
                }

                // Debounce search
                customerSearchTimeout = setTimeout(() => {
                    searchCustomers(query);
                }, 300);
            });
        }

        // Select customer from search results
        document.addEventListener('click', function(e) {
            const selectBtn = e.target.closest('.btn-select-customer');
            if (!selectBtn) return;

            const resultItem = selectBtn.closest('.customer-result-item');
            const customerId = resultItem.dataset.customerId;
            const customerName = resultItem.dataset.fullName || resultItem.dataset.email;
            const customerEmail = resultItem.dataset.email;

            // Set hidden input value
            document.getElementById('selected-customer-id').value = customerId;

            // Update selected customer display
            document.getElementById('selected-customer-name').textContent = customerName;
            document.getElementById('selected-customer-email').textContent = customerEmail;

            // Show selected display, hide search results
            document.getElementById('customer-search-input').classList.add('d-none');
            document.getElementById('customer-search-results').classList.add('d-none');
            document.getElementById('selected-customer-display').classList.remove('d-none');
        });

        // Clear customer selection
        document.addEventListener('click', function(e) {
            if (e.target.closest('#clear-customer-selection')) {
                document.getElementById('selected-customer-id').value = '';
                document.getElementById('customer-search-input').value = '';
                document.getElementById('customer-search-input').classList.remove('d-none');
                document.getElementById('selected-customer-display').classList.add('d-none');

                // Clear search results
                const searchResults = document.getElementById('customer-search-results');
                if (searchResults) {
                    searchResults.classList.add('d-none');
                    searchResults.innerHTML = '';
                }
            }
        });

        // Submit customer change form
        document.addEventListener('submit', async function(e) {
            if (e.target.id !== 'customer-change-form') return;
            e.preventDefault();

            const form = e.target;
            const orderId = form.dataset.orderId;
            const formData = new FormData(form);

            try {
                const url = `/api/admin/order/${orderId}/customer/update/`;
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'same-origin',
                });

                const result = await response.json();

                if (result.success) {
                    showMessage(result.message, 'success');

                    // Hide customer change form first
                    const oldCustomerForm = document.querySelector('.customer-change-form');
                    if (oldCustomerForm) {
                        oldCustomerForm.classList.add('d-none');
                    }

                    // Update customer section
                    if (result.customer_html) {
                        // Remove old customer form to prevent duplicates
                        if (oldCustomerForm && oldCustomerForm.parentNode) {
                            oldCustomerForm.parentNode.removeChild(oldCustomerForm);
                        }

                        // Replace customer info content
                        document.querySelector('.customer-info-content').outerHTML = result.customer_html;
                        initCustomerManagement(); // Re-initialize
                    }

                    // Ensure customer info is visible and form is hidden
                    const customerInfo = document.querySelector('.customer-info-content');
                    const customerForm = document.querySelector('.customer-change-form');
                    if (customerInfo) {
                        customerInfo.classList.remove('d-none');
                    }
                    if (customerForm) {
                        customerForm.classList.add('d-none');
                    }

                    // Handle customer addresses if available
                    if (result.customer_addresses || result.previous_order_addresses) {
                        handleCustomerAddresses(
                            result.customer_addresses,
                            result.has_existing_addresses,
                            orderId,
                            result.previous_order_addresses
                        );
                    }
                } else {
                    showMessage(result.message, 'error');
                }
            } catch (error) {
                console.error('Error updating customer:', error);
                showMessage('Error updating customer. Please try again.', 'error');
            }
        });
    }

    // ==========================================
    // ADDRESS MANAGEMENT
    // ==========================================

    function initAddressManagement() {
        // Edit address button
        document.addEventListener('click', function(e) {
            const editBtn = e.target.closest('[data-action="edit-address"]');
            if (!editBtn) return;

            const addressType = editBtn.dataset.addressType;
            const display = document.getElementById(`${addressType}-address-display`);
            const form = document.getElementById(`${addressType}-address-form`);

            display.classList.add('d-none');
            form.classList.remove('d-none');
        });

        // Cancel address edit
        document.addEventListener('click', function(e) {
            const cancelBtn = e.target.closest('[data-action="cancel-address-edit"]');
            if (!cancelBtn) return;

            const form = cancelBtn.closest('.address-edit-form');
            const addressType = form.querySelector('[name="address_type"]').value;
            const display = document.getElementById(`${addressType}-address-display`);

            display.classList.remove('d-none');
            form.classList.add('d-none');
        });

        // Close address selection modal (button or backdrop click)
        document.addEventListener('click', function(e) {
            const closeBtn = e.target.closest('[data-action="close-addresses-modal"]');
            if (closeBtn) {
                closePreviousAddressesModal();
                return;
            }

            // Backdrop click on overlay
            const overlay = document.getElementById('addressSelectionModal');
            if (overlay && e.target === overlay) {
                closePreviousAddressesModal();
            }
        });

        // Copy from shipping/billing
        document.addEventListener('click', function(e) {
            const copyBtn = e.target.closest('[data-action^="copy-from"]');
            if (!copyBtn) return;

            const action = copyBtn.dataset.action;
            const currentForm = copyBtn.closest('form');
            const sourceType = action === 'copy-from-shipping' ? 'shipping' : 'billing';

            // Copy values from source
            const sourceDisplay = document.getElementById(`${sourceType}-address-display`);
            // Implementation would copy values - simplified here
            AdminModal.alert(`Copy from ${sourceType} - to be implemented`);
        });

        // Submit address form
        document.addEventListener('submit', async function(e) {
            if (!e.target.classList.contains('address-form')) return;
            e.preventDefault();

            const form = e.target;
            const orderId = form.dataset.orderId;
            const formData = new FormData(form);

            try {
                const url = `/api/admin/order/${orderId}/address/update/`;
                const response = await fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    credentials: 'same-origin',
                });

                const result = await response.json();

                if (result.success) {
                    showMessage(result.message, 'success');

                    // Update addresses section
                    if (result.addresses_html) {
                        document.querySelector('.addresses-grid').outerHTML = result.addresses_html;
                        initAddressManagement(); // Re-initialize
                    }
                } else {
                    showMessage(result.message, 'error');
                }
            } catch (error) {
                console.error('Error updating address:', error);
                showMessage('Error updating address. Please try again.', 'error');
            }
        });
    }

    // ==========================================
    // PAYMENT FORM TOGGLE
    // ==========================================

    document.addEventListener('click', function(e) {
        if (!e.target.closest('[data-action="toggle-payment-form"]')) return;
        e.preventDefault();
        var form = document.getElementById('mark-paid-form');
        var btn = document.getElementById('show-payment-form-btn');
        if (!form) return;
        if (form.classList.contains('d-none')) {
            form.classList.remove('d-none');
            if (btn) btn.classList.add('d-none');
        } else {
            form.classList.add('d-none');
            if (btn) btn.classList.remove('d-none');
        }
    });

    // ==========================================
    // DATA-CONFIRM HANDLER
    // ==========================================

    document.addEventListener('click', async function(e) {
        var btn = e.target.closest('button[data-confirm]');
        if (!btn) return;
        var msg = btn.dataset.confirm;
        if (msg) {
            e.preventDefault();
            e.stopPropagation();
            if (await AdminModal.confirm(msg)) {
                btn.closest('form')?.submit();
            }
        }
    });

    // ==========================================
    // QUICK ACTIONS LOADING STATE
    // ==========================================

    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.quick-actions form').forEach(function(form) {
            form.addEventListener('submit', function() {
                var button = this.querySelector('button');
                if (button) {
                    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                    button.disabled = true;
                }
            });
        });
    });

    // ==========================================
    // INITIALIZATION
    // ==========================================

    function init() {
        initStatusSelect();
        initItemEditing();
        initProductSearch();
        initVoucherManagement();
        initManualDiscount();
        initCustomerManagement();
        initAddressManagement();
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
