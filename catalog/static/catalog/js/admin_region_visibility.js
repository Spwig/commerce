/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.region-visibility');
    if (!container) return;

    const table = container.querySelector('.region-visibility__hidden-table');
    const cardsContainer = container.querySelector('.region-cards');
    if (!table || !cardsContainer) return;

    // Build cards from existing table rows
    buildCards();

    // Handle "Add Region Rule" click ourselves (Django's inline JS
    // expects a specific DOM structure we don't provide)
    const addLink = container.querySelector('.add-row a');
    if (addLink) {
      addLink.addEventListener('click', function (e) {
        e.preventDefault();
        addRow();
      });
    }
  });

  function addRow() {
    const container = document.querySelector('.region-visibility');
    const table = container.querySelector('.region-visibility__hidden-table');
    const tbody = table.querySelector('tbody');
    const templateRow = tbody.querySelector('tr.empty-form');
    if (!templateRow) return;

    // Read prefix from the inline formset data
    const inlineGroup = container;
    const formsetData = JSON.parse(inlineGroup.dataset.inlineFormset || '{}');
    const prefix = formsetData.options ? formsetData.options.prefix : 'region_visibility';

    // Get current total and increment
    const totalInput = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
    if (!totalInput) return;
    const total = parseInt(totalInput.value, 10);

    // Clone the template row
    const newRow = templateRow.cloneNode(true);
    newRow.classList.remove('empty-form');
    newRow.id = prefix + '-' + total;

    // Replace __prefix__ with the actual index in all attributes
    const html = newRow.innerHTML.replace(/__prefix__/g, total);
    newRow.innerHTML = html;

    // Insert before the template row
    tbody.insertBefore(newRow, templateRow);

    // Increment total forms
    totalInput.value = total + 1;

    // Build a visual card from the new row
    buildCardFromRow(newRow);
  }

  function buildCards() {
    const container = document.querySelector('.region-visibility');
    const table = container.querySelector('.region-visibility__hidden-table');
    const rows = table.querySelectorAll('tbody tr.form-row:not(.empty-form)');

    rows.forEach(function (row) {
      const deleteCheckbox = row.querySelector('td.delete input[type="checkbox"]');
      if (deleteCheckbox && deleteCheckbox.checked) return;
      buildCardFromRow(row);
    });
  }

  function buildCardFromRow(row) {
    const cardsContainer = document.querySelector('.region-cards');
    if (!cardsContainer) return;

    // Find form elements in the hidden row
    const regionSelect = row.querySelector('.field-region select');
    const visibleCheckbox = row.querySelector('.field-is_visible input[type="checkbox"]');
    const deleteCheckbox = row.querySelector('td.delete input[type="checkbox"]');

    if (!regionSelect) return;

    // Create card
    const card = document.createElement('div');
    card.className = 'region-card';
    card.dataset.rowId = row.id;

    // Region select wrapper
    const selectWrapper = document.createElement('div');
    selectWrapper.className = 'region-card__select';
    const selectClone = regionSelect.cloneNode(true);
    selectClone.id = '';
    selectWrapper.appendChild(selectClone);

    // Sync cloned select back to original
    selectClone.addEventListener('change', function () {
      regionSelect.value = this.value;
    });
    selectClone.value = regionSelect.value;

    // Toggle wrapper
    const toggle = document.createElement('label');
    toggle.className = 'region-toggle';

    const checkClone = document.createElement('input');
    checkClone.type = 'checkbox';
    checkClone.checked = visibleCheckbox ? visibleCheckbox.checked : true;

    const track = document.createElement('span');
    track.className = 'region-toggle__track';
    const thumb = document.createElement('span');
    thumb.className = 'region-toggle__thumb';
    track.appendChild(thumb);

    const labelVisible = document.createElement('span');
    labelVisible.className = 'region-toggle__label-visible';
    labelVisible.textContent = 'Visible';

    const labelHidden = document.createElement('span');
    labelHidden.className = 'region-toggle__label-hidden';
    labelHidden.textContent = 'Hidden';

    toggle.appendChild(checkClone);
    toggle.appendChild(track);
    toggle.appendChild(labelVisible);
    toggle.appendChild(labelHidden);

    // Sync toggle to original checkbox
    checkClone.addEventListener('change', function () {
      if (visibleCheckbox) visibleCheckbox.checked = this.checked;
    });

    // Delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.type = 'button';
    deleteBtn.className = 'region-card__delete';
    deleteBtn.title = 'Remove';
    deleteBtn.innerHTML = '&times;';

    deleteBtn.addEventListener('click', function () {
      if (deleteCheckbox) {
        // Existing row — mark for deletion
        deleteCheckbox.checked = true;
        card.classList.add('region-card--deleted');
      } else {
        // Newly added row — remove entirely
        row.parentNode.removeChild(row);
        card.parentNode.removeChild(card);
        // Decrement total forms
        const container = document.querySelector('.region-visibility');
        const formsetData = JSON.parse(container.dataset.inlineFormset || '{}');
        const prefix = formsetData.options ? formsetData.options.prefix : 'region_visibility';
        const totalInput = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
        if (totalInput) {
          totalInput.value = Math.max(0, parseInt(totalInput.value, 10) - 1);
        }
      }
    });

    card.appendChild(selectWrapper);
    card.appendChild(toggle);
    card.appendChild(deleteBtn);

    cardsContainer.appendChild(card);
  }
})();
