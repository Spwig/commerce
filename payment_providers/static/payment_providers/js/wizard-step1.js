/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Payment Provider Wizard Step 1: Select Provider
 * Handles card selection feedback and auto-contrast for provider logos.
 */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('provider-select-form');
    const cards = document.querySelectorAll('.provider-card');

    // Reinstall buttons for providers whose registry row is present but
    // whose on-disk files are missing. POST to the install endpoint —
    // which now self-heals the orphan row before re-downloading — and
    // reload so the page picks up the now-healthy entry.
    document.querySelectorAll('[data-action="reinstall-provider"]').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const url = btn.dataset.installUrl;
        if (!url || btn.disabled) return;

        const originalLabel = btn.innerHTML;
        btn.disabled = true;
        btn.innerHTML =
          '<i class="fas fa-spinner fa-spin"></i> ' + (btn.dataset.busyLabel || 'Reinstalling…');

        const csrf =
          (document.querySelector('input[name="csrfmiddlewaretoken"]') || {}).value || '';
        fetch(url, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
          credentials: 'same-origin',
        })
          .then(function (res) {
            return res.json();
          })
          .then(function (data) {
            if (data && data.success) {
              window.location.reload();
            } else {
              btn.disabled = false;
              btn.innerHTML = originalLabel;
              alert((data && data.error) || 'Reinstall failed. Check server logs.');
            }
          })
          .catch(function () {
            btn.disabled = false;
            btn.innerHTML = originalLabel;
            alert('Reinstall request failed. Check your connection.');
          });
      });
    });

    // Add visual feedback when selecting a provider
    cards.forEach(function (card) {
      const radio = card.querySelector('input[type="radio"]');

      card.addEventListener('click', function (e) {
        if (e.target.tagName !== 'INPUT') {
          radio.checked = true;
        }

        cards.forEach(function (c) {
          c.classList.remove('selected');
        });
        if (radio.checked) {
          card.classList.add('selected');
        }
      });

      if (radio.checked) {
        card.classList.add('selected');
      }
    });

    // Auto-contrast for provider logos
    document.querySelectorAll('[data-auto-contrast]').forEach(function (plate) {
      const img = plate.querySelector('img');
      if (img && img.complete) {
        adjustContrast(img, plate);
      } else if (img) {
        img.addEventListener('load', function () {
          adjustContrast(img, plate);
        });
      }
    });

    function adjustContrast(img, plate) {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      try {
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        let r = 0,
          g = 0,
          b = 0;

        for (let i = 0; i < data.length; i += 4) {
          r += data[i];
          g += data[i + 1];
          b += data[i + 2];
        }

        const pixelCount = data.length / 4;
        r = Math.floor(r / pixelCount);
        g = Math.floor(g / pixelCount);
        b = Math.floor(b / pixelCount);

        const brightness = (r * 299 + g * 587 + b * 114) / 1000;

        if (brightness > 200) {
          plate.style.backgroundColor = '#f5f5f5';
        } else {
          plate.style.backgroundColor = '#ffffff';
        }
      } catch (e) {
        // CORS or other error - use default
        plate.style.backgroundColor = '#ffffff';
      }
    }
  });
})();
