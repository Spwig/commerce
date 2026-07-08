/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Translation Integration for Page Builder
 * Simplified integration - translation editors are attached directly to translatable fields
 */

// This file is kept for backward compatibility but most functionality
// has been moved to property_renderer.js where translation editors
// are initialized directly on translatable fields

// Legacy function kept for compatibility if needed
window.openTranslationEditor = function(elementId) {
    console.warn('openTranslationEditor is deprecated. Translation editors are now attached directly to translatable fields.');
};