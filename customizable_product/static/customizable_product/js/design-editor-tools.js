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
    var dom = null;
    var state = null;
    var selectedObject = null;
    var clipartPage = 1;
    var clipartCategory = '';
    var clipartSearchTimer = null;

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
        var config = state.config;

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
        var tab = document.getElementById('tool-' + toolName);
        var panel = document.getElementById('panel-tool-' + toolName);
        if (tab) tab.style.display = 'none';
        if (panel) panel.style.display = 'none';
    }

    function showToolTab(toolName) {
        var tab = document.getElementById('tool-' + toolName);
        var panel = document.getElementById('panel-tool-' + toolName);
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
        var surface = state.surfaces[state.activeSurfaceIndex];
        if (!surface) return;

        // Per-surface values are already resolved by the API (inherit logic applied server-side)
        var allowText = surface.allow_text !== undefined ? surface.allow_text : (state.config && state.config.allow_text);
        var allowImage = surface.allow_image_upload !== undefined ? surface.allow_image_upload : (state.config && state.config.allow_image_upload);
        var allowClipart = surface.allow_clipart !== undefined ? surface.allow_clipart : (state.config && state.config.allow_clipart);

        if (allowText) showToolTab('text'); else hideToolTab('text');
        if (allowImage) showToolTab('image'); else hideToolTab('image');
        if (allowClipart) showToolTab('clipart'); else hideToolTab('clipart');

        // If the currently active tool tab was hidden, switch to the first visible tab
        var activePanelHidden = false;
        var tabs = document.querySelectorAll('.design-editor__tool-tab');
        var firstVisibleTab = null;
        tabs.forEach(function(tab) {
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
        var btnAddText = document.getElementById('btn-add-text');
        if (btnAddText) {
            btnAddText.addEventListener('click', addTextObject);
        }

        // Text property controls
        var propFontFamily = document.getElementById('prop-font-family');
        var propFontSize = document.getElementById('prop-font-size');
        var propFontColor = document.getElementById('prop-font-color');
        var propBold = document.getElementById('prop-bold');
        var propItalic = document.getElementById('prop-italic');
        var propAlignLeft = document.getElementById('prop-align-left');
        var propAlignCenter = document.getElementById('prop-align-center');
        var propAlignRight = document.getElementById('prop-align-right');
        var propStrokeColor = document.getElementById('prop-stroke-color');
        var propStrokeWidth = document.getElementById('prop-stroke-width');

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

        var canvas = window.DesignEditorCanvas.getCanvas();
        if (!canvas) return;

        var centerX = canvas.getWidth() / 2;
        var centerY = canvas.getHeight() / 2;
        var textWidth = Math.round(canvas.getWidth() * 0.6);

        var text = new fabric.Textbox('Your text here', {
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

        var canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
        if (canvas) canvas.requestRenderAll();

        if (window.DesignEditorHistory) {
            window.DesignEditorHistory.recordState();
        }
    }

    function toggleTextStyle(style) {
        if (!selectedObject) return;

        if (style === 'bold') {
            var isBold = selectedObject.fontWeight === 'bold';
            selectedObject.set('fontWeight', isBold ? 'normal' : 'bold');
            var propBold = document.getElementById('prop-bold');
            if (propBold) propBold.classList.toggle('active', !isBold);
        } else if (style === 'italic') {
            var isItalic = selectedObject.fontStyle === 'italic';
            selectedObject.set('fontStyle', isItalic ? 'normal' : 'italic');
            var propItalic = document.getElementById('prop-italic');
            if (propItalic) propItalic.classList.toggle('active', !isItalic);
        }

        var canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
        if (canvas) canvas.requestRenderAll();

        if (window.DesignEditorHistory) {
            window.DesignEditorHistory.recordState();
        }
    }

    function updateAlignButtons(align) {
        ['left', 'center', 'right'].forEach(function (a) {
            var btn = document.getElementById('prop-align-' + a);
            if (btn) btn.classList.toggle('active', a === align);
        });
    }

    function populateFontSelector() {
        var select = document.getElementById('prop-font-family');
        if (!select) return;

        select.innerHTML = '';

        // System fonts first
        var systemFonts = ['Arial', 'Helvetica', 'Times New Roman', 'Georgia', 'Verdana', 'Courier New'];
        systemFonts.forEach(function (font) {
            var opt = document.createElement('option');
            opt.value = font;
            opt.textContent = font;
            select.appendChild(opt);
        });

        // Custom fonts from config
        if (state && state.fonts) {
            state.fonts.forEach(function (font) {
                var opt = document.createElement('option');
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
        var btnUpload = document.getElementById('btn-upload-image');
        var fileInput = document.getElementById('image-upload-input');

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
        var propOpacity = document.getElementById('prop-opacity');
        if (propOpacity) {
            propOpacity.addEventListener('input', function () {
                if (selectedObject && selectedObject.type === 'image') {
                    selectedObject.set('opacity', parseFloat(this.value));
                    var canvas = window.DesignEditorCanvas
                        ? window.DesignEditorCanvas.getCanvas()
                        : null;
                    if (canvas) canvas.requestRenderAll();
                }
            });
        }

        bindImageFilters();
    }

    /* ─── Image Filters ────────────────────────────────────────────────── */

    function getFilterValue(filters, filterType, prop, defaultVal) {
        for (var i = 0; i < filters.length; i++) {
            if (filters[i].type === filterType) return filters[i][prop];
        }
        return defaultVal;
    }

    function applyImageFilter(filterType, options) {
        if (!selectedObject || selectedObject.type !== 'image') return;

        // Remove existing filter of this type
        var filters = selectedObject.filters || [];
        selectedObject.filters = filters.filter(function (f) {
            return f.type !== filterType;
        });

        // Add new filter if non-default value
        if (options && options._active !== false) {
            var FilterClass = fabric.filters[filterType];
            if (FilterClass) {
                var filterOpts = {};
                for (var key in options) {
                    if (key !== '_active') filterOpts[key] = options[key];
                }
                selectedObject.filters.push(new FilterClass(filterOpts));
            }
        }

        selectedObject.applyFilters();
        var canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
        if (canvas) canvas.requestRenderAll();
        if (window.DesignEditorHistory) window.DesignEditorHistory.recordState();
    }

    function setImageTransform(prop, value) {
        if (!selectedObject || selectedObject.type !== 'image') return;
        selectedObject.set(prop, value);
        selectedObject.setCoords();
        var canvas = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas() : null;
        if (canvas) canvas.requestRenderAll();
        if (window.DesignEditorHistory) window.DesignEditorHistory.recordState();
    }

    function bindImageFilters() {
        // Brightness
        var propBrightness = document.getElementById('prop-brightness');
        if (propBrightness) {
            propBrightness.addEventListener('input', function () {
                var val = parseFloat(this.value);
                applyImageFilter('Brightness', {
                    brightness: val,
                    _active: val !== 0,
                });
            });
        }

        // Contrast
        var propContrast = document.getElementById('prop-contrast');
        if (propContrast) {
            propContrast.addEventListener('input', function () {
                var val = parseFloat(this.value);
                applyImageFilter('Contrast', {
                    contrast: val,
                    _active: val !== 0,
                });
            });
        }

        // Saturation
        var propSaturation = document.getElementById('prop-saturation');
        if (propSaturation) {
            propSaturation.addEventListener('input', function () {
                var val = parseFloat(this.value);
                applyImageFilter('Saturation', {
                    saturation: val,
                    _active: val !== 0,
                });
            });
        }

        // Tint (BlendColor)
        var propTintColor = document.getElementById('prop-tint-color');
        var propTintAlpha = document.getElementById('prop-tint-alpha');
        function applyTint() {
            if (!propTintColor || !propTintAlpha) return;
            var alpha = parseFloat(propTintAlpha.value);
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
        var propRemoveColor = document.getElementById('prop-remove-color');
        var propRemoveDistance = document.getElementById('prop-remove-distance');
        function applyRemoveColor() {
            if (!propRemoveColor || !propRemoveDistance) return;
            var distance = parseFloat(propRemoveDistance.value);
            applyImageFilter('RemoveColor', {
                color: propRemoveColor.value,
                distance: distance,
                _active: distance > 0,
            });
        }
        if (propRemoveColor) propRemoveColor.addEventListener('input', applyRemoveColor);
        if (propRemoveDistance) propRemoveDistance.addEventListener('input', applyRemoveColor);

        // Rotation (direct angle)
        var propRotation = document.getElementById('prop-rotation');
        if (propRotation) {
            propRotation.addEventListener('change', function () {
                setImageTransform('angle', parseFloat(this.value) || 0);
            });
        }

        // Rotate 90° CW
        var propRotateCW = document.getElementById('prop-rotate-cw');
        if (propRotateCW) {
            propRotateCW.addEventListener('click', function () {
                if (!selectedObject) return;
                var newAngle = ((selectedObject.angle || 0) + 90) % 360;
                setImageTransform('angle', newAngle);
                var el = document.getElementById('prop-rotation');
                if (el) el.value = Math.round(newAngle);
            });
        }

        // Rotate 90° CCW
        var propRotateCCW = document.getElementById('prop-rotate-ccw');
        if (propRotateCCW) {
            propRotateCCW.addEventListener('click', function () {
                if (!selectedObject) return;
                var newAngle = ((selectedObject.angle || 0) - 90 + 360) % 360;
                setImageTransform('angle', newAngle);
                var el = document.getElementById('prop-rotation');
                if (el) el.value = Math.round(newAngle);
            });
        }

        // Flip Horizontal
        var propFlipH = document.getElementById('prop-flip-h');
        if (propFlipH) {
            propFlipH.addEventListener('click', function () {
                if (!selectedObject) return;
                setImageTransform('flipX', !selectedObject.flipX);
            });
        }

        // Flip Vertical
        var propFlipV = document.getElementById('prop-flip-v');
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
        var maxSize = (state.config && state.config.max_upload_size_mb) || 10;
        if (file.size > maxSize * 1024 * 1024) {
            window.DesignEditor.showNotification(
                'File too large. Maximum size: ' + maxSize + 'MB',
                'error'
            );
            return;
        }

        var formData = new FormData();
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

        var canvas = window.DesignEditorCanvas.getCanvas();
        if (!canvas) return;

        fabric.Image.fromURL(url, { crossOrigin: 'anonymous' }).then(function (img) {
            if (!img) return;

            // Scale image to fit within canvas bounds
            var canvasW = canvas.getWidth();
            var canvasH = canvas.getHeight();
            var maxDim = Math.min(canvasW, canvasH) * 0.6;

            var scale = 1;
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
        var surface = state.surfaces[state.activeSurfaceIndex];
        if (!surface || !surface.width || !surface.height) return;
        if (surface.dimension_unit === 'px') return; // DPI only relevant for physical units

        // Convert physical dimensions to inches
        var widthInches, heightInches;
        if (surface.dimension_unit === 'mm') {
            widthInches = parseFloat(surface.width) / 25.4;
            heightInches = parseFloat(surface.height) / 25.4;
        } else {
            widthInches = parseFloat(surface.width);
            heightInches = parseFloat(surface.height);
        }

        // Calculate effective DPI for the image at its current scale
        var imgPixelWidth = img.width * scale;
        var imgPixelHeight = img.height * scale;
        var canvasW = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas().getWidth() : 500;
        var canvasH = window.DesignEditorCanvas ? window.DesignEditorCanvas.getCanvas().getHeight() : 500;

        // How much of the surface does the image cover?
        var coverageX = imgPixelWidth / canvasW;
        var coverageY = imgPixelHeight / canvasH;

        // Effective DPI = original pixels / (physical size of coverage area in inches)
        var effectiveDpiX = img.width / (widthInches * coverageX);
        var effectiveDpiY = img.height / (heightInches * coverageY);
        var effectiveDpi = Math.min(effectiveDpiX, effectiveDpiY);

        var minDpi = surface.min_dpi || 150;
        var recDpi = surface.recommended_dpi || 300;

        if (effectiveDpi < minDpi) {
            showDpiWarning('Low resolution (' + Math.round(effectiveDpi) + ' DPI). Minimum: ' + minDpi + ' DPI', true);
        } else if (effectiveDpi < recDpi) {
            showDpiWarning('Medium resolution (' + Math.round(effectiveDpi) + ' DPI). Recommended: ' + recDpi + ' DPI', false);
        }
    }

    function showDpiWarning(message, isCritical) {
        // Remove any existing warning
        var existing = document.querySelector('.design-editor__dpi-warning');
        if (existing) existing.remove();

        var viewport = document.getElementById('design-editor-viewport');
        if (!viewport) return;

        var warning = document.createElement('div');
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
        var viewport = document.getElementById('design-editor-viewport');
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

            var files = e.dataTransfer && e.dataTransfer.files;
            if (files && files.length > 0) {
                var file = files[0];
                // Validate it's an allowed raster image (no SVG - XSS risk)
                var allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
                if (file.type && allowedTypes.indexOf(file.type) !== -1) {
                    uploadImage(file);
                }
            }
        });
    }

    /* ─── Clipart Browser ────────────────────────────────────────────────── */

    function bindClipartTool() {
        renderClipartCategories();

        var searchInput = document.getElementById('clipart-search');
        if (searchInput) {
            searchInput.addEventListener('input', function () {
                clearTimeout(clipartSearchTimer);
                var query = this.value;
                clipartSearchTimer = setTimeout(function () {
                    loadClipart(clipartCategory, query);
                }, 300);
            });
        }
    }

    function renderClipartCategories() {
        var container = document.getElementById('clipart-categories');
        if (!container || !state) return;

        container.innerHTML = '';

        // "All" button
        var allBtn = document.createElement('button');
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
            var btn = document.createElement('button');
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
        var container = document.getElementById('clipart-categories');
        if (!container) return;
        container.querySelectorAll('.design-editor__clipart-cat-btn').forEach(function (btn) {
            btn.classList.remove('active');
        });
        activeBtn.classList.add('active');
    }

    function loadClipart(category, search) {
        if (!window.DesignEditor) return;

        var url = 'clipart/?product_id=' + state.productId;
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
        var grid = document.getElementById('clipart-grid');
        if (!grid) return;

        grid.innerHTML = '';

        if (clipartItems.length === 0) {
            grid.innerHTML = '<div class="design-editor__empty" style="grid-column:1/-1;padding:1rem;">' +
                '<i class="fas fa-icons"></i><p style="margin:0;font-size:0.75rem;">No clipart found</p></div>';
            return;
        }

        clipartItems.forEach(function (item) {
            var div = document.createElement('div');
            div.className = 'design-editor__clipart-item';
            div.title = item.name;

            var img = document.createElement('img');
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

        var canvas = window.DesignEditorCanvas.getCanvas();
        if (!canvas) return;

        fabric.Image.fromURL(url, { crossOrigin: 'anonymous' }).then(function (img) {
            if (!img) return;

            var canvasW = canvas.getWidth();
            var canvasH = canvas.getHeight();
            var maxDim = Math.min(canvasW, canvasH) * 0.3;

            var scale = 1;
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
        var grid = document.getElementById('template-grid');
        if (!grid || !state) return;

        var templates = state.templates || [];
        grid.innerHTML = '';

        if (templates.length === 0) {
            grid.innerHTML = '<div class="design-editor__empty" style="grid-column:1/-1;padding:1rem;">' +
                '<i class="fas fa-palette"></i><p style="margin:0;font-size:0.75rem;">No templates available</p></div>';
            return;
        }

        templates.forEach(function (template) {
            var card = document.createElement('div');
            card.className = 'design-editor__template-card';

            if (template.thumbnail_url) {
                var img = document.createElement('img');
                img.src = template.thumbnail_url;
                img.alt = template.name;
                img.loading = 'lazy';
                card.appendChild(img);
            }

            var name = document.createElement('div');
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
        if (!await AdminModal.confirm('Apply this template? Your current design will be replaced.')) return;

        var surfacesData = template.design_data.surfaces || {};

        // Load template data into surface states
        Object.keys(surfacesData).forEach(function (slug) {
            var sd = surfacesData[slug];
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
        var list = document.getElementById('layers-list');
        if (!list || !window.DesignEditorCanvas) return;

        var canvas = window.DesignEditorCanvas.getCanvas();
        if (!canvas) return;

        list.innerHTML = '';
        var objects = canvas.getObjects();
        var activeObj = canvas.getActiveObject();

        if (objects.length === 0) {
            list.innerHTML = '<div class="design-editor__empty" style="padding:1rem;">' +
                '<p style="margin:0;font-size:0.75rem;">No elements yet</p></div>';
            return;
        }

        // Render in reverse z-order (top layer first)
        for (var i = objects.length - 1; i >= 0; i--) {
            var obj = objects[i];
            var item = document.createElement('div');
            item.className = 'design-editor__layer-item' + (obj === activeObj ? ' active' : '');

            var icon = getLayerIcon(obj);
            var label = getLayerLabel(obj);

            item.innerHTML =
                '<span class="design-editor__layer-icon"><i class="fas ' + icon + '"></i></span>' +
                '<span class="design-editor__layer-name">' + escapeHtml(label) + '</span>' +
                '<div class="design-editor__layer-actions">' +
                    '<button type="button" class="design-editor__layer-btn" data-action="visibility" title="Toggle visibility">' +
                        '<i class="fas ' + (obj.visible === false ? 'fa-eye-slash' : 'fa-eye') + '"></i>' +
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
        var t = obj.type;
        if (t === 'textbox' || t === 'i-text' || t === 'text') return 'fa-font';
        if (obj.custom_type === 'clipart') return 'fa-icons';
        if (t === 'image') return 'fa-image';
        return 'fa-cube';
    }

    function getLayerLabel(obj) {
        var t = obj.type;
        if (t === 'textbox' || t === 'i-text' || t === 'text') {
            var txt = obj.text || '';
            return txt.length > 18 ? txt.substring(0, 18) + '...' : (txt || 'Text');
        }
        if (obj.custom_type === 'clipart') return 'Clipart';
        if (t === 'image') return 'Image';
        return obj.type || 'Object';
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
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
        var btnDuplicate = document.getElementById('btn-duplicate');
        if (btnDuplicate) btnDuplicate.disabled = false;

        renderLayersPanel();
    }

    function onObjectDeselected() {
        selectedObject = null;
        hideAllProperties();

        var btnDuplicate = document.getElementById('btn-duplicate');
        if (btnDuplicate) btnDuplicate.disabled = true;

        renderLayersPanel();
    }

    function onCanvasChanged() {
        renderLayersPanel();
    }

    function showTextProperties(obj) {
        var panel = document.getElementById('text-properties');
        if (!panel) return;
        panel.style.display = '';

        // Update controls to match object state
        var propFontFamily = document.getElementById('prop-font-family');
        var propFontSize = document.getElementById('prop-font-size');
        var propFontColor = document.getElementById('prop-font-color');
        var propBold = document.getElementById('prop-bold');
        var propItalic = document.getElementById('prop-italic');
        var propStrokeColor = document.getElementById('prop-stroke-color');
        var propStrokeWidth = document.getElementById('prop-stroke-width');

        if (propFontFamily) propFontFamily.value = obj.fontFamily || 'Arial';
        if (propFontSize) propFontSize.value = obj.fontSize || 24;
        if (propFontColor) propFontColor.value = obj.fill || '#000000';
        if (propBold) propBold.classList.toggle('active', obj.fontWeight === 'bold');
        if (propItalic) propItalic.classList.toggle('active', obj.fontStyle === 'italic');
        if (propStrokeColor) propStrokeColor.value = obj.stroke || '#ffffff';
        if (propStrokeWidth) propStrokeWidth.value = obj.strokeWidth || 0;

        updateAlignButtons(obj.textAlign || 'left');

        // Hide image properties
        var imgPanel = document.getElementById('image-properties');
        if (imgPanel) imgPanel.style.display = 'none';
    }

    function showImageProperties(obj) {
        var panel = document.getElementById('image-properties');
        if (!panel) return;
        panel.style.display = '';

        // Opacity
        var propOpacity = document.getElementById('prop-opacity');
        if (propOpacity) propOpacity.value = obj.opacity !== undefined ? obj.opacity : 1;

        // Read current filter values
        var filters = obj.filters || [];
        var brightness = getFilterValue(filters, 'Brightness', 'brightness', 0);
        var contrast = getFilterValue(filters, 'Contrast', 'contrast', 0);
        var saturation = getFilterValue(filters, 'Saturation', 'saturation', 0);

        var propBrightness = document.getElementById('prop-brightness');
        if (propBrightness) propBrightness.value = brightness;

        var propContrast = document.getElementById('prop-contrast');
        if (propContrast) propContrast.value = contrast;

        var propSaturation = document.getElementById('prop-saturation');
        if (propSaturation) propSaturation.value = saturation;

        // Tint (BlendColor)
        var tintColor = '#ff0000';
        var tintAlpha = 0;
        for (var i = 0; i < filters.length; i++) {
            if (filters[i].type === 'BlendColor') {
                tintColor = filters[i].color || '#ff0000';
                tintAlpha = filters[i].alpha || 0;
                break;
            }
        }
        var propTintColor = document.getElementById('prop-tint-color');
        var propTintAlpha = document.getElementById('prop-tint-alpha');
        if (propTintColor) propTintColor.value = tintColor;
        if (propTintAlpha) propTintAlpha.value = tintAlpha;

        // Remove Color
        var removeColor = '#ffffff';
        var removeDistance = 0;
        for (var j = 0; j < filters.length; j++) {
            if (filters[j].type === 'RemoveColor') {
                removeColor = filters[j].color || '#ffffff';
                removeDistance = filters[j].distance || 0;
                break;
            }
        }
        var propRemoveColor = document.getElementById('prop-remove-color');
        var propRemoveDistance = document.getElementById('prop-remove-distance');
        if (propRemoveColor) propRemoveColor.value = removeColor;
        if (propRemoveDistance) propRemoveDistance.value = removeDistance;

        // Rotation
        var propRotation = document.getElementById('prop-rotation');
        if (propRotation) propRotation.value = Math.round(obj.angle || 0);

        // Hide text properties
        var textPanel = document.getElementById('text-properties');
        if (textPanel) textPanel.style.display = 'none';
    }

    function hideAllProperties() {
        var textPanel = document.getElementById('text-properties');
        var imagePanel = document.getElementById('image-properties');
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
