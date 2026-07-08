/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Domain & SSL Configuration Wizard
 * AJAX-driven wizard within the Site Settings admin tab.
 * Handles DNS validation, configuration dispatch, and progress polling.
 *
 * Reads configuration from a JSON data island (#domain-ssl-config-data)
 * and uses AdminUtils for CSRF and fetch helpers.
 */
(function() {
    'use strict';

    var config = null;
    var t = {};
    var pollTimer = null;
    var configuredDomain = '';
    var configuredSslMode = '';
    var pollErrorCount = 0;

    // Status → progress percentage mapping
    var STATUS_PROGRESS = {
        idle: 100,
        validating_dns: 15,
        configuring: 35,
        obtaining_cert: 60,
        reloading: 85,
        error: 100
    };

    function init() {
        var dataEl = document.getElementById('domain-ssl-config-data');
        if (!dataEl) return;

        try {
            config = JSON.parse(dataEl.textContent);
            t = config.translations || {};
        } catch (e) {
            return;
        }

        // Populate current values from data attributes
        var domainInput = document.getElementById('domain-ssl-domain');
        if (domainInput) {
            if (domainInput.dataset.currentDomain) {
                domainInput.value = domainInput.dataset.currentDomain;
            } else if (domainInput.dataset.siteUrl) {
                // Fallback: extract hostname from site_url (set in setup wizard)
                try {
                    var hostname = new URL(domainInput.dataset.siteUrl).hostname;
                    if (hostname && hostname !== 'localhost' && hostname !== '127.0.0.1' &&
                        hostname !== 'example.com' && !/^\d+\.\d+\.\d+\.\d+$/.test(hostname)) {
                        domainInput.value = hostname;
                    }
                } catch (e) { /* invalid URL, skip */ }
            }
        }

        var emailInput = document.getElementById('domain-ssl-email');
        if (emailInput && emailInput.dataset.currentEmail) {
            emailInput.value = emailInput.dataset.currentEmail;
        }

        // Bind events
        bindEvents();

        // Load current status
        loadStatus();
    }

    function bindEvents() {
        // DNS check button
        var dnsBtn = document.getElementById('domain-ssl-check-dns');
        if (dnsBtn) {
            dnsBtn.addEventListener('click', checkDns);
        }

        // SSL mode radio cards
        var modeCards = document.querySelectorAll('.domain-ssl-mode-card');
        modeCards.forEach(function(card) {
            card.addEventListener('click', function() {
                var radio = card.querySelector('input[type="radio"]');
                if (radio) {
                    radio.checked = true;
                    onModeChange(radio.value);
                }
            });
        });

        // Also listen for radio change directly
        var radios = document.querySelectorAll('input[name="domain-ssl-mode"]');
        radios.forEach(function(radio) {
            radio.addEventListener('change', function() {
                onModeChange(this.value);
            });
        });

        // Configure button
        var configBtn = document.getElementById('domain-ssl-configure');
        if (configBtn) {
            configBtn.addEventListener('click', startConfiguration);
        }
    }

    function onModeChange(mode) {
        // Update card selection visually
        document.querySelectorAll('.domain-ssl-mode-card').forEach(function(card) {
            card.classList.toggle('selected', card.dataset.mode === mode);
        });

        // Show/hide conditional steps (supports comma-separated modes)
        document.querySelectorAll('.domain-ssl-conditional').forEach(function(el) {
            var showFor = el.dataset.showFor;
            var modes = showFor ? showFor.split(',') : [];
            el.classList.toggle('visible', modes.indexOf(mode) !== -1);
        });
    }

    function getCSRFToken() {
        if (window.AdminUtils && AdminUtils.getCsrfToken) {
            return AdminUtils.getCsrfToken();
        }
        // Fallback
        var cookie = document.cookie.split(';').find(function(c) {
            return c.trim().startsWith('csrftoken=');
        });
        return cookie ? cookie.split('=')[1] : '';
    }

    function fetchJSON(url, options) {
        options = options || {};
        var headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
        };

        return fetch(url, {
            method: options.method || 'GET',
            headers: headers,
            body: options.body ? JSON.stringify(options.body) : undefined,
            credentials: 'same-origin'
        }).then(function(resp) {
            return resp.json();
        });
    }

    // ── Load Status ─────────────────────────────────────

    function loadStatus() {
        var statusEl = document.getElementById('domain-ssl-status');
        if (!statusEl) return;

        fetchJSON(config.statusUrl).then(function(data) {
            renderStatus(data);

            // Pre-select current SSL mode
            if (data.ssl_mode) {
                var radio = document.querySelector(
                    'input[name="domain-ssl-mode"][value="' + data.ssl_mode + '"]'
                );
                if (radio) {
                    radio.checked = true;
                    onModeChange(data.ssl_mode);
                }
            }

            // If a task is running, start polling
            if (data.status && data.status !== 'idle' && data.status !== 'error') {
                showProgress(data.status);
                startPolling();
            }
        }).catch(function() {
            statusEl.innerHTML = '<div class="domain-ssl-status-value">' +
                '<span class="status-badge none">' + (t.noDomain || 'Not configured') + '</span>' +
                '</div>';
        });
    }

    function renderStatus(data) {
        var statusEl = document.getElementById('domain-ssl-status');
        if (!statusEl) return;

        var domain = data.domain || (t.noDomain || 'No domain configured');
        var sslLabel = data.ssl_mode_display || (t.noSsl || 'None');
        var statusBadge = 'none';

        if (data.domain && data.is_ssl_enabled) {
            statusBadge = 'active';
        } else if (data.domain) {
            statusBadge = 'warning';
        }
        if (data.status === 'error') {
            statusBadge = 'error';
        }

        var certHtml = '';
        if (data.cert && data.cert.has_valid_cert) {
            certHtml = '<div class="domain-ssl-status-item">' +
                '<div class="domain-ssl-status-label">' + (t.certIssuer || 'Issued by') + '</div>' +
                '<div class="domain-ssl-status-value">' + escapeHtml(data.cert.issuer || '—') + '</div>' +
                '</div>' +
                '<div class="domain-ssl-status-item">' +
                '<div class="domain-ssl-status-label">' + (t.certExpires || 'Expires') + '</div>' +
                '<div class="domain-ssl-status-value">' +
                (data.cert.days_remaining != null ? data.cert.days_remaining + ' ' + (t.daysRemaining || 'days remaining') : '—') +
                '</div></div>';
        }

        var errorHtml = '';
        if (data.last_error) {
            var isWarning = data.last_error.indexOf('Warning:') === 0;
            var badgeClass = isWarning ? 'warning' : 'error';
            var labelText = isWarning ? (t.warning || 'Warning') : (t.error || 'Error');
            errorHtml = '<div class="domain-ssl-status-item" style="grid-column: 1 / -1;">' +
                '<div class="domain-ssl-status-label">' + labelText + '</div>' +
                '<div class="domain-ssl-status-value"><span class="status-badge ' + badgeClass + '">' +
                escapeHtml(data.last_error) + '</span></div></div>';
        }

        statusEl.innerHTML = '<div class="domain-ssl-status-grid">' +
            '<div class="domain-ssl-status-item">' +
            '<div class="domain-ssl-status-label">Domain</div>' +
            '<div class="domain-ssl-status-value">' + escapeHtml(domain) + '</div>' +
            '</div>' +
            '<div class="domain-ssl-status-item">' +
            '<div class="domain-ssl-status-label">SSL</div>' +
            '<div class="domain-ssl-status-value"><span class="status-badge ' + statusBadge + '">' +
            escapeHtml(sslLabel) + '</span></div>' +
            '</div>' +
            certHtml + errorHtml +
            '</div>';
    }

    // ── DNS Check ───────────────────────────────────────

    function checkDns() {
        var domain = getDomain();
        if (!domain) {
            showDnsResult('error', '<ul class="messagelist"><li class="error">' +
                (t.domainRequired || 'Please enter a domain name') + '</li></ul>');
            return;
        }

        var btn = document.getElementById('domain-ssl-check-dns');
        btn.disabled = true;
        showDnsResult('info', '<ul class="messagelist"><li class="info">' +
            '<i class="fas fa-spinner fa-spin"></i> ' + (t.checking || 'Checking...') + '</li></ul>');

        fetchJSON(config.validateDnsUrl, {
            method: 'POST',
            body: { domain: domain }
        }).then(function(data) {
            btn.disabled = false;

            if (data.valid) {
                var items = '<li class="success"><i class="fas fa-check-circle"></i> ' +
                    (t.validDns || 'DNS resolves correctly') + '</li>';

                if (data.resolved_ips && data.resolved_ips.length) {
                    items += '<li class="info"><i class="fas fa-info-circle"></i> IP: ' +
                        escapeHtml(data.resolved_ips.join(', ')) + '</li>';
                }

                if (data.ip_match) {
                    items += '<li class="success"><i class="fas fa-check"></i> ' +
                        (t.ipMatch || 'IP matches this server') + '</li>';
                } else if (data.server_ip) {
                    items += '<li class="warning"><i class="fas fa-exclamation-triangle"></i> ' +
                        (t.ipMismatch || 'IP does not match this server') +
                        ' (' + escapeHtml(data.server_ip) + '). ' +
                        (t.ipMismatchHint || 'This is normal if you use Cloudflare or a load balancer.') +
                        '</li>';
                }

                showDnsResult('success', '<ul class="messagelist">' + items + '</ul>');
            } else {
                showDnsResult('error',
                    '<ul class="messagelist"><li class="error"><i class="fas fa-times-circle"></i> ' +
                    (t.invalidDns || 'DNS does not resolve') +
                    (data.error ? ': ' + escapeHtml(data.error) : '') + '</li></ul>'
                );
            }
        }).catch(function(err) {
            btn.disabled = false;
            showDnsResult('error', '<ul class="messagelist"><li class="error">' +
                '<i class="fas fa-times-circle"></i> ' +
                escapeHtml(err.message || 'Request failed') + '</li></ul>');
        });
    }

    function showDnsResult(type, html) {
        var el = document.getElementById('domain-ssl-dns-result');
        if (el) el.innerHTML = html;
    }

    // ── Configuration ───────────────────────────────────

    function startConfiguration() {
        var domain = getDomain();
        var sslMode = getSelectedMode();
        var email = (document.getElementById('domain-ssl-email') || {}).value || '';

        // Validation
        if (sslMode !== 'none' && !domain) {
            showResult('error', t.domainRequired || 'Please enter a domain name');
            return;
        }

        if ((sslMode === 'letsencrypt' || sslMode === 'letsencrypt_dns') && !email) {
            showResult('error', t.emailRequired || "Email is required for Let's Encrypt");
            return;
        }

        // For custom/cloudflare_origin cert, upload first
        if (sslMode === 'custom' || sslMode === 'cloudflare_origin') {
            uploadCertThenConfigure(domain, sslMode, email);
            return;
        }

        dispatchConfigure(domain, sslMode, email);
    }

    function uploadCertThenConfigure(domain, sslMode, email) {
        var certPem = (document.getElementById('domain-ssl-cert-pem') || {}).value || '';
        var keyPem = (document.getElementById('domain-ssl-key-pem') || {}).value || '';

        if (!certPem || !keyPem) {
            showResult('error', 'Both certificate and key are required');
            return;
        }

        disableActions();
        showProgress('configuring');

        fetchJSON(config.uploadCertUrl, {
            method: 'POST',
            body: { cert_pem: certPem, key_pem: keyPem }
        }).then(function(data) {
            if (data.success) {
                dispatchConfigure(domain, sslMode, email);
            } else {
                enableActions();
                hideProgress();
                showResult('error', data.message || 'Certificate upload failed');
            }
        }).catch(function(err) {
            enableActions();
            hideProgress();
            showResult('error', err.message || 'Upload failed');
        });
    }

    function dispatchConfigure(domain, sslMode, email) {
        configuredDomain = domain;
        configuredSslMode = sslMode;
        pollErrorCount = 0;

        disableActions();
        hideResult();
        showProgress('validating_dns');

        var body = {
            domain: domain,
            ssl_mode: sslMode,
            email: email
        };

        fetchJSON(config.configureUrl, {
            method: 'POST',
            body: body
        }).then(function(data) {
            if (data.error) {
                enableActions();
                hideProgress();
                showResult('error', data.error);
                return;
            }

            // Synchronous fallback: task completed inline (Celery unavailable)
            if (data.status === 'completed') {
                hideProgress();
                enableActions();
                showResult('success', '<i class="fas fa-check-circle"></i> ' +
                    (data.message || t.success || 'Configuration complete!'));
                loadStatus();
                return;
            }

            // Configuration task dispatched — start polling
            startPolling();
        }).catch(function(err) {
            enableActions();
            hideProgress();
            showResult('error', err.message || 'Request failed');
        });
    }

    // ── Polling ─────────────────────────────────────────

    function startPolling() {
        stopPolling();
        pollTimer = setInterval(pollProgress, 2000);
    }

    function stopPolling() {
        if (pollTimer) {
            clearInterval(pollTimer);
            pollTimer = null;
        }
    }

    function pollProgress() {
        fetchJSON(config.progressUrl).then(function(data) {
            pollErrorCount = 0;
            showProgress(data.status);

            if (data.is_complete) {
                stopPolling();
                hideProgress();
                enableActions();

                // If SSL was configured locally, redirect to the new HTTPS domain
                // (managed_externally doesn't change local nginx to HTTPS)
                if (configuredDomain && configuredSslMode &&
                    configuredSslMode !== 'none' && configuredSslMode !== 'managed_externally') {
                    var newUrl = 'https://' + configuredDomain + window.location.pathname;
                    showResult('success', '<i class="fas fa-check-circle"></i> ' +
                        (t.success || 'Configuration complete!') +
                        ' <a href="' + escapeHtml(newUrl) + '">' +
                        (t.redirecting || 'Redirecting to secure site...') + '</a>');
                    setTimeout(function() { window.location.href = newUrl; }, 2000);
                    return;
                }

                // Show success, with any warnings displayed separately
                showResult('success', '<i class="fas fa-check-circle"></i> ' +
                    (t.success || 'Configuration complete!'));
                if (data.last_error) {
                    showWarning(escapeHtml(data.last_error));
                }

                loadStatus();
            } else if (data.is_error) {
                stopPolling();
                hideProgress();
                enableActions();
                showResult('error', '<i class="fas fa-times-circle"></i> ' +
                    escapeHtml(data.last_error || 'Configuration failed'));
                loadStatus();
            }
        }).catch(function() {
            pollErrorCount++;

            // During NGINX reload, the server is briefly unreachable.
            // Show a "reloading" status and keep polling.
            if (pollErrorCount <= 15) {
                showProgress('reloading');
                return;
            }

            // After many failures with an SSL mode that switches to HTTPS,
            // assume the config succeeded and the browser can't reach the old URL.
            if (configuredDomain && configuredSslMode &&
                configuredSslMode !== 'none' && configuredSslMode !== 'managed_externally') {
                stopPolling();
                hideProgress();
                enableActions();
                var newUrl = 'https://' + configuredDomain + window.location.pathname;
                showResult('success', '<i class="fas fa-check-circle"></i> ' +
                    (t.sslApplied || 'SSL certificate has been applied.') +
                    ' <a href="' + escapeHtml(newUrl) + '">' +
                    (t.openSecureSite || 'Open your secure site') + ' →</a>');
                return;
            }

            // For non-HTTPS modes (none, managed_externally), if server
            // is down for too long, ask the merchant to reload.
            stopPolling();
            hideProgress();
            enableActions();
            showResult('warning', '<i class="fas fa-exclamation-triangle"></i> ' +
                (t.connectionLost || 'Lost connection to the server. The configuration may have completed.') +
                ' <a href="javascript:location.reload()">' +
                (t.reloadPage || 'Reload this page') + '</a>');
        });
    }

    // ── UI Helpers ──────────────────────────────────────

    function getDomain() {
        var el = document.getElementById('domain-ssl-domain');
        return el ? el.value.trim().toLowerCase() : '';
    }

    function getSelectedMode() {
        var radio = document.querySelector('input[name="domain-ssl-mode"]:checked');
        return radio ? radio.value : 'none';
    }

    function showProgress(status) {
        var el = document.getElementById('domain-ssl-progress');
        var fill = document.getElementById('domain-ssl-progress-fill');
        var text = document.getElementById('domain-ssl-progress-text');

        if (el) el.classList.add('active');
        if (fill) fill.style.width = (STATUS_PROGRESS[status] || 50) + '%';
        if (text) text.textContent = t[status] || status;
    }

    function hideProgress() {
        var el = document.getElementById('domain-ssl-progress');
        if (el) el.classList.remove('active');
    }

    function showResult(type, html) {
        var el = document.getElementById('domain-ssl-result');
        if (!el) return;
        el.className = 'domain-ssl-result visible ' + type;
        el.innerHTML = html;
    }

    function showWarning(message) {
        // Show a warning below the result area (non-blocking, informational)
        var el = document.getElementById('domain-ssl-warning');
        if (!el) {
            // Create warning element after result
            var result = document.getElementById('domain-ssl-result');
            if (!result) return;
            el = document.createElement('div');
            el.id = 'domain-ssl-warning';
            result.parentNode.insertBefore(el, result.nextSibling);
        }
        el.className = 'domain-ssl-result visible warning';
        el.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ' + message;
    }

    function hideWarning() {
        var el = document.getElementById('domain-ssl-warning');
        if (el) {
            el.className = 'domain-ssl-result';
            el.innerHTML = '';
        }
    }

    function hideResult() {
        var el = document.getElementById('domain-ssl-result');
        if (el) {
            el.className = 'domain-ssl-result';
            el.innerHTML = '';
        }
        hideWarning();
    }

    function disableActions() {
        var btn = document.getElementById('domain-ssl-configure');
        if (btn) btn.disabled = true;
    }

    function enableActions() {
        var btn = document.getElementById('domain-ssl-configure');
        if (btn) btn.disabled = false;
    }

    function escapeHtml(str) {
        if (!str) return '';
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    // ── Bootstrap ───────────────────────────────────────

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
