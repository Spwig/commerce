/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Sale products element: countdown timer and carousel navigation.
 * Auto-initializes all .sale-products sections on the page.
 */
(function () {
    'use strict';

    function initSaleProducts(section) {
        // Countdown functionality
        var countdowns = section.querySelectorAll('.sale-products__countdown[data-ends]');
        countdowns.forEach(function (countdown) {
            var timer = countdown.querySelector('.sale-products__countdown-timer');
            var endDate = new Date(countdown.dataset.ends).getTime();

            function update() {
                var now = Date.now();
                var diff = endDate - now;

                if (diff <= 0) {
                    if (timer) timer.textContent = 'Ended';
                    return;
                }

                var days = Math.floor(diff / (1000 * 60 * 60 * 24));
                var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                var mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

                if (timer) {
                    timer.textContent = days > 0
                        ? days + 'd ' + hours + 'h'
                        : hours + 'h ' + mins + 'm';
                }
            }

            update();
            setInterval(update, 60000);
        });

        // Carousel navigation
        if (section.classList.contains('sale-products--carousel')) {
            var container = section.querySelector('.sale-products__container');
            var prevBtn = section.querySelector('.sale-products__arrow--prev');
            var nextBtn = section.querySelector('.sale-products__arrow--next');

            if (prevBtn && nextBtn && container) {
                prevBtn.addEventListener('click', function () {
                    var scrollAmount = container.offsetWidth * 0.8;
                    container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
                });

                nextBtn.addEventListener('click', function () {
                    var scrollAmount = container.offsetWidth * 0.8;
                    container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
                });
            }
        }
    }

    function init() {
        document.querySelectorAll('.sale-products').forEach(initSaleProducts);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
