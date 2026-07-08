/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Language Management JavaScript
 * Handles drag-and-drop functionality for language configuration
 */

class LanguageManager {
    constructor() {
        this.availableList = document.getElementById('available-languages');
        this.activeList = document.getElementById('active-languages');
        this.searchInput = document.getElementById('language-search');
        // Filter buttons removed - no longer needed
        this.saveButton = document.getElementById('save-languages');
        this.resetButton = document.getElementById('reset-languages');

        this.originalState = this.captureState();

        this.initDragAndDrop();
        this.initSearch();
        // Filters removed - search only now
        this.initButtons();
        this.updateCounts();
    }

    captureState() {
        // Capture the initial state for reset functionality
        return {
            available: Array.from(this.availableList.children).map(el => el.dataset.id),
            active: Array.from(this.activeList.children).map(el => el.dataset.id)
        };
    }

    initDragAndDrop() {
        // Initialize Sortable for available languages
        new Sortable(this.availableList, {
            group: 'languages',
            animation: 150,
            fallbackOnBody: true,
            swapThreshold: 0.65,
            ghostClass: 'dragging',
            filter: '.filtered-out',
            onStart: (evt) => {
                evt.item.classList.add('dragging');
            },
            onEnd: (evt) => {
                evt.item.classList.remove('dragging');
                this.updateCounts();
                this.checkRequirements();
            }
        });

        // Initialize Sortable for active languages
        new Sortable(this.activeList, {
            group: 'languages',
            animation: 150,
            fallbackOnBody: true,
            swapThreshold: 0.65,
            ghostClass: 'dragging',
            handle: '.drag-handle',
            onStart: (evt) => {
                evt.item.classList.add('dragging');
            },
            onEnd: (evt) => {
                evt.item.classList.remove('dragging');
                this.updateCounts();
                this.checkRequirements();
                this.updateLanguageItem(evt.item, evt.to === this.activeList);
            },
            onAdd: (evt) => {
                this.updateLanguageItem(evt.item, true);
            },
            onRemove: (evt) => {
                this.updateLanguageItem(evt.item, false);
            }
        });

        // Handle remove buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-remove-language')) {
                const btn = e.target.closest('.btn-remove-language');
                const item = btn.closest('.language-item');
                if (item && !item.classList.contains('is-default')) {
                    this.moveToAvailable(item);
                } else if (item.classList.contains('is-default')) {
                    AdminModal.alert({message: 'Cannot remove the default language. Please set another language as default first.', type: 'warning'});
                }
            }
        });
    }

    updateLanguageItem(item, isActive) {
        if (isActive) {
            // Add drag handle if not present
            if (!item.querySelector('.drag-handle')) {
                const handle = document.createElement('span');
                handle.className = 'drag-handle';
                handle.innerHTML = '<i class="fas fa-grip-vertical"></i>';
                item.insertBefore(handle, item.firstChild);
            }

            // Add remove button if not present
            if (!item.querySelector('.btn-remove-language')) {
                const removeBtn = document.createElement('button');
                removeBtn.className = 'btn-remove-language';
                removeBtn.dataset.id = item.dataset.id;
                removeBtn.title = 'Remove language';
                removeBtn.innerHTML = '<i class="fas fa-times"></i>';
                item.appendChild(removeBtn);
            }
        } else {
            // Remove drag handle
            const handle = item.querySelector('.drag-handle');
            if (handle) handle.remove();

            // Remove remove button
            const removeBtn = item.querySelector('.btn-remove-language');
            if (removeBtn) removeBtn.remove();

            // Remove default badge if present
            const defaultBadge = item.querySelector('.badge-default');
            if (defaultBadge) defaultBadge.remove();
            item.classList.remove('is-default');
        }
    }

    moveToAvailable(item) {
        this.updateLanguageItem(item, false);
        this.availableList.appendChild(item);
        this.updateCounts();
        this.checkRequirements();
    }

    initSearch() {
        this.searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            // Only search within available languages list, not active languages
            const availableItems = this.availableList.querySelectorAll('.language-item');

            availableItems.forEach(item => {
                const name = item.querySelector('.language-name').textContent.toLowerCase();
                const code = item.dataset.code.toLowerCase();
                const englishName = item.querySelector('.language-code').textContent.toLowerCase();

                if (name.includes(query) || code.includes(query) || englishName.includes(query)) {
                    item.classList.remove('filtered-out');
                    item.style.display = '';
                } else {
                    item.classList.add('filtered-out');
                    item.style.display = 'none';
                }
            });
        });
    }

    // Filter methods removed - using search only

    initButtons() {
        // Save button
        this.saveButton.addEventListener('click', () => {
            this.saveConfiguration();
        });

        // Reset button
        this.resetButton.addEventListener('click', async () => {
            if (await AdminModal.confirm({ message: 'Reset to the original configuration? This will discard all changes.', danger: true, confirmText: 'Reset' })) {
                this.resetToOriginal();
            }
        });
    }

    updateCounts() {
        const availableCount = this.availableList.querySelectorAll('.language-item:not(.filtered-out)').length;
        const activeCount = this.activeList.querySelectorAll('.language-item').length;

        document.getElementById('available-count').textContent = `(${availableCount})`;
        document.getElementById('active-list-count').textContent = `(${activeCount})`;
        document.getElementById('active-count').textContent = activeCount;
    }

    checkRequirements() {
        const activeItems = this.activeList.querySelectorAll('.language-item');
        let needsNllb = false;
        let hasLimited = false;

        activeItems.forEach(item => {
            if (item.dataset.requiresNllb === 'true') {
                needsNllb = true;
            }
            if (item.dataset.support === 'limited') {
                hasLimited = true;
            }
        });

        // Show warnings if needed (could display a notification)
        if (needsNllb) {
            console.log('Some selected languages require NLLB model');
        }
        if (hasLimited) {
            console.log('Some selected languages have limited support in M2M100 418M');
        }
    }

    saveConfiguration() {
        const activeIds = Array.from(this.activeList.children).map(el => el.dataset.id);
        const deactivateIds = Array.from(this.availableList.children).map(el => el.dataset.id);

        // Show loading state
        this.saveButton.disabled = true;
        this.saveButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

        fetch('/api/translations/service/languages/bulk-update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': AdminUtils.getCsrfToken()
            },
            body: JSON.stringify({
                activate_ids: activeIds,
                deactivate_ids: deactivateIds
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update original state
                this.originalState = this.captureState();

                // Show success message
                this.showMessage('Languages saved successfully!', 'success');

                // Reset button state
                this.saveButton.disabled = false;
                this.saveButton.innerHTML = '<i class="fas fa-save"></i> Save Configuration';
            } else {
                throw new Error(data.error || 'Failed to save languages');
            }
        })
        .catch(error => {
            console.error('Error saving languages:', error);
            this.showMessage('Failed to save languages: ' + error.message, 'error');

            // Reset button state
            this.saveButton.disabled = false;
            this.saveButton.innerHTML = '<i class="fas fa-save"></i> Save Configuration';
        });
    }

    resetToOriginal() {
        // This would need to be implemented to restore the original state
        // For now, just reload the page
        window.location.reload();
    }

    showMessage(message, type = 'info') {
        // Create or update message element
        let messageEl = document.getElementById('language-message');
        if (!messageEl) {
            messageEl = document.createElement('div');
            messageEl.id = 'language-message';
            document.querySelector('#content-main').insertBefore(
                messageEl,
                document.querySelector('#content-main').firstChild
            );
        }

        messageEl.className = `module message-${type}`;
        messageEl.innerHTML = `
            <div class="message-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-triangle'}"></i>
                ${message}
            </div>
        `;

        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageEl.style.display = 'none';
        }, 5000);
    }
}

// Badge legend toggle
document.addEventListener('click', function(e) {
    const toggle = e.target.closest('[data-action="toggle-badge-legend"]');
    if (!toggle) return;
    const legend = document.getElementById('badge-legend');
    const icon = document.getElementById('legend-toggle');
    if (legend) {
        legend.hidden = !legend.hidden;
        if (icon) icon.classList.toggle('fa-chevron-up', !legend.hidden);
        if (icon) icon.classList.toggle('fa-chevron-down', legend.hidden);
    }
});

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    new LanguageManager();
});