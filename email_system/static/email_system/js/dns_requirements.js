/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* DNS Requirements page JS - registrar tabs, copy-to-clipboard, collapsibles */
(function () {
  'use strict';

  document.addEventListener('click', function (e) {
    // Registrar tab
    const tabBtn = e.target.closest('[data-action="show-registrar"]');
    if (tabBtn) {
      const registrar = tabBtn.dataset.registrar;
      document.querySelectorAll('.registrar-content').forEach(function (el) {
        el.classList.remove('active');
      });
      document.querySelectorAll('.registrar-tab').forEach(function (el) {
        el.classList.remove('active');
      });
      const content = document.getElementById(registrar);
      if (content) content.classList.add('active');
      tabBtn.classList.add('active');
      return;
    }

    // Validation details toggle
    const detailsBtn = e.target.closest('[data-action="toggle-details"]');
    if (detailsBtn) {
      const line = detailsBtn.closest('.validation-line');
      const details = line && line.querySelector('.validation-details');
      if (details) {
        details.classList.toggle('show');
        const icon = detailsBtn.querySelector('i');
        if (icon) {
          if (details.classList.contains('show')) {
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
          } else {
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
          }
        }
      }
      return;
    }

    // Collapsible section toggle
    const collapsible = e.target.closest('[data-action="toggle-collapsible"]');
    if (collapsible) {
      const collContent = collapsible.nextElementSibling;
      if (collContent) collContent.classList.toggle('show');
      collapsible.classList.toggle('open');
      return;
    }

    // Copy to clipboard
    const copyBtn = e.target.closest('[data-action="copy-to-clipboard"]');
    if (copyBtn) {
      const text = copyBtn.dataset.copyValue || '';
      navigator.clipboard.writeText(text).then(function () {
        const originalText = copyBtn.getAttribute('data-copy-text');
        const copiedText = copyBtn.getAttribute('data-copied-text');
        copyBtn.textContent = copiedText;
        copyBtn.classList.add('copied');
        setTimeout(function () {
          copyBtn.textContent = originalText;
          copyBtn.classList.remove('copied');
        }, 2000);
      });
    }
  });

  // Auto-select detected provider tab on page load
  document.addEventListener('DOMContentLoaded', function () {
    const configEl = document.getElementById('dns-requirements-config');
    let detectedProvider = '';
    if (configEl) {
      try {
        const config = JSON.parse(configEl.textContent);
        detectedProvider = config.detectedProvider || '';
      } catch (e) {}
    }

    const providerTabMap = {
      cloudflare: 'cloudflare',
      godaddy: 'godaddy',
      namecheap: 'namecheap',
      route53: 'route53',
      google: 'generic',
      azure: 'generic',
    };

    const tabId = providerTabMap[detectedProvider] || 'generic';

    if (detectedProvider && detectedProvider !== 'unknown') {
      const tabButton = document.getElementById('tab-' + tabId);
      if (tabButton) {
        tabButton.classList.add('active');
        const tabContent = document.getElementById(tabId);
        if (tabContent) tabContent.classList.add('active');
      }
    } else {
      const genericTab = document.getElementById('tab-generic');
      const genericContent = document.getElementById('generic');
      if (genericTab) genericTab.classList.add('active');
      if (genericContent) genericContent.classList.add('active');
    }
  });
})();
