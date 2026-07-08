---
slug: checkout-trust-badges
title_i18n_key: Checkout Trust Badges
category: design-content
component: design
keywords:
  - trust badges
  - checkout
  - trust
  - badges
  - security
  - secure checkout
  - payment
  - trust signals
  - conversion
  - template config
url_patterns:
  - /theme/template-config/
related:
  - design-themes
  - product-trust-badges
published: true
---

Trust badges are small icons with text that appear during checkout to reassure customers that their purchase is safe. They can significantly improve conversion rates by reducing hesitation at the point of payment. You can fully configure which badges appear across all checkout templates from the **Template Configuration** page.

## Accessing the Badge Editor

1. Navigate to **Settings > Design & Theme** to open the Design Dashboard.
2. Click **Page Templates** to open the Template Configuration page.
3. Scroll down to the **Checkout Trust Badges** section, located below the Checkout Template selector and its options.

## How It Works

The badges you configure here appear on **all checkout templates** (Accordion, Multi-Step, Single Page, and Express) whenever the **Show trust badges** option is enabled for the active checkout template. If trust badges are disabled in the checkout template options, they will not appear regardless of what you configure here.

By default, two badges are included:

| Icon | Text |
|------|------|
| Lock | Secure Checkout |
| Shield | Data Protected |

## Adding a Badge

1. Click the **+ Add Badge** button below the existing badges.
2. A new badge row appears with a default icon and empty text field.
3. Select an icon from the dropdown — over 30 icons are available, including shields, locks, certificates, delivery trucks, and more.
4. Type the badge text in the text field (up to 60 characters).

You can add a maximum of **6 badges**. The Add Badge button is automatically disabled once the limit is reached.

## Editing a Badge

Each badge row contains:

- **Drag handle** — The dotted grip on the left for reordering.
- **Icon preview** — Shows the currently selected icon.
- **Icon dropdown** — Choose from the available icons. The preview updates immediately when you select a new icon.
- **Text field** — The label displayed next to the icon on the checkout page.
- **Delete button** — The X button on the right removes the badge.

Simply change the icon or text directly in the row — changes are held in memory until you click **Save Configuration**.

## Reordering Badges

Drag any badge by its handle on the left side and drop it into a new position. The order you set here is the order badges appear on the checkout page.

## Removing a Badge

Click the **X** button on the right side of any badge row to remove it. The badge is removed immediately from the editor. Remember to click **Save Configuration** to persist the change.

## Saving Changes

After making changes, click the **Save Configuration** button at the top or bottom of the page. A confirmation message appears when the save is successful. All changes apply immediately to your live checkout pages.

## Available Icons

The icon dropdown includes a curated set of icons suitable for trust signals:

- **Security** — Lock, Shield, Shield Check, User Shield, Key
- **Quality** — Check Circle, Certificate, Award, Medal, Star
- **Satisfaction** — Heart, Thumbs Up, Handshake
- **Payment** — Credit Card, Money, Percent
- **Shipping** — Truck, Fast Shipping, Returns, Exchange
- **Support** — Support (headset), Phone, Email, Clock
- **Digital** — Lightning, Download, Infinity
- **Other** — Gift, Globe, Leaf (Eco), Recycle

## Tips

- Keep badges concise — short text like "Secure Checkout" works better than long sentences.
- Two to four badges is the sweet spot. Too many badges can feel cluttered and lose their impact.
- Choose badges that address your customers' top concerns. For most stores, security and returns are the biggest hesitation points.
- If you sell internationally, consider badges like "Worldwide Shipping" or "Multi-Currency Support".
- Pair the trust badges option with the checkout template's **Show trust badges** toggle — you can quickly hide all badges without deleting them by unchecking that option.
