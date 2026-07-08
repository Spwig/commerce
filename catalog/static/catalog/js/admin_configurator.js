/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Configurator Cards Manager
 * AJAX-based slot and preset management for configurable products.
 * Replaces Django inlines with compact card rows + modal editing.
 */
(function() {
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
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
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

    if (!PRODUCT_ID) return; // New product

    // Common icon options for slot icons
    const ICON_OPTIONS = [
        { value: '', label: 'None' },
        { value: 'fas fa-microchip', label: 'Microchip (CPU)' },
        { value: 'fas fa-memory', label: 'Memory (RAM)' },
        { value: 'fas fa-hdd', label: 'Storage (HDD)' },
        { value: 'fas fa-desktop', label: 'Monitor' },
        { value: 'fas fa-keyboard', label: 'Keyboard' },
        { value: 'fas fa-palette', label: 'Color/Paint' },
        { value: 'fas fa-shoe-prints', label: 'Shoes' },
        { value: 'fas fa-tshirt', label: 'Clothing' },
        { value: 'fas fa-gem', label: 'Gem/Jewelry' },
        { value: 'fas fa-bolt', label: 'Power' },
        { value: 'fas fa-cog', label: 'Gear/Settings' },
        { value: 'fas fa-puzzle-piece', label: 'Component' },
        { value: 'fas fa-layer-group', label: 'Layers' },
        { value: 'fas fa-plus-circle', label: 'Add-ons' },
        { value: 'fas fa-star', label: 'Star/Premium' },
        { value: 'fas fa-box', label: 'Package' },
        { value: 'fas fa-tools', label: 'Tools' },
        { value: 'fas fa-shield-alt', label: 'Protection' },
        { value: 'fas fa-paint-brush', label: 'Design' },
    ];

    let currentSlotId = null;   // null = creating new slot
    let currentPresetId = null; // null = creating new preset

    // DOM refs
    let slotListEl, slotLoadingEl, slotCountBadge, addSlotBtn;
    let slotOverlay, slotModal, slotModalTitle, slotModalBody, slotSaveBtn;
    let presetListEl, presetLoadingEl, presetCountBadge, addPresetBtn;
    let presetOverlay, presetModal, presetModalTitle, presetModalBody, presetSaveBtn;

    // ===================================================================
    // SLOT MANAGEMENT
    // ===================================================================

    async function loadSlots() {
        try {
            const data = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/slots/list/`);
            renderSlotList(data.slots || []);
            if (slotCountBadge) slotCountBadge.textContent = data.count || 0;
        } catch (err) {
            console.error('[Configurator] Error loading slots:', err);
            if (slotListEl) slotListEl.innerHTML = '<div class="config-list-error"><i class="fas fa-exclamation-triangle"></i> Failed to load slots</div>';
        }
    }

    function renderSlotList(slots) {
        if (!slotListEl) return;
        if (!slots.length) {
            slotListEl.innerHTML = `
                <div class="config-slot-empty">
                    <i class="fas fa-layer-group"></i>
                    <p>No configuration slots yet</p>
                    <button type="button" class="button" data-action="trigger-add-slot">
                        <i class="fas fa-plus"></i> Add Your First Slot
                    </button>
                </div>
            `;
            var addSlotTrigger = slotListEl.querySelector('[data-action="trigger-add-slot"]');
            if (addSlotTrigger) {
                addSlotTrigger.addEventListener('click', function() {
                    document.getElementById('add-slot-btn').click();
                });
            }
            return;
        }

        slotListEl.innerHTML = slots.map(s => renderSlotRow(s)).join('');

        // Bind click events
        slotListEl.querySelectorAll('[data-edit-slot]').forEach(btn => {
            btn.addEventListener('click', e => {
                e.preventDefault();
                openSlotModal(parseInt(btn.dataset.editSlot));
            });
        });
        slotListEl.querySelectorAll('[data-delete-slot]').forEach(btn => {
            btn.addEventListener('click', e => {
                e.preventDefault();
                deleteSlot(parseInt(btn.dataset.deleteSlot), btn.dataset.slotName);
            });
        });
    }

    function renderSlotRow(s) {
        const icon = escapeHtml(s.icon || 'fas fa-puzzle-piece');
        const name = escapeHtml(s.name);
        const desc = s.description ? escapeHtml(s.description.substring(0, 80)) : '';
        const reqBadge = s.is_required
            ? '<span class="config-slot-row__badge config-slot-row__badge--required">Required</span>'
            : '<span class="config-slot-row__badge config-slot-row__badge--optional">Optional</span>';
        const selType = s.max_selections > 1
            ? `<span class="config-slot-row__badge">Multi (${s.min_selections}-${s.max_selections})</span>`
            : '<span class="config-slot-row__badge">Single select</span>';

        return `
            <div class="config-slot-row" data-slot-id="${s.id}">
                <div class="config-slot-row__icon"><i class="${icon}"></i></div>
                <div class="config-slot-row__info">
                    <span class="config-slot-row__name">${name}</span>
                    ${desc ? `<span class="config-slot-row__desc">${desc}</span>` : ''}
                </div>
                <div class="config-slot-row__badges">
                    ${reqBadge}
                    ${selType}
                </div>
                <div class="config-slot-row__options-count">
                    <span class="config-slot-row__count-pill">${s.option_count}</span>
                    <span>options</span>
                </div>
                <div class="config-slot-row__actions">
                    <a href="${escapeHtml(s.options_url)}" class="config-slot-row__action" title="Manage Options">
                        <i class="fas fa-list"></i>
                    </a>
                    <button type="button" class="config-slot-row__action" data-edit-slot="${s.id}" title="Edit Slot">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button type="button" class="config-slot-row__action config-slot-row__action--danger" data-delete-slot="${s.id}" data-slot-name="${escapeHtml(s.name)}" title="Delete Slot">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    }

    async function openSlotModal(slotId) {
        currentSlotId = slotId || null;

        if (slotId) {
            // Edit existing
            try {
                const data = await fetchJSON(`${BASE}/slot/${slotId}/detail/`);
                renderSlotModalContent(data.slot);
                slotModalTitle.textContent = 'Edit Slot';
            } catch (err) {
                showNotification('Failed to load slot: ' + err.message, 'error');
                return;
            }
        } else {
            // Create new
            renderSlotModalContent(null);
            slotModalTitle.textContent = 'Add Slot';
        }

        slotOverlay.style.display = 'flex';
        document.addEventListener('keydown', slotEscHandler);
    }

    function closeSlotModal() {
        slotOverlay.style.display = 'none';
        currentSlotId = null;
        document.removeEventListener('keydown', slotEscHandler);
    }

    function slotEscHandler(e) {
        if (e.key === 'Escape') closeSlotModal();
    }

    function renderSlotModalContent(data) {
        const d = data || {};
        const iconOptions = ICON_OPTIONS.map(o =>
            `<option value="${escapeHtml(o.value)}" ${d.icon === o.value ? 'selected' : ''}>${escapeHtml(o.label)}</option>`
        ).join('');

        slotModalBody.innerHTML = `
            <div class="config-modal-section">
                <h4><i class="fas fa-info-circle"></i> Basic Info</h4>
                <div class="config-modal-field">
                    <label for="slot-name">Name <span class="required">*</span></label>
                    <input type="text" id="slot-name" value="${escapeHtml(d.name || '')}" placeholder="e.g. Processor, Color, Material" autocomplete="off">
                </div>
                <div class="config-modal-field">
                    <label for="slot-slug">Slug</label>
                    <input type="text" id="slot-slug" value="${escapeHtml(d.slug || '')}" placeholder="Auto-generated from name">
                </div>
                <div class="config-modal-field">
                    <label for="slot-description">Description</label>
                    <textarea id="slot-description" rows="2" placeholder="Shown to customers when selecting options">${escapeHtml(d.description || '')}</textarea>
                </div>
                <div class="config-modal-field">
                    <label for="slot-icon">Icon</label>
                    <select id="slot-icon">${iconOptions}</select>
                </div>
            </div>
            <div class="config-modal-section">
                <h4><i class="fas fa-sliders-h"></i> Selection Rules</h4>
                <div class="config-modal-row">
                    <div class="config-modal-field config-modal-field--checkbox">
                        <label>
                            <input type="checkbox" id="slot-required" ${d.is_required !== false ? 'checked' : ''}>
                            Required
                        </label>
                        <span class="config-modal-help">Customer must select an option</span>
                    </div>
                </div>
                <div class="config-modal-row">
                    <div class="config-modal-field">
                        <label for="slot-min">Min Selections</label>
                        <input type="number" id="slot-min" value="${d.min_selections || 1}" min="0" max="20">
                    </div>
                    <div class="config-modal-field">
                        <label for="slot-max">Max Selections</label>
                        <input type="number" id="slot-max" value="${d.max_selections || 1}" min="1" max="20">
                    </div>
                    <div class="config-modal-field">
                        <label for="slot-order">Sort Order</label>
                        <input type="number" id="slot-order" value="${d.sort_order || 0}" min="0">
                    </div>
                </div>
            </div>
        `;

        // Auto-generate slug from name
        const nameInput = document.getElementById('slot-name');
        const slugInput = document.getElementById('slot-slug');
        if (nameInput && slugInput && !currentSlotId) {
            nameInput.addEventListener('input', () => {
                slugInput.value = nameInput.value.toLowerCase()
                    .replace(/[^\w\s-]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-');
            });
        }
    }

    function collectSlotData() {
        return {
            name: document.getElementById('slot-name')?.value?.trim() || '',
            slug: document.getElementById('slot-slug')?.value?.trim() || '',
            description: document.getElementById('slot-description')?.value?.trim() || '',
            icon: document.getElementById('slot-icon')?.value || '',
            is_required: document.getElementById('slot-required')?.checked ?? true,
            min_selections: parseInt(document.getElementById('slot-min')?.value || '1'),
            max_selections: parseInt(document.getElementById('slot-max')?.value || '1'),
            sort_order: parseInt(document.getElementById('slot-order')?.value || '0'),
        };
    }

    async function saveSlot() {
        const data = collectSlotData();
        if (!data.name) {
            showNotification('Name is required.', 'error');
            return;
        }

        try {
            if (currentSlotId) {
                await postJSON(`${BASE}/slot/${currentSlotId}/update/`, data);
                showNotification('Slot updated.', 'success');
            } else {
                await postJSON(`${BASE}/product/${PRODUCT_ID}/slots/create/`, data);
                showNotification('Slot created.', 'success');
            }
            closeSlotModal();
            await loadSlots();
        } catch (err) {
            showNotification('Error: ' + err.message, 'error');
        }
    }

    async function deleteSlot(slotId, slotName) {
        if (!await AdminModal.confirm({ message: `Delete slot "${slotName || 'this slot'}"?\n\nThis will also delete all options and compatibility rules for this slot.`, danger: true, confirmText: 'Delete' })) {
            return;
        }
        try {
            await postJSON(`${BASE}/slot/${slotId}/delete/`, {});
            showNotification('Slot deleted.', 'success');
            await loadSlots();
        } catch (err) {
            showNotification('Error: ' + err.message, 'error');
        }
    }

    // ===================================================================
    // PRESET MANAGEMENT
    // ===================================================================

    async function loadPresets() {
        try {
            const data = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/presets/list/`);
            renderPresetList(data.presets || []);
            if (presetCountBadge) presetCountBadge.textContent = data.count || 0;
        } catch (err) {
            console.error('[Configurator] Error loading presets:', err);
            if (presetListEl) presetListEl.innerHTML = '<div class="config-list-error"><i class="fas fa-exclamation-triangle"></i> Failed to load presets</div>';
        }
    }

    function renderPresetList(presets) {
        if (!presetListEl) return;
        if (!presets.length) {
            presetListEl.innerHTML = `
                <div class="config-preset-empty">
                    <i class="fas fa-magic"></i>
                    <p>No presets yet</p>
                    <button type="button" class="button" data-action="trigger-add-preset">
                        <i class="fas fa-plus"></i> Add Your First Preset
                    </button>
                </div>
            `;
            var addPresetTrigger = presetListEl.querySelector('[data-action="trigger-add-preset"]');
            if (addPresetTrigger) {
                addPresetTrigger.addEventListener('click', function() {
                    document.getElementById('add-preset-btn').click();
                });
            }
            return;
        }

        presetListEl.innerHTML = presets.map(p => renderPresetRow(p)).join('');

        // Bind events
        presetListEl.querySelectorAll('[data-edit-preset]').forEach(btn => {
            btn.addEventListener('click', e => {
                e.preventDefault();
                openPresetModal(parseInt(btn.dataset.editPreset));
            });
        });
        presetListEl.querySelectorAll('[data-delete-preset]').forEach(btn => {
            btn.addEventListener('click', e => {
                e.preventDefault();
                deletePreset(parseInt(btn.dataset.deletePreset), btn.dataset.presetName);
            });
        });
    }

    function renderPresetRow(p) {
        const name = escapeHtml(p.name);
        const desc = p.description ? escapeHtml(p.description.substring(0, 80)) : '';
        const featBadge = p.is_featured
            ? '<span class="config-preset-row__badge config-preset-row__badge--featured"><i class="fas fa-star"></i> Featured</span>'
            : '';

        return `
            <div class="config-preset-row" data-preset-id="${p.id}">
                <div class="config-preset-row__icon"><i class="fas fa-magic"></i></div>
                <div class="config-preset-row__info">
                    <span class="config-preset-row__name">${name}</span>
                    ${desc ? `<span class="config-preset-row__desc">${desc}</span>` : ''}
                </div>
                <div class="config-preset-row__badges">
                    ${featBadge}
                </div>
                <div class="config-preset-row__options-count">
                    <span class="config-preset-row__count-pill">${p.selection_count}</span>
                    <span>selections</span>
                </div>
                <div class="config-preset-row__actions">
                    <button type="button" class="config-preset-row__action" data-edit-preset="${p.id}" title="Edit Preset">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button type="button" class="config-preset-row__action config-preset-row__action--danger" data-delete-preset="${p.id}" data-preset-name="${escapeHtml(p.name)}" title="Delete Preset">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
    }

    async function openPresetModal(presetId) {
        currentPresetId = presetId || null;

        if (presetId) {
            try {
                const data = await fetchJSON(`${BASE}/preset/${presetId}/detail/`);
                renderPresetModalContent(data.preset, data.slots || []);
                presetModalTitle.textContent = 'Edit Preset';
            } catch (err) {
                showNotification('Failed to load preset: ' + err.message, 'error');
                return;
            }
        } else {
            // For create, we need slots info with options — fetch from list endpoint
            try {
                const slotData = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/slots/list/?include_options=1`);
                renderPresetModalContent(null, slotData.slots || []);
                presetModalTitle.textContent = 'Add Preset';
            } catch (err) {
                renderPresetModalContent(null, []);
                presetModalTitle.textContent = 'Add Preset';
            }
        }

        presetOverlay.style.display = 'flex';
        document.addEventListener('keydown', presetEscHandler);
    }

    function closePresetModal() {
        presetOverlay.style.display = 'none';
        currentPresetId = null;
        document.removeEventListener('keydown', presetEscHandler);
    }

    function presetEscHandler(e) {
        if (e.key === 'Escape') closePresetModal();
    }

    function renderPresetModalContent(data, slots) {
        const d = data || {};
        const selections = d.selections || {};

        // Build slot selection UI
        let slotsHtml = '';
        if (slots && slots.length) {
            slotsHtml = `
                <div class="config-modal-section">
                    <h4><i class="fas fa-check-square"></i> Selections</h4>
                    <p class="config-modal-help">Choose which options are pre-selected in this preset for each slot.</p>
                    ${slots.map(slot => {
                        const slotSelections = selections[String(slot.id)] || [];
                        const options = slot.options || [];
                        if (!options.length) {
                            return `<div class="config-preset-slot-group">
                                <label class="config-preset-slot-label"><i class="${escapeHtml(slot.icon)}"></i> ${escapeHtml(slot.name)}</label>
                                <span class="config-modal-help">No options available</span>
                            </div>`;
                        }
                        return `<div class="config-preset-slot-group">
                            <label class="config-preset-slot-label"><i class="${escapeHtml(slot.icon)}"></i> ${escapeHtml(slot.name)}</label>
                            <div class="config-preset-options" data-slot-id="${slot.id}" data-max="${slot.max_selections}">
                                ${options.map(opt => {
                                    const checked = slotSelections.includes(opt.id) ? 'checked' : '';
                                    const label = opt.variant_name ? `${escapeHtml(opt.name)} - ${escapeHtml(opt.variant_name)}` : escapeHtml(opt.name);
                                    if (slot.max_selections === 1) {
                                        return `<label class="config-preset-option">
                                            <input type="radio" name="preset-slot-${slot.id}" value="${opt.id}" ${checked}>
                                            ${label}
                                        </label>`;
                                    }
                                    return `<label class="config-preset-option">
                                        <input type="checkbox" name="preset-slot-${slot.id}" value="${opt.id}" ${checked}>
                                        ${label}
                                    </label>`;
                                }).join('')}
                            </div>
                        </div>`;
                    }).join('')}
                </div>
            `;
        }

        presetModalBody.innerHTML = `
            <div class="config-modal-section">
                <h4><i class="fas fa-info-circle"></i> Basic Info</h4>
                <div class="config-modal-field">
                    <label for="preset-name">Name <span class="required">*</span></label>
                    <input type="text" id="preset-name" value="${escapeHtml(d.name || '')}" placeholder="e.g. Budget Build, Pro Package" autocomplete="off">
                </div>
                <div class="config-modal-field">
                    <label for="preset-slug">Slug</label>
                    <input type="text" id="preset-slug" value="${escapeHtml(d.slug || '')}" placeholder="Auto-generated from name">
                </div>
                <div class="config-modal-field">
                    <label for="preset-description">Description</label>
                    <textarea id="preset-description" rows="2" placeholder="Short description for customers">${escapeHtml(d.description || '')}</textarea>
                </div>
                <div class="config-modal-row">
                    <div class="config-modal-field config-modal-field--checkbox">
                        <label>
                            <input type="checkbox" id="preset-featured" ${d.is_featured ? 'checked' : ''}>
                            Featured Preset
                        </label>
                        <span class="config-modal-help">Highlighted to customers as recommended</span>
                    </div>
                    <div class="config-modal-field">
                        <label for="preset-order">Sort Order</label>
                        <input type="number" id="preset-order" value="${d.sort_order || 0}" min="0">
                    </div>
                </div>
            </div>
            ${slotsHtml}
        `;

        // Auto-generate slug
        const nameInput = document.getElementById('preset-name');
        const slugInput = document.getElementById('preset-slug');
        if (nameInput && slugInput && !currentPresetId) {
            nameInput.addEventListener('input', () => {
                slugInput.value = nameInput.value.toLowerCase()
                    .replace(/[^\w\s-]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-');
            });
        }
    }

    function collectPresetData() {
        // Collect selections from radio/checkbox groups
        const selections = {};
        document.querySelectorAll('.config-preset-options').forEach(group => {
            const slotId = group.dataset.slotId;
            const checked = group.querySelectorAll('input:checked');
            if (checked.length) {
                selections[slotId] = Array.from(checked).map(c => parseInt(c.value));
            }
        });

        return {
            name: document.getElementById('preset-name')?.value?.trim() || '',
            slug: document.getElementById('preset-slug')?.value?.trim() || '',
            description: document.getElementById('preset-description')?.value?.trim() || '',
            is_featured: document.getElementById('preset-featured')?.checked ?? false,
            sort_order: parseInt(document.getElementById('preset-order')?.value || '0'),
            selections: selections,
        };
    }

    async function savePreset() {
        const data = collectPresetData();
        if (!data.name) {
            showNotification('Name is required.', 'error');
            return;
        }

        try {
            if (currentPresetId) {
                await postJSON(`${BASE}/preset/${currentPresetId}/update/`, data);
                showNotification('Preset updated.', 'success');
            } else {
                await postJSON(`${BASE}/product/${PRODUCT_ID}/presets/create/`, data);
                showNotification('Preset created.', 'success');
            }
            closePresetModal();
            await loadPresets();
        } catch (err) {
            showNotification('Error: ' + err.message, 'error');
        }
    }

    async function deletePreset(presetId, presetName) {
        if (!await AdminModal.confirm({ message: `Delete preset "${presetName || 'this preset'}"?`, danger: true, confirmText: 'Delete' })) {
            return;
        }
        try {
            await postJSON(`${BASE}/preset/${presetId}/delete/`, {});
            showNotification('Preset deleted.', 'success');
            await loadPresets();
        } catch (err) {
            showNotification('Error: ' + err.message, 'error');
        }
    }

    // ===================================================================
    // INITIALIZATION
    // ===================================================================

    function init() {
        // Check if the configuration tab exists
        const configPanel = document.getElementById('panel-configuration');
        if (!configPanel) return;

        // Only run for configurable products — avoid AJAX errors on other product types
        const productTypeField = document.getElementById('id_product_type');
        if (!productTypeField || productTypeField.value !== 'configurable') return;

        // Slot DOM refs
        slotListEl = document.getElementById('config-slot-list');
        slotCountBadge = document.getElementById('config-slot-count');
        addSlotBtn = document.getElementById('add-slot-btn');
        slotOverlay = document.getElementById('config-slot-modal-overlay');
        slotModal = slotOverlay?.querySelector('.config-slot-modal');
        slotModalTitle = document.getElementById('config-slot-modal-title');
        slotModalBody = document.getElementById('config-slot-modal-body');
        slotSaveBtn = document.getElementById('config-slot-modal-save');

        // Preset DOM refs
        presetListEl = document.getElementById('config-preset-list');
        presetCountBadge = document.getElementById('config-preset-count');
        addPresetBtn = document.getElementById('add-preset-btn');
        presetOverlay = document.getElementById('config-preset-modal-overlay');
        presetModal = presetOverlay?.querySelector('.config-preset-modal');
        presetModalTitle = document.getElementById('config-preset-modal-title');
        presetModalBody = document.getElementById('config-preset-modal-body');
        presetSaveBtn = document.getElementById('config-preset-modal-save');

        // Bind slot events
        if (addSlotBtn) addSlotBtn.addEventListener('click', () => openSlotModal(null));
        if (slotSaveBtn) slotSaveBtn.addEventListener('click', saveSlot);
        if (slotOverlay) {
            slotOverlay.querySelector('.config-slot-modal-close')?.addEventListener('click', closeSlotModal);
            document.getElementById('config-slot-modal-cancel')?.addEventListener('click', closeSlotModal);
            slotOverlay.addEventListener('click', e => { if (e.target === slotOverlay) closeSlotModal(); });
        }

        // Bind preset events
        if (addPresetBtn) addPresetBtn.addEventListener('click', () => openPresetModal(null));
        if (presetSaveBtn) presetSaveBtn.addEventListener('click', savePreset);
        if (presetOverlay) {
            presetOverlay.querySelector('.config-preset-modal-close')?.addEventListener('click', closePresetModal);
            document.getElementById('config-preset-modal-cancel')?.addEventListener('click', closePresetModal);
            presetOverlay.addEventListener('click', e => { if (e.target === presetOverlay) closePresetModal(); });
        }

        // Load data
        if (slotListEl) loadSlots();
        if (presetListEl) loadPresets();
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
