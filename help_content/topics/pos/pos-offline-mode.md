---
slug: pos-offline-mode
title_i18n_key: POS Offline Mode & App Install
category: point-of-sale
component: pos_app
keywords:
  - POS offline
  - offline mode point of sale
  - install POS app
  - add to home screen
  - PWA POS
  - progressive web app
  - POS no internet
  - offline sales
  - pending transactions sync
  - POS home screen icon
  - install POS iPad
  - install POS Android
  - POS service worker
  - POS cached data
  - POS update app
  - POS storage
  - reset POS installation
url_patterns:
  - /pos/
related:
  - pos-overview
  - pos-terminal-setup
  - getting-started-with-pos
published: true
---

<!-- screenshots-needed:
- url: /pos/
  filename: pos-pwa-idle.webp
  description: POS PWA at rest — main login/terminal chooser view showing the Spwig POS branding
  save-to: core/static/core/admin/img/help/pos-offline-mode/
  viewport: 1440x900
  notes: Add-to-Home-Screen screenshots (iPad Safari, Android Chrome) are OS/browser-specific
         annotated reference shots. The session capturing this should use device emulation
         or reference images rather than attempting to trigger the browser install prompt.
-->

The Spwig POS is a Progressive Web App (PWA). It runs entirely in the browser and can be installed to a device's home screen like a native app. Because the app, your product catalog, and recent order history are cached locally on the device, your register keeps working through brief network outages and slow connections.

This topic explains exactly what works when the connection drops, how queued sales are reconciled when it returns, how to install the POS to a device home screen, and how updates reach installed devices.

## How offline mode works

When you open the POS for the first time on a device, the browser downloads and caches the entire app — its interface, images, and all supporting code. A background component called a Service Worker manages this cache. From that point forward, the app loads from the local cache even if the server is unreachable.

On top of the app cache, the POS maintains a local database on the device (using the browser's built-in IndexedDB storage). This database holds:

- **Products and variants** — synced from your catalog and refreshed every five minutes while online
- **Categories** — synced at startup and refreshed alongside products
- **Inventory levels** — synced every two minutes while online (using a network-first strategy that falls back to cached data if the server doesn't respond within three seconds)
- **Customer records** — up to 1,000 recent customers
- **Order history** — a configurable number of recent POS orders (default: 500 orders over 14 days; set per terminal in **POS > POS Terminals**)
- **Product images** — cached locally for up to 24 hours

When the POS detects that the device has gone offline, a banner appears at the top of the screen: **"Offline Mode - Sales will be synced when connection is restored."** The register continues operating using the locally cached data.

## What works offline

| Feature | Offline availability |
|---------|---------------------|
| Product search and browsing | Available — uses locally cached catalog |
| Barcode scanning | Available — scans look up products in the local cache |
| Adding items to the cart | Available |
| Applying manual discounts | Available |
| Applying voucher codes | Not available — balance checks require a live connection |
| Cash payments | Available — recorded locally and queued for sync |
| Card payments (Manual Entry) | Available — cashier processes on a separate terminal and enters the reference; recorded locally and queued for sync |
| Card payments (integrated reader — Stripe Terminal, etc.) | Not available — integrated card readers communicate with the payment network in real time |
| Gift card payments | Not available — balance lookup requires a live connection |
| Split payments combining cash and manual card | Available |
| Receipt printing to a network printer | Available if the printer is on the same local network as the device — printing does not need internet access, only local network connectivity |
| Digital receipts (email/SMS/WhatsApp) | Not available — sending requires a live connection |
| Order history browsing | Available — shows cached orders with a banner indicating you are viewing offline data |
| Refunds and voids | Not available — these require a live connection |
| Customer loyalty point lookup | Not available |
| Opening and closing shifts | Available — shift state is stored locally |

## Queued sales and sync when connection returns

Offline sales are not lost. When the register cannot reach the server, each completed sale is written to a local queue (the `pendingTransactions` store in the device's local database). The sale includes all cart items, quantities, prices, payment method, and the time it was completed.

When internet access is restored, the POS automatically:

1. Detects the reconnection via the browser's `online` event
2. Shows a banner: **"Syncing N pending transaction(s)..."**
3. Sends queued sales to the backend in order, using an exponential back-off retry schedule if the first attempt fails (up to 10 retries over a maximum window of five minutes per attempt)
4. Marks each sale as synced once the backend confirms it

**Duplicate-sale protection** — each queued sale is assigned a unique local ID before it leaves the device. The backend checks for this ID before creating an order. If the same sale is submitted twice (for example, because a retry overlapped with a successful first attempt), the backend ignores the duplicate. You will never end up with double-counted sales.

**Conflict detection** — in rare cases the backend may flag a queued sale as a conflict (for example, if a product was deleted server-side while the device was offline). Conflicted sales appear in **POS > Settings > Pending Transactions** so you can review and resolve them manually.

**Inventory adjustments** offline are handled the same way: stock changes made while offline are queued and replayed when the connection returns. Local inventory figures on the device are updated immediately so the cashier sees an accurate (estimated) count.

## Installing the POS to a device home screen

Installing the POS to a home screen gives you a full-screen experience with no browser address bar, a shortcut icon on the device, and faster launch times.

### iPad (Safari)

1. Open Safari and navigate to your store's POS URL: `https://yourstore.com/pos/`
2. Log in and complete the initial pairing if this is a new device.
3. Tap the **Share** button (the square with an upward arrow) in the Safari toolbar.
4. Scroll down in the Share sheet and tap **Add to Home Screen**.
5. Edit the name if you like (it defaults to "Spwig POS") and tap **Add**.

The POS icon now appears on your iPad home screen. Tapping it opens the app full-screen without Safari's browser chrome.

> **Note:** Safari on iPad is required for the Add to Home Screen option. Third-party browsers on iOS (Chrome, Firefox) do not support PWA installation as of mid-2025.

### Android (Chrome)

1. Open Chrome and navigate to your store's POS URL: `https://yourstore.com/pos/`
2. Log in and complete pairing if needed.
3. Tap the **three-dot menu** (top right) and tap **Install app** (or **Add to Home screen** on older versions of Chrome).
4. Confirm by tapping **Install**.

The POS icon appears on the home screen and in the app drawer. Launching from the icon opens the app in standalone mode.

### Desktop (Chrome or Edge)

1. Navigate to your store's POS URL in Chrome or Edge.
2. Look for the **install icon** in the browser's address bar (a computer monitor with a down arrow, or a "+" icon depending on the version).
3. Alternatively, open the **three-dot menu** and choose **Install Spwig POS** (Chrome) or **Apps > Install this site as an app** (Edge).
4. Confirm the installation.

The POS opens as a standalone window without browser tabs or the address bar. It appears in your system's app list and can be pinned to the taskbar.

## How the app updates

The POS manages its own updates through the Service Worker. You do not need to visit an app store or manually download anything.

**Update cycle:**

1. Each time you open the POS (or the tab becomes active after being in the background), the Service Worker checks the server for a new version.
2. If a new version is available, the Service Worker downloads it in the background while you continue working — your current session is not interrupted.
3. The update takes effect the next time you open the POS. If the app is already open and a sync is pending, the POS waits for the queue to empty before signalling that a reload is ready, to avoid interrupting an active shift with unsynced sales.

**What "reload" means when sales are pending** — if you see a prompt to reload for an update and you have pending offline sales, close out the current shift cleanly (or wait until the sync banner clears) before reloading. Reloading while sales are queued does not delete them — they remain in the local database — but it is safer to sync first to confirm they were received.

**Checking the installed version** — open the POS, tap the **menu icon** (three horizontal lines), and go to **Settings**. The current build version is shown at the bottom of the settings panel.

## Storage and clearing the installation

The POS stores several types of data locally:

| What | Typical size |
|------|-------------|
| App shell (HTML, CSS, JS, icons) | ~3–5 MB |
| Product catalog (text and metadata) | 1–10 MB depending on catalog size |
| Product images (cached) | 5–50 MB depending on catalog size |
| Order history | 1–5 MB (500 orders) |
| Customer records | 1–3 MB (1,000 customers) |
| Pending transaction queue | Minimal; cleared on sync |

**If the device runs low on storage** — browsers apply pressure to cached storage when the device is full. The POS sets its caches as persistent where the browser allows, but on very full devices the browser may evict product images first. If images stop loading, the POS will re-cache them on the next sync. Synced sales and the app shell are not affected.

**Resetting the installation** — if the POS is behaving unexpectedly (stuck on an old version, catalog not refreshing, sync permanently stuck), you can perform a clean reset:

1. **Uninstall the app** — on mobile, press and hold the POS icon and choose **Remove** or **Uninstall**. On desktop, right-click the app window title bar and choose **Uninstall**.
2. Open the POS URL directly in the browser and log in again.
3. The device will be asked for the terminal's 8-character pairing code again. You can find or regenerate this code in the admin at **POS > POS Terminals** — open the terminal and click **Regenerate pairing code**.
4. A fresh pairing forces a complete re-sync of all cached data.

> **After resetting**: any offline sales that were queued but not yet synced before the reset will be lost, because the local database is cleared. Always ensure the connection is restored and the sync banner clears before resetting an installation.

## Troubleshooting

### The POS is stuck on an old version

The Service Worker may not have activated the new version yet. Try closing all browser tabs that have the POS open, then reopening it. If the problem persists, reset the installation as described above.

### The "No connection" banner won't clear

Check that the device has internet access outside the POS (try loading another site). If the device is online but the banner persists:

- The POS server may be temporarily unreachable — wait a minute and the POS will retry automatically.
- If you are on a network that requires a sign-in page (captive portal), open a new browser tab, complete the sign-in, and then return to the POS.

### A product is missing from the POS that exists in the admin

The POS syncs products every five minutes while online. If you added a product in the admin very recently, tap the **menu icon** and go to **Settings > Sync Now** to trigger an immediate sync. If the product still doesn't appear, confirm it is marked as **Active** and is not excluded from POS availability in the product settings.

### Pending transactions are stuck in "Conflict" status

Go to **POS > Settings** (in the POS app itself) and check the **Pending Transactions** panel. Conflicted transactions are usually caused by a product or price that changed between when the sale was made offline and when it was synced. You can view the sale details and, if the sale was received correctly, mark it as reviewed.

## Tips

- Run the POS on a dedicated device that stays connected to your local Wi-Fi. Brief Wi-Fi drops are handled automatically, but a device that spends long periods offline will need more time to re-sync when it reconnects.
- Sync intervals are per-device. If you have multiple terminals, each one syncs independently. A sale on one terminal appears in the admin immediately on sync, but the other terminal's local order cache only refreshes on its own sync cycle.
- Before a planned internet outage (for example, moving to an event without Wi-Fi), open the POS while still connected so the catalog and inventory data are fully up to date. Cash sales will queue reliably; just avoid integrated card payments until you're back online.
- If you only need cash sales at an event, the Manual card payment method (cashier processes on a standalone terminal and enters a reference) works offline for card transactions too.
- Keep the device plugged in during a long shift — the local database and sync process do not significantly affect battery compared to the screen, but a charged device is always safer for trading.
