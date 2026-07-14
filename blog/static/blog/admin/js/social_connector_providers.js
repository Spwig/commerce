/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let data = {};

  function init() {
    const dataEl = document.getElementById('social-connector-providers-data');
    if (dataEl) {
      try {
        data = JSON.parse(dataEl.textContent);
      } catch (e) {}
    }

    document.addEventListener('click', handleActions);
  }

  function handleActions(e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) {
      return;
    }
    const action = btn.dataset.action;

    if (action === 'install-provider') {
      installProvider(btn.dataset.slug, btn.dataset.name);
    } else if (action === 'update-provider') {
      updateProvider(btn.dataset.slug, btn.dataset.version);
    }
  }

  function getLanguageCode() {
    return document.documentElement.lang || 'en';
  }

  function getCsrfToken() {
    return AdminUtils.getCsrfToken();
  }

  async function installProvider(slug, name) {
    const t = data.translations || {};
    if (!(await AdminModal.confirm((t.install || 'Install') + ' ' + name + '?'))) {
      return;
    }

    const loading = document.getElementById('provider-install-loading');
    const message = document.getElementById('loading-message');
    if (loading) {
      loading.style.display = 'flex';
    }
    if (message) {
      message.textContent = (t.installing || 'Installing') + ' ' + name + '...';
    }

    const languageCode = getLanguageCode();
    fetch('/' + languageCode + '/admin/blog/social-connectors/providers/install/' + slug + '/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (responseData) {
        if (loading) {
          loading.style.display = 'none';
        }
        if (responseData.success) {
          AdminModal.toast(t.installed || 'Provider installed successfully!', 'success');
          if (responseData.redirect_url) {
            window.location.href = '/' + languageCode + responseData.redirect_url;
          } else {
            window.location.reload();
          }
        } else {
          AdminModal.alert({
            message: (t.installFailed || 'Installation failed') + ': ' + responseData.error,
            type: 'error',
          });
        }
      })
      .catch(function (error) {
        if (loading) {
          loading.style.display = 'none';
        }
        AdminModal.alert({
          message: (t.installFailed || 'Installation failed') + ': ' + error,
          type: 'error',
        });
      });
  }

  async function updateProvider(slug, version) {
    const t = data.translations || {};
    if (
      !(await AdminModal.confirm((t.updateToVersion || 'Update to version') + ' ' + version + '?'))
    ) {
      return;
    }

    const loading = document.getElementById('provider-install-loading');
    const message = document.getElementById('loading-message');
    if (loading) {
      loading.style.display = 'flex';
    }
    if (message) {
      message.textContent = t.updating || 'Updating provider...';
    }

    const languageCode = getLanguageCode();
    fetch('/' + languageCode + '/admin/blog/social-connectors/providers/update/' + slug + '/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (responseData) {
        if (loading) {
          loading.style.display = 'none';
        }
        if (responseData.success) {
          AdminModal.toast(t.updated || 'Provider updated successfully!', 'success');
          window.location.reload();
        } else {
          AdminModal.alert({
            message: (t.updateFailed || 'Update failed') + ': ' + responseData.error,
            type: 'error',
          });
        }
      })
      .catch(function (error) {
        if (loading) {
          loading.style.display = 'none';
        }
        AdminModal.alert({
          message: (t.updateFailed || 'Update failed') + ': ' + error,
          type: 'error',
        });
      });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
