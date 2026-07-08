/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Log Viewer Settings - Field relocation and toggle switch logic.
 *
 * Reads translated help strings from a #lvs-config element's data attributes
 * set in the Django template, then moves real Django form inputs into the
 * custom card-layout slots so form submission works natively.
 */
(function () {
    'use strict';

    var config = document.getElementById('lvs-config');
    if (!config) return;

    var form = document.getElementById('logviewersettings_form');
    var layout = document.getElementById('lvs-layout');
    if (!form || !layout) return;

    // Move card layout container INSIDE the Django form
    // so relocated inputs remain within the <form> tag
    form.appendChild(layout);

    // Move Django messages (success/error) between header and cards
    var messageList = document.querySelector('.messagelist');
    if (messageList) {
        layout.insertBefore(messageList, layout.firstChild);
    }

    // Field configuration – help text comes from data attributes
    var fieldMap = {
        'redis_retention_minutes': { type: 'number', help: config.dataset.helpRedis },
        'db_retention_days':       { type: 'number', help: config.dataset.helpDb },
        'archive_batch_size':      { type: 'number', help: config.dataset.helpBatch },
        'archive_interval_seconds':{ type: 'number', help: config.dataset.helpInterval },
        'stream_enabled':          { type: 'checkbox', help: config.dataset.helpStream },
        'max_logs_per_container':  { type: 'number', help: config.dataset.helpMaxLogs },
        'sensitive_patterns':      { type: 'textarea', help: config.dataset.helpPatterns },
        'default_page_size':       { type: 'number', help: config.dataset.helpPageSize },
        'auto_refresh_interval':   { type: 'number', help: config.dataset.helpRefresh }
    };

    var toggleLabel = config.dataset.labelStreamEnabled;

    Object.keys(fieldMap).forEach(function (fieldName) {
        var slot = document.getElementById('slot-' + fieldName);
        var input = document.getElementById('id_' + fieldName);
        if (!slot || !input) return;

        var meta = fieldMap[fieldName];

        if (meta.type === 'checkbox') {
            // Build toggle switch using the actual Django checkbox
            var wrapper = document.createElement('div');
            wrapper.className = 'lvs-toggle-group';

            var label = document.createElement('label');
            label.className = 'toggle-switch';
            label.appendChild(input);

            var slider = document.createElement('span');
            slider.className = 'toggle-slider';
            label.appendChild(slider);
            wrapper.appendChild(label);

            var textDiv = document.createElement('div');
            textDiv.innerHTML =
                '<div class="toggle-label">' + toggleLabel + '</div>' +
                '<div class="toggle-desc">' + meta.help + '</div>';
            wrapper.appendChild(textDiv);
            slot.appendChild(wrapper);
        } else {
            // Add CSS class so stylesheet rules apply
            input.classList.add('lvs-input');
            if (meta.type === 'textarea') {
                input.classList.add('lvs-input--textarea');
                // Pretty-print JSON
                try {
                    var val = JSON.parse(input.value);
                    input.value = JSON.stringify(val, null, 2);
                } catch (e) { /* leave as-is */ }
            }

            slot.appendChild(input);

            var helpDiv = document.createElement('div');
            helpDiv.className = 'help-text';
            helpDiv.textContent = meta.help;
            slot.appendChild(helpDiv);
        }
    });

    // Cancel button navigation
    var cancelBtn = document.getElementById('lvs-cancel-btn');
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function () {
            window.location.href = config.dataset.cancelUrl;
        });
    }
})();
