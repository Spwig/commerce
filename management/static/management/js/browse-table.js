/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  function exportTable() {
    const table = document.getElementById('dataTable');
    if (!table) return;
    let csv = '';
    const headers = Array.from(table.querySelectorAll('thead th')).map(function (th) {
      return th.textContent;
    });
    csv += headers.join(',') + '\n';
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(function (row) {
      const cells = Array.from(row.querySelectorAll('td')).map(function (td) {
        let text = td.textContent.trim();
        if (text === 'NULL') text = '';
        if (text.indexOf(',') !== -1 || text.indexOf('"') !== -1) {
          text = '"' + text.replace(/"/g, '""') + '"';
        }
        return text;
      });
      csv += cells.join(',') + '\n';
    });
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    const configEl = document.getElementById('browse-table-config');
    const tableName = configEl ? configEl.dataset.tableName : 'table';
    const page = configEl ? configEl.dataset.page : '1';
    a.download = tableName + '_page_' + page + '.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  }

  document.addEventListener('click', function (e) {
    const el = e.target.closest('[data-action]');
    if (!el) return;
    if (el.dataset.action === 'export-table') {
      exportTable();
    }
  });

  document.addEventListener('keydown', function (e) {
    const configEl = document.getElementById('browse-table-config');
    if (!configEl) return;
    const hasPrevious = configEl.dataset.hasPrevious === 'true';
    const hasNext = configEl.dataset.hasNext === 'true';
    const previousPage = configEl.dataset.previousPage;
    const nextPage = configEl.dataset.nextPage;
    if (e.key === 'ArrowLeft' && e.ctrlKey && hasPrevious) {
      window.location.href = '?page=' + previousPage;
    }
    if (e.key === 'ArrowRight' && e.ctrlKey && hasNext) {
      window.location.href = '?page=' + nextPage;
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    const cells = document.querySelectorAll('.data-table td');
    cells.forEach(function (cell) {
      if (cell.scrollWidth > cell.clientWidth) {
        cell.title = cell.textContent;
      }
    });
  });
})();
