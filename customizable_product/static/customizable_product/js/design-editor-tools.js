/**
 * Design Editor - Tools Module
 * Implements text, image upload, clipart browser, template selector,
 * layers panel, feature toggles, and object ordering.
 *
 * Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0.
 */
(function () {
  'use strict';

  /* ─── State ──────────────────────────────────────────────────────────── */
  let dom = null;
  let state = null;
  let selectedObject = null;
  const clipartPage = 1;
  let clipartCategory = '';
  let clipartSearchTimer = null;

  /* ─── Initialization ─────────────────────────────────────────────────── */

  function init(sharedDom, sharedState) {
    dom = sharedDom;
    state = sharedState;

    // C1: Feature toggle enforcement - hide disabled tools
    enforceFeatureToggles();

    bindTextTool();
    bindImageTool();
    bindClipartTool();
    bindTemplateTool();
    populateFontSelector();
    bindDragAndDrop();
  }

  /* ─── C1: Feature Toggle Enforcement ──────────────────────────────────── */

  function enforceFeatureToggles() {
    if (!state || !state.config) return;
    const config = state.config;

    if (!config.allow_text) {
      hideToolTab('text');
    }
    if (!config.allow_image_upload) {
      hideToolTab('image');
    }
    if (!config.allow_clipart) {
      hideToolTab('clipart');
    }
  }

  function hideToolTab(toolName) {
    const tab = document.getElementById('tool-' + toolName);
    const panel = document.getElementById('panel-tool-' + toolName);
    if (tab) tab.style.display = 'none';
    if (panel) panel.style.display = 'none';
  }

  function showToolTab(toolName) {
    const tab = document.getElementById('tool-' + toolName);
    const panel = document.getElementById('panel-tool-' + toolName);
    if (tab) tab.style.display = '';
    if (panel) panel.style.display = '';
  }

  /**
   * Re-evaluate tool visibility based on the active surface's constraints.
   * Each surface may override the global config's allow_text/allow_image_upload/allow_clipart.
   * Called whenever the active surface changes.
   */
  function enforcePerSurfaceToggles() {
    if (!state || !state.surfaces || !state.surfaces.length) return;
    const surface = state.surfaces[state.activeSurfaceIndex];
    if (!surface) return;

    // Per-surface values are already resolved by the API (inherit logic applied server-side)
    const allowText =
      surface.allow_text !== undefined
        ? surface.allow_text
        : state.config && state.config.allow_text;
    const allowImage =
      surface.allow_image_upload !== undefined
        ? surface.allow_image_upload
        : state.config && state.config.allow_image_upload;
    const allowClipart =
      surface.allow_clipart !== undefined
        ? surface.allow_clipart
        : state.config && state.config.allow_clipart;

    if (allowText) showToolTab('text');
    else hideToolTab('text');
    if (allowImage) showToolTab('image');
    else hideToolTab('image');
    if (allowClipart) showToolTab('clipart');
    else hideToolTab('clipart');

    // If the currently active tool tab was hidden, switch to the first visible tab
    let activePanelHidden = false;
    const tabs = document.querySelectorAll('.design-editor__tool-tab');
    let firstVisibleTab = null;
    tabs.forEach(function (tab) {
      if (tab.style.display !== 'none') {
        if (!firstVisibleTab) firstVisibleTab = tab;
      }
      if (tab.classList.contains('active') && tab.style.display === 'none') {
        activePanelHidden = true;
      }
    });
    if (activePanelHidden && firstVisibleTab) {
      firstVisibleTab.click();
    }
  }

  /* ─── Text Tool ──────────────────────────────────────────────────────── */

  function bindTextTool() {
    const btnAddText = document.getElementById('btn-add-text');
    if (btnAddText) {
      btnAddText.addEventListener('click', addTextObject);
    }

    // Text property controls
    const propFontFamily = document.getElementById('prop-font-family');
    const propFontSize = document.getElementById('prop-font-size');
    const propFontColor = document.getElementById('prop-font-color');
    const propBold = document.getElementById('prop-bold');
    const propItalic = document.getElementById('prop-italic');
    const propAlignLeft = document.getElementById('prop-align-left');
    const propAlignCenter = document.getElementById('prop-align-center');
    const propAlignRight = document.getElementById('prop-align-right');
    const propStrokeColor = document.getElementById('prop-stroke-color');
    const propStrokeWidth = document.getElementById('prop-stroke-width');

    if (propFontFamily) {
      propFontFamily.addEventListener('change', function () {
        setTextProperty('fontFamily', this.value);
      });
    }
    if (propFontSize) {
      propFontSize.addEventListener('change', function () {
        setTextProperty('fontSize', parseInt(this.value, 10));
      });
    }
    if (propFontColor) {
      propFontColor.addEventListener('input', function () {
        setTextProperty('fill', this.value);
      });
    }
    if (propBold) {
      propBold.addEventListener('click', function () {
        toggleTextStyle('bold');
      });
    }
    if (propItalic) {
      propItalic.addEventListener('click', function () {
        toggleTextStyle('italic');
      });
    }
    if (propAlignLeft) {
      propAlignLeft.addEventListener('click', function () {
        setTextProperty('textAlign', 'left');
        updateAlignButtons('left');
      });
    }
    if (propAlignCenter) {
      propAlignCenter.addEventListener('click', function () {
        setTextProperty('textAlign', 'center');
        updateAlignButtons('center');
      });
    }
    if (propAlignRight) {
      propAlignRight.addEventListener('click', function () {
        setTextProperty('textAlign', 'right');
        updateAlignButtons('right');
      });
    }
    if (propStrokeColor) {
      propStrokeColor.addEventListener('input', function () {
        setTextProperty('stroke', this.value);
      });
    }
    if (propStrokeWidth) {
      propStrokeWidth.addEventListener('change', function () {
        setTextProperty('strokeWidth', parseFloat(this.value));
      });
    }
  }

  // C4: Use Textbox instead of IText for word wrapping support
  function addTextObject() {
    if (!window.DesignEditorCanvas) return;

    const canvas = window.DesignEditorCanvas.getCanvas();
    if (!canvas) return;

    const centerX = canvas.getWidth() / 2;
    const centerY = canvas.getHeight() / 2;
    const textWidth = Math.round(canvas.getWidth() * 0.6);

    const text = new fabric.Textbox('Your text here', {
      left: centerX,
      top: centerY,
      originX: 'center',
      originY: 'center',
      width: textWidth,
      fontSize: 24,
      fontFamily: getDefaultFont(),
      fill: '#000000',
      textAlign: 'center',
      custom_type: 'text',
    });

    window.DesignEditorCanvas.addObject(text);

    // Explicitly show text properties (safety net — canvas selection
    // events should also trigger this, but explicit call ensures it)
    if (window.DesignEditor) {
      window.DesignEditor.switchTool('text');
    }
    selectedObject = text;
    showTextProperties(text);
  }

  function setTextProperty(prop, value) {
    if (!selectedObject) return;
    if (selectedObject.type !== 'i-text' && selectedObject.type !== 'textbox') return;

    selectedObject.set(prop, value);

    const canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
    if (canvas) canvas.requestRenderAll();

    if (window.DesignEditorHistory) {
      window.DesignEditorHistory.recordState();
    }
  }

  function toggleTextStyle(style) {
    if (!selectedObject) return;

    if (style === 'bold') {
      const isBold = selectedObject.fontWeight === 'bold';
      selectedObject.set('fontWeight', isBold ? 'normal' : 'bold');
      const propBold = document.getElementById('prop-bold');
      if (propBold) propBold.classList.toggle('active', !isBold);
    } else if (style === 'italic') {
      const isItalic = selectedObject.fontStyle === 'italic';
      selectedObject.set('fontStyle', isItalic ? 'normal' : 'italic');
      const propItalic = document.getElementById('prop-italic');
      if (propItalic) propItalic.classList.toggle('active', !isItalic);
    }

    const canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
    if (canvas) canvas.requestRenderAll();

    if (window.DesignEditorHistory) {
      window.DesignEditorHistory.recordState();
    }
  }

  function updateAlignButtons(align) {
    ['left', 'center', 'right'].forEach(function (a) {
      const btn = document.getElementById('prop-align-' + a);
      if (btn) btn.classList.toggle('active', a === align);
    });
  }

  function populateFontSelector() {
    const select = document.getElementById('prop-font-family');
    if (!select) return;

    select.innerHTML = '';

    // System fonts first
    const systemFonts = [
      'Arial',
      'Helvetica',
      'Times New Roman',
      'Georgia',
      'Verdana',
      'Courier New',
    ];
    systemFonts.forEach(function (font) {
      const opt = document.createElement('option');
      opt.value = font;
      opt.textContent = font;
      select.appendChild(opt);
    });

    // Custom fonts from config
    if (state && state.fonts) {
      state.fonts.forEach(function (font) {
        const opt = document.createElement('option');
        opt.value = font.family;
        opt.textContent = font.name;
        select.appendChild(opt);
      });
    }
  }

  function getDefaultFont() {
    if (state && state.fonts && state.fonts.length > 0) {
      return state.fonts[0].family;
    }
    return 'Arial';
  }

  /* ─── Image Upload Tool ──────────────────────────────────────────────── */

  function bindImageTool() {
    const btnUpload = document.getElementById('btn-upload-image');
    const fileInput = document.getElementById('image-upload-input');

    if (btnUpload && fileInput) {
      btnUpload.addEventListener('click', function () {
        fileInput.click();
      });

      fileInput.addEventListener('change', function () {
        if (this.files && this.files.length > 0) {
          uploadImage(this.files[0]);
          this.value = ''; // Reset for same file re-upload
        }
      });
    }

    // Opacity control
    const propOpacity = document.getElementById('prop-opacity');
    if (propOpacity) {
      propOpacity.addEventListener('input', function () {
        if (selectedObject && selectedObject.type === 'image') {
          selectedObject.set('opacity', parseFloat(this.value));
          const canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
          if (canvas) canvas.requestRenderAll();
        }
      });
    }

    bindImageFilters();
  }

  /* ─── Image Filters ────────────────────────────────────────────────── */

  function getFilterValue(filters, filterType, prop, defaultVal) {
    for (let i = 0; i < filters.length; i++) {
      if (filters[i].type === filterType) return filters[i][prop];
    }
    return defaultVal;
  }

  function applyImageFilter(filterType, options) {
    if (!selectedObject || selectedObject.type !== 'image') return;

    // Remove existing filter of this type
    const filters = selectedObject.filters || [];
    selectedObject.filters = filters.filter(function (f) {
      return f.type !== filterType;
    });

    // Add new filter if non-default value
    if (options && options._active !== false) {
      const FilterClass = fabric.filters[filterType];
      if (FilterClass) {
        const filterOpts = {};
        for (const key in options) {
          if (key !== '_active') filterOpts[key] = options[key];
        }
        selectedObject.filters.push(new FilterClass(filterOpts));
      }
    }

    selectedObject.applyFilters();
    const canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
    if (canvas) canvas.requestRenderAll();
    if (window.DesignEditorHistory) window.DesignEditorHistory.recordState();
  }

  function setImageTransform(prop, value) {
    if (!selectedObject || selectedObject.type !== 'image') return;
    selectedObject.set(prop, value);
    selectedObject.setCoords();
    const canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
    if (canvas) canvas.requestRenderAll();
    if (window.DesignEditorHistory) window.DesignEditorHistory.recordState();
  }

  function bindImageFilters() {
    // Brightness
    const propBrightness = document.getElementById('prop-brightness');
    if (propBrightness) {
      propBrightness.addEventListener('input', function () {
        const val = parseFloat(this.value);
        applyImageFilter('Brightness', {
          brightness: val,
          _active: val !== 0,
        });
      });
    }

    // Contrast
    const propContrast = document.getElementById('prop-contrast');
    if (propContrast) {
      propContrast.addEventListener('input', function () {
        const val = parseFloat(this.value);
        applyImageFilter('Contrast', {
          contrast: val,
          _active: val !== 0,
        });
      });
    }

    // Saturation
    const propSaturation = document.getElementById('prop-saturation');
    if (propSaturation) {
      propSaturation.addEventListener('input', function () {
        const val = parseFloat(this.value);
        applyImageFilter('Saturation', {
          saturation: val,
          _active: val !== 0,
        });
      });
    }

    // Tint (BlendColor)
    const propTintColor = document.getElementById('prop-tint-color');
    const propTintAlpha = document.getElementById('prop-tint-alpha');
    function applyTint() {
      if (!propTintColor || !propTintAlpha) return;
      const alpha = parseFloat(propTintAlpha.value);
      applyImageFilter('BlendColor', {
        color: propTintColor.value,
        alpha: alpha,
        mode: 'tint',
        _active: alpha > 0,
      });
    }
    if (propTintColor) propTintColor.addEventListener('input', applyTint);
    if (propTintAlpha) propTintAlpha.addEventListener('input', applyTint);

    // Remove Color
    const propRemoveColor = document.getElementById('prop-remove-color');
    const propRemoveDistance = document.getElementById('prop-remove-distance');
    function applyRemoveColor() {
      if (!propRemoveColor || !propRemoveDistance) return;
      const distance = parseFloat(propRemoveDistance.value);
      applyImageFilter('RemoveColor', {
        color: propRemoveColor.value,
        distance: distance,
        _active: distance > 0,
      });
    }
    if (propRemoveColor) propRemoveColor.addEventListener('input', applyRemoveColor);
    if (propRemoveDistance) propRemoveDistance.addEventListener('input', applyRemoveColor);

    // Rotation (direct angle)
    const propRotation = document.getElementById('prop-rotation');
    if (propRotation) {
      propRotation.addEventListener('change', function () {
        setImageTransform('angle', parseFloat(this.value) || 0);
      });
    }

    // Rotate 90° CW
    const propRotateCW = document.getElementById('prop-rotate-cw');
    if (propRotateCW) {
      propRotateCW.addEventListener('click', function () {
        if (!selectedObject) return;
        const newAngle = ((selectedObject.angle || 0) + 90) % 360;
        setImageTransform('angle', newAngle);
        const el = document.getElementById('prop-rotation');
        if (el) el.value = Math.round(newAngle);
      });
    }

    // Rotate 90° CCW
    const propRotateCCW = document.getElementById('prop-rotate-ccw');
    if (propRotateCCW) {
      propRotateCCW.addEventListener('click', function () {
        if (!selectedObject) return;
        const newAngle = ((selectedObject.angle || 0) - 90 + 360) % 360;
        setImageTransform('angle', newAngle);
        const el = document.getElementById('prop-rotation');
        if (el) el.value = Math.round(newAngle);
      });
    }

    // Flip Horizontal
    const propFlipH = document.getElementById('prop-flip-h');
    if (propFlipH) {
      propFlipH.addEventListener('click', function () {
        if (!selectedObject) return;
        setImageTransform('flipX', !selectedObject.flipX);
      });
    }

    // Flip Vertical
    const propFlipV = document.getElementById('prop-flip-v');
    if (propFlipV) {
      propFlipV.addEventListener('click', function () {
        if (!selectedObject) return;
        setImageTransform('flipY', !selectedObject.flipY);
      });
    }
  }

  function uploadImage(file) {
    if (!window.DesignEditor) return;

    // Validate file size
    const maxSize = (state.config && state.config.max_upload_size_mb) || 10;
    if (file.size > maxSize * 1024 * 1024) {
      window.DesignEditor.showNotification(
        'File too large. Maximum size: ' + maxSize + 'MB',
        'error'
      );
      return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('product_id', state.productId);

    window.DesignEditor.apiRequest('upload-image/', {
      method: 'POST',
      body: formData,
    })
      .then(function (data) {
        if (data.url) {
          addImageToCanvas(data.url, data.asset_id);
        }
      })
      .catch(function (err) {
        console.error('[DesignEditorTools] Upload failed:', err);
        window.DesignEditor.showNotification('Failed to upload image', 'error');
      });
  }

  function addImageToCanvas(url, mediaAssetId) {
    if (!window.DesignEditorCanvas) return;

    const canvas = window.DesignEditorCanvas.getCanvas();
    if (!canvas) return;

    fabric.Image.fromURL(url, { crossOrigin: 'anonymous' }).then(function (img) {
      if (!img) return;

      // Scale image to fit within canvas bounds
      const canvasW = canvas.getWidth();
      const canvasH = canvas.getHeight();
      const maxDim = Math.min(canvasW, canvasH) * 0.6;

      let scale = 1;
      if (img.width > maxDim || img.height > maxDim) {
        scale = maxDim / Math.max(img.width, img.height);
      }

      img.set({
        left: canvasW / 2,
        top: canvasH / 2,
        originX: 'center',
        originY: 'center',
        scaleX: scale,
        scaleY: scale,
        custom_type: 'image',
        custom_media_asset_id: mediaAssetId || null,
      });

      window.DesignEditorCanvas.addObject(img);

      // C5: DPI Warning
      checkDpiWarning(img, scale);
    });
  }

  /* ─── C5: DPI Warning ────────────────────────────────────────────────── */

  function checkDpiWarning(img, scale) {
    if (!state || !state.surfaces || state.activeSurfaceIndex == null) return;
    const surface = state.surfaces[state.activeSurfaceIndex];
    if (!surface || !surface.width || !surface.height) return;
    if (surface.dimension_unit === 'px') return; // DPI only relevant for physical units

    // Convert physical dimensions to inches
    let widthInches, heightInches;
    if (surface.dimension_unit === 'mm') {
      widthInches = parseFloat(surface.width) / 25.4;
      heightInches = parseFloat(surface.height) / 25.4;
    } else {
      widthInches = parseFloat(surface.width);
      heightInches = parseFloat(surface.height);
    }

    // Calculate effective DPI for the image at its current scale
    const imgPixelWidth = img.width * scale;
    const imgPixelHeight = img.height * scale;
    const canvasW = window.DesignEditorCanvas
      ? window.DesignEditorCanvas.getCanvas().getWidth()
      : 500;
    const canvasH = window.DesignEditorCanvas
      ? window.DesignEditorCanvas.getCanvas().getHeight()
      : 500;

    // How much of the surface does the image cover?
    const coverageX = imgPixelWidth / canvasW;
    const coverageY = imgPixelHeight / canvasH;

    // Effective DPI = original pixels / (physical size of coverage area in inches)
    const effectiveDpiX = img.width / (widthInches * coverageX);
    const effectiveDpiY = img.height / (heightInches * coverageY);
    const effectiveDpi = Math.min(effectiveDpiX, effectiveDpiY);

    const minDpi = surface.min_dpi || 150;
    const recDpi = surface.recommended_dpi || 300;

    if (effectiveDpi < minDpi) {
      showDpiWarning(
        'Low resolution (' + Math.round(effectiveDpi) + ' DPI). Minimum: ' + minDpi + ' DPI',
        true
      );
    } else if (effectiveDpi < recDpi) {
      showDpiWarning(
        'Medium resolution (' + Math.round(effectiveDpi) + ' DPI). Recommended: ' + recDpi + ' DPI',
        false
      );
    }
  }

  function showDpiWarning(message, isCritical) {
    // Remove any existing warning
    const existing = document.querySelector('.design-editor__dpi-warning');
    if (existing) existing.remove();

    const viewport = document.getElementById('design-editor-viewport');
    if (!viewport) return;

    const warning = document.createElement('div');
    warning.className = 'design-editor__dpi-warning';
    if (isCritical) {
      warning.style.background = 'rgba(220, 38, 38, 0.9)';
    }
    warning.textContent = message;
    viewport.appendChild(warning);

    // Auto-remove after 6 seconds
    setTimeout(function () {
      if (warning.parentNode) warning.remove();
    }, 6000);
  }

  /* ─── C6: Drag-and-Drop Upload ───────────────────────────────────────── */

  function bindDragAndDrop() {
    const viewport = document.getElementById('design-editor-viewport');
    if (!viewport) return;

    viewport.addEventListener('dragover', function (e) {
      e.preventDefault();
      viewport.classList.add('design-editor__canvas-viewport--drag-over');
    });

    viewport.addEventListener('dragenter', function (e) {
      e.preventDefault();
      viewport.classList.add('design-editor__canvas-viewport--drag-over');
    });

    viewport.addEventListener('dragleave', function (e) {
      // Only remove if leaving the viewport
      if (!viewport.contains(e.relatedTarget)) {
        viewport.classList.remove('design-editor__canvas-viewport--drag-over');
      }
    });

    viewport.addEventListener('drop', function (e) {
      e.preventDefault();
      viewport.classList.remove('design-editor__canvas-viewport--drag-over');

      if (!state || !state.config || !state.config.allow_image_upload) return;

      const files = e.dataTransfer && e.dataTransfer.files;
      if (files && files.length > 0) {
        const file = files[0];
        // Validate it's an allowed raster image (no SVG - XSS risk)
        const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
        if (file.type && allowedTypes.indexOf(file.type) !== -1) {
          uploadImage(file);
        }
      }
    });
  }

  /* ─── Clipart Browser ────────────────────────────────────────────────── */

  function bindClipartTool() {
    renderClipartCategories();

    const searchInput = document.getElementById('clipart-search');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        clearTimeout(clipartSearchTimer);
        const query = this.value;
        clipartSearchTimer = setTimeout(function () {
          loadClipart(clipartCategory, query);
        }, 300);
      });
    }
  }

  function renderClipartCategories() {
    const container = document.getElementById('clipart-categories');
    if (!container || !state) return;

    container.innerHTML = '';

    // "All" button
    const allBtn = document.createElement('button');
    allBtn.type = 'button';
    allBtn.className = 'design-editor__clipart-cat-btn active';
    allBtn.textContent = 'All';
    allBtn.addEventListener('click', function () {
      clipartCategory = '';
      setActiveClipartCategory(allBtn);
      loadClipart('', '');
    });
    container.appendChild(allBtn);

    // Category buttons
    (state.clipartCategories || []).forEach(function (cat) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'design-editor__clipart-cat-btn';
      btn.textContent = cat.name;
      btn.addEventListener('click', function () {
        clipartCategory = cat.slug;
        setActiveClipartCategory(btn);
        loadClipart(cat.slug, '');
      });
      container.appendChild(btn);
    });

    // Load initial clipart
    loadClipart('', '');
  }

  function setActiveClipartCategory(activeBtn) {
    const container = document.getElementById('clipart-categories');
    if (!container) return;
    container.querySelectorAll('.design-editor__clipart-cat-btn').forEach(function (btn) {
      btn.classList.remove('active');
    });
    activeBtn.classList.add('active');
  }

  function loadClipart(category, search) {
    if (!window.DesignEditor) return;

    let url = 'clipart/?product_id=' + state.productId;
    if (category) url += '&category=' + encodeURIComponent(category);
    if (search) url += '&search=' + encodeURIComponent(search);

    window.DesignEditor.apiRequest(url)
      .then(function (data) {
        renderClipartGrid(data.assets || []);
      })
      .catch(function (err) {
        console.error('[DesignEditorTools] Clipart load failed:', err);
      });
  }

  function renderClipartGrid(clipartItems) {
    const grid = document.getElementById('clipart-grid');
    if (!grid) return;

    grid.innerHTML = '';

    if (clipartItems.length === 0) {
      grid.innerHTML =
        '<div class="design-editor__empty" style="grid-column:1/-1;padding:1rem;">' +
        '<i class="fas fa-icons"></i><p style="margin:0;font-size:0.75rem;">No clipart found</p></div>';
      return;
    }

    clipartItems.forEach(function (item) {
      const div = document.createElement('div');
      div.className = 'design-editor__clipart-item';
      div.title = item.name;

      const img = document.createElement('img');
      img.src = item.url;
      img.alt = item.name;
      img.loading = 'lazy';
      div.appendChild(img);

      div.addEventListener('click', function () {
        addClipartToCanvas(item.url, item.id);
      });

      grid.appendChild(div);
    });
  }

  function addClipartToCanvas(url, clipartId) {
    if (!window.DesignEditorCanvas) return;

    const canvas = window.DesignEditorCanvas.getCanvas();
    if (!canvas) return;

    fabric.Image.fromURL(url, { crossOrigin: 'anonymous' }).then(function (img) {
      if (!img) return;

      const canvasW = canvas.getWidth();
      const canvasH = canvas.getHeight();
      const maxDim = Math.min(canvasW, canvasH) * 0.3;

      let scale = 1;
      if (img.width > maxDim || img.height > maxDim) {
        scale = maxDim / Math.max(img.width, img.height);
      }

      img.set({
        left: canvasW / 2,
        top: canvasH / 2,
        originX: 'center',
        originY: 'center',
        scaleX: scale,
        scaleY: scale,
        custom_type: 'clipart',
        custom_media_asset_id: clipartId || null,
      });

      window.DesignEditorCanvas.addObject(img);
    });
  }

  /* ─── Template Selector ──────────────────────────────────────────────── */

  function bindTemplateTool() {
    renderTemplateGrid();
  }

  function renderTemplateGrid() {
    const grid = document.getElementById('template-grid');
    if (!grid || !state) return;

    const templates = state.templates || [];
    grid.innerHTML = '';

    if (templates.length === 0) {
      grid.innerHTML =
        '<div class="design-editor__empty" style="grid-column:1/-1;padding:1rem;">' +
        '<i class="fas fa-palette"></i><p style="margin:0;font-size:0.75rem;">No templates available</p></div>';
      return;
    }

    templates.forEach(function (template) {
      const card = document.createElement('div');
      card.className = 'design-editor__template-card';

      if (template.thumbnail_url) {
        const img = document.createElement('img');
        img.src = template.thumbnail_url;
        img.alt = template.name;
        img.loading = 'lazy';
        card.appendChild(img);
      }

      const name = document.createElement('div');
      name.className = 'design-editor__template-card__name';
      name.textContent = template.name;
      card.appendChild(name);

      card.addEventListener('click', function () {
        applyTemplate(template);
      });

      grid.appendChild(card);
    });
  }

  async function applyTemplate(template) {
    if (!template.design_data) return;
    if (!(await AdminModal.confirm('Apply this template? Your current design will be replaced.')))
      return;

    const surfacesData = template.design_data.surfaces || {};

    // Load template data into surface states
    Object.keys(surfacesData).forEach(function (slug) {
      const sd = surfacesData[slug];
      if (state) {
        state.surfaceStates[slug] = {
          canvasJSON: sd.canvas_json || { version: '6.0.0', objects: [] },
          dirty: true,
        };
      }
    });

    // Reload current surface
    if (window.DesignEditor) {
      window.DesignEditor.switchSurface(state.activeSurfaceIndex);
      window.DesignEditor.showNotification('Template applied!', 'success');
    }
  }

  /* ─── C2: Layers Panel ───────────────────────────────────────────────── */

  function renderLayersPanel() {
    const list = document.getElementById('layers-list');
    if (!list || !window.DesignEditorCanvas) return;

    const canvas = window.DesignEditorCanvas.getCanvas();
    if (!canvas) return;

    list.innerHTML = '';
    const objects = canvas.getObjects();
    const activeObj = canvas.getActiveObject();

    if (objects.length === 0) {
      list.innerHTML =
        '<div class="design-editor__empty" style="padding:1rem;">' +
        '<p style="margin:0;font-size:0.75rem;">No elements yet</p></div>';
      return;
    }

    // Render in reverse z-order (top layer first)
    for (let i = objects.length - 1; i >= 0; i--) {
      const obj = objects[i];
      var item = document.createElement('div');
      item.className = 'design-editor__layer-item' + (obj === activeObj ? ' active' : '');

      const icon = getLayerIcon(obj);
      const label = getLayerLabel(obj);

      item.innerHTML =
        '<span class="design-editor__layer-icon"><i class="fas ' +
        icon +
        '"></i></span>' +
        '<span class="design-editor__layer-name">' +
        escapeHtml(label) +
        '</span>' +
        '<div class="design-editor__layer-actions">' +
        '<button type="button" class="design-editor__layer-btn" data-action="visibility" title="Toggle visibility">' +
        '<i class="fas ' +
        (obj.visible === false ? 'fa-eye-slash' : 'fa-eye') +
        '"></i>' +
        '</button>' +
        '<button type="button" class="design-editor__layer-btn" data-action="delete" title="Delete">' +
        '<i class="fas fa-times"></i>' +
        '</button>' +
        '</div>';

      // Click to select
      (function (o) {
        item.addEventListener('click', function (e) {
          if (e.target.closest('[data-action]')) return;
          canvas.setActiveObject(o);
          canvas.requestRenderAll();
        });
      })(obj);

      // Visibility toggle
      (function (o, el) {
        el.querySelector('[data-action="visibility"]').addEventListener('click', function () {
          o.visible = o.visible === false ? true : false;
          canvas.requestRenderAll();
          renderLayersPanel();
          if (window.DesignEditorHistory) window.DesignEditorHistory.recordState();
        });
      })(obj, item);

      // Delete
      (function (o) {
        item.querySelector('[data-action="delete"]').addEventListener('click', function () {
          if (o.custom_no_delete) return;
          canvas.remove(o);
          canvas.requestRenderAll();
          if (window.DesignEditorHistory) window.DesignEditorHistory.recordState();
        });
      })(obj);

      list.appendChild(item);
    }
  }

  function getLayerIcon(obj) {
    const t = obj.type;
    if (t === 'textbox' || t === 'i-text' || t === 'text') return 'fa-font';
    if (obj.custom_type === 'clipart') return 'fa-icons';
    if (t === 'image') return 'fa-image';
    return 'fa-cube';
  }

  function getLayerLabel(obj) {
    const t = obj.type;
    if (t === 'textbox' || t === 'i-text' || t === 'text') {
      const txt = obj.text || '';
      return txt.length > 18 ? txt.substring(0, 18) + '...' : txt || 'Text';
    }
    if (obj.custom_type === 'clipart') return 'Clipart';
    if (t === 'image') return 'Image';
    return obj.type || 'Object';
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str || ''));
    return div.innerHTML;
  }

  /* ─── Selection Callbacks ────────────────────────────────────────────── */

  function onObjectSelected(obj) {
    selectedObject = obj;

    if (obj.type === 'i-text' || obj.type === 'textbox') {
      // Switch to text tool FIRST so the panel is visible,
      // then show properties inside it
      if (window.DesignEditor) {
        window.DesignEditor.switchTool('text');
      }
      showTextProperties(obj);
    } else if (obj.type === 'image') {
      if (window.DesignEditor) {
        window.DesignEditor.switchTool('image');
      }
      showImageProperties(obj);
    }

    // Enable duplicate button
    const btnDuplicate = document.getElementById('btn-duplicate');
    if (btnDuplicate) btnDuplicate.disabled = false;

    renderLayersPanel();
  }

  function onObjectDeselected() {
    selectedObject = null;
    hideAllProperties();

    const btnDuplicate = document.getElementById('btn-duplicate');
    if (btnDuplicate) btnDuplicate.disabled = true;

    renderLayersPanel();
  }

  function onCanvasChanged() {
    renderLayersPanel();
  }

  function showTextProperties(obj) {
    const panel = document.getElementById('text-properties');
    if (!panel) return;
    panel.style.display = '';

    // Update controls to match object state
    const propFontFamily = document.getElementById('prop-font-family');
    const propFontSize = document.getElementById('prop-font-size');
    const propFontColor = document.getElementById('prop-font-color');
    const propBold = document.getElementById('prop-bold');
    const propItalic = document.getElementById('prop-italic');
    const propStrokeColor = document.getElementById('prop-stroke-color');
    const propStrokeWidth = document.getElementById('prop-stroke-width');

    if (propFontFamily) propFontFamily.value = obj.fontFamily || 'Arial';
    if (propFontSize) propFontSize.value = obj.fontSize || 24;
    if (propFontColor) propFontColor.value = obj.fill || '#000000';
    if (propBold) propBold.classList.toggle('active', obj.fontWeight === 'bold');
    if (propItalic) propItalic.classList.toggle('active', obj.fontStyle === 'italic');
    if (propStrokeColor) propStrokeColor.value = obj.stroke || '#ffffff';
    if (propStrokeWidth) propStrokeWidth.value = obj.strokeWidth || 0;

    updateAlignButtons(obj.textAlign || 'left');

    // Hide image properties
    const imgPanel = document.getElementById('image-properties');
    if (imgPanel) imgPanel.style.display = 'none';
  }

  function showImageProperties(obj) {
    const panel = document.getElementById('image-properties');
    if (!panel) return;
    panel.style.display = '';

    // Opacity
    const propOpacity = document.getElementById('prop-opacity');
    if (propOpacity) propOpacity.value = obj.opacity !== undefined ? obj.opacity : 1;

    // Read current filter values
    const filters = obj.filters || [];
    const brightness = getFilterValue(filters, 'Brightness', 'brightness', 0);
    const contrast = getFilterValue(filters, 'Contrast', 'contrast', 0);
    const saturation = getFilterValue(filters, 'Saturation', 'saturation', 0);

    const propBrightness = document.getElementById('prop-brightness');
    if (propBrightness) propBrightness.value = brightness;

    const propContrast = document.getElementById('prop-contrast');
    if (propContrast) propContrast.value = contrast;

    const propSaturation = document.getElementById('prop-saturation');
    if (propSaturation) propSaturation.value = saturation;

    // Tint (BlendColor)
    let tintColor = '#ff0000';
    let tintAlpha = 0;
    for (let i = 0; i < filters.length; i++) {
      if (filters[i].type === 'BlendColor') {
        tintColor = filters[i].color || '#ff0000';
        tintAlpha = filters[i].alpha || 0;
        break;
      }
    }
    const propTintColor = document.getElementById('prop-tint-color');
    const propTintAlpha = document.getElementById('prop-tint-alpha');
    if (propTintColor) propTintColor.value = tintColor;
    if (propTintAlpha) propTintAlpha.value = tintAlpha;

    // Remove Color
    let removeColor = '#ffffff';
    let removeDistance = 0;
    for (let j = 0; j < filters.length; j++) {
      if (filters[j].type === 'RemoveColor') {
        removeColor = filters[j].color || '#ffffff';
        removeDistance = filters[j].distance || 0;
        break;
      }
    }
    const propRemoveColor = document.getElementById('prop-remove-color');
    const propRemoveDistance = document.getElementById('prop-remove-distance');
    if (propRemoveColor) propRemoveColor.value = removeColor;
    if (propRemoveDistance) propRemoveDistance.value = removeDistance;

    // Rotation
    const propRotation = document.getElementById('prop-rotation');
    if (propRotation) propRotation.value = Math.round(obj.angle || 0);

    // Hide text properties
    const textPanel = document.getElementById('text-properties');
    if (textPanel) textPanel.style.display = 'none';
  }

  function hideAllProperties() {
    const textPanel = document.getElementById('text-properties');
    const imagePanel = document.getElementById('image-properties');
    if (textPanel) textPanel.style.display = 'none';
    if (imagePanel) imagePanel.style.display = 'none';
  }

  /* ─── Public API ─────────────────────────────────────────────────────── */

  window.DesignEditorTools = {
    init: init,
    onObjectSelected: onObjectSelected,
    onObjectDeselected: onObjectDeselected,
    onCanvasChanged: onCanvasChanged,
    renderLayersPanel: renderLayersPanel,
    addTextObject: addTextObject,
    addImageToCanvas: addImageToCanvas,
    addClipartToCanvas: addClipartToCanvas,
    applyTemplate: applyTemplate,
    uploadImage: uploadImage,
    enforcePerSurfaceToggles: enforcePerSurfaceToggles,
  };
})();
