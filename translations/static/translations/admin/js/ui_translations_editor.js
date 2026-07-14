/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

'use strict';

/**
 * UI Translations Editor
 *
 * Handles loading, editing, saving, and auto-translating
 * merchant UI string overrides.
 */
var UITransEditor = {
  currentLang: null,
  data: null,
  dirty: {}, // {string_key: new_value}
  filter: 'all',
  sectionFilter: 'all',

  selectLanguage: function (langCode, tabEl) {
    // Update tab UI
    document.querySelectorAll('.ui-trans-tab').forEach(function (t) {
      t.classList.remove('ui-trans-tab--active');
    });
    if (tabEl) tabEl.classList.add('ui-trans-tab--active');

    this.currentLang = langCode;
    this.dirty = {};
    this.updateSaveBtn();
    this.loadStrings(langCode);
  },

  loadStrings: function (langCode) {
    const container = document.getElementById('strings-container');
    container.innerHTML =
      '<div class="ui-trans-loading"><i class="fas fa-spinner fa-spin"></i><p>Loading translations...</p></div>';

    fetch('/api/translations/service/ui-translations/' + langCode + '/')
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.success) {
          UITransEditor.data = data;
          UITransEditor.renderStrings(data);
          UITransEditor.updateProgress(data.translated_count, data.total_strings);
        } else {
          container.innerHTML =
            '<div class="ui-trans-loading"><i class="fas fa-exclamation-triangle"></i><p>' +
            (data.error || 'Failed to load') +
            '</p></div>';
        }
      })
      .catch(function (err) {
        container.innerHTML =
          '<div class="ui-trans-loading"><i class="fas fa-exclamation-triangle"></i><p>Failed to load translations</p></div>';
        console.error(err);
      });
  },

  renderStrings: function (data) {
    const container = document.getElementById('strings-container');
    let html = '';
    const sections = data.sections;

    for (const sectionKey in sections) {
      const section = sections[sectionKey];
      const strings = section.strings;
      const count = Object.keys(strings).length;
      let translated = 0;
      for (const k in strings) {
        if (strings[k].translation) translated++;
      }

      html += '<div class="ui-trans-section" data-section="' + sectionKey + '">';
      html += '<div class="ui-trans-section__header" onclick="UITransEditor.toggleSection(this)">';
      html += '<div class="ui-trans-section__title">' + this.esc(section.label);
      html +=
        ' <span class="ui-trans-section__count">' + translated + '/' + count + '</span></div>';
      html += '<i class="fas fa-chevron-down ui-trans-section__toggle"></i>';
      html += '</div>';
      html += '<div class="ui-trans-section__body">';

      for (const stringKey in strings) {
        const entry = strings[stringKey];
        const meta = entry.meta || {};
        const isEmpty = !entry.translation;
        const isLocked = !!meta.locked;

        let badge = '';
        if (isLocked) {
          badge =
            '<span class="ui-trans-badge ui-trans-badge--locked"><i class="fas fa-lock"></i> Locked</span>';
        } else if (isEmpty) {
          badge = '<span class="ui-trans-badge ui-trans-badge--missing">Missing</span>';
        } else if (entry.source === 'shipped') {
          badge =
            '<span class="ui-trans-badge ui-trans-badge--shipped"><i class="fas fa-box"></i> Shipped</span>';
        } else if (meta.verified) {
          badge = '<span class="ui-trans-badge ui-trans-badge--verified">Verified</span>';
        } else if (meta.auto) {
          badge = '<span class="ui-trans-badge ui-trans-badge--auto">Auto</span>';
        }

        html +=
          '<div class="ui-trans-row' +
          (isLocked ? ' ui-trans-row--locked' : '') +
          '" data-key="' +
          stringKey +
          '"';
        html += ' data-has-translation="' + !isEmpty + '"';
        html += ' data-is-auto="' + !!meta.auto + '"';
        html += ' data-is-verified="' + !!meta.verified + '"';
        html += ' data-is-locked="' + isLocked + '"';
        html += ' data-source="' + (entry.source || '') + '">';

        html += '<div class="ui-trans-row__source">';
        html += this.esc(entry.english);
        html += '<code>' + this.esc(stringKey) + '</code>';
        html += '</div>';

        html +=
          '<textarea class="ui-trans-row__input' +
          (isEmpty ? ' ui-trans-row__input--empty' : '') +
          '"';
        html += ' data-key="' + stringKey + '"';
        html += ' oninput="UITransEditor.onInput(this)"';
        if (isLocked) html += ' readonly';
        html += ' rows="1">' + this.esc(entry.translation || '') + '</textarea>';

        html += '<div class="ui-trans-row__actions">';
        html +=
          '<button type="button" class="ui-trans-row__lock' +
          (isLocked ? ' ui-trans-row__lock--active' : '') +
          '" data-key="' +
          stringKey +
          '"';
        html +=
          ' onclick="UITransEditor.toggleLock(this)" title="' +
          (isLocked ? 'Unlock translation' : 'Lock translation') +
          '">';
        html += '<i class="fas ' + (isLocked ? 'fa-lock' : 'fa-lock-open') + '"></i></button>';
        html +=
          '<button type="button" class="ui-trans-row__translate" data-key="' + stringKey + '"';
        html += ' onclick="UITransEditor.translateString(this)" title="AI Translate"';
        if (isLocked) html += ' disabled';
        html += '>';
        html += '<i class="fas fa-language"></i></button>';
        html += '</div>';

        html += '<div class="ui-trans-row__status">' + badge + '</div>';
        html += '</div>';
      }

      html += '</div></div>';
    }

    container.innerHTML = html;
    this.applyFilter(this.filter);
    this.filterSection(this.sectionFilter);
  },

  toggleSection: function (headerEl) {
    const section = headerEl.closest('.ui-trans-section');
    section.classList.toggle('ui-trans-section--collapsed');
  },

  onInput: function (textarea) {
    const key = textarea.dataset.key;
    this.dirty[key] = textarea.value;
    this.updateSaveBtn();

    // Update empty styling
    if (textarea.value.trim()) {
      textarea.classList.remove('ui-trans-row__input--empty');
    } else {
      textarea.classList.add('ui-trans-row__input--empty');
    }
  },

  updateSaveBtn: function () {
    const btn = document.getElementById('save-btn');
    if (btn) {
      btn.disabled = Object.keys(this.dirty).length === 0;
    }
  },

  updateProgress: function (translated, total) {
    const pct = total > 0 ? Math.round((translated / total) * 100) : 0;
    const fill = document.getElementById('progress-fill');
    const text = document.getElementById('progress-text');
    if (fill) fill.style.width = pct + '%';
    if (text) text.textContent = translated + ' / ' + total;
  },

  applyFilter: function (filter) {
    this.filter = filter;
    document.querySelectorAll('.ui-trans-row').forEach(function (row) {
      let show = true;
      if (filter === 'untranslated') {
        show = row.dataset.hasTranslation === 'false';
      } else if (filter === 'shipped') {
        show = row.dataset.source === 'shipped';
      } else if (filter === 'auto') {
        show = row.dataset.isAuto === 'true';
      } else if (filter === 'verified') {
        show = row.dataset.isVerified === 'true';
      } else if (filter === 'locked') {
        show = row.dataset.isLocked === 'true';
      }
      row.classList.toggle('ui-trans-row--hidden', !show);
    });
  },

  filterSection: function (section) {
    this.sectionFilter = section;
    document.querySelectorAll('.ui-trans-section').forEach(function (el) {
      if (section === 'all') {
        el.style.display = '';
      } else {
        el.style.display = el.dataset.section === section ? '' : 'none';
      }
    });
  },

  saveAll: function () {
    if (!this.currentLang || Object.keys(this.dirty).length === 0) return;

    const btn = document.getElementById('save-btn');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    }

    fetch('/api/translations/service/ui-translations/' + this.currentLang + '/save/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
      },
      body: JSON.stringify({ translations: this.dirty }),
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.success) {
          UITransEditor.dirty = {};
          UITransEditor.showToast(data.message || 'Saved', 'success');
          UITransEditor.updateProgress(data.translated_count, data.total_strings);
          // Update tab badge
          const tab = document.querySelector(
            '.ui-trans-tab[data-lang="' + UITransEditor.currentLang + '"]'
          );
          if (tab) {
            const pct =
              data.total_strings > 0
                ? Math.round((data.translated_count / data.total_strings) * 100)
                : 0;
            const badge = tab.querySelector('.ui-trans-tab__badge');
            if (badge) {
              badge.textContent = pct + '%';
              badge.className = 'ui-trans-tab__badge';
              if (pct >= 100) badge.classList.add('ui-trans-tab__badge--complete');
              else if (pct > 0) badge.classList.add('ui-trans-tab__badge--partial');
            }
          }
        } else {
          UITransEditor.showToast(data.error || 'Save failed', 'error');
        }
      })
      .catch(function (err) {
        UITransEditor.showToast('Save failed: ' + err.message, 'error');
      })
      .finally(function () {
        if (btn) {
          btn.innerHTML = '<i class="fas fa-save"></i> Save changes';
          UITransEditor.updateSaveBtn();
        }
      });
  },

  autoTranslate: function () {
    if (!this.currentLang) return;

    this.showToast('Auto-translation started...', 'info');

    fetch('/api/translations/service/ui-translations/' + this.currentLang + '/auto-translate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
      },
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.success) {
          UITransEditor.showToast(data.message || 'Auto-translation queued', 'success');
          // Reload after a short delay to show results
          setTimeout(function () {
            UITransEditor.loadStrings(UITransEditor.currentLang);
          }, 3000);
        } else {
          UITransEditor.showToast(data.error || 'Auto-translate failed', 'error');
        }
      })
      .catch(function (err) {
        UITransEditor.showToast('Failed: ' + err.message, 'error');
      });
  },

  showToast: function (message, type) {
    AdminModal.toast(message, type || 'info');
  },

  esc: function (text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
  },

  // === Export / Import ===

  _importFile: null,

  exportPack: function () {
    if (!this.currentLang) {
      this.showToast('Please select a language first', 'error');
      return;
    }
    window.location.href =
      '/api/translations/service/ui-translations/' + this.currentLang + '/export/';
  },

  showImportModal: function () {
    if (!this.currentLang) {
      this.showToast('Please select a language first', 'error');
      return;
    }
    this._importFile = null;
    document.getElementById('import-modal').classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
    document.getElementById('import-dropzone').hidden = false;
    document.getElementById('import-preview').hidden = true;
    document.getElementById('import-footer').hidden = true;
    const fileInput = document.getElementById('import-file-input');
    if (fileInput) fileInput.value = '';
    this._setupDropzone();
  },

  closeImportModal: function () {
    document.getElementById('import-modal').classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
    this._importFile = null;
  },

  _setupDropzone: function () {
    const dropzone = document.getElementById('import-dropzone');
    const self = this;
    dropzone.ondragover = function (e) {
      e.preventDefault();
      dropzone.classList.add('ui-trans-import-dropzone--active');
    };
    dropzone.ondragleave = function () {
      dropzone.classList.remove('ui-trans-import-dropzone--active');
    };
    dropzone.ondrop = function (e) {
      e.preventDefault();
      dropzone.classList.remove('ui-trans-import-dropzone--active');
      if (e.dataTransfer.files.length > 0) {
        self.previewImport(e.dataTransfer.files[0]);
      }
    };
  },

  previewImport: function (file) {
    if (!file) return;
    if (!file.name.endsWith('.json')) {
      this.showToast('Please select a .json file', 'error');
      return;
    }
    this._importFile = file;
    const formData = new FormData();
    formData.append('file', file);

    const url =
      '/api/translations/service/ui-translations/' + this.currentLang + '/import/preview/';

    document.getElementById('import-dropzone').hidden = true;
    const previewEl = document.getElementById('import-preview');
    previewEl.hidden = false;
    previewEl.innerHTML =
      '<div class="ui-trans-loading"><i class="fas fa-spinner fa-spin"></i><p>Validating...</p></div>';

    const self = this;
    fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': AdminUtils.getCsrfToken() },
      body: formData,
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.success) {
          self._renderPreview(data.preview, file.name);
          document.getElementById('import-footer').hidden = false;
        } else {
          previewEl.innerHTML =
            '<div class="ui-trans-import-error"><i class="fas fa-exclamation-triangle"></i><p>' +
            self.esc(data.error) +
            '</p></div>';
          document.getElementById('import-footer').hidden = true;
        }
      })
      .catch(function (err) {
        previewEl.innerHTML =
          '<div class="ui-trans-import-error"><i class="fas fa-exclamation-triangle"></i><p>Validation failed</p></div>';
      });
  },

  _renderPreview: function (preview, filename) {
    let html = '<div class="ui-trans-import-summary">';
    html += '<h4><i class="fas fa-file-alt"></i> ' + this.esc(filename) + '</h4>';
    html += '<div class="ui-trans-import-stats">';
    html +=
      '<div class="ui-trans-import-stat ui-trans-import-stat--new"><span class="ui-trans-import-stat__value">' +
      preview.new +
      '</span><span class="ui-trans-import-stat__label">New</span></div>';
    html +=
      '<div class="ui-trans-import-stat ui-trans-import-stat--updated"><span class="ui-trans-import-stat__value">' +
      preview.updated +
      '</span><span class="ui-trans-import-stat__label">Updated</span></div>';
    html +=
      '<div class="ui-trans-import-stat ui-trans-import-stat--unchanged"><span class="ui-trans-import-stat__value">' +
      preview.unchanged +
      '</span><span class="ui-trans-import-stat__label">Unchanged</span></div>';
    html +=
      '<div class="ui-trans-import-stat ui-trans-import-stat--skipped"><span class="ui-trans-import-stat__value">' +
      preview.skipped +
      '</span><span class="ui-trans-import-stat__label">Skipped</span></div>';
    html += '</div>';

    if (preview.skipped > 0 && preview.skipped_keys && preview.skipped_keys.length > 0) {
      html +=
        '<details class="ui-trans-import-skipped"><summary>Skipped keys (not in registry)</summary><ul>';
      for (let i = 0; i < preview.skipped_keys.length; i++) {
        html += '<li><code>' + this.esc(preview.skipped_keys[i]) + '</code></li>';
      }
      if (preview.skipped > preview.skipped_keys.length) {
        html += '<li>... and ' + (preview.skipped - preview.skipped_keys.length) + ' more</li>';
      }
      html += '</ul></details>';
    }

    if (
      preview.pack_registry_version &&
      preview.pack_registry_version !== preview.current_registry_version
    ) {
      html += '<p class="ui-trans-import-notice"><i class="fas fa-info-circle"></i> ';
      html +=
        'Pack was exported with ' +
        preview.pack_registry_version +
        ' strings; current registry has ' +
        preview.current_registry_version +
        '.</p>';
    }

    html += '</div>';
    document.getElementById('import-preview').innerHTML = html;
  },

  applyImport: function () {
    if (!this._importFile || !this.currentLang) return;

    const btn = document.getElementById('import-apply-btn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Importing...';

    const formData = new FormData();
    formData.append('file', this._importFile);

    const url = '/api/translations/service/ui-translations/' + this.currentLang + '/import/apply/';

    const self = this;
    fetch(url, {
      method: 'POST',
      headers: { 'X-CSRFToken': AdminUtils.getCsrfToken() },
      body: formData,
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.success) {
          self.showToast(data.message || 'Import complete', 'success');
          self.closeImportModal();
          self.loadStrings(self.currentLang);
          self.updateProgress(data.translated_count, data.total_strings);
          // Update tab badge
          const tab = document.querySelector('.ui-trans-tab[data-lang="' + self.currentLang + '"]');
          if (tab) {
            const pct =
              data.total_strings > 0
                ? Math.round((data.translated_count / data.total_strings) * 100)
                : 0;
            const badge = tab.querySelector('.ui-trans-tab__badge');
            if (badge) {
              badge.textContent = pct + '%';
              badge.className = 'ui-trans-tab__badge';
              if (pct >= 100) badge.classList.add('ui-trans-tab__badge--complete');
              else if (pct > 0) badge.classList.add('ui-trans-tab__badge--partial');
            }
          }
        } else {
          self.showToast(data.error || 'Import failed', 'error');
        }
      })
      .catch(function (err) {
        self.showToast('Import failed: ' + err.message, 'error');
      })
      .finally(function () {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-check"></i> Apply Import';
      });
  },

  // === Lock Toggle ===

  toggleLock: function (btnEl) {
    const key = btnEl.dataset.key;
    if (!key || !this.currentLang) return;

    btnEl.disabled = true;
    const icon = btnEl.querySelector('i');
    const origClass = icon.className;
    icon.className = 'fas fa-spinner fa-spin';

    const url = '/api/translations/service/ui-translations/' + this.currentLang + '/lock/';

    const self = this;
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
      },
      body: JSON.stringify({ key: key }),
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.success) {
          const row = btnEl.closest('.ui-trans-row');
          const isLocked = data.is_locked;

          // Update row state
          row.dataset.isLocked = '' + isLocked;
          row.classList.toggle('ui-trans-row--locked', isLocked);
          btnEl.classList.toggle('ui-trans-row__lock--active', isLocked);
          btnEl.title = isLocked ? 'Unlock translation' : 'Lock translation';
          icon.className = isLocked ? 'fas fa-lock' : 'fas fa-lock-open';

          // Toggle textarea readonly
          const textarea = row.querySelector('.ui-trans-row__input');
          if (textarea) textarea.readOnly = isLocked;

          // Toggle AI translate button
          const translateBtn = row.querySelector('.ui-trans-row__translate');
          if (translateBtn) translateBtn.disabled = isLocked;

          // Update badge
          const statusDiv = row.querySelector('.ui-trans-row__status');
          if (statusDiv) {
            if (isLocked) {
              statusDiv.innerHTML =
                '<span class="ui-trans-badge ui-trans-badge--locked"><i class="fas fa-lock"></i> Locked</span>';
            } else {
              // Restore original badge based on data attributes
              const hasTranslation = row.dataset.hasTranslation === 'true';
              const isAuto = row.dataset.isAuto === 'true';
              const isVerified = row.dataset.isVerified === 'true';
              const source = row.dataset.source || '';
              if (!hasTranslation) {
                statusDiv.innerHTML =
                  '<span class="ui-trans-badge ui-trans-badge--missing">Missing</span>';
              } else if (source === 'shipped') {
                statusDiv.innerHTML =
                  '<span class="ui-trans-badge ui-trans-badge--shipped"><i class="fas fa-box"></i> Shipped</span>';
              } else if (isVerified) {
                statusDiv.innerHTML =
                  '<span class="ui-trans-badge ui-trans-badge--verified">Verified</span>';
              } else if (isAuto) {
                statusDiv.innerHTML =
                  '<span class="ui-trans-badge ui-trans-badge--auto">Auto</span>';
              } else {
                statusDiv.innerHTML = '';
              }
            }
          }

          self.showToast(isLocked ? 'Translation locked' : 'Translation unlocked', 'success');
        } else {
          self.showToast(data.error || 'Lock toggle failed', 'error');
          icon.className = origClass;
        }
      })
      .catch(function (err) {
        self.showToast('Lock toggle failed: ' + err.message, 'error');
        icon.className = origClass;
      })
      .finally(function () {
        btnEl.disabled = false;
      });
  },

  // === Per-field AI Translate ===

  translateString: function (btnEl) {
    const key = btnEl.dataset.key;
    if (!key || !this.currentLang) return;

    // Check if locked
    const row = btnEl.closest('.ui-trans-row');
    if (row && row.dataset.isLocked === 'true') {
      this.showToast('This translation is locked', 'error');
      return;
    }

    btnEl.disabled = true;
    const icon = btnEl.querySelector('i');
    icon.className = 'fas fa-spinner fa-spin';

    const url =
      '/api/translations/service/ui-translations/' + this.currentLang + '/translate-string/';

    const self = this;
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
      },
      body: JSON.stringify({ key: key }),
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.success && data.translated_text) {
          const textarea = document.querySelector('textarea[data-key="' + key + '"]');
          if (textarea) {
            textarea.value = data.translated_text;
            textarea.classList.remove('ui-trans-row__input--empty');
            self.dirty[key] = data.translated_text;
            self.updateSaveBtn();
          }
        } else {
          self.showToast(data.error || 'Translation failed', 'error');
        }
      })
      .catch(function (err) {
        self.showToast('Translation failed: ' + err.message, 'error');
      })
      .finally(function () {
        btnEl.disabled = false;
        icon.className = 'fas fa-language';
      });
  },
};

/**
 * Event delegation handler for UI translations editor
 */
function handleUITransEditorActions(e) {
  const actionElement = e.target.closest('[data-action]');
  if (!actionElement) return;

  const action = actionElement.dataset.action;

  switch (action) {
    case 'select-language':
      e.preventDefault();
      const langCode = actionElement.dataset.lang;
      if (langCode) {
        UITransEditor.selectLanguage(langCode, actionElement);
      }
      break;
    case 'apply-filter':
      const filterValue = e.target.value;
      UITransEditor.applyFilter(filterValue);
      break;
    case 'filter-section':
      const sectionValue = e.target.value;
      UITransEditor.filterSection(sectionValue);
      break;
    case 'export-pack':
      e.preventDefault();
      UITransEditor.exportPack();
      break;
    case 'show-import-modal':
      e.preventDefault();
      UITransEditor.showImportModal();
      break;
    case 'auto-translate':
      e.preventDefault();
      UITransEditor.autoTranslate();
      break;
    case 'save-all':
      e.preventDefault();
      UITransEditor.saveAll();
      break;
    case 'close-import-modal':
      e.preventDefault();
      UITransEditor.closeImportModal();
      break;
    case 'apply-import':
      e.preventDefault();
      UITransEditor.applyImport();
      break;
  }
}

/**
 * Handle file input change
 */
function handleFileInputChange(e) {
  const fileInput = e.target.closest('[data-action="preview-import"]');
  if (fileInput && fileInput.files && fileInput.files[0]) {
    UITransEditor.previewImport(fileInput.files[0]);
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
  // Set up event delegation
  document.addEventListener('click', handleUITransEditorActions);
  document.addEventListener('change', handleUITransEditorActions);
  document.addEventListener('change', handleFileInputChange);

  // Auto-select first language if languages exist
  const firstTab = document.querySelector('.ui-trans-tab');
  if (firstTab) {
    const langCode = firstTab.dataset.lang;
    if (langCode) {
      UITransEditor.selectLanguage(langCode, firstTab);
    }
  }
});
