---
slug: pos-customer-display-setup
title_i18n_key: POS Customer Display Setup
category: point-of-sale
component: pos_app
keywords:
  - customer display
  - second screen
  - customer-facing screen
  - dual screen pos
  - display pairing
  - pairing code
  - pos display setup
  - customer screen setup
  - pole display
  - idle display
  - pos hardware
  - second monitor pos
  - customer display pairing
  - display device
  - pos dual screen
url_patterns:
  - /admin/pos_app/posterminal/
  - /pos/display/
related:
  - pos-system-overview
  - getting-started-with-pos
  - managing-pos-terminals
  - customer-display-promo-slides
published: true
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/posterminal/add/
  filename: terminal-capabilities-toggle.webp
  description: POS terminal add/change form scrolled to the Device tab, Hardware Configuration card, showing the hardware_config JSON field where customer_display is set to true
- url: /pos/display/
  filename: customer-display-view.webp
  description: The public customer display view (idle state without an active cart, showing placeholder or welcome screen)
  image-dir: core/static/core/admin/img/help/pos-customer-display-setup/
-->

A customer display is a second screen that faces your customer during a sale. While you process the transaction, the customer sees each item as it's scanned, the running total, the price and tax breakdown, and — when no sale is in progress — a rotating slideshow of your promotional content.

This guide covers the hardware and pairing side of setting up your customer display: enabling the feature on a terminal, pairing a separate device as the display screen, and handling common setup scenarios. For information on the promotional slides shown during idle periods, see [Customer Display Promo Slides](customer-display-promo-slides).

## What the customer display shows

When a sale is active, the customer display shows:

- Each item as it is added or removed, with quantity and price
- The cart subtotal, any discounts applied, and the tax breakdown
- The total due and, during payment, the amount tendered and change

When the terminal is idle (no active transaction), the display switches to a promotional slideshow. You control the content of that slideshow separately — see [Customer Display Promo Slides](customer-display-promo-slides).

## Common hardware setups

There are three practical ways to set up a customer-facing screen:

- **Separate tablet or monitor on a stand** — the most common setup for counter sales. A small tablet propped on a stand faces the customer while your main terminal faces you. You pair the two devices using a short-lived code (described below).
- **Second monitor in extended desktop mode** — if your main terminal is a laptop or desktop, plug in a second monitor, extend your desktop to it, then drag the display window onto the second monitor and maximise it. Both screens run on the same device; no pairing code is needed.
- **Dedicated pole display** — a hardware display unit mounted on a pole, typically connected to the counter terminal via USB or positioned on the counter. Open `/pos/display/` on the pole device's browser and pair it using the code from the main terminal.

## Enabling the customer display on a terminal

The customer display feature is enabled per terminal through the terminal's hardware configuration.

1. Navigate to **POS > Terminals** and open the terminal you want to configure (or click **+ Add POS Terminal** for a new one).
2. Click the **Device** tab.
3. Scroll to the **Hardware Configuration** card. You will see a JSON field.
4. Add `"customer_display": true` to the JSON object. For example:

```json
{
  "customer_display": true
}
```

If the field already contains other hardware settings (such as printer or scanner configuration), add `"customer_display": true` alongside them:

```json
{
  "printer": {"type": "network", "url": "http://192.168.1.100:9100"},
  "scanner": "keyboard_wedge",
  "customer_display": true
}
```

5. Click **Save**.

![Terminal hardware configuration with customer_display enabled](/static/core/admin/img/help/pos-customer-display-setup/terminal-capabilities-toggle.webp)

Once enabled, the POS app on that terminal will open the customer display view in a second browser window or tab when a session starts.

## Pairing a separate device as the display

If you are using a separate physical device for the customer screen (a tablet, phone, or second computer), you pair it to the terminal using a short-lived 6-digit code.

### Step 1: Generate a pairing code on the main terminal

Open the POS app on your main terminal and go to the display settings or pairing section of the terminal interface. Request a new display pairing code. The code is a 6-digit number and is valid for **5 minutes**. When you generate a new code, any previous unused codes for this terminal are automatically cancelled.

### Step 2: Open the display URL on the customer device

On the customer-facing device, open a web browser and go to:

```
https://your-store-domain.com/pos/display/
```

No login is required — the display page is publicly accessible. This is intentional: the display device does not need staff credentials, and the pairing code provides the link between the display and the correct terminal.

![Customer display idle view](/static/core/admin/img/help/pos-customer-display-setup/customer-display-view.webp)

### Step 3: Enter the pairing code

On the customer device, enter the 6-digit code from the main terminal. The display will pair to that terminal and begin showing live cart data.

Once the code is used, it is immediately invalidated and cannot be reused.

## Regenerating a pairing code

If the pairing code expires before you can enter it, or if you need to re-pair the display device (for example, if a display device is replaced or reset), generate a new code from the POS app on the main terminal.

Generating a new code automatically cancels any existing unused code for that terminal. The new code is valid for 5 minutes.

You do not need to change anything in the admin to regenerate a code — this is done entirely within the POS app.

## Multi-monitor setup on a single device

If your main terminal is a laptop or a desktop with two monitors:

1. Connect the second monitor and set it to **extended desktop** mode in your operating system display settings (not mirrored).
2. Open the POS app on the primary screen as usual.
3. The POS app will open the customer display in a second window. Drag that window across to the second monitor.
4. Maximise or go full screen on the second monitor.

No pairing code is required because both windows are running on the same device and communicate directly.

## Idle behaviour

When there is no active sale, the customer display shows a rotating slideshow of promotional images. You create and manage those slides separately under **POS > Promo Slides**.

For details on creating slides, targeting them to specific stores, and managing seasonal content, see [Customer Display Promo Slides](customer-display-promo-slides).

If no slides are configured, the display shows a simple welcome screen with your store name.

## Troubleshooting

**The display went blank or stopped updating**

The display communicates with the main terminal in real time. If the connection is interrupted, the display may go blank or show stale data. Refresh the browser on the customer device. If that does not help, generate a new pairing code and re-pair.

**The display is showing the wrong terminal's cart**

Each display is paired to a specific terminal. If you have multiple terminals, make sure you generated the pairing code on the correct terminal and entered it on the display. To fix a mismatch, generate a new code on the correct terminal and re-pair the display device.

**The pairing code expired before I could enter it**

Codes are valid for 5 minutes. Generate a new code from the POS app and enter it on the display device promptly. Keep the two devices near each other during the pairing process.

**The pairing code was entered but the display did not connect**

Check that the customer device can reach your store's domain (it needs network access). Also verify that `"customer_display": true` is set in the terminal's hardware configuration and that the terminal has been saved.

**The display URL returns an error**

Make sure you are navigating to `/pos/display/` on your store's domain, not the admin URL. The display view does not require a login — if you are being asked to log in, double-check the URL.

## Tips

- **Keep the pairing session short** — have the customer device ready and the browser open to `/pos/display/` before generating the pairing code. You have 5 minutes, but completing it in under a minute avoids timing out.
- **Test before opening** — complete a test sale with the display connected to verify customers will see the correct items and totals before your first real transaction.
- **Bookmark the display URL** — set the customer device's browser to open `/pos/display/` on startup so it is always ready.
- **Use extended desktop for simplicity** — if your terminal has a spare HDMI port and a monitor available, the extended desktop approach requires no ongoing pairing and never expires.
- **Add promo slides before opening** — an idle display that shows only a blank welcome screen is a missed opportunity. Set up at least a few promotional slides so the display is useful even when no sale is in progress. See [Customer Display Promo Slides](customer-display-promo-slides).
- **Secure the display device** — the display URL is publicly accessible by design, but it only shows live cart data when paired to an active terminal. Still, consider a kiosk browser mode on the customer device to prevent customers from navigating elsewhere.
