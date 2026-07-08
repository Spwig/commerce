/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.kv-editor').forEach(initEditor);
    });

    function initEditor(editor) {
        var rows = editor.querySelector('.kv-editor__rows');

        // Add row
        editor.querySelector('.kv-editor__add').addEventListener('click', function() {
            var fieldName = this.dataset.fieldName;
            var keyLabel = this.dataset.keyLabel;
            var valueLabel = this.dataset.valueLabel;

            // Remove empty message if present
            var empty = rows.querySelector('.kv-editor__empty');
            if (empty) empty.remove();

            var row = document.createElement('div');
            row.className = 'kv-editor__row';
            row.innerHTML =
                '<input type="text" name="' + fieldName + '_keys" value="" class="kv-editor__key" placeholder="' + keyLabel + '">' +
                '<input type="text" name="' + fieldName + '_values" value="" class="kv-editor__value" placeholder="' + valueLabel + '">' +
                '<button type="button" class="kv-editor__remove" title="Remove">&times;</button>';
            rows.appendChild(row);
            row.querySelector('.kv-editor__key').focus();
        });

        // Remove row (event delegation)
        rows.addEventListener('click', function(e) {
            if (e.target.classList.contains('kv-editor__remove')) {
                e.target.closest('.kv-editor__row').remove();
                if (!rows.querySelector('.kv-editor__row')) {
                    var empty = document.createElement('div');
                    empty.className = 'kv-editor__empty';
                    empty.textContent = 'No entries yet. Click "Add Row" to begin.';
                    rows.appendChild(empty);
                }
            }
        });
    }
})();
