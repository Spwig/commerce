/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Communication Preferences Page
 * Handles enable/disable sub-options, subscribe all, unsubscribe all,
 * and send verification email actions.
 * Replaces inline onclick handlers and inline <script> block.
 *
 * Translations are passed via data attributes on action buttons:
 *   [data-action="confirm-unsubscribe-all"] data-confirm-msg="..."
 *   [data-action="send-verification-email"] data-success-msg="..." data-error-msg="..."
 */
(function () {
  'use strict';

  const MARKETING_CHECKBOXES = [
    'email_marketing',
    'blog_enabled',
    'loyalty_enabled',
    'referrals_enabled',
    'affiliate_enabled',
  ];

  const TOGGLE_SECTIONS = [
    { main: 'blog_enabled', frequency: 'blog_frequency' },
    {
      main: 'loyalty_enabled',
      subs: [
        'loyalty_points_earned',
        'loyalty_tier_changes',
        'loyalty_rewards_available',
        'loyalty_points_expiring',
      ],
    },
    {
      main: 'referrals_enabled',
      subs: ['referrals_reward_issued', 'referrals_referral_converted'],
    },
    {
      main: 'affiliate_enabled',
      subs: [
        'affiliate_commission_earned',
        'affiliate_payout_processed',
        'affiliate_monthly_report',
      ],
    },
  ];

  function subscribeAll() {
    MARKETING_CHECKBOXES.forEach(function (name) {
      const checkbox = document.getElementById(name);
      if (checkbox && !checkbox.disabled) {
        checkbox.checked = true;
        checkbox.dispatchEvent(new Event('change'));
      }
    });
  }

  function unsubscribeAll() {
    MARKETING_CHECKBOXES.forEach(function (name) {
      const checkbox = document.getElementById(name);
      if (checkbox && !checkbox.disabled) {
        checkbox.checked = false;
        checkbox.dispatchEvent(new Event('change'));
      }
    });
  }

  function sendVerificationEmail(btn) {
    const successMsg =
      (btn && btn.dataset.successMsg) || 'Verification email sent! Please check your inbox.';
    const errorMsg =
      (btn && btn.dataset.errorMsg) || 'Error sending verification email. Please try again.';
    const csrfToken = window.getCSRFToken ? window.getCSRFToken() : '';

    fetch('/api/accounts/send-verification-email/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          AdminModal.toast(successMsg, 'success');
        } else {
          AdminModal.alert({ message: errorMsg, type: 'error' });
        }
      });
  }

  function setupToggleSections() {
    TOGGLE_SECTIONS.forEach(function (section) {
      const mainCheckbox = document.getElementById(section.main);
      if (!mainCheckbox) return;

      mainCheckbox.addEventListener('change', function () {
        if (section.frequency) {
          const freqSelect = document.querySelector('select[name="' + section.frequency + '"]');
          if (freqSelect) freqSelect.disabled = !mainCheckbox.checked;
        }
        if (section.subs) {
          section.subs.forEach(function (subName) {
            const subCheckbox = document.querySelector('input[name="' + subName + '"]');
            if (subCheckbox) subCheckbox.disabled = !mainCheckbox.checked;
          });
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    setupToggleSections();

    document.addEventListener('click', async function (e) {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;

      const action = btn.dataset.action;

      if (action === 'subscribe-all') {
        subscribeAll();
      } else if (action === 'confirm-unsubscribe-all') {
        const confirmMsg =
          btn.dataset.confirmMsg ||
          'Are you sure you want to unsubscribe from all marketing communications?';
        if (await AdminModal.confirm(confirmMsg)) {
          unsubscribeAll();
        }
      } else if (action === 'send-verification-email') {
        e.preventDefault();
        sendVerificationEmail(btn);
      }
    });
  });
})();
