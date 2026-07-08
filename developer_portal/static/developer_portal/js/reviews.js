/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var T = {};

    document.addEventListener('DOMContentLoaded', function () {
        var el = document.getElementById('reviews-translations');
        if (el) {
            try { T = JSON.parse(el.textContent); } catch (err) {}
        }
        initCharCounters();
    });

    function showNotification(message, type) {
        AdminModal.toast(message, type || 'info');
    }

    function initCharCounters() {
        document.querySelectorAll('.dev-review-response-form textarea').forEach(function (ta) {
            ta.addEventListener('input', function () {
                var id = this.id.replace('response-text-', '');
                var counter = document.getElementById('char-count-' + id);
                if (counter) counter.textContent = this.value.length + ' / 2000';
            });
        });
    }

    function toggleResponseForm(reviewId) {
        var form = document.getElementById('response-form-' + reviewId);
        if (!form) return;
        var toggle = form.previousElementSibling;
        if (form.style.display === 'none') {
            form.style.display = 'block';
            if (toggle) toggle.style.display = 'none';
            var ta = form.querySelector('textarea');
            if (ta) ta.focus();
        } else {
            form.style.display = 'none';
            if (toggle) toggle.style.display = '';
        }
    }

    function submitResponse(reviewId) {
        var textarea = document.getElementById('response-text-' + reviewId);
        if (!textarea) return;
        var text = textarea.value.trim();
        if (!text) {
            showNotification(T.pleaseEnterResponse || 'Please enter a response.', 'warning');
            return;
        }

        var configEl = document.getElementById('reviews-config');
        var respondUrlTemplate = configEl ? configEl.dataset.respondUrlTemplate : '';
        var url = respondUrlTemplate.replace('/0/', '/' + reviewId + '/');

        var formData = new FormData();
        formData.append('response', text);
        formData.append('csrfmiddlewaretoken', getCsrfToken());

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(function (r) { return r.json(); })
        .then(function (data) {
            if (data.success) {
                var card = document.getElementById('review-' + reviewId);
                if (!card) return;
                var section = card.querySelector('.dev-review-response-section');
                var date = new Date(data.responded_at).toLocaleDateString(undefined, {
                    year: 'numeric', month: 'short', day: 'numeric'
                });
                section.innerHTML =
                    '<div class="dev-review-response">' +
                        '<div class="dev-review-response-header">' +
                            '<i class="fas fa-reply"></i> ' +
                            '<strong>' + (T.yourResponse || 'Your Response') + '</strong> ' +
                            '<span class="dev-review-response-date">' + date + '</span>' +
                        '</div>' +
                        '<p class="dev-review-response-text">' + data.response.replace(/</g, '&lt;') + '</p>' +
                    '</div>';
            } else {
                showNotification(data.error || (T.failedSubmit || 'Failed to submit response.'), 'error');
            }
        })
        .catch(function () {
            showNotification(T.networkError || 'Network error. Please try again.', 'error');
        });
    }

    document.addEventListener('click', function (e) {
        var btn = e.target.closest('[data-action]');
        if (!btn) return;

        var reviewId = btn.dataset.reviewId;

        switch (btn.dataset.action) {
            case 'toggle-response-form':
                if (reviewId) toggleResponseForm(reviewId);
                break;
            case 'submit-response':
                if (reviewId) submitResponse(reviewId);
                break;
        }
    });

    function getCsrfToken() {
        return AdminUtils.getCsrfToken();
    }

}());
