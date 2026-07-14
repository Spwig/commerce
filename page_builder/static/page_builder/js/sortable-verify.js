/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
/* Verifies that Sortable.js loaded correctly before the visual builder initializes */
(function () {
  'use strict';
  if (typeof Sortable === 'undefined') {
    console.error('CRITICAL: Sortable.js failed to load! Drag and drop will not work.');
  } else {
    console.log('✅ Sortable.js loaded successfully (v' + (Sortable.version || '1.15.0') + ')');
  }
})();
