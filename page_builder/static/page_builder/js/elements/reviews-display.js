/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * ReviewsCarousel - Carousel navigation for reviews display element.
 * Handles sliding with transform, prev/next arrows, dot indicators, autoplay.
 */
class ReviewsCarousel {
    constructor(element) {
        this.element = element;
        this.track = element.querySelector('.reviews-display__carousel-track');
        this.slides = element.querySelectorAll('.reviews-display__card');
        this.prevBtn = element.querySelector('.reviews-display__carousel-arrow--prev');
        this.nextBtn = element.querySelector('.reviews-display__carousel-arrow--next');
        this.dotsContainer = element.querySelector('.reviews-display__carousel-dots');

        if (!this.track || this.slides.length === 0) return;

        this.config = {
            autoplay: element.dataset.autoplay === 'true',
            interval: (parseInt(element.dataset.interval) || 5) * 1000,
            perView: parseInt(element.dataset.perView) || 3
        };
        this.currentIndex = 0;
        this.autoplayTimer = null;
        this.totalSlides = this.slides.length;

        this.init();
    }

    init() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }

        this.element.addEventListener('mouseenter', () => this.stopAutoplay());
        this.element.addEventListener('mouseleave', () => this.startAutoplay());

        window.addEventListener('resize', () => {
            this.currentIndex = Math.min(this.currentIndex, this.getMaxIndex());
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
        const gapPx = 24; // 1.5rem
        const trackWidth = this.track.offsetWidth || 1;
        const gapPercent = gapPx * 100 / trackWidth;
        const offset = this.currentIndex * (slideWidth + gapPercent);
        this.track.style.transform = `translateX(-${offset}%)`;
        this.updateDots();
        this.updateButtons();
    }

    updateButtons() {
        const maxIndex = this.getMaxIndex();
        if (this.prevBtn) this.prevBtn.disabled = this.currentIndex === 0;
        if (this.nextBtn) this.nextBtn.disabled = this.currentIndex >= maxIndex;
    }

    updateDots() {
        if (!this.dotsContainer) return;
        const perView = this.getPerView();
        const numDots = Math.max(1, this.totalSlides - perView + 1);

        if (this.dotsContainer.children.length !== numDots) {
            this.dotsContainer.innerHTML = '';
            for (let i = 0; i < numDots; i++) {
                const dot = document.createElement('button');
                dot.className = 'reviews-display__carousel-dot';
                dot.setAttribute('aria-label', `Slide ${i + 1}`);
                dot.addEventListener('click', () => this.goTo(i));
                this.dotsContainer.appendChild(dot);
            }
        }

        this.dotsContainer.querySelectorAll('.reviews-display__carousel-dot').forEach((dot, i) => {
            dot.classList.toggle('reviews-display__carousel-dot--active', i === this.currentIndex);
        });
    }

    goTo(index) {
        this.currentIndex = Math.max(0, Math.min(index, this.getMaxIndex()));
        this.updateCarousel();
    }

    next() {
        const maxIndex = this.getMaxIndex();
        if (this.currentIndex < maxIndex) {
            this.currentIndex++;
        } else {
            this.currentIndex = 0;
        }
        this.updateCarousel();
    }

    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
        } else {
            this.currentIndex = this.getMaxIndex();
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
}


/**
 * ReviewForm - Handles the "Write a Review" modal and form submission.
 * Submits to /api/catalog/reviews/ via AJAX.
 */
class ReviewForm {
    constructor(element) {
        this.element = element;
        this.modal = element.querySelector('[data-review-modal]');
        this.form = element.querySelector('[data-review-form]');

        if (!this.modal || !this.form) return;

        this.productId = this.form.dataset.productId;
        this.selectedRating = 0;
        this.submitting = false;

        this.successMsg = this.form.querySelector('.reviews-display__form-message--success');
        this.errorMsg = this.form.querySelector('.reviews-display__form-message--error');
        this.loginMsg = this.form.querySelector('.reviews-display__form-message--login');

        this.init();
    }

    init() {
        // Open modal buttons
        this.element.querySelectorAll('[data-action="open-review-modal"]').forEach(btn => {
            btn.addEventListener('click', () => this.openModal());
        });

        // Close modal buttons
        this.element.querySelectorAll('[data-action="close-review-modal"]').forEach(btn => {
            btn.addEventListener('click', () => this.closeModal());
        });

        // Escape key closes modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.modal.hidden) {
                this.closeModal();
            }
        });

        // Star rating interaction
        const starInput = this.form.querySelector('[data-star-input]');
        if (starInput) {
            const starBtns = starInput.querySelectorAll('.reviews-display__star-btn');
            starBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    this.selectedRating = parseInt(btn.dataset.rating);
                    this.updateStars(starBtns, this.selectedRating);
                });
                btn.addEventListener('mouseenter', () => {
                    this.updateStars(starBtns, parseInt(btn.dataset.rating));
                });
            });
            starInput.addEventListener('mouseleave', () => {
                this.updateStars(starBtns, this.selectedRating);
            });
        }

        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    updateStars(buttons, rating) {
        buttons.forEach(btn => {
            const r = parseInt(btn.dataset.rating);
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = r <= rating ? 'fas fa-star' : 'far fa-star';
            }
        });
    }

    openModal() {
        this.modal.hidden = false;
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.modal.hidden = true;
        document.body.style.overflow = '';
    }

    hideMessages() {
        if (this.successMsg) this.successMsg.hidden = true;
        if (this.errorMsg) this.errorMsg.hidden = true;
        if (this.loginMsg) this.loginMsg.hidden = true;
    }

    getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) return meta.content;
        const input = this.form.querySelector('[name="csrfmiddlewaretoken"]');
        if (input) return input.value;
        return '';
    }

    async handleSubmit(e) {
        e.preventDefault();
        if (this.submitting) return;

        this.hideMessages();

        // Validate
        if (!this.selectedRating) {
            this.showError('Please select a rating.');
            return;
        }

        const title = this.form.querySelector('[name="title"]').value.trim();
        const comment = this.form.querySelector('[name="comment"]').value.trim();
        if (!title || !comment) {
            this.showError('Please fill in all required fields.');
            return;
        }

        this.submitting = true;
        const submitBtn = this.form.querySelector('.reviews-display__form-submit');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.dataset.originalText = submitBtn.textContent;
            submitBtn.textContent = submitBtn.textContent.trim() + '...';
        }

        try {
            const response = await fetch('/api/catalog/reviews/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    product: parseInt(this.productId),
                    rating: this.selectedRating,
                    title: title,
                    comment: comment
                })
            });

            if (response.status === 201) {
                if (this.successMsg) this.successMsg.hidden = false;
                this.form.reset();
                this.selectedRating = 0;
                const starBtns = this.form.querySelectorAll('.reviews-display__star-btn');
                this.updateStars(starBtns, 0);
                // Close modal after a brief delay
                setTimeout(() => this.closeModal(), 3000);
            } else if (response.status === 401 || response.status === 403) {
                // Check if it's an auth issue or a permission issue
                const data = await response.json().catch(() => ({}));
                if (response.status === 401 || (data.detail && data.detail.includes('credentials'))) {
                    if (this.loginMsg) this.loginMsg.hidden = false;
                } else {
                    this.showError(data.detail || data.error || 'You do not have permission to perform this action.');
                }
            } else if (response.status === 400) {
                const data = await response.json().catch(() => ({}));
                // Handle validation errors
                const errors = [];
                for (const [key, value] of Object.entries(data)) {
                    if (Array.isArray(value)) {
                        errors.push(...value);
                    } else if (typeof value === 'string') {
                        errors.push(value);
                    }
                }
                this.showError(errors[0] || 'Please check your input and try again.');
            } else {
                this.showError('Something went wrong. Please try again.');
            }
        } catch {
            this.showError('Something went wrong. Please try again.');
        } finally {
            this.submitting = false;
            if (submitBtn) {
                submitBtn.disabled = false;
                if (submitBtn.dataset.originalText) {
                    submitBtn.textContent = submitBtn.dataset.originalText;
                }
            }
        }
    }

    showError(message) {
        if (this.errorMsg) {
            this.errorMsg.textContent = message;
            this.errorMsg.hidden = false;
        }
    }
}


// Self-initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize carousels
    document.querySelectorAll('[data-reviews-carousel]').forEach(element => {
        new ReviewsCarousel(element);
    });
    // Initialize review forms
    document.querySelectorAll('[data-reviews-display]').forEach(element => {
        if (element.querySelector('[data-review-modal]')) {
            new ReviewForm(element);
        }
    });
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ReviewsCarousel, ReviewForm };
}
