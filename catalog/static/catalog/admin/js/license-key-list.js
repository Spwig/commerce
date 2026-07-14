/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  document.addEventListener('click', function (e) {
    const btn = e.target.classList.contains('copy-license-key')
      ? e.target
      : e.target.closest('.copy-license-key');
    if (!btn) return;

    const key = btn.dataset.key;
    if (!key) return;

    navigator.clipboard.writeText(key).then(function () {
      const originalHTML = btn.innerHTML;
      btn.innerHTML = '<i class="fas fa-check"></i>';
      btn.style.color = 'var(--success-fg)';
      setTimeout(function () {
        btn.innerHTML = originalHTML;
        btn.style.color = '';
      }, 2000);
    });
  });
})();
