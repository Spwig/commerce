/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * AdminLinkSelector — reusable search-based link picker for Django admin.
 *
 * Replaces heavy FK <select> dropdowns with a search UI:
 *   type dropdown → search input → results with thumbnails → selection preview
 *
 * Works with HiddenInput FK widgets — sets the integer ID on selection.
 * Uses the page builder link-sources API for search.
 *
 * Usage:
 *   new AdminLinkSelector({
 *       linkTypeFieldId: 'id_link_type',
 *       fieldMap: {
 *           'product':   { inputId: 'id_product_reference',   apiType: 'product',  resultKey: 'products',   icon: 'fa-box' },
 *           'category':  { inputId: 'id_category_reference',  apiType: 'category', resultKey: 'categories', icon: 'fa-folder' },
 *           'blog_post': { inputId: 'id_blog_post_reference', apiType: 'blog',     resultKey: 'blog_posts', icon: 'fa-newspaper' },
 *           'page':      { inputId: 'id_page_reference',      apiType: 'page',     resultKey: 'pages',      icon: 'fa-file' },
 *       },
 *       customUrlContainerId: 'ref-custom_url',
 *       linkOptionsSelector: '#ann-link-options',
 *       searchContainerId: 'link-search-container',
 *       apiUrl: '/api/page-builder/link-sources/',
 *       initialData: {},
 *   });
 */
class AdminLinkSelector {
  constructor(config) {
    this.linkTypeField = document.getElementById(config.linkTypeFieldId);
    if (!this.linkTypeField) return;

    this.fieldMap = config.fieldMap || {};
    this.customUrlContainerId = config.customUrlContainerId || '';
    this.linkOptionsSelector = config.linkOptionsSelector || '';
    this.searchContainer = document.getElementById(config.searchContainerId);
    this.apiUrl = config.apiUrl || '/api/page-builder/link-sources/';
    this.initialData = config.initialData || {};

    this._searchTimeout = null;
    this._currentType = null;

    this.linkTypeField.addEventListener('change', () => this.update());
    this.update();
    this.loadInitialData();
  }

  update() {
    const selected = this.linkTypeField.value;
    const hasLink = selected && selected !== 'none';
    const isEntityType = hasLink && selected !== 'custom_url' && this.fieldMap[selected];

    // Show/hide custom URL container
    const customEl = this.customUrlContainerId
      ? document.getElementById(this.customUrlContainerId)
      : null;
    if (customEl) {
      if (selected === 'custom_url') {
        customEl.classList.add('visible');
      } else {
        customEl.classList.remove('visible');
      }
    }

    // Show/hide link options (link_text + show_modal)
    const opts = this.linkOptionsSelector ? document.querySelector(this.linkOptionsSelector) : null;
    if (opts) {
      if (hasLink) {
        opts.classList.add('visible');
      } else {
        opts.classList.remove('visible');
      }
    }

    // Search container: show for entity types, hide otherwise
    if (this.searchContainer) {
      if (isEntityType) {
        // If type changed, rebuild search UI
        if (this._currentType !== selected) {
          this._currentType = selected;
          this.renderSearch(selected);
        }
        this.searchContainer.style.display = 'block';
      } else {
        this.searchContainer.style.display = 'none';
        this._currentType = null;
      }
    }

    // Clear FK inputs for non-selected types
    if (hasLink) {
      for (const type in this.fieldMap) {
        if (type !== selected) {
          const input = document.getElementById(this.fieldMap[type].inputId);
          if (input) input.value = '';
        }
      }
    }
  }

  renderSearch(type) {
    if (!this.searchContainer) return;
    const fc = this.fieldMap[type];
    if (!fc) return;

    this.searchContainer.innerHTML = '';

    // Search wrapper
    const searchDiv = document.createElement('div');
    searchDiv.className = 'als-search';

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'als-search-input';
    input.placeholder = this._getPlaceholder(type);
    input.autocomplete = 'off';

    const icon = document.createElement('span');
    icon.className = 'als-search-icon';
    icon.innerHTML = '<i class="fas fa-search"></i>';

    searchDiv.appendChild(input);
    searchDiv.appendChild(icon);
    this.searchContainer.appendChild(searchDiv);

    // Results dropdown
    const resultsDiv = document.createElement('div');
    resultsDiv.className = 'als-results';
    resultsDiv.style.display = 'none';
    this.searchContainer.appendChild(resultsDiv);

    // Preview (hidden initially)
    const previewDiv = document.createElement('div');
    previewDiv.className = 'als-preview';
    previewDiv.style.display = 'none';
    this.searchContainer.appendChild(previewDiv);

    // Check if there's already a value selected (re-opening same type)
    const hiddenInput = document.getElementById(fc.inputId);
    if (hiddenInput && hiddenInput.value) {
      // Value exists but we lost the preview (type switching back)
      // Initial data load will handle this
    }

    const self = this;

    // Debounced search
    input.addEventListener('input', function () {
      clearTimeout(self._searchTimeout);
      const query = input.value.trim();
      if (query.length < 2) {
        resultsDiv.style.display = 'none';
        return;
      }
      self._searchTimeout = setTimeout(function () {
        self.doSearch(fc, query, resultsDiv, searchDiv, previewDiv);
      }, 300);
    });

    // Hide results on blur
    input.addEventListener('blur', function () {
      setTimeout(function () {
        resultsDiv.style.display = 'none';
      }, 200);
    });

    // Show results on focus if populated
    input.addEventListener('focus', function () {
      if (input.value.trim().length >= 2 && resultsDiv.children.length > 0) {
        resultsDiv.style.display = 'block';
      }
    });
  }

  doSearch(fc, query, resultsDiv, searchDiv, previewDiv) {
    const self = this;
    resultsDiv.innerHTML =
      '<div class="als-loading"><i class="fas fa-spinner"></i> Searching...</div>';
    resultsDiv.style.display = 'block';

    fetch(
      this.apiUrl +
        '?type=' +
        encodeURIComponent(fc.apiType) +
        '&search=' +
        encodeURIComponent(query) +
        '&limit=10'
    )
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        const results = data[fc.resultKey] || [];
        if (results.length === 0) {
          resultsDiv.innerHTML = '<div class="als-no-results">No results found</div>';
          return;
        }
        self.renderResults(results, fc, resultsDiv, searchDiv, previewDiv);
      })
      .catch(function (err) {
        console.error('Link search error:', err);
        resultsDiv.innerHTML = '<div class="als-error">Search failed. Please try again.</div>';
      });
  }

  renderResults(items, fc, resultsDiv, searchDiv, previewDiv) {
    const self = this;
    resultsDiv.innerHTML = '';

    items.forEach(function (item) {
      const row = document.createElement('div');
      row.className = 'als-result-item';

      let thumbHtml;
      if (item.thumbnail) {
        thumbHtml = '<img src="' + self._escapeAttr(item.thumbnail) + '" alt="">';
      } else {
        thumbHtml = '<i class="fas ' + (fc.icon || 'fa-link') + '"></i>';
      }

      row.innerHTML =
        '<div class="als-result-thumb">' +
        thumbHtml +
        '</div>' +
        '<div class="als-result-info">' +
        '<div class="als-result-title">' +
        self._escapeHtml(item.title || item.name) +
        '</div>' +
        '<div class="als-result-url">' +
        self._escapeHtml(item.url || '') +
        '</div>' +
        '</div>';

      row.addEventListener('click', function () {
        self.selectItem(fc, item, searchDiv, previewDiv, resultsDiv);
      });

      resultsDiv.appendChild(row);
    });
  }

  selectItem(fc, item, searchDiv, previewDiv, resultsDiv) {
    // Set the hidden FK input value
    const hiddenInput = document.getElementById(fc.inputId);
    if (hiddenInput) hiddenInput.value = item.id;

    // Show preview, hide search
    this.showPreview(fc, item, searchDiv, previewDiv);
    if (searchDiv) searchDiv.style.display = 'none';
    if (resultsDiv) resultsDiv.style.display = 'none';
  }

  showPreview(fc, item, searchDiv, previewDiv) {
    if (!previewDiv) return;
    const self = this;

    const typeLabels = {
      product: 'Product',
      category: 'Category',
      blog_post: 'Blog Post',
      page: 'Page',
    };

    previewDiv.innerHTML =
      '<div class="als-preview-content">' +
      '<div class="als-preview-info">' +
      '<span class="als-preview-type">' +
      self._escapeHtml(typeLabels[self._currentType] || self._currentType) +
      '</span>' +
      '<span class="als-preview-title">' +
      self._escapeHtml(item.title || item.name || '') +
      '</span>' +
      '<span class="als-preview-url">' +
      self._escapeHtml(item.url || '') +
      '</span>' +
      '</div>' +
      '<button type="button" class="als-preview-clear" title="Clear selection">&times;</button>' +
      '</div>';

    previewDiv.style.display = 'block';

    // Clear button
    previewDiv.querySelector('.als-preview-clear').addEventListener('click', function () {
      const hiddenInput = document.getElementById(fc.inputId);
      if (hiddenInput) hiddenInput.value = '';

      previewDiv.style.display = 'none';
      previewDiv.innerHTML = '';

      if (searchDiv) {
        searchDiv.style.display = 'block';
        const searchInput = searchDiv.querySelector('input');
        if (searchInput) {
          searchInput.value = '';
          searchInput.focus();
        }
      }
    });
  }

  loadInitialData() {
    if (!this.initialData || !this.initialData.type) return;

    const type = this.initialData.type;
    const fc = this.fieldMap[type];
    if (!fc) return;

    // Make sure the search container is rendered for this type
    if (this._currentType !== type) {
      this._currentType = type;
      this.renderSearch(type);
    }

    // Show preview directly from initial data (no API call needed)
    const searchDiv = this.searchContainer
      ? this.searchContainer.querySelector('.als-search')
      : null;
    const previewDiv = this.searchContainer
      ? this.searchContainer.querySelector('.als-preview')
      : null;

    if (previewDiv) {
      this.showPreview(
        fc,
        {
          id: this.initialData.id,
          name: this.initialData.name || '',
          title: this.initialData.name || '',
          url: this.initialData.url || '',
        },
        searchDiv,
        previewDiv
      );

      if (searchDiv) searchDiv.style.display = 'none';
    }
  }

  _getPlaceholder(type) {
    const labels = {
      product: 'Search products...',
      category: 'Search categories...',
      blog_post: 'Search blog posts...',
      page: 'Search pages...',
    };
    return labels[type] || 'Search...';
  }

  _escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  _escapeAttr(str) {
    return this._escapeHtml(str).replace(/"/g, '&quot;');
  }
}

// Keep backwards compatibility — old LinkSelector still works
class LinkSelector {
  constructor(config) {
    this.linkTypeField = document.getElementById(config.linkTypeFieldId);
    if (!this.linkTypeField) return;
    this.fieldMap = config.fieldMap || {};
    this.linkActiveFields = config.linkActiveFields || [];
    this.hiddenClass = config.hiddenClass || 'link-field-hidden';
    this.linkTypeField.addEventListener('change', () => this.update());
    this.update();
  }
  update() {
    const selected = this.linkTypeField.value;
    Object.values(this.fieldMap).forEach(selector => {
      const field = document.querySelector(selector);
      if (field) field.classList.add(this.hiddenClass);
    });
    if (selected && selected !== 'none' && this.fieldMap[selected]) {
      const active = document.querySelector(this.fieldMap[selected]);
      if (active) active.classList.remove(this.hiddenClass);
    }
    const hasLink = selected && selected !== 'none';
    this.linkActiveFields.forEach(selector => {
      const field = document.querySelector(selector);
      if (field) field.classList.toggle(this.hiddenClass, !hasLink);
    });
  }
}

window.AdminLinkSelector = AdminLinkSelector;
window.LinkSelector = LinkSelector;
