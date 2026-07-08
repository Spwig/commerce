/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    // Read config from JSON data island
    var configEl = document.getElementById('translation-editor-init-config');
    if (!configEl) return;

    var config;
    try {
        config = JSON.parse(configEl.textContent);
    } catch (e) {
        console.error('TranslationEditor: failed to parse config', e);
        return;
    }

    var TRANS = {
        saved: config.i18n.saved,
        unsaved: config.i18n.unsaved
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeTranslationEditor);
    } else {
        initializeTranslationEditor();
    }

    function initializeTranslationEditor() {
        var modelType = config.modelType;
        var objectId = config.objectId;

        var apiEndpoints = {
            status: '/api/translation/' + modelType + '/' + objectId + '/FIELD_KEY/status/',
            translate: '/api/translation/' + modelType + '/' + objectId + '/FIELD_KEY/translate/',
            save: '/api/translation/' + modelType + '/' + objectId + '/FIELD_KEY/save/',
            saveField: '/api/translation/' + modelType + '/' + objectId + '/FIELD_KEY/save_field/'
        };

        console.log('Initializing generic translation editor with config:', config);

        document.querySelectorAll('.translate-field-btn').forEach(function (button) {
            var fieldName = button.getAttribute('data-field-name');
            var fieldInput = document.querySelector('#id_' + fieldName);
            if (!fieldInput) {
                console.warn('Field input not found for: ' + fieldName);
                return;
            }

            button.setAttribute('data-model-type', modelType);
            button.setAttribute('data-object-id', objectId);
            button.style.display = '';

            button.addEventListener('click', async function (e) {
                e.preventDefault();

                var fieldEndpoints = {
                    status: apiEndpoints.status.replace('FIELD_KEY', fieldName),
                    translate: apiEndpoints.translate.replace('FIELD_KEY', fieldName),
                    save: apiEndpoints.save.replace('FIELD_KEY', fieldName),
                    saveField: apiEndpoints.saveField.replace('FIELD_KEY', fieldName)
                };

                var currentValue = fieldInput.value.trim();
                if (!currentValue) {
                    AdminModal.alert({message: 'Please enter some text before translating.', type: 'warning'});
                    return;
                }

                button.disabled = true;
                var originalHTML = button.innerHTML;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

                try {
                    var csrfToken = AdminUtils.getCsrfToken();
                    var saveResponse = await fetch(fieldEndpoints.saveField, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                        body: JSON.stringify({ value: currentValue })
                    });
                    if (!saveResponse.ok) {
                        var errorData = await saveResponse.json();
                        throw new Error(errorData.error || 'Failed to save field value');
                    }
                    console.log('Field ' + fieldName + ' saved before translation');
                    await openTranslationEditor(fieldName, fieldInput, fieldEndpoints, config.availableLanguages);
                } catch (error) {
                    console.error('Error saving field before translation:', error);
                    AdminModal.alert({message: 'Failed to save field: ' + error.message, type: 'error'});
                } finally {
                    button.disabled = false;
                    button.innerHTML = originalHTML;
                }
            });
        });

        console.log('Generic translation editor initialized successfully');
    }

    async function openTranslationEditor(fieldName, fieldInput, endpoints, availableLanguages) {
        var translateBtn = document.querySelector('.translate-field-btn[data-field-name="' + fieldName + '"]');
        var fieldType = (translateBtn && translateBtn.getAttribute('data-field-type')) || 'text';
        var isRichText = fieldType === 'richtext';
        var ckeditorConfig = (translateBtn && translateBtn.getAttribute('data-ckeditor-config')) || 'default';
        var ckeditorEditorConfig = null;

        var currentValue;
        if (isRichText && typeof ClassicEditor !== 'undefined') {
            var editorElement = fieldInput.closest('.django-ckeditor-5');
            if (editorElement && editorElement.ckeditorInstance) {
                currentValue = editorElement.ckeditorInstance.getData().trim();
            } else {
                currentValue = fieldInput.value.trim();
            }
        } else {
            currentValue = fieldInput.value.trim();
        }

        var fieldLabel = fieldName.replace(/_/g, ' ').replace(/\b\w/g, function (l) { return l.toUpperCase(); });
        var editorInstances = {};
        var existingTranslations = {};
        var coverage = {};
        var lockedFields = {};

        try {
            var response = await fetch(endpoints.status);
            if (response.ok) {
                var data = await response.json();
                existingTranslations = data.translations || {};
                coverage = data.coverage || {};
                lockedFields = data.locked_fields || {};
            }
        } catch (error) {
            console.error('Error loading translations:', error);
        }

        var charCount = currentValue.length;
        var languageCount = availableLanguages.length;

        var modal = document.createElement('div');
        modal.className = 'utility-translation-modal';
        modal.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 10000;';

        var modalContent = document.createElement('div');
        modalContent.className = 'utility-popup large utility-translation-editor';
        modalContent.style.cssText = 'background: var(--body-bg); color: var(--body-fg); border-radius: 8px; max-width: 800px; max-height: 90vh; overflow: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.2);';

        var header = document.createElement('div');
        header.className = 'utility-header';
        header.style.cssText = 'padding: 20px; border-bottom: 1px solid var(--hairline-color); display: flex; justify-content: space-between; align-items: center;';
        header.innerHTML =
            '<h3 class="utility-title" style="margin: 0; color: var(--body-fg);"><i class="fas fa-globe"></i> Manage Translations - ' + fieldLabel + '</h3>' +
            '<button type="button" class="utility-close" style="background: none; border: none; font-size: 24px; cursor: pointer; padding: 0; width: 30px; height: 30px; color: var(--body-fg);"><i class="fas fa-times"></i></button>';

        var body = document.createElement('div');
        body.className = 'utility-body';
        body.style.cssText = 'padding: 20px;';

        body.innerHTML =
            '<div class="utility-translation-analysis" style="background: var(--darkened-bg); padding: 12px; border-radius: 4px; margin-bottom: 20px;">' +
            '<div style="display: flex; gap: 20px; margin-bottom: 8px;">' +
            '<div class="utility-analysis-item"><span class="utility-analysis-label" style="color: var(--body-quiet-color);">Content Size:</span> <span class="utility-analysis-value" style="color: var(--body-fg); font-weight: bold;">' + charCount + ' characters</span></div>' +
            '<div class="utility-analysis-item"><span class="utility-analysis-label" style="color: var(--body-quiet-color);">Languages:</span> <span class="utility-analysis-value" style="color: var(--body-fg); font-weight: bold;">' + languageCount + ' available</span></div>' +
            '<div class="utility-analysis-item"><span class="utility-analysis-label" style="color: var(--body-quiet-color);">Coverage:</span> <span class="utility-analysis-value" style="color: var(--body-fg); font-weight: bold;">' + (coverage.percentage || 0) + '%</span></div>' +
            '</div>' +
            '<div class="utility-analysis-recommendation" id="recommendation" style="color: var(--body-quiet-color); font-size: 0.9em;"></div>' +
            '</div>' +
            '<div style="margin-bottom: 20px;">' +
            '<label style="font-weight: bold; display: block; margin-bottom: 8px; color: var(--body-fg);">Source Text ' + (isRichText ? '(Preview)' : '') + ':</label>' +
            '<div id="source-text-display" style="padding: 12px; background: var(--darkened-bg); border-radius: 4px; color: var(--body-fg); max-height: 200px; overflow-y: auto;"></div>' +
            '</div>' +
            '<div style="margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">' +
            '<label style="font-weight: bold; color: var(--body-fg);">Target Languages:</label>' +
            '<div style="display: flex; gap: 8px;">' +
            '<button type="button" class="btn-select-all" style="padding: 4px 12px; font-size: 0.85em; border: 1px solid var(--hairline-color); background: var(--body-bg); color: var(--body-fg); cursor: pointer; border-radius: 4px;"><i class="fas fa-check-double"></i> Select All</button>' +
            '<button type="button" class="btn-select-none" style="padding: 4px 12px; font-size: 0.85em; border: 1px solid var(--hairline-color); background: var(--body-bg); color: var(--body-fg); cursor: pointer; border-radius: 4px;"><i class="fas fa-times"></i> Deselect All</button>' +
            '</div></div>' +
            '<div class="utility-language-list" style="display: flex; flex-direction: column; gap: 12px; max-height: 300px; overflow-y: auto;"></div>';

        var languagesList = body.querySelector('.utility-language-list');
        var lockEndpoint = config.lockEndpoint;

        availableLanguages.forEach(function (lang) {
            var langItem = document.createElement('div');
            langItem.className = 'utility-language-item';
            langItem.dataset.lang = lang.code;
            var existingTranslation = existingTranslations[lang.code] || '';
            var isTranslated = !!existingTranslation;
            var langLockedFields = lockedFields[lang.code] || [];
            var isLocked = langLockedFields.includes(fieldName);

            langItem.style.cssText = 'display: flex; flex-direction: column; gap: 8px; padding: 12px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--darkened-bg);' +
                (isLocked ? 'border-left: 3px solid #c62828; opacity: 0.8;' : (isTranslated ? 'border-left: 3px solid var(--info-color);' : ''));

            var escapedTranslation = existingTranslation.replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            var lockBtnStyle = 'background: ' + (isLocked ? '#fce4ec' : 'none') + '; border: 1px solid ' + (isLocked ? '#c62828' : 'var(--hairline-color)') + '; border-radius: 4px; cursor: pointer; color: ' + (isLocked ? '#c62828' : 'var(--body-quiet-color)') + '; padding: 4px 8px; font-size: 0.85em; transition: all 0.15s;';
            var checkboxAttrs = isLocked ? 'disabled' : (isTranslated ? '' : 'checked');
            var translationStatus = isLocked
                ? '<span style="color: #c62828; margin-left: 8px;"><i class="fas fa-lock"></i> Locked</span>'
                : (isTranslated
                    ? '<span style="color: var(--info-color); margin-left: 8px;"><i class="fas fa-check-circle"></i> Translated</span>'
                    : '<span style="color: var(--body-quiet-color); margin-left: 8px;">Not translated</span>');
            var savedBadge = (isTranslated && !isLocked)
                ? '<span class="translation-status-badge" data-lang="' + lang.code + '" style="padding: 2px 8px; border-radius: 3px; font-size: 0.75em; font-weight: bold; background: var(--success-bg, #d4edda); color: var(--success-color, #28a745); border: 1px solid var(--success-color, #28a745);">' + TRANS.saved + '</span>'
                : '';
            var editField = '';
            if (isTranslated && !isLocked) {
                if (isRichText) {
                    editField = '<div class="translation-edit-field-richtext" data-lang="' + lang.code + '" data-original-value="' + escapedTranslation + '" id="editor_' + lang.code + '" style="width: 100%;"></div>';
                } else {
                    editField = '<textarea class="translation-edit-field" data-lang="' + lang.code + '" data-original-value="' + escapedTranslation + '" placeholder="Edit ' + lang.name + ' translation..." style="width: 100%; padding: 8px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--body-bg); color: var(--body-fg); font-family: inherit; font-size: 0.9em; min-height: 60px; resize: vertical;">' + escapedTranslation + '</textarea>';
                }
            } else if (isLocked && isTranslated) {
                editField = '<div style="padding: 8px; background: var(--darkened-bg); border: 1px solid var(--hairline-color); border-radius: 4px; font-size: 0.9em; color: var(--body-quiet-color); opacity: 0.7;">' + escapedTranslation.substring(0, 200) + (escapedTranslation.length > 200 ? '...' : '') + '</div>';
            }

            langItem.innerHTML =
                '<div style="display: flex; align-items: center; gap: 12px;">' +
                '<input type="checkbox" id="lang_' + lang.code + '" value="' + lang.code + '" ' + checkboxAttrs + ' style="width: 18px; height: 18px; flex-shrink: 0;">' +
                '<label for="lang_' + lang.code + '" style="flex: 1; margin: 0; color: var(--body-fg);"><strong>' + lang.name + '</strong>' + translationStatus + '</label>' +
                '<button type="button" class="translation-lock-btn" data-lang="' + lang.code + '" data-locked="' + isLocked + '" title="' + (isLocked ? 'Unlock translation' : 'Lock translation') + '" style="' + lockBtnStyle + '"><i class="fas ' + (isLocked ? 'fa-lock' : 'fa-lock-open') + '"></i></button>' +
                savedBadge + '</div>' + editField;

            languagesList.appendChild(langItem);
        });

        languagesList.querySelectorAll('.translation-lock-btn').forEach(function (btn) {
            btn.addEventListener('click', async function (e) {
                e.preventDefault();
                var langCode = btn.dataset.lang;
                btn.disabled = true;
                var icon = btn.querySelector('i');
                icon.className = 'fas fa-spinner fa-spin';
                try {
                    var csrfToken = AdminUtils.getCsrfToken();
                    var resp = await fetch(lockEndpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
                        body: JSON.stringify({ content_type: config.modelType, object_id: config.objectId, field_name: fieldName, language: langCode })
                    });
                    var data = await resp.json();
                    if (data.success) { modal.remove(); openTranslationEditor(fieldName, fieldInput, endpoints, availableLanguages); }
                } catch (err) {
                    console.error('Lock toggle failed:', err);
                    icon.className = btn.dataset.locked === 'true' ? 'fas fa-lock' : 'fas fa-lock-open';
                } finally { btn.disabled = false; }
            });
        });

        var footer = document.createElement('div');
        footer.className = 'utility-footer';
        footer.style.cssText = 'padding: 20px; border-top: 1px solid var(--hairline-color); display: flex; justify-content: space-between; align-items: center; gap: 12px;';
        footer.innerHTML =
            '<div style="color: var(--body-quiet-color); font-size: 0.9em;"><i class="fas fa-info-circle"></i> Edit existing translations or select languages to translate</div>' +
            '<div style="display: flex; gap: 12px;">' +
            '<button type="button" class="btn btn-cancel" style="padding: 8px 16px; border: 1px solid var(--hairline-color); background: var(--body-bg); color: var(--body-fg); cursor: pointer; border-radius: 4px;">Cancel</button>' +
            '<button type="button" class="btn btn-save" style="padding: 8px 16px; border: 1px solid var(--hairline-color); background: var(--body-bg); color: var(--body-fg); cursor: pointer; border-radius: 4px;"><i class="fas fa-save"></i> Save Edits</button>' +
            '<button type="button" class="btn btn-apply" style="padding: 8px 16px; border: none; background: var(--button-bg); color: var(--button-fg); cursor: pointer; border-radius: 4px;"><i class="fas fa-language"></i> Translate</button>' +
            '</div>';

        modalContent.appendChild(header);
        modalContent.appendChild(body);
        modalContent.appendChild(footer);
        modal.appendChild(modalContent);
        document.body.appendChild(modal);

        var sourceTextDisplay = body.querySelector('#source-text-display');
        if (isRichText) { sourceTextDisplay.innerHTML = currentValue; }
        else { sourceTextDisplay.textContent = currentValue; }

        if (isRichText && typeof ClassicEditor !== 'undefined') {
            var baseConfig = (window.django_ckeditor_5_configs &&
                (window.django_ckeditor_5_configs[ckeditorConfig] || window.django_ckeditor_5_configs['default'])) || {};
            ckeditorEditorConfig = Object.assign({}, baseConfig, { licenseKey: 'GPL' });

            availableLanguages.forEach(function (lang) {
                var existingTranslation = existingTranslations[lang.code] || '';
                if (existingTranslation) {
                    var editorEl = document.getElementById('editor_' + lang.code);
                    if (editorEl) {
                        ClassicEditor.create(editorEl, ckeditorEditorConfig)
                            .then(function (editor) {
                                editorInstances[lang.code] = editor;
                                var unescapedContent = existingTranslation
                                    .replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
                                editor.setData(unescapedContent);
                                editor.originalValue = unescapedContent;
                                editor.model.document.on('change:data', function () {
                                    var currentData = editor.getData();
                                    var badge = languagesList.querySelector('.translation-status-badge[data-lang="' + lang.code + '"]');
                                    if (badge) {
                                        if (currentData !== editor.originalValue) {
                                            badge.style.background = 'var(--warning-bg, #fff3cd)'; badge.style.color = 'var(--warning-color, #856404)'; badge.style.borderColor = 'var(--warning-color, #856404)'; badge.innerHTML = TRANS.unsaved;
                                        } else {
                                            badge.style.background = 'var(--success-bg, #d4edda)'; badge.style.color = 'var(--success-color, #28a745)'; badge.style.borderColor = 'var(--success-color, #28a745)'; badge.innerHTML = TRANS.saved;
                                        }
                                        updateSaveButtonState();
                                    }
                                });
                            })
                            .catch(function (error) {
                                console.error('Error initializing CKEditor for ' + lang.code + ':', error);
                                editorEl.outerHTML = '<textarea class="translation-edit-field" data-lang="' + lang.code + '" data-original-value="' + existingTranslation + '" style="width: 100%; padding: 8px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--body-bg); color: var(--body-fg); font-family: inherit; font-size: 0.9em; min-height: 100px; resize: vertical;">' + existingTranslation + '</textarea>';
                            });
                    }
                }
            });
        }

        var closeBtn = header.querySelector('.utility-close');
        var cancelBtn = footer.querySelector('.btn-cancel');
        var saveBtn = footer.querySelector('.btn-save');
        var applyBtn = footer.querySelector('.btn-apply');
        var recommendationEl = body.querySelector('#recommendation');
        var selectAllBtn = body.querySelector('.btn-select-all');
        var selectNoneBtn = body.querySelector('.btn-select-none');
        var translationsModified = false;

        function closeModal() {
            Object.values(editorInstances).forEach(function (editor) {
                if (editor && typeof editor.destroy === 'function') {
                    editor.destroy().catch(function (err) { console.error('Error destroying editor:', err); });
                }
            });
            modal.remove();
            if (translationsModified) { window.location.reload(); }
        }

        function setupChangeTracking() {
            languagesList.querySelectorAll('.translation-edit-field').forEach(function (textarea) {
                textarea.addEventListener('input', function () {
                    var lang = this.getAttribute('data-lang');
                    var originalValue = this.getAttribute('data-original-value');
                    var badge = languagesList.querySelector('.translation-status-badge[data-lang="' + lang + '"]');
                    if (badge) {
                        if (this.value !== originalValue) {
                            badge.style.background = 'var(--warning-bg, #fff3cd)'; badge.style.color = 'var(--warning-color, #856404)'; badge.style.borderColor = 'var(--warning-color, #856404)'; badge.innerHTML = TRANS.unsaved;
                        } else {
                            badge.style.background = 'var(--success-bg, #d4edda)'; badge.style.color = 'var(--success-color, #28a745)'; badge.style.borderColor = 'var(--success-color, #28a745)'; badge.innerHTML = TRANS.saved;
                        }
                    }
                    updateSaveButtonState();
                });
            });
        }

        function updateSaveButtonState() {
            var hasUnsaved = Array.from(languagesList.querySelectorAll('.translation-edit-field')).some(function (t) {
                return t.value !== t.getAttribute('data-original-value');
            });
            if (!hasUnsaved && isRichText) {
                hasUnsaved = Object.values(editorInstances).some(function (editor) {
                    return editor && editor.originalValue !== undefined && editor.getData() !== editor.originalValue;
                });
            }
            saveBtn.disabled = !hasUnsaved;
            saveBtn.style.opacity = hasUnsaved ? '1' : '0.6';
        }

        setupChangeTracking();
        updateSaveButtonState();
        closeBtn.addEventListener('click', closeModal);
        cancelBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
        selectAllBtn.addEventListener('click', function () { languagesList.querySelectorAll('input[type="checkbox"]').forEach(function (cb) { cb.checked = true; }); });
        selectNoneBtn.addEventListener('click', function () { languagesList.querySelectorAll('input[type="checkbox"]').forEach(function (cb) { cb.checked = false; }); });

        saveBtn.addEventListener('click', async function () {
            var editedTranslations = {};
            var hasEdits = false;
            languagesList.querySelectorAll('.translation-edit-field').forEach(function (textarea) {
                var lang = textarea.getAttribute('data-lang');
                var newValue = textarea.value.trim();
                if (newValue && newValue !== (existingTranslations[lang] || '')) { editedTranslations[lang] = newValue; hasEdits = true; }
            });
            if (isRichText) {
                Object.entries(editorInstances).forEach(function (entry) {
                    var lang = entry[0], editor = entry[1];
                    if (editor && editor.originalValue !== undefined) {
                        var newValue = editor.getData().trim();
                        if (newValue && newValue !== (editor.originalValue || '')) { editedTranslations[lang] = newValue; hasEdits = true; }
                    }
                });
            }
            if (!hasEdits) { AdminModal.alert('No changes to save.'); return; }
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
            try {
                var csrfToken = AdminUtils.getCsrfToken();
                var response = await fetch(endpoints.save, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken }, body: JSON.stringify({ translations: editedTranslations }) });
                if (!response.ok) { var errorData = await response.json(); throw new Error(errorData.error || 'Save failed'); }
                var result = await response.json();
                if (result.success) {
                    translationsModified = true;
                    recommendationEl.innerHTML = '<div style="padding: 12px; background: var(--success-bg, #d4edda); border-left: 3px solid var(--success-color, #28a745); color: var(--body-fg); border-radius: 4px;"><strong><i class="fas fa-check-circle"></i> Edits Saved!</strong><br>Successfully saved ' + result.saved_languages.length + ' translation(s).</div>';
                    result.saved_languages.forEach(function (lang) {
                        var badge = languagesList.querySelector('.translation-status-badge[data-lang="' + lang + '"]');
                        var textarea = languagesList.querySelector('.translation-edit-field[data-lang="' + lang + '"]');
                        if (badge) { badge.style.background = 'var(--success-bg, #d4edda)'; badge.style.color = 'var(--success-color, #28a745)'; badge.style.borderColor = 'var(--success-color, #28a745)'; badge.innerHTML = TRANS.saved; }
                        if (textarea) { textarea.setAttribute('data-original-value', textarea.value.replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;')); existingTranslations[lang] = textarea.value; }
                        if (isRichText && editorInstances[lang]) { var currentData = editorInstances[lang].getData(); editorInstances[lang].originalValue = currentData; existingTranslations[lang] = currentData; }
                    });
                    saveBtn.disabled = false;
                    saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Edits';
                    updateSaveButtonState();
                } else { throw new Error(result.message || 'Save failed'); }
            } catch (error) {
                console.error('Save error:', error);
                AdminModal.alert({message: 'Save failed: ' + error.message, type: 'error'});
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Edits';
            }
        });

        applyBtn.addEventListener('click', async function () {
            var selectedLanguages = [];
            languagesList.querySelectorAll('input[type="checkbox"]:checked').forEach(function (cb) { selectedLanguages.push(cb.value); });
            if (selectedLanguages.length === 0) { AdminModal.alert({message: 'Please select at least one language to translate to.', type: 'warning'}); return; }
            var forceImmediate = applyBtn.dataset.forceImmediate === 'true';
            applyBtn.disabled = true;
            applyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Translating...';
            recommendationEl.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing translation...';
            try {
                var csrfToken = AdminUtils.getCsrfToken();
                var response = await fetch(endpoints.translate, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken }, body: JSON.stringify({ text: currentValue, languages: selectedLanguages, force_immediate: forceImmediate }) });
                var result = await response.json();

                if (response.status === 202 && result.recommend_schedule) {
                    recommendationEl.innerHTML = '<div style="padding: 12px; background: var(--blue-subtle); border-left: 3px solid var(--blue-accent); color: var(--body-fg); border-radius: 4px;"><strong><i class="fas fa-clock"></i> Heavy Workload Detected</strong><br>' + result.reason + '<br><em>Estimated time: ' + result.estimated_time + '</em><div style="display: flex; gap: 8px; margin-top: 8px;"><button data-action="translate-anyway" style="padding: 6px 12px; background: var(--button-bg); color: var(--button-fg); border: none; border-radius: 4px; cursor: pointer;"><i class="fas fa-bolt"></i> Translate Anyway</button><button data-action="schedule-translation" style="padding: 6px 12px; background: var(--primary); color: #fff; border: none; border-radius: 4px; cursor: pointer;"><i class="fas fa-calendar-plus"></i> Schedule for Later</button></div></div>';
                    recommendationEl.querySelector('[data-action="translate-anyway"]').addEventListener('click', function () { var m = this.closest('.utility-translation-modal'); if (m) m.querySelector('.btn-apply').click(); });
                    var schedBtn = recommendationEl.querySelector('[data-action="schedule-translation"]');
                    if (schedBtn) {
                        schedBtn.addEventListener('click', async function () {
                            schedBtn.disabled = true;
                            schedBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scheduling...';
                            try {
                                var csrfToken = AdminUtils.getCsrfToken();
                                var schedResponse = await fetch(endpoints.translate, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken }, body: JSON.stringify({ text: currentValue, languages: selectedLanguages, schedule: true }) });
                                var schedResult = await schedResponse.json();
                                if (schedResult.success && schedResult.scheduled) {
                                    recommendationEl.innerHTML = '<div style="padding: 12px; background: var(--success-bg, #d4edda); border-left: 3px solid var(--success-color, #28a745); color: var(--body-fg); border-radius: 4px;"><strong><i class="fas fa-check-circle"></i> Translations Scheduled</strong><br>' + schedResult.job_count + ' translation job(s) queued for background processing. Translations will appear automatically once completed.</div>';
                                    applyBtn.disabled = false; applyBtn.innerHTML = '<i class="fas fa-language"></i> Translate'; applyBtn.dataset.forceImmediate = 'false';
                                } else { throw new Error(schedResult.error || 'Scheduling failed'); }
                            } catch (err) {
                                console.error('Schedule error:', err);
                                recommendationEl.innerHTML += '<div style="padding: 8px; background: var(--error-bg, #f8d7da); color: var(--error-fg, #842029); border-radius: 4px; margin-top: 8px;">Scheduling failed: ' + err.message + '</div>';
                                schedBtn.disabled = false; schedBtn.innerHTML = '<i class="fas fa-calendar-plus"></i> Schedule for Later';
                            }
                        });
                    }
                    applyBtn.disabled = false; applyBtn.innerHTML = '<i class="fas fa-language"></i> Translate'; applyBtn.dataset.forceImmediate = 'true';
                    return;
                }

                if (!response.ok) { throw new Error(result.error || 'Translation failed'); }

                if (result.success) {
                    translationsModified = true;
                    if (result.warnings && result.warnings.length > 0) { console.warn('Translation warnings:', result.warnings); }
                    recommendationEl.innerHTML = '<div style="padding: 12px; background: var(--success-bg, #d4edda); border-left: 3px solid var(--success-color, #28a745); color: var(--body-fg); border-radius: 4px;"><strong><i class="fas fa-check-circle"></i> Translation Complete!</strong><br>Successfully translated to ' + result.successful_languages.length + ' language(s).</div>';
                    languagesList.innerHTML = '';
                    var allTranslations = Object.assign({}, existingTranslations, result.translations);

                    availableLanguages.forEach(function (lang) {
                        var langItem = document.createElement('div');
                        langItem.className = 'utility-language-item';
                        var translation = allTranslations[lang.code] || '';
                        var isTranslated = !!translation;
                        langItem.style.cssText = 'display: flex; flex-direction: column; gap: 8px; padding: 12px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--darkened-bg);' + (isTranslated ? 'border-left: 3px solid var(--info-color);' : '');
                        var escapedTranslation = translation.replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                        var isNew = result.successful_languages.includes(lang.code);
                        var savedBadge2 = isTranslated ? '<span class="translation-status-badge" data-lang="' + lang.code + '" style="padding: 2px 8px; border-radius: 3px; font-size: 0.75em; font-weight: bold; background: var(--success-bg, #d4edda); color: var(--success-color, #28a745); border: 1px solid var(--success-color, #28a745);">' + TRANS.saved + '</span>' : '';
                        var editField2 = '';
                        if (isTranslated) {
                            if (isRichText) { editField2 = '<div class="translation-edit-field-richtext" data-lang="' + lang.code + '" data-original-value="' + escapedTranslation + '" id="editor_new_' + lang.code + '" style="width: 100%;"></div>'; }
                            else { editField2 = '<textarea class="translation-edit-field" data-lang="' + lang.code + '" data-original-value="' + escapedTranslation + '" placeholder="Edit ' + lang.name + ' translation..." style="width: 100%; padding: 8px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--body-bg); color: var(--body-fg); font-family: inherit; font-size: 0.9em; min-height: 60px; resize: vertical;">' + escapedTranslation + '</textarea>'; }
                        }
                        langItem.innerHTML = '<div style="display: flex; align-items: center; gap: 12px;"><input type="checkbox" id="lang_' + lang.code + '" value="' + lang.code + '" ' + (isTranslated ? '' : 'checked') + ' style="width: 18px; height: 18px; flex-shrink: 0;"><label for="lang_' + lang.code + '" style="flex: 1; margin: 0; color: var(--body-fg);"><strong>' + lang.name + '</strong>' + (isTranslated ? '<span style="color: var(--info-color); margin-left: 8px;"><i class="fas fa-check-circle"></i> Translated' + (isNew ? ' (New)' : '') + '</span>' : '<span style="color: var(--body-quiet-color); margin-left: 8px;">Not translated</span>') + '</label>' + savedBadge2 + '</div>' + editField2;
                        languagesList.appendChild(langItem);
                    });

                    existingTranslations = allTranslations;
                    var translatedCount = Object.keys(allTranslations).length;
                    var totalCount = availableLanguages.length;
                    var analysisItems = body.querySelectorAll('.utility-analysis-item');
                    if (analysisItems.length >= 3) { var coverageEl = analysisItems[2].querySelector('.utility-analysis-value'); if (coverageEl) coverageEl.textContent = (translatedCount / totalCount * 100).toFixed(1) + '%'; }
                    applyBtn.disabled = false; applyBtn.innerHTML = '<i class="fas fa-language"></i> Translate'; applyBtn.dataset.forceImmediate = 'false';

                    if (isRichText && typeof ClassicEditor !== 'undefined' && ckeditorEditorConfig) {
                        availableLanguages.forEach(function (lang) {
                            var translation = allTranslations[lang.code];
                            if (translation) {
                                var editorEl = document.getElementById('editor_new_' + lang.code);
                                if (editorEl && !editorInstances[lang.code]) {
                                    ClassicEditor.create(editorEl, ckeditorEditorConfig)
                                        .then(function (editor) {
                                            editorInstances[lang.code] = editor;
                                            var unescapedContent = translation.replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>');
                                            editor.setData(unescapedContent);
                                            editor.originalValue = unescapedContent;
                                            editor.model.document.on('change:data', function () {
                                                var currentData = editor.getData();
                                                var badge = languagesList.querySelector('.translation-status-badge[data-lang="' + lang.code + '"]');
                                                if (badge) {
                                                    if (currentData !== editor.originalValue) { badge.innerHTML = TRANS.unsaved; badge.style.background = 'var(--warning-bg, #fff3cd)'; badge.style.color = 'var(--warning-color, #856404)'; badge.style.borderColor = 'var(--warning-color, #856404)'; }
                                                    else { badge.innerHTML = TRANS.saved; badge.style.background = 'var(--success-bg, #d4edda)'; badge.style.color = 'var(--success-color, #28a745)'; badge.style.borderColor = 'var(--success-color, #28a745)'; }
                                                    updateSaveButtonState();
                                                }
                                            });
                                        })
                                        .catch(function (error) { console.error('Error initializing CKEditor for ' + lang.code + ':', error); });
                                }
                            }
                        });
                    }

                    setupChangeTracking();
                    updateSaveButtonState();
                    console.log('Translation results displayed, modal kept open for review');
                } else { throw new Error(result.message || 'Translation failed'); }
            } catch (error) {
                console.error('Translation error:', error);
                recommendationEl.innerHTML = '<div style="color: var(--error-color);"><i class="fas fa-exclamation-triangle"></i> ' + error.message + '</div>';
                AdminModal.alert({message: 'Translation failed: ' + error.message, type: 'error'});
                applyBtn.disabled = false;
                applyBtn.innerHTML = '<i class="fas fa-language"></i> Translate';
            }
        });
    }

    function showAdminMessage(message, type) {
        var messageDiv = document.createElement('div');
        messageDiv.className = 'messagelist';
        messageDiv.innerHTML = '<div class="' + type + '">' + message + '</div>';
        messageDiv.style.cssText = 'margin: 20px; animation: fadeIn 0.3s;';
        var contentDiv = document.querySelector('.content') || document.querySelector('main');
        if (contentDiv) {
            contentDiv.insertBefore(messageDiv, contentDiv.firstChild);
            setTimeout(function () {
                messageDiv.style.opacity = '0';
                messageDiv.style.transition = 'opacity 0.5s';
                setTimeout(function () { messageDiv.remove(); }, 500);
            }, 3000);
        }
    }
}());
