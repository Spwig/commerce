/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Category Masonry - Enhances CSS columns masonry layout.
 * Applies data-attribute driven column/gap settings and handles
 * responsive recalculation.
 */
(function() {
    'use strict';

    document.querySelectorAll('.cat-masonry').forEach(initMasonry);

    function initMasonry(container) {
        var columns = container.dataset.columns || '3';
        var gap = container.dataset.gap || 'md';

        // Apply modifier classes based on data attributes
        container.classList.add('cat-masonry--cols-' + columns);
        container.classList.add('cat-masonry--gap-' + gap);

        // Stagger animation on load
        var items = container.querySelectorAll('.cat-masonry__item');
        items.forEach(function(item, index) {
            item.style.animationDelay = (index * 50) + 'ms';
            item.classList.add('cat-masonry__item--animate');
        });

        // Handle image loading to prevent layout shifts
        var images = container.querySelectorAll('.cat-masonry__image');
        var loadedCount = 0;

        if (images.length === 0) return;

        images.forEach(function(img) {
            if (img.complete) {
                loadedCount++;
                if (loadedCount === images.length) {
                    onAllImagesLoaded();
                }
            } else {
                img.addEventListener('load', function() {
                    loadedCount++;
                    if (loadedCount === images.length) {
                        onAllImagesLoaded();
                    }
                });
                img.addEventListener('error', function() {
                    loadedCount++;
                    if (loadedCount === images.length) {
                        onAllImagesLoaded();
                    }
                });
            }
        });

        function onAllImagesLoaded() {
            container.classList.add('cat-masonry--loaded');
        }
    }
})();
