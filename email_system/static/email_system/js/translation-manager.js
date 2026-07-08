/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Email Template Translation Manager
 * Handles translation modal and bulk translation actions
 */

(function() {
    'use strict';

    /**
     * Show translate modal for specific template
     */
    function showTranslateModal(templateId, templateName) {
        const modal = document.getElementById('translateModal');
        const form = document.getElementById('translateForm');
        const title = document.getElementById('modal-title');
        const forceRetranslate = document.getElementById('forceRetranslate');

        if (!modal || !form || !title) return;

        // Get translation label from form data attribute or default
        const translateLabel = form.dataset.translateLabel || 'Translate:';
        title.textContent = translateLabel + ' ' + templateName;

        // Always force retranslate
        if (forceRetranslate) {
            forceRetranslate.value = 'true';
        }

        // Set form action with template ID
        const urlTemplate = form.dataset.actionTemplate;
        if (urlTemplate) {
            form.action = urlTemplate.replace('00000000-0000-0000-0000-000000000000', templateId);
        }

        modal.classList.add('active');
    }

    /**
     * Hide translate modal
     */
    function hideTranslateModal() {
        const modal = document.getElementById('translateModal');
        const form = document.getElementById('translateForm');

        if (modal) {
            modal.classList.remove('active');
        }

        if (form) {
            form.reset();
        }
    }

    /**
     * Confirm bulk translate all action
     */
    async function confirmBulkTranslate(message) {
        return await AdminModal.confirm(message);
    }

    /**
     * Event delegation handler
     */
    async function handleTranslationActions(e) {
        const actionElement = e.target.closest('[data-action]');
        if (!actionElement) return;

        const action = actionElement.dataset.action;
        if (!action) return;

        switch (action) {
            case 'show-translate-modal':
                e.preventDefault();
                const templateId = actionElement.dataset.templateId;
                const templateName = actionElement.dataset.templateName;
                if (templateId && templateName) {
                    showTranslateModal(templateId, templateName);
                }
                break;
            case 'hide-translate-modal':
                e.preventDefault();
                hideTranslateModal();
                break;
            case 'confirm-bulk-translate':
                // Allow default form submission, but confirm first
                e.preventDefault();
                const confirmMessage = actionElement.dataset.confirmMessage;
                if (confirmMessage && await confirmBulkTranslate(confirmMessage)) {
                    actionElement.closest('form')?.submit();
                }
                break;
        }
    }

    /**
     * Handle outside clicks to close modals
     */
    function handleOutsideClick(e) {
        const modal = document.getElementById('translateModal');
        if (modal && e.target === modal) {
            hideTranslateModal();
        }
    }

    /**
     * Handle Escape key to close modals
     */
    function handleEscapeKey(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('translateModal');
            if (modal && modal.classList.contains('active')) {
                hideTranslateModal();
            }
        }
    }

    /**
     * Initialize
     */
    function init() {
        // Set up event delegation
        document.addEventListener('click', handleTranslationActions);
        document.addEventListener('submit', handleTranslationActions);
        document.addEventListener('click', handleOutsideClick);
        document.addEventListener('keydown', handleEscapeKey);
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
