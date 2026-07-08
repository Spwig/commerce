/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Configurator 3D Viewer
 *
 * Companion script to product_configurator.js. Listens for
 * 'configurator:selection-changed' CustomEvents and applies
 * material, texture, geometry, and visibility changes to
 * the <model-viewer> element.
 *
 * Does NOT duplicate wizard logic — only handles 3D visual updates.
 */
(function () {
    'use strict';

    var dataEl = document.getElementById('configurator-data');
    if (!dataEl) return;

    var configData;
    try {
        configData = JSON.parse(dataEl.textContent);
    } catch (e) {
        console.error('Failed to parse configurator data:', e);
        return;
    }

    var scene3d = configData.scene_3d;
    if (!scene3d || !scene3d.base_model_url) return;

    var viewer = document.getElementById('product-3d-viewer');
    if (!viewer) return;

    var mappings = scene3d.mappings || {};
    var geometryCache = {};

    // --- Initialization ---

    function setViewerProp(prop, attr, value) {
        if (prop in viewer) {
            viewer[prop] = value;
        } else {
            viewer.setAttribute(attr, value);
        }
    }

    function initViewer() {
        viewer.setAttribute('src', scene3d.base_model_url);
        viewer.setAttribute('camera-orbit', scene3d.camera_orbit || '0deg 75deg 2m');
        viewer.setAttribute('camera-target', scene3d.camera_target || '0m 0m 0m');
        setViewerProp('exposure', 'exposure', parseFloat(scene3d.exposure) || 1.0);
        setViewerProp('shadowIntensity', 'shadow-intensity', parseFloat(scene3d.shadow_intensity) || 0.5);
        setViewerProp('shadowSoftness', 'shadow-softness', parseFloat(scene3d.shadow_softness) || 0.5);
        setViewerProp('toneMapping', 'tone-mapping', scene3d.tone_mapping || 'commerce');
        viewer.style.setProperty('--viewer-bg', scene3d.background_color || '#ffffff');

        if (scene3d.auto_rotate) viewer.setAttribute('auto-rotate', '');
        if (scene3d.ar_enabled) viewer.setAttribute('ar', '');
        // Use uploaded HDR, or fall back to 'legacy' for better metallic reflections
        viewer.setAttribute('environment-image', scene3d.environment_url || 'legacy');

        // Show loading state
        viewer.addEventListener('load', function () {
            var overlay = document.getElementById('viewer-loading');
            if (overlay) overlay.classList.add('hidden');
        });
    }

    // --- Color Helpers ---

    function hexToRgb(hex) {
        hex = hex.replace('#', '');
        return [
            parseInt(hex.substring(0, 2), 16) / 255,
            parseInt(hex.substring(2, 4), 16) / 255,
            parseInt(hex.substring(4, 6), 16) / 255,
        ];
    }

    /** Perceived luminance (ITU-R BT.709). */
    function rgbLuminance(rgb) {
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
    }

    // --- Material Color ---

    function applyMaterialColor(mapping) {
        if (!viewer.model) return;
        var data = mapping.data;
        var matName = data.material_name;
        if (!matName) return;

        var materials = viewer.model.materials;
        for (var i = 0; i < materials.length; i++) {
            if (materials[i].name === matName) {
                var rgb = hexToRgb(data.color || '#ffffff');
                var alpha = data.alpha !== undefined ? data.alpha : 1;
                materials[i].pbrMetallicRoughness.setBaseColorFactor([rgb[0], rgb[1], rgb[2], alpha]);
                if (data.metallic !== undefined) {
                    materials[i].pbrMetallicRoughness.setMetallicFactor(data.metallic);
                }
                if (data.roughness !== undefined) {
                    materials[i].pbrMetallicRoughness.setRoughnessFactor(data.roughness);
                }
                if (data.emissive) {
                    var emRgb = hexToRgb(data.emissive);
                    materials[i].setEmissiveFactor(emRgb);
                    if (data.emissive_strength !== undefined) {
                        // Normalize strength by luminance so saturated colors
                        // (e.g. deep red, purple) bloom as strongly as white.
                        var lum = rgbLuminance(emRgb);
                        var adjStrength = lum > 0.01 ? data.emissive_strength / lum : data.emissive_strength;
                        materials[i].setEmissiveStrength(adjStrength);
                    }
                }
                // If no emissive in mapping, preserve the GLB's baked-in emissive
                break;
            }
        }
    }

    // --- Material Texture ---

    async function applyMaterialTexture(mapping) {
        if (!viewer.model) return;
        var data = mapping.data;
        var matName = data.material_name;
        if (!matName) return;

        var materials = viewer.model.materials;
        for (var i = 0; i < materials.length; i++) {
            if (materials[i].name === matName) {
                if (data.base_color_url) {
                    try {
                        var texture = await viewer.createTexture(data.base_color_url);
                        materials[i].pbrMetallicRoughness.baseColorTexture.setTexture(texture);
                    } catch (e) {
                        console.warn('Error applying base color texture:', e);
                    }
                }
                if (data.normal_url) {
                    try {
                        var normalTex = await viewer.createTexture(data.normal_url);
                        materials[i].normalTexture.setTexture(normalTex);
                    } catch (e) {
                        console.warn('Error applying normal texture:', e);
                    }
                }
                if (data.metallic !== undefined) {
                    materials[i].pbrMetallicRoughness.setMetallicFactor(data.metallic);
                }
                if (data.roughness !== undefined) {
                    materials[i].pbrMetallicRoughness.setRoughnessFactor(data.roughness);
                }
                break;
            }
        }
    }

    // --- Geometry Swap ---

    async function applyGeometrySwap(mapping) {
        var data = mapping.data;
        var glbUrl = data.glb_url;
        var targetNode = mapping.node;

        if (!glbUrl || !targetNode) return;
        if (!window.THREE) {
            console.warn('THREE.js not available for geometry swap');
            return;
        }

        try {
            // Get the Three.js scene from model-viewer
            var scene = getThreeScene();
            if (!scene) return;

            // Load or get cached geometry
            var loaded = geometryCache[glbUrl];
            if (!loaded) {
                var loader = new window.THREE.GLTFLoader();
                loaded = await new Promise(function (resolve, reject) {
                    loader.load(glbUrl, resolve, undefined, reject);
                });
                geometryCache[glbUrl] = loaded;
            }

            // Find target node in scene
            scene.traverse(function (node) {
                if (node.name === targetNode) {
                    // Remove existing children meshes
                    while (node.children.length > 0) {
                        node.remove(node.children[0]);
                    }
                    // Clone and add new children from loaded GLB
                    loaded.scene.children.forEach(function (child) {
                        node.add(child.clone());
                    });
                }
            });

            viewer.requestUpdate();
        } catch (e) {
            console.warn('Error in geometry swap:', e);
        }
    }

    // --- Visibility ---

    function applyVisibility(mapping) {
        var scene = getThreeScene();
        if (!scene) return;

        scene.traverse(function (node) {
            if (node.name === mapping.node) {
                node.visible = mapping.data.visible !== false;
            }
        });

        viewer.requestUpdate();
    }

    // --- Three.js Scene Access ---

    function getThreeScene() {
        // Access the internal Three.js scene from model-viewer
        // model-viewer exposes it through various methods
        if (viewer.model && viewer.model.scene) {
            return viewer.model.scene;
        }

        // Try symbol-based access
        var symbols = Object.getOwnPropertySymbols(viewer);
        for (var i = 0; i < symbols.length; i++) {
            if (symbols[i].description === 'scene' || String(symbols[i]).indexOf('scene') !== -1) {
                var s = viewer[symbols[i]];
                if (s && s.traverse) return s;
            }
        }

        return null;
    }

    // --- Apply All Mappings for Selected Options ---

    function applySelections(selections) {
        if (!viewer.model) return;

        // Collect all active option IDs
        var activeOptionIds = new Set();
        Object.keys(selections).forEach(function (slotId) {
            var opts = selections[slotId];
            if (Array.isArray(opts)) {
                opts.forEach(function (id) { activeOptionIds.add(String(id)); });
            }
        });

        // Apply mappings for each active option
        activeOptionIds.forEach(function (optionId) {
            var optionMappings = mappings[optionId];
            if (!optionMappings) return;

            optionMappings.forEach(function (mapping) {
                switch (mapping.action) {
                    case 'material_color':
                        applyMaterialColor(mapping);
                        break;
                    case 'material_texture':
                        applyMaterialTexture(mapping);
                        break;
                    case 'geometry_swap':
                        applyGeometrySwap(mapping);
                        break;
                    case 'visibility':
                        applyVisibility(mapping);
                        break;
                }
            });
        });
    }

    // --- Event Listener ---

    document.addEventListener('configurator:selection-changed', function (e) {
        var selections = e.detail.selections;
        if (selections) {
            applySelections(selections);
        }
    });

    // --- Emissive Defaults from GLB Node Tree ---

    var DEFAULT_EMISSIVE_BOOST = 10.0;

    function applyEmissiveDefaults() {
        if (!viewer.model) return;
        var treeMats = (scene3d.node_tree || {}).materials || {};
        var materials = viewer.model.materials;
        var bloomStrength = parseFloat(scene3d.bloom_strength) || 0;

        for (var i = 0; i < materials.length; i++) {
            var treeData = treeMats[materials[i].name];
            if (!treeData) continue;

            var ec = treeData.emissive_color;
            if (ec && (ec[0] > 0 || ec[1] > 0 || ec[2] > 0)) {
                materials[i].setEmissiveFactor([ec[0], ec[1], ec[2]]);
                var strength = treeData.emissive_strength || 0;
                if (strength > 0) {
                    materials[i].setEmissiveStrength(strength);
                } else if (bloomStrength > 0) {
                    materials[i].setEmissiveStrength(DEFAULT_EMISSIVE_BOOST);
                }
            }
        }
    }

    // --- Wait for model-viewer to load then init ---

    viewer.addEventListener('load', function () {
        // Restore emissive properties from node_tree before applying mappings
        applyEmissiveDefaults();

        // Apply default selections if any are already set
        var configDataEl = document.getElementById('configurator-data');
        if (configDataEl) {
            try {
                var configData = JSON.parse(configDataEl.textContent);
                var defaults = {};
                (configData.slots || []).forEach(function (slot) {
                    defaults[slot.id] = [];
                    (slot.options || []).forEach(function (opt) {
                        if (opt.is_default) {
                            defaults[slot.id].push(opt.id);
                        }
                    });
                });
                applySelections(defaults);
            } catch (e) {
                // No defaults
            }
        }

        // Bloom <effect-composer> is rendered server-side in the template
        // with the correct strength value, so no JS activation needed.
    });

    // --- Fullscreen Toggle (desktop) ---

    function initFullscreenToggle() {
        var btn = document.getElementById('btn-3d-fullscreen');
        var section = document.querySelector('.configurator-3d-section');
        if (!btn || !section) return;

        var FS_CLASS = 'configurator-3d-section--fullscreen';

        btn.addEventListener('click', toggle);

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && section.classList.contains(FS_CLASS)) {
                toggle();
            }
        });

        function toggle() {
            var isFs = section.classList.toggle(FS_CLASS);
            var icon = btn.querySelector('i');
            if (icon) {
                icon.className = isFs ? 'fas fa-compress' : 'fas fa-expand';
            }
            document.body.style.overflow = isFs ? 'hidden' : '';
        }
    }

    initFullscreenToggle();

    // Wait for model-viewer custom element to be defined (module scripts
    // execute after defer scripts, so the element may not be upgraded yet)
    if (customElements.get('model-viewer')) {
        initViewer();
    } else {
        customElements.whenDefined('model-viewer').then(initViewer);
    }
})();
