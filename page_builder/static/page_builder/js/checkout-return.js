/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Checkout return page: polls payment intent status and transitions UI.
 * Reads intentId and orderNumber from <script type="application/json" id="checkout-return-data">.
 */
(function () {
    'use strict';

    var configEl = document.getElementById('checkout-return-data');
    var config = configEl ? JSON.parse(configEl.textContent) : {};

    var PaymentReturn = {
        intentId: config.intentId || '',
        orderNumber: config.orderNumber || '',
        maxAttempts: 30,
        attempt: 0,
        pollInterval: 2000,

        init: function () {
            if (!this.intentId) {
                this.intentId = sessionStorage.getItem('payment_intent_id') || '';
            }
            if (!this.orderNumber) {
                this.orderNumber = sessionStorage.getItem('order_number') || '';
            }

            if (!this.intentId) {
                this.showFailed();
                return;
            }

            this.poll();
        },

        poll: function () {
            var self = this;
            self.attempt++;
            fetch('/api/payments/intents/' + self.intentId + '/', {
                headers: { 'Accept': 'application/json' }
            })
            .then(function (response) {
                if (!response.ok) throw new Error('HTTP ' + response.status);
                return response.json();
            })
            .then(function (data) {
                if (data.status === 'succeeded') {
                    self.showSuccess(data.order_number || self.orderNumber);
                    return;
                }
                if (data.status === 'failed' || data.status === 'canceled') {
                    self.showFailed();
                    return;
                }
                if (self.attempt >= self.maxAttempts) {
                    self.showTimeout();
                    return;
                }
                setTimeout(function () { self.poll(); }, self.pollInterval);
            })
            .catch(function (err) {
                console.error('Payment poll error:', err);
                if (self.attempt >= self.maxAttempts) {
                    self.showTimeout();
                    return;
                }
                setTimeout(function () { self.poll(); }, self.pollInterval);
            });
        },

        showSuccess: function (orderNumber) {
            var processing = document.getElementById('return-processing');
            var success = document.getElementById('return-success');
            if (processing) processing.hidden = true;
            if (success) success.hidden = false;
            sessionStorage.removeItem('payment_intent_id');
            sessionStorage.removeItem('order_number');
            var lang = document.documentElement.lang || 'en';
            setTimeout(function () {
                window.location.href = '/' + lang + '/checkout/confirmation/' + orderNumber + '/';
            }, 1500);
        },

        showFailed: function () {
            var processing = document.getElementById('return-processing');
            var failed = document.getElementById('return-failed');
            if (processing) processing.hidden = true;
            if (failed) failed.hidden = false;
            sessionStorage.removeItem('payment_intent_id');
            sessionStorage.removeItem('order_number');
        },

        showTimeout: function () {
            var processing = document.getElementById('return-processing');
            var timeout = document.getElementById('return-timeout');
            if (processing) processing.hidden = true;
            if (timeout) timeout.hidden = false;
            if (this.orderNumber) {
                var el = document.getElementById('return-order-number');
                if (el) el.textContent = 'Order #' + this.orderNumber;
            }
        }
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { PaymentReturn.init(); });
    } else {
        PaymentReturn.init();
    }
})();
