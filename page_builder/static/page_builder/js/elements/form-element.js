/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Form element initializer: reads form data from JSON data island and initializes DynamicForm.
 * Auto-initializes all [data-form-id] containers that have a matching #fb-form-data-{id} island.
 */
(function () {
  'use strict';

  function initFormElement(formContainer) {
    const formId = formContainer.dataset.formId;
    const dataIsland = document.getElementById('fb-form-data-' + formId);
    if (!dataIsland) return;

    let formData;
    try {
      formData = JSON.parse(dataIsland.textContent);
    } catch (e) {
      return;
    }

    if (window.DynamicForm) {
      new window.DynamicForm(formContainer, formData);
    }
  }

  function init() {
    document.querySelectorAll('[data-form-id]').forEach(initFormElement);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
