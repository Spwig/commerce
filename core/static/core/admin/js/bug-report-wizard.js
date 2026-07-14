/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
'use strict';

/**
 * Bug Report Wizard
 *
 * Provides a 4-step modal wizard for merchants to submit bug reports.
 * Captures console logs and navigation breadcrumbs for diagnostic context.
 */
(function () {
  // =========================================================================
  // Console & navigation buffers — populated by inline <script> in <head>
  // so messages from page load are captured before this deferred script runs.
  // =========================================================================
  const consoleBuffer = window.__spwig_console_buffer || [];
  const navBreadcrumbs = window.__spwig_nav_breadcrumbs || [];
  const MAX_BREADCRUMBS = 10;

  // Continue tracking navigation via popstate
  window.addEventListener('popstate', function () {
    navBreadcrumbs.push({
      url: window.location.href,
      timestamp: new Date().toISOString(),
    });
    if (navBreadcrumbs.length > MAX_BREADCRUMBS) {
      navBreadcrumbs.shift();
    }
  });

  // =========================================================================
  // Wizard state
  // =========================================================================
  let currentStep = 1;
  const totalSteps = 4;
  const formData = {
    category: '',
    description: '',
    severity: '',
    consentFlags: {
      console_logs: true,
      page_url: true,
      browser_info: true,
      navigation: false,
    },
    browserData: {},
    contactName: '',
    contactEmail: '',
    contactConsent: false,
  };

  // =========================================================================
  // DOM references (lazy-initialized)
  // =========================================================================
  const els = {};

  function getEls() {
    if (els._initialized) return;
    els.overlay = document.getElementById('bugReportModalOverlay');
    els.steps = [
      document.getElementById('bugStep1'),
      document.getElementById('bugStep2'),
      document.getElementById('bugStep3'),
      document.getElementById('bugStep4'),
    ];
    els.successStep = document.getElementById('bugStepSuccess');
    els.errorStep = document.getElementById('bugStepError');
    els.dots = document.querySelectorAll('.bug-step-dot');
    els.btnBack = document.getElementById('bugBtnBack');
    els.btnNext = document.getElementById('bugBtnNext');
    els.btnSkip = document.getElementById('bugBtnSkip');
    els.btnSubmit = document.getElementById('bugBtnSubmit');
    els.btnClose = document.getElementById('bugBtnClose');
    els.footer = document.getElementById('bugReportFooter');
    els.stepsIndicator = document.getElementById('bugStepsIndicator');
    els.categoryGrid = document.getElementById('bugCategoryGrid');
    els.description = document.getElementById('bugDescription');
    els.charCount = document.getElementById('bugDescCharCount');
    els.severityOptions = document.getElementById('bugSeverityOptions');
    els.reviewSections = document.getElementById('bugReviewSections');
    els._initialized = true;
  }

  // =========================================================================
  // Step navigation
  // =========================================================================
  function showStep(step) {
    getEls();
    currentStep = step;

    // Hide all steps
    els.steps.forEach(function (s) {
      if (s) s.setAttribute('data-visible', 'false');
    });
    if (els.successStep) els.successStep.setAttribute('data-visible', 'false');
    if (els.errorStep) els.errorStep.setAttribute('data-visible', 'false');

    // Show target step
    if (step >= 1 && step <= totalSteps) {
      els.steps[step - 1].setAttribute('data-visible', 'true');
    }

    // Update dots
    els.dots.forEach(function (dot) {
      const dotStep = parseInt(dot.getAttribute('data-step'), 10);
      dot.classList.remove('active', 'completed');
      if (dotStep === step) {
        dot.classList.add('active');
      } else if (dotStep < step) {
        dot.classList.add('completed');
      }
    });

    // Update buttons
    updateButtons(step);

    // Step-specific actions
    if (step === 2) {
      updateConsentPreviews();
    } else if (step === 4) {
      buildReview();
    }
  }

  function updateButtons(step) {
    // Back button
    els.btnBack.style.display = step > 1 ? '' : 'none';

    // Skip button (only on steps 2 and 3)
    els.btnSkip.style.display = step === 2 || step === 3 ? '' : 'none';

    // Next button (steps 1-3)
    els.btnNext.style.display = step < totalSteps ? '' : 'none';

    // Submit button (step 4 only)
    els.btnSubmit.style.display = step === totalSteps ? '' : 'none';

    // Close button hidden during wizard
    els.btnClose.style.display = 'none';
  }

  function showFinalState(type) {
    getEls();
    // Hide all wizard steps
    els.steps.forEach(function (s) {
      if (s) s.setAttribute('data-visible', 'false');
    });

    if (type === 'success') {
      els.successStep.setAttribute('data-visible', 'true');
    } else {
      els.errorStep.setAttribute('data-visible', 'true');
    }

    // Hide step dots
    if (els.stepsIndicator) els.stepsIndicator.style.display = 'none';

    // Show only close button
    els.btnBack.style.display = 'none';
    els.btnNext.style.display = 'none';
    els.btnSkip.style.display = 'none';
    els.btnSubmit.style.display = 'none';
    els.btnClose.style.display = '';
  }

  // =========================================================================
  // Step 1: Validation & data capture
  // =========================================================================
  function initStep1Listeners() {
    getEls();

    // Category selection
    if (els.categoryGrid) {
      els.categoryGrid.addEventListener('click', function (e) {
        const card = e.target.closest('.bug-category-card');
        if (!card) return;
        // Deselect all
        els.categoryGrid.querySelectorAll('.bug-category-card').forEach(function (c) {
          c.classList.remove('selected');
        });
        card.classList.add('selected');
        formData.category = card.getAttribute('data-value');
      });
    }

    // Description char counter
    if (els.description) {
      els.description.addEventListener('input', function () {
        formData.description = this.value;
        if (els.charCount) {
          els.charCount.textContent = this.value.length;
        }
      });
    }

    // Severity selection
    if (els.severityOptions) {
      els.severityOptions.addEventListener('click', function (e) {
        const card = e.target.closest('.bug-severity-card');
        if (!card) return;
        els.severityOptions.querySelectorAll('.bug-severity-card').forEach(function (c) {
          c.classList.remove('selected');
        });
        card.classList.add('selected');
        formData.severity = card.getAttribute('data-value');
      });
    }
  }

  function validateStep1() {
    if (!formData.category) {
      shakeElement(els.categoryGrid);
      return false;
    }
    if (!formData.description.trim()) {
      shakeElement(els.description);
      els.description.focus();
      return false;
    }
    if (!formData.severity) {
      shakeElement(els.severityOptions);
      return false;
    }
    return true;
  }

  function shakeElement(el) {
    if (!el) return;
    el.classList.add('bug-shake');
    setTimeout(function () {
      el.classList.remove('bug-shake');
    }, 500);
  }

  // =========================================================================
  // Step 2: Browser data consent & preview
  // =========================================================================
  function initStep2Listeners() {
    // Toggle preview panels
    document.querySelectorAll('.bug-consent-preview-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const targetId = this.getAttribute('data-target');
        const preview = document.getElementById(targetId);
        if (preview) {
          preview.classList.toggle('open');
          const icon = this.querySelector('i');
          if (icon) {
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
          }
        }
      });
    });

    // Consent checkbox changes
    ['consentConsole', 'consentPageUrl', 'consentBrowser', 'consentNavigation'].forEach(
      function (id) {
        const checkbox = document.getElementById(id);
        if (checkbox) {
          checkbox.addEventListener('change', function () {
            const map = {
              consentConsole: 'console_logs',
              consentPageUrl: 'page_url',
              consentBrowser: 'browser_info',
              consentNavigation: 'navigation',
            };
            formData.consentFlags[map[id]] = this.checked;
          });
        }
      }
    );
  }

  function updateConsentPreviews() {
    // Console logs preview
    const consoleContent = document.getElementById('consolePreviewContent');
    if (consoleContent) {
      if (consoleBuffer.length === 0) {
        consoleContent.textContent = '(no console messages captured)';
      } else {
        var lines = consoleBuffer.slice(-10).map(function (entry) {
          return '[' + entry.level.toUpperCase() + '] ' + entry.message.substring(0, 120);
        });
        consoleContent.textContent = lines.join('\n');
      }
    }

    // Page URL preview
    const pageUrlContent = document.getElementById('pageUrlPreviewContent');
    if (pageUrlContent) {
      const breadcrumbs = document.querySelector('.breadcrumbs');
      pageUrlContent.textContent =
        'URL: ' +
        window.location.href +
        '\n' +
        'Section: ' +
        (breadcrumbs ? breadcrumbs.textContent.trim() : '(unknown)');
    }

    // Browser info preview
    const browserContent = document.getElementById('browserPreviewContent');
    if (browserContent) {
      browserContent.textContent =
        'User Agent: ' +
        navigator.userAgent +
        '\n' +
        'Viewport: ' +
        window.innerWidth +
        'x' +
        window.innerHeight +
        '\n' +
        'Screen: ' +
        screen.width +
        'x' +
        screen.height +
        '\n' +
        'Language: ' +
        navigator.language;
    }

    // Navigation preview
    const navContent = document.getElementById('navPreviewContent');
    if (navContent) {
      if (navBreadcrumbs.length === 0) {
        navContent.textContent = '(no navigation history)';
      } else {
        var lines = navBreadcrumbs.map(function (entry) {
          return entry.url;
        });
        navContent.textContent = lines.join('\n');
      }
    }
  }

  function collectBrowserData() {
    const data = {};
    const flags = formData.consentFlags;

    if (flags.console_logs) {
      data.console_logs = consoleBuffer.slice();
    }
    if (flags.page_url) {
      const breadcrumbs = document.querySelector('.breadcrumbs');
      data.page_url = window.location.href;
      data.admin_section = breadcrumbs ? breadcrumbs.textContent.trim() : '';
    }
    if (flags.browser_info) {
      data.user_agent = navigator.userAgent;
      data.viewport = { width: window.innerWidth, height: window.innerHeight };
      data.screen_size = { width: screen.width, height: screen.height };
      data.language = navigator.language;
    }
    if (flags.navigation) {
      data.breadcrumbs = navBreadcrumbs.slice();
    }

    return data;
  }

  // =========================================================================
  // Step 3: Contact info capture
  // =========================================================================
  function captureContactInfo() {
    const nameEl = document.getElementById('bugContactName');
    const emailEl = document.getElementById('bugContactEmail');
    const consentEl = document.getElementById('bugContactConsent');
    formData.contactName = nameEl ? nameEl.value.trim() : '';
    formData.contactEmail = emailEl ? emailEl.value.trim() : '';
    formData.contactConsent = consentEl ? consentEl.checked : false;
  }

  // =========================================================================
  // Step 4: Review
  // =========================================================================
  function buildReview() {
    getEls();
    if (!els.reviewSections) return;

    // Collect final data
    formData.browserData = collectBrowserData();
    captureContactInfo();

    const categoryLabels = {
      ui_visual: 'UI/Visual Issue',
      functionality: 'Functionality Broken',
      performance: 'Performance',
      data: 'Data Issue',
      other: 'Other',
    };
    const severityLabels = {
      minor: 'Minor Annoyance',
      significant: 'Significant Issue',
      blocking: 'Blocking Issue',
    };

    let html = '';

    // Bug details section
    html += '<div class="bug-review-section">';
    html += '<div class="bug-review-section-header">';
    html += '<h4><i class="fas fa-bug"></i> Bug Details</h4>';
    html +=
      '<button type="button" class="bug-review-edit" data-goto="1"><i class="fas fa-pencil-alt"></i> Edit</button>';
    html += '</div>';
    html +=
      '<div class="bug-review-field"><span class="bug-review-label">Category:</span> <span class="bug-review-value">' +
      escapeHtml(categoryLabels[formData.category] || formData.category) +
      '</span></div>';
    html +=
      '<div class="bug-review-field"><span class="bug-review-label">Severity:</span> <span class="bug-review-value bug-severity-badge bug-severity-' +
      escapeHtml(formData.severity) +
      '">' +
      escapeHtml(severityLabels[formData.severity] || formData.severity) +
      '</span></div>';
    html +=
      '<div class="bug-review-field"><span class="bug-review-label">Description:</span></div>';
    html += '<div class="bug-review-description">' + escapeHtml(formData.description) + '</div>';
    html += '</div>';

    // Browser data section
    const browserKeys = Object.keys(formData.browserData);
    html += '<div class="bug-review-section">';
    html += '<div class="bug-review-section-header">';
    html += '<h4><i class="fas fa-laptop"></i> Browser Data</h4>';
    html +=
      '<button type="button" class="bug-review-edit" data-goto="2"><i class="fas fa-pencil-alt"></i> Edit</button>';
    html += '</div>';
    if (browserKeys.length === 0) {
      html += '<div class="bug-review-field"><em>No browser data included</em></div>';
    } else {
      browserKeys.forEach(function (key) {
        const val = formData.browserData[key];
        let displayVal;
        if (typeof val === 'string') {
          displayVal = escapeHtml(val);
        } else if (Array.isArray(val)) {
          displayVal = val.length + ' items';
        } else if (typeof val === 'object') {
          displayVal = escapeHtml(JSON.stringify(val));
        } else {
          displayVal = escapeHtml(String(val));
        }
        html +=
          '<div class="bug-review-field"><span class="bug-review-label">' +
          escapeHtml(key.replace(/_/g, ' ')) +
          ':</span> <span class="bug-review-value">' +
          displayVal +
          '</span></div>';
      });
    }
    html += '</div>';

    // Contact info section
    html += '<div class="bug-review-section">';
    html += '<div class="bug-review-section-header">';
    html += '<h4><i class="fas fa-user"></i> Contact Information</h4>';
    html +=
      '<button type="button" class="bug-review-edit" data-goto="3"><i class="fas fa-pencil-alt"></i> Edit</button>';
    html += '</div>';
    if (!formData.contactName && !formData.contactEmail) {
      html += '<div class="bug-review-field"><em>Submitting anonymously</em></div>';
    } else {
      if (formData.contactName) {
        html +=
          '<div class="bug-review-field"><span class="bug-review-label">Name:</span> <span class="bug-review-value">' +
          escapeHtml(formData.contactName) +
          '</span></div>';
      }
      if (formData.contactEmail) {
        html +=
          '<div class="bug-review-field"><span class="bug-review-label">Email:</span> <span class="bug-review-value">' +
          escapeHtml(formData.contactEmail) +
          '</span></div>';
      }
      html +=
        '<div class="bug-review-field"><span class="bug-review-label">OK to contact:</span> <span class="bug-review-value">' +
        (formData.contactConsent ? 'Yes' : 'No') +
        '</span></div>';
    }
    html += '</div>';

    els.reviewSections.innerHTML = html;

    // Bind edit buttons
    els.reviewSections.querySelectorAll('.bug-review-edit').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const step = parseInt(this.getAttribute('data-goto'), 10);
        showStep(step);
      });
    });
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // =========================================================================
  // Submission
  // =========================================================================
  function submitReport() {
    getEls();
    const breadcrumbs = document.querySelector('.breadcrumbs');

    const payload = {
      category: formData.category,
      description: formData.description,
      severity: formData.severity,
      browser_data: formData.browserData,
      consent_flags: formData.consentFlags,
      contact_name: formData.contactName,
      contact_email: formData.contactEmail,
      contact_consent: formData.contactConsent,
      page_url: window.location.href,
      admin_section: breadcrumbs ? breadcrumbs.textContent.trim() : '',
    };

    // Disable submit button
    els.btnSubmit.disabled = true;
    els.btnSubmit.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

    fetch('/api/bug-reports/submit/', AdminUtils.buildFetchOptions('POST', payload))
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          showFinalState('success');
        } else {
          showFinalState('error');
        }
      })
      .catch(function () {
        showFinalState('error');
      });
  }

  // =========================================================================
  // Open / Close
  // =========================================================================
  function openWizard() {
    getEls();
    if (!els.overlay) return;

    // Reset form state
    resetWizard();

    // Close help drawer if open
    const helpDrawer = document.getElementById('helpDrawer');
    const helpOverlay = document.getElementById('helpDrawerOverlay');
    if (helpDrawer && helpDrawer.classList.contains('open')) {
      helpDrawer.classList.remove('open');
      if (helpOverlay) helpOverlay.classList.remove('active');
      helpDrawer.setAttribute('aria-hidden', 'true');
    }

    els.overlay.classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
  }

  function closeWizard() {
    getEls();
    if (!els.overlay) return;
    els.overlay.classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
  }

  function resetWizard() {
    getEls();
    formData.category = '';
    formData.description = '';
    formData.severity = '';
    formData.consentFlags = {
      console_logs: true,
      page_url: true,
      browser_info: true,
      navigation: false,
    };
    formData.browserData = {};
    formData.contactName = '';
    formData.contactEmail = '';
    formData.contactConsent = false;

    // Reset UI
    if (els.categoryGrid) {
      els.categoryGrid.querySelectorAll('.bug-category-card').forEach(function (c) {
        c.classList.remove('selected');
      });
    }
    if (els.description) {
      els.description.value = '';
    }
    if (els.charCount) {
      els.charCount.textContent = '0';
    }
    if (els.severityOptions) {
      els.severityOptions.querySelectorAll('.bug-severity-card').forEach(function (c) {
        c.classList.remove('selected');
      });
    }

    // Reset consent checkboxes
    const consentIds = ['consentConsole', 'consentPageUrl', 'consentBrowser'];
    consentIds.forEach(function (id) {
      const el = document.getElementById(id);
      if (el) el.checked = true;
    });
    const navConsent = document.getElementById('consentNavigation');
    if (navConsent) navConsent.checked = false;

    // Reset contact fields
    const nameEl = document.getElementById('bugContactName');
    const emailEl = document.getElementById('bugContactEmail');
    const contactConsentEl = document.getElementById('bugContactConsent');
    if (nameEl) nameEl.value = '';
    if (emailEl) emailEl.value = '';
    if (contactConsentEl) contactConsentEl.checked = false;

    // Reset submit button
    if (els.btnSubmit) {
      els.btnSubmit.disabled = false;
      els.btnSubmit.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Report';
    }

    // Reset steps indicator
    if (els.stepsIndicator) els.stepsIndicator.style.display = '';

    // Reset drag position
    resetDragPosition();

    // Close all previews
    document.querySelectorAll('.bug-consent-preview.open').forEach(function (p) {
      p.classList.remove('open');
    });
    document.querySelectorAll('.bug-consent-preview-btn i').forEach(function (icon) {
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    });

    showStep(1);
  }

  // =========================================================================
  // Action handlers
  // =========================================================================
  function handleNext() {
    if (currentStep === 1 && !validateStep1()) return;
    if (currentStep === 2) {
      // Capture consent state from checkboxes
    }
    if (currentStep === 3) {
      captureContactInfo();
    }
    if (currentStep < totalSteps) {
      showStep(currentStep + 1);
    }
  }

  function handleBack() {
    if (currentStep > 1) {
      showStep(currentStep - 1);
    }
  }

  function handleSkip() {
    // Skip goes to next step without validation
    if (currentStep < totalSteps) {
      showStep(currentStep + 1);
    }
  }

  // =========================================================================
  // Draggable modal (desktop only)
  // =========================================================================
  const drag = { active: false, startX: 0, startY: 0, modalX: 0, modalY: 0 };

  function initDrag() {
    getEls();
    if (!els.overlay) return;

    const header = els.overlay.querySelector('.admin-modal-header');
    const modal = els.overlay.querySelector('.admin-modal');
    if (!header || !modal) return;

    header.addEventListener('mousedown', function (e) {
      // Skip if clicking a button inside the header, or on mobile
      if (e.target.closest('button') || window.innerWidth <= 768) return;

      const rect = modal.getBoundingClientRect();
      drag.active = true;
      drag.startX = e.clientX;
      drag.startY = e.clientY;

      // If first drag, initialize position from current centered location
      if (!els.overlay.classList.contains('bug-dragging')) {
        drag.modalX = rect.left;
        drag.modalY = rect.top;
        els.overlay.classList.add('bug-dragging');
        modal.style.left = drag.modalX + 'px';
        modal.style.top = drag.modalY + 'px';
      } else {
        drag.modalX = parseInt(modal.style.left, 10) || 0;
        drag.modalY = parseInt(modal.style.top, 10) || 0;
      }

      e.preventDefault();
    });

    document.addEventListener('mousemove', function (e) {
      if (!drag.active) return;
      const dx = e.clientX - drag.startX;
      const dy = e.clientY - drag.startY;

      let newX = drag.modalX + dx;
      let newY = drag.modalY + dy;

      // Clamp so modal header stays in viewport
      const modalRect = modal.getBoundingClientRect();
      const minY = 0;
      const maxY = window.innerHeight - 40;
      const minX = -(modalRect.width - 80);
      const maxX = window.innerWidth - 80;

      newX = Math.max(minX, Math.min(maxX, newX));
      newY = Math.max(minY, Math.min(maxY, newY));

      modal.style.left = newX + 'px';
      modal.style.top = newY + 'px';
    });

    document.addEventListener('mouseup', function () {
      drag.active = false;
    });
  }

  function resetDragPosition() {
    getEls();
    if (!els.overlay) return;
    const modal = els.overlay.querySelector('.admin-modal');
    if (modal) {
      modal.style.left = '';
      modal.style.top = '';
    }
    els.overlay.classList.remove('bug-dragging');
  }

  // =========================================================================
  // Escape key handler
  // =========================================================================
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      getEls();
      if (els.overlay && els.overlay.classList.contains('active')) {
        closeWizard();
      }
    }
  });

  // =========================================================================
  // Overlay click to close
  // =========================================================================
  document.addEventListener('click', function (e) {
    if (e.target && e.target.id === 'bugReportModalOverlay') {
      closeWizard();
    }
  });

  // =========================================================================
  // Initialize on DOM ready
  // =========================================================================
  function init() {
    getEls();
    initStep1Listeners();
    initStep2Listeners();
    initDrag();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // =========================================================================
  // Public API
  // =========================================================================
  window.BugReportWizard = {
    open: openWizard,
    close: closeWizard,
    next: handleNext,
    back: handleBack,
    skip: handleSkip,
    submit: submitReport,
  };
})();
