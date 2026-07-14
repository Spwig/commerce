/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Provider Confirm Modal
 * ======================
 * Reusable styled confirmation dialog for provider actions (update, delete, etc.).
 * Returns a Promise that resolves to true (confirmed) or false (cancelled).
 *
 * Uses the admin-modal CSS classes from admin-base.css.
 * CSP-safe: No inline styles, no inline event handlers, no innerHTML with external data.
 *
 * Usage:
 *   const confirmed = await ProviderConfirm.show({
 *       title: 'Update Provider',
 *       message: 'Update DeepL to version 1.0.2?',
 *       confirmText: 'Update',
 *       cancelText: 'Cancel'
 *   });
 *   if (!confirmed) return;
 */

const ProviderConfirm = (function () {
  'use strict';

  let overlay = null;
  let resolvePromise = null;
  let escHandler = null;

  function makeEl(tag, className) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    return el;
  }

  function show(opts) {
    // Dismiss any existing modal
    if (overlay) hide(false);

    const title = opts.title || 'Confirm';
    const message = opts.message || 'Are you sure?';
    const confirmText = opts.confirmText || 'Confirm';
    const cancelText = opts.cancelText || 'Cancel';
    const icon = opts.icon || 'fa-sync-alt';

    return new Promise(function (resolve) {
      resolvePromise = resolve;

      // Overlay
      overlay = makeEl('div', 'admin-modal-overlay');
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-modal', 'true');

      // Modal container
      const modal = makeEl('div', 'admin-modal admin-modal--sm');

      // Header
      const header = makeEl('div', 'admin-modal-header');
      const titleEl = makeEl('h3', 'admin-modal-title');
      const titleIcon = makeEl('i', 'fas ' + icon);
      titleEl.appendChild(titleIcon);
      titleEl.appendChild(document.createTextNode(' ' + title));
      header.appendChild(titleEl);

      const closeBtn = makeEl('button', 'admin-modal-close');
      closeBtn.setAttribute('type', 'button');
      closeBtn.setAttribute('aria-label', 'Close');
      const closeIcon = makeEl('i', 'fas fa-times');
      closeBtn.appendChild(closeIcon);
      header.appendChild(closeBtn);

      // Body
      const body = makeEl('div', 'admin-modal-body');
      const msgEl = makeEl('p');
      msgEl.textContent = message;
      body.appendChild(msgEl);

      // Footer
      const footer = makeEl('div', 'admin-modal-footer');

      const cancelBtn = makeEl('button', 'button');
      cancelBtn.setAttribute('type', 'button');
      cancelBtn.textContent = cancelText;

      const confirmBtn = makeEl('button', 'button btn-primary');
      confirmBtn.setAttribute('type', 'button');
      const confirmIcon = makeEl('i', 'fas ' + icon);
      confirmBtn.appendChild(confirmIcon);
      confirmBtn.appendChild(document.createTextNode(' ' + confirmText));

      footer.appendChild(cancelBtn);
      footer.appendChild(confirmBtn);

      // Assemble
      modal.appendChild(header);
      modal.appendChild(body);
      modal.appendChild(footer);
      overlay.appendChild(modal);

      // Event listeners
      closeBtn.addEventListener('click', function () {
        hide(false);
      });
      cancelBtn.addEventListener('click', function () {
        hide(false);
      });
      confirmBtn.addEventListener('click', function () {
        hide(true);
      });

      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) hide(false);
      });

      escHandler = function (e) {
        if (e.key === 'Escape') hide(false);
      };
      document.addEventListener('keydown', escHandler);

      // Show
      document.body.appendChild(overlay);
      document.body.classList.add('admin-modal-body-locked');

      // Trigger reflow then activate for CSS transition
      overlay.offsetHeight; // force reflow
      overlay.classList.add('active');

      // Focus the confirm button
      confirmBtn.focus();
    });
  }

  function hide(result) {
    if (!overlay) return;

    overlay.classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');

    if (escHandler) {
      document.removeEventListener('keydown', escHandler);
      escHandler = null;
    }

    // Wait for CSS transition then remove
    const el = overlay;
    setTimeout(function () {
      if (el.parentNode) el.parentNode.removeChild(el);
    }, 300);

    overlay = null;

    if (resolvePromise) {
      resolvePromise(result);
      resolvePromise = null;
    }
  }

  return { show: show };
})();
