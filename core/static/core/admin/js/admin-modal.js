/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * AdminModal - Centralized Modal & Toast Utility
 * ===============================================
 * Replaces native alert(), confirm(), prompt() with styled modals
 * and provides a toast notification system.
 *
 * Uses admin-modal CSS classes from admin-base.css.
 * Toast styles from admin-toast.css.
 * CSP-safe: No innerHTML with user data, no inline event handlers.
 *
 * Available globally as window.AdminModal
 *
 * Usage:
 *   await AdminModal.alert('Something happened');
 *   await AdminModal.alert({ message: 'Failed', type: 'error' });
 *
 *   if (!await AdminModal.confirm('Delete this?')) return;
 *   if (!await AdminModal.confirm({ message: 'Delete?', danger: true })) return;
 *
 *   var name = await AdminModal.prompt('Enter name:');
 *   var url = await AdminModal.prompt({ message: 'Image URL:', inputType: 'url' });
 *
 *   AdminModal.toast('Settings saved', 'success');
 *   AdminModal.toast('Connection lost', 'error', 8000);
 */

const AdminModal = (function () {
  'use strict';

  // --- State ---
  let overlay = null;
  let resolvePromise = null;
  let escHandler = null;
  let previousFocus = null;
  let toastContainer = null;
  const activeToasts = [];
  const MAX_TOASTS = 5;

  // --- Type defaults ---
  const TYPE_ICONS = {
    info: 'fa-info-circle',
    success: 'fa-check-circle',
    warning: 'fa-exclamation-triangle',
    error: 'fa-times-circle',
  };

  const TYPE_TITLES = {
    info: 'Information',
    success: 'Success',
    warning: 'Warning',
    error: 'Error',
  };

  const TOAST_ICONS = {
    info: 'fa-info-circle',
    success: 'fa-check-circle',
    warning: 'fa-exclamation-triangle',
    error: 'fa-times-circle',
  };

  // --- Helpers ---

  function makeEl(tag, className) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    return el;
  }

  function normalizeOpts(opts, defaultMessage) {
    if (typeof opts === 'string') {
      return { message: opts };
    }
    return opts || { message: defaultMessage || '' };
  }

  function getFocusableElements(container) {
    return container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
  }

  // --- Modal core ---

  function showModal(build) {
    // Dismiss any existing modal
    if (overlay) hideModal(null);

    previousFocus = document.activeElement;

    return new Promise(function (resolve) {
      resolvePromise = resolve;

      // Overlay
      overlay = makeEl('div', 'admin-modal-overlay');
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-modal', 'true');

      // Let the builder populate the modal
      const modal = makeEl('div', 'admin-modal admin-modal--sm');
      const focusTarget = build(modal, overlay);

      overlay.appendChild(modal);

      // Backdrop click
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) hideModal(null);
      });

      // Escape key
      escHandler = function (e) {
        if (e.key === 'Escape') hideModal(null);
      };
      document.addEventListener('keydown', escHandler);

      // Tab trapping
      overlay.addEventListener('keydown', function (e) {
        if (e.key !== 'Tab') return;
        const focusable = getFocusableElements(modal);
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey) {
          if (document.activeElement === first) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      });

      // Show
      document.body.appendChild(overlay);
      document.body.classList.add('admin-modal-body-locked');

      // Force reflow then activate for CSS transition
      overlay.offsetHeight;
      overlay.classList.add('active');

      // Focus
      if (focusTarget) focusTarget.focus();
    });
  }

  function hideModal(result) {
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

    // Restore focus
    if (previousFocus && previousFocus.focus) {
      try {
        previousFocus.focus();
      } catch (e) {
        /* noop */
      }
    }
    previousFocus = null;

    if (resolvePromise) {
      const fn = resolvePromise;
      resolvePromise = null;
      fn(result);
    }
  }

  function buildHeader(modal, title, icon, iconColorClass) {
    const header = makeEl('div', 'admin-modal-header');

    const titleEl = makeEl('h3', 'admin-modal-title');
    if (icon) {
      const iconEl = makeEl('i', 'fas ' + icon + (iconColorClass ? ' ' + iconColorClass : ''));
      titleEl.appendChild(iconEl);
    }
    titleEl.appendChild(document.createTextNode((icon ? ' ' : '') + title));
    header.appendChild(titleEl);

    const closeBtn = makeEl('button', 'admin-modal-close');
    closeBtn.setAttribute('type', 'button');
    closeBtn.setAttribute('aria-label', 'Close');
    const closeIcon = makeEl('i', 'fas fa-times');
    closeBtn.appendChild(closeIcon);
    closeBtn.addEventListener('click', function () {
      hideModal(null);
    });
    header.appendChild(closeBtn);

    modal.appendChild(header);
    return header;
  }

  // --- AdminModal.alert ---

  function alertModal(opts) {
    opts = normalizeOpts(opts, 'Notice');
    const type = opts.type || 'info';
    const title = opts.title || TYPE_TITLES[type] || 'Information';
    const message = opts.message || '';
    const icon = opts.icon || TYPE_ICONS[type] || 'fa-info-circle';
    const dismissText = opts.dismissText || 'OK';
    const iconColorClass = 'admin-modal-icon--' + type;

    return showModal(function (modal) {
      buildHeader(modal, title, icon, iconColorClass);

      // Body
      const body = makeEl('div', 'admin-modal-body');
      const msgEl = makeEl('p');
      msgEl.textContent = message;
      body.appendChild(msgEl);
      modal.appendChild(body);

      // Footer - single dismiss button
      const footer = makeEl('div', 'admin-modal-footer');
      const dismissBtn = makeEl('button', 'button btn-primary');
      dismissBtn.setAttribute('type', 'button');
      dismissBtn.textContent = dismissText;
      dismissBtn.addEventListener('click', function () {
        hideModal(undefined);
      });
      footer.appendChild(dismissBtn);
      modal.appendChild(footer);

      return dismissBtn;
    });
  }

  // --- AdminModal.confirm ---

  function confirmModal(opts) {
    opts = normalizeOpts(opts, 'Are you sure?');
    const title = opts.title || 'Confirm';
    const message = opts.message || 'Are you sure?';
    const confirmText = opts.confirmText || 'Confirm';
    const cancelText = opts.cancelText || 'Cancel';
    const icon = opts.icon || 'fa-question-circle';
    const danger = opts.danger || false;

    return showModal(function (modal) {
      buildHeader(modal, title, icon, danger ? 'admin-modal-icon--error' : '');

      // Body
      const body = makeEl('div', 'admin-modal-body');
      const msgEl = makeEl('p');
      msgEl.textContent = message;
      body.appendChild(msgEl);
      modal.appendChild(body);

      // Footer
      const footer = makeEl('div', 'admin-modal-footer');

      const cancelBtn = makeEl('button', 'button');
      cancelBtn.setAttribute('type', 'button');
      cancelBtn.textContent = cancelText;
      cancelBtn.addEventListener('click', function () {
        hideModal(false);
      });
      footer.appendChild(cancelBtn);

      const confirmBtn = makeEl(
        'button',
        danger ? 'button admin-modal-btn--danger' : 'button btn-primary'
      );
      confirmBtn.setAttribute('type', 'button');
      if (icon && !danger) {
        const btnIcon = makeEl('i', 'fas ' + icon);
        confirmBtn.appendChild(btnIcon);
        confirmBtn.appendChild(document.createTextNode(' '));
      }
      confirmBtn.appendChild(document.createTextNode(confirmText));
      confirmBtn.addEventListener('click', function () {
        hideModal(true);
      });
      footer.appendChild(confirmBtn);

      modal.appendChild(footer);

      return confirmBtn;
    });
  }

  // --- AdminModal.prompt ---

  function promptModal(opts) {
    opts = normalizeOpts(opts, 'Enter a value:');
    const title = opts.title || 'Input Required';
    const message = opts.message || 'Enter a value:';
    const placeholder = opts.placeholder || '';
    const defaultValue = opts.defaultValue || '';
    const confirmText = opts.confirmText || 'OK';
    const cancelText = opts.cancelText || 'Cancel';
    const inputType = opts.inputType || 'text';

    return showModal(function (modal) {
      buildHeader(modal, title, 'fa-edit', 'admin-modal-icon--info');

      // Body
      const body = makeEl('div', 'admin-modal-body');
      const msgEl = makeEl('p');
      msgEl.textContent = message;
      body.appendChild(msgEl);

      const input = makeEl('input', 'admin-modal-input');
      input.setAttribute('type', inputType);
      if (placeholder) input.setAttribute('placeholder', placeholder);
      input.value = defaultValue;
      body.appendChild(input);
      modal.appendChild(body);

      // Enter key in input submits
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          hideModal(input.value);
        }
      });

      // Footer
      const footer = makeEl('div', 'admin-modal-footer');

      const cancelBtn = makeEl('button', 'button');
      cancelBtn.setAttribute('type', 'button');
      cancelBtn.textContent = cancelText;
      cancelBtn.addEventListener('click', function () {
        hideModal(null);
      });
      footer.appendChild(cancelBtn);

      const confirmBtn = makeEl('button', 'button btn-primary');
      confirmBtn.setAttribute('type', 'button');
      confirmBtn.textContent = confirmText;
      confirmBtn.addEventListener('click', function () {
        hideModal(input.value);
      });
      footer.appendChild(confirmBtn);

      modal.appendChild(footer);

      return input;
    });
  }

  // --- AdminModal.toast ---

  function ensureToastContainer() {
    if (toastContainer && toastContainer.parentNode) return toastContainer;
    toastContainer = makeEl('div', 'admin-toast-container');
    document.body.appendChild(toastContainer);
    return toastContainer;
  }

  function dismissToast(toast, timerId) {
    if (toast._dismissed) return;
    toast._dismissed = true;

    if (timerId) clearTimeout(timerId);
    toast.classList.add('exiting');

    // Remove from tracking
    const idx = activeToasts.indexOf(toast);
    if (idx > -1) activeToasts.splice(idx, 1);

    setTimeout(function () {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 300);
  }

  function toast(message, type, duration) {
    type = type || 'info';
    if (typeof duration === 'undefined') duration = 4000;
    const icon = TOAST_ICONS[type] || TOAST_ICONS.info;

    const container = ensureToastContainer();

    // Enforce max toasts
    while (activeToasts.length >= MAX_TOASTS) {
      dismissToast(activeToasts[0]);
    }

    const el = makeEl('div', 'admin-toast admin-toast--' + type);

    // Icon
    const iconEl = makeEl('i', 'admin-toast-icon fas ' + icon);
    el.appendChild(iconEl);

    // Message
    const msgEl = makeEl('span', 'admin-toast-message');
    msgEl.textContent = message;
    el.appendChild(msgEl);

    // Close button
    const closeBtn = makeEl('button', 'admin-toast-close');
    closeBtn.setAttribute('type', 'button');
    closeBtn.setAttribute('aria-label', 'Dismiss');
    const closeIcon = makeEl('i', 'fas fa-times');
    closeBtn.appendChild(closeIcon);
    el.appendChild(closeBtn);

    activeToasts.push(el);
    container.appendChild(el);

    // Auto-dismiss timer
    let timerId = null;
    let remaining = duration;
    let startTime = null;

    function startTimer() {
      if (remaining <= 0) return;
      startTime = Date.now();
      timerId = setTimeout(function () {
        dismissToast(el, null);
      }, remaining);
    }

    function pauseTimer() {
      if (timerId) {
        clearTimeout(timerId);
        timerId = null;
        remaining -= Date.now() - startTime;
        if (remaining < 0) remaining = 0;
      }
    }

    if (duration > 0) {
      startTimer();

      // Pause on hover
      el.addEventListener('mouseenter', pauseTimer);
      el.addEventListener('mouseleave', startTimer);
    }

    // Close button
    closeBtn.addEventListener('click', function () {
      dismissToast(el, timerId);
    });
  }

  // --- Public API ---
  return {
    alert: alertModal,
    confirm: confirmModal,
    prompt: promptModal,
    toast: toast,
  };
})();
