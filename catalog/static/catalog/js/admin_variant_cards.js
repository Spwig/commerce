/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Variant Cards Manager
 * Replaces stacked inline variant editing with compact list rows + modal editing.
 * All variant CRUD is handled via AJAX.
 */
(function () {
  'use strict';

  // ===== Utilities =====

  function getLanguagePrefix() {
    const match = window.location.pathname.match(/^\/([a-z]{2}(?:-[a-z]{2})?)\/admin/);
    return match ? '/' + match[1] : '';
  }

  function getProductId() {
    const urlMatch = window.location.pathname.match(/\/admin\/catalog\/product\/(\d+)\//);
    return urlMatch ? parseInt(urlMatch[1]) : null;
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
  }

  function showNotification(message, type) {
    AdminModal.toast(message, type || 'info');
  }

  async function fetchJSON(url) {
    const resp = await fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    });
    if (!resp.ok) {
      const data = await resp.json().catch(() => ({}));
      throw new Error(data.error || `HTTP ${resp.status}`);
    }
    return resp.json();
  }

  async function postJSON(url, data) {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify(data),
    });
    const result = await resp.json();
    if (!resp.ok || !result.success) {
      throw new Error(result.error || `HTTP ${resp.status}`);
    }
    return result;
  }

  // ===== Main Manager =====

  const LANG = getLanguagePrefix();
  const PRODUCT_ID = getProductId();
  const BASE = `${LANG}/admin/catalog`;

  if (!PRODUCT_ID) return; // New product, no variants yet

  let variants = [];
  let formContext = null;
  let currentVariantId = null; // null = creating new
  let variantMediaManager = null;

  // DOM refs (populated in init)
  let listEl,
    loadingEl,
    countBadge,
    addBtn,
    overlay,
    modal,
    modalTitle,
    modalBody,
    saveBtn,
    cancelBtn,
    closeBtn;

  // ===== Card Grid =====

  async function loadVariants() {
    try {
      const data = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/variants/list/`);
      variants = data.variants || [];
      renderList();
    } catch (err) {
      console.error('[VariantCards] Error loading variants:', err);
      if (loadingEl)
        loadingEl.innerHTML =
          '<span class="text-error"><i class="fas fa-exclamation-triangle"></i> Failed to load variants</span>';
    }
  }

  async function loadFormContext() {
    try {
      formContext = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/variants/form-context/`);
    } catch (err) {
      console.error('[VariantCards] Error loading form context:', err);
    }
  }

  function renderList() {
    if (loadingEl) loadingEl.style.display = 'none';
    if (countBadge) countBadge.textContent = variants.length;

    // Remove existing rows
    listEl.querySelectorAll('.variant-row').forEach(el => el.remove());
    const emptyMsg = listEl.querySelector('.variant-list-empty');
    if (emptyMsg) emptyMsg.remove();

    if (variants.length === 0) {
      listEl.insertAdjacentHTML(
        'beforeend',
        `
                <div class="variant-list-empty">
                    <i class="fas fa-layer-group"></i>
                    <p>No variants yet. Click "Add New Variant" to create one.</p>
                </div>
            `
      );
      return;
    }

    variants.forEach(v => {
      listEl.insertAdjacentHTML('beforeend', renderRow(v));
    });

    // Attach click handlers
    listEl.querySelectorAll('.variant-row').forEach(row => {
      row.addEventListener('click', e => {
        // Don't open modal if clicking delete
        if (e.target.closest('.variant-row-delete')) return;
        const id = parseInt(row.dataset.variantId);
        openEditModal(id);
      });
    });

    listEl.querySelectorAll('.variant-row-delete').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const id = parseInt(btn.dataset.variantId);
        deleteVariant(id);
      });
    });
  }

  function renderRow(v) {
    const thumb = v.thumbnail_url
      ? `<img src="${escapeHtml(v.thumbnail_url)}" alt="${escapeHtml(v.name)}" class="variant-row-thumb">`
      : '<div class="variant-row-thumb-placeholder"><i class="fas fa-image"></i></div>';

    const stockClass =
      v.stock_status === 'in_stock'
        ? 'stock-in'
        : v.stock_status === 'low_stock'
          ? 'stock-low'
          : 'stock-out';
    const stockLabel =
      v.stock_status === 'in_stock'
        ? 'In Stock'
        : v.stock_status === 'low_stock'
          ? 'Low Stock'
          : 'Out of Stock';

    // Attribute pills
    let pillsHtml = '';
    if (v.attribute_pills && v.attribute_pills.length) {
      pillsHtml = v.attribute_pills
        .map(p => {
          if (p.color_hex) {
            return `<span class="variant-attr-pill">
                        <span class="variant-color-dot" style="background-color: ${escapeHtml(p.color_hex)}"></span>
                        ${escapeHtml(p.value)}
                    </span>`;
          }
          return `<span class="variant-attr-pill">${escapeHtml(p.attribute_name)}: ${escapeHtml(p.value)}</span>`;
        })
        .join('');
    }

    const activeClass = v.is_active ? '' : ' variant-row-inactive';

    return `
        <div class="variant-row${activeClass}" data-variant-id="${v.id}">
            <div class="variant-row-thumb-cell">${thumb}</div>
            <div class="variant-row-info">
                <span class="variant-row-name">${escapeHtml(v.name)}</span>
                <span class="variant-row-sku">${escapeHtml(v.sku)}</span>
            </div>
            <div class="variant-row-attrs">${pillsHtml}</div>
            <div class="variant-row-price">${v.price_display ? escapeHtml(v.price_display) : '<em>Inherited</em>'}</div>
            <div class="variant-row-stock">
                <span class="variant-stock-count">${v.total_stock}</span>
                <span class="variant-stock-badge ${stockClass}">${stockLabel}</span>
            </div>
            <div class="variant-row-actions">
                <button type="button" class="variant-row-edit" title="Edit"><i class="fas fa-pen"></i></button>
                <button type="button" class="variant-row-delete" data-variant-id="${v.id}" title="Delete"><i class="fas fa-trash"></i></button>
            </div>
        </div>`;
  }

  // ===== Modal =====

  function openModal() {
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
    // Focus trap — close on Escape
    document.addEventListener('keydown', onEscapeKey);
  }

  function closeModal() {
    overlay.style.display = 'none';
    document.body.style.overflow = '';
    currentVariantId = null;
    variantMediaManager = null;
    modalBody.innerHTML = '';
    document.removeEventListener('keydown', onEscapeKey);
  }

  function onEscapeKey(e) {
    if (e.key === 'Escape') closeModal();
  }

  async function openEditModal(variantId) {
    currentVariantId = variantId;
    modalTitle.textContent = 'Edit Variant';
    modalBody.innerHTML =
      '<div class="variant-modal-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    openModal();

    try {
      if (!formContext) await loadFormContext();
      const data = await fetchJSON(`${BASE}/variant/${variantId}/detail/`);
      renderModalContent(data.variant);
    } catch (err) {
      modalBody.innerHTML = `<div class="text-error"><i class="fas fa-exclamation-triangle"></i> ${escapeHtml(err.message)}</div>`;
    }
  }

  function openCreateModal() {
    currentVariantId = null;
    modalTitle.textContent = 'Add New Variant';
    modalBody.innerHTML =
      '<div class="variant-modal-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    openModal();

    if (!formContext) {
      loadFormContext().then(() => renderModalContent(null));
    } else {
      renderModalContent(null);
    }
  }

  function renderModalContent(data) {
    // data is null for create, variant object for edit
    const isEdit = data !== null;
    const ctx = formContext || {};

    let html = '';

    // Section 1: Basic Info
    html += `
        <div class="variant-modal-section">
            <h4><i class="fas fa-info-circle"></i> Basic Information</h4>
            <div class="variant-modal-fields">
                <div class="variant-modal-field">
                    <label for="vm-name">Name <span class="required">*</span></label>
                    <input type="text" id="vm-name" value="${escapeHtml(data?.name || '')}" placeholder="Variant name" required>
                </div>
                <div class="variant-modal-field">
                    <label for="vm-sku">SKU <span class="required">*</span></label>
                    <input type="text" id="vm-sku" value="${escapeHtml(data?.sku || '')}" placeholder="Unique SKU" required>
                </div>
                <div class="variant-modal-field variant-modal-field-checkbox">
                    <label>
                        <input type="checkbox" id="vm-is-active" ${data?.is_active !== false ? 'checked' : ''}>
                        Active
                    </label>
                </div>
            </div>
        </div>`;

    // Section 2: Attributes
    if (ctx.attributes && ctx.attributes.length) {
      const selectedIds = new Set((data?.selected_attributes || []).map(a => a.id));

      html += `<div class="variant-modal-section">
                <h4><i class="fas fa-tags"></i> Attributes</h4>`;

      ctx.attributes.forEach(attr => {
        html += `<div class="variant-modal-attr-group" data-attr-id="${attr.id}">
                    <label class="variant-modal-attr-label">${escapeHtml(attr.name)}${attr.is_required ? ' <span class="required">*</span>' : ''}</label>
                    <div class="variant-modal-attr-values">`;

        attr.values.forEach(val => {
          const checked = selectedIds.has(val.id) ? 'checked' : '';
          if (attr.type === 'color') {
            const colorStyle = val.color_hex
              ? `background-color: ${val.color_hex}`
              : 'background-color: #ccc';
            html += `
                        <label class="variant-attr-option variant-attr-option-color ${checked ? 'selected' : ''}" data-value-id="${val.id}">
                            <input type="checkbox" name="attr_${attr.id}" value="${val.id}" ${checked} class="variant-attr-checkbox">
                            <span class="variant-attr-swatch" style="${colorStyle}"></span>
                            <span class="variant-attr-text">${escapeHtml(val.value)}</span>
                            <input type="color" class="variant-color-picker" data-value-id="${val.id}" value="${val.color_hex || '#cccccc'}" title="Edit color">
                        </label>`;
          } else {
            html += `
                        <label class="variant-attr-option ${checked ? 'selected' : ''}" data-value-id="${val.id}">
                            <input type="checkbox" name="attr_${attr.id}" value="${val.id}" ${checked} class="variant-attr-checkbox">
                            <span class="variant-attr-text">${escapeHtml(val.value)}</span>
                        </label>`;
          }
        });

        html += '</div></div>';
      });

      html += '</div>';
    }

    // Section 3: Pricing
    const strategy = data?.pricing_strategy || 'inherit';
    const priceAmount =
      data?.price_amount !== null && data?.price_amount !== undefined ? data.price_amount : '';
    const priceCurrency = data?.price_currency || window.__shopCurrency || 'USD';
    const productPrice = ctx.product_defaults?.price || 'N/A';

    html += `
        <div class="variant-modal-section">
            <h4><i class="fas fa-tag"></i> Pricing</h4>
            <div class="variant-modal-fields">
                <div class="variant-modal-field">
                    <label for="vm-pricing-strategy">Pricing Strategy</label>
                    <select id="vm-pricing-strategy">
                        <option value="inherit" ${strategy === 'inherit' ? 'selected' : ''}>Inherit from product (${escapeHtml(productPrice)})</option>
                        <option value="custom" ${strategy === 'custom' ? 'selected' : ''}>Custom price</option>
                    </select>
                </div>
                <div class="variant-modal-field" id="vm-price-field" style="${strategy !== 'custom' ? 'display:none' : ''}">
                    <label for="vm-price">Price</label>
                    <input type="number" id="vm-price" value="${priceAmount}" step="0.01" min="0" placeholder="0.00">
                </div>
            </div>
        </div>`;

    // Section 4: Images
    html += `
        <div class="variant-modal-section">
            <h4><i class="fas fa-images"></i> Images</h4>
            <div class="variant-modal-images-grid" id="vm-images-grid">
                ${renderModalImages(data?.images || [])}
            </div>
            <input type="hidden" id="vm-images-data" value="">
            <button type="button" class="button" id="vm-add-image-btn">
                <i class="fas fa-plus"></i> Add Images
            </button>
        </div>`;

    // Section 5: Physical Attributes
    const defaults = ctx.product_defaults || {};
    html += `
        <div class="variant-modal-section">
            <h4><i class="fas fa-ruler-combined"></i> Physical Attributes</h4>
            <div class="variant-modal-fields variant-modal-fields-4">
                <div class="variant-modal-field">
                    <label for="vm-weight">Weight (kg)</label>
                    <input type="number" id="vm-weight" value="${data?.weight || ''}" step="0.001" min="0" placeholder="${defaults.weight || 'Inherit'}">
                </div>
                <div class="variant-modal-field">
                    <label for="vm-length">Length (cm)</label>
                    <input type="number" id="vm-length" value="${data?.length || ''}" step="0.01" min="0" placeholder="${defaults.length || 'Inherit'}">
                </div>
                <div class="variant-modal-field">
                    <label for="vm-width">Width (cm)</label>
                    <input type="number" id="vm-width" value="${data?.width || ''}" step="0.01" min="0" placeholder="${defaults.width || 'Inherit'}">
                </div>
                <div class="variant-modal-field">
                    <label for="vm-height">Height (cm)</label>
                    <input type="number" id="vm-height" value="${data?.height || ''}" step="0.01" min="0" placeholder="${defaults.height || 'Inherit'}">
                </div>
            </div>
            <div class="variant-modal-fields">
                <div class="variant-modal-field">
                    <label for="vm-barcode">Barcode</label>
                    <input type="text" id="vm-barcode" value="${escapeHtml(data?.barcode || '')}" placeholder="UPC, EAN, etc.">
                </div>
                <div class="variant-modal-field">
                    <label for="vm-shipping-package">Shipping Package</label>
                    <select id="vm-shipping-package">
                        <option value="">Inherit from product</option>
                        ${(ctx.shipping_packages || [])
                          .map(
                            p =>
                              `<option value="${p.id}" ${data?.preferred_shipping_package_id === p.id ? 'selected' : ''}>${escapeHtml(p.name)}</option>`
                          )
                          .join('')}
                    </select>
                </div>
            </div>
        </div>`;

    // Section 6: Stock Management
    const stockItems = data?.stock_items || [];
    if (isEdit && stockItems.length > 0) {
      html += `
            <div class="variant-modal-section">
                <h4><i class="fas fa-warehouse"></i> Stock Management</h4>
                <table class="variant-stock-table">
                    <thead>
                        <tr>
                            <th>Warehouse</th>
                            <th>On Hand</th>
                            <th>Allocated</th>
                            <th>Available</th>
                            <th>Low Stock Threshold</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${stockItems
                          .map(
                            si => `
                            <tr data-stock-item-id="${si.stock_item_id}">
                                <td class="warehouse-name">${escapeHtml(si.warehouse_name)} <span class="warehouse-code">(${escapeHtml(si.warehouse_code)})</span></td>
                                <td><input type="number" class="stock-on-hand" value="${si.on_hand}" min="0" data-original="${si.on_hand}"></td>
                                <td class="stock-allocated">${si.allocated}</td>
                                <td class="stock-available">${si.available}</td>
                                <td><input type="number" class="stock-threshold" value="${si.low_stock_threshold}" min="0" data-original="${si.low_stock_threshold}"></td>
                            </tr>
                        `
                          )
                          .join('')}
                    </tbody>
                </table>
            </div>`;
    } else if (!isEdit && ctx.warehouses && ctx.warehouses.length > 0) {
      // For new variants, show warehouses with 0 stock (read-only info)
      html += `
            <div class="variant-modal-section">
                <h4><i class="fas fa-warehouse"></i> Stock Management</h4>
                <p class="help-text"><i class="fas fa-info-circle"></i> Stock can be managed after saving the variant.</p>
            </div>`;
    }

    modalBody.innerHTML = html;

    // Initialize event handlers
    initModalHandlers();
  }

  function renderModalImages(images) {
    if (!images || images.length === 0) {
      return `<div class="no-images-placeholder variant-modal-no-images">
                <i class="fas fa-images"></i>
                <p>No images added yet</p>
            </div>`;
    }

    return images
      .map(
        (img, idx) => `
            <div class="variant-modal-image-card" data-image-id="${img.id}" data-media-asset-id="${img.media_asset_id}">
                <div class="image-card-header">
                    <i class="fas fa-grip-vertical drag-handle"></i>
                    ${img.is_primary ? '<span class="primary-badge"><i class="fas fa-star"></i> Primary</span>' : ''}
                    <button type="button" class="image-card-delete" data-image-id="${img.id}" aria-label="Delete image">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="image-card-preview">
                    <img src="${escapeHtml(img.thumbnail_url || img.image_url)}" alt="${escapeHtml(img.alt_text)}">
                </div>
                <div class="image-card-details">
                    <div class="form-row">
                        <label>Alt Text</label>
                        <input type="text" class="image-alt-input" value="${escapeHtml(img.alt_text)}" placeholder="Alt text">
                    </div>
                    <div class="image-card-toggles">
                        <label class="toggle-label"><input type="checkbox" class="img-show-gallery" ${img.show_in_gallery ? 'checked' : ''}> Gallery</label>
                        <label class="toggle-label"><input type="checkbox" class="img-show-listing" ${img.show_in_listing ? 'checked' : ''}> Listing</label>
                        <label class="toggle-label"><input type="checkbox" class="img-is-primary" data-image-id="${img.id}" ${img.is_primary ? 'checked' : ''}> Primary</label>
                    </div>
                </div>
            </div>
        `
      )
      .join('');
  }

  function initModalHandlers() {
    // Pricing strategy toggle
    const strategySelect = document.getElementById('vm-pricing-strategy');
    const priceField = document.getElementById('vm-price-field');
    if (strategySelect && priceField) {
      strategySelect.addEventListener('change', () => {
        priceField.style.display = strategySelect.value === 'custom' ? '' : 'none';
      });
    }

    // Attribute checkboxes — toggle selected class + single selection per attribute group
    modalBody.querySelectorAll('.variant-attr-checkbox').forEach(cb => {
      cb.addEventListener('change', e => {
        const option = e.target.closest('.variant-attr-option');
        if (e.target.checked) {
          // Uncheck siblings — each attribute should have one selected value per variant
          const group = e.target.closest('.variant-modal-attr-values');
          group.querySelectorAll('.variant-attr-checkbox').forEach(other => {
            if (other !== e.target) {
              other.checked = false;
              other.closest('.variant-attr-option').classList.remove('selected');
            }
          });
          option.classList.add('selected');
        } else {
          option.classList.remove('selected');
        }
      });
    });

    // Color picker changes
    modalBody.querySelectorAll('.variant-color-picker').forEach(picker => {
      picker.addEventListener('change', async e => {
        const valueId = e.target.dataset.valueId;
        const newColor = e.target.value;
        // Update the swatch preview
        const option = e.target.closest('.variant-attr-option-color');
        if (option) {
          const swatch = option.querySelector('.variant-attr-swatch');
          if (swatch) swatch.style.backgroundColor = newColor;
        }
        // Save to backend
        try {
          await postJSON(`${BASE}/attribute-value/${valueId}/color/`, { color_hex: newColor });
        } catch (err) {
          console.error('[VariantCards] Error updating color:', err);
        }
      });
    });

    // Image add button
    const addImageBtn = document.getElementById('vm-add-image-btn');
    if (addImageBtn) {
      addImageBtn.addEventListener('click', () => {
        if (window.selectMultipleMedia) {
          window.selectMultipleMedia(
            selectedMedia => {
              addModalImages(selectedMedia);
            },
            { fileTypeFilter: 'image' }
          );
        }
      });
    }

    // Image delete buttons
    setupModalImageHandlers();

    // Stock on_hand change — update available
    modalBody.querySelectorAll('.stock-on-hand').forEach(input => {
      input.addEventListener('input', () => {
        const row = input.closest('tr');
        const allocated = parseInt(row.querySelector('.stock-allocated').textContent) || 0;
        const onHand = parseInt(input.value) || 0;
        row.querySelector('.stock-available').textContent = Math.max(0, onHand - allocated);
      });
    });
  }

  function setupModalImageHandlers() {
    // Delete buttons
    modalBody.querySelectorAll('.variant-modal-image-card .image-card-delete').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const card = e.target.closest('.variant-modal-image-card');
        card.remove();
        // Show placeholder if empty
        const grid = document.getElementById('vm-images-grid');
        if (grid && grid.querySelectorAll('.variant-modal-image-card').length === 0) {
          grid.innerHTML = renderModalImages([]);
        }
      });
    });

    // Primary toggles — radio behavior
    modalBody.querySelectorAll('.img-is-primary').forEach(toggle => {
      toggle.addEventListener('change', e => {
        if (e.target.checked) {
          modalBody.querySelectorAll('.img-is-primary').forEach(other => {
            if (other !== e.target) {
              other.checked = false;
              const otherCard = other.closest('.variant-modal-image-card');
              const badge = otherCard?.querySelector('.primary-badge');
              if (badge) badge.remove();
            }
          });
          const card = e.target.closest('.variant-modal-image-card');
          const header = card?.querySelector('.image-card-header');
          if (header && !header.querySelector('.primary-badge')) {
            const handle = header.querySelector('.drag-handle');
            handle?.insertAdjacentHTML(
              'afterend',
              '<span class="primary-badge"><i class="fas fa-star"></i> Primary</span>'
            );
          }
        } else {
          const card = e.target.closest('.variant-modal-image-card');
          const badge = card?.querySelector('.primary-badge');
          if (badge) badge.remove();
        }
      });
    });
  }

  function addModalImages(selectedMedia) {
    if (!selectedMedia || selectedMedia.length === 0) return;
    const grid = document.getElementById('vm-images-grid');
    if (!grid) return;

    // Remove placeholder
    const placeholder = grid.querySelector('.variant-modal-no-images');
    if (placeholder) placeholder.remove();

    selectedMedia.forEach((media, index) => {
      const id = `new_${Date.now()}_${index}`;
      const cardHtml = `
            <div class="variant-modal-image-card" data-image-id="${id}" data-media-asset-id="${media.id}">
                <div class="image-card-header">
                    <i class="fas fa-grip-vertical drag-handle"></i>
                    <button type="button" class="image-card-delete" data-image-id="${id}" aria-label="Delete image">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="image-card-preview">
                    <img src="${escapeHtml(media.url)}" alt="${escapeHtml(media.title || '')}">
                </div>
                <div class="image-card-details">
                    <div class="form-row">
                        <label>Alt Text</label>
                        <input type="text" class="image-alt-input" value="${escapeHtml(media.title || '')}" placeholder="Alt text">
                    </div>
                    <div class="image-card-toggles">
                        <label class="toggle-label"><input type="checkbox" class="img-show-gallery" checked> Gallery</label>
                        <label class="toggle-label"><input type="checkbox" class="img-show-listing" checked> Listing</label>
                        <label class="toggle-label"><input type="checkbox" class="img-is-primary" data-image-id="${id}"> Primary</label>
                    </div>
                </div>
            </div>`;
      grid.insertAdjacentHTML('beforeend', cardHtml);
    });

    setupModalImageHandlers();
  }

  function collectModalData() {
    const data = {
      name: document.getElementById('vm-name')?.value?.trim() || '',
      sku: document.getElementById('vm-sku')?.value?.trim() || '',
      is_active: document.getElementById('vm-is-active')?.checked ?? true,
      pricing_strategy: document.getElementById('vm-pricing-strategy')?.value || 'inherit',
      barcode: document.getElementById('vm-barcode')?.value?.trim() || '',
      weight: document.getElementById('vm-weight')?.value || null,
      length: document.getElementById('vm-length')?.value || null,
      width: document.getElementById('vm-width')?.value || null,
      height: document.getElementById('vm-height')?.value || null,
    };

    // Price
    if (data.pricing_strategy === 'custom') {
      data.price_amount = parseFloat(document.getElementById('vm-price')?.value) || 0;
      data.price_currency =
        (formContext && formContext.default_currency) || window.__shopCurrency || 'USD';
    }

    // Shipping package
    const pkgSelect = document.getElementById('vm-shipping-package');
    data.preferred_shipping_package_id = pkgSelect?.value ? parseInt(pkgSelect.value) : null;

    // Selected attributes — collect checked checkboxes
    const selectedIds = [];
    modalBody.querySelectorAll('.variant-attr-checkbox:checked').forEach(cb => {
      selectedIds.push(parseInt(cb.value));
    });
    data.selected_attribute_ids = selectedIds;

    return data;
  }

  function collectStockData() {
    const stockItems = [];
    modalBody.querySelectorAll('.variant-stock-table tbody tr').forEach(row => {
      const stockItemId = parseInt(row.dataset.stockItemId);
      const onHandInput = row.querySelector('.stock-on-hand');
      const thresholdInput = row.querySelector('.stock-threshold');

      const onHand = parseInt(onHandInput?.value) || 0;
      const threshold = parseInt(thresholdInput?.value) || 0;
      const originalOnHand = parseInt(onHandInput?.dataset.original) || 0;
      const originalThreshold = parseInt(thresholdInput?.dataset.original) || 0;

      // Only include if changed
      if (onHand !== originalOnHand || threshold !== originalThreshold) {
        stockItems.push({
          stock_item_id: stockItemId,
          on_hand: onHand,
          low_stock_threshold: threshold,
        });
      }
    });
    return stockItems;
  }

  function collectImageData() {
    const grid = document.getElementById('vm-images-grid');
    if (!grid) return [];

    const cards = grid.querySelectorAll('.variant-modal-image-card');
    const images = [];
    cards.forEach((card, idx) => {
      const imageId = card.dataset.imageId;
      const mediaAssetId = card.dataset.mediaAssetId;
      images.push({
        id: imageId?.startsWith('new_') ? null : imageId,
        media_asset_id: mediaAssetId,
        alt_text: card.querySelector('.image-alt-input')?.value || '',
        show_in_gallery: card.querySelector('.img-show-gallery')?.checked ?? true,
        show_in_listing: card.querySelector('.img-show-listing')?.checked ?? true,
        is_primary: card.querySelector('.img-is-primary')?.checked ?? false,
        position: idx,
      });
    });
    return images;
  }

  async function saveVariant() {
    const data = collectModalData();

    // Validation
    if (!data.name) {
      showNotification('Variant name is required.', 'error');
      return;
    }
    if (!data.sku) {
      showNotification('SKU is required.', 'error');
      return;
    }

    saveBtn.disabled = true;
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

    try {
      let result;
      if (currentVariantId) {
        // Update existing
        result = await postJSON(`${BASE}/variant/${currentVariantId}/update/`, data);
      } else {
        // Create new
        result = await postJSON(`${BASE}/product/${PRODUCT_ID}/variants/create/`, data);
        currentVariantId = result.variant.id;
      }

      // Update stock if changed
      const stockData = collectStockData();
      if (stockData.length > 0) {
        await postJSON(`${BASE}/variant/${currentVariantId}/stock/update/`, {
          stock_items: stockData,
        });
      }

      // Update images
      const imageData = collectImageData();
      if (imageData.length > 0 || currentVariantId) {
        await postJSON(`${BASE}/variant/${currentVariantId}/images/update/`, { images: imageData });
      }

      // Refresh list
      await loadVariants();
      closeModal();
      showNotification(result.message || 'Variant saved successfully.', 'success');
    } catch (err) {
      showNotification(err.message || 'Failed to save variant.', 'error');
    } finally {
      saveBtn.disabled = false;
      saveBtn.innerHTML = '<i class="fas fa-check"></i> Save Variant';
    }
  }

  async function deleteVariant(variantId) {
    const variant = variants.find(v => v.id === variantId);
    const name = variant ? variant.name : 'this variant';

    if (
      !(await AdminModal.confirm({
        message: `Are you sure you want to delete "${name}"? This action cannot be undone.`,
        danger: true,
        confirmText: 'Delete',
      }))
    )
      return;

    try {
      await postJSON(`${BASE}/variant/${variantId}/delete/`, {});
      await loadVariants();
      showNotification(`Variant "${name}" deleted.`, 'success');
    } catch (err) {
      showNotification(err.message || 'Failed to delete variant.', 'error');
    }
  }

  // ===== Init =====

  function init() {
    const variationsPanel = document.getElementById('panel-variations');
    if (!variationsPanel) return;

    // Populate DOM refs
    listEl = document.getElementById('variant-list');
    loadingEl = document.getElementById('variant-list-loading');
    countBadge = document.getElementById('variant-count-badge');
    addBtn = document.getElementById('add-variant-btn');
    overlay = document.getElementById('variant-modal-overlay');
    modal = document.getElementById('variant-modal');
    modalTitle = document.getElementById('variant-modal-title');
    modalBody = document.getElementById('variant-modal-body');
    saveBtn = document.getElementById('variant-modal-save');
    cancelBtn = document.getElementById('variant-modal-cancel');
    closeBtn = document.getElementById('variant-modal-close');

    if (!listEl) return;

    // Event binding
    if (addBtn) addBtn.addEventListener('click', openCreateModal);
    if (saveBtn) saveBtn.addEventListener('click', saveVariant);
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (overlay) {
      overlay.addEventListener('click', e => {
        if (e.target === overlay) closeModal();
      });
    }

    // Refresh form context when product attributes change
    document.addEventListener('product-attributes-changed', () => {
      loadFormContext();
    });

    // Load data
    Promise.all([loadVariants(), loadFormContext()]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
