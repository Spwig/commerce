/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Translation Coverage Detail
 * Handles coverage visualization and bulk translation actions
 */

(function() {
    'use strict';

    const CoverageDetail = {
        _pollInterval: null,
        _jobIds: [],
        _scope: null,

        init: function() {
            // Initialize dynamic widths from data attributes (CSP-safe)
            document.querySelectorAll('[data-width]').forEach(function(el) {
                el.style.width = el.dataset.width + '%';
            });
            // Initialize SVG coverage rings
            document.querySelectorAll('.coverage-ring__fill[data-percentage]').forEach(function(el) {
                var pct = parseFloat(el.dataset.percentage) || 0;
                el.style.strokeDashoffset = 326.73 - (326.73 * pct / 100);
            });

            // Populate per-language stats from server data
            const _coverageEl = document.getElementById('translations-coverage-data');
            const COVERAGE_DATA = _coverageEl ? JSON.parse(_coverageEl.textContent) : {};
            const cts = COVERAGE_DATA.content_types || [];
            for (let i = 0; i < cts.length; i++) {
                const ct = cts[i];
                const bl = ct.by_language || {};
                for (const code in bl) {
                    const stats = bl[code];
                    const fill = document.querySelector('[data-ct="' + ct.key + '"][data-lang="' + code + '"]');
                    if (fill) fill.style.width = stats.pct + '%';
                    const stat = document.querySelector('[data-ct="' + ct.key + '"][data-lang="' + code + '-stats"]');
                    if (stat) stat.textContent = stats.translated + '/' + stats.total + ' (' + stats.pct + '%)';
                }
            }
        },

        toggleCard: function(card) {
            card.classList.toggle('coverage-card--collapsed');
        },

        translateAll: function() {
            this._scope = {scope: 'all'};
            this._openModal();
        },

        translateContentType: function(ctKey, langCode) {
            this._scope = {scope: 'content_type', content_type: ctKey, language: langCode};
            this._openModal();
        },

        _openModal: function() {
            const modal = document.getElementById('translate-all-modal');
            modal.classList.add('active');
            document.body.classList.add('admin-modal-body-locked');
            document.getElementById('translate-all-footer').setAttribute('hidden', '');
            document.getElementById('translate-all-body').innerHTML =
                '<div class="translate-all-loading"><i class="fas fa-spinner fa-spin"></i>' +
                '<p>Calculating what needs to be translated...</p></div>';

            fetch('/api/translations/service/translate-all/estimate/')
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    this._renderEstimate(data);
                } else {
                    document.getElementById('translate-all-body').innerHTML =
                        '<div class="translate-all-error"><i class="fas fa-exclamation-circle"></i>' +
                        '<p>' + (data.error || 'Failed to calculate estimate') + '</p></div>';
                }
            })
            .catch(err => {
                document.getElementById('translate-all-body').innerHTML =
                    '<div class="translate-all-error"><i class="fas fa-exclamation-circle"></i>' +
                    '<p>Error: ' + err.message + '</p></div>';
            });
        },

        _renderEstimate: function(data) {
            let html = '<div class="translate-all-estimate">';
            html += '<div class="translate-all-summary">';
            html += '<p><strong>' + data.total_fields + '</strong> fields across ';
            html += '<strong>' + data.content_types.length + '</strong> content types need translation into ';
            html += '<strong>' + data.languages.length + '</strong> languages.</p>';
            html += '<p class="translate-all-jobs-info"><i class="fas fa-tasks"></i> ';
            html += 'This will create <strong>' + data.total_jobs + '</strong> translation jobs.</p>';
            html += '</div>';

            // Content type breakdown
            html += '<table class="translate-all-breakdown"><thead><tr>';
            html += '<th>Content Type</th><th>Missing Fields</th><th>Jobs</th>';
            html += '</tr></thead><tbody>';
            for (let i = 0; i < data.content_types.length; i++) {
                const ct = data.content_types[i];
                html += '<tr><td><i class="' + ct.icon + '"></i> ' + ct.label + '</td>';
                html += '<td>' + ct.missing_fields + '</td>';
                html += '<td>' + ct.jobs + '</td></tr>';
            }
            html += '</tbody></table>';

            // Warning
            if (data.is_large) {
                html += '<div class="translate-all-warning">';
                html += '<i class="fas fa-exclamation-triangle"></i> ';
                html += 'Large translation batch. We recommend running during off-peak hours to avoid impacting site performance for your shoppers.';
                html += '</div>';
            }

            html += '</div>';
            document.getElementById('translate-all-body').innerHTML = html;
            document.getElementById('translate-all-footer').removeAttribute('hidden');
        },

        confirmTranslate: function() {
            const btn = document.getElementById('translate-all-confirm');
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Starting...';

            const body = this._scope || {scope: 'all'};

            fetch('/api/translations/service/translate-all/', {
                method: 'POST',
                headers: {'Content-Type': 'application/json', 'X-CSRFToken': AdminUtils.getCsrfToken()},
                body: JSON.stringify(body)
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    this._jobIds = data.job_ids || [];
                    this._showProgress(data);
                } else {
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fas fa-play"></i> Start Translation';
                    AdminModal.alert({message: data.error || 'Failed', type: 'error'});
                }
            })
            .catch(err => {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-play"></i> Start Translation';
                AdminModal.alert({message: err.message, type: 'error'});
            });
        },

        _showProgress: function(data) {
            document.getElementById('translate-all-footer').setAttribute('hidden', '');
            let html = '<div class="translate-all-progress">';
            html += '<div class="translate-all-progress__icon"><i class="fas fa-cogs fa-spin"></i></div>';
            html += '<h4>Translation in progress</h4>';
            html += '<p>' + (data.job_ids ? data.job_ids.length : 0) + ' jobs created and queued.</p>';
            html += '<div class="translate-all-progress__bar"><div class="translate-all-progress__fill" id="ta-progress-fill"></div></div>';
            html += '<p class="translate-all-progress__text" id="ta-progress-text">Starting...</p>';
            html += '<p class="translate-all-progress__tip"><i class="fas fa-info-circle"></i> You can close this dialog. Jobs will continue in the background. <a href="' + ((document.getElementById('translations-config') || document.body).dataset.jobsUrl || '/admin/translations/translation-jobs/') + '">View Jobs</a></p>';
            html += '</div>';
            document.getElementById('translate-all-body').innerHTML = html;

            this._pollInterval = setInterval(() => { this._poll(); }, 5000);
        },

        _poll: function() {
            if (!this._jobIds.length) return;
            fetch('/api/translations/service/translate-all/status/?job_ids=' + this._jobIds.join(','))
            .then(r => r.json())
            .then(data => {
                if (!data.success) return;
                const fill = document.getElementById('ta-progress-fill');
                const text = document.getElementById('ta-progress-text');
                if (fill) fill.style.width = data.overall_progress + '%';
                if (text) text.textContent = data.completed + '/' + data.total_jobs + ' jobs completed' +
                    (data.failed > 0 ? ' (' + data.failed + ' failed)' : '');
                if (data.completed + data.failed >= data.total_jobs) {
                    clearInterval(this._pollInterval);
                    if (text) text.textContent += ' — Done!';
                    if (fill) fill.style.width = '100%';
                }
            })
            .catch(() => {});
        },

        closeModal: function() {
            document.getElementById('translate-all-modal').classList.remove('active');
            document.body.classList.remove('admin-modal-body-locked');
            if (this._pollInterval) {
                clearInterval(this._pollInterval);
                this._pollInterval = null;
            }
            if (this._jobIds.length) {
                this._jobIds = [];
                location.reload();
            }
        }
    };

    /**
     * Handle coverage detail actions via delegation
     */
    function handleCoverageActions(e) {
        const actionElement = e.target.closest('[data-action]');
        if (!actionElement) return;

        const action = actionElement.dataset.action;

        switch (action) {
            case 'translate-all':
                e.preventDefault();
                CoverageDetail.translateAll();
                break;
            case 'toggle-card':
                e.preventDefault();
                CoverageDetail.toggleCard(actionElement.closest('.coverage-card'));
                break;
            case 'translate-content-type':
                e.preventDefault();
                const ctKey = actionElement.dataset.ctKey;
                const langCode = actionElement.dataset.langCode;
                if (ctKey && langCode) {
                    CoverageDetail.translateContentType(ctKey, langCode);
                }
                break;
            case 'close-translate-modal':
                e.preventDefault();
                CoverageDetail.closeModal();
                break;
            case 'confirm-translate':
                e.preventDefault();
                CoverageDetail.confirmTranslate();
                break;
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            CoverageDetail.init();
            document.addEventListener('click', handleCoverageActions);
        });
    } else {
        CoverageDetail.init();
        document.addEventListener('click', handleCoverageActions);
    }

    // Export for external access if needed
    window.CoverageDetail = CoverageDetail;

})();
