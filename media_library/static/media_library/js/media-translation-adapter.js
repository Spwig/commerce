/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Media Library Translation Adapter
 * Adapts the TranslationEditor for use with media assets
 */

class MediaTranslationAdapter {
    constructor() {
        this.apiBaseUrl = this.getApiBaseUrl();
        this.editors = new Map();
    }

    getApiBaseUrl() {
        // API is outside i18n_patterns, no language prefix needed
        return '/api/media';
    }

    initializeField(field) {
        const mediaId = field.dataset.mediaId;
        const fieldName = field.dataset.fieldName;

        console.log('Initializing translation field:', fieldName, 'for media:', mediaId);

        if (!mediaId || !fieldName) {
            console.warn('Missing media ID or field name for translation field', field);
            return;
        }

        // Create custom translation editor for media
        const editor = new MediaFieldTranslationEditor({
            apiBaseUrl: this.apiBaseUrl,
            mediaId: mediaId,
            fieldName: fieldName,
            field: field
        });

        this.editors.set(field, editor);
    }

    initializeAll() {
        console.log('MediaTranslationAdapter: Looking for translatable fields...');

        // Find all translatable fields
        const translatableFields = document.querySelectorAll('[data-translatable="true"]');

        console.log('Found translatable fields:', translatableFields.length);

        translatableFields.forEach(field => {
            if (!field.dataset.translationInitialized) {
                this.initializeField(field);
                field.dataset.translationInitialized = 'true';
            }
        });
    }
}

class MediaFieldTranslationEditor {
    constructor(options) {
        this.apiBaseUrl = options.apiBaseUrl;
        this.mediaId = options.mediaId;
        this.fieldName = options.fieldName;
        this.field = options.field;
        this.translations = {};
        this.availableLanguages = [];

        this.createTranslateButton();
        this.loadTranslations();
    }

    createTranslateButton() {
        console.log('Creating translate button for field:', this.fieldName);

        // Create translate button next to field
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'translation-trigger util-btn';
        button.innerHTML = '<i class="fas fa-language"></i>';
        button.title = 'Translate';
        button.style.marginLeft = '10px';
        button.style.marginTop = '5px';

        // Find the right place to insert the button
        // For textareas, insert after the field
        // For input fields, insert in the same line
        const container = this.field.parentNode;

        if (this.field.tagName === 'TEXTAREA') {
            // For textarea, insert after it
            const buttonContainer = document.createElement('div');
            buttonContainer.style.marginTop = '5px';
            buttonContainer.appendChild(button);

            if (this.field.nextSibling) {
                container.insertBefore(buttonContainer, this.field.nextSibling);
            } else {
                container.appendChild(buttonContainer);
            }
        } else {
            // For input fields, insert inline
            if (this.field.nextSibling) {
                container.insertBefore(button, this.field.nextSibling);
            } else {
                container.appendChild(button);
            }
        }

        button.addEventListener('click', async (e) => {
            e.preventDefault();
            e.stopPropagation();
            await this.openTranslationEditor();
        });

        this.triggerButton = button;
        console.log('Translation button created for:', this.fieldName);
    }

    async loadTranslations() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/media/${this.mediaId}/translation-status/`);
            const data = await response.json();

            if (data.translations) {
                this.translations = data.translations;
                this.availableLanguages = data.missing_languages || [];
                this.updateButtonIndicator();
            }
        } catch (error) {
            console.error('Failed to load translations:', error);
        }
    }

    updateButtonIndicator() {
        // Update button to show if translations exist
        const translatedCount = Object.keys(this.translations).filter(lang => {
            const langTranslations = this.translations[lang];
            return langTranslations && langTranslations[this.fieldName];
        }).length;

        if (translatedCount > 0) {
            this.triggerButton.classList.add('has-translations');
        } else {
            this.triggerButton.classList.remove('has-translations');
        }
    }

    async openTranslationEditor() {
        // Check if TranslationEditor is available
        if (typeof TranslationEditor === 'undefined') {
            console.error('TranslationEditor not loaded');
            AdminModal.alert({message: 'Translation editor is not available. Please check your configuration.', type: 'error'});
            return;
        }

        // Create a custom editor instance for media
        const editor = new TranslationEditor({
            translateEndpoint: `${this.apiBaseUrl}/translate/`,
            statusEndpoint: `${this.apiBaseUrl}/media/${this.mediaId}/translation-status/`,
            saveEndpoint: `${this.apiBaseUrl}/media/${this.mediaId}/save-translations/`,
            onTranslate: (translations) => {
                this.handleTranslationComplete(translations);
            },
            onError: (error) => {
                console.error('Translation error:', error);
                AdminModal.alert({message: 'Translation failed: ' + error, type: 'error'});
            }
        });

        // Fetch and set available languages for media library context
        await editor.fetchAndUpdateLanguages();

        // Custom attach method for media fields
        editor.currentElement = { id: this.mediaId };
        editor.currentField = this.fieldName;
        editor.targetInput = this.field;
        editor.translations = this.translations;

        // Open the editor
        editor.open();
    }

    handleTranslationComplete(translations) {
        // Update local translations
        this.translations = translations;
        this.updateButtonIndicator();

        // Show success message
        const message = document.createElement('div');
        message.className = 'messagelist';
        message.innerHTML = `
            <div class="success">
                <i class="fas fa-check-circle"></i>
                Translations saved successfully
            </div>
        `;

        // Insert message at top of form
        const form = this.field.closest('form');
        if (form) {
            form.insertBefore(message, form.firstChild);
            setTimeout(() => message.remove(), 5000);
        }
    }
}

// Initialize on DOM ready
function initializeMediaTranslations() {
    console.log('Initializing MediaTranslationAdapter...');
    const adapter = new MediaTranslationAdapter();
    adapter.initializeAll();

    // Make adapter globally available
    window.MediaTranslationAdapter = adapter;

    // Also try initializing after a short delay to catch any dynamically loaded content
    setTimeout(() => {
        console.log('Re-checking for translatable fields...');
        adapter.initializeAll();
    }, 500);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeMediaTranslations);
} else {
    // DOM is already ready
    initializeMediaTranslations();
}