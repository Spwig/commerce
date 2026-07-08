/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Sync Categories JS
 * Handles "Select All" checkbox and category selection validation
 * for both Settings Sync step 2 and Full Migration step 2.
 */
(function() {
    'use strict';

    const selectAllCheckbox = document.getElementById('select-all-categories');
    const categoryCheckboxes = document.querySelectorAll('input[name="categories"]');
    const form = document.getElementById('categories-form') || document.getElementById('scope-form');

    if (!selectAllCheckbox || !categoryCheckboxes.length) return;

    // Select All toggle
    selectAllCheckbox.addEventListener('change', function() {
        categoryCheckboxes.forEach(cb => {
            cb.checked = this.checked;
        });
    });

    // Update Select All state when individual checkboxes change
    categoryCheckboxes.forEach(cb => {
        cb.addEventListener('change', function() {
            const allChecked = Array.from(categoryCheckboxes).every(c => c.checked);
            const anyChecked = Array.from(categoryCheckboxes).some(c => c.checked);
            selectAllCheckbox.checked = allChecked;
            selectAllCheckbox.indeterminate = anyChecked && !allChecked;
        });
    });

    // Initialize Select All state
    const allChecked = Array.from(categoryCheckboxes).every(c => c.checked);
    const anyChecked = Array.from(categoryCheckboxes).some(c => c.checked);
    selectAllCheckbox.checked = allChecked;
    selectAllCheckbox.indeterminate = anyChecked && !allChecked;

    // Form validation: require at least one category
    if (form) {
        form.addEventListener('submit', function(e) {
            const checked = Array.from(categoryCheckboxes).filter(c => c.checked);
            if (checked.length === 0) {
                e.preventDefault();
                alert('Please select at least one category.');
            }
        });
    }
})();
