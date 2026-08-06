/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/*
 * Region confirmation modal.
 *
 * Auto-detection has already applied the visitor's region; the modal (rendered
 * server-side only on first visit — see catalog.context_processors.region_suggestion)
 * confirms it and lets them change it:
 *   - Change country: POST the chosen country to /api/set-region/ and reload.
 *   - Keep browsing / dismiss: remember the choice in a cookie so it never nags again.
 */
(function () {
  'use strict';

  if (window._regionSuggestionInit) {
    return;
  }
  window._regionSuggestionInit = true;

  var DISMISS_COOKIE = 'region_prompt_dismissed';
  var COOKIE_MAX_AGE = 60 * 60 * 24 * 365; // 1 year

  function setCookie(name, value) {
    document.cookie = name + '=' + value + '; path=/; max-age=' + COOKIE_MAX_AGE + '; SameSite=Lax';
  }

  function getCsrfToken() {
    var meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) {
      return meta.content;
    }
    var input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
  }

  function open(modal) {
    modal.classList.remove('hidden');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    var focusable = modal.querySelector('button');
    if (focusable) {
      focusable.focus();
    }
  }

  function dismiss(modal) {
    setCookie(DISMISS_COOKIE, '1');
    modal.classList.add('hidden');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  function switchRegion(modal, country) {
    var url = modal.dataset.regionUrl;
    if (!country || !url) {
      dismiss(modal);
      return;
    }
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({ country: country }),
    })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('set-region failed');
        }
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          window.location.reload();
        } else {
          dismiss(modal);
        }
      })
      .catch(function () {
        dismiss(modal);
      });
  }

  function init() {
    var modal = document.getElementById('region-suggestion-modal');
    if (!modal) {
      return;
    }

    modal.querySelectorAll('[data-region-dismiss]').forEach(function (el) {
      el.addEventListener('click', function () {
        dismiss(modal);
      });
    });

    var select = modal.querySelector('[data-region-select]');
    if (select) {
      select.addEventListener('change', function () {
        if (select.value) {
          switchRegion(modal, select.value);
        }
      });
    }

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
        dismiss(modal);
      }
    });

    open(modal);
  }

  document.addEventListener('DOMContentLoaded', init);
})();
