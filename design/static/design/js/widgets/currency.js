/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  if (window._widgetCurrencyInit) {
    return;
  }
  window._widgetCurrencyInit = true;

  function initWidget(widget) {
    if (widget.dataset.currencyInitialized) {
      return;
    }
    widget.dataset.currencyInitialized = 'true';

    const currencyUrl = widget.dataset.currencyUrl || '';
    const showCurrentOnly = widget.dataset.showCurrentOnly === 'true';
    const meta = document.querySelector('meta[name="csrf-token"]');
    let csrfToken = meta && meta.content ? meta.content : '';
    if (!csrfToken) {
      const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
      csrfToken = csrfInput ? csrfInput.value : '';
    }

    if (showCurrentOnly) {
      const button = widget.querySelector('.currency-button');
      const dropdown = widget.querySelector('.currency-dropdown');
      const options = dropdown ? dropdown.querySelectorAll('.currency-option') : [];

      if (!button || !dropdown) {
        return;
      }

      button.addEventListener('click', function (e) {
        e.stopPropagation();
        dropdown.hidden = !dropdown.hidden;
        button.setAttribute('aria-expanded', String(!dropdown.hidden));
      });

      document.addEventListener('click', function (e) {
        if (!widget.contains(e.target)) {
          dropdown.hidden = true;
          button.setAttribute('aria-expanded', 'false');
        }
      });

      Array.prototype.forEach.call(options, function (option) {
        option.addEventListener('click', function () {
          const currency = option.dataset.currency;
          changeCurrency(currency, currencyUrl, csrfToken, widget);
          dropdown.hidden = true;
          button.setAttribute('aria-expanded', 'false');
        });
      });

      button.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          button.click();
        }
      });
    } else {
      const select = widget.querySelector('.currency-select');
      if (!select) {
        return;
      }

      select.addEventListener('change', function () {
        changeCurrency(select.value, currencyUrl, csrfToken, widget);
      });
    }
  }

  function changeCurrency(currencyCode, currencyUrl, csrfToken, widget) {
    const loading = widget.querySelector('.currency-loading');
    if (loading) {
      loading.hidden = false;
    }

    setCookie('selected_currency', currencyCode, 365);

    fetch(currencyUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ currency: currencyCode }),
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Currency change failed');
        }
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          window.location.reload();
        } else {
          console.error('Currency change failed:', data.error);
          if (loading) {
            loading.hidden = true;
          }
        }
      })
      .catch(function () {
        window.location.href = window.location.pathname + '?currency=' + currencyCode;
      });
  }

  function setCookie(name, value, days) {
    let expires = '';
    if (days) {
      const date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + value + expires + '; path=/; SameSite=Lax';
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.widget-currency[data-widget-id]').forEach(initWidget);
  });
})();
