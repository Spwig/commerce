/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Gift card balance lookup.
 *
 * The page is a shell; POST /api/catalog/gift-cards/check-balance/ owns the
 * security posture (throttles, uniform 404, kill switch). Whatever the server
 * refuses — unknown code, expired, disabled endpoint — renders as the ONE
 * generic error, deliberately: distinguishing cases here would rebuild the
 * enumeration oracle the uniform response exists to prevent.
 */
(function () {
  'use strict';

  const section = document.querySelector('.gc-balance');
  if (!section) return;
  const endpoint = section.dataset.endpoint;
  const form = document.getElementById('gc-balance-form');
  const input = document.getElementById('gc-code');
  const result = document.getElementById('gc-result');
  const amount = document.getElementById('gc-amount');
  const meta = document.getElementById('gc-meta');
  const error = document.getElementById('gc-error');

  function getCsrfToken() {
    // CSRF_COOKIE_HTTPONLY=True: the cookie is unreadable from JS, so the
    // token comes from the base template's meta tag or a rendered form
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const code = input.value.trim().toUpperCase();
    if (!code) return;

    result.hidden = true;
    error.hidden = true;

    try {
      const resp = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        body: JSON.stringify({ code: code }),
        credentials: 'same-origin',
      });
      const data = await resp.json().catch(() => null);

      if (!resp.ok || !data || data.success === false) {
        error.hidden = false;
        return;
      }

      const card = data.gift_card || data;
      const balance = card.current_balance || {};
      amount.textContent = `${balance.amount ?? ''} ${balance.currency ?? ''}`.trim();
      meta.textContent = card.expires_at ? new Date(card.expires_at).toLocaleDateString() : '';
      result.hidden = false;
    } catch (err) {
      error.hidden = false;
    }
  });
})();
