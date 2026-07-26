/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Gift card product form.
 *
 * Builds the gift_card_data payload for POST /api/cart/add/ with EXACTLY the
 * six keys GiftCardDataSerializer allows — the serializer rejects unknown
 * keys, strips nothing silently, and refuses markup in the message. The
 * client-side checks here mirror those rules for a good error experience;
 * the SERVER is the enforcement, and its messages render verbatim.
 *
 * scheduled_send_at is sent offset-aware (the serializer refuses naive
 * datetimes): the local datetime from the picker is converted through
 * Date.toISOString(), which carries the customer's own zone into UTC.
 */
(function () {
  'use strict';

  const form = document.getElementById('gift-card-form');
  const configEl = document.getElementById('gift-card-config');
  if (!form || !configEl) return;
  const config = JSON.parse(configEl.textContent);

  const denomButtons = Array.from(document.querySelectorAll('.gift-card-denom'));
  const customInput = document.getElementById('gc-custom-amount');
  const messageInput = document.getElementById('gc-message');
  const messageCount = document.getElementById('gc-message-count');
  const errorEl = document.getElementById('gc-form-error');
  const submitBtn = document.getElementById('gc-add-to-cart');

  let selectedDenomination = null;

  // A single implied value needs no choice; preselect it.
  if (
    config.denominationType !== 'custom' &&
    Array.isArray(config.denominations) &&
    config.denominations.length === 1
  ) {
    selectedDenomination = config.denominations[0];
    if (denomButtons[0]) denomButtons[0].classList.add('gift-card-denom--selected');
  }

  denomButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      denomButtons.forEach(b => b.classList.remove('gift-card-denom--selected'));
      btn.classList.add('gift-card-denom--selected');
      selectedDenomination = btn.dataset.amount;
      if (customInput) customInput.value = '';
    });
  });

  if (customInput) {
    customInput.addEventListener('input', () => {
      if (customInput.value) {
        denomButtons.forEach(b => b.classList.remove('gift-card-denom--selected'));
        selectedDenomination = null;
      }
    });
  }

  if (messageInput && messageCount) {
    messageInput.addEventListener('input', () => {
      messageCount.textContent = String(messageInput.value.length);
    });
  }

  function showError(message) {
    errorEl.textContent = message;
    errorEl.hidden = !message;
  }

  function chosenAmount() {
    if (selectedDenomination !== null) return String(selectedDenomination);
    if (customInput && customInput.value) return customInput.value;
    return null;
  }

  function getCsrfToken() {
    // CSRF_COOKIE_HTTPONLY=True: the cookie is unreadable from JS, so the
    // token comes from the base template's meta tag or a rendered form
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    showError('');

    const recipientEmail = document.getElementById('gc-recipient-email').value.trim();
    if (!recipientEmail) {
      showError('Please enter the recipient’s email address.');
      return;
    }

    const amount = chosenAmount();
    const needsAmount =
      config.denominationType === 'custom' ||
      (Array.isArray(config.denominations) && config.denominations.length > 1);
    if (needsAmount && !amount) {
      showError('Please choose an amount for the gift card.');
      return;
    }

    // Exactly the serializer's allowed keys; empty optionals are omitted, not
    // sent as blanks.
    const giftCardData = { recipient_email: recipientEmail };
    if (amount) giftCardData.amount = amount;

    const recipientName = document.getElementById('gc-recipient-name').value.trim();
    if (recipientName) giftCardData.recipient_name = recipientName;

    const senderName = document.getElementById('gc-sender-name').value.trim();
    if (senderName) giftCardData.sender_name = senderName;

    const message = messageInput ? messageInput.value.trim() : '';
    if (message) giftCardData.message = message;

    const sendAt = document.getElementById('gc-send-at').value;
    if (sendAt) {
      // datetime-local is zoneless; toISOString() makes it offset-aware in
      // the customer's own zone, which is what the serializer demands.
      giftCardData.scheduled_send_at = new Date(sendAt).toISOString();
    }

    submitBtn.disabled = true;
    try {
      const resp = await fetch('/api/cart/add/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
        },
        credentials: 'same-origin',
        body: JSON.stringify({
          product_id: config.productId,
          quantity: 1,
          gift_card_data: giftCardData,
        }),
      });
      const data = await resp.json().catch(() => null);

      if (resp.ok && data && data.success !== false) {
        document.dispatchEvent(new CustomEvent('cart:updated'));
        form.reset();
        denomButtons.forEach(b => b.classList.remove('gift-card-denom--selected'));
        selectedDenomination = null;
        if (messageCount) messageCount.textContent = '0';
        submitBtn.innerHTML = '<i class="fas fa-check"></i> Added';
        setTimeout(() => {
          submitBtn.innerHTML =
            '<i class="fas fa-gift" aria-hidden="true"></i> Add gift card to cart';
          submitBtn.disabled = false;
        }, 1500);
      } else {
        // Server messages are localised and specific (denomination rules,
        // markup refusal, schedule bounds) — show them verbatim.
        showError((data && (data.message || data.error)) || 'Could not add the gift card.');
        submitBtn.disabled = false;
      }
    } catch (err) {
      showError('Could not add the gift card. Please try again.');
      submitBtn.disabled = false;
    }
  });
})();
