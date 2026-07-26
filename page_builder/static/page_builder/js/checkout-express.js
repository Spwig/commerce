/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Checkout Express UI
 *
 * Streamlined flow for returning customers with saved details.
 * Shows saved address/payment in compact view with "Change" toggles.
 * Falls back to another template if no saved details.
 * Loaded AFTER checkout.js.
 */
(function () {
  'use strict';

  function initExpress() {
    const C = window.Checkout;
    if (!C) {
      console.error('Checkout base not loaded');
      return;
    }

    const config = C.config || {};
    const container = document.querySelector('.checkout-container--express');
    if (!container) return;

    const fallbackTemplate = container.dataset.fallbackTemplate || 'accordion';

    // === Check for saved details ===

    function checkSavedDetails() {
      // No-shipping carts have no address to express — the flow is just
      // email/name + payment, which express handles fine for anyone.
      if (!C.requiresShipping) return true;

      const hasSavedAddress = document.querySelectorAll('.saved-address-card').length > 0;
      const hasSession =
        C.sessionData && (C.sessionData.shipping_address || C.sessionData.shipping_address_data);

      if (!hasSavedAddress && !hasSession) {
        const lang = config.lang || 'en';
        const fallbackUrl = `/${lang}/checkout/?template=${fallbackTemplate}`;
        window.location.href = fallbackUrl;
        return false;
      }
      return true;
    }

    // === Render saved info ===

    function renderSavedAddress() {
      const addressEl = document.getElementById('express-default-address');
      if (!addressEl) return;

      const addr =
        C.sessionData && (C.sessionData.shipping_address || C.sessionData.shipping_address_data);
      if (addr) {
        addressEl.innerHTML = `<div class="express__saved-card-content">
                    ${[
                      addr.name,
                      addr.address1,
                      addr.address2,
                      `${addr.city || ''}, ${addr.state || ''} ${addr.postal_code || ''}`.trim(),
                      addr.country,
                      addr.phone,
                    ]
                      .filter(Boolean)
                      .map(l => `<p>${C.esc(l)}</p>`)
                      .join('')}
                </div>`;
      }
    }

    function renderSavedShippingMethod() {
      const el = document.getElementById('express-selected-shipping-method');
      if (!el) return;

      const method = C.sessionData && C.sessionData.selected_shipping_method;
      const cost = C.sessionData && C.sessionData.shipping_cost;
      if (method) {
        const costDisplay =
          cost !== null && cost !== undefined
            ? parseFloat(cost) === 0
              ? 'Free'
              : C.formatCurrency(cost)
            : '';
        el.innerHTML = `<div class="express__saved-card-content">
                    <p class="express__saved-card-name">${C.esc(method.name)}</p>
                    ${costDisplay ? `<p>${costDisplay}</p>` : ''}
                </div>`;
      }
    }

    function renderSavedPayment() {
      const paymentEl = document.getElementById('express-selected-payment');
      if (!paymentEl) return;

      if (C.sessionData && C.sessionData.payment_provider_name) {
        paymentEl.innerHTML = `<div class="express__saved-card-content">
                    <p class="express__saved-card-name">${C.esc(C.sessionData.payment_provider_name)}</p>
                </div>`;
      }
    }

    function renderExpressItems() {
      const itemsEl = document.getElementById('express-items');
      if (!itemsEl || !C.cartData) return;

      const items = C.cartData.items || [];
      itemsEl.innerHTML = items
        .map(item => {
          const product = item.product || {};
          const name = product.name || 'Product';
          const imageUrl =
            product.images && product.images.length > 0
              ? product.images[0].thumbnail_url || product.images[0].image_url || ''
              : '/static/img/placeholder-product-thumb.png';
          return `
                    <div class="express__item">
                        ${imageUrl ? `<img src="${C.escAttr(imageUrl)}" alt="${C.escAttr(name)}" class="express__item-image">` : ''}
                        <div class="express__item-info">
                            <div class="express__item-name">${C.esc(name)}</div>
                            <div class="express__item-qty">x${item.quantity}</div>
                        </div>
                        <div class="express__item-price">${C.formatCurrency(item.total_price)}</div>
                    </div>
                `;
        })
        .join('');
    }

    // === Change toggles ===

    document.querySelectorAll('.express__change-link').forEach(btn => {
      btn.addEventListener('click', function () {
        const section = this.closest('.express__section');
        const targetId = this.dataset.target;
        const panel = targetId ? document.getElementById(targetId) : null;
        const savedCard = section.querySelector('.express__saved-card');

        if (panel) {
          const isVisible = !panel.hidden;
          panel.hidden = isVisible;
          this.textContent = isVisible ? 'Change' : 'Cancel';
          if (savedCard) savedCard.style.display = isVisible ? '' : 'none';

          // Fetch fresh data when opening change panels
          if (!isVisible) {
            if (targetId === 'express-shipping-method-picker') {
              C.fetchShippingMethods();
            } else if (targetId === 'express-payment-picker') {
              C.fetchPaymentProviders();
            }
          }
        }
      });
    });

    // The compact summary cards double as a Change affordance: tapping a card
    // (or Enter/Space when it's focused) opens the same picker as its header
    // link — a much bigger target than the small "Change" text, which matters
    // most on mobile. Only acts while the picker is closed so a tap can't
    // toggle an already-open panel shut.
    document.querySelectorAll('.express__saved-card[data-change-target]').forEach(card => {
      const openFromCard = () => {
        const targetId = card.dataset.changeTarget;
        const panel = document.getElementById(targetId);
        const link = document.querySelector(`.express__change-link[data-target="${targetId}"]`);
        if (link && panel && panel.hidden) link.click();
      };
      card.addEventListener('click', openFromCard);
      card.addEventListener('keydown', e => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openFromCard();
        }
      });
    });

    // Cancel buttons close the change panel
    document.querySelectorAll('[id^="express-cancel-"]').forEach(btn => {
      btn.addEventListener('click', function () {
        const panel = this.closest('.express__change-panel');
        if (panel) {
          panel.hidden = true;
          const section = panel.closest('.express__section');
          const savedCard = section.querySelector('.express__saved-card');
          if (savedCard) savedCard.style.display = '';
          const changeBtn = section.querySelector('.express__change-link');
          if (changeBtn) changeBtn.textContent = 'Change';
        }
      });
    });

    // Confirm button for the address picker ("Use this address")
    const confirmAddressBtn = document.getElementById('express-confirm-address');
    if (confirmAddressBtn) {
      confirmAddressBtn.addEventListener('click', async function () {
        // submitShippingAddress() marks the step complete only on success —
        // clear the marker first so failures (missing phone, server
        // rejection) leave the picker open for correction
        C.completedSteps.delete('shipping');
        await C.submitShippingAddress();
        if (!C.completedSteps.has('shipping')) return;

        renderSavedAddress();
        const panel = document.getElementById('express-address-picker');
        if (panel) panel.hidden = true;
        const savedCard = document.getElementById('express-default-address');
        if (savedCard) savedCard.style.display = '';
        const changeBtn = document.getElementById('express-change-address');
        if (changeBtn) changeBtn.textContent = 'Change';
        // Address change invalidated the shipping method server-side —
        // walk the customer to the next incomplete section
        renderSavedShippingMethod();
        openFirstIncompleteSection();
      });
    }

    // Confirm buttons for shipping method and payment
    const confirmShippingBtn = document.getElementById('express-confirm-shipping-method');
    if (confirmShippingBtn) {
      confirmShippingBtn.addEventListener('click', async function () {
        const selected = document.querySelector(
          '#shipping-methods-list input[type="radio"]:checked'
        );
        if (!selected) {
          C.showAlert('Please select a shipping method.', 'error');
          return;
        }
        // autoMountPayment() (reached via openFirstIncompleteSection below)
        // fetches providers itself — don't let submit fetch them too.
        await C.submitShippingMethod({ skipProviderFetch: true });
        // Re-render after submission
        renderSavedShippingMethod();
        const panel = document.getElementById('express-shipping-method-picker');
        if (panel) panel.hidden = true;
        const savedCard = document.getElementById('express-selected-shipping-method');
        if (savedCard) savedCard.style.display = '';
        const changeBtn = document.getElementById('express-change-shipping-method');
        if (changeBtn) changeBtn.textContent = 'Change';
        // Walk the customer forward: open payment if none picked yet
        openFirstIncompleteSection();
      });
    }

    // Selecting a payment provider applies immediately — no confirm button.
    // submitPaymentMethod() creates the payment intent and mounts the
    // gateway's embedded form inside the panel, so the panel stays open for
    // card entry. Delegated: the provider list re-renders on every fetch.
    // After a provider is applied, collapse the list to save vertical space:
    // the selected gateway's form is the focus. A "Change payment method"
    // link brings the list back (only shown when there is a choice to make).
    function collapseProviderList() {
      const list = document.getElementById('payment-providers-list');
      if (!list) return;
      const count = list.querySelectorAll('.payment-provider-card').length;
      if (count < 1) return;
      list.hidden = true;
      let link = document.getElementById('express-change-provider');
      if (count > 1) {
        if (!link) {
          link = document.createElement('button');
          link.type = 'button';
          link.id = 'express-change-provider';
          link.className = 'express__change-provider-link';
          link.textContent =
            (window.UI_STRINGS && window.UI_STRINGS['js.change_payment_method']) ||
            'Change payment method';
          link.addEventListener('click', function () {
            list.hidden = false;
            link.hidden = true;
          });
          list.parentNode.insertBefore(link, list);
        }
        link.hidden = false;
      }
    }

    let submittingPayment = false;
    const providersList = document.getElementById('payment-providers-list');
    if (providersList) {
      providersList.addEventListener('change', async function (e) {
        if (!e.target || e.target.name !== 'payment_provider' || submittingPayment) return;
        submittingPayment = true;
        collapseProviderList();
        try {
          await C.submitPaymentMethod();
          renderSavedPayment();
        } finally {
          submittingPayment = false;
        }
      });
    }

    // No-shipping express has no "Continue to payment" button — the gateway
    // auto-mounts. On load that only fires when billing is pre-filled (a
    // signed-in customer with a saved default). For a guest, or a signed-in
    // customer with no saved address, the billing form starts empty; watch its
    // fields and mount the moment contact + billing become complete, so the
    // customer is never left with providers shown but no card form and no way
    // to trigger it. Fire on change/blur (not per keystroke); autoMountPayment
    // guards against remounting an already-live form.
    if (!C.requiresShipping) {
      [
        'checkout-email',
        'billing-name',
        'billing-address1',
        'billing-city',
        'billing-state',
        'billing-postal-code',
        'billing-country',
      ].forEach(id => {
        const field = document.getElementById(id);
        if (field) {
          field.addEventListener('change', function () {
            if (noShippingBillingReady()) autoMountPayment();
          });
        }
      });
    }

    // Mobile order-summary toggle; total mirrors the summary as it updates
    const summaryToggle = document.getElementById('express-summary-toggle');
    const asideEl = document.getElementById('express-aside');
    if (summaryToggle && asideEl) {
      summaryToggle.addEventListener('click', function () {
        const open = asideEl.classList.toggle('express__aside--open');
        summaryToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
      const syncToggleTotal = function () {
        const totalEl = document.getElementById('summary-total');
        const target = document.getElementById('express-summary-toggle-total');
        if (totalEl && target) target.textContent = totalEl.textContent;
      };
      document.addEventListener('checkout:summary-updated', syncToggleTotal);
      setTimeout(syncToggleTotal, 1500);
    }

    // Voucher / discount code (order summary)
    const voucherBtn = document.getElementById('express-apply-voucher');
    if (voucherBtn) {
      voucherBtn.addEventListener('click', async function () {
        const input = document.getElementById('express-voucher-code');
        const msg = document.getElementById('express-voucher-msg');
        const code = input ? input.value.trim() : '';
        if (!code) return;
        voucherBtn.disabled = true;
        try {
          const resp = await C.api('/api/cart/apply-voucher/', 'POST', { code });
          if (msg) {
            msg.textContent = resp.message || '';
            msg.classList.toggle('express__voucher-msg--error', !resp.success);
            msg.hidden = false;
          }
          if (resp.success) {
            if (input) input.value = '';
            C.cartData = await C.api(C.endpoints.cart);

            // A discount changes the amount the gateway will be asked for.
            // If a payment form is already mounted, its intent was raised
            // for the OLD total — discard it and remount at the new figure.
            const embedded = document.getElementById('embedded-payment-container');
            if (embedded && embedded.children.length > 0) {
              embedded.innerHTML = '';
              sessionStorage.removeItem('payment_intent_id');
              sessionStorage.removeItem('order_number');
              C.renderSummary();
              renderExpressItems();
              C.fetchTenders();
              await autoMountPayment();
              return;
            }

            C.renderSummary();
            renderExpressItems();
            C.fetchTenders();
          }
        } catch (err) {
          // C.api throws with the server's message (e.g. wrong currency,
          // minimum order value) — show it rather than a generic failure
          if (msg) {
            msg.textContent = err.message || 'Could not apply this code.';
            msg.classList.add('express__voucher-msg--error');
            msg.hidden = false;
          }
        } finally {
          voucherBtn.disabled = false;
        }
      });
    }

    // === Override Checkout navigation ===

    // Express doesn't use step navigation
    C.openStep = function () {};
    C.updateStepUI = function () {};

    // The guided "this address needs a phone number" flow reopens the
    // address UI — in express that's the address picker panel, not a step
    C.openAddressSectionForPhone = function () {
      openPanelIfClosed('express-address-picker');
    };

    // === Auto-complete flow ===

    // Open a section's change panel (which also triggers its data fetch)
    // as if the customer clicked "Change"
    function openPanelIfClosed(targetId) {
      const panel = document.getElementById(targetId);
      if (panel && panel.hidden) {
        const btn = document.querySelector(`.express__change-link[data-target="${targetId}"]`);
        if (btn) btn.click();
      }
    }

    // Swap any template spinner that survived rendering (its section has no
    // saved data yet) for a quiet empty state — a spinner that never
    // resolves reads as "broken", not "waiting for you"
    function clearStalePlaceholders() {
      ['express-default-address', 'express-selected-shipping-method', 'express-selected-payment']
        .map(id => document.getElementById(id))
        .filter(el => el && el.querySelector('.fa-spinner'))
        .forEach(el => {
          el.innerHTML = '<div class="express__saved-card-content"><p>Not selected yet</p></div>';
        });
    }

    // Open a panel without simulating a click (no duplicate data fetch)
    function openPanelDirect(targetId) {
      const panel = document.getElementById(targetId);
      if (!panel || !panel.hidden) return;
      panel.hidden = false;
      const section = panel.closest('.express__section');
      const savedCard = section && section.querySelector('.express__saved-card');
      if (savedCard) savedCard.style.display = 'none';
      const btn = document.querySelector(`.express__change-link[data-target="${targetId}"]`);
      if (btn) {
        // Auto-opened payment is the terminal pay surface, not a panel the
        // customer chose to open. A header "Cancel" here would hide the
        // mounted gateway form — the dead end we're removing. Hide the header
        // control instead; switching provider is offered by the in-panel
        // "Change payment method" link when there is more than one.
        if (targetId === 'express-payment-picker') {
          btn.hidden = true;
        } else {
          btn.textContent = 'Cancel';
        }
      }
    }

    // Express best practice: the payment form is on screen from the start.
    // Opens the payment panel, fetches providers, selects the session's
    // provider (or the first one) and lets the change handler create the
    // intent + mount the gateway form — one tap less for the customer.
    async function autoMountPayment() {
      // A phoneless saved address will fail PSP validation the moment an
      // intent is raised — don't auto-fire the gateway mount; walk the
      // customer to the address panel's supplemental phone field instead.
      if (C.shippingPhoneMissing && C.shippingPhoneMissing()) {
        console.warn('[Checkout] Shipping address has no phone — prompting before payment');
        // The gateway form can't be mounted until the address has a delivery
        // phone. A provider chosen on a previous visit is already painted into
        // the payment card by renderSavedPayment() — left alone it reads as
        // "payment ready" with no button, the dead end customers get stuck on.
        // Replace it with the reason and where to fix it so the section is
        // never a selected-but-unactionable void.
        const paymentEl = document.getElementById('express-selected-payment');
        if (paymentEl) {
          const msg =
            (window.UI_STRINGS && window.UI_STRINGS['js.add_phone_to_pay']) ||
            'Add a phone number to your shipping address above to continue to payment.';
          paymentEl.innerHTML = `<div class="express__saved-card-content express__saved-card-content--pending"><p>${C.esc(msg)}</p></div>`;
        }
        C.promptForShippingPhone();
        return;
      }
      const due = C.tendersData ? parseFloat(C.tendersData.amount_due || '0') : null;
      if (due !== null && due <= 0) {
        // Zero due: the tenders panel shows its own Place Order
        openPanelDirect('express-payment-picker');
        return;
      }
      // The billing-field change-listeners (no-shipping) can re-enter this as
      // the customer edits — never remount over an already-mounted gateway.
      const alreadyMounted = document.getElementById('embedded-payment-container');
      if (alreadyMounted && alreadyMounted.children.length > 0) return;

      openPanelDirect('express-payment-picker');
      await C.fetchPaymentProviders();
      // No-shipping carts need a full billing address before an intent can be
      // created. Providers are shown above; wait until contact + billing are
      // complete before mounting — pre-filled (signed-in with a saved default)
      // fires immediately; manual entry re-triggers this via the field
      // change-listeners set up in initExpress. This avoids firing a mount
      // that would only surface "required field" errors before they've typed.
      if (!C.requiresShipping && !noShippingBillingReady()) return;

      const radios = Array.from(document.querySelectorAll('input[name="payment_provider"]'));
      if (!radios.length) return;
      const sd = C.sessionData || {};
      const target =
        radios.find(r => String(r.value) === String(sd.payment_provider || '')) || radios[0];
      target.checked = true;
      // The delegated change handler submits and mounts the form
      target.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // No-shipping carts complete when contact (email) + the full billing
    // address are present. Shared by autoMountPayment and the field listeners.
    function noShippingBillingReady() {
      const email = document.getElementById('checkout-email')?.value.trim() || '';
      const requiredBilling = [
        'billing-name',
        'billing-address1',
        'billing-city',
        'billing-state',
        'billing-postal-code',
        'billing-country',
      ];
      return !!email && requiredBilling.every(id => document.getElementById(id)?.value.trim());
    }

    // Adopt the default shipping method without a "Use this method" tap.
    // fetchShippingMethods() pre-checks the first option (the server sorts
    // them cheapest/recommended-first); we just submit that and show the
    // compact card. Returns true once the session has a method. Falls back to
    // false when there's nothing safe to auto-pick (no method serves the
    // destination) so the caller can open the picker instead.
    async function autoSelectShippingMethod() {
      await C.fetchShippingMethods();
      const methods = C.shippingMethodsData || [];
      if (!methods.length) return false;
      // Never silently upgrade the customer to a premium method: auto-adopt
      // the cheapest available option (methods are ordered by merchant
      // priority, not cost, so we can't trust the first). Ties keep list
      // order. They can still pick a faster one via "Change".
      const cheapest = methods.reduce((best, m) =>
        parseFloat(m.final_cost) < parseFloat(best.final_cost) ? m : best
      );
      const radio = document.querySelector(
        `#shipping-methods-list input[name="shipping_method"][value="${cheapest.id}"]`
      );
      if (!radio) return false;
      radio.checked = true;
      // autoMountPayment() fetches providers next — skip the duplicate here.
      await C.submitShippingMethod({ skipProviderFetch: true });
      if (!(C.sessionData && C.sessionData.selected_shipping_method)) return false;
      renderSavedShippingMethod();
      return true;
    }

    // Express rides the customer's defaults straight to a ready-to-pay state.
    // It only stops to ask when a step has no safe default: no address on
    // file, a saved address still missing its required delivery phone, or no
    // shipping method available for the destination. Everything else
    // auto-adopts — the "Change" links let the customer revisit any of it.
    async function openFirstIncompleteSection() {
      // No shipping sections exist for no-shipping carts — payment is the
      // only section there is
      if (!C.requiresShipping) {
        autoMountPayment();
        return;
      }
      const sd = C.sessionData || {};
      const hasAddress = sd.shipping_address || sd.shipping_address_data;
      if (!hasAddress) {
        // Nothing to default to — the customer must supply an address.
        openPanelIfClosed('express-address-picker');
        return;
      }
      // A phoneless saved address blocks the payment intent; autoMountPayment
      // prompts for the phone. Don't auto-pick shipping first — the customer
      // confirms the (unchanged) address after adding the phone, and the
      // server preserves any method rather than clearing it.
      if (C.shippingPhoneMissing && C.shippingPhoneMissing()) {
        autoMountPayment();
        return;
      }
      if (!sd.selected_shipping_method) {
        const adopted = await autoSelectShippingMethod();
        if (!adopted) {
          // No method serves this destination — let the customer choose.
          openPanelIfClosed('express-shipping-method-picker');
          return;
        }
      }
      autoMountPayment();
    }

    // After checkout loads, if we have session data, render express view
    const originalLoadCheckout = C.loadCheckout.bind(C);
    C.loadCheckout = async function () {
      await originalLoadCheckout();

      if (!checkSavedDetails()) return;

      // If session has no address yet, adopt the default (or first) saved
      // address before rendering, so express has something to express
      // (only meaningful when the cart actually ships)
      if (
        C.requiresShipping &&
        !C.sessionData.shipping_address &&
        !C.sessionData.shipping_address_data
      ) {
        const radio =
          document.querySelector('.saved-address-card--selected input[type="radio"]') ||
          document.querySelector('.saved-address-card input[type="radio"]');
        if (radio) {
          radio.checked = true;
          await C.submitShippingAddress();
        }
      }

      // A previously selected provider can stop being offered (address or
      // currency changed, account deactivated). Showing it as the chosen
      // method while the picker omits it is a dead end — treat it as
      // unselected instead.
      if (C.sessionData.payment_provider) {
        try {
          const resp = await C.api(C.endpoints.paymentProviders);
          const available = (resp.payment_providers || []).map(p => String(p.id));
          if (!available.includes(String(C.sessionData.payment_provider))) {
            C.sessionData.payment_provider = null;
            C.sessionData.payment_provider_name = null;
          }
        } catch (err) {
          // Offline/errored providers endpoint: keep the session's choice
        }
      }

      renderSavedAddress();
      renderSavedShippingMethod();
      renderSavedPayment();
      renderExpressItems();
      // Totals are rendered by base renderSummary() using standard summary IDs

      clearStalePlaceholders();
      openFirstIncompleteSection();
    };

    // After load, re-trigger
    C.loadCheckout();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      setTimeout(initExpress, 10);
    });
  } else {
    setTimeout(initExpress, 10);
  }
})();
