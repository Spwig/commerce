/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  function init() {
    const availableZones = document.getElementById('available-zones');
    const selectedZones = document.getElementById('selected-zones');
    const addBtn = document.getElementById('add-zones');
    const addAllBtn = document.getElementById('add-all-zones');
    const removeBtn = document.getElementById('remove-zones');
    const removeAllBtn = document.getElementById('remove-all-zones');
    const form = document.getElementById('method-coverage-form');

    if (addBtn && availableZones && selectedZones) {
      addBtn.addEventListener('click', function () {
        moveOptions(availableZones, selectedZones, false);
      });
      addAllBtn.addEventListener('click', function () {
        moveOptions(availableZones, selectedZones, true);
      });
      removeBtn.addEventListener('click', function () {
        moveOptions(selectedZones, availableZones, false);
      });
      removeAllBtn.addEventListener('click', function () {
        moveOptions(selectedZones, availableZones, true);
      });
    }

    if (form && selectedZones) {
      form.addEventListener('submit', function () {
        Array.from(selectedZones.options).forEach(function (option) {
          option.selected = true;
        });
      });
    }
  }

  function moveOptions(fromSelect, toSelect, moveAll) {
    const options = moveAll
      ? Array.from(fromSelect.options)
      : Array.from(fromSelect.selectedOptions);
    options.forEach(function (option) {
      toSelect.appendChild(option);
    });
    sortSelect(fromSelect);
    sortSelect(toSelect);
  }

  function sortSelect(select) {
    const options = Array.from(select.options);
    options.sort(function (a, b) {
      return a.text.localeCompare(b.text);
    });
    select.innerHTML = '';
    options.forEach(function (option) {
      select.appendChild(option);
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
