/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Blog Post Change Form JavaScript
 * Handles sidebar toggle, tabs, and page builder toggle
 *
 *  */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog change form JS loaded');

    // ========================================
    // Mobile Sidebar Toggle Functionality
    // ========================================
    const sidebarToggle = document.getElementById('blog-sidebar-toggle');
    const sidebarClose = document.getElementById('blog-sidebar-close');
    const sidebar = document.getElementById('blog-sidebar');
    const backdrop = document.getElementById('blog-sidebar-backdrop');

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

    // ========================================
    // Tab Management (handled by AdminTabs)
    // ========================================
    // AdminTabs (admin-tabs.js) auto-initializes on .admin-tabs container.
    // It handles tab switching, localStorage persistence, error scanning,
    // error badges, and auto-switching to the first tab with errors.

    // ========================================
    // Page Builder Toggle Functionality
    // ========================================
    const usePageBuilderCheckbox = document.getElementById('id_use_page_builder');
    const simpleContentWrapper = document.getElementById('simple-content-wrapper');
    const pageBuilderWrapper = document.getElementById('page-builder-wrapper');

    function toggleContentFields() {
        if (!usePageBuilderCheckbox) return;

        if (usePageBuilderCheckbox.checked) {
            if (simpleContentWrapper) {
                simpleContentWrapper.style.display = 'none';
            }
            if (pageBuilderWrapper) {
                pageBuilderWrapper.style.display = 'block';
            }
        } else {
            if (simpleContentWrapper) {
                simpleContentWrapper.style.display = 'block';
            }
            if (pageBuilderWrapper) {
                pageBuilderWrapper.style.display = 'none';
            }
        }
    }

    if (usePageBuilderCheckbox) {
        toggleContentFields();
        usePageBuilderCheckbox.addEventListener('change', toggleContentFields);
    }

    // ========================================
    // Duplicate Post Button
    // ========================================
    const duplicateBtn = document.getElementById('duplicate-post-btn');
    if (duplicateBtn) {
        duplicateBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            const confirmMsg = this.getAttribute('data-confirm-msg') || 'Create a duplicate of this post?';
            if (!await AdminModal.confirm(confirmMsg)) {
                return false;
            }
            window.location.href = this.href || this.dataset.url;
        });
    }

    // ========================================
    // Social Share Message Character Counter
    // ========================================
    const shareMessageTextarea = document.getElementById('id_social_share_message');
    const charCounter = document.getElementById('share-message-counter');

    if (shareMessageTextarea && charCounter) {
        const maxChars = parseInt(shareMessageTextarea.getAttribute('maxlength') || 280, 10);

        function updateCharCount() {
            const remaining = maxChars - shareMessageTextarea.value.length;
            charCounter.textContent = `${shareMessageTextarea.value.length}/${maxChars}`;

            if (remaining < 20) {
                charCounter.classList.add('warning');
            } else {
                charCounter.classList.remove('warning');
            }
        }

        updateCharCount();
        shareMessageTextarea.addEventListener('input', updateCharCount);
    }

    // ========================================
    // Auto-Share Retry Button
    // ========================================
    document.querySelectorAll('.share-retry-btn').forEach(button => {
        button.addEventListener('click', function() {
            const shareId = this.dataset.shareId;
            const csrfToken = AdminUtils.getCsrfToken();

            if (!shareId || !csrfToken) return;

            // Disable button and show loading
            const originalHTML = this.innerHTML;
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

            fetch(`/api/blog/auto-shares/${shareId}/retry/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    AdminModal.alert({message: data.message || 'Failed to retry share', type: 'error'});
                    this.disabled = false;
                    this.innerHTML = originalHTML;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                AdminModal.alert({message: 'An error occurred', type: 'error'});
                this.disabled = false;
                this.innerHTML = originalHTML;
            });
        });
    });

    // ========================================
    // Scheduled Date/Time Validation
    // ========================================
    const statusSelect = document.getElementById('id_status');
    const scheduledAtInput = document.getElementById('id_scheduled_at');

    if (statusSelect && scheduledAtInput) {
        statusSelect.addEventListener('change', function() {
            if (this.value === 'scheduled' && !scheduledAtInput.value) {
                // Highlight the scheduled_at field
                scheduledAtInput.focus();
                scheduledAtInput.style.borderColor = 'var(--warning-fg)';
            } else {
                scheduledAtInput.style.borderColor = '';
            }
        });
    }

    // ========================================
    // Slug Auto-Generation from Title
    // ========================================
    const titleInput = document.getElementById('id_title');
    const slugInput = document.getElementById('id_slug');

    if (titleInput && slugInput) {
        // Only auto-generate if slug is empty and we're creating a new post
        const isNewPost = window.location.pathname.includes('/add/');

        if (isNewPost) {
            titleInput.addEventListener('blur', function() {
                if (!slugInput.value && this.value) {
                    // Generate slug from title
                    const slug = this.value
                        .toLowerCase()
                        .replace(/[^\w\s-]/g, '')  // Remove special chars
                        .replace(/\s+/g, '-')      // Replace spaces with hyphens
                        .replace(/-+/g, '-')       // Replace multiple hyphens
                        .substring(0, 255);        // Limit length

                    slugInput.value = slug;
                }
            });
        }
    }

    // CKEditor Media Library integration is handled by the shared
    // ckeditor_media_library.js loaded before this script.
});
