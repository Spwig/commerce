/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Email Template List - CSP Compliant
 * Handles template list filtering and delete modal
 * Version: 2026.02.14
 */

(function () {
  'use strict';

  /**
   * Show delete confirmation modal
   */
  function showDeleteModal(templateId, templateName) {
    const modal = document.getElementById('deleteModal');
    if (!modal) return;

    // Get translation strings from data attributes or use defaults
    const confirmMsg = modal.dataset.confirmMsg || 'Are you sure you want to delete the template';
    const warningMsg = modal.dataset.warningMsg || 'This action cannot be undone.';

    const message = `${confirmMsg} "${templateName}"? ${warningMsg}`;
    const messageEl = document.getElementById('deleteMessage');
    const deleteForm = document.getElementById('deleteForm');

    if (messageEl) {
      messageEl.textContent = message;
    }

    if (deleteForm) {
      // Replace placeholder UUID with actual template ID
      const actionUrl = deleteForm.dataset.urlTemplate.replace(
        '00000000-0000-0000-0000-000000000000',
        templateId
      );
      deleteForm.action = actionUrl;
    }

    modal.classList.add('active');
  }

  /**
   * Hide delete confirmation modal
   */
  function hideDeleteModal() {
    const modal = document.getElementById('deleteModal');
    if (modal) {
      modal.classList.remove('active');
    }
  }

  /**
   * Handle all template list actions via event delegation
   */
  function handleTemplateActions(e) {
    // Find the nearest element with data-action
    const actionElement = e.target.closest('[data-action]');
    if (!actionElement) return;

    const action = actionElement.dataset.action;
    if (!action) return;

    switch (action) {
      case 'confirm-delete':
        e.preventDefault();
        const templateId = actionElement.dataset.templateId;
        const templateName = actionElement.dataset.templateName;
        if (templateId && templateName) {
          showDeleteModal(templateId, templateName);
        }
        break;
      case 'hide-delete-modal':
        e.preventDefault();
        hideDeleteModal();
        break;
    }
  }

  /**
   * Handle filter form changes - auto-submit on change
   */
  function handleFilterChange(e) {
    // Check if the changed element is a filter form control
    const filterForm = e.target.closest('#filter-form');
    if (!filterForm) return;

    // Auto-submit on select change or checkbox change
    if (e.target.matches('select[name], input[type="checkbox"][name]')) {
      filterForm.submit();
    }
  }

  /**
   * Close modal on outside click
   */
  function handleModalOutsideClick(e) {
    const modal = document.getElementById('deleteModal');
    if (modal && e.target === modal) {
      hideDeleteModal();
    }
  }

  /**
   * Close modal on Escape key
   */
  function handleEscapeKey(e) {
    if (e.key === 'Escape') {
      const modal = document.getElementById('deleteModal');
      if (modal && modal.classList.contains('active')) {
        hideDeleteModal();
      }
    }
  }

  /**
   * Initialize template list functionality
   */
  function init() {
    // Event delegation for all template actions
    document.addEventListener('click', handleTemplateActions);

    // Event delegation for filter form changes
    document.addEventListener('change', handleFilterChange);

    // Close modal on outside click
    document.addEventListener('click', handleModalOutsideClick);

    // Close modal on Escape key
    document.addEventListener('keydown', handleEscapeKey);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export minimal API for backwards compatibility
  window.EmailTemplateList = {
    showDeleteModal: showDeleteModal,
    hideDeleteModal: hideDeleteModal,
  };
})();
