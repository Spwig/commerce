/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        // Filter elements
        var filterInputs = document.querySelectorAll('.filter-input');
        var clearFiltersBtn = document.getElementById('clearFilters');

        // Advanced filters elements
        var advancedWrapper = document.getElementById('advancedFiltersWrapper');
        var moreFiltersBtn = document.getElementById('moreFiltersBtn');
        var advancedFilterBadge = document.getElementById('advancedFilterBadge');

        var advancedFilterNames = [
            'brand', 'is_digital', 'has_digital_assets', 'requires_license',
            'pricing_strategy', 'on_sale', 'is_subscription', 'is_preorder',
            'is_featured', 'track_inventory', 'import_source'
        ];

        var debounceTimer = null;

        // Initialize filter inputs from URL params
        var urlParams = new URLSearchParams(window.location.search);
        filterInputs.forEach(function (input) {
            var filterName = input.dataset.filter;
            var value = urlParams.get(filterName);
            if (value) {
                input.value = value;
                input.classList.add('has-value');
            }
        });

        // Count active advanced filters and update badge
        function updateAdvancedBadge() {
            var count = 0;
            advancedFilterNames.forEach(function (name) {
                if (urlParams.get(name)) count++;
            });
            if (advancedFilterBadge) {
                if (count > 0) {
                    advancedFilterBadge.textContent = count;
                    advancedFilterBadge.classList.remove('product-list-hidden');
                } else {
                    advancedFilterBadge.classList.add('product-list-hidden');
                }
            }
            return count;
        }

        // Auto-expand advanced filters if any are active
        var activeAdvancedCount = updateAdvancedBadge();
        if (activeAdvancedCount > 0 && advancedWrapper) {
            advancedWrapper.classList.add('expanded');
            if (moreFiltersBtn) moreFiltersBtn.classList.add('expanded');
        }

        // Toggle advanced filters
        if (moreFiltersBtn && advancedWrapper) {
            moreFiltersBtn.addEventListener('click', function () {
                advancedWrapper.classList.toggle('expanded');
                moreFiltersBtn.classList.toggle('expanded');
            });
        }

        // Apply filters via URL navigation (persists with pagination)
        function applyFilters() {
            var params = new URLSearchParams();

            filterInputs.forEach(function (input) {
                var value = input.value.trim();
                var filterName = input.dataset.filter;

                if (value) {
                    input.classList.add('has-value');
                    params.set(filterName, value);
                } else {
                    input.classList.remove('has-value');
                }
            });

            // Navigate to URL with filter params
            var queryString = params.toString();
            window.location.href = window.location.pathname + (queryString ? '?' + queryString : '');
        }

        // Attach event listeners to filter inputs
        filterInputs.forEach(function (input) {
            var eventType = input.tagName === 'INPUT' ? 'input' : 'change';
            var debounceTime = input.tagName === 'INPUT' ? 500 : 0;

            input.addEventListener(eventType, function () {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(applyFilters, debounceTime);
            });
        });

        // Clear all filters
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', function () {
                filterInputs.forEach(function (input) {
                    input.value = '';
                    input.classList.remove('has-value');
                });
                window.location.href = window.location.pathname;
            });
        }

        // Initialize infinite scroll
        if (typeof ProductInfiniteScroll !== 'undefined') {
            window.productInfiniteScroll = new ProductInfiniteScroll();
        }
    });
})();
