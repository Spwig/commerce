/**
 * Design Editor - History Module
 * Manages undo/redo stack per surface for the design editor.
 *
 * Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0.
 */
(function () {
  'use strict';

  /* ─── Constants ──────────────────────────────────────────────────────── */
  const MAX_HISTORY = 50;

  /* ─── State ──────────────────────────────────────────────────────────── */
  let dom = null;
  let state = null;
  let activeSurfaceSlug = null;

  // Per-surface history stacks: { slug: { undoStack: [], redoStack: [] } }
  let histories = {};

  let isApplyingState = false; // Prevent recording during undo/redo

  /* ─── Initialization ─────────────────────────────────────────────────── */

  function init(sharedDom, sharedState) {
    dom = sharedDom;
    state = sharedState;
  }

  /* ─── Surface Switching ──────────────────────────────────────────────── */

  function switchSurface(slug) {
    activeSurfaceSlug = slug;

    // Initialize history for this surface if not exists
    if (!histories[slug]) {
      histories[slug] = {
        undoStack: [],
        redoStack: [],
      };

      // Record initial state
      recordState();
    }

    updateButtons();
  }

  /* ─── Record State ───────────────────────────────────────────────────── */

  function recordState() {
    if (isApplyingState) return;
    if (!activeSurfaceSlug) return;
    if (!window.DesignEditorCanvas) return;

    const history = histories[activeSurfaceSlug];
    if (!history) return;

    const currentJSON = JSON.stringify(window.DesignEditorCanvas.toJSON());

    // Don't record if state hasn't changed
    if (history.undoStack.length > 0) {
      const lastState = history.undoStack[history.undoStack.length - 1];
      if (lastState === currentJSON) return;
    }

    // Push to undo stack
    history.undoStack.push(currentJSON);

    // Trim if exceeds max
    if (history.undoStack.length > MAX_HISTORY) {
      history.undoStack.shift();
    }

    // Clear redo stack (new action invalidates redo history)
    history.redoStack = [];

    updateButtons();
  }

  /* ─── Undo ───────────────────────────────────────────────────────────── */

  function undo() {
    if (!activeSurfaceSlug) return;

    const history = histories[activeSurfaceSlug];
    if (!history || history.undoStack.length <= 1) return;

    // Move current state to redo stack
    const currentState = history.undoStack.pop();
    history.redoStack.push(currentState);

    // Apply previous state
    const previousState = history.undoStack[history.undoStack.length - 1];
    applyState(previousState);

    updateButtons();
  }

  /* ─── Redo ───────────────────────────────────────────────────────────── */

  function redo() {
    if (!activeSurfaceSlug) return;

    const history = histories[activeSurfaceSlug];
    if (!history || history.redoStack.length === 0) return;

    // Pop from redo and push to undo
    const nextState = history.redoStack.pop();
    history.undoStack.push(nextState);

    // Apply state
    applyState(nextState);

    updateButtons();
  }

  /* ─── Apply State ────────────────────────────────────────────────────── */

  function applyState(jsonString) {
    if (!window.DesignEditorCanvas) return;

    isApplyingState = true;

    try {
      const json = JSON.parse(jsonString);
      window.DesignEditorCanvas.loadFromJSON(json, function () {
        isApplyingState = false;
      });
    } catch (e) {
      console.error('[DesignEditorHistory] Failed to apply state:', e);
      isApplyingState = false;
    }
  }

  /* ─── Update UI ──────────────────────────────────────────────────────── */

  function updateButtons() {
    if (!activeSurfaceSlug) return;

    const history = histories[activeSurfaceSlug];
    if (!history) return;

    const canUndo = history.undoStack.length > 1;
    const canRedo = history.redoStack.length > 0;

    if (dom.btnUndo) dom.btnUndo.disabled = !canUndo;
    if (dom.btnRedo) dom.btnRedo.disabled = !canRedo;
  }

  /* ─── Clear History ──────────────────────────────────────────────────── */

  function clearHistory(slug) {
    if (slug) {
      delete histories[slug];
    } else {
      histories = {};
    }
    updateButtons();
  }

  /* ─── Public API ─────────────────────────────────────────────────────── */

  window.DesignEditorHistory = {
    init: init,
    switchSurface: switchSurface,
    recordState: recordState,
    undo: undo,
    redo: redo,
    clearHistory: clearHistory,
  };
})();
