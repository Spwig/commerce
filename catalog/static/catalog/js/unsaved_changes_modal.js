/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Unsaved Changes Modal
 * Intercepts navigation to external editors (Design Editor, 3D Configurator)
 * when the product form has unsaved changes.
 *
 * Dirty state is detected via data-dirty="true" on #product-form, set by
 * initDirtyTracking() in admin_product_form.js.
 */
(function () {
  'use strict';

  const STORAGE_KEY = 'product_editor_redirect';
  let pendingUrl = null;
  const overlay = document.getElementById('unsaved-changes-modal');
  const form = document.getElementById('product-form');

  // On page load, check if we need to redirect after a save
  const redirectUrl = sessionStorage.getItem(STORAGE_KEY);
  if (redirectUrl) {
    sessionStorage.removeItem(STORAGE_KEY);
    window.location.href = redirectUrl;
    return;
  }

  if (!overlay || !form) return;

  function isFormDirty() {
    return form.dataset.dirty === 'true';
  }

  function showModal(url) {
    pendingUrl = url;
    overlay.classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
  }

  function hideModal() {
    overlay.classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
    pendingUrl = null;
  }

  // Intercept clicks on editor launch buttons
  document.querySelectorAll('.viewer-3d-launch-btn').forEach(function (link) {
    link.addEventListener('click', function (e) {
      if (isFormDirty()) {
        e.preventDefault();
        showModal(link.href);
      }
      // If not dirty, normal navigation proceeds
    });
  });

  // Cancel / close buttons
  const cancelBtn = document.getElementById('unsaved-modal-cancel');
  const closeBtn = document.getElementById('unsaved-modal-close');
  if (cancelBtn) cancelBtn.addEventListener('click', hideModal);
  if (closeBtn) closeBtn.addEventListener('click', hideModal);

  // Click outside to close
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) hideModal();
  });

  // Save & Continue - save form then redirect to editor
  const saveBtn = document.getElementById('unsaved-modal-save');
  if (saveBtn) {
    saveBtn.addEventListener('click', function () {
      if (!pendingUrl) return;
      // Store where to redirect after save
      sessionStorage.setItem(STORAGE_KEY, pendingUrl);
      // Clear dirty state so beforeunload handler doesn't block the submit
      delete form.dataset.dirty;
      // Submit the form with _continue so Django redirects back to the change form
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = '_continue';
      input.value = '1';
      form.appendChild(input);
      form.submit();
    });
  }
})();
