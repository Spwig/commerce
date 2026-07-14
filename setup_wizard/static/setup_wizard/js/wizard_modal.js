(function () {
  'use strict';

  const lang = document.documentElement.lang || 'en';
  const API_BASE = `/${lang}/admin/setup/api`;

  const GROUPS = ['store', 'contact', 'locale', 'payments', 'finetune'];

  let currentGroupIndex = 0;
  let overlay, modal, body, dots, footerLeft, footerRight;

  // --- Initialization ---

  document.addEventListener('DOMContentLoaded', function () {
    overlay = document.getElementById('setup-wizard-overlay');
    if (!overlay) return;

    modal = overlay.querySelector('.admin-modal');
    body = overlay.querySelector('.admin-modal-body');
    dots = overlay.querySelectorAll('.wizard-step-dot');
    footerLeft = overlay.querySelector('.wizard-nav-left');
    footerRight = overlay.querySelector('.wizard-nav-right');

    // Bind open triggers
    document.querySelectorAll('[data-setup-wizard-open]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        openWizard();
      });
    });

    // Close button
    overlay.querySelector('.admin-modal-close').addEventListener('click', closeWizard);

    // Overlay click to close
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeWizard();
    });

    // Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('active')) {
        closeWizard();
      }
    });

    // Step dot clicks
    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        navigateToGroup(i);
      });
    });

    // Auto-open if requested by URL param or data attribute
    if (overlay.dataset.autoOpen === 'true') {
      openWizard();
    }
  });

  // --- Modal open/close ---

  function openWizard() {
    // Find the first incomplete group, or the first group
    let firstIncomplete = 0;
    dots.forEach(function (dot, i) {
      if (!dot.classList.contains('completed') && firstIncomplete === 0) {
        // Check if all previous are completed
        let allPrevCompleted = true;
        for (let j = 0; j < i; j++) {
          if (!dots[j].classList.contains('completed')) {
            allPrevCompleted = false;
            break;
          }
        }
        if (allPrevCompleted && !dot.classList.contains('completed')) {
          firstIncomplete = i;
        }
      }
    });

    overlay.classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
    navigateToGroup(firstIncomplete);
  }

  function closeWizard() {
    overlay.classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
  }

  // --- Navigation ---

  function navigateToGroup(index) {
    if (index < 0 || index >= GROUPS.length) return;
    currentGroupIndex = index;
    updateDots();
    updateFooter();
    loadGroupContent(GROUPS[index]);
  }

  function updateDots() {
    dots.forEach(function (dot, i) {
      dot.classList.toggle('active', i === currentGroupIndex);
    });
  }

  function updateFooter() {
    const isFirst = currentGroupIndex === 0;
    const isLast = currentGroupIndex === GROUPS.length - 1;
    const isOptional = currentGroupIndex === GROUPS.length - 1; // finetune

    footerLeft.innerHTML = '';
    footerRight.innerHTML = '';

    if (!isFirst) {
      const backBtn = document.createElement('button');
      backBtn.type = 'button';
      backBtn.className = 'wizard-nav-btn btn-back';
      backBtn.innerHTML = '<i class="fas fa-arrow-left"></i> Back';
      backBtn.addEventListener('click', function () {
        navigateToGroup(currentGroupIndex - 1);
      });
      footerLeft.appendChild(backBtn);
    }

    if (isOptional) {
      const skipBtn = document.createElement('button');
      skipBtn.type = 'button';
      skipBtn.className = 'wizard-nav-btn btn-skip';
      skipBtn.textContent = 'Skip for now';
      skipBtn.addEventListener('click', closeWizard);
      footerLeft.appendChild(skipBtn);
    }

    const saveBtn = document.createElement('button');
    saveBtn.type = 'button';
    saveBtn.className = 'wizard-nav-btn btn-next';
    saveBtn.id = 'wizard-save-btn';

    if (isLast) {
      saveBtn.innerHTML = 'Save & Finish <i class="fas fa-check"></i>';
    } else {
      saveBtn.innerHTML = 'Save & Continue <i class="fas fa-arrow-right"></i>';
    }

    saveBtn.addEventListener('click', function () {
      saveCurrentStep();
    });
    footerRight.appendChild(saveBtn);
  }

  // --- Content Loading ---

  function loadGroupContent(groupKey) {
    // Clean up timezone interval when leaving locale step
    if (timezoneInterval) {
      clearInterval(timezoneInterval);
      timezoneInterval = null;
    }
    body.innerHTML = '<div class="wizard-loading"><div class="wizard-spinner"></div></div>';

    fetch(API_BASE + '/step/' + groupKey + '/', {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.html) {
          body.innerHTML = data.html;
          initFinetuneToggles();
          initTimezoneDisplay();
        } else {
          body.innerHTML = '<div class="wizard-form-error">Failed to load step content.</div>';
        }
      })
      .catch(function () {
        body.innerHTML = '<div class="wizard-form-error">Network error. Please try again.</div>';
      });
  }

  // --- Saving ---

  function saveCurrentStep() {
    const groupKey = GROUPS[currentGroupIndex];
    const saveBtn = document.getElementById('wizard-save-btn');
    if (!saveBtn) return;

    // For payments step, check acknowledgment
    if (groupKey === 'payments') {
      const ackCheckbox = body.querySelector('#payments-ack');
      if (ackCheckbox && !ackCheckbox.checked) {
        let errorDiv = body.querySelector('.wizard-form-error');
        if (!errorDiv) {
          errorDiv = document.createElement('div');
          errorDiv.className = 'wizard-form-error';
          body.querySelector('.payments-info-card').appendChild(errorDiv);
        }
        errorDiv.textContent = 'Please acknowledge that you will configure payment providers.';
        return;
      }
    }

    saveBtn.disabled = true;
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

    // Collect form data
    const formData = new FormData();
    const forms = body.querySelectorAll('form');
    if (forms.length > 0) {
      // Merge all forms into one FormData (for finetune step with multiple forms)
      forms.forEach(function (form) {
        const fd = new FormData(form);
        for (const pair of fd.entries()) {
          formData.append(pair[0], pair[1]);
        }
      });
    }

    // Add CSRF token
    const csrfInput = body.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) {
      formData.set('csrfmiddlewaretoken', csrfInput.value);
    } else {
      const csrfToken = AdminUtils.getCsrfToken();
      if (csrfToken) {
        formData.set('csrfmiddlewaretoken', csrfToken);
      }
    }

    // Handle unchecked checkboxes (they aren't included in FormData)
    const checkboxes = body.querySelectorAll('input[type="checkbox"][name]');
    checkboxes.forEach(function (cb) {
      if (!cb.checked && cb.name !== 'csrfmiddlewaretoken') {
        formData.set(cb.name, '');
      }
    });

    fetch(API_BASE + '/step/' + groupKey + '/save/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
      },
    })
      .then(function (resp) {
        return resp.json().then(function (data) {
          return { ok: resp.ok, data: data };
        });
      })
      .then(function (result) {
        if (result.ok && result.data.success) {
          // Update progress
          updateProgressUI(result.data.progress);

          // Navigate to next or show completion
          if (currentGroupIndex < GROUPS.length - 1) {
            navigateToGroup(currentGroupIndex + 1);
          } else {
            showCompletion(result.data.progress);
          }
        } else {
          displayErrors(result.data.errors || {});
          saveBtn.disabled = false;
          updateFooter();
        }
      })
      .catch(function () {
        body.insertAdjacentHTML(
          'afterbegin',
          '<div class="wizard-form-error">Network error. Please try again.</div>'
        );
        saveBtn.disabled = false;
        updateFooter();
      });
  }

  // --- Progress Updates ---

  function updateProgressUI(progress) {
    if (!progress) return;

    // Update dots
    if (progress.groups) {
      progress.groups.forEach(function (group, i) {
        if (i < dots.length) {
          dots[i].classList.toggle('completed', group.completed);
        }
      });
    }

    // Update banner
    const banner = document.querySelector('.setup-progress-banner');
    if (banner) {
      const title = banner.querySelector('.setup-progress-title');
      const subtitle = banner.querySelector('.setup-progress-subtitle');
      const ringText = banner.querySelector('.ring-text');
      const ringFill = banner.querySelector('.ring-fill');

      if (progress.is_essential_complete) {
        banner.classList.add('setup-complete');
        if (title) title.textContent = 'Setup Complete';
        if (subtitle) subtitle.textContent = 'Your store is ready. Fine-tune settings anytime.';
      } else {
        const completed = progress.groups
          ? progress.groups.filter(function (g, i) {
              return i < 4 && g.completed;
            }).length
          : 0;
        if (title) title.textContent = 'Store Setup: ' + completed + ' of 4 steps complete';
      }

      const pct = progress.essential_completion_percentage || 0;
      if (ringText) ringText.textContent = pct + '%';
      if (ringFill) {
        const circumference = 2 * Math.PI * 20;
        ringFill.style.strokeDashoffset = circumference - (pct / 100) * circumference;
      }
    }
  }

  function showCompletion(progress) {
    body.innerHTML =
      '<div class="wizard-complete-card">' +
      '<div class="wizard-complete-icon"><i class="fas fa-check-circle"></i></div>' +
      '<h3 class="wizard-complete-title">Setup Complete!</h3>' +
      '<p class="wizard-complete-text">' +
      'Your store is configured and ready to go. You can always return to adjust these settings.' +
      '</p>' +
      '</div>';

    footerLeft.innerHTML = '';
    footerRight.innerHTML = '';

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'wizard-nav-btn btn-next';
    closeBtn.innerHTML = 'Go to Dashboard <i class="fas fa-arrow-right"></i>';
    closeBtn.addEventListener('click', function () {
      closeWizard();
      // Reload to update dashboard if all essential steps are done
      if (progress && progress.is_essential_complete) {
        window.location.reload();
      }
    });
    footerRight.appendChild(closeBtn);

    updateProgressUI(progress);
  }

  // --- Error Display ---

  function displayErrors(errors) {
    // Clear existing errors
    body.querySelectorAll('.wizard-field-error').forEach(function (el) {
      el.remove();
    });
    body.querySelectorAll('.wizard-form-error').forEach(function (el) {
      el.remove();
    });

    if (errors.__all__) {
      body.insertAdjacentHTML(
        'afterbegin',
        '<div class="wizard-form-error">' + escapeHtml(errors.__all__.join(', ')) + '</div>'
      );
    }

    Object.keys(errors).forEach(function (fieldName) {
      if (fieldName === '__all__') return;
      const input = body.querySelector('[name="' + fieldName + '"]');
      if (input) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'wizard-field-error';
        errorDiv.textContent = errors[fieldName].join(', ');
        input.parentNode.appendChild(errorDiv);
      }
    });
  }

  // --- Timezone Display ---

  var timezoneInterval = null;

  function initTimezoneDisplay() {
    // Clear any previous interval
    if (timezoneInterval) {
      clearInterval(timezoneInterval);
      timezoneInterval = null;
    }

    const el = document.getElementById('tz-user-time');
    if (!el) return;

    function updateUserTime() {
      const now = new Date();
      const timeStr = now.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      });
      const tzName = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
      el.textContent = timeStr + (tzName ? ' (' + tzName + ')' : '');
    }

    updateUserTime();
    timezoneInterval = setInterval(updateUserTime, 1000);
  }

  // --- Fine-tune Toggle ---

  function initFinetuneToggles() {
    body.querySelectorAll('.finetune-section-header').forEach(function (header) {
      header.addEventListener('click', function () {
        header.parentElement.classList.toggle('open');
      });
    });
  }

  // --- Utilities ---

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
})();
