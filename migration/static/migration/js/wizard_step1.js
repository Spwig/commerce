/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var platformInfo = {};
    var selectedPlatform = null;
    var translations = {};

    function init() {
        var tEl = document.getElementById('step1-data');
        if (tEl) {
            try {
                var data = JSON.parse(tEl.textContent);
                platformInfo = data.platforms || {};
                translations = data.translations || {};
            } catch (e) {}
        }

        // Event delegation for platform card selection
        document.addEventListener('click', function (e) {
            var card = e.target.closest('[data-action="select-platform"]');
            if (!card) return;
            selectPlatform(card.dataset.platform, card);
        });

        // Form validation on submit
        var form = document.getElementById('platform-form');
        if (form) {
            form.addEventListener('submit', function (e) {
                if (!selectedPlatform) {
                    e.preventDefault();
                    AdminModal.alert({message: translations.selectPlatform || 'Please select a platform to continue.', type: 'warning'});
                }
            });
        }
    }

    function selectPlatform(platform, card) {
        document.querySelectorAll('.platform-card').forEach(function (c) {
            c.classList.remove('selected');
        });

        if (card) { card.classList.add('selected'); }

        var radio = document.getElementById('platform-' + platform);
        if (radio) { radio.checked = true; }
        selectedPlatform = platform;

        var info = platformInfo[platform] || {};
        var infoBox = document.getElementById('platform-info');
        var infoTitle = document.getElementById('platform-info-title');
        var infoDesc = document.getElementById('platform-info-description');

        if (infoTitle) { infoTitle.textContent = info.title || ''; }
        if (infoDesc) { infoDesc.textContent = info.description || ''; }
        if (infoBox) { infoBox.style.display = 'flex'; }

        var nextBtn = document.getElementById('next-button');
        if (nextBtn) {
            nextBtn.disabled = false;
        }
    }

    document.addEventListener('DOMContentLoaded', init);
}());
