/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * StoreLocator - Interactive store locator with map and search
 * Handles map initialization, store loading, search, and marker management
 * Requires Leaflet.js to be loaded first
 */
class StoreLocator {
  constructor(element) {
    this.element = element;
    this.mapContainer = element.querySelector('#store-map');
    this.listContainer = element.querySelector('#stores-list');
    this.searchInput = element.querySelector('#location-search');
    this.searchBtn = element.querySelector('[data-search-btn]');

    if (!this.mapContainer) {
      return;
    }

    this.config = this.parseConfig();
    this.map = null;
    this.markers = [];
    this.stores = [];

    this.init();
  }

  parseConfig() {
    return {
      apiUrl: this.element.dataset.apiUrl || '/api/catalog/pickup-locations/',
      defaultLat: parseFloat(this.element.dataset.defaultLat) || 40.7128,
      defaultLng: parseFloat(this.element.dataset.defaultLng) || -74.006,
      defaultZoom: parseInt(this.element.dataset.defaultZoom) || 4,
      // Translations passed via data attributes
      noLocationsText: this.element.dataset.noLocationsText || 'No store locations available',
      errorText: this.element.dataset.errorText || 'Error loading store locations',
      noResultsText: this.element.dataset.noResultsText || 'No stores found matching your search',
      pickupAvailableText: this.element.dataset.pickupAvailableText || 'Pickup available',
    };
  }

  async init() {
    // Wait for Leaflet to be available
    if (typeof L === 'undefined') {
      console.error('StoreLocator: Leaflet.js is required but not loaded');
      return;
    }

    this.initializeMap();
    this.setupEventListeners();
    await this.loadStores();
  }

  initializeMap() {
    // Fix Leaflet default marker icon paths for self-hosted deployment
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl:
        (this.element.dataset.leafletImages || '/static/core/vendor/leaflet/images') +
        '/marker-icon-2x.png',
      iconUrl:
        (this.element.dataset.leafletImages || '/static/core/vendor/leaflet/images') +
        '/marker-icon.png',
      shadowUrl:
        (this.element.dataset.leafletImages || '/static/core/vendor/leaflet/images') +
        '/marker-shadow.png',
    });

    // Initialize Leaflet map
    this.map = L.map(this.mapContainer).setView(
      [this.config.defaultLat, this.config.defaultLng],
      this.config.defaultZoom
    );

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19,
    }).addTo(this.map);
  }

  setupEventListeners() {
    // Search button click
    if (this.searchBtn) {
      this.searchBtn.addEventListener('click', () => this.searchStores());
    }

    // Also support inline onclick on the button (for backwards compatibility)
    const legacySearchBtn = this.element.querySelector('button[onclick*="searchStores"]');
    if (legacySearchBtn) {
      legacySearchBtn.removeAttribute('onclick');
      legacySearchBtn.addEventListener('click', () => this.searchStores());
    }

    // Enter key to trigger search
    if (this.searchInput) {
      this.searchInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') {
          this.searchStores();
        }
      });
    }
  }

  async loadStores() {
    try {
      const response = await fetch(this.config.apiUrl);
      const data = await response.json();
      this.stores = data.locations || [];

      if (this.stores.length === 0) {
        this.showEmptyState(this.config.noLocationsText);
        return;
      }

      // Display stores
      this.displayStores(this.stores);

      // Add markers to map
      this.addMarkersToMap(this.stores);
    } catch (error) {
      console.error('Error loading stores:', error);
      this.showErrorState(this.config.errorText);
    }
  }

  showEmptyState(message) {
    this.listContainer.innerHTML = `
            <div class="empty-state">
                <svg class="empty-state__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <p class="empty-state__text">${message}</p>
            </div>
        `;
  }

  showErrorState(message) {
    this.listContainer.innerHTML = `
            <div class="empty-state empty-state--error">
                <svg class="empty-state__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <p class="empty-state__text">${message}</p>
            </div>
        `;
  }

  displayStores(storesToDisplay) {
    let html = '';

    storesToDisplay.forEach((location, index) => {
      const warehouse = location.warehouse;

      html += `
                <div class="store-card" data-store-index="${index}">
                    <h4 class="store-card__name">${this.escapeHtml(warehouse.name)}</h4>
                    <div class="store-card__details">
                        <div class="store-card__detail">
                            <svg class="store-card__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                            </svg>
                            <div>
                                ${this.escapeHtml(warehouse.address_line1)}<br>
                                ${this.escapeHtml(warehouse.city)}, ${this.escapeHtml(warehouse.state_province || '')} ${this.escapeHtml(warehouse.postal_code)}
                            </div>
                        </div>
                        ${
                          warehouse.contact_phone
                            ? `
                            <div class="store-card__detail">
                                <svg class="store-card__icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
                                </svg>
                                ${this.escapeHtml(warehouse.contact_phone)}
                            </div>
                        `
                            : ''
                        }
                        ${
                          warehouse.supports_pickup
                            ? `
                            <div class="store-card__badge store-card__badge--success">
                                <svg class="store-card__badge-icon" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                                </svg>
                                ${this.escapeHtml(this.config.pickupAvailableText)}
                            </div>
                        `
                            : ''
                        }
                    </div>
                </div>
            `;
    });

    this.listContainer.innerHTML = html;

    // Add click handlers to store cards
    this.listContainer.querySelectorAll('.store-card').forEach(card => {
      card.addEventListener('click', () => {
        const index = parseInt(card.dataset.storeIndex);
        this.focusStore(index);
      });
    });
  }

  addMarkersToMap(storesToDisplay) {
    // Clear existing markers
    this.markers.forEach(marker => marker.remove());
    this.markers = [];

    const bounds = [];

    storesToDisplay.forEach((location, index) => {
      const warehouse = location.warehouse;

      if (warehouse.latitude && warehouse.longitude) {
        const lat = parseFloat(warehouse.latitude);
        const lng = parseFloat(warehouse.longitude);

        // Create marker
        const marker = L.marker([lat, lng]).addTo(this.map);

        // Create popup
        marker.bindPopup(`
                    <div class="store-popup">
                        <h4 class="store-popup__name">${this.escapeHtml(warehouse.name)}</h4>
                        <div class="store-popup__details">
                            <p>${this.escapeHtml(warehouse.address_line1)}</p>
                            <p>${this.escapeHtml(warehouse.city)}, ${this.escapeHtml(warehouse.state_province || '')} ${this.escapeHtml(warehouse.postal_code)}</p>
                            ${warehouse.contact_phone ? `<p class="store-popup__phone">${this.escapeHtml(warehouse.contact_phone)}</p>` : ''}
                            ${warehouse.supports_pickup ? '<p class="store-popup__pickup">✓ Pickup available</p>' : ''}
                        </div>
                    </div>
                `);

        this.markers.push(marker);
        bounds.push([lat, lng]);
      }
    });

    // Fit map to show all markers
    if (bounds.length > 0) {
      this.map.fitBounds(bounds, { padding: [50, 50] });
    }
  }

  focusStore(index) {
    const location = this.stores[index];
    if (!location) return;

    const warehouse = location.warehouse;

    if (warehouse.latitude && warehouse.longitude) {
      const lat = parseFloat(warehouse.latitude);
      const lng = parseFloat(warehouse.longitude);

      // Center map on store
      this.map.setView([lat, lng], 15);

      // Open marker popup
      if (this.markers[index]) {
        this.markers[index].openPopup();
      }
    }
  }

  searchStores() {
    const query = this.searchInput?.value.trim().toLowerCase();

    if (!query) {
      // Reset to show all stores
      this.displayStores(this.stores);
      this.addMarkersToMap(this.stores);
      return;
    }

    // Filter stores by search query
    const filtered = this.stores.filter(location => {
      const warehouse = location.warehouse;
      return (
        warehouse.name.toLowerCase().includes(query) ||
        warehouse.address_line1.toLowerCase().includes(query) ||
        warehouse.city.toLowerCase().includes(query) ||
        warehouse.state_province?.toLowerCase().includes(query) ||
        warehouse.postal_code.toLowerCase().includes(query) ||
        warehouse.country.toLowerCase().includes(query)
      );
    });

    if (filtered.length === 0) {
      this.showEmptyState(this.config.noResultsText);
    } else {
      this.displayStores(filtered);
    }
    this.addMarkersToMap(filtered);
  }

  escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  destroy() {
    if (this.map) {
      this.map.remove();
    }
    this.markers = [];
    this.stores = [];
  }
}

// Self-initialize: Find all store locator elements and create instances
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-store-locator]').forEach(element => {
    new StoreLocator(element);
  });
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = StoreLocator;
}
