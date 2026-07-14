/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  const configEl = document.getElementById('slot-options-config');
  if (!configEl) return;
  const config = JSON.parse(configEl.textContent);

  let searchTimeout;
  const lang = document.documentElement.lang || 'en';
  const slotId = config.slotId;

  function searchProducts() {
    const search = document.getElementById('product-search').value;
    if (!search || search.length < 2) {
      document.getElementById('search-results').innerHTML = '';
      return;
    }
    const url =
      '/' +
      lang +
      '/admin/catalog/slot/' +
      slotId +
      '/options/search/?search=' +
      encodeURIComponent(search);
    fetch(url, {
      method: 'GET',
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        document.getElementById('search-results').innerHTML = data.html;
      })
      .catch(function (error) {
        console.error('Search error:', error);
      });
  }

  document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('product-search');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(searchProducts, 300);
      });
    }

    // Event delegation for data-action and data-confirm
    document.addEventListener('click', async function (e) {
      // data-action="search-products"
      if (e.target.closest('[data-action="search-products"]')) {
        searchProducts();
        return;
      }
      // data-confirm
      const confirmBtn = e.target.closest('[data-confirm]');
      if (confirmBtn) {
        const msg = confirmBtn.getAttribute('data-confirm');
        if (msg) {
          e.preventDefault();
          if (!(await AdminModal.confirm({ message: msg, danger: true, confirmText: 'Remove' }))) {
            return;
          }
          // Re-trigger the action after confirmation
          if (confirmBtn.tagName === 'A') {
            window.location.href = confirmBtn.href;
          } else if (confirmBtn.form) {
            if (confirmBtn.name) {
              const hidden = document.createElement('input');
              hidden.type = 'hidden';
              hidden.name = confirmBtn.name;
              hidden.value = confirmBtn.value || '';
              confirmBtn.form.appendChild(hidden);
            }
            confirmBtn.form.submit();
          } else {
            confirmBtn.removeAttribute('data-confirm');
            confirmBtn.click();
          }
        }
      }
    });
  });
})();
