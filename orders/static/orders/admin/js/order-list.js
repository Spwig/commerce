/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* Orders changelist: auto-submit the filters form when a dropdown changes.
   (Stat tiles and the quick search are plain GET links/forms; the bulk-actions
   bar is handled by card-bulk-actions.js.) */
(function () {
  'use strict';
  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('orders-filters');
    if (!form) return;
    form.querySelectorAll('select[data-autosubmit]').forEach(function (sel) {
      sel.addEventListener('change', function () {
        form.submit();
      });
    });
  });
})();
