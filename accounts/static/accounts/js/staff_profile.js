/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Staff Profile Dashboard - Tab switching, inline edits, session management.
 * Uses AdminUtils.getCsrfToken() from globally loaded admin-utils.js.
 */
(function () {
    'use strict';

    /* ---- Tab switching handled by global AdminTabs utility ---- */

    /* ---- Toast notifications ---- */
    function showToast(message, type) {
        AdminModal.toast(message, type || 'info');
    }

    /* ---- Helper: POST with CSRF ---- */
    function postJSON(url, data) {
        var csrfToken = '';
        if (typeof AdminUtils !== 'undefined' && AdminUtils.getCsrfToken) {
            csrfToken = AdminUtils.getCsrfToken();
        } else {
            var meta = document.querySelector('[name=csrfmiddlewaretoken]');
            csrfToken = meta ? meta.value : '';
        }

        return fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: JSON.stringify(data),
        }).then(function (res) {
            return res.json().then(function (json) {
                json._status = res.status;
                return json;
            });
        });
    }

    /* ---- Inline Name Edit ---- */
    function initNameEdit() {
        var editBtn = document.getElementById('edit-name-btn');
        var form = document.getElementById('name-edit-form');
        var saveBtn = document.getElementById('name-save-btn');
        var cancelBtn = document.getElementById('name-cancel-btn');
        var display = document.getElementById('name-display');

        if (!editBtn || !form) return;

        editBtn.addEventListener('click', function () {
            form.classList.add('visible');
            editBtn.style.display = 'none';
            form.querySelector('input').focus();
        });

        cancelBtn.addEventListener('click', function () {
            form.classList.remove('visible');
            editBtn.style.display = '';
        });

        saveBtn.addEventListener('click', function () {
            var firstName = document.getElementById('edit-first-name').value.trim();
            var lastName = document.getElementById('edit-last-name').value.trim();

            if (!firstName && !lastName) {
                showToast('Please enter a name.', 'error');
                return;
            }

            postJSON(form.dataset.url, {
                first_name: firstName,
                last_name: lastName,
            }).then(function (data) {
                if (data.success) {
                    display.textContent = data.full_name || (firstName + ' ' + lastName);
                    form.classList.remove('visible');
                    editBtn.style.display = '';
                    showToast('Name updated successfully.');

                    // Update initials in avatar
                    var avatar = document.querySelector('.profile-avatar');
                    if (avatar) {
                        var initials = (firstName.charAt(0) + lastName.charAt(0)).toUpperCase();
                        avatar.textContent = initials || avatar.textContent;
                    }
                } else {
                    showToast(data.error || 'Failed to update name.', 'error');
                }
            }).catch(function () {
                showToast('Network error. Please try again.', 'error');
            });
        });

        // Submit on Enter
        form.querySelectorAll('input').forEach(function (input) {
            input.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') { e.preventDefault(); saveBtn.click(); }
                if (e.key === 'Escape') { cancelBtn.click(); }
            });
        });
    }

    /* ---- Inline PIN Edit ---- */
    function initPinEdit() {
        var editBtn = document.getElementById('edit-pin-btn');
        var form = document.getElementById('pin-edit-form');
        var saveBtn = document.getElementById('pin-save-btn');
        var cancelBtn = document.getElementById('pin-cancel-btn');
        var pinDisplay = document.getElementById('pin-display');

        if (!editBtn || !form) return;

        editBtn.addEventListener('click', function () {
            form.classList.add('visible');
            editBtn.style.display = 'none';
            form.querySelector('input').focus();
        });

        cancelBtn.addEventListener('click', function () {
            form.classList.remove('visible');
            editBtn.style.display = '';
            form.querySelector('input').value = '';
        });

        saveBtn.addEventListener('click', function () {
            var pin = document.getElementById('edit-pin-input').value.trim();

            if (pin.length < 4 || pin.length > 6 || !/^\d+$/.test(pin)) {
                showToast('PIN must be 4-6 digits.', 'error');
                return;
            }

            postJSON(form.dataset.url, { pin: pin }).then(function (data) {
                if (data.success) {
                    // Update display
                    var dots = '';
                    for (var i = 0; i < pin.length; i++) {
                        dots += '<span class="pin-dot"></span>';
                    }
                    pinDisplay.innerHTML = '<span class="pin-dots">' + dots + '</span>';
                    form.classList.remove('visible');
                    editBtn.style.display = '';
                    form.querySelector('input').value = '';
                    showToast('PIN updated successfully.');
                } else {
                    showToast(data.error || 'Failed to update PIN.', 'error');
                }
            }).catch(function () {
                showToast('Network error. Please try again.', 'error');
            });
        });

        var pinInput = document.getElementById('edit-pin-input');
        if (pinInput) {
            pinInput.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') { e.preventDefault(); saveBtn.click(); }
                if (e.key === 'Escape') { cancelBtn.click(); }
            });
            // Only allow digits
            pinInput.addEventListener('input', function () {
                this.value = this.value.replace(/\D/g, '').slice(0, 6);
            });
        }
    }

    /* ---- Mobile Session Revoke ---- */
    function initSessionRevoke() {
        document.querySelectorAll('.revoke-session-btn').forEach(function (btn) {
            btn.addEventListener('click', async function (e) {
                e.preventDefault();
                if (!await AdminModal.confirm({ message: 'Remove this device? It will be signed out and its push notification registration will be removed.', danger: true, confirmText: 'Remove' })) return;

                var url = this.dataset.url;
                var item = this.closest('.session-item');

                postJSON(url, {}).then(function (data) {
                    if (data.success) {
                        if (item) {
                            item.style.opacity = '0';
                            item.style.transition = 'opacity 0.3s ease';
                            setTimeout(function () { item.remove(); }, 300);
                        }
                        showToast('Device removed successfully.');
                    } else {
                        showToast(data.error || 'Failed to revoke session.', 'error');
                    }
                }).catch(function () {
                    showToast('Network error. Please try again.', 'error');
                });
            });
        });
    }

    /* ---- Form Confirmation Dialogs ---- */
    function initFormConfirmations() {
        // Handle form submissions that require confirmation
        document.addEventListener('submit', async function (e) {
            var submitBtn = e.submitter;
            if (!submitBtn) return;

            var confirmMessage = submitBtn.dataset.confirm;
            if (confirmMessage) {
                e.preventDefault();
                if (await AdminModal.confirm(confirmMessage)) {
                    submitBtn.removeAttribute('data-confirm');
                    submitBtn.click();
                }
            }
        });
    }

    /* ---- Init ---- */
    document.addEventListener('DOMContentLoaded', function () {
        // Tab switching handled by global AdminTabs utility
        initNameEdit();
        initPinEdit();
        initSessionRevoke();
        initFormConfirmations();
    });
})();
