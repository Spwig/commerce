/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * AdminTabs - Unified Tab Management Utility
 * ==========================================
 * Handles tab switching, localStorage persistence, ARIA attributes,
 * error badge management, and auto-detection of panel patterns.
 *
 * Auto-loaded globally (window.AdminTabs) on every admin page.
 * Auto-initializes on DOMContentLoaded if .admin-tabs exists.
 *
 * HTML Patterns Supported (auto-detected in priority order):
 *   Pattern B: <div class="tab-panel" data-panel="{name}">           (product form etc.)
 *   Pattern D: <div class="tab-panel" id="panel-{name}">             (custom fields)
 *   Pattern C: <div class="admin-tab-content" data-tab="{name}">     (site settings)
 *   Pattern A: <div class="admin-tab-content" id="tab-{name}">       (standard)
 *
 * Usage:
 *   // Auto-init (no code needed — just have .admin-tabs on page)
 *
 *   // Manual init with options:
 *   AdminTabs.init({ storageKey: 'myPage_tab', onTabChange: fn });
 *
 *   // Programmatic API:
 *   AdminTabs.switchTo('settings');
 *   AdminTabs.getActiveTab();
 *   AdminTabs.addErrorBadge('basic', 3);
 *   AdminTabs.clearErrorBadges();
 *   AdminTabs.scanForErrors();
 */
(function () {
  'use strict';

  const PATTERNS = {
    ID_TAB: 'id-tab',
    DATA_PANEL: 'data-panel',
    DATA_TAB: 'data-tab',
    ID_PANEL: 'id-panel',
  };

  const AdminTabs = {
    _initialized: false,
    _container: null,
    _buttons: [],
    _pattern: null,
    _storageKey: null,
    _onTabChange: null,
    _activeTab: null,
    _persistHash: false,

    /**
     * Initialize tab management.
     * @param {Object} [options]
     * @param {string} [options.storageKey] - localStorage key (auto-derived if omitted)
     * @param {Element|string} [options.container] - .admin-tabs element or CSS selector
     * @param {Function} [options.onTabChange] - callback(tabName, prevTabName)
     * @param {boolean} [options.persistHash] - also update URL hash (default: false)
     * @param {boolean} [options.autoScanErrors] - auto-scan for .errorlist on init (default: true)
     * @returns {Object} AdminTabs instance
     */
    init: function (options) {
      if (this._initialized) return this;
      options = options || {};

      // Find container
      if (options.container) {
        this._container =
          typeof options.container === 'string'
            ? document.querySelector(options.container)
            : options.container;
      } else {
        this._container = document.querySelector('.admin-tabs');
      }

      if (!this._container) return this;

      // Collect buttons within this container
      this._buttons = Array.prototype.slice.call(
        this._container.querySelectorAll('.admin-tab-btn[data-tab]')
      );
      if (!this._buttons.length) return this;

      // Detect panel pattern
      this._pattern = this._detectPattern();
      if (!this._pattern) {
        return this;
      }

      // Configure
      this._storageKey = options.storageKey || this._deriveStorageKey();
      this._onTabChange = options.onTabChange || null;
      this._persistHash = options.persistHash || false;

      // Bind click handlers
      const self = this;
      this._buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          self.switchTo(btn.getAttribute('data-tab'));
        });
      });

      // Scan for errors first (takes priority for tab selection)
      let firstErrorTab = null;
      if (options.autoScanErrors !== false) {
        firstErrorTab = this.scanForErrors();
      }

      // Determine which tab to activate
      let restored = false;

      // Priority 1: Error tabs
      if (firstErrorTab) {
        restored = this.switchTo(firstErrorTab);
      }

      // Priority 2: URL hash
      if (!restored && window.location.hash) {
        const hash = window.location.hash.substring(1);
        restored = this.switchTo(hash);
      }

      // Priority 3: localStorage
      if (!restored) {
        const saved = this._restoreState();
        if (saved) {
          restored = this.switchTo(saved);
        }
      }

      // Priority 4: First visible tab (only if no tab is already active)
      if (!restored && !this._activeTab) {
        // Check if a tab is already marked active in HTML
        const activeBtn = this._container.querySelector('.admin-tab-btn.active');
        if (activeBtn) {
          this._activeTab = activeBtn.getAttribute('data-tab');
        } else {
          let firstVisible = null;
          for (let i = 0; i < this._buttons.length; i++) {
            if (!this._buttons[i].classList.contains('hidden')) {
              firstVisible = this._buttons[i];
              break;
            }
          }
          if (firstVisible) {
            this.switchTo(firstVisible.getAttribute('data-tab'));
          }
        }
      }

      this._initialized = true;
      return this;
    },

    /**
     * Switch to a specific tab by name.
     * @param {string} tabName - value of data-tab attribute
     * @returns {boolean} true if switch succeeded
     */
    switchTo: function (tabName) {
      if (!this._container) return false;

      const button = this._container.querySelector('.admin-tab-btn[data-tab="' + tabName + '"]');
      const panel = this._findPanel(tabName);

      if (!button || !panel || button.classList.contains('hidden')) {
        return false;
      }

      const prevTab = this._activeTab;

      // Deactivate all buttons
      this._buttons.forEach(function (btn) {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
      });

      // Deactivate all panels (button-mapped approach)
      this._getAllPanels().forEach(function (p) {
        if (p) p.classList.remove('active');
      });

      // Activate target
      button.classList.add('active');
      button.setAttribute('aria-selected', 'true');
      panel.classList.add('active');

      this._activeTab = tabName;

      // Persist
      this._saveState(tabName);
      if (this._persistHash) {
        history.replaceState(null, '', '#' + tabName);
      }

      // Callback
      if (this._onTabChange && tabName !== prevTab) {
        this._onTabChange(tabName, prevTab);
      }

      return true;
    },

    /**
     * Get the currently active tab name.
     * @returns {string|null}
     */
    getActiveTab: function () {
      return this._activeTab;
    },

    /**
     * Add an error count badge to a tab button.
     * @param {string} tabName
     * @param {number} count
     */
    addErrorBadge: function (tabName, count) {
      if (!this._container) return;

      const btn = this._container.querySelector('.admin-tab-btn[data-tab="' + tabName + '"]');
      if (!btn) return;

      // Remove existing badge
      const existing = btn.querySelector('.error-badge');
      if (existing) existing.remove();

      // Add new badge
      const badge = document.createElement('span');
      badge.className = 'error-badge';
      badge.textContent = count;
      btn.appendChild(badge);
      btn.classList.add('has-errors');
    },

    /**
     * Remove all error badges and .has-errors classes.
     */
    clearErrorBadges: function () {
      if (!this._container) return;

      const badges = this._container.querySelectorAll('.error-badge');
      for (let i = 0; i < badges.length; i++) {
        badges[i].remove();
      }
      this._buttons.forEach(function (btn) {
        btn.classList.remove('has-errors');
      });
    },

    /**
     * Auto-scan tab panels for .errorlist/.errors elements
     * and add badges accordingly.
     * @returns {string|null} first tab with errors, or null
     */
    scanForErrors: function () {
      if (!this._buttons.length) return null;

      this.clearErrorBadges();
      let firstErrorTab = null;
      const self = this;

      this._buttons.forEach(function (btn) {
        const tabName = btn.getAttribute('data-tab');
        const panel = self._findPanel(tabName);
        if (!panel) return;

        const errors = panel.querySelectorAll('.errorlist li, .errors, p.error');
        if (errors.length > 0) {
          self.addErrorBadge(tabName, errors.length);
          if (!firstErrorTab) firstErrorTab = tabName;
        }
      });

      return firstErrorTab;
    },

    // --- Internal methods ---

    /**
     * Auto-detect which panel pattern is in use on the page.
     */
    _detectPattern: function () {
      const firstBtn = this._buttons[0];
      if (!firstBtn) return null;
      const testName = firstBtn.getAttribute('data-tab');

      // Pattern B: [data-panel="{name}"] — check before id-based patterns
      // to avoid false positives when buttons have id="tab-{name}"
      if (document.querySelector('[data-panel="' + testName + '"]')) {
        return PATTERNS.DATA_PANEL;
      }
      // Pattern D: id="panel-{name}"
      if (document.getElementById('panel-' + testName)) {
        return PATTERNS.ID_PANEL;
      }
      // Pattern C: .admin-tab-content[data-tab="{name}"]
      if (document.querySelector('.admin-tab-content[data-tab="' + testName + '"]')) {
        return PATTERNS.DATA_TAB;
      }
      // Pattern A: id="tab-{name}" — checked last because tab buttons
      // often have id="tab-{name}" which would be a false positive
      const idTabEl = document.getElementById('tab-' + testName);
      if (idTabEl && !idTabEl.classList.contains('admin-tab-btn')) {
        return PATTERNS.ID_TAB;
      }

      return null;
    },

    /**
     * Find the panel element for a given tab name.
     */
    _findPanel: function (tabName) {
      switch (this._pattern) {
        case PATTERNS.ID_TAB:
          return document.getElementById('tab-' + tabName);
        case PATTERNS.DATA_TAB:
          return document.querySelector('.admin-tab-content[data-tab="' + tabName + '"]');
        case PATTERNS.DATA_PANEL:
          return document.querySelector('[data-panel="' + tabName + '"]');
        case PATTERNS.ID_PANEL:
          return document.getElementById('panel-' + tabName);
        default:
          return null;
      }
    },

    /**
     * Get all panels mapped to buttons (avoids cross-contamination).
     */
    _getAllPanels: function () {
      const self = this;
      return this._buttons
        .map(function (btn) {
          return self._findPanel(btn.getAttribute('data-tab'));
        })
        .filter(Boolean);
    },

    /**
     * Derive a localStorage key from the URL path.
     * /en/admin/catalog/product/123/change/ → adminTabs_catalog_product_123
     */
    _deriveStorageKey: function () {
      const parts = window.location.pathname.split('/').filter(Boolean);
      const adminIdx = parts.indexOf('admin');
      if (adminIdx >= 0 && parts.length > adminIdx + 2) {
        const app = parts[adminIdx + 1];
        const model = parts[adminIdx + 2];
        const nextPart = parts[adminIdx + 3];
        const id = nextPart && /^\d+$/.test(nextPart) ? nextPart : 'new';
        return 'adminTabs_' + app + '_' + model + '_' + id;
      }
      return 'adminTabs_' + window.location.pathname.replace(/\W+/g, '_');
    },

    /**
     * Save active tab to localStorage.
     */
    _saveState: function (tabName) {
      if (!this._storageKey) return;
      try {
        localStorage.setItem(this._storageKey, tabName);
      } catch (e) {
        // localStorage may be full or disabled
      }
    },

    /**
     * Restore active tab from localStorage.
     * @returns {string|null}
     */
    _restoreState: function () {
      if (!this._storageKey) return null;
      try {
        return localStorage.getItem(this._storageKey);
      } catch (e) {
        return null;
      }
    },
  };

  // Export globally
  window.AdminTabs = AdminTabs;

  // Auto-initialize on DOMContentLoaded if .admin-tabs exists
  document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.admin-tabs') && !AdminTabs._initialized) {
      AdminTabs.init();
    }
  });
})();
