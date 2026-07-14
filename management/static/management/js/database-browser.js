/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  function filterTables() {
    const searchTerm = document.getElementById('tableSearch').value.toLowerCase();
    const tableCards = document.querySelectorAll('.table-card');
    tableCards.forEach(function (card) {
      const tableName = card.getAttribute('data-table-name');
      if (tableName) {
        card.classList.toggle('mgmt-hidden', !tableName.includes(searchTerm));
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    const tableSearchEl = document.getElementById('tableSearch');
    if (tableSearchEl) {
      tableSearchEl.addEventListener('keyup', filterTables);
    }
    const tableCount = document.querySelector('.table-count');
    if (tableCount) {
      let count = 0;
      const target = parseInt(tableCount.textContent, 10);
      const increment = Math.ceil(target / 20);
      var timer = setInterval(function () {
        count += increment;
        if (count >= target) {
          count = target;
          clearInterval(timer);
        }
        tableCount.textContent = count;
      }, 50);
    }
  });
})();
