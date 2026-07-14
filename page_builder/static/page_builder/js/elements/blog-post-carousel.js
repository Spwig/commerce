/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * BlogPostCarousel - Blog posts carousel handler
 * Handles sliding carousel with autoplay and navigation
 */
class BlogPostCarousel {
  constructor(element) {
    this.element = element;
    this.track = element.querySelector('.blog-carousel__track');
    this.slides = element.querySelectorAll('.blog-carousel__slide');
    this.prevBtn = element.querySelector('.blog-carousel__arrow--prev');
    this.nextBtn = element.querySelector('.blog-carousel__arrow--next');
    this.dotsContainer = element.querySelector('.blog-carousel__dots');

    if (this.slides.length === 0) return;

    this.config = this.parseConfig();
    this.currentIndex = 0;
    this.autoplayTimer = null;
    this.totalSlides = this.slides.length;

    this.init();
  }

  parseConfig() {
    return {
      autoplay: this.element.dataset.autoplay === 'true',
      interval: parseInt(this.element.dataset.interval) * 1000 || 5000,
      infinite: this.element.dataset.infinite !== 'false',
      pauseOnHover: this.element.dataset.pauseHover !== 'false',
      perView: parseInt(this.element.dataset.perView) || 3,
    };
  }

  init() {
    if (this.prevBtn) {
      this.prevBtn.addEventListener('click', () => this.prev());
    }
    if (this.nextBtn) {
      this.nextBtn.addEventListener('click', () => this.next());
    }

    if (this.config.pauseOnHover) {
      this.element.addEventListener('mouseenter', () => this.stopAutoplay());
      this.element.addEventListener('mouseleave', () => this.startAutoplay());
    }

    window.addEventListener('resize', () => {
      this.currentIndex = Math.min(
        this.currentIndex,
        Math.max(0, this.totalSlides - this.getPerView())
      );
      this.updateCarousel();
    });

    this.updateCarousel();
    this.startAutoplay();
  }

  getPerView() {
    if (window.innerWidth <= 640) return 1;
    if (window.innerWidth <= 1024) return Math.min(this.config.perView, 2);
    return this.config.perView;
  }

  getMaxIndex() {
    return Math.max(0, this.totalSlides - this.getPerView());
  }

  updateCarousel() {
    const perView = this.getPerView();
    const slideWidth = 100 / perView;
    const gapPercent = (1.5 * 100) / this.track.offsetWidth;
    const offset = this.currentIndex * (slideWidth + gapPercent);
    this.track.style.transform = `translateX(-${offset}%)`;
    this.updateDots();
    this.updateButtons();
  }

  updateButtons() {
    const maxIndex = this.getMaxIndex();
    if (this.prevBtn) this.prevBtn.disabled = !this.config.infinite && this.currentIndex === 0;
    if (this.nextBtn)
      this.nextBtn.disabled = !this.config.infinite && this.currentIndex >= maxIndex;
  }

  updateDots() {
    if (!this.dotsContainer) return;
    const perView = this.getPerView();
    const numDots = Math.ceil(this.totalSlides / perView);

    if (this.dotsContainer.children.length !== numDots) {
      this.dotsContainer.innerHTML = '';
      for (let i = 0; i < numDots; i++) {
        const dot = document.createElement('button');
        dot.className = 'blog-carousel__dot';
        dot.addEventListener('click', () => this.goTo(i * perView));
        this.dotsContainer.appendChild(dot);
      }
    }

    const activeDot = Math.floor(this.currentIndex / perView);
    this.dotsContainer.querySelectorAll('.blog-carousel__dot').forEach((dot, i) => {
      dot.classList.toggle('blog-carousel__dot--active', i === activeDot);
    });
  }

  goTo(index) {
    const max = this.config.infinite ? this.totalSlides - 1 : this.getMaxIndex();
    this.currentIndex = Math.max(0, Math.min(index, max));
    this.updateCarousel();
  }

  next() {
    const maxIndex = this.getMaxIndex();
    if (this.currentIndex >= maxIndex && this.config.infinite) {
      this.currentIndex = 0;
    } else {
      this.currentIndex = Math.min(this.currentIndex + 1, maxIndex);
    }
    this.updateCarousel();
  }

  prev() {
    const maxIndex = this.getMaxIndex();
    if (this.currentIndex <= 0 && this.config.infinite) {
      this.currentIndex = maxIndex;
    } else {
      this.currentIndex = Math.max(this.currentIndex - 1, 0);
    }
    this.updateCarousel();
  }

  startAutoplay() {
    if (!this.config.autoplay) return;
    this.stopAutoplay();
    this.autoplayTimer = setInterval(() => this.next(), this.config.interval);
  }

  stopAutoplay() {
    if (this.autoplayTimer) {
      clearInterval(this.autoplayTimer);
      this.autoplayTimer = null;
    }
  }

  destroy() {
    this.stopAutoplay();
  }
}

// Self-initialize: Find all blog carousel elements and create instances
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-blog-post-carousel]').forEach(element => {
    new BlogPostCarousel(element);
  });
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BlogPostCarousel;
}
