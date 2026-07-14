/**
 * StorefrontModal — lightweight, reusable modal utility for the storefront.
 *
 * Usage:
 *   StorefrontModal.open({ title, body, footer, size, onOpen, onClose })
 *   StorefrontModal.prompt({ title, label, placeholder, value, help, submitText, onSubmit, onCancel })
 *   StorefrontModal.close(modalEl)
 *   StorefrontModal.closeAll()
 */
(function () {
  'use strict';

  const stack = []; // open modal stack (for nested modals / escape handling)

  /* ------------------------------------------------------------------ */
  /*  Helpers                                                            */
  /* ------------------------------------------------------------------ */

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  function createEl(tag, className, attrs) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (attrs) {
      for (const k in attrs) {
        if (attrs.hasOwnProperty(k)) el.setAttribute(k, attrs[k]);
      }
    }
    return el;
  }

  /* ------------------------------------------------------------------ */
  /*  Core: open / close                                                 */
  /* ------------------------------------------------------------------ */

  function open(options) {
    options = options || {};

    const id = 'sf-modal-' + Date.now() + '-' + Math.random().toString(36).substr(2, 5);

    // Overlay
    const overlay = createEl('div', 'sf-modal', { id: id, role: 'dialog', 'aria-modal': 'true' });

    // Backdrop
    const backdrop = createEl('div', 'sf-modal__backdrop');
    overlay.appendChild(backdrop);

    // Dialog
    const sizeClass = options.size ? ' sf-modal__dialog--' + options.size : '';
    const dialog = createEl('div', 'sf-modal__dialog' + sizeClass);

    // Header
    if (options.title) {
      const titleId = id + '-title';
      overlay.setAttribute('aria-labelledby', titleId);

      const header = createEl('div', 'sf-modal__header');
      const title = createEl('h3', 'sf-modal__title', { id: titleId });
      title.textContent = options.title;
      header.appendChild(title);

      const closeBtn = createEl('button', 'sf-modal__close', {
        type: 'button',
        'aria-label': 'Close',
      });
      closeBtn.innerHTML = '&times;';
      closeBtn.addEventListener('click', function () {
        close(overlay);
      });
      header.appendChild(closeBtn);
      dialog.appendChild(header);
    }

    // Body
    const body = createEl('div', 'sf-modal__body');
    if (options.body) body.innerHTML = options.body;
    dialog.appendChild(body);

    // Footer
    if (options.footer) {
      const footer = createEl('div', 'sf-modal__footer');
      footer.innerHTML = options.footer;
      dialog.appendChild(footer);
    }

    overlay.appendChild(dialog);
    document.body.appendChild(overlay);

    // Store callbacks on the element
    overlay._sfOnClose = options.onClose || null;

    // Backdrop click to close
    if (options.closeOnBackdrop !== false) {
      backdrop.addEventListener('click', function () {
        close(overlay);
      });
    }

    // Activate (next frame for CSS transition)
    requestAnimationFrame(function () {
      overlay.classList.add('sf-modal--active');
    });

    // Body scroll lock
    document.body.classList.add('sf-modal-open');

    // Push to stack
    stack.push(overlay);

    // Focus first focusable element inside body
    requestAnimationFrame(function () {
      const focusable = body.querySelector(
        'input, textarea, select, button, [tabindex]:not([tabindex="-1"]), a[href]'
      );
      if (focusable) focusable.focus();
    });

    if (options.onOpen) options.onOpen(overlay);

    return overlay;
  }

  function close(modal) {
    if (!modal || !modal.parentNode) return;

    modal.classList.remove('sf-modal--active');

    const onClose = modal._sfOnClose;

    // Wait for transition
    setTimeout(function () {
      if (modal.parentNode) modal.parentNode.removeChild(modal);
    }, 220);

    // Remove from stack
    const idx = stack.indexOf(modal);
    if (idx !== -1) stack.splice(idx, 1);

    // Body scroll unlock if no more modals
    if (stack.length === 0) {
      document.body.classList.remove('sf-modal-open');
    }

    if (onClose) onClose();
  }

  function closeAll() {
    // Close in reverse order
    const copy = stack.slice();
    for (let i = copy.length - 1; i >= 0; i--) {
      close(copy[i]);
    }
  }

  /* ------------------------------------------------------------------ */
  /*  Convenience: prompt                                                */
  /* ------------------------------------------------------------------ */

  function prompt(options) {
    options = options || {};

    const inputId = 'sf-modal-prompt-input-' + Date.now();
    const bodyHtml =
      '<div class="sf-modal__form-group">' +
      (options.label
        ? '<label class="sf-modal__label" for="' +
          inputId +
          '">' +
          escapeHtml(options.label) +
          '</label>'
        : '') +
      '<input type="text" id="' +
      inputId +
      '" class="sf-modal__input"' +
      (options.placeholder ? ' placeholder="' + escapeHtml(options.placeholder) + '"' : '') +
      (options.value ? ' value="' + escapeHtml(options.value) + '"' : '') +
      '>' +
      (options.help ? '<p class="sf-modal__help">' + escapeHtml(options.help) + '</p>' : '') +
      '</div>';

    const submitText = options.submitText || 'Save';
    const cancelText = options.cancelText || 'Cancel';

    const footerHtml =
      '<button type="button" class="sf-modal__btn sf-modal__btn--outline" data-sf-action="cancel">' +
      escapeHtml(cancelText) +
      '</button>' +
      '<button type="button" class="sf-modal__btn sf-modal__btn--primary" data-sf-action="submit">' +
      escapeHtml(submitText) +
      '</button>';

    const modal = open({
      title: options.title || '',
      body: bodyHtml,
      footer: footerHtml,
      size: options.size || 'sm',
      closeOnBackdrop: options.closeOnBackdrop !== false,
      onClose: options.onCancel || null,
    });

    const input = modal.querySelector('#' + inputId);
    const submitBtn = modal.querySelector('[data-sf-action="submit"]');
    const cancelBtn = modal.querySelector('[data-sf-action="cancel"]');

    function doSubmit() {
      const val = input ? input.value : '';
      if (!val.trim()) {
        // Shake the input to indicate it's required
        if (input) {
          input.style.borderColor = 'var(--theme-color-error, #ef4444)';
          input.focus();
          setTimeout(function () {
            input.style.borderColor = '';
          }, 1500);
        }
        return;
      }
      // Detach onClose so cancel callback doesn't fire
      modal._sfOnClose = null;
      close(modal);
      if (options.onSubmit) options.onSubmit(val.trim());
    }

    if (submitBtn) submitBtn.addEventListener('click', doSubmit);
    if (cancelBtn) {
      cancelBtn.addEventListener('click', function () {
        close(modal);
      });
    }

    // Enter key submits
    if (input) {
      input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          doSubmit();
        }
      });
    }

    return modal;
  }

  /* ------------------------------------------------------------------ */
  /*  Global escape key handler                                          */
  /* ------------------------------------------------------------------ */

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && stack.length > 0) {
      e.preventDefault();
      close(stack[stack.length - 1]);
    }
  });

  /* ------------------------------------------------------------------ */
  /*  Public API                                                         */
  /* ------------------------------------------------------------------ */

  window.StorefrontModal = {
    open: open,
    close: close,
    closeAll: closeAll,
    prompt: prompt,
  };
})();
