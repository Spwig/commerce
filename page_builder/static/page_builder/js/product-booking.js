/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Booking Product Widget
 *
 * Handles date/time selection, resource picking, person counts,
 * live price calculation, and add-to-cart for booking products.
 * Supports calendar, date_picker, dropdown, and date_range display modes.
 */
(function () {
  'use strict';

  const MONTH_NAMES = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('booking-form');
    if (!form) return;

    // ========== Configuration from data attributes ==========
    const config = {
      productSlug: form.dataset.productSlug,
      productId: form.dataset.productId,
      calendarDisplay: form.dataset.calendarDisplay,
      bookingType: form.dataset.bookingType,
      durationType: form.dataset.durationType,
      duration: parseInt(form.dataset.duration) || 60,
      durationUnit: form.dataset.durationUnit,
      minDuration: parseInt(form.dataset.minDuration) || 0,
      maxDuration: parseInt(form.dataset.maxDuration) || 0,
      timezoneEnabled: form.dataset.timezoneEnabled === 'true',
      depositEnabled: form.dataset.depositEnabled === 'true',
      currencyCode: form.dataset.currencyCode || window.__shopCurrency || 'USD',
      currencySymbol: form.dataset.currencySymbol || '$',
      minStay: 1,
      maxStay: 365,
      standardOccupancy: 2,
      maxOccupancy: 0, // 0 = no limit
    };

    // ========== State ==========
    const state = {
      currentYear: new Date().getFullYear(),
      currentMonth: new Date().getMonth() + 1,
      selectedDate: null,
      selectedSlot: null,
      selectedResource: null,
      selectedEndDate: null, // for date_range
      persons: {},
      customDuration: config.duration,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      availableDates: [], // from API
      availableSlots: [], // from API
      lastCheckResult: null,
      rangeMode: 'checkin', // 'checkin' or 'checkout' (for accommodation calendar range)
    };

    // ========== API Helpers ==========
    const apiBase = `/api/catalog/products/${config.productSlug}/booking`;

    async function fetchAvailability(year, month) {
      const params = new URLSearchParams({ year, month });
      if (state.selectedResource) params.append('resource_id', state.selectedResource);
      if (state.timezone) params.append('timezone', state.timezone);
      const resp = await fetch(`${apiBase}/availability/?${params}`);
      if (!resp.ok) throw new Error('Failed to fetch availability');
      return resp.json();
    }

    async function fetchSlots(dateStr) {
      const params = new URLSearchParams({ date: dateStr });
      if (state.selectedResource) params.append('resource_id', state.selectedResource);
      if (state.timezone) params.append('timezone', state.timezone);
      const resp = await fetch(`${apiBase}/slots/?${params}`);
      if (!resp.ok) throw new Error('Failed to fetch slots');
      return resp.json();
    }

    async function checkBooking(data) {
      const csrfToken = getCSRFToken();
      const resp = await fetch(`${apiBase}/check/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'same-origin',
        body: JSON.stringify(data),
      });
      if (!resp.ok) throw new Error('Booking check failed');
      return resp.json();
    }

    async function fetchResourceAvailability(checkin, checkout) {
      const params = new URLSearchParams({ checkin, checkout });
      const resp = await fetch(`${apiBase}/resource-availability/?${params}`);
      if (!resp.ok) throw new Error('Failed to fetch resource availability');
      return resp.json();
    }

    async function fetchResourceDetail(resourceId) {
      const resp = await fetch(`${apiBase}/resources/${resourceId}/`);
      if (!resp.ok) throw new Error('Failed to fetch resource detail');
      return resp.json();
    }

    async function joinWaitlist(email) {
      const csrfToken = getCSRFToken();
      const resp = await fetch(`${apiBase}/waitlist/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          email,
          date: state.selectedDate,
          time_start: state.selectedSlot ? state.selectedSlot.start : null,
          time_end: state.selectedSlot ? state.selectedSlot.end : null,
          persons: Object.keys(state.persons).length > 0 ? state.persons : null,
        }),
      });
      return resp.json();
    }

    function getCSRFToken() {
      return window.getCSRFToken ? window.getCSRFToken() : '';
    }

    // ========== Calendar Rendering ==========
    function renderCalendar() {
      const calDays = document.getElementById('cal-days');
      const calLabel = document.getElementById('cal-month-label');
      if (!calDays || !calLabel) return;

      calLabel.textContent = `${MONTH_NAMES[state.currentMonth - 1]} ${state.currentYear}`;

      // Mark loading
      calDays.classList.add('booking-calendar__days--loading');

      fetchAvailability(state.currentYear, state.currentMonth)
        .then(data => {
          // Capture accommodation config from first API response
          if (data.config) {
            if (data.config.min_stay) config.minStay = data.config.min_stay;
            if (data.config.max_stay) config.maxStay = data.config.max_stay;
            if (data.config.standard_occupancy)
              config.standardOccupancy = data.config.standard_occupancy;
            if (data.config.max_occupancy) config.maxOccupancy = data.config.max_occupancy;
          }
          state.availableDates = (data.available_dates || [])
            .filter(d => d.available)
            .map(d => d.date);
          const availableSet = new Set(state.availableDates);

          const firstDay = new Date(state.currentYear, state.currentMonth - 1, 1);
          const lastDay = new Date(state.currentYear, state.currentMonth, 0);
          const startDow = (firstDay.getDay() + 6) % 7; // Monday = 0
          const totalDays = lastDay.getDate();
          const today = new Date();
          const todayStr = formatDate(today);

          let html = '';
          // Empty cells before first day
          for (let i = 0; i < startDow; i++) {
            html +=
              '<button type="button" class="booking-calendar__day booking-calendar__day--empty" disabled></button>';
          }
          // Day cells
          const isAccom = config.bookingType === 'accommodation';
          for (let d = 1; d <= totalDays; d++) {
            const dateStr = `${state.currentYear}-${String(state.currentMonth).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
            const isAvailable = availableSet.has(dateStr);
            const isToday = dateStr === todayStr;
            const isSelected = dateStr === state.selectedDate;

            let cls = 'booking-calendar__day';
            if (isToday) cls += ' booking-calendar__day--today';
            if (!isAvailable) cls += ' booking-calendar__day--disabled';

            // Range highlighting for accommodation
            if (isAccom && state.selectedDate) {
              if (dateStr === state.selectedDate) {
                cls += ' booking-calendar__day--range-start';
              } else if (dateStr === state.selectedEndDate) {
                cls += ' booking-calendar__day--range-end';
              } else if (
                state.selectedEndDate &&
                dateStr > state.selectedDate &&
                dateStr < state.selectedEndDate
              ) {
                cls += ' booking-calendar__day--in-range';
              }
            } else if (isSelected) {
              cls += ' booking-calendar__day--selected';
            }

            html += `<button type="button" class="${cls}" data-date="${dateStr}" ${!isAvailable ? 'disabled' : ''}>${d}</button>`;
          }

          calDays.innerHTML = html;
          calDays.classList.remove('booking-calendar__days--loading');

          // Click handlers
          calDays.querySelectorAll('.booking-calendar__day:not([disabled])').forEach(btn => {
            btn.addEventListener('click', function () {
              if (isAccom) {
                selectRangeDate(this.dataset.date);
              } else {
                selectDate(this.dataset.date);
              }
            });
          });

          // Hover preview for accommodation checkout selection
          if (isAccom) {
            initRangeHover(calDays);

            // Auto-select first available date as check-in on initial load
            if (!state.selectedDate && state.availableDates.length) {
              selectRangeDate(state.availableDates[0]);
            }
          }
        })
        .catch(() => {
          calDays.innerHTML =
            '<p style="grid-column: span 7; text-align: center; color: #999; padding: 20px;">Unable to load availability</p>';
          calDays.classList.remove('booking-calendar__days--loading');
        });
    }

    function initCalendarNav() {
      const prevBtn = document.getElementById('cal-prev');
      const nextBtn = document.getElementById('cal-next');
      if (prevBtn) {
        prevBtn.addEventListener('click', function () {
          state.currentMonth--;
          if (state.currentMonth < 1) {
            state.currentMonth = 12;
            state.currentYear--;
          }
          renderCalendar();
        });
      }
      if (nextBtn) {
        nextBtn.addEventListener('click', function () {
          state.currentMonth++;
          if (state.currentMonth > 12) {
            state.currentMonth = 1;
            state.currentYear++;
          }
          renderCalendar();
        });
      }
    }

    // ========== Date Picker Init ==========
    function initDatePicker() {
      const input = document.getElementById('booking-date-input');
      if (!input) return;

      // Set min to today
      input.min = formatDate(new Date());

      input.addEventListener('change', function () {
        if (this.value) selectDate(this.value);
      });
    }

    // ========== Dropdown Init ==========
    function initDropdown() {
      const select = document.getElementById('booking-date-select');
      if (!select) return;

      // Fetch 2 months of availability
      const now = new Date();
      const promises = [];
      for (let i = 0; i < 2; i++) {
        const m = now.getMonth() + 1 + i;
        const y = now.getFullYear() + (m > 12 ? 1 : 0);
        promises.push(fetchAvailability(y, ((m - 1) % 12) + 1));
      }

      Promise.all(promises).then(results => {
        const allDates = [];
        results.forEach(data => {
          (data.available_dates || []).forEach(d => allDates.push(d));
        });
        allDates.sort((a, b) => a.date.localeCompare(b.date));

        allDates.forEach(d => {
          const opt = document.createElement('option');
          opt.value = d.date;
          const dt = new Date(d.date + 'T00:00:00');
          opt.textContent = dt.toLocaleDateString(undefined, {
            weekday: 'short',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          });
          if (d.slots_available !== undefined) {
            opt.textContent += ` (${d.slots_available} available)`;
          }
          select.appendChild(opt);
        });
      });

      select.addEventListener('change', function () {
        if (this.value) selectDate(this.value);
      });
    }

    // ========== Date Range Init ==========
    function initDateRange() {
      const checkin = document.getElementById('booking-checkin');
      const checkout = document.getElementById('booking-checkout');
      if (!checkin || !checkout) return;

      const todayStr = formatDate(new Date());
      checkin.min = todayStr;
      checkout.min = todayStr;

      checkin.addEventListener('change', function () {
        if (this.value) {
          // Set checkout min to checkin + min_stay days
          const minNights = config.minStay || 1;
          const nextDay = new Date(this.value + 'T00:00:00');
          nextDay.setDate(nextDay.getDate() + minNights);
          checkout.min = formatDate(nextDay);
          if (checkout.value && checkout.value <= this.value) {
            checkout.value = formatDate(nextDay);
          }
          state.selectedDate = this.value;
          if (checkout.value) {
            state.selectedEndDate = checkout.value;
            onDateRangeSelected();
          }
        }
      });

      checkout.addEventListener('change', function () {
        if (this.value && state.selectedDate) {
          state.selectedEndDate = this.value;
          onDateRangeSelected();
        }
      });
    }

    function onDateRangeSelected() {
      // Pre-populate summary date with check-in/check-out range
      const summaryDate = document.getElementById('summary-date');
      if (summaryDate && state.selectedDate && state.selectedEndDate) {
        const ci = new Date(state.selectedDate + 'T00:00:00');
        const co = new Date(state.selectedEndDate + 'T00:00:00');
        const nights = Math.round((co - ci) / (1000 * 60 * 60 * 24));
        const fmt = { month: 'short', day: 'numeric' };
        summaryDate.textContent = `${ci.toLocaleDateString(undefined, fmt)} \u2013 ${co.toLocaleDateString(undefined, fmt)} (${nights} night${nights !== 1 ? 's' : ''})`;
      }

      enableStep('booking-step-resource');
      enableStep('booking-step-persons');
      enableStep('booking-step-duration');
      updateResourceAvailability();
      runPriceCheck();
    }

    // ========== Accommodation Calendar Range Selection ==========
    function daysBetween(a, b) {
      const da = new Date(a + 'T00:00:00');
      const db = new Date(b + 'T00:00:00');
      return Math.round((db - da) / (1000 * 60 * 60 * 24));
    }

    function selectRangeDate(dateStr) {
      if (state.rangeMode === 'checkin' || !state.selectedDate) {
        // First click: set check-in
        state.selectedDate = dateStr;
        state.selectedEndDate = null;
        state.rangeMode = 'checkout';
        updateRangeSummary();
        renderCalendar();
      } else {
        // Second click: set check-out
        if (dateStr <= state.selectedDate) {
          // Clicked before or on check-in — reset to new check-in
          state.selectedDate = dateStr;
          state.selectedEndDate = null;
          state.rangeMode = 'checkout';
          updateRangeSummary();
          renderCalendar();
          return;
        }
        // Enforce min/max stay
        const nights = daysBetween(state.selectedDate, dateStr);
        const minStay = config.minStay || 1;
        const maxStay = config.maxStay || 365;
        if (nights < minStay || nights > maxStay) return;

        state.selectedEndDate = dateStr;
        state.rangeMode = 'checkin';
        updateRangeSummary();
        renderCalendar();
        onDateRangeSelected();
      }
    }

    function updateRangeSummary() {
      const ciLabel = document.getElementById('range-checkin-label');
      const coLabel = document.getElementById('range-checkout-label');
      const nightsEl = document.getElementById('range-nights-label');
      if (!ciLabel) return;

      const fmt = { month: 'short', day: 'numeric' };

      if (state.selectedDate) {
        const ci = new Date(state.selectedDate + 'T00:00:00');
        ciLabel.textContent = ci.toLocaleDateString(undefined, fmt);
      } else {
        ciLabel.textContent = 'Select date';
      }

      if (state.selectedEndDate) {
        const co = new Date(state.selectedEndDate + 'T00:00:00');
        coLabel.textContent = co.toLocaleDateString(undefined, fmt);
        const nights = daysBetween(state.selectedDate, state.selectedEndDate);
        if (nightsEl) {
          nightsEl.style.display = '';
          nightsEl.querySelector('span').textContent = `${nights} night${nights !== 1 ? 's' : ''}`;
        }
      } else {
        coLabel.textContent = 'Select date';
        if (nightsEl) nightsEl.style.display = 'none';
      }
    }

    function initRangeHover(calDays) {
      calDays.addEventListener('mouseover', function (e) {
        const btn = e.target.closest(
          '.booking-calendar__day:not([disabled]):not(.booking-calendar__day--empty)'
        );
        if (!btn || state.rangeMode !== 'checkout' || !state.selectedDate) return;

        const hoverDate = btn.dataset.date;
        if (!hoverDate || hoverDate <= state.selectedDate) return;

        // Check min/max stay
        const nights = daysBetween(state.selectedDate, hoverDate);
        const minStay = config.minStay || 1;
        const maxStay = config.maxStay || 365;
        if (nights < minStay || nights > maxStay) return;

        // Clear previous hover highlights
        calDays.querySelectorAll('.booking-calendar__day--range-hover').forEach(el => {
          el.classList.remove('booking-calendar__day--range-hover');
        });

        // Highlight all days between check-in and hover
        calDays.querySelectorAll('.booking-calendar__day').forEach(dayBtn => {
          const d = dayBtn.dataset.date;
          if (
            d &&
            d > state.selectedDate &&
            d <= hoverDate &&
            !dayBtn.classList.contains('booking-calendar__day--range-start')
          ) {
            dayBtn.classList.add('booking-calendar__day--range-hover');
          }
        });
      });

      calDays.addEventListener('mouseleave', function () {
        calDays.querySelectorAll('.booking-calendar__day--range-hover').forEach(el => {
          el.classList.remove('booking-calendar__day--range-hover');
        });
      });
    }

    // ========== Date Selection ==========
    function selectDate(dateStr) {
      state.selectedDate = dateStr;
      state.selectedSlot = null;

      // Highlight in calendar
      document.querySelectorAll('.booking-calendar__day--selected').forEach(el => {
        el.classList.remove('booking-calendar__day--selected');
      });
      const dayBtn = document.querySelector(`.booking-calendar__day[data-date="${dateStr}"]`);
      if (dayBtn) dayBtn.classList.add('booking-calendar__day--selected');

      // Update summary
      const summaryDate = document.getElementById('summary-date');
      if (summaryDate) {
        const dt = new Date(dateStr + 'T00:00:00');
        summaryDate.textContent = dt.toLocaleDateString(undefined, {
          weekday: 'short',
          month: 'long',
          day: 'numeric',
          year: 'numeric',
        });
      }

      // For non-accommodation, load time slots
      if (config.bookingType !== 'accommodation') {
        loadTimeSlots(dateStr);
        enableStep('booking-step-time');
      } else {
        enableStep('booking-step-resource');
        enableStep('booking-step-persons');
        enableStep('booking-step-duration');
        runPriceCheck();
      }
    }

    // ========== Time Slots ==========
    function loadTimeSlots(dateStr) {
      const slotsContainer = document.getElementById('booking-slots');
      if (!slotsContainer) return;

      slotsContainer.innerHTML = '<p class="booking-slots__placeholder">Loading...</p>';

      fetchSlots(dateStr)
        .then(data => {
          state.availableSlots = data.slots || [];

          if (state.availableSlots.length === 0) {
            slotsContainer.innerHTML =
              '<p class="booking-slots__placeholder">No available time slots for this date</p>';
            return;
          }

          let html = '<div class="booking-slots__grid">';
          state.availableSlots.forEach(slot => {
            const isFull = slot.remaining <= 0;
            let cls = 'booking-slot';
            if (isFull) cls += ' booking-slot--full';

            html += `<button type="button" class="${cls}"
                                data-start="${slot.start}" data-end="${slot.end}"
                                ${isFull ? 'disabled' : ''}>
                        <span class="booking-slot__time">${slot.start}</span>
                        ${slot.capacity > 1 ? `<span class="booking-slot__capacity">${slot.remaining}/${slot.capacity} left</span>` : ''}
                    </button>`;
          });
          html += '</div>';
          slotsContainer.innerHTML = html;

          // Click handlers
          slotsContainer.querySelectorAll('.booking-slot:not([disabled])').forEach(btn => {
            btn.addEventListener('click', function () {
              selectSlot(this);
            });
          });
        })
        .catch(() => {
          slotsContainer.innerHTML =
            '<p class="booking-slots__placeholder">Unable to load time slots</p>';
        });
    }

    function selectSlot(btn) {
      document.querySelectorAll('.booking-slot--selected').forEach(el => {
        el.classList.remove('booking-slot--selected');
      });
      btn.classList.add('booking-slot--selected');

      state.selectedSlot = {
        start: btn.dataset.start,
        end: btn.dataset.end,
      };

      // Update summary
      const summaryTime = document.getElementById('summary-time');
      const summaryTimeRow = document.getElementById('summary-time-row');
      if (summaryTime && summaryTimeRow) {
        summaryTime.textContent = `${state.selectedSlot.start} - ${state.selectedSlot.end}`;
        summaryTimeRow.style.display = '';
      }

      // Enable next steps
      enableStep('booking-step-resource');
      enableStep('booking-step-persons');
      enableStep('booking-step-duration');

      runPriceCheck();
    }

    // ========== Resource Selection ==========
    function selectResource(btn) {
      const container = document.getElementById('booking-resources');
      if (!container) return;
      container.querySelectorAll('.booking-resource--selected').forEach(el => {
        el.classList.remove('booking-resource--selected');
      });
      btn.classList.add('booking-resource--selected');
      state.selectedResource = btn.dataset.resourceId;

      const summaryResource = document.getElementById('summary-resource');
      const summaryResourceRow = document.getElementById('summary-resource-row');
      if (summaryResource && summaryResourceRow) {
        summaryResource.textContent = btn.querySelector('.booking-resource__name').textContent;
        summaryResourceRow.style.display = '';
      }

      if (config.calendarDisplay === 'calendar') {
        renderCalendar();
      }

      runPriceCheck();
    }

    function initResources() {
      const container = document.getElementById('booking-resources');
      if (!container) return;

      container.querySelectorAll('.booking-resource').forEach(btn => {
        btn.addEventListener('click', function (e) {
          // If clicking the detail button, open modal instead
          const detailBtn = e.target.closest('[data-resource-detail]');
          if (detailBtn) {
            e.preventDefault();
            e.stopPropagation();
            openResourceModal(detailBtn.dataset.resourceDetail);
            return;
          }
          selectResource(this);
        });
      });
    }

    // ========== Resource Availability (accommodation) ==========
    function updateResourceAvailability() {
      if (config.bookingType !== 'accommodation') return;
      if (!state.selectedDate || !state.selectedEndDate) return;

      const container = document.getElementById('booking-resources');
      if (!container) return;

      fetchResourceAvailability(state.selectedDate, state.selectedEndDate)
        .then(data => {
          const availMap = {};
          (data.resources || []).forEach(r => {
            availMap[String(r.id)] = r.available;
          });

          container.querySelectorAll('.booking-resource').forEach(btn => {
            const rid = btn.dataset.resourceId;
            const isAvailable = availMap[rid] !== false;

            // Remove existing unavailable label
            const existingLabel = btn.querySelector('.booking-resource__unavailable');
            if (existingLabel) existingLabel.remove();

            if (isAvailable) {
              btn.classList.remove('booking-resource--unavailable');
              btn.disabled = false;
            } else {
              btn.classList.add('booking-resource--unavailable');
              btn.classList.remove('booking-resource--selected');
              btn.disabled = true;

              // Add unavailable label
              const label = document.createElement('span');
              label.className = 'booking-resource__unavailable';
              label.textContent = 'Unavailable for selected dates';
              const info = btn.querySelector('.booking-resource__info');
              if (info) info.appendChild(label);

              // Deselect if this was the selected resource
              if (state.selectedResource === rid) {
                state.selectedResource = null;
                const summaryResourceRow = document.getElementById('summary-resource-row');
                if (summaryResourceRow) summaryResourceRow.style.display = 'none';
              }
            }
          });
        })
        .catch(() => {
          // Silently ignore - resources stay in their current state
        });
    }

    // ========== Person Types ==========
    const personButtonUpdaters = [];

    function totalGuests() {
      return Object.values(state.persons).reduce((s, n) => s + n, 0);
    }

    function updateAllPersonButtons() {
      personButtonUpdaters.forEach(fn => fn());
    }

    function initPersonTypes() {
      const container = document.getElementById('booking-persons');
      if (!container) return;

      container.querySelectorAll('.booking-person-type').forEach(row => {
        const typeName = row.dataset.personType;
        const min = parseInt(row.dataset.min) || 0;
        const max = parseInt(row.dataset.max) || 10;
        state.persons[typeName] = min;

        const valueEl = row.querySelector('.booking-qty-value');
        const minusBtn = row.querySelector('[data-action="decrease"]');
        const plusBtn = row.querySelector('[data-action="increase"]');

        function updateButtons() {
          minusBtn.disabled = state.persons[typeName] <= min;
          const atMax = state.persons[typeName] >= max;
          const atOccupancyLimit = config.maxOccupancy > 0 && totalGuests() >= config.maxOccupancy;
          plusBtn.disabled = atMax || atOccupancyLimit;
        }

        personButtonUpdaters.push(updateButtons);
        updateButtons();

        minusBtn.addEventListener('click', function () {
          if (state.persons[typeName] > min) {
            state.persons[typeName]--;
            valueEl.textContent = state.persons[typeName];
            updateAllPersonButtons();
            updatePersonsSummary();
            runPriceCheck();
          }
        });

        plusBtn.addEventListener('click', function () {
          if (state.persons[typeName] < max) {
            if (config.maxOccupancy > 0 && totalGuests() >= config.maxOccupancy) return;
            state.persons[typeName]++;
            valueEl.textContent = state.persons[typeName];
            updateAllPersonButtons();
            updatePersonsSummary();
            runPriceCheck();
          }
        });
      });
    }

    function updatePersonsSummary() {
      const summaryPersons = document.getElementById('summary-persons');
      const summaryPersonsRow = document.getElementById('summary-persons-row');
      if (!summaryPersons || !summaryPersonsRow) return;

      const parts = [];
      for (const [type, count] of Object.entries(state.persons)) {
        if (count > 0) parts.push(`${count} ${type}`);
      }
      if (parts.length > 0) {
        summaryPersons.textContent = parts.join(', ');
        summaryPersonsRow.style.display = '';
      } else {
        summaryPersonsRow.style.display = 'none';
      }
    }

    // ========== Duration Slider ==========
    function initDurationSlider() {
      const slider = document.getElementById('booking-duration-slider');
      const label = document.getElementById('duration-value');
      if (!slider || !label) return;

      slider.addEventListener('input', function () {
        state.customDuration = parseInt(this.value);
        label.textContent = `${state.customDuration} ${config.durationUnit}(s)`;
        runPriceCheck();
      });
    }

    // ========== Timezone Selector ==========
    function initTimezone() {
      if (!config.timezoneEnabled) return;
      const select = document.getElementById('booking-tz-select');
      if (!select) return;

      // Populate with browser timezones
      try {
        const zones = Intl.supportedValuesOf('timeZone');
        zones.forEach(tz => {
          const opt = document.createElement('option');
          opt.value = tz;
          opt.textContent = tz.replace(/_/g, ' ');
          if (tz === state.timezone) opt.selected = true;
          select.appendChild(opt);
        });
      } catch (e) {
        // Fallback for older browsers
        const common = [
          'America/New_York',
          'America/Chicago',
          'America/Denver',
          'America/Los_Angeles',
          'Europe/London',
          'Europe/Paris',
          'Europe/Berlin',
          'Asia/Tokyo',
          'Asia/Shanghai',
          'Australia/Sydney',
          'Pacific/Auckland',
        ];
        common.forEach(tz => {
          const opt = document.createElement('option');
          opt.value = tz;
          opt.textContent = tz.replace(/_/g, ' ');
          if (tz === state.timezone) opt.selected = true;
          select.appendChild(opt);
        });
      }

      select.addEventListener('change', function () {
        state.timezone = this.value;
        // Re-fetch availability
        if (config.calendarDisplay === 'calendar') renderCalendar();
        if (state.selectedDate) loadTimeSlots(state.selectedDate);
      });
    }

    // ========== Price Check ==========
    let priceCheckTimeout = null;

    function runPriceCheck() {
      clearTimeout(priceCheckTimeout);
      priceCheckTimeout = setTimeout(doCheckBooking, 300);
    }

    async function doCheckBooking() {
      // Need at least a date selected
      if (!state.selectedDate) return;
      // For non-accommodation, need a slot too
      if (config.bookingType !== 'accommodation' && !state.selectedSlot) return;

      const data = {
        date: state.selectedDate,
        persons: state.persons,
      };

      if (state.selectedSlot) {
        data.time_start = state.selectedSlot.start;
        data.time_end = state.selectedSlot.end;
      }
      if (state.selectedEndDate) {
        data.end_date = state.selectedEndDate;
      }
      if (state.selectedResource) {
        data.resource_id = parseInt(state.selectedResource);
      }
      if (config.durationType === 'customer_selected') {
        data.duration = state.customDuration;
      }
      if (state.timezone) {
        data.timezone = state.timezone;
      }

      try {
        const result = await checkBooking(data);
        state.lastCheckResult = result;
        updateSummaryFromCheck(result);
      } catch (e) {
        // Silently ignore - button stays disabled
      }
    }

    /**
     * Group consecutive nights with the same rate into ranges.
     * E.g. 3 nights at $150 → "Mar 15–17: $150/night × 3"
     */
    function groupNightlyRates(breakdown) {
      if (!breakdown || !breakdown.length) return [];
      const groups = [];
      let cur = { ...breakdown[0], count: 1 };
      for (let i = 1; i < breakdown.length; i++) {
        const n = breakdown[i];
        if (n.nightly_total === cur.nightly_total && n.rule_name === cur.rule_name) {
          cur.count++;
          cur.endDate = n.date;
        } else {
          groups.push(cur);
          cur = { ...n, count: 1 };
        }
      }
      groups.push(cur);
      return groups;
    }

    function fmtShort(isoDate) {
      const d = new Date(isoDate + 'T00:00:00');
      return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
    }

    function renderBreakdown(result) {
      const el = document.getElementById('summary-breakdown');
      if (!el) return;

      // Only show breakdown for accommodation with nightly data
      const bd = result.nightly_breakdown;
      if (!bd || !bd.length) {
        el.innerHTML = '';
        return;
      }

      const sym = config.currencySymbol;
      const numNights = bd.length;

      // Sum nightly totals and check if rates vary
      let nightlySum = 0;
      const rates = new Set();
      for (const n of bd) {
        const t = parseFloat(n.nightly_total);
        nightlySum += t;
        rates.add(t.toFixed(2));
      }
      const allSameRate = rates.size === 1;
      const avgPerNight = (nightlySum / numNights).toFixed(2);
      const perNightRate = allSameRate ? parseFloat(bd[0].nightly_total).toFixed(2) : avgPerNight;

      let html = '<div class="booking-breakdown">';

      // Nightly rate summary (single line)
      const nightLabel = numNights === 1 ? 'night' : 'nights';
      const avgTag = allSameRate ? '' : ' <span class="booking-breakdown__avg">avg</span>';
      html += `<div class="booking-breakdown__line">
                <span class="booking-breakdown__desc">
                    ${numNights} ${nightLabel} \u00d7 ${sym}${perNightRate}/night${avgTag}
                </span>
                <span class="booking-breakdown__amount">${sym}${nightlySum.toFixed(2)}</span>
            </div>`;

      // One-time charges
      if (result.one_time_charges && parseFloat(result.one_time_charges) > 0) {
        html += `<div class="booking-breakdown__line">
                    <span class="booking-breakdown__desc">One-time charges</span>
                    <span class="booking-breakdown__amount">${sym}${parseFloat(result.one_time_charges).toFixed(2)}</span>
                </div>`;
      }

      // Length-of-stay discount
      if (result.length_of_stay_discount) {
        const d = result.length_of_stay_discount;
        html += `<div class="booking-breakdown__line booking-breakdown__line--discount">
                    <span class="booking-breakdown__desc">${d.label}</span>
                    <span class="booking-breakdown__amount">-${sym}${parseFloat(d.amount).toFixed(2)}</span>
                </div>`;
      }

      html += '</div>';
      el.innerHTML = html;
    }

    function updateSummaryFromCheck(result) {
      const summary = document.getElementById('booking-summary');
      const addToCart = document.getElementById('add-to-cart');
      const waitlist = document.getElementById('booking-waitlist');
      const unavailNotice = document.getElementById('booking-unavailable');
      const unavailReason = document.getElementById('booking-unavailable-reason');

      if (!summary) return;

      if (result.available) {
        summary.style.display = '';
        if (unavailNotice) unavailNotice.style.display = 'none';
        if (waitlist) waitlist.style.display = 'none';

        const totalEl = document.getElementById('summary-total');
        if (totalEl) {
          totalEl.textContent = `${config.currencySymbol}${parseFloat(result.total_price).toFixed(2)}`;
        }

        const depositEl = document.getElementById('summary-deposit');
        if (depositEl && result.deposit_amount) {
          depositEl.textContent = `${config.currencySymbol}${parseFloat(result.deposit_amount).toFixed(2)}`;
        }

        // Render nightly breakdown for accommodation
        renderBreakdown(result);

        if (addToCart) {
          addToCart.disabled = false;
        }
      } else {
        summary.style.display = 'none';
        if (addToCart) addToCart.disabled = true;

        // Clear breakdown
        const bdEl = document.getElementById('summary-breakdown');
        if (bdEl) bdEl.innerHTML = '';

        // Show unavailability reason
        if (unavailNotice && unavailReason && result.reason) {
          unavailReason.textContent = result.reason;
          unavailNotice.style.display = '';
        } else if (unavailNotice) {
          unavailNotice.style.display = 'none';
        }

        // Show waitlist if slot is full
        if (waitlist && result.reason && result.reason.includes('capacity')) {
          waitlist.style.display = '';
        }
      }
    }

    // ========== Add to Cart ==========
    function initAddToCart() {
      const btn = document.getElementById('add-to-cart');
      if (!btn) return;

      btn.addEventListener('click', async function () {
        if (this.disabled) return;
        this.disabled = true;
        const originalHTML = this.innerHTML;
        this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Booking...</span>';

        try {
          const bookingData = {
            date: state.selectedDate,
            persons: state.persons,
            timezone: state.timezone,
          };

          if (state.selectedSlot) {
            bookingData.start_time = state.selectedSlot.start;
            bookingData.end_time = state.selectedSlot.end;
          }
          if (state.selectedEndDate) {
            bookingData.end_date = state.selectedEndDate;
          }
          if (state.selectedResource) {
            bookingData.resource_id = parseInt(state.selectedResource);
          }
          if (config.durationType === 'customer_selected') {
            bookingData.custom_duration = state.customDuration;
          }

          // Build start/end datetimes for the cart
          let startDt, endDt;
          if (state.selectedSlot) {
            startDt = `${state.selectedDate}T${state.selectedSlot.start}:00`;
            endDt = `${state.selectedDate}T${state.selectedSlot.end}:00`;
          } else if (state.selectedEndDate) {
            startDt = `${state.selectedDate}T00:00:00`;
            endDt = `${state.selectedEndDate}T00:00:00`;
          }

          const cartData = {
            product_id: parseInt(config.productId),
            quantity: 1,
            booking_data: {
              start_datetime: startDt,
              end_datetime: endDt,
              resource_id: state.selectedResource ? parseInt(state.selectedResource) : null,
              persons: state.persons,
              timezone: state.timezone,
            },
          };

          const csrfToken = getCSRFToken();
          const resp = await fetch('/api/cart/add/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            credentials: 'same-origin',
            body: JSON.stringify(cartData),
          });

          if (resp.ok) {
            this.innerHTML = '<i class="fas fa-check"></i> <span>Redirecting to checkout...</span>';
            document.dispatchEvent(new CustomEvent('cart:updated'));
            window.location.href = '/checkout/';
          } else {
            const err = await resp.json();
            this.innerHTML = originalHTML;
            this.disabled = false;
            AdminModal.alert({
              message: err.error || 'Failed to add booking to cart',
              type: 'error',
            });
          }
        } catch (e) {
          this.innerHTML = originalHTML;
          this.disabled = false;
          AdminModal.alert({ message: 'Network error. Please try again.', type: 'error' });
        }
      });
    }

    // ========== Waitlist ==========
    function initWaitlist() {
      const submitBtn = document.getElementById('waitlist-submit');
      if (!submitBtn) return;

      submitBtn.addEventListener('click', async function () {
        const emailInput = document.getElementById('waitlist-email');
        const statusEl = document.getElementById('waitlist-status');
        if (!emailInput || !emailInput.value) return;

        submitBtn.disabled = true;
        submitBtn.textContent = '...';

        try {
          const result = await joinWaitlist(emailInput.value);
          if (statusEl) {
            statusEl.style.display = '';
            if (result.success) {
              statusEl.className = 'booking-waitlist__status booking-waitlist__status--success';
              statusEl.textContent = result.message || "You've been added to the waitlist!";
            } else {
              statusEl.className = 'booking-waitlist__status booking-waitlist__status--error';
              statusEl.textContent = result.error || 'Failed to join waitlist';
            }
          }
        } catch (e) {
          if (statusEl) {
            statusEl.style.display = '';
            statusEl.className = 'booking-waitlist__status booking-waitlist__status--error';
            statusEl.textContent = 'Network error. Please try again.';
          }
        } finally {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Join Waitlist';
        }
      });
    }

    // ========== Helpers ==========
    function formatDate(d) {
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
    }

    function enableStep(stepId) {
      const step = document.getElementById(stepId);
      if (step) {
        step.classList.remove('booking-step--disabled');
        step.classList.add('booking-step--active');
      }
    }

    // ========== Resource Detail Modal ==========
    function openResourceModal(resourceId) {
      const modal = document.getElementById('booking-resource-modal');
      if (!modal) return;
      const loading = document.getElementById('resource-modal-loading');
      const body = document.getElementById('resource-modal-body');

      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      if (loading) loading.style.display = '';
      if (body) body.style.display = 'none';

      // Store the resource id for the "Select" button
      modal.dataset.resourceId = resourceId;

      fetchResourceDetail(resourceId)
        .then(data => {
          if (loading) loading.style.display = 'none';
          if (body) body.style.display = '';
          renderResourceModal(data);
        })
        .catch(() => {
          if (loading)
            loading.innerHTML =
              '<p style="color:var(--theme-color-error,#ef4444)">Failed to load details</p>';
        });
    }

    function closeResourceModal() {
      const modal = document.getElementById('booking-resource-modal');
      if (!modal) return;
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }

    function renderResourceModal(data) {
      const titleEl = document.getElementById('resource-modal-title');
      const priceEl = document.getElementById('resource-modal-price');
      const descEl = document.getElementById('resource-modal-description');
      const mainImageEl = document.getElementById('resource-modal-main-image');
      const thumbsEl = document.getElementById('resource-modal-thumbs');

      if (titleEl) titleEl.textContent = data.name || '';
      if (descEl) {
        descEl.innerHTML = '';
        if (data.description) {
          const p = document.createElement('p');
          p.textContent = data.description;
          descEl.appendChild(p);
        }
      }

      if (priceEl) {
        const adj = parseFloat(data.base_cost_adjustment || 0);
        if (adj !== 0) {
          priceEl.textContent =
            (adj > 0 ? '+' : '') + config.currencySymbol + Math.abs(adj).toFixed(2) + ' per night';
          priceEl.style.display = '';
        } else {
          priceEl.style.display = 'none';
        }
      }

      // Gallery
      const images = data.images || [];
      if (mainImageEl) {
        mainImageEl.innerHTML = '';
        if (images.length) {
          const primary = images.find(i => i.is_primary) || images[0];
          if (primary.is_video) {
            const video = document.createElement('video');
            video.controls = true;
            video.playsInline = true;
            video.className = 'booking-resource-modal__video';
            if (primary.poster) video.poster = primary.poster;
            const src = document.createElement('source');
            src.src = primary.url;
            if (primary.video_type) src.type = primary.video_type;
            video.appendChild(src);
            mainImageEl.appendChild(video);
          } else {
            const img = document.createElement('img');
            img.src = primary.url;
            img.alt = primary.alt_text || data.name;
            img.className = 'booking-resource-modal__img';
            mainImageEl.appendChild(img);
          }
        } else {
          mainImageEl.innerHTML =
            '<div class="booking-resource-modal__no-image"><i class="fas fa-image"></i></div>';
        }
      }

      if (thumbsEl) {
        thumbsEl.innerHTML = '';
        if (images.length > 1) {
          images.forEach((img, i) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className =
              'booking-resource-modal__thumb' +
              (i === 0 || img.is_primary ? ' booking-resource-modal__thumb--active' : '');
            if (img.is_video) {
              btn.innerHTML = `<span class="booking-resource-modal__thumb-video"><i class="fas fa-play"></i></span><img src="${img.thumbnail}" alt="${img.alt_text || ''}" loading="lazy">`;
            } else {
              btn.innerHTML = `<img src="${img.thumbnail}" alt="${img.alt_text || ''}" loading="lazy">`;
            }
            btn.addEventListener('click', function () {
              thumbsEl
                .querySelectorAll('.booking-resource-modal__thumb--active')
                .forEach(t => t.classList.remove('booking-resource-modal__thumb--active'));
              this.classList.add('booking-resource-modal__thumb--active');
              swapResourceModalImage(img);
            });
            thumbsEl.appendChild(btn);
          });
        }
      }
    }

    function swapResourceModalImage(imgData) {
      const mainImageEl = document.getElementById('resource-modal-main-image');
      if (!mainImageEl) return;
      mainImageEl.innerHTML = '';
      if (imgData.is_video) {
        const video = document.createElement('video');
        video.controls = true;
        video.playsInline = true;
        video.className = 'booking-resource-modal__video';
        if (imgData.poster) video.poster = imgData.poster;
        const src = document.createElement('source');
        src.src = imgData.url;
        if (imgData.video_type) src.type = imgData.video_type;
        video.appendChild(src);
        mainImageEl.appendChild(video);
      } else {
        const img = document.createElement('img');
        img.src = imgData.url;
        img.alt = imgData.alt_text || '';
        img.className = 'booking-resource-modal__img';
        mainImageEl.appendChild(img);
      }
    }

    function initResourceModal() {
      const modal = document.getElementById('booking-resource-modal');
      if (!modal) return;

      // Close handlers
      const backdrop = modal.querySelector('.booking-resource-modal__backdrop');
      const closeBtn = modal.querySelector('.booking-resource-modal__close');
      if (backdrop) backdrop.addEventListener('click', closeResourceModal);
      if (closeBtn) closeBtn.addEventListener('click', closeResourceModal);
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.style.display !== 'none') {
          closeResourceModal();
        }
      });

      // "Select This Room" button
      const selectBtn = document.getElementById('resource-modal-select');
      if (selectBtn) {
        selectBtn.addEventListener('click', function () {
          const rid = modal.dataset.resourceId;
          if (rid) {
            const container = document.getElementById('booking-resources');
            const btn = container?.querySelector(`.booking-resource[data-resource-id="${rid}"]`);
            if (btn && !btn.disabled) {
              selectResource(btn);
            }
          }
          closeResourceModal();
        });
      }
    }

    // ========== Init ==========
    if (config.bookingType === 'accommodation') {
      // Accommodation always uses calendar grid with range selection
      initCalendarNav();
      renderCalendar();
    } else if (config.calendarDisplay === 'calendar') {
      initCalendarNav();
      renderCalendar();
    } else if (config.calendarDisplay === 'date_picker') {
      initDatePicker();
    } else if (config.calendarDisplay === 'dropdown') {
      initDropdown();
    } else if (config.calendarDisplay === 'date_range') {
      initDateRange();
    }

    initResources();
    initResourceModal();
    initPersonTypes();
    initDurationSlider();
    initTimezone();
    initAddToCart();
    initWaitlist();
  });
})();
