/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Property Renderer System for Page Builder
 *
 * Maps property types to utility classes and handles initialization
 */

class PropertyRenderer {
  constructor() {
    // Map property types to utility classes
    this.utilityMap = {
      color_advanced: 'ColorPickerUtility',
      gradient: 'GradientCreatorUtility',
      border_advanced: 'BorderEditorUtility',
      shadow: 'ShadowEditor',
      spacing: 'SpacingEditor',
      typography: 'TypographyEditor',
      translation: 'TranslationEditor',
      background: 'BackgroundEditor',
      visibility_rules: 'VisibilityRulesEditor',
      form_select: 'FormSelectorUtility',
      focal_point: 'FocalPointEditor',
      icon_picker: 'IconPickerUtility',
    };

    // Store active utility instances for cleanup
    this.activeUtilities = new Map();

    // Store current element config and values for show_when conditions
    this.currentElementConfig = null;
    this.currentElementData = null;
    this.currentValues = {};

    // Track properties that have show_when dependents
    this.showWhenDependents = new Map();

    // Track previous tag value for heading elements
    this.previousTagValue = null;
  }

  /**
   * Check if a property should be shown based on show_when/show_if condition
   * @param {Object} propConfig - Property configuration
   * @param {Object} values - Current property values
   * @returns {boolean} - Whether property should be shown
   *
   * Supports two formats:
   * 1. show_when: {"property": "field_name", "value": "value"} or {"property": "field_name", "values": ["v1", "v2"]}
   * 2. show_if: {"field_name": "value"} or {"field_name": ["v1", "v2"]} (simpler shorthand)
   */
  shouldShowProperty(propConfig, values) {
    // Check for show_when format
    if (propConfig.show_when) {
      const condition = propConfig.show_when;
      const dependentProp = condition.property;
      const currentValue = values[dependentProp];

      // Support both single value and array of values
      const allowedValues = condition.values || [condition.value];
      return allowedValues.includes(currentValue);
    }

    // Check for show_if format (simpler shorthand)
    if (propConfig.show_if) {
      for (const [dependentProp, expectedValue] of Object.entries(propConfig.show_if)) {
        const currentValue = values[dependentProp];
        // Support both single value and array of values
        const allowedValues = Array.isArray(expectedValue) ? expectedValue : [expectedValue];
        if (!allowedValues.includes(currentValue)) {
          return false;
        }
      }
      return true;
    }

    return true;
  }

  /**
   * Build a map of which properties have show_when/show_if dependents
   * @param {Object} properties - Flattened properties object
   */
  buildShowWhenDependentsMap(properties) {
    this.showWhenDependents.clear();

    for (const [propKey, propConfig] of Object.entries(properties)) {
      // Handle show_when format
      if (propConfig.show_when) {
        const dependentProp = propConfig.show_when.property;
        if (!this.showWhenDependents.has(dependentProp)) {
          this.showWhenDependents.set(dependentProp, []);
        }
        this.showWhenDependents.get(dependentProp).push(propKey);
      }
      // Handle show_if format (simpler shorthand)
      if (propConfig.show_if) {
        for (const dependentProp of Object.keys(propConfig.show_if)) {
          if (!this.showWhenDependents.has(dependentProp)) {
            this.showWhenDependents.set(dependentProp, []);
          }
          this.showWhenDependents.get(dependentProp).push(propKey);
        }
      }
    }
  }

  /**
   * Check if a property change should trigger re-render of properties panel
   * @param {string} propertyKey - The property that changed
   * @returns {boolean} - Whether re-render is needed
   */
  hasShowWhenDependents(propertyKey) {
    return this.showWhenDependents.has(propertyKey);
  }

  /**
   * Re-render the properties panel while preserving current values and active tab
   */
  refreshPropertiesPanel() {
    if (!this.currentElementConfig || !this.currentElementData) {
      return;
    }

    // Get the current form to find container
    const form = document.querySelector('.element-properties-form');
    if (!form) return;

    const container = form.parentElement;
    if (!container) return;

    // Detect currently active tab before re-rendering
    const activeTabBtn = form.querySelector('.admin-tab-btn.active');
    const activeTab = activeTabBtn ? activeTabBtn.dataset.tab : null;

    // Update element data content with current values
    const updatedElementData = {
      ...this.currentElementData,
      content: { ...this.currentValues },
    };

    // Re-render with preserved active tab
    this.renderProperties(container.id, this.currentElementConfig, updatedElementData, activeTab);
  }

  /**
   * Render properties for an element based on its config
   * @param {string} containerId - Container element ID
   * @param {Object} elementConfig - Element configuration
   * @param {Object} elementData - Element data with content
   * @param {string|null} activeTab - Optional tab key to set as active (preserves tab on re-render)
   */
  renderProperties(containerId, elementConfig, elementData, activeTab = null) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Clear any existing utilities
    this.cleanup();

    // Clear container
    container.innerHTML = '';

    // Store config and data for show_when re-renders
    this.currentElementConfig = elementConfig;
    this.currentElementData = elementData;
    this.currentValues = { ...elementData.content };

    // Apply config defaults for any missing values (ensures show_if conditions
    // work correctly on initial render when element content is sparse)
    const allProperties = elementConfig.tabs
      ? this.flattenTabProperties(elementConfig.tabs)
      : elementConfig.properties;
    if (allProperties) {
      for (const [propKey, propConfig] of Object.entries(allProperties)) {
        if (this.currentValues[propKey] === undefined && propConfig.default !== undefined) {
          this.currentValues[propKey] = propConfig.default;
        }
      }
    }

    // Ensure array properties are properly parsed (can be JSON strings after server refresh)
    for (const [key, value] of Object.entries(this.currentValues)) {
      if (typeof value === 'string' && value.startsWith('[')) {
        try {
          this.currentValues[key] = JSON.parse(value);
        } catch (e) {
          // Not a valid JSON array, keep as string
        }
      }
    }

    // Build show_when dependents map
    const properties = allProperties;
    this.buildShowWhenDependentsMap(properties);

    // Create properties form
    const form = document.createElement('form');
    form.className = 'element-properties-form';
    form.dataset.elementId = elementData.id;
    form.dataset.elementType = elementData.element_type;

    // Translation support is now integrated directly into translatable fields

    // Check if element has tabbed structure
    // Use this.currentValues (which includes config defaults) for correct show_if evaluation
    if (elementConfig.tabs) {
      this.renderTabs(form, elementConfig.tabs, this.currentValues, activeTab);
    } else {
      // Fallback to legacy section-based rendering
      const sections = this.groupPropertiesBySection(elementConfig.properties);
      for (const [sectionName, sectionProperties] of Object.entries(sections)) {
        const section = this.renderSection(sectionName, sectionProperties, this.currentValues);
        form.appendChild(section);
      }
    }

    container.appendChild(form);

    // Initialize utilities for advanced property types (only for visible properties)
    const visibleProperties = this.getVisibleProperties(properties, elementData.content);
    this.initializeUtilities(form, visibleProperties, elementData.content);

    // Setup change handlers
    this.setupChangeHandlers(form, elementData.id);

    // Trigger initial style application after a short delay
    // This ensures typography and other saved styles are applied
    setTimeout(() => {
      if (window.livePreview) {
        window.livePreview.applyStyles(elementData.id, elementData.content);
      }
    }, 50);
  }

  /**
   * Get only properties that should be visible based on show_when conditions
   * @param {Object} properties - All properties
   * @param {Object} values - Current values
   * @returns {Object} - Filtered properties
   */
  getVisibleProperties(properties, values) {
    const visible = {};
    for (const [key, config] of Object.entries(properties)) {
      if (this.shouldShowProperty(config, values)) {
        visible[key] = config;
      }
    }
    return visible;
  }

  /**
   * Group properties into logical sections
   */
  groupPropertiesBySection(properties) {
    const sections = {
      content: {},
      typography: {},
      colors: {},
      spacing: {},
      borders: {},
      effects: {},
      advanced: {},
    };

    for (const [key, prop] of Object.entries(properties)) {
      // Categorize properties
      if (['text', 'allow_html', 'url', 'title'].includes(key)) {
        sections.content[key] = prop;
      } else if (
        [
          'size',
          'weight',
          'font_family',
          'align',
          'line_height',
          'letter_spacing',
          'uppercase',
          'lowercase',
          'capitalize',
          'italic',
          'underline',
          'line_through',
        ].includes(key)
      ) {
        sections.typography[key] = prop;
      } else if (key.includes('color') || key === 'opacity') {
        sections.colors[key] = prop;
      } else if (key.includes('margin') || key.includes('padding')) {
        sections.spacing[key] = prop;
      } else if (key.includes('border') || key.includes('rounded')) {
        sections.borders[key] = prop;
      } else if (key.includes('shadow') || key === 'z_index') {
        sections.effects[key] = prop;
      } else {
        sections.advanced[key] = prop;
      }
    }

    // Remove empty sections
    for (const key of Object.keys(sections)) {
      if (Object.keys(sections[key]).length === 0) {
        delete sections[key];
      }
    }

    return sections;
  }

  /**
   * Render tabbed properties interface
   * @param {HTMLElement} form - Form element to append tabs to
   * @param {Object} tabs - Tab configuration object
   * @param {Object} values - Current property values
   * @param {string|null} activeTab - Optional tab key to set as active (for preserving tab on re-render)
   */
  renderTabs(form, tabs, values, activeTab = null) {
    // Create tab navigation
    const tabNav = document.createElement('div');
    tabNav.className = 'admin-tabs';

    // Create tab content container
    const tabContainer = document.createElement('div');
    tabContainer.className = 'tab-container';

    const tabKeys = Object.keys(tabs);
    // If no activeTab specified or it doesn't exist, default to first tab
    const effectiveActiveTab = activeTab && tabKeys.includes(activeTab) ? activeTab : tabKeys[0];

    // Render each tab
    for (const [tabKey, tabConfig] of Object.entries(tabs)) {
      const isActive = tabKey === effectiveActiveTab;

      // Create tab button
      const tabButton = document.createElement('button');
      tabButton.type = 'button';
      tabButton.className = `admin-tab-btn${isActive ? ' active' : ''}`;
      tabButton.dataset.tab = tabKey;
      tabButton.innerHTML = `<i class="${tabConfig.icon}"></i> ${tabConfig.label}`;
      tabNav.appendChild(tabButton);

      // Create tab content
      const tabContent = document.createElement('div');
      tabContent.className = `admin-tab-content${isActive ? ' active' : ''}`;
      tabContent.dataset.tabContent = tabKey;

      // Create properties grid container
      const propertiesGrid = document.createElement('div');
      propertiesGrid.className = 'properties-grid';
      propertiesGrid.style.cssText = 'display: flex; flex-direction: column; gap: 8px;';

      // Group properties into rows of 2
      let currentRow = null;
      let itemsInRow = 0;

      // Render properties for this tab
      for (const [propKey, propConfig] of Object.entries(tabConfig.properties)) {
        // Check show_when condition before rendering
        if (!this.shouldShowProperty(propConfig, values)) {
          continue; // Skip this property
        }

        // Determine if this property should be full-width
        const isFullWidth =
          propConfig.type === 'textarea' ||
          propConfig.type === 'property_group' ||
          propConfig.type === 'header' ||
          propConfig.type === 'aspect_ratio_selector' ||
          propConfig.full_width === true;

        // Handle header type for visual grouping
        if (propConfig.type === 'header') {
          // Close any open row first
          if (currentRow && itemsInRow > 0) {
            propertiesGrid.appendChild(currentRow);
            currentRow = null;
            itemsInRow = 0;
          }
          const header = document.createElement('div');
          header.className = 'property-section-header';
          header.innerHTML = `<h5>${propConfig.label}</h5>`;
          propertiesGrid.appendChild(header);
          continue;
        }

        if (isFullWidth) {
          // Close any open row first
          if (currentRow && itemsInRow > 0) {
            propertiesGrid.appendChild(currentRow);
            currentRow = null;
            itemsInRow = 0;
          }

          // Add full-width element in its own row
          const fullWidthRow = document.createElement('div');
          fullWidthRow.className = 'property-row full-width';

          // For property groups, pass the entire values object
          const propValue = propConfig.type === 'property_group' ? values : values[propKey];
          const propertyElement = this.renderProperty(propKey, propConfig, propValue);
          fullWidthRow.appendChild(propertyElement);
          propertiesGrid.appendChild(fullWidthRow);
        } else {
          // Start new row if needed
          if (!currentRow || itemsInRow >= 2) {
            if (currentRow) {
              propertiesGrid.appendChild(currentRow);
            }
            currentRow = document.createElement('div');
            currentRow.className = 'property-row';
            itemsInRow = 0;
          }

          const propertyElement = this.renderProperty(propKey, propConfig, values[propKey]);
          currentRow.appendChild(propertyElement);
          itemsInRow++;
        }
      }

      // Append any remaining row
      if (currentRow && itemsInRow > 0) {
        propertiesGrid.appendChild(currentRow);
      }

      tabContent.appendChild(propertiesGrid);
      tabContainer.appendChild(tabContent);
    }

    // Add tab switching functionality
    this.setupTabSwitching(tabNav);

    form.appendChild(tabNav);
    form.appendChild(tabContainer);
  }

  /**
   * Flatten tab properties for utility initialization
   * Handles nested property_group types
   */
  flattenTabProperties(tabs) {
    const flattened = {};
    for (const tabConfig of Object.values(tabs)) {
      for (const [propKey, propConfig] of Object.entries(tabConfig.properties)) {
        // If this is a property group, include both the group itself (for show_when tracking)
        // and its nested properties (for utility initialization)
        if (propConfig.type === 'property_group' && propConfig.properties) {
          // Include the property_group itself so show_when conditions are tracked
          flattened[propKey] = propConfig;
          // Also flatten nested properties for utility initialization
          Object.assign(flattened, propConfig.properties);
        } else {
          flattened[propKey] = propConfig;
        }
      }
    }
    return flattened;
  }

  /**
   * Setup tab switching functionality
   */
  setupTabSwitching(tabNav) {
    const tabButtons = tabNav.querySelectorAll('.admin-tab-btn');

    tabButtons.forEach(button => {
      button.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();

        const tabName = button.dataset.tab;

        console.log('Tab clicked:', tabName); // Debug logging

        // Update buttons
        tabButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        // Update content
        const form = tabNav.closest('.element-properties-form');
        if (!form) {
          console.error('Could not find form element');
          return;
        }

        const tabContents = form.querySelectorAll('.admin-tab-content');
        tabContents.forEach(content => content.classList.remove('active'));

        const targetContent = form.querySelector(`[data-tab-content="${tabName}"]`);
        if (targetContent) {
          targetContent.classList.add('active');
          console.log('Switched to tab:', tabName); // Debug logging
        } else {
          console.error('Could not find target content for tab:', tabName);
        }
      });
    });
  }

  /**
   * Render a property section
   */
  renderSection(sectionName, properties, values) {
    const section = document.createElement('div');
    section.className = 'property-section';

    // Add section header
    const header = document.createElement('h4');
    header.className = 'property-section-title';
    header.textContent = this.formatSectionName(sectionName);
    section.appendChild(header);

    // Create grid container for properties
    const propertiesGrid = document.createElement('div');
    propertiesGrid.className = 'properties-grid';
    propertiesGrid.style.cssText = 'display: flex; flex-direction: column; gap: 8px;';

    let currentRow = null;
    let itemsInRow = 0;

    // Render each property in 2-column grid
    for (const [key, config] of Object.entries(properties)) {
      const isFullWidth =
        config.type === 'textarea' ||
        config.type === 'property_group' ||
        config.type === 'aspect_ratio_selector' ||
        config.full_width === true;

      if (isFullWidth) {
        if (currentRow && itemsInRow > 0) {
          propertiesGrid.appendChild(currentRow);
          currentRow = null;
          itemsInRow = 0;
        }
        const fullWidthRow = document.createElement('div');
        fullWidthRow.className = 'property-row full-width';
        const propertyElement = this.renderProperty(key, config, values[key]);
        fullWidthRow.appendChild(propertyElement);
        propertiesGrid.appendChild(fullWidthRow);
      } else {
        if (!currentRow || itemsInRow >= 2) {
          if (currentRow) {
            propertiesGrid.appendChild(currentRow);
          }
          currentRow = document.createElement('div');
          currentRow.className = 'property-row';
          itemsInRow = 0;
        }
        const propertyElement = this.renderProperty(key, config, values[key]);
        currentRow.appendChild(propertyElement);
        itemsInRow++;
      }
    }

    if (currentRow && itemsInRow > 0) {
      propertiesGrid.appendChild(currentRow);
    }

    section.appendChild(propertiesGrid);
    return section;
  }

  /**
   * Render a single property based on its type
   */
  renderProperty(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'property-field';
    wrapper.dataset.property = key;

    // Add label
    const label = document.createElement('label');
    label.textContent = config.label || this.formatPropertyName(key);
    label.htmlFor = `prop-${key}`;
    wrapper.appendChild(label);

    // Handle property groups differently
    if (config.type === 'property_group') {
      return this.renderPropertyGroup(key, config, value);
    }

    // Render input based on type
    let input;
    switch (config.type) {
      case 'string':
      case 'url':
        input = this.renderTextInput(key, config, value);
        break;
      case 'size':
        // Size type for CSS dimensions (e.g., "8px", "2rem", "100%")
        input = this.renderSizeInput(key, config, value);
        break;
      case 'textarea':
        input = this.renderTextarea(key, config, value);
        break;
      case 'select':
        input = this.renderSelect(key, config, value);
        break;
      case 'boolean':
      case 'checkbox':
        input = this.renderCheckbox(key, config, value);
        break;
      case 'number':
        input = this.renderNumberInput(key, config, value);
        break;
      case 'range':
        input = this.renderRangeInput(key, config, value);
        break;
      case 'color':
        input = this.renderColorInput(key, config, value);
        break;
      case 'color_advanced':
      case 'gradient':
      case 'border_advanced':
      case 'shadow':
      case 'spacing':
      case 'typography':
      case 'background':
      case 'visibility_rules':
      case 'form_select':
      case 'icon_picker':
        // Advanced types get a text input with utility button
        input = this.renderAdvancedInput(key, config, value);
        break;
      case 'focal_point':
        // Focal point gets special rendering with position display
        input = this.renderFocalPointInput(key, config, value);
        break;
      case 'media_library':
      case 'image':
        // Media library selector with preview
        input = this.renderMediaLibraryInput(key, config, value);
        break;
      case 'aspect_ratio_selector':
        // Visual aspect ratio selector with common presets
        input = this.renderAspectRatioSelector(key, config, value);
        break;
      case 'array':
        // Array type for repeatable items (e.g., frames, images)
        input = this.renderArrayInput(key, config, value);
        break;
      case 'link_selector':
        // Link selector with type dropdown and entity search
        input = this.renderLinkSelectorInput(key, config, value);
        break;
      case 'product_picker':
        // Product search and selection picker
        input = this.renderProductPicker(key, config, value);
        break;
      case 'entity_picker':
        // Entity search picker (category, collection, etc.)
        input = this.renderEntityPicker(key, config, value);
        break;
      case 'category_picker':
        // Category search and multi-selection picker
        input = this.renderCategoryPicker(key, config, value);
        break;
      default:
        input = this.renderTextInput(key, config, value);
    }

    wrapper.appendChild(input);

    // Add help text if provided
    if (config.help_text) {
      const helpText = document.createElement('small');
      helpText.className = 'property-help-text';
      helpText.textContent = config.help_text;
      wrapper.appendChild(helpText);
    }

    return wrapper;
  }

  /**
   * Render text input
   */
  renderTextInput(key, config, value) {
    const input = document.createElement('input');
    input.type = 'text';
    input.id = `prop-${key}`;
    input.name = key;
    input.className = 'property-input';
    input.value = value || config.default || '';
    input.placeholder = config.placeholder || '';

    if (config.required) {
      input.required = true;
    }

    // If field is translatable, wrap it and add translation button
    if (config.translatable) {
      const wrapper = document.createElement('div');
      wrapper.className = 'translatable-field-wrapper';
      wrapper.dataset.translatable = 'true';
      wrapper.dataset.fieldKey = key;
      wrapper.appendChild(input);

      // Translation button will be added by TranslationEditor when initialized
      return wrapper;
    }

    return input;
  }

  /**
   * Render textarea
   */
  renderTextarea(key, config, value) {
    const textarea = document.createElement('textarea');
    textarea.id = `prop-${key}`;
    textarea.name = key;
    textarea.className = 'property-textarea';
    textarea.value = value || config.default || '';
    textarea.rows = config.rows || 3;
    textarea.placeholder = config.placeholder || '';

    if (config.required) {
      textarea.required = true;
    }

    // If field is translatable, wrap it and add translation button
    if (config.translatable) {
      const wrapper = document.createElement('div');
      wrapper.className = 'translatable-field-wrapper';
      wrapper.dataset.translatable = 'true';
      wrapper.dataset.fieldKey = key;
      wrapper.appendChild(textarea);

      // Translation button will be added by TranslationEditor when initialized
      return wrapper;
    }

    return textarea;
  }

  /**
   * Render select dropdown
   */
  renderSelect(key, config, value) {
    const select = document.createElement('select');
    select.id = `prop-${key}`;
    select.name = key;
    select.className = 'property-select';

    // Add options
    if (config.options) {
      config.options.forEach(option => {
        const optionEl = document.createElement('option');
        optionEl.value = option.value;
        optionEl.textContent = option.label;
        if (value === option.value || (!value && option.value === config.default)) {
          optionEl.selected = true;
        }
        select.appendChild(optionEl);
      });
    }

    return select;
  }

  /**
   * Render checkbox
   */
  renderCheckbox(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'checkbox-wrapper';

    const input = document.createElement('input');
    input.type = 'checkbox';
    input.id = `prop-${key}`;
    input.name = key;
    input.className = 'property-checkbox';
    input.checked = value !== undefined ? value : config.default;

    const label = document.createElement('label');
    label.htmlFor = `prop-${key}`;
    label.textContent = config.label || this.formatPropertyName(key);

    wrapper.appendChild(input);
    wrapper.appendChild(label);

    return wrapper;
  }

  /**
   * Render number input
   */
  renderNumberInput(key, config, value) {
    const input = document.createElement('input');
    input.type = 'number';
    input.id = `prop-${key}`;
    input.name = key;
    input.className = 'property-input';
    input.value = value || config.default || '';

    if (config.min !== undefined) input.min = config.min;
    if (config.max !== undefined) input.max = config.max;
    if (config.step !== undefined) input.step = config.step;

    return input;
  }

  /**
   * Render range input
   */
  renderRangeInput(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'range-wrapper';

    const input = document.createElement('input');
    input.type = 'range';
    input.id = `prop-${key}`;
    input.name = key;
    input.className = 'property-range';
    input.value = value || config.default || 0;

    if (config.min !== undefined) input.min = config.min;
    if (config.max !== undefined) input.max = config.max;
    if (config.step !== undefined) input.step = config.step;

    const valueDisplay = document.createElement('span');
    valueDisplay.className = 'range-value';
    valueDisplay.textContent = input.value;

    input.addEventListener('input', () => {
      valueDisplay.textContent = input.value;
    });

    wrapper.appendChild(input);
    wrapper.appendChild(valueDisplay);

    return wrapper;
  }

  /**
   * Render basic color input
   */
  renderColorInput(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'color-input-wrapper';

    const input = document.createElement('input');
    input.type = 'color';
    input.id = `prop-${key}`;
    input.name = key;
    input.className = 'property-color';
    input.value = value || config.default || '#000000';

    const textInput = document.createElement('input');
    textInput.type = 'text';
    textInput.className = 'property-input color-text';
    textInput.value = input.value;

    // Sync inputs
    input.addEventListener('change', () => {
      textInput.value = input.value;
    });

    textInput.addEventListener('change', () => {
      if (/^#[0-9A-F]{6}$/i.test(textInput.value)) {
        input.value = textInput.value;
      }
    });

    wrapper.appendChild(input);
    wrapper.appendChild(textInput);

    return wrapper;
  }

  /**
   * Render size input for CSS dimensions (e.g., "8px", "2rem", "100%")
   */
  renderSizeInput(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'size-input-wrapper';

    // Parse current value to extract number and unit
    const currentValue = value || config.default || '';
    const match = currentValue.match(/^([\d.]+)(.*)$/);
    const numValue = match ? match[1] : '';
    const unitValue = match ? match[2] : 'px';

    // Number input
    const numberInput = document.createElement('input');
    numberInput.type = 'number';
    numberInput.className = 'property-input size-number';
    numberInput.value = numValue;
    numberInput.min = config.min || 0;
    numberInput.step = config.step || 1;
    numberInput.placeholder = '0';

    // Unit selector
    const unitSelect = document.createElement('select');
    unitSelect.className = 'property-select size-unit';

    const units = config.units || ['px', 'em', 'rem', '%', 'vh', 'vw'];
    units.forEach(unit => {
      const option = document.createElement('option');
      option.value = unit;
      option.textContent = unit;
      if (unit === unitValue || (!unitValue && unit === 'px')) {
        option.selected = true;
      }
      unitSelect.appendChild(option);
    });

    // Hidden input to store combined value
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.id = `prop-${key}`;
    hiddenInput.name = key;
    hiddenInput.value = currentValue;

    // Sync combined value
    const updateHiddenValue = () => {
      const num = numberInput.value || '0';
      const unit = unitSelect.value;
      hiddenInput.value = num + unit;

      // Trigger change event
      const event = new Event('change', { bubbles: true });
      hiddenInput.dispatchEvent(event);
    };

    numberInput.addEventListener('input', updateHiddenValue);
    unitSelect.addEventListener('change', updateHiddenValue);

    wrapper.appendChild(numberInput);
    wrapper.appendChild(unitSelect);
    wrapper.appendChild(hiddenInput);

    return wrapper;
  }

  /**
   * Render property group with subheading (collapsible section style)
   */
  renderPropertyGroup(key, config, values) {
    const wrapper = document.createElement('div');
    wrapper.className = 'property-group-container';
    wrapper.dataset.propertyGroup = key;

    // Add group heading with toggle icon
    const heading = document.createElement('div');
    heading.className = 'property-group-heading';

    // Add toggle icon
    const toggleIcon = document.createElement('i');
    toggleIcon.className = 'fas fa-chevron-down toggle-icon';
    heading.appendChild(toggleIcon);

    const headingLabel = document.createElement('span');
    headingLabel.className = 'property-group-label';
    headingLabel.textContent = config.label || this.formatPropertyName(key);
    heading.appendChild(headingLabel);

    // Add collapse toggle functionality
    heading.addEventListener('click', () => {
      wrapper.classList.toggle('collapsed');
    });

    // Add group help text if provided
    if (config.help_text) {
      const helpText = document.createElement('small');
      helpText.className = 'property-group-help';
      helpText.textContent = config.help_text;
      heading.appendChild(helpText);
    }

    wrapper.appendChild(heading);

    // Create container for sub-properties
    const propertiesContainer = document.createElement('div');
    // Support columns option: 1 for single column, 2 (default) for two columns
    const columns = config.columns || 2;
    propertiesContainer.className =
      columns === 1 ? 'property-group-properties single-column' : 'property-group-properties';

    // Render each sub-property
    if (config.properties) {
      for (const [subKey, subConfig] of Object.entries(config.properties)) {
        // Check show_when/show_if condition before rendering
        if (!this.shouldShowProperty(subConfig, values || {})) {
          continue; // Skip this property
        }

        // Use full property key for actual value storage
        const fullKey = subKey; // Keep original key for animation properties
        const subValue = values ? values[subKey] : undefined;

        const subWrapper = document.createElement('div');
        // Support full_width option for individual properties within group
        const isFullWidth =
          subConfig.full_width === true ||
          subConfig.type === 'textarea' ||
          subConfig.type === 'aspect_ratio_selector';
        subWrapper.className = isFullWidth ? 'property-subgroup full-width' : 'property-subgroup';
        subWrapper.dataset.property = fullKey;

        // Add label
        const label = document.createElement('label');
        label.textContent = subConfig.label || this.formatPropertyName(subKey);
        label.htmlFor = `prop-${fullKey}`;
        label.className = 'property-subgroup-label';
        subWrapper.appendChild(label);

        // Render the input based on type
        let input;
        switch (subConfig.type) {
          case 'select':
            input = this.renderSelect(fullKey, subConfig, subValue);
            break;
          case 'string':
          case 'url':
            input = this.renderTextInput(fullKey, subConfig, subValue);
            break;
          case 'number':
            input = this.renderNumberInput(fullKey, subConfig, subValue);
            break;
          case 'boolean':
          case 'checkbox':
            input = this.renderCheckbox(fullKey, subConfig, subValue);
            break;
          case 'textarea':
            input = this.renderTextarea(fullKey, subConfig, subValue);
            break;
          case 'range':
            input = this.renderRangeInput(fullKey, subConfig, subValue);
            break;
          case 'color_advanced':
          case 'gradient':
          case 'border_advanced':
          case 'shadow':
          case 'spacing':
          case 'typography':
          case 'background':
          case 'visibility_rules':
          case 'form_select':
          case 'icon_picker':
            // Advanced types get a text input with utility button
            input = this.renderAdvancedInput(fullKey, subConfig, subValue);
            break;
          case 'focal_point':
            // Focal point gets special rendering with position display
            input = this.renderFocalPointInput(fullKey, subConfig, subValue);
            break;
          case 'media_library':
          case 'image':
            // Media library selector with preview
            input = this.renderMediaLibraryInput(fullKey, subConfig, subValue);
            break;
          case 'aspect_ratio_selector':
            // Visual aspect ratio selector with common presets
            input = this.renderAspectRatioSelector(fullKey, subConfig, subValue);
            break;
          case 'array':
            // Array type for repeatable items (e.g., frames, images)
            input = this.renderArrayInput(fullKey, subConfig, subValue);
            break;
          case 'link_selector':
            input = this.renderLinkSelectorInput(fullKey, subConfig, subValue);
            break;
          case 'product_picker':
            input = this.renderProductPicker(fullKey, subConfig, subValue);
            break;
          case 'entity_picker':
            input = this.renderEntityPicker(fullKey, subConfig, subValue);
            break;
          case 'category_picker':
            input = this.renderCategoryPicker(fullKey, subConfig, subValue);
            break;
          default:
            input = this.renderTextInput(fullKey, subConfig, subValue);
        }

        subWrapper.appendChild(input);

        // Add help text if provided
        if (subConfig.help_text) {
          const helpText = document.createElement('small');
          helpText.className = 'property-help-text';
          helpText.textContent = subConfig.help_text;
          subWrapper.appendChild(helpText);
        }

        propertiesContainer.appendChild(subWrapper);
      }
    }

    wrapper.appendChild(propertiesContainer);
    return wrapper;
  }

  /**
   * Render advanced input with utility trigger
   */
  renderAdvancedInput(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'property-input-with-utility';
    wrapper.dataset.utilityType = config.type;
    wrapper.dataset.utility = config.utility;

    const input = document.createElement('input');
    input.type = 'text';
    input.id = `prop-${key}`;
    input.name = key;
    input.className = 'property-input';
    input.value = value || config.default || '';
    input.placeholder = config.placeholder || '';

    wrapper.appendChild(input);

    // The utility will be attached later in initializeUtilities()
    return wrapper;
  }

  /**
   * Render focal point input with position display and editor trigger
   */
  renderFocalPointInput(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'property-input-with-utility focal-point-input';
    wrapper.dataset.utilityType = 'focal_point';
    wrapper.dataset.utility = config.utility || 'focal_point_editor';

    // Parse current value - can be object {x, y} or string "50% 50%"
    let focalX = 0.5,
      focalY = 0.5;
    if (value) {
      if (typeof value === 'object') {
        // Object format: {x: 0.65, y: 0.40} or {default: {x, y}, tablet: {...}}
        if (value.default) {
          focalX = value.default.x ?? 0.5;
          focalY = value.default.y ?? 0.5;
        } else if (value.x !== undefined) {
          focalX = value.x;
          focalY = value.y ?? 0.5;
        }
      } else if (typeof value === 'string') {
        // String format: "65% 40%" or JSON string
        try {
          const parsed = JSON.parse(value);
          if (parsed.default) {
            focalX = parsed.default.x ?? 0.5;
            focalY = parsed.default.y ?? 0.5;
          } else if (parsed.x !== undefined) {
            focalX = parsed.x;
            focalY = parsed.y ?? 0.5;
          }
        } catch (e) {
          // Try parsing percentage format
          const match = value.match(/(\d+(?:\.\d+)?)\s*%?\s+(\d+(?:\.\d+)?)\s*%?/);
          if (match) {
            focalX = parseFloat(match[1]) / 100;
            focalY = parseFloat(match[2]) / 100;
          }
        }
      }
    }

    // Hidden input to store JSON value
    const input = document.createElement('input');
    input.type = 'hidden';
    input.id = `prop-${key}`;
    input.name = key;
    input.className = 'property-input focal-point-value';
    // Store as JSON object
    const storedValue = { x: focalX, y: focalY };
    input.value = JSON.stringify(storedValue);

    // Position display
    const positionDisplay = document.createElement('span');
    positionDisplay.className = 'focal-point-position';
    positionDisplay.textContent = this.formatFocalPointPosition(focalX, focalY);

    // Edit button
    const editButton = document.createElement('button');
    editButton.type = 'button';
    editButton.className = 'utility-trigger-btn focal-point-btn';
    editButton.innerHTML = '<i class="fas fa-crosshairs"></i>';

    wrapper.appendChild(input);
    wrapper.appendChild(positionDisplay);
    wrapper.appendChild(editButton);

    return wrapper;
  }

  /**
   * Format focal point position for display
   */
  formatFocalPointPosition(x, y) {
    // Convert to percentages
    const xPercent = Math.round(x * 100);
    const yPercent = Math.round(y * 100);

    // Check for named positions
    if (xPercent === 50 && yPercent === 50) return 'Center';
    if (xPercent === 0 && yPercent === 0) return 'Top Left';
    if (xPercent === 50 && yPercent === 0) return 'Top Center';
    if (xPercent === 100 && yPercent === 0) return 'Top Right';
    if (xPercent === 0 && yPercent === 50) return 'Center Left';
    if (xPercent === 100 && yPercent === 50) return 'Center Right';
    if (xPercent === 0 && yPercent === 100) return 'Bottom Left';
    if (xPercent === 50 && yPercent === 100) return 'Bottom Center';
    if (xPercent === 100 && yPercent === 100) return 'Bottom Right';

    // Custom position
    return `${xPercent}% × ${yPercent}%`;
  }

  /**
   * Render media library input with preview and selection button
   */
  renderMediaLibraryInput(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'media-library-input-wrapper';

    // Hidden input to store the URL value
    const input = document.createElement('input');
    input.type = 'hidden';
    input.id = `prop-${key}`;
    input.name = key;
    input.value = value || '';

    // Preview container
    const previewContainer = document.createElement('div');
    previewContainer.className = 'media-library-preview';
    if (value) {
      previewContainer.innerHTML = `
                <img src="${value}" alt="Preview" class="media-library-preview-img">
            `;
    } else {
      previewContainer.innerHTML = `
                <div class="media-library-no-image">
                    <i class="fas fa-image"></i>
                    <span>No image selected</span>
                </div>
            `;
    }

    // Button container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'media-library-buttons';

    // Select button
    const selectBtn = document.createElement('button');
    selectBtn.type = 'button';
    selectBtn.className = 'btn btn-sm btn-primary media-library-select-btn';
    selectBtn.innerHTML = '<i class="fas fa-images"></i> Select Image';
    selectBtn.addEventListener('click', async () => {
      if (window.selectImageFromLibrary) {
        window.selectImageFromLibrary(selectedMedia => {
          if (selectedMedia) {
            // Update the hidden input value
            input.value = selectedMedia.url;

            // Store metadata for size switching
            input.dataset.mediaId = selectedMedia.id || '';
            input.dataset.mediaTitle = selectedMedia.title || '';
            input.dataset.thumbnails = JSON.stringify(selectedMedia.thumbnails || []);
            input.dataset.webpUrl = selectedMedia.webp_url || '';
            input.dataset.originalUrl = selectedMedia.original_url || selectedMedia.url || '';

            // Update preview
            previewContainer.innerHTML = `
                            <img src="${selectedMedia.url}" alt="${selectedMedia.title || 'Preview'}" class="media-library-preview-img">
                        `;

            // Auto-populate alt text and caption from media library (if fields are empty)
            const form = input.closest('form') || input.closest('.property-panel');
            if (form) {
              // Populate alt text if empty
              const altInput = form.querySelector('#prop-alt');
              if (altInput && !altInput.value && selectedMedia.alt_text) {
                altInput.value = selectedMedia.alt_text;
                altInput.dispatchEvent(new Event('change', { bubbles: true }));
              }

              // Populate caption if empty (use description from media library)
              const captionInput = form.querySelector('#prop-caption');
              if (captionInput && !captionInput.value && selectedMedia.description) {
                captionInput.value = selectedMedia.description;
                captionInput.dispatchEvent(new Event('change', { bubbles: true }));
              }

              // Populate title if empty
              const titleInput = form.querySelector('#prop-title');
              if (titleInput && !titleInput.value && selectedMedia.title) {
                titleInput.value = selectedMedia.title;
                titleInput.dispatchEvent(new Event('change', { bubbles: true }));
              }
            }

            // Trigger change event for live preview
            input.dispatchEvent(new Event('change', { bubbles: true }));
          }
        });
      } else {
        console.warn('Media library not available. Falling back to URL input.');
        const url = await AdminModal.prompt('Enter image URL:');
        if (url) {
          input.value = url;
          previewContainer.innerHTML = `
                        <img src="${url}" alt="Preview" class="media-library-preview-img">
                    `;
          input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      }
    });

    // Clear button
    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'btn btn-sm btn-outline-danger media-library-clear-btn';
    clearBtn.innerHTML = '<i class="fas fa-times"></i>';
    clearBtn.title = 'Clear image';
    clearBtn.addEventListener('click', () => {
      input.value = '';
      delete input.dataset.mediaId;
      delete input.dataset.mediaTitle;
      delete input.dataset.thumbnails;
      delete input.dataset.webpUrl;
      delete input.dataset.originalUrl;

      previewContainer.innerHTML = `
                <div class="media-library-no-image">
                    <i class="fas fa-image"></i>
                    <span>No image selected</span>
                </div>
            `;

      // Trigger change event
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });

    buttonContainer.appendChild(selectBtn);
    buttonContainer.appendChild(clearBtn);

    wrapper.appendChild(input);
    wrapper.appendChild(previewContainer);
    wrapper.appendChild(buttonContainer);

    return wrapper;
  }

  /**
   * Render aspect ratio selector with visual buttons
   * Displays 6 common aspect ratios in a 3x2 grid with visual representations
   */
  renderAspectRatioSelector(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'aspect-ratio-selector';

    // Hidden input to store the value
    const input = document.createElement('input');
    input.type = 'hidden';
    input.id = `prop-${key}`;
    input.name = key;
    input.value = value || config.default || '';

    wrapper.appendChild(input);

    // Define aspect ratios with their visual properties
    const aspectRatios = [
      { value: '16/9', label: '16:9', description: 'Widescreen', widthRatio: 16, heightRatio: 9 },
      { value: '1/1', label: '1:1', description: 'Square', widthRatio: 1, heightRatio: 1 },
      { value: '3/2', label: '3:2', description: 'Standard', widthRatio: 3, heightRatio: 2 },
      { value: '4/3', label: '4:3', description: 'Classic', widthRatio: 4, heightRatio: 3 },
      { value: '4/1', label: '4:1', description: 'Banner', widthRatio: 4, heightRatio: 1 },
      { value: '9/16', label: '9:16', description: 'Portrait', widthRatio: 9, heightRatio: 16 },
    ];

    // Create grid container
    const grid = document.createElement('div');
    grid.className = 'aspect-ratio-grid';

    aspectRatios.forEach(ratio => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'aspect-ratio-btn';
      button.dataset.value = ratio.value;
      if (value === ratio.value) {
        button.classList.add('active');
      }

      // Calculate visual box dimensions (max 40px in any direction)
      const maxSize = 40;
      let boxWidth, boxHeight;
      if (ratio.widthRatio >= ratio.heightRatio) {
        boxWidth = maxSize;
        boxHeight = Math.round((ratio.heightRatio / ratio.widthRatio) * maxSize);
      } else {
        boxHeight = maxSize;
        boxWidth = Math.round((ratio.widthRatio / ratio.heightRatio) * maxSize);
      }

      button.innerHTML = `
                <div class="aspect-ratio-visual">
                    <div class="aspect-ratio-box" style="width: ${boxWidth}px; height: ${boxHeight}px;"></div>
                </div>
                <div class="aspect-ratio-label">${ratio.label}</div>
                <div class="aspect-ratio-desc">${ratio.description}</div>
            `;

      button.addEventListener('click', () => {
        // Remove active from all buttons
        grid.querySelectorAll('.aspect-ratio-btn').forEach(btn => btn.classList.remove('active'));
        // Add active to clicked button
        button.classList.add('active');
        // Update input value
        input.value = ratio.value;
        // Trigger change event
        input.dispatchEvent(new Event('change', { bubbles: true }));
      });

      grid.appendChild(button);
    });

    // Add "None/Auto" option
    const noneBtn = document.createElement('button');
    noneBtn.type = 'button';
    noneBtn.className = 'aspect-ratio-btn aspect-ratio-none';
    noneBtn.dataset.value = '';
    if (!value) {
      noneBtn.classList.add('active');
    }
    noneBtn.innerHTML = `
            <div class="aspect-ratio-visual">
                <div class="aspect-ratio-box aspect-ratio-auto">
                    <i class="fas fa-expand"></i>
                </div>
            </div>
            <div class="aspect-ratio-label">Auto</div>
            <div class="aspect-ratio-desc">Natural</div>
        `;
    noneBtn.addEventListener('click', () => {
      grid.querySelectorAll('.aspect-ratio-btn').forEach(btn => btn.classList.remove('active'));
      noneBtn.classList.add('active');
      input.value = '';
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });

    // Insert Auto button at the beginning of the second row (after first 3)
    const buttons = grid.querySelectorAll('.aspect-ratio-btn');
    if (buttons.length >= 3) {
      grid.insertBefore(noneBtn, buttons[3]);
    } else {
      grid.appendChild(noneBtn);
    }

    wrapper.appendChild(grid);

    // Add custom input option
    const customWrapper = document.createElement('div');
    customWrapper.className = 'aspect-ratio-custom';
    customWrapper.innerHTML = `
            <label class="aspect-ratio-custom-label">
                <input type="text" class="aspect-ratio-custom-input" placeholder="Custom (e.g., 21/9)" value="${value && !aspectRatios.find(r => r.value === value) ? value : ''}">
            </label>
        `;
    const customInput = customWrapper.querySelector('.aspect-ratio-custom-input');
    customInput.addEventListener('input', () => {
      const customValue = customInput.value.trim();
      if (customValue) {
        grid.querySelectorAll('.aspect-ratio-btn').forEach(btn => btn.classList.remove('active'));
        input.value = customValue;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
    customInput.addEventListener('focus', () => {
      grid.querySelectorAll('.aspect-ratio-btn').forEach(btn => btn.classList.remove('active'));
    });

    wrapper.appendChild(customWrapper);

    return wrapper;
  }

  /**
   * Render link selector with type dropdown and entity search
   * Allows selecting internal content (Product, Page, Category, Blog) or entering custom URL
   */
  renderLinkSelectorInput(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'link-selector-wrapper';
    wrapper.dataset.propertyKey = key;

    // Parse existing value to determine current state
    const currentState = this.parseLinkValue(value);

    // 1. Link type dropdown
    const typeWrapper = document.createElement('div');
    typeWrapper.className = 'link-selector-type';

    const typeLabel = document.createElement('label');
    typeLabel.textContent = 'Link Type';
    typeLabel.className = 'link-selector-type-label';
    typeWrapper.appendChild(typeLabel);

    const typeSelect = document.createElement('select');
    typeSelect.className = 'property-select link-type-select';

    const options = [
      { value: 'custom', label: 'Custom URL' },
      { value: 'product', label: 'Product' },
      { value: 'page', label: 'Page' },
      { value: 'category', label: 'Category' },
      { value: 'blog', label: 'Blog Post' },
    ];

    options.forEach(opt => {
      const option = document.createElement('option');
      option.value = opt.value;
      option.textContent = opt.label;
      if (opt.value === currentState.type) option.selected = true;
      typeSelect.appendChild(option);
    });

    typeWrapper.appendChild(typeSelect);
    wrapper.appendChild(typeWrapper);

    // 2. Input area (dynamic based on type)
    const inputArea = document.createElement('div');
    inputArea.className = 'link-selector-input-area';
    wrapper.appendChild(inputArea);

    // 3. Selected item preview (hidden initially)
    const preview = document.createElement('div');
    preview.className = 'link-selector-preview';
    preview.style.display = 'none';
    wrapper.appendChild(preview);

    // 4. Hidden input for actual value storage
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.id = `prop-${key}`;
    hiddenInput.name = key;
    hiddenInput.value = typeof value === 'string' ? value : value?.url || '';
    wrapper.appendChild(hiddenInput);

    // Initialize the input area based on current type
    this.updateLinkSelectorInputArea(wrapper, currentState, hiddenInput);

    // Setup type change handler
    typeSelect.addEventListener('change', () => {
      const newType = typeSelect.value;
      this.updateLinkSelectorInputArea(
        wrapper,
        { type: newType, url: '', id: null, title: '' },
        hiddenInput
      );
    });

    return wrapper;
  }

  /**
   * Parse link value to determine type from URL pattern or object
   */
  parseLinkValue(value) {
    if (!value) {
      return { type: 'custom', url: '', id: null, title: '' };
    }

    // If value is an object with type info
    if (typeof value === 'object' && value.type) {
      return {
        type: value.type || 'custom',
        url: value.url || '',
        id: value.id || null,
        title: value.title || '',
      };
    }

    // Plain URL string - try to determine type from URL pattern
    const urlStr = String(value);

    if (urlStr.includes('/products/') || urlStr.includes('/product/')) {
      return { type: 'product', url: urlStr, id: null, title: '' };
    }
    if (urlStr.includes('/page/') || urlStr.includes('/pages/')) {
      return { type: 'page', url: urlStr, id: null, title: '' };
    }
    if (urlStr.includes('/category/') || urlStr.includes('/categories/')) {
      return { type: 'category', url: urlStr, id: null, title: '' };
    }
    if (urlStr.includes('/blog/') || urlStr.includes('/posts/')) {
      return { type: 'blog', url: urlStr, id: null, title: '' };
    }

    // Default to custom URL
    return { type: 'custom', url: urlStr, id: null, title: '' };
  }

  /**
   * Update link selector input area based on selected type
   */
  updateLinkSelectorInputArea(wrapper, state, hiddenInput) {
    const inputArea = wrapper.querySelector('.link-selector-input-area');
    const preview = wrapper.querySelector('.link-selector-preview');

    inputArea.innerHTML = '';
    preview.style.display = 'none';

    if (state.type === 'custom') {
      // Simple URL text input
      const urlInput = document.createElement('input');
      urlInput.type = 'url';
      urlInput.className = 'property-input link-url-input';
      urlInput.placeholder = 'https://example.com or /page-slug/';
      urlInput.value = state.url || '';

      // Update hidden input on change (blur)
      urlInput.addEventListener('change', () => {
        hiddenInput.value = urlInput.value;
        hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
      });

      inputArea.appendChild(urlInput);
    } else {
      // Entity search input
      this.renderLinkEntitySearch(wrapper, state, hiddenInput);
    }
  }

  /**
   * Render entity search input with autocomplete results
   */
  renderLinkEntitySearch(wrapper, state, hiddenInput) {
    const inputArea = wrapper.querySelector('.link-selector-input-area');
    const preview = wrapper.querySelector('.link-selector-preview');

    // Search input wrapper
    const searchWrapper = document.createElement('div');
    searchWrapper.className = 'link-selector-search';

    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'property-input link-search-input';
    searchInput.placeholder = `Search ${state.type}s...`;

    const searchIcon = document.createElement('span');
    searchIcon.className = 'link-search-icon';
    searchIcon.innerHTML = '<i class="fas fa-search"></i>';

    searchWrapper.appendChild(searchInput);
    searchWrapper.appendChild(searchIcon);
    inputArea.appendChild(searchWrapper);

    // Results dropdown
    const resultsDropdown = document.createElement('div');
    resultsDropdown.className = 'link-selector-results';
    resultsDropdown.style.display = 'none';
    inputArea.appendChild(resultsDropdown);

    // If we have a pre-selected item with title, show the preview
    if (state.id && state.title) {
      this.showLinkSelectorPreview(wrapper, state, hiddenInput, searchWrapper);
      searchWrapper.style.display = 'none';
    } else if (state.url && !state.title) {
      // We have a URL but no title - show the URL in the input so merchant knows something is selected
      searchInput.value = state.url;
      searchInput.dataset.selectedUrl = state.url;
    }

    // Debounced search handler
    let searchTimeout;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      const query = searchInput.value.trim();

      if (query.length < 2) {
        resultsDropdown.style.display = 'none';
        return;
      }

      searchTimeout = setTimeout(() => {
        this.searchLinkSources(state.type, query, resultsDropdown, selected => {
          // Store selected item
          hiddenInput.value = selected.url;
          hiddenInput.dataset.linkType = state.type;
          hiddenInput.dataset.linkId = selected.id;
          hiddenInput.dataset.linkTitle = selected.title || selected.name;

          // Show preview
          this.showLinkSelectorPreview(
            wrapper,
            {
              type: state.type,
              id: selected.id,
              url: selected.url,
              title: selected.title || selected.name,
              thumbnail: selected.thumbnail,
            },
            hiddenInput,
            searchWrapper
          );

          // Hide search
          searchWrapper.style.display = 'none';
          resultsDropdown.style.display = 'none';

          // Trigger change event for server sync
          hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
        });
      }, 300);
    });

    // Hide results on blur (with delay for click handling)
    searchInput.addEventListener('blur', () => {
      setTimeout(() => {
        resultsDropdown.style.display = 'none';
      }, 200);
    });

    // Show results on focus if there's a query
    searchInput.addEventListener('focus', () => {
      if (searchInput.value.trim().length >= 2 && resultsDropdown.children.length > 0) {
        resultsDropdown.style.display = 'block';
      }
    });
  }

  /**
   * Search link sources via API
   */
  async searchLinkSources(type, query, resultsContainer, onSelect) {
    resultsContainer.innerHTML =
      '<div class="link-selector-loading"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    resultsContainer.style.display = 'block';

    try {
      const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/api/page-builder';
      const response = await fetch(
        `${apiBaseUrl}/link-sources/?type=${type}&search=${encodeURIComponent(query)}&limit=10`
      );
      const data = await response.json();

      // Get results for the selected type
      // Handle irregular plurals: category -> categories, blog -> blog_posts
      let typeKey;
      if (type === 'blog') {
        typeKey = 'blog_posts';
      } else if (type === 'category') {
        typeKey = 'categories';
      } else {
        typeKey = `${type}s`;
      }
      const results = data[typeKey] || [];

      if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="link-selector-no-results">No results found</div>';
        return;
      }

      resultsContainer.innerHTML = '';
      results.forEach(item => {
        const resultItem = document.createElement('div');
        resultItem.className = 'link-selector-result-item';
        resultItem.innerHTML = `
                    <div class="link-result-thumb">
                        ${item.thumbnail ? `<img src="${item.thumbnail}" alt="">` : '<i class="fas fa-link"></i>'}
                    </div>
                    <div class="link-result-info">
                        <div class="link-result-title">${this.escapeHtml(item.title || item.name)}</div>
                        <div class="link-result-url">${this.escapeHtml(item.url)}</div>
                    </div>
                `;

        resultItem.addEventListener('click', () => onSelect(item));
        resultsContainer.appendChild(resultItem);
      });
    } catch (error) {
      console.error('Error searching link sources:', error);
      resultsContainer.innerHTML =
        '<div class="link-selector-error">Search failed. Please try again.</div>';
    }
  }

  /**
   * Show selected link preview with clear button
   */
  showLinkSelectorPreview(wrapper, state, hiddenInput, searchWrapper) {
    const preview = wrapper.querySelector('.link-selector-preview');

    const typeLabels = {
      product: 'Product',
      page: 'Page',
      category: 'Category',
      blog: 'Blog Post',
    };

    preview.innerHTML = `
            <div class="link-preview-content">
                <div class="link-preview-info">
                    <span class="link-preview-type">${typeLabels[state.type] || state.type}</span>
                    <span class="link-preview-title">${this.escapeHtml(state.title)}</span>
                    <span class="link-preview-url">${this.escapeHtml(state.url)}</span>
                </div>
                <button type="button" class="link-preview-clear" title="Clear selection">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    preview.style.display = 'block';

    // Clear button handler
    preview.querySelector('.link-preview-clear').addEventListener('click', () => {
      hiddenInput.value = '';
      delete hiddenInput.dataset.linkType;
      delete hiddenInput.dataset.linkId;
      delete hiddenInput.dataset.linkTitle;

      preview.style.display = 'none';
      if (searchWrapper) {
        searchWrapper.style.display = 'block';
        const searchInput = searchWrapper.querySelector('input');
        if (searchInput) {
          searchInput.value = '';
          searchInput.focus();
        }
      }

      hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
    });
  }

  // =========================================================================
  // Product Picker - search and select products by ID
  // =========================================================================

  /**
   * Render product picker for product_grid element.
   * Shows a search bar to find products, selected products as cards with reorder/remove.
   */
  renderProductPicker(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'product-picker';
    wrapper.dataset.propertyKey = key;

    // Hidden input for form data collection
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = key;
    hiddenInput.id = `prop-${key}`;
    wrapper.appendChild(hiddenInput);

    // Current product IDs
    const productIds = Array.isArray(value) ? [...value] : [];
    hiddenInput.value = JSON.stringify(productIds);

    // Helper to sync hidden input and fire change
    const syncValue = () => {
      hiddenInput.value = JSON.stringify(productIds);
      hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
    };

    // Search input area
    const searchWrapper = document.createElement('div');
    searchWrapper.className = 'product-picker__search';

    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'property-input product-picker__search-input';
    searchInput.placeholder = 'Search products by name or SKU...';
    searchWrapper.appendChild(searchInput);

    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'product-picker__results';
    resultsContainer.style.display = 'none';
    document.body.appendChild(resultsContainer);

    wrapper.appendChild(searchWrapper);

    // Selected products list
    const selectedList = document.createElement('div');
    selectedList.className = 'product-picker__selected';
    wrapper.appendChild(selectedList);

    // Empty state
    const emptyState = document.createElement('div');
    emptyState.className = 'product-picker__empty';
    emptyState.innerHTML =
      '<i class="fas fa-search"></i><span>Search and add products to display</span>';
    wrapper.appendChild(emptyState);

    // Load existing selections
    if (productIds.length > 0) {
      emptyState.style.display = 'none';
      this._loadProductPickerSelections(selectedList, productIds, key, emptyState, syncValue);
    }

    // Search with debounce
    let searchTimeout;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      const query = searchInput.value.trim();

      if (query.length < 2) {
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        return;
      }

      searchTimeout = setTimeout(async () => {
        await this._searchProducts(query, resultsContainer, productIds, searchInput, product => {
          // Add product ID to the list
          productIds.push(product.id);
          syncValue();

          // Add to selected list UI
          this._addProductPickerCard(selectedList, product, productIds, key, emptyState, syncValue);
          emptyState.style.display = 'none';

          // Clear search
          searchInput.value = '';
          resultsContainer.innerHTML = '';
          resultsContainer.style.display = 'none';
        });
      }, 300);
    });

    // Close results on outside click (check both search wrapper and results container since it's in body)
    document.addEventListener('click', e => {
      if (!searchWrapper.contains(e.target) && !resultsContainer.contains(e.target)) {
        resultsContainer.style.display = 'none';
      }
    });

    // Clean up body-appended dropdown when wrapper is removed from DOM
    const cleanupObserver = new MutationObserver(() => {
      if (!document.body.contains(wrapper)) {
        resultsContainer.remove();
        cleanupObserver.disconnect();
      }
    });
    // Start observing once wrapper is in the DOM
    requestAnimationFrame(() => {
      if (wrapper.parentElement) {
        cleanupObserver.observe(wrapper.parentElement, { childList: true });
      }
    });

    return wrapper;
  }

  /**
   * Position a fixed dropdown below a reference element
   */
  _positionFixedDropdown(dropdown, referenceEl) {
    const rect = referenceEl.getBoundingClientRect();
    dropdown.style.top = `${rect.bottom + 4}px`;
    dropdown.style.left = `${rect.left}px`;
    dropdown.style.width = `${rect.width}px`;
  }

  /**
   * Search products via enriched API
   */
  async _searchProducts(query, resultsContainer, currentIds, searchInput, onSelect) {
    resultsContainer.innerHTML =
      '<div class="product-picker__loading"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    resultsContainer.style.display = 'block';
    this._positionFixedDropdown(resultsContainer, searchInput);

    try {
      const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/api/page-builder';
      const response = await fetch(
        `${apiBaseUrl}/product-search/?search=${encodeURIComponent(query)}&limit=10`
      );
      const data = await response.json();

      const products = (data.products || []).filter(p => !currentIds.includes(p.id));

      if (products.length === 0) {
        resultsContainer.innerHTML =
          '<div class="product-picker__no-results">No products found</div>';
        return;
      }

      resultsContainer.innerHTML = '';
      products.forEach(product => {
        const item = document.createElement('div');
        item.className = 'product-picker__result-item';
        item.innerHTML = `
                    <div class="product-picker__result-thumb">
                        ${product.thumbnail ? `<img src="${product.thumbnail}" alt="">` : '<i class="fas fa-box"></i>'}
                    </div>
                    <div class="product-picker__result-info">
                        <div class="product-picker__result-name">${this.escapeHtml(product.name)}</div>
                        <div class="product-picker__result-meta">
                            <span class="product-picker__result-price">${this.escapeHtml(product.price)}</span>
                            ${product.sku ? `<span class="product-picker__result-sku">${this.escapeHtml(product.sku)}</span>` : ''}
                        </div>
                    </div>
                `;
        item.addEventListener('click', () => onSelect(product));
        resultsContainer.appendChild(item);
      });
    } catch (error) {
      console.error('Product search error:', error);
      resultsContainer.innerHTML = '<div class="product-picker__error">Search failed</div>';
    }
  }

  /**
   * Load existing product selections by IDs
   */
  async _loadProductPickerSelections(selectedList, productIds, key, emptyState, syncValue) {
    if (!productIds.length) return;

    try {
      const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/api/page-builder';
      const response = await fetch(`${apiBaseUrl}/product-search/?ids=${productIds.join(',')}`);
      const data = await response.json();

      selectedList.innerHTML = '';
      (data.products || []).forEach(product => {
        this._addProductPickerCard(selectedList, product, productIds, key, emptyState, syncValue);
      });
    } catch (error) {
      console.error('Failed to load product selections:', error);
    }
  }

  /**
   * Add a product card to the selected list
   */
  _addProductPickerCard(selectedList, product, productIds, key, emptyState, syncValue) {
    const card = document.createElement('div');
    card.className = 'product-picker__card';
    card.dataset.productId = product.id;
    card.draggable = true;

    card.innerHTML = `
            <div class="product-picker__card-drag" title="Drag to reorder">
                <i class="fas fa-grip-vertical"></i>
            </div>
            <div class="product-picker__card-thumb">
                ${product.thumbnail ? `<img src="${product.thumbnail}" alt="">` : '<i class="fas fa-box"></i>'}
            </div>
            <div class="product-picker__card-info">
                <div class="product-picker__card-name">${this.escapeHtml(product.name)}</div>
                <div class="product-picker__card-price">${this.escapeHtml(product.price)}${product.is_on_sale ? ' <span class="product-picker__sale-badge">Sale</span>' : ''}</div>
            </div>
            <button type="button" class="product-picker__card-remove" title="Remove">
                <i class="fas fa-times"></i>
            </button>
        `;

    // Remove handler
    card.querySelector('.product-picker__card-remove').addEventListener('click', () => {
      const idx = productIds.indexOf(product.id);
      if (idx > -1) productIds.splice(idx, 1);
      syncValue();
      card.remove();
      if (productIds.length === 0) emptyState.style.display = '';
    });

    // Drag & drop reorder
    card.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', product.id);
      card.classList.add('product-picker__card--dragging');
    });
    card.addEventListener('dragend', () => {
      card.classList.remove('product-picker__card--dragging');
    });
    card.addEventListener('dragover', e => {
      e.preventDefault();
      card.classList.add('product-picker__card--dragover');
    });
    card.addEventListener('dragleave', () => {
      card.classList.remove('product-picker__card--dragover');
    });
    card.addEventListener('drop', e => {
      e.preventDefault();
      card.classList.remove('product-picker__card--dragover');
      const draggedId = parseInt(e.dataTransfer.getData('text/plain'));
      const targetId = product.id;
      if (draggedId === targetId) return;

      // Reorder in the productIds array
      const fromIdx = productIds.indexOf(draggedId);
      const toIdx = productIds.indexOf(targetId);
      if (fromIdx > -1 && toIdx > -1) {
        productIds.splice(fromIdx, 1);
        productIds.splice(toIdx, 0, draggedId);
        syncValue();

        // Reorder DOM
        const draggedCard = selectedList.querySelector(`[data-product-id="${draggedId}"]`);
        if (draggedCard) {
          selectedList.insertBefore(draggedCard, card);
        }
      }
    });

    selectedList.appendChild(card);
  }

  // =========================================================================
  // Entity Picker - search and select categories, collections, etc.
  // =========================================================================

  /**
   * Render entity picker (category, collection) with search
   */
  renderEntityPicker(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'entity-picker';
    wrapper.dataset.propertyKey = key;

    const entityType = config.entity_type || 'category';
    const currentId = value || null;

    // Hidden input for form data collection
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = key;
    hiddenInput.id = `prop-${key}`;
    hiddenInput.value = currentId || '';
    wrapper.appendChild(hiddenInput);

    // Helper to sync hidden input and fire change
    const syncValue = val => {
      hiddenInput.value = val != null ? val : '';
      hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
    };

    // Search input
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'property-input entity-picker__search';
    searchInput.placeholder = `Search ${entityType}...`;

    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'entity-picker__results';
    resultsContainer.style.display = 'none';
    document.body.appendChild(resultsContainer);

    // Preview of selected entity
    const preview = document.createElement('div');
    preview.className = 'entity-picker__preview';
    preview.style.display = 'none';

    wrapper.appendChild(searchInput);
    wrapper.appendChild(preview);

    // Load current selection if exists
    if (currentId) {
      searchInput.style.display = 'none';
      this._loadEntityPreview(entityType, currentId, preview, searchInput, syncValue);
    }

    // Search with debounce
    let searchTimeout;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      const query = searchInput.value.trim();

      if (query.length < 2) {
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        return;
      }

      searchTimeout = setTimeout(async () => {
        await this._searchEntities(entityType, query, resultsContainer, searchInput, entity => {
          syncValue(entity.id);
          searchInput.style.display = 'none';
          searchInput.value = '';
          resultsContainer.style.display = 'none';
          this._showEntityPreview(preview, entity, searchInput, syncValue);
        });
      }, 300);
    });

    // Close results on outside click (check both wrapper and results container since it's in body)
    document.addEventListener('click', e => {
      if (!wrapper.contains(e.target) && !resultsContainer.contains(e.target)) {
        resultsContainer.style.display = 'none';
      }
    });

    // Clean up body-appended dropdown when wrapper is removed from DOM
    const cleanupObserver = new MutationObserver(() => {
      if (!document.body.contains(wrapper)) {
        resultsContainer.remove();
        cleanupObserver.disconnect();
      }
    });
    requestAnimationFrame(() => {
      if (wrapper.parentElement) {
        cleanupObserver.observe(wrapper.parentElement, { childList: true });
      }
    });

    return wrapper;
  }

  /**
   * Search entities via link-sources API
   */
  async _searchEntities(entityType, query, resultsContainer, searchInput, onSelect) {
    resultsContainer.innerHTML =
      '<div class="entity-picker__loading"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    resultsContainer.style.display = 'block';
    this._positionFixedDropdown(resultsContainer, searchInput);

    try {
      const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/api/page-builder';

      let url, resultsKey;
      if (entityType === 'collection') {
        // Collections are not in link-sources, use product-search for now or a custom endpoint
        // For now, use link-sources with type=category as a fallback
        url = `${apiBaseUrl}/link-sources/?type=category&search=${encodeURIComponent(query)}&limit=10`;
        resultsKey = 'categories';
      } else {
        url = `${apiBaseUrl}/link-sources/?type=${entityType}&search=${encodeURIComponent(query)}&limit=10`;
        resultsKey = entityType === 'category' ? 'categories' : `${entityType}s`;
      }

      const response = await fetch(url);
      const data = await response.json();
      const results = data[resultsKey] || [];

      if (results.length === 0) {
        resultsContainer.innerHTML =
          '<div class="entity-picker__no-results">No results found</div>';
        return;
      }

      resultsContainer.innerHTML = '';
      results.forEach(entity => {
        const item = document.createElement('div');
        item.className = 'entity-picker__result-item';
        item.innerHTML = `
                    <div class="entity-picker__result-thumb">
                        ${entity.thumbnail ? `<img src="${entity.thumbnail}" alt="">` : '<i class="fas fa-folder"></i>'}
                    </div>
                    <div class="entity-picker__result-info">
                        <div class="entity-picker__result-name">${this.escapeHtml(entity.name || entity.title)}</div>
                    </div>
                `;
        item.addEventListener('click', () => onSelect(entity));
        resultsContainer.appendChild(item);
      });
    } catch (error) {
      console.error('Entity search error:', error);
      resultsContainer.innerHTML = '<div class="entity-picker__error">Search failed</div>';
    }
  }

  /**
   * Load and show entity preview for a saved ID
   */
  async _loadEntityPreview(entityType, entityId, preview, searchInput, syncValue) {
    try {
      const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/api/page-builder';
      const response = await fetch(
        `${apiBaseUrl}/link-sources/?type=${entityType}&search=&limit=50`
      );
      const data = await response.json();
      const resultsKey = entityType === 'category' ? 'categories' : `${entityType}s`;
      const entities = data[resultsKey] || [];
      const entity = entities.find(e => e.id === entityId);

      if (entity) {
        this._showEntityPreview(preview, entity, searchInput, syncValue);
      } else {
        // Entity not found - show search input
        searchInput.style.display = '';
        preview.style.display = 'none';
      }
    } catch (error) {
      console.error('Failed to load entity preview:', error);
      searchInput.style.display = '';
    }
  }

  /**
   * Show selected entity preview with clear button
   */
  _showEntityPreview(preview, entity, searchInput, syncValue) {
    preview.innerHTML = `
            <div class="entity-picker__preview-content">
                <div class="entity-picker__preview-thumb">
                    ${entity.thumbnail ? `<img src="${entity.thumbnail}" alt="">` : '<i class="fas fa-folder"></i>'}
                </div>
                <div class="entity-picker__preview-name">${this.escapeHtml(entity.name || entity.title)}</div>
                <button type="button" class="entity-picker__preview-clear" title="Clear">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
    preview.style.display = 'block';

    preview.querySelector('.entity-picker__preview-clear').addEventListener('click', () => {
      syncValue(null);
      preview.style.display = 'none';
      searchInput.style.display = '';
      searchInput.focus();
    });
  }

  // =========================================================================
  // Category Picker - search and select multiple categories
  // =========================================================================

  /**
   * Render category picker for category_showcase element.
   * Shows a search bar to find categories, selected categories as cards with reorder/remove.
   */
  renderCategoryPicker(key, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'category-picker';
    wrapper.dataset.propertyKey = key;

    // Hidden input for form data collection
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = key;
    hiddenInput.id = `prop-${key}`;
    wrapper.appendChild(hiddenInput);

    // Current category IDs
    const categoryIds = Array.isArray(value) ? [...value] : [];
    hiddenInput.value = JSON.stringify(categoryIds);

    // Helper to sync hidden input and fire change
    const syncValue = () => {
      hiddenInput.value = JSON.stringify(categoryIds);
      hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
    };

    // Search input area
    const searchWrapper = document.createElement('div');
    searchWrapper.className = 'category-picker__search';

    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.className = 'property-input category-picker__search-input';
    searchInput.placeholder = 'Search categories by name...';
    searchWrapper.appendChild(searchInput);

    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'category-picker__results';
    resultsContainer.style.display = 'none';
    document.body.appendChild(resultsContainer);

    wrapper.appendChild(searchWrapper);

    // Selected categories list
    const selectedList = document.createElement('div');
    selectedList.className = 'category-picker__selected';
    wrapper.appendChild(selectedList);

    // Empty state
    const emptyState = document.createElement('div');
    emptyState.className = 'category-picker__empty';
    emptyState.innerHTML =
      '<i class="fas fa-search"></i><span>Search and add categories to display</span>';
    wrapper.appendChild(emptyState);

    // Load existing selections
    if (categoryIds.length > 0) {
      emptyState.style.display = 'none';
      this._loadCategoryPickerSelections(selectedList, categoryIds, key, emptyState, syncValue);
    }

    // Search with debounce
    let searchTimeout;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimeout);
      const query = searchInput.value.trim();

      if (query.length < 2) {
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
        return;
      }

      searchTimeout = setTimeout(async () => {
        await this._searchCategories(
          query,
          resultsContainer,
          categoryIds,
          searchInput,
          category => {
            // Add category ID to the list
            categoryIds.push(category.id);
            syncValue();

            // Add to selected list UI
            this._addCategoryPickerCard(
              selectedList,
              category,
              categoryIds,
              key,
              emptyState,
              syncValue
            );
            emptyState.style.display = 'none';

            // Clear search
            searchInput.value = '';
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
          }
        );
      }, 300);
    });

    // Close results on outside click
    document.addEventListener('click', e => {
      if (!searchWrapper.contains(e.target) && !resultsContainer.contains(e.target)) {
        resultsContainer.style.display = 'none';
      }
    });

    // Clean up body-appended dropdown when wrapper is removed from DOM
    const cleanupObserver = new MutationObserver(() => {
      if (!document.body.contains(wrapper)) {
        resultsContainer.remove();
        cleanupObserver.disconnect();
      }
    });
    requestAnimationFrame(() => {
      if (wrapper.parentElement) {
        cleanupObserver.observe(wrapper.parentElement, { childList: true });
      }
    });

    return wrapper;
  }

  /**
   * Search categories via link-sources API
   */
  async _searchCategories(query, resultsContainer, currentIds, searchInput, onSelect) {
    resultsContainer.innerHTML =
      '<div class="category-picker__loading"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    resultsContainer.style.display = 'block';
    this._positionFixedDropdown(resultsContainer, searchInput);

    try {
      const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/api/page-builder';
      const response = await fetch(
        `${apiBaseUrl}/link-sources/?type=category&search=${encodeURIComponent(query)}&limit=20`
      );
      const data = await response.json();

      const categories = (data.categories || []).filter(c => !currentIds.includes(c.id));

      if (categories.length === 0) {
        resultsContainer.innerHTML =
          '<div class="category-picker__no-results">No categories found</div>';
        return;
      }

      resultsContainer.innerHTML = '';
      categories.forEach(category => {
        const item = document.createElement('div');
        item.className = 'category-picker__result-item';
        item.innerHTML = `
                    <div class="category-picker__result-thumb">
                        ${category.thumbnail ? `<img src="${category.thumbnail}" alt="">` : '<i class="fas fa-folder"></i>'}
                    </div>
                    <div class="category-picker__result-info">
                        <div class="category-picker__result-name">${this.escapeHtml(category.name || category.title)}</div>
                    </div>
                `;
        item.addEventListener('click', () => onSelect(category));
        resultsContainer.appendChild(item);
      });
    } catch (error) {
      console.error('Category search error:', error);
      resultsContainer.innerHTML = '<div class="category-picker__error">Search failed</div>';
    }
  }

  /**
   * Load existing category selections by IDs
   */
  async _loadCategoryPickerSelections(selectedList, categoryIds, key, emptyState, syncValue) {
    if (!categoryIds.length) return;

    try {
      const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/api/page-builder';
      // Fetch all categories to match by ID
      const response = await fetch(`${apiBaseUrl}/link-sources/?type=category&search=&limit=100`);
      const data = await response.json();
      const allCategories = data.categories || [];

      selectedList.innerHTML = '';
      // Preserve order from categoryIds
      categoryIds.forEach(id => {
        const category = allCategories.find(c => c.id === id);
        if (category) {
          this._addCategoryPickerCard(
            selectedList,
            category,
            categoryIds,
            key,
            emptyState,
            syncValue
          );
        }
      });
    } catch (error) {
      console.error('Failed to load category selections:', error);
    }
  }

  /**
   * Add a category card to the selected list
   */
  _addCategoryPickerCard(selectedList, category, categoryIds, key, emptyState, syncValue) {
    const card = document.createElement('div');
    card.className = 'category-picker__card';
    card.dataset.categoryId = category.id;
    card.draggable = true;

    card.innerHTML = `
            <div class="category-picker__card-drag" title="Drag to reorder">
                <i class="fas fa-grip-vertical"></i>
            </div>
            <div class="category-picker__card-thumb">
                ${category.thumbnail ? `<img src="${category.thumbnail}" alt="">` : '<i class="fas fa-folder"></i>'}
            </div>
            <div class="category-picker__card-info">
                <div class="category-picker__card-name">${this.escapeHtml(category.name || category.title)}</div>
            </div>
            <button type="button" class="category-picker__card-remove" title="Remove">
                <i class="fas fa-times"></i>
            </button>
        `;

    // Remove handler
    card.querySelector('.category-picker__card-remove').addEventListener('click', () => {
      const idx = categoryIds.indexOf(category.id);
      if (idx > -1) categoryIds.splice(idx, 1);
      syncValue();
      card.remove();
      if (categoryIds.length === 0) emptyState.style.display = '';
    });

    // Drag & drop reorder
    card.addEventListener('dragstart', e => {
      e.dataTransfer.setData('text/plain', category.id);
      card.classList.add('category-picker__card--dragging');
    });
    card.addEventListener('dragend', () => {
      card.classList.remove('category-picker__card--dragging');
    });
    card.addEventListener('dragover', e => {
      e.preventDefault();
      card.classList.add('category-picker__card--dragover');
    });
    card.addEventListener('dragleave', () => {
      card.classList.remove('category-picker__card--dragover');
    });
    card.addEventListener('drop', e => {
      e.preventDefault();
      card.classList.remove('category-picker__card--dragover');
      const draggedId = parseInt(e.dataTransfer.getData('text/plain'));
      const targetId = category.id;
      if (draggedId === targetId) return;

      // Reorder in the categoryIds array
      const fromIdx = categoryIds.indexOf(draggedId);
      const toIdx = categoryIds.indexOf(targetId);
      if (fromIdx > -1 && toIdx > -1) {
        categoryIds.splice(fromIdx, 1);
        categoryIds.splice(toIdx, 0, draggedId);
        syncValue();

        // Reorder DOM
        const draggedCard = selectedList.querySelector(`[data-category-id="${draggedId}"]`);
        if (draggedCard) {
          selectedList.insertBefore(draggedCard, card);
        }
      }
    });

    selectedList.appendChild(card);
  }

  /**
   * Initialize utilities for advanced property types
   */
  initializeUtilities(form, properties, values) {
    // Initialize translation editor for translatable fields
    this.initializeTranslationFields(form, properties, values);

    // Initialize other utilities
    for (const [key, config] of Object.entries(properties)) {
      // Skip property groups - their nested properties are already flattened by flattenTabProperties()
      // Processing them here would cause duplicate utility initialization
      if (config.type === 'property_group') {
        continue;
      }

      if (this.utilityMap[config.type]) {
        const wrapper = form.querySelector(`[data-property="${key}"] .property-input-with-utility`);
        if (!wrapper) continue;

        const input = wrapper.querySelector('input');
        if (!input) continue;

        const utilityClass = this.utilityMap[config.type];
        const UtilityConstructor = window[utilityClass];

        if (UtilityConstructor) {
          // Create utility instance with options
          // Pass property context so utilities can emit property-specific updates
          const utilityOptions = {
            propertyKey: key, // The property key (e.g., 'button_background', 'typography')
            elementId: form.dataset.elementId,
            elementType: form.dataset.elementType,
            onChange: (value, cssString) => {
              // Handle border editor which passes (borderObject, cssString)
              // and other utilities which pass just (value)
              const finalValue = typeof cssString === 'string' ? cssString : value;
              input.value = finalValue;

              // Apply live preview immediately
              const elementId = form.dataset.elementId;
              if (window.livePreview && elementId) {
                const styleUpdate = {};
                styleUpdate[key] = finalValue;
                window.livePreview.applyStyles(elementId, styleUpdate);
              }

              this.handlePropertyChange(form, key, finalValue);
            },
            onApply: (value, cssString) => {
              // Handle border editor which passes (borderObject, cssString)
              // and other utilities which pass just (value)
              const finalValue = typeof cssString === 'string' ? cssString : value;
              input.value = finalValue;

              // Apply final styles
              const elementId = form.dataset.elementId;
              if (window.livePreview && elementId) {
                const styleUpdate = {};
                styleUpdate[key] = finalValue;
                window.livePreview.applyStyles(elementId, styleUpdate);
              }

              this.handlePropertyChange(form, key, finalValue);
            },
          };

          // Add shadow type for shadow editor
          if (config.type === 'shadow' && config.shadow_type) {
            utilityOptions.shadowType = config.shadow_type;
          }

          // Handle focal point editor specially - needs image URL and wrapper
          if (config.type === 'focal_point') {
            // Get the image URL from the src media library input in the form
            // The media library input stores the actual URL, whereas values['src']
            // might have a different format or be a media ID
            const srcInput = form.querySelector('#prop-src');
            const imageUrl = srcInput
              ? srcInput.value || srcInput.dataset.originalUrl || ''
              : values['src'] || '';
            console.log(
              '[PropertyRenderer] Focal point image URL:',
              imageUrl,
              'srcInput:',
              srcInput,
              'srcInput.value:',
              srcInput?.value
            );
            utilityOptions.imageUrl = imageUrl;
            utilityOptions.wrapper = wrapper;

            // Add callback to update position display
            const positionDisplay = wrapper.querySelector('.focal-point-position');
            const originalOnChange = utilityOptions.onChange;
            utilityOptions.onChange = (value, cssString) => {
              // Update position display
              if (positionDisplay && typeof value === 'object') {
                const x = value.default?.x ?? value.x ?? 0.5;
                const y = value.default?.y ?? value.y ?? 0.5;
                positionDisplay.textContent = this.formatFocalPointPosition(x, y);
              }
              // Store as JSON
              input.value = JSON.stringify(value);
              originalOnChange(JSON.stringify(value), cssString);
            };
            const originalOnApply = utilityOptions.onApply;
            utilityOptions.onApply = (value, cssString) => {
              if (positionDisplay && typeof value === 'object') {
                const x = value.default?.x ?? value.x ?? 0.5;
                const y = value.default?.y ?? value.y ?? 0.5;
                positionDisplay.textContent = this.formatFocalPointPosition(x, y);
              }
              input.value = JSON.stringify(value);
              originalOnApply(JSON.stringify(value), cssString);
            };
          }

          const utility = new UtilityConstructor(utilityOptions);

          // For background editor, check if there's stored _data (contains hover/full config)
          if (config.type === 'background') {
            const dataKey = key + '_data';
            if (values[dataKey]) {
              // Create hidden input for the stored data
              let dataInput = wrapper.querySelector(`input[name="${dataKey}"]`);
              if (!dataInput) {
                dataInput = document.createElement('input');
                dataInput.type = 'hidden';
                dataInput.name = dataKey;
                wrapper.appendChild(dataInput);
              }
              dataInput.value =
                typeof values[dataKey] === 'string'
                  ? values[dataKey]
                  : JSON.stringify(values[dataKey]);
              console.log('[PropertyRenderer] Restored background_data hidden input:', dataKey);
            }
          }

          // Pass the input element and its current value to the utility
          utility.attach(input, input.value || values[key] || config.default || '');

          // Store reference for cleanup
          this.activeUtilities.set(key, utility);
        }
      }
    }

    // Initialize image size switcher for image elements
    this.initializeImageSizeSwitcher(form);
  }

  /**
   * Initialize image size switcher for media library integration
   * When image_size changes, update the src with the appropriate thumbnail URL
   */
  initializeImageSizeSwitcher(form) {
    const imageSizeSelect = form.querySelector('#prop-image_size');
    const srcInput = form.querySelector('#prop-src');
    const previewContainer = form.querySelector('.media-library-preview');

    if (!imageSizeSelect || !srcInput) {
      return; // Not an image element or missing required inputs
    }

    imageSizeSelect.addEventListener('change', e => {
      const selectedSize = e.target.value;
      const thumbnailsJson = srcInput.dataset.thumbnails;
      const originalUrl = srcInput.dataset.originalUrl;

      if (!thumbnailsJson && !originalUrl) {
        return; // No image data stored
      }

      let newUrl = srcInput.value; // Default to current value

      if (selectedSize === 'original' && originalUrl) {
        newUrl = originalUrl;
      } else if (thumbnailsJson) {
        try {
          const thumbnails = JSON.parse(thumbnailsJson);
          // Map size preset to thumbnail preset names
          const sizeMap = {
            small: 'small',
            medium: 'medium',
            large: 'large',
            original: null, // handled above
          };

          const presetName = sizeMap[selectedSize];
          if (presetName) {
            const thumbnail = thumbnails.find(t => t.preset === presetName);
            if (thumbnail && thumbnail.url) {
              newUrl = thumbnail.url;
            }
          }
        } catch (err) {
          console.warn('[PropertyRenderer] Failed to parse thumbnails:', err);
        }
      }

      // Update the src input value
      if (newUrl !== srcInput.value) {
        srcInput.value = newUrl;

        // Update the preview image
        if (previewContainer) {
          const previewImg = previewContainer.querySelector('img');
          if (previewImg) {
            previewImg.src = newUrl;
          }
        }

        // Trigger change event for live preview
        srcInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
  }

  /**
   * Initialize translation editor for translatable fields
   */
  initializeTranslationFields(form, properties, values) {
    // Check if TranslationEditor is available
    const TranslationEditorClass = window.TranslationEditorUtility || window.TranslationEditor;
    if (!TranslationEditorClass) {
      return;
    }

    // Find all translatable fields
    const translatableWrappers = form.querySelectorAll('.translatable-field-wrapper');

    translatableWrappers.forEach(wrapper => {
      const fieldKey = wrapper.dataset.fieldKey;
      const input = wrapper.querySelector('textarea, input[type="text"]');

      if (!input || !fieldKey) return;

      // Get element data from form
      const elementId = form.dataset.elementId;
      const elementType = form.dataset.elementType;

      // Create translation editor instance for this field
      const editor = new TranslationEditorClass({
        onTranslate: async languages => {
          // Handle translation
          console.log('Translating field', fieldKey, 'to', languages);
          // The actual translation logic will be handled by the editor
        },
      });

      // Attach to the input
      editor.attach(input, fieldKey);

      // Store reference for cleanup
      this.activeUtilities.set(`translation_${fieldKey}`, editor);
    });
  }

  /**
   * Setup change handlers for form inputs
   */
  setupChangeHandlers(form, elementId) {
    // Debounce function
    const debounce = (func, wait) => {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    };

    // Update handler for server sync
    const updateElement = debounce(() => {
      const formData = new FormData(form);
      const properties = {};

      for (const [key, value] of formData.entries()) {
        // Try to parse JSON values (for array properties like frames, images, etc.)
        if (
          value &&
          typeof value === 'string' &&
          (value.startsWith('[') || value.startsWith('{'))
        ) {
          try {
            properties[key] = JSON.parse(value);
          } catch (e) {
            properties[key] = value;
          }
        } else {
          properties[key] = value;
        }
      }

      // Get checkboxes (FormData doesn't include unchecked boxes)
      form.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
        properties[checkbox.name] = checkbox.checked;
      });

      // Call onPropertyChange callback if defined (used by PageSettingsManager)
      if (typeof this.onPropertyChange === 'function') {
        // Call for each changed property
        for (const [key, value] of Object.entries(properties)) {
          this.onPropertyChange(key, value, null);
        }
      }

      // Send update to server
      this.updateElementProperties(elementId, properties);
    }, 500);

    // Live preview handler for instant text feedback (shorter debounce)
    const updateLivePreview = debounce((changedKey, changedValue) => {
      if (window.livePreview && elementId) {
        const update = {};
        update[changedKey] = changedValue;
        window.livePreview.applyStyles(elementId, update);
      }
    }, 100);

    // Handler for show_when re-renders (immediate, not debounced)
    const handleShowWhenChange = e => {
      const target = e.target;
      const propertyKey = target.name;

      if (!propertyKey) return;

      // Update current values
      if (target.type === 'checkbox') {
        this.currentValues[propertyKey] = target.checked;
      } else {
        this.currentValues[propertyKey] = target.value;
      }

      // Check if this property has show_when dependents
      if (this.hasShowWhenDependents(propertyKey)) {
        // Debounce the re-render slightly to allow value to settle
        setTimeout(() => {
          this.refreshPropertiesPanel();
          // After re-render, sync full current values to server so preview
          // updates correctly (e.g., switching data_source back to "static"
          // needs to re-render with stored product_ids)
          this.updateElementProperties(elementId, { ...this.currentValues });
        }, 50);
      }
    };

    // Initialize previous tag value for heading elements
    const tagSelect = form.querySelector('select[name="tag"]');
    if (tagSelect) {
      this.previousTagValue = tagSelect.value;
    }

    // Add listeners to all inputs
    form.addEventListener('input', e => {
      // Trigger server sync (debounced)
      updateElement();

      // Trigger instant live preview for text inputs, number inputs, and range sliders
      const target = e.target;
      if (
        target.name &&
        (target.type === 'text' ||
          target.type === 'number' ||
          target.tagName === 'TEXTAREA' ||
          target.type === 'range')
      ) {
        updateLivePreview(target.name, target.value);
      }
    });
    form.addEventListener('change', e => {
      const target = e.target;

      // Special handling for tag changes on heading elements
      if (target.name === 'tag' && target.tagName === 'SELECT') {
        const typographyInput = form.querySelector('input[name="typography"]');
        const textColorInput = form.querySelector('input[name="text_color"]');

        const hasTypography =
          typographyInput && typographyInput.value && typographyInput.value.trim() !== '';
        const hasTextColor =
          textColorInput && textColorInput.value && textColorInput.value.trim() !== '';

        // If typography or text_color is set, show confirmation dialog
        if (
          (hasTypography || hasTextColor) &&
          this.previousTagValue &&
          target.value !== this.previousTagValue
        ) {
          // Show dialog - don't trigger updates yet
          this.showTagChangeDialog(
            target,
            target.value,
            this.previousTagValue,
            form,
            updateElement,
            updateLivePreview
          );
          return; // Don't proceed with normal change handling
        }

        // No typography set, just update the previous tag value
        this.previousTagValue = target.value;
      }

      updateElement();
      handleShowWhenChange(e);

      // Also trigger live preview on change for select/checkbox
      if (target.name) {
        const value = target.type === 'checkbox' ? target.checked : target.value;
        updateLivePreview(target.name, value);
      }
    });
  }

  /**
   * Show tag change confirmation dialog when typography is set
   * @param {HTMLSelectElement} tagSelect - The tag select element
   * @param {string} newTag - The new tag value
   * @param {string} previousTag - The previous tag value
   * @param {HTMLFormElement} form - The form element
   * @param {Function} updateElement - The update function to call after confirmation
   * @param {Function} updateLivePreview - The live preview function
   */
  showTagChangeDialog(tagSelect, newTag, previousTag, form, updateElement, updateLivePreview) {
    // Remove any existing dialog
    const existingDialog = document.getElementById('tag-change-dialog');
    if (existingDialog) {
      existingDialog.remove();
    }

    // Create dialog HTML
    const dialogHTML = `
            <div id="tag-change-dialog" class="modal-overlay" style="
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(0, 0, 0, 0.6);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 10000;
                padding: 2rem;
            ">
                <div class="modal-content" style="
                    background: var(--body-bg, #1a1a2e);
                    border-radius: 12px;
                    max-width: 420px;
                    width: 100%;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
                    border: 1px solid var(--border-color, #2d2d44);
                ">
                    <div class="modal-header" style="
                        padding: 1.25rem 1.5rem;
                        border-bottom: 1px solid var(--border-color, #2d2d44);
                        display: flex;
                        align-items: center;
                        justify-content: space-between;
                    ">
                        <h3 style="margin: 0; font-size: 1.1rem; color: var(--body-fg, #e0e0e0); display: flex; align-items: center; gap: 0.5rem;">
                            <i class="fas fa-heading" style="color: var(--primary, #6366f1);"></i>
                            Change Heading Tag
                        </h3>
                        <button id="tag-dialog-close" style="
                            background: none;
                            border: none;
                            color: var(--muted-fg, #888);
                            cursor: pointer;
                            padding: 0.25rem;
                            font-size: 1.1rem;
                        ">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="modal-body" style="padding: 1.5rem;">
                        <p style="margin: 0 0 1rem; color: var(--body-fg, #e0e0e0); line-height: 1.5;">
                            This heading has custom typography settings. Changing from <strong>${previousTag.toUpperCase()}</strong> to <strong>${newTag.toUpperCase()}</strong> may affect the appearance.
                        </p>
                        <p style="margin: 0; color: var(--muted-fg, #888); font-size: 0.9rem;">
                            How would you like to proceed?
                        </p>
                    </div>
                    <div class="modal-footer" style="
                        padding: 1rem 1.5rem;
                        border-top: 1px solid var(--border-color, #2d2d44);
                        display: flex;
                        gap: 0.75rem;
                        justify-content: flex-end;
                        flex-wrap: wrap;
                    ">
                        <button id="tag-dialog-cancel" style="
                            padding: 0.6rem 1rem;
                            border-radius: 6px;
                            border: 1px solid var(--border-color, #2d2d44);
                            background: transparent;
                            color: var(--body-fg, #e0e0e0);
                            cursor: pointer;
                            font-size: 0.875rem;
                        ">
                            Cancel
                        </button>
                        <button id="tag-dialog-reset" style="
                            padding: 0.6rem 1rem;
                            border-radius: 6px;
                            border: none;
                            background: var(--error-fg, #ef4444);
                            color: white;
                            cursor: pointer;
                            font-size: 0.875rem;
                        ">
                            Reset to Defaults
                        </button>
                        <button id="tag-dialog-keep" style="
                            padding: 0.6rem 1rem;
                            border-radius: 6px;
                            border: none;
                            background: var(--primary, #6366f1);
                            color: white;
                            cursor: pointer;
                            font-size: 0.875rem;
                        ">
                            Keep Typography
                        </button>
                    </div>
                </div>
            </div>
        `;

    // Insert dialog into DOM
    document.body.insertAdjacentHTML('beforeend', dialogHTML);

    const dialog = document.getElementById('tag-change-dialog');
    const closeBtn = document.getElementById('tag-dialog-close');
    const cancelBtn = document.getElementById('tag-dialog-cancel');
    const resetBtn = document.getElementById('tag-dialog-reset');
    const keepBtn = document.getElementById('tag-dialog-keep');

    // Close dialog helper
    const closeDialog = () => {
      dialog.remove();
    };

    // Cancel - revert to previous tag
    const handleCancel = () => {
      tagSelect.value = previousTag;
      this.previousTagValue = previousTag;
      closeDialog();
    };

    // Reset to defaults - clear typography and text_color
    const handleReset = () => {
      // Clear typography and text_color in the form
      const typographyInput = form.querySelector('input[name="typography"]');
      const textColorInput = form.querySelector('input[name="text_color"]');

      if (typographyInput) {
        typographyInput.value = '';
      }
      if (textColorInput) {
        textColorInput.value = '';
      }

      // Update previous tag value
      this.previousTagValue = newTag;

      // Trigger updates
      updateElement();
      updateLivePreview('tag', newTag);

      closeDialog();
    };

    // Keep typography - just change the tag
    const handleKeep = () => {
      // Update previous tag value
      this.previousTagValue = newTag;

      // Trigger updates (typography is already preserved)
      updateElement();
      updateLivePreview('tag', newTag);

      closeDialog();
    };

    // Event listeners
    closeBtn.addEventListener('click', handleCancel);
    cancelBtn.addEventListener('click', handleCancel);
    resetBtn.addEventListener('click', handleReset);
    keepBtn.addEventListener('click', handleKeep);

    // Close on overlay click
    dialog.addEventListener('click', e => {
      if (e.target === dialog) {
        handleCancel();
      }
    });

    // Close on Escape key
    const handleEscape = e => {
      if (e.key === 'Escape') {
        handleCancel();
        document.removeEventListener('keydown', handleEscape);
      }
    };
    document.addEventListener('keydown', handleEscape);
  }

  /**
   * Handle property change from utility
   */
  handlePropertyChange(form, key, value) {
    // Trigger form update
    const event = new Event('input', { bubbles: true });
    form.dispatchEvent(event);
  }

  /**
   * Update element properties on server
   */
  async updateElementProperties(elementId, properties) {
    try {
      // Skip update for page settings - PageSettingsManager handles its own saving
      // Page settings use a different API endpoint (/page/<id>/settings/update/)
      if (typeof elementId === 'string' && elementId.startsWith('page-')) {
        console.log(
          '[PropertyRenderer] Skipping element update for page settings (handled by PageSettingsManager)'
        );
        return;
      }

      console.log('[PropertyRenderer] updateElementProperties called:', {
        elementId,
        propertyKeys: Object.keys(properties),
        hasLivePreview: !!window.livePreview,
        hasSendUpdateToServer: !!(
          window.livePreview && typeof window.livePreview.sendUpdateToServer === 'function'
        ),
      });

      // Use live preview manager if available (handles HTML refresh for re-render properties)
      if (window.livePreview && typeof window.livePreview.sendUpdateToServer === 'function') {
        console.log('[PropertyRenderer] Using livePreview.sendUpdateToServer');
        await window.livePreview.sendUpdateToServer(elementId, properties);
        return;
      }

      // Fallback: direct API call (without HTML refresh support)
      const apiBaseUrl = window.builderInstance?.getApiBaseUrl() || '/page_builder/api';
      const response = await fetch(`${apiBaseUrl}/elements/${elementId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({ content: properties }),
      });

      if (!response.ok) {
        throw new Error('Failed to update element');
      }

      // Update preview if available
      if (window.updateElementPreview) {
        window.updateElementPreview(elementId, properties);
      }
    } catch (error) {
      console.error('Error updating element:', error);
    }
  }

  /**
   * Get CSRF token
   */
  getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) return token.value;
    return '';
  }

  /**
   * Render translation section for elements that support translation
   */
  renderTranslationSection(elementData, elementConfig) {
    const section = document.createElement('div');
    section.className = 'translation-section';

    // Get translation coverage if available
    const translations = elementData.content._translations || {};
    const availableLanguages = Object.keys(translations);
    const translationMeta = elementData.content._translation_meta || {};

    section.innerHTML = `
            <div class="translation-header">
                <h4><i class="fas fa-language"></i> Translations</h4>
                ${
                  availableLanguages.length > 0
                    ? `<span class="translation-badge">${availableLanguages.length} languages</span>`
                    : '<span class="translation-badge no-translations">No translations</span>'
                }
            </div>
            <div class="translation-content">
                ${
                  translationMeta.last_updated
                    ? `<p class="translation-info">Last updated: ${new Date(translationMeta.last_updated).toLocaleDateString()}</p>`
                    : ''
                }
                ${
                  availableLanguages.length > 0
                    ? `<p class="translation-languages">Available: ${availableLanguages.join(', ')}</p>`
                    : ''
                }
                <div class="translation-actions">
                    <button type="button" class="btn btn-primary translation-btn" onclick="window.openTranslationEditor('${elementData.id}')">
                        <i class="fas fa-globe"></i> Manage Translations
                    </button>
                </div>
            </div>
        `;

    return section;
  }

  /**
   * Render array input for repeatable items (e.g., frames, images, items)
   */
  renderArrayInput(key, config, value) {
    const container = document.createElement('div');
    container.className = 'array-input-container';
    container.dataset.arrayKey = key;

    // Ensure value is an array
    const items = Array.isArray(value) ? value : config.default || [];
    const itemSchema = config.item_schema || {};
    const itemProperties = itemSchema.properties || config.item_properties || {};

    // Create items list
    const itemsList = document.createElement('div');
    itemsList.className = 'array-items-list';

    // Render each item
    items.forEach((item, index) => {
      const itemElement = this.renderArrayItem(key, index, item, itemProperties, config);
      itemsList.appendChild(itemElement);
    });

    container.appendChild(itemsList);

    // Add button
    const addButton = document.createElement('button');
    addButton.type = 'button';
    addButton.className = 'btn btn--sm btn--outline array-add-btn';
    addButton.innerHTML = '<i class="fas fa-plus"></i> Add Item';
    addButton.addEventListener('click', () => {
      // Create new item with defaults from schema
      const newItem = {};
      for (const [propKey, propConfig] of Object.entries(itemProperties)) {
        newItem[propKey] = propConfig.default !== undefined ? propConfig.default : '';
      }

      // Add to items array
      const currentItems = this.currentValues[key] || [];
      currentItems.push(newItem);
      this.currentValues[key] = currentItems;

      // Re-render the array container
      const newItemElement = this.renderArrayItem(
        key,
        currentItems.length - 1,
        newItem,
        itemProperties,
        config
      );
      itemsList.appendChild(newItemElement);

      // Trigger change
      this.triggerArrayChange(key, currentItems);

      // Expand the new item
      newItemElement.classList.add('expanded');
    });

    container.appendChild(addButton);

    // Store hidden input for form submission
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = key;
    hiddenInput.id = `prop-${key}`;
    hiddenInput.value = JSON.stringify(items);
    container.appendChild(hiddenInput);

    return container;
  }

  /**
   * Render a single array item with collapsible editor
   */
  renderArrayItem(arrayKey, index, item, itemProperties, arrayConfig) {
    const itemContainer = document.createElement('div');
    itemContainer.className = 'array-item';
    itemContainer.dataset.index = index;

    // Get a display title for the item
    const displayTitle =
      item.title || item.name || item.label || item.question || `Item ${index + 1}`;
    const hasImage = item.image || item.src;

    // Item header (collapsible trigger)
    const header = document.createElement('div');
    header.className = 'array-item__header';
    header.innerHTML = `
            <div class="array-item__preview">
                ${hasImage ? `<img src="${item.image || item.src}" alt="" class="array-item__thumb">` : `<span class="array-item__number">${index + 1}</span>`}
                <span class="array-item__title">${this.escapeHtml(displayTitle)}</span>
            </div>
            <div class="array-item__actions">
                <button type="button" class="array-item__btn array-item__btn--move-up" title="Move up" ${index === 0 ? 'disabled' : ''}>
                    <i class="fas fa-chevron-up"></i>
                </button>
                <button type="button" class="array-item__btn array-item__btn--move-down" title="Move down">
                    <i class="fas fa-chevron-down"></i>
                </button>
                <button type="button" class="array-item__btn array-item__btn--delete" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
                <button type="button" class="array-item__btn array-item__btn--toggle">
                    <i class="fas fa-chevron-down"></i>
                </button>
            </div>
        `;

    // Toggle expand/collapse
    header.querySelector('.array-item__btn--toggle').addEventListener('click', () => {
      itemContainer.classList.toggle('expanded');
    });

    // Also toggle on header click (except buttons)
    header.querySelector('.array-item__preview').addEventListener('click', () => {
      itemContainer.classList.toggle('expanded');
    });

    // Move up button
    header.querySelector('.array-item__btn--move-up').addEventListener('click', e => {
      e.stopPropagation();
      this.moveArrayItem(arrayKey, index, index - 1);
    });

    // Move down button
    header.querySelector('.array-item__btn--move-down').addEventListener('click', e => {
      e.stopPropagation();
      this.moveArrayItem(arrayKey, index, index + 1);
    });

    // Delete button
    header.querySelector('.array-item__btn--delete').addEventListener('click', async e => {
      e.stopPropagation();
      if (
        await AdminModal.confirm({
          message: 'Are you sure you want to delete this item?',
          danger: true,
          confirmText: 'Delete',
        })
      ) {
        this.deleteArrayItem(arrayKey, index);
      }
    });

    itemContainer.appendChild(header);

    // Item content (expanded editor)
    const content = document.createElement('div');
    content.className = 'array-item__content';

    // Render each property in the item
    for (const [propKey, propConfig] of Object.entries(itemProperties)) {
      const propValue = item[propKey];
      const fieldWrapper = document.createElement('div');
      fieldWrapper.className = 'array-item__field';

      const label = document.createElement('label');
      label.textContent = propConfig.label || this.formatPropertyName(propKey);
      fieldWrapper.appendChild(label);

      // Render appropriate input based on type
      let input;
      const fullKey = `${arrayKey}[${index}].${propKey}`;

      switch (propConfig.type) {
        case 'image':
          input = this.renderArrayItemImageInput(arrayKey, index, propKey, propConfig, propValue);
          break;
        case 'select':
          input = this.renderArrayItemSelect(arrayKey, index, propKey, propConfig, propValue);
          break;
        case 'boolean':
          input = this.renderArrayItemCheckbox(arrayKey, index, propKey, propConfig, propValue);
          break;
        case 'range':
          input = this.renderArrayItemRange(arrayKey, index, propKey, propConfig, propValue);
          break;
        case 'color':
          input = this.renderArrayItemColor(arrayKey, index, propKey, propConfig, propValue);
          break;
        case 'textarea':
          input = this.renderArrayItemTextarea(arrayKey, index, propKey, propConfig, propValue);
          break;
        case 'url':
          // Check if link_selector is enabled for this URL field
          if (propConfig.link_selector === true) {
            input = this.renderArrayItemLinkSelector(
              arrayKey,
              index,
              propKey,
              propConfig,
              propValue
            );
          } else {
            input = this.renderArrayItemTextInput(arrayKey, index, propKey, propConfig, propValue);
          }
          break;
        case 'link_selector':
          // Explicit link_selector type
          input = this.renderArrayItemLinkSelector(arrayKey, index, propKey, propConfig, propValue);
          break;
        case 'icon_picker':
          input = this.renderArrayItemIconPicker(arrayKey, index, propKey, propConfig, propValue);
          break;
        default:
          input = this.renderArrayItemTextInput(arrayKey, index, propKey, propConfig, propValue);
      }

      fieldWrapper.appendChild(input);

      if (propConfig.help_text) {
        const helpText = document.createElement('small');
        helpText.className = 'property-help-text';
        helpText.textContent = propConfig.help_text;
        fieldWrapper.appendChild(helpText);
      }

      content.appendChild(fieldWrapper);
    }

    itemContainer.appendChild(content);

    return itemContainer;
  }

  /**
   * Render text input for array item
   */
  renderArrayItemTextInput(arrayKey, index, propKey, config, value) {
    const input = document.createElement('input');
    input.type = config.type === 'url' ? 'url' : 'text';
    input.className = 'property-input';
    input.value = value || '';
    input.placeholder = config.placeholder || '';
    input.dataset.arrayKey = arrayKey;
    input.dataset.index = index;
    input.dataset.propKey = propKey;

    // 'input' event: Update local state only (no server sync)
    // This keeps form state consistent while typing without triggering expensive server refreshes
    input.addEventListener('input', () => {
      this.updateArrayItemValue(arrayKey, index, propKey, input.value, false);
    });

    // 'change' event (blur): Trigger server sync
    // This saves the changes when user finishes editing the field
    input.addEventListener('change', () => {
      this.updateArrayItemValue(arrayKey, index, propKey, input.value, true);
    });

    // If field is translatable, wrap it and add translation button
    if (config.translatable) {
      const wrapper = document.createElement('div');
      wrapper.className = 'translatable-field-wrapper';
      wrapper.dataset.translatable = 'true';
      wrapper.dataset.fieldKey = `${arrayKey}[${index}].${propKey}`;
      wrapper.appendChild(input);
      return wrapper;
    }

    return input;
  }

  /**
   * Render textarea for array item
   */
  renderArrayItemTextarea(arrayKey, index, propKey, config, value) {
    const textarea = document.createElement('textarea');
    textarea.className = 'property-textarea';
    textarea.value = value || '';
    textarea.rows = config.rows || 2;
    textarea.placeholder = config.placeholder || '';
    textarea.dataset.arrayKey = arrayKey;
    textarea.dataset.index = index;
    textarea.dataset.propKey = propKey;

    // 'input' event: Update local state only (no server sync)
    textarea.addEventListener('input', () => {
      this.updateArrayItemValue(arrayKey, index, propKey, textarea.value, false);
    });

    // 'change' event (blur): Trigger server sync
    textarea.addEventListener('change', () => {
      this.updateArrayItemValue(arrayKey, index, propKey, textarea.value, true);
    });

    // If field is translatable, wrap it and add translation button
    if (config.translatable) {
      const wrapper = document.createElement('div');
      wrapper.className = 'translatable-field-wrapper';
      wrapper.dataset.translatable = 'true';
      wrapper.dataset.fieldKey = `${arrayKey}[${index}].${propKey}`;
      wrapper.appendChild(textarea);
      return wrapper;
    }

    return textarea;
  }

  /**
   * Render select for array item
   */
  renderArrayItemSelect(arrayKey, index, propKey, config, value) {
    const select = document.createElement('select');
    select.className = 'property-select';
    select.dataset.arrayKey = arrayKey;
    select.dataset.index = index;
    select.dataset.propKey = propKey;

    const options = config.options || [];
    options.forEach(opt => {
      const option = document.createElement('option');
      option.value = opt.value;
      option.textContent = opt.label;
      if (opt.value === value || (value === undefined && opt.value === config.default)) {
        option.selected = true;
      }
      select.appendChild(option);
    });

    select.addEventListener('change', () => {
      this.updateArrayItemValue(arrayKey, index, propKey, select.value);
    });

    return select;
  }

  /**
   * Render checkbox for array item
   */
  renderArrayItemCheckbox(arrayKey, index, propKey, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'checkbox-wrapper';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.className = 'property-checkbox';
    checkbox.checked = value === true || value === 'true';
    checkbox.dataset.arrayKey = arrayKey;
    checkbox.dataset.index = index;
    checkbox.dataset.propKey = propKey;

    checkbox.addEventListener('change', () => {
      this.updateArrayItemValue(arrayKey, index, propKey, checkbox.checked);
    });

    wrapper.appendChild(checkbox);
    return wrapper;
  }

  /**
   * Render range input for array item
   */
  renderArrayItemRange(arrayKey, index, propKey, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'range-input-wrapper';

    const range = document.createElement('input');
    range.type = 'range';
    range.className = 'property-range';
    range.min = config.min || 0;
    range.max = config.max || 100;
    range.step = config.step || 1;
    range.value = value !== undefined ? value : config.default || 0;
    range.dataset.arrayKey = arrayKey;
    range.dataset.index = index;
    range.dataset.propKey = propKey;

    const valueDisplay = document.createElement('span');
    valueDisplay.className = 'range-value';
    valueDisplay.textContent = range.value;

    range.addEventListener('input', () => {
      valueDisplay.textContent = range.value;
    });

    range.addEventListener('change', () => {
      this.updateArrayItemValue(arrayKey, index, propKey, parseFloat(range.value));
    });

    wrapper.appendChild(range);
    wrapper.appendChild(valueDisplay);
    return wrapper;
  }

  /**
   * Render color input for array item
   */
  renderArrayItemColor(arrayKey, index, propKey, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'color-input-wrapper';

    const color = document.createElement('input');
    color.type = 'color';
    color.className = 'property-color';
    color.value = value || config.default || '#000000';
    color.dataset.arrayKey = arrayKey;
    color.dataset.index = index;
    color.dataset.propKey = propKey;

    color.addEventListener('change', () => {
      this.updateArrayItemValue(arrayKey, index, propKey, color.value);
    });

    wrapper.appendChild(color);
    return wrapper;
  }

  /**
   * Render icon picker for array item.
   * Uses IconPickerUtility in composeFullClass mode so the full FA class
   * (e.g., "fas fa-lock") is stored as a single value in the array item data.
   */
  renderArrayItemIconPicker(arrayKey, index, propKey, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'property-input-with-utility array-item-icon-picker';
    wrapper.dataset.utilityType = 'icon_picker';

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'property-input';
    input.value = value || '';
    input.dataset.arrayKey = arrayKey;
    input.dataset.index = index;
    input.dataset.propKey = propKey;

    wrapper.appendChild(input);

    // Initialize IconPickerUtility in composeFullClass mode
    if (typeof window.IconPickerUtility === 'function') {
      const self = this;
      const utility = new window.IconPickerUtility({
        propertyKey: propKey,
        composeFullClass: true,
        onChange: function (composedValue) {
          self.updateArrayItemValue(arrayKey, index, propKey, composedValue, false);
        },
        onApply: function (composedValue) {
          self.updateArrayItemValue(arrayKey, index, propKey, composedValue, true);
        },
      });
      utility.attach(input, value || '');
    }

    return wrapper;
  }

  /**
   * Render link selector for array item (compact inline version)
   * Dropdown for link type + search input for entity selection
   */
  renderArrayItemLinkSelector(arrayKey, index, propKey, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'link-selector-wrapper array-item-link-selector';
    wrapper.dataset.arrayKey = arrayKey;
    wrapper.dataset.index = index;
    wrapper.dataset.propKey = propKey;

    const currentState = this.parseLinkValue(value);

    // Type dropdown (compact)
    const typeSelect = document.createElement('select');
    typeSelect.className = 'property-select link-type-select-inline';

    const options = [
      { value: 'custom', label: 'URL' },
      { value: 'product', label: 'Product' },
      { value: 'page', label: 'Page' },
      { value: 'category', label: 'Category' },
      { value: 'blog', label: 'Blog' },
    ];

    options.forEach(opt => {
      const option = document.createElement('option');
      option.value = opt.value;
      option.textContent = opt.label;
      if (opt.value === currentState.type) option.selected = true;
      typeSelect.appendChild(option);
    });
    wrapper.appendChild(typeSelect);

    // Input container (changes based on type)
    const inputContainer = document.createElement('div');
    inputContainer.className = 'link-selector-input-container';
    wrapper.appendChild(inputContainer);

    // Initialize based on current type
    this.updateArrayItemLinkInput(wrapper, currentState, arrayKey, index, propKey);

    // Type change handler
    typeSelect.addEventListener('change', () => {
      const newType = typeSelect.value;
      this.updateArrayItemLinkInput(
        wrapper,
        { type: newType, url: '', id: null, title: '' },
        arrayKey,
        index,
        propKey
      );
    });

    return wrapper;
  }

  /**
   * Update array item link input based on selected type
   */
  updateArrayItemLinkInput(wrapper, state, arrayKey, index, propKey) {
    const container = wrapper.querySelector('.link-selector-input-container');
    container.innerHTML = '';

    if (state.type === 'custom') {
      // Simple URL input
      const input = document.createElement('input');
      input.type = 'url';
      input.className = 'property-input';
      input.value = state.url || '';
      input.placeholder = 'Enter URL...';

      input.addEventListener('input', () => {
        this.updateArrayItemValue(arrayKey, index, propKey, input.value, false);
      });

      input.addEventListener('change', () => {
        this.updateArrayItemValue(arrayKey, index, propKey, input.value, true);
      });

      container.appendChild(input);
    } else {
      // Entity search
      const searchInput = document.createElement('input');
      searchInput.type = 'text';
      searchInput.className = 'property-input link-search-mini';
      searchInput.placeholder = `Search ${state.type}...`;

      // If we have a previous selection, show title or URL
      if (state.title) {
        searchInput.value = state.title;
        searchInput.dataset.selectedUrl = state.url;
      } else if (state.url) {
        // No title but we have a URL - show the URL so merchant knows something is selected
        searchInput.value = state.url;
        searchInput.dataset.selectedUrl = state.url;
      }

      const resultsContainer = document.createElement('div');
      resultsContainer.className = 'link-selector-results link-selector-results-mini';
      resultsContainer.style.display = 'none';

      let searchTimeout;
      searchInput.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        const query = searchInput.value.trim();

        // Clear previous selection if user is typing
        delete searchInput.dataset.selectedUrl;

        if (query.length < 2) {
          resultsContainer.innerHTML = '';
          resultsContainer.style.display = 'none';
          return;
        }

        searchTimeout = setTimeout(() => {
          this.searchLinkSources(state.type, query, resultsContainer, selected => {
            // Update array item value with selected URL
            this.updateArrayItemValue(arrayKey, index, propKey, selected.url, true);

            // Update display
            searchInput.value = selected.title || selected.name;
            searchInput.dataset.selectedUrl = selected.url;
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
          });
        }, 300);
      });

      searchInput.addEventListener('blur', () => {
        setTimeout(() => {
          resultsContainer.style.display = 'none';
        }, 200);
      });

      searchInput.addEventListener('focus', () => {
        if (searchInput.value.trim().length >= 2 && resultsContainer.children.length > 0) {
          resultsContainer.style.display = 'block';
        }
      });

      container.appendChild(searchInput);
      container.appendChild(resultsContainer);
    }
  }

  /**
   * Render image input for array item (uses media library)
   */
  renderArrayItemImageInput(arrayKey, index, propKey, config, value) {
    const wrapper = document.createElement('div');
    wrapper.className = 'media-library-input-wrapper array-item__image-input';

    // Hidden input for value
    const hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.value = value || '';
    hiddenInput.dataset.arrayKey = arrayKey;
    hiddenInput.dataset.index = index;
    hiddenInput.dataset.propKey = propKey;
    wrapper.appendChild(hiddenInput);

    // Preview container (matches media library style)
    const previewContainer = document.createElement('div');
    previewContainer.className = 'media-library-preview';
    if (value) {
      previewContainer.innerHTML = `
                <img src="${value}" alt="Preview" class="media-library-preview-img">
            `;
    } else {
      previewContainer.innerHTML = `
                <div class="media-library-no-image">
                    <i class="fas fa-image"></i>
                    <span>No image selected</span>
                </div>
            `;
    }
    wrapper.appendChild(previewContainer);

    // Button container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'media-library-buttons';

    // Select button
    const selectBtn = document.createElement('button');
    selectBtn.type = 'button';
    selectBtn.className = 'btn btn-sm btn-primary media-library-select-btn';
    selectBtn.innerHTML = '<i class="fas fa-images"></i> Select Image';
    selectBtn.addEventListener('click', async () => {
      // Use media library if available (same as image element)
      if (window.selectImageFromLibrary) {
        window.selectImageFromLibrary(selectedMedia => {
          if (selectedMedia) {
            const url = selectedMedia.url;
            hiddenInput.value = url;

            // Store metadata
            hiddenInput.dataset.mediaId = selectedMedia.id || '';
            hiddenInput.dataset.mediaTitle = selectedMedia.title || '';

            // Update preview
            previewContainer.innerHTML = `
                            <img src="${url}" alt="${selectedMedia.title || 'Preview'}" class="media-library-preview-img">
                        `;

            // Update the value
            this.updateArrayItemValue(arrayKey, index, propKey, url);

            // Also update the thumbnail in the array item header
            const itemContainer = wrapper.closest('.array-item');
            if (itemContainer) {
              const thumb = itemContainer.querySelector('.array-item__thumb');
              const number = itemContainer.querySelector('.array-item__number');
              if (thumb) {
                thumb.src = url;
              } else if (number) {
                number.outerHTML = `<img src="${url}" alt="" class="array-item__thumb">`;
              }
            }

            // Show clear button if hidden
            if (clearBtn.style.display === 'none') {
              clearBtn.style.display = '';
            }
          }
        });
      } else {
        // Fallback to URL prompt
        console.warn('Media library not available. Falling back to URL input.');
        const url = await AdminModal.prompt({
          message: 'Enter image URL:',
          defaultValue: hiddenInput.value,
        });
        if (url) {
          hiddenInput.value = url;
          previewContainer.innerHTML = `
                        <img src="${url}" alt="Preview" class="media-library-preview-img">
                    `;
          this.updateArrayItemValue(arrayKey, index, propKey, url);

          // Update header thumbnail
          const itemContainer = wrapper.closest('.array-item');
          if (itemContainer) {
            const thumb = itemContainer.querySelector('.array-item__thumb');
            const number = itemContainer.querySelector('.array-item__number');
            if (thumb) {
              thumb.src = url;
            } else if (number) {
              number.outerHTML = `<img src="${url}" alt="" class="array-item__thumb">`;
            }
          }

          if (clearBtn.style.display === 'none') {
            clearBtn.style.display = '';
          }
        }
      }
    });
    buttonContainer.appendChild(selectBtn);

    // Clear button
    const clearBtn = document.createElement('button');
    clearBtn.type = 'button';
    clearBtn.className = 'btn btn-sm btn-outline-danger media-library-clear-btn';
    clearBtn.innerHTML = '<i class="fas fa-times"></i>';
    clearBtn.title = 'Clear image';
    if (!value) {
      clearBtn.style.display = 'none';
    }
    clearBtn.addEventListener('click', () => {
      hiddenInput.value = '';
      delete hiddenInput.dataset.mediaId;
      delete hiddenInput.dataset.mediaTitle;

      previewContainer.innerHTML = `
                <div class="media-library-no-image">
                    <i class="fas fa-image"></i>
                    <span>No image selected</span>
                </div>
            `;

      this.updateArrayItemValue(arrayKey, index, propKey, '');

      // Update header - remove thumbnail, show number
      const itemContainer = wrapper.closest('.array-item');
      if (itemContainer) {
        const thumb = itemContainer.querySelector('.array-item__thumb');
        if (thumb) {
          const idx = itemContainer.dataset.index;
          thumb.outerHTML = `<span class="array-item__number">${parseInt(idx) + 1}</span>`;
        }
      }

      clearBtn.style.display = 'none';
    });
    buttonContainer.appendChild(clearBtn);

    wrapper.appendChild(buttonContainer);

    return wrapper;
  }

  /**
   * Update a single value within an array item
   * @param {string} arrayKey - The array property key (e.g., 'frames')
   * @param {number} index - Index of the item in the array
   * @param {string} propKey - Property key within the item (e.g., 'title')
   * @param {*} newValue - New value to set
   * @param {boolean} triggerSync - Whether to trigger server sync (default: true)
   */
  updateArrayItemValue(arrayKey, index, propKey, newValue, triggerSync = true) {
    let items = this.currentValues[arrayKey] || [];

    // Parse JSON string if needed (can happen after DOM refresh)
    if (typeof items === 'string') {
      try {
        items = JSON.parse(items);
        this.currentValues[arrayKey] = items;
      } catch (e) {
        console.error('Failed to parse array items:', e);
        return;
      }
    }

    if (Array.isArray(items) && items[index]) {
      items[index][propKey] = newValue;
      this.currentValues[arrayKey] = items;

      // Always update hidden input value for form state consistency
      this.updateArrayHiddenInput(arrayKey, items);

      // Only trigger server sync if requested (e.g., on blur, not on every keystroke)
      if (triggerSync) {
        this.triggerArrayChange(arrayKey, items);
      }
    }
  }

  /**
   * Update hidden input value without triggering change event
   * Used for keeping form state in sync during typing
   */
  updateArrayHiddenInput(arrayKey, items) {
    const hiddenInput = document.querySelector(`input[name="${arrayKey}"]`);
    if (hiddenInput) {
      hiddenInput.value = JSON.stringify(items);
    }
  }

  /**
   * Move array item to new position
   */
  moveArrayItem(arrayKey, fromIndex, toIndex) {
    let items = this.currentValues[arrayKey] || [];

    // Parse JSON string if needed
    if (typeof items === 'string') {
      try {
        items = JSON.parse(items);
        this.currentValues[arrayKey] = items;
      } catch (e) {
        console.error('Failed to parse array items:', e);
        return;
      }
    }

    if (!Array.isArray(items) || toIndex < 0 || toIndex >= items.length) return;

    // Swap items
    const item = items.splice(fromIndex, 1)[0];
    items.splice(toIndex, 0, item);
    this.currentValues[arrayKey] = items;

    // Re-render the array input
    this.refreshArrayInput(arrayKey);
    this.triggerArrayChange(arrayKey, items);
  }

  /**
   * Delete array item
   */
  deleteArrayItem(arrayKey, index) {
    let items = this.currentValues[arrayKey] || [];

    // Parse JSON string if needed
    if (typeof items === 'string') {
      try {
        items = JSON.parse(items);
        this.currentValues[arrayKey] = items;
      } catch (e) {
        console.error('Failed to parse array items:', e);
        return;
      }
    }

    if (!Array.isArray(items)) return;

    items.splice(index, 1);
    this.currentValues[arrayKey] = items;

    // Re-render the array input
    this.refreshArrayInput(arrayKey);
    this.triggerArrayChange(arrayKey, items);
  }

  /**
   * Refresh array input after structural changes
   */
  refreshArrayInput(arrayKey) {
    const container = document.querySelector(
      `.array-input-container[data-array-key="${arrayKey}"]`
    );
    if (!container) return;

    const form = container.closest('.element-properties-form');
    if (!form) return;

    const elementType = form.dataset.elementType;
    const config = this.currentElementConfig;

    // Find the array config
    let arrayConfig = null;
    if (config.tabs) {
      const flatProps = this.flattenTabProperties(config.tabs);
      arrayConfig = flatProps[arrayKey];
    } else if (config.properties) {
      arrayConfig = config.properties[arrayKey];
    }

    if (!arrayConfig) return;

    // Re-render items list
    const itemsList = container.querySelector('.array-items-list');
    if (itemsList) {
      itemsList.innerHTML = '';
      let items = this.currentValues[arrayKey] || [];

      // Parse JSON string if needed
      if (typeof items === 'string') {
        try {
          items = JSON.parse(items);
          this.currentValues[arrayKey] = items;
        } catch (e) {
          console.error('Failed to parse array items:', e);
          items = [];
        }
      }

      const itemSchema = arrayConfig.item_schema || {};
      const itemProperties = itemSchema.properties || arrayConfig.item_properties || {};

      if (Array.isArray(items)) {
        items.forEach((item, index) => {
          const itemElement = this.renderArrayItem(
            arrayKey,
            index,
            item,
            itemProperties,
            arrayConfig
          );
          itemsList.appendChild(itemElement);
        });
      }
    }

    // Update hidden input
    const hiddenInput = container.querySelector(`input[name="${arrayKey}"]`);
    if (hiddenInput) {
      const items = this.currentValues[arrayKey] || [];
      hiddenInput.value = JSON.stringify(Array.isArray(items) ? items : []);
    }
  }

  /**
   * Trigger change event for array updates
   */
  triggerArrayChange(arrayKey, items) {
    // Update hidden input
    const hiddenInput = document.querySelector(`input[name="${arrayKey}"]`);
    if (hiddenInput) {
      hiddenInput.value = JSON.stringify(items);

      // Dispatch change event
      const event = new Event('change', { bubbles: true });
      hiddenInput.dispatchEvent(event);
    }
  }

  /**
   * Escape HTML for safe display
   */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
  }

  /**
   * Cleanup utilities
   */
  cleanup() {
    for (const [key, utility] of this.activeUtilities) {
      if (utility && typeof utility.close === 'function') {
        utility.close();
      }
    }
    this.activeUtilities.clear();
  }

  /**
   * Format section name for display
   */
  formatSectionName(name) {
    return name.charAt(0).toUpperCase() + name.slice(1).replace(/_/g, ' ');
  }

  /**
   * Format property name for display
   */
  formatPropertyName(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  }
}

// Create global instance
window.propertyRenderer = new PropertyRenderer();
