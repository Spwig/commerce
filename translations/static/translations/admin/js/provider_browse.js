/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Translation Provider Browse Page JavaScript
 * Handles provider installation, updates, and UI interactions
 */

(function () {
  'use strict';

  // Load i18n strings from data island
  function loadI18n() {
    const el = document.getElementById('translation-browse-i18n');
    if (!el) return {};
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return {};
    }
  }

  let i18n = {};

  // Notification system
  const NotificationManager = {
    container: null,

    init() {
      this.container = document.getElementById('provider-notification-container');
    },

    show(message, type = 'success', duration = 5000) {
      if (!this.container) return;

      const notification = document.createElement('div');
      notification.className = `provider-notification ${type}`;

      const iconEl = document.createElement('i');
      iconEl.className = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';

      const contentDiv = document.createElement('div');
      contentDiv.className = 'notification-content';

      const strong = document.createElement('strong');
      strong.textContent =
        type === 'success' ? i18n.success || 'Success' : i18n.errorLabel || 'Error';

      const p = document.createElement('p');
      p.textContent = message;

      contentDiv.appendChild(strong);
      contentDiv.appendChild(p);
      notification.appendChild(iconEl);
      notification.appendChild(contentDiv);

      this.container.appendChild(notification);

      if (duration > 0) {
        setTimeout(() => {
          notification.classList.add('d-none');
          setTimeout(() => notification.remove(), 300);
        }, duration);
      }

      return notification;
    },

    success(message, duration = 5000) {
      return this.show(message, 'success', duration);
    },

    error(message, duration = 7000) {
      return this.show(message, 'error', duration);
    },
  };

  // Loading overlay manager
  const LoadingOverlay = {
    overlay: null,

    init() {
      this.overlay = document.getElementById('provider-install-loading');
    },

    show(message) {
      if (!this.overlay) return;

      const messageEl = this.overlay.querySelector('.loading-message');
      if (messageEl) {
        messageEl.textContent = message || i18n.installing || 'Installing provider...';
      }

      this.overlay.style.display = 'flex';
    },

    hide() {
      if (!this.overlay) return;
      this.overlay.style.display = 'none';
    },
  };

  // Provider installation handler
  class ProviderInstaller {
    async install(providerSlug, providerName) {
      try {
        LoadingOverlay.show(
          (i18n.installingProvider || 'Installing %s...').replace('%s', providerName)
        );

        const response = await fetch(
          AdminUtils.buildAdminUrl(`/admin/translations/providers/install/${providerSlug}/`),
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': AdminUtils.getCsrfToken(),
            },
            credentials: 'same-origin',
          }
        );

        const contentType = response.headers.get('content-type') || '';
        if (!contentType.includes('application/json')) {
          LoadingOverlay.show('Installation is being processed. Refreshing...');
          setTimeout(() => window.location.reload(), 3000);
          return true;
        }

        const data = await response.json();

        LoadingOverlay.hide();

        if (data.success) {
          NotificationManager.success(
            data.message || i18n.installSuccess || 'Provider installed successfully!'
          );

          this.updateCardToInstalled(providerSlug);

          setTimeout(() => {
            if (data.redirect_url) {
              window.location.href = data.redirect_url;
            }
          }, 1500);

          return true;
        } else {
          NotificationManager.error(
            data.error || i18n.installFailed || 'Installation failed. Please try again.'
          );
          return false;
        }
      } catch (error) {
        console.error('Installation error:', error);
        LoadingOverlay.show('Installation is being processed. Refreshing...');
        setTimeout(() => window.location.reload(), 3000);
        return true;
      }
    }

    updateCardToInstalled(providerSlug) {
      const card = document.querySelector(`[data-provider-slug="${providerSlug}"]`);
      if (!card) return;

      card.classList.add('configured');

      const statusBadge = card.querySelector('.provider-title .status-badge');
      if (statusBadge) {
        statusBadge.className = 'status-badge status-installed';
        statusBadge.textContent = '';
        const icon = document.createElement('i');
        icon.className = 'fas fa-check-circle';
        statusBadge.appendChild(icon);
        statusBadge.appendChild(document.createTextNode(' ' + (i18n.installed || 'Installed')));
      }

      const installBtn = card.querySelector('.btn-install');
      if (installBtn) {
        const configureBtn = document.createElement('a');
        configureBtn.href = AdminUtils.buildAdminUrl(
          `/admin/translations/provider-wizard/${providerSlug}/`
        );
        configureBtn.className = 'button btn-primary';
        const cogIcon = document.createElement('i');
        cogIcon.className = 'fas fa-cog';
        configureBtn.appendChild(cogIcon);
        configureBtn.appendChild(document.createTextNode(' ' + (i18n.configure || 'Configure')));
        installBtn.parentNode.replaceChild(configureBtn, installBtn);
      }
    }
  }

  // Information card collapse functionality
  const InfoCardManager = {
    STORAGE_KEY: 'translation_provider_info_card_collapsed',

    init() {
      const card = document.getElementById('providerInfoCard');
      if (!card) return;

      const toggleBtn = card.querySelector('.collapse-toggle');
      const cardBody = document.getElementById('cardBody');

      if (!toggleBtn || !cardBody) return;

      const isCollapsed = localStorage.getItem(this.STORAGE_KEY) === 'true';
      if (isCollapsed) {
        cardBody.classList.add('collapsed');
        toggleBtn.setAttribute('aria-expanded', 'false');
        const icon = toggleBtn.querySelector('i');
        if (icon) {
          icon.classList.remove('fa-chevron-down');
          icon.classList.add('fa-chevron-right');
        }
      }

      toggleBtn.addEventListener('click', () => {
        const isNowCollapsed = cardBody.classList.toggle('collapsed');
        toggleBtn.setAttribute('aria-expanded', !isNowCollapsed);

        const icon = toggleBtn.querySelector('i');
        if (icon) {
          if (isNowCollapsed) {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-right');
          } else {
            icon.classList.remove('fa-chevron-right');
            icon.classList.add('fa-chevron-down');
          }
        }

        localStorage.setItem(this.STORAGE_KEY, isNowCollapsed);
      });
    },
  };

  // Provider update handler
  class ProviderUpdater {
    async update(providerSlug, providerVersion) {
      try {
        LoadingOverlay.show(`Updating ${providerSlug} to v${providerVersion}...`);

        const response = await fetch(
          AdminUtils.buildAdminUrl(`/admin/translations/providers/update/${providerSlug}/`),
          {
            method: 'POST',
            headers: {
              'X-CSRFToken': AdminUtils.getCsrfToken(),
              'Content-Type': 'application/json',
            },
            credentials: 'same-origin',
          }
        );

        const contentType = response.headers.get('content-type') || '';
        if (!contentType.includes('application/json')) {
          LoadingOverlay.show('Update is being processed. Refreshing...');
          setTimeout(() => window.location.reload(), 3000);
          return true;
        }

        const data = await response.json();

        LoadingOverlay.hide();

        if (data.success) {
          NotificationManager.success(
            data.message || i18n.updateSuccess || 'Provider updated successfully!'
          );
          setTimeout(() => window.location.reload(), 1000);
          return true;
        } else {
          NotificationManager.error(data.error || i18n.updateFailed || 'Update failed.');
          return false;
        }
      } catch (error) {
        console.error('Update error:', error);
        LoadingOverlay.show('Update is being processed. Refreshing...');
        setTimeout(() => window.location.reload(), 3000);
        return true;
      }
    }
  }

  // Make install and update functions globally available for modal
  window.installProvider = function (slug, name) {
    const installer = new ProviderInstaller();
    return installer.install(slug, name);
  };

  window.updateProvider = async function (slug, version, name) {
    const confirmed = await ProviderConfirm.show({
      title: i18n.updateTitle || 'Update Provider',
      message: (i18n.confirmUpdate || 'Update {name} to version {version}?')
        .replace('{name}', name || slug)
        .replace('{version}', version),
      confirmText: i18n.updateBtn || 'Update',
      cancelText: i18n.cancelBtn || 'Cancel',
    });
    if (!confirmed) return false;
    const updater = new ProviderUpdater();
    return updater.update(slug, version);
  };

  // Initialize on DOM ready
  function init() {
    i18n = loadI18n();

    NotificationManager.init();
    LoadingOverlay.init();
    InfoCardManager.init();

    const installer = new ProviderInstaller();
    const updater = new ProviderUpdater();

    // Install buttons
    document.querySelectorAll('.btn-install').forEach(button => {
      button.addEventListener('click', async function (e) {
        e.preventDefault();

        const providerSlug = this.dataset.providerSlug;
        const providerName = this.dataset.providerName;

        if (!providerSlug) {
          NotificationManager.error(
            i18n.invalidProvider || 'Invalid provider. Please refresh the page and try again.'
          );
          return;
        }

        this.disabled = true;
        const originalHTML = this.innerHTML;
        const spinnerIcon = document.createElement('i');
        spinnerIcon.className = 'fas fa-spinner fa-spin';
        this.textContent = '';
        this.appendChild(spinnerIcon);
        this.appendChild(document.createTextNode(' ' + (i18n.installingBtn || 'Installing...')));

        const success = await installer.install(providerSlug, providerName);

        if (!success) {
          this.disabled = false;
          this.innerHTML = originalHTML;
        }
      });
    });

    // Update buttons
    document.querySelectorAll('.btn-update').forEach(button => {
      button.addEventListener('click', async function (e) {
        e.preventDefault();

        const slug = this.dataset.slug;
        const version = this.dataset.version;
        const name = this.dataset.name || slug;

        if (!slug || !version) return;

        const confirmed = await ProviderConfirm.show({
          title: i18n.updateTitle || 'Update Provider',
          message: (i18n.confirmUpdate || 'Update {name} to version {version}?')
            .replace('{name}', name)
            .replace('{version}', version),
          confirmText: i18n.updateBtn || 'Update',
          cancelText: i18n.cancelBtn || 'Cancel',
        });
        if (!confirmed) return;

        this.disabled = true;
        const originalHTML = this.innerHTML;
        const spinnerIcon = document.createElement('i');
        spinnerIcon.className = 'fas fa-spinner fa-spin';
        this.textContent = '';
        this.appendChild(spinnerIcon);
        this.appendChild(document.createTextNode(' ' + (i18n.updatingBtn || 'Updating...')));

        const success = await updater.update(slug, version);

        if (!success) {
          this.disabled = false;
          this.innerHTML = originalHTML;
        }
      });
    });

    // View Details buttons
    document.querySelectorAll('.provider-details-link').forEach(button => {
      button.addEventListener('click', function (e) {
        e.preventDefault();

        const providerDataScript = document.getElementById('provider-data');
        if (!providerDataScript) {
          console.error('Provider data not found');
          return;
        }

        try {
          const providersData = JSON.parse(providerDataScript.textContent);
          const card = this.closest('.provider-card');
          const providerSlug = card ? card.dataset.providerSlug : null;

          if (!providerSlug) {
            console.error('Provider slug not found');
            return;
          }

          const providerData = providersData.find(p => p.slug === providerSlug);

          if (!providerData) {
            console.error('Provider data not found for slug:', providerSlug);
            return;
          }

          providerData.provider_type = 'translation_provider';

          if (typeof ProviderModal !== 'undefined') {
            ProviderModal.open(providerData);
          } else {
            console.error('ProviderModal not loaded');
          }
        } catch (error) {
          console.error('Error parsing provider data:', error);
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
