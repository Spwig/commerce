/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var translations = {};

    function init() {
        var dataEl = document.getElementById('media-gallery-data');
        if (dataEl) {
            try {
                var data = JSON.parse(dataEl.textContent);
                translations = data.translations || {};
            } catch (e) {}
        }

        showInfoBanner();

        window.mediaLibrary = new MediaLibrary({
            apiUrl: '/api/media/assets/',
            uploadUrl: '/api/media/assets/',
            selectionMode: 'multiple'
        });

        document.addEventListener('click', handleActions);
    }

    function showInfoBanner() {
        var banner = document.getElementById('mediaInfoBanner');
        var dismissed = localStorage.getItem('mediaInfoBannerDismissed');
        if (!dismissed && banner) {
            banner.classList.remove('hidden');
        }
    }

    function closeInfoBanner() {
        var banner = document.getElementById('mediaInfoBanner');
        if (banner) {
            banner.classList.add('hidden');
            localStorage.setItem('mediaInfoBannerDismissed', 'true');
        }
    }

    function handleActions(e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) { return; }

        var action = btn.dataset.action;

        if (action === 'close-info-banner') {
            closeInfoBanner();
            return;
        }

        var selectedItems = window.mediaLibrary ? window.mediaLibrary.getSelectedItems() : [];

        if (action === 'delete' || action === 'permanent-delete') {
            if (selectedItems.length === 0) {
                AdminModal.alert({message: translations.selectItemsToDelete || 'Please select items to delete', type: 'warning'});
                return;
            }
            var confirmMessage = action === 'permanent-delete'
                ? (translations.confirmPermanentDelete || 'Are you sure you want to permanently delete the selected items? This cannot be undone!')
                : (translations.confirmDelete || 'Are you sure you want to delete the selected items?');

            if (confirm(confirmMessage)) {
                var path = window.location.pathname;
                var langMatch = path.match(/^\/([a-z]{2})(?:-[a-z]{2})?\//);
                var lang = langMatch ? langMatch[1] : 'en';

                var apiEndpoint = action === 'permanent-delete'
                    ? '/' + lang + '/media-library/api/assets/permanent_delete/'
                    : '/' + lang + '/media-library/api/assets/bulk_operations/';

                var payload = action === 'permanent-delete'
                    ? { asset_ids: selectedItems }
                    : { asset_ids: selectedItems, action: 'delete' };

                fetch(apiEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': AdminUtils.getCsrfToken()
                    },
                    body: JSON.stringify(payload)
                })
                    .then(function (response) { return response.json(); })
                    .then(function (data) {
                        if (data.message) {
                            AdminModal.toast(data.message, 'success');
                            window.mediaLibrary.clearSelection();
                            window.mediaLibrary.loadMedia();
                        } else if (data.error) {
                            AdminModal.alert({message: (translations.error || 'Error:') + ' ' + data.error, type: 'error'});
                        }
                    })
                    .catch(function (error) {
                        AdminModal.alert({message: (translations.error || 'Error:') + ' ' + error, type: 'error'});
                    });
            }
        } else if (action === 'restore') {
            if (selectedItems.length === 0) {
                AdminModal.alert({message: translations.selectItemsToRestore || 'Please select items to restore', type: 'warning'});
                return;
            }

            var path = window.location.pathname;
            var langMatch = path.match(/^\/([a-z]{2})(?:-[a-z]{2})?\//);
            var lang = langMatch ? langMatch[1] : 'en';

            fetch('/' + lang + '/media-library/api/assets/restore/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': AdminUtils.getCsrfToken()
                },
                body: JSON.stringify({ asset_ids: selectedItems })
            })
                .then(function (response) { return response.json(); })
                .then(function (data) {
                    if (data.message) {
                        AdminModal.toast(data.message, 'success');
                        window.mediaLibrary.clearSelection();
                        window.mediaLibrary.loadMedia();
                    } else if (data.error) {
                        AdminModal.alert({message: (translations.error || 'Error:') + ' ' + data.error, type: 'error'});
                    }
                })
                .catch(function (error) {
                    AdminModal.alert({message: (translations.error || 'Error:') + ' ' + error, type: 'error'});
                });
        }
    }

    document.addEventListener('DOMContentLoaded', init);
}());
