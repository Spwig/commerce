/**
 * Design Editor Setup - Admin Page
 * Manages product surfaces, templates, clipart, fonts, pricing, and settings
 * for the customizable product visual editor.
 */
(function() {
    'use strict';

    // ─── State ──────────────────────────────────────────────────────────────
    var data = JSON.parse(document.getElementById('design-setup-data').textContent);
    var surfaces = data.surfaces || [];
    var templates = data.templates || [];
    var csrfToken = data.csrfToken || '';

    // Get CSRF token from cookie if not embedded
    if (!csrfToken) {
        var cookieMatch = document.cookie.match(/csrftoken=([^;]+)/);
        if (cookieMatch) csrfToken = cookieMatch[1];
    }

    // ─── Init ───────────────────────────────────────────────────────────────
    function init() {
        initTabs();
        renderSurfaces();
        renderTemplates();
        bindSurfaceModal();
        initZoneDragResize();
        bindTemplateModal();
        bindPricing();
        bindSettings();
        bindEnabledToggle();
    }

    // ─── Tabs ───────────────────────────────────────────────────────────────
    function initTabs() {
        var tabs = document.querySelectorAll('.design-setup-tab');
        tabs.forEach(function(tab) {
            tab.addEventListener('click', function() {
                tabs.forEach(function(t) { t.classList.remove('active'); });
                tab.classList.add('active');

                var panels = document.querySelectorAll('.design-setup-panel');
                panels.forEach(function(p) { p.classList.remove('active'); });
                var target = document.getElementById('panel-' + tab.dataset.tab);
                if (target) target.classList.add('active');
            });
        });
    }

    // ─── Notifications ──────────────────────────────────────────────────────
    function showNotification(message, type) {
        AdminModal.toast(message, type || 'info');
    }

    // ─── AJAX Helper ────────────────────────────────────────────────────────
    function ajaxPost(url, body) {
        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(body),
        }).then(function(res) {
            return res.json().then(function(json) {
                if (!res.ok) throw new Error(json.error || 'Request failed');
                return json;
            });
        });
    }

    // ─── Image Bounds Helper ─────────────────────────────────────────────────
    // Computes the rendered position/size of an image within its container,
    // accounting for object-fit: contain centering. Returns {left, top, width, height}
    // in pixels relative to the container.
    function getRenderedImageBounds(img) {
        var container = img.parentElement;
        var containerRect = container.getBoundingClientRect();
        var naturalW = img.naturalWidth;
        var naturalH = img.naturalHeight;
        if (!naturalW || !naturalH) return null;
        var containerW = containerRect.width;
        var containerH = containerRect.height;
        var scale = Math.min(containerW / naturalW, containerH / naturalH);
        var renderedW = naturalW * scale;
        var renderedH = naturalH * scale;
        return {
            left: (containerW - renderedW) / 2,
            top: (containerH - renderedH) / 2,
            width: renderedW,
            height: renderedH
        };
    }

    function positionCardZoneOverlays(container) {
        container.querySelectorAll('.design-setup-card__image img').forEach(function(img) {
            var positionOverlay = function() {
                var overlay = img.parentElement.querySelector('.design-setup-card__zone-overlay');
                if (!overlay) return;
                var bounds = getRenderedImageBounds(img);
                if (!bounds) return;
                var x = parseFloat(overlay.dataset.x) || 0;
                var y = parseFloat(overlay.dataset.y) || 0;
                var w = parseFloat(overlay.dataset.w) || 0;
                var h = parseFloat(overlay.dataset.h) || 0;
                overlay.style.left = (bounds.left + bounds.width * x / 100) + 'px';
                overlay.style.top = (bounds.top + bounds.height * y / 100) + 'px';
                overlay.style.width = (bounds.width * w / 100) + 'px';
                overlay.style.height = (bounds.height * h / 100) + 'px';
            };
            if (img.complete && img.naturalWidth) positionOverlay();
            else img.addEventListener('load', positionOverlay);
        });
    }

    // ─── Surfaces ───────────────────────────────────────────────────────────
    function renderSurfaces() {
        var grid = document.getElementById('surfaces-grid');
        grid.innerHTML = '';

        if (surfaces.length === 0) {
            grid.innerHTML = '<div class="design-setup-empty">' +
                '<i class="fas fa-layer-group"></i>' +
                '<p>No surfaces defined yet. Add a surface to get started.</p>' +
                '</div>';
            return;
        }

        surfaces.forEach(function(surface) {
            var card = document.createElement('div');
            card.className = 'design-setup-card';

            var imageHtml;
            if (surface.mockup_url) {
                imageHtml = '<div class="design-setup-card__image">' +
                    '<img src="' + escapeHtml(surface.mockup_url) + '" alt="' + escapeHtml(surface.name) + '">' +
                    '<div class="design-setup-card__zone-overlay"' +
                        ' data-x="' + surface.area_x_percent + '"' +
                        ' data-y="' + surface.area_y_percent + '"' +
                        ' data-w="' + surface.area_width_percent + '"' +
                        ' data-h="' + surface.area_height_percent + '">' +
                    '</div>' +
                    '</div>';
            } else {
                imageHtml = '<div class="design-setup-card__image design-setup-card__image--empty">' +
                    '<i class="fas fa-image"></i>No mockup image' +
                    '</div>';
            }

            card.innerHTML = imageHtml +
                '<div class="design-setup-card__body">' +
                    '<p class="design-setup-card__title">' + escapeHtml(surface.name) + '</p>' +
                    '<p class="design-setup-card__meta">' +
                        surface.width + ' × ' + surface.height + ' ' + surface.dimension_unit +
                        ' · ' + surface.recommended_dpi + ' DPI' +
                    '</p>' +
                '</div>' +
                '<div class="design-setup-card__actions">' +
                    '<button type="button" class="button button-small btn-edit-surface" data-id="' + surface.id + '">' +
                        '<i class="fas fa-edit"></i> Edit' +
                    '</button>' +
                    '<button type="button" class="button button-small button-danger btn-delete-surface" data-id="' + surface.id + '">' +
                        '<i class="fas fa-trash"></i> Delete' +
                    '</button>' +
                '</div>';

            grid.appendChild(card);
        });

        // Bind edit/delete buttons
        grid.querySelectorAll('.btn-edit-surface').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var id = parseInt(btn.dataset.id);
                var surface = surfaces.find(function(s) { return s.id === id; });
                if (surface) openSurfaceModal(surface);
            });
        });

        grid.querySelectorAll('.btn-delete-surface').forEach(function(btn) {
            btn.addEventListener('click', async function() {
                var id = parseInt(btn.dataset.id);
                if (await AdminModal.confirm({
                    message: data.strings.deleteConfirm || 'Are you sure?',
                    danger: true,
                    confirmText: 'Delete'
                })) {
                    deleteSurface(id);
                }
            });
        });

        // Position zone overlays after card images load (accounts for object-fit: contain)
        positionCardZoneOverlays(grid);
    }

    function deleteSurface(surfaceId) {
        var url = data.urls.deleteSurfaceBase + surfaceId + '/delete/';
        ajaxPost(url, {}).then(function() {
            surfaces = surfaces.filter(function(s) { return s.id !== surfaceId; });
            renderSurfaces();
            showNotification('Surface deleted');
        }).catch(function(err) {
            showNotification(err.message, 'error');
        });
    }

    // ─── Surface Modal ──────────────────────────────────────────────────────
    function bindSurfaceModal() {
        document.getElementById('btn-add-surface').addEventListener('click', function() {
            openSurfaceModal(null);
        });

        document.getElementById('btn-save-surface-modal').addEventListener('click', saveSurfaceFromModal);

        // Close handlers
        var modal = document.getElementById('modal-surface');
        modal.querySelector('.design-setup-modal__close').addEventListener('click', function() {
            closeSurfaceModal();
        });
        modal.querySelector('.design-setup-modal__backdrop').addEventListener('click', function() {
            closeSurfaceModal();
        });
        document.getElementById('btn-cancel-surface-modal').addEventListener('click', function() {
            closeSurfaceModal();
        });

        // Auto-generate slug from name
        document.getElementById('surface-name').addEventListener('input', function() {
            var slugField = document.getElementById('surface-slug');
            if (!document.getElementById('surface-edit-id').value) {
                slugField.value = slugify(this.value);
            }
        });

        // Media picker - uses media library widget modal
        document.getElementById('btn-select-mockup').addEventListener('click', function() {
            window.selectImageFromLibrary(function(selectedMedia) {
                if (!selectedMedia) return;
                document.getElementById('surface-mockup-asset-id').value = selectedMedia.id;
                var imgUrl = selectedMedia.thumbnail_url || selectedMedia.url;
                setMockupPreview(imgUrl);
                document.getElementById('btn-remove-mockup').classList.remove('hidden');
                updateZonePreview(imgUrl);
            });
        });

        document.getElementById('btn-remove-mockup').addEventListener('click', function() {
            document.getElementById('surface-mockup-asset-id').value = '';
            clearMockupPreview();
            this.classList.add('hidden');
            updateZonePreview(null);
        });

        // Zone position inputs update the preview
        ['surface-area-x', 'surface-area-y', 'surface-area-w', 'surface-area-h'].forEach(function(id) {
            document.getElementById(id).addEventListener('input', function() {
                updateZoneFromInputs();
            });
        });
    }

    function openSurfaceModal(surface) {
        var modal = document.getElementById('modal-surface');
        var title = document.getElementById('modal-surface-title');

        if (surface) {
            title.textContent = 'Edit Surface';
            document.getElementById('surface-edit-id').value = surface.id;
            document.getElementById('surface-name').value = surface.name;
            document.getElementById('surface-slug').value = surface.slug;
            document.getElementById('surface-width').value = surface.width;
            document.getElementById('surface-height').value = surface.height;
            document.getElementById('surface-unit').value = surface.dimension_unit;
            document.getElementById('surface-area-x').value = surface.area_x_percent;
            document.getElementById('surface-area-y').value = surface.area_y_percent;
            document.getElementById('surface-area-w').value = surface.area_width_percent;
            document.getElementById('surface-area-h').value = surface.area_height_percent;
            document.getElementById('surface-min-dpi').value = surface.min_dpi;
            document.getElementById('surface-rec-dpi').value = surface.recommended_dpi;
            document.getElementById('surface-bleed').value = surface.bleed_mm;
            document.getElementById('surface-max-colors').value = surface.max_colors || '';
            document.getElementById('surface-bg-color').value = surface.background_color || '#ffffff';
            document.getElementById('surface-sort-order').value = surface.sort_order;
            document.getElementById('surface-mockup-asset-id').value = surface.mockup_asset_id || '';
            document.getElementById('surface-allow-text').value = surface.allow_text === true ? 'true' : surface.allow_text === false ? 'false' : '';
            document.getElementById('surface-allow-image').value = surface.allow_image_upload === true ? 'true' : surface.allow_image_upload === false ? 'false' : '';
            document.getElementById('surface-allow-clipart').value = surface.allow_clipart === true ? 'true' : surface.allow_clipart === false ? 'false' : '';
            document.getElementById('surface-max-elements').value = surface.max_elements != null ? surface.max_elements : '';

            if (surface.mockup_url) {
                setMockupPreview(surface.mockup_url);
                document.getElementById('btn-remove-mockup').classList.remove('hidden');
                updateZonePreview(surface.mockup_url);
            } else {
                clearMockupPreview();
                document.getElementById('btn-remove-mockup').classList.add('hidden');
                updateZonePreview(null);
            }
        } else {
            title.textContent = 'Add Surface';
            document.getElementById('surface-edit-id').value = '';
            document.getElementById('surface-name').value = '';
            document.getElementById('surface-slug').value = '';
            document.getElementById('surface-width').value = '200';
            document.getElementById('surface-height').value = '200';
            document.getElementById('surface-unit').value = 'mm';
            document.getElementById('surface-area-x').value = '25';
            document.getElementById('surface-area-y').value = '15';
            document.getElementById('surface-area-w').value = '50';
            document.getElementById('surface-area-h').value = '70';
            document.getElementById('surface-min-dpi').value = '150';
            document.getElementById('surface-rec-dpi').value = '300';
            document.getElementById('surface-bleed').value = '0';
            document.getElementById('surface-max-colors').value = '';
            document.getElementById('surface-bg-color').value = '#ffffff';
            document.getElementById('surface-sort-order').value = surfaces.length;
            document.getElementById('surface-mockup-asset-id').value = '';
            document.getElementById('surface-allow-text').value = '';
            document.getElementById('surface-allow-image').value = '';
            document.getElementById('surface-allow-clipart').value = '';
            document.getElementById('surface-max-elements').value = '';
            clearMockupPreview();
            document.getElementById('btn-remove-mockup').classList.add('hidden');
            updateZonePreview(null);
        }

        updateZoneFromInputs();
        modal.setAttribute('aria-hidden', 'false');
    }

    function closeSurfaceModal() {
        document.getElementById('modal-surface').setAttribute('aria-hidden', 'true');
    }

    function saveSurfaceFromModal() {
        var editId = document.getElementById('surface-edit-id').value;
        var name = document.getElementById('surface-name').value.trim();
        var slug = document.getElementById('surface-slug').value.trim();

        if (!name || !slug) {
            showNotification('Name and slug are required', 'error');
            return;
        }

        var body = {
            name: name,
            slug: slug,
            dimension_unit: document.getElementById('surface-unit').value,
            width: parseFloat(document.getElementById('surface-width').value),
            height: parseFloat(document.getElementById('surface-height').value),
            area_x_percent: parseFloat(document.getElementById('surface-area-x').value),
            area_y_percent: parseFloat(document.getElementById('surface-area-y').value),
            area_width_percent: parseFloat(document.getElementById('surface-area-w').value),
            area_height_percent: parseFloat(document.getElementById('surface-area-h').value),
            min_dpi: parseInt(document.getElementById('surface-min-dpi').value) || 150,
            recommended_dpi: parseInt(document.getElementById('surface-rec-dpi').value) || 300,
            bleed_mm: parseFloat(document.getElementById('surface-bleed').value) || 0,
            max_colors: parseInt(document.getElementById('surface-max-colors').value) || null,
            background_color: document.getElementById('surface-bg-color').value,
            sort_order: parseInt(document.getElementById('surface-sort-order').value) || 0,
            mockup_asset_id: document.getElementById('surface-mockup-asset-id').value || null,
        };

        // Per-surface constraint overrides
        var allowTextVal = document.getElementById('surface-allow-text').value;
        body.allow_text = allowTextVal === '' ? null : allowTextVal === 'true';
        var allowImageVal = document.getElementById('surface-allow-image').value;
        body.allow_image_upload = allowImageVal === '' ? null : allowImageVal === 'true';
        var allowClipartVal = document.getElementById('surface-allow-clipart').value;
        body.allow_clipart = allowClipartVal === '' ? null : allowClipartVal === 'true';
        var maxElVal = document.getElementById('surface-max-elements').value;
        body.max_elements = maxElVal ? parseInt(maxElVal) : null;

        if (editId) body.id = parseInt(editId);

        ajaxPost(data.urls.saveSurface, body).then(function(response) {
            // Refresh surface list
            return fetch(data.urls.listSurfaces).then(function(res) { return res.json(); });
        }).then(function(response) {
            surfaces = response.surfaces;
            renderSurfaces();
            closeSurfaceModal();
            showNotification(data.strings.saveSuccess || 'Saved successfully');
        }).catch(function(err) {
            showNotification(err.message, 'error');
        });
    }

    function updateZonePreview(mockupUrl) {
        var container = document.getElementById('zone-preview-mockup');
        var existingImg = container.querySelector('img');
        if (existingImg) existingImg.remove();

        if (mockupUrl) {
            var img = document.createElement('img');
            img.src = mockupUrl;
            img.addEventListener('load', function() {
                if (img.naturalWidth && img.naturalHeight) {
                    container.style.aspectRatio = img.naturalWidth + '/' + img.naturalHeight;
                }
                updateZoneFromInputs();
            });
            container.insertBefore(img, container.firstChild);
        } else {
            container.style.aspectRatio = '4/5';
        }
    }

    function updateZoneFromInputs() {
        var zone = document.getElementById('zone-preview-zone');
        zone.style.left = document.getElementById('surface-area-x').value + '%';
        zone.style.top = document.getElementById('surface-area-y').value + '%';
        zone.style.width = document.getElementById('surface-area-w').value + '%';
        zone.style.height = document.getElementById('surface-area-h').value + '%';
    }

    // ─── Zone Drag & Resize ─────────────────────────────────────────────────
    function initZoneDragResize() {
        var container = document.getElementById('zone-preview-mockup');
        var zone = document.getElementById('zone-preview-zone');
        var dragging = false;
        var resizing = false;
        var resizeHandle = null;
        var startX, startY, startLeft, startTop, startW, startH;

        function pxToPercent(px, total) {
            return (px / total) * 100;
        }

        function clamp(val, min, max) {
            return Math.max(min, Math.min(max, val));
        }

        function syncInputsFromZone() {
            var rect = container.getBoundingClientRect();
            var zoneRect = zone.getBoundingClientRect();
            var x = pxToPercent(zoneRect.left - rect.left, rect.width);
            var y = pxToPercent(zoneRect.top - rect.top, rect.height);
            var w = pxToPercent(zoneRect.width, rect.width);
            var h = pxToPercent(zoneRect.height, rect.height);
            document.getElementById('surface-area-x').value = Math.round(x * 2) / 2;
            document.getElementById('surface-area-y').value = Math.round(y * 2) / 2;
            document.getElementById('surface-area-w').value = Math.round(w * 2) / 2;
            document.getElementById('surface-area-h').value = Math.round(h * 2) / 2;
        }

        // Drag start on zone (but not on resize handles)
        zone.addEventListener('mousedown', function(e) {
            if (e.target.dataset.handle) return;
            e.preventDefault();
            dragging = true;
            var rect = container.getBoundingClientRect();
            startX = e.clientX;
            startY = e.clientY;
            startLeft = zone.offsetLeft;
            startTop = zone.offsetTop;
        });

        // Resize start on handles
        zone.addEventListener('mousedown', function(e) {
            if (!e.target.dataset.handle) return;
            e.preventDefault();
            e.stopPropagation();
            resizing = true;
            resizeHandle = e.target.dataset.handle;
            startX = e.clientX;
            startY = e.clientY;
            startLeft = zone.offsetLeft;
            startTop = zone.offsetTop;
            startW = zone.offsetWidth;
            startH = zone.offsetHeight;
        });

        document.addEventListener('mousemove', function(e) {
            if (!dragging && !resizing) return;
            e.preventDefault();
            var rect = container.getBoundingClientRect();
            var dx = e.clientX - startX;
            var dy = e.clientY - startY;

            if (dragging) {
                var newLeft = clamp(startLeft + dx, 0, rect.width - zone.offsetWidth);
                var newTop = clamp(startTop + dy, 0, rect.height - zone.offsetHeight);
                zone.style.left = pxToPercent(newLeft, rect.width) + '%';
                zone.style.top = pxToPercent(newTop, rect.height) + '%';
                syncInputsFromZone();
            }

            if (resizing) {
                var minSize = 10; // min px
                var newL, newT, newW, newH;

                if (resizeHandle === 'se') {
                    newW = clamp(startW + dx, minSize, rect.width - startLeft);
                    newH = clamp(startH + dy, minSize, rect.height - startTop);
                    zone.style.width = pxToPercent(newW, rect.width) + '%';
                    zone.style.height = pxToPercent(newH, rect.height) + '%';
                } else if (resizeHandle === 'sw') {
                    newW = clamp(startW - dx, minSize, startLeft + startW);
                    newL = startLeft + (startW - newW);
                    newH = clamp(startH + dy, minSize, rect.height - startTop);
                    zone.style.left = pxToPercent(newL, rect.width) + '%';
                    zone.style.width = pxToPercent(newW, rect.width) + '%';
                    zone.style.height = pxToPercent(newH, rect.height) + '%';
                } else if (resizeHandle === 'ne') {
                    newW = clamp(startW + dx, minSize, rect.width - startLeft);
                    newH = clamp(startH - dy, minSize, startTop + startH);
                    newT = startTop + (startH - newH);
                    zone.style.top = pxToPercent(newT, rect.height) + '%';
                    zone.style.width = pxToPercent(newW, rect.width) + '%';
                    zone.style.height = pxToPercent(newH, rect.height) + '%';
                } else if (resizeHandle === 'nw') {
                    newW = clamp(startW - dx, minSize, startLeft + startW);
                    newH = clamp(startH - dy, minSize, startTop + startH);
                    newL = startLeft + (startW - newW);
                    newT = startTop + (startH - newH);
                    zone.style.left = pxToPercent(newL, rect.width) + '%';
                    zone.style.top = pxToPercent(newT, rect.height) + '%';
                    zone.style.width = pxToPercent(newW, rect.width) + '%';
                    zone.style.height = pxToPercent(newH, rect.height) + '%';
                }
                syncInputsFromZone();
            }
        });

        document.addEventListener('mouseup', function() {
            dragging = false;
            resizing = false;
            resizeHandle = null;
        });
    }

    // ─── Templates ──────────────────────────────────────────────────────────
    function renderTemplates() {
        var grid = document.getElementById('templates-grid');
        grid.innerHTML = '';

        if (templates.length === 0) {
            grid.innerHTML = '<div class="design-setup-empty">' +
                '<i class="fas fa-palette"></i>' +
                '<p>No design templates yet. Create templates for customers to start from.</p>' +
                '</div>';
            return;
        }

        templates.forEach(function(template) {
            var card = document.createElement('div');
            card.className = 'design-setup-card';

            var imageHtml;
            if (template.thumbnail_url) {
                imageHtml = '<div class="design-setup-card__image">' +
                    '<img src="' + escapeHtml(template.thumbnail_url) + '" alt="' + escapeHtml(template.name) + '">' +
                    '</div>';
            } else {
                imageHtml = '<div class="design-setup-card__image design-setup-card__image--empty">' +
                    '<i class="fas fa-palette"></i>No preview' +
                    '</div>';
            }

            card.innerHTML = imageHtml +
                '<div class="design-setup-card__body">' +
                    '<p class="design-setup-card__title">' + escapeHtml(template.name) + '</p>' +
                    '<p class="design-setup-card__meta">' +
                        (template.category ? escapeHtml(template.category) : 'Uncategorized') +
                    '</p>' +
                '</div>' +
                '<div class="design-setup-card__actions">' +
                    '<button type="button" class="button button-small btn-edit-template" data-id="' + template.id + '">' +
                        '<i class="fas fa-edit"></i> Edit' +
                    '</button>' +
                    '<button type="button" class="button button-small button-danger btn-delete-template" data-id="' + template.id + '">' +
                        '<i class="fas fa-trash"></i> Delete' +
                    '</button>' +
                '</div>';

            grid.appendChild(card);
        });

        // Bind edit/delete buttons
        grid.querySelectorAll('.btn-edit-template').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var id = parseInt(btn.dataset.id);
                navigateToTemplateEditor(id);
            });
        });

        grid.querySelectorAll('.btn-delete-template').forEach(function(btn) {
            btn.addEventListener('click', async function() {
                var id = parseInt(btn.dataset.id);
                if (await AdminModal.confirm({
                    message: data.strings.deleteConfirm || 'Are you sure?',
                    danger: true,
                    confirmText: 'Delete'
                })) {
                    deleteTemplate(id);
                }
            });
        });
    }

    function deleteTemplate(templateId) {
        var url = data.urls.deleteTemplateBase + templateId + '/delete/';
        ajaxPost(url, {}).then(function() {
            templates = templates.filter(function(t) { return t.id !== templateId; });
            renderTemplates();
            showNotification('Template deleted');
        }).catch(function(err) {
            showNotification(err.message, 'error');
        });
    }

    // ─── Template Editor Navigation ─────────────────────────────────────────
    function bindTemplateModal() {
        document.getElementById('btn-add-template').addEventListener('click', function() {
            navigateToTemplateEditor(null);
        });
    }

    function navigateToTemplateEditor(templateId) {
        var baseUrl = '/admin/customizable-product/product/' + data.productId + '/template-editor/';
        if (templateId) {
            baseUrl += '?template_id=' + templateId;
        }
        window.location.href = baseUrl;
    }

    // ─── Pricing ────────────────────────────────────────────────────────────
    function bindPricing() {
        document.getElementById('btn-save-pricing').addEventListener('click', function() {
            var body = {
                base_design_fee: parseFloat(document.getElementById('pricing-base-fee').value) || 0,
                per_surface_fee: parseFloat(document.getElementById('pricing-surface-fee').value) || 0,
                per_upload_fee: parseFloat(document.getElementById('pricing-upload-fee').value) || 0,
                per_text_fee: parseFloat(document.getElementById('pricing-text-fee').value) || 0,
            };

            ajaxPost(data.urls.saveConfig, body).then(function() {
                showNotification('Pricing saved');
            }).catch(function(err) {
                showNotification(err.message, 'error');
            });
        });
    }

    // ─── Settings ───────────────────────────────────────────────────────────
    function bindSettings() {
        document.getElementById('btn-save-settings').addEventListener('click', function() {
            var uploadTypesRaw = document.getElementById('setting-upload-types').value;
            var uploadTypes = uploadTypesRaw
                ? uploadTypesRaw.split(',').map(function(s) { return s.trim().toLowerCase(); }).filter(Boolean)
                : [];

            var body = {
                editor_mode: document.getElementById('setting-editor-mode').value,
                allow_text: document.getElementById('setting-allow-text').checked,
                allow_image_upload: document.getElementById('setting-allow-upload').checked,
                allow_clipart: document.getElementById('setting-allow-clipart').checked,
                max_uploads_per_surface: parseInt(document.getElementById('setting-max-uploads').value) || 5,
                max_upload_size_mb: parseFloat(document.getElementById('setting-max-size').value) || 10,
                allowed_upload_types: uploadTypes,
            };

            ajaxPost(data.urls.saveConfig, body).then(function() {
                showNotification('Settings saved');
            }).catch(function(err) {
                showNotification(err.message, 'error');
            });
        });
    }

    // ─── Enabled Toggle ─────────────────────────────────────────────────────
    function bindEnabledToggle() {
        document.getElementById('editor-enabled').addEventListener('change', function() {
            ajaxPost(data.urls.saveConfig, { is_enabled: this.checked }).then(function() {
                showNotification('Editor ' + (document.getElementById('editor-enabled').checked ? 'enabled' : 'disabled'));
            }).catch(function(err) {
                showNotification(err.message, 'error');
            });
        });
    }

    // ─── Media Preview Helpers ──────────────────────────────────────────────
    function setMockupPreview(imageUrl) {
        var preview = document.getElementById('surface-mockup-preview');
        var img = document.createElement('img');
        img.src = imageUrl;
        img.alt = 'Mockup';
        img.className = 'preview-image';
        preview.innerHTML = '';
        preview.appendChild(img);
    }

    function clearMockupPreview() {
        var preview = document.getElementById('surface-mockup-preview');
        preview.innerHTML =
            '<div class="no-image-preview drop-zone">' +
            '<i class="fas fa-image"></i>' +
            '<span>No image selected</span>' +
            '</div>';
    }

    // ─── Utilities ──────────────────────────────────────────────────────────
    function slugify(text) {
        return text.toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/[\s_]+/g, '-')
            .replace(/^-+|-+$/g, '')
            .substring(0, 100);
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str || ''));
        return div.innerHTML;
    }

    // ─── Bootstrap ──────────────────────────────────────────────────────────
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
