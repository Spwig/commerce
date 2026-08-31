/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* Per-recipient activity timeline modal. The recipient list itself is driven by the
   shared admin-list-filters.js; this only wires the per-row "View activity" action to
   fetch its event timeline and show it in the shared admin modal. CSP-safe (no inline JS). */
(function () {
  'use strict';

  var overlay = document.getElementById('em-activity-modal');
  var body = document.getElementById('em-activity-body');
  if (!overlay || !body) return;

  function open() {
    overlay.classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
  }

  function close() {
    overlay.classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
    body.innerHTML = '';
  }

  function loadActivity(url) {
    body.innerHTML = '<p class="em-activity-loading"><i class="fas fa-spinner fa-spin"></i></p>';
    open();
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest', Accept: 'application/json' } })
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (d) {
        body.innerHTML = d.html || '';
      })
      .catch(function () {
        body.innerHTML = '<p class="error">Failed to load activity. Please try again.</p>';
      });
  }

  // Delegated: recipient cards are injected by admin-list-filters after page load.
  document.addEventListener('click', function (e) {
    var trigger = e.target.closest('[data-activity-url]');
    if (trigger) {
      e.preventDefault();
      loadActivity(trigger.getAttribute('data-activity-url'));
      return;
    }
    if (e.target === overlay || e.target.closest('[data-modal-close]')) {
      close();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && overlay.classList.contains('active')) close();
  });
})();
