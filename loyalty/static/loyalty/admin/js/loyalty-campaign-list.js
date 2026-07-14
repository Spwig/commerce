/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  let msgs = {
    confirmActivate: 'Are you sure you want to activate this campaign?',
    confirmPause: 'Are you sure you want to pause this campaign?',
    errorOccurred: 'An error occurred.',
    retryError: 'An error occurred. Please try again.',
  };

  document.addEventListener('DOMContentLoaded', function () {
    const island = document.getElementById('loyalty-campaign-i18n');
    if (island) {
      try {
        msgs = JSON.parse(island.textContent);
      } catch (e) {}
    }
  });

  async function toggleCampaignStatus(campaignId, activate) {
    const action = activate ? 'activate' : 'pause';
    const message = activate ? msgs.confirmActivate : msgs.confirmPause;

    if (!(await AdminModal.confirm(message))) {
      return;
    }

    const languageCode = document.documentElement.lang || 'en';
    const url = '/' + languageCode + '/admin/loyalty/campaigns/' + campaignId + '/' + action + '/';
    const csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');

    fetch(url, {
      method: 'POST',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrfEl ? csrfEl.value : '',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (data.success) {
          window.AdminListFilters.apply();
        } else {
          AdminModal.alert({ message: data.error || msgs.errorOccurred, type: 'error' });
        }
      })
      .catch(function (error) {
        console.error('Toggle error:', error);
        AdminModal.alert({ message: msgs.retryError, type: 'error' });
      });
  }

  window.toggleCampaignStatus = toggleCampaignStatus;
})();
