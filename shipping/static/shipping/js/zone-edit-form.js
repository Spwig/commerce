/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Shipping Zone Edit Form JavaScript
 * Enhances the admin change form with dual-listbox UI for JSON fields
 */

window.ZoneEditForm = (function() {
    'use strict';

    let allCountries = [];
    let zoneData = {
        countries: [],
        states: {},
        postal_code_patterns: []
    };
    let sortableInstances = {};

    /**
     * Initialize the edit form enhancements
     */
    function init(countriesData, initialZoneData) {
        allCountries = countriesData || [];
        zoneData = initialZoneData || { countries: [], states: {}, postal_code_patterns: [] };

        // Initialize all enhancements
        initCountriesDualListbox();
        initStatesDualListbox();
        initPostalPatternsHelper();
    }

    /**
     * Initialize countries dual-listbox
     */
    function initCountriesDualListbox() {
        const countriesField = document.getElementById('id_countries');
        if (!countriesField) return;

        // Hide the original textarea
        const countriesRow = countriesField.closest('.form-row');
        if (!countriesRow) return;

        // Create dual-listbox container
        const container = createDualListbox('countries', 'Countries');
        countriesRow.appendChild(container);

        // Hide original field
        countriesField.classList.add('field-hidden');
        const helpText = countriesRow.querySelector('.help');
        if (helpText) helpText.style.display = 'none';

        // Populate listboxes
        populateCountriesListbox();

        // Initialize Sortable
        initCountriesSortable();
    }

    /**
     * Create dual-listbox HTML structure
     */
    function createDualListbox(type, label) {
        const container = document.createElement('div');
        container.className = 'dual-listbox-container';
        container.innerHTML = `
            <div class="dual-listbox-column">
                <h4>
                    <i class="fas fa-globe"></i>
                    Available ${label}
                    <span class="count" id="available-${type}-count">(0)</span>
                </h4>
                <div class="listbox-search">
                    <input type="text" id="${type}-search" placeholder="Search ${label.toLowerCase()}...">
                    <i class="fas fa-search"></i>
                </div>
                <div class="dual-listbox" id="available-${type}"></div>
            </div>
            <div class="dual-listbox-column">
                <h4>
                    <i class="fas fa-check-circle"></i>
                    Selected ${label}
                    <span class="count" id="selected-${type}-count">(0)</span>
                </h4>
                <div class="dual-listbox" id="selected-${type}"></div>
            </div>
        `;
        return container;
    }

    /**
     * Populate countries listbox from data
     */
    function populateCountriesListbox() {
        const availableList = document.getElementById('available-countries');
        const selectedList = document.getElementById('selected-countries');
        if (!availableList || !selectedList) return;

        // Get selected country codes from zone data
        const selectedCodes = zoneData.countries || [];

        // Populate available countries
        allCountries.forEach(country => {
            if (!selectedCodes.includes(country.code)) {
                availableList.appendChild(createCountryItem(country, false));
            }
        });

        // Populate selected countries
        selectedCodes.forEach(code => {
            const country = allCountries.find(c => c.code === code);
            if (country) {
                selectedList.appendChild(createCountryItem(country, true));
            }
        });

        // Update counts
        updateCounts('countries');

        // Initialize search
        initSearch('countries');
    }

    /**
     * Create country listbox item
     */
    function createCountryItem(country, isSelected) {
        const item = document.createElement('div');
        item.className = 'listbox-item';
        item.dataset.code = country.code;
        item.dataset.name = country.name;
        item.innerHTML = `
            <span class="drag-handle">
                <i class="fas fa-grip-vertical"></i>
            </span>
            <span class="country-flag-img">
                <img src="/static/flags/${country.code.toLowerCase()}.gif" alt="${country.code}" class="country-flag" onerror="this.style.display='none'">
            </span>
            <span class="item-info">
                <span class="item-name">${country.name}</span>
                <span class="item-code">(${country.code})</span>
            </span>
        `;
        return item;
    }

    /**
     * Initialize Sortable for countries
     */
    function initCountriesSortable() {
        const availableEl = document.getElementById('available-countries');
        const selectedEl = document.getElementById('selected-countries');
        if (!availableEl || !selectedEl) return;

        const sortableOptions = {
            group: 'countries',
            animation: 150,
            ghostClass: 'sortable-ghost',
            onAdd: function(evt) {
                handleCountryMove(evt);
            },
            onRemove: function(evt) {
                handleCountryMove(evt);
            }
        };

        sortableInstances.availableCountries = new Sortable(availableEl, sortableOptions);
        sortableInstances.selectedCountries = new Sortable(selectedEl, sortableOptions);
    }

    /**
     * Handle country item movement
     */
    function handleCountryMove(evt) {
        updateCountriesField();
        updateCounts('countries');

        // Reload states when countries change
        loadStatesForSelectedCountries();
    }

    /**
     * Update the hidden countries JSON field
     */
    function updateCountriesField() {
        const selectedList = document.getElementById('selected-countries');
        if (!selectedList) return;

        const selectedCodes = Array.from(selectedList.querySelectorAll('.listbox-item'))
            .map(item => item.dataset.code);

        const countriesField = document.getElementById('id_countries');
        if (countriesField) {
            countriesField.value = JSON.stringify(selectedCodes);
        }
    }

    /**
     * Initialize states dual-listbox
     */
    function initStatesDualListbox() {
        const statesField = document.getElementById('id_states');
        if (!statesField) return;

        // Hide the original textarea
        const statesRow = statesField.closest('.form-row');
        if (!statesRow) return;

        // Create dual-listbox container
        const container = createDualListbox('states', 'States/Provinces');
        statesRow.appendChild(container);

        // Hide original field
        statesField.classList.add('field-hidden');
        const helpText = statesRow.querySelector('.help');
        if (helpText) helpText.style.display = 'none';

        // Add info box
        const infoBox = document.createElement('div');
        infoBox.className = 'info-box';
        infoBox.innerHTML = `
            <i class="fas fa-info-circle"></i>
            <p>States/provinces will load automatically based on selected countries above.</p>
        `;
        container.insertBefore(infoBox, container.firstChild);

        // Load states if countries are already selected
        loadStatesForSelectedCountries();
    }

    /**
     * Load states via AJAX for selected countries
     */
    function loadStatesForSelectedCountries() {
        const availableStatesEl = document.getElementById('available-states');
        const selectedStatesEl = document.getElementById('selected-states');
        if (!availableStatesEl || !selectedStatesEl) return;

        // Get selected country codes
        const selectedCountriesList = document.getElementById('selected-countries');
        if (!selectedCountriesList) return;

        const selectedCountries = Array.from(selectedCountriesList.querySelectorAll('.listbox-item'))
            .map(item => item.dataset.code);

        // If no countries selected, clear states
        if (selectedCountries.length === 0) {
            availableStatesEl.innerHTML = '<div class="info-box"><p>Select countries above to load states.</p></div>';
            selectedStatesEl.innerHTML = '';
            updateCounts('states');
            return;
        }

        // Show loading
        availableStatesEl.innerHTML = '<div class="info-box"><i class="fas fa-spinner fa-spin"></i> Loading states...</div>';

        // Get language for URL
        const lang = document.documentElement.lang || 'en';
        const url = `/${lang}/admin/shipping/zone-wizard/get-states/`;

        // Get CSRF token
        const csrfToken = AdminUtils.getCsrfToken();

        // Make AJAX request
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams({
                country_codes: selectedCountries.join(',')
            })
        })
        .then(response => response.json())
        .then(data => {
            populateStatesListbox(data.states);
            initStatesSortable();
        })
        .catch(error => {
            console.error('Error loading states:', error);
            availableStatesEl.innerHTML = '<div class="info-box" style="border-color: #dc3545;"><i class="fas fa-exclamation-triangle"></i> Failed to load states.</div>';
        });
    }

    /**
     * Populate states listbox from AJAX data
     */
    function populateStatesListbox(statesData) {
        const availableList = document.getElementById('available-states');
        const selectedList = document.getElementById('selected-states');
        if (!availableList || !selectedList) return;

        // Clear available list
        availableList.innerHTML = '';

        // Get currently selected state codes from zone data
        const selectedStateCodes = [];
        const statesDict = zoneData.states || {};
        for (const [country, states] of Object.entries(statesDict)) {
            states.forEach(state => {
                selectedStateCodes.push(`${country}:${state}`);
            });
        }

        // Clear selected list and rebuild from zone data
        selectedList.innerHTML = '';

        // Build available and selected lists
        for (const [countryCode, states] of Object.entries(statesData)) {
            states.forEach(state => {
                const stateCode = `${countryCode}:${state.code}`;
                const stateItem = createStateItem(countryCode, state);

                if (selectedStateCodes.includes(stateCode)) {
                    selectedList.appendChild(stateItem);
                } else {
                    availableList.appendChild(stateItem);
                }
            });
        }

        // Update counts
        updateCounts('states');

        // Initialize search
        initSearch('states');
    }

    /**
     * Create state listbox item
     */
    function createStateItem(countryCode, state) {
        const item = document.createElement('div');
        item.className = 'listbox-item';
        item.dataset.code = `${countryCode}:${state.code}`;
        item.dataset.country = countryCode;
        item.dataset.state = state.code;
        item.dataset.name = state.name;
        item.innerHTML = `
            <span class="drag-handle">
                <i class="fas fa-grip-vertical"></i>
            </span>
            <span class="item-info">
                <span class="item-name">${state.name}</span>
                <span class="item-code">(${countryCode}:${state.code})</span>
            </span>
        `;
        return item;
    }

    /**
     * Initialize Sortable for states
     */
    function initStatesSortable() {
        const availableEl = document.getElementById('available-states');
        const selectedEl = document.getElementById('selected-states');
        if (!availableEl || !selectedEl) return;

        // Destroy existing instances if they exist
        if (sortableInstances.availableStates) sortableInstances.availableStates.destroy();
        if (sortableInstances.selectedStates) sortableInstances.selectedStates.destroy();

        const sortableOptions = {
            group: 'states',
            animation: 150,
            ghostClass: 'sortable-ghost',
            onAdd: function(evt) {
                handleStateMove(evt);
            },
            onRemove: function(evt) {
                handleStateMove(evt);
            }
        };

        sortableInstances.availableStates = new Sortable(availableEl, sortableOptions);
        sortableInstances.selectedStates = new Sortable(selectedEl, sortableOptions);
    }

    /**
     * Handle state item movement
     */
    function handleStateMove(evt) {
        updateStatesField();
        updateCounts('states');
    }

    /**
     * Update the hidden states JSON field
     */
    function updateStatesField() {
        const selectedList = document.getElementById('selected-states');
        if (!selectedList) return;

        const statesDict = {};
        Array.from(selectedList.querySelectorAll('.listbox-item')).forEach(item => {
            const country = item.dataset.country;
            const state = item.dataset.state;
            if (!statesDict[country]) {
                statesDict[country] = [];
            }
            statesDict[country].push(state);
        });

        const statesField = document.getElementById('id_states');
        if (statesField) {
            statesField.value = JSON.stringify(statesDict);
        }
    }

    /**
     * Initialize postal patterns helper
     */
    function initPostalPatternsHelper() {
        const patternsField = document.getElementById('id_postal_code_patterns');
        if (!patternsField) return;

        const patternsRow = patternsField.closest('.form-row');
        if (!patternsRow) return;

        // Hide original field
        patternsField.classList.add('field-hidden');
        const helpText = patternsRow.querySelector('.help');
        if (helpText) helpText.style.display = 'none';

        // Create patterns helper UI
        const container = document.createElement('div');
        container.className = 'postal-patterns-enhanced';
        container.innerHTML = `
            <h4><i class="fas fa-mailbox"></i> Postal Code Patterns (Regex)</h4>
            <p style="margin: 0 0 15px 0; font-size: 13px; color: #666;">
                Define regex patterns to match postal codes. One pattern per line.
            </p>
            <div class="pattern-examples">
                <div class="pattern-example">
                    <div class="pattern-info">
                        <span class="pattern-label">Los Angeles (CA)</span>
                        <span class="pattern-value">^90[0-9]{3}$</span>
                    </div>
                    <button type="button" class="copy-btn" data-pattern="^90[0-9]{3}$">Copy</button>
                </div>
                <div class="pattern-example">
                    <div class="pattern-info">
                        <span class="pattern-label">New York (NY)</span>
                        <span class="pattern-value">^10[0-9]{3}$</span>
                    </div>
                    <button type="button" class="copy-btn" data-pattern="^10[0-9]{3}$">Copy</button>
                </div>
                <div class="pattern-example">
                    <div class="pattern-info">
                        <span class="pattern-label">Canada Postal</span>
                        <span class="pattern-value">^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$</span>
                    </div>
                    <button type="button" class="copy-btn" data-pattern="^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$">Copy</button>
                </div>
                <div class="pattern-example">
                    <div class="pattern-info">
                        <span class="pattern-label">UK Postcode</span>
                        <span class="pattern-value">^[A-Z]{1,2}[0-9]{1,2} [0-9][A-Z]{2}$</span>
                    </div>
                    <button type="button" class="copy-btn" data-pattern="^[A-Z]{1,2}[0-9]{1,2} [0-9][A-Z]{2}$">Copy</button>
                </div>
            </div>
            <textarea class="pattern-textarea" id="patterns-textarea" rows="8" placeholder="Enter regex patterns, one per line..."></textarea>
        `;
        patternsRow.appendChild(container);

        // Populate textarea from zone data
        const textarea = document.getElementById('patterns-textarea');
        if (textarea && zoneData.postal_code_patterns) {
            textarea.value = zoneData.postal_code_patterns.join('\n');
        }

        // Update hidden field on textarea change
        if (textarea) {
            textarea.addEventListener('input', updatePatternsField);
        }

        // Add copy button handlers
        container.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const pattern = this.dataset.pattern;
                const textarea = document.getElementById('patterns-textarea');
                if (textarea) {
                    const currentValue = textarea.value.trim();
                    textarea.value = currentValue ? currentValue + '\n' + pattern : pattern;
                    updatePatternsField();

                    // Visual feedback
                    this.textContent = 'Copied!';
                    this.classList.add('copied');
                    setTimeout(() => {
                        this.textContent = 'Copy';
                        this.classList.remove('copied');
                    }, 2000);
                }
            });
        });
    }

    /**
     * Update the hidden postal patterns JSON field
     */
    function updatePatternsField() {
        const textarea = document.getElementById('patterns-textarea');
        const patternsField = document.getElementById('id_postal_code_patterns');
        if (!textarea || !patternsField) return;

        const lines = textarea.value.split('\n')
            .map(line => line.trim())
            .filter(line => line.length > 0);

        patternsField.value = JSON.stringify(lines);
    }

    /**
     * Update count badges
     */
    function updateCounts(type) {
        const availableEl = document.getElementById(`available-${type}`);
        const selectedEl = document.getElementById(`selected-${type}`);
        const availableCountEl = document.getElementById(`available-${type}-count`);
        const selectedCountEl = document.getElementById(`selected-${type}-count`);

        if (availableEl && availableCountEl) {
            const count = availableEl.querySelectorAll('.listbox-item').length;
            availableCountEl.textContent = `(${count})`;
        }

        if (selectedEl && selectedCountEl) {
            const count = selectedEl.querySelectorAll('.listbox-item').length;
            selectedCountEl.textContent = `(${count})`;
        }
    }

    /**
     * Initialize search functionality
     */
    function initSearch(type) {
        const searchInput = document.getElementById(`${type}-search`);
        if (!searchInput) return;

        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const availableList = document.getElementById(`available-${type}`);
            if (!availableList) return;

            const items = availableList.querySelectorAll('.listbox-item');
            items.forEach(item => {
                const name = item.dataset.name.toLowerCase();
                const code = item.dataset.code.toLowerCase();
                const matches = name.includes(query) || code.includes(query);
                item.style.display = matches ? '' : 'none';
            });
        });
    }

    // Public API
    return {
        init: init
    };
})();

// Save button handler
function initSaveButtons() {
    var form = document.getElementById('shippingzone-form');
    var saveContinueBtn = document.getElementById('save-continue-btn');
    if (saveContinueBtn && form) {
        saveContinueBtn.addEventListener('click', function() {
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = '_continue';
            input.value = '1';
            form.appendChild(input);
            form.submit();
        });
    }
}

// Auto-initialize from data island when present
document.addEventListener('DOMContentLoaded', function() {
    initSaveButtons();

    var configEl = document.getElementById('zone-edit-config');
    if (!configEl) return;
    var config;
    try {
        config = JSON.parse(configEl.textContent);
    } catch (e) {
        return;
    }
    if (config && config.allCountries) {
        window.ZoneEditForm.init(config.allCountries, {
            countries: config.zone ? config.zone.countries : [],
            states: config.zone ? config.zone.states : {},
            postal_code_patterns: config.zone ? config.zone.postalCodePatterns : []
        });
    }
});
