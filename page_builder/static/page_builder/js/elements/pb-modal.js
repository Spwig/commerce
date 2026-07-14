/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * PBModal — Page Builder modal popup element.
 * Extracted from page_builder/templates/page_builder/elements/modal_popup/frontend.html
 * Auto-discovers all [data-modal-id] elements on the page.
 */
(function () {
  'use strict';

  class PBModal {
    constructor(element) {
      this.modal = element;
      this.id = element.dataset.modalId;
      this.config = {
        trigger: element.dataset.trigger || 'time_delay',
        triggerSelector: element.dataset.triggerSelector || '',
        delay: parseInt(element.dataset.delay, 10) || 5,
        scrollPercent: parseInt(element.dataset.scrollPercent, 10) || 50,
        onceSession: element.dataset.onceSession === 'true',
        onceVisitor: element.dataset.onceVisitor === 'true',
        closeOnBackdrop: element.dataset.closeOnBackdrop === 'true',
        closeOnEscape: element.dataset.closeOnEscape === 'true',
        animationDuration: parseInt(element.dataset.animationDuration, 10) || 300,
      };

      this.isOpen = false;
      this.triggerElement = null;
      this.previousActiveElement = null;
      this.focusableElements = [];

      this.init();
    }

    init() {
      if (this.shouldSkip()) return;
      this.registerTrigger();
      this.registerCloseHandlers();
    }

    shouldSkip() {
      const sessionKey = `pb_modal_shown_session_${this.id}`;
      const visitorKey = `pb_modal_shown_visitor_${this.id}`;
      if (this.config.onceVisitor && localStorage.getItem(visitorKey)) return true;
      if (this.config.onceSession && sessionStorage.getItem(sessionKey)) return true;
      return false;
    }

    markAsShown() {
      const sessionKey = `pb_modal_shown_session_${this.id}`;
      const visitorKey = `pb_modal_shown_visitor_${this.id}`;
      if (this.config.onceSession) sessionStorage.setItem(sessionKey, 'true');
      if (this.config.onceVisitor) localStorage.setItem(visitorKey, 'true');
    }

    registerTrigger() {
      switch (this.config.trigger) {
        case 'button_click':
          this.registerButtonTrigger();
          break;
        case 'time_delay':
          this.registerDelayTrigger();
          break;
        case 'exit_intent':
          this.registerExitIntentTrigger();
          break;
        case 'scroll_percent':
          this.registerScrollTrigger();
          break;
        case 'page_load':
          this.open();
          break;
      }
    }

    registerButtonTrigger() {
      if (!this.config.triggerSelector) return;
      const setupTrigger = () => {
        document.querySelectorAll(this.config.triggerSelector).forEach(trigger => {
          trigger.addEventListener('click', e => {
            e.preventDefault();
            this.triggerElement = trigger;
            this.open();
          });
        });
      };
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', setupTrigger);
      } else {
        setupTrigger();
      }
    }

    registerDelayTrigger() {
      setTimeout(() => this.open(), this.config.delay * 1000);
    }

    registerExitIntentTrigger() {
      let triggered = false;
      const handleMouseLeave = e => {
        if (triggered) return;
        if (e.clientY <= 0) {
          triggered = true;
          this.open();
          document.removeEventListener('mouseout', handleMouseLeave);
        }
      };
      document.addEventListener('mouseout', handleMouseLeave);
    }

    registerScrollTrigger() {
      let triggered = false;
      const handleScroll = () => {
        if (triggered) return;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const docHeight =
          document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        if (scrollPercent >= this.config.scrollPercent) {
          triggered = true;
          this.open();
          window.removeEventListener('scroll', handleScroll);
        }
      };
      window.addEventListener('scroll', handleScroll, { passive: true });
    }

    registerCloseHandlers() {
      const closeBtn = this.modal.querySelector('[data-modal-close]');
      if (closeBtn) closeBtn.addEventListener('click', () => this.close());

      if (this.config.closeOnBackdrop) {
        const backdrop = this.modal.querySelector('.pb-modal__backdrop');
        if (backdrop) backdrop.addEventListener('click', () => this.close());
        this.modal.addEventListener('click', e => {
          if (e.target === this.modal) this.close();
        });
      }

      if (this.config.closeOnEscape) {
        document.addEventListener('keydown', e => {
          if (e.key === 'Escape' && this.isOpen) this.close();
        });
      }
    }

    open() {
      if (this.isOpen) return;
      this.isOpen = true;
      this.previousActiveElement = document.activeElement;
      this.modal.setAttribute('aria-hidden', 'false');
      document.body.classList.add('pb-modal-open');
      this.markAsShown();
      this.setupFocusTrap();
      setTimeout(() => {
        if (this.focusableElements.length > 0) this.focusableElements[0].focus();
      }, this.config.animationDuration);
      this.modal.dispatchEvent(new CustomEvent('pb-modal-open', { detail: { id: this.id } }));
    }

    close() {
      if (!this.isOpen) return;
      this.isOpen = false;
      this.modal.setAttribute('aria-hidden', 'true');
      document.body.classList.remove('pb-modal-open');
      if (this.triggerElement && document.contains(this.triggerElement)) {
        this.triggerElement.focus();
      } else if (this.previousActiveElement && document.contains(this.previousActiveElement)) {
        this.previousActiveElement.focus();
      }
      this.modal.dispatchEvent(new CustomEvent('pb-modal-close', { detail: { id: this.id } }));
    }

    setupFocusTrap() {
      const dialog = this.modal.querySelector('.pb-modal__dialog');
      if (!dialog) return;
      const focusableSelectors = [
        'a[href]',
        'button:not([disabled])',
        'input:not([disabled])',
        'select:not([disabled])',
        'textarea:not([disabled])',
        '[tabindex]:not([tabindex="-1"])',
      ];
      this.focusableElements = Array.from(
        dialog.querySelectorAll(focusableSelectors.join(', '))
      ).filter(el => el.offsetParent !== null);

      this.modal.addEventListener('keydown', e => {
        if (e.key !== 'Tab' || !this.isOpen) return;
        const firstFocusable = this.focusableElements[0];
        const lastFocusable = this.focusableElements[this.focusableElements.length - 1];
        if (e.shiftKey) {
          if (document.activeElement === firstFocusable) {
            e.preventDefault();
            lastFocusable.focus();
          }
        } else {
          if (document.activeElement === lastFocusable) {
            e.preventDefault();
            firstFocusable.focus();
          }
        }
      });
    }

    static get(id) {
      return PBModal.instances.get(id);
    }
    static openById(id) {
      const i = PBModal.get(id);
      if (i) i.open();
    }
    static closeById(id) {
      const i = PBModal.get(id);
      if (i) i.close();
    }
    static closeAll() {
      PBModal.instances.forEach(i => i.close());
    }
  }

  PBModal.instances = new Map();

  function initAllModals() {
    document.querySelectorAll('.pb-modal[data-modal-id]').forEach(function (el) {
      if (!PBModal.instances.has(el.dataset.modalId)) {
        const instance = new PBModal(el);
        PBModal.instances.set(el.dataset.modalId, instance);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAllModals);
  } else {
    initAllModals();
  }

  window.PBModal = PBModal;
})();
