/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initSaveButtons();
        initAutoDiscover();
    });

    /**
     * Header save buttons trigger the hidden submit row inputs.
     */
    function initSaveButtons() {
        var form = document.getElementById('ssoproviderconfig-form');
        if (!form) return;

        var saveContinueBtn = document.getElementById('save-continue-btn');
        if (saveContinueBtn) {
            saveContinueBtn.addEventListener('click', function() {
                var input = document.createElement('input');
                input.type = 'hidden';
                input.name = '_continue';
                input.value = '1';
                form.appendChild(input);
                form.submit();
            });
        }

        var saveBtn = document.getElementById('save-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', function() {
                form.submit();
            });
        }
    }

    /**
     * Auto-Discover: fetch OIDC discovery document and populate endpoint fields.
     */
    function initAutoDiscover() {
        var discoverBtn = document.getElementById('btn-auto-discover');
        if (!discoverBtn) return;

        var discoverUrl = discoverBtn.getAttribute('data-discover-url');

        discoverBtn.addEventListener('click', function() {
            var discoveryField = document.getElementById('id_oidc_discovery_url');
            if (!discoveryField) return;

            var url = discoveryField.value.trim();
            if (!url) {
                showDiscoverResult('error', discoverBtn.getAttribute('data-msg-empty'));
                return;
            }

            // Disable button and show loading state
            discoverBtn.disabled = true;
            var originalHTML = discoverBtn.innerHTML;
            discoverBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' +
                discoverBtn.getAttribute('data-msg-discovering');

            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            if (!csrfToken) return;

            fetch(discoverUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken.value
                },
                body: JSON.stringify({ discovery_url: url })
            })
            .then(function(resp) { return resp.json(); })
            .then(function(data) {
                if (data.error) {
                    showDiscoverResult('error',
                        discoverBtn.getAttribute('data-msg-failed') + ' ' + data.error);
                    return;
                }

                // Switch to Advanced tab to show populated fields
                if (typeof AdminTabs !== 'undefined') {
                    AdminTabs.switchTo('advanced');
                }

                // Populate endpoint fields with flash animation
                var fieldMap = {
                    'id_oidc_authorization_endpoint': data.authorization_endpoint,
                    'id_oidc_token_endpoint': data.token_endpoint,
                    'id_oidc_userinfo_endpoint': data.userinfo_endpoint,
                    'id_oidc_jwks_endpoint': data.jwks_uri,
                    'id_oidc_end_session_endpoint': data.end_session_endpoint
                };

                var populated = 0;
                for (var fieldId in fieldMap) {
                    var field = document.getElementById(fieldId);
                    if (field && fieldMap[fieldId]) {
                        field.value = fieldMap[fieldId];
                        field.classList.add('field-discovered');
                        populated++;
                        // Remove flash class after animation
                        (function(f) {
                            setTimeout(function() {
                                f.classList.remove('field-discovered');
                            }, 2000);
                        })(field);
                    }
                }

                var issuer = data.issuer ? ' (Issuer: ' + data.issuer + ')' : '';
                showDiscoverResult('success',
                    discoverBtn.getAttribute('data-msg-success') + ' ' +
                    populated + ' ' +
                    discoverBtn.getAttribute('data-msg-endpoints') + issuer);
            })
            .catch(function(err) {
                showDiscoverResult('error',
                    discoverBtn.getAttribute('data-msg-request-failed') + ' ' + err.message);
            })
            .finally(function() {
                discoverBtn.disabled = false;
                discoverBtn.innerHTML = originalHTML;
            });
        });
    }

    /**
     * Show a brief notification for discover results.
     */
    function showDiscoverResult(type, message) {
        // Remove any existing notification
        var existing = document.querySelector('.sso-discover-notification');
        if (existing) existing.remove();

        var notification = document.createElement('div');
        notification.className = 'sso-discover-notification';
        notification.setAttribute('role', 'alert');

        var icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-triangle';
        var color = type === 'success' ? 'var(--success-fg)' : 'var(--error-fg)';

        notification.innerHTML = '<i class="fas ' + icon + '"></i> ' + message;
        notification.style.cssText =
            'position: fixed; top: 20px; right: 20px; z-index: 9999; ' +
            'padding: 14px 20px; border-radius: 8px; font-size: 14px; ' +
            'color: #fff; display: flex; align-items: center; gap: 8px; ' +
            'max-width: 500px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); ' +
            'background: ' + color + '; transition: opacity 0.3s ease;';

        document.body.appendChild(notification);

        // Auto-remove after 4 seconds
        setTimeout(function() {
            notification.style.opacity = '0';
            setTimeout(function() { notification.remove(); }, 300);
        }, 4000);
    }
})();
