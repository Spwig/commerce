/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Staff Management - Tab switching, role toggles, POS settings, session revoke.
 * Uses AdminUtils.getCsrfToken() from globally loaded admin-utils.js.
 */
(function () {
    'use strict';

    /* ---- Tab switching handled by global AdminTabs utility ---- */

    /* ---- Toast notifications ---- */
    function showToast(message, type) {
        AdminModal.toast(message, type || 'info');
    }

    /* ---- Helper: POST with CSRF ---- */
    function postJSON(url, data) {
        var csrfToken = '';
        if (typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken) {
            csrfToken = AdminUtils.getCsrfToken();
        } else {
            var meta = document.querySelector('[name=csrfmiddlewaretoken]');
            csrfToken = meta ? meta.value : '';
        }

        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: JSON.stringify(data),
        }).then(function (res) {
            return res.json().then(function (json) {
                json._status = res.status;
                return json;
            });
        });
    }

    /* ---- Role Toggle ---- */
    function initRoleToggles() {
        document.querySelectorAll('.role-toggle-switch input[type="checkbox"]').forEach(function (toggle) {
            toggle.addEventListener('change', function () {
                var card = this.closest('.role-toggle-card');
                var url = this.dataset.url;
                var roleId = this.dataset.roleId;
                var roleName = this.dataset.roleName;
                var isAssigning = this.checked;

                postJSON(url, { role_id: roleId, action: isAssigning ? 'assign' : 'remove' })
                    .then(function (data) {
                        if (data.success) {
                            if (isAssigning) {
                                card.classList.add('assigned');
                            } else {
                                card.classList.remove('assigned');
                            }
                            showToast(
                                isAssigning
                                    ? 'Role "' + roleName + '" assigned.'
                                    : 'Role "' + roleName + '" removed.'
                            );
                            // Update effective permissions if returned
                            if (data.permissions_html) {
                                var permGrid = document.getElementById('effective-permissions');
                                if (permGrid) permGrid.innerHTML = data.permissions_html;
                            }
                        } else {
                            // Revert toggle
                            toggle.checked = !isAssigning;
                            showToast(data.error || 'Failed to update role.', 'error');
                        }
                    })
                    .catch(function () {
                        toggle.checked = !isAssigning;
                        showToast('Network error. Please try again.', 'error');
                    });
            });
        });
    }

    /* ---- POS Settings Save ---- */
    function initPosSettings() {
        var saveBtn = document.getElementById('pos-settings-save');
        if (!saveBtn) return;

        saveBtn.addEventListener('click', function () {
            var form = document.getElementById('pos-settings-form');
            if (!form) return;

            var url = form.dataset.url;
            var data = {};

            // Gather form data
            form.querySelectorAll('input, select').forEach(function (input) {
                if (input.type === 'checkbox') {
                    data[input.name] = input.checked;
                } else {
                    data[input.name] = input.value;
                }
            });

            saveBtn.disabled = true;
            saveBtn.textContent = 'Saving...';

            postJSON(url, data)
                .then(function (result) {
                    if (result.success) {
                        showToast('POS settings saved.');
                    } else {
                        showToast(result.error || 'Failed to save POS settings.', 'error');
                    }
                })
                .catch(function () {
                    showToast('Network error. Please try again.', 'error');
                })
                .finally(function () {
                    saveBtn.disabled = false;
                    saveBtn.innerHTML = '<i class="fas fa-save"></i> Save POS Settings';
                });
        });
    }

    /* ---- POS Card & Biometric Removal ---- */
    function initPosSecurityActions() {
        var form = document.getElementById('pos-settings-form');
        if (!form) return;
        var url = form.dataset.url;

        var removeCardBtn = document.getElementById('pos-remove-card');
        if (removeCardBtn) {
            removeCardBtn.addEventListener('click', async function () {
                if (!await AdminModal.confirm({ message: 'Remove this staff member\'s unlock card?', danger: true, confirmText: 'Remove' })) return;
                removeCardBtn.disabled = true;
                postJSON(url, { remove_card: true })
                    .then(function (data) {
                        if (data.success) {
                            var row = removeCardBtn.closest('.pos-setting-row');
                            var container = row.querySelector('div');
                            container.innerHTML =
                                '<span style="color: var(--body-quiet-color);">Not registered</span>' +
                                '<span style="font-size: 11px; color: var(--body-quiet-color);">Register at POS terminal</span>';
                            showToast('Unlock card removed.');
                        } else {
                            showToast(data.error || 'Failed to remove card.', 'error');
                            removeCardBtn.disabled = false;
                        }
                    })
                    .catch(function () {
                        showToast('Network error.', 'error');
                        removeCardBtn.disabled = false;
                    });
            });
        }

        var removeBioBtn = document.getElementById('pos-remove-biometric');
        if (removeBioBtn) {
            removeBioBtn.addEventListener('click', async function () {
                if (!await AdminModal.confirm({ message: 'Remove all biometric credentials for this staff member?', danger: true, confirmText: 'Remove' })) return;
                removeBioBtn.disabled = true;
                postJSON(url, { remove_biometric: true })
                    .then(function (data) {
                        if (data.success) {
                            var row = removeBioBtn.closest('.pos-setting-row');
                            var container = row.querySelector('div');
                            container.innerHTML =
                                '<span style="color: var(--body-quiet-color);">Not registered</span>' +
                                '<span style="font-size: 11px; color: var(--body-quiet-color);">Register at POS terminal</span>';
                            showToast('Biometric credentials removed.');
                        } else {
                            showToast(data.error || 'Failed to remove biometric.', 'error');
                            removeBioBtn.disabled = false;
                        }
                    })
                    .catch(function () {
                        showToast('Network error.', 'error');
                        removeBioBtn.disabled = false;
                    });
            });
        }
    }

    /* ---- Session Revoke ---- */
    function initSessionRevoke() {
        document.querySelectorAll('.revoke-session-btn').forEach(function (btn) {
            btn.addEventListener('click', async function (e) {
                e.preventDefault();
                if (!await AdminModal.confirm({ message: 'Revoke this mobile session? The device will be signed out.', danger: true, confirmText: 'Revoke' })) return;

                var url = this.dataset.url;
                var item = this.closest('.session-item');

                postJSON(url, {}).then(function (data) {
                    if (data.success) {
                        if (item) {
                            item.style.opacity = '0';
                            item.style.transition = 'opacity 0.3s ease';
                            setTimeout(function () { item.remove(); }, 300);
                        }
                        showToast('Session revoked successfully.');
                    } else {
                        showToast(data.error || 'Failed to revoke session.', 'error');
                    }
                }).catch(function () {
                    showToast('Network error. Please try again.', 'error');
                });
            });
        });
    }

    /* ---- Change List Filters ---- */
    function initFilters() {
        var applyBtn = document.getElementById('apply-filters-btn');
        if (!applyBtn) return; // Not on change_list page

        var languageCode = document.documentElement.lang || 'en';
        var filterUrl = '/' + languageCode + '/admin/accounts/staffmember/filter/';
        var debounceTimer;

        function applyFilters() {
            var params = new URLSearchParams();
            var search = document.getElementById('filter-search').value.trim();
            var role = document.getElementById('filter-role').value;
            var access = document.getElementById('filter-access').value;
            var status = document.getElementById('filter-status').value;
            var mfa = document.getElementById('filter-mfa').value;

            if (search) params.set('search', search);
            if (role) params.set('role', role);
            if (access) params.set('access', access);
            if (status) params.set('status', status);
            if (mfa) params.set('mfa', mfa);

            var url = filterUrl + '?' + params.toString();
            var container = document.getElementById('results-container');
            container.style.opacity = '0.5';

            fetch(url, {
                method: 'GET',
                headers: {'X-Requested-With': 'XMLHttpRequest'}
            })
            .then(function(r) { return r.json(); })
            .then(function(data) {
                container.innerHTML = data.html;
                container.style.opacity = '1';
                document.getElementById('results-count').textContent = data.count;
                updateActiveFilters();
            })
            .catch(function(err) {
                container.style.opacity = '1';
                console.error('Filter error:', err);
            });
        }

        function updateActiveFilters() {
            var container = document.getElementById('active-filters');
            var label = '<span class="active-filters-label">Active:</span>';
            var tags = '';
            var search = document.getElementById('filter-search').value.trim();
            if (search) tags += '<span class="active-filter-tag">Search: ' + search + '</span>';
            var role = document.getElementById('filter-role');
            if (role.value) tags += '<span class="active-filter-tag">Role: ' + role.options[role.selectedIndex].text + '</span>';
            var access = document.getElementById('filter-access');
            if (access.value) tags += '<span class="active-filter-tag">Access: ' + access.options[access.selectedIndex].text + '</span>';
            var statusEl = document.getElementById('filter-status');
            if (statusEl.value) tags += '<span class="active-filter-tag">Status: ' + statusEl.options[statusEl.selectedIndex].text + '</span>';
            var mfa = document.getElementById('filter-mfa');
            if (mfa.value) tags += '<span class="active-filter-tag">2FA: ' + mfa.options[mfa.selectedIndex].text + '</span>';
            container.innerHTML = label + (tags || '<span style="color: var(--body-quiet-color); font-size: 12px;">None</span>');
        }

        function clearFilters() {
            document.getElementById('filter-search').value = '';
            document.getElementById('filter-role').value = '';
            document.getElementById('filter-access').value = '';
            document.getElementById('filter-status').value = '';
            document.getElementById('filter-mfa').value = '';
            applyFilters();
        }

        // Event listeners
        applyBtn.addEventListener('click', applyFilters);
        document.getElementById('clear-filters-btn').addEventListener('click', clearFilters);

        // Debounced search
        document.getElementById('filter-search').addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(applyFilters, 300);
        });

        // Filter toggle
        document.getElementById('toggle-filters-btn').addEventListener('click', function() {
            var fields = document.getElementById('filter-fields');
            var panel = document.getElementById('filters-panel');
            if (fields.style.display === 'none') {
                fields.style.display = '';
                panel.querySelector('.filters-panel-footer').style.display = '';
                this.querySelector('i').className = 'fas fa-chevron-down';
            } else {
                fields.style.display = 'none';
                panel.querySelector('.filters-panel-footer').style.display = 'none';
                this.querySelector('i').className = 'fas fa-chevron-right';
            }
        });

        // Select filter auto-apply
        ['filter-role', 'filter-access', 'filter-status', 'filter-mfa'].forEach(function(id) {
            document.getElementById(id).addEventListener('change', applyFilters);
        });
    }

    /* ---- Init ---- */
    document.addEventListener('DOMContentLoaded', function () {
        // Tab switching handled by global AdminTabs utility
        initRoleToggles();
        initPosSettings();
        initPosSecurityActions();
        initSessionRevoke();
        initFilters();
    });
})();
