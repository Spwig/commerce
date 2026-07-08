/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Home page functionality: featured products carousel.
 * Used by page_builder/templates/page_builder/page.html when page_type == 'home'.
 */
(function () {
    'use strict';

    function initHomePage() {
        var carousel = document.querySelector('.products-carousel');
        if (!carousel) return;

        var scrollAmount = 0;
        var scrollMax = carousel.scrollWidth - carousel.clientWidth;

        var nextBtn = document.querySelector('.carousel-next');
        var prevBtn = document.querySelector('.carousel-prev');

        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                scrollMax = carousel.scrollWidth - carousel.clientWidth;
                scrollAmount = Math.min(scrollAmount + 320, scrollMax);
                carousel.scrollTo({ left: scrollAmount, behavior: 'smooth' });
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                scrollAmount = Math.max(scrollAmount - 320, 0);
                carousel.scrollTo({ left: scrollAmount, behavior: 'smooth' });
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initHomePage);
    } else {
        initHomePage();
    }
})();
