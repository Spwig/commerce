/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Announcements Admin JavaScript
 * Handles link type toggling, image display mode toggle,
 * and collapsible card sections.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initLinkSelector();
    initImageDisplayToggle();
    initCollapsibleCards();
  });

  /**
   * Link type selector — uses AdminLinkSelector for search-based FK selection.
   */
  function initLinkSelector() {
    if (typeof AdminLinkSelector === 'undefined') return;

    let initialData = {};
    const dataEl = document.getElementById('link-selector-initial');
    if (dataEl) {
      try {
        initialData = JSON.parse(dataEl.textContent);
      } catch (e) {}
    }

    new AdminLinkSelector({
      linkTypeFieldId: 'id_link_type',
      fieldMap: {
        product: {
          inputId: 'id_product_reference',
          apiType: 'product',
          resultKey: 'products',
          icon: 'fa-box',
        },
        category: {
          inputId: 'id_category_reference',
          apiType: 'category',
          resultKey: 'categories',
          icon: 'fa-folder',
        },
        blog_post: {
          inputId: 'id_blog_post_reference',
          apiType: 'blog',
          resultKey: 'blog_posts',
          icon: 'fa-newspaper',
        },
        page: {
          inputId: 'id_page_reference',
          apiType: 'page',
          resultKey: 'pages',
          icon: 'fa-file',
        },
      },
      customUrlContainerId: 'ref-custom_url',
      linkOptionsSelector: '#ann-link-options',
      searchContainerId: 'link-search-container',
      apiUrl: '/api/page-builder/link-sources/',
      initialData: initialData,
    });
  }

  /**
   * Show/hide overlay opacity based on image_display_mode.
   */
  function initImageDisplayToggle() {
    const displayModeField = document.getElementById('id_image_display_mode');
    if (!displayModeField) return;

    function updateOverlay() {
      const opacityField = document.getElementById('ann-overlay-opacity');
      if (!opacityField) return;

      if (displayModeField.value === 'background') {
        opacityField.classList.remove('overlay-hidden');
      } else {
        opacityField.classList.add('overlay-hidden');
      }
    }

    displayModeField.addEventListener('change', updateOverlay);
    updateOverlay();
  }

  /**
   * Collapsible card toggle.
   */
  function initCollapsibleCards() {
    const toggles = document.querySelectorAll('.ann-card-toggle');
    for (let i = 0; i < toggles.length; i++) {
      toggles[i].addEventListener('click', function () {
        const card = this.closest('.ann-card-collapsible');
        if (card) card.classList.toggle('open');
      });
    }

    // Auto-expand visibility card if any rules are selected
    const visBody = document.getElementById('ann-visibility-body');
    if (visBody) {
      const sel = visBody.querySelector('select');
      const hasSelection = sel && sel.querySelector('option:checked');
      if (hasSelection) {
        const visCard = visBody.closest('.ann-card-collapsible');
        if (visCard) visCard.classList.add('open');
      }
    }
  }
})();
