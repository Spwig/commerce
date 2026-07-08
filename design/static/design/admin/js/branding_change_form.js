/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    function init() {
        // Group color fields
        var colorFields = document.querySelectorAll('.form-row[class*="field-"][class*="_color"]');
        if (colorFields.length > 0) {
            var colorGroup = document.createElement('div');
            colorGroup.className = 'color-group';
            Array.prototype.forEach.call(colorFields, function (field) {
                colorGroup.appendChild(field);
            });
            if (colorFields[0].parentNode) {
                colorFields[0].parentNode.insertBefore(colorGroup, colorFields[0]);
            }
        }

        // Group typography fields
        var typographyFields = document.querySelectorAll('.form-row[class*="font_"], .form-row[class*="line_height"]');
        if (typographyFields.length > 0) {
            var typographyGroup = document.createElement('div');
            typographyGroup.className = 'typography-group';
            Array.prototype.forEach.call(typographyFields, function (field) {
                typographyGroup.appendChild(field);
            });
            if (typographyFields[0].parentNode) {
                typographyFields[0].parentNode.insertBefore(typographyGroup, typographyFields[0]);
            }
        }

        // Group spacing fields
        var spacingFields = document.querySelectorAll('.form-row[class*="spacing_"], .form-row[class*="border_radius"]');
        if (spacingFields.length > 0) {
            var spacingGroup = document.createElement('div');
            spacingGroup.className = 'spacing-group';
            Array.prototype.forEach.call(spacingFields, function (field) {
                spacingGroup.appendChild(field);
            });
            if (spacingFields[0].parentNode) {
                spacingFields[0].parentNode.insertBefore(spacingGroup, spacingFields[0]);
            }
        }

        // Add color previews to color inputs
        document.querySelectorAll('input[type="color"]').forEach(function (input) {
            var preview = document.createElement('span');
            preview.className = 'color-preview';
            preview.style.backgroundColor = input.value;
            input.parentNode.appendChild(preview);
            input.addEventListener('change', function () {
                preview.style.backgroundColor = this.value;
            });
        });

        // Live preview update (debounced)
        var updateTimer;
        document.querySelectorAll('input, textarea').forEach(function (input) {
            input.addEventListener('input', function () {
                clearTimeout(updateTimer);
                updateTimer = setTimeout(updateLivePreview, 500);
            });
        });
    }

    function updateLivePreview() {
        console.log('Updating live preview...');
    }

    document.addEventListener('DOMContentLoaded', init);
}());
