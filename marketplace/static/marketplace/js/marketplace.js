/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Marketplace JavaScript
 * Handles AJAX browse, filtering, install, modal, reviews.
 */

(function () {
  'use strict';

  const _configEl = document.getElementById('marketplace-config-data');
  const CONFIG = _configEl ? JSON.parse(_configEl.textContent) : window.MARKETPLACE_CONFIG || {};
  const lang = document.documentElement.lang || 'en';
  const STR = CONFIG.strings || {};

  // State
  const currentFilters = {
    type: '',
    pricing: '',
    sort: 'popular',
    q: '',
    country: '',
    page: 1,
    page_size: 24,
  };
  let totalPages = 0;
  let searchDebounce = null;

  // ====================================================================
  // Initialize
  // ====================================================================

  function init() {
    // Only init browse page elements if they exist
    if (document.getElementById('marketplace-grid')) {
      initBrowse();
    }

    // Detail page
    initDetailPage();

    // Stars rendering
    renderAllStars();
  }

  // ====================================================================
  // Browse Page
  // ====================================================================

  function initBrowse() {
    // Type tabs
    document.querySelectorAll('.marketplace-tab[data-type]').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.marketplace-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentFilters.type = tab.dataset.type;
        currentFilters.page = 1;
        fetchComponents();
      });
    });

    // Pricing filter
    const pricingEl = document.getElementById('filter-pricing');
    if (pricingEl) {
      pricingEl.addEventListener('change', () => {
        currentFilters.pricing = pricingEl.value;
        currentFilters.page = 1;
        fetchComponents();
      });
    }

    // Sort filter
    const sortEl = document.getElementById('filter-sort');
    if (sortEl) {
      sortEl.addEventListener('change', () => {
        currentFilters.sort = sortEl.value;
        currentFilters.page = 1;
        fetchComponents();
      });
    }

    // Country filter (searchable)
    initCountryFilter();

    // Search
    const searchEl = document.getElementById('marketplace-search');
    if (searchEl) {
      searchEl.addEventListener('input', () => {
        clearTimeout(searchDebounce);
        searchDebounce = setTimeout(() => {
          currentFilters.q = searchEl.value.trim();
          currentFilters.page = 1;
          fetchComponents();
        }, 350);
      });
    }

    // Pagination
    const prevBtn = document.getElementById('btn-prev');
    const nextBtn = document.getElementById('btn-next');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (currentFilters.page > 1) {
          currentFilters.page--;
          fetchComponents();
        }
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        if (currentFilters.page < totalPages) {
          currentFilters.page++;
          fetchComponents();
        }
      });
    }

    // Modal close
    const modalOverlay = document.getElementById('preview-modal');
    const modalClose = document.getElementById('modal-close');
    if (modalOverlay) {
      modalOverlay.addEventListener('click', e => {
        if (e.target === modalOverlay) closeModal();
      });
    }
    if (modalClose) {
      modalClose.addEventListener('click', closeModal);
    }

    // Escape key
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeModal();
    });

    // Event delegation for card action buttons (install/purchase)
    const grid = document.getElementById('marketplace-grid');
    if (grid) {
      grid.addEventListener('click', function (e) {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        e.stopPropagation();
        const action = btn.dataset.action;
        if (action === 'install') {
          installComponent(btn.dataset.slug, btn.dataset.version);
        } else if (action === 'purchase') {
          purchaseComponent(btn.dataset.slug);
        }
      });
    }

    // Initial fetch
    fetchComponents();
  }

  function fetchComponents() {
    const grid = document.getElementById('marketplace-grid');
    const loadingEl = document.getElementById('marketplace-loading');
    const emptyEl = document.getElementById('marketplace-empty');
    const paginationEl = document.getElementById('marketplace-pagination');

    if (!grid) return;

    // Show loading
    grid.innerHTML = '';
    if (loadingEl) {
      loadingEl.classList.remove('marketplace-hidden');
      grid.appendChild(loadingEl);
    }
    if (emptyEl) emptyEl.classList.add('marketplace-hidden');
    if (paginationEl) paginationEl.classList.add('marketplace-hidden');

    // Build query params
    const params = new URLSearchParams();
    Object.entries(currentFilters).forEach(([k, v]) => {
      if (v) params.set(k, v);
    });

    fetch(`${CONFIG.browseUrl}?${params}`, {
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(r => r.json())
      .then(data => {
        grid.innerHTML = '';

        const results = data.results || [];
        totalPages = data.pages || 0;

        if (results.length === 0) {
          if (emptyEl) emptyEl.classList.remove('marketplace-hidden');
          return;
        }

        results.forEach(comp => {
          grid.appendChild(createCard(comp));
        });

        // Apply logo contrast detection to card thumbnails
        if (window.logoContrast) {
          window.logoContrast.init();
        }

        // Pagination
        if (totalPages > 1 && paginationEl) {
          paginationEl.classList.remove('marketplace-hidden');
          const pageInfo = document.getElementById('page-info');
          const prevBtn = document.getElementById('btn-prev');
          const nextBtn = document.getElementById('btn-next');

          if (pageInfo) pageInfo.textContent = `${currentFilters.page} / ${totalPages}`;
          if (prevBtn) prevBtn.disabled = currentFilters.page <= 1;
          if (nextBtn) nextBtn.disabled = currentFilters.page >= totalPages;
        }
      })
      .catch(err => {
        console.error('Marketplace fetch error:', err);
        grid.innerHTML =
          '<div class="marketplace-loading"><i class="fas fa-exclamation-triangle"></i><p>' +
          escapeHtml(STR.failedToLoad || 'Failed to load components') +
          '</p></div>';
      });
  }

  function createCard(comp) {
    const card = document.createElement('div');
    card.className = 'marketplace-card';
    card.dataset.slug = comp.slug;

    // Translate name/description if ManifestI18n is available
    const compName =
      typeof ManifestI18n !== 'undefined'
        ? ManifestI18n.translate(comp.translations, 'meta.name', comp.name)
        : comp.name;
    const compDesc =
      typeof ManifestI18n !== 'undefined'
        ? ManifestI18n.translate(comp.translations, 'meta.description', comp.description || '')
        : comp.description || '';

    // Rating display
    const rating = parseFloat(comp.average_rating) || 0;
    const ratingCount = comp.rating_count || 0;
    let ratingHtml = '';
    if (ratingCount > 0) {
      ratingHtml = `<span class="marketplace-rating-inline"><i class="fas fa-star"></i> ${rating.toFixed(1)} <small>(${ratingCount})</small></span>`;
    }

    // Type display
    const typeIcon = comp.type_icon ? `<i class="fas ${comp.type_icon}"></i> ` : '';
    const typeDisplay = comp.type_display || comp.component_type || '';

    // Author
    const verifiedBadge =
      comp.author && comp.author.is_verified
        ? ' <i class="fas fa-check-circle marketplace-verified"></i>'
        : '';
    const authorName = comp.author ? comp.author.name : '';

    // Thumbnail
    const isTheme = comp.component_type === 'theme';
    let thumbHtml;
    if (comp.thumbnail_url) {
      if (isTheme) {
        // Theme: scrolling preview on hover
        thumbHtml = `<div class="marketplace-card-scroll"><img src="${escapeHtml(comp.thumbnail_url)}" alt="${escapeHtml(compName)}" loading="lazy"></div>`;
      } else {
        // Non-theme: logo/icon style (contain, no clip)
        thumbHtml = `<img src="${escapeHtml(comp.thumbnail_url)}" alt="${escapeHtml(compName)}" loading="lazy" class="marketplace-card-logo">`;
      }
    } else {
      const icon = comp.type_icon || 'fa-cube';
      thumbHtml = `<i class="fas ${icon} marketplace-card-icon"></i>`;
    }

    // Media badge (screenshot/video counts)
    let mediaBadge = '';
    const sc = comp.screenshot_count || 0;
    const vc = comp.video_count || 0;
    if (sc || vc) {
      const parts = [];
      if (sc) parts.push(`<i class="fas fa-images"></i> ${sc}`);
      if (vc) parts.push(`<i class="fas fa-video"></i> ${vc}`);
      mediaBadge = `<span class="marketplace-card-media-badge">${parts.join(' ')}</span>`;
    }

    // Description
    const desc = compDesc ? escapeHtml(compDesc.substring(0, 120)) : '';

    // Country availability (only for provider types with has_country_scope)
    let countryHtml = '';
    if (comp.has_country_scope) {
      const countries = comp.supported_countries || [];
      if (countries.length === 0) {
        countryHtml =
          '<div class="marketplace-card-countries"><i class="fas fa-globe"></i> ' +
          escapeHtml(STR.global || 'Global') +
          '</div>';
      } else {
        const label =
          countries.length === 1 ? STR.country || 'country' : STR.countries || 'countries';
        countryHtml = `<div class="marketplace-card-countries"><i class="fas fa-map-marker-alt"></i> ${countries.length} ${escapeHtml(label)}</div>`;
      }
    }

    // Actions — use data-action attributes for CSP-safe event delegation
    let actionHtml;
    if (comp.is_installed) {
      actionHtml = `
                <span class="marketplace-badge marketplace-badge-installed"><i class="fas fa-check"></i> ${escapeHtml(STR.installed || 'Installed')}</span>
                <a href="${CONFIG.detailBaseUrl}${comp.slug}/" class="marketplace-btn marketplace-btn-sm marketplace-btn-secondary">${escapeHtml(STR.details || 'Details')}</a>
            `;
    } else if (comp.pricing_model === 'paid') {
      const price = parseFloat(comp.price_eur) || 0;
      actionHtml = `
                <span class="marketplace-badge marketplace-badge-price">&euro;${price.toFixed(2)}</span>
                <button class="marketplace-btn marketplace-btn-sm marketplace-btn-primary"
                        data-action="purchase" data-slug="${escapeHtml(comp.slug)}">
                    <i class="fas fa-shopping-cart"></i> ${escapeHtml(STR.purchase || 'Purchase')}
                </button>
            `;
    } else {
      actionHtml = `
                <span class="marketplace-badge marketplace-badge-free">${escapeHtml(STR.free || 'Free')}</span>
                <button class="marketplace-btn marketplace-btn-sm marketplace-btn-primary"
                        data-action="install" data-slug="${escapeHtml(comp.slug)}" data-version="${escapeHtml(comp.current_version)}">
                    <i class="fas fa-download"></i> ${escapeHtml(STR.install || 'Install')}
                </button>
            `;
    }

    // Add data-auto-contrast for non-theme cards with logo images
    const hasLogo = comp.thumbnail_url && !isTheme;
    const thumbAttrs = hasLogo ? ' data-auto-contrast' : '';

    card.innerHTML = `
            <div class="marketplace-card-thumb${hasLogo ? ' logo-plate' : ''}"${thumbAttrs}>${thumbHtml}${mediaBadge}</div>
            <div class="marketplace-card-body">
                <div class="marketplace-card-meta">
                    ${typeIcon}${escapeHtml(typeDisplay)}
                    ${ratingHtml}
                </div>
                <div class="marketplace-card-name">${escapeHtml(compName)}</div>
                <div class="marketplace-card-author">${escapeHtml(STR.by || 'by')} ${escapeHtml(authorName)}${verifiedBadge}</div>
                <div class="marketplace-card-desc">${desc}</div>
                ${countryHtml}
                <div class="marketplace-card-actions">${actionHtml}</div>
            </div>
        `;

    // Click card to open quick-preview modal
    card.addEventListener('click', e => {
      if (e.target.closest('[data-action]') || e.target.closest('a')) return;
      openModal(comp.slug);
    });

    return card;
  }

  // ====================================================================
  // Modal
  // ====================================================================

  function openModal(slug) {
    const overlay = document.getElementById('preview-modal');
    const content = document.getElementById('modal-content');
    if (!overlay || !content) return;

    overlay.classList.add('active');
    content.innerHTML =
      '<div class="marketplace-loading"><i class="fas fa-spinner fa-spin"></i></div>';
    document.body.classList.add('admin-modal-body-locked');

    fetch(`${CONFIG.detailBaseUrl}${slug}/?modal=true`, {
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(r => r.text())
      .then(html => {
        content.innerHTML = html;
      })
      .catch(() => {
        content.innerHTML =
          '<p class="marketplace-modal-error">' +
          escapeHtml(STR.failedToLoadDetails || 'Failed to load details') +
          '</p>';
      });
  }

  function closeModal() {
    const overlay = document.getElementById('preview-modal');
    if (overlay) {
      overlay.classList.remove('active');
      document.body.classList.remove('admin-modal-body-locked');
    }
  }

  // ====================================================================
  // Install
  // ====================================================================

  function installComponent(slug, version) {
    // Find the card or button and disable it
    const card = document.querySelector(`.marketplace-card[data-slug="${slug}"]`);
    if (card) card.classList.add('installing');

    const btnInstall = document.getElementById('btn-install');
    if (btnInstall && btnInstall.dataset.slug === slug) {
      btnInstall.disabled = true;
      btnInstall.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Installing...';
    }

    fetch(CONFIG.installUrl, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CONFIG.csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify({ slug, version }),
    })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          showToast(data.message || 'Component installed successfully!', 'success');
          // Refresh the browse grid or update the card
          if (card) {
            const actionsEl = card.querySelector('.marketplace-card-actions');
            if (actionsEl) {
              actionsEl.innerHTML = `
                            <span class="marketplace-badge marketplace-badge-installed"><i class="fas fa-check"></i> ${escapeHtml(STR.installed || 'Installed')}</span>
                            <a href="${CONFIG.detailBaseUrl}${slug}/" class="marketplace-btn marketplace-btn-sm marketplace-btn-secondary">${escapeHtml(STR.details || 'Details')}</a>
                        `;
            }
            card.classList.remove('installing');
          }
          // Detail page: refresh
          if (btnInstall) {
            setTimeout(() => window.location.reload(), 500);
          }
        } else {
          showToast(data.error || 'Installation failed', 'error');
          if (card) card.classList.remove('installing');
          if (btnInstall) {
            btnInstall.disabled = false;
            btnInstall.innerHTML =
              '<i class="fas fa-download"></i> ' + escapeHtml(STR.install || 'Install');
          }
        }
      })
      .catch(() => {
        showToast('Installation request failed', 'error');
        if (card) card.classList.remove('installing');
        if (btnInstall) {
          btnInstall.disabled = false;
          btnInstall.innerHTML =
            '<i class="fas fa-download"></i> ' + escapeHtml(STR.install || 'Install');
        }
      });
  }

  // ====================================================================
  // Purchase
  // ====================================================================

  function purchaseComponent(slug) {
    fetch(`${CONFIG.detailBaseUrl}${slug}/purchase/`, {
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(r => r.json())
      .then(data => {
        if (data.purchase_url) {
          window.open(data.purchase_url, '_blank');
        } else {
          showToast(data.error || 'Could not generate purchase URL', 'error');
        }
      })
      .catch(() => {
        showToast('Failed to get purchase URL', 'error');
      });
  }

  // ====================================================================
  // Detail Page
  // ====================================================================

  function initDetailPage() {
    // Tabs
    document.querySelectorAll('.marketplace-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        document
          .querySelectorAll('.marketplace-tab-btn')
          .forEach(b => b.classList.remove('active'));
        document
          .querySelectorAll('.marketplace-tab-content')
          .forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        const tabContent = document.getElementById(`tab-${tab}`);
        if (tabContent) tabContent.classList.add('active');
      });
    });

    // Carousel thumbs (images + videos)
    document.querySelectorAll('.marketplace-carousel-thumb').forEach(thumb => {
      thumb.addEventListener('click', () => {
        document
          .querySelectorAll('.marketplace-carousel-thumb')
          .forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');

        const mainImg = document.getElementById('carousel-main-img');
        const mainVideo = document.getElementById('carousel-main-video');
        const videoSource = document.getElementById('carousel-video-source');
        const type = thumb.dataset.type || 'image';

        if (type === 'video' && mainVideo) {
          // Show video, hide image
          if (mainImg) mainImg.classList.add('marketplace-hidden');
          videoSource.src = thumb.dataset.src;
          videoSource.type = thumb.dataset.mime || 'video/webm';
          mainVideo.load();
          mainVideo.classList.remove('marketplace-hidden');
          mainVideo.play().catch(() => {});
        } else {
          // Show image, hide/pause video
          if (mainVideo) {
            mainVideo.pause();
            mainVideo.classList.add('marketplace-hidden');
          }
          if (mainImg) {
            mainImg.src = thumb.dataset.src;
            mainImg.classList.remove('marketplace-hidden');
          }
        }
      });
    });

    // Rating bars (fill widths from CONFIG.reviewsSummary)
    if (CONFIG.reviewsSummary && CONFIG.ratingCount) {
      for (let star = 1; star <= 5; star++) {
        const count = CONFIG.reviewsSummary[String(star)] || 0;
        const pct = CONFIG.ratingCount > 0 ? (count / CONFIG.ratingCount) * 100 : 0;
        const fill = document.querySelector(`.marketplace-rating-bar-fill[data-star="${star}"]`);
        const countEl = document.querySelector(
          `.marketplace-rating-bar-count[data-star="${star}"]`
        );
        if (fill) fill.style.width = `${pct}%`;
        if (countEl) countEl.textContent = count;
      }
    }

    // Star selector for reviews
    initStarSelector();

    // Install button on detail page
    const btnInstall = document.getElementById('btn-install');
    if (btnInstall) {
      btnInstall.addEventListener('click', () => {
        installComponent(btnInstall.dataset.slug, btnInstall.dataset.version);
      });
    }

    // Purchase button on detail page
    const btnPurchase = document.getElementById('btn-purchase');
    if (btnPurchase) {
      btnPurchase.addEventListener('click', () => {
        purchaseComponent(btnPurchase.dataset.slug);
      });
    }

    // Submit review
    const btnReview = document.getElementById('btn-submit-review');
    if (btnReview) {
      btnReview.addEventListener('click', () => submitReview(btnReview.dataset.slug));
    }
  }

  function initStarSelector() {
    const stars = document.querySelectorAll('.marketplace-star-input i');
    let selectedRating = 0;

    stars.forEach(star => {
      star.addEventListener('mouseover', () => {
        const val = parseInt(star.dataset.value);
        stars.forEach(s => {
          const sv = parseInt(s.dataset.value);
          s.className = sv <= val ? 'fas fa-star active' : 'far fa-star';
        });
      });

      star.addEventListener('mouseout', () => {
        stars.forEach(s => {
          const sv = parseInt(s.dataset.value);
          s.className = sv <= selectedRating ? 'fas fa-star active' : 'far fa-star';
        });
      });

      star.addEventListener('click', () => {
        selectedRating = parseInt(star.dataset.value);
        stars.forEach(s => {
          const sv = parseInt(s.dataset.value);
          s.className = sv <= selectedRating ? 'fas fa-star active' : 'far fa-star';
        });
      });
    });

    // Store getter
    window._getSelectedRating = () => selectedRating;
  }

  function submitReview(slug) {
    const rating = window._getSelectedRating ? window._getSelectedRating() : 0;
    const title = (document.getElementById('review-title') || {}).value || '';
    const comment = (document.getElementById('review-comment') || {}).value || '';

    if (!rating) {
      showToast('Please select a rating', 'error');
      return;
    }

    const btn = document.getElementById('btn-submit-review');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
    }

    fetch(CONFIG.reviewUrl, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CONFIG.csrfToken,
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify({ slug, rating, title, comment }),
    })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          showToast('Review submitted!', 'success');
          setTimeout(() => window.location.reload(), 800);
        } else {
          showToast(data.error || 'Failed to submit review', 'error');
          if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Review';
          }
        }
      })
      .catch(() => {
        showToast('Request failed', 'error');
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Review';
        }
      });
  }

  // ====================================================================
  // Stars rendering
  // ====================================================================

  function renderAllStars() {
    document.querySelectorAll('.marketplace-stars[data-rating]').forEach(el => {
      const rating = parseFloat(el.dataset.rating) || 0;
      const stars = el.querySelectorAll('i');
      stars.forEach((star, i) => {
        const starVal = i + 1;
        if (rating >= starVal) {
          star.classList.add('marketplace-star-filled');
          star.classList.remove('marketplace-star-empty', 'marketplace-star-half');
        } else if (rating >= starVal - 0.5) {
          star.classList.add('marketplace-star-half');
          star.classList.remove('marketplace-star-empty', 'marketplace-star-filled');
          star.className = 'fas fa-star-half-alt marketplace-star-half';
        } else {
          star.classList.add('marketplace-star-empty');
          star.classList.remove('marketplace-star-filled', 'marketplace-star-half');
        }
      });
    });
  }

  // ====================================================================
  // Toast notifications
  // ====================================================================

  function showToast(message, type) {
    AdminModal.toast(message, type || 'info');
  }

  // ====================================================================
  // Utilities
  // ====================================================================

  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ====================================================================
  // Searchable Country Filter
  // ====================================================================

  function initCountryFilter() {
    const wrapper = document.getElementById('country-select-wrapper');
    const searchInput = document.getElementById('filter-country-search');
    const hiddenInput = document.getElementById('filter-country');
    const dropdown = document.getElementById('country-dropdown');
    const clearBtn = document.getElementById('country-clear');
    if (!wrapper || !searchInput || !hiddenInput || !dropdown) return;

    const allOptions = Array.from(dropdown.querySelectorAll('.marketplace-country-option'));
    let highlightIdx = -1;

    function showDropdown() {
      dropdown.classList.remove('marketplace-hidden');
      filterOptions(searchInput.value);
    }

    function hideDropdown() {
      dropdown.classList.add('marketplace-hidden');
      highlightIdx = -1;
      allOptions.forEach(o => o.classList.remove('highlighted'));
    }

    function filterOptions(query) {
      const q = query.toLowerCase();
      let visibleCount = 0;
      allOptions.forEach(opt => {
        const text = opt.textContent.toLowerCase();
        const match = !q || text.includes(q);
        opt.style.display = match ? '' : 'none';
        if (match) visibleCount++;
      });
      highlightIdx = -1;
      allOptions.forEach(o => o.classList.remove('highlighted'));
    }

    function getVisibleOptions() {
      return allOptions.filter(o => o.style.display !== 'none');
    }

    function selectOption(opt) {
      const value = opt.dataset.value;
      hiddenInput.value = value;
      searchInput.value = value ? opt.textContent.trim() : '';
      clearBtn.classList.toggle('marketplace-hidden', !value);
      allOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
      hideDropdown();
      currentFilters.country = value;
      currentFilters.page = 1;
      fetchComponents();
    }

    searchInput.addEventListener('focus', () => {
      searchInput.select();
      showDropdown();
    });

    searchInput.addEventListener('input', () => {
      showDropdown();
    });

    searchInput.addEventListener('keydown', e => {
      const visible = getVisibleOptions();
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        highlightIdx = Math.min(highlightIdx + 1, visible.length - 1);
        visible.forEach((o, i) => o.classList.toggle('highlighted', i === highlightIdx));
        if (visible[highlightIdx]) visible[highlightIdx].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        highlightIdx = Math.max(highlightIdx - 1, 0);
        visible.forEach((o, i) => o.classList.toggle('highlighted', i === highlightIdx));
        if (visible[highlightIdx]) visible[highlightIdx].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (highlightIdx >= 0 && visible[highlightIdx]) {
          selectOption(visible[highlightIdx]);
        }
      } else if (e.key === 'Escape') {
        hideDropdown();
        searchInput.blur();
      }
    });

    allOptions.forEach(opt => {
      opt.addEventListener('mousedown', e => {
        e.preventDefault();
        selectOption(opt);
      });
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        selectOption(allOptions[0]); // "All Countries"
        searchInput.value = '';
      });
    }

    // Close on click outside
    document.addEventListener('mousedown', e => {
      if (!wrapper.contains(e.target)) {
        hideDropdown();
        // Restore display text if dropdown closed without selection
        if (hiddenInput.value) {
          const sel = allOptions.find(o => o.dataset.value === hiddenInput.value);
          if (sel) searchInput.value = sel.textContent.trim();
        } else {
          searchInput.value = '';
        }
      }
    });
  }

  // ====================================================================
  // Public API
  // ====================================================================

  window.Marketplace = {
    installComponent,
    purchaseComponent,
    openModal,
    closeModal,
  };

  // Initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Country list toggle (detail page)
  document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('country-toggle');
    const list = document.getElementById('country-list');
    if (toggle && list) {
      toggle.addEventListener('click', function () {
        const expanded = !list.classList.contains('marketplace-hidden');
        list.classList.toggle('marketplace-hidden', expanded);
        toggle.classList.toggle('expanded', !expanded);
      });
    }
  });
})();
