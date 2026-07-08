/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Staff Role Editor - Permission category toggles, access toggles,
 * icon/color selectors, and member management.
 *
 * Tab switching is handled by AdminTabs (auto-initialized via .admin-tabs).
 */
(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initCategoryToggles();
        initAccessToggles();
        initIconSelector();
        initColorSelector();
        initMemberManagement();
        initCloneButton();
    });

    function initCategoryToggles() {
        document.querySelectorAll('.level-option').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var row = this.closest('.category-row');
                var catKey = row.dataset.category;
                var level = this.dataset.level;

                // Update visual state
                row.querySelectorAll('.level-option').forEach(function(b) {
                    b.classList.remove('active');
                });
                this.classList.add('active');

                // Update hidden input
                var input = document.getElementById('cat_' + catKey);
                if (input) input.value = level;
            });
        });
    }

    function initAccessToggles() {
        var adminToggle = document.getElementById('id_can_access_admin');
        var posToggle = document.getElementById('id_can_access_pos');

        function updateAccessVisuals() {
            // Update toggle card styling
            document.querySelectorAll('.access-toggle').forEach(function(toggle) {
                var cb = toggle.querySelector('input[type="checkbox"]');
                if (cb && cb.checked) {
                    toggle.classList.add('active');
                } else {
                    toggle.classList.remove('active');
                }
            });

            // Dim/undim relevant tab buttons via CSS class (CSP-safe)
            var adminTabBtn = document.querySelector('.admin-tab-btn[data-tab="permissions"]');
            var posTabBtn = document.querySelector('.admin-tab-btn[data-tab="pos"]');

            if (adminTabBtn) {
                adminTabBtn.classList.toggle('role-tab-dimmed', !(adminToggle && adminToggle.checked));
            }
            if (posTabBtn) {
                posTabBtn.classList.toggle('role-tab-dimmed', !(posToggle && posToggle.checked));
            }
        }

        if (adminToggle) {
            adminToggle.addEventListener('change', updateAccessVisuals);
        }
        if (posToggle) {
            posToggle.addEventListener('change', updateAccessVisuals);
        }

        // Initial state
        updateAccessVisuals();
    }

    function initIconSelector() {
        var iconInput = document.getElementById('id_icon');
        var container = document.getElementById('icon-selector');
        if (!iconInput || !container) return;
        if (container.children.length > 0) return; // Already initialized

        var currentIcon = container.dataset.current || 'fas fa-user';
        var icons = [
            'fas fa-user', 'fas fa-user-tie', 'fas fa-user-check', 'fas fa-user-shield',
            'fas fa-crown', 'fas fa-pen-fancy', 'fas fa-box', 'fas fa-bullhorn',
            'fas fa-cash-register', 'fas fa-cog', 'fas fa-paint-brush', 'fas fa-shopping-cart',
            'fas fa-chart-line', 'fas fa-envelope', 'fas fa-credit-card', 'fas fa-images',
            'fas fa-search', 'fas fa-users', 'fas fa-star', 'fas fa-key',
        ];

        icons.forEach(function(icon) {
            var div = document.createElement('div');
            div.className = 'icon-option' + (icon === currentIcon ? ' selected' : '');
            div.dataset.icon = icon;
            div.title = icon;
            var iconEl = document.createElement('i');
            iconEl.className = icon;
            div.appendChild(iconEl);
            div.addEventListener('click', function() {
                iconInput.value = icon;
                container.querySelectorAll('.icon-option').forEach(function(o) {
                    o.classList.remove('selected');
                });
                this.classList.add('selected');
            });
            container.appendChild(div);
        });
    }

    function initColorSelector() {
        var colorInput = document.getElementById('id_color');
        if (!colorInput) return;

        document.querySelectorAll('.color-option').forEach(function(opt) {
            opt.addEventListener('click', function() {
                var color = this.dataset.color;
                colorInput.value = color;

                document.querySelectorAll('.color-option').forEach(function(o) {
                    o.classList.remove('selected');
                });
                this.classList.add('selected');
            });
        });
    }

    function initCloneButton() {
        var btn = document.getElementById('clone-role-btn');
        if (!btn) return;

        btn.addEventListener('click', function() {
            var url = this.dataset.url;
            var csrfToken = (typeof AdminUtils !== 'undefined')
                ? AdminUtils.getCsrfToken()
                : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

            // Submit clone as POST via hidden form
            var form = document.createElement('form');
            form.method = 'POST';
            form.action = url;
            var csrf = document.createElement('input');
            csrf.type = 'hidden';
            csrf.name = 'csrfmiddlewaretoken';
            csrf.value = csrfToken;
            form.appendChild(csrf);
            document.body.appendChild(form);
            form.submit();
        });
    }

    function initMemberManagement() {
        var addBtn = document.getElementById('add-member-btn');
        if (!addBtn) return;

        var lang = document.documentElement.lang || 'en';

        addBtn.addEventListener('click', function() {
            var select = document.getElementById('member-select');
            if (!select || !select.value) return;

            var userId = select.value;
            var roleId = this.dataset.roleId;
            var csrfToken = (typeof AdminUtils !== 'undefined')
                ? AdminUtils.getCsrfToken()
                : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

            fetch('/' + lang + '/admin/staff_roles/staffrole/' + roleId + '/add-member/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: 'user_id=' + userId,
            })
            .then(function(res) { return res.json(); })
            .then(function(data) {
                if (data.success) {
                    location.reload();
                }
            });
        });

        document.querySelectorAll('.member-remove-btn').forEach(function(btn) {
            btn.addEventListener('click', async function() {
                var userId = this.dataset.userId;
                var roleId = this.dataset.roleId;
                var userName = this.dataset.userName;
                var csrfToken = (typeof AdminUtils !== 'undefined')
                    ? AdminUtils.getCsrfToken()
                    : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
                var removeBtn = this;

                if (!await AdminModal.confirm({ message: userName, danger: true, confirmText: 'Remove' })) return;

                fetch('/' + lang + '/admin/staff_roles/staffrole/' + roleId + '/remove-member/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: 'user_id=' + userId,
                })
                .then(function(res) { return res.json(); })
                .then(function(data) {
                    if (data.success) {
                        removeBtn.closest('.member-row').remove();
                        // Check if empty - use translated text from data attribute
                        var list = document.querySelector('.members-list');
                        if (list && list.children.length === 0) {
                            var emptyText = list.dataset.emptyText || 'No members assigned to this role';
                            list.textContent = '';
                            var emptyDiv = document.createElement('div');
                            emptyDiv.className = 'members-empty';
                            var emptyIcon = document.createElement('i');
                            emptyIcon.className = 'fas fa-user-slash';
                            emptyDiv.appendChild(emptyIcon);
                            var emptyP = document.createElement('p');
                            emptyP.textContent = emptyText;
                            emptyDiv.appendChild(emptyP);
                            list.appendChild(emptyDiv);
                        }
                    }
                });
            });
        });
    }
})();
