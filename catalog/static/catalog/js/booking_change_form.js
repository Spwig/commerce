/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        initQuickActions();
        initSectionToggles();
        initRescheduleForm();
    });

    /**
     * Confirm dialogs on destructive quick action buttons.
     * Buttons with data-confirm attribute trigger a confirmation prompt.
     */
    function initQuickActions() {
        document.querySelectorAll('[data-confirm]').forEach(function (btn) {
            btn.addEventListener('click', async function (e) {
                var message = btn.getAttribute('data-confirm');
                if (message) {
                    e.preventDefault();
                    if (!await AdminModal.confirm(message)) {
                        return;
                    }
                    // Re-trigger the action after confirmation
                    if (btn.tagName === 'A') {
                        window.location.href = btn.href;
                    } else if (btn.form) {
                        // For submit buttons, create a hidden input to carry the button's name/value
                        if (btn.name) {
                            var hidden = document.createElement('input');
                            hidden.type = 'hidden';
                            hidden.name = btn.name;
                            hidden.value = btn.value || '';
                            btn.form.appendChild(hidden);
                        }
                        btn.form.submit();
                    } else {
                        btn.removeAttribute('data-confirm');
                        btn.click();
                    }
                }
            });
        });
    }

    /**
     * Collapsible section panels via data-toggle attribute.
     */
    function initSectionToggles() {
        document.querySelectorAll('[data-toggle]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var targetId = btn.getAttribute('data-toggle');
                var target = document.getElementById(targetId);
                if (!target) return;

                var isHidden = target.classList.contains('booking-hidden');
                target.classList.toggle('booking-hidden', !isHidden);
                btn.classList.toggle('active', isHidden);
            });
        });
    }

    /**
     * Reschedule form: AJAX availability check and submit enable.
     */
    function initRescheduleForm() {
        var checkBtn = document.getElementById('check-availability-btn');
        var submitBtn = document.getElementById('reschedule-submit-btn');
        var resultDiv = document.getElementById('reschedule-result');

        if (!checkBtn || !submitBtn) return;

        var checkUrl = checkBtn.getAttribute('data-check-url');

        checkBtn.addEventListener('click', function () {
            var dateInput = document.getElementById('reschedule-date');
            var startInput = document.getElementById('reschedule-start');
            var endInput = document.getElementById('reschedule-end');

            if (!dateInput.value || !startInput.value || !endInput.value) {
                showResult(resultDiv, false, 'Please fill in all date and time fields.');
                return;
            }

            checkBtn.disabled = true;
            checkBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...';

            var params = new URLSearchParams({
                date: dateInput.value,
                time_start: startInput.value,
                time_end: endInput.value,
            });

            fetch(checkUrl + '?' + params.toString(), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                if (data.available) {
                    var msg = 'Available!';
                    if (data.price) {
                        msg += ' New price: ' + data.price;
                    }
                    showResult(resultDiv, true, msg);
                    submitBtn.disabled = false;
                } else {
                    showResult(resultDiv, false, data.message || 'Not available.');
                    submitBtn.disabled = true;
                }
            })
            .catch(function () {
                showResult(resultDiv, false, 'Error checking availability.');
                submitBtn.disabled = true;
            })
            .finally(function () {
                checkBtn.disabled = false;
                checkBtn.innerHTML = '<i class="fas fa-search"></i> Check Availability';
            });
        });

        // Re-disable submit when inputs change (force re-check)
        ['reschedule-date', 'reschedule-start', 'reschedule-end'].forEach(function (id) {
            var el = document.getElementById(id);
            if (el) {
                el.addEventListener('change', function () {
                    submitBtn.disabled = true;
                    resultDiv.classList.add('booking-hidden');
                });
            }
        });
    }

    function showResult(el, success, message) {
        el.classList.remove('booking-hidden', 'available', 'unavailable');
        el.classList.add(success ? 'available' : 'unavailable');
        el.textContent = message;
    }
})();
