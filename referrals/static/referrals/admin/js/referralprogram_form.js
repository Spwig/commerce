/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  /** Load config and i18n strings from page data island */
  let _cfg = {};
  function getCfg() {
    if (_cfg.loaded) return _cfg;
    const el = document.getElementById('referralprogram-form-config');
    if (el) {
      try {
        _cfg = JSON.parse(el.textContent || '{}');
      } catch (e) {
        _cfg = {};
      }
    }
    _cfg.loaded = true;
    _cfg.i18n = _cfg.i18n || {};
    _cfg.currency_symbol = _cfg.currency_symbol || '$';
    return _cfg;
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Tab switching handled by global AdminTabs utility
    initSaveButtons();
    initModals();
    initConfigButtons();
    loadExistingConfigs();
  });

  //==========================================================================
  // SAVE BUTTONS
  //==========================================================================
  function initSaveButtons() {
    const form = document.getElementById('program-form');
    const saveContinueBtn = document.getElementById('save-continue-btn');

    if (saveContinueBtn && form) {
      saveContinueBtn.addEventListener('click', function () {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = '_continue';
        input.value = '1';
        form.appendChild(input);
        form.submit();
      });
    }
  }

  //==========================================================================
  // MODAL MANAGEMENT
  //==========================================================================
  function initModals() {
    // Close modal buttons
    document.querySelectorAll('.admin-modal-close, .referral-modal-btn-secondary').forEach(btn => {
      btn.addEventListener('click', function () {
        const modalId = this.getAttribute('data-modal');
        if (modalId) closeModal(modalId);
      });
    });

    // Close on overlay click
    document.querySelectorAll('.admin-modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', function (e) {
        if (e.target === this) closeModal(this.id);
      });
    });

    // Escape key to close
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        const openModal = document.querySelector('.admin-modal-overlay.active');
        if (openModal) closeModal(openModal.id);
      }
    });

    // Dynamic field behavior
    initRewardModalBehavior();
    initEligibilityModalBehavior();
  }

  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add('active');
      document.body.classList.add('admin-modal-body-locked');
    }
  }

  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove('active');
      document.body.classList.remove('admin-modal-body-locked');
    }
  }

  //==========================================================================
  // CONFIG BUTTON HANDLERS
  //==========================================================================
  function initConfigButtons() {
    // Reward Config
    document.getElementById('open-reward-modal')?.addEventListener('click', () => {
      loadRewardConfig();
      openModal('reward-config-modal');
    });
    document.getElementById('save-reward-config')?.addEventListener('click', saveRewardConfig);

    // Eligibility Rules
    document.getElementById('open-eligibility-modal')?.addEventListener('click', () => {
      loadEligibilityConfig();
      openModal('eligibility-modal');
    });
    document
      .getElementById('save-eligibility-config')
      ?.addEventListener('click', saveEligibilityConfig);

    // Timing Config
    document.getElementById('open-timing-modal')?.addEventListener('click', () => {
      loadTimingConfig();
      openModal('timing-modal');
    });
    document.getElementById('save-timing-config')?.addEventListener('click', saveTimingConfig);

    // Caps Config
    document.getElementById('open-caps-modal')?.addEventListener('click', () => {
      loadCapsConfig();
      openModal('caps-modal');
    });
    document.getElementById('save-caps-config')?.addEventListener('click', saveCapsConfig);

    // Tracking Config
    document.getElementById('open-tracking-modal')?.addEventListener('click', () => {
      loadTrackingConfig();
      openModal('tracking-modal');
    });
    document.getElementById('save-tracking-config')?.addEventListener('click', saveTrackingConfig);

    // Fraud Policy
    document.getElementById('open-fraud-modal')?.addEventListener('click', () => {
      loadFraudConfig();
      openModal('fraud-modal');
    });
    document.getElementById('save-fraud-config')?.addEventListener('click', saveFraudConfig);
  }

  //==========================================================================
  // LOAD EXISTING CONFIGURATIONS
  //==========================================================================
  function loadExistingConfigs() {
    // Update all preview boxes with existing data
    updateRewardPreview();
    updateEligibilityPreview();
    updateTimingPreview();
    updateCapsPreview();
    updateTrackingPreview();
    updateFraudPreview();
  }

  //==========================================================================
  // REWARD CONFIGURATION
  //==========================================================================
  function initRewardModalBehavior() {
    // Toggle referee fields based on enabled checkbox
    const refereeEnabled = document.getElementById('reward-referee-enabled');
    const refereeConfig = document.getElementById('referee-rewards-config');

    refereeEnabled?.addEventListener('change', function () {
      if (refereeConfig) {
        refereeConfig.style.display = this.checked ? 'block' : 'none';
      }
    });

    // Update currency symbols based on reward type
    ['referrer', 'referee'].forEach(role => {
      const typeSelect = document.getElementById(`reward-${role}-type`);
      const unitSpan = document.getElementById(`reward-${role}-unit`);
      const percentRow = document.getElementById(`reward-${role}-percent-row`);

      typeSelect?.addEventListener('change', function () {
        const type = this.value;
        const cfg = getCfg();
        if (unitSpan) {
          if (type === 'points') {
            unitSpan.textContent = cfg.i18n.pts || 'pts';
          } else if (type === 'discount') {
            unitSpan.textContent = '%';
          } else {
            unitSpan.textContent = cfg.currency_symbol;
          }
        }
        if (percentRow) {
          percentRow.style.display = type === 'discount' || type === 'credit' ? 'block' : 'none';
        }
      });
    });
  }

  function loadRewardConfig() {
    const config = getJSONField('id_reward_config');

    // Referrer
    setFieldValue('reward-referrer-enabled', config.referrer?.enabled ?? true);
    setFieldValue('reward-referrer-type', config.referrer?.kind ?? 'credit');
    setFieldValue('reward-referrer-amount', config.referrer?.amount ?? '');
    setFieldValue('reward-referrer-percent', config.referrer?.is_percentage ?? false);

    // Referee
    setFieldValue('reward-referee-enabled', config.referee?.enabled ?? true);
    setFieldValue('reward-referee-type', config.referee?.kind ?? 'discount');
    setFieldValue('reward-referee-amount', config.referee?.amount ?? '');
    setFieldValue('reward-referee-percent', config.referee?.is_percentage ?? false);

    // Delivery
    setFieldValue('reward-auto-apply', config.auto_apply ?? false);
    setFieldValue('reward-expiry-days', config.expiry_days ?? 90);

    // Trigger UI updates
    document.getElementById('reward-referrer-type')?.dispatchEvent(new Event('change'));
    document.getElementById('reward-referee-type')?.dispatchEvent(new Event('change'));
    document.getElementById('reward-referee-enabled')?.dispatchEvent(new Event('change'));
  }

  function saveRewardConfig() {
    const config = {
      referrer: {
        enabled: getFieldValue('reward-referrer-enabled'),
        kind: getFieldValue('reward-referrer-type'),
        amount: parseFloat(getFieldValue('reward-referrer-amount')) || 0,
        is_percentage: getFieldValue('reward-referrer-percent'),
      },
      referee: {
        enabled: getFieldValue('reward-referee-enabled'),
        kind: getFieldValue('reward-referee-type'),
        amount: parseFloat(getFieldValue('reward-referee-amount')) || 0,
        is_percentage: getFieldValue('reward-referee-percent'),
      },
      auto_apply: getFieldValue('reward-auto-apply'),
      expiry_days: parseInt(getFieldValue('reward-expiry-days')) || 0,
    };

    setJSONField('id_reward_config', config);
    updateRewardPreview();
    closeModal('reward-config-modal');
  }

  function updateRewardPreview() {
    const config = getJSONField('id_reward_config');
    const preview = document.getElementById('reward-config-preview');
    const cfg = getCfg();

    if (!preview) return;

    if (!config.referrer && !config.referee) {
      preview.innerHTML =
        '<p class="empty-state">' +
        (cfg.i18n.configure_rewards_empty ||
          "Click 'Configure Rewards' to set up your reward structure.") +
        '</p>';
      return;
    }

    const cs = cfg.currency_symbol;
    let html = '<div class="config-summary">';

    if (config.referrer?.enabled) {
      const amount = config.referrer.is_percentage
        ? `${config.referrer.amount}%`
        : `${cs}${config.referrer.amount}`;
      html += `<div class="summary-item"><strong>${cfg.i18n.referrer || 'Referrer'}:</strong> ${amount} ${config.referrer.kind}</div>`;
    }

    if (config.referee?.enabled) {
      const amount = config.referee.is_percentage
        ? `${config.referee.amount}%`
        : `${cs}${config.referee.amount}`;
      html += `<div class="summary-item"><strong>${cfg.i18n.referee || 'Referee'}:</strong> ${amount} ${config.referee.kind}</div>`;
    }

    if (config.expiry_days > 0) {
      html += `<div class="summary-item"><strong>${cfg.i18n.expiry || 'Expiry'}:</strong> ${config.expiry_days} ${cfg.i18n.days || 'days'}</div>`;
    }

    html += '</div>';
    preview.innerHTML = html;
  }

  //==========================================================================
  // ELIGIBILITY CONFIGURATION
  //==========================================================================
  function initEligibilityModalBehavior() {
    // No special behavior needed for now
  }

  function loadEligibilityConfig() {
    const config = getJSONField('id_eligibility_rules');

    // Referrer requirements
    setFieldValue('elig-referrer-min-orders', config.referrer_min_orders ?? 1);
    setFieldValue('elig-referrer-min-spend', config.referrer_min_spend ?? 0);
    setFieldValue('elig-exclude-staff', config.exclude_staff ?? true);

    // Referee requirements
    setFieldValue('elig-new-customers-only', config.new_customers_only ?? true);
    setFieldValue('elig-referee-min-order-value', config.referee_min_order_value ?? 0);
    setFieldValue('elig-require-email-verify', config.require_email_verification ?? false);

    // Product/category restrictions
    setFieldValue('elig-exclude-sale-items', config.exclude_sale_items ?? false);
    setFieldValue('elig-allowed-categories', (config.allowed_categories || []).join(','));
    setFieldValue('elig-excluded-products', (config.excluded_products || []).join(','));
  }

  function saveEligibilityConfig() {
    const allowedCats = getFieldValue('elig-allowed-categories')
      .split(',')
      .filter(x => x.trim())
      .map(x => parseInt(x.trim()));
    const excludedProds = getFieldValue('elig-excluded-products')
      .split(',')
      .filter(x => x.trim())
      .map(x => parseInt(x.trim()));

    const config = {
      referrer_min_orders: parseInt(getFieldValue('elig-referrer-min-orders')) || 0,
      referrer_min_spend: parseFloat(getFieldValue('elig-referrer-min-spend')) || 0,
      exclude_staff: getFieldValue('elig-exclude-staff'),
      new_customers_only: getFieldValue('elig-new-customers-only'),
      referee_min_order_value: parseFloat(getFieldValue('elig-referee-min-order-value')) || 0,
      require_email_verification: getFieldValue('elig-require-email-verify'),
      exclude_sale_items: getFieldValue('elig-exclude-sale-items'),
      allowed_categories: allowedCats,
      excluded_products: excludedProds,
    };

    setJSONField('id_eligibility_rules', config);
    updateEligibilityPreview();
    closeModal('eligibility-modal');
  }

  function updateEligibilityPreview() {
    const config = getJSONField('id_eligibility_rules');
    const preview = document.getElementById('eligibility-config-preview');
    const cfg = getCfg();

    if (!preview) return;

    if (Object.keys(config).length === 0) {
      preview.innerHTML =
        '<p class="empty-state">' +
        (cfg.i18n.configure_eligibility_empty ||
          "Click 'Configure Eligibility' to set up participation rules.") +
        '</p>';
      return;
    }

    let html = '<div class="config-summary">';

    if (config.new_customers_only) {
      html +=
        '<div class="summary-item">✓ ' +
        (cfg.i18n.new_customers_only || 'New customers only') +
        '</div>';
    }
    if (config.referee_min_order_value > 0) {
      html += `<div class="summary-item"><strong>${cfg.i18n.min_order || 'Min order'}:</strong> ${cfg.currency_symbol}${config.referee_min_order_value}</div>`;
    }
    if (config.referrer_min_orders > 0) {
      html += `<div class="summary-item"><strong>${cfg.i18n.referrer_min_orders || 'Referrer min orders'}:</strong> ${config.referrer_min_orders}</div>`;
    }

    html += '</div>';
    preview.innerHTML = html;
  }

  //==========================================================================
  // TIMING CONFIGURATION
  //==========================================================================
  function loadTimingConfig() {
    const config = getJSONField('id_timing_config');

    setFieldValue('timing-cookie-ttl', config.cookie_ttl_days ?? 30);
    setFieldValue('timing-attribution-method', config.attribution_method ?? 'last-click');
    setFieldValue('timing-referrer-when', config.referrer_reward_when ?? 'first-order');
    setFieldValue('timing-referee-when', config.referee_reward_when ?? 'first-order');
    setFieldValue('timing-refund-window-days', config.refund_window_days ?? 30);
    setFieldValue('timing-auto-approve', config.auto_approve ?? true);
    setFieldValue('timing-batch-process', config.batch_process ?? false);
  }

  function saveTimingConfig() {
    const config = {
      cookie_ttl_days: parseInt(getFieldValue('timing-cookie-ttl')) || 30,
      attribution_method: getFieldValue('timing-attribution-method'),
      referrer_reward_when: getFieldValue('timing-referrer-when'),
      referee_reward_when: getFieldValue('timing-referee-when'),
      refund_window_days: parseInt(getFieldValue('timing-refund-window-days')) || 0,
      auto_approve: getFieldValue('timing-auto-approve'),
      batch_process: getFieldValue('timing-batch-process'),
    };

    setJSONField('id_timing_config', config);
    updateTimingPreview();
    closeModal('timing-modal');
  }

  function updateTimingPreview() {
    const config = getJSONField('id_timing_config');
    const preview = document.getElementById('timing-config-preview');
    const cfg = getCfg();

    if (!preview) return;

    if (Object.keys(config).length === 0) {
      preview.innerHTML =
        '<p class="empty-state">' +
        (cfg.i18n.configure_timing_empty ||
          "Click 'Configure Timing' to set up reward timing rules.") +
        '</p>';
      return;
    }

    let html = '<div class="config-summary">';
    html += `<div class="summary-item"><strong>${cfg.i18n.cookie_ttl || 'Cookie TTL'}:</strong> ${config.cookie_ttl_days || 30} ${cfg.i18n.days || 'days'}</div>`;
    html += `<div class="summary-item"><strong>${cfg.i18n.attribution || 'Attribution'}:</strong> ${config.attribution_method || 'last-click'}</div>`;
    html += `<div class="summary-item"><strong>${cfg.i18n.issue_rewards || 'Issue rewards'}:</strong> ${config.referrer_reward_when || 'first-order'}</div>`;
    html += '</div>';
    preview.innerHTML = html;
  }

  //==========================================================================
  // CAPS CONFIGURATION
  //==========================================================================
  function loadCapsConfig() {
    const config = getJSONField('id_caps_config');

    setFieldValue('caps-max-referrals-month', config.max_referrals_per_month ?? 0);
    setFieldValue('caps-max-referrals-lifetime', config.max_referrals_lifetime ?? 0);
    setFieldValue('caps-max-reward-month', config.max_reward_per_month ?? 0);
    setFieldValue('caps-max-reward-lifetime', config.max_reward_lifetime ?? 0);
    setFieldValue('caps-max-uses-per-referee', config.max_uses_per_referee ?? 1);
    setFieldValue('caps-max-budget-month', config.program_budget_monthly ?? 0);
    setFieldValue('caps-pause-when-exceeded', config.pause_when_exceeded ?? false);
  }

  function saveCapsConfig() {
    const config = {
      max_referrals_per_month: parseInt(getFieldValue('caps-max-referrals-month')) || 0,
      max_referrals_lifetime: parseInt(getFieldValue('caps-max-referrals-lifetime')) || 0,
      max_reward_per_month: parseFloat(getFieldValue('caps-max-reward-month')) || 0,
      max_reward_lifetime: parseFloat(getFieldValue('caps-max-reward-lifetime')) || 0,
      max_uses_per_referee: parseInt(getFieldValue('caps-max-uses-per-referee')) || 1,
      program_budget_monthly: parseFloat(getFieldValue('caps-max-budget-month')) || 0,
      pause_when_exceeded: getFieldValue('caps-pause-when-exceeded'),
    };

    setJSONField('id_caps_config', config);
    updateCapsPreview();
    closeModal('caps-modal');
  }

  function updateCapsPreview() {
    const config = getJSONField('id_caps_config');
    const preview = document.getElementById('caps-config-preview');
    const cfg = getCfg();

    if (!preview) return;

    if (Object.keys(config).length === 0) {
      preview.innerHTML =
        '<p class="empty-state">' +
        (cfg.i18n.configure_limits_empty || "Click 'Configure Limits' to set up reward caps.") +
        '</p>';
      return;
    }

    const cs = cfg.currency_symbol;
    let html = '<div class="config-summary">';

    if (config.max_referrals_per_month > 0) {
      html += `<div class="summary-item"><strong>${cfg.i18n.max_per_month || 'Max/month'}:</strong> ${config.max_referrals_per_month} ${cfg.i18n.referrals || 'referrals'}</div>`;
    }
    if (config.max_reward_per_month > 0) {
      html += `<div class="summary-item"><strong>${cfg.i18n.max_reward_per_month || 'Max reward/month'}:</strong> ${cs}${config.max_reward_per_month}</div>`;
    }
    if (config.program_budget_monthly > 0) {
      html += `<div class="summary-item"><strong>${cfg.i18n.program_budget || 'Program budget'}:</strong> ${cs}${config.program_budget_monthly}${cfg.i18n.per_month || '/month'}</div>`;
    }

    html += '</div>';
    preview.innerHTML = html;
  }

  //==========================================================================
  // TRACKING CONFIGURATION
  //==========================================================================
  function loadTrackingConfig() {
    const config = getJSONField('id_tracking_config');

    setFieldValue('tracking-param-name', config.param_name ?? 'ref');
    setFieldValue('tracking-code-format', config.code_format ?? 'custom-slug');
    setFieldValue('tracking-allow-custom-codes', config.allow_custom_codes ?? true);
    setFieldValue('tracking-conversion-event', config.conversion_event ?? 'first-order');
    setFieldValue('tracking-count-clicks', config.track_clicks ?? true);
    setFieldValue('tracking-count-signups', config.track_signups ?? true);
    setFieldValue('tracking-use-ip-fingerprint', config.use_ip_fingerprint ?? false);
    setFieldValue('tracking-cross-device', config.cross_device_tracking ?? false);
    setFieldValue('tracking-analytics-integration', config.analytics_integration ?? false);
  }

  function saveTrackingConfig() {
    const config = {
      param_name: getFieldValue('tracking-param-name') || 'ref',
      code_format: getFieldValue('tracking-code-format'),
      allow_custom_codes: getFieldValue('tracking-allow-custom-codes'),
      conversion_event: getFieldValue('tracking-conversion-event'),
      track_clicks: getFieldValue('tracking-count-clicks'),
      track_signups: getFieldValue('tracking-count-signups'),
      use_ip_fingerprint: getFieldValue('tracking-use-ip-fingerprint'),
      cross_device_tracking: getFieldValue('tracking-cross-device'),
      analytics_integration: getFieldValue('tracking-analytics-integration'),
    };

    setJSONField('id_tracking_config', config);
    updateTrackingPreview();
    closeModal('tracking-modal');
  }

  function updateTrackingPreview() {
    const config = getJSONField('id_tracking_config');
    const preview = document.getElementById('tracking-config-preview');
    const cfg = getCfg();

    if (!preview) return;

    if (Object.keys(config).length === 0) {
      preview.innerHTML =
        '<p class="empty-state">' +
        (cfg.i18n.configure_tracking_empty ||
          "Click 'Configure Tracking' to set up tracking settings.") +
        '</p>';
      return;
    }

    let html = '<div class="config-summary">';
    html += `<div class="summary-item"><strong>${cfg.i18n.url_param || 'URL param'}:</strong> ?${config.param_name || 'ref'}=CODE</div>`;
    html += `<div class="summary-item"><strong>${cfg.i18n.code_format || 'Code format'}:</strong> ${config.code_format || 'custom-slug'}</div>`;
    html += `<div class="summary-item"><strong>${cfg.i18n.conversion || 'Conversion'}:</strong> ${config.conversion_event || 'first-order'}</div>`;
    html += '</div>';
    preview.innerHTML = html;
  }

  //==========================================================================
  // FRAUD CONFIGURATION
  //==========================================================================
  function loadFraudConfig() {
    const config = getJSONField('id_fraud_policy');

    setFieldValue('fraud-policy-level', config.policy_level ?? 'balanced');
    setFieldValue('fraud-auto-reject-threshold', config.auto_reject_threshold ?? 80);
    setFieldValue('fraud-manual-review-threshold', config.manual_review_threshold ?? 50);
    setFieldValue('fraud-check-same-ip', config.check_same_ip ?? true);
    setFieldValue('fraud-check-same-device', config.check_same_device ?? true);
    setFieldValue('fraud-check-rapid-signups', config.check_rapid_signups ?? true);
    setFieldValue('fraud-rapid-signup-threshold', config.rapid_signup_hours ?? 24);
    setFieldValue('fraud-check-similar-emails', config.check_similar_emails ?? false);
    setFieldValue('fraud-check-disposable-emails', config.check_disposable_emails ?? true);
    setFieldValue('fraud-require-verification', config.require_verification ?? false);
    setFieldValue('fraud-delay-rewards', config.delay_flagged_rewards ?? true);
    setFieldValue('fraud-delay-days', config.delay_days ?? 7);
    setFieldValue('fraud-ban-repeat-offenders', config.ban_repeat_offenders ?? false);
  }

  function saveFraudConfig() {
    const config = {
      policy_level: getFieldValue('fraud-policy-level'),
      auto_reject_threshold: parseInt(getFieldValue('fraud-auto-reject-threshold')) || 80,
      manual_review_threshold: parseInt(getFieldValue('fraud-manual-review-threshold')) || 50,
      check_same_ip: getFieldValue('fraud-check-same-ip'),
      check_same_device: getFieldValue('fraud-check-same-device'),
      check_rapid_signups: getFieldValue('fraud-check-rapid-signups'),
      rapid_signup_hours: parseInt(getFieldValue('fraud-rapid-signup-threshold')) || 24,
      check_similar_emails: getFieldValue('fraud-check-similar-emails'),
      check_disposable_emails: getFieldValue('fraud-check-disposable-emails'),
      require_verification: getFieldValue('fraud-require-verification'),
      delay_flagged_rewards: getFieldValue('fraud-delay-rewards'),
      delay_days: parseInt(getFieldValue('fraud-delay-days')) || 0,
      ban_repeat_offenders: getFieldValue('fraud-ban-repeat-offenders'),
    };

    setJSONField('id_fraud_policy', config);
    updateFraudPreview();
    closeModal('fraud-modal');
  }

  function updateFraudPreview() {
    const config = getJSONField('id_fraud_policy');
    const preview = document.getElementById('fraud-config-preview');
    const cfg = getCfg();

    if (!preview) return;

    if (Object.keys(config).length === 0) {
      preview.innerHTML =
        '<p class="empty-state">' +
        (cfg.i18n.configure_fraud_empty ||
          "Click 'Configure Fraud Detection' to set up fraud prevention.") +
        '</p>';
      return;
    }

    let html = '<div class="config-summary">';
    html += `<div class="summary-item"><strong>${cfg.i18n.policy || 'Policy'}:</strong> ${config.policy_level || 'balanced'}</div>`;
    html += `<div class="summary-item"><strong>${cfg.i18n.auto_reject_at || 'Auto-reject at'}:</strong> ${config.auto_reject_threshold || 80}% ${cfg.i18n.risk || 'risk'}</div>`;
    html += `<div class="summary-item"><strong>${cfg.i18n.manual_review_at || 'Manual review at'}:</strong> ${config.manual_review_threshold || 50}% ${cfg.i18n.risk || 'risk'}</div>`;
    html += '</div>';
    preview.innerHTML = html;
  }

  //==========================================================================
  // UTILITY FUNCTIONS
  //==========================================================================
  function getFieldValue(id) {
    const field = document.getElementById(id);
    if (!field) return null;

    if (field.type === 'checkbox') {
      return field.checked;
    }
    return field.value;
  }

  function setFieldValue(id, value) {
    const field = document.getElementById(id);
    if (!field) return;

    if (field.type === 'checkbox') {
      field.checked = !!value;
    } else {
      field.value = value ?? '';
    }
  }

  function getJSONField(id) {
    const field = document.getElementById(id);
    if (!field || !field.value) return {};

    try {
      return JSON.parse(field.value) || {};
    } catch (e) {
      console.error('Error parsing JSON field:', id, e);
      return {};
    }
  }

  function setJSONField(id, value) {
    const field = document.getElementById(id);
    if (!field) return;

    field.value = JSON.stringify(value);
  }
})();
