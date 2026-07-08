/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        var container = document.querySelector('.region-visibility');
        if (!container) return;

        var table = container.querySelector('.region-visibility__hidden-table');
        var cardsContainer = container.querySelector('.region-cards');
        if (!table || !cardsContainer) return;

        // Build cards from existing table rows
        buildCards();

        // Handle "Add Region Rule" click ourselves (Django's inline JS
        // expects a specific DOM structure we don't provide)
        var addLink = container.querySelector('.add-row a');
        if (addLink) {
            addLink.addEventListener('click', function(e) {
                e.preventDefault();
                addRow();
            });
        }
    });

    function addRow() {
        var container = document.querySelector('.region-visibility');
        var table = container.querySelector('.region-visibility__hidden-table');
        var tbody = table.querySelector('tbody');
        var templateRow = tbody.querySelector('tr.empty-form');
        if (!templateRow) return;

        // Read prefix from the inline formset data
        var inlineGroup = container;
        var formsetData = JSON.parse(inlineGroup.dataset.inlineFormset || '{}');
        var prefix = formsetData.options ? formsetData.options.prefix : 'region_visibility';

        // Get current total and increment
        var totalInput = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
        if (!totalInput) return;
        var total = parseInt(totalInput.value, 10);

        // Clone the template row
        var newRow = templateRow.cloneNode(true);
        newRow.classList.remove('empty-form');
        newRow.id = prefix + '-' + total;

        // Replace __prefix__ with the actual index in all attributes
        var html = newRow.innerHTML.replace(/__prefix__/g, total);
        newRow.innerHTML = html;

        // Insert before the template row
        tbody.insertBefore(newRow, templateRow);

        // Increment total forms
        totalInput.value = total + 1;

        // Build a visual card from the new row
        buildCardFromRow(newRow);
    }

    function buildCards() {
        var container = document.querySelector('.region-visibility');
        var table = container.querySelector('.region-visibility__hidden-table');
        var rows = table.querySelectorAll('tbody tr.form-row:not(.empty-form)');

        rows.forEach(function(row) {
            var deleteCheckbox = row.querySelector('td.delete input[type="checkbox"]');
            if (deleteCheckbox && deleteCheckbox.checked) return;
            buildCardFromRow(row);
        });
    }

    function buildCardFromRow(row) {
        var cardsContainer = document.querySelector('.region-cards');
        if (!cardsContainer) return;

        // Find form elements in the hidden row
        var regionSelect = row.querySelector('.field-region select');
        var visibleCheckbox = row.querySelector('.field-is_visible input[type="checkbox"]');
        var deleteCheckbox = row.querySelector('td.delete input[type="checkbox"]');

        if (!regionSelect) return;

        // Create card
        var card = document.createElement('div');
        card.className = 'region-card';
        card.dataset.rowId = row.id;

        // Region select wrapper
        var selectWrapper = document.createElement('div');
        selectWrapper.className = 'region-card__select';
        var selectClone = regionSelect.cloneNode(true);
        selectClone.id = '';
        selectWrapper.appendChild(selectClone);

        // Sync cloned select back to original
        selectClone.addEventListener('change', function() {
            regionSelect.value = this.value;
        });
        selectClone.value = regionSelect.value;

        // Toggle wrapper
        var toggle = document.createElement('label');
        toggle.className = 'region-toggle';

        var checkClone = document.createElement('input');
        checkClone.type = 'checkbox';
        checkClone.checked = visibleCheckbox ? visibleCheckbox.checked : true;

        var track = document.createElement('span');
        track.className = 'region-toggle__track';
        var thumb = document.createElement('span');
        thumb.className = 'region-toggle__thumb';
        track.appendChild(thumb);

        var labelVisible = document.createElement('span');
        labelVisible.className = 'region-toggle__label-visible';
        labelVisible.textContent = 'Visible';

        var labelHidden = document.createElement('span');
        labelHidden.className = 'region-toggle__label-hidden';
        labelHidden.textContent = 'Hidden';

        toggle.appendChild(checkClone);
        toggle.appendChild(track);
        toggle.appendChild(labelVisible);
        toggle.appendChild(labelHidden);

        // Sync toggle to original checkbox
        checkClone.addEventListener('change', function() {
            if (visibleCheckbox) visibleCheckbox.checked = this.checked;
        });

        // Delete button
        var deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.className = 'region-card__delete';
        deleteBtn.title = 'Remove';
        deleteBtn.innerHTML = '&times;';

        deleteBtn.addEventListener('click', function() {
            if (deleteCheckbox) {
                // Existing row — mark for deletion
                deleteCheckbox.checked = true;
                card.classList.add('region-card--deleted');
            } else {
                // Newly added row — remove entirely
                row.parentNode.removeChild(row);
                card.parentNode.removeChild(card);
                // Decrement total forms
                var container = document.querySelector('.region-visibility');
                var formsetData = JSON.parse(container.dataset.inlineFormset || '{}');
                var prefix = formsetData.options ? formsetData.options.prefix : 'region_visibility';
                var totalInput = document.getElementById('id_' + prefix + '-TOTAL_FORMS');
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
