/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function() {
    'use strict';

    var configEl = document.getElementById('newsletter-send-config');
    var config = configEl ? JSON.parse(configEl.textContent) : { i18n: {} };

    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('sendForm');
        const segmentCheckboxes = document.querySelectorAll('input[name="segments[]"]');
        const statusRadios = document.querySelectorAll('input[name="customer_status"]');
        const csvInput = document.getElementById('csv_file');
        const recipientCountCard = document.getElementById('recipientCountCard');
        const recipientCountNumber = document.getElementById('recipientCountNumber');
        const sendButton = document.getElementById('sendButton');

        // Update recipient count on filter change
        function updateRecipientCount() {
            recipientCountCard.classList.add('loading');

            const formData = new FormData();
            formData.append('action', 'preview_recipients');
            // Read CSRF token from the form (not from an inline script)
            const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
            if (csrfInput) {
                formData.append('csrfmiddlewaretoken', csrfInput.value);
            }

            // Add selected segments
            segmentCheckboxes.forEach(checkbox => {
                if (checkbox.checked) {
                    formData.append('segments[]', checkbox.value);
                }
            });

            // Add customer status
            const selectedStatus = document.querySelector('input[name="customer_status"]:checked');
            if (selectedStatus) {
                formData.append('customer_status', selectedStatus.value);
            }

            fetch('', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                recipientCountNumber.textContent = data.recipient_count.toLocaleString();
                recipientCountCard.classList.remove('loading');
                sendButton.disabled = data.recipient_count === 0;
            })
            .catch(error => {
                console.error('Error updating recipient count:', error);
                recipientCountCard.classList.remove('loading');
            });
        }

        // Listen for filter changes
        segmentCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', updateRecipientCount);
        });

        statusRadios.forEach(radio => {
            radio.addEventListener('change', updateRecipientCount);
        });

        // CSV upload disables filters
        csvInput.addEventListener('change', function() {
            const hasFile = csvInput.files.length > 0;

            segmentCheckboxes.forEach(checkbox => {
                checkbox.disabled = hasFile;
            });

            statusRadios.forEach(radio => {
                radio.disabled = hasFile;
            });

            if (hasFile) {
                recipientCountNumber.textContent = '—';
                sendButton.disabled = false;
            } else {
                updateRecipientCount();
            }
        });

        // Confirm before sending
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const count = recipientCountNumber.textContent;
            const i18n = config.i18n || {};
            const msg = (i18n.confirmSendPrefix || 'Send newsletter to ') + count + (i18n.confirmSendSuffix || ' recipients?');
            if (await AdminModal.confirm(msg)) {
                form.submit();
            }
        });

        // Initial count
        updateRecipientCount();
    });
})();
