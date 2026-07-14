/* Product Grid Element - Multi-layout support (grid, list, carousel, masonry, featured) */
(function () {
  'use strict';

  function init() {
    document
      .querySelectorAll('.product-grid-section[data-element-type="product_grid"]')
      .forEach(initProductGrid);
  }

  function initProductGrid(section) {
    const layout = section.dataset.layout || 'grid';

    // Initialize product card interactions for all layouts
    initProductCards(section);

    // Layout-specific initialization
    if (layout === 'carousel') {
      initCarouselLayout(section);
    }
  }

  /**
   * Initialize product card interactions (add to cart, wishlist, quick view)
   * Shared across all layouts
   */
  function initProductCards(section) {
    // Add to cart buttons
    section.addEventListener('click', function (e) {
      const addBtn = e.target.closest('.product-card__add-btn');
      if (addBtn) {
        e.preventDefault();
        const productId = addBtn.dataset.productId;
        if (!productId) return;
        addBtn.dispatchEvent(
          new CustomEvent('product:addToCart', {
            bubbles: true,
            detail: { productId: parseInt(productId), button: addBtn },
          })
        );
      }

      // Quick view buttons
      const qvBtn = e.target.closest(
        '.product-card__quickview-btn, .product-card__action-btn--quickview'
      );
      if (qvBtn) {
        e.preventDefault();
        const productSlug = qvBtn.dataset.productSlug;
        if (productSlug) {
          qvBtn.dispatchEvent(
            new CustomEvent('product:quickView', {
              bubbles: true,
              detail: { productSlug },
            })
          );
        }
      }

      // Wishlist buttons
      const wishBtn = e.target.closest('.product-card__action-btn--wishlist');
      if (wishBtn) {
        e.preventDefault();
        const productId = wishBtn.dataset.productId;
        if (productId) {
          wishBtn.dispatchEvent(
            new CustomEvent('product:toggleWishlist', {
              bubbles: true,
              detail: { productId: parseInt(productId), button: wishBtn },
            })
          );
        }
      }
    });
  }

  /**
   * Initialize carousel layout
   * Adapts category-carousel.js logic for the product grid element context
   */
  function initCarouselLayout(section) {
    // Header-level nav arrows
    const headerPrev = section.querySelector('.product-grid-section__arrow--prev');
    const headerNext = section.querySelector('.product-grid-section__arrow--next');

    section.querySelectorAll('.cat-carousel').forEach(function (carousel) {
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

      function getSlideWidth() {
        if (slides.length === 0) return 0;
        return slides[0].offsetWidth + parseFloat(getComputedStyle(track).gap || 0);
      }

      function getVisibleCount() {
        const trackWidth = track.offsetWidth;
        if (trackWidth < 640) return 1;
        if (trackWidth < 1024) return Math.min(2, config.slidesPerView);
        return config.slidesPerView;
      }

      function getPageCount() {
        return Math.max(1, Math.ceil(slides.length / getVisibleCount()));
      }

      function scrollToIndex(index) {
        const maxIndex = slides.length - getVisibleCount();
        if (config.infinite) {
          currentIndex = index < 0 ? maxIndex : index > maxIndex ? 0 : index;
        } else {
          currentIndex = Math.max(0, Math.min(index, maxIndex));
        }
        track.scrollTo({ left: currentIndex * getSlideWidth(), behavior: 'smooth' });
        updateArrows();
        updateProgress();
      }

      function updateArrows() {
        [prevBtn, headerPrev].forEach(function (btn) {
          if (!btn) return;
          if (!config.infinite) {
            btn.disabled = currentIndex <= 0;
            btn.style.opacity = btn.disabled ? '0.3' : '1';
          }
        });
        [nextBtn, headerNext].forEach(function (btn) {
          if (!btn) return;
          if (!config.infinite) {
            btn.disabled = currentIndex >= slides.length - getVisibleCount();
            btn.style.opacity = btn.disabled ? '0.3' : '1';
          }
        });
      }

      function updateProgress() {
        if (!progressContainer) return;
        const fillEl = progressContainer.querySelector('.cat-carousel__progress-fill');
        const labelEl = progressContainer.querySelector('.cat-carousel__progress-label');
        const pageCount = getPageCount();
        const activePage = Math.floor(currentIndex / getVisibleCount());
        const pct = pageCount > 1 ? ((activePage + 1) / pageCount) * 100 : 100;
        if (fillEl) fillEl.style.width = pct + '%';
        if (labelEl) labelEl.textContent = activePage + 1 + ' / ' + pageCount;
      }

      function buildProgress() {
        if (!progressContainer) return;
        progressContainer.style.display = getPageCount() <= 1 ? 'none' : '';
        updateProgress();
      }

      // Navigation click handlers
      [prevBtn, headerPrev].forEach(function (btn) {
        if (btn)
          btn.addEventListener('click', function () {
            scrollToIndex(currentIndex - getVisibleCount());
            resetAutoplay();
          });
      });
      [nextBtn, headerNext].forEach(function (btn) {
        if (btn)
          btn.addEventListener('click', function () {
            scrollToIndex(currentIndex + getVisibleCount());
            resetAutoplay();
          });
      });

      // Scroll sync
      let scrollTimeout;
      track.addEventListener('scroll', function () {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function () {
          const sw = getSlideWidth();
          if (sw > 0) {
            currentIndex = Math.round(track.scrollLeft / sw);
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

      carousel.addEventListener('mouseenter', stopAutoplay);
      carousel.addEventListener('mouseleave', startAutoplay);

      // Touch
      let touchStartX = 0;
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
          const diff = touchStartX - e.changedTouches[0].screenX;
          if (Math.abs(diff) > 50) scrollToIndex(diff > 0 ? currentIndex + 1 : currentIndex - 1);
          startAutoplay();
        },
        { passive: true }
      );

      // Keyboard
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

      // Responsive
      let resizeTimer;
      window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
          buildProgress();
          updateArrows();
        }, 200);
      });

      // Reduced motion
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) config.autoplay = false;

      // Init
      buildProgress();
      updateArrows();
      startAutoplay();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
