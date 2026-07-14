/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  // Prevent double initialization if script is loaded multiple times
  if (window._mlSelectWidgetLoaded) return;
  window._mlSelectWidgetLoaded = true;

  // Read translations from data island (shared across all widget instances on the page)
  function getTranslations() {
    const i18nEl = document.querySelector('.media-widget-i18n');
    return i18nEl ? JSON.parse(i18nEl.textContent) : {};
  }

  const initialized = [];

  function initWidget(widget) {
    if (initialized.indexOf(widget) !== -1) return;
    initialized.push(widget);

    const i18n = getTranslations();
    const tSaved = i18n.saved || 'Saved';
    const tNoImage = i18n.noImage || 'No Image Selected, Drop Here';
    const tUploading = i18n.uploading || 'Uploading...';
    const tUploadFailed = i18n.uploadFailed || 'Upload failed';
    const tClear = i18n.clear || 'Clear';
    const tDropImage = i18n.dropImage || 'Please drop an image file';

    const selectBtn = widget.querySelector('.media-select-btn');
    const clearBtn = widget.querySelector('.media-clear-btn');
    const hiddenInput = widget.querySelector('.media-field-input');
    const preview = widget.querySelector('.media-preview');

    const autoSaveUrl = widget.dataset.autoSaveUrl;
    const autoSaveApp = widget.dataset.autoSaveApp;
    const autoSaveModel = widget.dataset.autoSaveModel;
    const autoSavePk = widget.dataset.autoSavePk;
    const autoSaveField = widget.dataset.autoSaveField;

    function autoSaveMediaField(assetId) {
      if (!autoSaveUrl || !autoSaveApp || !autoSaveModel || !autoSavePk || !autoSaveField) return;
      const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
      const csrfToken = csrfInput ? csrfInput.value : '';
      if (!csrfToken) {
        console.error('Auto-save: CSRF token not found');
        return;
      }

      fetch(autoSaveUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
        body: JSON.stringify({
          app_label: autoSaveApp,
          model_name: autoSaveModel,
          pk: autoSavePk,
          field: autoSaveField,
          asset_id: assetId || null,
        }),
      })
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          if (data.success) {
            showAutoSaveNotification();
          } else {
            console.error('Auto-save failed:', data.error);
          }
        })
        .catch(function (e) {
          console.error('Auto-save error:', e);
        });
    }

    function showAutoSaveNotification() {
      let notification = widget.querySelector('.auto-save-notification');
      if (!notification) {
        notification = document.createElement('span');
        notification.className = 'auto-save-notification';
        notification.style.cssText =
          'display:inline-block;margin-left:10px;color:var(--success-fg,#28a745);font-size:12px;opacity:0;transition:opacity 0.3s;';
        widget.querySelector('.media-controls').appendChild(notification);
      }
      notification.textContent = tSaved + ' \u2713';
      notification.style.opacity = '1';
      setTimeout(function () {
        notification.style.opacity = '0';
      }, 2000);
    }

    function makeNoImagePreview() {
      return (
        '<div class="no-image-preview drop-zone" style="width:150px;height:150px;border:2px dashed var(--border-color);display:flex;align-items:center;justify-content:center;color:var(--body-quiet-color);border-radius:4px;text-align:center;cursor:pointer;transition:all 0.2s ease;"><span>' +
        tNoImage +
        '</span></div>'
      );
    }

    function updatePreview(imageUrl) {
      if (imageUrl) {
        preview.innerHTML =
          '<img src="' +
          imageUrl +
          '" alt="Selected image" class="preview-image" style="max-width:150px;max-height:150px;object-fit:cover;border:1px solid var(--border-color);border-radius:4px;">';
        if (!widget.querySelector('.media-clear-btn')) {
          const newClearBtn = document.createElement('button');
          newClearBtn.type = 'button';
          newClearBtn.className = 'media-clear-btn';
          newClearBtn.style.cssText =
            'background:var(--delete-button-bg);color:#fff;border:none;padding:8px 15px;border-radius:4px;cursor:pointer;margin-left:10px;';
          newClearBtn.innerHTML = '\u2715 ' + tClear;
          newClearBtn.addEventListener('click', function () {
            hiddenInput.value = '';
            updatePreview(null);
            autoSaveMediaField(null);
          });
          widget.querySelector('.media-controls').appendChild(newClearBtn);
        }
      } else {
        preview.innerHTML = makeNoImagePreview();
        const cb = widget.querySelector('.media-clear-btn');
        if (cb) cb.remove();
        attachDragDropHandlers();
      }
    }

    function uploadFile(file) {
      preview.innerHTML =
        '<div class="no-image-preview" style="width:150px;height:150px;border:2px dashed var(--border-color);display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--body-quiet-color);border-radius:4px;text-align:center;"><i class="fas fa-spinner fa-spin" style="font-size:24px;margin-bottom:10px;"></i><span>' +
        tUploading +
        '</span></div>';
      const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
      const csrfToken = csrfInput ? csrfInput.value : '';
      if (!csrfToken) {
        console.error('CSRF token not found');
        return;
      }
      const formData = new FormData();
      formData.append('original_file', file);
      formData.append('title', file.name.split('.')[0]);
      const apiUrl = '/api/media/assets/';
      fetch(apiUrl, { method: 'POST', headers: { 'X-CSRFToken': csrfToken }, body: formData })
        .then(function (r) {
          if (!r.ok) {
            return r
              .json()
              .catch(function () {
                return {};
              })
              .then(function (e) {
                throw new Error(e.detail || e.error || 'Upload failed');
              });
          }
          return r.json();
        })
        .then(function (data) {
          if (!data.id) throw new Error('No media asset ID returned');
          const imgUrl = data.thumbnail_url || data.display_url;
          hiddenInput.value = data.id;
          updatePreview(imgUrl);
          autoSaveMediaField(data.id);
          notifyChange(data.id, imgUrl);
        })
        .catch(function (error) {
          console.error('Upload error:', error);
          preview.innerHTML =
            '<div class="no-image-preview" style="width:150px;height:150px;border:2px dashed var(--delete-button-bg);display:flex;flex-direction:column;align-items:center;justify-content:center;color:var(--delete-button-bg);border-radius:4px;text-align:center;"><i class="fas fa-exclamation-triangle" style="font-size:24px;margin-bottom:10px;"></i><span style="font-size:12px;">' +
            tUploadFailed +
            '</span></div>';
          setTimeout(function () {
            updatePreview(null);
          }, 2000);
        });
    }

    function notifyChange(assetId, imageUrl) {
      widget.dispatchEvent(
        new CustomEvent('media-widget-change', {
          bubbles: true,
          detail: { fieldName: hiddenInput.name, assetId: assetId, imageUrl: imageUrl },
        })
      );
    }

    function attachDragDropHandlers() {
      const dropZone = preview.querySelector('.drop-zone');
      if (!dropZone) return;

      ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(function (ev) {
        dropZone.addEventListener(
          ev,
          function (e) {
            e.preventDefault();
            e.stopPropagation();
          },
          false
        );
      });

      ['dragenter', 'dragover'].forEach(function (ev) {
        dropZone.addEventListener(
          ev,
          function (e) {
            if (e.dataTransfer.types.includes('Files')) {
              dropZone.style.borderColor = 'var(--primary)';
              dropZone.style.backgroundColor = 'var(--darkened-bg)';
            }
          },
          false
        );
      });

      ['dragleave', 'drop'].forEach(function (ev) {
        dropZone.addEventListener(
          ev,
          function () {
            dropZone.style.borderColor = 'var(--border-color)';
            dropZone.style.backgroundColor = 'transparent';
          },
          false
        );
      });

      dropZone.addEventListener(
        'drop',
        function (e) {
          const files = e.dataTransfer.files;
          if (files && files.length > 0) {
            const file = files[0];
            if (!file.type.startsWith('image/')) {
              AdminModal.alert({ message: tDropImage, type: 'warning' });
              return;
            }
            uploadFile(file);
          }
        },
        false
      );
    }

    if (selectBtn) {
      selectBtn.addEventListener('click', function () {
        window.selectImageFromLibrary(function (selectedMedia) {
          if (selectedMedia) {
            const imgUrl = selectedMedia.thumbnail_url || selectedMedia.url;
            hiddenInput.value = selectedMedia.id;
            updatePreview(imgUrl);
            autoSaveMediaField(selectedMedia.id);
            notifyChange(selectedMedia.id, imgUrl);
          }
        });
      });
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        hiddenInput.value = '';
        updatePreview(null);
        autoSaveMediaField(null);
        notifyChange(null, null);
      });
    }

    attachDragDropHandlers();
  }

  function initAll() {
    document.querySelectorAll('.media-library-widget').forEach(initWidget);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
