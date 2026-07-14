/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Category Carousel - Horizontal product slider with arrows, dots, and autoplay.
 * Uses CSS scroll-snap for smooth scrolling with JS-powered navigation.
 */
(function () {
  'use strict';

  document.querySelectorAll('.cat-carousel').forEach(initCarousel);

  function initCarousel(carousel) {
    const track = carousel.querySelector('.cat-carousel__track');
    if (!track || !track.children.length) return;

    const slides = Array.from(track.querySelectorAll('.cat-carousel__slide'));
    if (slides.length === 0) return;

    const config = {
      slidesPerView: parseInt(carousel.dataset.slidesPerView) || 4,
      autoplay: carousel.dataset.autoplay === 'true',
      autoplaySpeed: parseInt(carousel.dataset.autoplaySpeed) || 5000,
      infinite: carousel.dataset.infinite === 'true',
    };

    const prevBtn = carousel.querySelector('.cat-carousel__arrow--prev');
    const nextBtn = carousel.querySelector('.cat-carousel__arrow--next');
    const progressContainer = carousel.querySelector('.cat-carousel__progress');

    let currentIndex = 0;
    let autoplayTimer = null;

    // Calculate slide width based on track
    function getSlideWidth() {
      if (slides.length === 0) return 0;
      return slides[0].offsetWidth + parseFloat(getComputedStyle(track).gap || 0);
    }

    // Total number of "pages" for dot navigation
    function getPageCount() {
      return Math.max(1, Math.ceil(slides.length / getVisibleCount()));
    }

    // How many slides visible at once
    function getVisibleCount() {
      const trackWidth = track.offsetWidth;
      if (trackWidth < 640) return 1;
      if (trackWidth < 1024) return Math.min(2, config.slidesPerView);
      return config.slidesPerView;
    }

    // Scroll to a specific index
    function scrollToIndex(index) {
      const maxIndex = slides.length - getVisibleCount();
      if (config.infinite) {
        currentIndex = index < 0 ? maxIndex : index > maxIndex ? 0 : index;
      } else {
        currentIndex = Math.max(0, Math.min(index, maxIndex));
      }

      const slideWidth = getSlideWidth();
      track.scrollTo({
        left: currentIndex * slideWidth,
        behavior: 'smooth',
      });

      updateArrows();
      updateProgress();
    }

    // Arrow state
    function updateArrows() {
      if (!prevBtn || !nextBtn) return;
      if (!config.infinite) {
        prevBtn.disabled = currentIndex <= 0;
        nextBtn.disabled = currentIndex >= slides.length - getVisibleCount();
        prevBtn.style.opacity = prevBtn.disabled ? '0.3' : '1';
        nextBtn.style.opacity = nextBtn.disabled ? '0.3' : '1';
      }
    }

    // Progress indicator (page position bar + label)
    function buildProgress() {
      if (!progressContainer) return;
      const pageCount = getPageCount();
      progressContainer.style.display = pageCount <= 1 ? 'none' : '';
      updateProgress();
    }

    function updateProgress() {
      if (!progressContainer) return;
      const fillEl = progressContainer.querySelector('.cat-carousel__progress-fill');
      const labelEl = progressContainer.querySelector('.cat-carousel__progress-label');
      const pageCount = getPageCount();
      const visibleCount = getVisibleCount();
      const activePage = Math.floor(currentIndex / visibleCount);
      const pct = pageCount > 1 ? ((activePage + 1) / pageCount) * 100 : 100;
      if (fillEl) fillEl.style.width = pct + '%';
      if (labelEl) labelEl.textContent = activePage + 1 + ' / ' + pageCount;
    }

    // Navigation
    if (prevBtn) {
      prevBtn.addEventListener('click', function () {
        scrollToIndex(currentIndex - getVisibleCount());
        resetAutoplay();
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        scrollToIndex(currentIndex + getVisibleCount());
        resetAutoplay();
      });
    }

    // Track scroll sync (when user scrolls manually)
    let scrollTimeout;
    track.addEventListener('scroll', function () {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(function () {
        const slideWidth = getSlideWidth();
        if (slideWidth > 0) {
          currentIndex = Math.round(track.scrollLeft / slideWidth);
          updateArrows();
          updateProgress();
        }
      }, 100);
    });

    // Autoplay
    function startAutoplay() {
      if (!config.autoplay) return;
      stopAutoplay();
      autoplayTimer = setInterval(function () {
        scrollToIndex(currentIndex + getVisibleCount());
      }, config.autoplaySpeed);
    }

    function stopAutoplay() {
      if (autoplayTimer) {
        clearInterval(autoplayTimer);
        autoplayTimer = null;
      }
    }

    function resetAutoplay() {
      stopAutoplay();
      startAutoplay();
    }

    // Pause on hover
    carousel.addEventListener('mouseenter', stopAutoplay);
    carousel.addEventListener('mouseleave', startAutoplay);

    // Touch/swipe support
    let touchStartX = 0;
    let touchEndX = 0;

    track.addEventListener(
      'touchstart',
      function (e) {
        touchStartX = e.changedTouches[0].screenX;
        stopAutoplay();
      },
      { passive: true }
    );

    track.addEventListener(
      'touchend',
      function (e) {
        touchEndX = e.changedTouches[0].screenX;
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 50) {
          if (diff > 0) {
            scrollToIndex(currentIndex + 1);
          } else {
            scrollToIndex(currentIndex - 1);
          }
        }
        startAutoplay();
      },
      { passive: true }
    );

    // Keyboard navigation
    carousel.setAttribute('tabindex', '0');
    carousel.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        scrollToIndex(currentIndex - 1);
        resetAutoplay();
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        scrollToIndex(currentIndex + 1);
        resetAutoplay();
      }
    });

    // Responsive rebuild
    let resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        buildProgress();
        updateArrows();
      }, 200);
    });

    // Reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (prefersReducedMotion.matches) {
      config.autoplay = false;
    }

    // Init
    buildProgress();
    updateArrows();
    startAutoplay();
  }
})();
