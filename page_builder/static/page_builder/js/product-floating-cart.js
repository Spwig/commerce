/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const floatingBar = document.getElementById('floating-cart-bar');
        const mainAddToCart = document.getElementById('add-to-cart');
        const floatingAddToCart = document.getElementById('floating-add-to-cart');

        if (!floatingBar || !mainAddToCart) return;

        // Show/hide floating bar based on main button visibility
        let ticking = false;

        function updateFloatingBar() {
            const rect = mainAddToCart.getBoundingClientRect();
            const isOutOfView = rect.bottom < 0 || rect.top > window.innerHeight;

            if (isOutOfView) {
                floatingBar.classList.add('floating-cart-bar--visible');
                floatingBar.setAttribute('aria-hidden', 'false');
                floatingBar.style.display = '';
            } else {
                floatingBar.classList.remove('floating-cart-bar--visible');
                floatingBar.setAttribute('aria-hidden', 'true');
            }
            ticking = false;
        }

        window.addEventListener('scroll', function() {
            if (!ticking) {
                requestAnimationFrame(updateFloatingBar);
                ticking = true;
            }
        }, { passive: true });

        // Floating button mirrors the main add-to-cart
        if (floatingAddToCart) {
            floatingAddToCart.addEventListener('click', function() {
                // Sync variant ID from main button
                const variantId = mainAddToCart.dataset.variantId;
                if (variantId) {
                    this.dataset.variantId = variantId;
                }

                // Trigger click on the main (hidden) add-to-cart button
                mainAddToCart.click();

                // Mirror loading state
                const originalContent = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                this.disabled = true;

                setTimeout(function() {
                    floatingAddToCart.innerHTML = originalContent;
                    floatingAddToCart.disabled = false;
                }, 2500);
            });
        }

        // Keep floating price in sync when variant changes
        const priceObserver = new MutationObserver(function() {
            const mainPrice = document.getElementById('product-price');
            const floatingPrice = document.getElementById('floating-price');
            if (mainPrice && floatingPrice) {
                floatingPrice.innerHTML = mainPrice.innerHTML;
            }
        });

        const priceEl = document.getElementById('product-price');
        if (priceEl) {
            priceObserver.observe(priceEl, { childList: true, subtree: true, characterData: true });
        }

        // Initial check
        updateFloatingBar();
    });
})();
