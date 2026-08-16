---
slug: selling-products-as-subscriptions
title_i18n_key: Selling Products as Subscriptions
category: products
component: catalog
keywords:
  - subscription product
  - sell as subscription
  - recurring purchase
  - subscribe and save
  - enable subscription
  - one-time purchase
  - subscription default
  - subscriptions tab
  - recurring billing product
  - eligible product types
  - subscription eligible
  - product page subscription selector
  - attach subscription plan
url_patterns:
  - /admin/catalog/product/
  - /admin/catalog/product/add/
  - /admin/catalog/product/\d+/change/
related:
  - subscription-plans
  - managing-subscriptions
  - add-product
  - digital-products
published: true
---

Any Simple, Variable, or Digital product can now be sold on a recurring basis, right alongside — or instead of — a one-time purchase. This guide covers turning subscriptions on for a product, choosing which plans customers can pick from, and what your customers actually see when they buy.


## Which product types can be sold as subscriptions

Subscriptions are only available for these product types:

| Eligible | Not eligible |
|----------|---------------|
| Simple Product | Product Bundle |
| Variable Product | Gift Card |
| Digital Product | Customizable Product |
| | Configurable Product |
| | Booking Product |

The reason is fulfilment, not pricing: a subscription re-charges your customer every cycle and re-delivers the product through a new order each time. Spwig knows how to re-ship a Simple or Variable product and re-grant a Digital product's download or license on every renewal — but it can't safely re-run a gift card issuance, a multi-component bundle, a customer's saved customization, a configurator build, or a booking slot on a recurring schedule. Letting those types be sold as subscriptions would risk taking a customer's money on cycle 2 without being able to deliver anything.

The **Enable Subscription** checkbox itself isn't hidden or greyed out for ineligible types — you can technically check it on any product. If you try to save a Gift Card, Bundle, Customizable, Configurable, or Booking product with subscriptions enabled, Spwig will reject the save with a validation error explaining that this product type can't be sold as a subscription. Change the **Product Type** first (Basic Info tab), or leave subscriptions off for that product.

## Enabling subscriptions on a product

1. Navigate to **Products > All Products** and open the product you want to sell as a subscription (or create a new one).
2. Confirm the **Product Type** on the Basic Info tab is Simple, Variable, or Digital.
3. Click the **Subscriptions** tab.
4. Check **Enable Subscription**.
5. In the **Subscription Plans** field, select one or more plans this product should offer. You can only choose plans that already exist — if you haven't created any yet, see [Subscription Plans](/help/subscription-plans) first.
6. Configure the two purchase-mode checkboxes (below).
7. Click **Save**.

![The Subscriptions tab of the product edit form: Enable Subscription checked, a plan selected in the Subscription Plans list, and the Allow One-Time Purchase and Default to Subscription checkboxes](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Attaching subscription plans

A **Subscription Plan** is a reusable template — billing cadence options, trial, setup fee, cancellation rules — that you build once and can attach to any number of eligible products. The **Subscription Plans** field on the product's Subscriptions tab is where you connect a product to the plan(s) it should be sold under.

You can attach more than one plan to the same product. This is useful when, for example, you want to offer a "Standard" and a "Premium" recurring tier for the same item — each plan can carry its own pricing tiers, trial, and cancellation policy. When a product has more than one plan attached, customers see a plan chooser on the product page before picking a billing frequency.

## Controlling one-time vs. subscription purchases

Two checkboxes on the Subscriptions tab control how customers can buy the product:

- **Allow One-Time Purchase** — On by default. When checked, customers choose between a regular one-time purchase and subscribing. Uncheck it to make the product subscription-only — every purchase becomes a recurring order, and no one-time option is shown at all.
- **Default to Subscription** — Pre-selects the subscription option (and its default plan/tier) when the product page loads, instead of making customers actively choose it. This only has an effect when **Allow One-Time Purchase** is also checked — if one-time purchase is off, the product is subscription-only regardless of this setting.

Use **Default to Subscription** for products where recurring delivery is the natural expectation (coffee, supplements, consumables) — it removes a click and nudges customers toward the option that keeps them coming back, without removing their ability to buy just once.

## What customers see

### On the product page

When a product has subscriptions enabled and at least one active, public plan attached, a purchase-mode selector appears on the product page:

![The storefront purchase selector with "Subscribe & Save" chosen: a One-time purchase vs Subscribe & Save toggle above a delivery-frequency list showing Annual (Save 20%), Monthly and Quarterly (Save 10%) tiers with prices, plus trial, cancellation and payment notes](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- If one-time purchase is allowed, customers see a **"One-time purchase"** vs **"Subscribe & Save"** choice, defaulting to whichever mode you configured.
- If the product has more than one plan attached, a plan chooser appears once "Subscribe & Save" is selected.
- For the chosen plan, customers see a **delivery frequency** list built from that plan's pricing tiers (e.g., Monthly, Quarterly, Annual), each showing its price and a **"Save X%"** badge when the tier carries a discount.
- Trial length, setup fee, and the plan's cancellation policy (e.g., "Cancel anytime") are shown alongside the tier list, along with a note that a payment method is added at checkout.

### In the cart and at checkout

Subscription line items in the cart carry a **Subscription** badge, the billing cadence (e.g., "Every month"), and a trial note if one applies, so it's clear to the customer which lines are recurring. At checkout, the customer picks a payment provider as usual — this is the payment method that will be charged on future renewals.

> **Known limitation:** Automatically saving a customer's card for future subscription renewals at checkout is still being connected for some payment providers. Until a specific provider supports this, subscriptions placed through it may need extra follow-up (for example, contacting the customer for updated payment details ahead of a renewal) rather than being fully hands-off from day one. Check with your payment provider setup if you notice renewals aren't charging automatically for a subscription.

## Tips

- Create and test the subscription plan first (pricing tiers, trial, cancellation policy), then attach it to products — it's easier to get the plan right once than to fix it across several products later.
- Leave **Allow One-Time Purchase** checked for most products. Reserve subscription-only products for cases where a one-time purchase genuinely doesn't make sense for your business.
- If you're converting an existing best-seller into a subscription option, keep **Default to Subscription** off at first so you don't disrupt customers used to buying it once — turn it on later once you've seen how subscribers respond.
- Digital products are a great fit for subscriptions (software licenses, content memberships) since renewal re-grants access automatically with no shipping involved.
- If you need a product type that isn't eligible (a bundle or a customizable item, for instance) to be sold on a recurring basis, consider whether a simplified Simple or Digital equivalent could carry the subscription instead.
