/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Product Card Interactions
 * Handles add-to-cart, quick-view triggers, and wishlist from product cards.
 * Uses event delegation on document for cards rendered anywhere on the page.
 */
(function() {
    'use strict';

    // --- Add to Cart ---
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.product-card__add-btn');
        if (!btn || btn.disabled || btn.classList.contains('is-loading')) return;

        e.preventDefault();
        const productId = parseInt(btn.dataset.productId, 10);
        if (!productId) return;

        // Show loading state
        btn.classList.add('is-loading');

        // Use the global addToCart from base.html
        if (typeof addToCart === 'function') {
            addToCart(productId, 1, null);
        }

        // Re-enable after a timeout (addToCart doesn't return a promise)
        setTimeout(function() {
            btn.classList.remove('is-loading');
        }, 2000);
    });

    // --- Quick View (variable products) ---
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.product-card__quickview-btn') ||
                    e.target.closest('.product-card__action-btn--quickview');
        if (!btn) return;

        e.preventDefault();
        const slug = btn.dataset.productSlug;
        if (!slug) return;

        // Delegate to QuickView module (loaded from quick-view.js)
        if (window.QuickView) {
            window.QuickView.open(slug);
        } else {
            // Fallback: navigate to product page
            var lang = document.documentElement.lang || 'en';
            window.location.href = '/' + lang + '/product/' + slug + '/';
        }
    });

    // --- Wishlist ---
    // Map of product_id (string) → wishlist_item_id (int)
    var wishlistedItems = {};
    var wishlistLoaded = false;

    function loadWishlistState() {
        fetch('/api/wishlists/product-ids/', {
            credentials: 'same-origin',
            headers: { 'Accept': 'application/json' }
        })
        .then(function(response) {
            if (response.status === 401 || response.status === 403) {
                // User not authenticated — no wishlist state to load
                return null;
            }
            if (!response.ok) return null;
            return response.json();
        })
        .then(function(data) {
            if (!data) return;
            wishlistedItems = data.wishlisted || {};
            wishlistLoaded = true;
            // Mark existing wishlisted buttons
            document.querySelectorAll('.product-card__action-btn--wishlist').forEach(function(btn) {
                var productId = btn.dataset.productId;
                if (productId && wishlistedItems[productId]) {
                    btn.classList.add('is-active');
                    btn.dataset.wishlistItemId = wishlistedItems[productId];
                    var icon = btn.querySelector('i');
                    if (icon) {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                    }
                }
            });
        })
        .catch(function() {
            // Silently fail — wishlist state is non-critical
        });
    }

    // Load wishlist state on page load
    loadWishlistState();

    function setWishlistVisual(btn, active) {
        var icon = btn.querySelector('i');
        if (active) {
            btn.classList.add('is-active');
            if (icon) { icon.classList.remove('far'); icon.classList.add('fas'); }
        } else {
            btn.classList.remove('is-active');
            if (icon) { icon.classList.remove('fas'); icon.classList.add('far'); }
        }
    }

    document.addEventListener('click', function(e) {
        var btn = e.target.closest('.product-card__action-btn--wishlist');
        if (!btn || btn.classList.contains('is-loading')) return;

        e.preventDefault();
        var productId = btn.dataset.productId;
        if (!productId) return;

        var isCurrentlyActive = btn.classList.contains('is-active');
        var csrfToken = window.getCSRFToken();

        btn.classList.add('is-loading');

        if (isCurrentlyActive) {
            // Remove from wishlist
            var itemId = btn.dataset.wishlistItemId;
            if (!itemId) {
                btn.classList.remove('is-loading');
                return;
            }

            fetch('/api/wishlists/items/' + itemId + '/', {
                method: 'DELETE',
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Accept': 'application/json'
                }
            })
            .then(function(response) {
                btn.classList.remove('is-loading');
                if (response.ok) {
                    // Update all buttons for this product (multiple cards on same page)
                    document.querySelectorAll('.product-card__action-btn--wishlist[data-product-id="' + productId + '"]').forEach(function(b) {
                        setWishlistVisual(b, false);
                        delete b.dataset.wishlistItemId;
                    });
                    delete wishlistedItems[productId];
                    window.showNotification(
                        window._mt('removed_from_wishlist', 'Removed from wishlist'),
                        'success'
                    );
                } else {
                    window.showNotification(
                        window._mt('wishlist_error', 'Could not update wishlist'),
                        'error'
                    );
                }
            })
            .catch(function() {
                btn.classList.remove('is-loading');
                window.showNotification(
                    window._mt('wishlist_error', 'Could not update wishlist'),
                    'error'
                );
            });
        } else {
            // Add to wishlist
            fetch('/api/wishlists/add/', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ product_id: parseInt(productId, 10) })
            })
            .then(function(response) {
                if (response.status === 401 || response.status === 403) {
                    btn.classList.remove('is-loading');
                    // Redirect to login
                    var lang = document.documentElement.lang || 'en';
                    window.location.href = '/' + lang + '/account/login/?next=' + encodeURIComponent(window.location.pathname);
                    return null;
                }
                return response.json();
            })
            .then(function(data) {
                if (!data) return;
                btn.classList.remove('is-loading');
                if (data.success) {
                    // Extract the wishlist item ID from the response
                    var wishlistItemId = null;
                    var items = data.wishlist && data.wishlist.items;
                    if (items) {
                        for (var i = 0; i < items.length; i++) {
                            if (items[i].product && items[i].product.id === parseInt(productId, 10)) {
                                wishlistItemId = items[i].id;
                                wishlistedItems[productId] = wishlistItemId;
                                break;
                            }
                        }
                    }
                    // Update all buttons for this product (multiple cards on same page)
                    document.querySelectorAll('.product-card__action-btn--wishlist[data-product-id="' + productId + '"]').forEach(function(b) {
                        setWishlistVisual(b, true);
                        if (wishlistItemId) b.dataset.wishlistItemId = wishlistItemId;
                    });
                    window.showNotification(
                        window._mt('added_to_wishlist', 'Added to wishlist!'),
                        'success'
                    );
                } else {
                    window.showNotification(
                        data.message || window._mt('wishlist_error', 'Could not update wishlist'),
                        'error'
                    );
                }
            })
            .catch(function() {
                btn.classList.remove('is-loading');
                window.showNotification(
                    window._mt('wishlist_error', 'Could not update wishlist'),
                    'error'
                );
            });
        }
    });

})();
