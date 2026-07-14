/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Payment Provider Admin - Individual Account JavaScript
 * Handles sync methods link, method toggle checkboxes, and form validation.
 */

(function () {
  'use strict';

  // Load i18n strings from template config (if present)
  let i18n = {};
  const configEl = document.getElementById('pp-methods-config');
  if (configEl) {
    try {
      const config = JSON.parse(configEl.textContent);
      i18n = config.i18n || {};
    } catch (e) {
      // fall back to empty strings
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    initializeTooltips();
    initializeFormValidation();
    initializeSyncMethodsLink();
    initializeSyncMethodsButton();
    initializeMethodToggles();
    initializeToggleAllButtons();
    initializeRemoveCountryButtons();
  });

  /**
   * Initialize tooltips
   */
  function initializeTooltips() {
    const helpIcons = document.querySelectorAll('.help-icon');
    helpIcons.forEach(function (icon) {
      icon.title = icon.dataset.help || '';
    });
  }

  /**
   * Initialize form validation
   */
  function initializeFormValidation() {
    const form = document.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', function (e) {
      // Custom validation placeholder
    });
  }

  /**
   * Handle "Sync Payment Methods Now" link click
   */
  function initializeSyncMethodsLink() {
    const syncLink = document.querySelector('.pp-sync-methods-link');
    if (!syncLink) return;

    syncLink.addEventListener('click', function (e) {
      e.preventDefault();
      const accountId = this.dataset.accountId;
      if (!accountId) return;

      const csrfToken = getCsrf();
      const langPrefix = window.AdminUtils ? AdminUtils.getLanguagePrefix() : '';
      const url =
        langPrefix +
        '/admin/payment_providers/paymentprovideraccount/' +
        accountId +
        '/sync-methods/';

      this.textContent = 'Syncing...';
      this.style.pointerEvents = 'none';
      const link = this;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
        },
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          if (data.success) {
            link.textContent = data.message || 'Sync complete!';
            setTimeout(function () {
              window.location.reload();
            }, 1500);
          } else {
            link.textContent = data.error || 'Sync failed';
            link.style.pointerEvents = '';
          }
        })
        .catch(function () {
          link.textContent = 'Sync failed';
          link.style.pointerEvents = '';
        });
    });
  }

  /**
   * Handle "Sync from Provider" button on the change_form settings tab
   */
  function initializeSyncMethodsButton() {
    const btn = document.querySelector('.pp-sync-methods-btn');
    if (!btn) return;

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const accountId = this.dataset.accountId;
      if (!accountId) return;

      const csrfToken = getCsrf();
      const langPrefix = window.AdminUtils ? AdminUtils.getLanguagePrefix() : '';
      const url =
        langPrefix +
        '/admin/payment_providers/paymentprovideraccount/' +
        accountId +
        '/sync-payment-methods/';

      const origHtml = this.innerHTML;
      this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Syncing...';
      this.disabled = true;
      const button = this;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
        },
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          if (data.success) {
            button.innerHTML = '<i class="fas fa-check"></i> ' + (data.message || 'Sync complete!');
            setTimeout(function () {
              window.location.reload();
            }, 1500);
          } else {
            button.innerHTML =
              '<i class="fas fa-exclamation-triangle"></i> ' + (data.error || 'Sync failed');
            button.disabled = false;
            setTimeout(function () {
              button.innerHTML = origHtml;
            }, 3000);
          }
        })
        .catch(function () {
          button.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Sync failed';
          button.disabled = false;
          setTimeout(function () {
            button.innerHTML = origHtml;
          }, 3000);
        });
    });
  }

  /**
   * Initialize payment method toggle checkboxes (configure_payment_methods page)
   */
  function initializeMethodToggles() {
    const checkboxes = document.querySelectorAll('.pp-method-checkbox');
    if (!checkboxes.length) return;

    checkboxes.forEach(function (checkbox) {
      checkbox.addEventListener('change', function () {
        const accountId = this.dataset.accountId;
        const countryCode = this.dataset.countryCode;
        const methodSlug = this.dataset.methodSlug;
        const enabled = this.checked;
        const csrfToken = getCsrf();
        const langPrefix = window.AdminUtils ? AdminUtils.getLanguagePrefix() : '';

        fetch(
          langPrefix +
            '/admin/payment_providers/paymentprovideraccount/' +
            accountId +
            '/update-payment-method/',
          {
            method: 'POST',
            headers: {
              'X-CSRFToken': csrfToken,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              country_code: countryCode,
              method_slug: methodSlug,
              enabled: enabled,
            }),
          }
        )
          .then(function (r) {
            return r.json();
          })
          .then(function (data) {
            if (!data.success) {
              AdminModal.alert({
                message: data.error || i18n.error || 'Error saving change',
                type: 'error',
              });
            }
          })
          .catch(function () {
            AdminModal.alert({ message: i18n.error || 'Error saving change', type: 'error' });
          });
      });
    });
  }

  /**
   * Handle "Enable All" / "Disable All" buttons per country.
   * Sends requests sequentially to avoid race conditions on the JSONField.
   */
  function initializeToggleAllButtons() {
    const buttons = document.querySelectorAll('.pp-toggle-all-btn');
    if (!buttons.length) return;

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        const action = this.dataset.action; // 'enable' or 'disable'
        const enable = action === 'enable';
        const card = this.closest('.dashboard-card');
        if (!card) return;

        const checkboxes = Array.from(card.querySelectorAll('.pp-method-checkbox')).filter(
          function (cb) {
            return cb.checked !== enable;
          }
        );

        if (!checkboxes.length) return;

        // Disable buttons while processing
        const allBtns = card.querySelectorAll('.pp-toggle-all-btn');
        allBtns.forEach(function (b) {
          b.disabled = true;
        });

        // Send requests sequentially to prevent JSONField race conditions
        const csrfToken = getCsrf();
        const langPrefix = window.AdminUtils ? AdminUtils.getLanguagePrefix() : '';
        let idx = 0;
        const errors = [];

        function processNext() {
          if (idx >= checkboxes.length) {
            // Done — re-enable buttons
            allBtns.forEach(function (b) {
              b.disabled = false;
            });
            if (errors.length) {
              AdminModal.alert({
                message: errors.length + ' method(s) failed to update',
                type: 'error',
              });
            }
            return;
          }
          const cb = checkboxes[idx];
          idx++;
          cb.checked = enable;

          fetch(
            langPrefix +
              '/admin/payment_providers/paymentprovideraccount/' +
              cb.dataset.accountId +
              '/update-payment-method/',
            {
              method: 'POST',
              headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                country_code: cb.dataset.countryCode,
                method_slug: cb.dataset.methodSlug,
                enabled: enable,
              }),
            }
          )
            .then(function (r) {
              return r.json();
            })
            .then(function (data) {
              if (!data.success) {
                errors.push(cb.dataset.methodSlug);
                cb.checked = !enable; // Revert on failure
              }
              processNext();
            })
            .catch(function () {
              errors.push(cb.dataset.methodSlug);
              cb.checked = !enable;
              processNext();
            });
        }

        processNext();
      });
    });
  }

  /**
   * Handle "Remove" buttons on country override cards.
   * Removes the country-specific config so it falls back to global.
   */
  function initializeRemoveCountryButtons() {
    const buttons = document.querySelectorAll('.pp-remove-country-btn');
    if (!buttons.length) return;

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        const countryCode = this.dataset.country;
        if (!countryCode) return;

        const card = this.closest('.pp-country-card');
        if (!card) return;

        // Find account ID from the first checkbox in the card (or global section)
        const firstCb = document.querySelector('.pp-method-checkbox');
        const accountId = firstCb ? firstCb.dataset.accountId : '';
        if (!accountId) return;

        const csrfToken = getCsrf();
        const langPrefix = window.AdminUtils ? AdminUtils.getLanguagePrefix() : '';
        const url =
          langPrefix +
          '/admin/payment_providers/paymentprovideraccount/' +
          accountId +
          '/remove-country-override/';

        fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ country_code: countryCode }),
        })
          .then(function (r) {
            return r.json();
          })
          .then(function (data) {
            if (data.success) {
              // Remove the card from DOM
              card.style.transition = 'opacity 0.3s';
              card.style.opacity = '0';
              setTimeout(function () {
                card.remove();
              }, 300);
            } else {
              if (window.AdminModal) {
                AdminModal.alert({ message: data.error || 'Failed to remove', type: 'error' });
              }
            }
          })
          .catch(function () {
            if (window.AdminModal) {
              AdminModal.alert({ message: 'Failed to remove country override', type: 'error' });
            }
          });
      });
    });
  }

  /**
   * Get CSRF token (AdminUtils preferred, cookie fallback)
   */
  function getCsrf() {
    if (window.AdminUtils) {
      return AdminUtils.getCsrfToken();
    }
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return null;
  }
})();
