/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  const configEl = document.getElementById('page-change-form-config');
  const config = configEl ? JSON.parse(configEl.textContent) : {};
  const i18n = config.i18n || {};

  function initSEOPreview() {
    const titleField = document.querySelector('[name="title"]');
    const metaTitleField = document.querySelector('[name="meta_title"]');
    const metaDescField = document.querySelector('[name="meta_description"]');

    const previewTitle = document.getElementById('seo-preview-title');
    const previewDesc = document.getElementById('seo-preview-description');

    function updatePreview() {
      if (previewTitle) {
        const title =
          (metaTitleField && metaTitleField.value) ||
          (titleField && titleField.value) ||
          i18n.pageTitle ||
          'Page Title';
        previewTitle.textContent = title;
      }
      if (previewDesc) {
        let desc = (metaDescField && metaDescField.value) || i18n.pageDescPlaceholder || '';
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
    const titleField = document.querySelector('[name="title"]');
    const slugField = document.querySelector('[name="slug"]');

    if (titleField && slugField && !slugField.value) {
      titleField.addEventListener('input', function () {
        if (!slugField.dataset.edited) {
          const slug = this.value
            .toLowerCase()
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
