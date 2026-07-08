/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var translations = {};

    function init() {
        var dataEl = document.getElementById('loyaltytier-form-data');
        if (dataEl) {
            try {
                var data = JSON.parse(dataEl.textContent);
                translations = data.translations || {};
            } catch (e) {}
        }

        setTimeout(function () {
            initializePreview();
            initializeColorPicker();
        }, 100);
    }

    function updatePreview() {
        var nameField = document.querySelector('#id_name');
        var rankField = document.querySelector('#id_rank');
        var colorField = document.querySelector('#id_color');
        var iconField = document.querySelector('#id_icon');
        var multiplierField = document.querySelector('#id_points_multiplier');
        var pointsField = document.querySelector('#id_min_points_earned');
        var spendField = document.querySelector('#id_min_spend');

        var previewBadge = document.getElementById('preview-badge');
        var previewName = document.getElementById('preview-name');
        var previewIcon = document.getElementById('preview-icon');
        var previewRank = document.getElementById('preview-rank');
        var previewMultiplier = document.getElementById('preview-multiplier');
        var previewPoints = document.getElementById('preview-points');
        var previewSpend = document.getElementById('preview-spend');

        if (nameField && previewName) {
            previewName.textContent = nameField.value || (translations.newTier || 'New Tier');
        }
        if (colorField && previewBadge) {
            previewBadge.style.background = colorField.value || '#667eea';
        }
        if (iconField && previewIcon) {
            previewIcon.className = 'fas ' + (iconField.value || 'fa-layer-group') + ' tier-badge-icon';
        }
        if (rankField && previewRank) {
            previewRank.textContent = rankField.value || '1';
        }
        if (multiplierField && previewMultiplier) {
            previewMultiplier.textContent = (multiplierField.value || '1.00') + 'x';
        }
        if (pointsField && previewPoints) {
            previewPoints.textContent = pointsField.value || '0';
        }
        if (spendField && previewSpend) {
            previewSpend.textContent = '$' + (spendField.value || '0.00');
        }
    }

    function initializeColorPicker() {
        var colorField = document.querySelector('#id_color');
        if (colorField && typeof ColorPickerUtility !== 'undefined') {
            var picker = new ColorPickerUtility({
                showOpacity: false,
                onChange: function (color) {
                    colorField.value = color;
                    updatePreview();
                }
            });
            picker.attach(colorField, colorField.value || '#667eea');
        }
    }

    function initializePreview() {
        var nameField = document.querySelector('#id_name');
        var rankField = document.querySelector('#id_rank');
        var colorField = document.querySelector('#id_color');
        var iconField = document.querySelector('#id_icon');
        var multiplierField = document.querySelector('#id_points_multiplier');
        var pointsField = document.querySelector('#id_min_points_earned');
        var spendField = document.querySelector('#id_min_spend');

        if (nameField) { nameField.addEventListener('input', updatePreview); }
        if (rankField) { rankField.addEventListener('input', updatePreview); }
        if (colorField) { colorField.addEventListener('input', updatePreview); }
        if (iconField) {
            iconField.addEventListener('change', updatePreview);
            document.addEventListener('searchable-select-change', function (e) {
                if (e.detail && e.detail.select === iconField) { updatePreview(); }
            });
        }
        if (multiplierField) { multiplierField.addEventListener('input', updatePreview); }
        if (pointsField) { pointsField.addEventListener('input', updatePreview); }
        if (spendField) { spendField.addEventListener('input', updatePreview); }

        updatePreview();
    }

    document.addEventListener('DOMContentLoaded', init);
}());
