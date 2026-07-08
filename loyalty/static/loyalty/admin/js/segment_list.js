/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var translations = {};

    function init() {
        var tEl = document.getElementById('segment-list-translations');
        if (tEl) {
            try { translations = JSON.parse(tEl.textContent); } catch (e) {}
        }
        document.addEventListener('click', handleActions);
    }

    function handleActions(e) {
        var btn = e.target.closest('[data-action="refresh-segment"]');
        if (!btn) return;
        e.preventDefault();
        refreshSegment(btn.dataset.pk);
    }

    async function refreshSegment(segmentId) {
        var confirmMsg = translations.confirmRefresh ||
            'Are you sure you want to refresh the segment membership? This may take a moment for large segments.';

        if (!await AdminModal.confirm(confirmMsg)) { return; }

        var lang = document.documentElement.lang || 'en';
        var url = '/' + lang + '/admin/loyalty/segments/' + segmentId + '/refresh/';
        var csrf = document.querySelector('[name=csrfmiddlewaretoken]');

        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrf ? csrf.value : ''
            }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                AdminModal.toast(translations.refreshQueued ||
                    'Segment refresh has been queued. The member count will be updated shortly.', 'success');
                location.reload();
            } else {
                AdminModal.alert({message: data.error || translations.errorRefresh ||
                    'An error occurred while refreshing the segment.', type: 'error'});
            }
        })
        .catch(function () {
            AdminModal.alert({message: translations.errorRefresh ||
                'An error occurred while refreshing the segment.', type: 'error'});
        });
    }

    document.addEventListener('DOMContentLoaded', init);
}());
