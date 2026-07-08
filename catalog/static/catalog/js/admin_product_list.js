/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Product Admin List Interactive Features
 * Handles view toggle, multi-select, bulk actions, quick operations, and infinite scroll
 */

document.addEventListener('DOMContentLoaded', function() {
    // ========== AJAX Filter Tabs (No Page Reload) ==========
    const filterTabs = document.querySelectorAll('.admin-tab-btn');
    const productsContainer = document.getElementById('products-container');
    const searchInput = document.getElementById('product-search');
    let currentSearchQuery = new URLSearchParams(window.location.search).get('q') || '';

    // Ensure correct active tab based on URL parameters
    ensureCorrectActiveTab();

    // Attach click handlers to filter tabs for AJAX filtering
    filterTabs.forEach((tab, index) => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            const url = new URL(this.href, window.location.origin);
            loadProducts(url.search);

            // Update browser URL without reload
            window.history.pushState({}, '', url.search || '?');

            // Update active tab
            filterTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            return false;
        }, true);
    });

    function ensureCorrectActiveTab() {
        const urlParams = new URLSearchParams(window.location.search);
        const status = urlParams.get('status');
        const stock = urlParams.get('stock');
        const isFeatured = urlParams.get('is_featured');

        filterTabs.forEach(tab => tab.classList.remove('active'));

        if (status === 'published') {
            document.querySelector('[data-filter="published"]')?.classList.add('active');
        } else if (status === 'draft') {
            document.querySelector('[data-filter="draft"]')?.classList.add('active');
        } else if (isFeatured === '1') {
            document.querySelector('[data-filter="featured"]')?.classList.add('active');
        } else if (stock === 'low') {
            document.querySelector('[data-filter="low"]')?.classList.add('active');
        } else if (stock === 'out') {
            document.querySelector('[data-filter="out"]')?.classList.add('active');
        } else {
            document.querySelector('[data-filter="all"]')?.classList.add('active');
        }
    }

    function loadProducts(queryString) {
        if (!productsContainer) return;

        const loadingOverlay = document.getElementById('products-loading');
        if (loadingOverlay) {
            loadingOverlay.style.display = 'flex';
        }

        fetch(window.location.pathname + queryString, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newProducts = doc.querySelector('#products-container');

            if (newProducts) {
                productsContainer.innerHTML = newProducts.innerHTML;
                window.attachProductEventListeners();
            }

            updateTabCounts(doc);

            if (loadingOverlay) {
                loadingOverlay.style.display = 'none';
            }

            window.scrollTo({ top: 0, behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Error loading products:', error);
            if (loadingOverlay) {
                loadingOverlay.style.display = 'none';
            }
            AdminModal.alert({message: 'Failed to load products. Please try again.', type: 'error'});
        });
    }

    function updateTabCounts(doc) {
        function extractCount(labelText) {
            const match = labelText?.match(/\((\d+)\)/);
            return match ? match[1] : null;
        }

        function getCurrentLabelText(filterName) {
            const label = document.querySelector(`[data-filter="${filterName}"] .label`);
            if (!label) return null;
            const text = label.textContent;
            return text.replace(/\(\d+\)/g, '').replace(/\n/g, '').trim();
        }

        const counts = {
            all: extractCount(doc.querySelector('[data-filter="all"] .label')?.textContent),
            published: extractCount(doc.querySelector('[data-filter="published"] .label')?.textContent),
            draft: extractCount(doc.querySelector('[data-filter="draft"] .label')?.textContent),
            featured: extractCount(doc.querySelector('[data-filter="featured"] .label')?.textContent),
            low: extractCount(doc.querySelector('[data-filter="low"] .label')?.textContent),
            out: extractCount(doc.querySelector('[data-filter="out"] .label')?.textContent)
        };

        function updateTabCount(filterName, count) {
            const label = document.querySelector(`[data-filter="${filterName}"] .label`);
            const labelText = getCurrentLabelText(filterName);
            if (label && count !== null && labelText) {
                label.innerHTML = `${labelText}<br>(${count})`;
            }
        }

        updateTabCount('all', counts.all);
        updateTabCount('published', counts.published);
        updateTabCount('draft', counts.draft);
        updateTabCount('featured', counts.featured);
        updateTabCount('low', counts.low);
        updateTabCount('out', counts.out);
    }

    // Expose globally so ProductInfiniteScroll can reuse it
    window.attachProductEventListeners = function attachProductEventListeners() {
        // Reattach checkbox listeners
        document.querySelectorAll('.product-select').forEach(checkbox => {
            checkbox.addEventListener('change', updateSelectedCount);
        });

        // Reattach copy SKU buttons
        document.querySelectorAll('.copy-sku-btn').forEach(btn => {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                const sku = this.dataset.sku;
                navigator.clipboard.writeText(sku).then(() => {
                    showNotification('SKU copied to clipboard!', 'success');
                });
            });
        });

        // Reattach duplicate buttons
        document.querySelectorAll('.duplicate-btn').forEach(btn => {
            btn.addEventListener('click', async function(e) {
                e.preventDefault();
                const productId = this.dataset.productId;
                if (await AdminModal.confirm('Are you sure you want to duplicate this product?')) {
                    duplicateProduct(productId);
                }
            });
        });

        // Reattach delete buttons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', async function(e) {
                e.preventDefault();
                const productId = this.dataset.productId;
                if (await AdminModal.confirm({ message: 'Are you sure you want to delete this product?', danger: true, confirmText: 'Delete' })) {
                    deleteProduct(productId);
                }
            });
        });
    };

    // Handle browser back/forward buttons
    window.addEventListener('popstate', function() {
        window.location.reload();
    });

    // ========== View Toggle ==========
    const gridViewBtn = document.getElementById('grid-view-btn');
    const listViewBtn = document.getElementById('list-view-btn');

    const savedView = localStorage.getItem('productAdminView') || 'grid';
    setView(savedView);

    if (gridViewBtn && listViewBtn) {
        gridViewBtn.addEventListener('click', () => setView('grid'));
        listViewBtn.addEventListener('click', () => setView('list'));
    }

    function setView(view) {
        if (!productsContainer) return;

        if (view === 'grid') {
            productsContainer.classList.remove('products-list');
            productsContainer.classList.add('products-grid');
            gridViewBtn?.classList.add('active');
            listViewBtn?.classList.remove('active');
        } else {
            productsContainer.classList.remove('products-grid');
            productsContainer.classList.add('products-list');
            listViewBtn?.classList.add('active');
            gridViewBtn?.classList.remove('active');
        }

        localStorage.setItem('productAdminView', view);
    }

    // ========== Multi-Select ==========
    const selectedCount = document.getElementById('selected-count');
    const applyBulkActionBtn = document.getElementById('apply-bulk-action');
    const bulkActionSelector = document.getElementById('bulk-action-selector');

    function updateSelectedCount() {
        const selected = document.querySelectorAll('.product-select:checked');
        const count = selected.length;

        if (selectedCount) {
            if (count > 0) {
                selectedCount.textContent = `${count} selected`;
                applyBulkActionBtn.disabled = false;
            } else {
                selectedCount.textContent = '';
                applyBulkActionBtn.disabled = true;
            }
        }
    }

    // Add change listener to initial checkboxes
    document.querySelectorAll('.product-select').forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectedCount);
    });

    // Select All functionality — queries live DOM to include infinite-scroll loaded cards
    const selectAllCheckbox = document.getElementById('select-all-products');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            document.querySelectorAll('.product-select').forEach(checkbox => {
                checkbox.checked = this.checked;
            });
            updateSelectedCount();
        });
    }

    // ========== Bulk Actions ==========
    if (applyBulkActionBtn && bulkActionSelector) {
        applyBulkActionBtn.addEventListener('click', async function() {
            const action = bulkActionSelector.value;
            const selected = Array.from(document.querySelectorAll('.product-select:checked'))
                .map(cb => cb.value);

            if (!action || selected.length === 0) {
                return;
            }

            if (action === 'delete') {
                if (!await AdminModal.confirm({ message: `Are you sure you want to delete ${selected.length} product(s)?`, danger: true, confirmText: 'Delete' })) {
                    return;
                }
            }

            executeBulkAction(action, selected);
        });
    }

    function executeBulkAction(action, productIds) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                         document.querySelector('meta[name=csrf-token]')?.content ||
                         AdminUtils.getCsrfToken();

        applyBulkActionBtn.disabled = true;
        applyBulkActionBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

        fetch(window.location.pathname + 'bulk-action/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                action: action,
                product_ids: productIds
            })
        })
        .then(response => {
            const contentType = response.headers.get('Content-Type') || '';
            if (contentType.includes('text/csv')) {
                return response.blob().then(blob => {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'products_export.csv';
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    URL.revokeObjectURL(url);
                    applyBulkActionBtn.disabled = false;
                    applyBulkActionBtn.innerHTML = '<i class="fas fa-check"></i> Apply';
                    showNotification('Export downloaded successfully', 'success');
                });
            }
            return response.json().then(data => {
                if (data.success) {
                    showNotification(data.message || 'Bulk action completed successfully', 'success');
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    showNotification(data.message || 'Bulk action failed', 'error');
                    applyBulkActionBtn.disabled = false;
                    applyBulkActionBtn.innerHTML = '<i class="fas fa-check"></i> Apply';
                }
            });
        })
        .catch(error => {
            console.error('Bulk action error:', error);
            showNotification('An error occurred while processing the action', 'error');
            applyBulkActionBtn.disabled = false;
            applyBulkActionBtn.innerHTML = '<i class="fas fa-check"></i> Apply';
        });
    }

    // ========== Copy SKU ==========
    document.querySelectorAll('.copy-sku-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const sku = this.dataset.sku;

            navigator.clipboard.writeText(sku).then(() => {
                showNotification(`SKU "${sku}" copied to clipboard`, 'success');

                const icon = this.querySelector('i');
                icon.classList.remove('fa-copy');
                icon.classList.add('fa-check');

                setTimeout(() => {
                    icon.classList.remove('fa-check');
                    icon.classList.add('fa-copy');
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy SKU:', err);
                showNotification('Failed to copy SKU', 'error');
            });
        });
    });

    // ========== Quick Delete ==========
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('.product-name a').textContent;

            if (!await AdminModal.confirm({ message: `Are you sure you want to delete "${productName}"?`, danger: true, confirmText: 'Delete' })) {
                return;
            }

            deleteProduct(productId, productCard);
        });
    });

    function deleteProduct(productId, productCard) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                         document.querySelector('meta[name=csrf-token]')?.content ||
                         AdminUtils.getCsrfToken();

        fetch(`${window.location.pathname}${productId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if (response.ok) {
                if (productCard) {
                    productCard.style.opacity = '0';
                    productCard.style.transform = 'scale(0.9)';
                    setTimeout(() => productCard.remove(), 300);
                }
                showNotification('Product deleted successfully', 'success');
            } else {
                showNotification('Failed to delete product', 'error');
            }
        })
        .catch(error => {
            console.error('Delete error:', error);
            showNotification('An error occurred while deleting the product', 'error');
        });
    }

    // ========== Quick Duplicate ==========
    document.querySelectorAll('.duplicate-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            duplicateProduct(productId);
        });
    });

    function duplicateProduct(productId) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
                         document.querySelector('meta[name=csrf-token]')?.content ||
                         AdminUtils.getCsrfToken();

        showNotification('Duplicating product...', 'info');

        fetch(`${window.location.pathname}${productId}/duplicate/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification('Product duplicated successfully', 'success');
                setTimeout(() => window.location.reload(), 1000);
            } else {
                showNotification(data.message || 'Failed to duplicate product', 'error');
            }
        })
        .catch(error => {
            console.error('Duplicate error:', error);
            showNotification('An error occurred while duplicating the product', 'error');
        });
    }

    // ========== Real-time Search ==========
    if (searchInput) {
        let searchTimeout;

        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);

            searchTimeout = setTimeout(() => {
                this.form.submit();
            }, 500);
        });
    }

    // ========== Helper Functions ==========
    function showNotification(message, type = 'info') {
        AdminModal.toast(message, type);
    }

});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .product-card {
        transition: opacity 0.3s, transform 0.3s;
    }
`;
document.head.appendChild(style);

/**
 * Infinite Scroll for Product Admin List
 * Uses IntersectionObserver to load next pages as user scrolls down.
 */
class ProductInfiniteScroll {
    constructor() {
        this.container = document.getElementById('products-container');
        this.sentinel = document.getElementById('scroll-sentinel');
        this.spinner = document.getElementById('scroll-spinner');
        this.endIndicator = document.getElementById('scroll-end');

        if (!this.container || !this.sentinel) return;

        // Django 5.1+ uses 1-indexed pages: page 1 = first, page N = last
        this.currentPage = parseInt(this.container.dataset.currentPage, 10) || 1;
        this.totalPages = parseInt(this.container.dataset.totalPages, 10) || 1;
        this.totalCount = parseInt(this.container.dataset.totalCount, 10) || 0;
        this.pageSize = parseInt(this.container.dataset.pageSize, 10) || 50;
        this.isLoading = false;

        // If everything fits on one page, hide sentinel entirely
        if (this.totalPages <= 1) {
            this.sentinel.style.display = 'none';
            return;
        }

        // If we're already on the last page
        if (this.currentPage >= this.totalPages) {
            this._showEnd();
            return;
        }

        this._initObserver();
    }

    _initObserver() {
        this.observer = new IntersectionObserver(
            (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && !this.isLoading) {
                        this._loadNextPage();
                    }
                });
            },
            {
                rootMargin: '0px 0px 300px 0px',
                threshold: 0
            }
        );

        this.observer.observe(this.sentinel);
    }

    async _loadNextPage() {
        if (this.isLoading || this.currentPage >= this.totalPages) return;

        this.isLoading = true;
        this._showSpinner();

        const nextPage = this.currentPage + 1;
        const params = new URLSearchParams(window.location.search);
        params.set('p', nextPage);

        try {
            const response = await fetch(
                window.location.pathname + '?' + params.toString(),
                { headers: { 'X-Requested-With': 'XMLHttpRequest' } }
            );

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            const newContainer = doc.querySelector('#products-container');
            if (newContainer) {
                const fragment = document.createDocumentFragment();
                newContainer.querySelectorAll('.product-card').forEach(card => {
                    fragment.appendChild(document.importNode(card, true));
                });
                this.container.appendChild(fragment);

                // Reattach event listeners to all cards (including new ones)
                if (typeof window.attachProductEventListeners === 'function') {
                    window.attachProductEventListeners();
                }
            }

            this.currentPage = nextPage;
            this.container.dataset.currentPage = nextPage;

            if (this.currentPage >= this.totalPages) {
                this._showEnd();
            } else {
                this._hideSpinner();
            }
        } catch (error) {
            console.error('[Infinite Scroll] Error loading page:', error);
            this._hideSpinner();
            // Stop observing on error to prevent infinite retry loops
            if (this.observer) this.observer.disconnect();
        } finally {
            this.isLoading = false;
        }
    }

    _showSpinner() {
        if (this.spinner) this.spinner.style.display = 'flex';
        if (this.endIndicator) this.endIndicator.style.display = 'none';
    }

    _hideSpinner() {
        if (this.spinner) this.spinner.style.display = 'none';
    }

    _showEnd() {
        if (this.spinner) this.spinner.style.display = 'none';
        if (this.endIndicator) this.endIndicator.style.display = 'flex';
        if (this.observer) this.observer.disconnect();
    }
}
