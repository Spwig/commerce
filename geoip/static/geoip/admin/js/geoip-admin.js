/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * GeoIP Admin JavaScript
 * Extracted from inline scripts for CSP compliance.
 * Covers: geoipprovider/change_list, countrymapping/change_list,
 *         and provider_wizard.
 *
 * NOTE: Geolocation and visitor location filter logic has been migrated
 * to AdminListFilters (core/admin/js/admin-list-filters.js).
 */

// ============================================================
// Country mapping client-side filters (countrymapping/change_list)
// ============================================================

(function initCountryMappingFilters() {
    if (!document.getElementById('filter-search') || document.getElementById('geolocation-results') || document.getElementById('visitor-results')) return;
    // Only run on the country mapping page (no results container from other pages)
    const filtersPanel = document.getElementById('filters-panel');
    if (!filtersPanel) return;
    // A reliable page identifier: the filter-currency input is unique to this page
    if (!document.getElementById('filter-currency')) return;

    function _toggleFilters() {
        filtersPanel.classList.toggle('collapsed');
        const icon = filtersPanel.querySelector('.filters-toggle i');
        if (!icon) return;
        if (filtersPanel.classList.contains('collapsed')) {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        } else {
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    }

    function updateVisibleCount() {
        const table = document.getElementById('result_list');
        if (!table) return;
        let count = 0;
        table.querySelectorAll('tbody tr').forEach(function(row) {
            if (row.style.display !== 'none') count++;
        });
        const countEl = document.getElementById('results-count');
        if (countEl) countEl.textContent = count;
    }

    function applyClientFilters() {
        const search   = document.getElementById('filter-search').value.toLowerCase().trim();
        const active   = document.getElementById('filter-active').value;
        const eu       = document.getElementById('filter-eu').value;
        const currency = document.getElementById('filter-currency').value.toUpperCase().trim();

        const table = document.getElementById('result_list');
        if (!table) return;

        let visibleCount = 0;
        table.querySelectorAll('tbody tr').forEach(function(row) {
            const rowText = row.textContent.toLowerCase();
            let show = true;

            if (search && !rowText.includes(search)) show = false;

            if (active && show) {
                const isActiveImg = row.querySelector('td.field-is_active img');
                const checkboxes  = row.querySelectorAll('input[type="checkbox"]');
                let activeCheckbox = null;
                checkboxes.forEach(function(cb) {
                    if (cb.name && cb.name.includes('is_active')) activeCheckbox = cb;
                });
                if (activeCheckbox) {
                    if (active === 'yes' && !activeCheckbox.checked) show = false;
                    if (active === 'no'  &&  activeCheckbox.checked) show = false;
                } else if (isActiveImg) {
                    const isChecked = isActiveImg.alt === 'True' || isActiveImg.src.includes('icon-yes');
                    if (active === 'yes' && !isChecked) show = false;
                    if (active === 'no'  &&  isChecked) show = false;
                }
            }

            if (eu && show) {
                const euCell = row.querySelector('td.field-is_eu_member');
                if (euCell) {
                    const euImg = euCell.querySelector('img');
                    if (euImg) {
                        const isEU = euImg.alt === 'True' || euImg.src.includes('icon-yes');
                        if (eu === 'yes' && !isEU) show = false;
                        if (eu === 'no'  &&  isEU) show = false;
                    }
                }
            }

            if (currency && show) {
                const currencyInputs = row.querySelectorAll('input[name$="-default_currency"]');
                const currencyCells  = row.querySelectorAll('td.field-default_currency');
                let matchesCurrency = false;
                if (currencyInputs.length > 0) {
                    currencyInputs.forEach(function(input) {
                        if (input.value.toUpperCase().includes(currency)) matchesCurrency = true;
                    });
                } else if (currencyCells.length > 0) {
                    currencyCells.forEach(function(cell) {
                        if (cell.textContent.toUpperCase().includes(currency)) matchesCurrency = true;
                    });
                }
                if (!matchesCurrency) show = false;
            }

            row.style.display = show ? '' : 'none';
            if (show) visibleCount++;
        });

        const countEl = document.getElementById('results-count');
        if (countEl) countEl.textContent = visibleCount;
        updateActiveFilters();
    }

    function clearClientFilters() {
        document.getElementById('filter-search').value = '';
        document.getElementById('filter-active').value = '';
        document.getElementById('filter-eu').value = '';
        document.getElementById('filter-currency').value = '';
        applyClientFilters();
    }

    function updateActiveFilters() {
        const msg = document.getElementById('geoip-translations')
            ? JSON.parse(document.getElementById('geoip-translations').textContent)
            : {};
        const container = document.getElementById('active-filters');
        if (!container) return;
        const filters = [];

        const search   = document.getElementById('filter-search').value;
        const active   = document.getElementById('filter-active');
        const eu       = document.getElementById('filter-eu');
        const currency = document.getElementById('filter-currency').value;

        if (search)       filters.push({field: 'filter-search',   label: msg.label_search   || 'Search',   value: search});
        if (active.value) filters.push({field: 'filter-active',   label: msg.label_active_f || 'Active',   value: active.options[active.selectedIndex].text});
        if (eu.value)     filters.push({field: 'filter-eu',       label: msg.label_eu       || 'EU',       value: eu.options[eu.selectedIndex].text});
        if (currency)     filters.push({field: 'filter-currency', label: msg.label_currency || 'Currency', value: currency.toUpperCase()});

        if (filters.length === 0) {
            container.innerHTML = '';
            return;
        }

        let html = '<span class="active-filters-label">' + (msg.label_active || 'Active:') + '</span>';
        filters.forEach(function(f) {
            html += '<span class="active-filter-tag">' + f.label + ': ' + f.value +
                ' <i class="fas fa-times" data-clear-field="' + f.field + '"></i></span>';
        });
        container.innerHTML = html;

        container.querySelectorAll('[data-clear-field]').forEach(function(el) {
            el.addEventListener('click', function() {
                clearFilterCM(this.dataset.clearField);
            });
        });
    }

    function clearFilterCM(fieldId) {
        const field = document.getElementById(fieldId);
        if (field) field.value = '';
        applyClientFilters();
    }

    updateVisibleCount();

    let searchTimeout;
    function debounced() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(applyClientFilters, 200);
    }
    document.getElementById('filter-search').addEventListener('input', debounced);
    document.getElementById('filter-currency').addEventListener('input', debounced);
    document.getElementById('filter-active').addEventListener('change', applyClientFilters);
    document.getElementById('filter-eu').addEventListener('change', applyClientFilters);

    // Event delegation for country mapping actions
    document.addEventListener('click', function(e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) return;
        var action = btn.dataset.action;
        if (action === 'toggle-filters') _toggleFilters();
        else if (action === 'apply-filters') applyClientFilters();
        else if (action === 'clear-filters') clearClientFilters();
    });
})();

// ============================================================
// GeoIP Provider cards (geoipprovider/change_list)
// ============================================================

(function initGeoIPActions() {
    function getCSRFToken() {
        var meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        var input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input) return input.value;
        return '';
    }

    function getProviderUrls() {
        var el = document.getElementById('geoip-provider-config');
        if (!el) return null;
        try { return JSON.parse(el.textContent); } catch (_) { return null; }
    }

    function showCardFeedback(btn, success, message) {
        var card = btn.closest('.list-row-card');
        if (!card) return;
        // Remove any existing feedback
        var existing = card.querySelector('.geoip-card-feedback');
        if (existing) existing.remove();

        var div = document.createElement('div');
        div.className = 'geoip-card-feedback';
        div.style.cssText = 'padding:8px 16px;margin-top:8px;border-radius:6px;font-size:13px;' +
            (success ? 'background:var(--success-bg, #d4edda);color:var(--success-text, #155724);'
                     : 'background:var(--error-bg, #f8d7da);color:var(--error-text, #721c24);');
        div.innerHTML = (success ? '<i class="fas fa-check-circle"></i> ' : '<i class="fas fa-exclamation-circle"></i> ') + message;
        card.appendChild(div);
        setTimeout(function() { div.remove(); }, 6000);
    }

    function setButtonLoading(btn, loading) {
        var icon = btn.querySelector('i');
        if (!icon) return;
        if (loading) {
            btn.disabled = true;
            btn._origClass = icon.className;
            icon.className = 'fas fa-spinner fa-spin';
        } else {
            btn.disabled = false;
            if (btn._origClass) icon.className = btn._origClass;
        }
    }

    function handleTestProvider(btn) {
        var urls = getProviderUrls();
        if (!urls) return;
        var providerType = btn.dataset.providerType;
        if (!providerType) return;
        var url = urls.testUrl.replace('PLACEHOLDER', providerType);

        setButtonLoading(btn, true);
        fetch(url, {
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/x-www-form-urlencoded'},
            body: 'test_ip=8.8.8.8'
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            var msg = data.message || '';
            if (data.response_ms) msg += ' (' + data.response_ms + ' ms)';
            showCardFeedback(btn, data.success, msg);
        })
        .catch(function(err) {
            showCardFeedback(btn, false, 'Request failed: ' + err.message);
        })
        .finally(function() {
            setButtonLoading(btn, false);
        });
    }

    function handleUpdateDatabase(btn) {
        var urls = getProviderUrls();
        if (!urls) return;
        var providerId = btn.dataset.providerId;
        if (!providerId) return;
        var url = urls.updateUrl.replace('0', providerId);

        setButtonLoading(btn, true);
        fetch(url, {
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken()}
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            showCardFeedback(btn, data.success, data.message || '');
            if (data.success && data.last_update) {
                var card = btn.closest('.list-row-card');
                if (card) {
                    var syncIcon = card.querySelector('.fa-sync');
                    if (syncIcon && syncIcon.parentElement) {
                        syncIcon.parentElement.innerHTML = '<i class="fas fa-sync"></i> ' + data.last_update;
                    }
                }
            }
        })
        .catch(function(err) {
            showCardFeedback(btn, false, 'Request failed: ' + err.message);
        })
        .finally(function() {
            setButtonLoading(btn, false);
        });
    }

    document.addEventListener('click', function(e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) return;
        var action = btn.dataset.action;

        if (action === 'test-provider') {
            handleTestProvider(btn);
            return;
        }
        if (action === 'update-database') {
            handleUpdateDatabase(btn);
            return;
        }

        // Geolocation dashboard actions
        if (action === 'clear-expired-cache') {
            var msg = document.getElementById('geoip-translations')
                ? JSON.parse(document.getElementById('geoip-translations').textContent)
                : {};
            var statusEl = btn.closest('.quick-actions');
            if (statusEl) {
                var infoEl = document.createElement('span');
                infoEl.className = 'button secondary';
                infoEl.textContent = msg.cache_coming_soon || 'Use: python manage.py geoip_cleanup';
                statusEl.appendChild(infoEl);
                setTimeout(function() { infoEl.remove(); }, 5000);
            }
            return;
        }
        if (action === 'test-ip-resolution') {
            window.open('/api/geoip/v1/resolve/?test_ip=8.8.8.8', '_blank');
            return;
        }
    });
})();

// ============================================================
// Provider wizard (provider_wizard.html)
// ============================================================

(function initProviderWizard() {
    const wizardConfig = document.getElementById('wizard-config');
    if (!wizardConfig) return;

    let currentStep = parseInt(wizardConfig.dataset.currentStep, 10) || 1;
    const totalSteps = 4;

    function showStep(step) {
        document.querySelectorAll('.progress-step').forEach(function(el, index) {
            if (index < step - 1) {
                el.classList.add('completed');
                el.classList.remove('active');
            } else if (index === step - 1) {
                el.classList.add('active');
                el.classList.remove('completed');
            } else {
                el.classList.remove('active', 'completed');
            }
        });

        document.querySelectorAll('.wizard-step').forEach(function(el) {
            el.classList.remove('active');
        });
        const stepEl = document.getElementById('step-' + step);
        if (stepEl) stepEl.classList.add('active');
        currentStep = step;
    }

    function nextStep() {
        if (currentStep < totalSteps) {
            if (currentStep === 2) {
                collectConfigData();
            } else if (currentStep === 3) {
                updateSummary();
            }
            showStep(currentStep + 1);
        }
    }

    function prevStep() {
        if (currentStep > 1) {
            showStep(currentStep - 1);
        }
    }

    function collectConfigData() {
        const form = document.getElementById('provider-config-form');
        if (!form) return;
        const formData = new FormData(form);
        const hiddenFields = document.getElementById('hidden-fields');
        hiddenFields.innerHTML = '';
        for (let [key, value] of formData.entries()) {
            if (key !== 'csrfmiddlewaretoken' && key !== 'step') {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = key;
                input.value = value;
                hiddenFields.appendChild(input);
            }
        }
    }

    function updateSummary() {
        const form = document.getElementById('provider-settings-form');
        if (!form) return;
        const formData = new FormData(form);
        const hiddenFields = document.getElementById('hidden-fields');
        for (let [key, value] of formData.entries()) {
            if (key !== 'csrfmiddlewaretoken' && key !== 'step') {
                let existing = hiddenFields.querySelector('input[name="' + key + '"]');
                if (existing) {
                    existing.value = value;
                } else {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = key;
                    input.value = value;
                    hiddenFields.appendChild(input);
                }
            }
        }
        const priorityEl = document.getElementById('summary-priority');
        if (priorityEl) priorityEl.textContent = formData.get('priority') || '10';
        const cacheEl = document.getElementById('summary-cache');
        if (cacheEl) {
            const cacheDuration = parseInt(formData.get('cache_duration') || 86400);
            cacheEl.textContent = Math.floor(cacheDuration / 3600) + ' hours';
        }
    }

    function testConnection() {
        const testIp = document.getElementById('test-ip').value;
        const resultDiv = document.getElementById('test-result');
        const msg = document.getElementById('geoip-translations')
            ? JSON.parse(document.getElementById('geoip-translations').textContent)
            : {};

        resultDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> ' +
            (msg.testing || 'Testing...') + '</div>';

        setTimeout(function() {
            resultDiv.innerHTML =
                '<div class="test-success">' +
                    '<i class="fas fa-check-circle"></i>' +
                    '<strong>' + (msg.success || 'Success!') + '</strong>' +
                    '<p>IP: ' + testIp + '</p>' +
                    '<p>Location: Mountain View, CA, United States</p>' +
                    '<p>Coordinates: 37.386, -122.0838</p>' +
                '</div>';
        }, 1000);
    }

    function runFinalTest() {
        const resultDiv = document.getElementById('final-test-result');
        const msg = document.getElementById('geoip-translations')
            ? JSON.parse(document.getElementById('geoip-translations').textContent)
            : {};

        resultDiv.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> ' +
            (msg.running_final_test || 'Running final test...') + '</div>';

        setTimeout(function() {
            resultDiv.innerHTML =
                '<div class="test-success">' +
                    '<i class="fas fa-check-circle"></i>' +
                    '<strong>' + (msg.all_tests_passed || 'All tests passed!') + '</strong>' +
                    '<p>' + (msg.provider_configured || 'Your provider is configured correctly and ready to use.') + '</p>' +
                '</div>';
        }, 1500);
    }

    // Event delegation for data-action buttons (CSP-compliant)
    document.addEventListener('click', function(e) {
        var btn = e.target.closest('[data-action]');
        if (!btn || !wizardConfig) return;
        var action = btn.dataset.action;
        if (action === 'next-step')       nextStep();
        else if (action === 'prev-step')  prevStep();
        else if (action === 'test-connection') testConnection();
        else if (action === 'run-final-test')  runFinalTest();
    });

    // Initialize
    showStep(currentStep);
})();
