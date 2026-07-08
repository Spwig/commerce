/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var configEl = document.getElementById('compatibility-matrix-config');
    if (!configEl) return;
    var config = JSON.parse(configEl.textContent);

    var PRODUCT_ID = config.productId;
    var lang = document.documentElement.lang || 'en';

    function switchSlot(slotId) {
        // Update tab styles
        document.querySelectorAll('.slot-tab').forEach(function (tab) {
            tab.classList.toggle('active', tab.dataset.slotId == slotId);
        });
        // Show corresponding panel
        document.querySelectorAll('.matrix-panel').forEach(function (panel) {
            panel.classList.toggle('active', panel.id === 'panel-' + slotId);
        });
    }

    function loadRuleEditor(sourceSlotId) {
        var select = document.getElementById('source-select-' + sourceSlotId);
        var editor = document.getElementById('rule-editor-' + sourceSlotId);
        var sourceOptionId = select.value;

        if (!sourceOptionId) {
            editor.style.display = 'none';
            return;
        }

        editor.style.display = 'block';

        // Load existing rules for this source option from each target slot
        document.querySelectorAll('#rule-editor-' + sourceSlotId + ' [id^="target-grid-"]').forEach(function (grid) {
            var parts = grid.id.split('-');
            var targetSlotId = parts[parts.length - 1];
            loadExistingRule(sourceSlotId, sourceOptionId, targetSlotId);
        });
    }

    function loadExistingRule(sourceSlotId, sourceOptionId, targetSlotId) {
        var url = '/' + lang + '/admin/catalog/product/' + PRODUCT_ID + '/compatibility/api/?source_option_id=' + sourceOptionId + '&target_slot_id=' + targetSlotId;

        fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            var grid = document.getElementById('target-grid-' + sourceSlotId + '-' + targetSlotId);
            if (!grid) return;

            // Reset checkboxes
            grid.querySelectorAll('input[type="checkbox"]').forEach(function (cb) {
                cb.checked = false;
                cb.closest('.target-option-card').classList.remove('selected');
            });

            // Reset rule type buttons
            var ruleTypeBtns = document.querySelectorAll(
                '.rule-type-btn[data-source-slot="' + sourceSlotId + '"][data-target-slot="' + targetSlotId + '"]'
            );
            ruleTypeBtns.forEach(function (btn) {
                btn.classList.toggle('active', btn.dataset.ruleType === (data.rule_type || 'requires'));
            });

            var deleteBtn = document.getElementById('delete-btn-' + sourceSlotId + '-' + targetSlotId);

            if (data.exists) {
                // Check compatible options
                data.compatible_option_ids.forEach(function (id) {
                    var cb = document.getElementById('cb-' + sourceSlotId + '-' + targetSlotId + '-' + id);
                    if (cb) {
                        cb.checked = true;
                        cb.closest('.target-option-card').classList.add('selected');
                    }
                });
                if (deleteBtn) deleteBtn.style.display = '';
            } else {
                if (deleteBtn) deleteBtn.style.display = 'none';
            }
        })
        .catch(function (err) { console.error('Load rule error:', err); });
    }

    function setRuleType(btn, type) {
        var sourceSlotId = btn.dataset.sourceSlot;
        var targetSlotId = btn.dataset.targetSlot;
        document.querySelectorAll(
            '.rule-type-btn[data-source-slot="' + sourceSlotId + '"][data-target-slot="' + targetSlotId + '"]'
        ).forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
    }

    function getActiveRuleType(sourceSlotId, targetSlotId) {
        var active = document.querySelector(
            '.rule-type-btn.active[data-source-slot="' + sourceSlotId + '"][data-target-slot="' + targetSlotId + '"]'
        );
        return active ? active.dataset.ruleType : 'requires';
    }

    function saveRule(sourceSlotId, targetSlotId) {
        var sourceSelect = document.getElementById('source-select-' + sourceSlotId);
        var sourceOptionId = sourceSelect.value;
        if (!sourceOptionId) return;

        var grid = document.getElementById('target-grid-' + sourceSlotId + '-' + targetSlotId);
        var checkedIds = [];
        grid.querySelectorAll('input[type="checkbox"]:checked').forEach(function (cb) {
            checkedIds.push(parseInt(cb.value));
        });

        var ruleType = getActiveRuleType(sourceSlotId, targetSlotId);
        var url = '/' + lang + '/admin/catalog/product/' + PRODUCT_ID + '/compatibility/api/';

        showStatus('loading', config.strings.savingRule);

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                source_option_id: parseInt(sourceOptionId),
                target_slot_id: parseInt(targetSlotId),
                rule_type: ruleType,
                compatible_option_ids: checkedIds
            })
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                showStatus('success', config.strings.ruleSaved + ' (' + data.compatible_count + ' ' + config.strings.options + ')');
                var deleteBtn = document.getElementById('delete-btn-' + sourceSlotId + '-' + targetSlotId);
                if (deleteBtn) deleteBtn.style.display = '';
            } else {
                showStatus('error', data.error || config.strings.failedToSave);
            }
        })
        .catch(function (err) {
            showStatus('error', config.strings.errorSaving);
            console.error('Save rule error:', err);
        });
    }

    async function deleteRule(sourceSlotId, targetSlotId) {
        var sourceSelect = document.getElementById('source-select-' + sourceSlotId);
        var sourceOptionId = sourceSelect.value;
        if (!sourceOptionId) return;

        if (!await AdminModal.confirm({ message: config.strings.removeRuleConfirm, danger: true, confirmText: 'Remove' })) return;

        var url = '/' + lang + '/admin/catalog/product/' + PRODUCT_ID + '/compatibility/api/';

        showStatus('loading', config.strings.deletingRule);

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({
                source_option_id: parseInt(sourceOptionId),
                target_slot_id: parseInt(targetSlotId),
                rule_type: 'requires',
                compatible_option_ids: []
            })
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                showStatus('success', config.strings.ruleRemoved);
                // Reset UI
                var grid = document.getElementById('target-grid-' + sourceSlotId + '-' + targetSlotId);
                grid.querySelectorAll('input[type="checkbox"]').forEach(function (cb) {
                    cb.checked = false;
                    cb.closest('.target-option-card').classList.remove('selected');
                });
                var deleteBtn = document.getElementById('delete-btn-' + sourceSlotId + '-' + targetSlotId);
                if (deleteBtn) deleteBtn.style.display = 'none';
            }
        })
        .catch(function (err) { console.error('Delete rule error:', err); });
    }

    function showStatus(type, message) {
        var bar = document.getElementById('status-bar');
        bar.className = 'status-bar ' + type;
        var icons = { success: 'fa-check-circle', error: 'fa-exclamation-circle', loading: 'fa-spinner fa-spin' };
        bar.innerHTML = '<i class="fas ' + (icons[type] || '') + '"></i> ' + message;
        if (type !== 'loading') {
            setTimeout(function () { bar.className = 'status-bar'; }, 3000);
        }
    }

    function getCsrfToken() {
        return AdminUtils.getCsrfToken();
    }

    // Event delegation for data-action elements
    document.addEventListener('click', async function (e) {
        // Handle data-confirm on buttons/submit
        var confirmEl = e.target.closest('[data-confirm]');
        if (confirmEl) {
            var msg = confirmEl.getAttribute('data-confirm');
            if (msg) {
                e.preventDefault();
                if (!await AdminModal.confirm(msg)) {
                    return;
                }
                // Re-trigger the action after confirmation
                if (!confirmEl.dataset.action) {
                    if (confirmEl.tagName === 'A') {
                        window.location.href = confirmEl.href;
                    } else if (confirmEl.form) {
                        if (confirmEl.name) {
                            var hidden = document.createElement('input');
                            hidden.type = 'hidden';
                            hidden.name = confirmEl.name;
                            hidden.value = confirmEl.value || '';
                            confirmEl.form.appendChild(hidden);
                        }
                        confirmEl.form.submit();
                    }
                    return;
                }
            }
        }

        var btn = e.target.closest('[data-action]');
        if (!btn) return;

        var action = btn.dataset.action;
        if (action === 'switch-slot') {
            switchSlot(btn.dataset.slotId);
        } else if (action === 'set-rule-type') {
            setRuleType(btn, btn.dataset.ruleType);
        } else if (action === 'save-rule') {
            saveRule(btn.dataset.sourceSlot, btn.dataset.targetSlot);
        } else if (action === 'delete-rule') {
            deleteRule(btn.dataset.sourceSlot, btn.dataset.targetSlot);
        }
    });

    // Event delegation for data-action selects
    document.addEventListener('change', function (e) {
        if (e.target.tagName === 'SELECT' && e.target.dataset.action === 'load-rule-editor') {
            loadRuleEditor(e.target.dataset.slotId);
        }
        // Toggle selected class on checkbox click
        if (e.target.type === 'checkbox' && e.target.closest('.target-option-card')) {
            e.target.closest('.target-option-card').classList.toggle('selected', e.target.checked);
        }
    });
})();
