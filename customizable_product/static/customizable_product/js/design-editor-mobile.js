/**
 * Design Editor - Mobile Module
 * Handles touch gestures (pinch-to-zoom, two-finger rotate),
 * bottom sheet drawer, and responsive tool panel behavior.
 *
 * Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0.
 */
(function () {
    'use strict';

    /* ─── State ──────────────────────────────────────────────────────────── */
    var dom = null;
    var state = null;
    var isMobile = false;

    // Touch gesture tracking
    var touchState = {
        initialDistance: 0,
        initialAngle: 0,
        initialZoom: 1,
        initialObjAngle: 0,
        isPinching: false,
        isRotating: false,
        activeObj: null,
    };

    // Bottom sheet state
    var sheetState = {
        isDragging: false,
        startY: 0,
        currentTranslate: 0,
        expanded: false,
    };

    /* ─── Initialization ─────────────────────────────────────────────────── */

    function init(sharedDom, sharedState) {
        dom = sharedDom;
        state = sharedState;

        isMobile = window.matchMedia('(max-width: 768px)').matches || 'ontouchstart' in window;

        if (!isMobile) return;

        setupBottomSheet();
        setupTouchGestures();

        // Re-check on resize
        window.addEventListener('resize', function () {
            var wasMobile = isMobile;
            isMobile = window.matchMedia('(max-width: 768px)').matches;

            if (isMobile && !wasMobile) {
                setupBottomSheet();
            } else if (!isMobile && wasMobile) {
                teardownBottomSheet();
            }
        });
    }

    /* ─── Bottom Sheet ───────────────────────────────────────────────────── */

    function setupBottomSheet() {
        if (!dom.sheetHandle || !dom.toolsPanel) return;

        dom.sheetHandle.style.display = '';

        dom.sheetHandle.addEventListener('touchstart', onSheetTouchStart, { passive: false });
        dom.sheetHandle.addEventListener('touchmove', onSheetTouchMove, { passive: false });
        dom.sheetHandle.addEventListener('touchend', onSheetTouchEnd);

        // Tap to toggle
        dom.sheetHandle.addEventListener('click', function () {
            toggleSheet();
        });
    }

    function teardownBottomSheet() {
        if (!dom.sheetHandle) return;
        dom.sheetHandle.style.display = 'none';

        if (dom.toolsPanel) {
            dom.toolsPanel.classList.remove('expanded');
        }
    }

    function onSheetTouchStart(e) {
        sheetState.isDragging = true;
        sheetState.startY = e.touches[0].clientY;
    }

    function onSheetTouchMove(e) {
        if (!sheetState.isDragging) return;
        e.preventDefault();

        var currentY = e.touches[0].clientY;
        var diff = sheetState.startY - currentY;

        // If dragging up more than 30px, expand
        if (diff > 30 && !sheetState.expanded) {
            expandSheet();
            sheetState.isDragging = false;
        }
        // If dragging down more than 30px, collapse
        if (diff < -30 && sheetState.expanded) {
            collapseSheet();
            sheetState.isDragging = false;
        }
    }

    function onSheetTouchEnd() {
        sheetState.isDragging = false;
    }

    function toggleSheet() {
        if (sheetState.expanded) {
            collapseSheet();
        } else {
            expandSheet();
        }
    }

    function expandSheet() {
        if (!dom.toolsPanel) return;
        dom.toolsPanel.classList.add('expanded');
        sheetState.expanded = true;
    }

    function collapseSheet() {
        if (!dom.toolsPanel) return;
        dom.toolsPanel.classList.remove('expanded');
        sheetState.expanded = false;
    }

    /* ─── Touch Gestures (Pinch-to-Zoom, Two-Finger Rotate) ─────────────── */

    function setupTouchGestures() {
        if (!dom.viewport) return;

        dom.viewport.addEventListener('touchstart', onTouchStart, { passive: false });
        dom.viewport.addEventListener('touchmove', onTouchMove, { passive: false });
        dom.viewport.addEventListener('touchend', onTouchEnd);
    }

    function onTouchStart(e) {
        if (e.touches.length !== 2) return;

        var canvas = window.DesignEditorCanvas
            ? window.DesignEditorCanvas.getCanvas()
            : null;
        if (!canvas) return;

        e.preventDefault();

        var touch1 = e.touches[0];
        var touch2 = e.touches[1];

        touchState.initialDistance = getDistance(touch1, touch2);
        touchState.initialAngle = getAngle(touch1, touch2);

        var activeObj = canvas.getActiveObject();
        if (activeObj) {
            // Two-finger rotate on selected object
            touchState.isRotating = true;
            touchState.isPinching = false;
            touchState.activeObj = activeObj;
            touchState.initialObjAngle = activeObj.angle || 0;
        } else {
            // Pinch-to-zoom on canvas
            touchState.isPinching = true;
            touchState.isRotating = false;
            touchState.initialZoom = canvas.getZoom ? canvas.getZoom() : 1;
        }
    }

    function onTouchMove(e) {
        if (e.touches.length !== 2) return;
        if (!touchState.isPinching && !touchState.isRotating) return;

        e.preventDefault();

        var touch1 = e.touches[0];
        var touch2 = e.touches[1];
        var currentDistance = getDistance(touch1, touch2);

        if (touchState.isPinching) {
            // Pinch-to-zoom
            var scale = currentDistance / touchState.initialDistance;
            var newZoom = touchState.initialZoom * scale;

            if (window.DesignEditorCanvas) {
                window.DesignEditorCanvas.setZoom(newZoom);
            }
        }

        if (touchState.isRotating && touchState.activeObj) {
            // Two-finger rotate
            var currentAngle = getAngle(touch1, touch2);
            var angleDiff = currentAngle - touchState.initialAngle;
            var newAngle = touchState.initialObjAngle + angleDiff;

            if (!touchState.activeObj.lockRotation) {
                touchState.activeObj.set('angle', newAngle);
                var canvas = window.DesignEditorCanvas
                    ? window.DesignEditorCanvas.getCanvas()
                    : null;
                if (canvas) canvas.requestRenderAll();
            }
        }
    }

    function onTouchEnd(e) {
        if (touchState.isRotating && touchState.activeObj) {
            // Record rotation change for undo
            if (window.DesignEditorHistory) {
                window.DesignEditorHistory.recordState();
            }
        }

        touchState.isPinching = false;
        touchState.isRotating = false;
        touchState.activeObj = null;
    }

    /* ─── Geometry Helpers ───────────────────────────────────────────────── */

    function getDistance(touch1, touch2) {
        var dx = touch2.clientX - touch1.clientX;
        var dy = touch2.clientY - touch1.clientY;
        return Math.sqrt(dx * dx + dy * dy);
    }

    function getAngle(touch1, touch2) {
        var dx = touch2.clientX - touch1.clientX;
        var dy = touch2.clientY - touch1.clientY;
        return Math.atan2(dy, dx) * (180 / Math.PI);
    }

    /* ─── Public API ─────────────────────────────────────────────────────── */

    window.DesignEditorMobile = {
        init: init,
        expandSheet: expandSheet,
        collapseSheet: collapseSheet,
        isMobile: function () { return isMobile; },
    };
})();
