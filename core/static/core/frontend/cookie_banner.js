/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Cookie Consent Manager
 *
 * Configuration is read from #cookie-banner data attributes.
 * Fires window events:
 *   - spwig:consent:ready   — on page load when consent already exists
 *   - spwig:consent:updated — after user makes a choice
 *
 * Third-party scripts should listen for these events and check
 * event.detail.consent.analytics / .marketing / .functional before loading.
 *
 * Cookie name: spwig_cookie_consent
 * Cookie payload: {"necessary":true,"analytics":bool,"marketing":bool,"functional":bool}
 */
(function () {
  'use strict';

  const COOKIE_NAME = 'spwig_cookie_consent';
  const banner = document.getElementById('cookie-banner');

  if (!banner) return;

  const consentUrl = banner.dataset.cookieConsentUrl;
  const mode = banner.dataset.cookieConsentMode;
  const modal = document.getElementById('cookie-prefs-modal');

  /* ---- Utility: read a cookie ---- */
  function getCookie(name) {
    const match = document.cookie.match(
      new RegExp('(?:^|; )' + name.replace(/([.*+?^=!:${}()|[\]/\\])/g, '\\$1') + '=([^;]*)')
    );
    return match ? decodeURIComponent(match[1]) : null;
  }

  /* ---- Utility: parse stored consent ---- */
  function getStoredConsent() {
    const raw = getCookie(COOKIE_NAME);
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch (e) {
      return null;
    }
  }

  /* ---- Fire event ---- */
  function fireConsentEvent(eventName, consent) {
    window.dispatchEvent(new CustomEvent(eventName, { detail: { consent: consent } }));
  }

  /* ---- Set cookie client-side (fallback) ---- */
  function setConsentCookie(consent) {
    const secure = location.protocol === 'https:' ? '; secure' : '';
    document.cookie =
      COOKIE_NAME +
      '=' +
      encodeURIComponent(JSON.stringify(consent)) +
      '; max-age=' +
      365 * 24 * 3600 +
      '; path=/; samesite=lax' +
      secure;
  }

  /* ---- Send consent to server and store ---- */
  function saveConsent(consent) {
    /* Set cookie client-side immediately for instant UI response */
    setConsentCookie(consent);
    hideBanner();
    closeModal();
    fireConsentEvent('spwig:consent:updated', consent);

    /* Also POST to server for server-side cookie (belt & suspenders) */
    if (consentUrl) {
      fetch(consentUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(consent),
        credentials: 'same-origin',
      }).catch(function () {
        /* Network failure is fine — client cookie is already set */
      });
    }
  }

  /* ---- Banner visibility ---- */
  function hideBanner() {
    banner.classList.add('cookie-banner--hidden');
  }

  function showBanner() {
    banner.classList.remove('cookie-banner--hidden');
  }

  /* ---- Modal ---- */
  function openModal() {
    if (!modal) return;
    modal.classList.add('cookie-prefs-modal--open');
    /* Focus first interactive element */
    const firstBtn = modal.querySelector('button');
    if (firstBtn) firstBtn.focus();
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove('cookie-prefs-modal--open');
  }

  /* ---- Read checkbox state from modal ---- */
  function getModalConsent() {
    const analytics = document.getElementById('consent-analytics');
    const marketing = document.getElementById('consent-marketing');
    const functional = document.getElementById('consent-functional');
    return {
      necessary: true,
      analytics: analytics ? analytics.checked : false,
      marketing: marketing ? marketing.checked : false,
      functional: functional ? functional.checked : false,
    };
  }

  /* ---- Action handler (event delegation) ---- */
  function handleAction(action) {
    switch (action) {
      case 'accept':
        saveConsent({ necessary: true, analytics: true, marketing: true, functional: true });
        break;
      case 'reject':
        saveConsent({ necessary: true, analytics: false, marketing: false, functional: false });
        break;
      case 'manage':
        if (mode === 'granular') openModal();
        break;
      case 'save-prefs':
        saveConsent(getModalConsent());
        break;
      case 'close-modal':
        closeModal();
        break;
      case 'open-settings':
        /* Clear consent and re-show banner (for footer "Cookie Settings" link) */
        document.cookie = COOKIE_NAME + '=; max-age=0; path=/;';
        showBanner();
        break;
    }
  }

  /* Delegate clicks to both banner and modal */
  document.addEventListener('click', function (e) {
    const target = e.target.closest('[data-cookie-action]');
    if (!target) return;
    e.preventDefault();
    handleAction(target.dataset.cookieAction);
  });

  /* Close modal on Escape */
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal && modal.classList.contains('cookie-prefs-modal--open')) {
      closeModal();
    }
  });

  /* ---- Initialise ---- */
  const existing = getStoredConsent();
  if (existing && existing.necessary === true) {
    hideBanner();
    fireConsentEvent('spwig:consent:ready', existing);
  } else {
    showBanner();
  }

  /* ---- Public API for third-party scripts ---- */
  window.SpwigConsent = {
    getConsent: function () {
      return getStoredConsent();
    },
    hasConsented: function (category) {
      const c = getStoredConsent();
      return c ? !!c[category] : false;
    },
    openPreferences: function () {
      showBanner();
      if (mode === 'granular') openModal();
    },
    resetConsent: function () {
      document.cookie = COOKIE_NAME + '=; max-age=0; path=/;';
      showBanner();
    },
  };
})();
