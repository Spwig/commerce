/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Staff Role Editor - Permission category toggles, access toggles,
 * icon/color selectors, and member management.
 *
 * Tab switching is handled by AdminTabs (auto-initialized via .admin-tabs).
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initCategoryToggles();
    initAccessToggles();
    initIconSelector();
    initColorSelector();
    initMemberManagement();
    initCloneButton();
  });

  function initCategoryToggles() {
    document.querySelectorAll('.level-option').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const row = this.closest('.category-row');
        const catKey = row.dataset.category;
        const level = this.dataset.level;

        // Update visual state
        row.querySelectorAll('.level-option').forEach(function (b) {
          b.classList.remove('active');
        });
        this.classList.add('active');

        // Update hidden input
        const input = document.getElementById('cat_' + catKey);
        if (input) input.value = level;
      });
    });
  }

  function initAccessToggles() {
    const adminToggle = document.getElementById('id_can_access_admin');
    const posToggle = document.getElementById('id_can_access_pos');

    function updateAccessVisuals() {
      // Update toggle card styling
      document.querySelectorAll('.access-toggle').forEach(function (toggle) {
        const cb = toggle.querySelector('input[type="checkbox"]');
        if (cb && cb.checked) {
          toggle.classList.add('active');
        } else {
          toggle.classList.remove('active');
        }
      });

      // Dim/undim relevant tab buttons via CSS class (CSP-safe)
      const adminTabBtn = document.querySelector('.admin-tab-btn[data-tab="permissions"]');
      const posTabBtn = document.querySelector('.admin-tab-btn[data-tab="pos"]');

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
    const iconInput = document.getElementById('id_icon');
    const container = document.getElementById('icon-selector');
    if (!iconInput || !container) return;
    if (container.children.length > 0) return; // Already initialized

    const currentIcon = container.dataset.current || 'fas fa-user';
    const icons = [
      'fas fa-user',
      'fas fa-user-tie',
      'fas fa-user-check',
      'fas fa-user-shield',
      'fas fa-crown',
      'fas fa-pen-fancy',
      'fas fa-box',
      'fas fa-bullhorn',
      'fas fa-cash-register',
      'fas fa-cog',
      'fas fa-paint-brush',
      'fas fa-shopping-cart',
      'fas fa-chart-line',
      'fas fa-envelope',
      'fas fa-credit-card',
      'fas fa-images',
      'fas fa-search',
      'fas fa-users',
      'fas fa-star',
      'fas fa-key',
    ];

    icons.forEach(function (icon) {
      const div = document.createElement('div');
      div.className = 'icon-option' + (icon === currentIcon ? ' selected' : '');
      div.dataset.icon = icon;
      div.title = icon;
      const iconEl = document.createElement('i');
      iconEl.className = icon;
      div.appendChild(iconEl);
      div.addEventListener('click', function () {
        iconInput.value = icon;
        container.querySelectorAll('.icon-option').forEach(function (o) {
          o.classList.remove('selected');
        });
        this.classList.add('selected');
      });
      container.appendChild(div);
    });
  }

  function initColorSelector() {
    const colorInput = document.getElementById('id_color');
    if (!colorInput) return;

    document.querySelectorAll('.color-option').forEach(function (opt) {
      opt.addEventListener('click', function () {
        const color = this.dataset.color;
        colorInput.value = color;

        document.querySelectorAll('.color-option').forEach(function (o) {
          o.classList.remove('selected');
        });
        this.classList.add('selected');
      });
    });
  }

  function initCloneButton() {
    const btn = document.getElementById('clone-role-btn');
    if (!btn) return;

    btn.addEventListener('click', function () {
      const url = this.dataset.url;
      const csrfToken =
        typeof AdminUtils !== 'undefined'
          ? AdminUtils.getCsrfToken()
          : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

      // Submit clone as POST via hidden form
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = url;
      const csrf = document.createElement('input');
      csrf.type = 'hidden';
      csrf.name = 'csrfmiddlewaretoken';
      csrf.value = csrfToken;
      form.appendChild(csrf);
      document.body.appendChild(form);
      form.submit();
    });
  }

  function initMemberManagement() {
    const addBtn = document.getElementById('add-member-btn');
    if (!addBtn) return;

    const lang = document.documentElement.lang || 'en';

    addBtn.addEventListener('click', function () {
      const select = document.getElementById('member-select');
      if (!select || !select.value) return;

      const userId = select.value;
      const roleId = this.dataset.roleId;
      const csrfToken =
        typeof AdminUtils !== 'undefined'
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
        .then(function (res) {
          return res.json();
        })
        .then(function (data) {
          if (data.success) {
            location.reload();
          }
        });
    });

    document.querySelectorAll('.member-remove-btn').forEach(function (btn) {
      btn.addEventListener('click', async function () {
        const userId = this.dataset.userId;
        const roleId = this.dataset.roleId;
        const userName = this.dataset.userName;
        const csrfToken =
          typeof AdminUtils !== 'undefined'
            ? AdminUtils.getCsrfToken()
            : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
        const removeBtn = this;

        if (!(await AdminModal.confirm({ message: userName, danger: true, confirmText: 'Remove' })))
          return;

        fetch('/' + lang + '/admin/staff_roles/staffrole/' + roleId + '/remove-member/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
          },
          body: 'user_id=' + userId,
        })
          .then(function (res) {
            return res.json();
          })
          .then(function (data) {
            if (data.success) {
              removeBtn.closest('.member-row').remove();
              // Check if empty - use translated text from data attribute
              const list = document.querySelector('.members-list');
              if (list && list.children.length === 0) {
                const emptyText = list.dataset.emptyText || 'No members assigned to this role';
                list.textContent = '';
                const emptyDiv = document.createElement('div');
                emptyDiv.className = 'members-empty';
                const emptyIcon = document.createElement('i');
                emptyIcon.className = 'fas fa-user-slash';
                emptyDiv.appendChild(emptyIcon);
                const emptyP = document.createElement('p');
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
