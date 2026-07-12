---
slug: getting-started-with-pos
title_i18n_key: Getting Started with POS
category: point-of-sale
component: pos_app
keywords:
  - POS setup
  - point of sale getting started
  - enable POS
  - register terminal
  - pairing code
  - store location
  - shift open
  - card reader setup
  - payment provider POS
  - first sale POS
  - POS walkthrough
  - POS checklist
  - receipt template
  - open shift
  - close shift
url_patterns:
  - /admin/pos/
related:
  - pos-overview
  - pos-terminal-setup
  - pos-payment-provider-setup
  - pos-shifts
published: true
---

<!-- screenshots-needed:
- url: /en/admin/pos/
  filename: getting-started-dashboard.webp
  description: POS dashboard as it appears on a fresh install with no terminals registered
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/pos/terminal-provider/wizard/step1/
  filename: getting-started-provider-wizard-step1.webp
  description: Payment provider wizard first step showing available provider options
  save-to: core/static/core/admin/img/help/pos/
- url: /en/admin/catalog/warehouse/
  filename: getting-started-store-location.webp
  description: Warehouse list showing a store location with the POS toggle enabled
  save-to: core/static/core/admin/img/help/pos/
-->

Spwig POS turns any tablet or browser into a full in-store register — connected to your product catalog, inventory, and order history. This checklist walks you from a fresh install to ringing your first sale. Each step links to a dedicated topic if you want the full details.

![POS Dashboard](/static/core/admin/img/help/pos/getting-started-dashboard.webp)

## Step 1: Enable POS for a store location

POS terminals are tied to a physical store location. In Spwig, store locations are warehouses marked as retail locations.

1. Navigate to **Catalog > Warehouses** in your admin sidebar.
2. Open the warehouse you want to use as a store, or create a new one.
3. Check the **Retail location** toggle and enter a **POS display name** (e.g., "High Street Store"). This name appears on receipts and the terminal selector.
4. Save the warehouse.

If you have multiple stores or want to group them for regional reporting, create a **Store Group** first at **POS > Store Groups**, then assign each warehouse to that group. Store groups let you set a shared currency, timezone, and receipt template that all locations in the group inherit.

## Step 2: Create or verify at least one staff account with POS access

Your staff log in to the POS using the same credentials they use for the Spwig admin. Any staff account with **Active** status and at least the `pos_admin` permission can access the POS.

To check or grant access, go to **Settings > Staff Management**, open the staff member's account, and confirm they have the appropriate POS role assigned. No separate POS account is needed.

## Step 3: Register your first POS terminal

A terminal represents a single register or device. You register it in the admin, then pair a physical device to it using a one-time pairing code.

1. Navigate to **POS > POS Terminals** and click **+ Add POS Terminal**.
2. Give the terminal a name (e.g., "Front Register") and assign it to the store location you enabled in Step 1.
3. Save the terminal. Spwig generates an **8-character pairing code** — you'll see it on the terminal's detail page.
4. On the device you want to use as a register, open a browser and go to `/pos/`.
5. Enter the pairing code when prompted. The device is now linked to this terminal.

The pairing code is single-use. If you need to re-pair a device, open the terminal in the admin and click **Regenerate pairing code**.

For hardware configuration options (receipt printer, barcode scanner, cash drawer), see [POS Terminal Setup](pos-terminal-setup).

## Step 4: Configure a payment provider

The payment provider connects your card readers to a payment network such as Stripe Terminal or Square. Use the 5-step setup wizard to enter your credentials.

1. Navigate to **POS > Payment Providers** and click **Configure provider**.
2. The wizard opens at `/admin/pos/terminal-provider/wizard/step1/`.

![Payment Provider Wizard](/static/core/admin/img/help/pos/getting-started-provider-wizard-step1.webp)

3. Select your provider (e.g., **Stripe Terminal**) and follow the on-screen instructions through all five steps: select provider → setup instructions → enter credentials → test connection → configure location.
4. A green **Connected** badge confirms the integration is live.

If you only need cash and manual card entry, select **Manual** as the provider — no credentials required.

For detailed credential fields for each supported provider, see [POS Payment Provider Setup](pos-payment-provider-setup).

## Step 5: Pair a card reader

With a payment provider connected, you can pair a physical card reader to one of your terminals using the 3-step reader wizard.

1. Navigate to **POS > Card Readers** and click **Add reader**.
2. The reader wizard starts at `/admin/pos/reader/wizard/step1/`.
3. Select your provider, then choose to **Register new device** (enter the code shown on the reader's screen) or **Discover existing** (Spwig fetches readers already registered with the provider).
4. On the final step, assign the reader to the terminal you created in Step 3.

Each terminal supports one assigned card reader. You can reassign readers at any time from the Card Readers list.

## Step 6: Design your receipt (optional for day one)

Spwig creates a default receipt template automatically. You can start selling immediately without touching it — the default prints your store name, address, itemised sale, payment method, and a "Thank you for your purchase!" footer.

When you're ready to customise, go to **POS > Receipt Templates**. Options include your logo, tax ID number, QR code promotion, return policy, and paper width (58mm or 80mm for thermal printers). You can create separate templates per store or per store group.

## Step 7: Open your first shift

Shifts track who processed sales and how much cash should be in the drawer. Cashiers open and close shifts on the POS itself.

1. On the paired device, go to `/pos/` and log in with your staff credentials.
2. Select the terminal and store location.
3. Spwig prompts you to **count the opening float** — enter the cash amount already in the drawer (enter `0` if the drawer is empty).
4. Tap **Open Shift**. The register is now ready to sell.

For a full explanation of shifts, cash movements, and reconciliation reports, see [Managing POS Shifts](pos-shifts).

## Step 8: Ring your first sale

Once a shift is open, selling is straightforward:

1. Search for products by name, scan a barcode, or browse categories to add items to the cart.
2. Apply a discount or a voucher code if needed.
3. Tap **Charge** to begin payment. Choose the payment method (cash, card via reader, or split tender).
4. For card payments, the reader prompts the customer to tap or insert their card.
5. The receipt prints automatically (or displays a digital receipt option). The order is saved to your order history in real time.

## Step 9: Close the shift at end of day

Closing a shift locks the register and produces a reconciliation summary.

1. From the POS menu, tap **Close Shift**.
2. Count the cash in the drawer and enter the total when prompted.
3. Spwig calculates the expected cash based on opening float, cash sales, and any cash movements during the shift, and shows you the difference.
4. Confirm to close. The shift report is saved and visible in **POS > Shifts** in your admin.

Record any cash removed from or added to the drawer during the day as **cash movements** (via the shift menu) rather than adjusting the closing count — this keeps your reconciliation accurate.

## Tips

- Complete Steps 1 to 5 before your first day of trading. Steps 6 to 9 can be done on the day.
- Use a strong but memorable staff password — POS staff type their credentials at the register, so overly complex passwords slow them down.
- If the card reader does not appear online, click **Sync readers** on the Card Readers page to pull the latest status from your provider.
- Test the full flow (open shift → sale → receipt → close shift) with a $0.01 test transaction before your busy trading period.
- The POS works offline for basic cash sales. Card terminal payments require an internet connection to authorise.
- You can have multiple terminals at one store location — add a new terminal record in the admin and pair it to a different device.
