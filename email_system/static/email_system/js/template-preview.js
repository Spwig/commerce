/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Email Template Preview - Language Switching and Test Email
 * Provides preview functionality with translation management
 */

(function () {
  'use strict';

  /**
   * Change preview language
   */
  function changeLanguage(languageCode) {
    if (!languageCode) return;

    // Reload page with new language parameter
    const url = new URL(window.location.href);
    url.searchParams.set('language', languageCode);
    window.location.href = url.toString();
  }

  /**
   * Show test email modal
   */
  function showTestEmailModal() {
    const modal = document.getElementById('testEmailModal');
    if (modal) {
      modal.style.display = 'flex';
      // Focus on email input
      const emailInput = document.getElementById('test-email-input');
      if (emailInput) {
        setTimeout(() => emailInput.focus(), 100);
      }
    }
  }

  /**
   * Hide test email modal
   */
  function hideTestEmailModal() {
    const modal = document.getElementById('testEmailModal');
    if (modal) {
      modal.style.display = 'none';
      // Clear input
      const emailInput = document.getElementById('test-email-input');
      if (emailInput) {
        emailInput.value = '';
      }
    }
  }

  /**
   * Send test email
   */
  async function sendTestEmail() {
    const emailInput = document.getElementById('test-email-input');
    const email = emailInput ? emailInput.value.trim() : '';

    if (!email) {
      AdminModal.alert({ message: 'Please enter an email address', type: 'warning' });
      return;
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      AdminModal.alert({ message: 'Please enter a valid email address', type: 'warning' });
      return;
    }

    const sendBtn = document.querySelector('[data-action="send-test-email"]');
    const originalText = sendBtn ? sendBtn.textContent : '';

    if (sendBtn) {
      sendBtn.disabled = true;
      sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    }

    try {
      // Get current URL to extract template ID and language
      const urlParams = new URLSearchParams(window.location.search);
      const language = urlParams.get('language') || 'en';

      // Extract template ID from URL path
      const pathParts = window.location.pathname.split('/');
      const templateId = pathParts[pathParts.length - 2]; // ID is before 'preview'

      const response = await fetch(
        AdminUtils.buildAdminUrl(`/admin/email-system/templates/${templateId}/send-test/`),
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': AdminUtils.getCsrfToken(),
          },
          body: JSON.stringify({
            email: email,
            language: language,
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        AdminModal.toast(`Test email sent successfully to ${email}`, 'success');
        hideTestEmailModal();
      } else {
        AdminModal.alert({ message: data.error || 'Failed to send test email', type: 'error' });
      }
    } catch (error) {
      console.error('Error sending test email:', error);
      AdminModal.alert({ message: 'Error sending test email. Please try again.', type: 'error' });
    } finally {
      if (sendBtn) {
        sendBtn.disabled = false;
        sendBtn.textContent = originalText;
      }
    }
  }

  /**
   * Show translation editor modal
   */
  function showTranslationEditor(languageCode) {
    const modal = document.getElementById('translationEditorModal');
    if (!modal) return;

    // Set language in modal header
    const langDisplay = modal.querySelector('.modal-language');
    if (langDisplay) {
      langDisplay.textContent = languageCode.toUpperCase();
    }

    // Store current language in modal dataset
    modal.dataset.editingLanguage = languageCode;

    // Load existing translation if available
    loadTranslation(languageCode);

    modal.style.display = 'flex';
  }

  /**
   * Hide translation editor modal
   */
  function hideTranslationEditor() {
    const modal = document.getElementById('translationEditorModal');
    if (modal) {
      modal.style.display = 'none';

      // Reset Monaco editors if they exist
      if (typeof translationHtmlEditor !== 'undefined' && translationHtmlEditor) {
        translationHtmlEditor.setValue('');
      }
      if (typeof translationTextEditor !== 'undefined' && translationTextEditor) {
        translationTextEditor.setValue('');
      }
    }
  }

  /**
   * Load translation from server
   */
  async function loadTranslation(languageCode) {
    // Extract template ID from URL
    const pathParts = window.location.pathname.split('/');
    const templateId = pathParts[pathParts.length - 2];

    try {
      const response = await fetch(
        AdminUtils.buildAdminUrl(
          `/admin/email-system/templates/${templateId}/translation/${languageCode}/`
        ),
        {
          headers: {
            'X-CSRFToken': AdminUtils.getCsrfToken(),
          },
        }
      );

      if (response.ok) {
        const data = await response.json();

        // Populate subject
        const subjectInput = document.getElementById('translation-subject');
        if (subjectInput) {
          subjectInput.value = data.subject || '';
        }

        // Populate Monaco editors
        if (typeof translationHtmlEditor !== 'undefined' && translationHtmlEditor) {
          translationHtmlEditor.setValue(data.html_content || '');
        }
        if (typeof translationTextEditor !== 'undefined' && translationTextEditor) {
          translationTextEditor.setValue(data.text_content || '');
        }
      }
    } catch (error) {
      console.error('Error loading translation:', error);
    }
  }

  /**
   * Copy content from base template
   */
  function copyFromBase(contentType) {
    // Get base template data from page
    const baseData = window.baseTemplateData || {};

    if (contentType === 'html') {
      if (typeof translationHtmlEditor !== 'undefined' && translationHtmlEditor) {
        translationHtmlEditor.setValue(baseData.html_content || '');
      }
    } else if (contentType === 'text') {
      if (typeof translationTextEditor !== 'undefined' && translationTextEditor) {
        translationTextEditor.setValue(baseData.text_content || '');
      }
    }
  }

  /**
   * Save translation
   */
  async function saveTranslation() {
    const modal = document.getElementById('translationEditorModal');
    if (!modal) return;

    const languageCode = modal.dataset.editingLanguage;
    if (!languageCode) return;

    // Get values
    const subjectInput = document.getElementById('translation-subject');
    const subject = subjectInput ? subjectInput.value : '';

    let htmlContent = '';
    let textContent = '';

    if (typeof translationHtmlEditor !== 'undefined' && translationHtmlEditor) {
      htmlContent = translationHtmlEditor.getValue();
    }
    if (typeof translationTextEditor !== 'undefined' && translationTextEditor) {
      textContent = translationTextEditor.getValue();
    }

    // Extract template ID from URL
    const pathParts = window.location.pathname.split('/');
    const templateId = pathParts[pathParts.length - 2];

    const saveBtn = document.querySelector('[data-action="save-translation"]');
    const originalText = saveBtn ? saveBtn.textContent : '';

    if (saveBtn) {
      saveBtn.disabled = true;
      saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    }

    try {
      const response = await fetch(
        AdminUtils.buildAdminUrl(
          `/admin/email-system/templates/${templateId}/translation/${languageCode}/`
        ),
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': AdminUtils.getCsrfToken(),
          },
          body: JSON.stringify({
            subject: subject,
            html_content: htmlContent,
            text_content: textContent,
            language_code: languageCode,
          }),
        }
      );

      const data = await response.json();

      if (data.success) {
        AdminModal.toast('Translation saved successfully', 'success');
        hideTranslationEditor();

        // Reload page to show updated translation
        window.location.reload();
      } else {
        AdminModal.alert({ message: data.error || 'Failed to save translation', type: 'error' });
      }
    } catch (error) {
      console.error('Error saving translation:', error);
      AdminModal.alert({ message: 'Error saving translation. Please try again.', type: 'error' });
    } finally {
      if (saveBtn) {
        saveBtn.disabled = false;
        saveBtn.textContent = originalText;
      }
    }
  }

  /**
   * Initialize Monaco editors for translation modal
   */
  function initializeTranslationEditors() {
    if (typeof monaco === 'undefined') return;

    const htmlEditorEl = document.getElementById('translation-html-editor');
    const textEditorEl = document.getElementById('translation-text-editor');

    if (htmlEditorEl && !window.translationHtmlEditor) {
      window.translationHtmlEditor = monaco.editor.create(htmlEditorEl, {
        value: '',
        language: 'html',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: true },
        fontSize: 14,
        lineNumbers: 'on',
        wordWrap: 'on',
      });
    }

    if (textEditorEl && !window.translationTextEditor) {
      window.translationTextEditor = monaco.editor.create(textEditorEl, {
        value: '',
        language: 'plaintext',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 14,
        lineNumbers: 'on',
        wordWrap: 'on',
      });
    }
  }

  /**
   * Event delegation handler for template preview actions
   */
  function handlePreviewActions(e) {
    const actionElement = e.target.closest('[data-action]');
    if (!actionElement) return;

    const action = actionElement.dataset.action;
    if (!action) return;

    switch (action) {
      case 'change-language':
        // Only handle on change event, not click (to allow dropdown to open)
        if (e.type !== 'change') return;
        const languageSelect = actionElement;
        if (languageSelect.value) {
          changeLanguage(languageSelect.value);
        }
        break;
      case 'show-test-email':
        e.preventDefault();
        showTestEmailModal();
        break;
      case 'hide-test-email':
        e.preventDefault();
        hideTestEmailModal();
        break;
      case 'send-test-email':
        e.preventDefault();
        sendTestEmail();
        break;
      case 'show-translation-editor':
        e.preventDefault();
        const language = actionElement.dataset.language;
        if (language) {
          showTranslationEditor(language);
        }
        break;
      case 'hide-translation-editor':
        e.preventDefault();
        hideTranslationEditor();
        break;
      case 'copy-from-base':
        e.preventDefault();
        const contentType = actionElement.dataset.contentType;
        if (contentType) {
          copyFromBase(contentType);
        }
        break;
      case 'save-translation':
        e.preventDefault();
        saveTranslation();
        break;
      case 'refresh-preview':
      case 'reload-page':
        e.preventDefault();
        window.location.reload();
        break;
    }
  }

  /**
   * Handle outside clicks to close modals
   */
  function handleOutsideClick(e) {
    // Close test email modal
    const testModal = document.getElementById('testEmailModal');
    if (testModal && e.target === testModal) {
      hideTestEmailModal();
    }

    // Close translation editor modal
    const translationModal = document.getElementById('translationEditorModal');
    if (translationModal && e.target === translationModal) {
      hideTranslationEditor();
    }
  }

  /**
   * Handle Escape key to close modals
   */
  function handleEscapeKey(e) {
    if (e.key === 'Escape') {
      hideTestEmailModal();
      hideTranslationEditor();
    }
  }

  /**
   * Initialize
   */
  function init() {
    // Set up event delegation
    document.addEventListener('click', handlePreviewActions);
    document.addEventListener('change', handlePreviewActions);
    document.addEventListener('click', handleOutsideClick);
    document.addEventListener('keydown', handleEscapeKey);

    // Initialize translation editors if Monaco is loaded
    if (typeof require !== 'undefined') {
      require.config({
        paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' },
      });
      require(['vs/editor/editor.main'], function () {
        initializeTranslationEditors();
      });
    }
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
