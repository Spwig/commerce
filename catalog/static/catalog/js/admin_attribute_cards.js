/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Attribute Cards Manager
 * AJAX-based product attribute assignment management.
 * Allows adding/removing attributes and toggling allowed values.
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

  const API_BASE = '/api/catalog';
  const LANG = getLanguagePrefix();
  const ADMIN_BASE = `${LANG}/admin/catalog`;

  async function fetchJSON(url) {
    const resp = await fetch(url, { credentials: 'same-origin' });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return resp.json();
  }

  async function postJSON(url, body) {
    const resp = await fetch(url, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
      },
      body: JSON.stringify(body),
    });
    if (!resp.ok) {
      const data = await resp.json().catch(() => ({}));
      throw new Error(data.error || data.detail || `HTTP ${resp.status}`);
    }
    return resp.json();
  }

  // ===== State =====

  let productId = null;
  let assignments = [];

  // ===== DOM References =====

  let listEl, countBadge, builderBanner;

  // ===== Type icons =====

  const TYPE_ICONS = {
    select: 'fa-list',
    color: 'fa-palette',
    button: 'fa-hand-pointer',
    radio: 'fa-dot-circle',
  };

  const TYPE_LABELS = {
    select: 'Dropdown',
    color: 'Color Swatch',
    button: 'Button',
    radio: 'Radio',
  };

  // ===== Load & Render =====

  async function loadAssignments() {
    try {
      const data = await fetchJSON(`${API_BASE}/products/${productId}/attribute-assignments/`);
      assignments = data.assignments || [];
      renderList();
    } catch (err) {
      console.error('[AttributeCards] Failed to load:', err);
      listEl.innerHTML = `
                <div class="attr-list-empty">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Failed to load attributes</p>
                </div>
            `;
    }
  }

  function renderList() {
    countBadge.textContent = assignments.length;

    // Show/hide variation builder
    if (builderBanner) {
      builderBanner.style.display = assignments.length === 0 ? 'none' : 'flex';
    }

    if (assignments.length === 0) {
      listEl.innerHTML = `
                <div class="attr-list-empty">
                    <i class="fas fa-tags"></i>
                    <p>No attributes assigned</p>
                    <p style="font-size:0.8rem;opacity:0.7;">Add attributes like Size, Color, or Material to create product variations</p>
                </div>
            `;
      return;
    }

    listEl.innerHTML = assignments.map(a => renderCard(a)).join('');

    // Bind events
    listEl.querySelectorAll('.attr-value-pill').forEach(pill => {
      pill.addEventListener('click', e => {
        // Don't toggle when clicking the color picker
        if (e.target.closest('.attr-color-picker-wrap')) return;
        toggleValue(pill);
      });
    });
    listEl.querySelectorAll('.attr-card-remove').forEach(btn => {
      btn.addEventListener('click', () => removeAttribute(btn));
    });

    // Bind color picker inputs
    listEl.querySelectorAll('.attr-color-input').forEach(input => {
      input.addEventListener('click', e => e.stopPropagation());
      input.addEventListener('change', e => {
        e.stopPropagation();
        updateColor(input);
      });
    });
  }

  function renderCard(assignment) {
    const attr = assignment.attribute;
    const icon = TYPE_ICONS[attr.type] || 'fa-tag';
    const enabledCount = assignment.values.filter(v => v.enabled).length;
    const totalCount = assignment.values.length;
    const isColor = attr.type === 'color';

    const valuesHtml = assignment.values
      .map(v => {
        const cls = v.enabled ? 'enabled' : 'disabled';
        const iconHtml = v.enabled
          ? '<i class="fas fa-check pill-icon"></i>'
          : '<i class="fas fa-plus pill-icon"></i>';

        let colorHtml = '';
        if (isColor) {
          const hasColor = v.color_hex && v.color_hex !== '';
          const dotStyle = hasColor ? `background:${escapeHtml(v.color_hex)}` : '';
          const dotCls = hasColor ? 'attr-color-dot' : 'attr-color-dot attr-color-dot-empty';
          colorHtml = `<label class="attr-color-picker-wrap" title="Click to set color">
                    <span class="${dotCls}" style="${dotStyle}"></span>
                    <input type="color" class="attr-color-input" data-value-id="${v.id}" value="${escapeHtml(v.color_hex || '#cccccc')}">
                </label>`;
        }

        return `<span class="attr-value-pill ${cls}"
                          data-assignment-id="${assignment.id}"
                          data-value-id="${v.id}"
                          data-enabled="${v.enabled}"
                          title="${v.enabled ? 'Click to disable' : 'Click to enable'}"
                    >${iconHtml}${colorHtml}${escapeHtml(v.value)}</span>`;
      })
      .join('');

    return `
            <div class="attr-card" data-assignment-id="${assignment.id}">
                <div class="attr-card-header">
                    <div class="attr-card-icon"><i class="fas ${icon}"></i></div>
                    <span class="attr-card-name">${escapeHtml(attr.name)}</span>
                    <span class="attr-card-meta">${enabledCount}/${totalCount} ${TYPE_LABELS[attr.type] || attr.type}</span>
                    <button type="button" class="attr-card-remove" data-assignment-id="${assignment.id}" title="Remove attribute">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
                <div class="attr-card-values">${valuesHtml}</div>
            </div>
        `;
  }

  // ===== Update Color =====

  async function updateColor(input) {
    const valueId = input.dataset.valueId;
    const newColor = input.value;

    // Update the swatch dot immediately
    const dot = input.closest('.attr-color-picker-wrap').querySelector('.attr-color-dot');
    if (dot) {
      dot.style.background = newColor;
      dot.classList.remove('attr-color-dot-empty');
    }

    try {
      await postJSON(`${ADMIN_BASE}/attribute-value/${valueId}/color/`, { color_hex: newColor });
      // Update local state
      for (const a of assignments) {
        const val = a.values.find(v => v.id == valueId);
        if (val) {
          val.color_hex = newColor;
          break;
        }
      }
      notifyAttributesChanged();
    } catch (err) {
      console.error('[AttributeCards] Failed to update color:', err);
      showNotification('Failed to update color: ' + err.message, 'error');
    }
  }

  // ===== Toggle Value =====

  async function toggleValue(pill) {
    const assignmentId = pill.dataset.assignmentId;
    const valueId = parseInt(pill.dataset.valueId);
    const currentlyEnabled = pill.dataset.enabled === 'true';

    // Find the assignment
    const assignment = assignments.find(a => a.id == assignmentId);
    if (!assignment) return;

    // Compute new allowed set
    const newIds = assignment.values
      .filter(v => {
        if (v.id === valueId) return !currentlyEnabled;
        return v.enabled;
      })
      .map(v => v.id);

    // Optimistic UI update
    pill.dataset.enabled = String(!currentlyEnabled);
    if (!currentlyEnabled) {
      pill.classList.remove('disabled');
      pill.classList.add('enabled');
      pill.querySelector('.pill-icon').classList.replace('fa-plus', 'fa-check');
      pill.title = 'Click to disable';
    } else {
      pill.classList.remove('enabled');
      pill.classList.add('disabled');
      pill.querySelector('.pill-icon').classList.replace('fa-check', 'fa-plus');
      pill.title = 'Click to enable';
    }

    // Update meta count
    const card = pill.closest('.attr-card');
    const enabledPills = card.querySelectorAll('.attr-value-pill.enabled').length;
    const totalPills = card.querySelectorAll('.attr-value-pill').length;
    const metaEl = card.querySelector('.attr-card-meta');
    if (metaEl) {
      const typeLabel = metaEl.textContent.replace(/^\d+\/\d+\s*/, '');
      metaEl.textContent = `${enabledPills}/${totalPills} ${typeLabel}`;
    }

    try {
      await postJSON(
        `${API_BASE}/products/${productId}/attribute-assignments/${assignmentId}/values/`,
        {
          allowed_value_ids: newIds,
        }
      );
      // Update local state
      assignment.values.forEach(v => {
        v.enabled = newIds.includes(v.id);
      });
      notifyAttributesChanged();
    } catch (err) {
      console.error('[AttributeCards] Failed to update values:', err);
      showNotification('Failed to update values: ' + err.message, 'error');
      // Revert
      await loadAssignments();
    }
  }

  // ===== Remove Attribute =====

  async function removeAttribute(btn) {
    const assignmentId = btn.dataset.assignmentId;
    const assignment = assignments.find(a => a.id == assignmentId);
    const name = assignment ? assignment.attribute.name : 'this attribute';

    if (
      !(await AdminModal.confirm({
        message: `Remove "${name}" from this product?\n\nVariants using this attribute will not be deleted, but their attribute selections may become orphaned.`,
        danger: true,
        confirmText: 'Remove',
      }))
    ) {
      return;
    }

    try {
      const data = await postJSON(
        `${API_BASE}/products/${productId}/attribute-assignments/${assignmentId}/remove/`,
        {}
      );
      showNotification(data.message || 'Attribute removed', 'success');
      await loadAssignments();
      notifyAttributesChanged();
    } catch (err) {
      console.error('[AttributeCards] Failed to remove:', err);
      showNotification('Failed to remove attribute: ' + err.message, 'error');
    }
  }

  // ===== Add Attribute Modal =====

  let searchDebounce = null;

  function openAddModal() {
    const overlay = document.getElementById('add-attr-modal-overlay');
    if (!overlay) return;
    overlay.style.display = 'flex';

    const input = document.getElementById('attr-search-input');
    if (input) {
      input.value = '';
      input.focus();
    }

    // Load all available immediately
    searchAttributes('');
  }

  async function searchAttributes(query) {
    const resultsEl = document.getElementById('attr-search-results');
    if (!resultsEl) return;

    try {
      const url = `${API_BASE}/products/${productId}/attribute-assignments/search/?q=${encodeURIComponent(query)}`;
      const data = await fetchJSON(url);
      const attrs = data.attributes || [];

      if (attrs.length === 0) {
        resultsEl.innerHTML = `
                    <div class="attr-search-empty">
                        <i class="fas fa-search"></i>
                        <p>${query ? 'No matching attributes found' : 'All attributes are already assigned'}</p>
                    </div>
                `;
        return;
      }

      resultsEl.innerHTML = attrs
        .map(attr => {
          const icon = TYPE_ICONS[attr.type] || 'fa-tag';
          return `
                    <div class="attr-search-result">
                        <div class="attr-card-icon"><i class="fas ${icon}"></i></div>
                        <div class="attr-search-result-info">
                            <div class="attr-search-result-name">${escapeHtml(attr.name)}</div>
                            <div class="attr-search-result-meta">${TYPE_LABELS[attr.type] || attr.type} &middot; ${attr.value_count} values</div>
                        </div>
                        <button type="button" class="attr-search-result-add" data-attribute-id="${attr.id}">
                            <i class="fas fa-plus"></i> Add
                        </button>
                    </div>
                `;
        })
        .join('');

      // Bind add buttons
      resultsEl.querySelectorAll('.attr-search-result-add').forEach(btn => {
        btn.addEventListener('click', async () => {
          btn.disabled = true;
          btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
          try {
            await postJSON(`${API_BASE}/products/${productId}/attribute-assignments/add/`, {
              attribute_id: parseInt(btn.dataset.attributeId),
            });
            showNotification('Attribute added', 'success');
            closeModal('add-attr-modal-overlay');
            await loadAssignments();
            notifyAttributesChanged();
          } catch (err) {
            showNotification('Failed to add: ' + err.message, 'error');
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-plus"></i> Add';
          }
        });
      });
    } catch (err) {
      console.error('[AttributeCards] Search failed:', err);
      resultsEl.innerHTML = `
                <div class="attr-search-empty">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Search failed</p>
                </div>
            `;
    }
  }

  // ===== Create Attribute Modal =====

  function openCreateModal() {
    const overlay = document.getElementById('create-attr-modal-overlay');
    if (!overlay) return;
    overlay.style.display = 'flex';

    // Clear form
    const nameInput = document.getElementById('new-attr-name');
    const typeSelect = document.getElementById('new-attr-type');
    const valuesInput = document.getElementById('new-attr-values');
    if (nameInput) nameInput.value = '';
    if (typeSelect) typeSelect.value = 'select';
    if (valuesInput) valuesInput.value = '';
    if (nameInput) nameInput.focus();
  }

  async function saveNewAttribute() {
    const nameInput = document.getElementById('new-attr-name');
    const typeSelect = document.getElementById('new-attr-type');
    const valuesInput = document.getElementById('new-attr-values');

    const name = (nameInput ? nameInput.value : '').trim();
    const type = typeSelect ? typeSelect.value : 'select';
    const valuesRaw = (valuesInput ? valuesInput.value : '').trim();

    if (!name) {
      showNotification('Attribute name is required', 'error');
      if (nameInput) nameInput.focus();
      return;
    }

    if (!valuesRaw) {
      showNotification('At least one value is required', 'error');
      if (valuesInput) valuesInput.focus();
      return;
    }

    const values = valuesRaw
      .split(',')
      .map(v => v.trim())
      .filter(v => v);
    if (values.length === 0) {
      showNotification('At least one value is required', 'error');
      return;
    }

    const saveBtn = document.getElementById('create-attr-save');
    if (saveBtn) {
      saveBtn.disabled = true;
      saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
    }

    try {
      // Use existing quick-add-attribute admin endpoint
      const resp = await fetch(`${ADMIN_BASE}/quick-add-attribute/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': AdminUtils.getCsrfToken(),
        },
        body: JSON.stringify({
          attribute_name: name,
          attribute_type: type,
          values: values,
          product_id: productId,
        }),
      });
      const data = await resp.json();

      if (!data.success) {
        throw new Error((data.errors || []).join(', ') || 'Creation failed');
      }

      showNotification(`Attribute "${name}" created with ${values.length} values`, 'success');
      closeModal('create-attr-modal-overlay');
      await loadAssignments();
      notifyAttributesChanged();
    } catch (err) {
      console.error('[AttributeCards] Create failed:', err);
      showNotification('Failed to create: ' + err.message, 'error');
    } finally {
      if (saveBtn) {
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i class="fas fa-check"></i> Create Attribute';
      }
    }
  }

  // ===== Modal Helpers =====

  function closeModal(overlayId) {
    const overlay = document.getElementById(overlayId);
    if (overlay) overlay.style.display = 'none';
  }

  function notifyAttributesChanged() {
    document.dispatchEvent(new CustomEvent('product-attributes-changed'));
  }

  // ===== Init =====

  function init() {
    productId = getProductId();
    if (!productId) return;

    listEl = document.getElementById('attr-list');
    countBadge = document.getElementById('attr-count-badge');
    builderBanner = document.getElementById('variation-builder-banner');

    if (!listEl) return;

    // Add Attribute button
    const addBtn = document.getElementById('add-attribute-btn');
    if (addBtn) addBtn.addEventListener('click', openAddModal);

    // Create New button
    const createBtn = document.getElementById('create-attribute-btn');
    if (createBtn) createBtn.addEventListener('click', openCreateModal);

    // Create Attribute save button
    const createSaveBtn = document.getElementById('create-attr-save');
    if (createSaveBtn) createSaveBtn.addEventListener('click', saveNewAttribute);

    // Modal close buttons
    document
      .querySelectorAll('.attr-modal-close, .attr-modal-footer .button[data-modal]')
      .forEach(btn => {
        const modalId = btn.dataset.modal;
        if (modalId) {
          btn.addEventListener('click', () => closeModal(modalId));
        }
      });

    // Click overlay to close
    document.querySelectorAll('.attr-modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', e => {
        if (e.target === overlay) closeModal(overlay.id);
      });
    });

    // Search input debounce
    const searchInput = document.getElementById('attr-search-input');
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        clearTimeout(searchDebounce);
        searchDebounce = setTimeout(() => {
          searchAttributes(searchInput.value.trim());
        }, 250);
      });
    }

    // Load assignments
    loadAssignments();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
