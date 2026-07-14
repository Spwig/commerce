/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let data = {};

  function init() {
    const dataEl = document.getElementById('blogpost-list-data');
    if (dataEl) {
      try {
        data = JSON.parse(dataEl.textContent);
      } catch (e) {}
    }

    const categoryFilter = document.getElementById('category-filter');
    if (categoryFilter) {
      categoryFilter.addEventListener('change', function () {
        filterByCategory(this.value);
      });
    }

    const checkboxes = document.querySelectorAll('.post-select');
    const bulkSelector = document.getElementById('bulk-action-selector');
    const applyBtn = document.getElementById('apply-bulk-action');
    const selectedCount = document.getElementById('selected-count');

    if (!bulkSelector || !applyBtn) {
      return;
    }

    function updateSelectedCount() {
      const checked = document.querySelectorAll('.post-select:checked').length;
      if (checked > 0) {
        selectedCount.textContent = checked + ' ' + (data.selected || 'selected');
        applyBtn.disabled = !bulkSelector.value;
      } else {
        selectedCount.textContent = '';
        applyBtn.disabled = true;
      }
    }

    checkboxes.forEach(function (cb) {
      cb.addEventListener('change', updateSelectedCount);
    });

    bulkSelector.addEventListener('change', function () {
      const checked = document.querySelectorAll('.post-select:checked').length;
      applyBtn.disabled = !this.value || checked === 0;
    });

    applyBtn.addEventListener('click', async function () {
      const action = bulkSelector.value;
      const selected = Array.from(document.querySelectorAll('.post-select:checked')).map(
        function (cb) {
          return cb.value;
        }
      );

      if (!action || selected.length === 0) {
        return;
      }

      if (action === 'delete') {
        if (
          !(await AdminModal.confirm({
            message: data.confirmDelete || 'Are you sure you want to delete the selected posts?',
            danger: true,
            confirmText: 'Delete',
          }))
        ) {
          return;
        }
      }

      const form = document.createElement('form');
      form.method = 'POST';
      form.action = data.changelistUrl || '';

      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
      if (csrfToken) {
        form.appendChild(csrfToken.cloneNode());
      }

      const actionInput = document.createElement('input');
      actionInput.type = 'hidden';
      actionInput.name = 'action';
      actionInput.value = action;
      form.appendChild(actionInput);

      selected.forEach(function (id) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = '_selected_action';
        input.value = id;
        form.appendChild(input);
      });

      document.body.appendChild(form);
      form.submit();
    });
  }

  function filterByCategory(categoryId) {
    const url = new URL(window.location.href);
    if (categoryId) {
      url.searchParams.set('category__id__exact', categoryId);
    } else {
      url.searchParams.delete('category__id__exact');
    }
    window.location.href = url.toString();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
