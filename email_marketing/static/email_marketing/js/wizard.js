/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('em-wizard-form');
    if (!form) return;

    var steps = form.querySelectorAll('.wizard-step');
    var indicators = document.querySelectorAll('.wizard-steps .step');
    var total = steps.length;
    var current = 1;

    var btnPrev = document.getElementById('em-prev');
    var btnNext = document.getElementById('em-next');
    var btnCreate = document.getElementById('em-create');

    function show(step) {
      steps.forEach(function (s) {
        s.style.display = s.getAttribute('data-step') === String(step) ? 'block' : 'none';
      });
      indicators.forEach(function (ind) {
        var n = parseInt(ind.getAttribute('data-step'), 10);
        ind.classList.toggle('active', n === step);
        ind.classList.toggle('completed', n < step);
      });
      btnPrev.style.display = step > 1 ? 'inline-flex' : 'none';
      btnNext.style.display = step < total ? 'inline-flex' : 'none';
      btnCreate.style.display = step === total ? 'inline-flex' : 'none';
      if (step === total) fillReview();
    }

    function validate(step) {
      if (step === 2) {
        var name = document.getElementById('em-name');
        if (!name.value.trim()) {
          name.focus();
          name.classList.add('em-invalid');
          return false;
        }
        name.classList.remove('em-invalid');
      }
      return true;
    }

    function fillReview() {
      var type = form.querySelector('input[name="campaign_type"]:checked');
      var audience = document.getElementById('em-audience');
      document.getElementById('em-review-type').textContent = type
        ? type.parentNode.querySelector('.em-type-name').textContent
        : '—';
      document.getElementById('em-review-name').textContent =
        document.getElementById('em-name').value.trim() || '—';
      document.getElementById('em-review-subject').textContent =
        document.getElementById('em-subject').value.trim() || '—';
      document.getElementById('em-review-audience').textContent =
        audience.options[audience.selectedIndex].text;
    }

    // Type cards: selecting one checks its radio + highlights.
    form.querySelectorAll('.em-type-card input[type="radio"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        form.querySelectorAll('.em-type-card').forEach(function (c) {
          c.classList.remove('selected');
        });
        radio.closest('.em-type-card').classList.add('selected');
      });
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

    show(1);
  });
})();
