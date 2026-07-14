/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * CKEditor 5 Media Library Integration
 *
 * Shared module that integrates the platform Media Library with any CKEditor 5
 * instance on the page. Handles:
 *   1. Replacing CKEditor's native file dialog with Media Library image picker
 *   2. Adding "Browse Media Library" action button below editors
 *   3. Adding "Insert Video" action button for media library video or external URLs
 *
 * Requirements:
 *   - media-library.js must be loaded first (provides window.selectImageFromLibrary
 *     and window.selectMediaFromLibrary)
 *   - CKEditor 5 must be loaded on the page
 *
 * Skips editors that don't have image plugins (e.g. product_short config).
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    initCKEditorMediaIntegration();
  });

  /**
   * Open the media library filtered to images, insert selected image into editor.
   */
  function openImageLibrary(editorInstance) {
    if (typeof window.selectImageFromLibrary !== 'function') {
      AdminModal.alert({
        message: 'Media library is not available. Please reload the page.',
        type: 'error',
      });
      return;
    }
    window.selectImageFromLibrary(function (media) {
      if (media && media.url) {
        editorInstance.execute('insertImage', { source: media.url });
        editorInstance.editing.view.focus();
      }
    });
  }

  /**
   * Open the media library filtered to video, insert selected video into editor.
   */
  function openVideoLibrary(editorInstance) {
    if (typeof window.selectMediaFromLibrary !== 'function') {
      AdminModal.alert({
        message: 'Media library is not available. Please reload the page.',
        type: 'error',
      });
      return;
    }
    window.selectMediaFromLibrary(
      function (media) {
        if (!media || !media.url) return;

        const mime = media.mime_type || 'video/mp4';
        const videoHtml =
          '<figure class="media-video">' +
          '<video controls preload="metadata">' +
          '<source src="' +
          media.url +
          '" type="' +
          mime +
          '">' +
          '</video>' +
          '</figure>';

        insertRawHtml(editorInstance, videoHtml);
        editorInstance.editing.view.focus();
      },
      { fileTypeFilter: 'video' }
    );
  }

  /**
   * Prompt for an external video URL (YouTube, Vimeo, etc.) and embed it
   * via CKEditor's built-in mediaEmbed command.
   */
  async function insertExternalVideo(editorInstance) {
    let url = await AdminModal.prompt('Enter a video URL (YouTube, Vimeo, etc.):');
    if (!url || !url.trim()) return;
    url = url.trim();

    // Use CKEditor's built-in mediaEmbed command
    editorInstance.execute('mediaEmbed', url);
    editorInstance.editing.view.focus();

    // Show info notice about preview limitations
    showEmbedNotice(editorInstance);
  }

  /**
   * Show a transient notice near the editor explaining that embedded video
   * previews may not render in the editor but will work on the storefront.
   */
  function showEmbedNotice(editorInstance) {
    const editable = editorInstance.ui.getEditableElement();
    if (!editable) return;
    const ckEditor = editable.closest('.ck-editor');
    if (!ckEditor) return;

    // Don't stack multiple notices
    const existing = ckEditor.parentNode.querySelector('.ck-embed-notice');
    if (existing) existing.remove();

    const notice = document.createElement('div');
    notice.className = 'ck-embed-notice';
    notice.innerHTML =
      '<i class="fas fa-info-circle"></i> ' +
      'Video previews may not display in the editor due to security restrictions. ' +
      'The video will render correctly on your storefront.';

    ckEditor.parentNode.insertBefore(notice, ckEditor.nextSibling);

    // Auto-dismiss after 8 seconds
    setTimeout(function () {
      if (notice.parentNode) {
        notice.classList.add('ck-embed-notice--fade');
        setTimeout(function () {
          notice.remove();
        }, 300);
      }
    }, 8000);
  }

  /**
   * Insert raw HTML into CKEditor using the clipboard pipeline.
   */
  function insertRawHtml(editorInstance, html) {
    const data = editorInstance.data;
    const viewFragment = data.processor.toView(html);
    const modelFragment = data.toModel(viewFragment);
    editorInstance.model.insertContent(modelFragment);
  }

  /**
   * Poll for CKEditor instances and bind media library integration.
   */
  function initCKEditorMediaIntegration() {
    var checkInterval = setInterval(function () {
      const editables = document.querySelectorAll('.ck-editor__editable');
      if (editables.length === 0) return;

      let allReady = true;
      editables.forEach(function (editable) {
        if (!editable.ckeditorInstance) allReady = false;
      });
      if (!allReady) return;

      clearInterval(checkInterval);

      editables.forEach(function (editable) {
        const editorInstance = editable.ckeditorInstance;
        if (!editorInstance) return;

        const ckEditor = editable.closest('.ck-editor');
        if (!ckEditor) return;

        // Skip if already processed
        if (ckEditor.dataset.mediaLibraryBound) return;
        ckEditor.dataset.mediaLibraryBound = 'true';

        // Detect rich editor by checking for image upload button in toolbar
        // product_short config removes image plugins, so no .ck-file-dialog-button
        const isRichEditor =
          !!ckEditor.querySelector('.ck-file-dialog-button') ||
          editorInstance.plugins.has('ImageInsert');

        // Skip text-only editors (e.g. product_short)
        if (!isRichEditor) return;

        // Actions container
        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'ck-media-actions';

        // 1. Replace the toolbar file dialog button with media library
        replaceImageButton(ckEditor, editorInstance);

        // 2. "Browse Media Library" action button
        const browseBtn = document.createElement('button');
        browseBtn.type = 'button';
        browseBtn.className = 'ck-media-action-btn ck-media-browse-btn';
        browseBtn.innerHTML = '<i class="fas fa-images"></i> Browse Media Library';
        browseBtn.title = 'Insert image from Media Library';
        browseBtn.addEventListener('click', function () {
          openImageLibrary(editorInstance);
        });
        actionsContainer.appendChild(browseBtn);

        // 3. "Insert Video" action button
        const hasMediaEmbed = editorInstance.plugins.has('MediaEmbed');
        const videoBtn = document.createElement('button');
        videoBtn.type = 'button';
        videoBtn.className = 'ck-media-action-btn ck-video-insert-btn';
        videoBtn.innerHTML = '<i class="fas fa-video"></i> Insert Video';
        videoBtn.title = 'Insert video from Media Library or external URL';
        videoBtn.addEventListener('click', function () {
          showVideoMenu(videoBtn, editorInstance, hasMediaEmbed);
        });
        actionsContainer.appendChild(videoBtn);

        if (actionsContainer.children.length > 0) {
          ckEditor.parentNode.insertBefore(actionsContainer, ckEditor.nextSibling);
        }
      });
    }, 500);

    // Stop polling after 15 seconds
    setTimeout(function () {
      clearInterval(checkInterval);
    }, 15000);
  }

  /**
   * Replace CKEditor's native file dialog button with media library opener.
   * Uses cloneNode to strip CKEditor's internal event listeners.
   */
  function replaceImageButton(ckEditor, editorInstance) {
    const fileDialogBtn = ckEditor.querySelector('.ck-file-dialog-button');
    if (!fileDialogBtn) return;

    // Clone the button to strip all CKEditor event listeners
    const newBtn = fileDialogBtn.cloneNode(true);
    newBtn.dataset.mediaLibraryBound = 'true';
    newBtn.setAttribute('data-cke-tooltip-text', 'Insert image from Media Library');

    // Remove hidden file input that CKEditor uses for native dialog
    const fileInput = fileDialogBtn.parentElement.querySelector('input[type="file"]');
    if (fileInput) fileInput.remove();

    fileDialogBtn.parentNode.replaceChild(newBtn, fileDialogBtn);

    newBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      openImageLibrary(editorInstance);
    });
  }

  /**
   * Show a small dropdown menu for video insertion options.
   */
  function showVideoMenu(anchorBtn, editorInstance, hasMediaEmbed) {
    // Remove any existing menu
    const existing = document.querySelector('.ck-video-menu');
    if (existing) {
      existing.remove();
      return;
    }

    const menu = document.createElement('div');
    menu.className = 'ck-video-menu';

    // Option 1: From Media Library
    const libOption = document.createElement('button');
    libOption.type = 'button';
    libOption.className = 'ck-video-menu__item';
    libOption.innerHTML = '<i class="fas fa-photo-video"></i> From Media Library';
    libOption.addEventListener('click', function () {
      menu.remove();
      openVideoLibrary(editorInstance);
    });
    menu.appendChild(libOption);

    // Option 2: External URL (YouTube, Vimeo, etc.)
    if (hasMediaEmbed) {
      const extOption = document.createElement('button');
      extOption.type = 'button';
      extOption.className = 'ck-video-menu__item';
      extOption.innerHTML = '<i class="fab fa-youtube"></i> External URL (YouTube, Vimeo)';
      extOption.addEventListener('click', function () {
        menu.remove();
        insertExternalVideo(editorInstance);
      });
      menu.appendChild(extOption);
    }

    // Position below the button
    anchorBtn.style.position = 'relative';
    anchorBtn.appendChild(menu);

    // Close on outside click
    function closeMenu(e) {
      if (!menu.contains(e.target) && e.target !== anchorBtn) {
        menu.remove();
        document.removeEventListener('click', closeMenu, true);
      }
    }
    setTimeout(function () {
      document.addEventListener('click', closeMenu, true);
    }, 0);
  }
})();
