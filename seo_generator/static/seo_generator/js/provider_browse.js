/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * SEO Generator Provider Browse Page JavaScript
 * Handles install/update AJAX, filtering, and notifications.
 * Pattern follows exchange_rates/js/provider_browse.js.
 */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initInstallButtons();
        initUpdateButtons();
        initInfoCardCollapse();
    });

    function initInstallButtons() {
        document.querySelectorAll('.btn-install').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var slug = this.dataset.providerSlug;
                var name = this.dataset.providerName;
                installProvider(slug, name);
            });
        });
    }

    function initUpdateButtons() {
        document.querySelectorAll('.btn-update').forEach(function(btn) {
            btn.addEventListener('click', function() {
                var slug = this.dataset.slug;
                var version = this.dataset.version;
                updateProvider(slug, version);
            });
        });
    }

    function initInfoCardCollapse() {
        var toggleBtn = document.querySelector('.collapse-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function() {
                var body = document.getElementById('cardBody');
                var expanded = this.getAttribute('aria-expanded') === 'true';
                if (expanded) {
                    body.classList.add('d-none');
                    this.setAttribute('aria-expanded', 'false');
                } else {
                    body.classList.remove('d-none');
                    this.setAttribute('aria-expanded', 'true');
                }
            });
        }
    }

    function installProvider(slug, name) {
        var loading = document.getElementById('provider-install-loading');
        loading.style.display = 'flex';

        var csrfToken = (typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken)
            ? AdminUtils.getCsrfToken()
            : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

        fetch(AdminUtils.buildAdminUrl('/admin/seo-generator/providers/install/' + slug + '/'), {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(function(response) {
            // Handle gateway timeout or non-JSON responses (e.g. 504)
            var contentType = response.headers.get('content-type') || '';
            if (!contentType.includes('application/json')) {
                var loadingMsg = loading.querySelector('.loading-message');
                if (loadingMsg) loadingMsg.textContent = 'Installation is being processed. Refreshing...';
                setTimeout(function() { window.location.reload(); }, 3000);
                return null;
            }
            return response.json();
        })
        .then(function(data) {
            if (!data) return;
            loading.style.display = 'none';
            if (data.success) {
                showNotification(data.message, 'success');
                if (data.redirect_url) {
                    setTimeout(function() {
                        window.location.href = data.redirect_url;
                    }, 1500);
                }
            } else {
                showNotification(data.error || 'Installation failed.', 'error');
            }
        })
        .catch(function() {
            // Network error or JSON parse failure — install may still be completing
            var loadingMsg = loading.querySelector('.loading-message');
            if (loadingMsg) loadingMsg.textContent = 'Installation is being processed. Refreshing...';
            setTimeout(function() { window.location.reload(); }, 3000);
        });
    }

    function updateProvider(slug, version) {
        var loading = document.getElementById('provider-install-loading');
        var loadingMsg = loading.querySelector('.loading-message');
        if (loadingMsg) loadingMsg.textContent = 'Updating provider...';
        loading.style.display = 'flex';

        var csrfToken = (typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken)
            ? AdminUtils.getCsrfToken()
            : document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

        fetch(AdminUtils.buildAdminUrl('/admin/seo-generator/providers/update/' + slug + '/'), {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            }
        })
        .then(function(response) {
            // Handle gateway timeout or non-JSON responses (e.g. 504)
            var contentType = response.headers.get('content-type') || '';
            if (!contentType.includes('application/json')) {
                if (loadingMsg) loadingMsg.textContent = 'Update is being processed. Refreshing...';
                setTimeout(function() { window.location.reload(); }, 3000);
                return null;
            }
            return response.json();
        })
        .then(function(data) {
            if (!data) return;
            loading.style.display = 'none';
            if (data.success) {
                showNotification(data.message, 'success');
                if (data.redirect_url) {
                    setTimeout(function() {
                        window.location.href = data.redirect_url;
                    }, 1500);
                }
            } else {
                showNotification(data.error || 'Update failed.', 'error');
            }
        })
        .catch(function() {
            // Network error or JSON parse failure — update may still be completing
            if (loadingMsg) loadingMsg.textContent = 'Update is being processed. Refreshing...';
            setTimeout(function() { window.location.reload(); }, 3000);
        });
    }

    function showNotification(message, type) {
        AdminModal.toast(message, type || 'info');
    }

    function escapeHTML(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

})();
