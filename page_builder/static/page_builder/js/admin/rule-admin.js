/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    function toggleStatus(url, activate) {
        fetch(url, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            },
            body: JSON.stringify({ is_active: activate })
        })
        .then(function (response) { return response.json(); })
        .then(function (data) {
            if (data.success) {
                if (typeof applyFilters === 'function') {
                    applyFilters();
                } else {
                    window.location.reload();
                }
            } else {
                AdminModal.alert({message: data.error || 'Error updating status.', type: 'error'});
            }
        })
        .catch(function (error) {
            console.error('Error toggling status:', error);
            AdminModal.alert({message: 'Error updating status. Please try again.', type: 'error'});
        });
    }

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-action="toggle-group-status"]');
        if (btn) {
            var pk = btn.dataset.pk;
            var activate = btn.dataset.activate === 'true';
            var pathParts = window.location.pathname.split('/');
            var langCode = pathParts[1];
            toggleStatus('/' + langCode + '/admin/page_builder/rulegroup/' + pk + '/toggle-status/', activate);
            return;
        }

        btn = e.target.closest('[data-action="toggle-rule-status"]');
        if (btn) {
            var pk = btn.dataset.pk;
            var activate = btn.dataset.activate === 'true';
            var pathParts = window.location.pathname.split('/');
            var langCode = pathParts[1];
            toggleStatus('/' + langCode + '/admin/page_builder/visibilityrule/' + pk + '/toggle-status/', activate);
        }
    });

}());
