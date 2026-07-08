/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * 3D Scene Setup Admin JavaScript
 *
 * Handles the admin scene manager: model loading, node tree rendering,
 * viewer settings, geometry asset management, texture asset management,
 * visual mapping CRUD, and live preview of material/geometry/visibility changes.
 */
(function () {
    'use strict';

    var _configEl = document.getElementById('scene-setup-data');
    if (!_configEl) return;
    var D;
    try { D = JSON.parse(_configEl.textContent); } catch(e) { console.error('scene_setup: failed to parse config', e); return; }
    if (!D) return;

    var S = D.strings || {};
    var viewer = document.getElementById('model-viewer');
    var overlay = document.getElementById('viewer-overlay');

    // State
    var nodeTree = D.scene.node_tree || {};
    var mappings = D.mappings || [];
    var geometryAssets = D.geometry || [];
    var textureAssets = D.textures || [];
    var editingMappingId = null;

    // --- Helpers ---

    function escHtml(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.textContent = String(str);
        return div.innerHTML;
    }

    function ajax(url, method, body) {
        var opts = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': D.csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            },
        };
        if (body) opts.body = JSON.stringify(body);
        return fetch(url, opts).then(function(r) { return r.json(); });
    }

    /**
     * Build a delete URL from a template URL that contains /0/delete/
     * by replacing the placeholder 0 with the actual ID.
     */
    function buildDeleteUrl(template, id) {
        return template.replace('/0/delete/', '/' + id + '/delete/');
    }

    // --- Notifications ---

    function showNotification(msg, type) {
        AdminModal.toast(msg, type || 'info');
    }

    // --- Modal Helpers ---

    function openModal(modalEl) {
        modalEl.classList.add('scene-setup-modal--open');
        modalEl._previousFocus = document.activeElement;

        // Focus first focusable element
        var focusable = modalEl.querySelector('input, select, button, textarea');
        if (focusable) focusable.focus();

        // Bind Escape key
        modalEl._escHandler = function(e) {
            if (e.key === 'Escape') closeModal(modalEl);
        };
        document.addEventListener('keydown', modalEl._escHandler);

        // Focus trap
        modalEl._trapHandler = function(e) {
            if (e.key !== 'Tab') return;
            var focusables = modalEl.querySelectorAll(
                'input:not([type="hidden"]), select, button, textarea, [tabindex]:not([tabindex="-1"])'
            );
            if (focusables.length === 0) return;
            var first = focusables[0];
            var last = focusables[focusables.length - 1];
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        };
        modalEl.addEventListener('keydown', modalEl._trapHandler);
    }

    function closeModal(modalEl) {
        modalEl.classList.remove('scene-setup-modal--open');
        if (modalEl._escHandler) {
            document.removeEventListener('keydown', modalEl._escHandler);
            modalEl._escHandler = null;
        }
        if (modalEl._trapHandler) {
            modalEl.removeEventListener('keydown', modalEl._trapHandler);
            modalEl._trapHandler = null;
        }
        if (modalEl._previousFocus) {
            modalEl._previousFocus.focus();
            modalEl._previousFocus = null;
        }
    }

    // --- Model Viewer ---

    /**
     * Apply a viewer property using the JS property API (more reliable
     * than setAttribute when effect-composer is active).
     * Falls back to setAttribute for browsers / versions without the property.
     */
    function setViewerProp(prop, attr, value) {
        if (prop in viewer) {
            viewer[prop] = value;
        } else {
            viewer.setAttribute(attr, value);
        }
    }

    function initViewer() {
        if (D.scene.base_model_url) {
            viewer.setAttribute('src', D.scene.base_model_url);
            viewer.setAttribute('camera-orbit', D.scene.camera_orbit);
            viewer.setAttribute('camera-target', D.scene.camera_target);

            // Use JS properties for rendering attributes (more reliable with effect-composer)
            setViewerProp('exposure', 'exposure', parseFloat(D.scene.exposure));
            setViewerProp('shadowIntensity', 'shadow-intensity', parseFloat(D.scene.shadow_intensity));
            setViewerProp('shadowSoftness', 'shadow-softness', parseFloat(D.scene.shadow_softness));
            setViewerProp('toneMapping', 'tone-mapping', D.scene.tone_mapping);
            viewer.style.setProperty('--viewer-bg', D.scene.background_color);

            if (D.scene.auto_rotate) viewer.setAttribute('auto-rotate', '');
            else viewer.removeAttribute('auto-rotate');

            if (D.scene.ar_enabled) viewer.setAttribute('ar', '');
            else viewer.removeAttribute('ar');

            // Use uploaded HDR, or fall back to 'legacy' for better metallic reflections
            viewer.setAttribute('environment-image', D.scene.environment_url || 'legacy');

            overlay.classList.add('hidden');

            // Apply emissive properties and bloom after model loads
            viewer.addEventListener('load', function () {
                applyEmissiveDefaults();
                var bloomStrength = parseFloat(D.scene.bloom_strength) || 0;
                if (bloomStrength > 0) {
                    setBloomEnabled(bloomStrength);
                }
            });
        }

        // Apply initial background from data attribute
        var dataBg = viewer.getAttribute('data-bg');
        if (dataBg) {
            viewer.style.setProperty('--viewer-bg', dataBg);
        }
    }

    /**
     * Apply emissive color/strength stored in node_tree materials via
     * model-viewer's scene graph API.
     *
     * For materials with emissive color but no explicit strength, auto-boosts
     * to DEFAULT_EMISSIVE_BOOST when bloom is enabled so pixels exceed
     * threshold=1.0 and produce a visible glow.
     */
    var DEFAULT_EMISSIVE_BOOST = 10.0;

    function applyEmissiveDefaults() {
        if (!viewer.model) return;
        var materials = viewer.model.materials;
        var treeMats = (nodeTree.materials || {});
        var bloomStrength = parseFloat(D.scene.bloom_strength) || 0;

        for (var i = 0; i < materials.length; i++) {
            var mat = materials[i];
            var treeData = treeMats[mat.name];
            if (!treeData) continue;

            var ec = treeData.emissive_color;
            if (ec && (ec[0] > 0 || ec[1] > 0 || ec[2] > 0)) {
                mat.setEmissiveFactor([ec[0], ec[1], ec[2]]);

                // Use GLB's KHR_materials_emissive_strength if present,
                // otherwise auto-boost when bloom is enabled
                var strength = treeData.emissive_strength || 0;
                if (strength > 0) {
                    mat.setEmissiveStrength(strength);
                } else if (bloomStrength > 0) {
                    mat.setEmissiveStrength(DEFAULT_EMISSIVE_BOOST);
                }
            }
        }
    }

    /**
     * Dynamically inject or remove <effect-composer> with <bloom-effect>.
     * Uses the "high threshold" method: threshold >= 1.0 so only HDR-bright
     * pixels (emissive materials with intensity > 1) will bloom.
     * Only active when bloom strength > 0 to avoid interfering with normal rendering.
     */
    function setBloomEnabled(strength) {
        var existing = viewer.querySelector('effect-composer');
        if (strength > 0) {
            if (!existing) {
                var composer = document.createElement('effect-composer');
                // quality mode uses HalfFloatType for HDR — needed so emissive
                // pixels above 1.0 aren't clamped before the bloom pass
                composer.setAttribute('render-mode', 'quality');
                var bloom = document.createElement('bloom-effect');
                bloom.id = 'admin-bloom-effect';
                bloom.setAttribute('strength', strength);
                bloom.setAttribute('radius', '0.85');
                bloom.setAttribute('threshold', '3.0');
                bloom.setAttribute('smoothing', '0.5');
                composer.appendChild(bloom);
                viewer.appendChild(composer);
            } else {
                var bloomEl = existing.querySelector('bloom-effect');
                if (bloomEl) bloomEl.setAttribute('strength', strength);
            }
        } else if (existing) {
            existing.remove();
        }
    }

    // --- Node Tree ---

    function renderNodeTree() {
        var container = document.getElementById('node-tree-container');
        var countEl = document.getElementById('node-count');

        if (!nodeTree.nodes || Object.keys(nodeTree.nodes).length === 0) {
            container.innerHTML = '<p class="scene-setup-tree__empty">' + escHtml(S.parseGlbEmpty) + '</p>';
            countEl.textContent = '0';
            return;
        }

        var nodeCount = Object.keys(nodeTree.nodes).length;
        countEl.textContent = nodeCount;

        var html = '';
        var roots = nodeTree.root_nodes || [];

        function renderNode(name, depth) {
            var node = nodeTree.nodes[name];
            if (!node) return;
            var icon = node.mesh ? 'fa-cube' : 'fa-folder';
            var mats = node.materials && node.materials.length
                ? ' <span class="scene-setup-tree__materials">[' + escHtml(node.materials.join(', ')) + ']</span>'
                : '';
            html += '<div class="scene-setup-tree__node" data-node="' + escHtml(name) + '" style="--node-depth:' + depth + '" role="treeitem" tabindex="0">'
                + '<i class="fas ' + icon + ' scene-setup-tree__icon"></i>'
                + '<span>' + escHtml(name) + '</span>' + mats
                + '</div>';
            if (node.children) {
                node.children.forEach(function(c) { renderNode(c, depth + 1); });
            }
        }

        roots.forEach(function(r) { renderNode(r, 0); });

        // Also render any nodes not in the tree (orphans)
        var rendered = new Set();
        function collectRendered(name) {
            rendered.add(name);
            var node = nodeTree.nodes[name];
            if (node && node.children) node.children.forEach(function(c) { collectRendered(c); });
        }
        roots.forEach(function(r) { collectRendered(r); });

        Object.keys(nodeTree.nodes).forEach(function(name) {
            if (!rendered.has(name)) renderNode(name, 0);
        });

        container.innerHTML = html;

        // Click to highlight
        container.querySelectorAll('.scene-setup-tree__node').forEach(function(el) {
            el.addEventListener('click', function() {
                container.querySelectorAll('.scene-setup-tree__node--active').forEach(function(a) {
                    a.classList.remove('scene-setup-tree__node--active');
                });
                el.classList.add('scene-setup-tree__node--active');
            });
        });
    }

    // --- Populate Node/Material Dropdowns ---

    function populateNodeDropdown(selectEl) {
        selectEl.innerHTML = '<option value="">' + escHtml(S.selectNode) + '</option>';
        if (nodeTree.nodes) {
            Object.keys(nodeTree.nodes).forEach(function(name) {
                var opt = document.createElement('option');
                opt.value = name;
                opt.textContent = name;
                selectEl.appendChild(opt);
            });
        }
    }

    function populateMaterialDropdown(selectEl) {
        selectEl.innerHTML = '<option value="">' + escHtml(S.selectMaterial) + '</option>';
        if (nodeTree.materials) {
            Object.keys(nodeTree.materials).forEach(function(name) {
                var opt = document.createElement('option');
                opt.value = name;
                opt.textContent = name;
                selectEl.appendChild(opt);
            });
        }
    }

    function populateSlotOptionDropdown(selectEl) {
        selectEl.innerHTML = '';
        D.slots.forEach(function(slot) {
            var group = document.createElement('optgroup');
            group.label = slot.name;
            slot.options.forEach(function(opt) {
                var el = document.createElement('option');
                el.value = opt.id;
                el.textContent = opt.product_name + (opt.variant_name ? ' (' + opt.variant_name + ')' : '');
                group.appendChild(el);
            });
            selectEl.appendChild(group);
        });
    }

    function populateGeometryDropdown(selectEl) {
        selectEl.innerHTML = '<option value="">' + escHtml(S.selectGeometry) + '</option>';
        geometryAssets.forEach(function(ga) {
            var opt = document.createElement('option');
            opt.value = ga.media_url;
            opt.textContent = ga.label;
            opt.dataset.assetId = ga.media_asset_id;
            selectEl.appendChild(opt);
        });
    }

    // --- Mappings Rendering ---

    function renderMappings() {
        var container = document.getElementById('mappings-by-slot');
        var countEl = document.getElementById('mapping-count');
        countEl.textContent = mappings.length;

        if (mappings.length === 0) {
            container.innerHTML = '<p class="scene-setup-mappings__empty">' + escHtml(S.noMappings) + '</p>';
            return;
        }

        // Group by slot
        var bySlot = {};
        mappings.forEach(function(m) {
            var key = m.slot_name || 'Unknown';
            if (!bySlot[key]) bySlot[key] = [];
            bySlot[key].push(m);
        });

        var html = '';
        Object.keys(bySlot).forEach(function(slotName) {
            html += '<div class="scene-setup-slot-group">'
                + '<div class="scene-setup-slot-group__title">' + escHtml(slotName) + '</div>';
            bySlot[slotName].forEach(function(m) {
                var badgeClass = {
                    material_color: 'color',
                    material_texture: 'texture',
                    geometry_swap: 'geometry',
                    visibility: 'visibility',
                }[m.action_type] || 'color';

                var detail = '&rarr; ' + escHtml(m.target_node);
                var colorSwatch = '';
                if (m.action_type === 'material_color' && m.action_data.color) {
                    colorSwatch = '<span class="scene-setup-color-swatch" style="--swatch-color:' + escHtml(m.action_data.color) + '"></span>';
                }

                html += '<div class="scene-setup-item" data-mapping-id="' + m.id + '">'
                    + colorSwatch
                    + '<div class="scene-setup-item__info">'
                    + '<span class="scene-setup-item__label">' + escHtml(m.option_name) + '</span>'
                    + '<span class="scene-setup-item__detail">'
                    + '<span class="scene-setup-badge scene-setup-badge--' + badgeClass + '">' + escHtml(m.action_type.replace(/_/g, ' ')) + '</span>'
                    + detail
                    + '</span>'
                    + '</div>'
                    + '<div class="scene-setup-item__actions">'
                    + '<button class="scene-setup-item__btn btn-edit-mapping" data-id="' + m.id + '" title="Edit"><i class="fas fa-edit"></i></button>'
                    + '<button class="scene-setup-item__btn scene-setup-item__btn--danger btn-delete-mapping" data-id="' + m.id + '" title="Delete"><i class="fas fa-trash"></i></button>'
                    + '</div>'
                    + '</div>';
            });
            html += '</div>';
        });

        container.innerHTML = html;

        // Bind edit/delete
        container.querySelectorAll('.btn-edit-mapping').forEach(function(btn) {
            btn.addEventListener('click', function() { openMappingModal(parseInt(btn.dataset.id)); });
        });
        container.querySelectorAll('.btn-delete-mapping').forEach(function(btn) {
            btn.addEventListener('click', function() { confirmDelete(btn, function() { deleteMapping(parseInt(btn.dataset.id)); }); });
        });
    }

    // --- Geometry Assets Rendering ---

    function renderGeometryAssets() {
        var container = document.getElementById('geometry-list');
        var countEl = document.getElementById('geometry-count');
        countEl.textContent = geometryAssets.length;

        if (geometryAssets.length === 0) {
            container.innerHTML = '';
            return;
        }

        var html = '';
        geometryAssets.forEach(function(ga) {
            html += '<div class="scene-setup-item" data-geometry-id="' + ga.id + '">'
                + '<div class="scene-setup-item__info">'
                + '<span class="scene-setup-item__label">' + escHtml(ga.label) + '</span>'
                + '<span class="scene-setup-item__detail">' + escHtml(ga.target_node || S.noTarget) + ' &mdash; ' + escHtml(ga.media_asset_title) + '</span>'
                + '</div>'
                + '<div class="scene-setup-item__actions">'
                + '<button class="scene-setup-item__btn scene-setup-item__btn--danger btn-delete-geometry" data-id="' + ga.id + '" title="Delete"><i class="fas fa-trash"></i></button>'
                + '</div>'
                + '</div>';
        });

        container.innerHTML = html;

        container.querySelectorAll('.btn-delete-geometry').forEach(function(btn) {
            btn.addEventListener('click', function() { confirmDelete(btn, function() { deleteGeometryAsset(parseInt(btn.dataset.id)); }); });
        });
    }

    // --- Texture Assets Rendering ---

    function renderTextureAssets() {
        var container = document.getElementById('texture-list');
        var countEl = document.getElementById('texture-count');
        countEl.textContent = textureAssets.length;

        if (textureAssets.length === 0) {
            container.innerHTML = '';
            return;
        }

        var html = '';
        textureAssets.forEach(function(ta) {
            html += '<div class="scene-setup-item" data-texture-id="' + ta.id + '">'
                + '<div class="scene-setup-item__info">'
                + '<span class="scene-setup-item__label">' + escHtml(ta.label) + '</span>'
                + '<span class="scene-setup-item__detail">'
                + '<span class="scene-setup-badge scene-setup-badge--texture">' + escHtml(ta.texture_type_display || ta.texture_type) + '</span>'
                + escHtml(ta.media_asset_title)
                + '</span>'
                + '</div>'
                + '<div class="scene-setup-item__actions">'
                + '<button class="scene-setup-item__btn scene-setup-item__btn--danger btn-delete-texture" data-id="' + ta.id + '" title="Delete"><i class="fas fa-trash"></i></button>'
                + '</div>'
                + '</div>';
        });

        container.innerHTML = html;

        container.querySelectorAll('.btn-delete-texture').forEach(function(btn) {
            btn.addEventListener('click', function() { confirmDelete(btn, function() { deleteTextureAsset(parseInt(btn.dataset.id)); }); });
        });
    }

    // --- Inline Confirmation (replaces confirm()) ---

    function confirmDelete(btn, callback) {
        if (btn.classList.contains('scene-setup-item__btn--confirming')) {
            // Already confirming — execute
            callback();
            return;
        }

        btn.classList.add('scene-setup-item__btn--confirming');
        btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        btn.title = S.confirmDelete;

        var timeout = setTimeout(function() {
            btn.classList.remove('scene-setup-item__btn--confirming');
            btn.innerHTML = '<i class="fas fa-trash"></i>';
            btn.title = 'Delete';
        }, 3000);

        btn._confirmTimeout = timeout;
    }

    // --- Mapping Modal ---

    function openMappingModal(mappingId) {
        var modal = document.getElementById('mapping-modal');
        var title = document.getElementById('mapping-modal-title');

        editingMappingId = mappingId || null;

        // Populate dropdowns
        populateSlotOptionDropdown(document.getElementById('mapping-slot-option'));
        populateNodeDropdown(document.getElementById('mapping-target-node'));
        populateMaterialDropdown(document.getElementById('action-material-name'));
        populateMaterialDropdown(document.getElementById('action-texture-material'));
        populateGeometryDropdown(document.getElementById('action-geometry-asset'));

        if (editingMappingId) {
            title.textContent = S.editMapping;
            var m = mappings.find(function(x) { return x.id === editingMappingId; });
            if (m) {
                document.getElementById('mapping-slot-option').value = m.slot_option_id;
                document.getElementById('mapping-action-type').value = m.action_type;
                document.getElementById('mapping-target-node').value = m.target_node;
                showActionFields(m.action_type);
                populateActionFields(m.action_type, m.action_data);
            }
        } else {
            title.textContent = S.addMapping;
            document.getElementById('mapping-action-type').value = 'material_color';
            showActionFields('material_color');
        }

        openModal(modal);
    }

    function closeMappingModal() {
        closeModal(document.getElementById('mapping-modal'));
        editingMappingId = null;
    }

    function showActionFields(actionType) {
        document.querySelectorAll('.scene-setup-action-fields').forEach(function(el) {
            el.classList.remove('scene-setup-action-fields--active');
        });
        var map = {
            material_color: 'action-fields-color',
            material_texture: 'action-fields-texture',
            geometry_swap: 'action-fields-geometry',
            visibility: 'action-fields-visibility',
        };
        var id = map[actionType];
        if (id) document.getElementById(id).classList.add('scene-setup-action-fields--active');
    }

    function populateActionFields(actionType, data) {
        if (actionType === 'material_color') {
            document.getElementById('action-material-name').value = data.material_name || '';
            document.getElementById('action-color').value = data.color || '#ffffff';
            document.getElementById('action-metalness').value = data.metalness ?? 0;
            document.getElementById('metalness-value').textContent = data.metalness ?? 0;
            document.getElementById('action-roughness').value = data.roughness ?? 0.8;
            document.getElementById('roughness-value').textContent = data.roughness ?? 0.8;
            document.getElementById('action-emissive-color').value = data.emissive || '#000000';
            document.getElementById('action-emissive-strength').value = data.emissive_strength ?? 0;
            document.getElementById('emissive-strength-value').textContent = data.emissive_strength ?? 0;
        } else if (actionType === 'material_texture') {
            document.getElementById('action-texture-material').value = data.material_name || '';
            document.getElementById('action-base-texture-url').value = data.base_color_url || '';
            document.getElementById('base-texture-name').textContent = data.base_color_url ? S.selectedLabel : S.noneLabel;
            document.getElementById('action-normal-texture-url').value = data.normal_url || '';
            document.getElementById('normal-texture-name').textContent = data.normal_url ? S.selectedLabel : S.noneLabel;
        } else if (actionType === 'geometry_swap') {
            document.getElementById('action-geometry-asset').value = data.glb_url || '';
        } else if (actionType === 'visibility') {
            document.getElementById('action-visible').checked = data.visible !== false;
        }
    }

    function collectActionData(actionType) {
        if (actionType === 'material_color') {
            var result = {
                material_name: document.getElementById('action-material-name').value,
                color: document.getElementById('action-color').value,
                metalness: parseFloat(document.getElementById('action-metalness').value),
                roughness: parseFloat(document.getElementById('action-roughness').value),
            };
            var emissiveColor = document.getElementById('action-emissive-color').value;
            if (emissiveColor !== '#000000') {
                result.emissive = emissiveColor;
                result.emissive_strength = parseFloat(document.getElementById('action-emissive-strength').value);
            }
            return result;
        } else if (actionType === 'material_texture') {
            return {
                material_name: document.getElementById('action-texture-material').value,
                base_color_url: document.getElementById('action-base-texture-url').value,
                normal_url: document.getElementById('action-normal-texture-url').value,
            };
        } else if (actionType === 'geometry_swap') {
            var sel = document.getElementById('action-geometry-asset');
            return {
                glb_url: sel.value,
                glb_asset_id: sel.selectedOptions[0] ? sel.selectedOptions[0].dataset.assetId || '' : '',
            };
        } else if (actionType === 'visibility') {
            return {
                visible: document.getElementById('action-visible').checked,
            };
        }
        return {};
    }

    async function saveMapping() {
        var slotOptionId = parseInt(document.getElementById('mapping-slot-option').value);
        var actionType = document.getElementById('mapping-action-type').value;
        var targetNode = document.getElementById('mapping-target-node').value;
        var actionData = collectActionData(actionType);

        if (!slotOptionId || !actionType || !targetNode) {
            showNotification(S.fillRequired, 'error');
            return;
        }

        var body = {
            slot_option_id: slotOptionId,
            action_type: actionType,
            target_node: targetNode,
            action_data: actionData,
        };
        if (editingMappingId) body.id = editingMappingId;

        var result = await ajax(D.urls.saveMappings, 'POST', body);
        if (result.success) {
            closeMappingModal();
            var data = await ajax(D.urls.listMappings, 'GET');
            mappings = data.mappings || [];
            renderMappings();
            showNotification(S.mappingSaved, 'success');
        } else {
            showNotification(result.error || S.errorSaving, 'error');
        }
    }

    async function deleteMapping(id) {
        var url = buildDeleteUrl(D.urls.deleteMapping, id);
        var result = await ajax(url, 'POST');
        if (result.success) {
            mappings = mappings.filter(function(m) { return m.id !== id; });
            renderMappings();
            showNotification(S.mappingDeleted, 'success');
        }
    }

    // --- Geometry Asset Modal + CRUD ---

    function openGeometryModal() {
        var modal = document.getElementById('geometry-modal');
        document.getElementById('geometry-modal-title').textContent = S.addGeometry;
        document.getElementById('geometry-label').value = '';
        document.getElementById('geometry-target-node').value = '';
        document.getElementById('geometry-file-name').textContent = S.noneLabel;
        document.getElementById('geometry-media-asset-id').value = '';
        openModal(modal);
    }

    function closeGeometryModal() {
        closeModal(document.getElementById('geometry-modal'));
    }

    async function saveGeometryFromModal() {
        var label = document.getElementById('geometry-label').value.trim();
        var targetNode = document.getElementById('geometry-target-node').value.trim();
        var mediaAssetId = document.getElementById('geometry-media-asset-id').value;

        if (!label) {
            showNotification(S.labelRequired, 'error');
            return;
        }
        if (!mediaAssetId) {
            showNotification(S.selectFile, 'error');
            return;
        }

        var result = await ajax(D.urls.saveGeometry, 'POST', {
            label: label,
            media_asset_id: mediaAssetId,
            target_node: targetNode,
        });
        if (result.success) {
            geometryAssets.push(result.geometry_asset);
            renderGeometryAssets();
            closeGeometryModal();
            showNotification(S.geometrySaved, 'success');
        }
    }

    async function deleteGeometryAsset(id) {
        var url = buildDeleteUrl(D.urls.deleteGeometry, id);
        var result = await ajax(url, 'POST');
        if (result.success) {
            geometryAssets = geometryAssets.filter(function(ga) { return ga.id !== id; });
            renderGeometryAssets();
            showNotification(S.geometryDeleted, 'success');
        }
    }

    // --- Texture Asset Modal + CRUD ---

    function openTextureModal() {
        var modal = document.getElementById('texture-modal');
        document.getElementById('texture-modal-title').textContent = S.addTexture;
        document.getElementById('texture-label').value = '';
        document.getElementById('texture-type').value = 'base_color';
        document.getElementById('texture-file-name').textContent = S.noneLabel;
        document.getElementById('texture-media-asset-id').value = '';
        openModal(modal);
    }

    function closeTextureModal() {
        closeModal(document.getElementById('texture-modal'));
    }

    async function saveTextureFromModal() {
        var label = document.getElementById('texture-label').value.trim();
        var textureType = document.getElementById('texture-type').value;
        var mediaAssetId = document.getElementById('texture-media-asset-id').value;

        if (!label) {
            showNotification(S.labelRequired, 'error');
            return;
        }
        if (!mediaAssetId) {
            showNotification(S.selectFile, 'error');
            return;
        }

        var result = await ajax(D.urls.saveTexture, 'POST', {
            label: label,
            media_asset_id: mediaAssetId,
            texture_type: textureType,
        });
        if (result.success) {
            textureAssets.push(result.texture_asset);
            renderTextureAssets();
            closeTextureModal();
            showNotification(S.textureSaved, 'success');
        }
    }

    async function deleteTextureAsset(id) {
        var url = buildDeleteUrl(D.urls.deleteTexture, id);
        var result = await ajax(url, 'POST');
        if (result.success) {
            textureAssets = textureAssets.filter(function(ta) { return ta.id !== id; });
            renderTextureAssets();
            showNotification(S.textureDeleted, 'success');
        }
    }

    // --- Media Library Picker (Modal) ---

    function openMediaPicker(callback, options) {
        var opts = options || {};
        var pickerFn = window.selectMediaFromLibrary;
        if (opts.fileType === 'image') {
            pickerFn = window.selectImageFromLibrary || pickerFn;
        }

        if (!pickerFn) {
            console.error('MediaLibrary not loaded');
            return;
        }

        pickerFn(function(asset) {
            if (!asset) return;
            // Normalize: callers may use asset.original_file_url
            asset.original_file_url = asset.original_url || asset.url || '';
            callback(asset);
        });
    }

    // --- Viewer Settings ---

    // --- Background Picker State ---
    var bgMode = 'solid'; // 'solid' or 'gradient'
    var gradientCreator = null;

    function isGradientValue(val) {
        return val && (val.indexOf('gradient') !== -1);
    }

    function getBackgroundValue() {
        if (bgMode === 'gradient') {
            return document.getElementById('setting-bg-gradient').value || '#ffffff';
        }
        return document.getElementById('setting-bg-color').value || '#ffffff';
    }

    function setViewerBackground(val) {
        viewer.style.setProperty('--viewer-bg', val);
    }

    function initBackgroundPicker() {
        var bgColor = document.getElementById('setting-bg-color');
        var bgGradientInput = document.getElementById('setting-bg-gradient');
        var preview = document.getElementById('bg-gradient-preview');
        var previewLabel = preview.querySelector('.scene-setup-bg-gradient-preview__label');
        var hexLabel = document.getElementById('bg-hex-value');
        var tabs = document.querySelectorAll('.scene-setup-bg-tab');
        var panels = document.querySelectorAll('.scene-setup-bg-panel');

        // Detect initial value
        var initialBg = D.scene.background_color || '#ffffff';
        if (isGradientValue(initialBg)) {
            bgMode = 'gradient';
            bgGradientInput.value = initialBg;
            preview.style.background = initialBg;
            if (previewLabel) previewLabel.style.display = 'none';
        } else {
            bgMode = 'solid';
            bgColor.value = initialBg;
            hexLabel.textContent = initialBg;
        }

        // Set active tab/panel on init
        tabs.forEach(function(tab) {
            if (tab.dataset.bgMode === bgMode) {
                tab.classList.add('scene-setup-bg-tab--active');
            } else {
                tab.classList.remove('scene-setup-bg-tab--active');
            }
        });
        panels.forEach(function(panel) {
            if (panel.classList.contains('scene-setup-bg-panel--' + bgMode)) {
                panel.classList.add('scene-setup-bg-panel--active');
            } else {
                panel.classList.remove('scene-setup-bg-panel--active');
            }
        });

        // Tab switching
        tabs.forEach(function(tab) {
            tab.addEventListener('click', function() {
                bgMode = tab.dataset.bgMode;
                tabs.forEach(function(t) { t.classList.remove('scene-setup-bg-tab--active'); });
                tab.classList.add('scene-setup-bg-tab--active');
                panels.forEach(function(p) { p.classList.remove('scene-setup-bg-panel--active'); });
                document.querySelector('.scene-setup-bg-panel--' + bgMode).classList.add('scene-setup-bg-panel--active');
                // Live update viewer
                setViewerBackground(getBackgroundValue());
            });
        });

        // Solid color picker
        bgColor.addEventListener('input', function() {
            hexLabel.textContent = bgColor.value;
            setViewerBackground(bgColor.value);
        });

        // Gradient creator button
        var gradBtn = document.getElementById('btn-open-gradient');
        gradBtn.addEventListener('click', function() {
            if (!window.GradientCreator && !window.GradientCreatorUtility) {
                showNotification('Gradient editor not loaded', 'error');
                return;
            }
            var GC = window.GradientCreatorUtility || window.GradientCreator;

            if (!gradientCreator) {
                gradientCreator = new GC({
                    createTrigger: false,
                    onChange: function(css) {
                        bgGradientInput.value = css;
                        preview.style.background = css;
                        if (previewLabel) previewLabel.style.display = 'none';
                        setViewerBackground(css);
                    },
                    onApply: function(css) {
                        bgGradientInput.value = css;
                        preview.style.background = css;
                        if (previewLabel) previewLabel.style.display = 'none';
                        setViewerBackground(css);
                    }
                });
                // Attach to hidden input
                gradientCreator.attach(bgGradientInput, bgGradientInput.value);
            }

            // Parse current value if one exists
            if (bgGradientInput.value && isGradientValue(bgGradientInput.value)) {
                gradientCreator.parseGradient(bgGradientInput.value);
            }
            gradientCreator.open();
        });
    }

    function bindSettingsControls() {
        var exposure = document.getElementById('setting-exposure');
        var shadow = document.getElementById('setting-shadow');
        var bloom = document.getElementById('setting-bloom');
        var autoRotate = document.getElementById('setting-auto-rotate');

        exposure.addEventListener('input', function() {
            document.getElementById('exposure-value').textContent = exposure.value;
            setViewerProp('exposure', 'exposure', parseFloat(exposure.value));
        });

        shadow.addEventListener('input', function() {
            document.getElementById('shadow-value').textContent = shadow.value;
            setViewerProp('shadowIntensity', 'shadow-intensity', parseFloat(shadow.value));
        });

        var shadowSoftness = document.getElementById('setting-shadow-softness');
        shadowSoftness.addEventListener('input', function() {
            document.getElementById('shadow-softness-value').textContent = shadowSoftness.value;
            setViewerProp('shadowSoftness', 'shadow-softness', parseFloat(shadowSoftness.value));
        });

        var toneMapping = document.getElementById('setting-tone-mapping');
        toneMapping.addEventListener('change', function() {
            setViewerProp('toneMapping', 'tone-mapping', toneMapping.value);
        });

        bloom.addEventListener('input', function() {
            document.getElementById('bloom-value').textContent = bloom.value;
            setBloomEnabled(parseFloat(bloom.value));
        });

        autoRotate.addEventListener('change', function() {
            if (autoRotate.checked) viewer.setAttribute('auto-rotate', '');
            else viewer.removeAttribute('auto-rotate');
        });

        // Initialize background solid/gradient picker
        initBackgroundPicker();

        // Range value display for modal
        document.getElementById('action-metalness').addEventListener('input', function () {
            document.getElementById('metalness-value').textContent = this.value;
        });
        document.getElementById('action-roughness').addEventListener('input', function () {
            document.getElementById('roughness-value').textContent = this.value;
        });
        document.getElementById('action-emissive-strength').addEventListener('input', function () {
            document.getElementById('emissive-strength-value').textContent = this.value;
        });
        document.getElementById('btn-clear-emissive').addEventListener('click', function () {
            document.getElementById('action-emissive-color').value = '#000000';
            document.getElementById('action-emissive-strength').value = '0';
            document.getElementById('emissive-strength-value').textContent = '0';
        });
    }

    async function saveSettings() {
        var body = {
            exposure: parseFloat(document.getElementById('setting-exposure').value),
            shadow_intensity: parseFloat(document.getElementById('setting-shadow').value),
            shadow_softness: parseFloat(document.getElementById('setting-shadow-softness').value),
            tone_mapping: document.getElementById('setting-tone-mapping').value,
            bloom_strength: parseFloat(document.getElementById('setting-bloom').value),
            background_color: getBackgroundValue(),
            auto_rotate: document.getElementById('setting-auto-rotate').checked,
            ar_enabled: document.getElementById('setting-ar').checked,
            is_enabled: document.getElementById('scene-enabled').checked,
            camera_orbit: document.getElementById('setting-camera-orbit').value,
            camera_target: document.getElementById('setting-camera-target').value,
        };

        // Environment image
        var envId = document.getElementById('btn-select-environment').dataset.envId || null;
        if (envId !== undefined) {
            body.environment_image_id = envId;
        }

        var result = await ajax(D.urls.saveScene, 'POST', body);
        if (result.success) {
            showNotification(S.settingsSaved, 'success');
        }
    }

    // --- GLB Upload ---

    function selectBaseModel() {
        openMediaPicker(async function (asset) {
            document.getElementById('current-model-name').textContent = asset.title || S.uploading;

            var result = await ajax(D.urls.parseGlb, 'POST', { media_asset_id: asset.id });
            if (result.success) {
                nodeTree = result.node_tree;
                D.scene.base_model_url = asset.url || asset.original_file_url;
                D.scene.node_tree = nodeTree;

                // Update viewer
                viewer.setAttribute('src', D.scene.base_model_url);
                overlay.classList.add('hidden');

                // Update UI
                document.getElementById('current-model-name').textContent = asset.title;
                renderNodeTree();
                showNotification(S.modelLoaded, 'success');
            } else {
                showNotification(result.error || S.errorParsing, 'error');
            }
        });
    }

    // --- Thumbnail Capture ---

    async function captureThumbnail() {
        if (!viewer.src) {
            showNotification(S.loadModelFirst, 'error');
            return;
        }

        try {
            var blob = await viewer.toBlob({ idealAspect: true });
            var reader = new FileReader();
            reader.onloadend = async function () {
                var result = await ajax(D.urls.captureThumbnail, 'POST', {
                    image_data: reader.result,
                });
                if (result.success) {
                    showNotification(S.thumbnailCaptured, 'success');
                } else {
                    showNotification(result.error || S.errorCapturing, 'error');
                }
            };
            reader.readAsDataURL(blob);
        } catch (e) {
            showNotification(S.errorCapturing, 'error');
        }
    }

    // --- Live Preview (Test Mode) ---

    function getThreeScene() {
        // Defensive access — try public API first, then fall back to Symbol
        if (viewer.model && viewer.model.scene) {
            return viewer.model.scene;
        }

        try {
            var symbols = Object.getOwnPropertySymbols(viewer);
            for (var i = 0; i < symbols.length; i++) {
                if (symbols[i].description === 'scene' || String(symbols[i]).indexOf('scene') !== -1) {
                    var s = viewer[symbols[i]];
                    if (s && s.traverse) return s;
                }
            }
        } catch (e) {
            // Symbol access not available
        }

        return null;
    }

    function applyMappingPreview(mapping) {
        if (!viewer.model) return;

        try {
            if (mapping.action_type === 'material_color') {
                var matName = mapping.action_data.material_name;
                var materials = viewer.model.materials;
                for (var i = 0; i < materials.length; i++) {
                    if (materials[i].name === matName) {
                        var hex = mapping.action_data.color;
                        var r = parseInt(hex.slice(1, 3), 16) / 255;
                        var g = parseInt(hex.slice(3, 5), 16) / 255;
                        var b = parseInt(hex.slice(5, 7), 16) / 255;
                        var alpha = mapping.action_data.alpha !== undefined ? mapping.action_data.alpha : 1;
                        materials[i].pbrMetallicRoughness.setBaseColorFactor([r, g, b, alpha]);
                        if (mapping.action_data.metallic !== undefined) {
                            materials[i].pbrMetallicRoughness.setMetallicFactor(mapping.action_data.metallic);
                        }
                        if (mapping.action_data.roughness !== undefined) {
                            materials[i].pbrMetallicRoughness.setRoughnessFactor(mapping.action_data.roughness);
                        }
                        if (mapping.action_data.emissive) {
                            var eHex = mapping.action_data.emissive;
                            var er = parseInt(eHex.slice(1, 3), 16) / 255;
                            var eg = parseInt(eHex.slice(3, 5), 16) / 255;
                            var eb = parseInt(eHex.slice(5, 7), 16) / 255;
                            materials[i].setEmissiveFactor([er, eg, eb]);
                            if (mapping.action_data.emissive_strength !== undefined) {
                                // Normalize by luminance so saturated colors bloom equally
                                var eLum = 0.2126 * er + 0.7152 * eg + 0.0722 * eb;
                                var adjStr = eLum > 0.01 ? mapping.action_data.emissive_strength / eLum : mapping.action_data.emissive_strength;
                                materials[i].setEmissiveStrength(adjStr);
                            }
                        }
                        // If no emissive in mapping, preserve the GLB's baked-in emissive
                        break;
                    }
                }
            } else if (mapping.action_type === 'material_texture') {
                var matName = mapping.action_data.material_name;
                var materials = viewer.model.materials;
                for (var i = 0; i < materials.length; i++) {
                    if (materials[i].name === matName) {
                        if (mapping.action_data.base_color_url) {
                            viewer.createTexture(mapping.action_data.base_color_url).then(function(texture) {
                                materials[i].pbrMetallicRoughness.baseColorTexture.setTexture(texture);
                            }).catch(function(e) {
                                console.warn('Preview texture error:', e);
                            });
                        }
                        if (mapping.action_data.metallic !== undefined) {
                            materials[i].pbrMetallicRoughness.setMetallicFactor(mapping.action_data.metallic);
                        }
                        if (mapping.action_data.roughness !== undefined) {
                            materials[i].pbrMetallicRoughness.setRoughnessFactor(mapping.action_data.roughness);
                        }
                        break;
                    }
                }
            } else if (mapping.action_type === 'visibility') {
                var scene = getThreeScene();
                if (scene) {
                    scene.traverse(function(node) {
                        if (node.name === mapping.target_node) {
                            node.visible = mapping.action_data.visible !== false;
                        }
                    });
                    viewer.requestUpdate();
                }
            }
        } catch (e) {
            console.warn('Preview error:', e);
        }
    }

    // --- Environment Image Picker ---

    function bindEnvironmentPicker() {
        var selectBtn = document.getElementById('btn-select-environment');
        var clearBtn = document.getElementById('btn-clear-environment');
        var nameEl = document.getElementById('environment-name');

        // Restore from scene data
        if (D.scene.environment_image_id) {
            selectBtn.dataset.envId = D.scene.environment_image_id;
        }

        selectBtn.addEventListener('click', function() {
            openMediaPicker(function(asset) {
                nameEl.textContent = asset.title;
                selectBtn.dataset.envId = asset.id;
                if (asset.url || asset.original_file_url) {
                    viewer.setAttribute('environment-image', asset.url || asset.original_file_url);
                }
            });
        });

        clearBtn.addEventListener('click', function() {
            nameEl.textContent = S.noneLabel;
            selectBtn.dataset.envId = '';
            viewer.removeAttribute('environment-image');
        });
    }

    // --- Init ---

    function init() {
        initViewer();
        renderNodeTree();
        renderMappings();
        renderGeometryAssets();
        renderTextureAssets();
        bindSettingsControls();
        bindEnvironmentPicker();

        // Buttons
        document.getElementById('btn-select-model').addEventListener('click', selectBaseModel);
        document.getElementById('btn-save-settings').addEventListener('click', saveSettings);
        document.getElementById('btn-capture-thumbnail').addEventListener('click', captureThumbnail);
        document.getElementById('btn-add-mapping').addEventListener('click', function() { openMappingModal(null); });
        document.getElementById('btn-add-geometry').addEventListener('click', openGeometryModal);
        document.getElementById('btn-add-texture').addEventListener('click', openTextureModal);
        document.getElementById('btn-reset-camera').addEventListener('click', function() {
            viewer.setAttribute('camera-orbit', D.scene.camera_orbit);
            viewer.setAttribute('camera-target', D.scene.camera_target);
        });

        // Camera capture — read current orbit/target string from model-viewer
        document.getElementById('btn-capture-camera').addEventListener('click', function() {
            var orbitStr = viewer.getAttribute('camera-orbit');
            var targetStr = viewer.getAttribute('camera-target');
            // model-viewer updates these attributes as the user interacts
            // Use the internal properties if available for live values
            if (viewer.getCameraOrbit) {
                var orbit = viewer.getCameraOrbit();
                var RAD2DEG = 180 / Math.PI;
                orbitStr = (orbit.theta * RAD2DEG).toFixed(1) + 'deg '
                         + (orbit.phi * RAD2DEG).toFixed(1) + 'deg '
                         + orbit.radius.toFixed(3) + 'm';
            }
            if (viewer.getCameraTarget) {
                var tgt = viewer.getCameraTarget();
                targetStr = tgt.x.toFixed(4) + 'm ' + tgt.y.toFixed(4) + 'm ' + tgt.z.toFixed(4) + 'm';
            }
            document.getElementById('setting-camera-orbit').value = orbitStr;
            document.getElementById('setting-camera-target').value = targetStr;
            showNotification('Camera position captured', 'success');
        });

        // Camera reset to saved default
        document.getElementById('btn-reset-camera-default').addEventListener('click', function() {
            var orbit = D.scene.camera_orbit;
            var target = D.scene.camera_target;
            viewer.setAttribute('camera-orbit', orbit);
            viewer.setAttribute('camera-target', target);
            document.getElementById('setting-camera-orbit').value = orbit;
            document.getElementById('setting-camera-target').value = target;
        });

        // Mapping modal
        document.getElementById('mapping-modal-close').addEventListener('click', closeMappingModal);
        document.getElementById('btn-mapping-cancel').addEventListener('click', closeMappingModal);
        document.getElementById('btn-mapping-save').addEventListener('click', saveMapping);
        document.getElementById('mapping-modal').querySelector('.scene-setup-modal__backdrop').addEventListener('click', closeMappingModal);

        // Geometry modal
        document.getElementById('geometry-modal-close').addEventListener('click', closeGeometryModal);
        document.getElementById('btn-geometry-cancel').addEventListener('click', closeGeometryModal);
        document.getElementById('btn-geometry-save').addEventListener('click', saveGeometryFromModal);
        document.getElementById('geometry-modal').querySelector('.scene-setup-modal__backdrop').addEventListener('click', closeGeometryModal);
        document.getElementById('btn-geometry-select-file').addEventListener('click', function() {
            openMediaPicker(function(asset) {
                document.getElementById('geometry-file-name').textContent = asset.title;
                document.getElementById('geometry-media-asset-id').value = asset.id;
                if (!document.getElementById('geometry-label').value) {
                    document.getElementById('geometry-label').value = asset.title || '';
                }
            });
        });

        // Texture modal
        document.getElementById('texture-modal-close').addEventListener('click', closeTextureModal);
        document.getElementById('btn-texture-cancel').addEventListener('click', closeTextureModal);
        document.getElementById('btn-texture-save').addEventListener('click', saveTextureFromModal);
        document.getElementById('texture-modal').querySelector('.scene-setup-modal__backdrop').addEventListener('click', closeTextureModal);
        document.getElementById('btn-texture-select-file').addEventListener('click', function() {
            openMediaPicker(function(asset) {
                document.getElementById('texture-file-name').textContent = asset.title;
                document.getElementById('texture-media-asset-id').value = asset.id;
                if (!document.getElementById('texture-label').value) {
                    document.getElementById('texture-label').value = asset.title || '';
                }
            });
        });

        // Action type toggle
        document.getElementById('mapping-action-type').addEventListener('change', function () {
            showActionFields(this.value);
        });

        // Enable toggle
        document.getElementById('scene-enabled').addEventListener('change', saveSettings);

        // Texture pickers inside mapping modal
        document.getElementById('btn-select-base-texture').addEventListener('click', function() {
            openMediaPicker(function(asset) {
                document.getElementById('action-base-texture-url').value = asset.url || asset.original_file_url || '';
                document.getElementById('base-texture-name').textContent = asset.title || S.selectedLabel;
            });
        });
        document.getElementById('btn-select-normal-texture').addEventListener('click', function() {
            openMediaPicker(function(asset) {
                document.getElementById('action-normal-texture-url').value = asset.url || asset.original_file_url || '';
                document.getElementById('normal-texture-name').textContent = asset.title || S.selectedLabel;
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
