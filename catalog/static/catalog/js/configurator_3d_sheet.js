/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Configurator 3D Bottom Sheet Controller
 *
 * On mobile (< 1024px), transforms the 3D configurator into a bottom sheet UX:
 * - <model-viewer> fills the viewport background (position: fixed)
 * - Configuration options live in a draggable bottom sheet with snap points
 * - Customer drags the sheet to control how much of the 3D model is visible
 *
 * On desktop (>= 1024px), this script is inert — all elements stay in their
 * original positions and the standard 2-column grid layout is used.
 */
(function () {
    'use strict';

    var MOBILE_BREAKPOINT = 1024;

    // Snap points in vh (percentage of viewport height)
    var SNAP = {
        peek: 40,
        half: 60,
        full: 90
    };

    // Velocity threshold (vh/ms) for flick-based snapping
    var FLICK_VELOCITY = 0.15;

    // DOM references
    var sheet, handle, content, sheetFooter;
    var mobileViewer, desktopLayout, desktopRight, desktopViewerContainer;
    var viewer, loading;

    // State
    var currentSnap = 'peek';
    var isDragging = false;
    var isMobileActive = false;
    var startY = 0;
    var startHeight = 0;
    var lastY = 0;
    var lastTime = 0;
    var originalCameraOrbit = null;
    var headerHeight = 0;

    function init() {
        sheet = document.getElementById('config-sheet');
        handle = document.getElementById('sheet-handle');
        content = document.getElementById('sheet-content');
        sheetFooter = document.getElementById('sheet-footer');
        mobileViewer = document.getElementById('mobile-viewer-container');
        desktopLayout = document.querySelector('.configurator-3d-desktop-layout');
        desktopRight = document.getElementById('config-wizard-desktop');
        desktopViewerContainer = document.getElementById('viewer-container');
        viewer = document.getElementById('product-3d-viewer');
        loading = document.getElementById('viewer-loading');

        if (!sheet || !handle || !content || !mobileViewer) return;

        // Listen for viewport changes
        var mql = window.matchMedia('(max-width: ' + (MOBILE_BREAKPOINT - 1) + 'px)');
        handleViewportChange(mql);
        if (mql.addEventListener) {
            mql.addEventListener('change', handleViewportChange);
        } else if (mql.addListener) {
            mql.addListener(handleViewportChange); // Safari < 14
        }

        // Handle drag on the sheet handle
        handle.addEventListener('touchstart', onHandleDragStart, { passive: true });
        handle.addEventListener('mousedown', onHandleDragStart);

        // Content scroll-to-drag delegation
        content.addEventListener('touchstart', onContentTouchStart, { passive: true });
    }

    // =========================================================================
    // Responsive Layout Switching
    // =========================================================================

    function handleViewportChange(mql) {
        var matches = typeof mql.matches !== 'undefined' ? mql.matches : mql;
        if (matches) {
            activateMobileLayout();
        } else {
            deactivateMobileLayout();
        }
    }

    function activateMobileLayout() {
        if (isMobileActive) return;
        isMobileActive = true;

        // Measure the site header so we position the viewer below it
        measureHeaderHeight();

        // Move <model-viewer> + loading to the mobile fixed background
        if (viewer && mobileViewer) {
            if (loading) mobileViewer.appendChild(loading);
            mobileViewer.appendChild(viewer);
            // On mobile, model-viewer should capture all gestures
            viewer.setAttribute('touch-action', 'none');
        }

        // Move wizard content to the sheet
        if (desktopRight && content) {
            while (desktopRight.firstChild) {
                content.appendChild(desktopRight.firstChild);
            }
        }

        // Start at peek so 3D model gets maximum visibility on load
        setSnap('peek');

        // Adjust camera orbit for mobile: use percentage-based radius
        // so model auto-frames within the smaller mobile viewport
        adjustCameraForMobile();

        // Re-measure header after announcement bar JS may have hidden it (cookie check)
        setTimeout(function () {
            var prev = headerHeight;
            measureHeaderHeight();
            if (headerHeight !== prev) {
                updateViewerPosition();
            }
        }, 300);

        // Re-measure header if announcement bar is closed by user
        observeHeaderChanges();

        // Override scrollToWizard for the bottom sheet
        window.__configuratorScrollOverride = function () {
            setSnap('half');
            if (content) content.scrollTop = 0;
        };
    }

    function measureHeaderHeight() {
        // Find the site header element — try common selectors
        var header = document.querySelector('.site-header')
            || document.querySelector('header')
            || document.querySelector('[role="banner"]');
        if (header) {
            headerHeight = header.getBoundingClientRect().bottom;
        } else {
            headerHeight = 0;
        }
    }

    function observeHeaderChanges() {
        // When announcement bar is dismissed, header shrinks — re-measure
        var announceClose = document.querySelector('.announcement-close, .announcement-bar__close, .announcement__close, [data-announcement-close]');
        if (announceClose) {
            announceClose.addEventListener('click', function () {
                setTimeout(function () {
                    measureHeaderHeight();
                    updateViewerPosition();
                }, 400); // after CSS transition
            }, { once: true });
        }
    }

    function updateViewerPosition() {
        if (!mobileViewer || !isMobileActive) return;
        mobileViewer.style.top = headerHeight + 'px';
        var sheetVh = SNAP[currentSnap];
        mobileViewer.style.height = 'calc(' + (100 - sheetVh) + 'vh - ' + headerHeight + 'px)';
    }

    function adjustCameraForMobile() {
        if (!viewer) return;

        var doAdjust = function () {
            var orbit = viewer.getAttribute('camera-orbit') || '';
            var parts = orbit.trim().split(/\s+/);
            if (parts.length >= 3 && parts[2].indexOf('%') === -1) {
                // Save original so we can restore on desktop switch
                originalCameraOrbit = orbit;
                // Replace absolute distance with auto-framing percentage
                viewer.setAttribute('camera-orbit', parts[0] + ' ' + parts[1] + ' 110%');
            }
        };

        // model-viewer may not have loaded yet (GLB is fetched async)
        if (viewer.loaded) {
            doAdjust();
        } else {
            viewer.addEventListener('load', doAdjust, { once: true });
        }
    }

    function deactivateMobileLayout() {
        if (!isMobileActive) return;
        isMobileActive = false;

        // Move model-viewer back to desktop container
        if (viewer && desktopViewerContainer) {
            if (loading) desktopViewerContainer.appendChild(loading);
            desktopViewerContainer.appendChild(viewer);
            viewer.setAttribute('touch-action', 'pan-y');
        }

        // Restore original camera orbit
        if (viewer && originalCameraOrbit) {
            viewer.setAttribute('camera-orbit', originalCameraOrbit);
            originalCameraOrbit = null;
        }

        // Move wizard content back to desktop container
        if (content && desktopRight) {
            while (content.firstChild) {
                desktopRight.appendChild(content.firstChild);
            }
        }

        // Remove scroll override
        window.__configuratorScrollOverride = null;
    }

    // =========================================================================
    // Snap Management
    // =========================================================================

    function setSnap(snapName) {
        currentSnap = snapName;
        sheet.style.height = SNAP[snapName] + 'vh';

        // Update CSS class
        sheet.classList.remove('config-sheet--peek', 'config-sheet--half', 'config-sheet--full', 'config-sheet--dragging');
        sheet.classList.add('config-sheet--' + snapName);

        // Position mobile viewer: below header, above the sheet
        if (isMobileActive) {
            updateViewerPosition();
        }
    }

    function findNearestSnap(currentVh) {
        var points = [
            { name: 'peek', vh: SNAP.peek },
            { name: 'half', vh: SNAP.half },
            { name: 'full', vh: SNAP.full }
        ];
        var nearest = points[0];
        var minDist = Math.abs(currentVh - nearest.vh);
        for (var i = 1; i < points.length; i++) {
            var dist = Math.abs(currentVh - points[i].vh);
            if (dist < minDist) {
                minDist = dist;
                nearest = points[i];
            }
        }
        return nearest.name;
    }

    function getNextSnap(direction) {
        // direction: 'up' = expand, 'down' = collapse
        var order = ['peek', 'half', 'full'];
        var idx = order.indexOf(currentSnap);
        if (direction === 'up' && idx < order.length - 1) return order[idx + 1];
        if (direction === 'down' && idx > 0) return order[idx - 1];
        return currentSnap;
    }

    // =========================================================================
    // Drag Handling — Handle Bar
    // =========================================================================

    function onHandleDragStart(e) {
        if (!isMobileActive) return;

        isDragging = true;
        var touch = e.touches ? e.touches[0] : e;
        startY = touch.clientY;
        startHeight = sheet.getBoundingClientRect().height;
        lastY = startY;
        lastTime = Date.now();

        sheet.classList.add('config-sheet--dragging');

        document.addEventListener('touchmove', onDragMove, { passive: false });
        document.addEventListener('touchend', onDragEnd);
        document.addEventListener('mousemove', onDragMove);
        document.addEventListener('mouseup', onDragEnd);

        e.preventDefault && e.type === 'mousedown' && e.preventDefault();
    }

    function onDragMove(e) {
        if (!isDragging) return;
        e.preventDefault();

        var touch = e.touches ? e.touches[0] : e;
        var deltaY = startY - touch.clientY;
        var newHeight = startHeight + deltaY;

        // Clamp
        var viewportHeight = window.innerHeight;
        var minH = viewportHeight * 0.2;
        var maxH = viewportHeight * 0.92;
        newHeight = Math.max(minH, Math.min(maxH, newHeight));

        sheet.style.height = newHeight + 'px';

        // Track velocity
        lastY = touch.clientY;
        lastTime = Date.now();
    }

    function onDragEnd(e) {
        if (!isDragging) return;
        isDragging = false;

        document.removeEventListener('touchmove', onDragMove);
        document.removeEventListener('touchend', onDragEnd);
        document.removeEventListener('mousemove', onDragMove);
        document.removeEventListener('mouseup', onDragEnd);

        sheet.classList.remove('config-sheet--dragging');

        // Calculate final position in vh
        var currentHeight = sheet.getBoundingClientRect().height;
        var viewportHeight = window.innerHeight;
        var currentVh = (currentHeight / viewportHeight) * 100;

        // Calculate velocity for flick detection
        var touch = e.changedTouches ? e.changedTouches[0] : e;
        var velocity = 0;
        if (lastTime) {
            var timeDelta = Date.now() - lastTime;
            if (timeDelta > 0 && timeDelta < 300) {
                var pixelDelta = startY - touch.clientY;
                velocity = (pixelDelta / viewportHeight * 100) / timeDelta; // vh/ms
            }
        }

        // Determine snap: flick or nearest
        var targetSnap;
        if (Math.abs(velocity) > FLICK_VELOCITY) {
            targetSnap = getNextSnap(velocity > 0 ? 'up' : 'down');
        } else {
            targetSnap = findNearestSnap(currentVh);
        }

        setSnap(targetSnap);
    }

    // =========================================================================
    // Drag Handling — Content Scroll Delegation
    // =========================================================================
    // When the sheet content is scrolled to the top and the user drags down,
    // we intercept and move the sheet instead of scrolling.

    var contentDragging = false;
    var contentStartY = 0;
    var contentStartScrollTop = 0;

    function onContentTouchStart(e) {
        if (!isMobileActive) return;
        contentStartY = e.touches[0].clientY;
        contentStartScrollTop = content.scrollTop;
        contentDragging = false;

        content.addEventListener('touchmove', onContentTouchMove, { passive: false });
        content.addEventListener('touchend', onContentTouchEnd);
    }

    function onContentTouchMove(e) {
        var currentY = e.touches[0].clientY;
        var deltaY = currentY - contentStartY;

        // User is dragging down and content is at the top
        if (deltaY > 0 && content.scrollTop <= 0 && !contentDragging) {
            contentDragging = true;
            // Start sheet drag
            startY = currentY;
            startHeight = sheet.getBoundingClientRect().height;
            lastY = currentY;
            lastTime = Date.now();
            sheet.classList.add('config-sheet--dragging');
        }

        if (contentDragging) {
            e.preventDefault();
            // Move the sheet
            var sheetDelta = startY - currentY;
            var newHeight = startHeight + sheetDelta;
            var viewportHeight = window.innerHeight;
            var minH = viewportHeight * 0.2;
            var maxH = viewportHeight * 0.92;
            newHeight = Math.max(minH, Math.min(maxH, newHeight));
            sheet.style.height = newHeight + 'px';
            lastY = currentY;
            lastTime = Date.now();
        }
    }

    function onContentTouchEnd(e) {
        content.removeEventListener('touchmove', onContentTouchMove);
        content.removeEventListener('touchend', onContentTouchEnd);

        if (contentDragging) {
            contentDragging = false;
            sheet.classList.remove('config-sheet--dragging');

            var currentHeight = sheet.getBoundingClientRect().height;
            var viewportHeight = window.innerHeight;
            var currentVh = (currentHeight / viewportHeight) * 100;

            // Velocity
            var touch = e.changedTouches ? e.changedTouches[0] : e;
            var velocity = 0;
            if (lastTime) {
                var timeDelta = Date.now() - lastTime;
                if (timeDelta > 0 && timeDelta < 300) {
                    var pixelDelta = startY - touch.clientY;
                    velocity = (pixelDelta / viewportHeight * 100) / timeDelta;
                }
            }

            var targetSnap;
            if (Math.abs(velocity) > FLICK_VELOCITY) {
                targetSnap = getNextSnap(velocity > 0 ? 'up' : 'down');
            } else {
                targetSnap = findNearestSnap(currentVh);
            }
            setSnap(targetSnap);
        }
    }

    // =========================================================================
    // Initialize
    // =========================================================================

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
