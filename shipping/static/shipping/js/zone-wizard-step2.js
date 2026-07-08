/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Zone Wizard Step 2: Geographic Coverage
 * Interactive dual-listbox functionality with drag-and-drop, search, and dynamic state loading
 */

(function() {
    'use strict';

    // Wait for DOM and SortableJS to be ready
    document.addEventListener('DOMContentLoaded', function() {

        // =====================================================================
        // 0. READ CONFIG FROM DATA ISLAND
        // =====================================================================

        var zoneConfigEl = document.getElementById('zone-wizard-config');
        var getStatesUrl = '';
        if (zoneConfigEl) {
            try {
                var zoneConfig = JSON.parse(zoneConfigEl.textContent);
                getStatesUrl = zoneConfig.getStatesUrl || '';
            } catch (e) {
                console.error('Failed to parse zone-wizard-config:', e);
            }
        }

        // =====================================================================
        // 1. INITIALIZE SORTABLE (DRAG-AND-DROP)
        // =====================================================================

        const availableCountriesEl = document.getElementById('available-countries');
        const selectedCountriesEl = document.getElementById('selected-countries');
        const availableStatesEl = document.getElementById('available-states');
        const selectedStatesEl = document.getElementById('selected-states');

        if (!availableCountriesEl || !selectedCountriesEl) {
            console.error('Zone wizard listbox elements not found');
            return;
        }

        // Sortable options for drag-and-drop
        const sortableOptions = {
            group: 'shared',
            animation: 150,
            ghostClass: 'dragging',
            dragClass: 'dragging',
            onAdd: function(evt) {
                handleItemMove(evt);
            },
            onRemove: function(evt) {
                handleItemMove(evt);
            },
        };

        // Initialize SortableJS for countries
        const countriesSortable = {
            available: new Sortable(availableCountriesEl, {
                ...sortableOptions,
                group: 'countries',
            }),
            selected: new Sortable(selectedCountriesEl, {
                ...sortableOptions,
                group: 'countries',
            }),
        };

        // Initialize SortableJS for states
        if (availableStatesEl && selectedStatesEl) {
            const statesSortable = {
                available: new Sortable(availableStatesEl, {
                    ...sortableOptions,
                    group: 'states',
                }),
                selected: new Sortable(selectedStatesEl, {
                    ...sortableOptions,
                    group: 'states',
                }),
            };
        }

        // =====================================================================
        // 2. HANDLE ITEM MOVEMENTS
        // =====================================================================

        function handleItemMove(evt) {
            const item = evt.item;
            const toList = evt.to.id;

            // Update hidden input when item moves to selected list
            if (toList === 'selected-countries') {
                addHiddenInput(item, 'selected_countries[]', item.dataset.code);
                updateCountryCounts();
                // Reload states when countries change
                loadStatesForSelectedCountries();
            } else if (toList === 'available-countries') {
                removeHiddenInput(item, 'selected_countries[]');
                updateCountryCounts();
                // Reload states when countries change
                loadStatesForSelectedCountries();
            } else if (toList === 'selected-states') {
                addHiddenInput(item, 'selected_states[]', item.dataset.code);
                updateStateCounts();
            } else if (toList === 'available-states') {
                removeHiddenInput(item, 'selected_states[]');
                updateStateCounts();
            }

            // Update empty states
            updateEmptyStates();
        }

        function addHiddenInput(item, name, value) {
            // Check if hidden input already exists
            let input = item.querySelector(`input[name="${name}"]`);
            if (!input) {
                input = document.createElement('input');
                input.type = 'hidden';
                input.name = name;
                input.value = value;
                item.appendChild(input);
            }
        }

        function removeHiddenInput(item, name) {
            const input = item.querySelector(`input[name="${name}"]`);
            if (input) {
                input.remove();
            }
        }

        // =====================================================================
        // 3. UPDATE COUNT BADGES
        // =====================================================================

        function updateCountryCounts() {
            const availableCount = availableCountriesEl.querySelectorAll('.listbox-item:not(.hidden)').length;
            const selectedCount = selectedCountriesEl.querySelectorAll('.listbox-item').length;

            const availableCountEl = document.getElementById('available-countries-count');
            const selectedCountEl = document.getElementById('selected-countries-count');

            if (availableCountEl) {
                availableCountEl.textContent = `(${availableCount})`;
            }
            if (selectedCountEl) {
                selectedCountEl.textContent = `(${selectedCount})`;
            }
        }

        function updateStateCounts() {
            if (!availableStatesEl || !selectedStatesEl) return;

            const availableCount = availableStatesEl.querySelectorAll('.listbox-item:not(.hidden)').length;
            const selectedCount = selectedStatesEl.querySelectorAll('.listbox-item').length;

            const availableCountEl = document.getElementById('available-states-count');
            const selectedCountEl = document.getElementById('selected-states-count');

            if (availableCountEl) {
                availableCountEl.textContent = `(${availableCount})`;
            }
            if (selectedCountEl) {
                selectedCountEl.textContent = `(${selectedCount})`;
            }
        }

        // =====================================================================
        // 4. SEARCH FILTERING
        // =====================================================================

        const countrySearchInput = document.getElementById('country-search');
        const stateSearchInput = document.getElementById('state-search');

        if (countrySearchInput) {
            countrySearchInput.addEventListener('input', function() {
                filterListbox(this.value, availableCountriesEl);
                updateCountryCounts();
                updateEmptyStates();
            });
        }

        if (stateSearchInput) {
            stateSearchInput.addEventListener('input', function() {
                filterListbox(this.value, availableStatesEl);
                updateStateCounts();
                updateEmptyStates();
            });
        }

        function filterListbox(searchTerm, listboxEl) {
            const items = listboxEl.querySelectorAll('.listbox-item');
            const term = searchTerm.toLowerCase().trim();

            items.forEach(item => {
                const name = (item.dataset.name || '').toLowerCase();
                const code = (item.dataset.code || '').toLowerCase();

                if (name.includes(term) || code.includes(term)) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        }

        // =====================================================================
        // 5. EMPTY STATE HANDLING
        // =====================================================================

        function updateEmptyStates() {
            updateEmptyState(availableCountriesEl, 'No countries available');
            updateEmptyState(selectedCountriesEl, 'Drag countries here or click to add');

            if (availableStatesEl) {
                updateEmptyState(availableStatesEl, 'No states available');
            }
            if (selectedStatesEl) {
                updateEmptyState(selectedStatesEl, 'Drag states here or click to add');
            }
        }

        function updateEmptyState(listboxEl, message) {
            const visibleItems = listboxEl.querySelectorAll('.listbox-item:not(.hidden)');
            let emptyStateEl = listboxEl.querySelector('.empty-state');

            if (visibleItems.length === 0) {
                if (!emptyStateEl) {
                    emptyStateEl = document.createElement('div');
                    emptyStateEl.className = 'empty-state';
                    emptyStateEl.innerHTML = `
                        <i class="fas fa-inbox"></i>
                        <p>${message}</p>
                    `;
                    listboxEl.appendChild(emptyStateEl);
                }
            } else {
                if (emptyStateEl) {
                    emptyStateEl.remove();
                }
            }
        }

        // =====================================================================
        // 6. AJAX: LOAD STATES FOR SELECTED COUNTRIES
        // =====================================================================

        function loadStatesForSelectedCountries() {
            if (!availableStatesEl || !selectedStatesEl) return;

            // Get all selected country codes
            const selectedCountries = Array.from(
                selectedCountriesEl.querySelectorAll('.listbox-item')
            ).map(item => item.dataset.code);

            // If no countries selected, clear states
            if (selectedCountries.length === 0) {
                clearStatesList();
                return;
            }

            // Show loading indicator
            showStatesLoading(true);

            // Get CSRF token
            const csrfToken = AdminUtils.getCsrfToken();

            // Make AJAX request
            fetch(getStatesUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                },
                body: new URLSearchParams({
                    country_codes: selectedCountries.join(',')
                })
            })
            .then(response => response.json())
            .then(data => {
                updateStatesList(data.states);
                showStatesLoading(false);
            })
            .catch(error => {
                console.error('Error loading states:', error);
                showStatesLoading(false);
                showNotification('Failed to load states. Please try again.', 'error');
            });
        }

        function updateStatesList(statesData) {
            // Clear current available states
            availableStatesEl.innerHTML = '';

            // Get currently selected states to preserve them
            const selectedStateCodes = Array.from(
                selectedStatesEl.querySelectorAll('.listbox-item')
            ).map(item => item.dataset.code);

            // Build new states list
            const stateItems = [];

            for (const [countryCode, states] of Object.entries(statesData)) {
                states.forEach(state => {
                    const stateCode = `${countryCode}:${state.code}`;

                    // Only add to available list if not already selected
                    if (!selectedStateCodes.includes(stateCode)) {
                        stateItems.push({
                            code: stateCode,
                            name: state.name,
                            country: countryCode
                        });
                    }
                });
            }

            // Sort by name
            stateItems.sort((a, b) => a.name.localeCompare(b.name));

            // Add items to available list
            stateItems.forEach(state => {
                const itemEl = createStateListItem(state.code, state.name, state.country);
                availableStatesEl.appendChild(itemEl);
            });

            // Update counts and empty states
            updateStateCounts();
            updateEmptyStates();
        }

        function createStateListItem(code, name, countryCode) {
            const div = document.createElement('div');
            div.className = 'listbox-item';
            div.dataset.code = code;
            div.dataset.name = name;
            if (countryCode) {
                div.dataset.country = countryCode;
            }

            div.innerHTML = `
                <span class="drag-handle"><i class="fas fa-grip-vertical"></i></span>
                <span class="item-info">
                    <span class="item-name">${escapeHtml(name)}</span>
                </span>
            `;

            return div;
        }

        function clearStatesList() {
            if (availableStatesEl) {
                availableStatesEl.innerHTML = '';
            }
            updateStateCounts();
            updateEmptyStates();
        }

        function showStatesLoading(isLoading) {
            if (!availableStatesEl) return;

            let loadingEl = availableStatesEl.querySelector('.loading-indicator');

            if (isLoading) {
                if (!loadingEl) {
                    loadingEl = document.createElement('div');
                    loadingEl.className = 'loading-indicator';
                    loadingEl.innerHTML = `
                        <i class="fas fa-spinner fa-spin"></i>
                        <span>Loading states...</span>
                    `;
                    availableStatesEl.appendChild(loadingEl);
                }
            } else {
                if (loadingEl) {
                    loadingEl.remove();
                }
            }
        }

        // =====================================================================
        // 7. CLICK-TO-ADD FUNCTIONALITY
        // =====================================================================

        // Allow clicking on items to move them (in addition to drag-and-drop)
        document.addEventListener('click', function(e) {
            const item = e.target.closest('.listbox-item');
            if (!item) return;

            // Don't trigger on drag handle
            if (e.target.closest('.drag-handle')) return;

            const listbox = item.closest('.listbox');
            if (!listbox) return;

            // Move item to opposite list
            if (listbox.id === 'available-countries') {
                selectedCountriesEl.appendChild(item);
                addHiddenInput(item, 'selected_countries[]', item.dataset.code);
                updateCountryCounts();
                updateEmptyStates();
                loadStatesForSelectedCountries();
            } else if (listbox.id === 'selected-countries') {
                availableCountriesEl.appendChild(item);
                removeHiddenInput(item, 'selected_countries[]');
                updateCountryCounts();
                updateEmptyStates();
                loadStatesForSelectedCountries();
                // Re-apply search filter if active
                if (countrySearchInput && countrySearchInput.value) {
                    filterListbox(countrySearchInput.value, availableCountriesEl);
                }
            } else if (listbox.id === 'available-states') {
                selectedStatesEl.appendChild(item);
                addHiddenInput(item, 'selected_states[]', item.dataset.code);
                updateStateCounts();
                updateEmptyStates();
            } else if (listbox.id === 'selected-states') {
                availableStatesEl.appendChild(item);
                removeHiddenInput(item, 'selected_states[]');
                updateStateCounts();
                updateEmptyStates();
                // Re-apply search filter if active
                if (stateSearchInput && stateSearchInput.value) {
                    filterListbox(stateSearchInput.value, availableStatesEl);
                }
            }
        });

        // =====================================================================
        // 8. POSTAL PATTERN COPY BUTTONS
        // =====================================================================

        document.addEventListener('click', function(e) {
            const copyBtn = e.target.closest('.copy-pattern-btn');
            if (!copyBtn) return;

            const pattern = copyBtn.dataset.pattern;
            const textarea = document.getElementById('id_postal_patterns');

            if (textarea && pattern) {
                // Add pattern to textarea (new line if not empty)
                const currentValue = textarea.value.trim();
                textarea.value = currentValue ? `${currentValue}\n${pattern}` : pattern;

                // Visual feedback
                const icon = copyBtn.querySelector('i');
                const originalClass = icon.className;
                icon.className = 'fas fa-check';
                copyBtn.style.background = 'var(--success-fg)';
                copyBtn.style.color = 'white';

                setTimeout(() => {
                    icon.className = originalClass;
                    copyBtn.style.background = '';
                    copyBtn.style.color = '';
                }, 1500);
            }
        });

        // =====================================================================
        // 9. HELPER FUNCTIONS
        // =====================================================================

        function escapeHtml(text) {
            const map = {
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#039;'
            };
            return text.replace(/[&<>"']/g, m => map[m]);
        }

        function showNotification(message, type = 'info') {
            AdminModal.toast(message, type);
        }

        // =====================================================================
        // 10. INITIALIZE ON PAGE LOAD
        // =====================================================================

        // Set initial counts
        updateCountryCounts();
        updateStateCounts();
        updateEmptyStates();

        // Load states if countries are already selected
        const hasSelectedCountries = selectedCountriesEl.querySelectorAll('.listbox-item').length > 0;
        if (hasSelectedCountries) {
            loadStatesForSelectedCountries();
        }

        console.log('Zone Wizard Step 2 initialized successfully');
    });

})();
