/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Branding Builder JavaScript
 * Handles the interactive branding customization interface
 */

class BrandingBuilder {
  constructor() {
    // Read config from data island (CSP-safe)
    const _configEl = document.getElementById('branding-builder-config');
    const _cfg = _configEl ? JSON.parse(_configEl.textContent) : {};
    this.themeData = _cfg.themeData || window.themeData || {}; // Base theme tokens
    this.brandingData = _cfg.brandingData || window.brandingData || {}; // User customizations only
    this.mergedData = this.mergeTokens(); // Combined theme + branding
    this.brandingId = _cfg.brandingId !== undefined ? _cfg.brandingId : window.brandingId;
    this.csrfToken = _cfg.csrfToken || window.csrfToken;
    this.urls = _cfg.urls || window.brandingUrls || {};
    this.translations = _cfg.i18n || window.translations || {};
    this.currentDevice = 'desktop';
    this.autoSaveTimer = null;
    this.colorPickers = {};
    this.typographyEditors = {};
    this.borderEditors = {}; // Store border editor instances
    this.spacingEditors = {}; // Store spacing editor instances for Layout tab
    this.shadowEditors = {}; // Store shadow editor instances for Layout tab

    this.init();
  }

  mergeTokens() {
    // Merge theme base tokens with branding customizations
    // Branding values override theme values
    // Use defensive defaults for all token categories
    return {
      colors: { ...(this.themeData.colors || {}), ...(this.brandingData.colors || {}) },
      typography: { ...(this.themeData.typography || {}), ...(this.brandingData.typography || {}) },
      spacing: { ...(this.themeData.spacing || {}), ...(this.brandingData.spacing || {}) },
      borders: { ...(this.themeData.borders || {}), ...(this.brandingData.borders || {}) },
      shadows: { ...(this.themeData.shadows || {}), ...(this.brandingData.shadows || {}) },
      animations: { ...(this.themeData.animations || {}), ...(this.brandingData.animations || {}) },
      transitions: {
        ...(this.themeData.transitions || {}),
        ...(this.brandingData.transitions || {}),
      },
      header: { ...(this.themeData.header || {}), ...(this.brandingData.header || {}) },
      footer: { ...(this.themeData.footer || {}), ...(this.brandingData.footer || {}) },
      menu: { ...(this.themeData.menu || {}), ...(this.brandingData.menu || {}) },
      search: { ...(this.themeData.search || {}), ...(this.brandingData.search || {}) },
      elements: this.deepMerge(this.themeData.elements || {}, this.brandingData.elements || {}),
      // Card type tokens (top-level with hyphenated names)
      'card-default': {
        ...(this.themeData['card-default'] || {}),
        ...(this.brandingData['card-default'] || {}),
      },
      'card-elevated': {
        ...(this.themeData['card-elevated'] || {}),
        ...(this.brandingData['card-elevated'] || {}),
      },
      'card-bordered': {
        ...(this.themeData['card-bordered'] || {}),
        ...(this.brandingData['card-bordered'] || {}),
      },
      'card-minimal': {
        ...(this.themeData['card-minimal'] || {}),
        ...(this.brandingData['card-minimal'] || {}),
      },
      component_overrides: this.brandingData.component_overrides || {},
      custom_css: this.brandingData.custom_css || '',
    };
  }

  // Deep merge helper for nested objects (like elements)
  deepMerge(target, source) {
    const result = { ...target };
    for (const key in source) {
      if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
        result[key] = this.deepMerge(result[key] || {}, source[key]);
      } else {
        result[key] = source[key];
      }
    }
    return result;
  }

  // Recursively generate CSS variables for nested elements structure
  // e.g., elements.button.radius → --theme-element-button-radius
  generateElementsCSS(obj, prefix, callback) {
    for (const key in obj) {
      const value = obj[key];
      const cssKey = key.replace(/_/g, '-');
      const newPrefix = prefix ? `${prefix}-${cssKey}` : cssKey;

      if (value && typeof value === 'object' && !Array.isArray(value)) {
        // Recurse into nested objects
        this.generateElementsCSS(value, newPrefix, callback);
      } else if (value) {
        // Output the CSS variable
        const varName = `--theme-element-${newPrefix}`;
        callback(varName, value);
      }
    }
  }

  // Get nested value using dot notation (e.g., "header.background")
  getNestedValue(obj, path) {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }

  // Set nested value using dot notation (e.g., "header.background")
  setNestedValue(obj, path, value) {
    const keys = path.split('.');
    const lastKey = keys.pop();
    let current = obj;

    for (const key of keys) {
      if (!current[key] || typeof current[key] !== 'object') {
        current[key] = {};
      }
      current = current[key];
    }

    current[lastKey] = value;
  }

  // Setup event handlers for all data-token inputs
  setupTokenInputs() {
    const tokenInputs = document.querySelectorAll('[data-token]');

    tokenInputs.forEach(input => {
      const tokenPath = input.dataset.token;
      const [category] = tokenPath.split('.');

      // Skip color inputs in non-element sections (handled by setupColorInputs)
      // But element color inputs need handlers here for live preview
      if (input.classList.contains('color-input') && category !== 'elements') {
        return;
      }

      // Handle input changes
      input.addEventListener('input', () => {
        this.updateTokenValue(tokenPath, input.value);
        // Update color input styling if applicable
        if (input.classList.contains('color-input')) {
          this.applyColorToInput(input, input.value, true);
        }
      });

      // Handle blur for final value
      input.addEventListener('blur', () => {
        this.updateTokenValue(tokenPath, input.value);
      });
    });
  }

  // Load values into all data-token inputs
  loadTokenInputs() {
    const tokenInputs = document.querySelectorAll('[data-token]');

    // Layout sections that may have CSS variable values needing resolution
    const layoutSections = ['header', 'footer', 'menu', 'search'];

    // Categories that should have values resolved (for display purposes)
    const resolveValueCategories = ['elements'];

    tokenInputs.forEach(input => {
      const tokenPath = input.dataset.token;

      // Determine which data source to use based on token path prefix
      const [category, ...propertyParts] = tokenPath.split('.');
      const property = propertyParts.join('.');

      let customValue, themeDefault, effectiveValue;

      // Get values from appropriate source
      if (category === 'elements') {
        customValue = this.getNestedValue(this.brandingData.elements || {}, property);
        themeDefault = this.getNestedValue(this.themeData.elements || {}, property);
      } else {
        // Check both branding and theme data for all other categories
        customValue = this.brandingData[category]?.[property];
        themeDefault = this.themeData[category]?.[property];
      }

      effectiveValue = customValue !== undefined ? customValue : themeDefault;

      if (effectiveValue !== undefined) {
        // Check if this value needs CSS variable resolution
        const needsResolution =
          resolveValueCategories.includes(category) || layoutSections.includes(category);

        if (needsResolution && !input.hasAttribute('readonly')) {
          // Resolve CSS variables for display (elements and layout sections)
          const resolvedValue = this.resolveCssVariable(effectiveValue);
          input.value = resolvedValue;
          // Store original value as data attribute for reference
          input.dataset.originalValue = effectiveValue;
          // Apply color styling for color inputs
          if (input.classList.contains('color-input') && resolvedValue) {
            this.applyColorToInput(input, resolvedValue, customValue !== undefined);
          }
        } else {
          input.value = effectiveValue;
          // Apply color styling for other color inputs
          if (input.classList.contains('color-input') && effectiveValue) {
            this.applyColorToInput(input, effectiveValue, customValue !== undefined);
          }
        }
      }
    });
  }

  // Update a token value via its dot-notation path
  updateTokenValue(tokenPath, value) {
    const [category, ...propertyParts] = tokenPath.split('.');
    const property = propertyParts.join('.');

    // Initialize category in branding data if needed
    if (!this.brandingData[category]) {
      this.brandingData[category] = {};
    }

    // Handle nested elements tokens
    if (category === 'elements') {
      this.setNestedValue(this.brandingData.elements, property, value);
      // Update merged data
      if (!this.mergedData.elements) {
        this.mergedData.elements = {};
      }
      this.setNestedValue(this.mergedData.elements, property, value);
    } else {
      this.brandingData[category][property] = value;
      // Update merged data
      if (!this.mergedData[category]) {
        this.mergedData[category] = {};
      }
      this.mergedData[category][property] = value;
    }

    // Update preview
    this.updatePreviewFrame();

    // Send update to server
    this.sendUpdate(category, this.brandingData[category]);
  }

  init() {
    this.setupSectionTabs();
    this.setupColorSubTabs(); // Add color sub-tab navigation
    this.setupPropertyGroups(); // Setup collapsible property groups
    this.setupDeviceControls();
    this.setupColorInputs();
    this.setupBackgroundEditorFields(); // Initialize background editors for layout backgrounds
    this.setupTypographyInputs();
    this.setupSpacingInputs();
    this.setupBorderInputs(); // Keep for advanced global radius scale
    this.initializeBorderEditors(); // Initialize border editors for components
    this.setupShadowInputs();
    this.setupCustomCSS();
    this.setupTokenInputs(); // Setup data-token inputs for Layout/Components/Advanced tabs
    this.loadBrandingData();
    this.loadTokenInputs(); // Load values into data-token inputs
    this.loadThemeCSS(); // Load active theme CSS for preview
    this.initializeTypographyEditors(); // Initialize typography editors (includes menu)
    this.initializeButtonEditors(); // Initialize button-specific border and typography editors
    this.initializeCardEditors(); // Initialize card type editors (background, border, shadow)
    this.initializeSpacingEditors(); // Initialize spacing editors for Layout tab
    this.initializeShadowEditors(); // Initialize shadow editors for Layout tab
    this.setupTypographyInfoTooltips(); // Setup typography info icon tooltips
    this.loadPreviewContent();
    this.initializeStatusIndicators();
    this.setupEventDelegation();
  }

  // ==========================================================================
  // Event Delegation — replaces inline onclick handlers for CSP compliance
  // ==========================================================================

  setupEventDelegation() {
    document.addEventListener('click', e => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;

      switch (btn.dataset.action) {
        // Color pickers
        case 'open-color-picker':
          this.openColorPicker(btn.dataset.key);
          break;

        // Reset to theme default
        case 'reset-to-default':
          this.resetToThemeDefault(btn.dataset.section, btn.dataset.property);
          break;

        // Save / Export / Import
        case 'save-branding':
          this.saveBranding();
          break;
        case 'export-branding':
          this.exportBranding();
          break;
        case 'import-branding':
          this.importBranding();
          break;

        // Shadow & spacing editors
        case 'open-shadow-editor':
          this.openShadowEditor(btn.dataset.key);
          break;
        case 'open-spacing-editor':
          if (typeof this.openSpacingEditor === 'function') {
            this.openSpacingEditor();
          }
          break;

        // Preview
        case 'refresh-preview':
          this.refreshPreview();
          break;

        // Button resets
        case 'reset-button-border-defaults':
          this.resetButtonBorderDefaults();
          break;
        case 'reset-button-typography-defaults':
          this.resetButtonTypographyDefaults();
          break;

        // Card type resets
        case 'reset-card-default':
          this.resetCardTypeDefault(btn.dataset.cardType, btn.dataset.property);
          break;
        case 'reset-card-border':
          this.resetCardTypeBorder(btn.dataset.cardType);
          break;
        case 'reset-card-shadow':
          this.resetCardTypeShadow(btn.dataset.cardType, btn.dataset.property);
          break;
      }
    });
  }

  // ==========================================================================
  // Property Status Indicators
  // Visual dots showing property state: theme default, customized, or no value
  // ==========================================================================

  /**
   * Get status for a property: 'custom', 'default', or 'none'
   * @param {string} section - Token section (colors, typography, etc.)
   * @param {string} property - Property key within section
   * @returns {string} Status: 'custom', 'default', or 'none'
   */
  getPropertyStatus(section, property) {
    const custom = this.brandingData[section]?.[property];
    const themeDefault = this.themeData[section]?.[property];

    if (custom !== undefined && custom !== null && custom !== '') {
      return 'custom';
    } else if (themeDefault !== undefined && themeDefault !== null && themeDefault !== '') {
      return 'default';
    }
    return 'none';
  }

  /**
   * Update status indicator on a property field
   * @param {HTMLElement} field - The .bb-property-field element
   * @param {string} status - 'custom', 'default', or 'none'
   */
  updatePropertyStatus(field, status) {
    if (!field) return;

    field.classList.remove('status-custom', 'status-default', 'status-none');
    field.classList.add(`status-${status}`);

    const label = field.querySelector('label, .bb-property-label');
    if (label) {
      const tips = {
        custom: this.translations.statusCustom || 'Custom value',
        default: this.translations.statusDefault || 'Theme default',
        none: this.translations.statusNone || 'No value',
      };
      label.setAttribute('data-status-tip', tips[status]);
    }
  }

  /**
   * Find property field element for a given section/property
   * @param {string} section - Token section
   * @param {string} property - Property key
   * @returns {HTMLElement|null}
   */
  findPropertyField(section, property) {
    // Try data-color-key for color fields
    if (section === 'colors') {
      const colorField = document.querySelector(`.bb-property-field[data-color-key="${property}"]`);
      if (colorField) return colorField;
    }
    // Try data-status attributes
    return document.querySelector(
      `[data-status-section="${section}"][data-status-property="${property}"]`
    );
  }

  /**
   * Refresh status indicator for a specific property
   * @param {string} section - Token section
   * @param {string} property - Property key
   */
  refreshPropertyStatus(section, property) {
    const field = this.findPropertyField(section, property);
    if (field) {
      const status = this.getPropertyStatus(section, property);
      this.updatePropertyStatus(field, status);
    }
  }

  /**
   * Initialize status indicators for all property fields
   */
  initializeStatusIndicators() {
    document.querySelectorAll('.bb-property-field').forEach(field => {
      let section = field.dataset.statusSection;
      let property = field.dataset.statusProperty;

      if (!section || !property) {
        // Try data-color-key (color fields)
        const colorKey = field.dataset.colorKey;
        if (colorKey) {
          section = 'colors';
          property = colorKey;
        } else {
          // Try data-token (token-based fields)
          const tokenPath =
            field.dataset.token || field.querySelector('[data-token]')?.dataset.token;
          if (tokenPath) {
            const parts = tokenPath.split('.');
            section = parts[0];
            property = parts.slice(1).join('.');
          }
        }
      }

      if (section && property) {
        field.dataset.statusSection = section;
        field.dataset.statusProperty = property;
        const status = this.getPropertyStatus(section, property);
        this.updatePropertyStatus(field, status);
      }
    });
  }

  // Section Tab Navigation
  setupSectionTabs() {
    const tabs = document.querySelectorAll('.admin-tab-btn[data-section]');
    const panels = document.querySelectorAll('.section-panel');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const section = tab.dataset.section;

        // Update active states
        tabs.forEach(t => t.classList.remove('active'));
        panels.forEach(p => p.classList.remove('active'));

        tab.classList.add('active');
        const panel = document.getElementById(`${section}-section`);
        if (panel) {
          panel.classList.add('active');
        }
      });
    });
  }

  // Color Sub-tab Navigation (Basic/Advanced)
  setupColorSubTabs() {
    const colorSubTabs = document.querySelectorAll('.color-sub-tabs .admin-tab-btn');
    const colorTabContents = document.querySelectorAll('.color-tab-content');

    colorSubTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const colorTab = tab.dataset.colorTab;

        // Update active states for sub-tabs
        colorSubTabs.forEach(t => t.classList.remove('active'));
        colorTabContents.forEach(c => c.classList.remove('active'));

        tab.classList.add('active');
        const tabContent = document.getElementById(`${colorTab}-colors-tab`);
        if (tabContent) {
          tabContent.classList.add('active');
        }
      });
    });
  }

  // Property Group Toggle/Collapse Functionality
  setupPropertyGroups() {
    const groups = document.querySelectorAll('.bb-property-group');

    groups.forEach(group => {
      const header = group.querySelector('.bb-property-group-header');
      if (header) {
        header.addEventListener('click', () => {
          group.classList.toggle('collapsed');
        });
      }
    });
  }

  // Helper: Create a property group HTML structure
  createPropertyGroup(options) {
    const {
      id,
      title,
      helpText = '',
      expanded = false,
      singleColumn = false,
      content = '',
    } = options;

    const collapsedClass = expanded ? '' : 'collapsed';
    const columnClass = singleColumn ? 'single-column' : '';

    return `
            <div class="bb-property-group ${collapsedClass}" id="${id}">
                <div class="bb-property-group-header">
                    <i class="fas fa-chevron-down toggle-icon"></i>
                    <h4 class="bb-property-group-title">${title}</h4>
                    ${helpText ? `<span class="bb-property-group-help">${helpText}</span>` : ''}
                </div>
                <div class="bb-property-group-content ${columnClass}">
                    ${content}
                </div>
            </div>
        `;
  }

  // Helper: Create a property field HTML structure
  createPropertyField(options) {
    const {
      id,
      label,
      type = 'text',
      value = '',
      placeholder = '',
      section = '',
      property = '',
      fullWidth = false,
      showReset = true,
      options: selectOptions = [],
    } = options;

    const fullWidthClass = fullWidth ? 'full-width' : '';
    const resetButton = showReset
      ? `
            <button type="button" class="bb-property-reset"
                    onclick="brandingBuilder.resetToThemeDefault('${section}', '${property}')"
                    title="Reset to theme default">
                <i class="fas fa-undo"></i>
            </button>
        `
      : '';

    let inputHtml = '';
    if (type === 'select') {
      inputHtml = `
                <select id="${id}" data-section="${section}" data-property="${property}">
                    ${selectOptions.map(opt => `<option value="${opt.value}"${opt.value === value ? ' selected' : ''}>${opt.label}</option>`).join('')}
                </select>
            `;
    } else if (type === 'color') {
      inputHtml = `
                <input type="text" id="${id}" value="${value}" placeholder="${placeholder}"
                       data-section="${section}" data-property="${property}">
                <button type="button" class="bb-color-preview" onclick="brandingBuilder.openColorPicker('${id}')">
                    <div class="bb-color-preview-inner" style="background: ${value || 'transparent'};"></div>
                </button>
            `;
    } else {
      inputHtml = `
                <input type="${type}" id="${id}" value="${value}" placeholder="${placeholder}"
                       data-section="${section}" data-property="${property}">
            `;
    }

    return `
            <div class="bb-property-field ${fullWidthClass}">
                <label class="bb-property-label" for="${id}">${label}</label>
                <div class="bb-property-input-wrapper">
                    ${inputHtml}
                    ${resetButton}
                </div>
            </div>
        `;
  }

  // Helper: Create a property subgroup (nested grouping)
  createPropertySubgroup(options) {
    const { title, singleColumn = false, content = '' } = options;

    const columnClass = singleColumn ? 'single-column' : '';

    return `
            <div class="bb-property-subgroup">
                <div class="bb-property-subgroup-title">${title}</div>
                <div class="bb-property-subgroup-content ${columnClass}">
                    ${content}
                </div>
            </div>
        `;
  }

  // Device Preview Controls
  setupDeviceControls() {
    const deviceBtns = document.querySelectorAll('.device-preview-controls .util-btn');
    const previewFrame = document.getElementById('preview-frame');

    deviceBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const device = btn.dataset.device;

        // Update active states
        deviceBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update preview frame class
        previewFrame.className = `preview-frame ${device}-frame`;
        this.currentDevice = device;
      });
    });
  }

  // Helper function to calculate luminance for contrast
  getLuminance(color) {
    // Convert color to RGB
    let r, g, b;

    if (color.startsWith('#')) {
      // Handle hex colors
      const hex = color.replace('#', '');
      if (hex.length === 3) {
        r = parseInt(hex[0] + hex[0], 16);
        g = parseInt(hex[1] + hex[1], 16);
        b = parseInt(hex[2] + hex[2], 16);
      } else {
        r = parseInt(hex.substr(0, 2), 16);
        g = parseInt(hex.substr(2, 2), 16);
        b = parseInt(hex.substr(4, 2), 16);
      }
    } else if (color.startsWith('rgb')) {
      // Handle rgb/rgba colors
      const matches = color.match(/\d+/g);
      if (matches) {
        r = parseInt(matches[0]);
        g = parseInt(matches[1]);
        b = parseInt(matches[2]);
      }
    } else {
      // For named colors, we'll default to dark text
      return 0.5;
    }

    // Calculate relative luminance
    const sRGB = [r, g, b].map(val => {
      val = val / 255;
      return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    });

    return 0.2126 * sRGB[0] + 0.7152 * sRGB[1] + 0.0722 * sRGB[2];
  }

  // Apply color to input with proper contrast
  applyColorToInput(input, color, isCustom = false) {
    if (color && this.isValidColor(color)) {
      // Use setProperty with important to override theme styles
      input.style.setProperty('background-color', color, 'important');

      // Calculate contrast and set text color
      const luminance = this.getLuminance(color);
      input.style.setProperty('color', luminance > 0.5 ? '#000000' : '#ffffff', 'important');

      // Add visual indicator for custom vs theme default
      if (isCustom) {
        input.classList.add('using-custom');
        input.classList.remove('using-theme-default');
      } else {
        input.classList.add('using-theme-default');
        input.classList.remove('using-custom');
      }
    }
  }

  // Check if a color value is valid
  isValidColor(color) {
    return (
      color &&
      (color.match(/^#[0-9A-Fa-f]{3,6}$/) || color.match(/^rgb/) || color.match(/^[a-z]+$/i))
    );
  }

  // Resolve CSS variable references to actual values
  // Handles cases like "var(--theme-color-text)" → "#1f2937"
  // Also handles typography, spacing, borders, transitions variables
  resolveCssVariable(value, maxDepth = 5) {
    if (!value || typeof value !== 'string') {
      return value;
    }

    // If it's not a CSS variable, return as-is
    const trimmedValue = value.trim();
    if (!trimmedValue.startsWith('var(')) {
      return value;
    }

    // Prevent infinite recursion
    if (maxDepth <= 0) {
      console.warn('CSS variable resolution max depth reached:', value);
      return value;
    }

    // Check if it's a CSS variable - extract name and optional fallback
    const varMatch = trimmedValue.match(/^var\(\s*(--[a-zA-Z0-9-]+)\s*(?:,\s*(.+))?\s*\)$/);
    if (!varMatch) {
      return value; // Malformed var(), return as-is
    }

    const varName = varMatch[1]; // e.g., '--theme-color-text'
    const fallback = varMatch[2];

    // Try to resolve from theme data based on variable pattern
    const resolved = this.resolveThemeVariable(varName, maxDepth);
    if (resolved !== null) {
      return resolved;
    }

    // Fallback: Try getComputedStyle on #preview-frame (may work after CSS loads)
    const previewFrame = document.querySelector('#preview-frame');
    if (previewFrame) {
      const computedValue = getComputedStyle(previewFrame).getPropertyValue(varName).trim();
      if (computedValue) {
        return computedValue.startsWith('var(')
          ? this.resolveCssVariable(computedValue, maxDepth - 1)
          : computedValue;
      }
    }

    // Use fallback value if provided
    if (fallback) {
      return this.resolveCssVariable(fallback.trim(), maxDepth - 1);
    }

    // Return original value if can't resolve
    return value;
  }

  // Resolve a theme variable name to its actual value from mergedData
  resolveThemeVariable(varName, maxDepth = 5) {
    // Helper to recursively resolve if result is also a variable
    const maybeResolve = val => {
      if (val && typeof val === 'string' && val.startsWith('var(')) {
        return this.resolveCssVariable(val, maxDepth - 1);
      }
      return val;
    };

    // Pattern: --theme-color-{key} or --color-{key} → mergedData.colors.{key}
    const colorMatch = varName.match(/^--(theme-)?color-(.+)$/);
    if (colorMatch && this.mergedData?.colors) {
      // Try hyphen format first, then underscore
      const key = colorMatch[2];
      const colorValue =
        this.mergedData.colors[key] || this.mergedData.colors[key.replace(/-/g, '_')];
      if (colorValue) return maybeResolve(colorValue);
    }

    // Pattern: --theme-font-family-{key} or --font-family-{key} → mergedData.typography.font-family-{key}
    const fontFamilyMatch = varName.match(/^--(theme-)?font-family-(.+)$/);
    if (fontFamilyMatch && this.mergedData?.typography) {
      const key = `font-family-${fontFamilyMatch[2]}`;
      const value =
        this.mergedData.typography[key] || this.mergedData.typography[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-font-size-{key} or --font-size-{key} → mergedData.typography.font-size-{key}
    const fontSizeMatch = varName.match(/^--(theme-)?font-size-(.+)$/);
    if (fontSizeMatch && this.mergedData?.typography) {
      const key = `font-size-${fontSizeMatch[2]}`;
      const value =
        this.mergedData.typography[key] || this.mergedData.typography[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-font-weight-{key} or --font-weight-{key} → mergedData.typography.font-weight-{key}
    const fontWeightMatch = varName.match(/^--(theme-)?font-weight-(.+)$/);
    if (fontWeightMatch && this.mergedData?.typography) {
      const key = `font-weight-${fontWeightMatch[2]}`;
      const value =
        this.mergedData.typography[key] || this.mergedData.typography[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-line-height-{key} or --line-height-{key} → mergedData.typography.line-height-{key}
    const lineHeightMatch = varName.match(/^--(theme-)?line-height-(.+)$/);
    if (lineHeightMatch && this.mergedData?.typography) {
      const key = `line-height-${lineHeightMatch[2]}`;
      const value =
        this.mergedData.typography[key] || this.mergedData.typography[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-letter-spacing-{key} or --letter-spacing-{key} → mergedData.typography.letter-spacing-{key}
    const letterSpacingMatch = varName.match(/^--(theme-)?letter-spacing-(.+)$/);
    if (letterSpacingMatch && this.mergedData?.typography) {
      const key = `letter-spacing-${letterSpacingMatch[2]}`;
      const value =
        this.mergedData.typography[key] || this.mergedData.typography[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-space-{key} or --space-{key} → mergedData.spacing.{key}
    const spaceMatch = varName.match(/^--(theme-)?space-(.+)$/);
    if (spaceMatch && this.mergedData?.spacing) {
      const key = spaceMatch[2];
      const value = this.mergedData.spacing[key] || this.mergedData.spacing[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-radius-{key} or --radius-{key} → mergedData.borders.radius-{key}
    const radiusMatch = varName.match(/^--(theme-)?radius-(.+)$/);
    if (radiusMatch && this.mergedData?.borders) {
      const key = `radius-${radiusMatch[2]}`;
      const value = this.mergedData.borders[key] || this.mergedData.borders[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-border-width-{key} or --border-width-{key} → mergedData.borders.width-{key}
    const borderWidthMatch = varName.match(/^--(theme-)?border-width-(.+)$/);
    if (borderWidthMatch && this.mergedData?.borders) {
      const key = `width-${borderWidthMatch[2]}`;
      const value = this.mergedData.borders[key] || this.mergedData.borders[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-transition-duration-{key} or --transition-duration-{key} → mergedData.transitions.duration-{key}
    const transitionDurationMatch = varName.match(/^--(theme-)?transition-duration-(.+)$/);
    if (transitionDurationMatch && this.mergedData?.transitions) {
      const key = `duration-${transitionDurationMatch[2]}`;
      const value =
        this.mergedData.transitions[key] || this.mergedData.transitions[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-transition-easing-{key} or --transition-easing-{key} → mergedData.transitions.easing-{key}
    const transitionEasingMatch = varName.match(/^--(theme-)?transition-easing-(.+)$/);
    if (transitionEasingMatch && this.mergedData?.transitions) {
      const key = `easing-${transitionEasingMatch[2]}`;
      const value =
        this.mergedData.transitions[key] || this.mergedData.transitions[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-shadow-{key} or --shadow-{key} → mergedData.shadows.{key}
    const shadowMatch = varName.match(/^--(theme-)?shadow-(.+)$/);
    if (shadowMatch && this.mergedData?.shadows) {
      const key = shadowMatch[2];
      const value = this.mergedData.shadows[key] || this.mergedData.shadows[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    // Pattern: --theme-border-color-{key} or --border-color-{key} → try colors.border-{key}
    const borderColorMatch = varName.match(/^--(theme-)?border-color-(.+)$/);
    if (borderColorMatch && this.mergedData?.colors) {
      const key = `border-${borderColorMatch[2]}`;
      const value = this.mergedData.colors[key] || this.mergedData.colors[key.replace(/-/g, '_')];
      if (value) return maybeResolve(value);
    }

    return null; // Could not resolve
  }

  // Color Management
  setupColorInputs() {
    // Support both old .color-field and new .bb-property-field with data-color-key
    const colorFields = document.querySelectorAll(
      '.color-field[data-color-key], .bb-property-field[data-color-key]'
    );

    colorFields.forEach(field => {
      const input = field.querySelector('.color-input');
      const key = field.dataset.colorKey;

      if (input) {
        // Determine the section for this color input
        const section = this.getColorSection(key, input);

        // For non-color sections, we need to use the proper token key
        let tokenKey = key;
        if (section !== 'colors') {
          tokenKey = this.getColorProperty(key, input);
        }

        // Get custom value and theme default
        let customValue, themeDefault;

        if (section === 'typography') {
          const inputId = input.id;

          // Typography colors are stored in elements, not typography
          if (inputId === 'typography-color-body') {
            // Body color: stored in elements.body.color
            customValue = this.brandingData.elements?.body?.color;
            themeDefault = this.themeData.elements?.body?.color || this.themeData.colors?.text;
          } else if (inputId.match(/typography-color-h[1-6]/)) {
            // Heading colors: stored in elements.heading.{h1-6}-color
            const headingLevel = inputId.replace('typography-color-', '');
            customValue = this.brandingData.elements?.heading?.[`${headingLevel}-color`];
            themeDefault =
              this.themeData.elements?.heading?.[`${headingLevel}-color`] ||
              this.themeData.colors?.text;
          } else {
            // Non-color typography properties (font_family, etc.)
            customValue = this.brandingData.typography?.[tokenKey];
            themeDefault = this.themeData.typography?.[tokenKey];
          }
        } else {
          // Standard color section lookup
          customValue = this.brandingData[section]?.[tokenKey];
          themeDefault = this.themeData[section]?.[tokenKey];
        }

        const effectiveValue = customValue || themeDefault;

        if (effectiveValue) {
          // Resolve CSS variables to actual colors
          // This converts "var(--theme-color-text)" to "#1f2937"
          const resolvedColor = this.resolveCssVariable(effectiveValue);

          input.value = resolvedColor;
          // Apply color with proper styling (now with actual color value)
          this.applyColorToInput(input, resolvedColor, !!customValue);
        }

        // Handle manual input changes
        input.addEventListener('input', () => {
          const color = input.value;
          // Update the background preview with contrast
          this.applyColorToInput(input, color, true);

          // Use the correct update method based on section
          if (section === 'colors') {
            this.updateColor(key, color);
          } else {
            this.updateColorValue(section, tokenKey, color);
          }
        });

        // Also handle blur event to ensure color is valid
        input.addEventListener('blur', () => {
          const color = input.value;
          if (this.isValidColor(color)) {
            this.applyColorToInput(input, color, true);
          }
        });
      }
    });

    // Also handle layout section color inputs that use data-token instead of data-color-key
    // This covers header, footer, menu, and search color inputs
    this.setupLayoutColorInputs();
  }

  // Setup color inputs for layout sections (header, footer, menu, search) that use data-token
  setupLayoutColorInputs() {
    const layoutSections = ['header', 'footer', 'menu', 'search'];

    // Find all color inputs with data-token that belong to layout sections
    const layoutColorInputs = document.querySelectorAll('.color-input[data-token]');

    layoutColorInputs.forEach(input => {
      const tokenPath = input.dataset.token;
      if (!tokenPath) return;

      const [section, ...propertyParts] = tokenPath.split('.');
      const property = propertyParts.join('.');

      // Only handle layout section color inputs (not elements, etc.)
      if (!layoutSections.includes(section)) return;

      // Get custom value and theme default
      const customValue = this.brandingData[section]?.[property];
      const themeDefault = this.themeData[section]?.[property];
      const effectiveValue = customValue !== undefined ? customValue : themeDefault;

      if (effectiveValue) {
        // Resolve CSS variables to actual colors
        const resolvedColor = this.resolveCssVariable(effectiveValue);
        input.value = resolvedColor;
        this.applyColorToInput(input, resolvedColor, customValue !== undefined);
      }

      // Handle manual input changes
      input.addEventListener('input', () => {
        const color = input.value;
        this.applyColorToInput(input, color, true);
        this.updateColorValue(section, property, color);
      });

      // Handle blur event
      input.addEventListener('blur', () => {
        const color = input.value;
        if (this.isValidColor(color)) {
          this.applyColorToInput(input, color, true);
        }
      });
    });
  }

  // Background Editor for layout backgrounds (background, header-bg, footer-bg)
  setupBackgroundEditorFields() {
    // Initialize storage for background editor instances
    this.backgroundEditors = this.backgroundEditors || {};

    // Find all fields marked for background editor
    const bgEditorFields = document.querySelectorAll('[data-use-background-editor="true"]');

    bgEditorFields.forEach(field => {
      const colorKey = field.dataset.colorKey;
      // Try both selector patterns for the input
      let input = field.querySelector(`#color-${colorKey}`);
      if (!input) {
        input = field.querySelector('.color-input');
      }

      if (!input) return;

      // Get the initial value from branding or theme data
      const customValue = this.brandingData.colors?.[colorKey];
      const themeDefault = this.themeData.colors?.[colorKey];
      const initialValue = customValue || themeDefault || '';

      // Set input value and apply styling
      if (initialValue) {
        input.value = initialValue;
        this.applyColorToInput(input, initialValue, !!customValue);
      }

      // Check if BackgroundEditor is available
      if (typeof BackgroundEditor === 'undefined') {
        console.warn('Background Editor not loaded, falling back to color picker');
        return;
      }

      // Create new background editor instance
      const bgEditor = new BackgroundEditor({
        onChange: css => {
          // Live preview update
          if (!this.mergedData.colors) {
            this.mergedData.colors = {};
          }
          this.mergedData.colors[colorKey] = css;
          this.updatePreviewFrame();
        },
        onApply: css => {
          // Save to branding data
          if (!this.brandingData.colors) {
            this.brandingData.colors = {};
          }
          this.brandingData.colors[colorKey] = css;
          input.value = css;

          // Update merged data
          this.mergedData.colors[colorKey] = css;

          // Update preview
          this.updatePreviewFrame();

          // Auto-save
          this.autoSave();
        },
      });

      // Attach to input field (editor will create its own trigger button)
      bgEditor.attach(input, initialValue);

      // Store reference for cleanup
      this.backgroundEditors[colorKey] = bgEditor;
    });
  }

  openColorPicker(key) {
    // Try to find the input by multiple ID patterns
    let input = document.getElementById(`color-${key}`);
    if (!input) {
      input = document.getElementById(key);
    }

    if (!input) {
      console.error(`Color input not found for key: ${key}`);
      return;
    }

    const currentColor = input.value;

    // Determine the section and property from the input or its attributes
    const section = input.dataset.section || this.getColorSection(key, input);
    const property = input.dataset.property || this.getColorProperty(key, input);

    // Initialize color picker if not already created
    if (!this.colorPickers[key]) {
      this.colorPickers[key] = new ColorPickerUtility({
        onChange: color => {
          input.value = color;
          // Apply color with proper contrast and mark as custom
          this.applyColorToInput(input, color, true);
          this.updateColorValue(section, property, color);
        },
        onClose: () => {
          // Handle close
        },
      });
    }

    // Open color picker with current color
    this.colorPickers[key].open(input, currentColor);
  }

  // Determine the section for a color input
  getColorSection(key, input) {
    // Check for data-token attribute first (most reliable)
    const tokenPath = input.dataset.token;
    if (tokenPath) {
      const [category] = tokenPath.split('.');
      if (category === 'elements') {
        return 'elements';
      }
      return category;
    }

    // Check for typography color inputs
    if (key.startsWith('typography-color-') || input.id.startsWith('typography-color-')) {
      return 'typography';
    }
    // Check for form inputs (elements.form.*)
    if (key.startsWith('form-') || input.id.startsWith('form-')) {
      return 'elements';
    }
    // Check for header/footer inputs
    if (key.startsWith('header-') || input.id.startsWith('header-')) {
      return 'header';
    }
    if (key.startsWith('footer-') || input.id.startsWith('footer-')) {
      return 'footer';
    }
    if (key.startsWith('menu-') || input.id.startsWith('menu-')) {
      return 'menu';
    }
    // Default to colors section
    return 'colors';
  }

  // Determine the property name for a color input
  getColorProperty(key, input) {
    const inputId = input.id;

    // Check for data-token attribute first (most reliable)
    const tokenPath = input.dataset.token;
    if (tokenPath) {
      // For elements.form.input-bg, return "form.input-bg"
      const parts = tokenPath.split('.');
      if (parts[0] === 'elements') {
        return parts.slice(1).join('.');
      }
      // For other tokens, return everything after the first part
      return parts.slice(1).join('.');
    }

    // Typography color: typography-color-h1 -> color_h1
    if (inputId.startsWith('typography-color-')) {
      return 'color_' + inputId.replace('typography-color-', '');
    }
    // Header/Footer: header-background -> background
    if (inputId.startsWith('header-')) {
      return inputId.replace('header-', '');
    }
    if (inputId.startsWith('footer-')) {
      return inputId.replace('footer-', '');
    }
    if (inputId.startsWith('menu-')) {
      return inputId.replace('menu-', '');
    }
    // Colors section: color-primary -> primary
    if (inputId.startsWith('color-')) {
      return inputId.replace('color-', '');
    }
    // Default: use the key as-is
    return key;
  }

  // Update color value for any section
  updateColorValue(section, property, value) {
    if (section === 'colors') {
      // Use existing updateColor method for colors section
      this.updateColor(property, value);
    } else if (section === 'elements') {
      // Handle element color inputs (e.g., form.input-bg, form.label-color)
      // property is like "form.input-bg"

      // Initialize elements if needed
      if (!this.brandingData.elements) {
        this.brandingData.elements = {};
      }

      if (!value || value === '') {
        // Remove custom value - use nested delete
        const parts = property.split('.');
        let current = this.brandingData.elements;
        for (let i = 0; i < parts.length - 1; i++) {
          if (!current[parts[i]]) break;
          current = current[parts[i]];
        }
        if (current && parts.length > 0) {
          delete current[parts[parts.length - 1]];
        }
      } else {
        this.setNestedValue(this.brandingData.elements, property, value);
      }

      // Update merged data
      if (!this.mergedData.elements) {
        this.mergedData.elements = {};
      }
      const themeDefault = this.getNestedValue(this.themeData.elements || {}, property);
      this.setNestedValue(this.mergedData.elements, property, value || themeDefault || '');

      // Refresh preview and send update
      this.updatePreviewFrame();
      this.sendUpdate('elements', this.brandingData.elements || {});
      // Refresh status indicator
      this.refreshPropertyStatus(section, property);
    } else if (section === 'typography' && property.startsWith('color_')) {
      // Typography colors need to update elements for CSS variables to work
      // color_h1 → elements.heading.h1-color
      // color_body → elements.body.color
      const colorTarget = property.replace('color_', '');
      let elementPath;

      if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(colorTarget)) {
        elementPath = `heading.${colorTarget}-color`;
      } else if (colorTarget === 'body') {
        elementPath = 'body.color';
      }

      if (elementPath) {
        // Initialize elements if needed
        if (!this.brandingData.elements) {
          this.brandingData.elements = {};
        }

        if (!value || value === '') {
          // Remove custom value - use nested delete
          const parts = elementPath.split('.');
          if (parts.length === 2) {
            if (this.brandingData.elements[parts[0]]) {
              delete this.brandingData.elements[parts[0]][parts[1]];
            }
          }
        } else {
          this.setNestedValue(this.brandingData.elements, elementPath, value);
        }

        // Update merged data
        if (!this.mergedData.elements) {
          this.mergedData.elements = {};
        }
        const themeDefault = this.getNestedValue(this.themeData.elements || {}, elementPath);
        this.setNestedValue(this.mergedData.elements, elementPath, value || themeDefault || '');

        // Refresh preview and send update
        this.refreshPreview();
        this.sendUpdate('elements', this.brandingData.elements || {});
        // Refresh status indicator
        this.refreshPropertyStatus(section, property);
      }
    } else {
      // For other sections (header, footer, menu, search)
      if (!this.brandingData[section]) {
        this.brandingData[section] = {};
      }

      if (!value || value === '') {
        // Remove custom value to use theme default
        delete this.brandingData[section][property];
      } else {
        this.brandingData[section][property] = value;
      }

      // Update merged data
      if (!this.mergedData[section]) {
        this.mergedData[section] = {};
      }
      this.mergedData[section][property] = value || this.themeData[section]?.[property] || '';

      // Refresh preview and send update
      this.refreshPreview();
      this.sendUpdate(section, this.brandingData[section] || {});
      // Refresh status indicator
      this.refreshPropertyStatus(section, property);
    }
  }

  updateColor(key, value) {
    // Validate the color value
    if (!value || value === '') {
      // If empty, remove from branding data to use theme default
      if (this.brandingData.colors && this.brandingData.colors[key]) {
        delete this.brandingData.colors[key];
      }
      // Update merged data to use theme default
      this.mergedData.colors[key] = this.themeData.colors?.[key] || '';
    } else {
      // Update branding data
      if (!this.brandingData.colors) {
        this.brandingData.colors = {};
      }
      this.brandingData.colors[key] = value;

      // Update merged data
      this.mergedData.colors[key] = value;
    }

    // Update preview immediately with new color
    this.refreshPreview();

    // Refresh status indicator
    this.refreshPropertyStatus('colors', key);

    // Send update to server
    this.sendUpdate('colors', this.brandingData.colors || {});
  }

  // Typography Management
  setupTypographyInputs() {
    const fontInputs = document.querySelectorAll('[id^="font-"]');

    fontInputs.forEach(input => {
      const key = input.id.replace('font-', '').replace('-', '_');

      // Set initial value
      if (this.brandingData.typography && this.brandingData.typography[key]) {
        input.value = this.brandingData.typography[key];
      }

      // Handle changes
      input.addEventListener('input', () => {
        this.updateTypography(key, input.value);
      });
    });

    // Initialize typography editors after setup
    this.initializeTypographyEditors();
  }

  initializeTypographyEditors() {
    // Initialize typography editors for body + h1-h6 heading levels + menu
    ['body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'menu'].forEach(type => {
      // Idempotent guard: skip if already initialized
      if (this.typographyEditors[type]) return;

      const inputField = document.getElementById(`font-${type}`);
      if (!inputField) return;

      // Check if TypographyEditor class is available
      if (typeof TypographyEditor === 'undefined') {
        console.warn('Typography Editor not loaded');
        return;
      }

      // Get current settings
      const currentSettings = this.getTypographySettings(type);

      // Create new editor instance
      const editor = new TypographyEditor({
        showEffects: false,
        onChange: (css, settings) => {
          this.handleTypographyChange(type, settings);
        },
        onApply: (css, settings) => {
          this.applyTypographySettings(type, settings);
        },
      });

      // Attach to input field (editor will create its own button)
      editor.attach(inputField.parentElement, '');

      // Set current settings
      editor.setSettings(currentSettings);

      // Store reference
      this.typographyEditors[type] = editor;
    });
  }

  // This method is kept for backward compatibility but not used since editors are initialized on page load
  openTypographyEditor(type) {
    // The typography editors are now initialized on page load with their own trigger buttons
    // This method can be removed once all references are updated
    console.log('Typography editors are now self-managed with their own trigger buttons');
  }

  // Setup typography info tooltips to show full style declaration on hover
  setupTypographyInfoTooltips() {
    const infoIcons = document.querySelectorAll('.bb-typography-info');

    infoIcons.forEach(icon => {
      const type = icon.dataset.typographyType;
      const tooltip = icon.querySelector('.bb-typography-tooltip');

      if (!tooltip || !type) return;

      // Show tooltip on hover with positioning
      icon.addEventListener('mouseenter', () => {
        this.updateTypographyTooltip(type, tooltip);
        this.positionTooltip(icon, tooltip);
        tooltip.classList.add('visible');
      });

      icon.addEventListener('mouseleave', () => {
        tooltip.classList.remove('visible');
      });
    });
  }

  // Position tooltip using fixed positioning, ensuring it stays in viewport
  positionTooltip(icon, tooltip) {
    const iconRect = icon.getBoundingClientRect();
    const tooltipWidth = 320;
    const tooltipHeight = 250; // approximate height
    const gap = 10;

    // Calculate horizontal position
    let left = iconRect.left;

    // Ensure tooltip stays within viewport horizontally
    if (left + tooltipWidth > window.innerWidth - 20) {
      left = window.innerWidth - tooltipWidth - 20;
    }
    if (left < 20) {
      left = 20;
    }

    tooltip.style.left = `${left}px`;

    // Check if there's enough space above the icon
    const spaceAbove = iconRect.top;
    const spaceBelow = window.innerHeight - iconRect.bottom;

    if (spaceAbove >= tooltipHeight + gap) {
      // Position above the icon
      tooltip.style.bottom = `${window.innerHeight - iconRect.top + gap}px`;
      tooltip.style.top = 'auto';
    } else if (spaceBelow >= tooltipHeight + gap) {
      // Position below the icon
      tooltip.style.top = `${iconRect.bottom + gap}px`;
      tooltip.style.bottom = 'auto';
    } else {
      // Not enough space either way - position where there's more room
      if (spaceAbove > spaceBelow) {
        tooltip.style.bottom = `${window.innerHeight - iconRect.top + gap}px`;
        tooltip.style.top = 'auto';
      } else {
        tooltip.style.top = `${iconRect.bottom + gap}px`;
        tooltip.style.bottom = 'auto';
      }
    }
  }

  // Update a single typography tooltip with current settings
  updateTypographyTooltip(type, tooltip) {
    const settings = this.getTypographySettings(type);

    // Get computed styles from preview frame
    const computedStyles = this.getComputedTypographyStyles(type);

    // Build tooltip HTML with typography properties
    // Show computed value first, then variable name if different
    const rows = [
      { label: 'Font Family', value: settings.fontFamily, computed: computedStyles.fontFamily },
      { label: 'Font Size', value: settings.fontSize, computed: computedStyles.fontSize },
      { label: 'Font Weight', value: settings.fontWeight, computed: computedStyles.fontWeight },
      { label: 'Line Height', value: settings.lineHeight, computed: computedStyles.lineHeight },
      {
        label: 'Letter Spacing',
        value: settings.letterSpacing,
        computed: computedStyles.letterSpacing,
      },
      {
        label: 'Text Transform',
        value: settings.textTransform,
        computed: computedStyles.textTransform,
      },
    ];

    // Add non-default properties
    if (settings.wordSpacing && settings.wordSpacing !== 'normal') {
      rows.push({
        label: 'Word Spacing',
        value: settings.wordSpacing,
        computed: computedStyles.wordSpacing,
      });
    }
    if (settings.textDecoration && settings.textDecoration !== 'none') {
      rows.push({
        label: 'Text Decoration',
        value: settings.textDecoration,
        computed: computedStyles.textDecoration,
      });
    }
    if (settings.textAlign && settings.textAlign !== 'left') {
      rows.push({
        label: 'Text Align',
        value: settings.textAlign,
        computed: computedStyles.textAlign,
      });
    }

    tooltip.innerHTML = rows
      .map(row => {
        const hasVariable = row.value && row.value.startsWith('var(');
        const computedValue = row.computed || this.resolveDefaultValue(row.value);

        return `<div class="tooltip-row">
                <span class="tooltip-label">${row.label}</span>
                <span class="tooltip-computed">${computedValue}</span>
                ${hasVariable ? `<span class="tooltip-variable">${row.value}</span>` : ''}
            </div>`;
      })
      .join('');
  }

  // Get computed styles from the preview frame element
  getComputedTypographyStyles(type) {
    const defaults = {
      fontFamily: 'System UI',
      fontSize: '16px',
      fontWeight: '400',
      lineHeight: '1.5',
      letterSpacing: '0px',
      wordSpacing: '0px',
      textTransform: 'none',
      textDecoration: 'none',
      textAlign: 'left',
    };

    try {
      const previewFrame = document.getElementById('preview-frame');
      if (!previewFrame) return defaults;

      // Direct ID lookup within the div (preview-frame is a div, not an iframe)
      const element = previewFrame.querySelector(`#preview-${type}`);
      if (!element) return defaults;

      // Use window.getComputedStyle since preview-frame is a div, not an iframe
      const styles = window.getComputedStyle(element);

      return {
        fontFamily: this.cleanFontFamily(styles.fontFamily),
        fontSize: styles.fontSize,
        fontWeight: styles.fontWeight,
        lineHeight: styles.lineHeight,
        letterSpacing: styles.letterSpacing,
        wordSpacing: styles.wordSpacing,
        textTransform: styles.textTransform,
        textDecoration: styles.textDecorationLine || styles.textDecoration,
        textAlign: styles.textAlign,
      };
    } catch (e) {
      console.warn('Could not get computed styles from preview:', e);
      return defaults;
    }
  }

  // Clean up font family string for display
  cleanFontFamily(fontFamily) {
    if (!fontFamily) return 'System UI';
    // Take only the first font in the stack and clean up quotes
    const firstFont = fontFamily.split(',')[0].trim().replace(/['"]/g, '');
    return firstFont || 'System UI';
  }

  // Resolve default value when it's not a CSS variable
  resolveDefaultValue(value) {
    if (!value) return 'inherit';
    if (value.startsWith('var(')) {
      // Extract variable name for display
      return value;
    }
    return value;
  }

  getTypographySettings(type) {
    // Handle menu type separately - it stores in the menu section
    if (type === 'menu') {
      const menuBranding = this.brandingData.menu || {};
      const menuTheme = this.themeData.menu || {};
      return {
        fontFamily: menuBranding['font-family'] || menuTheme['font-family'] || 'inherit',
        fontSize: menuBranding['font-size'] || menuTheme['font-size'] || '0.9rem',
        fontWeight: menuBranding['font-weight'] || menuTheme['font-weight'] || '500',
        fontStyle: menuBranding['font-style'] || menuTheme['font-style'] || 'normal',
        lineHeight: menuBranding['line-height'] || menuTheme['line-height'] || 'normal',
        letterSpacing: menuBranding['letter-spacing'] || menuTheme['letter-spacing'] || 'normal',
        wordSpacing: menuBranding['word-spacing'] || menuTheme['word-spacing'] || 'normal',
        textTransform: menuBranding['text-transform'] || menuTheme['text-transform'] || 'none',
        textAlign: menuBranding['text-align'] || menuTheme['text-align'] || 'left',
        textDecoration: menuBranding['text-decoration'] || menuTheme['text-decoration'] || 'none',
        textDecorationStyle:
          menuBranding['text-decoration-style'] || menuTheme['text-decoration-style'] || 'solid',
        textIndent: menuBranding['text-indent'] || menuTheme['text-indent'] || '0',
        fontVariant: menuBranding['font-variant'] || menuTheme['font-variant'] || 'normal',
        verticalAlign: menuBranding['vertical-align'] || menuTheme['vertical-align'] || 'baseline',
        direction: menuBranding['direction'] || menuTheme['direction'] || 'ltr',
      };
    }

    // Convert branding data to TypographyEditor settings format
    // Check multiple data sources: branding, typography tokens, and element tokens
    const typography = this.brandingData.typography || {};
    const themeTypography = this.themeData.typography || {};
    const elements = this.themeData.elements || {};

    // Get element data from theme
    // Structure: elements.heading has keys like "h1-font-family", "h1-size"
    // Structure: elements.body has keys like "font-family", "font-size"
    const headingTokens = elements.heading || {};
    const bodyTokens = elements.body || {};

    // Helper to get value with priority: branding > theme typography > element tokens
    const getValue = (headingKey, bodyKey, brandingKey) => {
      // Check branding data first
      const brandingValue =
        typography[`${brandingKey}_${type}`] || typography[`font_${brandingKey}_${type}`];
      if (brandingValue) return brandingValue;

      // Check theme typography
      const themeValue =
        themeTypography[`${headingKey}-${type}`] || themeTypography[`${type}-${headingKey}`];
      if (themeValue) return themeValue;

      // Check element tokens
      if (type === 'body') {
        return bodyTokens[bodyKey] || null;
      } else if (type.match(/^h[1-6]$/)) {
        return headingTokens[`${type}-${headingKey}`] || null;
      }

      return null;
    };

    // Map each property to its token key format
    // Heading tokens: h1-font-family, h1-size (not h1-font-size), h1-font-weight, h1-line-height, etc.
    // Body tokens: font-family, font-size, font-weight, line-height, etc.
    return {
      fontFamily: getValue('font-family', 'font-family', 'family') || 'inherit',
      fontSize: getValue('size', 'font-size', 'size') || '16px',
      fontWeight: getValue('font-weight', 'font-weight', 'weight') || '400',
      fontStyle: getValue('font-style', 'font-style', 'style') || 'normal',
      lineHeight: getValue('line-height', 'line-height', 'line_height') || 'normal',
      letterSpacing: getValue('letter-spacing', 'letter-spacing', 'letter_spacing') || 'normal',
      wordSpacing: getValue('word-spacing', 'word-spacing', 'word_spacing') || 'normal',
      textTransform: getValue('text-transform', 'text-transform', 'text_transform') || 'none',
      textAlign: getValue('text-align', 'text-align', 'text_align') || 'left',
      textDecoration: getValue('text-decoration', 'text-decoration', 'text_decoration') || 'none',
      textDecorationStyle:
        getValue('text-decoration-style', 'text-decoration-style', 'text_decoration_style') ||
        'solid',
      textIndent: getValue('text-indent', 'text-indent', 'text_indent') || '0',
      fontVariant: getValue('font-variant', 'font-variant', 'font_variant') || 'normal',
      verticalAlign: getValue('vertical-align', 'vertical-align', 'vertical_align') || 'baseline',
      direction: getValue('direction', 'direction', 'direction') || 'ltr',
    };
  }

  handleTypographyChange(type, settings) {
    // Handle menu type separately - store in menu section
    if (type === 'menu') {
      if (!this.brandingData.menu) {
        this.brandingData.menu = {};
      }

      // Store menu typography settings using hyphen format
      if (settings.fontFamily) this.brandingData.menu['font-family'] = settings.fontFamily;
      if (settings.fontSize) this.brandingData.menu['font-size'] = settings.fontSize;
      if (settings.fontWeight) this.brandingData.menu['font-weight'] = settings.fontWeight;
      if (settings.lineHeight) this.brandingData.menu['line-height'] = settings.lineHeight;
      if (settings.letterSpacing) this.brandingData.menu['letter-spacing'] = settings.letterSpacing;
      if (settings.fontStyle) this.brandingData.menu['font-style'] = settings.fontStyle;
      if (settings.textTransform) this.brandingData.menu['text-transform'] = settings.textTransform;

      // Update merged data to reflect the changes
      this.mergedData = this.mergeTokens();

      // Update preview frame
      this.updatePreviewFrame();
      return;
    }

    // Update preview in real-time without saving
    if (!this.brandingData.typography) {
      this.brandingData.typography = {};
    }

    // Map settings to branding data format
    this.mapTypographySettings(this.brandingData.typography, type, settings);

    // Update merged data to reflect the changes
    this.mergedData = this.mergeTokens();

    // Update preview frame
    this.updatePreviewFrame();

    // Update typography info tooltip for this type
    const infoIcon = document.querySelector(`.bb-typography-info[data-typography-type="${type}"]`);
    if (infoIcon) {
      const tooltip = infoIcon.querySelector('.bb-typography-tooltip');
      if (tooltip) {
        this.updateTypographyTooltip(type, tooltip);
      }
    }
  }

  applyTypographySettings(type, settings) {
    // Handle menu type separately - store in menu section instead of typography
    if (type === 'menu') {
      if (!this.brandingData.menu) {
        this.brandingData.menu = {};
      }

      // Store menu typography settings using hyphen format
      if (settings.fontFamily) this.brandingData.menu['font-family'] = settings.fontFamily;
      if (settings.fontSize) this.brandingData.menu['font-size'] = settings.fontSize;
      if (settings.fontWeight) this.brandingData.menu['font-weight'] = settings.fontWeight;
      if (settings.lineHeight) this.brandingData.menu['line-height'] = settings.lineHeight;
      if (settings.letterSpacing) this.brandingData.menu['letter-spacing'] = settings.letterSpacing;
      if (settings.fontStyle) this.brandingData.menu['font-style'] = settings.fontStyle;
      if (settings.textTransform) this.brandingData.menu['text-transform'] = settings.textTransform;

      // Update the display input
      const input = document.getElementById('font-menu');
      if (input) {
        input.value = settings.fontFamily || 'Click to customize';
      }

      // Update preview
      this.mergedData = this.mergeTokens();
      this.updatePreviewFrame();

      // Send update to server
      this.sendUpdate('menu', this.brandingData.menu);
      return;
    }

    // Map and save typography settings to elements section
    if (!this.brandingData.typography) {
      this.brandingData.typography = {};
    }

    this.mapTypographySettings(this.brandingData.typography, type, settings);

    // Update the display input
    const input = document.getElementById(`font-${type}`);
    if (input) {
      input.value = settings.fontFamily;
    }

    // Update typography info tooltip for this type
    const infoIcon = document.querySelector(`.bb-typography-info[data-typography-type="${type}"]`);
    if (infoIcon) {
      const tooltip = infoIcon.querySelector('.bb-typography-tooltip');
      if (tooltip) {
        this.updateTypographyTooltip(type, tooltip);
      }
    }

    // Send updates to server - both elements (new format) and typography (legacy)
    this.sendUpdate('elements', this.brandingData.elements || {});
    this.sendUpdate('typography', this.brandingData.typography);
  }

  mapTypographySettings(target, type, settings) {
    // Store all typography settings in elements section using hyphen format
    // This matches the tokens.json structure: elements.heading.h1-font-family, elements.body.font-family

    // Determine element category and key prefix
    const elementCategory = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(type) ? 'heading' : type;
    const prefix = elementCategory === 'heading' ? `${type}-` : '';

    // Initialize elements storage
    if (!this.brandingData.elements) {
      this.brandingData.elements = {};
    }
    if (!this.brandingData.elements[elementCategory]) {
      this.brandingData.elements[elementCategory] = {};
    }

    const element = this.brandingData.elements[elementCategory];

    // Map settings to element tokens with hyphen format
    const mappings = {
      fontFamily: 'font-family',
      fontSize: 'font-size',
      fontWeight: 'font-weight',
      fontStyle: 'font-style',
      lineHeight: 'line-height',
      letterSpacing: 'letter-spacing',
      wordSpacing: 'word-spacing',
      textTransform: 'text-transform',
      textAlign: 'text-align',
      textDecoration: 'text-decoration',
      textDecorationStyle: 'text-decoration-style',
      textIndent: 'text-indent',
      verticalAlign: 'vertical-align',
      fontVariant: 'font-variant',
    };

    for (const [editorKey, tokenKey] of Object.entries(mappings)) {
      const fullKey = `${prefix}${tokenKey}`;

      if (
        settings[editorKey] &&
        settings[editorKey] !== 'inherit' &&
        settings[editorKey] !== 'normal' &&
        settings[editorKey] !== 'none' &&
        settings[editorKey] !== '0' &&
        settings[editorKey] !== '0px'
      ) {
        element[fullKey] = settings[editorKey];
      } else {
        // Remove the property if it's a default value
        delete element[fullKey];
      }
    }

    // Clean up empty objects
    if (Object.keys(element).length === 0) {
      delete this.brandingData.elements[elementCategory];
    }
    if (Object.keys(this.brandingData.elements).length === 0) {
      delete this.brandingData.elements;
    }

    // Also update legacy typography section for backward compatibility with save endpoint
    // (This will be removed once backend is updated to read from elements)
    if (settings.fontFamily) {
      target[`font_family_${type}`] = settings.fontFamily;
    }
  }

  updateTypography(key, value) {
    if (!this.brandingData.typography) {
      this.brandingData.typography = {};
    }
    // Use consistent key format: font_family_{type}
    const normalizedKey = key.startsWith('font_family_') ? key : `font_family_${key}`;
    this.brandingData.typography[normalizedKey] = value;

    // Also delete legacy short-form key if it exists
    if (!key.startsWith('font_family_') && this.brandingData.typography[key]) {
      delete this.brandingData.typography[key];
    }

    this.sendUpdate('typography', this.brandingData.typography);
  }

  // Spacing Management
  setupSpacingInputs() {
    const spacingBase = document.getElementById('spacing-base');

    if (spacingBase) {
      // Set initial value
      if (this.brandingData.spacing && this.brandingData.spacing.base) {
        spacingBase.value = this.brandingData.spacing.base;
      }

      // Handle changes
      spacingBase.addEventListener('input', () => {
        this.updateSpacing('base', spacingBase.value);
        this.updateSpacingScale(spacingBase.value);
      });
    }
  }

  updateSpacing(key, value) {
    if (!this.brandingData.spacing) {
      this.brandingData.spacing = {};
    }
    this.brandingData.spacing[key] = value;

    this.sendUpdate('spacing', { [key]: value });
  }

  updateSpacingScale(baseValue) {
    // Update the spacing scale preview
    const scaleItems = document.querySelectorAll('.scale-item');
    const baseNumber = parseFloat(baseValue);
    const unit = baseValue.replace(/[0-9.]/g, '');

    scaleItems.forEach(item => {
      const scale = parseInt(item.dataset.scale);
      const value = baseNumber * scale + unit;
      const span = item.querySelector('span');
      if (span) {
        span.textContent = value;
      }
    });
  }

  // Border Management
  setupBorderInputs() {
    const borderInputs = document.querySelectorAll('[id^="border-radius-"]');

    borderInputs.forEach(input => {
      const key = input.id.replace('border-radius-', '').replace('-', '_');

      // Set initial value
      if (this.brandingData.borders && this.brandingData.borders[`radius_${key}`]) {
        input.value = this.brandingData.borders[`radius_${key}`];
      }

      // Handle changes
      input.addEventListener('input', () => {
        this.updateBorder(`radius_${key}`, input.value);
      });
    });
  }

  updateBorder(key, value) {
    if (!this.brandingData.borders) {
      this.brandingData.borders = {};
    }
    this.brandingData.borders[key] = value;

    this.sendUpdate('borders', { [key]: value });
  }

  // Initialize Border Editors for Components
  initializeBorderEditors() {
    // Component contexts for border editing
    const borderContexts = ['button', 'input', 'card', 'modal'];

    borderContexts.forEach(context => {
      const inputField = document.getElementById(`border-${context}`);
      if (!inputField) return;

      // Check if BorderEditorUtility is available
      if (typeof BorderEditorUtility === 'undefined') {
        console.warn('Border Editor utility not loaded');
        return;
      }

      // Get current border settings for this context
      const currentSettings = this.getBorderSettings(context);

      // Create border editor instance with full features
      const editor = new BorderEditorUtility({
        showPreview: true,
        showPresets: true,
        showAdvanced: true,
        showCornerShape: true, // Enable corner shapes (round, bevel, scoop, notch)
        allowIndividualSides: true, // Enable individual side width controls
        allowIndividualCorners: true, // Allow per-corner radius
        colorPickerIntegration: true,
        unitSelectorIntegration: true,
        onChange: (borderData, css) => {
          this.handleBorderChange(context, borderData, css);
        },
        onApply: (borderData, css) => {
          this.applyBorderSettings(context, borderData, css);
        },
      });

      // Attach to input field's parent (so trigger button is added)
      editor.attach(inputField.parentElement, '');

      // Set initial settings from theme/branding
      if (currentSettings) {
        editor.setSettings(currentSettings);
      }

      // Update input field with summary
      this.updateBorderInputSummary(context, currentSettings);

      // Store reference
      this.borderEditors[context] = editor;
    });
  }

  getBorderSettings(context) {
    const borders = this.brandingData.borders || {};
    const themeBorders = this.themeData.borders || {};

    // Check both hyphen and underscore formats
    const getValue = key => {
      return (
        borders[`${context}-${key}`] ||
        borders[`${context}_${key}`] ||
        themeBorders[`${context}-${key}`] ||
        themeBorders[`${context}_${key}`]
      );
    };

    // Parse individual properties
    const width = getValue('width') || '1px';
    const style = getValue('style') || 'solid';
    const color = getValue('color') || this.mergedData.colors?.border || '#E5E7EB';
    const radius = getValue('radius') || '0.375rem';
    const cornerShape = getValue('corner-shape') || 'round';

    // Parse width into number and unit
    const widthMatch = width.match(/^(\d+(?:\.\d+)?)(px|em|rem|%)?$/);
    const radiusMatch = radius.match(/^(\d+(?:\.\d+)?)(px|em|rem|%)?$/);

    return {
      style: style,
      width: widthMatch ? widthMatch[1] : '1',
      widthUnit: widthMatch ? widthMatch[2] || 'px' : 'px',
      color: color,
      radius: radiusMatch ? radiusMatch[1] : '0',
      radiusUnit: radiusMatch ? radiusMatch[2] || 'px' : 'px',
      cornerShape: cornerShape,
      cornersLinked: true,
      sidesLinked: true,
    };
  }

  // Consolidated border persistence logic
  persistBorder(context, borderData, options = {}) {
    const { saveToServer = false } = options;

    if (!this.brandingData.borders) {
      this.brandingData.borders = {};
    }

    // Store all border properties
    this.brandingData.borders[`${context}-width`] = `${borderData.width}${borderData.widthUnit}`;
    this.brandingData.borders[`${context}-style`] = borderData.style;
    this.brandingData.borders[`${context}-color`] = borderData.color;

    // Handle radius - check if corners are linked
    if (borderData.cornersLinked) {
      this.brandingData.borders[`${context}-radius`] =
        `${borderData.radius}${borderData.radiusUnit}`;
    } else {
      const tl = borderData.topLeftRadius || borderData.radius;
      const tr = borderData.topRightRadius || borderData.radius;
      const br = borderData.bottomRightRadius || borderData.radius;
      const bl = borderData.bottomLeftRadius || borderData.radius;
      this.brandingData.borders[`${context}-radius`] =
        `${tl}${borderData.radiusUnit} ${tr}${borderData.radiusUnit} ${br}${borderData.radiusUnit} ${bl}${borderData.radiusUnit}`;
    }

    // Handle corner shape (experimental CSS feature)
    if (borderData.cornerShape && borderData.cornerShape !== 'round') {
      this.brandingData.borders[`${context}-corner-shape`] = borderData.cornerShape;
    } else {
      delete this.brandingData.borders[`${context}-corner-shape`];
    }

    // Update display input summary
    this.updateBorderInputSummary(context, borderData);

    if (saveToServer) {
      this.sendUpdate('borders', this.brandingData.borders);
    } else {
      this.mergedData = this.mergeTokens();
      this.updatePreviewFrame();
    }
  }

  handleBorderChange(context, borderData, css) {
    // Real-time preview update (no server save)
    this.persistBorder(context, borderData, { saveToServer: false });
  }

  applyBorderSettings(context, borderData, css) {
    // Final apply with server save
    this.persistBorder(context, borderData, { saveToServer: true });
  }

  updateBorderInputSummary(context, borderData) {
    const input = document.getElementById(`border-${context}`);
    if (!input) return;

    const width = `${borderData.width}${borderData.widthUnit}`;
    const style = borderData.style;
    const radius = `${borderData.radius}${borderData.radiusUnit}`;

    // Create readable summary
    if (style === 'none') {
      input.value = 'No border';
    } else {
      input.value = `${width} ${style} • ${radius} radius`;
    }
  }

  // ==========================================================================
  // BUTTON ELEMENT EDITORS (Border + Typography for button elements)
  // These use elements.button.* tokens instead of the borders/typography objects
  // ==========================================================================

  initializeButtonEditors() {
    this.initializeButtonBorderEditor();
    this.initializeButtonTypographyEditor();
    this.setupButtonSizeTabs();
  }

  // Button Border Editor - stores to elements.button.radius and elements.button.border-width
  initializeButtonBorderEditor() {
    const inputField = document.getElementById('button-border');
    if (!inputField) return;

    if (typeof BorderEditorUtility === 'undefined') {
      console.warn('Border Editor utility not loaded');
      return;
    }

    const currentSettings = this.getButtonBorderSettings();

    const editor = new BorderEditorUtility({
      showPreview: true,
      showPresets: true,
      showAdvanced: true,
      showCornerShape: true,
      allowIndividualSides: false, // Buttons typically use uniform borders
      allowIndividualCorners: true,
      colorPickerIntegration: true,
      unitSelectorIntegration: true,
      onChange: (borderData, css) => {
        this.handleButtonBorderChange(borderData);
      },
      onApply: (borderData, css) => {
        this.applyButtonBorderSettings(borderData);
      },
    });

    editor.attach(inputField.parentElement, '');

    if (currentSettings) {
      editor.setSettings(currentSettings);
    }

    this.updateButtonBorderSummary(currentSettings);
    this.borderEditors['button-element'] = editor;
  }

  getButtonBorderSettings() {
    const elements = this.mergedData.elements || {};
    const button = elements.button || {};

    // Get raw values and resolve CSS variables
    const rawRadius = button['radius'] || 'var(--theme-radius-md)';
    const rawBorderWidth = button['border-width'] || 'var(--theme-border-width-1)';

    const radius = this.resolveCssVariable(rawRadius);
    const borderWidth = this.resolveCssVariable(rawBorderWidth);

    // Parse CSS values - try to extract number and unit
    let radiusValue = '0.5';
    let radiusUnit = 'rem';
    let widthValue = '1';
    let widthUnit = 'px';

    // Try to parse actual values
    const radiusMatch = radius.match(/^(\d+(?:\.\d+)?)(px|em|rem|%)?$/);
    if (radiusMatch) {
      radiusValue = radiusMatch[1];
      radiusUnit = radiusMatch[2] || 'rem';
    }

    const widthMatch = borderWidth.match(/^(\d+(?:\.\d+)?)(px|em|rem|%)?$/);
    if (widthMatch) {
      widthValue = widthMatch[1];
      widthUnit = widthMatch[2] || 'px';
    }

    return {
      style: 'solid',
      width: widthValue,
      widthUnit: widthUnit,
      color: 'currentColor',
      radius: radiusValue,
      radiusUnit: radiusUnit,
      cornerShape: 'round',
      cornersLinked: true,
      sidesLinked: true,
    };
  }

  handleButtonBorderChange(borderData) {
    this.updateButtonBorderTokens(borderData, false);
  }

  applyButtonBorderSettings(borderData) {
    this.updateButtonBorderTokens(borderData, true);
    this.updateButtonBorderSummary(borderData);
  }

  updateButtonBorderTokens(borderData, saveToServer) {
    if (!this.brandingData.elements) {
      this.brandingData.elements = {};
    }
    if (!this.brandingData.elements.button) {
      this.brandingData.elements.button = {};
    }

    const buttonTokens = this.brandingData.elements.button;

    // Update radius
    if (borderData.cornersLinked) {
      buttonTokens['radius'] = `${borderData.radius}${borderData.radiusUnit}`;
    } else {
      const tl = borderData.topLeftRadius || borderData.radius;
      const tr = borderData.topRightRadius || borderData.radius;
      const br = borderData.bottomRightRadius || borderData.radius;
      const bl = borderData.bottomLeftRadius || borderData.radius;
      buttonTokens['radius'] =
        `${tl}${borderData.radiusUnit} ${tr}${borderData.radiusUnit} ${br}${borderData.radiusUnit} ${bl}${borderData.radiusUnit}`;
    }

    // Update border width
    buttonTokens['border-width'] = `${borderData.width}${borderData.widthUnit}`;

    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();

    if (saveToServer) {
      this.sendUpdate('elements', this.brandingData.elements);
    }
  }

  updateButtonBorderSummary(borderData) {
    const input = document.getElementById('button-border');
    if (!input) return;

    const radius = `${borderData.radius}${borderData.radiusUnit}`;
    const width = `${borderData.width}${borderData.widthUnit}`;

    input.value = `${radius} radius • ${width} border`;
  }

  resetButtonBorderDefaults() {
    // Reset button border tokens to theme defaults
    if (this.brandingData.elements?.button) {
      delete this.brandingData.elements.button['radius'];
      delete this.brandingData.elements.button['border-width'];

      // Clean up empty objects
      if (Object.keys(this.brandingData.elements.button).length === 0) {
        delete this.brandingData.elements.button;
      }
      if (Object.keys(this.brandingData.elements).length === 0) {
        delete this.brandingData.elements;
      }
    }

    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();
    this.sendUpdate('elements', this.brandingData.elements || {});

    // Reinitialize the editor with theme defaults
    const currentSettings = this.getButtonBorderSettings();
    if (this.borderEditors['button-element']) {
      this.borderEditors['button-element'].setSettings(currentSettings);
    }
    this.updateButtonBorderSummary(currentSettings);
  }

  // Button Typography Editor - stores to elements.button typography tokens
  initializeButtonTypographyEditor() {
    const inputField = document.getElementById('button-typography');
    if (!inputField) return;

    if (typeof TypographyEditor === 'undefined') {
      console.warn('Typography Editor not loaded');
      return;
    }

    const currentSettings = this.getButtonTypographySettings();

    const editor = new TypographyEditor({
      showEffects: false,
      onChange: (css, settings) => {
        this.handleButtonTypographyChange(settings);
      },
      onApply: (css, settings) => {
        this.applyButtonTypographySettings(settings);
      },
    });

    editor.attach(inputField.parentElement, '');
    editor.setSettings(currentSettings);

    this.updateButtonTypographySummary(currentSettings);
    this.typographyEditors['button-element'] = editor;
  }

  getButtonTypographySettings() {
    const elements = this.mergedData.elements || {};
    const button = elements.button || {};

    // Get raw values with defaults
    const rawFontFamily = button['font-family'] || 'var(--theme-font-family-body)';
    const rawLineHeight = button['line-height'] || 'var(--theme-line-height-normal)';
    const rawLetterSpacing = button['letter-spacing'] || 'var(--theme-letter-spacing-normal)';

    return {
      fontFamily: this.resolveCssVariable(rawFontFamily),
      fontWeight: button['font-weight'] || '500',
      lineHeight: this.resolveCssVariable(rawLineHeight),
      letterSpacing: this.resolveCssVariable(rawLetterSpacing),
      textTransform: button['text-transform'] || 'none',
    };
  }

  handleButtonTypographyChange(settings) {
    this.updateButtonTypographyTokens(settings, false);
  }

  applyButtonTypographySettings(settings) {
    this.updateButtonTypographyTokens(settings, true);
    this.updateButtonTypographySummary(settings);
  }

  updateButtonTypographyTokens(settings, saveToServer) {
    if (!this.brandingData.elements) {
      this.brandingData.elements = {};
    }
    if (!this.brandingData.elements.button) {
      this.brandingData.elements.button = {};
    }

    const buttonTokens = this.brandingData.elements.button;

    // Map TypographyEditor settings to button tokens
    if (settings.fontFamily) buttonTokens['font-family'] = settings.fontFamily;
    if (settings.fontWeight) buttonTokens['font-weight'] = settings.fontWeight;
    if (settings.lineHeight) buttonTokens['line-height'] = settings.lineHeight;
    if (settings.letterSpacing) buttonTokens['letter-spacing'] = settings.letterSpacing;
    if (settings.textTransform !== undefined)
      buttonTokens['text-transform'] = settings.textTransform;

    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();

    if (saveToServer) {
      this.sendUpdate('elements', this.brandingData.elements);
    }
  }

  updateButtonTypographySummary(settings) {
    const input = document.getElementById('button-typography');
    if (!input) return;

    // Extract readable font name from resolved value
    let fontName = settings.fontFamily || 'System';
    // Extract first font from stack (already resolved by getButtonTypographySettings)
    fontName = fontName.split(',')[0].replace(/['"]/g, '').trim();
    // Shorten system-ui to "System"
    if (fontName === 'system-ui' || fontName === '-apple-system') {
      fontName = 'System';
    }

    const weight = settings.fontWeight || '400';
    const transform = settings.textTransform || 'none';

    input.value = `${fontName} • ${weight} • ${transform}`;
  }

  resetButtonTypographyDefaults() {
    // Reset button typography tokens to theme defaults
    if (this.brandingData.elements?.button) {
      delete this.brandingData.elements.button['font-family'];
      delete this.brandingData.elements.button['font-weight'];
      delete this.brandingData.elements.button['line-height'];
      delete this.brandingData.elements.button['letter-spacing'];
      delete this.brandingData.elements.button['text-transform'];

      // Clean up empty objects
      if (Object.keys(this.brandingData.elements.button).length === 0) {
        delete this.brandingData.elements.button;
      }
      if (Object.keys(this.brandingData.elements).length === 0) {
        delete this.brandingData.elements;
      }
    }

    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();
    this.sendUpdate('elements', this.brandingData.elements || {});

    // Reinitialize the editor with theme defaults
    const currentSettings = this.getButtonTypographySettings();
    if (this.typographyEditors['button-element']) {
      this.typographyEditors['button-element'].setSettings(currentSettings);
    }
    this.updateButtonTypographySummary(currentSettings);
  }

  // Button Size Tabs (SM/MD/LG) for font-size and padding
  setupButtonSizeTabs() {
    // Find all size tab containers in button section
    const tabContainers = document.querySelectorAll('#buttons-group .bb-size-tabs');

    tabContainers.forEach(container => {
      const tabs = container.querySelectorAll('.bb-size-tab');
      const field = container.closest('.bb-size-variant-field');
      if (!field) return;

      const contents = field.querySelectorAll('.bb-size-content');

      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          const size = tab.dataset.size;

          // Update active tab
          tabs.forEach(t => t.classList.remove('active'));
          tab.classList.add('active');

          // Update visible content
          contents.forEach(c => {
            c.classList.toggle('active', c.dataset.size === size);
          });
        });
      });
    });
  }

  // ==========================================================================
  // CARD TYPE EDITORS (Background, Border, Shadow for card-default, card-elevated, etc.)
  // These use top-level card-* tokens (not nested under elements)
  // ==========================================================================

  initializeCardEditors() {
    this.setupCardTypeTabs();
    this.initializeCardBackgroundEditors();
    this.initializeCardBorderEditors();
    this.initializeCardShadowEditors();
  }

  // Card Type Tab Switching
  setupCardTypeTabs() {
    const tabs = document.querySelectorAll('#cards-group .bb-card-type-tab');
    const contents = document.querySelectorAll('#cards-group .bb-card-type-content');

    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const cardType = tab.dataset.cardType;

        // Update active tab
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        // Update visible content
        contents.forEach(c => {
          c.classList.toggle('active', c.dataset.cardType === cardType);
        });
      });
    });
  }

  // Card Background Editors - uses BackgroundEditor or ColorPicker
  initializeCardBackgroundEditors() {
    const cardTypes = ['default', 'elevated', 'bordered', 'minimal'];

    cardTypes.forEach(cardType => {
      const inputField = document.getElementById(`card-${cardType}-bg`);
      if (!inputField) return;

      const tokenKey = `card-${cardType}`;
      const currentValue = this.getCardTokenValue(cardType, 'bg');

      // Resolve and display current value
      const resolvedValue = this.resolveCssVariable(currentValue);
      inputField.value = resolvedValue || currentValue;

      // Check if BackgroundEditor is available
      if (typeof BackgroundEditor !== 'undefined') {
        const editor = new BackgroundEditor({
          onChange: css => {
            inputField.value = css;
            this.updateCardToken(cardType, 'bg', css, false);
          },
          onApply: css => {
            inputField.value = css;
            this.updateCardToken(cardType, 'bg', css, true);
          },
        });

        editor.attach(inputField, resolvedValue || currentValue);
        this.backgroundEditors[`card-${cardType}-bg`] = editor;
      } else if (typeof ColorPickerUtility !== 'undefined') {
        // Fallback to color picker
        const picker = new ColorPickerUtility({
          onChange: color => {
            inputField.value = color;
            this.updateCardToken(cardType, 'bg', color, false);
          },
          onApply: color => {
            inputField.value = color;
            this.updateCardToken(cardType, 'bg', color, true);
          },
        });

        picker.attach(inputField.parentElement, resolvedValue || currentValue);
        this.colorPickers[`card-${cardType}-bg`] = picker;
      }
    });
  }

  // Card Border Editors - uses BorderEditorUtility
  initializeCardBorderEditors() {
    const cardTypes = ['default', 'elevated', 'bordered', 'minimal'];

    cardTypes.forEach(cardType => {
      const inputField = document.getElementById(`card-${cardType}-border`);
      if (!inputField) return;

      if (typeof BorderEditorUtility === 'undefined') {
        console.warn('Border Editor utility not loaded for cards');
        return;
      }

      const currentSettings = this.getCardBorderSettings(cardType);

      const editor = new BorderEditorUtility({
        showPreview: true,
        showPresets: false,
        showAdvanced: false,
        showCornerShape: false,
        allowIndividualSides: false,
        allowIndividualCorners: false,
        colorPickerIntegration: true,
        onChange: (borderData, css) => {
          this.handleCardBorderChange(cardType, borderData);
        },
        onApply: (borderData, css) => {
          this.applyCardBorderSettings(cardType, borderData);
        },
      });

      editor.attach(inputField.parentElement, '');

      if (currentSettings) {
        editor.setSettings(currentSettings);
      }

      this.updateCardBorderSummary(cardType, currentSettings);
      this.borderEditors[`card-${cardType}`] = editor;
    });
  }

  getCardBorderSettings(cardType) {
    const borderWidth = this.getCardTokenValue(cardType, 'border-width') || '0';
    const borderColor = this.getCardTokenValue(cardType, 'border-color') || 'transparent';

    // Resolve CSS variables
    const resolvedWidth = this.resolveCssVariable(borderWidth);
    const resolvedColor = this.resolveCssVariable(borderColor);

    // Parse width
    let widthValue = '0';
    let widthUnit = 'px';
    const widthMatch = resolvedWidth.match(/^(\d+(?:\.\d+)?)(px|em|rem|%)?$/);
    if (widthMatch) {
      widthValue = widthMatch[1];
      widthUnit = widthMatch[2] || 'px';
    }

    return {
      style: widthValue === '0' ? 'none' : 'solid',
      width: widthValue,
      widthUnit: widthUnit,
      color: resolvedColor,
      radius: '0',
      radiusUnit: 'px',
      cornersLinked: true,
      sidesLinked: true,
    };
  }

  handleCardBorderChange(cardType, borderData) {
    this.updateCardBorderTokens(cardType, borderData, false);
  }

  applyCardBorderSettings(cardType, borderData) {
    this.updateCardBorderTokens(cardType, borderData, true);
    this.updateCardBorderSummary(cardType, borderData);
  }

  updateCardBorderTokens(cardType, borderData, saveToServer) {
    const tokenKey = `card-${cardType}`;

    if (!this.brandingData[tokenKey]) {
      this.brandingData[tokenKey] = {};
    }

    // Update border-width and border-color
    const width = borderData.style === 'none' ? '0' : `${borderData.width}${borderData.widthUnit}`;
    this.brandingData[tokenKey]['border-width'] = width;
    this.brandingData[tokenKey]['border-color'] = borderData.color;

    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();

    if (saveToServer) {
      this.sendUpdate(tokenKey, this.brandingData[tokenKey]);
    }
  }

  updateCardBorderSummary(cardType, borderData) {
    const input = document.getElementById(`card-${cardType}-border`);
    if (!input) return;

    if (borderData.style === 'none' || borderData.width === '0') {
      input.value = 'No border';
    } else {
      const width = `${borderData.width}${borderData.widthUnit}`;
      input.value = `${width} solid ${borderData.color}`;
    }
  }

  // Card Shadow Editors - uses ShadowEditor
  initializeCardShadowEditors() {
    const cardTypes = ['default', 'elevated', 'bordered', 'minimal'];
    const shadowProperties = ['shadow', 'shadow-hover'];

    cardTypes.forEach(cardType => {
      shadowProperties.forEach(prop => {
        const inputId =
          prop === 'shadow' ? `card-${cardType}-shadow` : `card-${cardType}-shadow-hover`;
        const inputField = document.getElementById(inputId);
        if (!inputField) return;

        if (typeof ShadowEditor === 'undefined') {
          console.warn('Shadow Editor not loaded for cards');
          return;
        }

        const currentValue = this.getCardTokenValue(cardType, prop);
        const resolvedValue = this.resolveCssVariable(currentValue);

        // Display resolved value
        inputField.value = resolvedValue || currentValue || 'none';

        const editor = new ShadowEditor({
          propertyKey: `card_${cardType}_${prop.replace('-', '_')}`,
          shadowType: 'box',
          onChange: css => {
            inputField.value = css;
            this.updateCardToken(cardType, prop, css, false);
          },
          onApply: css => {
            inputField.value = css;
            this.updateCardToken(cardType, prop, css, true);
          },
        });

        editor.attach(inputField, resolvedValue || currentValue);
        this.shadowEditors[`card-${cardType}-${prop}`] = editor;
      });
    });
  }

  // Helper: Get card token value from merged data
  getCardTokenValue(cardType, property) {
    const tokenKey = `card-${cardType}`;
    return this.brandingData[tokenKey]?.[property] || this.themeData[tokenKey]?.[property] || '';
  }

  // Helper: Update a card token
  updateCardToken(cardType, property, value, saveToServer) {
    const tokenKey = `card-${cardType}`;

    if (!this.brandingData[tokenKey]) {
      this.brandingData[tokenKey] = {};
    }

    this.brandingData[tokenKey][property] = value;

    // Update merged data
    if (!this.mergedData[tokenKey]) {
      this.mergedData[tokenKey] = {};
    }
    this.mergedData[tokenKey][property] = value;

    this.updatePreviewFrame();

    if (saveToServer) {
      this.sendUpdate(tokenKey, this.brandingData[tokenKey]);
    }
  }

  // Reset methods for card properties
  resetCardTypeDefault(cardType, property) {
    const tokenKey = `card-${cardType}`;

    if (this.brandingData[tokenKey]) {
      delete this.brandingData[tokenKey][property];

      if (Object.keys(this.brandingData[tokenKey]).length === 0) {
        delete this.brandingData[tokenKey];
      }
    }

    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();
    this.sendUpdate(tokenKey, this.brandingData[tokenKey] || {});

    // Update input with theme default
    const currentValue = this.getCardTokenValue(cardType, property);
    const resolvedValue = this.resolveCssVariable(currentValue);
    const input = document.getElementById(`card-${cardType}-${property}`);
    if (input) {
      input.value = resolvedValue || currentValue;
    }

    // Update editor if exists
    if (property === 'bg' && this.backgroundEditors[`card-${cardType}-bg`]) {
      this.backgroundEditors[`card-${cardType}-bg`].parseValue(resolvedValue || currentValue);
    }
  }

  resetCardTypeBorder(cardType) {
    const tokenKey = `card-${cardType}`;

    if (this.brandingData[tokenKey]) {
      delete this.brandingData[tokenKey]['border-width'];
      delete this.brandingData[tokenKey]['border-color'];

      if (Object.keys(this.brandingData[tokenKey]).length === 0) {
        delete this.brandingData[tokenKey];
      }
    }

    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();
    this.sendUpdate(tokenKey, this.brandingData[tokenKey] || {});

    // Reinitialize editor with theme defaults
    const currentSettings = this.getCardBorderSettings(cardType);
    if (this.borderEditors[`card-${cardType}`]) {
      this.borderEditors[`card-${cardType}`].setSettings(currentSettings);
    }
    this.updateCardBorderSummary(cardType, currentSettings);
  }

  resetCardTypeShadow(cardType, property) {
    const tokenKey = `card-${cardType}`;

    if (this.brandingData[tokenKey]) {
      delete this.brandingData[tokenKey][property];

      if (Object.keys(this.brandingData[tokenKey]).length === 0) {
        delete this.brandingData[tokenKey];
      }
    }

    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();
    this.sendUpdate(tokenKey, this.brandingData[tokenKey] || {});

    // Update input with theme default
    const currentValue = this.getCardTokenValue(cardType, property);
    const resolvedValue = this.resolveCssVariable(currentValue);
    const inputId =
      property === 'shadow' ? `card-${cardType}-shadow` : `card-${cardType}-shadow-hover`;
    const input = document.getElementById(inputId);
    if (input) {
      input.value = resolvedValue || currentValue || 'none';
    }

    // Update shadow editor if exists
    const editorKey = `card-${cardType}-${property}`;
    if (this.shadowEditors[editorKey]) {
      this.shadowEditors[editorKey].parseValue(resolvedValue || currentValue);
    }
  }

  // Shadow Management
  setupShadowInputs() {
    const shadowInputs = document.querySelectorAll('[id^="shadow-"]');

    shadowInputs.forEach(input => {
      const key = input.id.replace('shadow-', '');

      // Set initial value
      if (this.brandingData.shadows && this.brandingData.shadows[key]) {
        input.value = this.brandingData.shadows[key];
      }

      // Handle changes
      input.addEventListener('input', () => {
        this.updateShadow(key, input.value);
      });
    });
  }

  openShadowEditor(key) {
    // Map key to input element and section
    const shadowConfigs = {
      'menu-dropdown': {
        inputId: 'menu-dropdown-shadow',
        section: 'menu',
        property: 'dropdown-shadow',
        shadowType: 'box',
      },
      modal: {
        inputId: 'modal-shadow',
        section: 'elements.modal',
        property: 'shadow',
        shadowType: 'box',
      },
      'form-shadow': {
        inputId: 'form-shadow',
        section: 'elements.form',
        property: 'shadow',
        shadowType: 'box',
      },
      'form-focus-shadow': {
        inputId: 'form-focus-shadow',
        section: 'elements.form',
        property: 'focus-shadow',
        shadowType: 'box',
      },
      'search-dropdown-shadow': {
        inputId: 'search-dropdown-shadow',
        section: 'search',
        property: 'dropdown-shadow',
        shadowType: 'box',
      },
      'search-input-focus-shadow': {
        inputId: 'search-input-focus-shadow',
        section: 'search',
        property: 'input-focus-shadow',
        shadowType: 'box',
      },
    };

    const config = shadowConfigs[key];
    if (!config) {
      console.warn(`No shadow config for key: ${key}`);
      return;
    }

    const input = document.getElementById(config.inputId);
    if (!input) return;

    // Create or reuse editor instance
    if (!this.shadowEditors[key]) {
      const editor = new ShadowEditor({
        propertyKey: `${config.section}_${config.property.replace('-', '_')}`,
        shadowType: config.shadowType,
        onChange: css => {
          // Live preview only
          input.value = css;
          this.updateLayoutToken(config.section, config.property, css);
        },
        onApply: css => {
          // Save to server
          input.value = css;
          this.applyLayoutToken(config.section, config.property, css);
        },
      });

      // Get raw value and resolve CSS variables
      let rawValue;
      if (config.section.startsWith('elements.')) {
        const elementType = config.section.replace('elements.', '');
        rawValue =
          this.brandingData.elements?.[elementType]?.[config.property] ||
          this.themeData.elements?.[elementType]?.[config.property] ||
          '';
      } else {
        rawValue =
          this.brandingData[config.section]?.[config.property] ||
          this.themeData[config.section]?.[config.property] ||
          '';
      }
      const resolvedValue = this.resolveCssVariable(rawValue) || rawValue;

      // Populate input with resolved value
      if (resolvedValue) {
        input.value = resolvedValue;
      }

      // Attach to input with resolved value (ShadowEditor creates its own trigger button)
      editor.attach(input, resolvedValue);

      this.shadowEditors[key] = editor;
    }

    // Open the editor
    this.shadowEditors[key].open();
  }

  updateShadow(key, value) {
    if (!this.brandingData.shadows) {
      this.brandingData.shadows = {};
    }
    this.brandingData.shadows[key] = value;

    this.sendUpdate('shadows', { [key]: value });
  }

  // Layout Tab Utility Editor Initialization
  initializeSpacingEditors() {
    const spacingConfigs = [
      { id: 'header-padding', section: 'header', property: 'padding', mode: 'padding' },
      { id: 'footer-padding', section: 'footer', property: 'padding', mode: 'padding' },
    ];

    spacingConfigs.forEach(config => {
      const input = document.getElementById(config.id);
      const btn = document.getElementById(`${config.id}-btn`);
      if (!input || !btn) return;

      // Skip if already initialized
      if (this.spacingEditors[config.id]) return;

      // Get current value from branding or theme
      const currentValue =
        this.brandingData[config.section]?.[config.property] ||
        this.themeData[config.section]?.[config.property] ||
        '';

      // Create SpacingEditor instance
      const editor = new SpacingEditor({
        mode: config.mode,
        showPresets: true,
        showVisualEditor: false,
        onChange: css => {
          // Live preview update
          input.value = css;
          this.updateLayoutToken(config.section, config.property, css);
        },
        onApply: css => {
          // Save to server
          input.value = css;
          this.applyLayoutToken(config.section, config.property, css);
        },
      });

      // Set up the editor's trigger button reference for positioning
      editor.triggerButton = btn;
      editor.targetElement = input;

      // Wire up the button click to open the editor
      btn.addEventListener('click', e => {
        e.preventDefault();
        e.stopPropagation();
        // Parse current value and open editor
        const latestValue =
          this.brandingData[config.section]?.[config.property] ||
          this.themeData[config.section]?.[config.property] ||
          '';
        if (latestValue) editor.parseValue(latestValue);
        editor.open();
      });

      // Display current value
      if (currentValue) input.value = currentValue;

      this.spacingEditors[config.id] = editor;
    });
  }

  initializeShadowEditors() {
    // Initialize shadow editors for all shadow inputs in Layout and Components tabs
    const shadowInputs = [
      {
        key: 'menu-dropdown',
        inputId: 'menu-dropdown-shadow',
        section: 'menu',
        property: 'dropdown-shadow',
      },
      { key: 'modal', inputId: 'modal-shadow', section: 'elements.modal', property: 'shadow' },
      { key: 'form-shadow', inputId: 'form-shadow', section: 'elements.form', property: 'shadow' },
      {
        key: 'form-focus-shadow',
        inputId: 'form-focus-shadow',
        section: 'elements.form',
        property: 'focus-shadow',
      },
      {
        key: 'search-dropdown-shadow',
        inputId: 'search-dropdown-shadow',
        section: 'search',
        property: 'dropdown-shadow',
      },
      {
        key: 'search-input-focus-shadow',
        inputId: 'search-input-focus-shadow',
        section: 'search',
        property: 'input-focus-shadow',
      },
    ];

    shadowInputs.forEach(config => {
      const input = document.getElementById(config.inputId);
      if (!input) return;

      // Skip if already initialized
      if (this.shadowEditors[config.key]) return;

      // Get raw value from branding or theme (handle nested element sections)
      let rawValue;
      if (config.section.startsWith('elements.')) {
        const elementType = config.section.replace('elements.', '');
        rawValue =
          this.brandingData.elements?.[elementType]?.[config.property] ||
          this.themeData.elements?.[elementType]?.[config.property] ||
          '';
      } else {
        rawValue =
          this.brandingData[config.section]?.[config.property] ||
          this.themeData[config.section]?.[config.property] ||
          '';
      }

      // Resolve CSS variables to actual values for the editor
      const resolvedValue = this.resolveCssVariable(rawValue) || rawValue;

      // Populate the input field with the resolved value
      if (resolvedValue) {
        input.value = resolvedValue;
      }

      const editor = new ShadowEditor({
        propertyKey: `${config.section}_${config.property.replace('-', '_')}`,
        shadowType: 'box',
        onChange: css => {
          input.value = css;
          this.updateLayoutToken(config.section, config.property, css);
        },
        onApply: css => {
          input.value = css;
          this.applyLayoutToken(config.section, config.property, css);
        },
      });

      editor.attach(input, resolvedValue);
      this.shadowEditors[config.key] = editor;
    });
  }

  // Layout token helper methods
  updateLayoutToken(section, property, value) {
    // Handle nested sections like 'elements.modal'
    if (section.startsWith('elements.')) {
      const elementType = section.replace('elements.', '');
      if (!this.brandingData.elements) {
        this.brandingData.elements = {};
      }
      if (!this.brandingData.elements[elementType]) {
        this.brandingData.elements[elementType] = {};
      }
      this.brandingData.elements[elementType][property] = value;
    } else {
      if (!this.brandingData[section]) {
        this.brandingData[section] = {};
      }
      this.brandingData[section][property] = value;
    }
    this.mergedData = this.mergeTokens();
    this.updatePreviewFrame();
  }

  applyLayoutToken(section, property, value) {
    // Handle nested sections like 'elements.modal'
    if (section.startsWith('elements.')) {
      const elementType = section.replace('elements.', '');
      if (!this.brandingData.elements) {
        this.brandingData.elements = {};
      }
      if (!this.brandingData.elements[elementType]) {
        this.brandingData.elements[elementType] = {};
      }
      this.brandingData.elements[elementType][property] = value;
      this.sendUpdate('elements', this.brandingData.elements);
    } else {
      if (!this.brandingData[section]) {
        this.brandingData[section] = {};
      }
      this.brandingData[section][property] = value;
      this.sendUpdate(section, this.brandingData[section]);
    }
  }

  // Custom CSS Management
  setupCustomCSS() {
    const customCSS = document.getElementById('custom-css');

    if (customCSS) {
      // Set initial value
      if (this.brandingData.custom_css) {
        customCSS.value = this.brandingData.custom_css;
      }

      // Handle changes with debounce
      let cssTimer;
      customCSS.addEventListener('input', () => {
        clearTimeout(cssTimer);
        cssTimer = setTimeout(() => {
          this.updateCustomCSS(customCSS.value);
        }, 500);
      });
    }
  }

  updateCustomCSS(css) {
    this.brandingData.custom_css = css;
    this.sendUpdate('custom_css', { css });
  }

  // Load initial branding data
  loadBrandingData() {
    // Note: Color inputs are handled by setupColorInputs() which properly resolves
    // CSS variables. Do not duplicate color loading here to avoid overwriting
    // resolved values with raw CSS variable strings.

    // Backward compatibility: Migrate old heading_family to individual h1-h6
    if (
      this.brandingData.typography?.font_family_heading &&
      !this.brandingData.typography?.font_family_h1
    ) {
      const headingFont = this.brandingData.typography.font_family_heading;
      ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].forEach(level => {
        this.brandingData.typography[`font_family_${level}`] = headingFont;
      });
      // Remove old property after migration
      delete this.brandingData.typography.font_family_heading;

      // Auto-save the migration
      this.autoSave();
    }

    // Typography - Load body + h1-h6 heading levels
    // Check both underscore (branding) and hyphen (theme) formats
    const typographyFields = ['body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'];
    typographyFields.forEach(field => {
      const input = document.getElementById(`font-${field}`);
      if (input && this.mergedData.typography) {
        // Try both formats
        const value =
          this.mergedData.typography[`font_family_${field}`] ||
          this.mergedData.typography[`font-family-${field}`];
        if (value) {
          input.value = value;
        }
      }
    });

    // Apply initial styles to preview
    this.updatePreviewFrame();
  }

  // Send update to server
  async sendUpdate(type, values) {
    // Update preview immediately with local changes
    this.updatePreviewFrame();

    // Clear auto-save timer
    clearTimeout(this.autoSaveTimer);

    // Set new auto-save timer
    this.autoSaveTimer = setTimeout(() => {
      this.autoSave();
    }, 2000);

    // Send to server in background
    try {
      const response = await fetch(this.urls.update, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.csrfToken,
        },
        body: JSON.stringify({ type, values }),
      });

      const data = await response.json();

      if (!data.success) {
        console.error('Update failed:', data.error);
        this.showError(data.error);
      }
    } catch (error) {
      console.error('Update error:', error);
      this.showError(this.translations.error || 'Error updating branding');
    }
  }

  // Update preview styles directly in the DOM
  updatePreviewFrame(css) {
    const styleElement = document.getElementById('branding-preview-styles');
    if (styleElement) {
      styleElement.textContent = css || this.generateCSS();
    }
  }

  // Load the active theme CSS and scope it to preview
  async loadThemeCSS() {
    const themeCssUrl = window.themeCssUrl;
    if (!themeCssUrl) {
      console.warn('No theme CSS URL provided');
      return;
    }

    try {
      // Fetch the theme CSS
      const response = await fetch(themeCssUrl);
      const themeCss = await response.text();

      // Scope the CSS to #preview-frame
      const scopedCss = this.scopeCSSToPreview(themeCss);

      // Inject into the preview-theme-styles element
      const themeStyleElement = document.getElementById('preview-theme-styles');
      if (themeStyleElement) {
        themeStyleElement.textContent = scopedCss;
      }
    } catch (error) {
      console.error('Failed to load theme CSS:', error);
    }
  }

  // Helper to scope CSS rules to #preview-frame
  scopeCSSToPreview(css) {
    // Replace :root selectors with #preview-frame
    let scopedCss = css.replace(/:root\s*\{/g, '#preview-frame {');

    // Replace html selectors with #preview-frame
    scopedCss = scopedCss.replace(/(?<![a-zA-Z0-9_-])html\s*\{/g, '#preview-frame {');

    // Scope all other CSS rules to #preview-frame
    // This handles selectors like .btn, .card, etc.
    const lines = scopedCss.split('\n');
    const scopedLines = [];
    let inKeyframes = false;
    let braceDepth = 0;

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];

      // Track @keyframes blocks (don't scope these)
      if (line.includes('@keyframes')) {
        inKeyframes = true;
      }

      // Track brace depth for @keyframes
      if (inKeyframes) {
        braceDepth += (line.match(/\{/g) || []).length;
        braceDepth -= (line.match(/\}/g) || []).length;
        if (braceDepth <= 0 && line.includes('}')) {
          inKeyframes = false;
          braceDepth = 0;
        }
        scopedLines.push(line);
        continue;
      }

      // Skip lines that are already scoped, comments, @rules, or empty
      if (
        line.trim().startsWith('/*') ||
        line.trim().startsWith('*') ||
        line.trim().startsWith('@') ||
        line.trim().startsWith('#preview-frame') ||
        line.trim() === '' ||
        line.trim() === '}' ||
        !line.includes('{')
      ) {
        scopedLines.push(line);
        continue;
      }

      // Check if this line contains a selector (has { but isn't already scoped)
      if (line.includes('{') && !line.trim().startsWith('#preview-frame')) {
        // Split selector from properties
        const braceIndex = line.indexOf('{');
        const selector = line.substring(0, braceIndex).trim();
        const rest = line.substring(braceIndex);

        // Skip if selector is a variable definition block or already scoped
        if (selector === '#preview-frame' || selector.startsWith('#preview-frame ')) {
          scopedLines.push(line);
          continue;
        }

        // Handle multiple selectors separated by commas
        const selectors = selector.split(',').map(s => s.trim());
        const scopedSelectors = selectors.map(s => {
          // Skip if already scoped or is :root/html (already handled)
          if (s.startsWith('#preview-frame') || s === ':root' || s === 'html') {
            return s;
          }
          return `#preview-frame ${s}`;
        });

        line = scopedSelectors.join(',\n') + ' ' + rest;
      }

      scopedLines.push(line);
    }

    return scopedLines.join('\n');
  }

  // Generate CSS from current data
  generateCSS() {
    // Generate CSS with branding overrides only (theme CSS is loaded separately)
    // Using standardized --theme- CSS variable naming convention:
    // - colors → --theme-color-{key}
    // - typography → --theme-{key} (keys already have font-, line-height- prefix)
    // - spacing → --theme-space-{key}
    // - borders → --theme-{key} (keys already have radius-, width- prefix)
    // - shadows → --theme-shadow-{key}
    // - animations → --theme-transition-{key}
    let css = '/* Branding Customizations */\n#preview-frame {\n';

    // Colors → --theme-color-{key}
    Object.keys(this.mergedData.colors || {}).forEach(key => {
      const value = this.mergedData.colors[key];
      if (value) {
        css += `    --theme-color-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Typography → --theme-{key} (keys already have font-, line-height- prefix)
    Object.keys(this.mergedData.typography || {}).forEach(key => {
      const value = this.mergedData.typography[key];
      if (value) {
        css += `    --theme-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Spacing → --theme-space-{key}
    Object.keys(this.mergedData.spacing || {}).forEach(key => {
      const value = this.mergedData.spacing[key];
      if (value) {
        css += `    --theme-space-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Borders → --theme-{key} (keys already have radius-, width- prefix)
    Object.keys(this.mergedData.borders || {}).forEach(key => {
      const value = this.mergedData.borders[key];
      if (value) {
        css += `    --theme-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Shadows → --theme-shadow-{key}
    Object.keys(this.mergedData.shadows || {}).forEach(key => {
      const value = this.mergedData.shadows[key];
      if (value) {
        css += `    --theme-shadow-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Animations/Transitions → --theme-transition-{key}
    Object.keys(this.mergedData.animations || {}).forEach(key => {
      const value = this.mergedData.animations[key];
      if (value) {
        css += `    --theme-transition-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Transitions → --theme-transition-{key}
    Object.keys(this.mergedData.transitions || {}).forEach(key => {
      const value = this.mergedData.transitions[key];
      if (value) {
        css += `    --theme-transition-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Header → --theme-header-{key}
    Object.keys(this.mergedData.header || {}).forEach(key => {
      const value = this.mergedData.header[key];
      if (value) {
        css += `    --theme-header-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Footer → --theme-footer-{key}
    Object.keys(this.mergedData.footer || {}).forEach(key => {
      const value = this.mergedData.footer[key];
      if (value) {
        css += `    --theme-footer-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Menu → --theme-menu-{key}
    Object.keys(this.mergedData.menu || {}).forEach(key => {
      const value = this.mergedData.menu[key];
      if (value) {
        css += `    --theme-menu-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Search → --theme-search-{key}
    Object.keys(this.mergedData.search || {}).forEach(key => {
      const value = this.mergedData.search[key];
      if (value) {
        css += `    --theme-search-${key.replace(/_/g, '-')}: ${value};\n`;
      }
    });

    // Elements → --theme-element-{category}-{key}
    this.generateElementsCSS(this.mergedData.elements || {}, '', (varName, value) => {
      css += `    ${varName}: ${value};\n`;
    });

    css += '}\n';

    // Apply typography variables to actual elements
    css += '\n/* Typography Application */\n';

    // Body typography - ONLY apply if customized in branding (not from theme defaults)
    // Typography property descriptor array for DRY generation
    const typographyProps = [
      { dataKey: 'font_family', cssKey: 'font-family' },
      { dataKey: 'font_size', cssKey: 'font-size' },
      { dataKey: 'font_weight', cssKey: 'font-weight' },
      { dataKey: 'font_style', cssKey: 'font-style' },
      { dataKey: 'line_height', cssKey: 'line-height' },
      { dataKey: 'letter_spacing', cssKey: 'letter-spacing' },
      { dataKey: 'word_spacing', cssKey: 'word-spacing' },
      { dataKey: 'text_transform', cssKey: 'text-transform' },
      { dataKey: 'text_align', cssKey: 'text-align' },
      { dataKey: 'text_decoration', cssKey: 'text-decoration' },
      { dataKey: 'text_decoration_style', cssKey: 'text-decoration-style' },
      { dataKey: 'text_indent', cssKey: 'text-indent' },
      { dataKey: 'font_variant', cssKey: 'font-variant' },
    ];

    if (this.brandingData.typography && Object.keys(this.brandingData.typography).length > 0) {
      // Body typography
      const bodyProps = typographyProps
        .filter(({ dataKey }) => this.brandingData.typography[`${dataKey}_body`])
        .map(
          ({ dataKey, cssKey }) =>
            `    ${cssKey}: ${this.brandingData.typography[`${dataKey}_body`]} !important;`
        );

      if (bodyProps.length > 0) {
        css += '#preview-frame, #preview-frame body {\n';
        css += bodyProps.join('\n') + '\n';
        // Note: color_body is handled via CSS variables (--theme-element-body-color) in elements section
        css += '}\n';
      }

      // Individual heading typography (H1-H6)
      ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].forEach(heading => {
        const headingProps = typographyProps
          .filter(({ dataKey }) => this.brandingData.typography[`${dataKey}_${heading}`])
          .map(
            ({ dataKey, cssKey }) =>
              `    ${cssKey}: ${this.brandingData.typography[`${dataKey}_${heading}`]} !important;`
          );

        if (headingProps.length > 0) {
          css += `#preview-frame ${heading}, #preview-frame .${heading}-text {\n`;
          css += headingProps.join('\n') + '\n';
          // Note: color_${heading} is handled via CSS variables (--theme-element-heading-*-color) in elements section
          css += '}\n';
        }
      });
    }

    // Add scoped custom CSS
    if (this.brandingData.custom_css) {
      // Scope custom CSS to preview frame as well
      const scopedCustomCSS = this.brandingData.custom_css
        .split('\n')
        .map(line => {
          // Add #preview-frame prefix to selectors (basic implementation)
          if (
            line.trim() &&
            !line.trim().startsWith('/*') &&
            !line.trim().startsWith('*') &&
            line.includes('{')
          ) {
            return `#preview-frame ${line}`;
          }
          return line;
        })
        .join('\n');
      css += '\n' + scopedCustomCSS;
    }

    return css;
  }

  // Save/Load/Export functions
  async saveBranding() {
    this.showSavingIndicator();

    try {
      const response = await fetch(this.urls.save, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.csrfToken,
        },
        body: JSON.stringify(this.brandingData),
      });

      const data = await response.json();

      if (data.success) {
        this.hideSavingIndicator();
        this.showSuccess(data.message);

        if (data.redirect_url) {
          setTimeout(() => {
            window.location.href = data.redirect_url;
          }, 1000);
        }
      } else {
        this.showError(data.error);
      }
    } catch (error) {
      console.error('Save error:', error);
      this.showError(this.translations.error || 'Error saving branding');
    }
  }

  async autoSave() {
    // Auto-save the entire branding data to server
    try {
      const response = await fetch(this.urls.save, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.csrfToken,
        },
        body: JSON.stringify(this.brandingData),
      });

      const data = await response.json();

      if (!data.success) {
        console.error('Auto-save failed:', data.error);
      } else {
        console.log('Auto-saved successfully');
      }
    } catch (error) {
      console.error('Auto-save error:', error);
    }
  }

  async exportBranding() {
    window.location.href = this.urls.export;
  }

  importBranding() {
    const fileInput = document.getElementById('import-file');
    fileInput.click();

    fileInput.addEventListener('change', async e => {
      const file = e.target.files[0];
      if (!file) return;

      if (!(await AdminModal.confirm(this.translations.confirmImport))) {
        return;
      }

      const formData = new FormData();
      formData.append('import_file', file);

      try {
        const response = await fetch(this.urls.import, {
          method: 'POST',
          headers: {
            'X-CSRFToken': this.csrfToken,
          },
          body: formData,
        });

        const data = await response.json();

        if (data.success) {
          this.showSuccess(data.message);
          setTimeout(() => {
            window.location.reload();
          }, 1000);
        } else {
          this.showError(data.error);
        }
      } catch (error) {
        console.error('Import error:', error);
        this.showError(this.translations.error || 'Error importing branding');
      }
    });
  }

  refreshPreview() {
    // Regenerate and apply CSS
    this.updatePreviewFrame();
    // Optionally reload preview content
    this.loadPreviewContent();
  }

  // Helper method to generate inline typography styles for preview elements
  getTypographyInlineStyles(type) {
    // Get typography values from merged data (theme + branding)
    const typography = this.mergedData.typography || {};
    const styles = [];

    // Debug: Log typography data for first heading to understand structure
    if (type === 'h1' && Object.keys(typography).length > 0) {
      console.log(
        'Typography data sample:',
        Object.keys(typography)
          .filter(k => k.includes('h1') || k.includes('body'))
          .slice(0, 10)
      );
    }

    // Try both underscore and hyphen formats for compatibility
    const fontFamily = typography[`font_family_${type}`] || typography[`font-family-${type}`];
    const fontSize = typography[`font_size_${type}`] || typography[`font-size-${type}`];
    const fontWeight = typography[`font_weight_${type}`] || typography[`font-weight-${type}`];
    const fontStyle = typography[`font_style_${type}`] || typography[`font-style-${type}`];
    const lineHeight = typography[`line_height_${type}`] || typography[`line-height-${type}`];

    // Build inline style string with CSS variables and fallbacks
    // Uses standardized naming: --font-{property}-{type}, --line-height-{type}
    if (fontFamily) {
      styles.push(`font-family: var(--theme-font-family-${type}, ${fontFamily})`);
    }
    if (fontSize) {
      styles.push(`font-size: var(--theme-font-size-${type}, ${fontSize})`);
    }
    if (fontWeight) {
      styles.push(`font-weight: var(--theme-font-weight-${type}, ${fontWeight})`);
    }
    if (fontStyle) {
      styles.push(`font-style: var(--theme-font-style-${type}, ${fontStyle})`);
    }
    if (lineHeight) {
      styles.push(`line-height: var(--theme-line-height-${type}, ${lineHeight})`);
    }

    // Always add color for visibility
    const textColor = this.mergedData.colors?.text || '#1F2937';
    styles.push(`color: var(--theme-color-text, ${textColor})`);

    return styles.join('; ');
  }

  loadPreviewContent() {
    const previewFrame = document.getElementById('preview-frame');
    if (!previewFrame) return;

    // Get effective color values from merged data
    const colors = this.mergedData.colors || {};

    // Create preview HTML content with inline styles using actual color values
    const previewHTML = `
            <div class="canvas-preview-content">
                <!-- Basic Colors Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Basic Colors</h3>
                    <div class="canvas-preview-color-swatches">
                        <div class="canvas-preview-color-swatch swatch-primary" style="background: var(--theme-color-primary, ${colors.primary || '#3B82F6'});">
                            <span>Primary</span>
                        </div>
                        <div class="canvas-preview-color-swatch swatch-secondary" style="background: var(--theme-color-secondary, ${colors.secondary || '#8B5CF6'});">
                            <span>Secondary</span>
                        </div>
                        <div class="canvas-preview-color-swatch swatch-accent" style="background: var(--theme-color-accent, ${colors.accent || '#EC4899'});">
                            <span>Accent</span>
                        </div>
                        <div class="canvas-preview-color-swatch swatch-success" style="background: var(--theme-color-success, ${colors.success || '#10b981'});">
                            <span>Success</span>
                        </div>
                        <div class="canvas-preview-color-swatch swatch-warning" style="background: var(--theme-color-warning, ${colors.warning || '#f59e0b'});">
                            <span>Warning</span>
                        </div>
                        <div class="canvas-preview-color-swatch swatch-error" style="background: var(--theme-color-error, ${colors.error || '#ef4444'});">
                            <span>Error</span>
                        </div>
                    </div>
                </section>

                <!-- Color Variants Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Color Variants</h3>

                    <!-- Primary Color Family -->
                    <p style="font-size: 0.7rem; color: var(--theme-color-text-muted, #6b7280); margin-bottom: 0.5rem; margin-top: 0;">Primary</p>
                    <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 1rem;">
                        <div style="background: var(--theme-color-primary-dark, ${colors['primary-dark'] || '#1e40af'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">dark</small>
                        </div>
                        <div style="background: var(--theme-color-primary, ${colors.primary || '#3B82F6'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">base</small>
                        </div>
                        <div style="background: var(--theme-color-primary-hover, ${colors['primary-hover'] || '#2563eb'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">hover</small>
                        </div>
                        <div style="background: var(--theme-color-primary-light, ${colors['primary-light'] || '#dbeafe'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">light</small>
                        </div>
                    </div>

                    <!-- Secondary Color Family -->
                    <p style="font-size: 0.7rem; color: var(--theme-color-text-muted, #6b7280); margin-bottom: 0.5rem; margin-top: 0;">Secondary</p>
                    <div style="display: flex; gap: 0.5rem; align-items: center; margin-bottom: 1rem;">
                        <div style="background: var(--theme-color-secondary-dark, ${colors['secondary-dark'] || '#334155'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">dark</small>
                        </div>
                        <div style="background: var(--theme-color-secondary, ${colors.secondary || '#64748B'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">base</small>
                        </div>
                        <div style="background: var(--theme-color-secondary-hover, ${colors['secondary-hover'] || '#475569'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">hover</small>
                        </div>
                        <div style="background: var(--theme-color-secondary-light, ${colors['secondary-light'] || '#f1f5f9'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">light</small>
                        </div>
                    </div>

                    <!-- Accent Color Family -->
                    <p style="font-size: 0.7rem; color: var(--theme-color-text-muted, #6b7280); margin-bottom: 0.5rem; margin-top: 0;">Accent</p>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <div style="background: var(--theme-color-accent-dark, ${colors['accent-dark'] || '#a16207'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">dark</small>
                        </div>
                        <div style="background: var(--theme-color-accent, ${colors.accent || '#F59E0B'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">base</small>
                        </div>
                        <div style="background: var(--theme-color-accent-hover, ${colors['accent-hover'] || '#d97706'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">hover</small>
                        </div>
                        <div style="background: var(--theme-color-accent-light, ${colors['accent-light'] || '#fef3c7'}); padding: 0.75rem 1rem; border-radius: 0.25rem; flex: 1; text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">light</small>
                        </div>
                    </div>
                </section>

                <!-- Typography & Text Variants Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Typography Hierarchy</h3>
                    <h1 id="preview-h1" class="canvas-preview-heading">H1 - Main Page Heading</h1>
                    <h2 id="preview-h2" class="canvas-preview-heading">H2 - Section Heading</h2>
                    <h3 id="preview-h3" class="canvas-preview-heading">H3 - Subsection Heading</h3>
                    <h4 id="preview-h4" class="canvas-preview-heading">H4 - Minor Heading</h4>
                    <h5 id="preview-h5" class="canvas-preview-heading">H5 - Small Heading</h5>
                    <h6 id="preview-h6" class="canvas-preview-heading">H6 - Smallest Heading</h6>
                    <p id="preview-body" class="canvas-preview-body" style="margin-top: 1rem;">
                        Body text: This is the main body text used throughout the interface. Each heading level above can be individually customized with different fonts, sizes, weights, and styles.
                    </p>
                </section>

                <!-- Text Color Variants Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Text Color Variants</h3>
                    <p class="canvas-preview-body">
                        Primary text (text): Main body text color used throughout the interface.
                    </p>
                    <p class="canvas-preview-body-light">
                        Light text (text-light): Secondary content and less prominent information.
                    </p>
                    <p class="canvas-preview-body-muted">
                        Muted text (text-muted): Hints, placeholders, and disabled states.
                    </p>
                    <div style="background: var(--theme-color-primary, ${colors.primary || '#3B82F6'}); padding: 1rem; border-radius: 0.25rem; margin-top: 0.5rem;">
                        <p style="color: var(--theme-color-text-inverse, ${colors['text-inverse'] || '#FFFFFF'}); margin: 0;">
                            Inverse text (text-inverse): Used on colored backgrounds for contrast.
                        </p>
                    </div>
                </section>

                <!-- Header Preview Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Header</h3>
                    <div id="preview-header" style="
                        background: var(--theme-header-background, ${colors['header-bg'] || '#FFFFFF'});
                        border-bottom: 1px solid var(--theme-header-border-color, var(--theme-color-border, #E5E7EB));
                        padding: var(--theme-header-padding-y, 1rem) var(--theme-header-padding-x, 1rem);
                        display: flex;
                        align-items: center;
                        gap: 1.5rem;
                        border-radius: 0.25rem;">
                        <span style="color: var(--theme-header-text-color, ${colors.text || '#1F2937'}); font-weight: 600;">Header Text</span>
                        <a href="#" onclick="return false;" style="color: var(--theme-header-link-color, ${colors.primary || '#3B82F6'}); text-decoration: none;">Link</a>
                        <a href="#" onclick="return false;" style="color: var(--theme-header-link-hover-color, ${colors['primary-hover'] || '#2563eb'}); text-decoration: none; border-bottom: 2px solid currentColor;">Hover Link</a>
                    </div>
                </section>

                <!-- Footer Preview Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Footer</h3>
                    <div id="preview-footer" style="
                        background: var(--theme-footer-background, ${colors['footer-bg'] || '#1F2937'});
                        border-top: 1px solid var(--theme-footer-border-color, var(--theme-color-border, #374151));
                        padding: var(--theme-footer-padding-top, 1.5rem) 1rem var(--theme-footer-padding-bottom, 1rem);
                        border-radius: 0.25rem;">
                        <h4 style="color: var(--theme-footer-heading-color, ${colors['text-inverse'] || '#FFFFFF'}); margin: 0 0 0.5rem 0; font-size: 1rem;">Footer Heading</h4>
                        <p style="color: var(--theme-footer-text-color, ${colors['text-inverse'] || '#D1D5DB'}); margin: 0 0 0.5rem 0; font-size: 0.875rem;">Footer text content</p>
                        <a href="#" onclick="return false;" style="color: var(--theme-footer-link-color, ${colors['primary-light'] || '#93C5FD'}); text-decoration: none; font-size: 0.875rem;">Footer Link</a>
                        <a href="#" onclick="return false;" style="color: var(--theme-footer-link-hover-color, ${colors['accent'] || '#F59E0B'}); text-decoration: underline; margin-left: 1rem; font-size: 0.875rem;">Hover Link</a>
                    </div>
                </section>

                <!-- Menu Preview Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Navigation Menu</h3>
                    <nav id="preview-menu" style="
                        background: var(--theme-menu-background, transparent);
                        font-size: var(--theme-menu-font-size, 0.9rem);
                        font-weight: var(--theme-menu-font-weight, 500);
                        display: flex;
                        gap: 0.25rem;
                        align-items: center;
                        padding: 0.5rem;
                        border: 1px solid var(--theme-color-border, #E5E7EB);
                        border-radius: 0.25rem;">
                        <span style="
                            color: var(--theme-menu-text-color, ${colors.text || '#1F2937'});
                            padding: 0.5rem 1rem;
                            border-radius: 0.25rem;">Menu Item</span>
                        <span style="
                            color: var(--theme-menu-text-hover-color, ${colors.primary || '#3B82F6'});
                            background: var(--theme-menu-background-hover, ${colors['surface-variant'] || '#F3F4F6'});
                            padding: 0.5rem 1rem;
                            border-radius: 0.25rem;">Hover State</span>
                        <div style="
                            background: var(--theme-menu-dropdown-background, ${colors.surface || '#FFFFFF'});
                            box-shadow: var(--theme-menu-dropdown-shadow, 0 4px 6px -1px rgba(0, 0, 0, 0.1));
                            padding: 0.5rem 1rem;
                            border-radius: 0.25rem;
                            margin-left: 0.5rem;
                            font-size: 0.85rem;
                            color: var(--theme-menu-text-color, ${colors.text || '#1F2937'});">
                            Dropdown Menu
                        </div>
                    </nav>
                </section>

                <!-- Surface & Background Variants Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Surfaces & Backgrounds</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-bottom: 1rem;">
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); border: 1px solid var(--theme-color-border, ${colors.border || '#E5E7EB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">surface</small>
                        </div>
                        <div style="background: var(--theme-color-surface-secondary, ${colors['surface-secondary'] || '#F9FAFB'}); border: 1px solid var(--theme-color-border, ${colors.border || '#E5E7EB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">surface-secondary</small>
                        </div>
                        <div style="background: var(--theme-color-surface-variant, ${colors['surface-variant'] || '#F3F4F6'}); border: 1px solid var(--theme-color-border, ${colors.border || '#E5E7EB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">surface-variant</small>
                        </div>
                        <div style="background: var(--theme-color-surface-dark, ${colors['surface-dark'] || '#E5E7EB'}); border: 1px solid var(--theme-color-border, ${colors.border || '#E5E7EB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">surface-dark</small>
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem;">
                        <div style="background: var(--theme-color-background, ${colors.background || '#FFFFFF'}); border: 1px solid var(--theme-color-border, ${colors.border || '#E5E7EB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">background</small>
                        </div>
                        <div style="background: var(--theme-color-background-secondary, ${colors['background-secondary'] || '#F9FAFB'}); border: 1px solid var(--theme-color-border, ${colors.border || '#E5E7EB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">background-secondary</small>
                        </div>
                        <div style="background: var(--theme-color-background-tertiary, ${colors['background-tertiary'] || '#F3F4F6'}); border: 1px solid var(--theme-color-border, ${colors.border || '#E5E7EB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">background-tertiary</small>
                        </div>
                    </div>
                </section>

                <!-- Border Variants Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Border Variants</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem;">
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); border: 2px solid var(--theme-color-border-light, ${colors['border-light'] || '#F3F4F6'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="color: var(--theme-color-text-muted, ${colors['text-muted'] || '#9CA3AF'});">border-light</small>
                        </div>
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); border: 2px solid var(--theme-color-border, ${colors.border || '#E5E7EB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="color: var(--theme-color-text-muted, ${colors['text-muted'] || '#9CA3AF'});">border</small>
                        </div>
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); border: 2px solid var(--theme-color-border-dark, ${colors['border-dark'] || '#D1D5DB'}); padding: 0.75rem; border-radius: 0.25rem;">
                            <small style="color: var(--theme-color-text-muted, ${colors['text-muted'] || '#9CA3AF'});">border-dark</small>
                        </div>
                    </div>
                </section>

                <!-- Buttons Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Buttons</h3>
                    <p style="font-size: 0.75rem; color: var(--theme-color-text-muted, #6b7280); margin-bottom: 0.75rem;">Solid Variants</p>
                    <div class="canvas-preview-button-group">
                        <button class="canvas-preview-btn btn-primary">Primary</button>
                        <button class="canvas-preview-btn btn-secondary">Secondary</button>
                        <button class="canvas-preview-btn btn-neutral">Neutral</button>
                        <button class="canvas-preview-btn btn-danger">Danger</button>
                    </div>
                    <p style="font-size: 0.75rem; color: var(--theme-color-text-muted, #6b7280); margin-bottom: 0.75rem;">Outline Variants</p>
                    <div class="canvas-preview-button-group">
                        <button class="canvas-preview-btn btn-primary-outline">Primary</button>
                        <button class="canvas-preview-btn btn-secondary-outline">Secondary</button>
                        <button class="canvas-preview-btn btn-neutral-outline">Neutral</button>
                        <button class="canvas-preview-btn btn-danger-outline">Danger</button>
                    </div>
                    <p style="font-size: 0.75rem; color: var(--theme-color-text-muted, #6b7280); margin-bottom: 0.75rem;">Ghost Variants</p>
                    <div class="canvas-preview-button-group">
                        <button class="canvas-preview-btn btn-primary-ghost">Primary</button>
                        <button class="canvas-preview-btn btn-secondary-ghost">Secondary</button>
                        <button class="canvas-preview-btn btn-neutral-ghost">Neutral</button>
                        <button class="canvas-preview-btn btn-danger-ghost">Danger</button>
                    </div>
                </section>

                <!-- Cards Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Card Styles</h3>
                    <div class="canvas-preview-card-grid">
                        <!-- Default Card -->
                        <div class="canvas-preview-card card-default">
                            <h4 class="canvas-preview-card-title">Default</h4>
                            <p class="canvas-preview-card-content">Subtle shadow with elevation on hover.</p>
                            <span class="canvas-preview-card-meta">Card meta text</span>
                        </div>
                        <!-- Elevated Card -->
                        <div class="canvas-preview-card card-elevated">
                            <h4 class="canvas-preview-card-title">Elevated</h4>
                            <p class="canvas-preview-card-content">Prominent shadow from start.</p>
                            <span class="canvas-preview-card-meta">Card meta text</span>
                        </div>
                        <!-- Bordered Card -->
                        <div class="canvas-preview-card card-bordered">
                            <h4 class="canvas-preview-card-title">Bordered</h4>
                            <p class="canvas-preview-card-content">Visible border, no shadow.</p>
                            <span class="canvas-preview-card-meta">Card meta text</span>
                        </div>
                        <!-- Minimal Card -->
                        <div class="canvas-preview-card card-minimal">
                            <h4 class="canvas-preview-card-title">Minimal</h4>
                            <p class="canvas-preview-card-content">No background, border, or shadow.</p>
                            <span class="canvas-preview-card-meta">Card meta text</span>
                        </div>
                    </div>
                </section>

                <!-- Alerts Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Alerts</h3>
                    <div class="canvas-preview-alert alert-success">Success: Your changes have been saved.</div>
                    <div class="canvas-preview-alert alert-info">Info: New features are available.</div>
                    <div class="canvas-preview-alert alert-warning">Warning: Please review before continuing.</div>
                    <div class="canvas-preview-alert alert-error">Error: Something went wrong.</div>
                </section>

                <!-- Effects Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Shadows</h3>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); padding: 1rem; border-radius: 0.5rem; box-shadow: var(--theme-shadow-sm, 0 1px 2px 0 rgba(0, 0, 0, 0.05)); text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">sm</small>
                        </div>
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); padding: 1rem; border-radius: 0.5rem; box-shadow: var(--theme-shadow-base, 0 1px 3px 0 rgba(0, 0, 0, 0.1)); text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">base</small>
                        </div>
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); padding: 1rem; border-radius: 0.5rem; box-shadow: var(--theme-shadow-md, 0 4px 6px -1px rgba(0, 0, 0, 0.1)); text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">md</small>
                        </div>
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); padding: 1rem; border-radius: 0.5rem; box-shadow: var(--theme-shadow-lg, 0 10px 15px -3px rgba(0, 0, 0, 0.1)); text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">lg</small>
                        </div>
                        <div style="background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); padding: 1rem; border-radius: 0.5rem; box-shadow: var(--theme-shadow-xl, 0 20px 25px -5px rgba(0, 0, 0, 0.1)); text-align: center;">
                            <small style="background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">xl</small>
                        </div>
                        <div style="position: relative; background: var(--theme-color-surface, ${colors.surface || '#FFFFFF'}); padding: 1rem; border-radius: 0.5rem; overflow: hidden; text-align: center;">
                            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: var(--theme-color-overlay, ${colors.overlay || 'rgba(0, 0, 0, 0.5)'});"></div>
                            <small style="position: relative; z-index: 1; background: rgba(255,255,255,0.9); padding: 2px 6px; border-radius: 4px; color: #1f2937;">overlay</small>
                        </div>
                    </div>
                </section>

                <!-- Form Elements Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Form Elements</h3>
                    <div style="display: grid; gap: 1rem;">
                        <!-- Label and Input -->
                        <div>
                            <label class="canvas-preview-form-label">Email Address</label>
                            <input type="email" class="canvas-preview-form-input" placeholder="you@example.com">
                        </div>

                        <!-- Input with Focus State (simulated) -->
                        <div>
                            <label class="canvas-preview-form-label">Focused Input</label>
                            <input type="text" class="canvas-preview-form-input canvas-preview-form-input--focus" value="Focused state" readonly>
                        </div>

                        <!-- Input with Error State -->
                        <div>
                            <label class="canvas-preview-form-label">Password <span style="color: var(--theme-element-form-error-color, var(--theme-color-error, #ef4444));">*</span></label>
                            <input type="password" class="canvas-preview-form-input canvas-preview-form-input--error" value="short" readonly>
                            <p class="canvas-preview-form-error">Password must be at least 8 characters</p>
                        </div>

                        <!-- Select Dropdown -->
                        <div>
                            <label class="canvas-preview-form-label">Country</label>
                            <select class="canvas-preview-form-select">
                                <option>Select a country</option>
                                <option>Antarctica</option>
                                <option>North Pole</option>
                            </select>
                        </div>

                        <!-- Textarea -->
                        <div>
                            <label class="canvas-preview-form-label">Message</label>
                            <textarea class="canvas-preview-form-textarea" placeholder="Enter your message..." rows="3"></textarea>
                        </div>

                        <!-- Checkbox and Radio -->
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                            <div>
                                <p class="canvas-preview-form-label" style="margin-bottom: 0.5rem;">Preferences</p>
                                <label class="canvas-preview-form-checkbox">
                                    <input type="checkbox" checked>
                                    <span>Email notifications</span>
                                </label>
                                <label class="canvas-preview-form-checkbox">
                                    <input type="checkbox">
                                    <span>SMS notifications</span>
                                </label>
                            </div>
                            <div>
                                <p class="canvas-preview-form-label" style="margin-bottom: 0.5rem;">Shipping</p>
                                <label class="canvas-preview-form-radio">
                                    <input type="radio" name="shipping" checked>
                                    <span>Standard</span>
                                </label>
                                <label class="canvas-preview-form-radio">
                                    <input type="radio" name="shipping">
                                    <span>Express</span>
                                </label>
                            </div>
                        </div>

                        <!-- Help Text -->
                        <p class="canvas-preview-form-help">Help text provides additional context for form fields.</p>
                    </div>
                </section>

                <!-- Modal Preview Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Modal</h3>
                    <div class="canvas-preview-modal-container">
                        <!-- Simulated backdrop -->
                        <div class="canvas-preview-modal-backdrop"></div>

                        <!-- Modal dialog -->
                        <div class="canvas-preview-modal-dialog">
                            <!-- Close button -->
                            <button type="button" class="canvas-preview-modal-close" aria-label="Close">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <line x1="18" y1="6" x2="6" y2="18"></line>
                                    <line x1="6" y1="6" x2="18" y2="18"></line>
                                </svg>
                            </button>

                            <!-- Modal content -->
                            <div class="canvas-preview-modal-content">
                                <h4 class="canvas-preview-modal-title">Modal Title</h4>
                                <p class="canvas-preview-modal-body">This is a preview of how modals will appear with your theme settings. The background, border radius, shadow, and close button all use theme tokens.</p>
                                <div class="canvas-preview-modal-actions">
                                    <button class="canvas-preview-btn canvas-preview-btn--outline">Cancel</button>
                                    <button class="canvas-preview-btn canvas-preview-btn--primary">Confirm</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <!-- Search Preview Section -->
                <section class="canvas-preview-section">
                    <h3 class="canvas-preview-section-title">Search</h3>
                    <div class="canvas-preview-search-container">
                        <!-- Search bar with button -->
                        <div class="canvas-preview-search-bar">
                            <div class="canvas-preview-search-input-wrapper">
                                <svg class="canvas-preview-search-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                </svg>
                                <input type="text" class="canvas-preview-search-input" placeholder="Search products..." value="">
                            </div>
                            <button class="canvas-preview-search-btn">
                                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                </svg>
                            </button>
                        </div>

                        <!-- Simulated dropdown with results -->
                        <div class="canvas-preview-search-dropdown">
                            <div class="canvas-preview-search-results">
                                <div class="canvas-preview-search-result-item">
                                    <div class="canvas-preview-search-result-image"></div>
                                    <div class="canvas-preview-search-result-content">
                                        <span class="canvas-preview-search-result-title">Product Name</span>
                                        <span class="canvas-preview-search-result-price">$29.99</span>
                                    </div>
                                </div>
                                <div class="canvas-preview-search-result-item">
                                    <div class="canvas-preview-search-result-image"></div>
                                    <div class="canvas-preview-search-result-content">
                                        <span class="canvas-preview-search-result-title">Another Product</span>
                                        <span class="canvas-preview-search-result-price">$49.99</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        `;

    previewFrame.innerHTML = previewHTML;

    // Apply generated CSS to preview
    this.updatePreviewFrame();
  }

  // UI Helper functions
  showSavingIndicator() {
    const indicator = document.getElementById('auto-save-indicator');
    if (indicator) {
      indicator.style.display = 'inline-flex';
    }
  }

  hideSavingIndicator() {
    const indicator = document.getElementById('auto-save-indicator');
    if (indicator) {
      indicator.style.display = 'none';
    }
  }

  showSuccess(message) {
    // Implement success notification
    console.log('Success:', message);
  }

  showError(message) {
    // Implement error notification
    console.error('Error:', message);
    this.hideSavingIndicator();
  }

  // Reset property to theme default
  async resetToThemeDefault(section, property) {
    // Clear any pending auto-save timer to prevent race conditions
    clearTimeout(this.autoSaveTimer);

    // Remove the property from branding data
    if (this.brandingData[section]) {
      delete this.brandingData[section][property];

      // For typography, also reset related properties and element tokens
      if (section === 'typography' && property.startsWith('font_family_')) {
        const type = property.replace('font_family_', '');

        // Delete legacy typography keys
        delete this.brandingData[section][type];

        // Delete all related typography properties
        const relatedProps = [
          'size',
          'weight',
          'style',
          'line_height',
          'letter_spacing',
          'word_spacing',
          'text_transform',
          'text_align',
          'text_decoration',
          'text_decoration_style',
          'text_indent',
          'font_variant',
          'vertical_align',
        ];
        relatedProps.forEach(prop => {
          delete this.brandingData[section][`font_${prop}_${type}`];
          delete this.brandingData[section][`${prop}_${type}`];
        });

        // Also clean up element tokens (where fonts are now stored)
        this.cleanupElementTypographyTokens(type);
      }

      // Handle typography color reset - stored in elements section
      if (section === 'typography' && property.startsWith('color_')) {
        const colorTarget = property.replace('color_', '');
        this.cleanupElementColorTokens(colorTarget);

        // Clean up legacy colors section
        if (this.brandingData.colors?.[property]) {
          delete this.brandingData.colors[property];
        }
      }
    }

    // Update the merged data
    this.mergedData = this.mergeTokens();

    // Update the input field to show theme default
    let themeDefault = null;
    let inputId = null;

    if (section === 'colors') {
      themeDefault = this.themeData.colors?.[property] || '';
      inputId = `color-${property}`;
    } else if (section === 'typography') {
      // Typography colors are stored in elements, other props in typography
      if (property.startsWith('color_')) {
        const colorTarget = property.replace('color_', '');
        if (colorTarget === 'body') {
          themeDefault = this.themeData.elements?.body?.color || this.themeData.colors?.text || '';
        } else if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(colorTarget)) {
          themeDefault =
            this.themeData.elements?.heading?.[`${colorTarget}-color`] ||
            this.themeData.colors?.text ||
            '';
        }
        // Color input IDs: typography-color-body, typography-color-h1, etc.
        inputId = `typography-color-${colorTarget}`;
      } else if (property.startsWith('font_family_')) {
        themeDefault = this.themeData.typography?.[property] || '';
        const type = property.replace('font_family_', '');
        inputId = `font-${type}`;
      } else {
        themeDefault = this.themeData.typography?.[property] || '';
        inputId = property;
      }
    } else if (section === 'spacing') {
      themeDefault = this.themeData.spacing?.[property] || '';
      inputId = property;
    } else if (section === 'borders') {
      themeDefault = this.themeData.borders?.[property] || '';
      inputId = property;
    } else if (section === 'shadows') {
      themeDefault = this.themeData.shadows?.[property] || '';
      inputId = property;
    } else if (section === 'transitions') {
      themeDefault = this.themeData.transitions?.[property] || '';
      inputId = property;
    } else if (section === 'header') {
      themeDefault = this.themeData.header?.[property] || '';
      inputId = property;
    } else if (section === 'footer') {
      themeDefault = this.themeData.footer?.[property] || '';
      inputId = property;
    } else if (section === 'menu') {
      themeDefault = this.themeData.menu?.[property] || '';
      inputId = property;
    } else if (section === 'search') {
      themeDefault = this.themeData.search?.[property] || '';
      inputId = property;
    } else if (section === 'elements') {
      // Handle nested elements with dot notation
      themeDefault = this.getNestedValue(this.themeData.elements || {}, property) || '';
      inputId = property;
    } else if (section.startsWith('elements.')) {
      // Handle elements.form, elements.button, etc. section paths
      // Section is like 'elements.form', property is like 'input-bg'
      const elementPath = section.replace('elements.', '');
      const fullPath = `${elementPath}.${property}`;
      themeDefault = this.getNestedValue(this.themeData.elements || {}, fullPath) || '';

      // Remove from branding data - handle both nested and flat formats
      if (this.brandingData.elements) {
        // Try nested format first: elements.form['input-bg']
        const elementData = this.getNestedValue(this.brandingData.elements, elementPath);
        if (elementData && typeof elementData === 'object') {
          delete elementData[property];
          // Clean up empty parent objects
          if (Object.keys(elementData).length === 0) {
            delete this.brandingData.elements[elementPath];
          }
        }

        // Also delete flat format: elements['form-input-bg']
        const flatKey = `${elementPath}-${property}`;
        if (this.brandingData.elements[flatKey] !== undefined) {
          delete this.brandingData.elements[flatKey];
        }
      }

      // Re-merge tokens after deletion to update mergedData
      this.mergedData = this.mergeTokens();
    }

    // Try to find input by data-token attribute if not found by id
    let input = document.getElementById(inputId);
    if (!input && section) {
      let tokenPath;
      if (section === 'elements') {
        tokenPath = `elements.${property}`;
      } else if (section.startsWith('elements.')) {
        // For elements.form, elements.button paths
        tokenPath = `${section}.${property}`;
      } else {
        tokenPath = `${section}.${property}`;
      }
      input = document.querySelector(`[data-token="${tokenPath}"]`);
    }

    // Update the input field
    if (input) {
      if (themeDefault) {
        // Update the color input with proper styling
        if (section === 'colors') {
          input.value = themeDefault;
          // Apply color with theme default indicator
          this.applyColorToInput(input, themeDefault, false);
        }
        // Handle typography color input reset styling
        else if (section === 'typography' && property.startsWith('color_')) {
          // Resolve CSS variable to actual hex color for display
          const resolvedColor = this.resolveCssVariable(themeDefault) || themeDefault;
          input.value = resolvedColor;
          this.applyColorToInput(input, resolvedColor, false);
        }
        // Handle Layout section color inputs (header, footer, menu, search)
        else if (
          ['header', 'footer', 'menu', 'search'].includes(section) &&
          input.classList.contains('color-input')
        ) {
          // Resolve CSS variable to actual hex color for display
          const resolvedColor = this.resolveCssVariable(themeDefault) || themeDefault;
          input.value = resolvedColor;
          this.applyColorToInput(input, resolvedColor, false);
        }
        // Handle element color inputs (e.g., elements.form colors)
        else if (
          (section === 'elements' || section.startsWith('elements.')) &&
          input.classList.contains('color-input')
        ) {
          // Resolve CSS variable to actual hex color for display
          const resolvedColor = this.resolveCssVariable(themeDefault) || themeDefault;
          input.value = resolvedColor;
          this.applyColorToInput(input, resolvedColor, false);
        } else {
          // For non-color inputs, also resolve CSS variables
          const resolvedValue = this.resolveCssVariable(themeDefault) || themeDefault;
          input.value = resolvedValue;
        }
      } else {
        // No theme default, clear the field
        input.value = '';
        if (
          section === 'colors' ||
          (['header', 'footer', 'menu', 'search'].includes(section) &&
            input.classList.contains('color-input')) ||
          ((section === 'elements' || section.startsWith('elements.')) &&
            input.classList.contains('color-input'))
        ) {
          input.style.removeProperty('background-color');
          input.style.removeProperty('color');
          input.classList.remove('using-custom', 'using-theme-default');
        }
      }

      // Add temporary visual indicator that it was reset
      input.classList.add('using-default');

      // Remove the indicator after a short time
      setTimeout(() => {
        input.classList.remove('using-default');
      }, 2000);
    }

    // Refresh status indicator to show theme default or no value
    this.refreshPropertyStatus(section, property);

    // Update the preview
    this.updatePreviewFrame();

    // Clear the timer that sendUpdate might set
    clearTimeout(this.autoSaveTimer);

    // Save the complete state to the server
    try {
      this.showSavingIndicator();
      const response = await fetch(this.urls.save, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.csrfToken,
        },
        body: JSON.stringify(this.brandingData),
      });

      const data = await response.json();

      if (data.success) {
        this.showSuccess(`Reset ${property} to theme default`);
      } else {
        this.showError(`Failed to save reset: ${data.error}`);
      }
    } catch (error) {
      this.showError(`Failed to save reset: ${error.message}`);
    } finally {
      this.hideSavingIndicator();
    }
  }

  // Helper: Clean up element tokens for a typography type (body, h1-h6)
  cleanupElementTypographyTokens(type) {
    if (!this.brandingData.elements) return;

    const elementCategory = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(type) ? 'heading' : type;
    const prefix = elementCategory === 'heading' ? `${type}-` : '';

    if (this.brandingData.elements[elementCategory]) {
      // Delete all typography-related keys for this type
      const typographyKeys = [
        'font-family',
        'font-size',
        'font-weight',
        'font-style',
        'line-height',
        'letter-spacing',
        'word-spacing',
        'text-transform',
        'text-align',
        'text-decoration',
        'text-decoration-style',
        'text-indent',
        'vertical-align',
        'font-variant',
      ];

      typographyKeys.forEach(key => {
        delete this.brandingData.elements[elementCategory][`${prefix}${key}`];
      });

      // Clean up empty category
      if (Object.keys(this.brandingData.elements[elementCategory]).length === 0) {
        delete this.brandingData.elements[elementCategory];
      }
    }

    // Clean up empty elements object
    if (Object.keys(this.brandingData.elements).length === 0) {
      delete this.brandingData.elements;
    }
  }

  // Helper: Clean up element color tokens
  cleanupElementColorTokens(colorTarget) {
    if (!this.brandingData.elements) return;

    let elementCategory, elementKey, flatKey;

    if (['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].includes(colorTarget)) {
      elementCategory = 'heading';
      elementKey = `${colorTarget}-color`;
      flatKey = `heading-${colorTarget}-color`;
    } else if (colorTarget === 'body') {
      elementCategory = 'body';
      elementKey = 'color';
      flatKey = 'body-color';
    }

    // Delete nested format (e.g., elements.body.color)
    if (this.brandingData.elements[elementCategory]?.[elementKey]) {
      delete this.brandingData.elements[elementCategory][elementKey];

      // Clean up empty category
      if (Object.keys(this.brandingData.elements[elementCategory]).length === 0) {
        delete this.brandingData.elements[elementCategory];
      }
    }

    // Delete flat format for legacy cleanup (e.g., elements["body-color"])
    if (this.brandingData.elements[flatKey]) {
      delete this.brandingData.elements[flatKey];
    }

    // Clean up empty elements object
    if (Object.keys(this.brandingData.elements).length === 0) {
      delete this.brandingData.elements;
    }
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.brandingBuilder = new BrandingBuilder();

  // Make functions globally accessible
  window.openColorPicker = key => window.brandingBuilder.openColorPicker(key);
  window.openShadowEditor = key => window.brandingBuilder.openShadowEditor(key);
  window.saveBranding = () => window.brandingBuilder.saveBranding();
  window.exportBranding = () => window.brandingBuilder.exportBranding();
  window.importBranding = () => window.brandingBuilder.importBranding();
  window.refreshPreview = () => window.brandingBuilder.refreshPreview();
  window.resetToThemeDefault = (section, property) =>
    window.brandingBuilder.resetToThemeDefault(section, property);
});
