/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Affiliate Portal JavaScript
 * Client-side functionality for the affiliate dashboard, portal landing page,
 * tracking links, programs, and payouts.
 *
 * Replaces inline onclick/onsubmit handlers throughout affiliate frontend templates.
 * i18n strings are read from <script type="application/json" id="affiliate-portal-i18n">.
 */

(function() {
    'use strict';

    var i18n = {};

    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        // Load i18n strings from optional JSON data island
        var i18nEl = document.getElementById('affiliate-portal-i18n');
        if (i18nEl) {
            try { i18n = JSON.parse(i18nEl.textContent); } catch (e) {}
        }

        initThemeListener();
        initCopyButtons();
        initCharts();
        initRegistrationModal();
        initAffiliatePrograms();
        initCreateLinkForm();
        initEditLinkForm();
        initPayoutRequestForm();
    });

    // ─── Event delegation hub ────────────────────────────────────────────────
    document.addEventListener('click', function(e) {
        var target = e.target.closest('[data-action]');
        if (!target) return;

        var action = target.dataset.action;

        if (action === 'show-registration-modal') {
            showRegistrationModal();
        } else if (action === 'hide-registration-modal') {
            hideRegistrationModal();
        } else if (action === 'switch-auth-mode') {
            switchAuthMode(target.dataset.mode || 'register');
        } else if (action === 'copy-link') {
            e.preventDefault();
            copyToClipboard(target.dataset.linkUrl || '', target);
        } else if (action === 'show-create-link-modal') {
            showCreateLinkModal();
        } else if (action === 'close-create-link-modal') {
            hideCreateLinkModal();
        } else if (action === 'show-link-stats') {
            showLinkStats(target.dataset.linkId);
        } else if (action === 'edit-link') {
            showEditLink(target.dataset.linkId);
        } else if (action === 'close-link-stats-modal') {
            hideLinkStatsModal();
        } else if (action === 'close-edit-link-modal') {
            hideEditLinkModal();
        } else if (action === 'request-payout') {
            showPayoutModal();
        } else if (action === 'close-payout-modal') {
            hidePayoutModal();
        } else if (action === 'navigate-to') {
            var url = target.dataset.url;
            if (url) window.location.href = url;
        }
    });

    // ─── Registration Modal ───────────────────────────────────────────────────
    var currentAuthMode = 'register';

    function showRegistrationModal() {
        var modal = document.getElementById('registrationModal');
        if (modal) {
            modal.classList.remove('hidden');
            document.body.classList.add('modal-open');
        }
    }

    function hideRegistrationModal() {
        var modal = document.getElementById('registrationModal');
        if (!modal) return;
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
        var form = document.getElementById('affiliateRegistrationForm');
        if (form) form.reset();
        var errEl = document.getElementById('registrationError');
        var sucEl = document.getElementById('registrationSuccess');
        if (errEl) errEl.classList.add('hidden');
        if (sucEl) sucEl.classList.add('hidden');
        switchAuthMode('register');
    }

    function switchAuthMode(mode) {
        currentAuthMode = mode;
        var tabs = document.querySelectorAll('.auth-tab');
        var form = document.getElementById('affiliateRegistrationForm');
        var loginPrompt = document.getElementById('loginPrompt');
        var accountFields = document.getElementById('accountFields');

        tabs.forEach(function(tab) {
            tab.classList.toggle('active', tab.dataset.mode === mode);
        });

        if (mode === 'login') {
            if (loginPrompt) loginPrompt.classList.remove('hidden');
            if (form) form.classList.add('hidden');
        } else {
            if (loginPrompt) loginPrompt.classList.add('hidden');
            if (form) form.classList.remove('hidden');
            if (accountFields) accountFields.classList.remove('hidden');
        }
    }

    function initRegistrationModal() {
        var form = document.getElementById('affiliateRegistrationForm');
        if (!form) return;

        // Close on Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') hideRegistrationModal();
        });

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            submitRegistration(form);
        });
    }

    function submitRegistration(form) {
        var submitBtn = document.getElementById('submitBtn');
        var errorDiv = document.getElementById('registrationError');
        var successDiv = document.getElementById('registrationSuccess');
        var isGuestMode = form.dataset.guestMode === 'true';
        var dashboardUrl = form.dataset.dashboardUrl || '/';

        var submittingLabel = (i18n.submitting || 'Submitting...');
        var submitLabel = (i18n.submitApplication || 'Submit Application');

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + submittingLabel;
        }
        if (errorDiv) errorDiv.classList.add('hidden');
        if (successDiv) successDiv.classList.add('hidden');

        var data = {
            payment_email: getVal('payment_email'),
            payment_method: getVal('payment_method'),
            company_name: getVal('company_name'),
            website: getVal('website'),
            how_heard: getVal('how_heard'),
            terms_accepted: getChecked('terms_accepted')
        };

        if (isGuestMode && currentAuthMode === 'register') {
            data.email = getVal('email');
            data.password = getVal('password');
            data.first_name = getVal('first_name');
            data.last_name = getVal('last_name');

            if (!data.email || !data.password) {
                showError(errorDiv, i18n.fillEmailPassword || 'Please fill in your email and password to create an account.');
                resetBtn(submitBtn, submitLabel);
                return;
            }
        }

        if (!data.terms_accepted) {
            showError(errorDiv, i18n.acceptTerms || 'You must accept the terms and conditions to continue.');
            resetBtn(submitBtn, submitLabel);
            return;
        }

        fetch('/api/affiliate/affiliates/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(data)
        })
        .then(function(response) {
            if (!response.ok) {
                return response.json().then(function(err) { throw err; });
            }
            return response.json();
        })
        .then(function(result) {
            var message = result.message || (i18n.applicationSubmitted || 'Your affiliate application has been submitted successfully!');
            var redirectingMsg = (i18n.redirecting || 'Redirecting to your dashboard...');
            if (successDiv) {
                successDiv.innerHTML = '<i class="fas fa-check-circle"></i> ' + message + ' ' + redirectingMsg;
                successDiv.classList.remove('hidden');
            }
            setTimeout(function() {
                window.location.href = result.redirect_url || dashboardUrl;
            }, 2000);
        })
        .catch(function(error) {
            var errorMessage = i18n.generalError || 'An error occurred. Please try again.';
            if (error && error.error) {
                errorMessage = error.error;
            } else if (error && error.detail) {
                errorMessage = error.detail;
            } else if (error && typeof error === 'object') {
                var messages = [];
                for (var field in error) {
                    if (Object.prototype.hasOwnProperty.call(error, field)) {
                        var fieldErrors = error[field];
                        if (Array.isArray(fieldErrors)) {
                            messages.push(field + ': ' + fieldErrors.join(', '));
                        } else {
                            messages.push(field + ': ' + fieldErrors);
                        }
                    }
                }
                if (messages.length > 0) errorMessage = messages.join('<br>');
            }
            showError(errorDiv, errorMessage);
            resetBtn(submitBtn, submitLabel);
        });
    }

    // ─── Affiliate Programs ──────────────────────────────────────────────────
    function initAffiliatePrograms() {
        document.addEventListener('click', async function(e) {
            var btn = e.target.closest('[data-action="apply-program"]');
            if (!btn) return;

            var programId = btn.dataset.programId;
            var programName = btn.dataset.programName || '';
            var confirmMsg = (i18n.confirmApply || 'Would you like to apply to join') + ' "' + programName + '"?';

            if (!await AdminModal.confirm(confirmMsg)) return;

            fetch('/api/affiliate/programs/' + programId + '/apply/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                }
            })
            .then(function(response) {
                if (response.ok) return response.json();
                throw new Error('Application failed');
            })
            .then(function() {
                AdminModal.toast(i18n.applicationSuccess || 'Application submitted successfully! You will be notified once it is reviewed.', 'success');
                location.reload();
            })
            .catch(function(err) {
                console.error('Error:', err);
                AdminModal.alert({message: i18n.applicationError || 'Unable to submit application. Please try again later.', type: 'error'});
            });
        });
    }

    // ─── Create Link Modal ──────────────────────────────────────────────────
    function showCreateLinkModal() {
        var modal = document.getElementById('createLinkModal');
        if (!modal) return;
        modal.classList.remove('hidden');
        document.body.classList.add('modal-open');
    }

    function hideCreateLinkModal() {
        var modal = document.getElementById('createLinkModal');
        if (!modal) return;
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
        var form = document.getElementById('createLinkForm');
        if (form) form.reset();
        var errorDiv = document.getElementById('createLinkError');
        if (errorDiv) errorDiv.classList.add('hidden');
    }

    function initCreateLinkForm() {
        var form = document.getElementById('createLinkForm');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var errorDiv = document.getElementById('createLinkError');
            var programSelect = document.getElementById('linkProgram');
            var labelInput = document.getElementById('linkLabel');
            var destInput = document.getElementById('linkDestination');

            if (!programSelect.value) {
                if (errorDiv) {
                    errorDiv.textContent = i18n.selectProgram || 'Please select a program.';
                    errorDiv.classList.remove('hidden');
                }
                return;
            }

            var payload = {
                program: parseInt(programSelect.value, 10),
                label: labelInput ? labelInput.value : '',
                destination_url: destInput ? destInput.value : ''
            };

            // Default destination to store homepage if empty
            if (!payload.destination_url) {
                payload.destination_url = window.location.origin + '/';
            }

            fetch('/api/affiliate/links/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(payload)
            })
            .then(function(response) {
                if (response.ok) return response.json();
                return response.json().then(function(err) { throw err; });
            })
            .then(function() {
                hideCreateLinkModal();
                location.reload();
            })
            .catch(function(err) {
                if (errorDiv) {
                    var msg = '';
                    if (err && typeof err === 'object') {
                        Object.keys(err).forEach(function(key) {
                            var val = Array.isArray(err[key]) ? err[key].join(', ') : err[key];
                            msg += val + ' ';
                        });
                    }
                    errorDiv.textContent = msg || (i18n.createLinkError || 'Failed to create link. Please try again.');
                    errorDiv.classList.remove('hidden');
                }
            });
        });
    }

    // ─── Link Statistics Modal ──────────────────────────────────────────────
    function showLinkStats(linkId) {
        if (!linkId) return;
        var modal = document.getElementById('linkStatsModal');
        var body = document.getElementById('linkStatsBody');
        if (!modal || !body) return;

        body.innerHTML = '<div class="loading-spinner"></div>';
        modal.classList.remove('hidden');
        document.body.classList.add('modal-open');

        fetch('/api/affiliate/links/' + linkId + '/', {
            headers: { 'X-CSRFToken': getCsrfToken() }
        })
        .then(function(response) {
            if (!response.ok) throw new Error('Failed to load statistics');
            return response.json();
        })
        .then(function(data) {
            var stats = data.statistics;
            var label = data.label || data.link_code;
            body.innerHTML =
                '<h3 class="stats-link-name">' + escapeHtml(label) + '</h3>' +
                '<div class="stats-grid">' +
                '  <div class="stats-grid-item"><div class="stats-grid-label">' + (i18n.totalClicks || 'Total Clicks') + '</div><div class="stats-grid-value">' + formatNumber(stats.clicks.total) + '</div></div>' +
                '  <div class="stats-grid-item"><div class="stats-grid-label">' + (i18n.last7Days || 'Last 7 Days') + '</div><div class="stats-grid-value">' + formatNumber(stats.clicks.last_7_days) + '</div></div>' +
                '  <div class="stats-grid-item"><div class="stats-grid-label">' + (i18n.totalConversions || 'Conversions') + '</div><div class="stats-grid-value">' + formatNumber(stats.conversions.total) + '</div></div>' +
                '  <div class="stats-grid-item"><div class="stats-grid-label">' + (i18n.conversionRate || 'Conversion Rate') + '</div><div class="stats-grid-value">' + stats.conversions.rate + '%</div></div>' +
                '  <div class="stats-grid-item highlight"><div class="stats-grid-label">' + (i18n.totalRevenue || 'Total Revenue') + '</div><div class="stats-grid-value">' + formatCurrency(stats.revenue.total) + '</div></div>' +
                '</div>';
        })
        .catch(function() {
            body.innerHTML = '<div class="affiliate-alert affiliate-alert-danger"><i class="fas fa-exclamation-circle"></i> ' + (i18n.statsError || 'Failed to load statistics. Please try again.') + '</div>';
        });
    }

    function hideLinkStatsModal() {
        var modal = document.getElementById('linkStatsModal');
        if (!modal) return;
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
    }

    // ─── Edit Link Modal ────────────────────────────────────────────────────
    function showEditLink(linkId) {
        if (!linkId) return;
        var modal = document.getElementById('editLinkModal');
        if (!modal) return;

        document.getElementById('editLinkId').value = linkId;
        var errorDiv = document.getElementById('editLinkError');
        var successDiv = document.getElementById('editLinkSuccess');
        if (errorDiv) errorDiv.classList.add('hidden');
        if (successDiv) successDiv.classList.add('hidden');

        modal.classList.remove('hidden');
        document.body.classList.add('modal-open');

        fetch('/api/affiliate/links/' + linkId + '/', {
            headers: { 'X-CSRFToken': getCsrfToken() }
        })
        .then(function(response) {
            if (!response.ok) throw new Error('Failed to load link');
            return response.json();
        })
        .then(function(data) {
            document.getElementById('editLinkLabel').value = data.label || '';
            document.getElementById('editLinkDestination').value = data.destination_url || '';
            document.getElementById('editLinkActive').checked = data.is_active;
        })
        .catch(function() {
            if (errorDiv) {
                errorDiv.textContent = i18n.loadLinkError || 'Failed to load link data.';
                errorDiv.classList.remove('hidden');
            }
        });
    }

    function hideEditLinkModal() {
        var modal = document.getElementById('editLinkModal');
        if (!modal) return;
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
        var form = document.getElementById('editLinkForm');
        if (form) form.reset();
    }

    function initEditLinkForm() {
        var form = document.getElementById('editLinkForm');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var linkId = document.getElementById('editLinkId').value;
            var errorDiv = document.getElementById('editLinkError');
            var successDiv = document.getElementById('editLinkSuccess');
            if (errorDiv) errorDiv.classList.add('hidden');
            if (successDiv) successDiv.classList.add('hidden');

            var payload = {
                label: document.getElementById('editLinkLabel').value,
                destination_url: document.getElementById('editLinkDestination').value,
                is_active: document.getElementById('editLinkActive').checked
            };

            fetch('/api/affiliate/links/' + linkId + '/', {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(payload)
            })
            .then(function(response) {
                if (response.ok) return response.json();
                return response.json().then(function(err) { throw err; });
            })
            .then(function() {
                if (successDiv) {
                    successDiv.innerHTML = '<i class="fas fa-check-circle"></i> ' + (i18n.linkUpdated || 'Link updated successfully!');
                    successDiv.classList.remove('hidden');
                }
                setTimeout(function() {
                    hideEditLinkModal();
                    location.reload();
                }, 1000);
            })
            .catch(function(err) {
                if (errorDiv) {
                    var msg = '';
                    if (err && typeof err === 'object') {
                        Object.keys(err).forEach(function(key) {
                            var val = Array.isArray(err[key]) ? err[key].join(', ') : err[key];
                            msg += val + ' ';
                        });
                    }
                    errorDiv.textContent = msg || (i18n.editLinkError || 'Failed to update link. Please try again.');
                    errorDiv.classList.remove('hidden');
                }
            });
        });
    }

    // ─── Payout Request Modal ───────────────────────────────────────────────
    function showPayoutModal() {
        var modal = document.getElementById('payoutRequestModal');
        if (!modal) return;
        var errorDiv = document.getElementById('payoutRequestError');
        var successDiv = document.getElementById('payoutRequestSuccess');
        if (errorDiv) errorDiv.classList.add('hidden');
        if (successDiv) successDiv.classList.add('hidden');
        modal.classList.remove('hidden');
        document.body.classList.add('modal-open');
    }

    function hidePayoutModal() {
        var modal = document.getElementById('payoutRequestModal');
        if (!modal) return;
        modal.classList.add('hidden');
        document.body.classList.remove('modal-open');
        var form = document.getElementById('payoutRequestForm');
        if (form) form.reset();
    }

    function initPayoutRequestForm() {
        var form = document.getElementById('payoutRequestForm');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var errorDiv = document.getElementById('payoutRequestError');
            var successDiv = document.getElementById('payoutRequestSuccess');
            var submitBtn = form.querySelector('button[type="submit"]');
            if (errorDiv) errorDiv.classList.add('hidden');
            if (successDiv) successDiv.classList.add('hidden');

            var affiliateId = document.getElementById('payoutAffiliateId');
            var amountInput = document.getElementById('payoutAmount');
            var methodSelect = document.getElementById('payoutMethod');

            if (!affiliateId || !amountInput.value) return;

            var payload = {
                affiliate_id: parseInt(affiliateId.value, 10),
                amount: amountInput.value,
                method: methodSelect.value
            };

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + (i18n.submitting || 'Submitting...');
            }

            fetch('/api/affiliate/payouts/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(payload)
            })
            .then(function(response) {
                if (response.ok || response.status === 201) return response.json();
                return response.json().then(function(err) { throw err; });
            })
            .then(function() {
                if (successDiv) {
                    successDiv.innerHTML = '<i class="fas fa-check-circle"></i> ' + (i18n.payoutSuccess || 'Payout request submitted successfully!');
                    successDiv.classList.remove('hidden');
                }
                setTimeout(function() {
                    hidePayoutModal();
                    location.reload();
                }, 1500);
            })
            .catch(function(err) {
                var msg = '';
                if (err && err.non_field_errors) {
                    msg = Array.isArray(err.non_field_errors) ? err.non_field_errors.join(', ') : err.non_field_errors;
                } else if (err && typeof err === 'object') {
                    Object.keys(err).forEach(function(key) {
                        var val = Array.isArray(err[key]) ? err[key].join(', ') : err[key];
                        msg += val + ' ';
                    });
                }
                if (errorDiv) {
                    errorDiv.textContent = msg || (i18n.payoutError || 'Failed to submit payout request. Please try again.');
                    errorDiv.classList.remove('hidden');
                }
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> ' + (i18n.submitRequest || 'Submit Request');
                }
            });
        });
    }

    // ─── Theme listener ──────────────────────────────────────────────────────
    function initThemeListener() {
        document.addEventListener('admin-theme-changed', function(e) {
            document.body.setAttribute('data-theme', e.detail.theme);
            if (typeof refreshCharts === 'function') refreshCharts();
        });
    }

    // ─── Copy buttons ([data-copy-text] and [data-action="copy-link"]) ───────
    function initCopyButtons() {
        document.addEventListener('click', function(e) {
            var btn = e.target.closest('[data-copy-text]');
            if (!btn) return;
            e.preventDefault();
            copyToClipboard(btn.getAttribute('data-copy-text'), btn);
        });
    }

    function copyToClipboard(text, button) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(text).then(function() {
                showCopyFeedback(button);
            }).catch(function(err) {
                console.error('Failed to copy text:', err);
                fallbackCopy(text, button);
            });
        } else {
            fallbackCopy(text, button);
        }
    }

    function showCopyFeedback(button) {
        if (!button) return;
        var originalHtml = button.innerHTML;
        var msg = i18n.copied || 'Copied!';
        button.innerHTML = '<i class="fas fa-check"></i> ' + msg;
        button.classList.add('btn-affiliate-success');
        setTimeout(function() {
            button.innerHTML = originalHtml;
            button.classList.remove('btn-affiliate-success');
        }, 2000);
    }

    function fallbackCopy(text, button) {
        var textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-9999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            if (document.execCommand('copy')) showCopyFeedback(button);
        } catch (err) {
            console.error('Fallback copy failed:', err);
        }
        document.body.removeChild(textArea);
    }

    // ─── Charts ─────────────────────────────────────────────────────────────
    function initCharts() {
        var chartElements = document.querySelectorAll('[data-chart]');
        if (chartElements.length === 0) return;

        if (typeof Chart === 'undefined') {
            console.error('Chart.js is not loaded');
            return;
        }

        var dataEl = document.getElementById('affiliate-chart-data');
        if (!dataEl) return;

        var config;
        try {
            config = JSON.parse(dataEl.textContent);
        } catch (e) {
            return;
        }

        var isDarkTheme = document.body.getAttribute('data-theme') === 'dark';
        var textColor = isDarkTheme ? '#e8e8e8' : '#333333';
        var gridColor = isDarkTheme ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.1)';

        Chart.defaults.color = textColor;
        Chart.defaults.borderColor = gridColor;

        var canvas = document.getElementById('affiliatePerformanceChart');
        if (!canvas) return;

        var labels = config.labels.map(function(d) {
            return new Date(d).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });

        new Chart(canvas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: config.clicksLabel,
                        data: config.clicks,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 3,
                        pointHoverRadius: 6,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: isDarkTheme ? '#1f2937' : '#fff',
                        pointBorderWidth: 2,
                        yAxisID: 'y'
                    },
                    {
                        label: config.revenueLabel,
                        data: config.revenue,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 3,
                        pointHoverRadius: 6,
                        pointBackgroundColor: '#10b981',
                        pointBorderColor: isDarkTheme ? '#1f2937' : '#fff',
                        pointBorderWidth: 2,
                        yAxisID: 'y1'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                plugins: {
                    legend: { display: true, position: 'top' },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        padding: 12,
                        callbacks: {
                            label: function(context) {
                                var label = context.dataset.label || '';
                                if (context.datasetIndex === 1) {
                                    return label + ': $' + context.parsed.y.toFixed(2);
                                }
                                return label + ': ' + context.parsed.y;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        beginAtZero: true,
                        title: { display: true, text: config.clicksLabel },
                        grid: { color: gridColor }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        beginAtZero: true,
                        title: { display: true, text: config.revenueLabel },
                        grid: { drawOnChartArea: false },
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toFixed(0);
                            }
                        }
                    },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    function refreshCharts() {
        // Re-init charts when theme changes
        var canvas = document.getElementById('affiliatePerformanceChart');
        if (canvas) {
            var existing = Chart.getChart(canvas);
            if (existing) existing.destroy();
        }
        initCharts();
    }

    // ─── Utilities ──────────────────────────────────────────────────────────
    function escapeHtml(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    function getVal(id) {
        var el = document.getElementById(id);
        return el ? el.value : '';
    }

    function getChecked(id) {
        var el = document.getElementById(id);
        return el ? el.checked : false;
    }

    function showError(errorDiv, msg) {
        if (errorDiv) {
            errorDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + msg;
            errorDiv.classList.remove('hidden');
        }
    }

    function resetBtn(btn, label) {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-paper-plane"></i> ' + label;
        }
    }

    function getCsrfToken() {
        if (window.getCSRFToken) return window.getCSRFToken();
        var meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        var el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : '';
    }

    // ─── Public API ──────────────────────────────────────────────────────────
    window.formatCurrency = function(amount, currency) {
        currency = currency || window.__shopCurrency || 'USD';
        return new Intl.NumberFormat('en-US', {style: 'currency', currency: currency}).format(amount);
    };

    window.formatNumber = function(number) {
        return new Intl.NumberFormat('en-US').format(number);
    };

    window.debounce = function(func, wait) {
        var timeout;
        return function() {
            var context = this;
            var args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                func.apply(context, args);
            }, wait);
        };
    };

    window.showLoading = function(element) {
        if (typeof element === 'string') element = document.querySelector(element);
        if (element) element.innerHTML = '<div class="loading-spinner"></div>';
    };

    window.hideLoading = function(element, content) {
        if (typeof element === 'string') element = document.querySelector(element);
        if (element && content) element.innerHTML = content;
    };

})();
