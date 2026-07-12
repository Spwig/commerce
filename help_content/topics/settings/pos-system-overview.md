---
slug: pos-system-overview
title_i18n_key: POS System Overview
category: point-of-sale
component: pos_app
keywords:
  - pos system
  - point of sale
  - spwig pos
  - pos editions
  - pos dashboard
  - terminal management
  - retail pos
  - pos overview
  - pos setup
  - pos getting started
  - pos included
  - pos configuration
  - pos architecture
  - offline pos
  - pos features
url_patterns:
  - /admin/pos/
related:
  - managing-pos-terminals
  - pos-shifts-cash-management
  - pos-store-groups
published: true
---

The Spwig POS system transforms your store into a complete retail solution with modern point-of-sale terminals. It's included in every edition — Community, Pro, and Enterprise — with unlimited terminals across unlimited locations at no additional cost. Each terminal is a Progressive Web App (PWA) that works offline, syncs automatically, and integrates seamlessly with your inventory, customer data, and payment processing. Manage everything from the admin dashboard—terminal configuration, shift reconciliation, receipt customization, and hardware integration.

Use the POS system when you have physical retail locations, pop-up shops, trade shows, or any environment where customers purchase in person rather than online.

![POS Dashboard](/static/core/admin/img/help/pos-system-overview/dashboard.webp)

## What is Spwig POS?

Spwig POS is a fully-integrated point-of-sale system designed for merchants who sell both online and in physical locations. Unlike third-party POS systems that require complex integrations, Spwig POS is built directly into your platform, ensuring perfect data synchronization across all sales channels.

**Key Characteristics**:
- **Unlimited Terminals** - Deploy as many terminals as needed at no additional cost
- **Offline-First Architecture** - Continues processing sales even when internet connectivity is lost
- **Progressive Web App** - No app store installations; access via browser on any device (tablets, computers, dedicated terminals)
- **Real Stock Sync** - Stock reservations (15-minute TTL) prevent overselling across channels
- **Split Tender Support** - Accept multiple payment methods per transaction (cash + card + gift card)
- **Hardware Integration** - ESC/POS thermal printers, barcode scanners, cash drawers, customer displays
- **Shift Management** - Cash reconciliation with opening/closing counts and discrepancy tracking
- **Multi-Location Ready** - Store groups with settings inheritance for franchise and regional management

## Editions

POS is included in every Spwig edition — Community, Pro, and Enterprise — as of Spwig 1.5.8. There is no separate POS licence, no activation step, and no per-terminal fee.

**What's included in every edition**:
- Unlimited terminal registrations
- Unlimited staff assignments
- All POS features (shifts, cash management, receipt customization, customer displays)
- Payment provider integrations (Stripe Terminal and other supported providers)
- Hardware integration support

Merchants running Spwig-hosted stores or paying for a Pro/Enterprise licence get higher limits on the optional Spwig-hosted services (GeoIP, geocoder, push notifications) and priority support, but the POS feature set itself is identical across editions.

## System Architecture

**Frontend** - React 18 Progressive Web App:
- Offline-first with Service Worker caching (works without internet)
- Vite build system for fast loading
- CSS Modules + design tokens (consistent with your store theme)
- IndexedDB for local data persistence
- 10 supported languages (English, Chinese Simplified/Traditional, French, German, Spanish, Portuguese, Japanese, Russian, Arabic)

**Backend** - Backend Integration:
- 13 POS models (POSTerminal, POSShift, CashMovement, ReceiptTemplate, PromoSlide, etc.)
- 43+ REST API endpoints for terminal operations
- Stock reservation system with TTL management
- Celery tasks for background synchronization
- Encrypted credential storage for payment providers

**Security**:
- Terminal pairing via 8-character codes (generated server-side, expire after use)
- Staff assignment controls which users can access which terminals
- Remote lock/unlock capability for admin emergencies
- Encrypted payment provider credentials
- Session-based authentication with biometric unlock support (browser-dependent)

## Getting Started Workflow

Follow these 4 steps to deploy your first POS terminal. For a complete step-by-step checklist including staff setup, payment providers, and running your first sale, see [Getting Started with POS](getting-started-with-pos).

**Step 1: Create Warehouse**
- Navigate to **Catalog > Warehouses**
- Create warehouse representing your retail location
- Configure address and contact information
- This warehouse will track physical inventory for POS sales

**Step 2: Register Terminal**
- Navigate to **POS > Terminals**
- Click **+ Add Terminal**
- Set terminal name (e.g., "Main Register", "Checkout 1")
- Assign warehouse from Step 2
- Configure hardware settings (printer, scanner, cash drawer)
- Save to generate 8-character pairing code

**Step 3: Assign Staff**
- In terminal configuration, scroll to **Assigned Users**
- Select staff members authorized to use this terminal
- Only assigned users can log into the terminal
- Users must have appropriate POS permissions in their staff role

**Step 4: Pair Device**
- On your terminal device (tablet/computer), navigate to `/pos/` URL
- Enter the 8-character pairing code from Step 3
- Terminal downloads configuration and syncs initial data
- Login with assigned staff credentials
- Terminal is ready for sales

After pairing, terminals automatically sync every 5 minutes (configurable). Offline mode allows continued operation when internet is unavailable—sales sync automatically when connectivity returns.

## Core POS Features

**Sales Processing**:
- Product search by name, SKU, or barcode
- Split tender (multiple payment methods per order)
- Parked carts (save incomplete transactions)
- Refunds and voids with reason tracking
- Discount application (vouchers, gift cards, promotions)
- Customer lookup and loyalty point redemption

**Cash Management**:
- Shift opening with starting cash count
- Shift closing with expected vs actual reconciliation
- Cash movements (float adds, petty cash withdrawals with reasons)
- Automatic expected cash calculation based on cash sales
- Discrepancy tracking and reporting

**Hardware Integration**:
- ESC/POS thermal receipt printers (network or serial)
- USB barcode scanners
- Cash drawer trigger via printer pulse
- Customer-facing displays (promotional carousel during idle)
- Stripe Terminal card readers (S700, WisePOS E, P400)

**Offline Capabilities**:
- Service Worker caches all terminal assets
- IndexedDB stores recent orders (configurable: 7-30 days, 200-1000 orders)
- Stock reservations with 15-minute TTL prevent overselling
- Queue sales for sync when connectivity returns
- Automatic reconnection detection

## POS Admin Pages

Access these admin pages to manage all aspects of your POS deployment:

**POS Dashboard** (`/admin/pos/`)
- System overview and quick stats
- Recent terminal activity
- Active shifts summary
- Hosted-service usage tiles (GeoIP, geocoder, push — see [Spwig Hosted Services](hosted-services))

**Terminal Management** (`/admin/pos_app/posterminal/`)
- Register and configure terminals
- Assign staff and warehouses
- Monitor online/offline status (heartbeat tracking)
- Remote unlock terminals
- [Learn more: Managing POS Terminals](managing-pos-terminals)

**Shift Management** (`/admin/pos_app/posshift/`)
- View all shifts (open, closed, historical)
- Review cash reconciliation reports
- Track cash movements and discrepancies
- Audit shift activity
- [Learn more: POS Shifts and Cash Management](pos-shifts-cash-management)

**Store Groups** (`/admin/pos_app/storegroup/`)
- Organize terminals by location/region
- Configure group-level settings (currency, language, timezone)
- Implement settings inheritance hierarchy
- [Learn more: POS Store Groups](pos-store-groups)

**Receipt Templates** (`/admin/pos_app/receipttemplate/`)
- Customize printed receipts (paper width, logo, header/footer)
- Configure compliance fields (tax ID, business registration)
- Add QR codes for promotions
- Scope templates to specific stores or groups
- [Learn more: Receipt Template Customization](receipt-template-customization)

**Promotional Slides** (`/admin/pos_app/promoslide/`)
- Create customer display carousel content
- Target slides to specific stores or groups
- Schedule seasonal promotions
- [Learn more: Customer Display Promo Slides](customer-display-promo-slides)

**Payment Providers** (`/admin/pos_app/posterminalprovider/`)
- Configure Stripe Terminal integration
- Manage payment provider credentials
- Monitor connection status
- [Learn more: Payment Terminal Providers](payment-terminal-providers)

**Card Readers** (`/admin/pos_app/posterminalreader/`)
- Register physical card readers
- Assign readers to terminals
- Customize splash screens (customer-facing display branding)
- Monitor reader status (online/offline/busy)
- [Learn more: Card Reader Management](card-reader-management)

## Multi-Location Deployment

For merchants with multiple retail locations, Spwig POS supports hierarchical settings inheritance:

**Settings Hierarchy** (highest priority to lowest):
1. Terminal-specific settings (override all)
2. Store-specific settings (override group and site)
3. Group settings (override site defaults)
4. Site defaults (fallback for all)

Configure shared settings at the group level (e.g., regional currency, language) and override for specific stores or terminals as needed. See [POS Store Groups](pos-store-groups) for detailed configuration guidance.

## Tips

- **Start with one terminal** - Test POS setup and workflow with a single terminal before deploying fleet-wide
- **Assign warehouse before pairing** - Terminals can't process sales without a warehouse assignment
- **Configure receipt templates early** - Compliance fields (tax IDs) vary by region; set up before going live
- **Test offline mode** - Disconnect internet and verify sales continue; confirm sync when reconnected
- **Use store groups for multi-location** - Simplifies configuration management for franchise or regional deployments
- **Monitor heartbeat status** - Terminals ping server every 5 minutes; offline terminals appear in admin dashboard
- **Configure sync limits for performance** - Terminals with slow connections benefit from lower sync_days/sync_limit settings
- **Backup hardware config** - Document printer IPs, scanner settings, cash drawer configuration for disaster recovery
