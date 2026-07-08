/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Product page functionality: image thumbnail gallery and variant selection.
 * Used by page_builder/templates/page_builder/page.html when page_type == 'product'.
 */
(function () {
    'use strict';

    function initProductPage() {
        var thumbnails = document.querySelectorAll('.thumbnail');
        var mainImage = document.getElementById('main-product-image');

        if (mainImage && thumbnails.length) {
            thumbnails.forEach(function (thumb) {
                thumb.addEventListener('click', function () {
                    mainImage.src = this.dataset.full;
                    thumbnails.forEach(function (t) { t.classList.remove('active'); });
                    this.classList.add('active');
                });
            });
        }

        var variantSelects = document.querySelectorAll('.variant-select');
        if (variantSelects.length) {
            variantSelects.forEach(function (select) {
                select.addEventListener('change', updateProductInfo);
            });
        }

        function updateProductInfo() {
            var selectedVariants = {};
            variantSelects.forEach(function (select) {
                if (select.value) {
                    selectedVariants[select.name] = select.value;
                }
            });
            // Find matching variant and update display
            // Implementation depends on your variant system
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initProductPage);
    } else {
        initProductPage();
    }
})();
