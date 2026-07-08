/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var configEl = document.getElementById('licenseprovider-config');
        if (!configEl) return;
        var config = JSON.parse(configEl.textContent);

        var providerId = config.providerId;
        var languageCode = config.languageCode;

        // URLs
        var getMappingsUrl = '/' + languageCode + '/admin/catalog/license-provider/' + providerId + '/mappings/';
        var saveMappingUrl = '/' + languageCode + '/admin/catalog/license-provider/' + providerId + '/mappings/save/';
        var deleteMappingUrl = '/' + languageCode + '/admin/catalog/license-provider/' + providerId + '/mappings/delete/';
        var searchProductsUrl = '/' + languageCode + '/admin/catalog/license-provider/search-products/';

        // Elements
        var productSearch = document.getElementById('product-search');
        var productSearchResults = document.getElementById('product-search-results');
        var selectedProductId = document.getElementById('selected-product-id');
        var externalIdInput = document.getElementById('external-id');
        var addMappingBtn = document.getElementById('add-mapping-btn');
        var mappingsContainer = document.getElementById('mappings-container');

        var searchTimeout;

        // Load existing mappings
        loadMappings();

        // Product search
        productSearch.addEventListener('input', function () {
            clearTimeout(searchTimeout);
            var query = this.value.trim();

            if (query.length < 2) {
                productSearchResults.classList.remove('active');
                return;
            }

            searchTimeout = setTimeout(function () { searchProducts(query); }, 300);
        });

        productSearch.addEventListener('focus', function () {
            if (this.value.trim().length >= 2) {
                searchProducts(this.value.trim());
            }
        });

        document.addEventListener('click', function (e) {
            if (!productSearch.contains(e.target) && !productSearchResults.contains(e.target)) {
                productSearchResults.classList.remove('active');
            }
        });

        // Add mapping button
        addMappingBtn.addEventListener('click', function () {
            var productId = selectedProductId.value;
            var externalId = externalIdInput.value.trim();

            if (!productId) {
                showToast(config.strings.selectProduct, 'error');
                return;
            }

            if (!externalId) {
                showToast(config.strings.enterExternalId, 'error');
                return;
            }

            saveMapping(productId, externalId);
        });

        // Event delegation for dynamically generated buttons
        document.addEventListener('click', function (e) {
            var btn = e.target.closest('[data-action="delete-mapping"]');
            if (btn) {
                deleteMapping(parseInt(btn.dataset.productId, 10));
            }
        });

        // Functions
        function loadMappings() {
            fetch(getMappingsUrl, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success) {
                    renderMappings(data.mappings);
                } else {
                    mappingsContainer.innerHTML = '<div class="mappings-empty"><p>' + data.error + '</p></div>';
                }
            })
            .catch(function (error) {
                console.error('Error loading mappings:', error);
                mappingsContainer.innerHTML = '<div class="mappings-empty"><p>' + config.strings.errorLoadingMappings + '</p></div>';
            });
        }

        function searchProducts(query) {
            fetch(searchProductsUrl + '?q=' + encodeURIComponent(query) + '&provider_id=' + providerId, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success && data.products.length > 0) {
                    productSearchResults.innerHTML = data.products.map(function (product) {
                        return '<div class="product-search-item" data-id="' + product.id + '" data-name="' + escapeHtml(product.name) + '">' +
                            (product.thumbnail ? '<img src="' + product.thumbnail + '" class="product-thumb" alt="">' : '<div class="product-thumb"></div>') +
                            '<div class="product-info">' +
                            '<div class="product-name">' + escapeHtml(product.name) + '</div>' +
                            (product.sku ? '<div class="product-sku">SKU: ' + escapeHtml(product.sku) + '</div>' : '') +
                            '</div></div>';
                    }).join('');

                    // Add click handlers
                    productSearchResults.querySelectorAll('.product-search-item').forEach(function (item) {
                        item.addEventListener('click', function () {
                            selectedProductId.value = this.dataset.id;
                            productSearch.value = this.dataset.name;
                            productSearchResults.classList.remove('active');
                        });
                    });

                    productSearchResults.classList.add('active');
                } else {
                    productSearchResults.innerHTML = '<div class="product-search-item no-results">' + config.strings.noProductsFound + '</div>';
                    productSearchResults.classList.add('active');
                }
            })
            .catch(function (error) {
                console.error('Error searching products:', error);
            });
        }

        function saveMapping(productId, externalId) {
            addMappingBtn.disabled = true;
            addMappingBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + config.strings.saving;

            var csrfToken = getCsrfToken();

            fetch(saveMappingUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ product_id: productId, external_id: externalId })
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success) {
                    showToast(data.message, 'success');
                    selectedProductId.value = '';
                    productSearch.value = '';
                    externalIdInput.value = '';
                    loadMappings();
                } else {
                    showToast(data.error, 'error');
                }
            })
            .catch(function (error) {
                console.error('Error saving mapping:', error);
                showToast(config.strings.errorSavingMapping, 'error');
            })
            .finally(function () {
                addMappingBtn.disabled = false;
                addMappingBtn.innerHTML = '<i class="fas fa-plus"></i> ' + config.strings.addMapping;
            });
        }

        async function deleteMapping(productId) {
            if (!await AdminModal.confirm({ message: config.strings.confirmDelete, danger: true, confirmText: 'Delete' })) return;

            var csrfToken = getCsrfToken();

            fetch(deleteMappingUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ product_id: productId })
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.success) {
                    showToast(data.message, 'success');
                    loadMappings();
                } else {
                    showToast(data.error, 'error');
                }
            })
            .catch(function (error) {
                console.error('Error deleting mapping:', error);
                showToast(config.strings.errorRemovingMapping, 'error');
            });
        }

        function renderMappings(mappings) {
            if (!mappings || mappings.length === 0) {
                mappingsContainer.innerHTML =
                    '<div class="mappings-empty">' +
                    '<i class="fas fa-link"></i>' +
                    '<p>' + config.strings.noMappings + '</p>' +
                    '</div>';
                return;
            }

            var rows = mappings.map(function (mapping) {
                return '<tr>' +
                    '<td><div class="product-cell"><div class="product-details">' +
                    '<div class="product-name">' + escapeHtml(mapping.product_name) + '</div>' +
                    (mapping.product_sku ? '<div class="product-sku">SKU: ' + escapeHtml(mapping.product_sku) + '</div>' : '') +
                    '</div></div></td>' +
                    '<td><span class="external-id">' + escapeHtml(mapping.external_id) + '</span></td>' +
                    '<td class="actions-cell">' +
                    '<button type="button" class="delete-btn" data-action="delete-mapping" data-product-id="' + mapping.product_id + '" title="' + config.strings.removeMapping + '">' +
                    '<i class="fas fa-trash"></i></button></td>' +
                    '</tr>';
            }).join('');

            mappingsContainer.innerHTML =
                '<table class="mappings-table"><thead><tr>' +
                '<th>' + config.strings.product + '</th>' +
                '<th>' + config.strings.externalId + '</th>' +
                '<th></th></tr></thead>' +
                '<tbody>' + rows + '</tbody></table>';
        }

        function showToast(message, type) {
            AdminModal.toast(message, type || 'info');
        }

        function escapeHtml(text) {
            var div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function getCsrfToken() {
            return AdminUtils.getCsrfToken();
        }
    });
})();
