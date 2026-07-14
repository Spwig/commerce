/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Gallery - Image gallery with lightbox, carousel, and masonry support
 * Handles lightbox popup, carousel sliding, and masonry layout
 */
class Gallery {
  constructor(element) {
    this.element = element;
    this.container = element.querySelector('.gallery__container');
    this.config = this.parseConfig();
    this.currentImageIndex = 0;
    this.currentSlide = 0;
    this.autoPlayInterval = null;

    this.init();
  }

  parseConfig() {
    return {
      layout: this.element.dataset.layout || 'grid',
      lightbox: this.element.dataset.lightbox === 'true',
      autoPlay: this.element.dataset.autoPlay === 'true',
      playInterval: parseInt(this.element.dataset.playInterval) || 5,
      columns: parseInt(this.element.dataset.columns) || 3,
    };
  }

  init() {
    if (this.config.lightbox) {
      this.initLightbox();
    }

    if (this.config.layout === 'carousel') {
      this.initCarousel();
    }

    if (this.config.layout === 'masonry') {
      this.initMasonry();
    }
  }

  // Lightbox functionality
  initLightbox() {
    this.galleryItems = this.element.querySelectorAll('.gallery__item[data-lightbox]');
    this.lightbox = document.getElementById('lightbox-modal');
    this.lightboxImage = document.getElementById('lightbox-image');
    this.lightboxCaption = document.getElementById('lightbox-caption');

    if (!this.lightbox || this.galleryItems.length === 0) return;

    // Click handlers for gallery items
    this.galleryItems.forEach((item, index) => {
      item.addEventListener('click', () => this.openLightbox(index));
    });

    // Close button
    const closeBtn = document.getElementById('lightbox-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.closeLightbox());
    }

    // Navigation buttons
    const nextBtn = document.getElementById('lightbox-next');
    const prevBtn = document.getElementById('lightbox-prev');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => this.nextImage());
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', () => this.prevImage());
    }

    // Keyboard navigation
    document.addEventListener('keydown', e => this.handleLightboxKeydown(e));

    // Close on background click
    this.lightbox.addEventListener('click', e => {
      if (e.target === this.lightbox) {
        this.closeLightbox();
      }
    });
  }

  openLightbox(index) {
    if (!this.lightbox) return;

    const item = this.galleryItems[index];
    const src = item.dataset.src;
    const alt = item.dataset.alt;
    const caption = item.querySelector('.gallery__item-text')?.textContent || '';

    this.lightboxImage.src = src;
    this.lightboxImage.alt = alt;
    if (this.lightboxCaption) {
      this.lightboxCaption.textContent = caption;
    }
    this.lightbox.classList.remove('hidden');
    this.lightbox.classList.add('modal--open');
    this.currentImageIndex = index;
    document.body.style.overflow = 'hidden';
  }

  closeLightbox() {
    if (!this.lightbox) return;

    this.lightbox.classList.add('hidden');
    this.lightbox.classList.remove('modal--open');
    document.body.style.overflow = 'auto';
  }

  nextImage() {
    if (!this.galleryItems) return;
    this.currentImageIndex = (this.currentImageIndex + 1) % this.galleryItems.length;
    this.openLightbox(this.currentImageIndex);
  }

  prevImage() {
    if (!this.galleryItems) return;
    this.currentImageIndex =
      (this.currentImageIndex - 1 + this.galleryItems.length) % this.galleryItems.length;
    this.openLightbox(this.currentImageIndex);
  }

  handleLightboxKeydown(e) {
    if (!this.lightbox || this.lightbox.classList.contains('hidden')) return;

    switch (e.key) {
      case 'Escape':
        this.closeLightbox();
        break;
      case 'ArrowRight':
        this.nextImage();
        break;
      case 'ArrowLeft':
        this.prevImage();
        break;
    }
  }

  // Carousel functionality
  initCarousel() {
    this.carousel = this.element.querySelector('.gallery__carousel .carousel__wrapper');
    this.slides = this.element.querySelectorAll('.carousel__slide');
    this.indicators = this.element.querySelectorAll('.carousel__indicator');
    this.prevBtn = this.element.querySelector('.carousel__prev');
    this.nextBtn = this.element.querySelector('.carousel__next');

    if (!this.slides || this.slides.length === 0) return;

    // Event listeners
    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', () => {
        this.nextSlide();
        this.resetAutoPlay();
      });
    }

    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', () => {
        this.prevSlide();
        this.resetAutoPlay();
      });
    }

    this.indicators.forEach((indicator, index) => {
      indicator.addEventListener('click', () => {
        this.showSlide(index);
        this.resetAutoPlay();
      });
    });

    // Pause on hover
    if (this.carousel) {
      this.carousel.addEventListener('mouseenter', () => this.stopAutoPlay());
      this.carousel.addEventListener('mouseleave', () => this.startAutoPlay());
    }

    // Start autoplay if enabled
    this.startAutoPlay();
  }

  showSlide(index) {
    this.slides.forEach((slide, i) => {
      slide.classList.toggle('carousel__slide--active', i === index);
    });
    this.indicators.forEach((indicator, i) => {
      indicator.classList.toggle('carousel__indicator--active', i === index);
    });
    this.currentSlide = index;
  }

  nextSlide() {
    this.showSlide((this.currentSlide + 1) % this.slides.length);
  }

  prevSlide() {
    this.showSlide((this.currentSlide - 1 + this.slides.length) % this.slides.length);
  }

  startAutoPlay() {
    if (!this.config.autoPlay) return;
    this.stopAutoPlay();
    this.autoPlayInterval = setInterval(() => this.nextSlide(), this.config.playInterval * 1000);
  }

  stopAutoPlay() {
    if (this.autoPlayInterval) {
      clearInterval(this.autoPlayInterval);
      this.autoPlayInterval = null;
    }
  }

  resetAutoPlay() {
    this.stopAutoPlay();
    this.startAutoPlay();
  }

  // Masonry layout
  initMasonry() {
    const grid = this.element.querySelector('.gallery__grid--masonry');
    if (!grid) return;

    const images = grid.querySelectorAll('.gallery__image');
    let loadedImages = 0;

    const applyMasonry = () => {
      grid.style.columnCount = this.config.columns;
      grid.style.columnGap = 'var(--space-4)';

      const items = grid.querySelectorAll('.gallery__item');
      items.forEach(item => {
        item.style.breakInside = 'avoid';
        item.style.marginBottom = 'var(--space-4)';
      });
    };

    const checkImagesLoaded = () => {
      loadedImages++;
      if (loadedImages === images.length) {
        applyMasonry();
      }
    };

    if (images.length === 0) {
      applyMasonry();
      return;
    }

    images.forEach(img => {
      if (img.complete) {
        checkImagesLoaded();
      } else {
        img.addEventListener('load', checkImagesLoaded);
      }
    });
  }

  destroy() {
    this.stopAutoPlay();
  }
}

// Self-initialize: Find all gallery elements and create instances
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-gallery]').forEach(element => {
    new Gallery(element);
  });
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Gallery;
}
