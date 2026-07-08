/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    var T = {};
    var currentStep = 1;
    var totalSteps = 4;

    document.addEventListener('DOMContentLoaded', function () {
        var el = document.getElementById('webhook-wizard-translations');
        if (el) {
            try { T = JSON.parse(el.textContent); } catch (err) {}
        }

        initEventSelection();
        initNavigation();
    });

    /**
     * Initialize event selection functionality
     */
    function initEventSelection() {
        var selectAllCheckbox = document.getElementById('select-all-events');
        var categoryCheckboxes = document.querySelectorAll('.select-category');
        var eventCheckboxes = document.querySelectorAll('.event-checkbox');
        var allEventsInput = document.getElementById('all-events-selected');

        if (!selectAllCheckbox) return;

        // Select all events
        selectAllCheckbox.addEventListener('change', function () {
            var isChecked = this.checked;
            allEventsInput.value = isChecked ? 'true' : 'false';

            // Disable/enable individual checkboxes
            categoryCheckboxes.forEach(function (cb) {
                cb.checked = false;
                cb.disabled = isChecked;
            });
            eventCheckboxes.forEach(function (cb) {
                cb.checked = false;
                cb.disabled = isChecked;
            });

            updateSelectedCount();
        });

        // Category selection
        categoryCheckboxes.forEach(function (categoryCheckbox) {
            categoryCheckbox.addEventListener('change', function () {
                var category = this.dataset.category;
                var isChecked = this.checked;

                document.querySelectorAll('.event-checkbox[data-category="' + category + '"]').forEach(function (cb) {
                    cb.checked = isChecked;
                });

                updateSelectedCount();
            });
        });

        // Individual event selection
        eventCheckboxes.forEach(function (eventCheckbox) {
            eventCheckbox.addEventListener('change', function () {
                var category = this.dataset.category;
                updateCategoryCheckbox(category);
                updateSelectedCount();
            });
        });
    }

    /**
     * Update category checkbox based on individual selections
     */
    function updateCategoryCheckbox(category) {
        var categoryCheckbox = document.querySelector('.select-category[data-category="' + category + '"]');
        var categoryEvents = document.querySelectorAll('.event-checkbox[data-category="' + category + '"]');
        var allChecked = Array.from(categoryEvents).every(function (cb) { return cb.checked; });
        var someChecked = Array.from(categoryEvents).some(function (cb) { return cb.checked; });

        if (categoryCheckbox) {
            categoryCheckbox.checked = allChecked;
            categoryCheckbox.indeterminate = someChecked && !allChecked;
        }
    }

    /**
     * Update selected events count
     */
    function updateSelectedCount() {
        var selectAllCheckbox = document.getElementById('select-all-events');
        var countEl = document.getElementById('selected-events-count');
        if (!countEl) return;

        if (selectAllCheckbox && selectAllCheckbox.checked) {
            countEl.textContent = T.all || 'All';
        } else {
            var count = document.querySelectorAll('.event-checkbox:checked').length;
            countEl.textContent = count;
        }
    }

    /**
     * Initialize navigation
     */
    function initNavigation() {
        var prevBtn = document.getElementById('prev-btn');
        var nextBtn = document.getElementById('next-btn');

        if (prevBtn) {
            prevBtn.addEventListener('click', function () {
                goToStep(currentStep - 1);
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', function () {
                if (validateStep(currentStep)) {
                    goToStep(currentStep + 1);
                }
            });
        }
    }

    /**
     * Navigate to step
     */
    function goToStep(step) {
        if (step < 1 || step > totalSteps) return;

        // Hide current step
        document.getElementById('step-' + currentStep).classList.add('hidden');
        document.querySelector('.step[data-step="' + currentStep + '"]').classList.remove('active');

        // Mark previous steps as completed
        for (var i = 1; i < step; i++) {
            document.querySelector('.step[data-step="' + i + '"]').classList.add('completed');
        }

        currentStep = step;

        // Show new step
        document.getElementById('step-' + currentStep).classList.remove('hidden');
        document.querySelector('.step[data-step="' + currentStep + '"]').classList.add('active');

        // Update buttons
        updateNavigationButtons();

        // If final step, populate review
        if (currentStep === 4) {
            populateReview();
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    /**
     * Update navigation buttons
     */
    function updateNavigationButtons() {
        var prevBtn = document.getElementById('prev-btn');
        var nextBtn = document.getElementById('next-btn');
        var submitBtn = document.getElementById('submit-btn');
        var cancelBtn = document.getElementById('cancel-btn');

        if (prevBtn) prevBtn.style.display = currentStep === 1 ? 'none' : 'inline-flex';
        if (cancelBtn) cancelBtn.style.display = currentStep === 1 ? 'inline-flex' : 'none';
        if (nextBtn) nextBtn.style.display = currentStep === totalSteps ? 'none' : 'inline-flex';
        if (submitBtn) submitBtn.style.display = currentStep === totalSteps ? 'inline-flex' : 'none';
    }

    /**
     * Validate current step
     */
    function validateStep(step) {
        var errors = [];

        if (step === 1) {
            var name = document.getElementById('endpoint-name').value.trim();
            var url = document.getElementById('endpoint-url').value.trim();

            if (!name) {
                errors.push(T.nameRequired || 'Endpoint name is required');
            }
            if (!url) {
                errors.push(T.urlRequired || 'Webhook URL is required');
            } else if (!url.startsWith('http://') && !url.startsWith('https://')) {
                errors.push(T.urlMustStartWith || 'URL must start with http:// or https://');
            }
        }

        if (step === 2) {
            var selectAll = document.getElementById('select-all-events').checked;
            var selectedEvents = document.querySelectorAll('.event-checkbox:checked').length;

            if (!selectAll && selectedEvents === 0) {
                errors.push(T.selectOneEvent || 'Please select at least one event');
            }
        }

        if (errors.length > 0) {
            AdminModal.alert({message: errors.join('\n'), type: 'warning'});
            return false;
        }

        return true;
    }

    /**
     * Populate review step
     */
    function populateReview() {
        // Endpoint details
        document.getElementById('review-name').textContent =
            document.getElementById('endpoint-name').value || '-';
        document.getElementById('review-url').textContent =
            document.getElementById('endpoint-url').value || '-';
        document.getElementById('review-description').textContent =
            document.getElementById('endpoint-description').value || (T.none || 'None');

        // Events
        var selectAll = document.getElementById('select-all-events').checked;
        var eventsContainer = document.getElementById('review-events');

        if (selectAll) {
            eventsContainer.innerHTML = '<span class="review-badge all-events"><i class="fas fa-asterisk"></i> ' + (T.allEvents || 'All Events') + '</span>';
        } else {
            var selectedEvents = Array.from(document.querySelectorAll('.event-checkbox:checked'))
                .map(function (cb) { return cb.value; });

            if (selectedEvents.length === 0) {
                eventsContainer.innerHTML = '<span class="review-badge no-events">' + (T.noneSelected || 'None selected') + '</span>';
            } else {
                eventsContainer.innerHTML = selectedEvents
                    .map(function (e) { return '<span class="review-badge event-badge">' + e + '</span>'; })
                    .join('');
            }
        }

        // Configuration
        document.getElementById('review-retries').textContent =
            document.getElementById('max-retries').value;
        document.getElementById('review-timeout').textContent =
            document.getElementById('timeout-seconds').value + 's';

        var isActive = document.getElementById('is-active').checked;
        document.getElementById('review-status').innerHTML = isActive
            ? '<span class="review-badge active">' + (T.active || 'Active') + '</span>'
            : '<span class="review-badge inactive">' + (T.inactive || 'Inactive') + '</span>';
    }

}());
