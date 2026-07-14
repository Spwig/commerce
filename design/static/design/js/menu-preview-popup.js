/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Menu Preview Popup
 * Handles device frame scaling, zoom, orientation, and keyboard shortcuts
 * for the standalone menu preview popup window.
 * Extracted from inline script in menu_builder/preview_popup.html.
 */
(function () {
  'use strict';

  // Device presets - viewport dimensions
  const PRESETS = {
    desktop: { w: 1200, h: 800, label: 'Desktop (1200\u00d7800)' },
    'tablet-portrait': { w: 768, h: 1024, label: 'Tablet Portrait (768\u00d71024)' },
    'tablet-landscape': { w: 1024, h: 768, label: 'Tablet Landscape (1024\u00d7768)' },
    'mobile-portrait': { w: 390, h: 844, label: 'Mobile Portrait (390\u00d7844)' },
    'mobile-landscape': { w: 844, h: 390, label: 'Mobile Landscape (844\u00d7390)' },
  };

  // Device chrome dimensions (borders only) - must match CSS
  const CHROME = {
    desktop: { borderWidth: 16 },
    tablet: { borderWidth: 20 },
    mobile: { borderWidth: 10 },
  };

  // State — initial device read from body data attribute (set by Django template)
  let currentDevice = document.body.dataset.initialDevice || 'desktop';
  let currentOrientation = 'portrait';
  let manualZoom = 75;
  let currentFrameWidth = 1232;
  let currentFrameHeight = 832;

  // DOM refs
  let frameWrapper, deviceFrame, menuContent, zoomSlider, zoomValue, deviceLabel;

  function applyDevice() {
    const presetKey =
      currentDevice === 'desktop' ? 'desktop' : `${currentDevice}-${currentOrientation}`;
    const preset = PRESETS[presetKey];
    const chrome = CHROME[currentDevice];
    if (!preset || !chrome) return;

    // Set content dimensions (the viewport)
    menuContent.style.width = preset.w + 'px';
    menuContent.style.height = preset.h + 'px';

    // Calculate frame dimensions: content + borders only
    currentFrameWidth = preset.w + chrome.borderWidth * 2;
    currentFrameHeight = preset.h + chrome.borderWidth * 2;

    // Set explicit frame dimensions
    deviceFrame.style.width = currentFrameWidth + 'px';
    deviceFrame.style.height = currentFrameHeight + 'px';

    // Update button states
    document.querySelectorAll('.device-buttons button[data-device]').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.device === currentDevice);
    });

    // Update frame class
    deviceFrame.className = 'device-frame ' + currentDevice;
    if (currentOrientation === 'landscape' && currentDevice !== 'desktop') {
      deviceFrame.classList.add('landscape');
    }

    // Show/hide orientation toggle
    const orientToggle = document.querySelector('.orientation-toggle');
    if (orientToggle) {
      orientToggle.classList.toggle('visible', currentDevice !== 'desktop');
      const icon = orientToggle.querySelector('i');
      if (icon) {
        icon.style.transform = currentOrientation === 'landscape' ? 'rotate(90deg)' : 'none';
      }
    }

    // Update label
    if (deviceLabel) {
      deviceLabel.textContent = preset.label;
    }

    // Fit to wrapper
    setTimeout(fitToWrapper, 10);
  }

  function fitToWrapper() {
    const bounds = frameWrapper.getBoundingClientRect();
    const padding = 60;
    const labelSpace = 80;

    const availableWidth = bounds.width - padding * 2;
    const availableHeight = bounds.height - padding * 2 - labelSpace;

    const scaleX = availableWidth / currentFrameWidth;
    const scaleY = availableHeight / currentFrameHeight;
    const autoScale = Math.min(scaleX, scaleY, 1);

    const scale = Math.max(autoScale * (manualZoom / 100), 0.15);

    deviceFrame.style.transform = 'translate(-50%, -50%) scale(' + scale + ')';
    deviceFrame.style.position = 'absolute';
    deviceFrame.style.left = '50%';
    deviceFrame.style.top = 'calc(50% - ' + labelSpace / 2 + 'px)';

    const displayZoom = Math.round(scale * 100);
    const isConstrained = autoScale < 1;
    if (zoomValue) {
      zoomValue.textContent = isConstrained ? displayZoom + '%*' : manualZoom + '%';
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    frameWrapper = document.getElementById('frame-wrapper');
    deviceFrame = document.getElementById('device-frame');
    menuContent = document.getElementById('menu-content');
    zoomSlider = document.getElementById('zoom');
    zoomValue = document.querySelector('.zoom-value');
    deviceLabel = document.querySelector('.device-label');

    // Device toggle buttons
    document.querySelectorAll('.device-buttons button[data-device]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        currentDevice = btn.dataset.device;
        if (currentDevice !== 'desktop') {
          currentOrientation = 'portrait';
        }
        applyDevice();
      });
    });

    // Orientation toggle
    const orientToggle = document.querySelector('.orientation-toggle');
    if (orientToggle) {
      orientToggle.addEventListener('click', function () {
        if (currentDevice === 'desktop') return;
        currentOrientation = currentOrientation === 'portrait' ? 'landscape' : 'portrait';
        applyDevice();
      });
    }

    // Zoom slider
    if (zoomSlider) {
      zoomSlider.addEventListener('input', function () {
        manualZoom = parseInt(zoomSlider.value);
        if (zoomValue) {
          zoomValue.textContent = manualZoom + '%';
        }
        fitToWrapper();
      });
    }

    // Close button (data-action="close-popup")
    document.addEventListener('click', function (e) {
      if (e.target.closest('[data-action="close-popup"]')) {
        window.close();
      }
      // Hamburger toggle for mobile menu preview
      const hamburger = e.target.closest('[data-action="toggle-hamburger"]');
      if (hamburger) {
        hamburger.closest('.menu-preview') &&
          hamburger.closest('.menu-preview').classList.toggle('menu-open');
      }
      // Preview-mode links — prevent navigation
      if (e.target.closest('[data-preview-link]')) {
        e.preventDefault();
      }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        window.close();
      }
      if (e.key === '1') {
        currentDevice = 'desktop';
        applyDevice();
      } else if (e.key === '2') {
        currentDevice = 'tablet';
        currentOrientation = 'portrait';
        applyDevice();
      } else if (e.key === '3') {
        currentDevice = 'mobile';
        currentOrientation = 'portrait';
        applyDevice();
      } else if ((e.key === 'r' || e.key === 'R') && currentDevice !== 'desktop') {
        currentOrientation = currentOrientation === 'portrait' ? 'landscape' : 'portrait';
        applyDevice();
      }
    });

    // Resize handler
    window.addEventListener('resize', fitToWrapper);

    // Initialize
    applyDevice();
  });
})();
