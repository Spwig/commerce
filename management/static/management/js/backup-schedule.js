/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  function updateScheduleOptions() {
    const frequency = document.getElementById('frequency').value;
    document
      .getElementById('weekly-options')
      .classList.toggle('mgmt-hidden', frequency !== 'weekly');
    document
      .getElementById('monthly-options')
      .classList.toggle('mgmt-hidden', frequency !== 'monthly');
  }

  document.addEventListener('DOMContentLoaded', function () {
    const frequencyEl = document.getElementById('frequency');
    if (frequencyEl) {
      frequencyEl.addEventListener('change', updateScheduleOptions);
    }
  });
})();
