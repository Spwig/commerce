/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let platformInfo = {};
  let selectedPlatform = null;
  let translations = {};

  function init() {
    const tEl = document.getElementById('step1-data');
    if (tEl) {
      try {
        const data = JSON.parse(tEl.textContent);
        platformInfo = data.platforms || {};
        translations = data.translations || {};
      } catch (e) {}
    }

    // Event delegation for platform card selection
    document.addEventListener('click', function (e) {
      const card = e.target.closest('[data-action="select-platform"]');
      if (!card) return;
      selectPlatform(card.dataset.platform, card);
    });

    // Form validation on submit
    const form = document.getElementById('platform-form');
    if (form) {
      form.addEventListener('submit', function (e) {
        if (!selectedPlatform) {
          e.preventDefault();
          AdminModal.alert({
            message: translations.selectPlatform || 'Please select a platform to continue.',
            type: 'warning',
          });
        }
      });
    }
  }

  function selectPlatform(platform, card) {
    document.querySelectorAll('.platform-card').forEach(function (c) {
      c.classList.remove('selected');
    });

    if (card) {
      card.classList.add('selected');
    }

    const radio = document.getElementById('platform-' + platform);
    if (radio) {
      radio.checked = true;
    }
    selectedPlatform = platform;

    const info = platformInfo[platform] || {};
    const infoBox = document.getElementById('platform-info');
    const infoTitle = document.getElementById('platform-info-title');
    const infoDesc = document.getElementById('platform-info-description');

    if (infoTitle) {
      infoTitle.textContent = info.title || '';
    }
    if (infoDesc) {
      infoDesc.textContent = info.description || '';
    }
    if (infoBox) {
      infoBox.style.display = 'flex';
    }

    const nextBtn = document.getElementById('next-button');
    if (nextBtn) {
      nextBtn.disabled = false;
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
