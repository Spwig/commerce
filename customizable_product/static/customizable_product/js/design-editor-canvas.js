/**
 * Design Editor - Canvas Module
 * Handles Fabric.js canvas setup, object management, clipping,
 * snap/alignment guides, zoom, and serialization.
 *
 * Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0.
 */
(function () {
    'use strict';

    /* ─── State ──────────────────────────────────────────────────────────── */
    var canvas = null;        // Fabric.js Canvas instance
    var dom = null;           // Shared DOM refs from main module
    var state = null;         // Shared state from main module
    var currentSurface = null;
    var zoomLevel = 1;
    var ZOOM_STEP = 0.1;
    var ZOOM_MIN = 0.5;
    var ZOOM_MAX = 3;
    var SNAP_THRESHOLD = 5;   // pixels
    var SNAP_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315, 360];
    var ANGLE_SNAP_THRESHOLD = 5; // degrees
    var clipboard = null;     // for copy/paste

    /* ─── Initialization ─────────────────────────────────────────────────── */

    function init(sharedDom, sharedState) {
        dom = sharedDom;
        state = sharedState;

        if (!dom.canvas) {
            console.error('[DesignEditorCanvas] Canvas element not found');
            return;
        }

        // Create Fabric.js canvas
        canvas = new fabric.Canvas(dom.canvas, {
            selection: true,
            preserveObjectStacking: true,
            allowTouchScrolling: false,
            stopContextMenu: true,
            fireRightClick: false,
            controlsAboveOverlay: true,
            backgroundColor: 'transparent',
        });

        // Set up event listeners
        bindCanvasEvents();

        // Handle keyboard shortcuts
        document.addEventListener('keydown', handleKeydown);
    }

    /* ─── Canvas Events ──────────────────────────────────────────────────── */

    function bindCanvasEvents() {
        canvas.on('selection:created', onSelectionChanged);
        canvas.on('selection:updated', onSelectionChanged);
        canvas.on('selection:cleared', onSelectionCleared);

        canvas.on('object:modified', onObjectModified);
        canvas.on('object:added', onObjectAdded);
        canvas.on('object:removed', onObjectRemoved);

        // Snap guides during movement
        canvas.on('object:moving', onObjectMoving);
        canvas.on('object:scaling', onObjectScaling);
        canvas.on('object:rotating', onObjectRotating);

        // Text editing events
        canvas.on('text:changed', onTextChanged);

        // Mouse wheel zoom (desktop)
        canvas.on('mouse:wheel', onMouseWheel);
    }

    function onSelectionChanged(e) {
        var obj = canvas.getActiveObject();
        if (!obj) return;

        // Enable delete button
        if (dom.btnDelete) dom.btnDelete.disabled = false;

        // Notify tools module about selection
        if (window.DesignEditorTools) {
            window.DesignEditorTools.onObjectSelected(obj);
        }
    }

    function onSelectionCleared() {
        // Disable delete button
        if (dom.btnDelete) dom.btnDelete.disabled = true;

        // Clear snap guides
        clearSnapGuides();

        // Notify tools module
        if (window.DesignEditorTools) {
            window.DesignEditorTools.onObjectDeselected();
        }
    }

    function onObjectModified(e) {
        // Record state for undo
        if (window.DesignEditorHistory) {
            window.DesignEditorHistory.recordState();
        }

        clearSnapGuides();
        debouncedPriceUpdate();
        notifyCanvasChanged();
    }

    function onObjectAdded(e) {
        // Record state for undo (delayed to avoid recording during load)
        if (state && state.isInitialized) {
            if (window.DesignEditorHistory) {
                window.DesignEditorHistory.recordState();
            }
            debouncedPriceUpdate();
            notifyCanvasChanged();
        }
    }

    function onObjectRemoved() {
        if (state && state.isInitialized) {
            if (window.DesignEditorHistory) {
                window.DesignEditorHistory.recordState();
            }
            debouncedPriceUpdate();
            notifyCanvasChanged();
        }
    }

    function notifyCanvasChanged() {
        if (window.DesignEditorTools && window.DesignEditorTools.onCanvasChanged) {
            window.DesignEditorTools.onCanvasChanged();
        }
    }

    function onTextChanged() {
        // Record text changes for undo (debounced)
        clearTimeout(onTextChanged._timer);
        onTextChanged._timer = setTimeout(function () {
            if (window.DesignEditorHistory) {
                window.DesignEditorHistory.recordState();
            }
        }, 500);
    }

    /* ─── Snap / Alignment Guides ────────────────────────────────────────── */

    function onObjectMoving(e) {
        var obj = e.target;
        if (!obj || !canvas) return;

        var canvasW = canvas.getWidth();
        var canvasH = canvas.getHeight();

        // Object bounds
        var objBound = obj.getBoundingRect(true);
        var objCenterX = objBound.left + objBound.width / 2;
        var objCenterY = objBound.top + objBound.height / 2;

        clearSnapGuides();

        // Snap to canvas center
        var centerX = canvasW / 2;
        var centerY = canvasH / 2;

        if (Math.abs(objCenterX - centerX) < SNAP_THRESHOLD) {
            obj.set('left', obj.left + (centerX - objCenterX));
            showSnapGuide('v', centerX);
        }

        if (Math.abs(objCenterY - centerY) < SNAP_THRESHOLD) {
            obj.set('top', obj.top + (centerY - objCenterY));
            showSnapGuide('h', centerY);
        }

        // Snap to canvas edges
        if (Math.abs(objBound.left) < SNAP_THRESHOLD) {
            obj.set('left', obj.left - objBound.left);
            showSnapGuide('v', 0);
        }
        if (Math.abs(objBound.top) < SNAP_THRESHOLD) {
            obj.set('top', obj.top - objBound.top);
            showSnapGuide('h', 0);
        }
        if (Math.abs(objBound.left + objBound.width - canvasW) < SNAP_THRESHOLD) {
            obj.set('left', obj.left + (canvasW - objBound.left - objBound.width));
            showSnapGuide('v', canvasW);
        }
        if (Math.abs(objBound.top + objBound.height - canvasH) < SNAP_THRESHOLD) {
            obj.set('top', obj.top + (canvasH - objBound.top - objBound.height));
            showSnapGuide('h', canvasH);
        }

        canvas.requestRenderAll();
    }

    function onObjectScaling(e) {
        // Keep objects within canvas bounds during scaling
        var obj = e.target;
        if (!obj || !canvas) return;
        constrainToCanvas(obj);
    }

    function onObjectRotating(e) {
        var obj = e.target;
        if (!obj) return;
        var angle = obj.angle % 360;
        if (angle < 0) angle += 360;

        for (var i = 0; i < SNAP_ANGLES.length; i++) {
            if (Math.abs(angle - SNAP_ANGLES[i]) < ANGLE_SNAP_THRESHOLD) {
                obj.set('angle', SNAP_ANGLES[i] % 360);
                break;
            }
        }
    }

    function showSnapGuide(direction, position) {
        if (!dom.canvasZone) return;

        var guide = document.createElement('div');
        guide.className = 'design-editor__snap-guide design-editor__snap-guide--' + direction;

        if (direction === 'h') {
            guide.style.top = position + 'px';
        } else {
            guide.style.left = position + 'px';
        }

        guide.dataset.snapGuide = 'true';
        dom.canvasZone.appendChild(guide);
    }

    function clearSnapGuides() {
        if (!dom.canvasZone) return;
        var guides = dom.canvasZone.querySelectorAll('[data-snap-guide]');
        guides.forEach(function (g) { g.parentNode.removeChild(g); });
    }

    /* ─── Object Constraint ──────────────────────────────────────────────── */

    function constrainToCanvas(obj) {
        if (!canvas) return;
        var bound = obj.getBoundingRect(true);
        var canvasW = canvas.getWidth();
        var canvasH = canvas.getHeight();

        if (bound.left < 0) obj.set('left', obj.left - bound.left);
        if (bound.top < 0) obj.set('top', obj.top - bound.top);
        if (bound.left + bound.width > canvasW) {
            obj.set('left', obj.left - (bound.left + bound.width - canvasW));
        }
        if (bound.top + bound.height > canvasH) {
            obj.set('top', obj.top - (bound.top + bound.height - canvasH));
        }
    }

    /* ─── Surface Loading ────────────────────────────────────────────────── */

    function loadSurface(surface, surfaceState) {
        currentSurface = surface;

        if (!canvas) return;

        // Set background color
        canvas.backgroundColor = surface.background_color || 'transparent';

        // Clear canvas
        canvas.clear();

        // Load saved state if available
        if (surfaceState && surfaceState.canvasJSON) {
            canvas.loadFromJSON(surfaceState.canvasJSON).then(function () {
                canvas.requestRenderAll();

                // Apply lock settings from template elements
                canvas.getObjects().forEach(function (obj) {
                    applyObjectLocks(obj);
                });
            });
        } else {
            canvas.requestRenderAll();
        }
    }

    function applyObjectLocks(obj) {
        if (!obj.custom_locked) return;

        if (obj.custom_lock_position) {
            obj.lockMovementX = true;
            obj.lockMovementY = true;
        }
        if (obj.custom_lock_size) {
            obj.lockScalingX = true;
            obj.lockScalingY = true;
        }
        if (obj.custom_lock_rotation) {
            obj.lockRotation = true;
        }
        if (obj.custom_lock_delete) {
            obj.custom_no_delete = true;
        }
        if (obj.custom_lock_content && (obj.type === 'i-text' || obj.type === 'textbox')) {
            obj.editable = false;
        }
    }

    /* ─── Resize ─────────────────────────────────────────────────────────── */

    function resize(width, height) {
        if (!canvas) return;

        var oldW = canvas.getWidth();
        var oldH = canvas.getHeight();
        canvas.setDimensions({ width: width, height: height });

        // Scale all objects proportionally if the canvas size changed significantly
        if (oldW > 0 && oldH > 0 && (Math.abs(width - oldW) > 1 || Math.abs(height - oldH) > 1)) {
            var scaleX = width / oldW;
            var scaleY = height / oldH;
            // Use uniform scale to preserve aspect ratios
            var scale = Math.min(scaleX, scaleY);

            canvas.getObjects().forEach(function (obj) {
                obj.set({
                    left: obj.left * scaleX,
                    top: obj.top * scaleY,
                    scaleX: obj.scaleX * scale,
                    scaleY: obj.scaleY * scale,
                });
                obj.setCoords();
            });
        }

        canvas.requestRenderAll();
    }

    /* ─── Zoom ───────────────────────────────────────────────────────────── */

    function zoomIn() {
        setZoom(zoomLevel + ZOOM_STEP);
    }

    function zoomOut() {
        setZoom(zoomLevel - ZOOM_STEP);
    }

    function setZoom(level) {
        zoomLevel = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, level));
        if (!canvas) return;
        canvas.setZoom(zoomLevel);
        canvas.requestRenderAll();
    }

    function onMouseWheel(opt) {
        var delta = opt.e.deltaY;
        var newZoom = zoomLevel + (delta > 0 ? -ZOOM_STEP : ZOOM_STEP);
        setZoom(newZoom);
        opt.e.preventDefault();
        opt.e.stopPropagation();
    }

    /* ─── Object Operations ──────────────────────────────────────────────── */

    function addObject(obj) {
        if (!canvas) return;
        canvas.add(obj);
        canvas.setActiveObject(obj);
        canvas.requestRenderAll();
    }

    function deleteSelected() {
        if (!canvas) return;

        var activeObjects = canvas.getActiveObjects();
        if (activeObjects.length === 0) return;

        activeObjects.forEach(function (obj) {
            // Check if object is locked from deletion
            if (obj.custom_no_delete) return;
            canvas.remove(obj);
        });

        canvas.discardActiveObject();
        canvas.requestRenderAll();
    }

    function getActiveObject() {
        return canvas ? canvas.getActiveObject() : null;
    }

    function getObjects() {
        return canvas ? canvas.getObjects() : [];
    }

    /* ─── Serialization ──────────────────────────────────────────────────── */

    function toJSON() {
        if (!canvas) return { version: '6.0.0', objects: [] };

        return canvas.toJSON([
            'custom_type',
            'custom_media_asset_id',
            'custom_locked',
            'custom_lock_position',
            'custom_lock_size',
            'custom_lock_rotation',
            'custom_lock_content',
            'custom_lock_delete',
            'custom_no_delete',
        ]);
    }

    function loadFromJSON(json, callback) {
        if (!canvas) return;
        canvas.loadFromJSON(json).then(function () {
            canvas.requestRenderAll();
            if (callback) callback();
        });
    }

    /* ─── Canvas Screenshot ──────────────────────────────────────────────── */

    function toDataURL(options) {
        if (!canvas) return '';
        return canvas.toDataURL(options || { format: 'png', quality: 0.8 });
    }

    /* ─── Keyboard Shortcuts ─────────────────────────────────────────────── */

    function handleKeydown(e) {
        // Only handle when design editor is visible and not typing in input
        if (!dom.editor || dom.editor.style.display === 'none') return;
        var tag = e.target.tagName.toLowerCase();
        if (tag === 'input' || tag === 'textarea' || tag === 'select') return;

        // Check if we're editing text on canvas
        if (canvas && canvas.getActiveObject()) {
            var activeObj = canvas.getActiveObject();
            if (activeObj.isEditing) return; // Let text editing handle keys
        }

        var ctrl = e.ctrlKey || e.metaKey;

        // Delete / Backspace
        if (e.key === 'Delete' || e.key === 'Backspace') {
            e.preventDefault();
            deleteSelected();
            return;
        }

        // Escape - deselect all
        if (e.key === 'Escape') {
            e.preventDefault();
            if (canvas) {
                canvas.discardActiveObject();
                canvas.requestRenderAll();
            }
            return;
        }

        // Ctrl+Z / Cmd+Z = Undo
        if (ctrl && e.key === 'z' && !e.shiftKey) {
            e.preventDefault();
            if (window.DesignEditorHistory) {
                window.DesignEditorHistory.undo();
            }
            return;
        }

        // Ctrl+Shift+Z / Cmd+Shift+Z = Redo
        if (ctrl && e.key === 'z' && e.shiftKey) {
            e.preventDefault();
            if (window.DesignEditorHistory) {
                window.DesignEditorHistory.redo();
            }
            return;
        }

        // Ctrl+Y / Cmd+Y = Redo
        if (ctrl && e.key === 'y') {
            e.preventDefault();
            if (window.DesignEditorHistory) {
                window.DesignEditorHistory.redo();
            }
            return;
        }

        // Ctrl+C = Copy
        if (ctrl && e.key === 'c') {
            e.preventDefault();
            copySelected();
            return;
        }

        // Ctrl+V = Paste
        if (ctrl && e.key === 'v') {
            e.preventDefault();
            pasteClipboard();
            return;
        }

        // Ctrl+D = Duplicate
        if (ctrl && e.key === 'd') {
            e.preventDefault();
            duplicateSelected();
            return;
        }

        // Ctrl+A = Select All
        if (ctrl && e.key === 'a') {
            e.preventDefault();
            selectAll();
            return;
        }

        // Arrow keys - nudge selected object
        if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].indexOf(e.key) !== -1) {
            var obj = canvas ? canvas.getActiveObject() : null;
            if (!obj) return;
            if (obj.lockMovementX && obj.lockMovementY) return;
            e.preventDefault();
            var step = e.shiftKey ? 10 : 1;
            switch (e.key) {
                case 'ArrowUp':
                    if (!obj.lockMovementY) obj.set('top', obj.top - step);
                    break;
                case 'ArrowDown':
                    if (!obj.lockMovementY) obj.set('top', obj.top + step);
                    break;
                case 'ArrowLeft':
                    if (!obj.lockMovementX) obj.set('left', obj.left - step);
                    break;
                case 'ArrowRight':
                    if (!obj.lockMovementX) obj.set('left', obj.left + step);
                    break;
            }
            obj.setCoords();
            canvas.requestRenderAll();
            if (window.DesignEditorHistory) {
                // Debounce nudge history recording
                clearTimeout(handleKeydown._nudgeTimer);
                handleKeydown._nudgeTimer = setTimeout(function () {
                    window.DesignEditorHistory.recordState();
                }, 300);
            }
        }
    }

    /* ─── Debounced Price Update ──────────────────────────────────────────── */

    var priceUpdateTimer = null;
    function debouncedPriceUpdate() {
        clearTimeout(priceUpdateTimer);
        priceUpdateTimer = setTimeout(function () {
            if (window.DesignEditor) {
                window.DesignEditor.updatePricing();
            }
        }, 1000);
    }

    /* ─── Duplicate / Copy / Paste ────────────────────────────────────────── */

    function duplicateSelected() {
        if (!canvas) return;
        var active = canvas.getActiveObject();
        if (!active) return;

        active.clone(['custom_type', 'custom_media_asset_id', 'custom_name']).then(function (cloned) {
            cloned.set({
                left: cloned.left + 20,
                top: cloned.top + 20,
            });
            canvas.add(cloned);
            canvas.setActiveObject(cloned);
            canvas.requestRenderAll();
        });
    }

    function copySelected() {
        if (!canvas) return;
        var active = canvas.getActiveObject();
        if (!active) return;

        active.clone(['custom_type', 'custom_media_asset_id', 'custom_name']).then(function (cloned) {
            clipboard = cloned;
        });
    }

    function pasteClipboard() {
        if (!canvas || !clipboard) return;

        clipboard.clone(['custom_type', 'custom_media_asset_id', 'custom_name']).then(function (cloned) {
            cloned.set({
                left: cloned.left + 20,
                top: cloned.top + 20,
                evented: true,
            });
            if (cloned.type === 'activeSelection') {
                cloned.canvas = canvas;
                cloned.forEachObject(function (obj) {
                    canvas.add(obj);
                });
                cloned.setCoords();
            } else {
                canvas.add(cloned);
            }
            // Update clipboard offset for subsequent pastes
            clipboard.left += 20;
            clipboard.top += 20;
            canvas.setActiveObject(cloned);
            canvas.requestRenderAll();
        });
    }

    function selectAll() {
        if (!canvas) return;
        var objs = canvas.getObjects();
        if (objs.length === 0) return;
        canvas.discardActiveObject();
        var sel = new fabric.ActiveSelection(objs, { canvas: canvas });
        canvas.setActiveObject(sel);
        canvas.requestRenderAll();
    }

    /* ─── Object Ordering ─────────────────────────────────────────────────── */

    function bringForward() {
        if (!canvas) return;
        var obj = canvas.getActiveObject();
        if (!obj) return;
        canvas.bringObjectForward(obj);
        canvas.requestRenderAll();
        notifyCanvasChanged();
    }

    function sendBackward() {
        if (!canvas) return;
        var obj = canvas.getActiveObject();
        if (!obj) return;
        canvas.sendObjectBackwards(obj);
        canvas.requestRenderAll();
        notifyCanvasChanged();
    }

    function bringToFront() {
        if (!canvas) return;
        var obj = canvas.getActiveObject();
        if (!obj) return;
        canvas.bringObjectToFront(obj);
        canvas.requestRenderAll();
        notifyCanvasChanged();
    }

    function sendToBack() {
        if (!canvas) return;
        var obj = canvas.getActiveObject();
        if (!obj) return;
        canvas.sendObjectToBack(obj);
        canvas.requestRenderAll();
        notifyCanvasChanged();
    }

    /* ─── Fabric.js Canvas Accessor ──────────────────────────────────────── */

    function getCanvas() {
        return canvas;
    }

    function renderAll() {
        if (canvas) canvas.requestRenderAll();
    }

    /* ─── Public API ─────────────────────────────────────────────────────── */

    window.DesignEditorCanvas = {
        init: init,
        getCanvas: getCanvas,
        loadSurface: loadSurface,
        resize: resize,
        zoomIn: zoomIn,
        zoomOut: zoomOut,
        setZoom: setZoom,
        addObject: addObject,
        deleteSelected: deleteSelected,
        duplicateSelected: duplicateSelected,
        copySelected: copySelected,
        pasteClipboard: pasteClipboard,
        selectAll: selectAll,
        bringForward: bringForward,
        sendBackward: sendBackward,
        bringToFront: bringToFront,
        sendToBack: sendToBack,
        getActiveObject: getActiveObject,
        getObjects: getObjects,
        toJSON: toJSON,
        loadFromJSON: loadFromJSON,
        toDataURL: toDataURL,
        renderAll: renderAll,
        constrainToCanvas: constrainToCanvas,
    };
})();
