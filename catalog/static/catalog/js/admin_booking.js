/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Booking Cards Manager
 * AJAX-based booking management for booking products.
 * Replaces Django inlines with compact card rows + modal editing.
 */
(function () {
  'use strict';

  // ===== Utilities =====

  function getLanguagePrefix() {
    const match = window.location.pathname.match(/^\/([a-z]{2}(?:-[a-z]{2})?)\/admin/);
    return match ? '/' + match[1] : '';
  }

  function getProductId() {
    const urlMatch = window.location.pathname.match(/\/admin\/catalog\/product\/(\d+)\//);
    return urlMatch ? parseInt(urlMatch[1]) : null;
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text || '';
    return div.innerHTML;
  }

  function showNotification(message, type) {
    AdminModal.toast(message, type || 'info');
  }

  async function fetchJSON(url) {
    const resp = await fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
    });
    if (!resp.ok) {
      const data = await resp.json().catch(() => ({}));
      throw new Error(data.error || `HTTP ${resp.status}`);
    }
    return resp.json();
  }

  async function postJSON(url, data) {
    const resp = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: JSON.stringify(data),
    });
    const result = await resp.json();
    if (!resp.ok || !result.success) {
      throw new Error(result.error || `HTTP ${resp.status}`);
    }
    return result;
  }

  // ===== Main Manager =====

  const LANG = getLanguagePrefix();
  const PRODUCT_ID = getProductId();
  const BASE = `${LANG}/admin/catalog`;

  if (!PRODUCT_ID) return;

  const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  // Current modal state
  let modalEntityType = null; // 'resource', 'person_type', 'availability_rule', 'recurrence_rule'
  let modalEntityId = null; // null = creating, id = editing
  let modalResourceImages = []; // images for the resource being edited
  let availableResources = []; // cached resources for availability rule dropdown

  // DOM refs
  let modalOverlay, modalTitle, modalBody, modalSaveBtn, modalSaveText;

  // ===================================================================
  // BOOKING CONFIG (Singleton form)
  // ===================================================================

  async function loadBookingConfig() {
    const container = document.getElementById('booking-config-form');
    if (!container) return;
    try {
      const data = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/booking-config/`);
      renderBookingConfigForm(container, data.exists ? data.config : null);
    } catch (e) {
      container.innerHTML =
        '<div class="booking-list-loading" style="color:var(--error-color,#d93025);"><i class="fas fa-exclamation-circle"></i> Failed to load configuration</div>';
    }
  }

  function renderBookingConfigForm(container, config) {
    const c = config || {};

    container.innerHTML = `
        <div class="booking-config-form">
            <div class="booking-config-section" id="bk-section-type">
                <div class="booking-config-section__header">
                    <h4><i class="fas fa-tag"></i> Booking Type & Duration</h4>
                    <i class="fas fa-chevron-down booking-config-section__toggle"></i>
                </div>
                <div class="booking-config-section__body">
                    <div class="booking-modal-field">
                        <label>Booking Type</label>
                        <select id="bk-booking_type">
                            <option value="appointment" ${c.booking_type === 'appointment' ? 'selected' : ''}>Appointment</option>
                            <option value="rental" ${c.booking_type === 'rental' ? 'selected' : ''}>Rental</option>
                            <option value="class" ${c.booking_type === 'class' ? 'selected' : ''}>Class / Workshop</option>
                            <option value="accommodation" ${c.booking_type === 'accommodation' ? 'selected' : ''}>Accommodation</option>
                            <option value="event" ${c.booking_type === 'event' ? 'selected' : ''}>Event</option>
                        </select>
                    </div>
                    <div class="booking-modal-field">
                        <label>Duration Type</label>
                        <select id="bk-duration_type">
                            <option value="fixed" ${c.duration_type === 'fixed' ? 'selected' : ''}>Fixed Duration</option>
                            <option value="customer_selected" ${c.duration_type === 'customer_selected' ? 'selected' : ''}>Customer Selects Duration</option>
                        </select>
                    </div>
                    <div class="booking-modal-field">
                        <label>Duration</label>
                        <input type="number" id="bk-duration" value="${c.duration || 60}" min="1">
                    </div>
                    <div class="booking-modal-field">
                        <label>Duration Unit</label>
                        <select id="bk-duration_unit">
                            <option value="minute" ${c.duration_unit === 'minute' ? 'selected' : ''}>Minute(s)</option>
                            <option value="hour" ${c.duration_unit === 'hour' ? 'selected' : ''}>Hour(s)</option>
                            <option value="day" ${c.duration_unit === 'day' ? 'selected' : ''}>Day(s)</option>
                            <option value="night" ${c.duration_unit === 'night' ? 'selected' : ''}>Night(s)</option>
                        </select>
                    </div>
                    <div class="booking-modal-field" id="bk-field-min_duration">
                        <label>Min Duration</label>
                        <input type="number" id="bk-min_duration" value="${c.min_duration || ''}" min="1" placeholder="Optional">
                        <span class="booking-modal-help">For customer-selected duration type</span>
                    </div>
                    <div class="booking-modal-field" id="bk-field-max_duration">
                        <label>Max Duration</label>
                        <input type="number" id="bk-max_duration" value="${c.max_duration || ''}" min="1" placeholder="Optional">
                    </div>
                </div>
            </div>

            <div class="booking-config-section" id="bk-section-scheduling">
                <div class="booking-config-section__header">
                    <h4><i class="fas fa-clock"></i> Scheduling</h4>
                    <i class="fas fa-chevron-down booking-config-section__toggle"></i>
                </div>
                <div class="booking-config-section__body">
                    <div class="booking-modal-field">
                        <label>Buffer Before (min)</label>
                        <input type="number" id="bk-buffer_before" value="${c.buffer_before || 0}" min="0">
                    </div>
                    <div class="booking-modal-field">
                        <label>Buffer After (min)</label>
                        <input type="number" id="bk-buffer_after" value="${c.buffer_after || 0}" min="0">
                    </div>
                    <div class="booking-modal-field">
                        <label>Min Advance Notice</label>
                        <input type="number" id="bk-min_advance" value="${c.min_advance || 0}" min="0">
                    </div>
                    <div class="booking-modal-field">
                        <label>Min Advance Unit</label>
                        <select id="bk-min_advance_unit">
                            <option value="hour" ${c.min_advance_unit === 'hour' ? 'selected' : ''}>Hours</option>
                            <option value="day" ${c.min_advance_unit === 'day' ? 'selected' : ''}>Days</option>
                            <option value="week" ${c.min_advance_unit === 'week' ? 'selected' : ''}>Weeks</option>
                            <option value="month" ${c.min_advance_unit === 'month' ? 'selected' : ''}>Months</option>
                        </select>
                    </div>
                    <div class="booking-modal-field">
                        <label>Max Advance Booking</label>
                        <input type="number" id="bk-max_advance" value="${c.max_advance || 365}" min="1">
                    </div>
                    <div class="booking-modal-field">
                        <label>Max Advance Unit</label>
                        <select id="bk-max_advance_unit">
                            <option value="hour" ${c.max_advance_unit === 'hour' ? 'selected' : ''}>Hours</option>
                            <option value="day" ${(c.max_advance_unit || 'day') === 'day' ? 'selected' : ''}>Days</option>
                            <option value="week" ${c.max_advance_unit === 'week' ? 'selected' : ''}>Weeks</option>
                            <option value="month" ${c.max_advance_unit === 'month' ? 'selected' : ''}>Months</option>
                        </select>
                    </div>
                    <div class="booking-modal-field booking-modal-field--full">
                        <label>Max Bookings Per Slot</label>
                        <input type="number" id="bk-max_bookings_per_slot" value="${c.max_bookings_per_slot || 1}" min="1">
                        <span class="booking-modal-help">Maximum simultaneous bookings per time slot</span>
                    </div>
                </div>
            </div>

            <div class="booking-config-section" id="bk-section-confirmation">
                <div class="booking-config-section__header">
                    <h4><i class="fas fa-check-double"></i> Confirmation & Cancellation</h4>
                    <i class="fas fa-chevron-down booking-config-section__toggle"></i>
                </div>
                <div class="booking-config-section__body">
                    <div class="booking-modal-field--checkbox booking-modal-field--full">
                        <label><input type="checkbox" id="bk-confirmation_required" ${c.confirmation_required ? 'checked' : ''}> Require manual confirmation</label>
                        <span class="booking-modal-help">If unchecked, bookings are auto-confirmed</span>
                    </div>
                    <div class="booking-modal-field--checkbox booking-modal-field--full">
                        <label><input type="checkbox" id="bk-cancellation_allowed" ${c.cancellation_allowed !== false ? 'checked' : ''}> Allow cancellation</label>
                    </div>
                    <div class="booking-modal-field" id="bk-field-cancellation_deadline">
                        <label>Cancellation Deadline</label>
                        <input type="number" id="bk-cancellation_deadline" value="${c.cancellation_deadline || 24}" min="0">
                    </div>
                    <div class="booking-modal-field" id="bk-field-cancellation_deadline_unit">
                        <label>Deadline Unit</label>
                        <select id="bk-cancellation_deadline_unit">
                            <option value="hour" ${(c.cancellation_deadline_unit || 'hour') === 'hour' ? 'selected' : ''}>Hours</option>
                            <option value="day" ${c.cancellation_deadline_unit === 'day' ? 'selected' : ''}>Days</option>
                            <option value="week" ${c.cancellation_deadline_unit === 'week' ? 'selected' : ''}>Weeks</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="booking-config-section" id="bk-section-display">
                <div class="booking-config-section__header">
                    <h4><i class="fas fa-desktop"></i> Display & UX</h4>
                    <i class="fas fa-chevron-down booking-config-section__toggle"></i>
                </div>
                <div class="booking-config-section__body">
                    <div class="booking-modal-field">
                        <label>Calendar Display</label>
                        <select id="bk-calendar_display">
                            <option value="calendar" ${(c.calendar_display || 'calendar') === 'calendar' ? 'selected' : ''}>Calendar View</option>
                            <option value="date_picker" ${c.calendar_display === 'date_picker' ? 'selected' : ''}>Date Picker</option>
                            <option value="dropdown" ${c.calendar_display === 'dropdown' ? 'selected' : ''}>Available Dates Dropdown</option>
                            <option value="date_range" ${c.calendar_display === 'date_range' ? 'selected' : ''}>Date Range Picker</option>
                        </select>
                    </div>
                    <div class="booking-modal-field--checkbox">
                        <label><input type="checkbox" id="bk-customer_timezone_enabled" ${c.customer_timezone_enabled ? 'checked' : ''}> Show times in customer timezone</label>
                    </div>
                </div>
            </div>

            <div class="booking-config-section collapsed" id="bk-section-deposits">
                <div class="booking-config-section__header">
                    <h4><i class="fas fa-money-bill-wave"></i> Deposits</h4>
                    <i class="fas fa-chevron-down booking-config-section__toggle"></i>
                </div>
                <div class="booking-config-section__body">
                    <div class="booking-modal-field--checkbox booking-modal-field--full">
                        <label><input type="checkbox" id="bk-deposit_enabled" ${c.deposit_enabled ? 'checked' : ''}> Enable deposits</label>
                    </div>
                    <div class="booking-modal-field" id="bk-field-deposit_type">
                        <label>Deposit Type</label>
                        <select id="bk-deposit_type">
                            <option value="fixed" ${c.deposit_type === 'fixed' ? 'selected' : ''}>Fixed Amount</option>
                            <option value="percentage" ${(c.deposit_type || 'percentage') === 'percentage' ? 'selected' : ''}>Percentage of Total</option>
                        </select>
                    </div>
                    <div class="booking-modal-field" id="bk-field-deposit_amount">
                        <label>Deposit Amount</label>
                        <input type="number" id="bk-deposit_amount" value="${c.deposit_amount || 0}" min="0" step="0.01">
                    </div>
                </div>
            </div>

            <div class="booking-config-section collapsed" id="bk-section-accommodation">
                <div class="booking-config-section__header">
                    <h4><i class="fas fa-bed"></i> Accommodation</h4>
                    <i class="fas fa-chevron-down booking-config-section__toggle"></i>
                </div>
                <div class="booking-config-section__body">
                    <div class="booking-modal-field">
                        <label>Check-in Time</label>
                        <input type="time" id="bk-check_in_time" value="${c.check_in_time || ''}">
                    </div>
                    <div class="booking-modal-field">
                        <label>Check-out Time</label>
                        <input type="time" id="bk-check_out_time" value="${c.check_out_time || ''}">
                    </div>
                    <div class="booking-modal-field">
                        <label>Standard Occupancy</label>
                        <input type="number" id="bk-standard_occupancy" min="1" value="${c.standard_occupancy || 2}">
                        <span class="booking-modal-help">Guests included in base rate</span>
                    </div>
                    <div class="booking-modal-field">
                        <label>Max Occupancy</label>
                        <input type="number" id="bk-max_occupancy" min="0" value="${c.max_occupancy || 0}">
                        <span class="booking-modal-help">Total guest limit (0 = no limit)</span>
                    </div>
                    <div class="booking-modal-field">
                        <label>Minimum Stay (nights)</label>
                        <input type="number" id="bk-min_stay" min="1" value="${c.min_stay || 1}">
                    </div>
                    <div class="booking-modal-field">
                        <label>Maximum Stay (nights)</label>
                        <input type="number" id="bk-max_stay" min="1" value="${c.max_stay || 365}">
                    </div>
                </div>
            </div>

            <div class="booking-config-section collapsed" id="bk-section-recurrence">
                <div class="booking-config-section__header">
                    <h4><i class="fas fa-redo"></i> Recurring Bookings</h4>
                    <i class="fas fa-chevron-down booking-config-section__toggle"></i>
                </div>
                <div class="booking-config-section__body">
                    <div class="booking-modal-field--checkbox booking-modal-field--full">
                        <label><input type="checkbox" id="bk-recurrence_enabled" ${c.recurrence_enabled ? 'checked' : ''}> Allow recurring booking schedules</label>
                    </div>
                </div>
            </div>

            <div class="booking-config-section collapsed" id="bk-section-reminders">
                <div class="booking-config-section__header">
                    <h4><i class="fas fa-bell"></i> Reminders</h4>
                    <i class="fas fa-chevron-down booking-config-section__toggle"></i>
                </div>
                <div class="booking-config-section__body">
                    <div class="booking-modal-field--checkbox booking-modal-field--full">
                        <label><input type="checkbox" id="bk-reminder_enabled" ${c.reminder_enabled !== false ? 'checked' : ''}> Enable reminders</label>
                    </div>
                    <div class="booking-modal-field booking-modal-field--full" id="bk-field-reminder_hours_before">
                        <label>Reminder Hours Before</label>
                        <input type="text" id="bk-reminder_hours_before" value="${(c.reminder_hours_before || []).join(', ')}" placeholder="e.g. 1, 24, 168">
                        <span class="booking-modal-help">Comma-separated hours (e.g. 1 = 1hr before, 24 = 1 day before)</span>
                    </div>
                </div>
            </div>

            <div class="booking-config-actions">
                <button type="button" class="booking-config-save-btn" id="booking-config-save-btn">
                    <i class="fas fa-save"></i> Save Configuration
                </button>
            </div>
        </div>`;

    // Bind collapsible section toggles
    container.querySelectorAll('.booking-config-section__header').forEach(header => {
      header.addEventListener('click', function () {
        this.parentElement.classList.toggle('collapsed');
      });
    });

    // Bind save button
    document.getElementById('booking-config-save-btn').addEventListener('click', saveBookingConfig);

    // Bind dynamic field visibility triggers
    const visibilityTriggers = [
      'bk-booking_type',
      'bk-duration_type',
      'bk-cancellation_allowed',
      'bk-deposit_enabled',
      'bk-reminder_enabled',
    ];
    visibilityTriggers.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('change', updateBookingConfigVisibility);
    });

    // Apply initial visibility based on loaded config values
    updateBookingConfigVisibility();
  }

  function updateBookingConfigVisibility() {
    const bookingType = document.getElementById('bk-booking_type')?.value;
    const durationType = document.getElementById('bk-duration_type')?.value;
    const cancellationAllowed = document.getElementById('bk-cancellation_allowed')?.checked;
    const depositEnabled = document.getElementById('bk-deposit_enabled')?.checked;
    const reminderEnabled = document.getElementById('bk-reminder_enabled')?.checked;

    // Accommodation section — only for accommodation type
    const accomSection = document.getElementById('bk-section-accommodation');
    if (accomSection) {
      accomSection.style.display = bookingType === 'accommodation' ? '' : 'none';
      if (bookingType === 'accommodation') accomSection.classList.remove('collapsed');
    }

    // Recurrence section — hide for appointment and rental
    const recurSection = document.getElementById('bk-section-recurrence');
    if (recurSection) {
      recurSection.style.display = ['class', 'event', 'accommodation'].includes(bookingType)
        ? ''
        : 'none';
    }

    // Min/Max duration — only when customer selects duration
    const showMinMax = durationType === 'customer_selected';
    ['bk-field-min_duration', 'bk-field-max_duration'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.display = showMinMax ? '' : 'none';
    });

    // Cancellation deadline fields — only when cancellation is allowed
    ['bk-field-cancellation_deadline', 'bk-field-cancellation_deadline_unit'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.display = cancellationAllowed ? '' : 'none';
    });

    // Deposit type/amount — only when deposit is enabled
    ['bk-field-deposit_type', 'bk-field-deposit_amount'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.display = depositEnabled ? '' : 'none';
    });

    // Reminder hours — only when reminders are enabled
    const reminderHoursField = document.getElementById('bk-field-reminder_hours_before');
    if (reminderHoursField) reminderHoursField.style.display = reminderEnabled ? '' : 'none';
  }

  async function saveBookingConfig() {
    const btn = document.getElementById('booking-config-save-btn');
    const origText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    btn.disabled = true;

    const getVal = id => document.getElementById(id)?.value || '';
    const getChecked = id => document.getElementById(id)?.checked || false;
    const getNum = id => {
      const v = document.getElementById(id)?.value;
      return v !== '' && v !== undefined ? parseInt(v) : null;
    };

    // Parse reminder hours
    const reminderStr = getVal('bk-reminder_hours_before');
    let reminderHours = [];
    if (reminderStr.trim()) {
      reminderHours = reminderStr
        .split(',')
        .map(s => parseInt(s.trim()))
        .filter(n => !isNaN(n));
    }

    const data = {
      booking_type: getVal('bk-booking_type'),
      duration_type: getVal('bk-duration_type'),
      duration: getNum('bk-duration'),
      duration_unit: getVal('bk-duration_unit'),
      min_duration: getNum('bk-min_duration'),
      max_duration: getNum('bk-max_duration'),
      buffer_before: getNum('bk-buffer_before'),
      buffer_after: getNum('bk-buffer_after'),
      min_advance: getNum('bk-min_advance'),
      min_advance_unit: getVal('bk-min_advance_unit'),
      max_advance: getNum('bk-max_advance'),
      max_advance_unit: getVal('bk-max_advance_unit'),
      max_bookings_per_slot: getNum('bk-max_bookings_per_slot'),
      confirmation_required: getChecked('bk-confirmation_required'),
      cancellation_allowed: getChecked('bk-cancellation_allowed'),
      cancellation_deadline: getNum('bk-cancellation_deadline'),
      cancellation_deadline_unit: getVal('bk-cancellation_deadline_unit'),
      calendar_display: getVal('bk-calendar_display'),
      customer_timezone_enabled: getChecked('bk-customer_timezone_enabled'),
      deposit_enabled: getChecked('bk-deposit_enabled'),
      deposit_type: getVal('bk-deposit_type'),
      deposit_amount: getVal('bk-deposit_amount'),
      check_in_time: getVal('bk-check_in_time'),
      check_out_time: getVal('bk-check_out_time'),
      standard_occupancy: getNum('bk-standard_occupancy'),
      max_occupancy: getNum('bk-max_occupancy'),
      min_stay: getNum('bk-min_stay'),
      max_stay: getNum('bk-max_stay'),
      recurrence_enabled: getChecked('bk-recurrence_enabled'),
      reminder_enabled: getChecked('bk-reminder_enabled'),
      reminder_hours_before: reminderHours,
    };

    try {
      await postJSON(`${BASE}/product/${PRODUCT_ID}/booking-config/save/`, data);
      showNotification('Configuration saved', 'success');
    } catch (e) {
      showNotification('Failed to save: ' + e.message, 'error');
    } finally {
      btn.innerHTML = origText;
      btn.disabled = false;
    }
  }

  // ===================================================================
  // RESOURCES (Card list)
  // ===================================================================

  async function loadResources() {
    try {
      const data = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/booking-resources/list/`);
      renderResourceList(data.resources || []);
      const badge = document.getElementById('booking-resource-count');
      if (badge) badge.textContent = data.count || 0;
    } catch (e) {
      const el = document.getElementById('booking-resource-list');
      if (el)
        el.innerHTML =
          '<div class="booking-list-loading" style="color:var(--error-color);"><i class="fas fa-exclamation-circle"></i> Failed to load</div>';
    }
  }

  function renderResourceList(resources) {
    const el = document.getElementById('booking-resource-list');
    if (!el) return;

    if (!resources.length) {
      el.innerHTML =
        '<div class="booking-empty-state"><i class="fas fa-users"></i><p>No resources yet. Add staff, rooms, or equipment.</p></div>';
      return;
    }

    const RESOURCE_ICONS = {
      staff: 'fas fa-user-tie',
      room: 'fas fa-door-open',
      equipment: 'fas fa-wrench',
      vehicle: 'fas fa-car',
      generic: 'fas fa-cube',
    };

    el.innerHTML = resources
      .map(
        r => `
            <div class="booking-card-row" data-id="${r.id}">
                <div class="booking-card-row__icon"><i class="${RESOURCE_ICONS[r.resource_type] || 'fas fa-cube'}"></i></div>
                <div class="booking-card-row__info">
                    <div class="booking-card-row__name">${escapeHtml(r.name)}</div>
                    <div class="booking-card-row__desc">${escapeHtml(r.resource_type_display)} &middot; Qty: ${r.quantity} &middot; ${escapeHtml(r.assignment_type_display)}</div>
                </div>
                <div class="booking-card-row__badges">
                    ${
                      r.is_active
                        ? '<span class="booking-card-row__badge booking-card-row__badge--active">Active</span>'
                        : '<span class="booking-card-row__badge booking-card-row__badge--inactive">Inactive</span>'
                    }
                    ${
                      parseFloat(r.base_cost_adjustment) !== 0
                        ? `<span class="booking-card-row__badge">${parseFloat(r.base_cost_adjustment) > 0 ? '+' : ''}${r.base_cost_adjustment}</span>`
                        : ''
                    }
                </div>
                <div class="booking-card-row__actions">
                    <button type="button" class="booking-card-row__action" data-action="edit" title="Edit"><i class="fas fa-pencil-alt"></i></button>
                    <button type="button" class="booking-card-row__action booking-card-row__action--danger" data-action="delete" title="Delete"><i class="fas fa-trash-alt"></i></button>
                </div>
            </div>
        `
      )
      .join('');
  }

  function openResourceModal(resourceId) {
    modalEntityType = 'resource';
    modalEntityId = resourceId;
    modalTitle.textContent = resourceId ? 'Edit Resource' : 'Add Resource';
    modalSaveText.textContent = resourceId ? 'Update Resource' : 'Save Resource';

    if (resourceId) {
      modalBody.innerHTML =
        '<div class="booking-list-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
      showModal();
      fetchJSON(`${BASE}/booking-resource/${resourceId}/detail/`)
        .then(data => {
          renderResourceForm(data.resource);
        })
        .catch(e => {
          modalBody.innerHTML = `<p style="color:var(--error-color);">Failed to load: ${escapeHtml(e.message)}</p>`;
        });
    } else {
      renderResourceForm(null);
      showModal();
    }
  }

  function renderResourceForm(r) {
    const d = r || {};
    modalResourceImages = (d.images || []).map(img => ({ ...img }));
    modalBody.innerHTML = `
            <div class="booking-modal-section">
                <h4><i class="fas fa-info-circle"></i> Resource Details</h4>
                <div class="booking-modal-field">
                    <label>Name <span class="required">*</span></label>
                    <input type="text" id="modal-resource-name" value="${escapeHtml(d.name || '')}" placeholder="e.g. Dr. Smith, Room A">
                </div>
                <div class="booking-modal-field">
                    <label>Description</label>
                    <textarea id="modal-resource-description" placeholder="Optional description">${escapeHtml(d.description || '')}</textarea>
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Resource Type</label>
                        <select id="modal-resource-type">
                            <option value="staff" ${d.resource_type === 'staff' ? 'selected' : ''}>Staff Member</option>
                            <option value="room" ${d.resource_type === 'room' ? 'selected' : ''}>Room</option>
                            <option value="equipment" ${d.resource_type === 'equipment' ? 'selected' : ''}>Equipment</option>
                            <option value="vehicle" ${d.resource_type === 'vehicle' ? 'selected' : ''}>Vehicle</option>
                            <option value="generic" ${(d.resource_type || 'generic') === 'generic' ? 'selected' : ''}>Generic Resource</option>
                        </select>
                    </div>
                    <div class="booking-modal-field">
                        <label>Quantity</label>
                        <input type="number" id="modal-resource-quantity" value="${d.quantity || 1}" min="1">
                    </div>
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Assignment Type</label>
                        <select id="modal-resource-assignment">
                            <option value="customer_selected" ${(d.assignment_type || 'customer_selected') === 'customer_selected' ? 'selected' : ''}>Customer Selects</option>
                            <option value="automatic" ${d.assignment_type === 'automatic' ? 'selected' : ''}>Auto-Assigned</option>
                        </select>
                    </div>
                    <div class="booking-modal-field">
                        <label>Cost Adjustment</label>
                        <input type="number" id="modal-resource-cost" value="${d.base_cost_adjustment || 0}" step="0.01">
                        <span class="booking-modal-help">Price modifier when selected</span>
                    </div>
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Email</label>
                        <input type="email" id="modal-resource-email" value="${escapeHtml(d.email || '')}" placeholder="For notifications">
                    </div>
                    <div class="booking-modal-field">
                        <label>Sort Order</label>
                        <input type="number" id="modal-resource-sort" value="${d.sort_order || 0}" min="0">
                    </div>
                </div>
                <div class="booking-modal-field--checkbox">
                    <label><input type="checkbox" id="modal-resource-active" ${d.is_active !== false ? 'checked' : ''}> Active</label>
                </div>
                <div class="booking-modal-field--checkbox">
                    <label><input type="checkbox" id="modal-resource-per-night" ${d.is_per_night !== false ? 'checked' : ''}> Charge per night (accommodation)</label>
                    <span class="booking-modal-help">If unchecked, cost adjustment is a one-time charge</span>
                </div>
            </div>
            <div class="booking-modal-section">
                <h4><i class="fas fa-images"></i> Images &amp; Media</h4>
                <div class="resource-images-grid" id="resource-images-grid"></div>
                <button type="button" class="booking-btn booking-btn--outline" id="resource-add-images">
                    <i class="fas fa-plus"></i> Add Images
                </button>
            </div>`;
    renderResourceImageGrid();
    document
      .getElementById('resource-add-images')
      .addEventListener('click', openResourceMediaPicker);
  }

  function openResourceMediaPicker() {
    if (typeof window.selectMultipleMedia !== 'function') {
      showNotification('Media library not available', 'error');
      return;
    }
    window.selectMultipleMedia(function (selectedMedia) {
      if (!selectedMedia || !selectedMedia.length) return;
      selectedMedia.forEach(m => {
        if (modalResourceImages.some(x => x.media_asset_id === m.id)) return;
        modalResourceImages.push({
          media_asset_id: m.id,
          url: m.url || m.original_url,
          thumbnail: m.thumbnail_url || m.url,
          alt_text: m.alt_text || m.title || '',
          is_primary: modalResourceImages.length === 0,
          is_video: m.type === 'video' || (m.mime_type && m.mime_type.startsWith('video/')),
          position: modalResourceImages.length,
        });
      });
      renderResourceImageGrid();
    });
  }

  function renderResourceImageGrid() {
    const grid = document.getElementById('resource-images-grid');
    if (!grid) return;
    if (!modalResourceImages.length) {
      grid.innerHTML =
        '<p class="booking-modal-help" style="margin:0">No images added yet. Click "Add Images" to select from the media library.</p>';
      return;
    }
    grid.innerHTML = modalResourceImages
      .map(
        (img, i) => `
            <div class="resource-image-card${img.is_primary ? ' resource-image-card--primary' : ''}" data-idx="${i}">
                <div class="resource-image-card__preview">
                    ${
                      img.is_video
                        ? '<i class="fas fa-video resource-image-card__video-icon"></i>'
                        : ''
                    }
                    <img src="${escapeHtml(img.thumbnail || img.url)}" alt="${escapeHtml(img.alt_text)}">
                </div>
                <div class="resource-image-card__actions">
                    <button type="button" class="resource-image-card__btn resource-image-card__btn--primary"
                            title="${img.is_primary ? 'Primary image' : 'Set as primary'}"
                            data-action="primary" data-idx="${i}">
                        <i class="fas fa-star${img.is_primary ? '' : ' far fa-star'}"></i>
                    </button>
                    <button type="button" class="resource-image-card__btn resource-image-card__btn--remove"
                            title="Remove" data-action="remove" data-idx="${i}">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `
      )
      .join('');

    grid.querySelectorAll('[data-action="primary"]').forEach(btn => {
      btn.addEventListener('click', function () {
        const idx = parseInt(this.dataset.idx);
        modalResourceImages.forEach((img, j) => {
          img.is_primary = j === idx;
        });
        renderResourceImageGrid();
      });
    });
    grid.querySelectorAll('[data-action="remove"]').forEach(btn => {
      btn.addEventListener('click', function () {
        const idx = parseInt(this.dataset.idx);
        modalResourceImages.splice(idx, 1);
        if (modalResourceImages.length && !modalResourceImages.some(x => x.is_primary)) {
          modalResourceImages[0].is_primary = true;
        }
        modalResourceImages.forEach((img, j) => {
          img.position = j;
        });
        renderResourceImageGrid();
      });
    });
  }

  function collectResourceData() {
    return {
      name: document.getElementById('modal-resource-name')?.value || '',
      description: document.getElementById('modal-resource-description')?.value || '',
      resource_type: document.getElementById('modal-resource-type')?.value || 'generic',
      quantity: parseInt(document.getElementById('modal-resource-quantity')?.value || 1),
      assignment_type:
        document.getElementById('modal-resource-assignment')?.value || 'customer_selected',
      base_cost_adjustment: document.getElementById('modal-resource-cost')?.value || '0',
      email: document.getElementById('modal-resource-email')?.value || '',
      sort_order: parseInt(document.getElementById('modal-resource-sort')?.value || 0),
      is_active: document.getElementById('modal-resource-active')?.checked ?? true,
      is_per_night: document.getElementById('modal-resource-per-night')?.checked ?? true,
      images: modalResourceImages.map((img, i) => ({
        media_asset_id: img.media_asset_id,
        alt_text: img.alt_text || '',
        is_primary: !!img.is_primary,
        position: i,
      })),
    };
  }

  async function saveResource() {
    const data = collectResourceData();
    if (!data.name.trim()) {
      showNotification('Name is required', 'error');
      return;
    }
    try {
      if (modalEntityId) {
        await postJSON(`${BASE}/booking-resource/${modalEntityId}/update/`, data);
        showNotification('Resource updated', 'success');
      } else {
        await postJSON(`${BASE}/product/${PRODUCT_ID}/booking-resources/create/`, data);
        showNotification('Resource created', 'success');
      }
      hideModal();
      loadResources();
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  async function deleteResource(id) {
    if (
      !(await AdminModal.confirm({
        message: 'Delete this resource? This cannot be undone.',
        danger: true,
        confirmText: 'Delete',
      }))
    )
      return;
    try {
      await postJSON(`${BASE}/booking-resource/${id}/delete/`, {});
      showNotification('Resource deleted', 'success');
      loadResources();
      loadAvailabilityRules(); // rules may reference this resource
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  // ===================================================================
  // PERSON TYPES (Card list)
  // ===================================================================

  async function loadPersonTypes() {
    try {
      const data = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/booking-person-types/list/`);
      renderPersonTypeList(data.person_types || []);
      const badge = document.getElementById('booking-person-type-count');
      if (badge) badge.textContent = data.count || 0;
    } catch (e) {
      const el = document.getElementById('booking-person-type-list');
      if (el)
        el.innerHTML =
          '<div class="booking-list-loading" style="color:var(--error-color);"><i class="fas fa-exclamation-circle"></i> Failed to load</div>';
    }
  }

  function renderPersonTypeList(types) {
    const el = document.getElementById('booking-person-type-list');
    if (!el) return;

    if (!types.length) {
      el.innerHTML =
        '<div class="booking-empty-state"><i class="fas fa-user-friends"></i><p>No person types yet. Add types like Adult, Child, Senior.</p></div>';
      return;
    }

    el.innerHTML = types
      .map(
        pt => `
            <div class="booking-card-row" data-id="${pt.id}">
                <div class="booking-card-row__icon"><i class="fas fa-user"></i></div>
                <div class="booking-card-row__info">
                    <div class="booking-card-row__name">${escapeHtml(pt.name)}</div>
                    <div class="booking-card-row__desc">Min: ${pt.min_persons} &middot; Max: ${pt.max_persons}${pt.is_counted_for_capacity ? '' : ' &middot; Not counted for capacity'}</div>
                </div>
                <div class="booking-card-row__badges">
                    <span class="booking-card-row__badge">${parseFloat(pt.cost_adjustment) >= 0 ? '+' : ''}${pt.cost_adjustment}</span>
                </div>
                <div class="booking-card-row__actions">
                    <button type="button" class="booking-card-row__action" data-action="edit" title="Edit"><i class="fas fa-pencil-alt"></i></button>
                    <button type="button" class="booking-card-row__action booking-card-row__action--danger" data-action="delete" title="Delete"><i class="fas fa-trash-alt"></i></button>
                </div>
            </div>
        `
      )
      .join('');
  }

  function openPersonTypeModal(id) {
    modalEntityType = 'person_type';
    modalEntityId = id;
    modalTitle.textContent = id ? 'Edit Person Type' : 'Add Person Type';
    modalSaveText.textContent = id ? 'Update' : 'Save';

    if (id) {
      modalBody.innerHTML =
        '<div class="booking-list-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
      showModal();
      fetchJSON(`${BASE}/booking-person-type/${id}/detail/`)
        .then(data => {
          renderPersonTypeForm(data.person_type);
        })
        .catch(e => {
          modalBody.innerHTML = `<p style="color:var(--error-color);">Failed to load: ${escapeHtml(e.message)}</p>`;
        });
    } else {
      renderPersonTypeForm(null);
      showModal();
    }
  }

  function renderPersonTypeForm(pt) {
    const d = pt || {};
    modalBody.innerHTML = `
            <div class="booking-modal-section">
                <h4><i class="fas fa-user-friends"></i> Person Type Details</h4>
                <div class="booking-modal-field">
                    <label>Name <span class="required">*</span></label>
                    <input type="text" id="modal-pt-name" value="${escapeHtml(d.name || '')}" placeholder="e.g. Adult, Child, Senior">
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Cost Adjustment</label>
                        <input type="number" id="modal-pt-cost" value="${d.cost_adjustment || 0}" step="0.01">
                        <span class="booking-modal-help">Per-person price modifier</span>
                    </div>
                    <div class="booking-modal-field">
                        <label>Sort Order</label>
                        <input type="number" id="modal-pt-sort" value="${d.sort_order || 0}" min="0">
                    </div>
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Min Persons</label>
                        <input type="number" id="modal-pt-min" value="${d.min_persons || 0}" min="0">
                    </div>
                    <div class="booking-modal-field">
                        <label>Max Persons</label>
                        <input type="number" id="modal-pt-max" value="${d.max_persons || 10}" min="1">
                    </div>
                </div>
                <div class="booking-modal-field--checkbox">
                    <label><input type="checkbox" id="modal-pt-capacity" ${d.is_counted_for_capacity !== false ? 'checked' : ''}> Count for capacity</label>
                    <span class="booking-modal-help">Count this person type against slot capacity</span>
                </div>
                <div class="booking-modal-field--checkbox">
                    <label><input type="checkbox" id="modal-pt-per-night" ${d.is_per_night !== false ? 'checked' : ''}> Charge per night (accommodation)</label>
                    <span class="booking-modal-help">If unchecked, cost adjustment is a one-time charge</span>
                </div>
            </div>`;
  }

  function collectPersonTypeData() {
    return {
      name: document.getElementById('modal-pt-name')?.value || '',
      cost_adjustment: document.getElementById('modal-pt-cost')?.value || '0',
      min_persons: parseInt(document.getElementById('modal-pt-min')?.value || 0),
      max_persons: parseInt(document.getElementById('modal-pt-max')?.value || 10),
      is_counted_for_capacity: document.getElementById('modal-pt-capacity')?.checked ?? true,
      is_per_night: document.getElementById('modal-pt-per-night')?.checked ?? true,
      sort_order: parseInt(document.getElementById('modal-pt-sort')?.value || 0),
    };
  }

  async function savePersonType() {
    const data = collectPersonTypeData();
    if (!data.name.trim()) {
      showNotification('Name is required', 'error');
      return;
    }
    try {
      if (modalEntityId) {
        await postJSON(`${BASE}/booking-person-type/${modalEntityId}/update/`, data);
        showNotification('Person type updated', 'success');
      } else {
        await postJSON(`${BASE}/product/${PRODUCT_ID}/booking-person-types/create/`, data);
        showNotification('Person type created', 'success');
      }
      hideModal();
      loadPersonTypes();
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  async function deletePersonType(id) {
    if (
      !(await AdminModal.confirm({
        message: 'Delete this person type?',
        danger: true,
        confirmText: 'Delete',
      }))
    )
      return;
    try {
      await postJSON(`${BASE}/booking-person-type/${id}/delete/`, {});
      showNotification('Person type deleted', 'success');
      loadPersonTypes();
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  // ===================================================================
  // AVAILABILITY RULES (Card list)
  // ===================================================================

  async function loadAvailabilityRules() {
    try {
      const data = await fetchJSON(
        `${BASE}/product/${PRODUCT_ID}/booking-availability-rules/list/`
      );
      availableResources = data.resources || [];
      // Exclude unavailable rules — they appear in the Blackout Periods section
      const nonBlackout = (data.rules || []).filter(r => r.rule_type !== 'unavailable');
      renderAvailabilityRuleList(nonBlackout);
      const badge = document.getElementById('booking-availability-rule-count');
      if (badge) badge.textContent = nonBlackout.length;
    } catch (e) {
      const el = document.getElementById('booking-availability-rule-list');
      if (el)
        el.innerHTML =
          '<div class="booking-list-loading" style="color:var(--error-color);"><i class="fas fa-exclamation-circle"></i> Failed to load</div>';
    }
  }

  function renderAvailabilityRuleList(rules) {
    const el = document.getElementById('booking-availability-rule-list');
    if (!el) return;

    if (!rules.length) {
      el.innerHTML =
        '<div class="booking-empty-state"><i class="fas fa-calendar-alt"></i><p>No availability rules yet. Add rules to control when bookings are available.</p></div>';
      return;
    }

    el.innerHTML = rules
      .map(r => {
        const badgeClass =
          r.rule_type === 'available'
            ? 'booking-card-row__badge--available'
            : r.rule_type === 'unavailable'
              ? 'booking-card-row__badge--unavailable'
              : 'booking-card-row__badge--custom-cost';
        let desc = r.scope_display;
        if (r.resource_name) desc += ` &middot; ${escapeHtml(r.resource_name)}`;
        if (r.start_date) desc += ` &middot; ${r.start_date}`;
        if (r.end_date) desc += ` to ${r.end_date}`;
        return `
            <div class="booking-card-row" data-id="${r.id}">
                <div class="booking-card-row__icon"><i class="fas fa-calendar-check"></i></div>
                <div class="booking-card-row__info">
                    <div class="booking-card-row__name">${escapeHtml(r.rule_type_display)} &mdash; ${escapeHtml(r.scope_display)}</div>
                    <div class="booking-card-row__desc">Priority: ${r.priority}${r.resource_name ? ' &middot; ' + escapeHtml(r.resource_name) : ''}${r.start_date ? ' &middot; ' + r.start_date : ''}${r.end_date ? ' to ' + r.end_date : ''}</div>
                </div>
                <div class="booking-card-row__badges">
                    <span class="booking-card-row__badge ${badgeClass}">${escapeHtml(r.rule_type_display)}</span>
                </div>
                <div class="booking-card-row__actions">
                    <button type="button" class="booking-card-row__action" data-action="edit" title="Edit"><i class="fas fa-pencil-alt"></i></button>
                    <button type="button" class="booking-card-row__action booking-card-row__action--danger" data-action="delete" title="Delete"><i class="fas fa-trash-alt"></i></button>
                </div>
            </div>`;
      })
      .join('');
  }

  function openAvailabilityRuleModal(id) {
    modalEntityType = 'availability_rule';
    modalEntityId = id;
    modalTitle.textContent = id ? 'Edit Availability Rule' : 'Add Availability Rule';
    modalSaveText.textContent = id ? 'Update Rule' : 'Save Rule';

    if (id) {
      modalBody.innerHTML =
        '<div class="booking-list-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
      showModal();
      fetchJSON(`${BASE}/booking-availability-rule/${id}/detail/`)
        .then(data => {
          renderAvailabilityRuleForm(data.rule);
        })
        .catch(e => {
          modalBody.innerHTML = `<p style="color:var(--error-color);">Failed to load: ${escapeHtml(e.message)}</p>`;
        });
    } else {
      renderAvailabilityRuleForm(null);
      showModal();
    }
  }

  function renderAvailabilityRuleForm(rule) {
    const d = rule || {};
    const resourceOptions = availableResources
      .map(
        r =>
          `<option value="${r.id}" ${d.resource_id === r.id ? 'selected' : ''}>${escapeHtml(r.name)}</option>`
      )
      .join('');

    const daysChecked = d.days_of_week || [];

    modalBody.innerHTML = `
            <div class="booking-modal-section">
                <h4><i class="fas fa-calendar-alt"></i> Rule Settings</h4>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Rule Type <span class="required">*</span></label>
                        <select id="modal-ar-rule_type">
                            <option value="available" ${(d.rule_type || 'available') === 'available' ? 'selected' : ''}>Available</option>
                            <option value="unavailable" ${d.rule_type === 'unavailable' ? 'selected' : ''}>Unavailable</option>
                            <option value="custom_cost" ${d.rule_type === 'custom_cost' ? 'selected' : ''}>Custom Cost</option>
                        </select>
                    </div>
                    <div class="booking-modal-field">
                        <label>Scope <span class="required">*</span></label>
                        <select id="modal-ar-scope">
                            <option value="all_dates" ${(d.scope || 'all_dates') === 'all_dates' ? 'selected' : ''}>All Dates</option>
                            <option value="date_range" ${d.scope === 'date_range' ? 'selected' : ''}>Date Range</option>
                            <option value="days_of_week" ${d.scope === 'days_of_week' ? 'selected' : ''}>Days of Week</option>
                            <option value="time_range" ${d.scope === 'time_range' ? 'selected' : ''}>Time Range</option>
                            <option value="specific_dates" ${d.scope === 'specific_dates' ? 'selected' : ''}>Specific Dates</option>
                        </select>
                    </div>
                </div>
                <div class="booking-modal-field">
                    <label>Resource (optional)</label>
                    <select id="modal-ar-resource">
                        <option value="">All resources</option>
                        ${resourceOptions}
                    </select>
                    <span class="booking-modal-help">Leave empty to apply to all resources</span>
                </div>
                <div class="booking-modal-field">
                    <label>Priority</label>
                    <input type="number" id="modal-ar-priority" value="${d.priority || 10}" min="0">
                    <span class="booking-modal-help">Higher priority overrides lower</span>
                </div>
            </div>
            <div class="booking-modal-section">
                <h4><i class="fas fa-clock"></i> Date / Time Range</h4>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Start Date</label>
                        <input type="date" id="modal-ar-start_date" value="${d.start_date || ''}">
                    </div>
                    <div class="booking-modal-field">
                        <label>End Date</label>
                        <input type="date" id="modal-ar-end_date" value="${d.end_date || ''}">
                    </div>
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Start Time</label>
                        <input type="time" id="modal-ar-start_time" value="${d.start_time || ''}">
                    </div>
                    <div class="booking-modal-field">
                        <label>End Time</label>
                        <input type="time" id="modal-ar-end_time" value="${d.end_time || ''}">
                    </div>
                </div>
                <div class="booking-modal-field">
                    <label>Days of Week</label>
                    <div class="booking-days-picker" id="modal-ar-days">
                        ${DAY_NAMES.map((name, i) => `<label class="${daysChecked.includes(i) ? 'active' : ''}"><input type="checkbox" value="${i}" ${daysChecked.includes(i) ? 'checked' : ''}><span>${name}</span></label>`).join('')}
                    </div>
                </div>
            </div>
            <div class="booking-modal-section">
                <h4><i class="fas fa-money-bill-wave"></i> Cost Overrides</h4>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Cost Override</label>
                        <input type="number" id="modal-ar-cost_override" value="${d.cost_override || ''}" step="0.01" placeholder="Replace base cost">
                    </div>
                    <div class="booking-modal-field">
                        <label>Cost Adjustment</label>
                        <input type="number" id="modal-ar-cost_adjustment" value="${d.cost_adjustment || ''}" step="0.01" placeholder="Add/subtract from base">
                    </div>
                </div>
                <div class="booking-modal-field">
                    <label>Adjustment Type</label>
                    <select id="modal-ar-cost_adjustment_type">
                        <option value="flat" ${(d.cost_adjustment_type || 'flat') === 'flat' ? 'selected' : ''}>Flat Amount</option>
                        <option value="percentage" ${d.cost_adjustment_type === 'percentage' ? 'selected' : ''}>Percentage (%)</option>
                    </select>
                    <span class="booking-modal-help">How the cost adjustment value is applied</span>
                </div>
            </div>
            <div class="booking-modal-section">
                <h4><i class="fas fa-bed"></i> Accommodation Options</h4>
                <div class="booking-modal-field">
                    <label>Min Stay Override (nights)</label>
                    <input type="number" id="modal-ar-min_stay_override" value="${d.min_stay_override || ''}" min="1" placeholder="Override min stay for matching dates">
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Length-of-Stay Min Nights</label>
                        <input type="number" id="modal-ar-los_min" value="${d.length_of_stay_min || ''}" min="1" placeholder="e.g. 7">
                    </div>
                    <div class="booking-modal-field">
                        <label>LOS Discount %</label>
                        <input type="number" id="modal-ar-los_discount" value="${d.length_of_stay_discount_percent || ''}" step="0.01" min="0" max="100" placeholder="e.g. 10">
                        <span class="booking-modal-help">Discount for stays >= min nights</span>
                    </div>
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Lead Time Min (days)</label>
                        <input type="number" id="modal-ar-lead_min" value="${d.lead_time_min_days || ''}" min="0" placeholder="Early-bird min days">
                    </div>
                    <div class="booking-modal-field">
                        <label>Lead Time Max (days)</label>
                        <input type="number" id="modal-ar-lead_max" value="${d.lead_time_max_days || ''}" min="0" placeholder="Last-minute max days">
                    </div>
                </div>
            </div>`;

    // Bind day picker toggle
    modalBody.querySelectorAll('.booking-days-picker label').forEach(label => {
      label.addEventListener('click', function (e) {
        if (e.target.tagName === 'INPUT') return;
        const cb = this.querySelector('input[type="checkbox"]');
        cb.checked = !cb.checked;
        this.classList.toggle('active', cb.checked);
        e.preventDefault();
      });
    });
  }

  function collectAvailabilityRuleData() {
    const daysEls = document.querySelectorAll('#modal-ar-days input[type="checkbox"]:checked');
    const days = Array.from(daysEls).map(cb => parseInt(cb.value));

    return {
      rule_type: document.getElementById('modal-ar-rule_type')?.value || 'available',
      scope: document.getElementById('modal-ar-scope')?.value || 'all_dates',
      resource_id: document.getElementById('modal-ar-resource')?.value || null,
      priority: parseInt(document.getElementById('modal-ar-priority')?.value || 10),
      start_date: document.getElementById('modal-ar-start_date')?.value || '',
      end_date: document.getElementById('modal-ar-end_date')?.value || '',
      start_time: document.getElementById('modal-ar-start_time')?.value || '',
      end_time: document.getElementById('modal-ar-end_time')?.value || '',
      days_of_week: days,
      cost_override: document.getElementById('modal-ar-cost_override')?.value || '',
      cost_adjustment: document.getElementById('modal-ar-cost_adjustment')?.value || '',
      cost_adjustment_type:
        document.getElementById('modal-ar-cost_adjustment_type')?.value || 'flat',
      min_stay_override: document.getElementById('modal-ar-min_stay_override')?.value || '',
      length_of_stay_min: document.getElementById('modal-ar-los_min')?.value || '',
      length_of_stay_discount_percent:
        document.getElementById('modal-ar-los_discount')?.value || '',
      lead_time_min_days: document.getElementById('modal-ar-lead_min')?.value || '',
      lead_time_max_days: document.getElementById('modal-ar-lead_max')?.value || '',
    };
  }

  async function saveAvailabilityRule() {
    const data = collectAvailabilityRuleData();
    try {
      if (modalEntityId) {
        await postJSON(`${BASE}/booking-availability-rule/${modalEntityId}/update/`, data);
        showNotification('Rule updated', 'success');
      } else {
        await postJSON(`${BASE}/product/${PRODUCT_ID}/booking-availability-rules/create/`, data);
        showNotification('Rule created', 'success');
      }
      hideModal();
      loadAvailabilityRules();
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  async function deleteAvailabilityRule(id) {
    if (
      !(await AdminModal.confirm({
        message: 'Delete this availability rule?',
        danger: true,
        confirmText: 'Delete',
      }))
    )
      return;
    try {
      await postJSON(`${BASE}/booking-availability-rule/${id}/delete/`, {});
      showNotification('Rule deleted', 'success');
      loadAvailabilityRules();
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  // ===================================================================
  // BLACKOUT PERIODS (Filtered view of unavailable rules)
  // ===================================================================

  async function loadBlackoutPeriods() {
    try {
      const data = await fetchJSON(
        `${BASE}/product/${PRODUCT_ID}/booking-availability-rules/list/?rule_type=unavailable`
      );
      renderBlackoutList(data.rules || []);
      renderBlackoutCalendar(data.rules || []);
      const badge = document.getElementById('booking-blackout-count');
      if (badge) badge.textContent = data.count || 0;
    } catch (e) {
      const el = document.getElementById('booking-blackout-list');
      if (el)
        el.innerHTML =
          '<div class="booking-list-loading" style="color:var(--error-color);"><i class="fas fa-exclamation-circle"></i> Failed to load</div>';
    }
  }

  function renderBlackoutList(rules) {
    const el = document.getElementById('booking-blackout-list');
    if (!el) return;

    if (!rules.length) {
      el.innerHTML =
        '<div class="booking-empty-state"><i class="fas fa-ban"></i><p>No blackout periods. Use "Block Dates" to prevent bookings on specific dates.</p></div>';
      return;
    }

    el.innerHTML = rules
      .map(r => {
        let desc = r.scope_display;
        if (r.resource_name) desc += ` &middot; ${escapeHtml(r.resource_name)}`;
        if (r.start_date) desc += ` &middot; ${r.start_date}`;
        if (r.end_date) desc += ` to ${r.end_date}`;
        if (r.days_of_week && r.days_of_week.length) {
          desc += ` &middot; ${r.days_of_week.map(d => DAY_NAMES[d] || '?').join(', ')}`;
        }
        return `
            <div class="booking-card-row" data-id="${r.id}">
                <div class="booking-card-row__icon"><i class="fas fa-ban" style="color:var(--error-color,#dc2626);"></i></div>
                <div class="booking-card-row__info">
                    <div class="booking-card-row__name">${escapeHtml(r.scope_display)}</div>
                    <div class="booking-card-row__desc">${desc}</div>
                </div>
                <div class="booking-card-row__badges">
                    <span class="booking-card-row__badge booking-card-row__badge--unavailable">Blocked</span>
                </div>
                <div class="booking-card-row__actions">
                    <button type="button" class="booking-card-row__action" data-action="edit" title="Edit"><i class="fas fa-pencil-alt"></i></button>
                    <button type="button" class="booking-card-row__action booking-card-row__action--danger" data-action="delete" title="Delete"><i class="fas fa-trash-alt"></i></button>
                </div>
            </div>`;
      })
      .join('');
  }

  function renderBlackoutCalendar(rules) {
    const container = document.getElementById('booking-blackout-calendar');
    if (!container) return;

    // Collect all blocked dates from rules
    const blockedDates = new Set();
    const blockedDays = new Set(); // days of week

    for (const r of rules) {
      if (r.scope === 'date_range' && r.start_date && r.end_date) {
        const d = new Date(r.start_date + 'T00:00:00');
        const end = new Date(r.end_date + 'T00:00:00');
        while (d <= end) {
          blockedDates.add(fmtDate(d));
          d.setDate(d.getDate() + 1);
        }
      } else if (r.scope === 'specific_dates' && r.specific_dates) {
        r.specific_dates.forEach(ds => blockedDates.add(ds));
      } else if (r.scope === 'days_of_week' && r.days_of_week) {
        r.days_of_week.forEach(d => blockedDays.add(d));
      } else if (r.scope === 'all_dates') {
        // All dates blocked — show indicator
        container.innerHTML =
          '<p style="padding:0.5rem;color:var(--error-color,#dc2626);font-size:0.875rem;"><i class="fas fa-exclamation-triangle"></i> All dates are blocked</p>';
        return;
      }
    }

    // Render 2-month mini calendar
    const now = new Date();
    let html = '';
    for (let m = 0; m < 2; m++) {
      const monthDate = new Date(now.getFullYear(), now.getMonth() + m, 1);
      const year = monthDate.getFullYear();
      const month = monthDate.getMonth();
      const monthName = monthDate.toLocaleDateString(undefined, {
        month: 'short',
        year: 'numeric',
      });
      const firstDow = (monthDate.getDay() + 6) % 7;
      const totalDays = new Date(year, month + 1, 0).getDate();

      html += '<div class="booking-blackout-calendar__month">';
      html += `<div class="booking-blackout-calendar__title">${monthName}</div>`;
      html += '<div class="booking-blackout-calendar__daynames">';
      for (const dn of DAY_NAMES) html += `<span>${dn.charAt(0)}</span>`;
      html += '</div><div class="booking-blackout-calendar__grid">';
      for (let i = 0; i < firstDow; i++)
        html += '<span class="booking-blackout-calendar__day--empty"></span>';
      for (let d = 1; d <= totalDays; d++) {
        const ds = fmtDate(new Date(year, month, d));
        const dayOfWeek = (new Date(year, month, d).getDay() + 6) % 7;
        const isBlocked = blockedDates.has(ds) || blockedDays.has(dayOfWeek);
        html += `<span class="booking-blackout-calendar__day${isBlocked ? ' booking-blackout-calendar__day--blocked' : ''}">${d}</span>`;
      }
      html += '</div></div>';
    }

    container.innerHTML = html;
  }

  function fmtDate(d) {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  }

  function openBlackoutModal(id) {
    modalEntityType = 'blackout';
    modalEntityId = id;
    modalTitle.textContent = id ? 'Edit Blackout Period' : 'Block Dates';
    modalSaveText.textContent = id ? 'Update' : 'Save';

    if (id) {
      modalBody.innerHTML =
        '<div class="booking-list-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
      showModal();
      fetchJSON(`${BASE}/booking-availability-rule/${id}/detail/`)
        .then(data => {
          renderBlackoutForm(data.rule);
        })
        .catch(e => {
          modalBody.innerHTML = `<p style="color:var(--error-color);">Failed to load: ${escapeHtml(e.message)}</p>`;
        });
    } else {
      renderBlackoutForm(null);
      showModal();
    }
  }

  function renderBlackoutForm(rule) {
    const d = rule || {};
    const resourceOptions = availableResources
      .map(
        r =>
          `<option value="${r.id}" ${d.resource_id === r.id ? 'selected' : ''}>${escapeHtml(r.name)}</option>`
      )
      .join('');

    modalBody.innerHTML = `
            <div class="booking-modal-section">
                <h4><i class="fas fa-ban"></i> Blackout Settings</h4>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Scope <span class="required">*</span></label>
                        <select id="modal-bo-scope">
                            <option value="date_range" ${(d.scope || 'date_range') === 'date_range' ? 'selected' : ''}>Date Range</option>
                            <option value="days_of_week" ${d.scope === 'days_of_week' ? 'selected' : ''}>Days of Week</option>
                            <option value="specific_dates" ${d.scope === 'specific_dates' ? 'selected' : ''}>Specific Dates</option>
                        </select>
                    </div>
                    <div class="booking-modal-field">
                        <label>Resource (optional)</label>
                        <select id="modal-bo-resource">
                            <option value="">All resources</option>
                            ${resourceOptions}
                        </select>
                    </div>
                </div>
                <div class="booking-modal-row" id="modal-bo-daterange-row">
                    <div class="booking-modal-field">
                        <label>Start Date</label>
                        <input type="date" id="modal-bo-start_date" value="${d.start_date || ''}">
                    </div>
                    <div class="booking-modal-field">
                        <label>End Date</label>
                        <input type="date" id="modal-bo-end_date" value="${d.end_date || ''}">
                    </div>
                </div>
                <div class="booking-modal-row" id="modal-bo-dow-row" style="display:none;">
                    <div class="booking-modal-field" style="flex:1;">
                        <label>Days of Week</label>
                        <div class="booking-dow-picker">
                            ${DAY_NAMES.map(
                              (name, i) =>
                                `<label class="booking-dow-picker__item">
                                    <input type="checkbox" value="${i}" ${(d.days_of_week || []).includes(i) ? 'checked' : ''}>
                                    <span>${name}</span>
                                </label>`
                            ).join('')}
                        </div>
                    </div>
                </div>
                <div class="booking-modal-field" id="modal-bo-specific-row" style="display:none;">
                    <label>Specific Dates (comma-separated YYYY-MM-DD)</label>
                    <input type="text" id="modal-bo-specific_dates" value="${(d.specific_dates || []).join(', ')}" placeholder="2026-12-25, 2026-12-31">
                </div>
                <div class="booking-modal-field">
                    <label>Priority</label>
                    <input type="number" id="modal-bo-priority" value="${d.priority || 50}" min="1" max="100">
                    <p class="help-text">Higher priority overrides lower. Default: 50.</p>
                </div>
            </div>
        `;

    // Toggle scope fields
    const scopeSelect = document.getElementById('modal-bo-scope');
    function toggleScopeFields() {
      const scope = scopeSelect.value;
      document.getElementById('modal-bo-daterange-row').style.display =
        scope === 'date_range' ? '' : 'none';
      document.getElementById('modal-bo-dow-row').style.display =
        scope === 'days_of_week' ? '' : 'none';
      document.getElementById('modal-bo-specific-row').style.display =
        scope === 'specific_dates' ? '' : 'none';
    }
    scopeSelect.addEventListener('change', toggleScopeFields);
    toggleScopeFields();
  }

  function collectBlackoutData() {
    const scope = document.getElementById('modal-bo-scope')?.value || 'date_range';
    const data = {
      rule_type: 'unavailable',
      scope: scope,
      resource_id: document.getElementById('modal-bo-resource')?.value || '',
      priority: document.getElementById('modal-bo-priority')?.value || '50',
    };
    if (scope === 'date_range') {
      data.start_date = document.getElementById('modal-bo-start_date')?.value || '';
      data.end_date = document.getElementById('modal-bo-end_date')?.value || '';
    } else if (scope === 'days_of_week') {
      const checked = [];
      document.querySelectorAll('#modal-bo-dow-row input[type="checkbox"]:checked').forEach(cb => {
        checked.push(parseInt(cb.value));
      });
      data.days_of_week = checked;
    } else if (scope === 'specific_dates') {
      const raw = document.getElementById('modal-bo-specific_dates')?.value || '';
      data.specific_dates = raw
        .split(',')
        .map(s => s.trim())
        .filter(Boolean);
    }
    return data;
  }

  async function saveBlackout() {
    const data = collectBlackoutData();
    try {
      if (modalEntityId) {
        await postJSON(`${BASE}/booking-availability-rule/${modalEntityId}/update/`, data);
        showNotification('Blackout period updated', 'success');
      } else {
        await postJSON(`${BASE}/product/${PRODUCT_ID}/booking-availability-rules/create/`, data);
        showNotification('Blackout period created', 'success');
      }
      hideModal();
      loadBlackoutPeriods();
      loadAvailabilityRules(); // Refresh the full list too
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  async function deleteBlackout(id) {
    if (
      !(await AdminModal.confirm({
        message: 'Remove this blackout period?',
        danger: true,
        confirmText: 'Remove',
      }))
    )
      return;
    try {
      await postJSON(`${BASE}/booking-availability-rule/${id}/delete/`, {});
      showNotification('Blackout period removed', 'success');
      loadBlackoutPeriods();
      loadAvailabilityRules();
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  // ===================================================================
  // RECURRENCE RULES (Card list)
  // ===================================================================

  async function loadRecurrenceRules() {
    try {
      const data = await fetchJSON(`${BASE}/product/${PRODUCT_ID}/booking-recurrence-rules/list/`);
      renderRecurrenceRuleList(data.rules || []);
      const badge = document.getElementById('booking-recurrence-rule-count');
      if (badge) badge.textContent = data.count || 0;
    } catch (e) {
      const el = document.getElementById('booking-recurrence-rule-list');
      if (el)
        el.innerHTML =
          '<div class="booking-list-loading" style="color:var(--error-color);"><i class="fas fa-exclamation-circle"></i> Failed to load</div>';
    }
  }

  function renderRecurrenceRuleList(rules) {
    const el = document.getElementById('booking-recurrence-rule-list');
    if (!el) return;

    if (!rules.length) {
      el.innerHTML =
        '<div class="booking-empty-state"><i class="fas fa-redo"></i><p>No recurrence rules yet. Add recurring schedules for repeating bookings.</p></div>';
      return;
    }

    el.innerHTML = rules
      .map(r => {
        let desc = `${r.start_time} - ${r.end_time}`;
        if (r.day_of_week !== null && r.day_of_week !== undefined)
          desc += ` &middot; ${DAY_NAMES[r.day_of_week] || '?'}`;
        if (r.start_date) desc += ` &middot; From ${r.start_date}`;
        if (r.end_date) desc += ` to ${r.end_date}`;
        return `
            <div class="booking-card-row" data-id="${r.id}">
                <div class="booking-card-row__icon"><i class="fas fa-sync-alt"></i></div>
                <div class="booking-card-row__info">
                    <div class="booking-card-row__name">${escapeHtml(r.frequency_display)}</div>
                    <div class="booking-card-row__desc">${desc} &middot; Auto-create: ${r.auto_create_days_ahead} days</div>
                </div>
                <div class="booking-card-row__badges">
                    ${
                      r.is_active
                        ? '<span class="booking-card-row__badge booking-card-row__badge--active">Active</span>'
                        : '<span class="booking-card-row__badge booking-card-row__badge--inactive">Inactive</span>'
                    }
                </div>
                <div class="booking-card-row__actions">
                    <button type="button" class="booking-card-row__action" data-action="edit" title="Edit"><i class="fas fa-pencil-alt"></i></button>
                    <button type="button" class="booking-card-row__action booking-card-row__action--danger" data-action="delete" title="Delete"><i class="fas fa-trash-alt"></i></button>
                </div>
            </div>`;
      })
      .join('');
  }

  function openRecurrenceRuleModal(id) {
    modalEntityType = 'recurrence_rule';
    modalEntityId = id;
    modalTitle.textContent = id ? 'Edit Recurrence Rule' : 'Add Recurrence Rule';
    modalSaveText.textContent = id ? 'Update' : 'Save';

    if (id) {
      modalBody.innerHTML =
        '<div class="booking-list-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
      showModal();
      fetchJSON(`${BASE}/booking-recurrence-rule/${id}/detail/`)
        .then(data => {
          renderRecurrenceRuleForm(data.rule);
        })
        .catch(e => {
          modalBody.innerHTML = `<p style="color:var(--error-color);">Failed to load: ${escapeHtml(e.message)}</p>`;
        });
    } else {
      renderRecurrenceRuleForm(null);
      showModal();
    }
  }

  function renderRecurrenceRuleForm(rule) {
    const d = rule || {};
    modalBody.innerHTML = `
            <div class="booking-modal-section">
                <h4><i class="fas fa-redo"></i> Recurrence Settings</h4>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Frequency <span class="required">*</span></label>
                        <select id="modal-rr-frequency">
                            <option value="daily" ${d.frequency === 'daily' ? 'selected' : ''}>Daily</option>
                            <option value="weekly" ${(d.frequency || 'weekly') === 'weekly' ? 'selected' : ''}>Weekly</option>
                            <option value="biweekly" ${d.frequency === 'biweekly' ? 'selected' : ''}>Every Two Weeks</option>
                            <option value="monthly" ${d.frequency === 'monthly' ? 'selected' : ''}>Monthly</option>
                        </select>
                    </div>
                    <div class="booking-modal-field">
                        <label>Day of Week</label>
                        <select id="modal-rr-day_of_week">
                            <option value="">N/A</option>
                            ${DAY_NAMES.map((name, i) => `<option value="${i}" ${d.day_of_week === i ? 'selected' : ''}>${name}</option>`).join('')}
                        </select>
                        <span class="booking-modal-help">For weekly/biweekly</span>
                    </div>
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Day of Month</label>
                        <input type="number" id="modal-rr-day_of_month" value="${d.day_of_month || ''}" min="1" max="31" placeholder="1-31">
                        <span class="booking-modal-help">For monthly frequency</span>
                    </div>
                    <div class="booking-modal-field">
                        <label>Auto-Create Days Ahead</label>
                        <input type="number" id="modal-rr-auto_create" value="${d.auto_create_days_ahead || 90}" min="1">
                    </div>
                </div>
            </div>
            <div class="booking-modal-section">
                <h4><i class="fas fa-clock"></i> Time & Date Range</h4>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Start Time <span class="required">*</span></label>
                        <input type="time" id="modal-rr-start_time" value="${d.start_time || '09:00'}">
                    </div>
                    <div class="booking-modal-field">
                        <label>End Time <span class="required">*</span></label>
                        <input type="time" id="modal-rr-end_time" value="${d.end_time || '17:00'}">
                    </div>
                </div>
                <div class="booking-modal-row">
                    <div class="booking-modal-field">
                        <label>Start Date <span class="required">*</span></label>
                        <input type="date" id="modal-rr-start_date" value="${d.start_date || ''}">
                    </div>
                    <div class="booking-modal-field">
                        <label>End Date</label>
                        <input type="date" id="modal-rr-end_date" value="${d.end_date || ''}" placeholder="Leave empty for ongoing">
                    </div>
                </div>
                <div class="booking-modal-field--checkbox">
                    <label><input type="checkbox" id="modal-rr-active" ${d.is_active !== false ? 'checked' : ''}> Active</label>
                </div>
            </div>`;
  }

  function collectRecurrenceRuleData() {
    const dayOfWeek = document.getElementById('modal-rr-day_of_week')?.value;
    const dayOfMonth = document.getElementById('modal-rr-day_of_month')?.value;
    return {
      frequency: document.getElementById('modal-rr-frequency')?.value || 'weekly',
      day_of_week: dayOfWeek !== '' ? dayOfWeek : null,
      day_of_month: dayOfMonth !== '' ? dayOfMonth : null,
      start_time: document.getElementById('modal-rr-start_time')?.value || '09:00',
      end_time: document.getElementById('modal-rr-end_time')?.value || '17:00',
      start_date: document.getElementById('modal-rr-start_date')?.value || '',
      end_date: document.getElementById('modal-rr-end_date')?.value || '',
      auto_create_days_ahead: parseInt(
        document.getElementById('modal-rr-auto_create')?.value || 90
      ),
      is_active: document.getElementById('modal-rr-active')?.checked ?? true,
    };
  }

  async function saveRecurrenceRule() {
    const data = collectRecurrenceRuleData();
    if (!data.start_date) {
      showNotification('Start date is required', 'error');
      return;
    }
    try {
      if (modalEntityId) {
        await postJSON(`${BASE}/booking-recurrence-rule/${modalEntityId}/update/`, data);
        showNotification('Recurrence rule updated', 'success');
      } else {
        await postJSON(`${BASE}/product/${PRODUCT_ID}/booking-recurrence-rules/create/`, data);
        showNotification('Recurrence rule created', 'success');
      }
      hideModal();
      loadRecurrenceRules();
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  async function deleteRecurrenceRule(id) {
    if (
      !(await AdminModal.confirm({
        message: 'Delete this recurrence rule?',
        danger: true,
        confirmText: 'Delete',
      }))
    )
      return;
    try {
      await postJSON(`${BASE}/booking-recurrence-rule/${id}/delete/`, {});
      showNotification('Recurrence rule deleted', 'success');
      loadRecurrenceRules();
    } catch (e) {
      showNotification('Error: ' + e.message, 'error');
    }
  }

  // ===================================================================
  // MODAL MANAGEMENT
  // ===================================================================

  function showModal() {
    if (modalOverlay) modalOverlay.style.display = 'flex';
  }

  function hideModal() {
    if (modalOverlay) modalOverlay.style.display = 'none';
    modalEntityType = null;
    modalEntityId = null;
  }

  function handleModalSave() {
    switch (modalEntityType) {
      case 'resource':
        saveResource();
        break;
      case 'person_type':
        savePersonType();
        break;
      case 'availability_rule':
        saveAvailabilityRule();
        break;
      case 'recurrence_rule':
        saveRecurrenceRule();
        break;
      case 'blackout':
        saveBlackout();
        break;
    }
  }

  // ===================================================================
  // INITIALIZATION
  // ===================================================================

  function init() {
    const panel = document.getElementById('panel-booking');
    if (!panel) return;

    // Check product type
    const typeSelect = document.getElementById('id_product_type');
    if (typeSelect && typeSelect.value !== 'booking') return;

    // Cache modal DOM refs
    modalOverlay = document.getElementById('booking-modal-overlay');
    modalTitle = document.getElementById('booking-modal-title');
    modalBody = document.getElementById('booking-modal-body');
    modalSaveBtn = document.getElementById('booking-modal-save');
    modalSaveText = document.getElementById('booking-modal-save-text');

    // Modal event binding
    if (modalSaveBtn) modalSaveBtn.addEventListener('click', handleModalSave);
    const cancelBtn = document.getElementById('booking-modal-cancel');
    if (cancelBtn) cancelBtn.addEventListener('click', hideModal);
    const closeBtn = document.getElementById('booking-modal-close-btn');
    if (closeBtn) closeBtn.addEventListener('click', hideModal);
    if (modalOverlay) {
      modalOverlay.addEventListener('click', function (e) {
        if (e.target === modalOverlay) hideModal();
      });
    }

    // Escape key to close modal
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modalOverlay && modalOverlay.style.display === 'flex') {
        hideModal();
      }
    });

    // Add buttons
    const addResourceBtn = document.getElementById('add-booking-resource-btn');
    if (addResourceBtn) addResourceBtn.addEventListener('click', () => openResourceModal(null));

    const addPersonTypeBtn = document.getElementById('add-booking-person-type-btn');
    if (addPersonTypeBtn)
      addPersonTypeBtn.addEventListener('click', () => openPersonTypeModal(null));

    const addAvailRuleBtn = document.getElementById('add-booking-availability-rule-btn');
    if (addAvailRuleBtn)
      addAvailRuleBtn.addEventListener('click', () => openAvailabilityRuleModal(null));

    const addRecurrenceBtn = document.getElementById('add-booking-recurrence-rule-btn');
    if (addRecurrenceBtn)
      addRecurrenceBtn.addEventListener('click', () => openRecurrenceRuleModal(null));

    const addBlackoutBtn = document.getElementById('add-booking-blackout-btn');
    if (addBlackoutBtn) addBlackoutBtn.addEventListener('click', () => openBlackoutModal(null));

    // Delegated card row actions (CSP-compliant: no inline onclick)
    [
      { listId: 'booking-resource-list', editFn: openResourceModal, deleteFn: deleteResource },
      {
        listId: 'booking-person-type-list',
        editFn: openPersonTypeModal,
        deleteFn: deletePersonType,
      },
      {
        listId: 'booking-availability-rule-list',
        editFn: openAvailabilityRuleModal,
        deleteFn: deleteAvailabilityRule,
      },
      {
        listId: 'booking-recurrence-rule-list',
        editFn: openRecurrenceRuleModal,
        deleteFn: deleteRecurrenceRule,
      },
      { listId: 'booking-blackout-list', editFn: openBlackoutModal, deleteFn: deleteBlackout },
    ].forEach(({ listId, editFn, deleteFn }) => {
      const list = document.getElementById(listId);
      if (!list) return;
      list.addEventListener('click', function (e) {
        const btn = e.target.closest('[data-action]');
        if (!btn) return;
        const id = parseInt(btn.closest('.booking-card-row').dataset.id);
        if (btn.dataset.action === 'edit') editFn(id);
        if (btn.dataset.action === 'delete') deleteFn(id);
      });
    });

    // Zero out Django inline management forms
    panel.querySelectorAll('input[name$="-TOTAL_FORMS"]').forEach(input => {
      input.value = '0';
    });
    panel.querySelectorAll('input[name$="-INITIAL_FORMS"]').forEach(input => {
      input.value = '0';
    });

    // Load all data
    loadBookingConfig();
    loadResources();
    loadPersonTypes();
    loadBlackoutPeriods();
    loadAvailabilityRules();
    loadRecurrenceRules();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
