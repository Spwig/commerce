/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Icon Picker Component
 *
 * Universal Font Awesome icon picker with compact grid + full modal browser.
 * Auto-initializes on elements with [data-icon-picker] attribute.
 *
 * Features:
 * - Priority (suggested) icon grid for quick selection
 * - "Browse all" modal with ~550 categorized icons
 * - Search/filter by name and keywords (200ms debounce)
 * - Category filter pills
 * - Works with both 'fa-star' and 'fas fa-star' value formats
 * - Dispatches 'icon-picker:change' and standard 'change' events
 * - Keyboard accessible (Escape to close, focus management)
 * - Dark mode aware via CSS variables
 *
 * Template: core/templates/admin/widgets/icon_picker.html
 * CSS: core/static/core/admin/css/icon_picker.css
 * Depends on: admin-base.css (modal system)
 */
(function () {
  'use strict';

  if (window._IconPickerLoaded) return;
  window._IconPickerLoaded = true;

  /**
   * IconPicker class — one instance per widget on the page.
   */
  class IconPicker {
    constructor(rootEl) {
      this.root = rootEl;
      this.widgetName = rootEl.dataset.widgetName;
      this.widgetId = rootEl.dataset.widgetId;
      this.stylePrefix = rootEl.dataset.stylePrefix === 'true';

      // Parse translations
      try {
        this.trans = JSON.parse(rootEl.dataset.translations || '{}');
      } catch (e) {
        this.trans = {};
      }

      // Load registry from the companion <script type="application/json"> tag
      this.registry = this._loadRegistry();

      // DOM refs
      this.hiddenInput = rootEl.querySelector('input[type="hidden"]');
      this.previewEl = rootEl.querySelector('[data-icon-picker-preview]');
      this.labelEl = rootEl.querySelector('[data-icon-picker-label]');
      this.clearBtn = rootEl.querySelector('[data-icon-picker-clear]');
      this.browseBtn = rootEl.querySelector('[data-icon-picker-browse]');
      this.priorityGrid = rootEl.querySelector('[data-icon-picker-priority]');

      // State
      this.selectedValue = this.hiddenInput ? this.hiddenInput.value : '';
      this.modal = null;
      this.modalSearch = null;
      this.modalGrid = null;
      this.modalCount = null;
      this.activeCategory = 'all';

      this._bindEvents();
    }

    /**
     * Load icon registry JSON from the companion script tag.
     */
    _loadRegistry() {
      const scriptTag = document.querySelector(
        'script[data-icon-picker-registry="' + this.widgetName + '"]'
      );
      if (!scriptTag) return { categories: {}, icons: [] };
      try {
        return JSON.parse(scriptTag.textContent);
      } catch (e) {
        return { categories: {}, icons: [] };
      }
    }

    /**
     * Bind event listeners for inline widget elements.
     */
    _bindEvents() {
      const self = this;

      // Priority grid item clicks (event delegation)
      if (this.priorityGrid) {
        this.priorityGrid.addEventListener('click', function (e) {
          const item = e.target.closest('.icon-picker-grid-item');
          if (item) self._selectFromGridItem(item);
        });
      }

      // Browse button
      if (this.browseBtn) {
        this.browseBtn.addEventListener('click', function () {
          self._openModal();
        });
      }

      // Clear button
      if (this.clearBtn) {
        this.clearBtn.addEventListener('click', function () {
          self._clearSelection();
        });
      }
    }

    // ── Selection ──

    /**
     * Select an icon programmatically.
     */
    _selectIcon(iconClass, iconStyle, iconLabel) {
      // Build stored value based on style_prefix setting
      const value = this.stylePrefix ? iconStyle + ' ' + iconClass : iconClass;

      this.selectedValue = value;
      if (this.hiddenInput) this.hiddenInput.value = value;

      // Update preview
      if (this.previewEl) {
        this.previewEl.innerHTML = '<i class="' + iconStyle + ' ' + iconClass + '"></i>';
      }
      if (this.labelEl) {
        this.labelEl.textContent = iconLabel;
      }
      if (this.clearBtn) {
        this.clearBtn.hidden = false;
      }

      // Update priority grid selection state
      this._updatePrioritySelection(iconClass);

      // Dispatch events
      this._dispatchChange(value, iconClass, iconStyle, iconLabel);
    }

    /**
     * Select from a priority grid item button.
     */
    _selectFromGridItem(item) {
      this._selectIcon(item.dataset.iconClass, item.dataset.iconStyle, item.dataset.iconLabel);
    }

    /**
     * Clear the current selection.
     */
    _clearSelection() {
      this.selectedValue = '';
      if (this.hiddenInput) this.hiddenInput.value = '';

      if (this.previewEl) {
        this.previewEl.innerHTML =
          '<span class="icon-picker-preview-empty"><i class="fas fa-icons"></i></span>';
      }
      if (this.labelEl) {
        this.labelEl.textContent = this.trans.noIconSelected || 'No icon selected';
      }
      if (this.clearBtn) {
        this.clearBtn.hidden = true;
      }

      // Clear priority grid selection
      this._updatePrioritySelection('');

      this._dispatchChange('', '', '', '');
    }

    /**
     * Update the visual selection state of priority grid items.
     */
    _updatePrioritySelection(iconClass) {
      if (!this.priorityGrid) return;
      const items = this.priorityGrid.querySelectorAll('.icon-picker-grid-item');
      for (let i = 0; i < items.length; i++) {
        if (items[i].dataset.iconClass === iconClass) {
          items[i].classList.add('selected');
        } else {
          items[i].classList.remove('selected');
        }
      }
    }

    /**
     * Dispatch change events for form integration.
     */
    _dispatchChange(value, iconClass, iconStyle, iconLabel) {
      // Custom event with detail
      this.root.dispatchEvent(
        new CustomEvent('icon-picker:change', {
          bubbles: true,
          detail: {
            value: value,
            iconClass: iconClass,
            iconStyle: iconStyle,
            iconLabel: iconLabel,
          },
        })
      );

      // Standard change on hidden input (for Django admin)
      if (this.hiddenInput) {
        this.hiddenInput.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }

    // ── Modal ──

    /**
     * Open the icon browser modal. Builds it on first open.
     */
    _openModal() {
      if (!this.modal) {
        this._buildModal();
      }

      // Mark current selection in modal grid
      this._updateModalSelection();

      this.modal.classList.add('active');
      document.body.classList.add('admin-modal-body-locked');

      // Focus search input
      const searchInput = this.modalSearch;
      setTimeout(function () {
        if (searchInput) searchInput.focus();
      }, 100);

      // Scroll to selected icon
      this._scrollToSelected();
    }

    /**
     * Close the modal and return focus.
     */
    _closeModal() {
      if (!this.modal) return;
      this.modal.classList.remove('active');
      document.body.classList.remove('admin-modal-body-locked');

      // Reset search and category
      if (this.modalSearch) this.modalSearch.value = '';
      this.activeCategory = 'all';

      // Reset category buttons
      const catBtns = this.modal.querySelectorAll('.icon-picker-category-btn');
      for (let i = 0; i < catBtns.length; i++) {
        catBtns[i].classList.toggle('active', catBtns[i].dataset.category === 'all');
      }

      // Re-render with no filter
      this._renderModalIcons('', 'all');

      // Return focus to browse button
      if (this.browseBtn) this.browseBtn.focus();
    }

    /**
     * Build the modal DOM and append to document body.
     */
    _buildModal() {
      const self = this;
      const trans = this.trans;

      // Create overlay
      const overlay = document.createElement('div');
      overlay.className = 'admin-modal-overlay icon-picker-modal';

      // Modal container
      const modal = document.createElement('div');
      modal.className = 'admin-modal admin-modal--lg';

      // Header
      const header = document.createElement('div');
      header.className = 'admin-modal-header';

      const title = document.createElement('h3');
      title.className = 'admin-modal-title';
      title.innerHTML = '<i class="fas fa-icons"></i> ' + (trans.chooseIcon || 'Choose an Icon');
      header.appendChild(title);

      const closeBtn = document.createElement('button');
      closeBtn.type = 'button';
      closeBtn.className = 'admin-modal-close';
      closeBtn.innerHTML = '<i class="fas fa-times"></i>';
      closeBtn.addEventListener('click', function () {
        self._closeModal();
      });
      header.appendChild(closeBtn);

      modal.appendChild(header);

      // Body
      const body = document.createElement('div');
      body.className = 'admin-modal-body';

      // Toolbar
      const toolbar = document.createElement('div');
      toolbar.className = 'icon-picker-modal-toolbar';

      // Search
      const searchWrap = document.createElement('div');
      searchWrap.className = 'icon-picker-modal-search';
      searchWrap.innerHTML = '<i class="fas fa-search"></i>';

      const searchInput = document.createElement('input');
      searchInput.type = 'text';
      searchInput.placeholder = trans.searchIcons || 'Search icons...';
      searchInput.autocomplete = 'off';
      searchWrap.appendChild(searchInput);
      toolbar.appendChild(searchWrap);
      this.modalSearch = searchInput;

      // Category pills
      const catContainer = document.createElement('div');
      catContainer.className = 'icon-picker-modal-categories';

      // "All" button
      const allBtn = document.createElement('button');
      allBtn.type = 'button';
      allBtn.className = 'icon-picker-category-btn active';
      allBtn.dataset.category = 'all';
      allBtn.textContent = trans.allCategories || 'All';
      catContainer.appendChild(allBtn);

      // Category buttons
      const categories = this.registry.categories || {};
      const catKeys = Object.keys(categories);
      for (let i = 0; i < catKeys.length; i++) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'icon-picker-category-btn';
        btn.dataset.category = catKeys[i];
        btn.textContent = categories[catKeys[i]];
        catContainer.appendChild(btn);
      }
      toolbar.appendChild(catContainer);
      body.appendChild(toolbar);

      // Count
      const countEl = document.createElement('div');
      countEl.className = 'icon-picker-modal-count';
      body.appendChild(countEl);
      this.modalCount = countEl;

      // Grid container
      const grid = document.createElement('div');
      grid.className = 'icon-picker-modal-grid';
      body.appendChild(grid);
      this.modalGrid = grid;

      modal.appendChild(body);
      overlay.appendChild(modal);
      document.body.appendChild(overlay);
      this.modal = overlay;

      // Render icons
      this._renderModalIcons('', 'all');

      // ── Bind modal events ──

      // Overlay click to close
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) self._closeModal();
      });

      // Escape key
      const escHandler = function (e) {
        if (e.key === 'Escape' && self.modal && self.modal.classList.contains('active')) {
          self._closeModal();
        }
      };
      document.addEventListener('keydown', escHandler);

      // Search with debounce
      let searchTimeout;
      searchInput.addEventListener('input', function () {
        const val = searchInput.value;
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(function () {
          self._renderModalIcons(val, self.activeCategory);
        }, 200);
      });

      // Category filter (event delegation)
      catContainer.addEventListener('click', function (e) {
        const catBtn = e.target.closest('.icon-picker-category-btn');
        if (!catBtn) return;

        const btns = catContainer.querySelectorAll('.icon-picker-category-btn');
        for (let j = 0; j < btns.length; j++) {
          btns[j].classList.remove('active');
        }
        catBtn.classList.add('active');

        self.activeCategory = catBtn.dataset.category;
        self._renderModalIcons(searchInput.value, self.activeCategory);
      });

      // Icon selection in grid (event delegation)
      grid.addEventListener('click', function (e) {
        const item = e.target.closest('.icon-picker-modal-item');
        if (!item) return;

        self._selectIcon(item.dataset.iconClass, item.dataset.iconStyle, item.dataset.iconLabel);
        self._closeModal();
      });
    }

    /**
     * Render icons into the modal grid.
     */
    _renderModalIcons(searchTerm, category) {
      const icons = this.registry.icons || [];
      const term = (searchTerm || '').toLowerCase().trim();
      const trans = this.trans;

      // Filter icons
      const filtered = [];
      for (let i = 0; i < icons.length; i++) {
        const icon = icons[i];
        // Category filter
        if (category !== 'all' && icon.category !== category) continue;
        // Search filter
        if (term) {
          const searchable =
            icon['class'] + ' ' + icon.label + ' ' + (icon.keywords || []).join(' ');
          if (searchable.toLowerCase().indexOf(term) === -1) continue;
        }
        filtered.push(icon);
      }

      // Build DOM with DocumentFragment for performance
      const fragment = document.createDocumentFragment();

      if (filtered.length === 0) {
        const empty = document.createElement('div');
        empty.className = 'icon-picker-modal-empty';
        empty.textContent = trans.noIconsFound || 'No icons found';
        fragment.appendChild(empty);
      } else if (category === 'all' && !term) {
        // Group by category
        const grouped = {};
        const groupOrder = [];
        for (let j = 0; j < filtered.length; j++) {
          const cat = filtered[j].category;
          if (!grouped[cat]) {
            grouped[cat] = [];
            groupOrder.push(cat);
          }
          grouped[cat].push(filtered[j]);
        }

        const categories = this.registry.categories || {};
        for (let k = 0; k < groupOrder.length; k++) {
          const catSlug = groupOrder[k];
          const catIcons = grouped[catSlug];

          const heading = document.createElement('div');
          heading.className = 'icon-picker-modal-category-heading';
          heading.textContent = categories[catSlug] || catSlug;
          fragment.appendChild(heading);

          const grid = document.createElement('div');
          grid.className = 'icon-picker-modal-category-grid';
          for (let m = 0; m < catIcons.length; m++) {
            grid.appendChild(this._createModalIconBtn(catIcons[m]));
          }
          fragment.appendChild(grid);
        }
      } else {
        // Flat grid (filtered by category or search)
        const flatGrid = document.createElement('div');
        flatGrid.className = 'icon-picker-modal-category-grid';
        for (let n = 0; n < filtered.length; n++) {
          flatGrid.appendChild(this._createModalIconBtn(filtered[n]));
        }
        fragment.appendChild(flatGrid);
      }

      // Replace grid content
      this.modalGrid.innerHTML = '';
      this.modalGrid.appendChild(fragment);

      // Scroll to top
      this.modalGrid.scrollTop = 0;

      // Update count
      const countWord = trans.iconCount || 'icons';
      this.modalCount.textContent = filtered.length + ' ' + countWord;
    }

    /**
     * Create a single icon button for the modal grid.
     */
    _createModalIconBtn(icon) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'icon-picker-modal-item';
      btn.dataset.iconClass = icon['class'];
      btn.dataset.iconStyle = icon.style;
      btn.dataset.iconLabel = icon.label;
      btn.title = icon.label;

      // Check if selected
      const fullValue = icon.style + ' ' + icon['class'];
      const bareValue = icon['class'];
      if (this.selectedValue === fullValue || this.selectedValue === bareValue) {
        btn.classList.add('selected');
      }

      const iconEl = document.createElement('i');
      iconEl.className = icon.style + ' ' + icon['class'];
      btn.appendChild(iconEl);

      const label = document.createElement('span');
      label.className = 'icon-picker-modal-item-label';
      label.textContent = icon.label;
      btn.appendChild(label);

      return btn;
    }

    /**
     * Update modal grid selection state after selecting a new icon.
     */
    _updateModalSelection() {
      if (!this.modalGrid) return;
      const items = this.modalGrid.querySelectorAll('.icon-picker-modal-item');
      for (let i = 0; i < items.length; i++) {
        const fullVal = items[i].dataset.iconStyle + ' ' + items[i].dataset.iconClass;
        const bareVal = items[i].dataset.iconClass;
        const isSelected = this.selectedValue === fullVal || this.selectedValue === bareVal;
        items[i].classList.toggle('selected', isSelected);
      }
    }

    /**
     * Scroll to the currently selected icon in the modal.
     */
    _scrollToSelected() {
      if (!this.selectedValue || !this.modalGrid) return;
      const selectedEl = this.modalGrid.querySelector('.icon-picker-modal-item.selected');
      if (selectedEl) {
        setTimeout(function () {
          selectedEl.scrollIntoView({ block: 'center', behavior: 'smooth' });
        }, 200);
      }
    }
  }

  // ── Auto-initialization ──

  function initAll() {
    const widgets = document.querySelectorAll('[data-icon-picker]');
    for (let i = 0; i < widgets.length; i++) {
      if (!widgets[i]._iconPicker) {
        widgets[i]._iconPicker = new IconPicker(widgets[i]);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  // Expose for programmatic use
  window.IconPicker = IconPicker;
})();
