/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* A/B test setup wizard — mirrors wizard.js (step show / validate / review),
   plus test-type-dependent variant sections and dynamic subject rows. */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('ab-form');
    if (!form) return;

    var steps = form.querySelectorAll('.wizard-step');
    var indicators = document.querySelectorAll('.wizard-steps .step');
    var total = steps.length;
    var current = 1;

    var btnPrev = document.getElementById('ab-prev');
    var btnNext = document.getElementById('ab-next');
    var btnCreate = document.getElementById('ab-create');
    var subjectSection = document.getElementById('ab-subject-variants');
    var contentSection = document.getElementById('ab-content-variants');
    var subjectRows = document.getElementById('ab-subject-rows');
    var metricSelect = document.getElementById('ab-metric');
    var LABELS = ['A', 'B', 'C', 'D'];

    function testType() {
      var checked = form.querySelector('input[name="test_type"]:checked');
      return checked ? checked.value : 'subject';
    }

    function show(step) {
      steps.forEach(function (s) {
        s.hidden = s.getAttribute('data-step') !== String(step);
      });
      indicators.forEach(function (ind) {
        var n = parseInt(ind.getAttribute('data-step'), 10);
        ind.classList.toggle('active', n === step);
        ind.classList.toggle('completed', n < step);
      });
      btnPrev.hidden = step <= 1;
      btnNext.hidden = step >= total;
      btnCreate.hidden = step !== total;
      if (step === total) fillReview();
    }

    function validate(step) {
      if (step === 2 && testType() === 'subject') {
        var filled = Array.prototype.filter.call(
          subjectRows.querySelectorAll('input[name="subject"]'),
          function (i) {
            return i.value.trim();
          }
        );
        if (filled.length < 2) {
          subjectRows.querySelector('input[name="subject"]').classList.add('em-invalid');
          return false;
        }
      }
      return true;
    }

    function syncType() {
      var t = testType();
      subjectSection.hidden = t !== 'subject';
      contentSection.hidden = t !== 'content';
      // Sensible default metric per test type (the merchant can still change it).
      if (metricSelect) metricSelect.value = t === 'content' ? 'clicks' : 'opens';
    }

    function subjectSummary() {
      var vals = Array.prototype.map
        .call(subjectRows.querySelectorAll('input[name="subject"]'), function (i) {
          return i.value.trim();
        })
        .filter(Boolean);
      return vals.length + ' subject line(s)';
    }

    function fillReview() {
      var typeCard = form.querySelector('input[name="test_type"]:checked');
      document.getElementById('ab-review-type').textContent = typeCard
        ? typeCard.closest('.em-type-card').querySelector('.em-type-name').textContent
        : '—';
      document.getElementById('ab-review-variants').textContent =
        testType() === 'subject'
          ? subjectSummary()
          : document.getElementById('ab-num-variants').value + ' designs';
      var sample = document.getElementById('ab-sample');
      document.getElementById('ab-review-sample').textContent =
        sample.options[sample.selectedIndex].text.split(' — ')[0];
      document.getElementById('ab-review-metric').textContent =
        metricSelect.options[metricSelect.selectedIndex].text;
    }

    // Type cards select + toggle the variant section.
    form.querySelectorAll('.em-type-card input[type="radio"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        form.querySelectorAll('.em-type-card').forEach(function (c) {
          c.classList.remove('selected');
        });
        radio.closest('.em-type-card').classList.add('selected');
        syncType();
      });
    });

    // Add another subject line (up to 4).
    document.getElementById('ab-add-subject').addEventListener('click', function () {
      var rows = subjectRows.querySelectorAll('.ab-subject-row');
      if (rows.length >= 4) return;
      var row = document.createElement('div');
      row.className = 'form-group ab-subject-row';
      var label = document.createElement('label');
      label.textContent = 'Subject ' + LABELS[rows.length];
      var input = document.createElement('input');
      input.type = 'text';
      input.name = 'subject';
      input.className = 'form-control';
      row.appendChild(label);
      row.appendChild(input);
      subjectRows.appendChild(row);
    });

    btnNext.addEventListener('click', function () {
      if (validate(current) && current < total) {
        current++;
        show(current);
      }
    });
    btnPrev.addEventListener('click', function () {
      if (current > 1) {
        current--;
        show(current);
      }
    });

    // Keep the review card live: re-fill it whenever a setting on the final step
    // (sample, metric, number of designs) changes, so it never shows stale values.
    form.addEventListener('change', function () {
      if (current === total) fillReview();
    });

    syncType();
    show(1);
  });
})();
