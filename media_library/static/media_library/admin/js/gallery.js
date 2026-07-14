/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let translations = {};

  function init() {
    const dataEl = document.getElementById('media-gallery-data');
    if (dataEl) {
      try {
        const data = JSON.parse(dataEl.textContent);
        translations = data.translations || {};
      } catch (e) {}
    }

    showInfoBanner();

    window.mediaLibrary = new MediaLibrary({
      apiUrl: '/api/media/assets/',
      uploadUrl: '/api/media/assets/',
      selectionMode: 'multiple',
    });

    document.addEventListener('click', handleActions);
  }

  function showInfoBanner() {
    const banner = document.getElementById('mediaInfoBanner');
    const dismissed = localStorage.getItem('mediaInfoBannerDismissed');
    if (!dismissed && banner) {
      banner.classList.remove('hidden');
    }
  }

  function closeInfoBanner() {
    const banner = document.getElementById('mediaInfoBanner');
    if (banner) {
      banner.classList.add('hidden');
      localStorage.setItem('mediaInfoBannerDismissed', 'true');
    }
  }

  function handleActions(e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) {
      return;
    }

    const action = btn.dataset.action;

    if (action === 'close-info-banner') {
      closeInfoBanner();
      return;
    }

    const selectedItems = window.mediaLibrary ? window.mediaLibrary.getSelectedItems() : [];

    if (action === 'delete' || action === 'permanent-delete') {
      if (selectedItems.length === 0) {
        AdminModal.alert({
          message: translations.selectItemsToDelete || 'Please select items to delete',
          type: 'warning',
        });
        return;
      }
      const confirmMessage =
        action === 'permanent-delete'
          ? translations.confirmPermanentDelete ||
            'Are you sure you want to permanently delete the selected items? This cannot be undone!'
          : translations.confirmDelete || 'Are you sure you want to delete the selected items?';

      if (confirm(confirmMessage)) {
        var path = window.location.pathname;
        var langMatch = path.match(/^\/([a-z]{2})(?:-[a-z]{2})?\//);
        var lang = langMatch ? langMatch[1] : 'en';

        const apiEndpoint =
          action === 'permanent-delete'
            ? '/' + lang + '/media-library/api/assets/permanent_delete/'
            : '/' + lang + '/media-library/api/assets/bulk_operations/';

        const payload =
          action === 'permanent-delete'
            ? { asset_ids: selectedItems }
            : { asset_ids: selectedItems, action: 'delete' };

        fetch(apiEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': AdminUtils.getCsrfToken(),
          },
          body: JSON.stringify(payload),
        })
          .then(function (response) {
            return response.json();
          })
          .then(function (data) {
            if (data.message) {
              AdminModal.toast(data.message, 'success');
              window.mediaLibrary.clearSelection();
              window.mediaLibrary.loadMedia();
            } else if (data.error) {
              AdminModal.alert({
                message: (translations.error || 'Error:') + ' ' + data.error,
                type: 'error',
              });
            }
          })
          .catch(function (error) {
            AdminModal.alert({
              message: (translations.error || 'Error:') + ' ' + error,
              type: 'error',
            });
          });
      }
    } else if (action === 'restore') {
      if (selectedItems.length === 0) {
        AdminModal.alert({
          message: translations.selectItemsToRestore || 'Please select items to restore',
          type: 'warning',
        });
        return;
      }

      var path = window.location.pathname;
      var langMatch = path.match(/^\/([a-z]{2})(?:-[a-z]{2})?\//);
      var lang = langMatch ? langMatch[1] : 'en';

      fetch('/' + lang + '/media-library/api/assets/restore/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': AdminUtils.getCsrfToken(),
        },
        body: JSON.stringify({ asset_ids: selectedItems }),
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          if (data.message) {
            AdminModal.toast(data.message, 'success');
            window.mediaLibrary.clearSelection();
            window.mediaLibrary.loadMedia();
          } else if (data.error) {
            AdminModal.alert({
              message: (translations.error || 'Error:') + ' ' + data.error,
              type: 'error',
            });
          }
        })
        .catch(function (error) {
          AdminModal.alert({
            message: (translations.error || 'Error:') + ' ' + error,
            type: 'error',
          });
        });
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
