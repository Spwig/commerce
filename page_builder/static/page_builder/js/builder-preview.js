/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  const PRESETS = {
    desktop: { w: 1440, h: 900, label: 'Desktop (1440×900)' },
    'tablet-portrait': { w: 768, h: 1024, label: 'Tablet Portrait (768×1024)' },
    'tablet-landscape': { w: 1024, h: 768, label: 'Tablet Landscape (1024×768)' },
    'mobile-portrait': { w: 390, h: 844, label: 'Mobile Portrait (390×844)' },
    'mobile-landscape': { w: 844, h: 390, label: 'Mobile Landscape (844×390)' },
  };

  const iframe = document.getElementById('preview');
  const wrapper = document.getElementById('frame-wrapper');
  const zoomEl = document.getElementById('zoom');
  const zoomValue = document.querySelector('.zoom-value');
  const deviceLabel = document.querySelector('.device-label');
  const loadingIndicator = document.querySelector('.loading-indicator');
  const orientationToggle = document.querySelector('.orientation-toggle');
  const deviceFrame = document.querySelector('.device-frame');

  let currentDevice = 'desktop';
  let currentOrientation = 'portrait';
  let manualZoom = 75;

  function applyDevice() {
    const presetKey =
      currentDevice === 'desktop' ? 'desktop' : currentDevice + '-' + currentOrientation;

    const preset = PRESETS[presetKey];
    const w = preset.w,
      h = preset.h,
      label = preset.label;

    iframe.style.width = w + 'px';
    iframe.style.height = h + 'px';

    document.querySelectorAll('.device-buttons button[data-device]').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.device === currentDevice);
    });

    deviceFrame.className = 'device-frame ' + currentDevice;

    if (currentOrientation === 'landscape' && currentDevice !== 'desktop') {
      deviceFrame.classList.add('landscape');
    }

    orientationToggle.classList.toggle('visible', currentDevice !== 'desktop');

    const orientationIcon = orientationToggle.querySelector('i');
    if (orientationIcon) {
      orientationIcon.style.transform =
        currentOrientation === 'landscape' ? 'rotate(90deg)' : 'none';
    }

    deviceLabel.textContent = label;

    setTimeout(function () {
      fitToWrapper();
    }, 10);

    notifyPreview({ mode: presetKey, width: w, height: h });
  }

  function fitToWrapper() {
    const bounds = wrapper.getBoundingClientRect();
    const padding = 100;

    const iframeWidth = parseInt(iframe.style.width) || iframe.offsetWidth;
    const iframeHeight = parseInt(iframe.style.height) || iframe.offsetHeight;

    let extraWidth = 0,
      extraHeight = 0;
    if (currentDevice === 'desktop') {
      extraWidth = 32;
      extraHeight = 100;
    } else if (currentDevice === 'tablet') {
      extraWidth = 54;
      extraHeight = 48;
    } else if (currentDevice === 'mobile') {
      extraWidth = 30;
      extraHeight = 40;
    }

    const scaleX = (bounds.width - padding) / (iframeWidth + extraWidth);
    const scaleY = (bounds.height - padding) / (iframeHeight + extraHeight);
    const autoScale = Math.min(scaleX, scaleY, 1);
    const scale = autoScale * (manualZoom / 100);

    deviceFrame.style.transform = 'translate(-50%, -50%) scale(' + scale + ')';
    deviceFrame.style.position = 'absolute';
    deviceFrame.style.left = '50%';
    deviceFrame.style.top = '50%';

    const effectiveZoom = Math.round(scale * 100);
    if (effectiveZoom < manualZoom) {
      zoomValue.textContent = effectiveZoom + '%*';
    } else {
      zoomValue.textContent = manualZoom + '%';
    }
  }

  function updateZoom() {
    manualZoom = parseInt(zoomEl.value);
    zoomValue.textContent = manualZoom + '%';
    fitToWrapper();
  }

  function notifyPreview(msg) {
    try {
      if (iframe.contentWindow) {
        iframe.contentWindow.postMessage({ __builderPreview: msg }, location.origin);
      }
    } catch (e) {
      // Silently fail if cross-origin
    }
  }

  document.querySelectorAll('.device-buttons button[data-device]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      currentDevice = btn.dataset.device;
      if (currentDevice !== 'desktop') {
        currentOrientation = 'portrait';
      }
      applyDevice();
    });
  });

  orientationToggle.addEventListener('click', function () {
    currentOrientation = currentOrientation === 'portrait' ? 'landscape' : 'portrait';
    applyDevice();
  });

  zoomEl.addEventListener('input', updateZoom);

  const closeBtn = document.querySelector('[data-action="close-preview"]');
  if (closeBtn) {
    closeBtn.addEventListener('click', function () {
      window.close();
    });
  }

  let resizeTimeout;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function () {
      fitToWrapper();
    }, 100);
  });

  iframe.addEventListener('load', function () {
    loadingIndicator.classList.remove('active');
    fitToWrapper();
  });

  iframe.addEventListener('error', function () {
    loadingIndicator.innerHTML = '<div class="error-message">Failed to load preview</div>';
  });

  applyDevice();

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      window.close();
    }
    if (!e.ctrlKey && !e.altKey) {
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
      } else if (e.key === 'r' && currentDevice !== 'desktop') {
        currentOrientation = currentOrientation === 'portrait' ? 'landscape' : 'portrait';
        applyDevice();
      }
    }
  });
})();
