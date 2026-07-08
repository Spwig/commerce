/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Blog Post Admin JavaScript
 *
 * Handles page builder toggle and content field visibility.
 *
 *  */
document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    var $ = django.jQuery;
    if (!$) return;

    var usePageBuilderCheckbox = $('#id_use_page_builder');
    var simpleContentField = $('.field-simple_content');
    var contentPageField = $('.field-content_page');

    /**
     * Toggle visibility of content fields based on page builder setting.
     */
    function toggleContentFields() {
        if (usePageBuilderCheckbox.is(':checked')) {
            // Page Builder mode - hide simple content, show page link
            simpleContentField.hide();
            contentPageField.show();
        } else {
            // Simple mode - show simple content, hide page link
            simpleContentField.show();
            contentPageField.hide();
        }
    }

    // Initial state
    if (usePageBuilderCheckbox.length) {
        toggleContentFields();

        // Listen for changes
        usePageBuilderCheckbox.on('change', toggleContentFields);
    }

    // Add "Create Page" button when enabling page builder without existing page
    var contentPageSelect = $('#id_content_page');
    if (usePageBuilderCheckbox.length && contentPageSelect.length) {
        usePageBuilderCheckbox.on('change', function() {
            if ($(this).is(':checked') && !contentPageSelect.val()) {
                // Could add a "Create Page" button here in future
                // For now, show a helpful message
                if (!$('.page-builder-help').length) {
                    contentPageField.append(
                        '<p class="page-builder-help" style="color: #666; margin-top: 5px;">' +
                        'Save the post first, then the linked page can be created.' +
                        '</p>'
                    );
                }
            }
        });
    }
});
