/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Search Element Component
 *
 * Extends the base SearchAutocomplete functionality with:
 * - Element-specific configuration via data attributes
 * - Inline results display (AJAX)
 * - Content type filtering
 * - Custom dropdown container support
 */
class SearchElement {
    constructor(element) {
        this.element = element;
        this.input = element.querySelector('.search__input');
        this.form = element.querySelector('.search__form');
        this.dropdown = element.querySelector('.search__dropdown');
        this.resultsContainer = element.querySelector('[data-inline-results-container]');

        if (!this.input) {
            console.warn('SearchElement: No input found');
            return;
        }

        this.config = this.parseConfig();
        this.autocomplete = null;
        this.currentPage = 1;
        this.totalResults = 0;
        this.currentQuery = '';
        this.currentFilter = 'all';
        this.allResults = null;

        this.init();
    }

    /**
     * Parse configuration from data attributes
     */
    parseConfig() {
        const input = this.input;
        return {
            elementId: input.dataset.searchElementId,
            useGlobalSettings: input.dataset.searchUseGlobal === 'true',
            minLength: parseInt(input.dataset.searchMinLength) || 2,
            debounceMs: parseInt(input.dataset.searchDebounce) || 300,
            maxResults: parseInt(input.dataset.searchMaxResults) || 8,
            submitAction: input.dataset.searchSubmitAction || 'redirect',
            resultsUrl: input.dataset.searchResultsUrl || '/search/',
            // Content types
            contentTypes: {
                products: input.dataset.searchProducts !== 'false',
                categories: input.dataset.searchCategories !== 'false',
                brands: input.dataset.searchBrands !== 'false',
                blog_posts: input.dataset.searchBlog !== 'false'
            },
            // Display settings
            displaySettings: {
                product_thumbnail: input.dataset.searchThumbnails !== 'false',
                product_price: input.dataset.searchPrices !== 'false',
                product_sku: input.dataset.searchSku === 'true',
                product_stock_status: input.dataset.searchStock === 'true',
                category_product_count: input.dataset.searchCount !== 'false',
                brand_product_count: input.dataset.searchCount !== 'false',
                show_view_all: input.dataset.searchViewAll !== 'false'
            },
            // Inline results config
            inline: this.parseInlineConfig()
        };
    }

    /**
     * Parse inline results configuration
     */
    parseInlineConfig() {
        const container = this.resultsContainer;
        if (!container) return null;

        return {
            layout: container.dataset.inlineLayout || 'grid',
            columns: container.dataset.inlineColumns || '4',
            maxResults: parseInt(container.dataset.inlineMaxResults) || 12,
            showFilters: container.dataset.inlineShowFilters === 'true',
            showPagination: container.dataset.inlineShowPagination === 'true',
            emptyMessage: container.dataset.inlineEmptyMessage || 'No results found.'
        };
    }

    /**
     * Initialize the search element
     */
    init() {
        this.initAutocomplete();
        this.bindFormEvents();

        if (this.resultsContainer) {
            this.bindInlineResultsEvents();
        }
    }

    /**
     * Initialize autocomplete with element-specific settings
     */
    initAutocomplete() {
        if (!this.input.hasAttribute('data-search-autocomplete')) return;
        if (typeof SearchAutocomplete === 'undefined') {
            console.warn('SearchElement: SearchAutocomplete not available');
            return;
        }

        const options = {
            engine: 'shop',
            onSelect: (item) => this.handleAutocompleteSelect(item)
        };

        // Use element-specific settings if not using global
        if (!this.config.useGlobalSettings) {
            options.minLength = this.config.minLength;
            options.debounceMs = this.config.debounceMs;
            options.maxResults = this.config.maxResults;
        }

        // Use custom dropdown if available
        if (this.dropdown) {
            // The autocomplete will use its own dropdown, but we can style ours
            // For now, let the default autocomplete handle it
        }

        this.autocomplete = new SearchAutocomplete(this.input, options);

        // Override display settings if configured
        if (!this.config.useGlobalSettings) {
            this.autocomplete.displaySettings = {
                ...this.autocomplete.displaySettings,
                ...this.config.displaySettings
            };
        }
    }

    /**
     * Handle autocomplete item selection
     */
    handleAutocompleteSelect(item) {
        // Default behavior - navigate to item URL
        // Can be overridden for custom behavior
    }

    /**
     * Bind form events
     */
    bindFormEvents() {
        if (!this.form) return;

        this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
    }

    /**
     * Handle form submission
     */
    handleFormSubmit(e) {
        const action = this.config.submitAction;

        if (action === 'autocomplete_only') {
            e.preventDefault();
            return;
        }

        if (action === 'inline') {
            e.preventDefault();
            this.loadInlineResults();
            return;
        }

        // Default: allow form to submit (redirect)
    }

    /**
     * Bind inline results events
     */
    bindInlineResultsEvents() {
        // Filter buttons
        const filterButtons = this.resultsContainer.querySelectorAll('.search__results-filter');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', () => this.handleFilterClick(btn));
        });

        // Load more button
        const loadMoreBtn = this.resultsContainer.querySelector('.search__results-load-more');
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', () => this.loadMoreResults());
        }
    }

    /**
     * Handle filter button click
     */
    handleFilterClick(button) {
        const filterType = button.dataset.filterType;

        // Update active state
        this.resultsContainer.querySelectorAll('.search__results-filter').forEach(btn => {
            btn.classList.remove('search__results-filter--active');
            btn.setAttribute('aria-selected', 'false');
        });
        button.classList.add('search__results-filter--active');
        button.setAttribute('aria-selected', 'true');

        this.currentFilter = filterType;
        this.renderFilteredResults();
    }

    /**
     * Load inline search results
     */
    async loadInlineResults() {
        const query = this.input.value.trim();
        if (query.length < this.config.minLength) return;

        this.currentQuery = query;
        this.currentPage = 1;
        this.currentFilter = 'all';

        // Show results container
        this.resultsContainer.hidden = false;

        // Build API URL
        const lang = document.documentElement.lang || 'en';
        const params = new URLSearchParams({
            q: query,
            lang: lang,
            engine: 'shop',
            per_page: this.config.inline.maxResults
        });

        // Add content type filters
        const types = [];
        if (this.config.contentTypes.products) types.push('product');
        if (this.config.contentTypes.categories) types.push('category');
        if (this.config.contentTypes.brands) types.push('brand');
        if (this.config.contentTypes.blog_posts) types.push('blog_post');
        if (types.length < 4) {
            params.set('type', types.join(','));
        }

        try {
            const response = await fetch(`/api/search/results/?${params}`);
            if (!response.ok) throw new Error('Search failed');

            const data = await response.json();
            this.allResults = data;
            this.totalResults = data.total_count || 0;

            this.renderInlineResults(data);
            this.updateResultsCount(data);
            this.updateViewAllLink(query);

        } catch (error) {
            console.error('Search error:', error);
            this.showEmptyState();
        }
    }

    /**
     * Render inline results
     */
    renderInlineResults(data) {
        const grid = this.resultsContainer.querySelector('.search__results-grid');
        const emptyState = this.resultsContainer.querySelector('.search__results-empty');
        const pagination = this.resultsContainer.querySelector('.search__results-pagination');

        // Clear existing results
        grid.innerHTML = '';

        // Count total results across all types
        const totalCount = (data.products?.length || 0) +
                          (data.categories?.length || 0) +
                          (data.brands?.length || 0) +
                          (data.blog_posts?.length || 0);

        if (totalCount === 0) {
            this.showEmptyState();
            return;
        }

        // Hide empty state
        if (emptyState) emptyState.hidden = true;

        // Render results based on current filter
        this.renderFilteredResults();

        // Show/hide pagination
        if (pagination && this.config.inline.showPagination) {
            pagination.hidden = this.totalResults <= this.config.inline.maxResults;
        }

        // Update filter counts
        this.updateFilterCounts(data);
    }

    /**
     * Render results filtered by current filter
     */
    renderFilteredResults() {
        const grid = this.resultsContainer.querySelector('.search__results-grid');
        grid.innerHTML = '';

        if (!this.allResults) return;

        const data = this.allResults;
        let results = [];

        // Collect results based on filter
        if (this.currentFilter === 'all' || this.currentFilter === 'products') {
            if (data.products) {
                results = results.concat(data.products.map(p => ({...p, type: 'product'})));
            }
        }
        if (this.currentFilter === 'all' || this.currentFilter === 'categories') {
            if (data.categories) {
                results = results.concat(data.categories.map(c => ({...c, type: 'category'})));
            }
        }
        if (this.currentFilter === 'all' || this.currentFilter === 'brands') {
            if (data.brands) {
                results = results.concat(data.brands.map(b => ({...b, type: 'brand'})));
            }
        }
        if (this.currentFilter === 'all' || this.currentFilter === 'blog_posts') {
            if (data.blog_posts) {
                results = results.concat(data.blog_posts.map(p => ({...p, type: 'blog_post'})));
            }
        }

        // Render cards
        results.forEach(item => {
            const card = this.createResultCard(item);
            grid.appendChild(card);
        });

        // Show empty state if no results for this filter
        const emptyState = this.resultsContainer.querySelector('.search__results-empty');
        if (emptyState) {
            emptyState.hidden = results.length > 0;
        }
    }

    /**
     * Create a result card element
     */
    createResultCard(item) {
        const card = document.createElement('a');
        card.className = `search__results-card search__results-card--${item.type}`;
        card.href = item.url;

        let html = '';

        // Thumbnail
        const thumbnail = item.thumbnail || item.logo || item.image;
        if (thumbnail && this.config.displaySettings.product_thumbnail) {
            html += `<div class="search__results-card-image">
                <img src="${thumbnail}" alt="" loading="lazy">
            </div>`;
        }

        html += '<div class="search__results-card-content">';

        // Type badge
        const typeLabels = {
            product: 'Product',
            category: 'Category',
            brand: 'Brand',
            blog_post: 'Blog'
        };
        html += `<span class="search__results-card-type">${typeLabels[item.type] || item.type}</span>`;

        // Name/title
        const name = item.name || item.title;
        html += `<h3 class="search__results-card-title">${this.escapeHtml(name)}</h3>`;

        // Type-specific content
        if (item.type === 'product') {
            if (this.config.displaySettings.product_price && item.price) {
                html += `<span class="search__results-card-price">${item.currency || ''} ${item.price}</span>`;
            }
            if (this.config.displaySettings.product_sku && item.sku) {
                html += `<span class="search__results-card-sku">SKU: ${this.escapeHtml(item.sku)}</span>`;
            }
            if (this.config.displaySettings.product_stock_status) {
                const stockClass = item.in_stock ? 'in-stock' : 'out-of-stock';
                const stockText = item.in_stock ? 'In Stock' : 'Out of Stock';
                html += `<span class="search__results-card-stock search__results-card-stock--${stockClass}">${stockText}</span>`;
            }
        } else if (item.type === 'category' || item.type === 'brand') {
            if (this.config.displaySettings.category_product_count && item.product_count !== undefined) {
                html += `<span class="search__results-card-count">${item.product_count} products</span>`;
            }
        } else if (item.type === 'blog_post') {
            if (item.excerpt) {
                const excerpt = item.excerpt.length > 100 ? item.excerpt.substring(0, 100) + '...' : item.excerpt;
                html += `<p class="search__results-card-excerpt">${this.escapeHtml(excerpt)}</p>`;
            }
        }

        html += '</div>';

        card.innerHTML = html;
        return card;
    }

    /**
     * Update results count display
     */
    updateResultsCount(data) {
        const countEl = this.resultsContainer.querySelector('.search__results-count');
        if (countEl) {
            const total = data.total_count || 0;
            countEl.textContent = `${total} result${total !== 1 ? 's' : ''} for "${this.currentQuery}"`;
        }
    }

    /**
     * Update view all link
     */
    updateViewAllLink(query) {
        const link = this.resultsContainer.querySelector('.search__results-view-all');
        if (link) {
            link.href = `${this.config.resultsUrl}?q=${encodeURIComponent(query)}`;
        }
    }

    /**
     * Update filter button counts
     */
    updateFilterCounts(data) {
        const filters = this.resultsContainer.querySelectorAll('.search__results-filter');
        filters.forEach(btn => {
            const type = btn.dataset.filterType;
            let count = 0;

            if (type === 'all') {
                count = (data.products?.length || 0) +
                       (data.categories?.length || 0) +
                       (data.brands?.length || 0) +
                       (data.blog_posts?.length || 0);
            } else if (type === 'products') {
                count = data.products?.length || 0;
            } else if (type === 'categories') {
                count = data.categories?.length || 0;
            } else if (type === 'brands') {
                count = data.brands?.length || 0;
            } else if (type === 'blog_posts') {
                count = data.blog_posts?.length || 0;
            }

            // Update button text with count
            const originalText = btn.textContent.replace(/\s*\(\d+\)$/, '');
            btn.textContent = `${originalText} (${count})`;

            // Disable if no results
            btn.disabled = count === 0 && type !== 'all';
        });
    }

    /**
     * Load more results
     */
    async loadMoreResults() {
        this.currentPage++;

        const lang = document.documentElement.lang || 'en';
        const params = new URLSearchParams({
            q: this.currentQuery,
            lang: lang,
            engine: 'shop',
            page: this.currentPage,
            per_page: this.config.inline.maxResults
        });

        try {
            const response = await fetch(`/api/search/results/?${params}`);
            if (!response.ok) throw new Error('Load more failed');

            const data = await response.json();

            // Append new results to existing
            if (data.products) {
                this.allResults.products = [...(this.allResults.products || []), ...data.products];
            }
            if (data.categories) {
                this.allResults.categories = [...(this.allResults.categories || []), ...data.categories];
            }
            if (data.brands) {
                this.allResults.brands = [...(this.allResults.brands || []), ...data.brands];
            }
            if (data.blog_posts) {
                this.allResults.blog_posts = [...(this.allResults.blog_posts || []), ...data.blog_posts];
            }

            this.renderFilteredResults();

            // Hide load more if no more results
            const pagination = this.resultsContainer.querySelector('.search__results-pagination');
            if (pagination) {
                const totalLoaded = (this.allResults.products?.length || 0) +
                                   (this.allResults.categories?.length || 0) +
                                   (this.allResults.brands?.length || 0) +
                                   (this.allResults.blog_posts?.length || 0);
                pagination.hidden = totalLoaded >= this.totalResults;
            }

        } catch (error) {
            console.error('Load more error:', error);
        }
    }

    /**
     * Show empty state
     */
    showEmptyState() {
        const grid = this.resultsContainer.querySelector('.search__results-grid');
        const emptyState = this.resultsContainer.querySelector('.search__results-empty');
        const pagination = this.resultsContainer.querySelector('.search__results-pagination');

        if (grid) grid.innerHTML = '';
        if (emptyState) emptyState.hidden = false;
        if (pagination) pagination.hidden = true;
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

/**
 * Initialize all search elements on page load
 */
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-search-element]').forEach(element => {
        new SearchElement(element);
    });
});

// Export for manual initialization
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SearchElement;
}
