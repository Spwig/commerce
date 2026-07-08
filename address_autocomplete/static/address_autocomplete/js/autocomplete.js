/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Address Autocomplete Widget for Spwig E-commerce Platform
 * Provides smart address search and form filling capabilities
 */

class AddressAutocomplete {
    constructor(element, options = {}) {
        // Element can be selector string or DOM element
        this.element = typeof element === 'string'
            ? document.querySelector(element)
            : element;

        if (!this.element) {
            console.error('AddressAutocomplete: Element not found');
            return;
        }

        // Default options
        this.options = {
            minChars: 3,
            delay: 500,
            maxSuggestions: 10,
            scrollThreshold: 4,
            autoDetectCountry: true,
            postalCodeFirst: false,
            placeholder: 'Start typing an address...',
            apiUrl: '/api/address/autocomplete',
            normalizeUrl: '/api/address/normalize',
            validateUrl: '/api/address/validate',
            reverseUrl: '/api/address/reverse',
            onSelect: null,
            onError: null,
            fieldMapping: {
                address1: '[name="shipping_address1"], #id_shipping_address1',
                address2: '[name="shipping_address2"], #id_shipping_address2',
                city: '[name="shipping_city"], #id_shipping_city',
                state: '[name="shipping_state"], #id_shipping_state',
                postal_code: '[name="shipping_postal_code"], #id_shipping_postal_code',
                country: '[name="shipping_country"], #id_shipping_country',
                latitude: '[name="latitude"], #id_latitude',
                longitude: '[name="longitude"], #id_longitude'
            },
            ...options
        };

        // State
        this.cache = new Map();
        this.debounceTimer = null;
        this.currentRequest = null;
        this.selectedSuggestion = null;
        this.isOpen = false;
        this.isLoading = false;
        this.lastQuery = null;

        // Initialize
        this.init();
    }

    init() {
        // Add class to element
        this.element.classList.add('address-autocomplete-input');

        // Set placeholder
        if (this.options.placeholder) {
            this.element.placeholder = this.options.placeholder;
        }

        // Create suggestions container
        this.createSuggestionsContainer();

        // Bind events
        this.bindEvents();

        // Auto-detect country if enabled
        if (this.options.autoDetectCountry) {
            this.detectCountry();
        }

        // Check for postal code first mode
        if (this.options.postalCodeFirst) {
            this.setupPostalCodeFirst();
        }
    }

    createSuggestionsContainer() {
        // Create container
        this.suggestionsContainer = document.createElement('div');
        this.suggestionsContainer.className = 'address-autocomplete-suggestions';
        this.suggestionsContainer.style.display = 'none';

        // Position relative to input
        const parent = this.element.parentElement;
        parent.style.position = 'relative';
        parent.appendChild(this.suggestionsContainer);

        // Create loading indicator
        this.loadingIndicator = document.createElement('div');
        this.loadingIndicator.className = 'address-autocomplete-loading';
        this.loadingIndicator.innerHTML = '<span class="spinner"></span> Searching...';
        this.loadingIndicator.style.display = 'none';
        this.suggestionsContainer.appendChild(this.loadingIndicator);

        // Create suggestions list
        this.suggestionsList = document.createElement('ul');
        this.suggestionsList.className = 'address-autocomplete-list';
        this.suggestionsContainer.appendChild(this.suggestionsList);
    }

    bindEvents() {
        // Input events
        this.element.addEventListener('input', this.handleInput.bind(this));
        this.element.addEventListener('focus', this.handleFocus.bind(this));
        this.element.addEventListener('blur', this.handleBlur.bind(this));
        this.element.addEventListener('keydown', this.handleKeydown.bind(this));

        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.element.contains(e.target) && !this.suggestionsContainer.contains(e.target)) {
                this.close();
            }
        });

        // Window resize
        window.addEventListener('resize', this.positionSuggestions.bind(this));
    }

    handleInput(e) {
        const query = e.target.value.trim();

        // Clear timer
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }

        // Check minimum characters
        if (query.length < this.options.minChars) {
            this.close();
            return;
        }

        // Debounce search
        this.debounceTimer = setTimeout(() => {
            this.search(query);
        }, this.options.delay);
    }

    handleFocus(e) {
        // Show suggestions if we have them
        if (this.suggestionsList.children.length > 0) {
            this.open();
        }
    }

    handleBlur(e) {
        // Delay close to allow click on suggestion
        setTimeout(() => {
            this.close();
        }, 200);
    }

    handleKeydown(e) {
        if (!this.isOpen) return;

        const items = this.suggestionsList.querySelectorAll('li');
        let currentIndex = Array.from(items).findIndex(item => item.classList.contains('selected'));

        switch(e.key) {
            case 'ArrowDown':
                e.preventDefault();
                if (currentIndex < items.length - 1) {
                    this.selectItem(items[currentIndex + 1], currentIndex + 1);
                }
                break;

            case 'ArrowUp':
                e.preventDefault();
                if (currentIndex > 0) {
                    this.selectItem(items[currentIndex - 1], currentIndex - 1);
                } else if (currentIndex === -1 && items.length > 0) {
                    this.selectItem(items[items.length - 1], items.length - 1);
                }
                break;

            case 'Enter':
                e.preventDefault();
                if (currentIndex >= 0) {
                    this.handleSuggestionClick(items[currentIndex].dataset.suggestion);
                }
                break;

            case 'Escape':
                this.close();
                break;
        }
    }

    async search(query) {
        const normalizedQuery = query.trim();

        // Don't search if identical query already in progress
        if (this.isLoading && this.lastQuery === normalizedQuery) {
            return;
        }

        // Check cache
        const cacheKey = this.getCacheKey(normalizedQuery);
        if (this.cache.has(cacheKey)) {
            this.displaySuggestions(this.cache.get(cacheKey));
            return;
        }

        // Cancel previous request
        if (this.currentRequest) {
            this.currentRequest.abort();
        }

        // Set loading state
        this.isLoading = true;
        this.lastQuery = normalizedQuery;

        // Show loading
        this.showLoading();

        try {
            // Create abort controller
            const controller = new AbortController();
            this.currentRequest = controller;

            // Build URL with parameters
            const params = new URLSearchParams({
                q: normalizedQuery,
                limit: this.options.maxSuggestions
            });

            // Add country bias if available
            const countryBias = this.getCountryBias();
            if (countryBias) {
                params.append('country', countryBias);
            }

            // Add geo bias if available
            const geoBias = this.getGeoBias();
            if (geoBias) {
                params.append('lat', geoBias.lat);
                params.append('lon', geoBias.lon);
            }

            // Make request
            const response = await fetch(`${this.options.apiUrl}?${params}`, {
                signal: controller.signal,
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();

            // Cache result
            this.cache.set(cacheKey, data);

            // Display suggestions
            this.displaySuggestions(data);

        } catch (error) {
            if (error.name !== 'AbortError') {
                console.error('Search error:', error);
                this.showError('Search failed. Please try again.');
                if (this.options.onError) {
                    this.options.onError(error);
                }
            }
        } finally {
            this.hideLoading();
            this.currentRequest = null;
            this.isLoading = false;
        }
    }

    displaySuggestions(data) {
        // Clear current suggestions
        this.suggestionsList.innerHTML = '';

        if (!data.suggestions || data.suggestions.length === 0) {
            this.showNoResults();
            return;
        }

        // Add suggestions
        data.suggestions.forEach((suggestion, index) => {
            const li = document.createElement('li');
            li.className = 'address-autocomplete-item';
            li.dataset.suggestion = JSON.stringify(suggestion);
            li.dataset.index = index;

            // Add country match indicator
            const isCountryMatch = this._isCountryMatch(suggestion);
            if (isCountryMatch) {
                li.classList.add('country-match');
            }

            // Build display HTML
            let html = `<span class="suggestion-label">${this._escapeHtml(suggestion.label)}</span>`;

            if (isCountryMatch) {
                html += '<span class="country-badge" title="From your country">📍</span>';
            }

            if (suggestion.confidence) {
                const conf = Math.round(suggestion.confidence * 100);
                html += `<span class="confidence" title="Confidence: ${conf}%">●</span>`;
            }

            li.innerHTML = html;

            // Click handler
            li.addEventListener('click', () => {
                this.handleSuggestionClick(suggestion);
            });

            // Hover handler
            li.addEventListener('mouseenter', () => {
                this.selectItem(li, index);
            });

            this.suggestionsList.appendChild(li);
        });

        // Add scroll hint if more than threshold
        if (data.suggestions.length > this.options.scrollThreshold) {
            this.suggestionsList.classList.add('has-scroll');
        } else {
            this.suggestionsList.classList.remove('has-scroll');
        }

        // Open suggestions
        this.open();
    }

    selectItem(item, index) {
        // Remove previous selection
        this.suggestionsList.querySelectorAll('.selected').forEach(el => {
            el.classList.remove('selected');
        });

        // Add selection
        item.classList.add('selected');
    }

    handleSuggestionClick(suggestionData) {
        // Parse suggestion if it's a string
        const suggestion = typeof suggestionData === 'string'
            ? JSON.parse(suggestionData)
            : suggestionData;

        this.selectedSuggestion = suggestion;

        // Fill form fields
        this.fillFormFields(suggestion);

        // Update input with label
        this.element.value = suggestion.label;

        // Close suggestions
        this.close();

        // Callback
        if (this.options.onSelect) {
            this.options.onSelect(suggestion);
        }

        // Track selection for analytics
        this.trackSelection(suggestion);
    }

    fillFormFields(suggestion) {
        const components = suggestion.components || {};

        // Map components to form fields
        const fieldMap = {
            address1: () => {
                const parts = [];
                if (components.house_number) parts.push(components.house_number);
                if (components.road) parts.push(components.road);
                return parts.join(' ');
            },
            address2: () => components.unit || components.suburb || '',
            city: () => components.city || components.town || components.village || '',
            state: () => components.state || components.region || '',
            postal_code: () => components.postcode || components.postal_code || '',
            country: () => components.country || ''  // Now enriched with full country name from backend
        };

        // Fill each field (always set value to clear old data, even if empty)
        Object.entries(this.options.fieldMapping).forEach(([field, selector]) => {
            const element = document.querySelector(selector);
            if (element && fieldMap[field]) {
                const value = fieldMap[field]() || ''; // Use empty string if no value
                element.value = value;
                // Trigger change event
                element.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });

        // Add coordinates if available
        if (suggestion.centroid) {
            this.fillCoordinates(suggestion.centroid);
        }
    }

    fillCoordinates(centroid) {
        if (this.options.fieldMapping.latitude) {
            const latElement = document.querySelector(this.options.fieldMapping.latitude);
            if (latElement) {
                latElement.value = centroid.lat;
            }
        }

        if (this.options.fieldMapping.longitude) {
            const lonElement = document.querySelector(this.options.fieldMapping.longitude);
            if (lonElement) {
                lonElement.value = centroid.lon;
            }
        }
    }

    async normalizeAddress(address) {
        try {
            const response = await fetch(this.options.normalizeUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ address })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return await response.json();

        } catch (error) {
            console.error('Normalize error:', error);
            return null;
        }
    }

    async validateAddress(addressData) {
        try {
            const params = new URLSearchParams(addressData);
            const response = await fetch(`${this.options.validateUrl}?${params}`, {
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return await response.json();

        } catch (error) {
            console.error('Validate error:', error);
            return { valid: false, errors: ['Validation failed'] };
        }
    }

    detectCountry() {
        // Try to get from GeoIP (if available in window object)
        if (window.GeoIP && window.GeoIP.country) {
            this.detectedCountry = window.GeoIP.country;
        }
    }

    getCountryBias() {
        // Check for explicit country field
        if (this.options.fieldMapping.country) {
            const countryElement = document.querySelector(this.options.fieldMapping.country);
            if (countryElement && countryElement.value) {
                return countryElement.value;
            }
        }

        // Return detected country
        return this.detectedCountry;
    }

    getGeoBias() {
        // Check if we have coordinates from GeoIP
        if (window.GeoIP && window.GeoIP.coordinates) {
            return window.GeoIP.coordinates;
        }
        return null;
    }

    setupPostalCodeFirst() {
        // Find postal code field
        const postalField = document.querySelector(this.options.fieldMapping.postal_code);
        if (postalField) {
            // Focus on postal code field first
            postalField.focus();

            // Watch for postal code changes
            postalField.addEventListener('change', async (e) => {
                const postalCode = e.target.value;
                const country = this.getCountryBias();

                if (postalCode && country) {
                    // Search by postal code
                    await this.search(`${postalCode}, ${country}`);
                }
            });
        }
    }

    getCacheKey(query) {
        const country = this.getCountryBias();
        const geo = this.getGeoBias();
        return `${query}-${country || ''}-${geo ? `${geo.lat},${geo.lon}` : ''}`;
    }

    _isCountryMatch(suggestion) {
        if (!this.detectedCountry || !suggestion.components) {
            return false;
        }
        const suggestionCountry = suggestion.components.country_code || '';
        return suggestionCountry.toUpperCase() === this.detectedCountry.toUpperCase();
    }

    _escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showLoading() {
        this.loadingIndicator.style.display = 'block';
        this.suggestionsList.style.display = 'none';
    }

    hideLoading() {
        this.loadingIndicator.style.display = 'none';
        this.suggestionsList.style.display = 'block';
    }

    showError(message) {
        this.suggestionsList.innerHTML = `
            <li class="address-autocomplete-error">
                <span class="error-icon">⚠</span> ${message}
            </li>
        `;
        this.open();
    }

    showNoResults() {
        this.suggestionsList.innerHTML = `
            <li class="address-autocomplete-no-results">
                No addresses found. Try typing more details.
            </li>
        `;
        this.open();
    }

    open() {
        this.suggestionsContainer.style.display = 'block';
        this.isOpen = true;
        this.positionSuggestions();
    }

    close() {
        this.suggestionsContainer.style.display = 'none';
        this.isOpen = false;
    }

    positionSuggestions() {
        if (!this.isOpen) return;

        const rect = this.element.getBoundingClientRect();
        const containerRect = this.element.parentElement.getBoundingClientRect();

        this.suggestionsContainer.style.top = `${rect.bottom - containerRect.top}px`;
        this.suggestionsContainer.style.left = `${rect.left - containerRect.left}px`;
        this.suggestionsContainer.style.width = `${rect.width}px`;
    }

    trackSelection(suggestion) {
        // Send analytics event (if analytics service is available)
        if (window.analytics) {
            window.analytics.track('Address Selected', {
                suggestion_id: suggestion.id,
                label: suggestion.label,
                confidence: suggestion.confidence
            });
        }
    }

    destroy() {
        // Remove event listeners
        this.element.removeEventListener('input', this.handleInput);
        this.element.removeEventListener('focus', this.handleFocus);
        this.element.removeEventListener('blur', this.handleBlur);
        this.element.removeEventListener('keydown', this.handleKeydown);

        // Remove suggestions container
        if (this.suggestionsContainer && this.suggestionsContainer.parentElement) {
            this.suggestionsContainer.parentElement.removeChild(this.suggestionsContainer);
        }

        // Clear state
        this.cache.clear();
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
    }
}

// Auto-initialize on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    // Find all elements with data-address-autocomplete attribute
    document.querySelectorAll('[data-address-autocomplete]').forEach(element => {
        // Parse options - first check data-options JSON blob, then individual attrs
        var options = {};
        if (element.dataset.options) {
            try { options = JSON.parse(element.dataset.options); } catch (e) {}
        }

        // Individual data attributes override JSON blob
        if (element.dataset.minChars) options.minChars = parseInt(element.dataset.minChars);
        if (element.dataset.delay) options.delay = parseInt(element.dataset.delay);
        if (element.dataset.maxSuggestions) options.maxSuggestions = parseInt(element.dataset.maxSuggestions);
        if (element.dataset.postalCodeFirst) options.postalCodeFirst = element.dataset.postalCodeFirst === 'true';

        // Initialize autocomplete
        new AddressAutocomplete(element, options);
    });
});

// Export for use as module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AddressAutocomplete;
}

// Make available globally
window.AddressAutocomplete = AddressAutocomplete;