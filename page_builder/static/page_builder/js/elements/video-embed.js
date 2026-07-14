/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * VideoEmbed - Video embed with lazy loading and consent handling
 * Handles YouTube, Vimeo, and self-hosted video embeds with privacy features
 */
class VideoEmbed {
  constructor(element) {
    this.element = element;
    this.wrapper = element.querySelector('.video-embed__wrapper');
    this.consent = element.querySelector('.video-embed__consent');
    this.iframe = element.querySelector('.video-embed__iframe');

    this.config = this.parseConfig();
    this.init();
  }

  /**
   * Parse configuration from data attributes
   */
  parseConfig() {
    return {
      lazyLoad: this.element.dataset.lazy !== 'false',
      showConsent: this.element.dataset.consent === 'true',
      source: this.element.dataset.source || 'youtube',
    };
  }

  /**
   * Initialize video embed functionality
   */
  init() {
    if (this.config.showConsent && this.consent) {
      this.setupConsent();
    } else if (this.config.lazyLoad) {
      this.setupLazyLoading();
    }
  }

  /**
   * Setup consent overlay
   */
  setupConsent() {
    const consentBtn = this.consent.querySelector('.video-embed__consent-button');
    if (consentBtn) {
      consentBtn.addEventListener('click', () => {
        this.consent.hidden = true;
        if (this.wrapper) {
          this.wrapper.hidden = false;
        }
        this.loadVideo();
      });
    }
  }

  /**
   * Setup lazy loading with IntersectionObserver
   */
  setupLazyLoading() {
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(
        entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              this.loadVideo();
              observer.disconnect();
            }
          });
        },
        { rootMargin: '100px' }
      );

      observer.observe(this.element);
    } else {
      // Fallback for browsers without IntersectionObserver
      this.loadVideo();
    }
  }

  /**
   * Load the video by setting iframe src
   */
  loadVideo() {
    if (this.iframe && this.iframe.dataset.src && !this.iframe.src) {
      this.iframe.src = this.iframe.dataset.src;
    }
  }
}

/**
 * Initialize all video embed elements on page load
 */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-video-embed]').forEach(element => {
    new VideoEmbed(element);
  });
});

// Export for manual initialization
if (typeof module !== 'undefined' && module.exports) {
  module.exports = VideoEmbed;
}
