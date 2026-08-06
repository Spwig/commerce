/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  if (window._widgetShipToInit) {
    return;
  }
  window._widgetShipToInit = true;

  function initWidget(widget) {
    if (widget.dataset.shipToInitialized) {
      return;
    }
    widget.dataset.shipToInitialized = 'true';

    const regionUrl = widget.dataset.regionUrl || '';
    const select = widget.querySelector('.ship-to-select');
    if (!select) {
      return;
    }

    const meta = document.querySelector('meta[name="csrf-token"]');
    let csrfToken = meta && meta.content ? meta.content : '';
    if (!csrfToken) {
      const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
      csrfToken = csrfInput ? csrfInput.value : '';
    }

    select.addEventListener('change', function () {
      if (select.value) {
        changeRegion(select.value, regionUrl, csrfToken, widget);
      }
    });
  }

  function changeRegion(countryCode, regionUrl, csrfToken, widget) {
    const loading = widget.querySelector('.ship-to-loading');
    if (loading) {
      loading.hidden = false;
    }

    fetch(regionUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ country: countryCode }),
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Ship-to change failed');
        }
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          window.location.reload();
        } else {
          console.error('Ship-to change failed:', data.error);
          if (loading) {
            loading.hidden = true;
          }
        }
      })
      .catch(function () {
        if (loading) {
          loading.hidden = true;
        }
      });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.widget-ship-to[data-widget-id]').forEach(initWidget);
  });
})();
