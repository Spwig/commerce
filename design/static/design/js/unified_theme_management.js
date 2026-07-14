/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Unified Theme Management JavaScript
 * External JS file for theme management interface
 * Version: 2026.02.14 - CSP-compliant with IIFE pattern
 */

// Read translation strings from JSON island (CSP-compliant), fall back to any existing value
(function () {
  const msgEl = document.getElementById('theme-messages');
  if (msgEl) {
    try {
      window.ThemeMessages = JSON.parse(msgEl.textContent);
    } catch (e) {}
  }
  window.ThemeMessages = window.ThemeMessages || {};
})();

(function () {
  'use strict';

  const csrftoken = AdminUtils.getCsrfToken();

  /**
   * Get base admin URL with language prefix
   * @returns {string} Admin base URL (e.g., '/en/admin' or '/admin')
   */
  function getAdminBaseUrl() {
    const path = window.location.pathname;
    const match = path.match(/^(\/[a-z]{2})?\/admin/);
    return match ? match[0] : '/admin';
  }

  const adminBaseUrl = getAdminBaseUrl();

  /**
   * Show loading overlay
   */
  function showLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
      overlay.style.display = 'flex';
    }
  }

  /**
   * Hide loading overlay
   */
  function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
      overlay.style.display = 'none';
    }
  }

  /**
   * Activate a theme
   * @param {string} slug - Theme slug
   * @param {string} version - Theme version
   */
  async function activateTheme(slug, version) {
    const msg =
      window.ThemeMessages.activateConfirm ||
      'Activate this theme? All other themes will be deactivated.';
    if (!(await AdminModal.confirm(msg))) {
      return;
    }

    showLoading();

    fetch(adminBaseUrl + '/design/theme/activate/' + slug + '/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'version=' + version,
    })
      .then(response => response.json())
      .then(data => {
        hideLoading();
        if (data.success) {
          location.reload();
        } else {
          const errMsg = window.ThemeMessages.activationFailed || 'Activation failed';
          AdminModal.alert({ message: errMsg + ': ' + data.error, type: 'error' });
        }
      })
      .catch(error => {
        hideLoading();
        const errMsg = window.ThemeMessages.error || 'Error';
        AdminModal.alert({ message: errMsg + ': ' + error, type: 'error' });
      });
  }

  /**
   * Install a theme
   * @param {string} slug - Theme slug
   */
  async function installTheme(slug) {
    const msg = window.ThemeMessages.installConfirm || 'Install this theme?';
    if (!(await AdminModal.confirm(msg))) {
      return;
    }

    showLoading();

    console.log('Installing theme:', slug);
    console.log('CSRF Token:', csrftoken);

    fetch(adminBaseUrl + '/design/theme/install/' + slug + '/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
      },
      credentials: 'same-origin',
    })
      .then(response => {
        console.log('Response status:', response.status);
        console.log('Response OK:', response.ok);

        // Check if response is actually JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          return response.text().then(text => {
            console.error('Non-JSON response:', text);
            throw new Error('Server returned non-JSON response: ' + text.substring(0, 100));
          });
        }

        return response.json();
      })
      .then(data => {
        console.log('Response data:', data);
        hideLoading();
        if (data.success) {
          location.reload();
        } else {
          const errMsg = window.ThemeMessages.installationFailed || 'Installation failed';
          AdminModal.alert({ message: errMsg + ': ' + data.error, type: 'error' });
        }
      })
      .catch(error => {
        hideLoading();
        const errMsg = window.ThemeMessages.error || 'Error';
        console.error('Install error:', error);
        AdminModal.alert({ message: errMsg + ': ' + error, type: 'error' });
      });
  }

  /**
   * Update a theme to latest version
   * @param {string} slug - Theme slug
   */
  async function updateTheme(slug) {
    const msg = window.ThemeMessages.updateConfirm || 'Update this theme to the latest version?';
    if (!(await AdminModal.confirm(msg))) {
      return;
    }

    showLoading();

    fetch(adminBaseUrl + '/design/theme/install/' + slug + '/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
    })
      .then(response => response.json())
      .then(data => {
        hideLoading();
        if (data.success) {
          location.reload();
        } else {
          const errMsg = window.ThemeMessages.updateFailed || 'Update failed';
          AdminModal.alert({ message: errMsg + ': ' + data.error, type: 'error' });
        }
      })
      .catch(error => {
        hideLoading();
        const errMsg = window.ThemeMessages.error || 'Error';
        AdminModal.alert({ message: errMsg + ': ' + error, type: 'error' });
      });
  }

  /**
   * Uninstall a theme
   * @param {string} slug - Theme slug
   */
  async function uninstallTheme(slug) {
    const msg =
      window.ThemeMessages.uninstallConfirm || 'Uninstall this theme? This cannot be undone.';
    if (
      !(await AdminModal.confirm({
        message: msg,
        danger: true,
        confirmText: 'Uninstall',
      }))
    ) {
      return;
    }

    showLoading();

    fetch(adminBaseUrl + '/design/theme/uninstall/' + slug + '/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
    })
      .then(response => response.json())
      .then(data => {
        hideLoading();
        if (data.success) {
          location.reload();
        } else {
          const errMsg = window.ThemeMessages.uninstallFailed || 'Uninstall failed';
          AdminModal.alert({ message: errMsg + ': ' + data.error, type: 'error' });
        }
      })
      .catch(error => {
        hideLoading();
        const errMsg = window.ThemeMessages.error || 'Error';
        AdminModal.alert({ message: errMsg + ': ' + error, type: 'error' });
      });
  }

  /**
   * Check for theme updates from upgrade server
   */
  function checkForUpdates() {
    showLoading();

    fetch(adminBaseUrl + '/design/theme/check-updates/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
      },
    })
      .then(response => response.json())
      .then(data => {
        hideLoading();
        if (data.success) {
          location.reload();
        } else {
          const errMsg = window.ThemeMessages.updateCheckFailed || 'Update check failed';
          AdminModal.alert({ message: errMsg + ': ' + data.error, type: 'error' });
        }
      })
      .catch(error => {
        hideLoading();
        const errMsg = window.ThemeMessages.error || 'Error';
        AdminModal.alert({ message: errMsg + ': ' + error, type: 'error' });
      });
  }

  /**
   * Toggle theme dropdown menu
   * @param {string} slug - Theme slug
   */
  function toggleDropdown(slug) {
    const dropdown = document.getElementById('dropdown-' + slug);
    const allDropdowns = document.querySelectorAll('.dropdown-menu');

    // Close all other dropdowns
    allDropdowns.forEach(d => {
      if (d !== dropdown) {
        d.classList.remove('show');
      }
    });

    // Toggle this dropdown
    if (dropdown) {
      dropdown.classList.toggle('show');
    }
  }

  /**
   * Purchase a paid theme via the marketplace purchase endpoint
   * @param {string} slug - Theme slug
   */
  function purchaseTheme(slug) {
    fetch(adminBaseUrl + '/marketplace/' + slug + '/purchase/', {
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.purchase_url) {
          window.open(data.purchase_url, '_blank');
        } else {
          const errMsg = window.ThemeMessages.purchaseFailed || 'Could not generate purchase URL';
          AdminModal.alert({ message: errMsg, type: 'error' });
        }
      })
      .catch(function (error) {
        const errMsg = window.ThemeMessages.error || 'Error';
        AdminModal.alert({ message: errMsg + ': ' + error, type: 'error' });
      });
  }

  /**
   * Show version history modal (placeholder)
   * @param {string} slug - Theme slug
   */
  function showVersions(slug) {
    const msg =
      (window.ThemeMessages.versionHistoryFor || 'Version history for') +
      ' ' +
      slug +
      ' - ' +
      (window.ThemeMessages.toBeImplemented || 'To be implemented');
    AdminModal.alert(msg);
  }

  // ================================================================
  // Theme Details Modal
  // ================================================================

  /**
   * Escape HTML to prevent XSS
   * @param {string} str - String to escape
   * @returns {string} Escaped string
   */
  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  /**
   * Open theme details modal and fetch data
   * @param {string} slug - Theme slug
   */
  function showThemeDetails(slug) {
    const overlay = document.getElementById('theme-detail-modal');
    const body = document.getElementById('modal-body');
    const footer = document.getElementById('modal-footer');
    const titleEl = document.getElementById('modal-theme-name');
    if (!overlay || !body) return;

    // Show modal with loading state
    overlay.classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
    titleEl.textContent = window.ThemeMessages.themeDetails || 'Theme Details';
    body.innerHTML =
      '<div style="text-align:center;padding:2rem;color:var(--body-quiet-color);"><i class="fas fa-spinner fa-spin" style="font-size:2rem;"></i></div>';
    footer.innerHTML = '';

    fetch(adminBaseUrl + '/design/theme/detail/' + slug + '/', {
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (!data.success) {
          body.innerHTML =
            '<p style="color:var(--error-fg);padding:1rem;">' +
            escapeHtml(data.error || 'Unknown error') +
            '</p>';
          return;
        }

        titleEl.textContent = data.name || slug;
        body.innerHTML = buildModalBody(data);
        footer.innerHTML = buildModalFooter(data);
        // Attach click-to-preview on screenshot thumbnails
        initScreenshotThumbs(body);
      })
      .catch(function () {
        body.innerHTML =
          '<p style="color:var(--error-fg);padding:1rem;">' +
          escapeHtml(window.ThemeMessages.detailsLoadFailed || 'Failed to load theme details') +
          '</p>';
      });
  }

  /**
   * Build a title lookup map from manifest.screenshots by matching filenames
   * to preview_images URLs.
   */
  function buildScreenshotTitleMap(data) {
    const titleMap = {};
    const manifestScreenshots = (data.manifest && data.manifest.screenshots) || [];
    if (!manifestScreenshots.length || !data.preview_images) return titleMap;

    for (let i = 0; i < manifestScreenshots.length; i++) {
      const entry = manifestScreenshots[i];
      if (!entry) continue;
      // entry can be {file, title} or a plain string
      const file = typeof entry === 'string' ? entry : entry.file || '';
      const title = typeof entry === 'object' ? entry.title || '' : '';
      if (!file) continue;
      // Extract just the filename for matching
      const filename = file.split('/').pop();
      titleMap[filename] = title;
    }
    return titleMap;
  }

  /**
   * Build modal body HTML from theme data
   * @param {Object} data - Theme detail data
   * @returns {string} HTML string
   */
  function buildModalBody(data) {
    let html = '';
    const titleMap = buildScreenshotTitleMap(data);

    // Separate preview_images into desktop and mobile
    const desktopImages = [];
    const mobileImages = [];
    if (data.preview_images && data.preview_images.length > 0) {
      for (let i = 0; i < data.preview_images.length; i++) {
        const img = data.preview_images[i];
        const imgUrl = typeof img === 'string' ? img : img.url || img.file || '';
        if (!imgUrl) continue;
        const filename = imgUrl.split('/').pop();
        const title = titleMap[filename] || (typeof img === 'object' ? img.title || '' : '');
        const isMobile =
          filename.indexOf('mobile') !== -1 ||
          (title && title.toLowerCase().indexOf('mobile') !== -1);
        const entry = { url: imgUrl, title: title, filename: filename };
        if (isMobile) {
          mobileImages.push(entry);
        } else {
          desktopImages.push(entry);
        }
      }
    }

    // Large preview area — shows the first desktop screenshot or thumbnail
    const firstPreviewUrl =
      (desktopImages.length > 0 ? desktopImages[0].url : null) || data.thumbnail_url || '';
    const firstPreviewTitle =
      (desktopImages.length > 0 ? desktopImages[0].title : '') || data.name || '';

    html += '<div class="admin-modal-section">';
    if (firstPreviewUrl) {
      html +=
        '<div id="modal-preview-container" style="text-align:center;margin-bottom:1rem;background:var(--darkened-bg);border-radius:8px;padding:0.5rem;min-height:200px;display:flex;align-items:center;justify-content:center;">';
      html +=
        '<img id="modal-preview-img" src="' +
        escapeHtml(firstPreviewUrl) +
        '" alt="' +
        escapeHtml(firstPreviewTitle) +
        '" style="max-width:100%;max-height:500px;border-radius:6px;object-fit:contain;">';
      html += '</div>';
    }

    // Desktop screenshots thumbnails
    if (desktopImages.length > 0) {
      html += '<h4 style="margin:0 0 0.75rem;font-size:0.9375rem;color:var(--body-fg);">';
      html += '<i class="fas fa-desktop" style="color:var(--primary);margin-right:0.5rem;"></i>';
      html += escapeHtml(window.ThemeMessages.screenshots || 'Screenshots');
      html += ' (' + desktopImages.length + ')</h4>';
      html += '<div style="display:flex;gap:0.5rem;overflow-x:auto;padding-bottom:0.5rem;">';
      for (let d = 0; d < desktopImages.length; d++) {
        const de = desktopImages[d];
        const isActive = (d === 0 && !data.thumbnail_url) || firstPreviewUrl === de.url;
        html +=
          '<img src="' +
          escapeHtml(de.url) +
          '" alt="' +
          escapeHtml(de.title || 'Screenshot ' + (d + 1)) +
          '"';
        html +=
          ' data-preview-url="' +
          escapeHtml(de.url) +
          '" data-preview-title="' +
          escapeHtml(de.title || '') +
          '"';
        html += ' class="modal-screenshot-thumb' + (isActive ? ' active' : '') + '"';
        html +=
          ' style="height:80px;min-width:120px;object-fit:cover;border-radius:6px;border:2px solid ' +
          (isActive ? 'var(--primary)' : 'var(--border-color)') +
          ';cursor:pointer;transition:border-color 0.2s;"';
        html += ' title="' + escapeHtml(de.title || '') + '">';
      }
      html += '</div>';
    }

    // Mobile screenshots thumbnails
    if (mobileImages.length > 0) {
      html += '<h4 style="margin:0.75rem 0 0.75rem;font-size:0.9375rem;color:var(--body-fg);">';
      html += '<i class="fas fa-mobile-alt" style="color:var(--primary);margin-right:0.5rem;"></i>';
      html += window.ThemeMessages.mobileScreenshots || 'Mobile Screenshots';
      html += ' (' + mobileImages.length + ')</h4>';
      html += '<div style="display:flex;gap:0.5rem;overflow-x:auto;padding-bottom:0.5rem;">';
      for (let m = 0; m < mobileImages.length; m++) {
        const me = mobileImages[m];
        html +=
          '<img src="' +
          escapeHtml(me.url) +
          '" alt="' +
          escapeHtml(me.title || 'Mobile ' + (m + 1)) +
          '"';
        html +=
          ' data-preview-url="' +
          escapeHtml(me.url) +
          '" data-preview-title="' +
          escapeHtml(me.title || '') +
          '"';
        html += ' class="modal-screenshot-thumb"';
        html +=
          ' style="height:80px;min-width:50px;object-fit:cover;border-radius:6px;border:2px solid var(--border-color);cursor:pointer;transition:border-color 0.2s;"';
        html += ' title="' + escapeHtml(me.title || '') + '">';
      }
      html += '</div>';
    }

    html += '</div>';

    // Info section
    html += '<div class="admin-modal-section">';
    html +=
      '<p style="color:var(--body-fg);line-height:1.6;margin:0 0 1rem;">' +
      escapeHtml(
        data.description || window.ThemeMessages.noDescription || 'No description available'
      ) +
      '</p>';

    // Meta info grid
    html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;">';

    // Version
    html +=
      '<div style="display:flex;align-items:center;gap:0.5rem;font-size:0.875rem;color:var(--body-quiet-color);">';
    html += '<i class="fas fa-code-branch" style="color:var(--primary);"></i>';
    html += '<span>' + escapeHtml(window.ThemeMessages.version || 'Version') + ': ';
    if (data.current_version) {
      html += 'v' + escapeHtml(data.current_version);
    }
    if (data.latest_version && data.latest_version !== data.current_version) {
      html += (data.current_version ? ' → ' : '') + 'v' + escapeHtml(data.latest_version);
    }
    html += '</span></div>';

    // Author
    html +=
      '<div style="display:flex;align-items:center;gap:0.5rem;font-size:0.875rem;color:var(--body-quiet-color);">';
    html += '<i class="fas fa-user" style="color:var(--primary);"></i>';
    html +=
      '<span>' +
      escapeHtml(window.ThemeMessages.author || 'Author') +
      ': ' +
      escapeHtml(data.author_name || 'Unknown') +
      '</span></div>';

    // Status
    html += '<div style="display:flex;align-items:center;gap:0.5rem;font-size:0.875rem;">';
    if (data.is_installed) {
      html += '<i class="fas fa-check-circle" style="color:#4CAF50;"></i>';
      html +=
        '<span style="color:#4CAF50;">' +
        escapeHtml(window.ThemeMessages.installed || 'Installed') +
        '</span>';
      if (data.is_active) {
        html +=
          ' <span style="background:#4CAF50;color:white;padding:0.125rem 0.5rem;border-radius:4px;font-size:0.75rem;margin-left:0.25rem;">Active</span>';
      }
    } else {
      html += '<i class="fas fa-circle" style="color:var(--body-quiet-color);"></i>';
      html +=
        '<span style="color:var(--body-quiet-color);">' +
        escapeHtml(window.ThemeMessages.notInstalled || 'Not Installed') +
        '</span>';
    }
    html += '</div>';

    // Pricing
    if (!data.is_installed && data.pricing_model === 'paid') {
      html +=
        '<div style="display:flex;align-items:center;gap:0.5rem;font-size:0.875rem;color:var(--body-fg);">';
      html += '<i class="fas fa-tag" style="color:var(--primary);"></i>';
      html += '<span>&euro;' + escapeHtml(data.price_eur || '0.00') + '</span></div>';
    }

    html += '</div>'; // end meta grid
    html += '</div>'; // end info section

    // Bundled components section
    if (data.bundled_components && data.bundled_components.length > 0) {
      html += '<div class="admin-modal-section">';
      html += '<h4 style="margin:0 0 0.75rem;font-size:0.9375rem;color:var(--body-fg);">';
      html +=
        '<i class="fas fa-puzzle-piece" style="color:var(--primary);margin-right:0.5rem;"></i>';
      html += escapeHtml(window.ThemeMessages.bundledComponents || 'Bundled Components');
      html += ' (' + data.bundled_components.length + ')</h4>';
      html += '<div style="display:flex;flex-direction:column;gap:0.5rem;">';
      for (let j = 0; j < data.bundled_components.length; j++) {
        const comp = data.bundled_components[j];
        let iconClass = 'fa-cube';
        if (comp.component_type === 'header') iconClass = 'fa-bars';
        else if (comp.component_type === 'footer') iconClass = 'fa-shoe-prints';
        else if (comp.component_type === 'section') iconClass = 'fa-layer-group';
        else if (comp.component_type === 'utility') iconClass = 'fa-tools';

        html +=
          '<div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0.75rem;background:var(--darkened-bg);border-radius:6px;font-size:0.875rem;">';
        html +=
          '<i class="fas ' +
          iconClass +
          '" style="color:var(--primary);min-width:1rem;text-align:center;"></i>';
        html +=
          '<span style="flex:1;color:var(--body-fg);font-weight:500;">' +
          escapeHtml(comp.display_name || comp.name || comp.slug) +
          '</span>';
        if (comp.version) {
          html +=
            '<span style="color:var(--body-quiet-color);font-size:0.75rem;font-family:monospace;">v' +
            escapeHtml(comp.version) +
            '</span>';
        }
        html += '</div>';
      }
      html += '</div>';
      html += '</div>';
    }

    return html;
  }

  /**
   * Build modal footer with action buttons
   * @param {Object} data - Theme detail data
   * @returns {string} HTML string
   */
  function buildModalFooter(data) {
    let html = '';

    if (data.is_installed) {
      if (!data.is_active) {
        html +=
          '<button class="theme-btn primary" data-action="activate-theme" data-theme-slug="' +
          escapeHtml(data.slug) +
          '" data-theme-version="' +
          escapeHtml(data.current_version || '') +
          '">';
        html += '<i class="fas fa-power-off"></i> Activate</button>';
      }
      if (data.has_update) {
        html +=
          '<button class="theme-btn warning" data-action="update-theme" data-theme-slug="' +
          escapeHtml(data.slug) +
          '">';
        html += '<i class="fas fa-download"></i> Update</button>';
      }
    } else {
      if (data.pricing_model === 'paid') {
        html +=
          '<span class="theme-price-badge">&euro;' +
          escapeHtml(data.price_eur || '0.00') +
          '</span>';
        html +=
          '<button class="theme-btn primary" data-action="purchase-theme" data-theme-slug="' +
          escapeHtml(data.slug) +
          '">';
        html += '<i class="fas fa-shopping-cart"></i> Purchase</button>';
      } else {
        html +=
          '<button class="theme-btn primary" data-action="install-theme" data-theme-slug="' +
          escapeHtml(data.slug) +
          '">';
        html += '<i class="fas fa-download"></i> Install</button>';
      }
    }

    return html;
  }

  /**
   * Attach click handlers to screenshot thumbnails in the modal.
   * Clicking a thumb swaps the large preview image.
   */
  function initScreenshotThumbs(container) {
    const thumbs = container.querySelectorAll('.modal-screenshot-thumb');
    if (!thumbs.length) return;
    thumbs.forEach(function (thumb) {
      thumb.addEventListener('click', function () {
        const previewImg = document.getElementById('modal-preview-img');
        if (!previewImg) return;
        const url = this.getAttribute('data-preview-url');
        const title = this.getAttribute('data-preview-title');
        if (url) {
          previewImg.src = url;
          previewImg.alt = title || '';
        }
        // Update active border on all thumbs
        thumbs.forEach(function (t) {
          t.style.borderColor = 'var(--border-color)';
          t.classList.remove('active');
        });
        this.style.borderColor = 'var(--primary)';
        this.classList.add('active');
      });
    });
  }

  /**
   * Close theme details modal
   */
  function closeThemeDetailModal() {
    const overlay = document.getElementById('theme-detail-modal');
    if (overlay) {
      overlay.classList.remove('active');
      document.body.classList.remove('admin-modal-body-locked');
    }
  }

  /**
   * Central event delegation handler for all theme actions
   * @param {Event} e - Click event
   */
  function handleThemeActions(e) {
    const actionElement = e.target.closest('[data-action]');
    if (!actionElement) return;

    e.preventDefault();

    const action = actionElement.dataset.action;
    const slug = actionElement.dataset.themeSlug;
    const version = actionElement.dataset.themeVersion;

    switch (action) {
      case 'activate-theme':
        if (slug && version) activateTheme(slug, version);
        break;
      case 'install-theme':
        if (slug) installTheme(slug);
        break;
      case 'purchase-theme':
        if (slug) purchaseTheme(slug);
        break;
      case 'update-theme':
        if (slug) updateTheme(slug);
        break;
      case 'uninstall-theme':
        if (slug) uninstallTheme(slug);
        break;
      case 'toggle-dropdown':
        if (slug) toggleDropdown(slug);
        break;
      case 'show-versions':
        if (slug) showVersions(slug);
        break;
      case 'show-details':
        if (slug) showThemeDetails(slug);
        break;
      case 'check-updates':
        checkForUpdates();
        break;
      default:
        console.warn('Unknown theme action:', action);
    }
  }

  /**
   * Handle outside clicks to close dropdowns
   * @param {Event} event - Click event
   */
  function handleOutsideClick(event) {
    if (!event.target.closest('.theme-more-dropdown')) {
      document.querySelectorAll('.dropdown-menu').forEach(d => {
        d.classList.remove('show');
      });
    }
  }

  /**
   * Initialize theme management module
   */
  function init() {
    // Attach event delegation handler for theme actions
    document.addEventListener('click', handleThemeActions);

    // Attach outside click handler for dropdowns
    document.addEventListener('click', handleOutsideClick);

    // Modal close button
    const closeBtn = document.getElementById('modal-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', closeThemeDetailModal);
    }

    // Close modal on overlay click (outside modal)
    const modalOverlay = document.getElementById('theme-detail-modal');
    if (modalOverlay) {
      modalOverlay.addEventListener('click', function (e) {
        if (e.target === modalOverlay) {
          closeThemeDetailModal();
        }
      });
    }

    // Close modal on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        closeThemeDetailModal();
      }
    });
  }

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Export minimal API for backwards compatibility
  window.ThemeManagement = {
    activateTheme: activateTheme,
    installTheme: installTheme,
    purchaseTheme: purchaseTheme,
    updateTheme: updateTheme,
    uninstallTheme: uninstallTheme,
    checkForUpdates: checkForUpdates,
    toggleDropdown: toggleDropdown,
    showVersions: showVersions,
    showThemeDetails: showThemeDetails,
    closeThemeDetailModal: closeThemeDetailModal,
  };
})();
