/**
 * Design Template Builder - Admin Visual Editor
 * Full Fabric.js canvas editor for merchants to create design templates
 * with per-element lock controls.
 */
(function () {
  'use strict';

  // ─── State ──────────────────────────────────────────────────────────
  const editorData = JSON.parse(document.getElementById('template-editor-data').textContent);
  const surfaces = editorData.surfaces || [];
  const fonts = editorData.fonts || [];
  const clipartCategories = editorData.clipartCategories || [];
  let templateData = editorData.template || null;

  let csrfToken = editorData.csrfToken || '';
  if (!csrfToken) {
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    if (m) csrfToken = m[1];
  }

  const state = {
    canvas: null,
    activeSurfaceIndex: 0,
    surfaceStates: {}, // slug -> { canvasJSON }
    undoStack: [],
    redoStack: [],
    zoom: 1,
    saving: false,
    fontsLoaded: false,
    dirty: false,
  };

  // Max undo/redo entries
  const MAX_HISTORY = 40;

  // ─── Initialization ─────────────────────────────────────────────────
  function init() {
    if (surfaces.length === 0) {
      showNotification('No surfaces defined. Please add surfaces first.', 'error');
      return;
    }

    initSurfaceTabs();
    initCanvas();
    loadFonts();
    populateFontSelector();
    bindTools();
    bindProperties();
    bindLocks();
    bindToolbar();
    bindSaveButtons();
    bindClipartModal();
    bindKeyboard();

    // Auto-gen slug from name
    const nameInput = document.getElementById('tmpl-name');
    const slugInput = document.getElementById('tmpl-slug');
    nameInput.addEventListener('input', function () {
      if (!templateData) {
        slugInput.value = slugify(nameInput.value);
      }
    });

    // Load existing template data
    if (templateData && templateData.design_data) {
      loadExistingDesign(templateData.design_data);
    }

    // Switch to first surface
    switchSurface(0);
  }

  // ─── Surface Tabs ───────────────────────────────────────────────────
  function initSurfaceTabs() {
    const container = document.getElementById('tmpl-surfaces');
    container.innerHTML = '';

    surfaces.forEach(function (surface, index) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'tmpl-builder__surface-tab' + (index === 0 ? ' active' : '');
      btn.textContent = surface.name;
      btn.addEventListener('click', function () {
        switchSurface(index);
      });
      container.appendChild(btn);
    });
  }

  function switchSurface(index) {
    // Save current surface state
    if (state.canvas) {
      saveCurrentSurfaceState();
    }

    state.activeSurfaceIndex = index;
    const surface = surfaces[index];

    // Update tab styles
    const tabs = document.querySelectorAll('.tmpl-builder__surface-tab');
    tabs.forEach(function (t, i) {
      t.classList.toggle('active', i === index);
    });

    // Update mockup image
    const mockupImg = document.getElementById('tmpl-mockup-img');
    const mockupContainer = document.getElementById('tmpl-mockup-container');
    if (surface.mockup_url) {
      mockupImg.src = surface.mockup_url;
      mockupImg.style.display = 'block';
      mockupImg.onload = function () {
        positionCanvasZone(surface, mockupImg);
      };
      if (mockupImg.complete) {
        positionCanvasZone(surface, mockupImg);
      }
    } else {
      mockupImg.style.display = 'none';
      mockupContainer.className = 'tmpl-builder__mockup-container tmpl-builder__no-mockup';
      positionCanvasZoneNoMockup(surface);
    }

    // Update dimensions label
    const dimLabel = document.getElementById('surface-dimensions');
    if (dimLabel) {
      dimLabel.textContent = surface.width + ' x ' + surface.height + ' ' + surface.dimension_unit;
    }

    // Restore canvas state for this surface
    restoreSurfaceState(surface.slug);
  }

  function positionCanvasZone(surface, mockupImg) {
    const zone = document.getElementById('tmpl-canvas-zone');
    const container = document.getElementById('tmpl-mockup-container');

    // Let the container size itself to the image
    container.className = 'tmpl-builder__mockup-container';
    container.style.width = mockupImg.naturalWidth + 'px';
    container.style.height = mockupImg.naturalHeight + 'px';

    // Limit container to viewport
    const viewport = document.getElementById('tmpl-viewport');
    const maxW = viewport.clientWidth - 40;
    const maxH = viewport.clientHeight - 40;
    const scale = Math.min(1, maxW / mockupImg.naturalWidth, maxH / mockupImg.naturalHeight);
    container.style.width = Math.round(mockupImg.naturalWidth * scale) + 'px';
    container.style.height = Math.round(mockupImg.naturalHeight * scale) + 'px';

    // Position zone
    const cw = container.offsetWidth;
    const ch = container.offsetHeight;
    const x = parseFloat(surface.area_x_percent) / 100;
    const y = parseFloat(surface.area_y_percent) / 100;
    const w = parseFloat(surface.area_width_percent) / 100;
    const h = parseFloat(surface.area_height_percent) / 100;

    zone.style.left = Math.round(cw * x) + 'px';
    zone.style.top = Math.round(ch * y) + 'px';
    zone.style.width = Math.round(cw * w) + 'px';
    zone.style.height = Math.round(ch * h) + 'px';

    resizeCanvas(Math.round(cw * w), Math.round(ch * h));
  }

  function positionCanvasZoneNoMockup(surface) {
    const zone = document.getElementById('tmpl-canvas-zone');
    const container = document.getElementById('tmpl-mockup-container');

    const viewport = document.getElementById('tmpl-viewport');
    const maxW = viewport.clientWidth - 40;
    const maxH = viewport.clientHeight - 40;
    const size = Math.min(500, maxW, maxH);

    container.style.width = size + 'px';
    container.style.height = size + 'px';
    zone.style.left = '0px';
    zone.style.top = '0px';
    zone.style.width = size + 'px';
    zone.style.height = size + 'px';

    resizeCanvas(size, size);
  }

  // ─── Canvas ─────────────────────────────────────────────────────────
  function initCanvas() {
    state.canvas = new fabric.Canvas('tmpl-canvas', {
      preserveObjectStacking: true,
      selection: true,
      backgroundColor: '#ffffff',
    });

    const canvas = state.canvas;

    canvas.on('selection:created', onSelectionChanged);
    canvas.on('selection:updated', onSelectionChanged);
    canvas.on('selection:cleared', onSelectionCleared);
    canvas.on('object:modified', function () {
      pushHistory();
      renderLayers();
      state.dirty = true;
    });
    canvas.on('object:added', function () {
      renderLayers();
      state.dirty = true;
    });
    canvas.on('object:removed', function () {
      renderLayers();
      state.dirty = true;
    });
  }

  function resizeCanvas(w, h) {
    if (!state.canvas) return;
    state.canvas.setDimensions({ width: w, height: h });
    state.canvas.setZoom(state.zoom);
    state.canvas.renderAll();
  }

  function saveCurrentSurfaceState() {
    if (!state.canvas) return;
    const slug = surfaces[state.activeSurfaceIndex].slug;
    state.surfaceStates[slug] = {
      canvasJSON: state.canvas.toJSON([
        'custom_type',
        'custom_name',
        'custom_lock_position',
        'custom_lock_size',
        'custom_lock_rotation',
        'custom_lock_content',
        'custom_lock_delete',
      ]),
      canvasWidth: state.canvas.getWidth(),
      canvasHeight: state.canvas.getHeight(),
    };
  }

  function restoreSurfaceState(slug) {
    if (!state.canvas) return;
    const surfaceState = state.surfaceStates[slug];
    if (surfaceState && surfaceState.canvasJSON) {
      state.canvas.loadFromJSON(surfaceState.canvasJSON).then(function () {
        state.canvas.renderAll();
        renderLayers();
        clearHistory();
      });
    } else {
      state.canvas.clear();
      state.canvas.backgroundColor = '#ffffff';
      state.canvas.renderAll();
      renderLayers();
      clearHistory();
    }
  }

  function loadExistingDesign(designData) {
    const surfacesData = designData.surfaces || {};
    Object.keys(surfacesData).forEach(function (slug) {
      const sd = surfacesData[slug];
      state.surfaceStates[slug] = {
        canvasJSON: sd.canvas_json || { version: '6.0.0', objects: [] },
      };
    });
  }

  // ─── History (Undo/Redo) ────────────────────────────────────────────
  function pushHistory() {
    if (!state.canvas) return;
    const json = state.canvas.toJSON([
      'custom_type',
      'custom_name',
      'custom_lock_position',
      'custom_lock_size',
      'custom_lock_rotation',
      'custom_lock_content',
      'custom_lock_delete',
    ]);
    state.undoStack.push(JSON.stringify(json));
    if (state.undoStack.length > MAX_HISTORY) {
      state.undoStack.shift();
    }
    state.redoStack = [];
    updateHistoryButtons();
  }

  function undo() {
    if (state.undoStack.length === 0) return;
    const current = state.canvas.toJSON([
      'custom_type',
      'custom_name',
      'custom_lock_position',
      'custom_lock_size',
      'custom_lock_rotation',
      'custom_lock_content',
      'custom_lock_delete',
    ]);
    state.redoStack.push(JSON.stringify(current));
    const prev = JSON.parse(state.undoStack.pop());
    state.canvas.loadFromJSON(prev).then(function () {
      state.canvas.renderAll();
      renderLayers();
      updateHistoryButtons();
    });
  }

  function redo() {
    if (state.redoStack.length === 0) return;
    const current = state.canvas.toJSON([
      'custom_type',
      'custom_name',
      'custom_lock_position',
      'custom_lock_size',
      'custom_lock_rotation',
      'custom_lock_content',
      'custom_lock_delete',
    ]);
    state.undoStack.push(JSON.stringify(current));
    const next = JSON.parse(state.redoStack.pop());
    state.canvas.loadFromJSON(next).then(function () {
      state.canvas.renderAll();
      renderLayers();
      updateHistoryButtons();
    });
  }

  function clearHistory() {
    state.undoStack = [];
    state.redoStack = [];
    updateHistoryButtons();
  }

  function updateHistoryButtons() {
    const undoBtn = document.getElementById('btn-undo');
    const redoBtn = document.getElementById('btn-redo');
    if (undoBtn) undoBtn.disabled = state.undoStack.length === 0;
    if (redoBtn) redoBtn.disabled = state.redoStack.length === 0;
  }

  // ─── Fonts ──────────────────────────────────────────────────────────
  function loadFonts() {
    fonts.forEach(function (font) {
      if (font.is_system_font || !font.regular_url) return;
      const style = document.createElement('style');
      style.textContent =
        '@font-face { font-family: "' +
        font.family +
        '"; ' +
        'src: url("' +
        font.regular_url +
        '"); font-weight: normal; font-style: normal; }';
      document.head.appendChild(style);

      if (font.bold_url) {
        const bs = document.createElement('style');
        bs.textContent =
          '@font-face { font-family: "' +
          font.family +
          '"; ' +
          'src: url("' +
          font.bold_url +
          '"); font-weight: bold; font-style: normal; }';
        document.head.appendChild(bs);
      }
      if (font.italic_url) {
        const is = document.createElement('style');
        is.textContent =
          '@font-face { font-family: "' +
          font.family +
          '"; ' +
          'src: url("' +
          font.italic_url +
          '"); font-weight: normal; font-style: italic; }';
        document.head.appendChild(is);
      }
    });
    state.fontsLoaded = true;
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
    systemFonts.forEach(function (name) {
      const opt = document.createElement('option');
      opt.value = name;
      opt.textContent = name;
      select.appendChild(opt);
    });

    // Custom fonts
    fonts.forEach(function (font) {
      const opt = document.createElement('option');
      opt.value = font.family;
      opt.textContent = font.name;
      select.appendChild(opt);
    });
  }

  // ─── Tools ──────────────────────────────────────────────────────────
  function bindTools() {
    document.getElementById('btn-add-text').addEventListener('click', addText);
    document.getElementById('btn-add-image').addEventListener('click', function () {
      document.getElementById('image-upload-input').click();
    });
    document.getElementById('btn-add-clipart').addEventListener('click', openClipartModal);
    document.getElementById('btn-add-rect').addEventListener('click', addRect);
    document.getElementById('btn-add-circle').addEventListener('click', addCircle);

    document.getElementById('image-upload-input').addEventListener('change', handleImageUpload);
  }

  function addText() {
    pushHistory();
    const text = new fabric.Textbox('Sample Text', {
      left: 50,
      top: 50,
      width: Math.round(state.canvas.getWidth() * 0.6),
      fontSize: 28,
      fontFamily: 'Arial',
      fill: '#000000',
      custom_type: 'text',
      custom_name: 'Text',
      custom_lock_position: false,
      custom_lock_size: false,
      custom_lock_rotation: false,
      custom_lock_content: false,
      custom_lock_delete: false,
    });
    state.canvas.add(text);
    state.canvas.setActiveObject(text);
    state.canvas.renderAll();
  }

  function addRect() {
    pushHistory();
    const rect = new fabric.Rect({
      left: 50,
      top: 50,
      width: 150,
      height: 100,
      fill: '#cccccc',
      stroke: '#000000',
      strokeWidth: 0,
      custom_type: 'shape',
      custom_name: 'Rectangle',
      custom_lock_position: false,
      custom_lock_size: false,
      custom_lock_rotation: false,
      custom_lock_content: false,
      custom_lock_delete: false,
    });
    state.canvas.add(rect);
    state.canvas.setActiveObject(rect);
    state.canvas.renderAll();
  }

  function addCircle() {
    pushHistory();
    const circle = new fabric.Circle({
      left: 50,
      top: 50,
      radius: 60,
      fill: '#cccccc',
      stroke: '#000000',
      strokeWidth: 0,
      custom_type: 'shape',
      custom_name: 'Circle',
      custom_lock_position: false,
      custom_lock_size: false,
      custom_lock_rotation: false,
      custom_lock_content: false,
      custom_lock_delete: false,
    });
    state.canvas.add(circle);
    state.canvas.setActiveObject(circle);
    state.canvas.renderAll();
  }

  function handleImageUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    e.target.value = '';

    // Upload to server
    const formData = new FormData();
    formData.append('image', file);
    formData.append('product_id', editorData.productId);

    fetch(editorData.urls.uploadImage, {
      method: 'POST',
      headers: { 'X-CSRFToken': csrfToken },
      body: formData,
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.error) {
          showNotification(data.error, 'error');
          return;
        }
        addImageToCanvas(data.url, data.filename);
      })
      .catch(function (err) {
        showNotification('Upload failed: ' + err.message, 'error');
      });
  }

  function addImageToCanvas(url, name) {
    pushHistory();
    fabric.Image.fromURL(url, { crossOrigin: 'anonymous' }).then(function (img) {
      // Scale to fit canvas
      const maxW = state.canvas.getWidth() * 0.6;
      const maxH = state.canvas.getHeight() * 0.6;
      const scale = Math.min(1, maxW / img.width, maxH / img.height);
      img.set({
        left: 30,
        top: 30,
        scaleX: scale,
        scaleY: scale,
        custom_type: 'image',
        custom_name: name || 'Image',
        custom_lock_position: false,
        custom_lock_size: false,
        custom_lock_rotation: false,
        custom_lock_content: false,
        custom_lock_delete: false,
      });
      state.canvas.add(img);
      state.canvas.setActiveObject(img);
      state.canvas.renderAll();
    });
  }

  // ─── Clipart ────────────────────────────────────────────────────────
  function bindClipartModal() {
    const modal = document.getElementById('modal-clipart');
    modal.querySelector('.tmpl-builder__modal-close').addEventListener('click', closeClipartModal);
    modal
      .querySelector('.tmpl-builder__modal-backdrop')
      .addEventListener('click', closeClipartModal);

    // Build category pills
    const catContainer = document.getElementById('clipart-categories');
    clipartCategories.forEach(function (cat, i) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'tmpl-builder__clipart-cat-btn' + (i === 0 ? ' active' : '');
      btn.textContent = cat.name;
      btn.dataset.slug = cat.slug;
      btn.addEventListener('click', function () {
        catContainer.querySelectorAll('.tmpl-builder__clipart-cat-btn').forEach(function (b) {
          b.classList.remove('active');
        });
        btn.classList.add('active');
        loadClipartAssets(cat.slug);
      });
      catContainer.appendChild(btn);
    });
  }

  function openClipartModal() {
    const modal = document.getElementById('modal-clipart');
    modal.classList.add('open');
    // Load first category
    if (clipartCategories.length > 0) {
      loadClipartAssets(clipartCategories[0].slug);
    }
  }

  function closeClipartModal() {
    document.getElementById('modal-clipart').classList.remove('open');
  }

  function loadClipartAssets(categorySlug) {
    const grid = document.getElementById('clipart-grid');
    grid.innerHTML = '<p style="font-size:0.85rem;color:#999;">Loading...</p>';

    const url =
      editorData.urls.clipartApi +
      '?category=' +
      encodeURIComponent(categorySlug) +
      '&product_id=' +
      editorData.productId;

    fetch(url)
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        grid.innerHTML = '';
        const assets = data.assets || [];
        if (assets.length === 0) {
          grid.innerHTML =
            '<p style="font-size:0.85rem;color:#999;">No clipart in this category.</p>';
          return;
        }
        assets.forEach(function (asset) {
          const item = document.createElement('div');
          item.className = 'tmpl-builder__clipart-item';
          item.innerHTML =
            '<img src="' + escapeAttr(asset.url) + '" alt="' + escapeAttr(asset.name) + '">';
          item.addEventListener('click', function () {
            addClipartToCanvas(asset.url, asset.name);
            closeClipartModal();
          });
          grid.appendChild(item);
        });
      })
      .catch(function () {
        grid.innerHTML = '<p style="font-size:0.85rem;color:#c00;">Failed to load clipart.</p>';
      });
  }

  function addClipartToCanvas(url, name) {
    pushHistory();
    fabric.Image.fromURL(url, { crossOrigin: 'anonymous' }).then(function (img) {
      const maxW = state.canvas.getWidth() * 0.4;
      const maxH = state.canvas.getHeight() * 0.4;
      const scale = Math.min(1, maxW / img.width, maxH / img.height);
      img.set({
        left: 40,
        top: 40,
        scaleX: scale,
        scaleY: scale,
        custom_type: 'clipart',
        custom_name: name || 'Clipart',
        custom_lock_position: false,
        custom_lock_size: false,
        custom_lock_rotation: false,
        custom_lock_content: false,
        custom_lock_delete: false,
      });
      state.canvas.add(img);
      state.canvas.setActiveObject(img);
      state.canvas.renderAll();
    });
  }

  // ─── Properties Panel ───────────────────────────────────────────────
  function bindProperties() {
    // Font family
    document.getElementById('prop-font-family').addEventListener('change', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      obj.set('fontFamily', this.value);
      state.canvas.renderAll();
      pushHistory();
    });

    // Font size
    document.getElementById('prop-font-size').addEventListener('change', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      obj.set('fontSize', parseInt(this.value) || 24);
      state.canvas.renderAll();
      pushHistory();
    });

    // Font color
    document.getElementById('prop-font-color').addEventListener('input', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      obj.set('fill', this.value);
      state.canvas.renderAll();
    });
    document.getElementById('prop-font-color').addEventListener('change', function () {
      pushHistory();
    });

    // Bold
    document.getElementById('prop-bold').addEventListener('click', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      const isBold = obj.fontWeight === 'bold';
      obj.set('fontWeight', isBold ? 'normal' : 'bold');
      this.classList.toggle('active', !isBold);
      state.canvas.renderAll();
      pushHistory();
    });

    // Italic
    document.getElementById('prop-italic').addEventListener('click', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      const isItalic = obj.fontStyle === 'italic';
      obj.set('fontStyle', isItalic ? 'normal' : 'italic');
      this.classList.toggle('active', !isItalic);
      state.canvas.renderAll();
      pushHistory();
    });

    // Text alignment
    ['left', 'center', 'right'].forEach(function (align) {
      document.getElementById('prop-align-' + align).addEventListener('click', function () {
        const obj = state.canvas.getActiveObject();
        if (!obj) return;
        obj.set('textAlign', align);
        document.querySelectorAll('[id^="prop-align-"]').forEach(function (b) {
          b.classList.remove('active');
        });
        this.classList.add('active');
        state.canvas.renderAll();
        pushHistory();
      });
    });

    // Opacity
    document.getElementById('prop-opacity').addEventListener('input', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      obj.set('opacity', parseFloat(this.value));
      state.canvas.renderAll();
    });
    document.getElementById('prop-opacity').addEventListener('change', function () {
      pushHistory();
    });

    // Shape fill
    document.getElementById('prop-fill').addEventListener('input', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      obj.set('fill', this.value);
      state.canvas.renderAll();
    });
    document.getElementById('prop-fill').addEventListener('change', function () {
      pushHistory();
    });

    // Shape stroke color
    document.getElementById('prop-stroke-color').addEventListener('input', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      obj.set('stroke', this.value);
      state.canvas.renderAll();
    });
    document.getElementById('prop-stroke-color').addEventListener('change', function () {
      pushHistory();
    });

    // Shape stroke width
    document.getElementById('prop-stroke-width').addEventListener('change', function () {
      const obj = state.canvas.getActiveObject();
      if (!obj) return;
      obj.set('strokeWidth', parseFloat(this.value) || 0);
      state.canvas.renderAll();
      pushHistory();
    });

    // Ordering
    document.getElementById('prop-bring-front').addEventListener('click', function () {
      const obj = state.canvas.getActiveObject();
      if (obj) {
        state.canvas.bringObjectToFront(obj);
        pushHistory();
        renderLayers();
      }
    });
    document.getElementById('prop-bring-forward').addEventListener('click', function () {
      const obj = state.canvas.getActiveObject();
      if (obj) {
        state.canvas.bringObjectForward(obj);
        pushHistory();
        renderLayers();
      }
    });
    document.getElementById('prop-send-backward').addEventListener('click', function () {
      const obj = state.canvas.getActiveObject();
      if (obj) {
        state.canvas.sendObjectBackwards(obj);
        pushHistory();
        renderLayers();
      }
    });
    document.getElementById('prop-send-back').addEventListener('click', function () {
      const obj = state.canvas.getActiveObject();
      if (obj) {
        state.canvas.sendObjectToBack(obj);
        pushHistory();
        renderLayers();
      }
    });
  }

  function onSelectionChanged() {
    const obj = state.canvas.getActiveObject();
    if (!obj) {
      onSelectionCleared();
      return;
    }

    document.getElementById('section-properties').style.display = '';
    document.getElementById('section-locks').style.display = '';

    const isText = isTextObject(obj);
    const isShape = obj.custom_type === 'shape';

    document.getElementById('props-text').style.display = isText ? '' : 'none';
    document.getElementById('props-shape').style.display = isShape ? '' : 'none';

    // Update property values
    document.getElementById('prop-opacity').value = obj.opacity != null ? obj.opacity : 1;

    if (isText) {
      document.getElementById('prop-font-family').value = obj.fontFamily || 'Arial';
      document.getElementById('prop-font-size').value = obj.fontSize || 24;
      document.getElementById('prop-font-color').value = obj.fill || '#000000';
      document.getElementById('prop-bold').classList.toggle('active', obj.fontWeight === 'bold');
      document.getElementById('prop-italic').classList.toggle('active', obj.fontStyle === 'italic');
      document.querySelectorAll('[id^="prop-align-"]').forEach(function (b) {
        b.classList.toggle('active', b.id === 'prop-align-' + (obj.textAlign || 'left'));
      });
    }

    if (isShape) {
      document.getElementById('prop-fill').value = obj.fill || '#cccccc';
      document.getElementById('prop-stroke-color').value = obj.stroke || '#000000';
      document.getElementById('prop-stroke-width').value = obj.strokeWidth || 0;
    }

    // Update lock checkboxes
    document.getElementById('lock-position').checked = !!obj.custom_lock_position;
    document.getElementById('lock-size').checked = !!obj.custom_lock_size;
    document.getElementById('lock-rotation').checked = !!obj.custom_lock_rotation;
    document.getElementById('lock-content').checked = !!obj.custom_lock_content;
    document.getElementById('lock-delete').checked = !!obj.custom_lock_delete;

    // Enable delete
    document.getElementById('btn-delete').disabled = false;

    // Highlight in layers
    renderLayers();
  }

  function onSelectionCleared() {
    document.getElementById('section-properties').style.display = 'none';
    document.getElementById('section-locks').style.display = 'none';
    document.getElementById('btn-delete').disabled = true;
    renderLayers();
  }

  // ─── Lock Controls ──────────────────────────────────────────────────
  function bindLocks() {
    const lockIds = ['lock-position', 'lock-size', 'lock-rotation', 'lock-content', 'lock-delete'];
    const lockProps = [
      'custom_lock_position',
      'custom_lock_size',
      'custom_lock_rotation',
      'custom_lock_content',
      'custom_lock_delete',
    ];

    lockIds.forEach(function (id, i) {
      document.getElementById(id).addEventListener('change', function () {
        const obj = state.canvas.getActiveObject();
        if (!obj) return;
        obj[lockProps[i]] = this.checked;
        state.dirty = true;
      });
    });
  }

  // ─── Layers Panel ───────────────────────────────────────────────────
  function renderLayers() {
    const list = document.getElementById('layers-list');
    if (!list || !state.canvas) return;
    list.innerHTML = '';

    const objects = state.canvas.getObjects();
    const activeObj = state.canvas.getActiveObject();

    // Render in reverse z-order (top to bottom)
    for (let i = objects.length - 1; i >= 0; i--) {
      const obj = objects[i];
      var item = document.createElement('div');
      item.className = 'tmpl-builder__layer-item' + (obj === activeObj ? ' active' : '');

      const icon = getObjectIcon(obj);
      const name = obj.custom_name || getObjectLabel(obj);

      let lockIndicator = '';
      if (
        obj.custom_lock_position ||
        obj.custom_lock_size ||
        obj.custom_lock_rotation ||
        obj.custom_lock_content ||
        obj.custom_lock_delete
      ) {
        lockIndicator =
          ' <i class="fas fa-lock" style="font-size:0.65rem;color:var(--body-quiet-color,#999);"></i>';
      }

      item.innerHTML =
        '<span class="tmpl-builder__layer-icon"><i class="fas ' +
        icon +
        '"></i></span>' +
        '<span class="tmpl-builder__layer-name">' +
        escapeHtml(name) +
        lockIndicator +
        '</span>' +
        '<div class="tmpl-builder__layer-actions">' +
        '<button type="button" class="tmpl-builder__layer-btn' +
        (obj.visible === false ? ' tmpl-builder__layer-btn--hidden' : '') +
        '" data-action="visibility" title="Toggle visibility">' +
        '<i class="fas ' +
        (obj.visible === false ? 'fa-eye-slash' : 'fa-eye') +
        '"></i>' +
        '</button>' +
        '<button type="button" class="tmpl-builder__layer-btn" data-action="delete" title="Delete">' +
        '<i class="fas fa-times"></i>' +
        '</button>' +
        '</div>';

      // Click to select
      (function (o) {
        item.addEventListener('click', function (e) {
          if (e.target.closest('[data-action]')) return;
          state.canvas.setActiveObject(o);
          state.canvas.renderAll();
        });
      })(obj);

      // Visibility toggle
      (function (o) {
        item.querySelector('[data-action="visibility"]').addEventListener('click', function () {
          o.visible = o.visible === false ? true : false;
          state.canvas.renderAll();
          renderLayers();
          pushHistory();
        });
      })(obj);

      // Delete
      (function (o) {
        item.querySelector('[data-action="delete"]').addEventListener('click', function () {
          pushHistory();
          state.canvas.remove(o);
          state.canvas.renderAll();
        });
      })(obj);

      list.appendChild(item);
    }

    if (objects.length === 0) {
      list.innerHTML = '<div class="tmpl-builder__no-selection">No elements yet.</div>';
    }
  }

  function getObjectIcon(obj) {
    if (isTextObject(obj)) return 'fa-font';
    if (obj.custom_type === 'clipart') return 'fa-icons';
    if (obj.custom_type === 'image') return 'fa-image';
    if (obj.custom_type === 'shape') {
      if (obj.type === 'circle') return 'fa-circle';
      return 'fa-square';
    }
    return 'fa-cube';
  }

  function getObjectLabel(obj) {
    if (isTextObject(obj)) {
      const txt = obj.text || '';
      return txt.length > 20 ? txt.substring(0, 20) + '...' : txt;
    }
    if (obj.custom_type === 'clipart') return 'Clipart';
    if (obj.custom_type === 'image') return 'Image';
    if (obj.type === 'circle') return 'Circle';
    if (obj.type === 'rect') return 'Rectangle';
    return obj.type || 'Object';
  }

  function isTextObject(obj) {
    return obj && (obj.type === 'textbox' || obj.type === 'i-text' || obj.type === 'text');
  }

  // ─── Toolbar ────────────────────────────────────────────────────────
  function bindToolbar() {
    document.getElementById('btn-undo').addEventListener('click', undo);
    document.getElementById('btn-redo').addEventListener('click', redo);
    document.getElementById('btn-zoom-in').addEventListener('click', function () {
      setZoom(state.zoom + 0.1);
    });
    document.getElementById('btn-zoom-out').addEventListener('click', function () {
      setZoom(state.zoom - 0.1);
    });
    document.getElementById('btn-delete').addEventListener('click', deleteSelected);
    document.getElementById('btn-duplicate').addEventListener('click', duplicateSelected);
  }

  function setZoom(z) {
    state.zoom = Math.max(0.3, Math.min(3, z));
    state.canvas.setZoom(state.zoom);
    state.canvas.setDimensions({
      width: state.canvas.getWidth(),
      height: state.canvas.getHeight(),
    });
    state.canvas.renderAll();
    document.getElementById('zoom-label').textContent = Math.round(state.zoom * 100) + '%';
  }

  function deleteSelected() {
    const obj = state.canvas.getActiveObject();
    if (!obj) return;
    pushHistory();
    if (obj.type === 'activeSelection') {
      obj.forEachObject(function (o) {
        state.canvas.remove(o);
      });
      state.canvas.discardActiveObject();
    } else {
      state.canvas.remove(obj);
    }
    state.canvas.renderAll();
  }

  function duplicateSelected() {
    const obj = state.canvas.getActiveObject();
    if (!obj) return;
    pushHistory();
    obj
      .clone([
        'custom_type',
        'custom_name',
        'custom_lock_position',
        'custom_lock_size',
        'custom_lock_rotation',
        'custom_lock_content',
        'custom_lock_delete',
      ])
      .then(function (cloned) {
        cloned.set({
          left: (obj.left || 0) + 20,
          top: (obj.top || 0) + 20,
        });
        state.canvas.add(cloned);
        state.canvas.setActiveObject(cloned);
        state.canvas.renderAll();
      });
  }

  // ─── Keyboard Shortcuts ─────────────────────────────────────────────
  function bindKeyboard() {
    document.addEventListener('keydown', function (e) {
      // Don't handle when typing in inputs
      if (
        e.target.tagName === 'INPUT' ||
        e.target.tagName === 'TEXTAREA' ||
        e.target.tagName === 'SELECT'
      )
        return;
      if (
        state.canvas &&
        state.canvas.getActiveObject() &&
        isTextObject(state.canvas.getActiveObject()) &&
        state.canvas.getActiveObject().isEditing
      )
        return;

      const key = e.key;
      const ctrlKey = e.ctrlKey || e.metaKey;

      if (ctrlKey && key === 'z') {
        e.preventDefault();
        undo();
      } else if (ctrlKey && key === 'y') {
        e.preventDefault();
        redo();
      } else if (ctrlKey && key === 'd') {
        e.preventDefault();
        duplicateSelected();
      } else if (key === 'Delete' || key === 'Backspace') {
        e.preventDefault();
        deleteSelected();
      } else if (key === 'Escape') {
        state.canvas.discardActiveObject();
        state.canvas.renderAll();
      } else if (
        key === 'ArrowUp' ||
        key === 'ArrowDown' ||
        key === 'ArrowLeft' ||
        key === 'ArrowRight'
      ) {
        const obj = state.canvas.getActiveObject();
        if (!obj) return;
        e.preventDefault();
        const step = e.shiftKey ? 10 : 1;
        if (key === 'ArrowUp') obj.top -= step;
        if (key === 'ArrowDown') obj.top += step;
        if (key === 'ArrowLeft') obj.left -= step;
        if (key === 'ArrowRight') obj.left += step;
        obj.setCoords();
        state.canvas.renderAll();
      }
    });
  }

  // ─── Save ───────────────────────────────────────────────────────────
  function bindSaveButtons() {
    document.getElementById('btn-save-template').addEventListener('click', function () {
      saveTemplate(false);
    });
    document.getElementById('btn-save-close').addEventListener('click', function () {
      saveTemplate(true);
    });
  }

  function saveTemplate(closeAfter) {
    if (state.saving) return;

    const name = document.getElementById('tmpl-name').value.trim();
    let slug = document.getElementById('tmpl-slug').value.trim();

    if (!name) {
      showNotification('Template name is required.', 'error');
      document.getElementById('tmpl-name').focus();
      return;
    }
    if (!slug) {
      slug = slugify(name);
      document.getElementById('tmpl-slug').value = slug;
    }

    state.saving = true;
    showNotification('Saving...', 'success');

    // Save current surface before collecting
    saveCurrentSurfaceState();

    // Build design_data
    const designData = { version: 1, surfaces: {} };
    surfaces.forEach(function (surface) {
      const ss = state.surfaceStates[surface.slug];
      designData.surfaces[surface.slug] = {
        canvas_json: ss ? ss.canvasJSON : { version: '6.0.0', objects: [] },
        canvas_width:
          ss && ss.canvasWidth ? ss.canvasWidth : state.canvas ? state.canvas.getWidth() : 500,
        canvas_height:
          ss && ss.canvasHeight ? ss.canvasHeight : state.canvas ? state.canvas.getHeight() : 500,
      };
    });

    // Capture thumbnail
    let thumbnailDataUrl = '';
    if (state.canvas && state.canvas.getObjects().length > 0) {
      thumbnailDataUrl = state.canvas.toDataURL({
        format: 'png',
        multiplier: 0.5,
      });
    }

    const body = {
      name: name,
      slug: slug,
      description: '',
      category: document.getElementById('tmpl-category').value.trim(),
      sort_order: templateData ? templateData.sort_order : 0,
      design_data: designData,
      is_active: true,
    };

    if (templateData && templateData.id) {
      body.id = templateData.id;
    }

    // Save template
    fetch(editorData.urls.saveTemplate, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(body),
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.error) {
          showNotification(data.error, 'error');
          state.saving = false;
          return;
        }

        // Update template reference for future saves
        if (data.template && data.template.id) {
          if (!templateData) {
            templateData = {
              id: data.template.id,
              name: name,
              slug: slug,
            };
            editorData.template = templateData;
          }
          templateData.id = data.template.id;
        }

        // Upload thumbnail if we have one
        if (thumbnailDataUrl && data.template) {
          saveThumbnail(data.template.id, thumbnailDataUrl);
        }

        state.dirty = false;
        showNotification('Template saved!', 'success');
        state.saving = false;

        if (closeAfter) {
          window.location.href = editorData.urls.designSetup;
        }
      })
      .catch(function (err) {
        showNotification('Save failed: ' + err.message, 'error');
        state.saving = false;
      });
  }

  function saveThumbnail(templateId, dataUrl) {
    fetch(editorData.urls.captureThumbnail, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        image_data: dataUrl,
        target_type: 'template',
        target_id: templateId,
      }),
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.success && data.asset_id) {
          // Link thumbnail to the template
          fetch(editorData.urls.saveTemplate, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
              id: templateId,
              thumbnail_asset_id: data.asset_id,
            }),
          });
        }
      })
      .catch(function () {
        // Non-critical: template saved, thumbnail failed
      });
  }

  // ─── Notifications ──────────────────────────────────────────────────
  function showNotification(msg, type) {
    AdminModal.toast(msg, type || 'info');
  }

  // ─── Utilities ──────────────────────────────────────────────────────
  function slugify(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_]+/g, '-')
      .replace(/^-+|-+$/g, '')
      .substring(0, 100);
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str || ''));
    return div.innerHTML;
  }

  function escapeAttr(str) {
    return (str || '')
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  // ─── Warn before leaving with unsaved changes ───────────────────────
  window.addEventListener('beforeunload', function (e) {
    if (state.dirty) {
      e.preventDefault();
      e.returnValue = '';
    }
  });

  // ─── Bootstrap ──────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
