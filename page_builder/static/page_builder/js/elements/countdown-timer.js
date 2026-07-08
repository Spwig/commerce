/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * CountdownTimer - Countdown timer handler for sales, launches, and events
 * Supports date countdown, fixed duration, and daily recurring modes
 */
class CountdownTimer {
    constructor(element) {
        this.element = element;
        this.config = this.parseConfig();
        this.display = element.querySelector('.countdown-timer__display');
        this.expiredEl = element.querySelector('.countdown-timer__expired');
        this.units = {
            days: element.querySelector('[data-unit="days"] .countdown-timer__number'),
            hours: element.querySelector('[data-unit="hours"] .countdown-timer__number'),
            minutes: element.querySelector('[data-unit="minutes"] .countdown-timer__number'),
            seconds: element.querySelector('[data-unit="seconds"] .countdown-timer__number')
        };
        this.intervalId = null;
        this.init();
    }

    parseConfig() {
        return {
            mode: this.element.dataset.countdownMode || 'date',
            targetDate: this.element.dataset.targetDate,
            durationHours: parseInt(this.element.dataset.durationHours) || 24,
            dailyEndTime: this.element.dataset.dailyEndTime || '23:59',
            timezone: this.element.dataset.timezone || 'local',
            onExpire: this.element.dataset.onExpire || 'message',
            redirectUrl: this.element.dataset.redirectUrl,
            redirectDelay: parseInt(this.element.dataset.redirectDelay) || 3
        };
    }

    init() {
        this.tick();
    }

    getTargetTime() {
        let target;

        if (this.config.mode === 'date' && this.config.targetDate) {
            target = new Date(this.config.targetDate);
            if (this.config.timezone !== 'local' && this.config.timezone !== 'UTC') {
                // Adjust for timezone if specified
                try {
                    const localStr = target.toLocaleString('en-US', { timeZone: this.config.timezone });
                    target = new Date(localStr);
                } catch (e) {
                    // Fallback to original date
                }
            }
        } else if (this.config.mode === 'duration') {
            const storageKey = 'countdown_' + (this.element.id || this.element.dataset.elementId || Math.random().toString(36).substr(2, 9));
            let startTime = localStorage.getItem(storageKey);
            if (!startTime) {
                startTime = Date.now();
                localStorage.setItem(storageKey, startTime);
            }
            target = new Date(parseInt(startTime) + (this.config.durationHours * 60 * 60 * 1000));
        } else if (this.config.mode === 'daily') {
            const [hours, minutes] = this.config.dailyEndTime.split(':').map(Number);
            target = new Date();
            target.setHours(hours, minutes, 0, 0);
            if (target <= new Date()) {
                target.setDate(target.getDate() + 1);
            }
        }

        return target;
    }

    updateDisplay(days, hours, minutes, seconds) {
        if (this.units.days) this.units.days.textContent = String(days).padStart(2, '0');
        if (this.units.hours) this.units.hours.textContent = String(hours).padStart(2, '0');
        if (this.units.minutes) this.units.minutes.textContent = String(minutes).padStart(2, '0');
        if (this.units.seconds) this.units.seconds.textContent = String(seconds).padStart(2, '0');
    }

    handleExpiry() {
        switch (this.config.onExpire) {
            case 'hide':
                this.element.style.display = 'none';
                break;
            case 'message':
                if (this.display) this.display.style.display = 'none';
                if (this.expiredEl) this.expiredEl.style.display = 'block';
                break;
            case 'redirect':
                if (this.config.redirectUrl) {
                    setTimeout(() => {
                        window.location.href = this.config.redirectUrl;
                    }, this.config.redirectDelay * 1000);
                }
                if (this.display) this.display.style.display = 'none';
                if (this.expiredEl) this.expiredEl.style.display = 'block';
                break;
            case 'zeros':
                this.updateDisplay(0, 0, 0, 0);
                break;
        }
    }

    tick() {
        const target = this.getTargetTime();
        if (!target) return;

        const now = new Date();
        const diff = target - now;

        if (diff <= 0) {
            this.handleExpiry();
            return;
        }

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        this.updateDisplay(days, hours, minutes, seconds);
        requestAnimationFrame(() => setTimeout(() => this.tick(), 1000));
    }

    destroy() {
        // Cleanup if needed
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
    }
}

// Self-initialize: Find all countdown timer elements and create instances
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-countdown-timer]').forEach(element => {
        new CountdownTimer(element);
    });
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CountdownTimer;
}
