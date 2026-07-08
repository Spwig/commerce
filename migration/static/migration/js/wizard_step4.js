/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    function init() {
        var typeSelect = document.getElementById('price_adjustment_type');
        if (typeSelect) {
            typeSelect.addEventListener('change', function () {
                var valueInput = document.getElementById('price_adjustment_value');
                if (!valueInput) { return; }
                valueInput.disabled = this.value === 'none';
                if (this.value === 'none') {
                    valueInput.value = '';
                }
            });
        }
    }

    document.addEventListener('DOMContentLoaded', init);
}());
