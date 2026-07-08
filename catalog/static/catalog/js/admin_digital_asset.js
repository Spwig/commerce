/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Digital Asset Inline JavaScript
 * Enhances file upload functionality with validation, auto-population, and progress tracking
 */

(function() {
    'use strict';

    /**
     * Initialize digital asset inline functionality
     */
    function initDigitalAssetInline() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    }

    function init() {
        // Initialize existing inlines
        const inlineGroup = document.querySelector('#digitalasset_set-group');
        if (!inlineGroup) return;

        // Find all digital asset inline forms
        const inlineForms = inlineGroup.querySelectorAll('.inline-related');
        inlineForms.forEach(initInlineForm);

        // Watch for dynamically added inlines
        observeInlineAdditions(inlineGroup);
    }

    /**
     * Initialize a single inline form
     */
    function initInlineForm(inlineForm) {
        const fileInput = inlineForm.querySelector('input[type="file"]');
        const filenameInput = inlineForm.querySelector('.field-filename input');

        if (fileInput) {
            // Auto-populate filename from uploaded file
            fileInput.addEventListener('change', function(e) {
                handleFileSelection(e, fileInput, filenameInput, inlineForm);
            });

            // Add drag-and-drop support
            addDragAndDropSupport(fileInput);
        }

        // Add validation for numeric fields
        addNumericFieldValidation(inlineForm);

        // Show/hide license key info based on requires_license checkbox
        const requiresLicenseCheckbox = inlineForm.querySelector('.field-requires_license input[type="checkbox"]');
        if (requiresLicenseCheckbox) {
            requiresLicenseCheckbox.addEventListener('change', function() {
                updateLicenseKeyInfo(inlineForm, this.checked);
            });
        }
    }

    /**
     * Handle file selection and auto-populate filename
     */
    function handleFileSelection(event, fileInput, filenameInput, inlineForm) {
        const file = fileInput.files[0];
        if (!file) return;

        // Validate file size (max 2GB for digital products)
        const maxSize = 2 * 1024 * 1024 * 1024; // 2GB
        if (file.size > maxSize) {
            AdminModal.alert({message: `File size (${formatFileSize(file.size)}) exceeds maximum allowed size (2GB). Please choose a smaller file.`, type: 'warning'});
            fileInput.value = '';
            return;
        }

        // Auto-populate filename if empty
        if (filenameInput && !filenameInput.value) {
            filenameInput.value = file.name;
        }

        // Show file info
        displayFileInfo(file, inlineForm);

        // Validate file type
        validateFileType(file, fileInput);
    }

    /**
     * Display file information near the file input
     */
    function displayFileInfo(file, inlineForm) {
        const fileField = inlineForm.querySelector('.field-file');
        if (!fileField) return;

        // Remove existing file info if present
        const existingInfo = fileField.querySelector('.file-upload-info');
        if (existingInfo) {
            existingInfo.remove();
        }

        // Create file info display
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-upload-info';
        fileInfo.style.cssText = `
            margin-top: 12px;
            padding: 12px;
            background: var(--darkened-bg, #f8f9fa);
            border: 1px solid var(--hairline-color, #e8e8e8);
            border-radius: 6px;
            font-size: 13px;
        `;

        fileInfo.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 6px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-weight: 600;">📄 ${escapeHtml(file.name)}</span>
                </div>
                <div style="color: var(--body-quiet-color, #666);">
                    Size: <strong>${formatFileSize(file.size)}</strong> |
                    Type: <strong>${file.type || 'Unknown'}</strong>
                </div>
            </div>
        `;

        fileField.appendChild(fileInfo);
    }

    /**
     * Validate file type and show warning for uncommon types
     */
    function validateFileType(file, fileInput) {
        // Common digital product file types
        const allowedTypes = [
            // Archives
            'application/zip', 'application/x-zip-compressed',
            'application/x-rar-compressed', 'application/x-7z-compressed',
            'application/x-tar', 'application/gzip',
            // Documents
            'application/pdf',
            'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            // Media
            'image/jpeg', 'image/png', 'image/gif', 'image/svg+xml',
            'video/mp4', 'video/mpeg', 'video/quicktime',
            'audio/mpeg', 'audio/wav', 'audio/ogg',
            // Code/Text
            'text/plain', 'text/html', 'text/css', 'application/javascript',
            'application/json', 'application/xml',
            // Executables (for software products)
            'application/x-msdownload', 'application/x-msdos-program',
            'application/x-executable',
            // Disk images
            'application/x-iso9660-image'
        ];

        if (file.type && !allowedTypes.includes(file.type)) {
            console.warn(`Uncommon file type detected: ${file.type}`);
            // Don't block, just warn in console
        }
    }

    /**
     * Add drag-and-drop support to file input
     */
    function addDragAndDropSupport(fileInput) {
        const fileField = fileInput.closest('.field-file');
        if (!fileField) return;

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileField.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            fileField.addEventListener(eventName, () => {
                fileInput.style.borderColor = 'var(--primary, #417690)';
                fileInput.style.background = 'var(--body-bg, #fff)';
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            fileField.addEventListener(eventName, () => {
                fileInput.style.borderColor = '';
                fileInput.style.background = '';
            }, false);
        });

        // Handle dropped files
        fileField.addEventListener('drop', function(e) {
            const dt = e.dataTransfer;
            const files = dt.files;

            if (files.length > 0) {
                // Create a new FileList and assign to input
                fileInput.files = files;

                // Trigger change event
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        }, false);
    }

    /**
     * Add validation for numeric fields (download_limit, expiration_days)
     */
    function addNumericFieldValidation(inlineForm) {
        const downloadLimitInput = inlineForm.querySelector('.field-download_limit input');
        const expirationDaysInput = inlineForm.querySelector('.field-expiration_days input');

        [downloadLimitInput, expirationDaysInput].forEach(input => {
            if (!input) return;

            input.addEventListener('blur', function() {
                const value = parseInt(this.value, 10);

                // Ensure positive number or empty
                if (this.value !== '' && (isNaN(value) || value < 0)) {
                    AdminModal.alert({message: 'Please enter a positive number or leave blank for unlimited.', type: 'warning'});
                    this.value = '';
                    this.focus();
                }
            });
        });
    }

    /**
     * Update license key information display
     */
    function updateLicenseKeyInfo(inlineForm, requiresLicense) {
        const licenseKeyField = inlineForm.querySelector('.field-license_key_preview');
        if (!licenseKeyField) return;

        // Visual feedback - highlight when license is required
        if (requiresLicense) {
            licenseKeyField.style.background = 'var(--success-light, #d4edda)';
            licenseKeyField.style.border = '1px solid var(--success-border, #c3e6cb)';
            licenseKeyField.style.padding = '12px';
            licenseKeyField.style.borderRadius = '6px';
        } else {
            licenseKeyField.style.background = '';
            licenseKeyField.style.border = '';
            licenseKeyField.style.padding = '';
            licenseKeyField.style.borderRadius = '';
        }
    }

    /**
     * Observe for dynamically added inline forms
     */
    function observeInlineAdditions(inlineGroup) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.classList.contains('inline-related')) {
                        initInlineForm(node);
                    }
                });
            });
        });

        observer.observe(inlineGroup, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Format file size to human-readable format
     */
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';

        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));

        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Add form submission validation
     */
    function addFormValidation() {
        const form = document.querySelector('form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            const inlineGroup = document.querySelector('#digitalasset_set-group');
            if (!inlineGroup) return;

            const inlineForms = inlineGroup.querySelectorAll('.inline-related:not(.empty-form)');
            let hasErrors = false;

            inlineForms.forEach(function(inlineForm) {
                // Skip if marked for deletion
                const deleteCheckbox = inlineForm.querySelector('.delete input[type="checkbox"]');
                if (deleteCheckbox && deleteCheckbox.checked) return;

                const fileInput = inlineForm.querySelector('input[type="file"]');
                const filenameInput = inlineForm.querySelector('.field-filename input');

                // Check if file is selected but filename is empty
                if (fileInput && fileInput.files.length > 0 && filenameInput && !filenameInput.value) {
                    AdminModal.alert({message: 'Please provide a filename for the uploaded file.', type: 'warning'});
                    filenameInput.focus();
                    hasErrors = true;
                }
            });

            if (hasErrors) {
                e.preventDefault();
                return false;
            }
        });
    }

    // Initialize when script loads
    initDigitalAssetInline();
    addFormValidation();

})();
