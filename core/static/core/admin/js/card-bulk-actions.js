/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/*
 * Select-all + live counter for the shared card-changelist bulk-actions bar
 * (templates/admin/includes/bulk_actions_open.html). Django's own actions.js
 * only wires table-row checkboxes, so card layouts need this.
 *
 * Self-contained and AJAX-safe: the change listener is delegated on the form,
 * and every count queries the checkboxes live, so results reloaded by the
 * filter modules keep working without re-initialisation.
 */
(function () {
  'use strict';

  function init() {
    var form = document.getElementById('changelist-form');
    if (!form || form.dataset.cbaWired) {
      return;
    }
    form.dataset.cbaWired = '1';

    var selectAll = form.querySelector('[data-select-all]');
    var counter = form.querySelector('[data-action-counter]');

    function boxes() {
      return form.querySelectorAll('input.action-select');
    }
    function checkedCount() {
      return form.querySelectorAll('input.action-select:checked').length;
    }
    function update() {
      var total = boxes().length;
      var checked = checkedCount();
      if (counter) {
        var of = counter.getAttribute('data-of-label') || 'of';
        var txt = checked + ' ' + of + ' ' + total;
        // Only write when the value actually changes — writing textContent is a
        // DOM mutation, so an unconditional write here would loop forever if
        // anything observes this subtree.
        if (counter.textContent !== txt) {
          counter.textContent = txt;
        }
      }
      if (selectAll) {
        selectAll.checked = total > 0 && checked === total;
        selectAll.indeterminate = checked > 0 && checked < total;
      }
    }

    if (selectAll) {
      selectAll.addEventListener('change', function () {
        var on = selectAll.checked;
        boxes().forEach(function (cb) {
          cb.checked = on;
        });
        update();
      });
    }

    // Delegated: catches checkboxes added by AJAX list reloads too.
    form.addEventListener('change', function (e) {
      if (e.target && e.target.matches && e.target.matches('input.action-select')) {
        update();
      }
    });

    update();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
