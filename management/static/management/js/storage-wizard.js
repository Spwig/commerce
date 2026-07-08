/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
    'use strict';

    /* Translations loaded from a <script type="application/json"> block */
    var T = {};

    /* S3-compatible presets: maps preset value -> endpoint URL template */
    var S3_PRESETS = {
        backblaze_b2:        { endpoint: 'https://s3.{region}.backblazeb2.com', region: 'us-west-004' },
        wasabi:              { endpoint: 'https://s3.{region}.wasabisys.com', region: 'us-east-1' },
        digitalocean_spaces: { endpoint: 'https://{region}.digitaloceanspaces.com', region: 'nyc3' },
        cloudflare_r2:       { endpoint: 'https://{account_id}.r2.cloudflarestorage.com', region: 'auto' },
        vultr:               { endpoint: 'https://{region}.vultrobjects.com', region: 'ewr1' },
        minio:               { endpoint: '', region: 'us-east-1' },
    };

    function init() {
        /* Load translations */
        var tEl = document.getElementById('storage-wizard-translations');
        if (tEl) {
            try { T = JSON.parse(tEl.textContent); } catch (e) { /* noop */ }
        }

        setupPresetSelector();
        setupPasswordToggles();
        setupTestConnection();
        setupCopyRedirectUri();
    }

    /* ── Preset auto-fill (S3 provider) ─────────────────────────── */

    function setupPresetSelector() {
        var presetSelect = document.getElementById('setting_preset');
        if (!presetSelect) return;

        presetSelect.addEventListener('change', function () {
            var preset = S3_PRESETS[this.value];
            if (!preset) return;

            var endpointInput = document.getElementById('setting_endpoint_url');
            var regionInput = document.getElementById('setting_region');

            if (endpointInput && preset.endpoint) {
                /* Fill endpoint - user will replace {region} or {account_id} */
                var region = regionInput ? regionInput.value : preset.region;
                endpointInput.value = preset.endpoint.replace('{region}', region);
            }
            if (regionInput && preset.region) {
                regionInput.value = preset.region;
            }
        });
    }

    /* ── Password visibility toggles ────────────────────────────── */

    function setupPasswordToggles() {
        document.querySelectorAll('.password-toggle').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var target = document.getElementById(this.dataset.target);
                if (!target) return;
                var icon = this.querySelector('i');
                if (target.type === 'password') {
                    target.type = 'text';
                    icon.className = 'fas fa-eye-slash';
                } else {
                    target.type = 'password';
                    icon.className = 'fas fa-eye';
                }
            });
        });
    }

    /* ── Test Connection (AJAX) ──────────────────────────────────── */

    function setupTestConnection() {
        var btn = document.getElementById('btn-test-connection');
        if (!btn) return;

        btn.addEventListener('click', function () {
            var container = document.querySelector('.wizard-container');
            var testUrl = container ? container.dataset.testUrl : '';
            var providerType = container ? container.dataset.providerType : '';
            if (!testUrl) return;

            /* Gather credential and setting values from the form */
            var credentials = {};
            document.querySelectorAll('[name^="cred_"]').forEach(function (el) {
                var key = el.name.replace('cred_', '');
                credentials[key] = el.value;
            });

            var settings = {};
            document.querySelectorAll('[name^="setting_"]').forEach(function (el) {
                var key = el.name.replace('setting_', '');
                settings[key] = el.value;
            });

            /* Show loading state */
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + (T.testing || 'Testing connection...');

            var resultsDiv = document.getElementById('test-results');
            resultsDiv.style.display = 'none';

            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');

            fetch(testUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken ? csrfToken.value : '',
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    provider_type: providerType,
                    credentials: credentials,
                    settings: settings,
                }),
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-plug"></i> ' + 'Test Connection';

                resultsDiv.style.display = 'block';

                if (data.success) {
                    resultsDiv.className = 'test-results success';
                    resultsDiv.innerHTML =
                        '<div class="test-result-icon"><i class="fas fa-check-circle"></i></div>' +
                        '<h3>' + (T.testSuccess || 'Connection successful!') + '</h3>' +
                        '<p>' + escapeHtml(data.message) + '</p>';

                    if (data.details) {
                        var detailsHtml = '<div class="test-details"><h4>Details</h4><dl>';
                        for (var key in data.details) {
                            if (data.details.hasOwnProperty(key)) {
                                detailsHtml += '<dt>' + escapeHtml(key) + '</dt><dd>' + escapeHtml(String(data.details[key])) + '</dd>';
                            }
                        }
                        detailsHtml += '</dl></div>';
                        resultsDiv.innerHTML += detailsHtml;
                    }
                } else {
                    resultsDiv.className = 'test-results error';
                    resultsDiv.innerHTML =
                        '<div class="test-result-icon"><i class="fas fa-times-circle"></i></div>' +
                        '<h3>' + (T.testFailed || 'Connection failed') + '</h3>' +
                        '<p>' + escapeHtml(data.message) + '</p>';
                }
            })
            .catch(function () {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-plug"></i> ' + 'Test Connection';
                resultsDiv.style.display = 'block';
                resultsDiv.className = 'test-results error';
                resultsDiv.innerHTML =
                    '<div class="test-result-icon"><i class="fas fa-times-circle"></i></div>' +
                    '<h3>' + (T.networkError || 'Network error. Please try again.') + '</h3>';
            });
        });
    }

    /* ── Copy Redirect URI (OAuth providers) ──────────────────── */

    function setupCopyRedirectUri() {
        var btn = document.getElementById('btn-copy-redirect-uri');
        if (!btn) return;

        btn.addEventListener('click', function () {
            var input = document.getElementById('oauth-redirect-uri');
            if (!input) return;

            navigator.clipboard.writeText(input.value).then(function () {
                var icon = btn.querySelector('i');
                icon.className = 'fas fa-check';
                setTimeout(function () { icon.className = 'fas fa-copy'; }, 2000);
            });
        });
    }

    function escapeHtml(text) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }

    document.addEventListener('DOMContentLoaded', init);
})();
