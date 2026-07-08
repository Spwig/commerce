/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Category page "Load More" pagination handler.
 * Fetches the next page and appends product cards to the grid.
 */
(function() {
    'use strict';

    const btn = document.querySelector('.load-more__btn');
    if (!btn) return;

    btn.addEventListener('click', async function() {
        const nextPage = this.dataset.nextPage;
        const sort = this.dataset.sort;
        const baseUrl = this.dataset.url || window.location.pathname;

        this.disabled = true;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';

        try {
            const url = `${baseUrl}?sort=${encodeURIComponent(sort)}&page=${nextPage}`;
            const resp = await fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const html = await resp.text();

            // Parse the response and extract product cards
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newProducts = doc.querySelectorAll('.product-card');
            const grid = document.querySelector('.product-grid');

            newProducts.forEach(function(card) {
                grid.appendChild(document.importNode(card, true));
            });

            // Check if there are more pages
            const newLoadMoreBtn = doc.querySelector('.load-more__btn');
            if (newLoadMoreBtn) {
                btn.dataset.nextPage = newLoadMoreBtn.dataset.nextPage;
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-plus"></i> Load More Products';
            } else {
                // No more pages - remove the load more section
                btn.closest('.load-more').remove();
                return;
            }

            // Update the info text
            const info = document.querySelector('.load-more__info');
            const newInfo = doc.querySelector('.load-more__info');
            if (info && newInfo) {
                info.innerHTML = newInfo.innerHTML;
            }

        } catch (err) {
            console.error('Load more error:', err);
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-plus"></i> Load More Products';
        }
    });
})();
