(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        // Tab switching handled by global AdminTabs utility

        // Save button handlers
        initSaveButtons();

        // Slug auto-generation
        initSlugGeneration();

        // SEO preview updates
        initSeoPreview();

        // Media preview updates on widget change
        initMediaPreview();
    });

    /**
     * Initialize save button handlers
     */
    function initSaveButtons() {
        var form = document.getElementById('category-form');
        var saveContinueBtn = document.getElementById('save-continue-btn');

        if (saveContinueBtn && form) {
            saveContinueBtn.addEventListener('click', function () {
                // Add _continue input to trigger "save and continue"
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = '_continue';
                input.value = '1';
                form.appendChild(input);
                form.submit();
            });
        }
    }

    /**
     * Initialize slug auto-generation from name
     */
    function initSlugGeneration() {
        var nameField = document.querySelector('[name="name"]');
        var slugField = document.querySelector('[name="slug"]');

        if (nameField && slugField && !slugField.value) {
            nameField.addEventListener('input', function () {
                if (!slugField.dataset.edited) {
                    slugField.value = nameField.value
                        .toLowerCase()
                        .replace(/[^\w\s-]/g, '')
                        .replace(/\s+/g, '-')
                        .replace(/-+/g, '-')
                        .trim();
                }
            });

            slugField.addEventListener('input', function () {
                slugField.dataset.edited = 'true';
            });
        }
    }

    /**
     * Update media preview boxes when images are selected, uploaded, or cleared
     */
    function initMediaPreview() {
        var previewMap = {
            'image_asset': { id: 'image-asset-preview', icon: 'fa-image', label: 'Category Image' },
            'banner_asset': { id: 'banner-asset-preview', icon: 'fa-panorama', label: 'Banner Image' }
        };

        document.addEventListener('media-widget-change', function (e) {
            var config = previewMap[e.detail.fieldName];
            if (!config) return;
            var box = document.getElementById(config.id);
            if (!box) return;

            if (e.detail.imageUrl) {
                box.innerHTML = '<img src="' + e.detail.imageUrl + '" alt="Preview">';
            } else {
                box.innerHTML = '<div class="placeholder"><i class="fas ' + config.icon + '"></i> ' + config.label + '</div>';
            }
        });
    }

    /**
     * Initialize SEO preview updates
     */
    function initSeoPreview() {
        var metaTitleField = document.querySelector('[name="meta_title"]');
        var metaDescField = document.querySelector('[name="meta_description"]');
        var nameField = document.querySelector('[name="name"]');
        var descField = document.querySelector('[name="description"]');

        var previewTitle = document.getElementById('seo-preview-title');
        var previewDesc = document.getElementById('seo-preview-description');

        function updatePreview() {
            if (previewTitle) {
                var title = (metaTitleField && metaTitleField.value) ||
                            (nameField && nameField.value) ||
                            'Category Title';
                previewTitle.textContent = title;
            }
            if (previewDesc) {
                var desc = (metaDescField && metaDescField.value) ||
                           (descField && descField.value) ||
                           'Category description will appear here...';
                // Truncate to ~160 chars for preview
                if (desc.length > 160) {
                    desc = desc.substring(0, 157) + '...';
                }
                previewDesc.textContent = desc;
            }
        }

        // Add listeners to relevant fields
        [metaTitleField, metaDescField, nameField, descField].forEach(function (field) {
            if (field) {
                field.addEventListener('input', updatePreview);
            }
        });
    }
})();
