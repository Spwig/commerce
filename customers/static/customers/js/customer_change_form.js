/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Customer Change Form JavaScript
 * Handles sidebar toggle, tabs, and customer profile actions
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Customer change form JS loaded');

    // ========================================
    // Mobile Sidebar Toggle Functionality
    // ========================================
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebarClose = document.getElementById('sidebar-close');
    const sidebar = document.getElementById('customer-sidebar');
    const backdrop = document.getElementById('sidebar-backdrop');

    console.log('Sidebar elements:', { sidebarToggle, sidebarClose, sidebar, backdrop });

    function openSidebar() {
        if (sidebar && backdrop) {
            sidebar.classList.add('open');
            backdrop.classList.add('active');
            // Only prevent scrolling on mobile/tablet (below 1024px)
            if (window.innerWidth <= 1024) {
                document.body.style.overflow = 'hidden';
            }
        }
    }

    function closeSidebar() {
        if (sidebar && backdrop) {
            sidebar.classList.remove('open');
            backdrop.classList.remove('active');
            // Restore scrolling
            document.body.style.overflow = '';
        }
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', openSidebar);
    }

    if (sidebarClose) {
        sidebarClose.addEventListener('click', closeSidebar);
    }

    if (backdrop) {
        backdrop.addEventListener('click', closeSidebar);
    }

    // Close sidebar on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('open')) {
            closeSidebar();
        }
    });

    // Tab switching handled by global AdminTabs utility

    // ========================================
    // Send Account Invitation Button
    // ========================================
    const inviteBtn = document.getElementById('send-account-invitation-btn');
    if (inviteBtn) {
        const actionUrl = inviteBtn.getAttribute('data-action-url');
        const csrfToken = AdminUtils.getCsrfToken();

        inviteBtn.addEventListener('click', async function() {
            const confirmMsg = inviteBtn.getAttribute('data-confirm-msg') || 'Send an account registration invitation to this guest customer?';
            if (!await AdminModal.confirm(confirmMsg)) {
                return;
            }

            this.disabled = true;
            const sendingMsg = inviteBtn.getAttribute('data-sending-msg') || 'Sending...';
            this.innerHTML = `<i class="fas fa-spinner fa-spin"></i> <span>${sendingMsg}</span>`;

            const formData = new FormData();
            formData.append('action', 'send_account_invitation');

            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const successMsg = inviteBtn.getAttribute('data-success-msg') || 'Invitation sent successfully!';
                const errorMsg = inviteBtn.getAttribute('data-error-msg') || 'Failed to send invitation';
                const sentMsg = inviteBtn.getAttribute('data-sent-msg') || 'Invitation Sent';
                const defaultMsg = inviteBtn.getAttribute('data-default-msg') || 'Send Account Invitation';

                if (data.success) {
                    AdminModal.toast(data.message || successMsg, 'success');
                    this.disabled = false;
                    this.innerHTML = `<i class="fas fa-check"></i> <span>${sentMsg}</span>`;
                } else {
                    AdminModal.alert({message: data.message || errorMsg, type: 'error'});
                    this.disabled = false;
                    this.innerHTML = `<i class="fas fa-envelope"></i> <span>${defaultMsg}</span>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const errorOccurredMsg = inviteBtn.getAttribute('data-error-occurred-msg') || 'An error occurred';
                const defaultMsg = inviteBtn.getAttribute('data-default-msg') || 'Send Account Invitation';
                AdminModal.alert({message: errorOccurredMsg, type: 'error'});
                this.disabled = false;
                this.innerHTML = `<i class="fas fa-envelope"></i> <span>${defaultMsg}</span>`;
            });
        });
    }

    // ========================================
    // Convert to Affiliate Button
    // ========================================
    const convertBtn = document.getElementById('convert-to-affiliate-btn');
    if (convertBtn) {
        const actionUrl = convertBtn.getAttribute('data-action-url');
        const csrfToken = AdminUtils.getCsrfToken();

        convertBtn.addEventListener('click', async function() {
            const confirmMsg = convertBtn.getAttribute('data-confirm-msg') || 'Are you sure you want to convert this customer to an affiliate?';
            if (!await AdminModal.confirm(confirmMsg)) {
                return;
            }

            this.disabled = true;
            const convertingMsg = convertBtn.getAttribute('data-converting-msg') || 'Converting...';
            this.innerHTML = `<i class="fas fa-spinner fa-spin"></i> <span>${convertingMsg}</span>`;

            const formData = new FormData();
            formData.append('action', 'convert_to_affiliate');

            fetch(actionUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    const errorMsg = convertBtn.getAttribute('data-error-msg') || 'Failed to convert to affiliate';
                    const defaultMsg = convertBtn.getAttribute('data-default-msg') || 'Convert to Affiliate';
                    AdminModal.alert({message: data.message || errorMsg, type: 'error'});
                    this.disabled = false;
                    this.innerHTML = `<i class="fas fa-handshake"></i> <span>${defaultMsg}</span>`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const errorOccurredMsg = convertBtn.getAttribute('data-error-occurred-msg') || 'An error occurred';
                const defaultMsg = convertBtn.getAttribute('data-default-msg') || 'Convert to Affiliate';
                AdminModal.alert({message: errorOccurredMsg, type: 'error'});
                this.disabled = false;
                this.innerHTML = `<i class="fas fa-handshake"></i> <span>${defaultMsg}</span>`;
            });
        });
    }

    // ========================================
    // Add Note Form
    // ========================================
    const addNoteForm = document.getElementById('add-note-form');
    if (addNoteForm) {
        const addNoteUrl = addNoteForm.getAttribute('data-add-note-url');
        const customerIdInput = addNoteForm.getAttribute('data-customer-id');
        const csrfToken = AdminUtils.getCsrfToken();

        addNoteForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            formData.append('customer_id', customerIdInput);

            fetch(addNoteUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    const errorMsg = addNoteForm.getAttribute('data-error-msg') || 'Failed to add note';
                    AdminModal.alert({message: data.message || errorMsg, type: 'error'});
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const errorOccurredMsg = addNoteForm.getAttribute('data-error-occurred-msg') || 'An error occurred';
                AdminModal.alert({message: errorOccurredMsg, type: 'error'});
            });
        });
    }

    // ========================================
    // Address "Set Default" Buttons
    // ========================================
    document.querySelectorAll('.address-action-default').forEach(button => {
        button.addEventListener('click', function() {
            const addressId = this.dataset.addressId;
            const addressType = this.dataset.addressType;
            const csrfToken = AdminUtils.getCsrfToken();

            if (!addressId) return;

            // Disable button and show loading
            const originalHTML = this.innerHTML;
            const settingMsg = this.getAttribute('data-setting-msg') || 'Setting...';
            this.disabled = true;
            this.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${settingMsg}`;

            fetch(`/api/customers/admin/addresses/${addressId}/set-default/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reload page to show updated default status
                    location.reload();
                } else {
                    const errorMsg = this.getAttribute('data-error-msg') || 'Failed to set address as default';
                    AdminModal.alert({message: data.message || errorMsg, type: 'error'});
                    this.disabled = false;
                    this.innerHTML = originalHTML;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const errorOccurredMsg = this.getAttribute('data-error-occurred-msg') || 'An error occurred while setting default address';
                AdminModal.alert({message: errorOccurredMsg, type: 'error'});
                this.disabled = false;
                this.innerHTML = originalHTML;
            });
        });
    });
});
