/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    'use strict';

    document.addEventListener('change', function (e) {
        var el = e.target;
        if (el.dataset.action === 'filter-by-provider') {
            var url = new URL(window.location.href);
            var provider = el.value;
            if (provider) {
                url.searchParams.set('provider_key__exact', provider);
            } else {
                url.searchParams.delete('provider_key__exact');
            }
            window.location.href = url.toString();
        }
    });

}());
