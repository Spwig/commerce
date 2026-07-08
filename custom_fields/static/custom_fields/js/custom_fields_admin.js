/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Custom Fields Management Page - Admin JavaScript
 *
 * Handles CRUD operations for custom field groups and definitions
 * via AJAX modals on the centralized management page.
 *
 * Uses AdminUtils for language-aware URL building, CSRF, and fetch helpers.
 * Tab switching handled by global AdminTabs (auto-initialized).
 */
(function() {
    'use strict';

    var BASE_URL = AdminUtils.buildAdminUrl('/admin/custom-fields');

    // i18n strings from data attributes
    var i18nEl = document.getElementById('cf-i18n');
    var i18n = i18nEl ? i18nEl.dataset : {};

    // ═══════════════════════════════════════════
    // Toast Notifications (Django .messagelist pattern)
    // ═══════════════════════════════════════════

    function showMessage(message, type) {
        var messagesDiv = document.querySelector('.messagelist');
        if (!messagesDiv) {
            messagesDiv = document.createElement('ul');
            messagesDiv.className = 'messagelist';
            var content = document.getElementById('content-main');
            if (content && content.parentNode) {
                content.parentNode.insertBefore(messagesDiv, content);
            }
        }
        var li = document.createElement('li');
        li.className = type || 'info';
        li.textContent = message;
        messagesDiv.appendChild(li);
        setTimeout(function() { li.remove(); }, 5000);
    }

    // ═══════════════════════════════════════════
    // API Helper
    // ═══════════════════════════════════════════

    function apiRequest(url, method, data) {
        var options = AdminUtils.buildFetchOptions(method, data, {
            'X-Requested-With': 'XMLHttpRequest'
        });
        return fetch(url, options).then(function(r) { return r.json(); });
    }

    // ═══════════════════════════════════════════
    // Modal Helpers (class-based, no inline styles)
    // ═══════════════════════════════════════════

    function openModal(id) {
        document.getElementById(id).classList.remove('cf-hidden');
    }

    function closeModal(id) {
        document.getElementById(id).classList.add('cf-hidden');
    }

    // Close modals on overlay click or cancel
    document.querySelectorAll('.cf-modal-overlay').forEach(function(overlay) {
        overlay.addEventListener('click', function(e) {
            if (e.target === this) closeModal(this.id);
        });
    });
    document.querySelectorAll('.cf-modal-close, .cf-modal-cancel').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var modal = this.closest('.cf-modal-overlay');
            if (modal) closeModal(modal.id);
        });
    });

    // ═══════════════════════════════════════════
    // Group CRUD
    // ═══════════════════════════════════════════

    // Add Group button
    document.querySelectorAll('.cf-btn-add-group').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.getElementById('groupModalId').value = '';
            document.getElementById('groupModalContentTypeId').value = this.dataset.contentTypeId;
            document.getElementById('groupModalTitle').textContent = i18n.addGroup || 'Add Field Group';
            document.getElementById('groupName').value = '';
            document.getElementById('groupShowStorefront').checked = false;
            openModal('groupModal');
            document.getElementById('groupName').focus();
        });
    });

    // Edit Group button
    document.querySelectorAll('.cf-btn-edit-group').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var card = this.closest('.field-group-card');
            var groupId = card.dataset.groupId;
            var name = card.querySelector('.field-group-header-left h3').textContent.trim();
            var showStorefront = card.dataset.showStorefront === 'true';

            document.getElementById('groupModalId').value = groupId;
            document.getElementById('groupModalTitle').textContent = i18n.editGroup || 'Edit Field Group';
            document.getElementById('groupName').value = name;
            document.getElementById('groupShowStorefront').checked = showStorefront;
            openModal('groupModal');
        });
    });

    // Save Group
    document.getElementById('groupModalSave').addEventListener('click', function() {
        var groupId = document.getElementById('groupModalId').value;
        var name = document.getElementById('groupName').value.trim();
        var showStorefront = document.getElementById('groupShowStorefront').checked;
        var ctId = document.getElementById('groupModalContentTypeId').value;

        if (!name) {
            document.getElementById('groupName').focus();
            return;
        }

        if (groupId) {
            apiRequest(BASE_URL + '/groups/' + groupId + '/update/', 'POST', {
                name: name,
                show_on_storefront: showStorefront,
            }).then(function(resp) {
                if (resp.success) {
                    showMessage(i18n.successSaved || 'Changes saved successfully.', 'success');
                    location.reload();
                } else {
                    showMessage(resp.error || i18n.errorGeneric || 'An error occurred.', 'error');
                }
            });
        } else {
            apiRequest(BASE_URL + '/groups/create/', 'POST', {
                name: name,
                content_type_id: parseInt(ctId),
                show_on_storefront: showStorefront,
            }).then(function(resp) {
                if (resp.success) {
                    showMessage(i18n.successSaved || 'Changes saved successfully.', 'success');
                    location.reload();
                } else {
                    showMessage(resp.error || i18n.errorGeneric || 'An error occurred.', 'error');
                }
            });
        }
    });

    // Delete Group
    document.querySelectorAll('.cf-btn-delete-group').forEach(function(btn) {
        btn.addEventListener('click', async function() {
            var confirmMsg = i18n.confirmDeleteGroup || 'Are you sure you want to delete this group?';
            if (!await AdminModal.confirm({
                message: confirmMsg,
                danger: true,
                confirmText: 'Delete'
            })) {
                return;
            }
            var groupId = this.closest('.field-group-card').dataset.groupId;
            apiRequest(BASE_URL + '/groups/' + groupId + '/delete/', 'POST').then(function(resp) {
                if (resp.success) {
                    showMessage(i18n.successDeleted || 'Item moved to recycle bin.', 'success');
                    location.reload();
                } else {
                    showMessage(resp.error || i18n.errorGeneric || 'An error occurred.', 'error');
                }
            });
        });
    });

    // ═══════════════════════════════════════════
    // Field CRUD
    // ═══════════════════════════════════════════

    function resetFieldModal() {
        document.getElementById('fieldModalId').value = '';
        document.getElementById('fieldName').value = '';
        document.getElementById('fieldType').value = 'text';
        document.getElementById('fieldType').disabled = false;
        document.getElementById('fieldHelpText').value = '';
        document.getElementById('fieldDefault').value = '';
        document.getElementById('fieldMinLength').value = '';
        document.getElementById('fieldMaxLength').value = '';
        document.getElementById('fieldRegex').value = '';
        document.getElementById('fieldMin').value = '';
        document.getElementById('fieldMax').value = '';
        document.getElementById('fieldDecMin').value = '';
        document.getElementById('fieldDecMax').value = '';
        document.getElementById('fieldDecPlaces').value = '2';
        document.getElementById('fieldRequired').checked = false;
        document.getElementById('fieldStorefront').checked = false;
        document.getElementById('fieldTranslatable').checked = false;
        document.getElementById('choicesList').innerHTML = '';
        updateValidationVisibility('text');
    }

    function updateValidationVisibility(fieldType) {
        document.querySelectorAll('.validation-fields').forEach(function(el) {
            el.classList.add('cf-hidden');
        });

        if (fieldType === 'text' || fieldType === 'textarea') {
            document.getElementById('textValidation').classList.remove('cf-hidden');
        } else if (fieldType === 'number') {
            document.getElementById('numberValidation').classList.remove('cf-hidden');
        } else if (fieldType === 'decimal') {
            document.getElementById('decimalValidation').classList.remove('cf-hidden');
        } else if (fieldType === 'select' || fieldType === 'multiselect') {
            document.getElementById('choicesValidation').classList.remove('cf-hidden');
        }

        // Translatable option only for text/textarea
        var transOpt = document.getElementById('translatableOption');
        if (fieldType === 'text' || fieldType === 'textarea') {
            transOpt.classList.remove('cf-hidden');
        } else {
            transOpt.classList.add('cf-hidden');
            document.getElementById('fieldTranslatable').checked = false;
        }
    }

    document.getElementById('fieldType').addEventListener('change', function() {
        updateValidationVisibility(this.value);
    });

    // Add Field button
    document.querySelectorAll('.cf-btn-add-field').forEach(function(btn) {
        btn.addEventListener('click', function() {
            resetFieldModal();
            document.getElementById('fieldModalGroupId').value = this.dataset.groupId;
            document.getElementById('fieldModalContentTypeId').value = this.dataset.contentTypeId;
            document.getElementById('fieldModalTitle').textContent = i18n.addField || 'Add Custom Field';
            openModal('fieldModal');
            document.getElementById('fieldName').focus();
        });
    });

    // Edit Field button
    document.querySelectorAll('.cf-btn-edit-field').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var fieldId = this.dataset.fieldId;

            fetch(BASE_URL + '/fields/' + fieldId + '/', {
                headers: {
                    'X-CSRFToken': AdminUtils.getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(function(r) { return r.json(); })
            .then(function(resp) {
                if (!resp.success) {
                    showMessage(resp.error || i18n.errorGeneric, 'error');
                    return;
                }
                var f = resp.field;
                resetFieldModal();

                document.getElementById('fieldModalId').value = f.id;
                document.getElementById('fieldModalGroupId').value = f.group_id;
                document.getElementById('fieldName').value = f.name;
                document.getElementById('fieldType').value = f.field_type;
                // Disable field type on edit to prevent data integrity issues
                document.getElementById('fieldType').disabled = true;
                document.getElementById('fieldHelpText').value = f.help_text || '';
                document.getElementById('fieldDefault').value = f.default_value != null ? f.default_value : '';
                document.getElementById('fieldRequired').checked = f.is_required;
                document.getElementById('fieldStorefront').checked = f.show_on_storefront;
                document.getElementById('fieldTranslatable').checked = f.is_translatable;
                document.getElementById('fieldModalTitle').textContent = i18n.editField || 'Edit Custom Field';

                updateValidationVisibility(f.field_type);

                // Populate type-specific validation
                var vc = f.validation_config || {};
                if (f.field_type === 'text' || f.field_type === 'textarea') {
                    document.getElementById('fieldMinLength').value = vc.min_length || '';
                    document.getElementById('fieldMaxLength').value = vc.max_length || '';
                    document.getElementById('fieldRegex').value = vc.regex || '';
                } else if (f.field_type === 'number') {
                    document.getElementById('fieldMin').value = vc.min != null ? vc.min : '';
                    document.getElementById('fieldMax').value = vc.max != null ? vc.max : '';
                } else if (f.field_type === 'decimal') {
                    document.getElementById('fieldDecMin').value = vc.min != null ? vc.min : '';
                    document.getElementById('fieldDecMax').value = vc.max != null ? vc.max : '';
                    document.getElementById('fieldDecPlaces').value = vc.decimal_places || '2';
                } else if (f.field_type === 'select' || f.field_type === 'multiselect') {
                    var choices = vc.choices || [];
                    choices.forEach(function(c) { addChoiceRow(c.value, c.label); });
                }

                openModal('fieldModal');
            });
        });
    });

    // Save Field
    document.getElementById('fieldModalSave').addEventListener('click', function() {
        var fieldId = document.getElementById('fieldModalId').value;
        var groupId = document.getElementById('fieldModalGroupId').value;
        var name = document.getElementById('fieldName').value.trim();
        // Read field_type from select even if disabled
        var fieldType = document.getElementById('fieldType').value;

        if (!name) {
            document.getElementById('fieldName').focus();
            return;
        }

        var data = {
            group_id: parseInt(groupId),
            name: name,
            field_type: fieldType,
            help_text: document.getElementById('fieldHelpText').value.trim(),
            default_value: document.getElementById('fieldDefault').value.trim() || null,
            is_required: document.getElementById('fieldRequired').checked,
            show_on_storefront: document.getElementById('fieldStorefront').checked,
            is_translatable: document.getElementById('fieldTranslatable').checked,
        };

        // Type-specific validation config
        var validationConfig = {};
        if (fieldType === 'text' || fieldType === 'textarea') {
            var minLen = document.getElementById('fieldMinLength').value;
            var maxLen = document.getElementById('fieldMaxLength').value;
            var regex = document.getElementById('fieldRegex').value;
            if (minLen) validationConfig.min_length = parseInt(minLen);
            if (maxLen) validationConfig.max_length = parseInt(maxLen);
            if (regex) validationConfig.regex = regex;
        } else if (fieldType === 'number') {
            var nMin = document.getElementById('fieldMin').value;
            var nMax = document.getElementById('fieldMax').value;
            if (nMin !== '') validationConfig.min = parseFloat(nMin);
            if (nMax !== '') validationConfig.max = parseFloat(nMax);
        } else if (fieldType === 'decimal') {
            var dMin = document.getElementById('fieldDecMin').value;
            var dMax = document.getElementById('fieldDecMax').value;
            var places = document.getElementById('fieldDecPlaces').value;
            if (dMin !== '') validationConfig.min = parseFloat(dMin);
            if (dMax !== '') validationConfig.max = parseFloat(dMax);
            if (places) validationConfig.decimal_places = parseInt(places);
        } else if (fieldType === 'select' || fieldType === 'multiselect') {
            var choices = [];
            document.querySelectorAll('#choicesList .cf-choice-row').forEach(function(row) {
                var val = row.querySelector('.choice-value').value.trim();
                var label = row.querySelector('.choice-label').value.trim();
                if (val && label) {
                    choices.push({ value: val, label: label });
                }
            });
            validationConfig.choices = choices;
        }

        data.validation_config = validationConfig;

        var url;
        if (fieldId) {
            url = BASE_URL + '/fields/' + fieldId + '/update/';
        } else {
            url = BASE_URL + '/fields/create/';
        }

        apiRequest(url, 'POST', data).then(function(resp) {
            if (resp.success) {
                showMessage(i18n.successSaved || 'Changes saved successfully.', 'success');
                location.reload();
            } else {
                showMessage(resp.error || i18n.errorGeneric || 'An error occurred.', 'error');
            }
        });
    });

    // Delete Field
    document.querySelectorAll('.cf-btn-delete-field').forEach(function(btn) {
        btn.addEventListener('click', async function() {
            var confirmMsg = i18n.confirmDeleteField || 'Are you sure you want to delete this field?';
            if (!await AdminModal.confirm({
                message: confirmMsg,
                danger: true,
                confirmText: 'Delete'
            })) {
                return;
            }
            var fieldId = this.dataset.fieldId;
            var fieldRow = this.closest('.field-row');
            apiRequest(BASE_URL + '/fields/' + fieldId + '/delete/', 'POST').then(function(resp) {
                if (resp.success) {
                    fieldRow.remove();
                    showMessage(i18n.successDeleted || 'Item moved to recycle bin.', 'success');
                } else {
                    showMessage(resp.error || i18n.errorGeneric || 'An error occurred.', 'error');
                }
            });
        });
    });

    // ═══════════════════════════════════════════
    // Choices Editor
    // ═══════════════════════════════════════════

    function addChoiceRow(value, label) {
        var list = document.getElementById('choicesList');
        var row = document.createElement('div');
        row.className = 'cf-choice-row';
        row.innerHTML = '<input type="text" class="choice-value" placeholder="Value" value="' + (value || '') + '">' +
            '<input type="text" class="choice-label" placeholder="Label" value="' + (label || '') + '">' +
            '<button type="button" class="cf-btn-remove-choice" title="Remove"><i class="fas fa-times"></i></button>';
        row.querySelector('.cf-btn-remove-choice').addEventListener('click', function() {
            row.remove();
        });
        list.appendChild(row);
    }

    var addChoiceBtn = document.querySelector('.cf-btn-add-choice');
    if (addChoiceBtn) {
        addChoiceBtn.addEventListener('click', function() {
            addChoiceRow('', '');
        });
    }

    // ═══════════════════════════════════════════
    // Color field sync (admin change forms)
    // ═══════════════════════════════════════════

    document.querySelectorAll('.vColorField').forEach(function(input) {
        input.addEventListener('input', function() {
            var hex = this.nextElementSibling;
            if (hex) hex.value = this.value;
        });
    });

    // Color hex display: clicking it triggers the hidden color picker input (CSP-safe delegation)
    document.addEventListener('click', function(e) {
        var hex = e.target.closest('.color-hex-display[data-action="trigger-color-picker"]');
        if (hex) {
            var prev = hex.previousElementSibling;
            if (prev) { prev.click(); }
        }
    });

    // ═══════════════════════════════════════════
    // Storefront color swatch initialization
    // ═══════════════════════════════════════════

    document.querySelectorAll('.custom-field-color[data-color]').forEach(function(el) {
        var color = el.dataset.color;
        // Only set background for valid hex colors
        if (/^#[0-9a-fA-F]{6}$/.test(color)) {
            el.style.backgroundColor = color;
        }
    });

})();
