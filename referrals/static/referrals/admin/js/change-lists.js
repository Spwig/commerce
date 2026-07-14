/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Referrals Admin Change List Initializations
 * Handles filter initialization and action buttons for all referrals change_list templates.
 *
 * Reads i18n strings from a data-i18n JSON attribute on #referrals-changelist-config.
 */

(function () {
  'use strict';

  const lang = document.documentElement.lang || 'en';

  /** Load i18n strings from page data island */
  function getI18n() {
    const el = document.getElementById('referrals-changelist-config');
    if (el) {
      try {
        return JSON.parse(el.textContent || '{}');
      } catch (e) {
        return {};
      }
    }
    return {};
  }

  /**
   * Initialize filters based on current page
   */
  function initializeReferralsFilters() {
    const path = window.location.pathname;

    if (path.includes('/referralidentity/')) {
      window.AdminListFilters.init({
        url: '/' + lang + '/admin/referrals/referrers/filter/',
        resultsContainer: 'results-container',
        resultsCount: 'results-count',
      });
    } else if (path.includes('/referralevent/')) {
      window.AdminListFilters.init({
        url: '/' + lang + '/admin/referrals/events/filter/',
        resultsContainer: 'results-container',
        resultsCount: 'results-count',
      });
    } else if (path.includes('/referralattribution/')) {
      window.AdminListFilters.init({
        url: '/' + lang + '/admin/referrals/attributions/filter/',
        resultsContainer: 'results-container',
        resultsCount: 'results-count',
      });
    } else if (path.includes('/referralreward/')) {
      window.AdminListFilters.init({
        url: '/' + lang + '/admin/referrals/rewards/filter/',
        resultsContainer: 'results-container',
        resultsCount: 'results-count',
      });
    }
  }

  /**
   * Perform an AJAX POST action and refresh results
   */
  function performAction(url) {
    const i18n = getI18n();

    fetch(url, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': window.AdminUtils ? AdminUtils.getCsrfToken() : '',
        'Content-Type': 'application/json',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success || data.status === 'ok') {
          if (window.AdminListFilters && window.AdminListFilters.apply) {
            window.AdminListFilters.apply();
          } else {
            window.location.reload();
          }
        } else {
          AdminModal.alert({
            message: data.error || i18n.action_failed || 'Action failed. Please try again.',
            type: 'error',
          });
        }
      })
      .catch(function () {
        AdminModal.alert({
          message: i18n.error_performing_action || 'Error performing action. Please try again.',
          type: 'error',
        });
      });
  }

  /**
   * Event delegation for attribution and reward action buttons
   */
  function initActionButtons() {
    const i18n = getI18n();

    document.addEventListener('click', async function (e) {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;

      const action = btn.dataset.action;
      const pk = btn.dataset.pk;
      if (!pk) return;

      if (action === 'approve-attribution') {
        performAction('/' + lang + '/admin/referrals/attributions/' + pk + '/approve/');
      } else if (action === 'reject-attribution') {
        if (
          !(await AdminModal.confirm({
            message: i18n.confirm_reject_attribution || 'Reject this referral attribution?',
            danger: true,
            confirmText: 'Reject',
          }))
        )
          return;
        performAction('/' + lang + '/admin/referrals/attributions/' + pk + '/reject/');
      } else if (action === 'issue-reward') {
        performAction('/' + lang + '/admin/referrals/rewards/' + pk + '/issue/');
      } else if (action === 'revoke-reward') {
        if (
          !(await AdminModal.confirm({
            message: i18n.confirm_revoke_reward || 'Revoke this reward?',
            danger: true,
            confirmText: 'Revoke',
          }))
        )
          return;
        performAction('/' + lang + '/admin/referrals/rewards/' + pk + '/revoke/');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initializeReferralsFilters();
    initActionButtons();
  });
})();
