/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Email Template Editor - Monaco Editor Integration
 * Provides MJML/HTML syntax highlighting and live preview
 */

let mjmlEditor, textEditor;
let previewUpdateTimeout;

// Read config from data island (CSP-safe)
const _templateEditorEl = document.getElementById('template-editor-data');
const templateData = _templateEditorEl ? JSON.parse(_templateEditorEl.textContent) : {};

// Initialize Monaco Editor
require.config({
  paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs' },
});

require(['vs/editor/editor.main'], function () {
  initializeEditors();
});

/**
 * Initialize both editors
 */
function initializeEditors() {
  // MJML Editor (HTML mode with dark theme)
  mjmlEditor = monaco.editor.create(document.getElementById('mjml-editor'), {
    value: templateData.htmlContent,
    language: 'html',
    theme: 'vs-dark',
    automaticLayout: true,
    minimap: { enabled: true },
    fontSize: 14,
    lineNumbers: 'on',
    roundedSelection: true,
    scrollBeyondLastLine: false,
    readOnly: templateData.isSystem,
    wordWrap: 'on',
    wrappingIndent: 'indent',
    formatOnPaste: true,
    formatOnType: true,
  });

  // Plain Text Editor
  textEditor = monaco.editor.create(document.getElementById('text-editor'), {
    value: templateData.textContent,
    language: 'plaintext',
    theme: 'vs-dark',
    automaticLayout: true,
    minimap: { enabled: false },
    fontSize: 14,
    lineNumbers: 'on',
    roundedSelection: true,
    scrollBeyondLastLine: false,
    readOnly: templateData.isSystem,
    wordWrap: 'on',
  });

  // Auto-update preview on change (debounced)
  if (!templateData.isSystem) {
    mjmlEditor.onDidChangeModelContent(() => {
      clearTimeout(previewUpdateTimeout);
      previewUpdateTimeout = setTimeout(() => {
        updatePreview();
      }, 1000); // Update after 1 second of no typing
    });
  }

  // Initial preview load
  updatePreview();
}

/**
 * Switch between tabs
 */
function switchTab(tabName) {
  // Update tab buttons
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabName);
  });

  // Update tab content
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.toggle('active', content.id === `${tabName}-tab`);
  });

  // Refresh editor layout when switching tabs
  setTimeout(() => {
    if (tabName === 'mjml') {
      mjmlEditor.layout();
    } else if (tabName === 'text') {
      textEditor.layout();
    }
  }, 100);
}

/**
 * Format code in active editor
 */
function formatCode() {
  mjmlEditor.getAction('editor.action.formatDocument').run();
  showStatus('Code formatted', 'success');
}

/**
 * Validate MJML syntax
 */
async function validateMJML() {
  const mjmlContent = mjmlEditor.getValue();

  if (!mjmlContent.trim()) {
    showStatus('MJML content is empty', 'error');
    return;
  }

  try {
    // Send to server for validation
    const response = await fetch(window.location.href, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': templateData.csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: new URLSearchParams({
        subject: document.getElementById('subject-input').value,
        html_content: mjmlContent,
        text_content: textEditor.getValue(),
        validate_only: 'true',
      }),
    });

    if (response.ok) {
      showStatus('MJML is valid!', 'success');
    } else {
      const data = await response.json();
      showStatus(data.error || 'MJML validation failed', 'error');
    }
  } catch (error) {
    showStatus('Validation error: ' + error.message, 'error');
  }
}

/**
 * Save template
 */
async function saveTemplate() {
  const saveBtn = document.getElementById('save-btn');
  const originalText = saveBtn.innerHTML;

  saveBtn.disabled = true;
  saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

  try {
    const response = await fetch(window.location.href, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': templateData.csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: new URLSearchParams({
        subject: document.getElementById('subject-input').value,
        html_content: mjmlEditor.getValue(),
        text_content: textEditor.getValue(),
      }),
    });

    const data = await response.json();

    if (data.success) {
      showStatus(data.message, 'success');

      // Update version badge
      if (data.version) {
        document.querySelector('.version-badge').innerHTML =
          `<i class="fas fa-code-branch"></i> Version ${data.version}`;
      }
    } else {
      showStatus(data.error || 'Failed to save template', 'error');
    }
  } catch (error) {
    showStatus('Error saving template: ' + error.message, 'error');
  } finally {
    saveBtn.disabled = false;
    saveBtn.innerHTML = originalText;
  }
}

/**
 * Update live preview
 */
async function updatePreview() {
  const iframe = document.getElementById('preview-iframe');
  const loading = document.querySelector('.preview-loading');
  const mjmlContent = mjmlEditor.getValue();

  if (!mjmlContent.trim()) {
    iframe.srcdoc =
      '<div style="padding: 40px; text-align: center; color: #999;">No content to preview</div>';
    return;
  }

  loading.style.display = 'block';

  try {
    // Convert MJML to HTML via AJAX
    const response = await fetch(
      AdminUtils.buildAdminUrl('/admin/email-system/templates/preview-render/'),
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': templateData.csrfToken,
        },
        body: JSON.stringify({
          mjml_content: mjmlContent,
        }),
      }
    );

    if (response.ok) {
      const data = await response.json();
      iframe.srcdoc =
        data.html || '<div style="padding: 20px; color: red;">Preview generation failed</div>';
    } else {
      iframe.srcdoc = '<div style="padding: 20px; color: red;">Error loading preview</div>';
    }
  } catch (error) {
    console.error('Preview error:', error);
    // For now, just show the MJML content as-is (will be raw HTML)
    iframe.srcdoc = mjmlContent;
  } finally {
    loading.style.display = 'none';
  }
}

/**
 * Refresh preview manually
 */
function refreshPreview() {
  updatePreview();
  showStatus('Preview refreshed', 'success');
}

/**
 * Change preview device
 */
function setPreviewDevice(device) {
  const iframe = document.getElementById('preview-iframe');
  const buttons = document.querySelectorAll('.preview-actions .btn-tool');

  buttons.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.device === device);
  });

  iframe.classList.remove('desktop', 'mobile');
  iframe.classList.add(device);
}

/**
 * Copy variable to clipboard
 * Uses modern clipboard API with fallback for non-secure contexts (HTTP)
 */
function copyVariable(varName) {
  const variableText = `{{ ${varName} }}`;

  // Modern clipboard API (requires secure context: HTTPS or localhost)
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard
      .writeText(variableText)
      .then(() => {
        showStatus(`Copied: ${variableText}`, 'success');
      })
      .catch(err => {
        console.error('Failed to copy:', err);
        fallbackCopyToClipboard(variableText);
      });
  } else {
    // Fallback for non-secure contexts (HTTP with IP address)
    fallbackCopyToClipboard(variableText);
  }
}

/**
 * Fallback copy method for non-secure contexts
 */
function fallbackCopyToClipboard(text) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  textArea.style.position = 'fixed';
  textArea.style.left = '-9999px';
  textArea.style.top = '-9999px';
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    const successful = document.execCommand('copy');
    if (successful) {
      showStatus(`Copied: ${text}`, 'success');
    } else {
      showStatus('Failed to copy variable', 'error');
    }
  } catch (err) {
    console.error('Fallback copy failed:', err);
    showStatus('Failed to copy variable', 'error');
  }

  document.body.removeChild(textArea);
}

/**
 * Show status message
 */
function showStatus(message, type = 'success') {
  const status = document.getElementById('save-status');
  const messageEl = document.getElementById('status-message');
  const icon = status.querySelector('i');

  messageEl.textContent = message;
  status.className = `save-status show ${type === 'error' ? 'error' : ''}`;

  if (type === 'error') {
    icon.className = 'fas fa-exclamation-circle';
  } else {
    icon.className = 'fas fa-check-circle';
  }

  // Auto-hide after 3 seconds
  setTimeout(() => {
    status.classList.remove('show');
  }, 3000);
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', e => {
  // Ctrl/Cmd + S to save
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault();
    if (!templateData.isSystem) {
      saveTemplate();
    }
  }

  // Ctrl/Cmd + P to refresh preview
  if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
    e.preventDefault();
    refreshPreview();
  }
});

// Auto-save warning on page unload
window.addEventListener('beforeunload', e => {
  if (!templateData.isSystem) {
    const currentContent = mjmlEditor.getValue();
    if (currentContent !== templateData.htmlContent) {
      e.preventDefault();
      e.returnValue = '';
      return '';
    }
  }
});

/**
 * Panel Expand/Collapse Functionality - Overlay Mode
 */
let expandedPanel = null;

function togglePanelExpand(panelType) {
  const editorPanel = document.getElementById('editor-panel');
  const previewPanel = document.getElementById('preview-panel');
  const targetPanel = panelType === 'editor' ? editorPanel : previewPanel;

  if (targetPanel.classList.contains('panel-expanded')) {
    // Close expanded panel
    targetPanel.classList.remove('panel-expanded');
    expandedPanel = null;
    updateExpandIcon(panelType, false);

    // Resize Monaco editors when returning to normal view
    if (panelType === 'editor') {
      setTimeout(() => {
        if (mjmlEditor) mjmlEditor.layout();
        if (textEditor) textEditor.layout();
      }, 300);
    }
  } else {
    // Close any currently expanded panel first
    if (expandedPanel) {
      document.getElementById(expandedPanel + '-panel').classList.remove('panel-expanded');
      updateExpandIcon(expandedPanel, false);
    }

    // Expand target panel as full-screen overlay
    targetPanel.classList.add('panel-expanded');
    expandedPanel = panelType;
    updateExpandIcon(panelType, true);

    // Handle panel-specific expansion logic
    setTimeout(() => {
      if (panelType === 'editor') {
        // Resize Monaco editors after expansion
        if (mjmlEditor) mjmlEditor.layout();
        if (textEditor) textEditor.layout();
      } else if (panelType === 'preview') {
        // Refresh preview iframe after expansion
        const iframe = document.getElementById('preview-frame');
        if (iframe) {
          // Force iframe reload by re-assigning src; browsers treat identical src as a no-op
          // unless the src property is set again, so this is intentional.
          // eslint-disable-next-line no-self-assign
          iframe.src = iframe.src;
        }
      }
    }, 300);
  }

  // Save state to sessionStorage
  sessionStorage.setItem('expandedPanel', expandedPanel || '');
}

function updateExpandIcon(panelType, isExpanded) {
  const panel =
    panelType === 'editor'
      ? document.getElementById('editor-panel')
      : document.getElementById('preview-panel');

  const icon = panel.querySelector('.expand-btn i');
  if (icon) {
    if (isExpanded) {
      icon.className = 'fas fa-compress';
    } else {
      icon.className = 'fas fa-expand';
    }
  }
}

// Restore expand state on page load
document.addEventListener('DOMContentLoaded', function () {
  const savedExpandedPanel = sessionStorage.getItem('expandedPanel');
  if (savedExpandedPanel && (savedExpandedPanel === 'editor' || savedExpandedPanel === 'preview')) {
    togglePanelExpand(savedExpandedPanel);
  }
});

/**
 * Event delegation handler for template editor actions
 */
function handleEditorActions(e) {
  const actionElement = e.target.closest('[data-action]');
  if (!actionElement) return;

  const action = actionElement.dataset.action;
  if (!action) return;

  switch (action) {
    case 'switch-tab':
      e.preventDefault();
      const tabName = actionElement.dataset.tab;
      if (tabName) {
        switchTab(tabName);
      }
      break;
    case 'toggle-panel-expand':
      e.preventDefault();
      const panelType = actionElement.dataset.panel;
      if (panelType) {
        togglePanelExpand(panelType);
      }
      break;
    case 'format-code':
      e.preventDefault();
      formatCode();
      break;
    case 'validate-mjml':
      e.preventDefault();
      validateMJML();
      break;
    case 'save-template':
      e.preventDefault();
      saveTemplate();
      break;
    case 'refresh-preview':
      e.preventDefault();
      refreshPreview();
      break;
    case 'set-preview-device':
      e.preventDefault();
      const device = actionElement.dataset.device;
      if (device) {
        setPreviewDevice(device);
      }
      break;
    case 'copy-variable':
      e.preventDefault();
      const varName = actionElement.dataset.varName;
      if (varName) {
        copyVariable(varName);
      }
      break;
  }
}

// Set up event delegation for all editor actions
document.addEventListener('click', handleEditorActions);
