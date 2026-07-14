/**
 * Design Editor - Main Module
 * Initializes the visual product design editor, manages surfaces, state,
 * and coordinates between canvas, tools, and history modules.
 *
 * Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0.
 */
(function () {
  'use strict';

  /* ─── Constants ──────────────────────────────────────────────────────── */
  const API_BASE = '/api/customizable-product/';
  const AUTOSAVE_KEY_PREFIX = 'spwig_design_';
  const AUTOSAVE_INTERVAL = 10000; // 10 seconds

  /* ─── State ──────────────────────────────────────────────────────────── */
  const state = {
    productId: null,
    config: null, // Full editor config from API
    surfaces: [], // Surface definitions
    activeSurfaceIndex: 0, // Currently active surface
    surfaceStates: {}, // { slug: { canvasJSON, dirty } }
    fonts: [], // Loaded fonts
    clipartCategories: [], // Clipart category list
    templates: [], // Design templates
    pricing: null, // Current pricing config
    designToken: null, // Token from prepare-for-cart
    isAuthenticated: false, // Whether user is logged in
    isInitialized: false,
    isLoading: true,
    currencySymbol: '$',
  };

  /* ─── DOM References ─────────────────────────────────────────────────── */
  const dom = {};

  function cacheDom() {
    dom.editor = document.getElementById('design-editor');
    if (!dom.editor) return false;

    dom.surfacesContainer = document.getElementById('design-editor-surfaces');
    dom.viewport = document.getElementById('design-editor-viewport');
    dom.mockupContainer = document.getElementById('design-editor-mockup');
    dom.mockupImg = document.getElementById('design-editor-mockup-img');
    dom.canvasZone = document.getElementById('design-editor-zone');
    dom.canvas = document.getElementById('design-editor-canvas');
    dom.toolbar = document.getElementById('design-editor-toolbar');
    dom.toolsPanel = document.getElementById('design-editor-tools');
    dom.priceTotal = document.getElementById('design-price-total');
    dom.sheetHandle = document.getElementById('design-editor-sheet-handle');

    // Toolbar buttons
    dom.btnUndo = document.getElementById('btn-undo');
    dom.btnRedo = document.getElementById('btn-redo');
    dom.btnZoomIn = document.getElementById('btn-zoom-in');
    dom.btnZoomOut = document.getElementById('btn-zoom-out');
    dom.btnDelete = document.getElementById('btn-delete');
    dom.btnDuplicate = document.getElementById('btn-duplicate');
    dom.btnFullscreen = document.getElementById('btn-fullscreen');

    // Tool tabs
    dom.toolTabs = dom.toolsPanel
      ? dom.toolsPanel.querySelectorAll('.design-editor__tool-tab')
      : [];
    dom.toolPanels = dom.toolsPanel
      ? dom.toolsPanel.querySelectorAll('.design-editor__tool-panel')
      : [];

    // Save/Load
    dom.btnSaveDesign = document.getElementById('btn-save-design');
    dom.btnLoadDesign = document.getElementById('btn-load-design');

    return true;
  }

  /* ─── API Helpers ────────────────────────────────────────────────────── */

  function getCsrfToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input) return input.value;
    return '';
  }

  function apiRequest(url, options) {
    options = options || {};
    const method = (options.method || 'GET').toUpperCase();
    const headers = { 'X-Requested-With': 'XMLHttpRequest' };

    if (method !== 'GET') {
      headers['X-CSRFToken'] = getCsrfToken();
    }

    const fetchOptions = {
      method: method,
      headers: headers,
      credentials: 'same-origin',
    };

    if (options.body) {
      if (options.body instanceof FormData) {
        fetchOptions.body = options.body;
      } else {
        headers['Content-Type'] = 'application/json';
        fetchOptions.body = JSON.stringify(options.body);
      }
    }

    fetchOptions.headers = headers;

    return fetch(API_BASE + url, fetchOptions).then(function (resp) {
      if (!resp.ok) {
        return resp.text().then(function (text) {
          throw new Error('API error ' + resp.status + ': ' + text);
        });
      }
      return resp.json();
    });
  }

  /* ─── Initialization ─────────────────────────────────────────────────── */

  function init() {
    if (!cacheDom()) return;

    state.productId = parseInt(dom.editor.dataset.productId, 10);
    if (!state.productId) return;

    state.isAuthenticated = dom.editor.dataset.authenticated === 'true';

    // Get currency symbol from the page
    const priceEl = dom.priceTotal;
    if (priceEl) {
      const text = priceEl.textContent.trim();
      state.currencySymbol = text.replace(/[\d.,]/g, '').trim() || '$';
    }

    // Show editor, start loading
    dom.editor.style.display = '';
    showLoading(true);

    // Load editor config from API
    apiRequest(state.productId + '/config/')
      .then(function (data) {
        state.config = data;
        state.surfaces = data.surfaces || [];
        state.fonts = data.fonts || [];
        state.clipartCategories = data.clipart_categories || [];
        state.templates = data.templates || [];
        state.pricing = data.pricing || {};

        if (state.surfaces.length === 0) {
          showEmptyState();
          return;
        }

        renderSurfaceTabs();
        loadFonts();
        bindToolbarEvents();
        bindToolTabEvents();
        bindSaveLoadEvents();

        // Initialize canvas module
        if (window.DesignEditorCanvas) {
          window.DesignEditorCanvas.init(dom, state);
        }

        // Initialize tools module
        if (window.DesignEditorTools) {
          window.DesignEditorTools.init(dom, state);
        }

        // Initialize history module
        if (window.DesignEditorHistory) {
          window.DesignEditorHistory.init(dom, state);
        }

        // Initialize mobile module
        if (window.DesignEditorMobile) {
          window.DesignEditorMobile.init(dom, state);
        }

        // Restore autosaved state if available
        restoreAutosave();

        // Switch to first surface
        switchSurface(0);

        // Start autosave timer
        setInterval(autosave, AUTOSAVE_INTERVAL);

        state.isInitialized = true;
        showLoading(false);
      })
      .catch(function (err) {
        console.error('[DesignEditor] Failed to load config:', err);
        showEmptyState();
      });
  }

  /* ─── Surface Management ─────────────────────────────────────────────── */

  function renderSurfaceTabs() {
    if (!dom.surfacesContainer) return;
    dom.surfacesContainer.innerHTML = '';

    state.surfaces.forEach(function (surface, index) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'design-editor__surface-tab' + (index === 0 ? ' active' : '');
      btn.dataset.index = index;

      if (surface.mockup_url) {
        const img = document.createElement('img');
        img.src = surface.mockup_url;
        img.alt = surface.name;
        img.className = 'design-editor__surface-tab__icon';
        btn.appendChild(img);
      }

      const span = document.createElement('span');
      span.textContent = surface.name;
      btn.appendChild(span);

      btn.addEventListener('click', function () {
        switchSurface(index);
      });

      dom.surfacesContainer.appendChild(btn);
    });
  }

  function switchSurface(index) {
    if (index < 0 || index >= state.surfaces.length) return;

    // Save current surface state before switching
    saveCurrentSurfaceState();

    // Update active tab
    const tabs = dom.surfacesContainer.querySelectorAll('.design-editor__surface-tab');
    tabs.forEach(function (tab, i) {
      tab.classList.toggle('active', i === index);
    });

    state.activeSurfaceIndex = index;
    const surface = state.surfaces[index];

    // Position canvas zone first, THEN load surface state.
    // This order is critical: resize() scales existing objects, so we must
    // resize before loading new objects to avoid double-scaling.
    const loadAfterPosition = function () {
      positionCanvasZone(surface);

      if (window.DesignEditorCanvas) {
        const surfaceState = state.surfaceStates[surface.slug];
        window.DesignEditorCanvas.loadSurface(surface, surfaceState);
      }

      if (window.DesignEditorHistory) {
        window.DesignEditorHistory.switchSurface(surface.slug);
      }

      if (window.DesignEditorTools && window.DesignEditorTools.enforcePerSurfaceToggles) {
        window.DesignEditorTools.enforcePerSurfaceToggles();
      }
    };

    // Update mockup image, then position + load once image is ready
    if (dom.mockupImg && surface.mockup_url) {
      dom.mockupImg.src = surface.mockup_url;
      dom.mockupImg.alt = surface.name;

      if (dom.mockupImg.complete && dom.mockupImg.naturalWidth) {
        loadAfterPosition();
      } else {
        dom.mockupImg.onload = loadAfterPosition;
      }
    } else {
      loadAfterPosition();
    }
  }

  function positionCanvasZone(surface) {
    if (!dom.canvasZone || !dom.mockupImg) return;

    const imgRect = dom.mockupImg.getBoundingClientRect();
    const containerRect = dom.mockupContainer.getBoundingClientRect();

    // Calculate the actual rendered size of the image (accounting for object-fit: contain)
    const naturalW = dom.mockupImg.naturalWidth;
    const naturalH = dom.mockupImg.naturalHeight;
    const containerW = imgRect.width;
    const containerH = imgRect.height;

    const scale = Math.min(containerW / naturalW, containerH / naturalH);
    const renderedW = naturalW * scale;
    const renderedH = naturalH * scale;

    // Offset from container edge to where the image actually starts
    const offsetX = (containerW - renderedW) / 2 + (imgRect.left - containerRect.left);
    const offsetY = (containerH - renderedH) / 2 + (imgRect.top - containerRect.top);

    // Position canvas zone using surface percentages
    const zoneX = offsetX + (surface.area_x_percent / 100) * renderedW;
    const zoneY = offsetY + (surface.area_y_percent / 100) * renderedH;
    const zoneW = (surface.area_width_percent / 100) * renderedW;
    const zoneH = (surface.area_height_percent / 100) * renderedH;

    dom.canvasZone.style.left = zoneX + 'px';
    dom.canvasZone.style.top = zoneY + 'px';
    dom.canvasZone.style.width = zoneW + 'px';
    dom.canvasZone.style.height = zoneH + 'px';

    // Resize Fabric.js canvas to match zone
    if (window.DesignEditorCanvas) {
      window.DesignEditorCanvas.resize(Math.round(zoneW), Math.round(zoneH));
    }
  }

  /* ─── Fullscreen ──────────────────────────────────────────────────────── */

  function toggleFullscreen() {
    const isFullscreen = dom.editor.classList.toggle('design-editor--fullscreen');
    const icon = dom.btnFullscreen.querySelector('i');
    if (icon) {
      icon.className = isFullscreen ? 'fas fa-compress' : 'fas fa-expand';
    }
    document.body.style.overflow = isFullscreen ? 'hidden' : '';

    // Reposition canvas after layout reflow (mockup image resizes)
    const repositionCanvas = function () {
      const surface = state.surfaces[state.activeSurfaceIndex];
      if (surface) positionCanvasZone(surface);
    };
    // First pass after DOM reflow
    requestAnimationFrame(function () {
      requestAnimationFrame(repositionCanvas);
    });
  }

  /* ─── State Management ───────────────────────────────────────────────── */

  function saveCurrentSurfaceState() {
    if (!state.isInitialized) return;
    const surface = state.surfaces[state.activeSurfaceIndex];
    if (!surface) return;

    if (window.DesignEditorCanvas) {
      const c = window.DesignEditorCanvas.getCanvas();
      state.surfaceStates[surface.slug] = {
        canvasJSON: window.DesignEditorCanvas.toJSON(),
        canvasWidth: c ? c.getWidth() : 0,
        canvasHeight: c ? c.getHeight() : 0,
        dirty: true,
      };
    }
  }

  function getFullDesignState() {
    // Make sure current surface is saved
    saveCurrentSurfaceState();

    const surfaces = {};
    state.surfaces.forEach(function (surface) {
      const ss = state.surfaceStates[surface.slug];
      const canvasJSON = ss ? ss.canvasJSON : { version: '6.0.0', objects: [] };

      // Read per-surface canvas dimensions stored by saveCurrentSurfaceState
      const canvasW = ss && ss.canvasWidth ? ss.canvasWidth : 0;
      const canvasH = ss && ss.canvasHeight ? ss.canvasHeight : 0;

      surfaces[surface.slug] = {
        canvas_json: canvasJSON,
        canvas_width: canvasW,
        canvas_height: canvasH,
        thumbnail_asset_id: null,
      };
    });

    return {
      version: '1.0',
      product_id: state.productId,
      surfaces: surfaces,
    };
  }

  /* ─── Autosave (localStorage) ────────────────────────────────────────── */

  function getAutosaveKey() {
    return AUTOSAVE_KEY_PREFIX + state.productId;
  }

  function autosave() {
    if (!state.isInitialized) return;
    try {
      const designState = getFullDesignState();
      localStorage.setItem(getAutosaveKey(), JSON.stringify(designState));
    } catch (e) {
      // localStorage might be full or unavailable
    }
  }

  function restoreAutosave() {
    try {
      const saved = localStorage.getItem(getAutosaveKey());
      if (!saved) return;

      const data = JSON.parse(saved);
      if (data.product_id !== state.productId) return;

      const surfacesData = data.surfaces || {};
      Object.keys(surfacesData).forEach(function (slug) {
        const sd = surfacesData[slug];
        if (sd.canvas_json && sd.canvas_json.objects && sd.canvas_json.objects.length > 0) {
          state.surfaceStates[slug] = {
            canvasJSON: sd.canvas_json,
            dirty: false,
          };
        }
      });
    } catch (e) {
      // Ignore corrupt autosave data
    }
  }

  function clearAutosave() {
    try {
      localStorage.removeItem(getAutosaveKey());
    } catch (e) {
      // Ignore
    }
  }

  /* ─── Toolbar Events ─────────────────────────────────────────────────── */

  function bindToolbarEvents() {
    if (dom.btnUndo) {
      dom.btnUndo.addEventListener('click', function () {
        if (window.DesignEditorHistory) {
          window.DesignEditorHistory.undo();
        }
      });
    }

    if (dom.btnRedo) {
      dom.btnRedo.addEventListener('click', function () {
        if (window.DesignEditorHistory) {
          window.DesignEditorHistory.redo();
        }
      });
    }

    if (dom.btnZoomIn) {
      dom.btnZoomIn.addEventListener('click', function () {
        if (window.DesignEditorCanvas) {
          window.DesignEditorCanvas.zoomIn();
        }
      });
    }

    if (dom.btnZoomOut) {
      dom.btnZoomOut.addEventListener('click', function () {
        if (window.DesignEditorCanvas) {
          window.DesignEditorCanvas.zoomOut();
        }
      });
    }

    if (dom.btnDelete) {
      dom.btnDelete.addEventListener('click', function () {
        if (window.DesignEditorCanvas) {
          window.DesignEditorCanvas.deleteSelected();
        }
      });
    }

    if (dom.btnDuplicate) {
      dom.btnDuplicate.addEventListener('click', function () {
        if (window.DesignEditorCanvas) {
          window.DesignEditorCanvas.duplicateSelected();
        }
      });
    }

    // Fullscreen toggle
    if (dom.btnFullscreen) {
      dom.btnFullscreen.addEventListener('click', function () {
        toggleFullscreen();
      });
    }

    // Escape key exits fullscreen
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && dom.editor.classList.contains('design-editor--fullscreen')) {
        toggleFullscreen();
      }
    });

    // Handle window resize to reposition canvas zone
    let resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        const surface = state.surfaces[state.activeSurfaceIndex];
        if (surface) {
          positionCanvasZone(surface);
        }
      }, 150);
    });
  }

  /* ─── Tool Tab Switching ─────────────────────────────────────────────── */

  function bindToolTabEvents() {
    dom.toolTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        const tool = tab.dataset.tool;
        switchTool(tool);
      });
    });
  }

  function switchTool(toolName) {
    dom.toolTabs.forEach(function (tab) {
      tab.classList.toggle('active', tab.dataset.tool === toolName);
    });

    dom.toolPanels.forEach(function (panel) {
      panel.classList.toggle('active', panel.id === 'panel-tool-' + toolName);
    });
  }

  /* ─── Save/Load Design ───────────────────────────────────────────────── */

  function bindSaveLoadEvents() {
    if (dom.btnSaveDesign) {
      dom.btnSaveDesign.addEventListener('click', handleSaveDesign);
    }

    if (dom.btnLoadDesign) {
      dom.btnLoadDesign.addEventListener('click', handleLoadDesigns);
    }
  }

  async function handleSaveDesign() {
    if (!state.isAuthenticated) {
      showSignupEncouragementModal();
      return;
    }

    if (!window.StorefrontModal) {
      // Fallback if StorefrontModal hasn't loaded
      const name = await AdminModal.prompt('Design name:');
      if (!name) return;
      doSaveDesign(name);
      return;
    }

    window.StorefrontModal.prompt({
      title: 'Save Design',
      label: 'Design Name',
      placeholder: 'Enter a name for your design...',
      submitText: 'Save',
      onSubmit: function (name) {
        doSaveDesign(name);
      },
    });
  }

  function doSaveDesign(name) {
    const designState = getFullDesignState();

    apiRequest('designs/save/', {
      method: 'POST',
      body: {
        product_id: state.productId,
        name: name,
        design_data: designState,
      },
    })
      .then(function () {
        showNotification('Design saved!', 'success');
      })
      .catch(function (err) {
        console.error('[DesignEditor] Save failed:', err);
        showNotification('Failed to save design', 'error');
      });
  }

  function showSignupEncouragementModal() {
    if (!window.StorefrontModal) return;

    const currentPath = encodeURIComponent(window.location.pathname + window.location.search);
    const loginUrl = '/accounts/login/?next=' + currentPath;
    const signupUrl = '/accounts/signup/?next=' + currentPath;

    window.StorefrontModal.open({
      title: 'Save Your Design',
      size: 'sm',
      body:
        '<div style="text-align:center; padding: 0.5rem 0;">' +
        '<div class="sf-modal__icon">' +
        '<i class="fas fa-user-plus" style="font-size:2.5rem; color:var(--theme-color-primary, #4f46e5);"></i>' +
        '</div>' +
        '<p class="sf-modal__message" style="margin:1rem 0 0.5rem; font-size:1.05rem; font-weight:500;">' +
        'Create an account to save your designs' +
        '</p>' +
        '<p class="sf-modal__message" style="color:var(--theme-color-text-muted, #6b7280); font-size:0.9rem;">' +
        'Access your saved designs from any device, continue editing anytime, and never lose your work.' +
        '</p>' +
        '</div>',
      footer:
        '<a href="' +
        signupUrl +
        '" class="sf-modal__btn sf-modal__btn--primary">' +
        '<i class="fas fa-user-plus"></i> Create Account' +
        '</a>' +
        '<a href="' +
        loginUrl +
        '" class="sf-modal__btn sf-modal__btn--outline">' +
        '<i class="fas fa-sign-in-alt"></i> Sign In' +
        '</a>',
    });
  }

  let _savedDesignsModal = null; // reference to the currently open saved-designs modal

  function handleLoadDesigns() {
    if (!state.isAuthenticated) {
      showSignupEncouragementModal();
      return;
    }

    if (!window.StorefrontModal) return;

    _savedDesignsModal = window.StorefrontModal.open({
      title: 'My Saved Designs',
      size: 'md',
      body:
        '<div class="design-editor__loading" style="text-align:center; padding:2rem 0;">' +
        '<div class="design-editor__spinner"></div> Loading...' +
        '</div>',
      onClose: function () {
        _savedDesignsModal = null;
      },
    });

    const bodyEl = _savedDesignsModal.querySelector('.sf-modal__body');

    apiRequest('designs/?product_id=' + state.productId)
      .then(function (data) {
        const designs = data.designs || [];
        if (designs.length === 0) {
          bodyEl.innerHTML =
            '<div style="text-align:center; padding:2rem 0; color:var(--theme-color-text-muted, #6b7280);">' +
            '<i class="fas fa-folder-open" style="font-size:2rem; margin-bottom:0.75rem; display:block;"></i>' +
            '<p>No saved designs yet</p>' +
            '</div>';
          return;
        }

        bodyEl.innerHTML = '';
        designs.forEach(function (design) {
          const card = document.createElement('div');
          card.className = 'design-editor__saved-card';

          card.innerHTML =
            '<div class="design-editor__saved-card__info">' +
            '<div class="design-editor__saved-card__name">' +
            escapeHtml(design.name) +
            '</div>' +
            '<div class="design-editor__saved-card__date">' +
            escapeHtml(design.created_at || '') +
            '</div>' +
            '</div>' +
            '<div class="design-editor__saved-card__actions">' +
            '<button type="button" class="design-editor__saved-card__delete" title="Delete" data-id="' +
            design.id +
            '"><i class="fas fa-trash"></i></button>' +
            '</div>';

          // Click to load
          card.addEventListener('click', function (e) {
            if (e.target.closest('.design-editor__saved-card__delete')) return;
            loadSavedDesign(design);
          });

          // Delete button
          const deleteBtn = card.querySelector('.design-editor__saved-card__delete');
          if (deleteBtn) {
            deleteBtn.addEventListener('click', function (e) {
              e.stopPropagation();
              deleteSavedDesign(design.id, card);
            });
          }

          bodyEl.appendChild(card);
        });
      })
      .catch(function (err) {
        console.error('[DesignEditor] Load designs failed:', err);
        bodyEl.innerHTML =
          '<div style="text-align:center; padding:2rem 0; color:var(--theme-color-text-muted, #6b7280);">' +
          '<i class="fas fa-exclamation-circle" style="font-size:2rem; margin-bottom:0.75rem; display:block;"></i>' +
          '<p>Failed to load designs</p>' +
          '</div>';
      });
  }

  function loadSavedDesign(design) {
    // If design_data is already available (e.g. from detail), apply directly
    if (design.design_data) {
      applyDesignData(design.design_data);
      return;
    }

    // Otherwise fetch the full design from the detail endpoint
    apiRequest('designs/' + design.id + '/')
      .then(function (data) {
        if (data.design_data) {
          applyDesignData(data.design_data);
        } else {
          showNotification('Design has no data', 'error');
        }
      })
      .catch(function (err) {
        console.error('[DesignEditor] Load design failed:', err);
        showNotification('Failed to load design', 'error');
      });
  }

  function applyDesignData(designData) {
    const surfacesData = designData.surfaces || {};
    Object.keys(surfacesData).forEach(function (slug) {
      const sd = surfacesData[slug];
      state.surfaceStates[slug] = {
        canvasJSON: sd.canvas_json || { version: '6.0.0', objects: [] },
        dirty: true,
      };
    });

    // Reload current surface
    switchSurface(state.activeSurfaceIndex);

    // Close the saved designs modal if it's open
    if (_savedDesignsModal && window.StorefrontModal) {
      window.StorefrontModal.close(_savedDesignsModal);
      _savedDesignsModal = null;
    }

    showNotification('Design loaded!', 'success');
  }

  async function deleteSavedDesign(designId, cardEl) {
    if (
      !(await AdminModal.confirm({
        message: 'Delete this saved design?',
        danger: true,
        confirmText: 'Delete',
      }))
    )
      return;

    apiRequest('designs/' + designId + '/delete/', { method: 'POST' })
      .then(function () {
        if (cardEl && cardEl.parentNode) {
          cardEl.parentNode.removeChild(cardEl);
        }
        showNotification('Design deleted', 'success');
      })
      .catch(function (err) {
        console.error('[DesignEditor] Delete failed:', err);
        showNotification('Failed to delete design', 'error');
      });
  }

  /* ─── Pricing ────────────────────────────────────────────────────────── */

  function updatePricing() {
    const designState = getFullDesignState();

    apiRequest('calculate-price/', {
      method: 'POST',
      body: {
        product_id: state.productId,
        design_data: designState,
      },
    })
      .then(function (data) {
        const pricing = data.pricing || {};
        if (dom.priceTotal && pricing.total !== undefined) {
          dom.priceTotal.textContent = state.currencySymbol + parseFloat(pricing.total).toFixed(2);
        }
      })
      .catch(function (err) {
        console.error('[DesignEditor] Price calculation failed:', err);
      });
  }

  /* ─── Cart Integration ───────────────────────────────────────────────── */

  /**
   * Called by the add-to-cart flow to prepare the design for the cart.
   * Returns a Promise that resolves with { token, pricing_breakdown }.
   */
  function prepareForCart() {
    const designState = getFullDesignState();

    return apiRequest('prepare-for-cart/', {
      method: 'POST',
      body: {
        product_id: state.productId,
        design_data: designState,
      },
    }).then(function (data) {
      state.designToken = data.design_token;
      clearAutosave();
      return data;
    });
  }

  /**
   * Returns the design customization data for the add-to-cart request.
   */
  function getCartCustomizations() {
    if (!state.designToken) return null;

    // Count elements across surfaces
    const surfacesUsed = [];
    const elementCounts = { text: 0, image: 0, clipart: 0 };

    state.surfaces.forEach(function (surface) {
      const ss = state.surfaceStates[surface.slug];
      if (ss && ss.canvasJSON && ss.canvasJSON.objects && ss.canvasJSON.objects.length > 0) {
        surfacesUsed.push(surface.slug);
        ss.canvasJSON.objects.forEach(function (obj) {
          if (obj.type === 'i-text' || obj.type === 'textbox') {
            elementCounts.text++;
          } else if (obj.custom_type === 'clipart') {
            elementCounts.clipart++;
          } else if (obj.type === 'image') {
            elementCounts.image++;
          }
        });
      }
    });

    return {
      _design: {
        token: state.designToken,
        surfaces_used: surfacesUsed,
        element_counts: elementCounts,
      },
    };
  }

  /* ─── UI Helpers ─────────────────────────────────────────────────────── */

  function showLoading(isLoading) {
    state.isLoading = isLoading;
    // Simple loading state - just show/hide content
    if (dom.viewport) {
      dom.viewport.style.opacity = isLoading ? '0.5' : '1';
    }
  }

  function showEmptyState() {
    showLoading(false);
    if (dom.viewport) {
      dom.viewport.innerHTML =
        '<div class="design-editor__empty"><i class="fas fa-paint-brush"></i>' +
        '<p>Design editor is not configured for this product yet.</p></div>';
    }
  }

  function showNotification(message, type) {
    AdminModal.toast(message, type || 'info');
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  /* ─── Font Loading ───────────────────────────────────────────────────── */

  function loadFonts() {
    if (!state.fonts || state.fonts.length === 0) return;

    state.fonts.forEach(function (font) {
      if (font.is_system_font) return; // System fonts don't need loading

      if (font.regular_url) {
        loadFontFace(font.family, font.regular_url, 'normal', 'normal');
      }
      if (font.bold_url) {
        loadFontFace(font.family, font.bold_url, 'normal', 'bold');
      }
      if (font.italic_url) {
        loadFontFace(font.family, font.italic_url, 'italic', 'normal');
      }
      if (font.bold_italic_url) {
        loadFontFace(font.family, font.bold_italic_url, 'italic', 'bold');
      }
    });
  }

  function loadFontFace(family, url, style, weight) {
    if (!('FontFace' in window)) return;

    const fontFace = new FontFace(family, 'url(' + url + ')', {
      style: style,
      weight: weight,
    });

    fontFace
      .load()
      .then(function (loaded) {
        document.fonts.add(loaded);
      })
      .catch(function (err) {
        console.warn('[DesignEditor] Failed to load font:', family, err);
      });
  }

  /* ─── Public API ─────────────────────────────────────────────────────── */

  window.DesignEditor = {
    init: init,
    getState: function () {
      return state;
    },
    getDom: function () {
      return dom;
    },
    getFullDesignState: getFullDesignState,
    switchSurface: switchSurface,
    switchTool: switchTool,
    updatePricing: updatePricing,
    prepareForCart: prepareForCart,
    getCartCustomizations: getCartCustomizations,
    apiRequest: apiRequest,
    showNotification: showNotification,
    positionCanvasZone: positionCanvasZone,
    saveCurrentSurfaceState: saveCurrentSurfaceState,
  };

  /* ─── Auto-init on DOMContentLoaded ──────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
