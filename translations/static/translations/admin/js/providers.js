/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * External Providers Management JavaScript
 */

class ProvidersManager {
    constructor() {
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Filter provider cards based on configuration status
        const filterButtons = document.querySelectorAll('.filter-btn');
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filterProviders(e.target.dataset.filter);
            });
        });

        // Search functionality
        const searchInput = document.getElementById('provider-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.searchProviders(e.target.value);
            });
        }
    }

    filterProviders(filter) {
        const cards = document.querySelectorAll('.provider-card');

        cards.forEach(card => {
            switch (filter) {
                case 'all':
                    card.style.display = '';
                    break;
                case 'configured':
                    card.style.display = card.classList.contains('configured') ? '' : 'none';
                    break;
                case 'not-configured':
                    card.style.display = !card.classList.contains('configured') ? '' : 'none';
                    break;
            }
        });

        // Update active filter button
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-filter="${filter}"]`)?.classList.add('active');
    }

    searchProviders(query) {
        const cards = document.querySelectorAll('.provider-card');
        const searchTerm = query.toLowerCase();

        cards.forEach(card => {
            const providerName = card.querySelector('h3').textContent.toLowerCase();
            const providerDesc = card.querySelector('.provider-description')?.textContent.toLowerCase() || '';

            if (providerName.includes(searchTerm) || providerDesc.includes(searchTerm)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
        `;

        document.body.appendChild(notification);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

/**
 * Toggle provider account active status
 */
function toggleProvider(accountId) {
    const csrfToken = AdminUtils.getCsrfToken();

    // Build URL from template, replacing the placeholder UUID
    const config = document.getElementById('translations-config');
    const urlTemplate = config?.dataset.toggleProviderUrlTemplate || '';
    const url = urlTemplate.replace('00000000-0000-0000-0000-000000000000', accountId);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            AdminModal.alert({message: 'Error: ' + data.error, type: 'error'});
        }
    })
    .catch(error => {
        console.error('Error:', error);
        AdminModal.alert({message: 'Failed to toggle provider', type: 'error'});
    });
}

/**
 * Handle provider actions via delegation
 */
function handleProviderActions(e) {
    const actionElement = e.target.closest('[data-action]');
    if (!actionElement) return;

    const action = actionElement.dataset.action;

    if (action === 'toggle-provider') {
        e.preventDefault();
        const accountId = actionElement.dataset.accountId;
        if (accountId) {
            toggleProvider(accountId);
        }
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    new ProvidersManager();

    // Event delegation for provider actions
    document.addEventListener('click', handleProviderActions);
});