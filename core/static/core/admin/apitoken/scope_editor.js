/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* Progressive enhancement for the API token scope picker.
   The picker works without JS (plain radios); this only adds the per-group
   "Clear group" convenience. CSP-safe: no inline handlers. */

(function () {
  'use strict';

  function clearGroup(group) {
    // Check the "No access" radio (empty value) in every row of the group.
    var radios = group.querySelectorAll('input[type="radio"][value=""]');
    radios.forEach(function (radio) {
      radio.checked = true;
    });
  }

  function init() {
    var editor = document.querySelector('[data-scope-editor]');
    if (!editor) {
      return;
    }
    editor.addEventListener('click', function (event) {
      var button = event.target.closest('[data-action="clear-group"]');
      if (!button) {
        return;
      }
      event.preventDefault();
      var group = button.closest('.scope-group');
      if (group) {
        clearGroup(group);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
