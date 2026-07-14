/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Form Builder Visual Builder
 *
 * Main JavaScript class for the drag-and-drop form builder interface.
 * Handles field management, drag-drop, properties editing, and persistence.
 */

class FormBuilder {
  constructor(formData, fieldsData = [], stepsData = [], rulesData = []) {
    this.formId = formData.id;
    this.form = formData;
    this.fields = fieldsData || [];
    this.steps = stepsData || [];
    this.rules = rulesData || [];
    this.selectedField = null;
    this.currentStep = null;
    this.isDirty = false;
    this.history = [];
    this.historyIndex = -1;
    this.maxHistorySize = 50;
    this.autoSaveTimer = null;
    this.autoSaveDelay = 3000;
    this.editingRuleId = null; // Track which rule is being edited

    // Base URL for API calls (determined from current URL)
    const langMatch = window.location.pathname.match(/^\/([a-z]{2})\//);
    const langPrefix = langMatch ? `/${langMatch[1]}` : '';
    this.baseUrl = `${langPrefix}/admin/form_builder/forms/${this.formId}`;

    // BroadcastChannel for cross-window communication with Page Builder
    this.broadcastChannel = null;
    this.initBroadcastChannel();

    this.init();
  }

  /**
   * Safely escape HTML to prevent XSS
   */
  escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  /**
   * Initialize BroadcastChannel for cross-window communication
   * Used to notify the Page Builder when forms are created/updated
   */
  initBroadcastChannel() {
    try {
      this.broadcastChannel = new BroadcastChannel('form_builder_updates');
    } catch (e) {
      // BroadcastChannel not supported in this browser
      console.warn('BroadcastChannel not supported:', e);
    }
  }

  /**
   * Broadcast form update to other windows (Page Builder)
   * @param {string} action - The action type: 'created', 'updated', 'deleted'
   */
  broadcastFormUpdate(action = 'updated') {
    if (!this.broadcastChannel) return;

    const formInfo = {
      id: this.formId,
      slug: this.form.slug,
      name: this.form.name,
      title: this.form.title,
      is_multi_step: this.form.is_multi_step,
      field_count: this.fields.length,
      step_count: this.steps.length,
    };

    this.broadcastChannel.postMessage({
      type: 'form_' + action,
      form: formInfo,
      timestamp: Date.now(),
    });

    console.log('Broadcasted form update:', action, formInfo);
  }

  /**
   * Initialize the form builder
   */
  init() {
    this.initDragDrop();
    this.initFieldLibrary();
    this.initPropertyPanel();
    this.initStepManagement();
    this.initModalTabs();
    this.initFormHeader();
    this.initKeyboardShortcuts();
    this.initRulesManagement();
    this.saveHistoryState();
    console.log('Form Builder initialized', this.form);
  }

  // =========================================================================
  // Drag and Drop
  // =========================================================================

  initDragDrop() {
    // Initialize Sortable on fields container
    const fieldsContainer = document.getElementById('fields-container');
    if (fieldsContainer && typeof Sortable !== 'undefined') {
      this.fieldsSortable = new Sortable(fieldsContainer, {
        animation: 150,
        handle: '.drag-handle',
        ghostClass: 'sortable-ghost',
        dragClass: 'sortable-drag',
        chosenClass: 'sortable-chosen',
        filter: '.empty-drop-zone',
        onEnd: evt => this.onFieldReorder(evt),
      });
    }

    // Initialize drag from field library
    this.initFieldLibraryDrag();
  }

  initFieldLibraryDrag() {
    const fieldItems = document.querySelectorAll('.field-library .field-item');
    const fieldsContainer = document.getElementById('fields-container');

    fieldItems.forEach(item => {
      item.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/plain', item.dataset.fieldType);
        e.dataTransfer.effectAllowed = 'copy';
        item.classList.add('dragging');
      });

      item.addEventListener('dragend', () => {
        item.classList.remove('dragging');
      });
    });

    // Handle drop on fields container
    fieldsContainer.addEventListener('dragover', e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'copy';
      fieldsContainer.classList.add('drag-over');
    });

    fieldsContainer.addEventListener('dragleave', () => {
      fieldsContainer.classList.remove('drag-over');
    });

    fieldsContainer.addEventListener('drop', e => {
      e.preventDefault();
      fieldsContainer.classList.remove('drag-over');

      // Skip if drop was on the empty zone (it has its own handler)
      const emptyZone = document.getElementById('empty-drop-zone');
      if (emptyZone && (e.target === emptyZone || emptyZone.contains(e.target))) {
        return;
      }

      const fieldType = e.dataTransfer.getData('text/plain');
      if (fieldType && FIELD_TYPES[fieldType]) {
        this.addField(fieldType);
      }
    });

    // Also handle empty drop zone
    const emptyZone = document.getElementById('empty-drop-zone');
    if (emptyZone) {
      emptyZone.addEventListener('dragover', e => {
        e.preventDefault();
        emptyZone.classList.add('drag-over');
      });

      emptyZone.addEventListener('dragleave', () => {
        emptyZone.classList.remove('drag-over');
      });

      emptyZone.addEventListener('drop', e => {
        e.preventDefault();
        e.stopPropagation(); // Prevent bubbling to fields-container
        emptyZone.classList.remove('drag-over');
        const fieldType = e.dataTransfer.getData('text/plain');
        if (fieldType && FIELD_TYPES[fieldType]) {
          this.addField(fieldType);
        }
      });
    }
  }

  onFieldReorder(evt) {
    // Get new order of field IDs
    const fieldIds = Array.from(document.querySelectorAll('.field-wrapper[data-field-id]')).map(
      el => parseInt(el.dataset.fieldId)
    );

    // Update local state
    this.fields.sort((a, b) => {
      return fieldIds.indexOf(a.id) - fieldIds.indexOf(b.id);
    });

    this.fields.forEach((field, index) => {
      field.order = index;
    });

    // Save to server
    this.saveFieldOrder(fieldIds);
    this.markDirty();
    this.saveHistoryState();
  }

  // =========================================================================
  // Field Library
  // =========================================================================

  initFieldLibrary() {
    // Field search
    const searchInput = document.getElementById('field-search');
    if (searchInput) {
      searchInput.addEventListener('input', e => {
        this.filterFieldLibrary(e.target.value);
      });
    }
  }

  filterFieldLibrary(query) {
    const normalizedQuery = query.toLowerCase().trim();
    const fieldItems = document.querySelectorAll('.field-library .field-item');
    const fieldGroups = document.querySelectorAll('.field-library .field-group');

    fieldItems.forEach(item => {
      const fieldType = item.dataset.fieldType;
      const typeInfo = FIELD_TYPES[fieldType];
      const name = typeInfo ? typeInfo.name.toLowerCase() : '';
      const matches = name.includes(normalizedQuery) || fieldType.includes(normalizedQuery);
      item.style.display = matches ? '' : 'none';
    });

    // Hide empty groups
    fieldGroups.forEach(group => {
      const visibleItems = group.querySelectorAll('.field-item:not([style*="display: none"])');
      group.style.display = visibleItems.length > 0 ? '' : 'none';
    });
  }

  // =========================================================================
  // Field CRUD Operations
  // =========================================================================

  async addField(fieldType, position = null) {
    const typeInfo = FIELD_TYPES[fieldType];
    if (!typeInfo) {
      console.error('Unknown field type:', fieldType);
      return;
    }

    // Generate unique field name
    const existingNames = this.fields.map(f => f.field_name);
    const baseName = fieldType.replace(/_/g, '');
    let fieldName = baseName;
    let counter = 1;
    while (existingNames.includes(fieldName)) {
      fieldName = `${baseName}${counter++}`;
    }

    // Create field data
    const fieldData = {
      field_type: fieldType,
      field_name: fieldName,
      label: typeInfo.name,
      placeholder: '',
      help_text: '',
      is_required: false,
      order: position !== null ? position : this.fields.length,
      width: 'full',
      step_id: this.currentStep,
      options: typeInfo.hasOptions
        ? [
            { value: 'option1', label: FB_TRANSLATIONS.option + ' 1' },
            { value: 'option2', label: FB_TRANSLATIONS.option + ' 2' },
          ]
        : [],
      rating_config: typeInfo.hasRatingConfig ? { max_stars: 5 } : {},
      file_config: typeInfo.hasFileConfig ? { max_size_mb: 5, max_files: 1 } : {},
    };

    const url = `${this.baseUrl}/builder/fields/add/`;
    console.log('[ADD_FIELD] Making API request to:', url);
    console.log('[ADD_FIELD] Field data:', JSON.stringify(fieldData, null, 2));

    try {
      const response = await this.apiRequest('POST', url, fieldData);
      console.log('[ADD_FIELD] Response received:', JSON.stringify(response, null, 2));

      if (response.success) {
        // Add to local state
        const newField = response.field;
        this.fields.push(newField);

        // Render field in canvas
        this.renderField(newField);

        // Hide empty drop zone
        const emptyZone = document.getElementById('empty-drop-zone');
        if (emptyZone) {
          emptyZone.style.display = 'none';
        }

        // Select the new field
        this.selectField(newField.id);

        this.markDirty();
        this.saveHistoryState();
        this.showNotification(FB_TRANSLATIONS.fieldAdded, 'success');
        // Broadcast update to Page Builder (field count changed)
        this.broadcastFormUpdate('updated');
      }
    } catch (error) {
      console.error('Error adding field:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
    }
  }

  async updateField(fieldId, data) {
    const field = this.fields.find(f => f.id === fieldId);
    if (!field) return;

    try {
      const response = await this.apiRequest(
        'POST',
        `${this.baseUrl}/builder/fields/${fieldId}/update/`,
        data
      );

      if (response.success) {
        // Update local state
        Object.assign(field, data);

        // Re-render field preview
        this.refreshFieldPreview(fieldId);

        this.markDirty();
        this.saveHistoryState();
      }
    } catch (error) {
      console.error('Error updating field:', error);

      // Handle 404 - field doesn't exist in database (stale local state)
      if (error.message && error.message.includes('404')) {
        console.warn(`Field ${fieldId} not found in database. Removing from local state.`);
        // Remove stale field from local state
        this.fields = this.fields.filter(f => f.id !== fieldId);
        // Remove from DOM
        const fieldWrapper = document.querySelector(`.field-wrapper[data-field-id="${fieldId}"]`);
        if (fieldWrapper) {
          fieldWrapper.remove();
        }
        // Deselect if selected
        if (this.selectedField && this.selectedField.id === fieldId) {
          this.deselectField();
        }
        this.showNotification(
          FB_TRANSLATIONS.fieldNotFound || 'Field not found. It may have been deleted.',
          'warning'
        );
      } else {
        this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
      }
    }
  }

  async deleteField(fieldId) {
    const field = this.fields.find(f => f.id === fieldId);
    if (!field) return;

    // Show confirmation modal
    this.pendingDeleteType = 'field';
    this.pendingDeleteId = fieldId;
    document.getElementById('delete-modal-message').textContent = FB_TRANSLATIONS.confirmDelete;
    document.getElementById('delete-modal').classList.remove('fb-hidden');
  }

  async duplicateField(fieldId) {
    const field = this.fields.find(f => f.id === fieldId);
    if (!field) return;

    // Create copy with new name
    const fieldData = { ...field };
    delete fieldData.id;
    fieldData.field_name = field.field_name + '_copy';
    fieldData.label = field.label + ' (Copy)';
    fieldData.order = this.fields.length;

    try {
      const response = await this.apiRequest(
        'POST',
        `${this.baseUrl}/builder/fields/add/`,
        fieldData
      );

      if (response.success) {
        this.fields.push(response.field);
        this.renderField(response.field);
        this.selectField(response.field.id);
        this.markDirty();
        this.saveHistoryState();
      }
    } catch (error) {
      console.error('Error duplicating field:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
    }
  }

  async confirmDelete() {
    this.closeDeleteModal();

    if (this.pendingDeleteType === 'field') {
      await this.performDeleteField(this.pendingDeleteId);
    } else if (this.pendingDeleteType === 'step') {
      await this.performDeleteStep(this.pendingDeleteId);
    }
  }

  async performDeleteField(fieldId) {
    try {
      const response = await this.apiRequest(
        'POST',
        `${this.baseUrl}/builder/fields/${fieldId}/delete/`
      );

      if (response.success) {
        // Remove from local state
        this.fields = this.fields.filter(f => f.id !== fieldId);

        // Remove from DOM
        const fieldWrapper = document.querySelector(`.field-wrapper[data-field-id="${fieldId}"]`);
        if (fieldWrapper) {
          fieldWrapper.remove();
        }

        // Deselect if was selected
        if (this.selectedField && this.selectedField.id === fieldId) {
          this.deselectField();
        }

        // Show empty zone if no fields
        if (this.fields.length === 0) {
          const emptyZone = document.getElementById('empty-drop-zone');
          if (emptyZone) {
            emptyZone.style.display = 'flex';
          }
        }

        this.markDirty();
        this.saveHistoryState();
        this.showNotification(FB_TRANSLATIONS.fieldDeleted, 'success');
        // Broadcast update to Page Builder (field count changed)
        this.broadcastFormUpdate('updated');
      }
    } catch (error) {
      console.error('Error deleting field:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
    }
  }

  // =========================================================================
  // Field Selection & Properties
  // =========================================================================

  selectField(fieldId) {
    // Deselect previous
    document.querySelectorAll('.field-wrapper.selected').forEach(el => {
      el.classList.remove('selected');
    });

    // Select new
    const fieldWrapper = document.querySelector(`.field-wrapper[data-field-id="${fieldId}"]`);
    if (fieldWrapper) {
      fieldWrapper.classList.add('selected');
    }

    // Find field data
    this.selectedField = this.fields.find(f => f.id === fieldId);
    if (!this.selectedField) return;

    // Show properties panel
    this.showPropertiesPanel();
    this.loadFieldProperties(this.selectedField);
  }

  deselectField() {
    document.querySelectorAll('.field-wrapper.selected').forEach(el => {
      el.classList.remove('selected');
    });
    this.selectedField = null;
    this.hidePropertiesPanel();
  }

  showPropertiesPanel() {
    document.getElementById('no-selection').style.display = 'none';
    document.getElementById('field-properties').classList.remove('fb-hidden');
  }

  hidePropertiesPanel() {
    document.getElementById('no-selection').style.display = 'flex';
    document.getElementById('field-properties').classList.add('fb-hidden');
  }

  loadFieldProperties(field) {
    const typeInfo = FIELD_TYPES[field.field_type] || {};

    // Update type badge
    document.getElementById('field-type-badge').innerHTML = `
            <i class="fas ${typeInfo.icon || 'fa-question'}"></i>
            <span id="field-type-name">${typeInfo.name || field.field_type}</span>
        `;

    // Content tab
    document.getElementById('prop-label').value = field.label || '';
    document.getElementById('prop-placeholder').value = field.placeholder || '';
    document.getElementById('prop-help-text').value = field.help_text || '';
    document.getElementById('prop-default-value').value = field.default_value || '';

    // Show/hide options editor
    const optionsEditor = document.getElementById('options-editor');
    if (typeInfo.hasOptions) {
      optionsEditor.classList.remove('fb-hidden');
      this.renderOptions(field.options || []);
    } else {
      optionsEditor.classList.add('fb-hidden');
    }

    // Show/hide rating config
    const ratingConfig = document.getElementById('rating-config');
    if (typeInfo.hasRatingConfig) {
      ratingConfig.classList.remove('fb-hidden');
      document.getElementById('prop-max-stars').value = field.rating_config?.max_stars || 5;
      document.getElementById('prop-allow-half').checked = field.rating_config?.allow_half || false;
    } else {
      ratingConfig.classList.add('fb-hidden');
    }

    // Show/hide file config
    const fileConfig = document.getElementById('file-config');
    if (typeInfo.hasFileConfig) {
      fileConfig.classList.remove('fb-hidden');
      document.getElementById('prop-max-size').value = field.file_config?.max_size_mb || 5;
      document.getElementById('prop-max-files').value = field.file_config?.max_files || 1;
      document.getElementById('prop-allowed-types').value = (
        field.file_config?.allowed_types || []
      ).join(', ');
    } else {
      fileConfig.classList.add('fb-hidden');
    }

    // Validation tab
    document.getElementById('prop-required').checked = field.is_required || false;
    document.getElementById('prop-min-length').value = field.min_length || '';
    document.getElementById('prop-max-length').value = field.max_length || '';
    document.getElementById('prop-min-value').value = field.min_value || '';
    document.getElementById('prop-max-value').value = field.max_value || '';
    document.getElementById('prop-regex').value = field.validation_regex || '';
    document.getElementById('prop-validation-message').value = field.validation_message || '';

    // Show/hide number validation
    const isNumber = field.field_type === 'number';
    document.getElementById('number-validation').classList.toggle('fb-hidden', !isNumber);
    document.getElementById('number-validation-max').classList.toggle('fb-hidden', !isNumber);

    // Style tab - width selector
    document.querySelectorAll('.width-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.width === field.width);
    });
    document.getElementById('prop-css-class').value = field.css_class || '';

    // Advanced tab
    document.getElementById('prop-field-name').value = field.field_name || '';
    const stepSelect = document.getElementById('prop-step');
    if (stepSelect) {
      stepSelect.value = field.step_id || '';
    }

    // Load conditions if any
    this.renderConditions(field);
  }

  initPropertyPanel() {
    // Tab switching
    document.querySelectorAll('.property-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.property-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        tab.classList.add('active');
        document
          .querySelector(`.tab-content[data-tab-content="${tab.dataset.tab}"]`)
          .classList.add('active');
      });
    });

    // Width selector
    document.querySelectorAll('.width-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.width-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        if (this.selectedField) {
          this.updateField(this.selectedField.id, { width: btn.dataset.width });
        }
      });
    });

    // Property inputs with debounced save
    const debounce = (fn, delay) => {
      let timer;
      return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
      };
    };

    const saveProperty = debounce((key, value) => {
      if (this.selectedField) {
        this.updateField(this.selectedField.id, { [key]: value });
      }
    }, 500);

    // Content properties
    document
      .getElementById('prop-label')
      .addEventListener('input', e => saveProperty('label', e.target.value));
    document
      .getElementById('prop-placeholder')
      .addEventListener('input', e => saveProperty('placeholder', e.target.value));
    document
      .getElementById('prop-help-text')
      .addEventListener('input', e => saveProperty('help_text', e.target.value));
    document
      .getElementById('prop-default-value')
      .addEventListener('input', e => saveProperty('default_value', e.target.value));

    // Validation properties
    document
      .getElementById('prop-required')
      .addEventListener('change', e => saveProperty('is_required', e.target.checked));
    document
      .getElementById('prop-min-length')
      .addEventListener('input', e =>
        saveProperty('min_length', e.target.value ? parseInt(e.target.value) : null)
      );
    document
      .getElementById('prop-max-length')
      .addEventListener('input', e =>
        saveProperty('max_length', e.target.value ? parseInt(e.target.value) : null)
      );
    document
      .getElementById('prop-min-value')
      .addEventListener('input', e =>
        saveProperty('min_value', e.target.value ? parseFloat(e.target.value) : null)
      );
    document
      .getElementById('prop-max-value')
      .addEventListener('input', e =>
        saveProperty('max_value', e.target.value ? parseFloat(e.target.value) : null)
      );
    document
      .getElementById('prop-regex')
      .addEventListener('input', e => saveProperty('validation_regex', e.target.value));
    document
      .getElementById('prop-validation-message')
      .addEventListener('input', e => saveProperty('validation_message', e.target.value));

    // Style properties
    document
      .getElementById('prop-css-class')
      .addEventListener('input', e => saveProperty('css_class', e.target.value));

    // Advanced properties
    document
      .getElementById('prop-field-name')
      .addEventListener('input', e => saveProperty('field_name', e.target.value));
    document
      .getElementById('prop-step')
      .addEventListener('change', e =>
        saveProperty('step_id', e.target.value ? parseInt(e.target.value) : null)
      );

    // Rating config
    document.getElementById('prop-max-stars').addEventListener('change', e => {
      if (this.selectedField) {
        const config = { ...this.selectedField.rating_config, max_stars: parseInt(e.target.value) };
        this.updateField(this.selectedField.id, { rating_config: config });
      }
    });
    document.getElementById('prop-allow-half').addEventListener('change', e => {
      if (this.selectedField) {
        const config = { ...this.selectedField.rating_config, allow_half: e.target.checked };
        this.updateField(this.selectedField.id, { rating_config: config });
      }
    });

    // File config
    document.getElementById('prop-max-size').addEventListener('change', e => {
      if (this.selectedField) {
        const config = { ...this.selectedField.file_config, max_size_mb: parseInt(e.target.value) };
        this.updateField(this.selectedField.id, { file_config: config });
      }
    });
    document.getElementById('prop-max-files').addEventListener('change', e => {
      if (this.selectedField) {
        const config = { ...this.selectedField.file_config, max_files: parseInt(e.target.value) };
        this.updateField(this.selectedField.id, { file_config: config });
      }
    });
    document.getElementById('prop-allowed-types').addEventListener('input', e => {
      if (this.selectedField) {
        const types = e.target.value
          .split(',')
          .map(t => t.trim())
          .filter(t => t);
        const config = { ...this.selectedField.file_config, allowed_types: types };
        this.updateField(this.selectedField.id, { file_config: config });
      }
    });
  }

  // =========================================================================
  // Options Editor
  // =========================================================================

  renderOptions(options) {
    const container = document.getElementById('options-list');
    container.innerHTML = options
      .map(
        (opt, index) => `
            <div class="option-item" data-index="${index}">
                <input type="text" value="${this.escapeHtml(opt.label || '')}" placeholder="${this.escapeHtml(FB_TRANSLATIONS.option)} ${index + 1}"
                       data-action="fb-update-option" data-option-index="${index}">
                <button data-action="fb-remove-option" data-option-index="${index}" title="Remove">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `
      )
      .join('');
  }

  addOption() {
    if (!this.selectedField) return;

    const options = this.selectedField.options || [];
    const newIndex = options.length + 1;
    options.push({
      value: `option${newIndex}`,
      label: `${FB_TRANSLATIONS.option} ${newIndex}`,
    });

    this.updateField(this.selectedField.id, { options });
    this.renderOptions(options);
  }

  updateOption(index, label) {
    if (!this.selectedField) return;

    const options = this.selectedField.options || [];
    if (options[index]) {
      options[index].label = label;
      options[index].value = label
        .toLowerCase()
        .replace(/\s+/g, '_')
        .replace(/[^a-z0-9_]/g, '');
      this.updateField(this.selectedField.id, { options });
    }
  }

  removeOption(index) {
    if (!this.selectedField) return;

    const options = this.selectedField.options || [];
    options.splice(index, 1);
    this.updateField(this.selectedField.id, { options });
    this.renderOptions(options);
  }

  // =========================================================================
  // Field Rendering
  // =========================================================================

  renderField(field) {
    const container = document.getElementById('fields-container');
    const typeInfo = FIELD_TYPES[field.field_type] || {};

    const wrapper = document.createElement('div');
    wrapper.className = 'field-wrapper';
    wrapper.dataset.fieldId = field.id;
    wrapper.dataset.fieldType = field.field_type;
    wrapper.dataset.fieldStep = field.step_id || '';
    wrapper.dataset.fieldWidth = field.width;

    // Generate step badge HTML
    const stepBadgeHTML = this.getStepBadgeHTML(field.step_id);

    // Check if field should be greyed out (not in current step)
    if (this.currentStep && field.step_id && field.step_id != this.currentStep) {
      wrapper.classList.add('out-of-step');
    }

    wrapper.innerHTML = `
            <div class="field-controls">
                <span class="drag-handle"><i class="fas fa-grip-vertical"></i></span>
                <div class="field-actions">
                    <button class="control-btn duplicate-btn" onclick="formBuilder.duplicateField(${field.id})" title="Duplicate">
                        <i class="fas fa-copy"></i>
                    </button>
                    <button class="control-btn delete-btn" onclick="formBuilder.deleteField(${field.id})" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                ${stepBadgeHTML}
            </div>
            <div class="field-content" onclick="formBuilder.selectField(${field.id})">
                ${this.getFieldPreviewHTML(field)}
            </div>
            <div class="width-indicator">${field.width}</div>
        `;

    container.appendChild(wrapper);
  }

  /**
   * Generate step badge HTML for a field
   */
  getStepBadgeHTML(stepId) {
    if (!this.form.is_multi_step || this.steps.length === 0) {
      return ''; // No badge needed for single-step forms
    }

    if (!stepId) {
      return `<span class="step-badge no-step" title="Not assigned to any step">
                <i class="fas fa-layer-group"></i> All
            </span>`;
    }

    const step = this.steps.find(s => s.id == stepId);
    if (!step) {
      return `<span class="step-badge no-step" title="Step not found">
                <i class="fas fa-question"></i> ?
            </span>`;
    }

    const stepIndex = this.steps.indexOf(step) + 1;
    return `<span class="step-badge" title="Step ${stepIndex}: ${step.title}">
            <i class="fas fa-layer-group"></i> ${stepIndex}
        </span>`;
  }

  refreshFieldPreview(fieldId) {
    const field = this.fields.find(f => f.id === fieldId);
    if (!field) return;

    const wrapper = document.querySelector(`.field-wrapper[data-field-id="${fieldId}"]`);
    if (!wrapper) return;

    const content = wrapper.querySelector('.field-content');
    if (content) {
      content.innerHTML = this.getFieldPreviewHTML(field);
    }

    // Update width
    wrapper.dataset.fieldWidth = field.width;
    wrapper.querySelector('.width-indicator').textContent = field.width;

    // Update step assignment
    wrapper.dataset.fieldStep = field.step_id || '';

    // Update step badge
    const existingBadge = wrapper.querySelector('.step-badge');
    if (existingBadge) {
      existingBadge.remove();
    }
    const stepBadgeHTML = this.getStepBadgeHTML(field.step_id);
    if (stepBadgeHTML) {
      const controls = wrapper.querySelector('.field-controls');
      if (controls) {
        controls.insertAdjacentHTML('beforeend', stepBadgeHTML);
      }
    }

    // Update out-of-step styling
    const isInStep = !this.currentStep || !field.step_id || field.step_id == this.currentStep;
    if (isInStep) {
      wrapper.classList.remove('out-of-step');
      wrapper.style.pointerEvents = '';
    } else {
      wrapper.classList.add('out-of-step');
      wrapper.style.pointerEvents = 'none';
    }
  }

  getFieldPreviewHTML(field) {
    const typeInfo = FIELD_TYPES[field.field_type] || {};
    const isLayout = typeInfo.isLayout;

    let preview = '';

    // Label (except for layout elements)
    if (!isLayout || field.field_type === 'heading') {
      if (field.field_type !== 'heading') {
        preview += `<label class="field-label-preview">
                    ${field.label}
                    ${field.is_required ? '<span class="required-star">*</span>' : ''}
                </label>`;
      }
    }

    // Field-specific preview
    switch (field.field_type) {
      case 'text':
      case 'email':
      case 'phone':
      case 'url':
        preview += `<input type="${field.field_type === 'url' ? 'url' : field.field_type}"
                    class="field-input-preview" placeholder="${field.placeholder || ''}" disabled>`;
        break;

      case 'textarea':
        preview += `<textarea class="field-input-preview" placeholder="${field.placeholder || ''}" rows="3" disabled></textarea>`;
        break;

      case 'number':
        preview += `<input type="number" class="field-input-preview" placeholder="${field.placeholder || '0'}" disabled>`;
        break;

      case 'date':
        preview += '<input type="date" class="field-input-preview" disabled>';
        break;

      case 'time':
        preview += '<input type="time" class="field-input-preview" disabled>';
        break;

      case 'datetime':
        preview += '<input type="datetime-local" class="field-input-preview" disabled>';
        break;

      case 'select':
        const selectOptions = field.options || [];
        preview += `<select class="field-input-preview" disabled>
                    <option value="">${field.placeholder || 'Select...'}</option>
                    ${selectOptions.map(opt => `<option>${opt.label}</option>`).join('')}
                </select>`;
        break;

      case 'radio':
        const radioOptions = field.options || [{ label: 'Option 1' }, { label: 'Option 2' }];
        preview += `<div class="radio-group-preview">
                    ${radioOptions
                      .map(
                        (opt, i) => `
                        <label class="radio-label-preview">
                            <input type="radio" name="preview_${field.id}" disabled>
                            <span>${opt.label}</span>
                        </label>
                    `
                      )
                      .join('')}
                </div>`;
        break;

      case 'checkbox':
        preview += `<label class="checkbox-label-preview">
                    <input type="checkbox" disabled>
                    <span>${field.placeholder || field.label}</span>
                </label>`;
        break;

      case 'checkbox_group':
        const cbOptions = field.options || [{ label: 'Option 1' }, { label: 'Option 2' }];
        preview += `<div class="checkbox-group-preview">
                    ${cbOptions
                      .map(
                        opt => `
                        <label class="checkbox-label-preview">
                            <input type="checkbox" disabled>
                            <span>${opt.label}</span>
                        </label>
                    `
                      )
                      .join('')}
                </div>`;
        break;

      case 'rating_stars':
        const maxStars = field.rating_config?.max_stars || 5;
        preview += `<div class="stars-preview">
                    ${Array(maxStars)
                      .fill(0)
                      .map(() => '<i class="fas fa-star star-preview"></i>')
                      .join('')}
                </div>`;
        break;

      case 'rating_likert':
        preview += `<div class="likert-preview">
                    <div class="likert-scale">
                        <span class="likert-label">Strongly Disagree</span>
                        <div class="likert-options">
                            ${Array(5)
                              .fill(0)
                              .map(
                                (_, i) => `
                                <label class="likert-option"><input type="radio" disabled><span>${i + 1}</span></label>
                            `
                              )
                              .join('')}
                        </div>
                        <span class="likert-label">Strongly Agree</span>
                    </div>
                </div>`;
        break;

      case 'rating_nps':
        preview += `<div class="nps-preview">
                    <div class="nps-scale">
                        <span class="nps-label">Not likely</span>
                        <div class="nps-options">
                            ${Array(11)
                              .fill(0)
                              .map((_, i) => {
                                const cls = i <= 6 ? 'detractor' : i <= 8 ? 'passive' : 'promoter';
                                return `<button class="nps-btn ${cls}" disabled>${i}</button>`;
                              })
                              .join('')}
                        </div>
                        <span class="nps-label">Very likely</span>
                    </div>
                </div>`;
        break;

      case 'file':
        preview += `<div class="file-upload-preview">
                    <i class="fas fa-cloud-upload-alt"></i>
                    <span>Click or drag files to upload</span>
                    ${field.file_config?.max_size_mb ? `<small>Max size: ${field.file_config.max_size_mb}MB</small>` : ''}
                </div>`;
        break;

      case 'product_select':
        preview += `<div class="product-select-preview">
                    <div class="product-placeholder">
                        <i class="fas fa-shopping-bag"></i>
                        <span>Product selector will appear here</span>
                    </div>
                </div>`;
        break;

      case 'hidden':
        preview += `<div class="hidden-field-preview">
                    <i class="fas fa-eye-slash"></i>
                    <span>Hidden field (${field.field_name})</span>
                    ${field.default_value ? `<small>Value: ${field.default_value}</small>` : ''}
                </div>`;
        break;

      case 'heading':
        preview += `<h3 class="heading-preview">${field.label}</h3>`;
        if (field.help_text) {
          preview += `<p class="heading-description-preview">${field.help_text}</p>`;
        }
        break;

      case 'paragraph':
        preview += `<div class="paragraph-preview">${field.label}</div>`;
        break;

      case 'divider':
        preview += '<hr class="divider-preview">';
        break;

      default:
        preview += `<input type="text" class="field-input-preview" placeholder="${field.placeholder || ''}" disabled>`;
    }

    // Help text (except for layout elements)
    if (field.help_text && !isLayout) {
      preview += `<span class="field-help-preview">${field.help_text}</span>`;
    }

    return preview;
  }

  // =========================================================================
  // Step Management
  // =========================================================================

  initStepManagement() {
    // Step tab clicks
    document.querySelectorAll('.step-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        this.switchToStep(tab.dataset.stepId);
      });
    });

    // Step list item clicks
    document.querySelectorAll('.step-item').forEach(item => {
      item.addEventListener('click', e => {
        if (!e.target.closest('.step-actions')) {
          this.switchToStep(item.dataset.stepId);
        }
      });
    });
  }

  switchToStep(stepId) {
    // Update current step
    this.currentStep = stepId ? parseInt(stepId) : null;

    // Update step tabs
    document.querySelectorAll('.step-tab').forEach(tab => {
      tab.classList.toggle('active', tab.dataset.stepId == stepId);
    });

    // Update step list
    document.querySelectorAll('.step-item').forEach(item => {
      item.classList.toggle('active', item.dataset.stepId == stepId);
    });

    // Filter fields by step
    this.filterFieldsByStep(stepId);
  }

  filterFieldsByStep(stepId) {
    document.querySelectorAll('.field-wrapper').forEach(wrapper => {
      const fieldStep = wrapper.dataset.fieldStep;
      // Field is "in step" if:
      // - No step is selected (showing all)
      // - Field has no step assigned (appears in all steps)
      // - Field's step matches the current step
      const isInStep = !stepId || !fieldStep || fieldStep == stepId;

      // Grey out instead of hiding
      if (isInStep) {
        wrapper.classList.remove('out-of-step');
        wrapper.style.pointerEvents = '';
      } else {
        wrapper.classList.add('out-of-step');
        wrapper.style.pointerEvents = 'none';
      }
    });
  }

  async addStep() {
    const stepData = {
      title: FB_TRANSLATIONS.newStep,
      description: '',
      order: this.steps.length,
      is_skippable: false,
      next_button_text: 'Next',
      back_button_text: 'Back',
    };

    try {
      const response = await this.apiRequest(
        'POST',
        `${this.baseUrl}/builder/steps/add/`,
        stepData
      );

      if (response.success) {
        this.steps.push(response.step);
        this.refreshStepUI();
        this.editStep(response.step.id);
        this.markDirty();
        // Broadcast update to Page Builder (step count changed)
        this.broadcastFormUpdate('updated');
      }
    } catch (error) {
      console.error('Error adding step:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
    }
  }

  editStep(stepId) {
    const step = this.steps.find(s => s.id === stepId);
    if (!step) return;

    document.getElementById('step-edit-id').value = stepId;
    document.getElementById('step-modal-title').textContent = 'Edit Step';
    document.getElementById('step-title').value = step.title || '';
    document.getElementById('step-description').value = step.description || '';
    document.getElementById('step-skippable').checked = step.is_skippable || false;
    document.getElementById('step-next-text').value = step.next_button_text || 'Next';
    document.getElementById('step-back-text').value = step.back_button_text || 'Back';

    document.getElementById('step-modal').classList.remove('fb-hidden');
  }

  async saveStep() {
    const stepId = document.getElementById('step-edit-id').value;
    const stepData = {
      title: document.getElementById('step-title').value,
      description: document.getElementById('step-description').value,
      is_skippable: document.getElementById('step-skippable').checked,
      next_button_text: document.getElementById('step-next-text').value,
      back_button_text: document.getElementById('step-back-text').value,
    };

    try {
      const response = await this.apiRequest(
        'POST',
        `${this.baseUrl}/builder/steps/${stepId}/update/`,
        stepData
      );

      if (response.success) {
        const step = this.steps.find(s => s.id == stepId);
        if (step) {
          Object.assign(step, stepData);
        }
        this.refreshStepUI();
        this.closeStepModal();
        this.markDirty();
      }
    } catch (error) {
      console.error('Error saving step:', error);

      // Handle 404 - step doesn't exist in database (stale local state)
      if (error.message && error.message.includes('404')) {
        console.warn(`Step ${stepId} not found in database. Removing from local state.`);
        // Remove stale step from local state
        this.steps = this.steps.filter(s => s.id != stepId);
        // Refresh UI
        this.refreshStepUI();
        this.closeStepModal();
        this.showNotification(
          FB_TRANSLATIONS.stepNotFound || 'Step not found. It may have been deleted.',
          'warning'
        );
      } else {
        this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
      }
    }
  }

  async deleteStep(stepId) {
    this.pendingDeleteType = 'step';
    this.pendingDeleteId = stepId;
    document.getElementById('delete-modal-message').textContent = FB_TRANSLATIONS.confirmDeleteStep;
    document.getElementById('delete-modal').classList.remove('fb-hidden');
  }

  async performDeleteStep(stepId) {
    try {
      const response = await this.apiRequest(
        'POST',
        `${this.baseUrl}/builder/steps/${stepId}/delete/`
      );

      if (response.success) {
        this.steps = this.steps.filter(s => s.id !== stepId);

        // Unassign fields from deleted step
        this.fields.forEach(field => {
          if (field.step_id === stepId) {
            field.step_id = null;
          }
        });

        this.refreshStepUI();
        this.markDirty();
        // Broadcast update to Page Builder (step count changed)
        this.broadcastFormUpdate('updated');
      }
    } catch (error) {
      console.error('Error deleting step:', error);

      // Handle 404 - step already deleted or doesn't exist
      if (error.message && error.message.includes('404')) {
        console.warn(`Step ${stepId} not found in database. Removing from local state.`);
        // Remove from local state anyway
        this.steps = this.steps.filter(s => s.id !== stepId);
        this.fields.forEach(field => {
          if (field.step_id === stepId) {
            field.step_id = null;
          }
        });
        this.refreshStepUI();
        this.showNotification(
          FB_TRANSLATIONS.stepNotFound || 'Step not found. It may have already been deleted.',
          'warning'
        );
      } else {
        this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
      }
    }
  }

  refreshStepUI() {
    // Refresh step tabs
    const tabsContainer = document.getElementById('step-tabs');
    tabsContainer.innerHTML = this.steps
      .map(
        (step, index) => `
            <button class="step-tab ${index === 0 ? 'active' : ''}" data-step-id="${step.id}">
                <span class="step-tab-number">${index + 1}</span>
                <span class="step-tab-title">${step.title}</span>
            </button>
        `
      )
      .join('');

    // Refresh step list
    const listContainer = document.getElementById('step-list');
    listContainer.innerHTML = this.steps
      .map(
        (step, index) => `
            <div class="step-item ${index === 0 ? 'active' : ''}" data-step-id="${step.id}" data-step-order="${step.order}">
                <span class="step-number">${index + 1}</span>
                <span class="step-title">${step.title}</span>
                <div class="step-actions">
                    <button class="step-btn" onclick="formBuilder.editStep(${step.id})" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="step-btn danger" onclick="formBuilder.deleteStep(${step.id})" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `
      )
      .join('');

    // Re-init event listeners
    this.initStepManagement();

    // Update step select in properties
    const stepSelect = document.getElementById('prop-step');
    stepSelect.innerHTML = `
            <option value="">All Steps (Single Page)</option>
            ${this.steps.map(s => `<option value="${s.id}">${s.title}</option>`).join('')}
        `;
  }

  closeStepModal() {
    document.getElementById('step-modal').classList.add('fb-hidden');
  }

  // =========================================================================
  // Form Header & Settings
  // =========================================================================

  initFormHeader() {
    // Editable title
    const titleEl = document.getElementById('form-title-preview');
    if (titleEl) {
      titleEl.addEventListener('blur', () => {
        this.form.title = titleEl.textContent;
        this.markDirty();
      });
    }

    // Editable description
    const descEl = document.getElementById('form-description-preview');
    if (descEl) {
      descEl.addEventListener('blur', () => {
        this.form.description = descEl.textContent;
        this.markDirty();
      });
    }

    // Form name input
    const nameInput = document.getElementById('form-name');
    if (nameInput) {
      nameInput.addEventListener('change', () => {
        this.form.name = nameInput.value;
        this.markDirty();
      });
    }
  }

  openFormSettings() {
    // Populate settings form
    document.getElementById('setting-name').value = this.form.name || '';
    document.getElementById('setting-slug').value = this.form.slug || '';
    document.getElementById('setting-title').value = this.form.title || '';
    document.getElementById('setting-description').value = this.form.description || '';
    document.getElementById('setting-submit-text').value = this.form.submit_button_text || 'Submit';
    document.getElementById('setting-success').value = this.form.success_message || '';
    document.getElementById('setting-error').value = this.form.error_message || '';
    document.getElementById('setting-active').checked = this.form.is_active;
    document.getElementById('setting-multi-step').checked = this.form.is_multi_step;
    document.getElementById('setting-require-login').checked = this.form.require_login;
    document.getElementById('setting-save-partial').checked = this.form.save_partial_responses;
    document.getElementById('setting-spam-protection').value =
      this.form.spam_protection || 'honeypot';
    document.getElementById('setting-recaptcha-site').value = this.form.recaptcha_site_key || '';
    document.getElementById('setting-recaptcha-secret').value =
      this.form.recaptcha_secret_key || '';

    // Show/hide recaptcha settings
    const spamSelect = document.getElementById('setting-spam-protection');
    spamSelect.addEventListener('change', () => {
      document
        .getElementById('recaptcha-settings')
        .classList.toggle('fb-hidden', spamSelect.value !== 'recaptcha');
    });

    document.getElementById('form-settings-modal').classList.remove('fb-hidden');
  }

  closeFormSettings() {
    document.getElementById('form-settings-modal').classList.add('fb-hidden');
  }

  async saveFormSettings() {
    const formData = {
      name: document.getElementById('setting-name').value,
      slug: document.getElementById('setting-slug').value,
      title: document.getElementById('setting-title').value,
      description: document.getElementById('setting-description').value,
      submit_button_text: document.getElementById('setting-submit-text').value,
      success_message: document.getElementById('setting-success').value,
      error_message: document.getElementById('setting-error').value,
      is_active: document.getElementById('setting-active').checked,
      is_multi_step: document.getElementById('setting-multi-step').checked,
      require_login: document.getElementById('setting-require-login').checked,
      save_partial_responses: document.getElementById('setting-save-partial').checked,
      spam_protection: document.getElementById('setting-spam-protection').value,
      recaptcha_site_key: document.getElementById('setting-recaptcha-site').value,
      recaptcha_secret_key: document.getElementById('setting-recaptcha-secret').value,
    };

    try {
      const response = await this.apiRequest('POST', `${this.baseUrl}/builder/save/`, {
        form: formData,
      });

      if (response.success) {
        Object.assign(this.form, formData);

        // Update UI
        document.getElementById('form-name').value = formData.name;
        document.getElementById('form-title-preview').textContent = formData.title;
        document.getElementById('form-description-preview').textContent = formData.description;
        document.getElementById('submit-btn-preview').textContent = formData.submit_button_text;

        // Update status badge
        const badge = document.querySelector('.status-badge');
        if (badge) {
          badge.className = `status-badge ${formData.is_active ? 'status-active' : 'status-inactive'}`;
          badge.innerHTML = formData.is_active
            ? '<i class="fas fa-check-circle"></i><span class="status-text">Active</span>'
            : '<i class="fas fa-pause-circle"></i><span class="status-text">Inactive</span>';
        }

        // Show/hide step management
        document
          .getElementById('step-management')
          .classList.toggle('fb-hidden', !formData.is_multi_step);
        document.getElementById('step-tabs').classList.toggle('fb-hidden', !formData.is_multi_step);
        document
          .getElementById('step-assignment')
          .classList.toggle('fb-hidden', !formData.is_multi_step);

        this.closeFormSettings();
        this.showNotification(FB_TRANSLATIONS.formSaved, 'success');

        // Broadcast update to Page Builder
        this.broadcastFormUpdate('updated');
      }
    } catch (error) {
      console.error('Error saving form settings:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
    }
  }

  // =========================================================================
  // Modal Tabs
  // =========================================================================

  initModalTabs() {
    document.querySelectorAll('.modal-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        const modal = tab.closest('.modal-content');
        modal.querySelectorAll('.modal-tab').forEach(t => t.classList.remove('active'));
        modal.querySelectorAll('.modal-tab-content').forEach(c => c.classList.remove('active'));

        tab.classList.add('active');
        modal
          .querySelector(`.modal-tab-content[data-modal-tab-content="${tab.dataset.modalTab}"]`)
          .classList.add('active');
      });
    });
  }

  // =========================================================================
  // Translation Editor (using generic translation API)
  // =========================================================================

  handleTranslateClick(buttonEl) {
    const fieldKey = buttonEl.dataset.fieldKey;
    const modelType = buttonEl.dataset.modelType;
    let objectId, inputEl;

    if (modelType === 'form_builder.formfield') {
      if (!this.selectedField) return;
      objectId = this.selectedField.id;
      const inputMap = {
        label: '#prop-label',
        placeholder: '#prop-placeholder',
        help_text: '#prop-help-text',
      };
      inputEl = document.querySelector(inputMap[fieldKey]);
    } else if (modelType === 'form_builder.form') {
      objectId = this.formId;
      const inputMap = {
        title: '#setting-title',
        description: '#setting-description',
        submit_button_text: '#setting-submit-text',
        success_message: '#setting-success',
        error_message: '#setting-error',
      };
      inputEl = document.querySelector(inputMap[fieldKey]);
    } else if (modelType === 'form_builder.formstep') {
      objectId = document.getElementById('step-edit-id').value;
      if (!objectId) return;
      const inputMap = {
        title: '#step-title',
        description: '#step-description',
        next_button_text: '#step-next-text',
        back_button_text: '#step-back-text',
      };
      inputEl = document.querySelector(inputMap[fieldKey]);
    }

    if (!objectId || !inputEl) return;
    this.openTranslationEditor(modelType, objectId, fieldKey, inputEl, buttonEl);
  }

  async openTranslationEditor(modelType, objectId, fieldKey, fieldInput, triggerBtn) {
    const currentValue = fieldInput.value
      ? fieldInput.value.trim()
      : (fieldInput.textContent || '').trim();
    if (!currentValue) {
      AdminModal.alert({ message: 'Please enter some text before translating.', type: 'warning' });
      return;
    }

    const languages = window.FB_LANGUAGES || [];
    if (languages.length === 0) return;

    const csrfToken = AdminUtils.getCsrfToken();
    const lockEndpointEl = document.getElementById('fb-lock-endpoint');
    const lockEndpoint = lockEndpointEl ? JSON.parse(lockEndpointEl.textContent) : null;

    // Build API endpoints
    const apiBase = '/api/translation/' + modelType + '/' + objectId + '/' + fieldKey;
    const endpoints = {
      status: apiBase + '/status/',
      translate: apiBase + '/translate/',
      save: apiBase + '/save/',
      saveField: apiBase + '/save_field/',
    };

    // Disable trigger button while loading
    if (triggerBtn) {
      triggerBtn.disabled = true;
      triggerBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }

    try {
      // Save current field value first
      const saveResponse = await fetch(endpoints.saveField, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
        body: JSON.stringify({ value: currentValue }),
      });
      if (!saveResponse.ok) {
        const errorData = await saveResponse.json();
        throw new Error(errorData.error || 'Failed to save field value');
      }

      // Fetch translation status
      let existingTranslations = {};
      let coverage = {};
      let lockedFields = {};
      try {
        const statusResponse = await fetch(endpoints.status);
        if (statusResponse.ok) {
          const statusData = await statusResponse.json();
          existingTranslations = statusData.translations || {};
          coverage = statusData.coverage || {};
          lockedFields = statusData.locked_fields || {};
        }
      } catch (err) {
        console.error('Error loading translations:', err);
      }

      // Build and show modal
      this._buildTranslationModal(
        modelType,
        objectId,
        fieldKey,
        currentValue,
        languages,
        existingTranslations,
        coverage,
        lockedFields,
        endpoints,
        csrfToken,
        lockEndpoint,
        fieldInput
      );
    } catch (error) {
      console.error('Error opening translation editor:', error);
      AdminModal.alert({
        message: 'Failed to open translation editor: ' + error.message,
        type: 'error',
      });
    } finally {
      if (triggerBtn) {
        triggerBtn.disabled = false;
        triggerBtn.innerHTML = '<i class="fas fa-globe"></i>';
      }
    }
  }

  _buildTranslationModal(
    modelType,
    objectId,
    fieldKey,
    currentValue,
    languages,
    existingTranslations,
    coverage,
    lockedFields,
    endpoints,
    csrfToken,
    lockEndpoint,
    fieldInput
  ) {
    const self = this;
    const fieldLabel = fieldKey.replace(/_/g, ' ').replace(/\b\w/g, function (l) {
      return l.toUpperCase();
    });
    const charCount = currentValue.length;
    const languageCount = languages.length;

    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'utility-translation-modal';
    modal.style.cssText =
      'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 10100;';

    const modalContent = document.createElement('div');
    modalContent.className = 'utility-popup large utility-translation-editor';
    modalContent.style.cssText =
      'background: var(--body-bg); color: var(--body-fg); border-radius: 8px; max-width: 800px; max-height: 90vh; overflow: auto; box-shadow: 0 4px 20px rgba(0,0,0,0.2);';

    // Header
    const header = document.createElement('div');
    header.className = 'utility-header';
    header.style.cssText =
      'padding: 20px; border-bottom: 1px solid var(--hairline-color); display: flex; justify-content: space-between; align-items: center;';
    header.innerHTML =
      '<h3 class="utility-title" style="margin: 0; color: var(--body-fg);"><i class="fas fa-globe"></i> Manage Translations - ' +
      this.escapeHtml(fieldLabel) +
      '</h3>' +
      '<button type="button" class="utility-close" style="background: none; border: none; font-size: 24px; cursor: pointer; padding: 0; width: 30px; height: 30px; color: var(--body-fg);"><i class="fas fa-times"></i></button>';

    // Body
    const body = document.createElement('div');
    body.className = 'utility-body';
    body.style.cssText = 'padding: 20px;';

    body.innerHTML =
      '<div class="utility-translation-analysis" style="background: var(--darkened-bg); padding: 12px; border-radius: 4px; margin-bottom: 20px;">' +
      '<div style="display: flex; gap: 20px; margin-bottom: 8px;">' +
      '<div class="utility-analysis-item"><span class="utility-analysis-label" style="color: var(--body-quiet-color);">Content Size:</span> <span class="utility-analysis-value" style="color: var(--body-fg); font-weight: bold;">' +
      charCount +
      ' characters</span></div>' +
      '<div class="utility-analysis-item"><span class="utility-analysis-label" style="color: var(--body-quiet-color);">Languages:</span> <span class="utility-analysis-value" style="color: var(--body-fg); font-weight: bold;">' +
      languageCount +
      ' available</span></div>' +
      '<div class="utility-analysis-item"><span class="utility-analysis-label" style="color: var(--body-quiet-color);">Coverage:</span> <span class="utility-analysis-value" style="color: var(--body-fg); font-weight: bold;">' +
      (coverage.percentage || 0) +
      '%</span></div>' +
      '</div>' +
      '<div class="utility-analysis-recommendation" id="te-recommendation" style="color: var(--body-quiet-color); font-size: 0.9em;"></div>' +
      '</div>' +
      '<div style="margin-bottom: 20px;">' +
      '<label style="font-weight: bold; display: block; margin-bottom: 8px; color: var(--body-fg);">Source Text:</label>' +
      '<div id="te-source-text" style="padding: 12px; background: var(--darkened-bg); border-radius: 4px; color: var(--body-fg); max-height: 200px; overflow-y: auto;"></div>' +
      '</div>' +
      '<div style="margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">' +
      '<label style="font-weight: bold; color: var(--body-fg);">Target Languages:</label>' +
      '<div style="display: flex; gap: 8px;">' +
      '<button type="button" class="btn-select-all" style="padding: 4px 12px; font-size: 0.85em; border: 1px solid var(--hairline-color); background: var(--body-bg); color: var(--body-fg); cursor: pointer; border-radius: 4px;"><i class="fas fa-check-double"></i> Select All</button>' +
      '<button type="button" class="btn-select-none" style="padding: 4px 12px; font-size: 0.85em; border: 1px solid var(--hairline-color); background: var(--body-bg); color: var(--body-fg); cursor: pointer; border-radius: 4px;"><i class="fas fa-times"></i> Deselect All</button>' +
      '</div></div>' +
      '<div class="utility-language-list" style="display: flex; flex-direction: column; gap: 12px; max-height: 300px; overflow-y: auto;"></div>';

    // Set source text safely
    const sourceTextEl = body.querySelector('#te-source-text');

    const languagesList = body.querySelector('.utility-language-list');

    // Build language items
    languages.forEach(function (lang) {
      const langItem = document.createElement('div');
      langItem.className = 'utility-language-item';
      langItem.dataset.lang = lang.code;
      const existingTranslation = existingTranslations[lang.code] || '';
      const isTranslated = !!existingTranslation;
      const langLockedFields = lockedFields[lang.code] || [];
      const isLocked = langLockedFields.includes(fieldKey);

      langItem.style.cssText =
        'display: flex; flex-direction: column; gap: 8px; padding: 12px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--darkened-bg);' +
        (isLocked
          ? 'border-left: 3px solid #c62828; opacity: 0.8;'
          : isTranslated
            ? 'border-left: 3px solid var(--info-color);'
            : '');

      const escapedTranslation = self.escapeHtml(existingTranslation);
      const lockBtnStyle =
        'background: ' +
        (isLocked ? '#fce4ec' : 'none') +
        '; border: 1px solid ' +
        (isLocked ? '#c62828' : 'var(--hairline-color)') +
        '; border-radius: 4px; cursor: pointer; color: ' +
        (isLocked ? '#c62828' : 'var(--body-quiet-color)') +
        '; padding: 4px 8px; font-size: 0.85em; transition: all 0.15s;';
      const checkboxAttrs = isLocked ? 'disabled' : isTranslated ? '' : 'checked';
      const translationStatus = isLocked
        ? '<span style="color: #c62828; margin-left: 8px;"><i class="fas fa-lock"></i> Locked</span>'
        : isTranslated
          ? '<span style="color: var(--info-color); margin-left: 8px;"><i class="fas fa-check-circle"></i> Translated</span>'
          : '<span style="color: var(--body-quiet-color); margin-left: 8px;">Not translated</span>';
      const savedBadge =
        isTranslated && !isLocked
          ? '<span class="translation-status-badge" data-lang="' +
            lang.code +
            '" style="padding: 2px 8px; border-radius: 3px; font-size: 0.75em; font-weight: bold; background: var(--success-bg, #d4edda); color: var(--success-color, #28a745); border: 1px solid var(--success-color, #28a745);">Saved</span>'
          : '';
      let editField = '';
      if (isTranslated && !isLocked) {
        editField =
          '<textarea class="translation-edit-field" data-lang="' +
          lang.code +
          '" data-original-value="' +
          escapedTranslation +
          '" placeholder="Edit ' +
          self.escapeHtml(lang.name) +
          ' translation..." style="width: 100%; padding: 8px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--body-bg); color: var(--body-fg); font-family: inherit; font-size: 0.9em; min-height: 60px; resize: vertical;">' +
          escapedTranslation +
          '</textarea>';
      } else if (isLocked && isTranslated) {
        editField =
          '<div style="padding: 8px; background: var(--darkened-bg); border: 1px solid var(--hairline-color); border-radius: 4px; font-size: 0.9em; color: var(--body-quiet-color); opacity: 0.7;">' +
          escapedTranslation.substring(0, 200) +
          (escapedTranslation.length > 200 ? '...' : '') +
          '</div>';
      }

      langItem.innerHTML =
        '<div style="display: flex; align-items: center; gap: 12px;">' +
        '<input type="checkbox" id="te_lang_' +
        lang.code +
        '" value="' +
        lang.code +
        '" ' +
        checkboxAttrs +
        ' style="width: 18px; height: 18px; flex-shrink: 0;">' +
        '<label for="te_lang_' +
        lang.code +
        '" style="flex: 1; margin: 0; color: var(--body-fg);"><strong>' +
        self.escapeHtml(lang.name) +
        '</strong>' +
        translationStatus +
        '</label>' +
        (lockEndpoint
          ? '<button type="button" class="translation-lock-btn" data-lang="' +
            lang.code +
            '" data-locked="' +
            isLocked +
            '" title="' +
            (isLocked ? 'Unlock translation' : 'Lock translation') +
            '" style="' +
            lockBtnStyle +
            '"><i class="fas ' +
            (isLocked ? 'fa-lock' : 'fa-lock-open') +
            '"></i></button>'
          : '') +
        savedBadge +
        '</div>' +
        editField;

      languagesList.appendChild(langItem);
    });

    // Lock button handlers
    if (lockEndpoint) {
      languagesList.querySelectorAll('.translation-lock-btn').forEach(function (btn) {
        btn.addEventListener('click', async function (e) {
          e.preventDefault();
          const langCode = btn.dataset.lang;
          btn.disabled = true;
          const icon = btn.querySelector('i');
          icon.className = 'fas fa-spinner fa-spin';
          try {
            const resp = await fetch(lockEndpoint, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
              body: JSON.stringify({
                content_type: modelType,
                object_id: objectId,
                field_name: fieldKey,
                language: langCode,
              }),
            });
            const data = await resp.json();
            if (data.success) {
              // Re-open modal to refresh lock state
              modal.remove();
              self.openTranslationEditor(modelType, objectId, fieldKey, fieldInput, null);
            }
          } catch (err) {
            console.error('Lock toggle failed:', err);
            icon.className = btn.dataset.locked === 'true' ? 'fas fa-lock' : 'fas fa-lock-open';
          } finally {
            btn.disabled = false;
          }
        });
      });
    }

    // Footer
    const footer = document.createElement('div');
    footer.className = 'utility-footer';
    footer.style.cssText =
      'padding: 20px; border-top: 1px solid var(--hairline-color); display: flex; justify-content: space-between; align-items: center; gap: 12px;';
    footer.innerHTML =
      '<div style="color: var(--body-quiet-color); font-size: 0.9em;"><i class="fas fa-info-circle"></i> Edit existing translations or select languages to translate</div>' +
      '<div style="display: flex; gap: 12px;">' +
      '<button type="button" class="btn btn-cancel" style="padding: 8px 16px; border: 1px solid var(--hairline-color); background: var(--body-bg); color: var(--body-fg); cursor: pointer; border-radius: 4px;">Cancel</button>' +
      '<button type="button" class="btn btn-save" style="padding: 8px 16px; border: 1px solid var(--hairline-color); background: var(--body-bg); color: var(--body-fg); cursor: pointer; border-radius: 4px;"><i class="fas fa-save"></i> Save Edits</button>' +
      '<button type="button" class="btn btn-apply" style="padding: 8px 16px; border: none; background: var(--button-bg); color: var(--button-fg); cursor: pointer; border-radius: 4px;"><i class="fas fa-language"></i> Translate</button>' +
      '</div>';

    // Assemble modal
    modalContent.appendChild(header);
    modalContent.appendChild(body);
    modalContent.appendChild(footer);
    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Set source text safely (after DOM insertion)
    sourceTextEl.textContent = currentValue;

    // Get references
    const closeBtn = header.querySelector('.utility-close');
    const cancelBtn = footer.querySelector('.btn-cancel');
    const saveBtn = footer.querySelector('.btn-save');
    const applyBtn = footer.querySelector('.btn-apply');
    const recommendationEl = body.querySelector('#te-recommendation');
    const selectAllBtn = body.querySelector('.btn-select-all');
    const selectNoneBtn = body.querySelector('.btn-select-none');

    function closeModal() {
      modal.remove();
    }

    function setupChangeTracking() {
      languagesList.querySelectorAll('.translation-edit-field').forEach(function (textarea) {
        textarea.addEventListener('input', function () {
          const lang = this.getAttribute('data-lang');
          const originalValue = this.getAttribute('data-original-value');
          const badge = languagesList.querySelector(
            '.translation-status-badge[data-lang="' + lang + '"]'
          );
          if (badge) {
            if (this.value !== originalValue) {
              badge.style.background = 'var(--warning-bg, #fff3cd)';
              badge.style.color = 'var(--warning-color, #856404)';
              badge.style.borderColor = 'var(--warning-color, #856404)';
              badge.innerHTML = 'Unsaved';
            } else {
              badge.style.background = 'var(--success-bg, #d4edda)';
              badge.style.color = 'var(--success-color, #28a745)';
              badge.style.borderColor = 'var(--success-color, #28a745)';
              badge.innerHTML = 'Saved';
            }
          }
          updateSaveButtonState();
        });
      });
    }

    function updateSaveButtonState() {
      const hasUnsaved = Array.from(languagesList.querySelectorAll('.translation-edit-field')).some(
        function (t) {
          return t.value !== t.getAttribute('data-original-value');
        }
      );
      saveBtn.disabled = !hasUnsaved;
      saveBtn.style.opacity = hasUnsaved ? '1' : '0.6';
    }

    setupChangeTracking();
    updateSaveButtonState();

    // Event listeners
    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) {
      if (e.target === modal) closeModal();
    });
    selectAllBtn.addEventListener('click', function () {
      languagesList
        .querySelectorAll('input[type="checkbox"]:not(:disabled)')
        .forEach(function (cb) {
          cb.checked = true;
        });
    });
    selectNoneBtn.addEventListener('click', function () {
      languagesList
        .querySelectorAll('input[type="checkbox"]:not(:disabled)')
        .forEach(function (cb) {
          cb.checked = false;
        });
    });

    // Save edits handler
    saveBtn.addEventListener('click', async function () {
      const editedTranslations = {};
      let hasEdits = false;
      languagesList.querySelectorAll('.translation-edit-field').forEach(function (textarea) {
        const lang = textarea.getAttribute('data-lang');
        const newValue = textarea.value.trim();
        if (newValue && newValue !== (existingTranslations[lang] || '')) {
          editedTranslations[lang] = newValue;
          hasEdits = true;
        }
      });
      if (!hasEdits) {
        AdminModal.alert('No changes to save.');
        return;
      }
      saveBtn.disabled = true;
      saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
      try {
        const response = await fetch(endpoints.save, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
          body: JSON.stringify({ translations: editedTranslations }),
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Save failed');
        }
        const result = await response.json();
        if (result.success) {
          recommendationEl.innerHTML =
            '<div style="padding: 12px; background: var(--success-bg, #d4edda); border-left: 3px solid var(--success-color, #28a745); color: var(--body-fg); border-radius: 4px;"><strong><i class="fas fa-check-circle"></i> Edits Saved!</strong><br>Successfully saved ' +
            result.saved_languages.length +
            ' translation(s).</div>';
          result.saved_languages.forEach(function (lang) {
            const badge = languagesList.querySelector(
              '.translation-status-badge[data-lang="' + lang + '"]'
            );
            const textarea = languagesList.querySelector(
              '.translation-edit-field[data-lang="' + lang + '"]'
            );
            if (badge) {
              badge.style.background = 'var(--success-bg, #d4edda)';
              badge.style.color = 'var(--success-color, #28a745)';
              badge.style.borderColor = 'var(--success-color, #28a745)';
              badge.innerHTML = 'Saved';
            }
            if (textarea) {
              textarea.setAttribute('data-original-value', self.escapeHtml(textarea.value));
              existingTranslations[lang] = textarea.value;
            }
          });
          saveBtn.disabled = false;
          saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Edits';
          updateSaveButtonState();
        } else {
          throw new Error(result.message || 'Save failed');
        }
      } catch (error) {
        console.error('Save error:', error);
        AdminModal.alert({ message: 'Save failed: ' + error.message, type: 'error' });
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Edits';
      }
    });

    // Translate handler
    applyBtn.addEventListener('click', async function () {
      const selectedLanguages = [];
      languagesList.querySelectorAll('input[type="checkbox"]:checked').forEach(function (cb) {
        selectedLanguages.push(cb.value);
      });
      if (selectedLanguages.length === 0) {
        AdminModal.alert({
          message: 'Please select at least one language to translate to.',
          type: 'warning',
        });
        return;
      }
      const forceImmediate = applyBtn.dataset.forceImmediate === 'true';
      applyBtn.disabled = true;
      applyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Translating...';
      recommendationEl.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> Processing translation...';
      try {
        const response = await fetch(endpoints.translate, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
          body: JSON.stringify({
            text: currentValue,
            languages: selectedLanguages,
            force_immediate: forceImmediate,
          }),
        });
        const result = await response.json();

        if (response.status === 202 && result.recommend_schedule) {
          recommendationEl.innerHTML =
            '<div style="padding: 12px; background: var(--blue-subtle); border-left: 3px solid var(--blue-accent); color: var(--body-fg); border-radius: 4px;"><strong><i class="fas fa-clock"></i> Heavy Workload Detected</strong><br>' +
            result.reason +
            '<br><em>Estimated time: ' +
            result.estimated_time +
            '</em><br><button data-action="te-translate-anyway" style="margin-top: 8px; padding: 6px 12px; background: var(--button-bg); color: var(--button-fg); border: none; border-radius: 4px; cursor: pointer;"><i class="fas fa-bolt"></i> Translate Anyway</button></div>';
          recommendationEl
            .querySelector('[data-action="te-translate-anyway"]')
            .addEventListener('click', function () {
              applyBtn.dataset.forceImmediate = 'true';
              applyBtn.click();
            });
          applyBtn.disabled = false;
          applyBtn.innerHTML = '<i class="fas fa-language"></i> Translate';
          return;
        }

        if (!response.ok) {
          throw new Error(result.error || 'Translation failed');
        }

        if (result.success) {
          recommendationEl.innerHTML =
            '<div style="padding: 12px; background: var(--success-bg, #d4edda); border-left: 3px solid var(--success-color, #28a745); color: var(--body-fg); border-radius: 4px;"><strong><i class="fas fa-check-circle"></i> Translation Complete!</strong><br>Successfully translated to ' +
            result.successful_languages.length +
            ' language(s).</div>';

          // Rebuild language list with new translations
          const allTranslations = Object.assign({}, existingTranslations, result.translations);
          languagesList.innerHTML = '';

          languages.forEach(function (lang) {
            const langItem = document.createElement('div');
            langItem.className = 'utility-language-item';
            const translation = allTranslations[lang.code] || '';
            const isTranslated = !!translation;
            langItem.style.cssText =
              'display: flex; flex-direction: column; gap: 8px; padding: 12px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--darkened-bg);' +
              (isTranslated ? 'border-left: 3px solid var(--info-color);' : '');
            const escapedTranslation = self.escapeHtml(translation);
            const isNew = result.successful_languages.includes(lang.code);
            const savedBadge2 = isTranslated
              ? '<span class="translation-status-badge" data-lang="' +
                lang.code +
                '" style="padding: 2px 8px; border-radius: 3px; font-size: 0.75em; font-weight: bold; background: var(--success-bg, #d4edda); color: var(--success-color, #28a745); border: 1px solid var(--success-color, #28a745);">Saved</span>'
              : '';
            const editField2 = isTranslated
              ? '<textarea class="translation-edit-field" data-lang="' +
                lang.code +
                '" data-original-value="' +
                escapedTranslation +
                '" placeholder="Edit ' +
                self.escapeHtml(lang.name) +
                ' translation..." style="width: 100%; padding: 8px; border: 1px solid var(--hairline-color); border-radius: 4px; background: var(--body-bg); color: var(--body-fg); font-family: inherit; font-size: 0.9em; min-height: 60px; resize: vertical;">' +
                escapedTranslation +
                '</textarea>'
              : '';
            langItem.innerHTML =
              '<div style="display: flex; align-items: center; gap: 12px;"><input type="checkbox" id="te_lang_' +
              lang.code +
              '" value="' +
              lang.code +
              '" ' +
              (isTranslated ? '' : 'checked') +
              ' style="width: 18px; height: 18px; flex-shrink: 0;"><label for="te_lang_' +
              lang.code +
              '" style="flex: 1; margin: 0; color: var(--body-fg);"><strong>' +
              self.escapeHtml(lang.name) +
              '</strong>' +
              (isTranslated
                ? '<span style="color: var(--info-color); margin-left: 8px;"><i class="fas fa-check-circle"></i> Translated' +
                  (isNew ? ' (New)' : '') +
                  '</span>'
                : '<span style="color: var(--body-quiet-color); margin-left: 8px;">Not translated</span>') +
              '</label>' +
              savedBadge2 +
              '</div>' +
              editField2;
            languagesList.appendChild(langItem);
          });

          // Update existingTranslations reference and coverage
          Object.assign(existingTranslations, result.translations);
          const translatedCount = Object.keys(allTranslations).length;
          const totalCount = languages.length;
          const analysisItems = body.querySelectorAll('.utility-analysis-item');
          if (analysisItems.length >= 3) {
            const coverageEl = analysisItems[2].querySelector('.utility-analysis-value');
            if (coverageEl)
              coverageEl.textContent = ((translatedCount / totalCount) * 100).toFixed(1) + '%';
          }
          applyBtn.disabled = false;
          applyBtn.innerHTML = '<i class="fas fa-language"></i> Translate';
          applyBtn.dataset.forceImmediate = 'false';
          setupChangeTracking();
          updateSaveButtonState();
        } else {
          throw new Error(result.message || 'Translation failed');
        }
      } catch (error) {
        console.error('Translation error:', error);
        recommendationEl.innerHTML =
          '<div style="color: var(--error-color);"><i class="fas fa-exclamation-triangle"></i> ' +
          error.message +
          '</div>';
        AdminModal.alert({ message: 'Translation failed: ' + error.message, type: 'error' });
        applyBtn.disabled = false;
        applyBtn.innerHTML = '<i class="fas fa-language"></i> Translate';
      }
    });
  }

  // =========================================================================
  // Conditional Rules Management
  // =========================================================================

  /**
   * Initialize rules management UI
   */
  initRulesManagement() {
    // Update rule count badge on init
    this.updateRuleCountBadge();

    // Set up event listeners for rule editor form changes
    const sourceFieldSelect = document.getElementById('rule-source-field');
    const actionSelect = document.getElementById('rule-action');

    if (sourceFieldSelect) {
      sourceFieldSelect.addEventListener('change', () => this.updateOperatorOptions());
    }

    if (actionSelect) {
      actionSelect.addEventListener('change', () => this.updateActionTargets());
    }
  }

  /**
   * Open the rules manager modal
   */
  openRulesModal() {
    this.renderRulesList();
    document.getElementById('rules-modal').classList.remove('fb-hidden');
  }

  /**
   * Close the rules manager modal
   */
  closeRulesModal() {
    document.getElementById('rules-modal').classList.add('fb-hidden');
  }

  /**
   * Render the list of rules in the rules manager modal
   */
  renderRulesList() {
    const container = document.getElementById('rules-list');

    if (!this.rules || this.rules.length === 0) {
      container.innerHTML = `
                <div class="no-rules-message">
                    <i class="fas fa-code-branch"></i>
                    <p>${FB_TRANSLATIONS.noRules || 'No conditional rules defined yet. Add a rule to create branching logic.'}</p>
                </div>
            `;
      return;
    }

    container.innerHTML = this.rules
      .map(rule => {
        const sourceField = this.fields.find(f => f.id === rule.source_field_id);
        const sourceLabel = sourceField
          ? sourceField.label
          : rule.source_field_label || 'Unknown Field';
        const operatorLabel = window.FB_OPERATORS[rule.operator] || rule.operator;
        const actionLabel = window.FB_ACTIONS[rule.action] || rule.action;

        // Build target description
        let targetDescription = '';
        if (rule.action.includes('field')) {
          const targetField = this.fields.find(f => f.id === rule.target_field_id);
          targetDescription = targetField
            ? targetField.label
            : rule.target_field_label || 'Unknown Field';
        } else if (rule.action.includes('step')) {
          const targetStep = this.steps.find(s => s.id === rule.target_step_id);
          targetDescription = targetStep
            ? targetStep.title
            : rule.target_step_title || 'Unknown Step';
        }

        // Format the value for display
        let valueDisplay = '';
        if (rule.value && typeof rule.value === 'object') {
          if (rule.value.value !== undefined) {
            valueDisplay = rule.value.value;
          } else if (Array.isArray(rule.value)) {
            valueDisplay = rule.value.join(', ');
          }
        } else if (rule.value) {
          valueDisplay = rule.value;
        }

        return `
                <div class="rule-card ${rule.is_active ? '' : 'inactive'}" data-rule-id="${rule.id}">
                    <div class="rule-toggle">
                        <label class="switch">
                            <input type="checkbox" ${rule.is_active ? 'checked' : ''}
                                   onchange="formBuilder.toggleRuleActive(${rule.id}, this.checked)">
                            <span class="slider"></span>
                        </label>
                    </div>
                    <div class="rule-info">
                        <div class="rule-name">${rule.name || `Rule #${rule.id}`}</div>
                        <div class="rule-description">
                            <span class="rule-condition">
                                <strong>IF</strong> "${sourceLabel}" ${operatorLabel.toLowerCase()} ${valueDisplay ? `"${valueDisplay}"` : ''}
                            </span>
                            <span class="rule-action-text">
                                <strong>THEN</strong> ${actionLabel.toLowerCase()} ${targetDescription ? `"${targetDescription}"` : ''}
                            </span>
                        </div>
                    </div>
                    <div class="rule-actions">
                        <button class="rule-action-btn edit" onclick="formBuilder.editRule(${rule.id})" title="${FB_TRANSLATIONS.edit || 'Edit'}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="rule-action-btn delete" onclick="formBuilder.deleteRule(${rule.id})" title="${FB_TRANSLATIONS.delete || 'Delete'}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
      })
      .join('');
  }

  /**
   * Open the rule editor modal
   * @param {number|null} ruleId - Rule ID to edit, or null for new rule
   */
  openRuleEditor(ruleId = null) {
    this.editingRuleId = ruleId;
    const isNew = !ruleId;
    const rule = ruleId ? this.rules.find(r => r.id === ruleId) : null;

    // Update modal title
    document.getElementById('rule-editor-title').textContent = isNew
      ? FB_TRANSLATIONS.addRule || 'Add Rule'
      : FB_TRANSLATIONS.editRule || 'Edit Rule';

    // Populate field selects
    this.populateFieldSelects();

    // Reset or populate form
    document.getElementById('rule-name').value = rule ? rule.name : '';
    document.getElementById('rule-source-field').value = rule ? rule.source_field_id : '';
    document.getElementById('rule-operator').value = rule ? rule.operator : 'equals';

    // Handle value - it's stored as an object with a 'value' key
    const valueField = document.getElementById('rule-value');
    if (rule && rule.value) {
      if (typeof rule.value === 'object' && rule.value.value !== undefined) {
        valueField.value = rule.value.value;
      } else if (typeof rule.value === 'string') {
        valueField.value = rule.value;
      } else {
        valueField.value = '';
      }
    } else {
      valueField.value = '';
    }

    document.getElementById('rule-action').value = rule ? rule.action : 'show_field';
    document.getElementById('rule-target-field').value = rule ? rule.target_field_id || '' : '';
    document.getElementById('rule-target-step').value = rule ? rule.target_step_id || '' : '';
    document.getElementById('rule-priority').value = rule ? rule.priority : 0;

    // Update dynamic UI based on selections
    this.updateOperatorOptions();
    this.updateActionTargets();

    // Show modal
    document.getElementById('rule-editor-modal').classList.remove('fb-hidden');
  }

  /**
   * Close the rule editor modal
   */
  closeRuleEditor() {
    document.getElementById('rule-editor-modal').classList.add('fb-hidden');
    this.editingRuleId = null;
  }

  /**
   * Populate the source and target field select dropdowns
   */
  populateFieldSelects() {
    const sourceSelect = document.getElementById('rule-source-field');
    const targetFieldSelect = document.getElementById('rule-target-field');
    const targetStepSelect = document.getElementById('rule-target-step');

    // Clear existing options
    sourceSelect.innerHTML = `<option value="">${FB_TRANSLATIONS.selectField || 'Select a field...'}</option>`;
    targetFieldSelect.innerHTML = `<option value="">${FB_TRANSLATIONS.selectField || 'Select a field...'}</option>`;
    targetStepSelect.innerHTML = `<option value="">${FB_TRANSLATIONS.selectStep || 'Select a step...'}</option>`;

    // Populate source field (fields that can trigger rules)
    const triggerableFields = this.fields.filter(
      f => !['heading', 'paragraph', 'divider', 'hidden'].includes(f.field_type)
    );
    triggerableFields.forEach(field => {
      const option = document.createElement('option');
      option.value = field.id;
      option.textContent = field.label;
      sourceSelect.appendChild(option);
    });

    // Populate target fields
    this.fields.forEach(field => {
      const option = document.createElement('option');
      option.value = field.id;
      option.textContent = field.label;
      targetFieldSelect.appendChild(option);
    });

    // Populate target steps
    this.steps.forEach(step => {
      const option = document.createElement('option');
      option.value = step.id;
      option.textContent = step.title;
      targetStepSelect.appendChild(option);
    });
  }

  /**
   * Update available operators based on source field type
   */
  updateOperatorOptions() {
    const sourceFieldId = document.getElementById('rule-source-field').value;
    const operatorSelect = document.getElementById('rule-operator');
    const valueContainer = document.getElementById('rule-value-group');
    const currentOperator = operatorSelect.value;

    // Get source field type
    const sourceField = this.fields.find(f => f.id == sourceFieldId);
    const fieldType = sourceField ? sourceField.field_type : 'text';

    // Define operators by field type
    const textOperators = [
      'equals',
      'not_equals',
      'contains',
      'not_contains',
      'starts_with',
      'ends_with',
      'is_empty',
      'is_not_empty',
    ];
    const numberOperators = [
      'equals',
      'not_equals',
      'greater_than',
      'less_than',
      'greater_than_or_equal',
      'less_than_or_equal',
      'is_empty',
      'is_not_empty',
    ];
    const selectOperators = [
      'equals',
      'not_equals',
      'in_list',
      'not_in_list',
      'is_empty',
      'is_not_empty',
    ];
    const boolOperators = ['equals', 'not_equals'];

    let operators;
    switch (fieldType) {
      case 'number':
      case 'rating_stars':
      case 'rating_nps':
        operators = numberOperators;
        break;
      case 'select':
      case 'radio':
      case 'checkbox_group':
        operators = selectOperators;
        break;
      case 'checkbox':
        operators = boolOperators;
        break;
      default:
        operators = textOperators;
    }

    // Rebuild operator select
    operatorSelect.innerHTML = operators
      .map(op => `<option value="${op}">${window.FB_OPERATORS[op] || op}</option>`)
      .join('');

    // Restore selection if still valid
    if (operators.includes(currentOperator)) {
      operatorSelect.value = currentOperator;
    }

    // Show/hide value input based on operator
    const noValueOperators = ['is_empty', 'is_not_empty'];
    if (valueContainer) {
      valueContainer.style.display = noValueOperators.includes(operatorSelect.value)
        ? 'none'
        : 'block';
    }

    // Update value container visibility on operator change
    operatorSelect.onchange = () => {
      if (valueContainer) {
        valueContainer.style.display = noValueOperators.includes(operatorSelect.value)
          ? 'none'
          : 'block';
      }
    };
  }

  /**
   * Update target field/step visibility based on selected action
   */
  updateActionTargets() {
    const action = document.getElementById('rule-action').value;
    const targetFieldContainer = document.getElementById('rule-target-field-group');
    const targetStepContainer = document.getElementById('rule-target-step-group');
    const actionValueContainer = document.getElementById('rule-action-value-group');

    // Hide all first
    if (targetFieldContainer) targetFieldContainer.style.display = 'none';
    if (targetStepContainer) targetStepContainer.classList.add('fb-hidden');
    if (actionValueContainer) actionValueContainer.classList.add('fb-hidden');

    // Show appropriate container based on action
    if (
      ['show_field', 'hide_field', 'require_field', 'unrequire_field', 'set_value'].includes(action)
    ) {
      if (targetFieldContainer) targetFieldContainer.style.display = 'block';
      if (action === 'set_value' && actionValueContainer) {
        actionValueContainer.classList.remove('fb-hidden');
      }
    } else if (['skip_to_step', 'show_step', 'hide_step'].includes(action)) {
      if (targetStepContainer) targetStepContainer.classList.remove('fb-hidden');
    }
  }

  /**
   * Save the rule (create or update)
   */
  async saveRule() {
    const isNew = !this.editingRuleId;

    // Gather form data
    const sourceFieldId = document.getElementById('rule-source-field').value;
    const operator = document.getElementById('rule-operator').value;
    const value = document.getElementById('rule-value').value;
    const action = document.getElementById('rule-action').value;
    const targetFieldId = document.getElementById('rule-target-field').value;
    const targetStepId = document.getElementById('rule-target-step').value;
    const name = document.getElementById('rule-name').value;
    const priority = parseInt(document.getElementById('rule-priority').value) || 0;

    // Validation
    if (!sourceFieldId) {
      this.showNotification(
        FB_TRANSLATIONS.selectSourceField || 'Please select a source field',
        'error'
      );
      return;
    }

    // Check if value is required based on operator
    const noValueOperators = ['is_empty', 'is_not_empty'];
    if (!noValueOperators.includes(operator) && !value) {
      this.showNotification(
        FB_TRANSLATIONS.enterValue || 'Please enter a comparison value',
        'error'
      );
      return;
    }

    // Check target based on action
    const fieldActions = [
      'show_field',
      'hide_field',
      'require_field',
      'unrequire_field',
      'set_value',
    ];
    const stepActions = ['skip_to_step', 'show_step', 'hide_step'];

    if (fieldActions.includes(action) && !targetFieldId) {
      this.showNotification(
        FB_TRANSLATIONS.selectTargetField || 'Please select a target field',
        'error'
      );
      return;
    }

    if (stepActions.includes(action) && !targetStepId) {
      this.showNotification(
        FB_TRANSLATIONS.selectTargetStep || 'Please select a target step',
        'error'
      );
      return;
    }

    const ruleData = {
      name: name,
      source_field_id: parseInt(sourceFieldId),
      operator: operator,
      value: { value: value }, // Store value as object for flexibility
      action: action,
      target_field_id: targetFieldId ? parseInt(targetFieldId) : null,
      target_step_id: targetStepId ? parseInt(targetStepId) : null,
      priority: priority,
      is_active: true,
    };

    try {
      let response;
      if (isNew) {
        response = await this.apiRequest('POST', `${this.baseUrl}/builder/rules/add/`, ruleData);
      } else {
        response = await this.apiRequest(
          'POST',
          `${this.baseUrl}/builder/rules/${this.editingRuleId}/update/`,
          ruleData
        );
      }

      if (response.success) {
        // Update local state
        if (isNew) {
          this.rules.push(response.rule);
        } else {
          const index = this.rules.findIndex(r => r.id === this.editingRuleId);
          if (index !== -1) {
            this.rules[index] = response.rule;
          }
        }

        this.closeRuleEditor();
        this.renderRulesList();
        this.updateRuleCountBadge();
        this.showNotification(
          isNew
            ? FB_TRANSLATIONS.ruleAdded || 'Rule added'
            : FB_TRANSLATIONS.ruleUpdated || 'Rule updated',
          'success'
        );
      }
    } catch (error) {
      console.error('Error saving rule:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed || 'Save failed', 'error');
    }
  }

  /**
   * Edit an existing rule
   * @param {number} ruleId - Rule ID to edit
   */
  editRule(ruleId) {
    this.openRuleEditor(ruleId);
  }

  /**
   * Delete a rule
   * @param {number} ruleId - Rule ID to delete
   */
  async deleteRule(ruleId) {
    if (
      !(await AdminModal.confirm({
        message: FB_TRANSLATIONS.confirmDeleteRule || 'Are you sure you want to delete this rule?',
        danger: true,
        confirmText: 'Delete',
      }))
    ) {
      return;
    }

    try {
      const response = await this.apiRequest(
        'POST',
        `${this.baseUrl}/builder/rules/${ruleId}/delete/`
      );

      if (response.success) {
        // Remove from local state
        this.rules = this.rules.filter(r => r.id !== ruleId);

        this.renderRulesList();
        this.updateRuleCountBadge();
        this.showNotification(FB_TRANSLATIONS.ruleDeleted || 'Rule deleted', 'success');
      }
    } catch (error) {
      console.error('Error deleting rule:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed || 'Delete failed', 'error');
    }
  }

  /**
   * Toggle rule active state
   * @param {number} ruleId - Rule ID
   * @param {boolean} isActive - New active state
   */
  async toggleRuleActive(ruleId, isActive) {
    try {
      const response = await this.apiRequest(
        'POST',
        `${this.baseUrl}/builder/rules/${ruleId}/update/`,
        { is_active: isActive }
      );

      if (response.success) {
        const rule = this.rules.find(r => r.id === ruleId);
        if (rule) {
          rule.is_active = isActive;
        }

        // Update card styling
        const card = document.querySelector(`.rule-card[data-rule-id="${ruleId}"]`);
        if (card) {
          card.classList.toggle('inactive', !isActive);
        }
      }
    } catch (error) {
      console.error('Error toggling rule:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed || 'Update failed', 'error');
    }
  }

  /**
   * Update the rule count badge in the sidebar
   */
  updateRuleCountBadge() {
    const badge = document.getElementById('rule-count-badge');
    if (badge) {
      const activeCount = this.rules.filter(r => r.is_active).length;
      if (activeCount > 0) {
        badge.textContent = activeCount;
        badge.classList.remove('fb-hidden');
      } else {
        badge.classList.add('fb-hidden');
      }
    }
  }

  /**
   * Render conditions for a field (for properties panel)
   */
  renderConditions(field) {
    // Get rules that target this field
    const targetingRules = this.rules.filter(r => r.target_field_id === field.id);
    const conditionsList = document.getElementById('conditions-list');

    if (!conditionsList) return;

    if (targetingRules.length === 0) {
      conditionsList.innerHTML = `<p class="no-conditions">${FB_TRANSLATIONS.noConditions || 'No conditions set'}</p>`;
      return;
    }

    conditionsList.innerHTML = targetingRules
      .map(rule => {
        const sourceField = this.fields.find(f => f.id === rule.source_field_id);
        const sourceLabel = sourceField ? sourceField.label : 'Unknown';
        return `
                <div class="condition-preview">
                    <span class="condition-text">
                        ${window.FB_ACTIONS[rule.action] || rule.action} when "${sourceLabel}" ${window.FB_OPERATORS[rule.operator] || rule.operator}
                    </span>
                    <button class="edit-condition-btn" onclick="formBuilder.editRule(${rule.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                </div>
            `;
      })
      .join('');
  }

  // Legacy method for compatibility
  openConditionEditor() {
    this.openRulesModal();
  }

  closeConditionModal() {
    this.closeRulesModal();
  }

  saveConditions() {
    // Handled by saveRule now
    this.closeRulesModal();
  }

  // =========================================================================
  // Delete Modal
  // =========================================================================

  closeDeleteModal() {
    document.getElementById('delete-modal').classList.add('fb-hidden');
    this.pendingDeleteType = null;
    this.pendingDeleteId = null;
  }

  // =========================================================================
  // Save & Persistence
  // =========================================================================

  markDirty() {
    this.isDirty = true;
    this.scheduleAutoSave();
  }

  scheduleAutoSave() {
    if (this.autoSaveTimer) {
      clearTimeout(this.autoSaveTimer);
    }
    this.autoSaveTimer = setTimeout(() => this.autoSave(), this.autoSaveDelay);
  }

  async autoSave() {
    if (!this.isDirty) return;

    document.getElementById('auto-save-indicator').classList.remove('fb-hidden');

    try {
      await this.save(true);
    } finally {
      document.getElementById('auto-save-indicator').classList.add('fb-hidden');
    }
  }

  async save(silent = false) {
    try {
      const formData = {
        name: this.form.name,
        title: this.form.title,
        description: this.form.description,
      };

      const response = await this.apiRequest('POST', `${this.baseUrl}/builder/save/`, {
        form: formData,
      });

      if (response.success) {
        this.isDirty = false;
        if (!silent) {
          this.showNotification(FB_TRANSLATIONS.formSaved, 'success');
        }
        // Broadcast update to Page Builder
        this.broadcastFormUpdate('updated');
      }
    } catch (error) {
      console.error('Error saving form:', error);
      if (!silent) {
        this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
      }
    }
  }

  async saveAndClose() {
    await this.save();
    // Broadcast one final time before closing
    this.broadcastFormUpdate('updated');
    const langMatch = window.location.pathname.match(/^\/([a-z]{2})\//);
    const langPrefix = langMatch ? `/${langMatch[1]}` : '';
    window.location.href = `${langPrefix}/admin/form_builder/form/`;
  }

  async saveFieldOrder(fieldIds) {
    try {
      await this.apiRequest('POST', `${this.baseUrl}/fields/reorder/`, { field_order: fieldIds });
    } catch (error) {
      console.error('Error saving field order:', error);
    }
  }

  async duplicateForm() {
    try {
      const response = await this.apiRequest('POST', `${this.baseUrl}/duplicate/`);

      if (response.redirect) {
        window.location.href = response.redirect;
      }
    } catch (error) {
      console.error('Error duplicating form:', error);
      this.showNotification(FB_TRANSLATIONS.saveFailed, 'error');
    }
  }

  // =========================================================================
  // Preview
  // =========================================================================

  previewForm() {
    const url = `${this.baseUrl}/preview/`;
    window.open(url, '_blank', 'width=800,height=600');
  }

  // =========================================================================
  // History (Undo/Redo)
  // =========================================================================

  saveHistoryState() {
    const state = {
      fields: JSON.parse(JSON.stringify(this.fields)),
      steps: JSON.parse(JSON.stringify(this.steps)),
      form: JSON.parse(JSON.stringify(this.form)),
    };

    // Remove any redo states
    this.history = this.history.slice(0, this.historyIndex + 1);

    // Add new state
    this.history.push(state);
    this.historyIndex++;

    // Limit history size
    if (this.history.length > this.maxHistorySize) {
      this.history.shift();
      this.historyIndex--;
    }

    this.updateHistoryButtons();
  }

  undo() {
    if (this.historyIndex <= 0) return;

    this.historyIndex--;
    this.restoreHistoryState(this.history[this.historyIndex]);
    this.updateHistoryButtons();
  }

  redo() {
    if (this.historyIndex >= this.history.length - 1) return;

    this.historyIndex++;
    this.restoreHistoryState(this.history[this.historyIndex]);
    this.updateHistoryButtons();
  }

  restoreHistoryState(state) {
    this.fields = JSON.parse(JSON.stringify(state.fields));
    this.steps = JSON.parse(JSON.stringify(state.steps));
    this.form = JSON.parse(JSON.stringify(state.form));

    // Re-render everything
    this.refreshAllFields();
    this.refreshStepUI();
    this.markDirty();
  }

  refreshAllFields() {
    const container = document.getElementById('fields-container');
    container.innerHTML = '';

    if (this.fields.length === 0) {
      container.innerHTML = `
                <div class="empty-drop-zone" id="empty-drop-zone">
                    <i class="fas fa-plus-circle"></i>
                    <p>Drag fields here to start building your form</p>
                </div>
            `;
      this.initFieldLibraryDrag();
    } else {
      this.fields.forEach(field => this.renderField(field));
    }
  }

  updateHistoryButtons() {
    const undoBtn = document.getElementById('undo-btn');
    const redoBtn = document.getElementById('redo-btn');

    if (undoBtn) {
      undoBtn.disabled = this.historyIndex <= 0;
    }
    if (redoBtn) {
      redoBtn.disabled = this.historyIndex >= this.history.length - 1;
    }
  }

  // =========================================================================
  // Keyboard Shortcuts
  // =========================================================================

  initKeyboardShortcuts() {
    document.addEventListener('keydown', e => {
      // Ctrl/Cmd + S = Save
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        this.save();
      }

      // Ctrl/Cmd + Z = Undo
      if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        this.undo();
      }

      // Ctrl/Cmd + Shift + Z or Ctrl/Cmd + Y = Redo
      if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
        e.preventDefault();
        this.redo();
      }

      // Delete/Backspace = Delete selected field
      if ((e.key === 'Delete' || e.key === 'Backspace') && this.selectedField) {
        // Don't delete if focus is in an input
        if (!['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
          e.preventDefault();
          this.deleteField(this.selectedField.id);
        }
      }

      // Escape = Deselect
      if (e.key === 'Escape') {
        this.deselectField();
      }
    });
  }

  // =========================================================================
  // API Helper
  // =========================================================================

  async apiRequest(method, url, data = null) {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': window.csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
      },
    };

    if (data && method !== 'GET') {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  }

  // =========================================================================
  // Notifications
  // =========================================================================

  showNotification(message, type = 'info') {
    // Simple notification - could be enhanced with a toast library
    console.log(`[${type.toUpperCase()}] ${message}`);

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `fb-toast fb-toast-${type}`;
    toast.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
            <span>${message}</span>
        `;

    // Add styles if not already present
    if (!document.getElementById('fb-toast-styles')) {
      const style = document.createElement('style');
      style.id = 'fb-toast-styles';
      style.textContent = `
                .fb-toast {
                    position: fixed;
                    bottom: 24px;
                    right: 24px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    padding: 12px 20px;
                    background: var(--fb-bg-primary);
                    border-radius: var(--fb-radius);
                    box-shadow: var(--fb-shadow-lg);
                    font-size: 14px;
                    z-index: 10000;
                    animation: slideInRight 0.3s ease;
                }
                .fb-toast-success { border-left: 4px solid var(--fb-success); }
                .fb-toast-success i { color: var(--fb-success); }
                .fb-toast-error { border-left: 4px solid var(--fb-error); }
                .fb-toast-error i { color: var(--fb-error); }
                .fb-toast-info { border-left: 4px solid var(--fb-info); }
                .fb-toast-info i { color: var(--fb-info); }
                @keyframes slideInRight {
                    from { opacity: 0; transform: translateX(20px); }
                    to { opacity: 1; transform: translateX(0); }
                }
            `;
      document.head.appendChild(style);
    }

    document.body.appendChild(toast);

    // Remove after delay
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(20px)';
      toast.style.transition = '0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }
}

// =========================================================================
// CSRF Token Setup (read from data island — cookie is httpOnly)
// =========================================================================
(function () {
  const el = document.getElementById('fb-csrf-token');
  if (el) {
    try {
      window.csrfToken = JSON.parse(el.textContent);
    } catch (e) {
      window.csrfToken = '';
    }
  } else {
    window.csrfToken = '';
  }
})();

// =========================================================================
// Data Island Initialization & Event Delegation
// =========================================================================
document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  function readIsland(id, fallback) {
    const el = document.getElementById(id);
    if (!el) return fallback;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return fallback;
    }
  }

  const formData = readIsland('fb-form-data', null);
  if (!formData) return;

  const fieldsData = readIsland('fb-fields-data', []);
  const stepsData = readIsland('fb-steps-data', []);
  const rulesData = readIsland('fb-rules-data', []);

  window.FB_LANGUAGES = readIsland('fb-languages', []);
  window.FB_PRIMARY_LANGUAGE = readIsland('fb-primary-language', { code: 'en', name: 'English' });
  window.FIELD_TYPES = readIsland('fb-field-types', {});
  window.FB_TRANSLATIONS = readIsland('fb-translations', {});
  window.FB_OPERATORS = readIsland('fb-operators', {});
  window.FB_ACTIONS = readIsland('fb-actions', {});

  window.formBuilder = new FormBuilder(formData, fieldsData, stepsData, rulesData);

  const ruleAction = document.getElementById('rule-action');
  if (ruleAction) {
    ruleAction.addEventListener('change', function () {
      if (window.formBuilder) window.formBuilder.updateActionTargets();
    });
  }

  document.addEventListener('click', function (e) {
    const menu = document.getElementById('saveDropdownMenu');
    if (menu && !e.target.closest('.save-dropdown-wrapper')) {
      menu.classList.remove('show');
    }
  });

  document.addEventListener('click', function (e) {
    const el = e.target.closest('[data-action]');
    if (!el) return;
    const action = el.dataset.action;
    const fb = window.formBuilder;
    if (!fb) return;

    switch (action) {
      case 'fb-undo':
        fb.undo();
        break;
      case 'fb-redo':
        fb.redo();
        break;
      case 'fb-preview':
        fb.previewForm();
        break;
      case 'fb-save':
        fb.save();
        break;
      case 'fb-toggle-save-dropdown':
        e.stopPropagation();
        var menu = document.getElementById('saveDropdownMenu');
        if (menu) menu.classList.toggle('show');
        break;
      case 'fb-save-and-close':
        fb.saveAndClose();
        break;
      case 'fb-duplicate-form':
        fb.duplicateForm();
        break;
      case 'fb-open-rules-modal':
        fb.openRulesModal();
        break;
      case 'fb-add-step':
        fb.addStep();
        break;
      case 'fb-edit-step':
        fb.editStep(parseInt(el.dataset.stepId, 10));
        break;
      case 'fb-delete-step':
        fb.deleteStep(parseInt(el.dataset.stepId, 10));
        break;
      case 'fb-duplicate-field':
        fb.duplicateField(parseInt(el.dataset.fieldId, 10));
        break;
      case 'fb-delete-field':
        fb.deleteField(parseInt(el.dataset.fieldId, 10));
        break;
      case 'fb-select-field':
        fb.selectField(parseInt(el.dataset.fieldId, 10));
        break;
      case 'fb-deselect-field':
        fb.deselectField();
        break;
      case 'fb-open-translation-editor':
        fb.handleTranslateClick(el);
        break;
      case 'fb-add-option':
        fb.addOption();
        break;
      case 'fb-open-condition-editor':
        fb.openConditionEditor();
        break;
      case 'fb-open-form-settings':
        fb.openFormSettings();
        break;
      case 'fb-close-form-settings':
        fb.closeFormSettings();
        break;
      case 'fb-save-form-settings':
        fb.saveFormSettings();
        break;
      case 'fb-close-step-modal':
        fb.closeStepModal();
        break;
      case 'fb-save-step':
        fb.saveStep();
        break;
      case 'fb-close-rules-modal':
        fb.closeRulesModal();
        break;
      case 'fb-open-rule-editor':
        fb.openRuleEditor();
        break;
      case 'fb-close-rule-editor':
        fb.closeRuleEditor();
        break;
      case 'fb-save-rule':
        fb.saveRule();
        break;
      case 'fb-close-delete-modal':
        fb.closeDeleteModal();
        break;
      case 'fb-confirm-delete':
        fb.confirmDelete();
        break;
      case 'fb-remove-option':
        fb.removeOption(parseInt(el.dataset.optionIndex, 10));
        break;
    }
  });

  document.addEventListener('change', function (e) {
    const el = e.target.closest('[data-action]');
    if (!el) return;
    const fb = window.formBuilder;
    if (!fb) return;

    if (el.dataset.action === 'fb-update-option') {
      fb.updateOption(parseInt(el.dataset.optionIndex, 10), el.value);
    }
  });
});
