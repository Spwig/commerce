/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * ProductCarousel - Product showcase carousel element
 * Handles carousel navigation, autoplay, touch/swipe, and add-to-cart functionality
 */
class ProductCarousel {
    constructor(element) {
        this.element = element;
        this.carousel = element.querySelector('.product-carousel__carousel');

        if (!this.carousel) {
            return;
        }

        this.track = this.carousel.querySelector('.carousel__track');
        this.slides = this.carousel.querySelectorAll('.carousel__slide');
        this.container = this.carousel.closest('.carousel-container');
        this.prevBtn = this.container?.querySelector('.carousel__prev');
        this.nextBtn = this.container?.querySelector('.carousel__next');
        this.dotsContainer = this.container?.parentElement.querySelector('.carousel__indicators--bottom');

        this.config = this.parseConfig();
        this.currentIndex = 0;
        this.autoPlayTimer = null;
        this.totalSlides = this.slides.length;
        this.maxIndex = Math.max(0, this.totalSlides - this.config.productsPerView);

        // Touch/swipe state
        this.startX = 0;
        this.currentX = 0;
        this.isDragging = false;

        this.init();
    }

    parseConfig() {
        return {
            productsPerView: parseInt(this.carousel.dataset.productsPerView) || 4,
            autoPlay: this.carousel.dataset.autoPlay === 'true',
            playInterval: parseInt(this.carousel.dataset.playInterval) || 4,
            infinite: this.carousel.dataset.infinite === 'true',
            addedText: this.element.dataset.addedText || 'Added!'
        };
    }

    init() {
        // Set up navigation buttons
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => {
                this.prevSlide();
                this.restartAutoPlay();
            });
        }

        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => {
                this.nextSlide();
                this.restartAutoPlay();
            });
        }

        // Pause autoplay on hover
        this.carousel.addEventListener('mouseenter', () => this.stopAutoPlay());
        this.carousel.addEventListener('mouseleave', () => this.startAutoPlay());

        // Touch/swipe support
        this.carousel.addEventListener('touchstart', (e) => this.handleTouchStart(e));
        this.carousel.addEventListener('touchmove', (e) => this.handleTouchMove(e));
        this.carousel.addEventListener('touchend', () => this.handleTouchEnd());

        // Resize handler
        window.addEventListener('resize', () => this.updateSlideWidths());

        // Add to cart button handling
        this.element.addEventListener('click', (e) => this.handleAddToCart(e));

        // Initialize
        this.updateSlideWidths();
        this.createDots();
        this.startAutoPlay();
    }

    getVisibleSlides() {
        let slidesVisible = this.config.productsPerView;

        // Responsive breakpoints
        if (window.innerWidth < 640) {
            slidesVisible = 1;
        } else if (window.innerWidth < 768) {
            slidesVisible = Math.min(2, this.config.productsPerView);
        } else if (window.innerWidth < 1024) {
            slidesVisible = Math.min(3, this.config.productsPerView);
        }

        return slidesVisible;
    }

    updateSlideWidths() {
        const containerWidth = this.carousel.offsetWidth;
        const slidesVisible = this.getVisibleSlides();
        const slideWidth = (containerWidth - (slidesVisible - 1) * 16) / slidesVisible; // 16px gap

        this.slides.forEach(slide => {
            slide.style.width = slideWidth + 'px';
            slide.style.marginRight = '1rem';
        });

        // Recalculate maxIndex based on visible slides
        this.maxIndex = Math.max(0, this.totalSlides - slidesVisible);

        // Ensure currentIndex is still valid
        if (this.currentIndex > this.maxIndex) {
            this.currentIndex = this.maxIndex;
        }

        this.updateCarouselPosition();
    }

    updateCarouselPosition() {
        const slideWidth = this.slides[0]?.offsetWidth || 0;
        const gap = 16; // 1rem in pixels
        const offset = this.currentIndex * (slideWidth + gap);
        this.track.style.transform = `translateX(-${offset}px)`;

        // Update button states
        if (this.prevBtn) {
            this.prevBtn.disabled = !this.config.infinite && this.currentIndex === 0;
        }
        if (this.nextBtn) {
            this.nextBtn.disabled = !this.config.infinite && this.currentIndex >= this.maxIndex;
        }

        // Update dots
        this.updateDots();
    }

    goToSlide(index) {
        if (this.config.infinite) {
            if (index < 0) {
                this.currentIndex = this.maxIndex;
            } else if (index > this.maxIndex) {
                this.currentIndex = 0;
            } else {
                this.currentIndex = index;
            }
        } else {
            this.currentIndex = Math.max(0, Math.min(index, this.maxIndex));
        }
        this.updateCarouselPosition();
    }

    nextSlide() {
        this.goToSlide(this.currentIndex + 1);
    }

    prevSlide() {
        this.goToSlide(this.currentIndex - 1);
    }

    createDots() {
        if (!this.dotsContainer) return;

        this.dotsContainer.innerHTML = '';
        const slidesVisible = this.getVisibleSlides();
        const dotsNeeded = Math.ceil(this.totalSlides / slidesVisible);

        for (let i = 0; i < dotsNeeded; i++) {
            const dot = document.createElement('button');
            dot.className = 'carousel__indicator';
            dot.addEventListener('click', () => this.goToSlide(i * slidesVisible));
            this.dotsContainer.appendChild(dot);
        }

        this.updateDots();
    }

    updateDots() {
        if (!this.dotsContainer) return;

        const dots = this.dotsContainer.querySelectorAll('.carousel__indicator');
        const slidesVisible = this.getVisibleSlides();
        const activeDotIndex = Math.floor(this.currentIndex / slidesVisible);

        dots.forEach((dot, index) => {
            dot.classList.toggle('carousel__indicator--active', index === activeDotIndex);
        });
    }

    startAutoPlay() {
        if (!this.config.autoPlay) return;

        this.autoPlayTimer = setInterval(() => {
            this.nextSlide();
        }, this.config.playInterval * 1000);
    }

    stopAutoPlay() {
        if (this.autoPlayTimer) {
            clearInterval(this.autoPlayTimer);
            this.autoPlayTimer = null;
        }
    }

    restartAutoPlay() {
        this.stopAutoPlay();
        this.startAutoPlay();
    }

    handleTouchStart(e) {
        this.startX = e.touches[0].clientX;
        this.isDragging = true;
        this.stopAutoPlay();
    }

    handleTouchMove(e) {
        if (!this.isDragging) return;
        this.currentX = e.touches[0].clientX;
    }

    handleTouchEnd() {
        if (!this.isDragging) return;

        const deltaX = this.startX - this.currentX;
        if (Math.abs(deltaX) > 50) { // Minimum swipe distance
            if (deltaX > 0) {
                this.nextSlide();
            } else {
                this.prevSlide();
            }
        }

        this.isDragging = false;
        this.startAutoPlay();
    }

    handleAddToCart(e) {
        const btn = e.target.closest('.add-to-cart-btn');
        if (!btn) return;

        const sku = btn.dataset.sku;
        const name = btn.dataset.name;
        const price = btn.dataset.price;

        // Dispatch custom event for cart integration
        const event = new CustomEvent('product:addToCart', {
            bubbles: true,
            detail: { sku, name, price }
        });
        this.element.dispatchEvent(event);

        // Visual feedback
        const originalText = btn.textContent;
        btn.textContent = this.config.addedText;
        btn.classList.remove('btn--primary');
        btn.classList.add('btn--success');

        setTimeout(() => {
            btn.textContent = originalText;
            btn.classList.remove('btn--success');
            btn.classList.add('btn--primary');
        }, 2000);
    }

    destroy() {
        this.stopAutoPlay();
        window.removeEventListener('resize', () => this.updateSlideWidths());
    }
}

// Self-initialize: Find all product carousel elements and create instances
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-product-carousel]').forEach(element => {
        new ProductCarousel(element);
    });
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProductCarousel;
}
