/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var configEl = document.getElementById('page-change-form-config');
    var config = configEl ? JSON.parse(configEl.textContent) : {};
    var i18n = config.i18n || {};

    function initSEOPreview() {
        var titleField = document.querySelector('[name="title"]');
        var metaTitleField = document.querySelector('[name="meta_title"]');
        var metaDescField = document.querySelector('[name="meta_description"]');

        var previewTitle = document.getElementById('seo-preview-title');
        var previewDesc = document.getElementById('seo-preview-description');

        function updatePreview() {
            if (previewTitle) {
                var title = (metaTitleField && metaTitleField.value) || (titleField && titleField.value) || i18n.pageTitle || 'Page Title';
                previewTitle.textContent = title;
            }
            if (previewDesc) {
                var desc = (metaDescField && metaDescField.value) || i18n.pageDescPlaceholder || '';
                if (desc.length > 160) {
                    desc = desc.substring(0, 157) + '...';
                }
                previewDesc.textContent = desc;
            }
        }

        [titleField, metaTitleField, metaDescField].forEach(function (field) {
            if (field) {
                field.addEventListener('input', updatePreview);
            }
        });

        updatePreview();
    }

    function initSlugPrepopulate() {
        var titleField = document.querySelector('[name="title"]');
        var slugField = document.querySelector('[name="slug"]');

        if (titleField && slugField && !slugField.value) {
            titleField.addEventListener('input', function () {
                if (!slugField.dataset.edited) {
                    var slug = this.value.toLowerCase()
                        .replace(/[^\w\s-]/g, '')
                        .replace(/\s+/g, '-')
                        .replace(/-+/g, '-')
                        .trim();
                    slugField.value = slug;
                }
            });

            slugField.addEventListener('input', function () {
                this.dataset.edited = 'true';
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initSEOPreview();
            initSlugPrepopulate();
        });
    } else {
        initSEOPreview();
        initSlugPrepopulate();
    }
})();
