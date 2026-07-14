/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Manual Exchange Rates Admin JavaScript
 * Handles toggle active/inactive, lock/unlock, provider comparison, sync from provider
 */
(function () {
  'use strict';

  const languageCode = document.documentElement.lang || 'en';

  function showNotification(message, type) {
    AdminModal.toast(message, type || 'info');
  }

  function toggleRateActive(rateId, button) {
    const url =
      '/' + languageCode + '/admin/exchange-rates/admin/manual-rate/' + rateId + '/toggle-active/';

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          const icon = button.querySelector('i');
          const card = button.closest('.list-row-card');
          const badge = card.querySelector('.list-row-card-badge');

          if (data.is_active) {
            button.setAttribute('data-active', 'true');
            icon.className = 'fas fa-toggle-on';
            card.classList.remove('disabled');
            if (badge) {
              badge.className = 'list-row-card-badge success';
              badge.textContent = data.active_label || 'Active';
            }
          } else {
            button.setAttribute('data-active', 'false');
            icon.className = 'fas fa-toggle-off';
            card.classList.add('disabled');
            if (badge) {
              badge.className = 'list-row-card-badge';
              badge.textContent = data.inactive_label || 'Inactive';
            }
          }

          showNotification(data.message, 'success');
        } else {
          showNotification(data.message || 'An error occurred.', 'error');
        }
      })
      .catch(function (error) {
        console.error('Toggle error:', error);
        showNotification('An error occurred while updating the rate.', 'error');
      });
  }

  function toggleRateLocked(rateId, button) {
    const url =
      '/' + languageCode + '/admin/exchange-rates/admin/manual-rate/' + rateId + '/toggle-locked/';

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          const icon = button.querySelector('i');
          const card = button.closest('.list-row-card');
          const lockedBadge = card.querySelector('.locked-badge');

          if (data.exclude_from_auto_sync) {
            button.setAttribute('data-locked', 'true');
            button.title = 'Unlock (allow auto-sync)';
            icon.className = 'fas fa-lock';
            card.classList.add('locked');
            // Add locked badge if not present
            if (!lockedBadge) {
              const badgesContainer = card.querySelector('.list-row-card-badges');
              if (badgesContainer) {
                const badge = document.createElement('span');
                badge.className = 'list-row-card-badge locked-badge';
                badge.innerHTML = '<i class="fas fa-lock"></i> ' + (data.locked_label || 'Locked');
                badgesContainer.appendChild(badge);
              }
            }
          } else {
            button.setAttribute('data-locked', 'false');
            button.title = 'Lock (exclude from auto-sync)';
            icon.className = 'fas fa-lock-open';
            card.classList.remove('locked');
            // Remove locked badge
            if (lockedBadge) {
              lockedBadge.remove();
            }
          }

          showNotification(data.message, 'success');
        } else {
          showNotification(data.message || 'An error occurred.', 'error');
        }
      })
      .catch(function (error) {
        console.error('Lock toggle error:', error);
        showNotification('An error occurred while updating the rate.', 'error');
      });
  }

  function syncFromProvider() {
    const overlay = document.getElementById('sync-overlay');
    if (overlay) overlay.hidden = false;

    const url = '/' + languageCode + '/admin/exchange-rates/admin/manual-rate/sync-from-provider/';

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (overlay) overlay.hidden = true;

        if (data.success) {
          showNotification(data.message, 'success');
          // Reload after a brief delay so the notification is visible
          setTimeout(function () {
            window.location.reload();
          }, 1200);
        } else {
          let msg = data.message || 'Sync completed with errors.';
          if (data.errors && data.errors.length > 0) {
            msg += ' (' + data.errors.length + ' errors)';
          }
          showNotification(msg, data.created || data.updated ? 'success' : 'error');
          if (data.created || data.updated) {
            setTimeout(function () {
              window.location.reload();
            }, 1500);
          }
        }
      })
      .catch(function (error) {
        if (overlay) overlay.hidden = true;
        console.error('Sync error:', error);
        showNotification('An error occurred during sync.', 'error');
      });
  }

  function populateProviderComparisons() {
    const dataEl = document.getElementById('provider-rates-data');
    const providerRates = dataEl ? JSON.parse(dataEl.textContent) : {};
    const displays = document.querySelectorAll('.provider-rate-display');

    displays.forEach(function (el) {
      const pair = el.getAttribute('data-pair');
      const data = providerRates[pair];

      if (data && data.rate) {
        const card = el.closest('.list-row-card');
        const manualRateEl = card.querySelector('.manual-rate-value');
        const manualRateText = manualRateEl ? manualRateEl.textContent : '';

        // Extract manual rate number (format: "1 USD = 0.92 EUR")
        const manualMatch = manualRateText.match(/=\s*([\d.]+)/);
        const manualRate = manualMatch ? parseFloat(manualMatch[1]) : 0;
        const providerRate = parseFloat(data.rate);

        // Build provider rate display
        let html = '<i class="fas fa-cloud"></i> Provider: ' + parseFloat(data.rate).toFixed(6);

        // Calculate difference percentage
        if (manualRate > 0 && providerRate > 0) {
          const diff = ((manualRate - providerRate) / providerRate) * 100;
          const diffClass =
            diff > 0 ? 'diff-positive' : diff < 0 ? 'diff-negative' : 'diff-neutral';
          const diffSign = diff > 0 ? '+' : '';
          html +=
            ' <span class="rate-diff ' + diffClass + '">' + diffSign + diff.toFixed(2) + '%</span>';
        }

        el.innerHTML = html;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Populate provider comparisons
    populateProviderComparisons();

    // Event delegation
    document.addEventListener('click', function (e) {
      // Toggle active
      const toggleBtn = e.target.closest('.manual-rate-toggle');
      if (toggleBtn) {
        e.preventDefault();
        const rateId = toggleBtn.getAttribute('data-rate-id');
        if (rateId) toggleRateActive(rateId, toggleBtn);
        return;
      }

      // Toggle locked
      const lockBtn = e.target.closest('.manual-rate-lock-toggle');
      if (lockBtn) {
        e.preventDefault();
        const lockRateId = lockBtn.getAttribute('data-rate-id');
        if (lockRateId) toggleRateLocked(lockRateId, lockBtn);
        return;
      }

      // Sync from provider
      const syncBtn = e.target.closest('#sync-from-provider-btn, #sync-from-provider-empty-btn');
      if (syncBtn) {
        e.preventDefault();
        syncFromProvider();
        return;
      }
    });
  });
})();
