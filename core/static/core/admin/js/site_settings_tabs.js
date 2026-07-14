/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Site Settings Tab Management
 * Handles tab switching, error navigation, and state persistence for site settings admin
 */

(function ($) {
  'use strict';

  // Field to tab mapping - populated from data attribute or auto-discovered from DOM
  let fieldTabMap = {};

  // Tab name translations
  const tabNames = {
    general: gettext('General'),
    contact: gettext('Contact'),
    locale: gettext('Locale'),
    multicurrency: gettext('Multi-Currency'),
    ecommerce: gettext('Commerce'),
    shipping: gettext('Shipping'),
    authentication: gettext('Security'),
    advanced: gettext('Advanced'),
    pages: gettext('Pages & SEO'),
    cookies: gettext('Cookies'),
    'domain-ssl': gettext('Domain & SSL'),
  };

  $(document).ready(function () {
    // Tab switching handled by global AdminTabs utility

    // Initialize field-tab mapping first
    initializeFieldTabMapping();

    // Initialize error handling (badges, navigation, etc.)
    initializeErrorHandling();

    // Initialize compliance bar width from data attribute
    initializeComplianceBar();

    // Initialize character counters
    initializeCharacterCounters();

    // Initialize maintenance mode warning
    initializeMaintenanceWarning();

    // Initialize 2FA enforcement settings
    initialize2FAEnforcement();

    // Initialize multi-currency toggle
    initializeMultiCurrencyToggle();
  });

  /**
   * Initialize field to tab mapping from DOM data attribute or auto-discover
   */
  function initializeFieldTabMapping() {
    const $tabsContainer = $('#settings-tabs');
    if ($tabsContainer.length && $tabsContainer.data('field-tab-map')) {
      fieldTabMap = $tabsContainer.data('field-tab-map');
    }

    // Fallback: auto-discover from DOM if not provided
    if (Object.keys(fieldTabMap).length === 0) {
      discoverFieldTabMappingFromDOM();
    }
  }

  /**
   * Auto-discover field-to-tab mapping by scanning DOM
   */
  function discoverFieldTabMappingFromDOM() {
    $('.tab-panel').each(function () {
      const tabId = $(this).data('panel');
      $(this)
        .find('.form-row[class*="field-"]')
        .each(function () {
          const classes = $(this).attr('class').split(' ');
          classes.forEach(function (cls) {
            if (cls.startsWith('field-')) {
              const fieldName = cls.replace('field-', '');
              fieldTabMap[fieldName] = tabId;
            }
          });
        });
    });
  }

  /**
   * Initialize error handling - badges, navigation, and highlighting
   */
  function initializeErrorHandling() {
    // Only proceed if there are errors
    if ($('#error-summary').length === 0) {
      return;
    }

    // Count errors per tab and add badges
    addErrorBadgesToTabs();

    // Add tab indicator text to error items
    populateErrorTabIndicators();

    // Make error summary links clickable
    bindErrorLinkHandlers();

    // Auto-switch to first tab with errors
    switchToFirstErrorTab();
  }

  /**
   * Add error count badges to tabs that have errors
   */
  function addErrorBadgesToTabs() {
    const errorCounts = {};

    // Count errors per tab using field-tab mapping
    $('.error-item[data-field]').each(function () {
      const fieldName = $(this).data('field');
      const tabId = fieldTabMap[fieldName];
      if (tabId) {
        errorCounts[tabId] = (errorCounts[tabId] || 0) + 1;
      }
    });

    // Add badges via AdminTabs API
    Object.keys(errorCounts).forEach(function (tabId) {
      if (window.AdminTabs) {
        window.AdminTabs.addErrorBadge(tabId, errorCounts[tabId]);
      }
    });
  }

  /**
   * Populate tab indicator text for each error item
   */
  function populateErrorTabIndicators() {
    $('.error-item[data-field]').each(function () {
      const fieldName = $(this).data('field');
      const tabId = fieldTabMap[fieldName];
      const tabName = tabNames[tabId] || tabId;

      if (tabName) {
        $(this)
          .find('.error-tab-indicator')
          .text(' (' + tabName + ' ' + gettext('tab') + ')');
      }
    });
  }

  /**
   * Bind click handlers to error links
   */
  function bindErrorLinkHandlers() {
    $('.error-link').on('click', function (e) {
      e.preventDefault();
      const fieldName = $(this).data('field');
      navigateToField(fieldName);
    });
  }

  /**
   * Navigate to a specific field - switch tab and scroll
   */
  function navigateToField(fieldName) {
    const tabId = fieldTabMap[fieldName];

    if (tabId) {
      // Switch to the correct tab via AdminTabs
      if (window.AdminTabs) {
        window.AdminTabs.switchTo(tabId);
      }

      // Wait for tab switch animation
      setTimeout(function () {
        // Find and highlight the field
        const $fieldRow = $(`.form-row.field-${fieldName}`);

        if ($fieldRow.length) {
          // Scroll to field
          $('html, body').animate(
            {
              scrollTop: $fieldRow.offset().top - 120,
            },
            300
          );

          // Highlight field temporarily
          highlightField($fieldRow);
        }
      }, 150);
    }
  }

  /**
   * Highlight a field row temporarily
   */
  function highlightField($fieldRow) {
    $fieldRow.addClass('field-highlight-error');

    // Remove highlight after delay
    setTimeout(function () {
      $fieldRow.removeClass('field-highlight-error');
    }, 3000);
  }

  /**
   * Switch to the first tab that has errors
   */
  function switchToFirstErrorTab() {
    const $firstErrorTab = $('.admin-tab-btn.has-errors').first();
    if ($firstErrorTab.length && window.AdminTabs) {
      window.AdminTabs.switchTo($firstErrorTab.data('tab'));
    }
  }

  /**
   * Initialize compliance bar width from data attribute (CSP-safe)
   */
  function initializeComplianceBar() {
    const $bar = $('.compliance-bar[data-width]');
    if ($bar.length) {
      $bar.css('width', $bar.data('width') + '%');
    }
  }

  /**
   * Initialize character counters for SEO fields
   */
  function initializeCharacterCounters() {
    const counters = [
      { fieldId: 'id_meta_title', counterId: 'meta_title_counter', maxLength: 60 },
      { fieldId: 'id_meta_description', counterId: 'meta_description_counter', maxLength: 160 },
    ];

    counters.forEach(function (counter) {
      const $field = $(counter.fieldId);
      const $counter = $('#' + counter.counterId);

      if ($field.length && $counter.length) {
        function updateCounter() {
          const length = $field.val().length;
          const text = interpolate(
            gettext('%(count)s/%(max)s characters'),
            {
              count: length,
              max: counter.maxLength,
            },
            true
          );

          $counter.text(text);

          // Change color if over limit
          if (length > counter.maxLength) {
            $counter.css('color', 'var(--error-fg)');
          } else if (length > counter.maxLength * 0.9) {
            $counter.css('color', 'var(--warning-fg)');
          } else {
            $counter.css('color', 'var(--body-quiet-color)');
          }
        }

        $field.on('input', updateCounter);
        updateCounter();
      }
    });
  }

  /**
   * Initialize maintenance mode warning
   */
  function initializeMaintenanceWarning() {
    const $checkbox = $('#id_maintenance_mode');

    if ($checkbox.length) {
      $checkbox.on('change', async function () {
        if ($(this).is(':checked')) {
          const message = gettext(
            'Warning: Enabling maintenance mode will make your site inaccessible to customers. Are you sure?'
          );
          if (!(await AdminModal.confirm(message))) {
            $(this).prop('checked', false);
            return false;
          }
        }
      });
    }
  }

  /**
   * Initialize 2FA enforcement settings
   * Handles enforcement card selection and grace period visibility
   */
  function initialize2FAEnforcement() {
    const $enforcementCards = $('.enforcement-card');
    const $gracePeriodRow = $('#grace-period-row');
    const $trustedDeviceCheckbox = $('#id_allow_trusted_devices');
    const $trustedDeviceDurationRow = $('#trusted-device-duration-row');

    if ($enforcementCards.length === 0) {
      return;
    }

    // Handle enforcement card clicks
    $enforcementCards.on('click', function () {
      const $card = $(this);
      const value = $card.data('value');

      // Update selected state
      $enforcementCards.removeClass('selected');
      $card.addClass('selected');

      // Update the radio input
      $card.find('input[type="radio"]').prop('checked', true);

      // Show/hide grace period based on selection
      if (value === 'required') {
        $gracePeriodRow.slideDown(200);
      } else {
        $gracePeriodRow.slideUp(200);
      }
    });

    // Handle trusted devices checkbox
    if ($trustedDeviceCheckbox.length && $trustedDeviceDurationRow.length) {
      function toggleTrustedDeviceDuration() {
        if ($trustedDeviceCheckbox.is(':checked')) {
          $trustedDeviceDurationRow.slideDown(200);
        } else {
          $trustedDeviceDurationRow.slideUp(200);
        }
      }

      $trustedDeviceCheckbox.on('change', toggleTrustedDeviceDuration);

      // Set initial state
      if (!$trustedDeviceCheckbox.is(':checked')) {
        $trustedDeviceDurationRow.hide();
      }
    }

    // Initialize selected state on page load
    const $selectedRadio = $enforcementCards.find('input[type="radio"]:checked');
    if ($selectedRadio.length) {
      $selectedRadio.closest('.enforcement-card').addClass('selected');
    }
  }

  /**
   * Initialize multi-currency toggle
   * Hides all multi-currency options when the feature is disabled
   */
  function initializeMultiCurrencyToggle() {
    const $checkbox = $('#id_enable_multi_currency');
    const $options = $('#multi-currency-options');
    const $optionsCards = $('#multi-currency-options-cards');
    const $warning = $('#multi-currency-warning');

    if (!$checkbox.length || !$options.length) {
      return;
    }

    function toggleOptions() {
      if ($checkbox.is(':checked')) {
        $warning.slideDown(200);
        $options.slideDown(200);
        $optionsCards.slideDown(200);
      } else {
        $warning.slideUp(200);
        $options.slideUp(200);
        $optionsCards.slideUp(200);
      }
    }

    $checkbox.on('change', toggleOptions);

    // Set initial state (no animation)
    if (!$checkbox.is(':checked')) {
      $options.hide();
      $optionsCards.hide();
      $warning.hide();
    } else {
      $warning.show();
    }

    // Help link — opens help drawer and loads multi-currency topic
    $('#multi-currency-help-link').on('click', function (e) {
      e.preventDefault();
      const helpBtn = document.querySelector('[data-action="toggle-help"]');
      if (helpBtn) {
        helpBtn.click();
      }
      setTimeout(function () {
        if (typeof HelpSystem !== 'undefined') {
          HelpSystem.loadTopic('multi-currency-setup');
        }
      }, 300);
    });
  }

  // Expose functions globally for external use
  window.siteSettingsSwitchTab = function (tabId) {
    return window.AdminTabs ? window.AdminTabs.switchTo(tabId) : false;
  };
  window.navigateToField = navigateToField;

  // Event delegation for data-action buttons
  document.addEventListener('click', function (e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) {
      return;
    }
    const action = btn.dataset.action;

    if (action === 'open-external') {
      const url = btn.dataset.url;
      if (url) {
        window.open(url, '_blank');
      }
    }
  });
})(django.jQuery);
