/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Translation Manager for Page Builder
 * Manages translations with health checks and scheduling
 */

class TranslationManager {
  constructor() {
    this.healthCheckInterval = null;
    this.currentHealth = null;
    this.pendingTranslations = new Map();
    this.init();
  }

  async init() {
    // Check health on initialization
    await this.checkHealth();

    // Set up periodic health checks (every 60 seconds)
    this.healthCheckInterval = setInterval(() => {
      this.checkHealth();
    }, 60000);

    // Set up event listeners
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Listen for translation requests from elements
    document.addEventListener('pagebuilder:translate-element', e => {
      this.handleTranslateRequest(e.detail);
    });

    // Listen for bulk translation requests
    document.addEventListener('pagebuilder:translate-page', e => {
      this.handlePageTranslation(e.detail);
    });
  }

  async checkHealth() {
    try {
      const response = await fetch('/api/translation-health/');
      const health = await response.json();

      this.currentHealth = health;
      this.updateHealthIndicators(health);

      // Emit health update event
      document.dispatchEvent(
        new CustomEvent('translation:health-update', {
          detail: health,
        })
      );

      return health;
    } catch (error) {
      console.error('Failed to check translation service health:', error);
      this.currentHealth = {
        available: false,
        status: 'offline',
        message: 'Unable to connect to translation service',
      };
      return this.currentHealth;
    }
  }

  updateHealthIndicators(health) {
    // Update any health indicators in the UI
    const indicators = document.querySelectorAll('[data-translation-health]');

    indicators.forEach(indicator => {
      // Update status class
      indicator.classList.remove('health-healthy', 'health-degraded', 'health-offline');
      indicator.classList.add(`health-${health.status}`);

      // Update tooltip
      if (health.message) {
        indicator.setAttribute('title', health.message);
      }

      // Show/hide based on availability
      if (!health.available) {
        indicator.classList.add('health-unavailable');
      } else {
        indicator.classList.remove('health-unavailable');
      }
    });

    // Show warnings if service is degraded
    if (health.ui_recommendations?.warnings?.length > 0) {
      this.showHealthWarnings(health.ui_recommendations.warnings);
    }
  }

  showHealthWarnings(warnings) {
    // Show warnings in a non-intrusive way
    const warningContainer = document.getElementById('translation-warnings');
    if (!warningContainer) {
      // Create warning container if it doesn't exist
      const container = document.createElement('div');
      container.id = 'translation-warnings';
      container.className = 'translation-warnings';
      document.body.appendChild(container);
    }

    const container = document.getElementById('translation-warnings');
    container.innerHTML = warnings
      .map(
        warning => `
            <div class="translation-warning">
                <i class="fas fa-exclamation-triangle"></i>
                <span>${warning}</span>
            </div>
        `
      )
      .join('');

    // Auto-hide after 10 seconds
    setTimeout(() => {
      container.innerHTML = '';
    }, 10000);
  }

  async handleTranslateRequest(detail) {
    const { elementId, languages, fields, callback } = detail;

    // Check health first
    if (!this.currentHealth || !this.currentHealth.available) {
      await this.checkHealth();
    }

    if (!this.currentHealth.available) {
      // Service unavailable - show error and offer to schedule
      this.showServiceUnavailable(elementId, callback);
      return;
    }

    // Get element content to calculate size
    const element = document.querySelector(`[data-element-id="${elementId}"]`);
    const textContent = this.extractTextContent(element, fields);
    const charCount = textContent.length;

    // Check if we should recommend scheduling
    const shouldSchedule = await this.shouldScheduleTranslation(charCount, languages.length);

    if (shouldSchedule) {
      // Show scheduling dialog
      this.showSchedulingDialog({
        elementId,
        languages,
        fields,
        charCount,
        callback,
      });
      return;
    }

    // Proceed with immediate translation
    await this.translateElement(elementId, languages, fields, callback);
  }

  extractTextContent(element, fields) {
    let content = '';

    fields.forEach(field => {
      if (field === 'text') {
        content += element.textContent || '';
      } else {
        // Handle other field types
        const fieldElement = element.querySelector(`[data-field="${field}"]`);
        if (fieldElement) {
          content += fieldElement.textContent || '';
        }
      }
    });

    return content;
  }

  async shouldScheduleTranslation(charCount, languageCount) {
    // Use current health status to determine
    if (this.currentHealth.status === 'degraded') {
      return true;
    }

    // Check thresholds
    const totalWork = charCount * languageCount;

    // Large jobs should be scheduled
    if (totalWork > 10000) {
      return true;
    }

    // Many languages should be scheduled
    if (languageCount > 5) {
      return true;
    }

    // Check server recommendation
    if (this.currentHealth.performance?.cpu_percent > 60) {
      return true;
    }

    return false;
  }

  showServiceUnavailable(elementId, callback) {
    const modal = document.createElement('div');
    modal.className = 'translation-modal service-unavailable';
    modal.innerHTML = `
            <div class="modal-content">
                <h3><i class="fas fa-exclamation-circle"></i> Translation Service Unavailable</h3>
                <p>The translation service is currently offline. Your translation has been queued and will be processed when the service becomes available.</p>
                <div class="modal-actions">
                    <button class="btn btn-primary" onclick="this.closest('.translation-modal').remove()">
                        Understood
                    </button>
                </div>
            </div>
        `;
    document.body.appendChild(modal);

    if (callback) {
      callback({
        success: false,
        error: 'service_unavailable',
        queued: true,
      });
    }
  }

  showSchedulingDialog(options) {
    const { elementId, languages, fields, charCount, callback } = options;

    // Calculate estimated time
    const estimatedTime = this.estimateTranslationTime(charCount, languages.length);

    const modal = document.createElement('div');
    modal.className = 'translation-modal scheduling-dialog';
    modal.innerHTML = `
            <div class="modal-content">
                <h3><i class="fas fa-clock"></i> Large Translation Job Detected</h3>
                <div class="job-details">
                    <p><strong>Content size:</strong> ${charCount.toLocaleString()} characters</p>
                    <p><strong>Target languages:</strong> ${languages.length}</p>
                    <p><strong>Estimated time:</strong> ${this.formatTime(estimatedTime)}</p>
                </div>
                <p>This translation job is large and may impact performance. We recommend scheduling it for background processing.</p>
                <div class="modal-actions">
                    <button class="btn btn-secondary" onclick="window.translationManager.proceedWithTranslation('${elementId}', ${JSON.stringify(languages)}, ${JSON.stringify(fields)})">
                        Translate Now
                    </button>
                    <button class="btn btn-primary" onclick="window.translationManager.scheduleTranslation('${elementId}', ${JSON.stringify(languages)}, ${JSON.stringify(fields)})">
                        Schedule Translation
                    </button>
                </div>
            </div>
        `;
    document.body.appendChild(modal);

    // Store callback for later use
    this.pendingTranslations.set(elementId, callback);
  }

  estimateTranslationTime(charCount, languageCount) {
    // Base estimate: ~100 chars/second per language
    let baseRate = 100;

    // Adjust for degraded service
    if (this.currentHealth?.status === 'degraded') {
      baseRate = 50;
    }

    const seconds = (charCount * languageCount) / baseRate;
    return Math.ceil(seconds);
  }

  formatTime(seconds) {
    if (seconds < 60) {
      return `${seconds} seconds`;
    } else if (seconds < 3600) {
      const minutes = Math.ceil(seconds / 60);
      return `${minutes} minute${minutes > 1 ? 's' : ''}`;
    } else {
      const hours = Math.ceil(seconds / 3600);
      return `${hours} hour${hours > 1 ? 's' : ''}`;
    }
  }

  async proceedWithTranslation(elementId, languages, fields) {
    // Close dialog
    document.querySelector('.translation-modal.scheduling-dialog')?.remove();

    // Get callback
    const callback = this.pendingTranslations.get(elementId);

    // Proceed with translation
    await this.translateElement(elementId, languages, fields, callback);

    // Clean up
    this.pendingTranslations.delete(elementId);
  }

  async scheduleTranslation(elementId, languages, fields) {
    // Close dialog
    document.querySelector('.translation-modal.scheduling-dialog')?.remove();

    try {
      const response = await fetch('/api/translate-element/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({
          element_id: elementId,
          languages: languages,
          fields: fields,
          schedule: true,
        }),
      });

      const result = await response.json();

      // Show success message
      this.showNotification('Translation scheduled successfully', 'success');

      // Execute callback
      const callback = this.pendingTranslations.get(elementId);
      if (callback) {
        callback(result);
      }

      // Clean up
      this.pendingTranslations.delete(elementId);
    } catch (error) {
      console.error('Failed to schedule translation:', error);
      this.showNotification('Failed to schedule translation', 'error');
    }
  }

  async translateElement(elementId, languages, fields, callback) {
    // Show progress indicator
    this.showProgress(elementId, 'Translating...');

    try {
      const response = await fetch('/api/translate-element/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({
          element_id: elementId,
          languages: languages,
          fields: fields || ['text'],
          schedule: false,
        }),
      });

      const result = await response.json();

      if (result.recommend_schedule) {
        // Server recommends scheduling
        this.showSchedulingDialog({
          elementId,
          languages,
          fields,
          charCount: result.char_count,
          callback,
        });
        this.hideProgress(elementId);
        return;
      }

      if (result.success) {
        // Translation successful
        this.showNotification('Translation completed successfully', 'success');

        // Update element to show new translations are available
        this.updateElementTranslationStatus(elementId, result.translations);
      } else if (result.success === 'partial') {
        // Partial success
        this.showNotification(`Partially translated: ${result.message}`, 'warning');
      } else {
        // Failed
        this.showNotification(result.error || 'Translation failed', 'error');
      }

      // Execute callback
      if (callback) {
        callback(result);
      }
    } catch (error) {
      console.error('Translation error:', error);
      this.showNotification('Translation failed: ' + error.message, 'error');

      if (callback) {
        callback({
          success: false,
          error: error.message,
        });
      }
    } finally {
      this.hideProgress(elementId);
    }
  }

  async handlePageTranslation(detail) {
    const { pageId, languages } = detail;

    // Check health first
    if (!this.currentHealth || !this.currentHealth.available) {
      await this.checkHealth();
    }

    if (!this.currentHealth.available) {
      this.showNotification('Translation service is unavailable', 'error');
      return;
    }

    // Always schedule page translations (they're usually large)
    try {
      const response = await fetch('/api/schedule-page-translation/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({
          page_id: pageId,
          languages: languages,
        }),
      });

      const result = await response.json();

      if (result.success) {
        this.showNotification(
          `Scheduled translation for ${result.element_count} elements (${this.formatTime(result.estimated_time)})`,
          'success'
        );
      } else {
        this.showNotification(result.error || 'Failed to schedule page translation', 'error');
      }
    } catch (error) {
      console.error('Page translation error:', error);
      this.showNotification('Failed to schedule page translation', 'error');
    }
  }

  updateElementTranslationStatus(elementId, translations) {
    const element = document.querySelector(`[data-element-id="${elementId}"]`);
    if (!element) return;

    // Add data attributes to indicate available translations
    const availableLanguages = Object.keys(translations);
    element.dataset.availableTranslations = availableLanguages.join(',');

    // Trigger event for other components
    document.dispatchEvent(
      new CustomEvent('translation:updated', {
        detail: {
          elementId,
          languages: availableLanguages,
        },
      })
    );
  }

  showProgress(elementId, message) {
    const element = document.querySelector(`[data-element-id="${elementId}"]`);
    if (!element) return;

    // Add progress overlay
    const overlay = document.createElement('div');
    overlay.className = 'translation-progress-overlay';
    overlay.innerHTML = `
            <div class="progress-spinner"></div>
            <span>${message}</span>
        `;
    element.style.position = 'relative';
    element.appendChild(overlay);
  }

  hideProgress(elementId) {
    const element = document.querySelector(`[data-element-id="${elementId}"]`);
    if (!element) return;

    const overlay = element.querySelector('.translation-progress-overlay');
    if (overlay) {
      overlay.remove();
    }
  }

  showNotification(message, type = 'info') {
    // Create or get notification container
    let container = document.getElementById('translation-notifications');
    if (!container) {
      container = document.createElement('div');
      container.id = 'translation-notifications';
      container.className = 'translation-notifications';
      document.body.appendChild(container);
    }

    // Create notification
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.remove()">×</button>
        `;

    container.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  getNotificationIcon(type) {
    const icons = {
      success: 'check-circle',
      error: 'exclamation-circle',
      warning: 'exclamation-triangle',
      info: 'info-circle',
    };
    return icons[type] || icons.info;
  }

  getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) return token.value;
    return '';
  }

  destroy() {
    // Clean up
    if (this.healthCheckInterval) {
      clearInterval(this.healthCheckInterval);
    }

    // Remove event listeners
    document.removeEventListener('pagebuilder:translate-element', this.handleTranslateRequest);
    document.removeEventListener('pagebuilder:translate-page', this.handlePageTranslation);
  }
}

// Initialize translation manager when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.translationManager = new TranslationManager();
});
