/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    function parseJsonScript(id) {
        var el = document.getElementById(id);
        if (!el) return {};
        try {
            return JSON.parse(el.textContent);
        } catch (e) {
            console.error('StaffRole: failed to parse ' + id, e);
            return {};
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        // Set current permission category values
        var currentCategories = parseJsonScript('staff-role-categories');
        for (var key in currentCategories) {
            var input = document.getElementById('cat_' + key);
            if (input) {
                input.value = currentCategories[key];
                // Update button visuals
                var row = document.querySelector('.category-row[data-category="' + key + '"]');
                if (row) {
                    row.querySelectorAll('.level-option').forEach(function (btn) {
                        btn.classList.remove('active');
                        if (btn.dataset.level === currentCategories[key]) {
                            btn.classList.add('active');
                        }
                    });
                }
            }
        }

        // Set current POS permission values
        var currentPos = parseJsonScript('staff-role-pos-permissions');
        for (var posKey in currentPos) {
            var el = document.getElementById('pos_' + posKey);
            if (el) {
                if (el.type === 'checkbox') {
                    el.checked = !!currentPos[posKey];
                } else if (el.type === 'number') {
                    el.value = currentPos[posKey];
                }
            }
        }
    });
}());
