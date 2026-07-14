/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let currentStep = 1;
  const totalSteps = 5;
  let actionIndex = 1;
  let translations = {};
  let typeLabels = {};
  let eventLabels = {};

  function init() {
    const tEl = document.getElementById('campaign-wizard-data');
    if (tEl) {
      try {
        const data = JSON.parse(tEl.textContent);
        translations = data.translations || {};
        typeLabels = data.typeLabels || {};
        eventLabels = data.eventLabels || {};
      } catch (e) {}
    }

    /* Event delegation for button actions */
    document.addEventListener('click', handleActions);

    /* Action type select change (covers dynamically added selects too) */
    document.addEventListener('change', function (e) {
      if (e.target.matches('.action-type-select')) {
        updateActionFields(e.target);
      }
      if (e.target.id === 'schedule_type') {
        updateScheduleDisplay(e.target.value);
      }
      if (e.target.id === 'target_all_members') {
        const opts = document.getElementById('targeting-options');
        if (opts) {
          opts.classList.toggle('wizard-hidden', e.target.checked);
        }
      }
    });

    /* Campaign type card selection */
    document.querySelectorAll('.type-card').forEach(function (card) {
      card.addEventListener('click', function () {
        document.querySelectorAll('.type-card').forEach(function (c) {
          c.classList.remove('active');
        });
        this.classList.add('active');
        updateTriggerConfig();
      });
    });

    /* Trigger event card selection */
    document.querySelectorAll('.trigger-event-card').forEach(function (card) {
      card.addEventListener('click', function () {
        document.querySelectorAll('.trigger-event-card').forEach(function (c) {
          c.classList.remove('active');
        });
        this.classList.add('active');
        updateTriggerConditions();
      });
    });

    updateTriggerConfig();
    applyTierBadgeContrast();
  }

  function handleActions(e) {
    if (e.target.closest('[data-action="next-step"]')) {
      nextStep();
      return;
    }
    if (e.target.closest('[data-action="prev-step"]')) {
      previousStep();
      return;
    }
    if (e.target.closest('[data-action="add-action"]')) {
      addAction();
      return;
    }
    const removeBtn = e.target.closest('[data-action="remove-action"]');
    if (removeBtn) {
      removeAction(removeBtn);
    }
  }

  function showStep(step) {
    document.querySelectorAll('.wizard-step').forEach(function (el) {
      el.classList.remove('active');
    });
    const stepEl = document.getElementById('step-' + step);
    if (stepEl) {
      stepEl.classList.add('active');
    }

    document.querySelectorAll('.wizard-steps .step').forEach(function (el, index) {
      el.classList.remove('active', 'completed');
      if (index + 1 < step) {
        el.classList.add('completed');
      } else if (index + 1 === step) {
        el.classList.add('active');
      }
    });

    document.querySelectorAll('.step-connector').forEach(function (el, index) {
      el.classList.toggle('active', index < step - 1);
    });

    if (step === 5) {
      updateSummary();
    }
  }

  function nextStep() {
    if (validateStep(currentStep) && currentStep < totalSteps) {
      currentStep++;
      showStep(currentStep);
      window.scrollTo(0, 0);
    }
  }

  function previousStep() {
    if (currentStep > 1) {
      currentStep--;
      showStep(currentStep);
      window.scrollTo(0, 0);
    }
  }

  function validateStep(step) {
    if (step === 1) {
      const nameEl = document.getElementById('name');
      if (!nameEl || !nameEl.value.trim()) {
        AdminModal.alert({
          message: translations.enterCampaignName || 'Please enter a campaign name.',
          type: 'warning',
        });
        if (nameEl) {
          nameEl.focus();
        }
        return false;
      }
    }
    if (step === 2) {
      const typeInput = document.querySelector('input[name="campaign_type"]:checked');
      if (typeInput && typeInput.value === 'trigger_based') {
        const triggerEvent = document.querySelector('input[name="trigger_event"]:checked');
        if (!triggerEvent) {
          AdminModal.alert({
            message: translations.selectTrigger || 'Please select a trigger event.',
            type: 'warning',
          });
          return false;
        }
      }
    }
    return true;
  }

  function updateTriggerConfig() {
    const typeInput = document.querySelector('input[name="campaign_type"]:checked');
    if (!typeInput) {
      return;
    }
    const selectedType = typeInput.value;

    document.querySelectorAll('.trigger-config').forEach(function (el) {
      el.classList.add('wizard-hidden');
    });

    const configEl = document.getElementById('config-' + selectedType);
    if (configEl) {
      configEl.classList.remove('wizard-hidden');
    }
  }

  function updateTriggerConditions() {
    const selectedEvent = document.querySelector('input[name="trigger_event"]:checked');
    if (!selectedEvent) {
      return;
    }

    document.querySelectorAll('.trigger-conditions').forEach(function (el) {
      el.classList.add('wizard-hidden');
    });

    const conditionsEl = document.getElementById('conditions-' + selectedEvent.value);
    if (conditionsEl) {
      conditionsEl.classList.remove('wizard-hidden');
    }
  }

  function updateScheduleDisplay(value) {
    const weekly = document.querySelector('.schedule-weekly');
    const monthly = document.querySelector('.schedule-monthly');
    if (weekly) {
      weekly.classList.toggle('wizard-hidden', value !== 'weekly');
    }
    if (monthly) {
      monthly.classList.toggle('wizard-hidden', value !== 'monthly');
    }
  }

  function addAction() {
    const container = document.getElementById('actions-container');
    if (!container) {
      return;
    }
    const template = container.querySelector('.action-item');
    if (!template) {
      return;
    }
    const clone = template.cloneNode(true);

    clone.setAttribute('data-action-index', actionIndex);
    const numEl = clone.querySelector('.action-number');
    if (numEl) {
      numEl.textContent = (translations.action || 'Action') + ' ' + (actionIndex + 1);
    }
    const removeBtn = clone.querySelector('[data-action="remove-action"]');
    if (removeBtn) {
      removeBtn.classList.remove('wizard-hidden');
    }

    clone.querySelectorAll('input, select').forEach(function (el) {
      if (el.type === 'number') {
        el.value = el.defaultValue || '';
      } else if (el.type === 'text') {
        el.value = '';
      } else if (el.tagName === 'SELECT') {
        el.selectedIndex = 0;
      }
    });

    clone.querySelectorAll('.action-field-group').forEach(function (el) {
      el.classList.toggle('wizard-hidden', el.getAttribute('data-action') !== 'award_points');
    });

    container.appendChild(clone);
    actionIndex++;
  }

  function removeAction(btn) {
    const actionItem = btn.closest('.action-item');
    if (!actionItem) {
      return;
    }
    if (document.querySelectorAll('.action-item').length > 1) {
      actionItem.remove();
      document.querySelectorAll('.action-item').forEach(function (item, idx) {
        const numEl = item.querySelector('.action-number');
        if (numEl) {
          numEl.textContent = (translations.action || 'Action') + ' ' + (idx + 1);
        }
      });
    }
  }

  function updateActionFields(select) {
    const actionItem = select.closest('.action-item');
    if (!actionItem) {
      return;
    }
    const selectedAction = select.value;
    actionItem.querySelectorAll('.action-field-group').forEach(function (el) {
      el.classList.toggle('wizard-hidden', el.getAttribute('data-action') !== selectedAction);
    });
  }

  function updateSummary() {
    const nameEl = document.getElementById('name');
    const name =
      nameEl && nameEl.value ? nameEl.value : translations.untitledCampaign || 'Untitled Campaign';

    const typeInput = document.querySelector('input[name="campaign_type"]:checked');
    const campaignType = typeInput ? typeInput.value : '';

    const triggerInput = document.querySelector('input[name="trigger_event"]:checked');
    const triggerEvent = triggerInput ? triggerInput.value : '';

    const targetAllEl = document.getElementById('target_all_members');
    const targetAll = targetAllEl ? targetAllEl.checked : true;

    const actionCount = document.querySelectorAll('.action-item').length;

    let triggerRow = '';
    if (campaignType === 'trigger_based' && triggerEvent) {
      triggerRow =
        '<div class="summary-row">' +
        '<span class="summary-label">' +
        (translations.trigger || 'Trigger') +
        '</span>' +
        '<span class="summary-value">' +
        (eventLabels[triggerEvent] || triggerEvent) +
        '</span>' +
        '</div>';
    }

    const html =
      '<div class="summary-card">' +
      '<div class="summary-row">' +
      '<span class="summary-label">' +
      (translations.campaignName || 'Campaign Name') +
      '</span>' +
      '<span class="summary-value">' +
      name +
      '</span>' +
      '</div>' +
      '<div class="summary-row">' +
      '<span class="summary-label">' +
      (translations.type || 'Type') +
      '</span>' +
      '<span class="summary-value">' +
      (typeLabels[campaignType] || campaignType) +
      '</span>' +
      '</div>' +
      triggerRow +
      '<div class="summary-row">' +
      '<span class="summary-label">' +
      (translations.targeting || 'Targeting') +
      '</span>' +
      '<span class="summary-value">' +
      (targetAll
        ? translations.allMembers || 'All Members'
        : translations.specificSegments || 'Specific Segments/Tiers') +
      '</span>' +
      '</div>' +
      '<div class="summary-row">' +
      '<span class="summary-label">' +
      (translations.actions || 'Actions') +
      '</span>' +
      '<span class="summary-value">' +
      actionCount +
      ' ' +
      (translations.actionsConfigured || 'action(s) configured') +
      '</span>' +
      '</div>' +
      '</div>';

    const summaryEl = document.getElementById('campaign-summary');
    if (summaryEl) {
      summaryEl.innerHTML = html;
    }
  }

  function applyTierBadgeContrast() {
    document.querySelectorAll('.tier-badge[data-color]').forEach(function (badge) {
      const bgColor = badge.dataset.color;
      if (!bgColor) {
        return;
      }
      badge.style.backgroundColor = bgColor;
      const rgb = parseColor(bgColor);
      if (!rgb) {
        return;
      }
      const luminance = getRelativeLuminance(rgb.r, rgb.g, rgb.b);
      badge.style.color = luminance > 0.5 ? '#1f2937' : '#ffffff';
    });
  }

  function parseColor(colorStr) {
    const rgbMatch = colorStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
    if (rgbMatch) {
      return { r: parseInt(rgbMatch[1]), g: parseInt(rgbMatch[2]), b: parseInt(rgbMatch[3]) };
    }
    const hexMatch = colorStr.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
    if (hexMatch) {
      return {
        r: parseInt(hexMatch[1], 16),
        g: parseInt(hexMatch[2], 16),
        b: parseInt(hexMatch[3], 16),
      };
    }
    return null;
  }

  function getRelativeLuminance(r, g, b) {
    const sRGB = [r, g, b].map(function (val) {
      val = val / 255;
      return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * sRGB[0] + 0.7152 * sRGB[1] + 0.0722 * sRGB[2];
  }

  document.addEventListener('DOMContentLoaded', init);
})();
