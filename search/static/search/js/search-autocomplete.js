/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Search Autocomplete Component
 *
 * Provides predictive search suggestions with keyboard navigation,
 * language support, and click tracking.
 */
class SearchAutocomplete {
    constructor(inputElement, options = {}) {
        this.input = inputElement;
        this.options = {
            debounceMs: options.debounceMs || 300,
            minLength: options.minLength || 2,
            maxResults: options.maxResults || 8,
            engine: options.engine || 'shop',
            showThumbnails: options.showThumbnails !== false,
            apiBase: options.apiBase || '/api/search',
            onSelect: options.onSelect || null,
            ...options
        };

        this.dropdown = null;
        this.selectedIndex = -1;
        this.results = [];
        this.isOpen = false;
        this.debounceTimer = null;
        this.lastQuery = '';
        this.searchQueryId = null;
        this.displaySettings = this._getDefaultDisplaySettings();

        this.init();
    }

    /**
     * Get a UI string from the global registry, with fallback
     */
    _str(key, fallback) {
        if (window.UI_STRINGS && window.UI_STRINGS[key]) {
            return window.UI_STRINGS[key];
        }
        return fallback;
    }

    /**
     * Get default display settings
     */
    _getDefaultDisplaySettings() {
        return {
            // Products
            product_thumbnail: true,
            product_description: false,
            product_price: true,
            product_sku: true,
            product_stock_status: false,
            // Blog posts
            blog_thumbnail: true,
            blog_excerpt: true,
            blog_excerpt_length: 60,
            // Categories
            category_thumbnail: false,
            category_product_count: true,
            // Brands
            brand_logo: false,
            brand_product_count: true,
        };
    }

    init() {
        this.createDropdown();
        this.bindEvents();
        this.loadSettings();
    }

    /**
     * Get the current language from the page
     */
    getLanguage() {
        // Check data attribute first
        if (this.input.dataset.searchLang) {
            return this.input.dataset.searchLang;
        }
        // Check HTML lang attribute
        return document.documentElement.lang || 'en';
    }

    /**
     * Load search settings from the API
     */
    async loadSettings() {
        try {
            const response = await fetch(`${this.options.apiBase}/settings/`);
            if (response.ok) {
                const settings = await response.json();
                this.options.minLength = settings.min_query_length || this.options.minLength;
                this.options.debounceMs = settings.autocomplete_debounce_ms || this.options.debounceMs;
                this.options.maxResults = settings.autocomplete_max_results || this.options.maxResults;
                this.options.showThumbnails = settings.show_thumbnails !== false;

                // Load autocomplete display settings
                this.displaySettings = {
                    // Products
                    product_thumbnail: settings.autocomplete_product_thumbnail !== false,
                    product_description: settings.autocomplete_product_description === true,
                    product_price: settings.autocomplete_product_price !== false,
                    product_sku: settings.autocomplete_product_sku !== false,
                    product_stock_status: settings.autocomplete_product_stock_status === true,
                    // Blog posts
                    blog_thumbnail: settings.autocomplete_blog_thumbnail !== false,
                    blog_excerpt: settings.autocomplete_blog_excerpt !== false,
                    blog_excerpt_length: settings.autocomplete_blog_excerpt_length || 60,
                    // Categories
                    category_thumbnail: settings.autocomplete_category_thumbnail === true,
                    category_product_count: settings.autocomplete_category_product_count !== false,
                    // Brands
                    brand_logo: settings.autocomplete_brand_logo === true,
                    brand_product_count: settings.autocomplete_brand_product_count !== false,
                };
            }
        } catch (error) {
            console.warn('Could not load search settings:', error);
        }
    }

    /**
     * Create the autocomplete dropdown element
     */
    createDropdown() {
        this.dropdown = document.createElement('div');
        this.dropdown.className = 'search-autocomplete-dropdown';
        this.dropdown.setAttribute('role', 'listbox');
        this.dropdown.setAttribute('aria-label', 'Search suggestions');

        // Position relative to input
        const wrapper = this.input.parentElement;
        wrapper.classList.add('search-autocomplete-wrapper');
        wrapper.appendChild(this.dropdown);
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Input events
        this.input.addEventListener('input', this.handleInput.bind(this));
        this.input.addEventListener('focus', this.handleFocus.bind(this));
        this.input.addEventListener('blur', this.handleBlur.bind(this));
        this.input.addEventListener('keydown', this.handleKeyboard.bind(this));

        // Form submit
        const form = this.input.closest('form');
        if (form) {
            form.addEventListener('submit', this.handleSubmit.bind(this));
        }

        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.input.contains(e.target) && !this.dropdown.contains(e.target)) {
                this.close();
            }
        });
    }

    /**
     * Handle input changes with debouncing
     */
    handleInput(e) {
        const query = e.target.value.trim();

        clearTimeout(this.debounceTimer);

        if (query.length < this.options.minLength) {
            this.close();
            return;
        }

        this.debounceTimer = setTimeout(() => {
            this.search(query);
        }, this.options.debounceMs);
    }

    /**
     * Handle input focus
     */
    handleFocus() {
        if (this.input.value.trim().length >= this.options.minLength && this.results.length > 0) {
            this.open();
        }
    }

    /**
     * Handle input blur
     */
    handleBlur() {
        // Delay to allow click on dropdown items
        setTimeout(() => {
            if (!this.dropdown.contains(document.activeElement)) {
                this.close();
            }
        }, 200);
    }

    /**
     * Handle keyboard navigation
     */
    handleKeyboard(e) {
        if (!this.isOpen) {
            if (e.key === 'ArrowDown' && this.input.value.trim().length >= this.options.minLength) {
                this.search(this.input.value.trim());
            }
            return;
        }

        const items = this.dropdown.querySelectorAll('.autocomplete-item');

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.selectedIndex = Math.min(this.selectedIndex + 1, items.length - 1);
                this.updateSelection(items);
                break;

            case 'ArrowUp':
                e.preventDefault();
                this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
                this.updateSelection(items);
                break;

            case 'Enter':
                if (this.selectedIndex >= 0 && items[this.selectedIndex]) {
                    e.preventDefault();
                    this.selectItem(items[this.selectedIndex]);
                }
                break;

            case 'Escape':
                e.preventDefault();
                this.close();
                this.input.blur();
                break;

            case 'Tab':
                this.close();
                break;
        }
    }

    /**
     * Update visual selection state
     */
    updateSelection(items) {
        items.forEach((item, index) => {
            item.classList.toggle('selected', index === this.selectedIndex);
            item.setAttribute('aria-selected', index === this.selectedIndex);
        });

        if (this.selectedIndex >= 0 && items[this.selectedIndex]) {
            items[this.selectedIndex].scrollIntoView({ block: 'nearest' });
        }
    }

    /**
     * Handle form submit
     */
    handleSubmit(e) {
        // If an item is selected, navigate to it instead of searching
        const items = this.dropdown.querySelectorAll('.autocomplete-item');
        if (this.selectedIndex >= 0 && items[this.selectedIndex]) {
            e.preventDefault();
            this.selectItem(items[this.selectedIndex]);
        }
    }

    /**
     * Perform search
     */
    async search(query) {
        if (query === this.lastQuery) return;
        this.lastQuery = query;

        const lang = this.getLanguage();
        const url = `${this.options.apiBase}/autocomplete/?q=${encodeURIComponent(query)}&lang=${lang}&engine=${this.options.engine}&limit=${this.options.maxResults}`;

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('Search failed');

            const data = await response.json();

            // Handle redirect
            if (data.redirect) {
                window.location.href = data.redirect.url;
                return;
            }

            // Store search query ID for click tracking
            this.searchQueryId = data.search_query_id;

            this.results = data;
            this.renderResults(data);

            if (data.total_count > 0) {
                this.open();
            } else {
                this.close();
            }

        } catch (error) {
            console.error('Search error:', error);
            this.close();
        }
    }

    /**
     * Render search results
     */
    renderResults(data) {
        this.dropdown.innerHTML = '';
        this.selectedIndex = -1;

        let itemIndex = 0;

        // Did you mean suggestion
        if (data.did_you_mean) {
            const suggestion = document.createElement('div');
            suggestion.className = 'autocomplete-suggestion';
            const didYouMeanText = this._str('js.search_did_you_mean', 'Did you mean:');
            suggestion.innerHTML = `
                <span class="suggestion-text">${this.escapeHtml(didYouMeanText)} </span>
                <a href="?q=${encodeURIComponent(data.did_you_mean)}" class="suggestion-link">${this.escapeHtml(data.did_you_mean)}</a>
            `;
            this.dropdown.appendChild(suggestion);
        }

        // Products section
        if (data.products && data.products.length > 0) {
            this.renderSection(this._str('js.search_products', 'Products'), data.products, 'product', itemIndex);
            itemIndex += data.products.length;
        }

        // Categories section
        if (data.categories && data.categories.length > 0) {
            this.renderSection(this._str('js.search_categories', 'Categories'), data.categories, 'category', itemIndex);
            itemIndex += data.categories.length;
        }

        // Brands section
        if (data.brands && data.brands.length > 0) {
            this.renderSection(this._str('js.search_brands', 'Brands'), data.brands, 'brand', itemIndex);
            itemIndex += data.brands.length;
        }

        // Blog posts section
        if (data.blog_posts && data.blog_posts.length > 0) {
            this.renderSection(this._str('js.search_blog', 'Blog'), data.blog_posts, 'blog_post', itemIndex);
            itemIndex += data.blog_posts.length;
        }

        // View all link
        if (data.total_count > 0) {
            const viewAll = document.createElement('a');
            viewAll.className = 'autocomplete-view-all';
            const lang = this.getLanguage();
            viewAll.href = `/${lang}/search/?q=${encodeURIComponent(data.query)}`;
            const viewAllText = this._str('js.search_view_all_results', 'View all {count} results').replace('{count}', data.total_count);
            viewAll.innerHTML = `${this.escapeHtml(viewAllText)} <i class="fas fa-arrow-right"></i>`;
            this.dropdown.appendChild(viewAll);
        }
    }

    /**
     * Render a section of results
     */
    renderSection(title, items, type, startIndex) {
        const section = document.createElement('div');
        section.className = 'autocomplete-section';

        const header = document.createElement('div');
        header.className = 'autocomplete-section-header';
        header.textContent = title;
        section.appendChild(header);

        items.forEach((item, index) => {
            const element = this.createResultItem(item, type, startIndex + index);
            section.appendChild(element);
        });

        this.dropdown.appendChild(section);
    }

    /**
     * Create a result item element
     */
    createResultItem(item, type, index) {
        const element = document.createElement('div');
        element.className = `autocomplete-item autocomplete-item--${type}`;
        element.setAttribute('role', 'option');
        element.setAttribute('data-index', index);
        element.setAttribute('data-url', item.url);
        element.setAttribute('data-type', type);
        element.setAttribute('data-id', item.id);

        let html = '';
        const ds = this.displaySettings;

        // Thumbnail/logo based on type and settings
        if (type === 'product' && ds.product_thumbnail && item.thumbnail) {
            html += `<img src="${item.thumbnail}" alt="" class="autocomplete-thumbnail" loading="lazy">`;
        } else if (type === 'category' && ds.category_thumbnail && item.thumbnail) {
            html += `<img src="${item.thumbnail}" alt="" class="autocomplete-thumbnail" loading="lazy">`;
        } else if (type === 'brand' && ds.brand_logo && item.logo) {
            html += `<img src="${item.logo}" alt="" class="autocomplete-logo" loading="lazy">`;
        } else if (type === 'blog_post' && ds.blog_thumbnail && item.thumbnail) {
            html += `<img src="${item.thumbnail}" alt="" class="autocomplete-thumbnail" loading="lazy">`;
        }

        html += '<div class="autocomplete-content">';

        // Name/title
        const name = item.name || item.title;
        html += `<span class="autocomplete-name">${this.escapeHtml(name)}</span>`;

        // Additional info based on type
        if (type === 'product') {
            // Price
            if (ds.product_price) {
                html += `<span class="autocomplete-price">${item.currency} ${item.price}</span>`;
            }
            // SKU
            if (ds.product_sku && item.sku) {
                html += `<span class="autocomplete-sku">SKU: ${this.escapeHtml(item.sku)}</span>`;
            }
            // Stock status
            if (ds.product_stock_status) {
                const stockClass = item.in_stock ? 'autocomplete-stock--in-stock' : 'autocomplete-stock--out-of-stock';
                const stockText = item.in_stock
                    ? this._str('js.search_in_stock', 'In Stock')
                    : this._str('js.search_out_of_stock', 'Out of Stock');
                html += `<span class="autocomplete-stock ${stockClass}">${this.escapeHtml(stockText)}</span>`;
            }
            // Description
            if (ds.product_description && item.description) {
                html += `<span class="autocomplete-description">${this.escapeHtml(item.description.substring(0, 80))}...</span>`;
            }
        } else if (type === 'category') {
            if (ds.category_product_count && item.product_count !== undefined) {
                const countText = this._str('js.search_products_count', '{count} products').replace('{count}', item.product_count);
                html += `<span class="autocomplete-count">${this.escapeHtml(countText)}</span>`;
            }
        } else if (type === 'brand') {
            if (ds.brand_product_count && item.product_count !== undefined) {
                const countText = this._str('js.search_products_count', '{count} products').replace('{count}', item.product_count);
                html += `<span class="autocomplete-count">${this.escapeHtml(countText)}</span>`;
            }
        } else if (type === 'blog_post') {
            if (ds.blog_excerpt && item.excerpt) {
                const maxLen = ds.blog_excerpt_length || 60;
                const excerpt = item.excerpt.length > maxLen ? item.excerpt.substring(0, maxLen) + '...' : item.excerpt;
                html += `<span class="autocomplete-excerpt">${this.escapeHtml(excerpt)}</span>`;
            }
        }

        // Translation indicator
        if (item.is_translated) {
            html += '<span class="autocomplete-translated" title="Available in your language"><i class="fas fa-language"></i></span>';
        }

        html += '</div>';

        element.innerHTML = html;

        // Click handler
        element.addEventListener('click', () => this.selectItem(element));

        // Mouse hover
        element.addEventListener('mouseenter', () => {
            this.selectedIndex = index;
            const items = this.dropdown.querySelectorAll('.autocomplete-item');
            this.updateSelection(items);
        });

        return element;
    }

    /**
     * Select an item and navigate to it
     */
    selectItem(element) {
        const url = element.dataset.url;
        const type = element.dataset.type;
        const id = element.dataset.id;
        const position = parseInt(element.dataset.index) + 1;

        // Track click
        this.trackClick(type, id, position);

        // Callback
        if (this.options.onSelect) {
            this.options.onSelect({ url, type, id, position });
        }

        // Navigate
        window.location.href = url;
    }

    /**
     * Track a click on a search result
     */
    async trackClick(type, objectId, position) {
        if (!this.searchQueryId) return;

        const contentTypeMap = {
            'product': 'catalog.product',
            'category': 'catalog.category',
            'brand': 'catalog.brand',
            'blog_post': 'blog.blogpost',
        };

        try {
            await fetch(`${this.options.apiBase}/click/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken(),
                },
                body: JSON.stringify({
                    search_query_id: this.searchQueryId,
                    content_type: contentTypeMap[type] || type,
                    object_id: parseInt(objectId),
                    position: position,
                }),
            });
        } catch (error) {
            console.warn('Could not track click:', error);
        }
    }

    /**
     * Get CSRF token from cookie
     */
    getCSRFToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input) return input.value;
        return '';
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Open the dropdown
     */
    open() {
        this.dropdown.classList.add('search-autocomplete-dropdown--open');
        this.isOpen = true;
        this.input.setAttribute('aria-expanded', 'true');
    }

    /**
     * Close the dropdown
     */
    close() {
        this.dropdown.classList.remove('search-autocomplete-dropdown--open');
        this.isOpen = false;
        this.selectedIndex = -1;
        this.input.setAttribute('aria-expanded', 'false');
    }
}

// Auto-initialize on elements with data-search-autocomplete attribute
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-search-autocomplete]').forEach(input => {
        new SearchAutocomplete(input, {
            engine: input.dataset.searchEngine || 'shop',
            maxResults: parseInt(input.dataset.searchMaxResults) || 8,
            debounceMs: parseInt(input.dataset.searchDebounce) || 300,
        });
    });
});

// Export for manual initialization
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SearchAutocomplete;
}
