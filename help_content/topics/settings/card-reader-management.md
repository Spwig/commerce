---
slug: card-reader-management
title_i18n_key: Card Reader Management
category: point-of-sale
component: pos_app
keywords:
  - card readers
  - reader management
  - stripe readers
  - wisep pos e
  - s700 reader
  - p400 reader
  - reader assignment
  - reader status
  - splash screen
  - reader branding
  - terminal readers
  - payment hardware
  - card reader setup
  - reader registration
url_patterns:
  - /admin/pos_app/posterminalreader/
related:
  - payment-terminal-providers
  - managing-pos-terminals
  - pos-system-overview
published: true
---

Card reader management tracks physical payment hardware devices, assigns them to POS terminals, and monitors their operational status. Each card reader represents actual hardware (Stripe S700, WisePOS E, or P400) registered with your payment provider. Readers have one-to-one relationships with terminals—each register has its dedicated card reader. Monitor reader status (online, offline, busy) in real-time, customize splash screens with your branding, and troubleshoot connectivity issues before they impact customer checkout experiences.

Use card reader management to ensure payment hardware is properly configured, assigned, and operational at all locations.

![Card Reader List](/static/core/admin/img/help/card-reader-management/reader-list.webp)

## Understanding Card Readers

Card readers are physical hardware devices that process credit and debit card payments:

**Hardware Components**:
- EMV chip card slot
- NFC antenna (contactless/tap-to-pay)
- Magnetic stripe reader (legacy, rarely used)
- Display screen (shows amount, prompts for PIN, signature)
- Network connectivity (Wi-Fi or Ethernet, depending on model)

**Software Integration**:
- Readers connect to Stripe Terminal API (cloud-based, not direct connection to POS device)
- POS terminal requests payment via API
- Stripe routes request to registered reader
- Reader processes card and returns result to POS
- No USB/Bluetooth connection between POS and reader needed

**One Reader Per Terminal**:
- Each POS terminal should have exactly one assigned card reader
- One-to-one relationship ensures clear accountability and simplified troubleshooting
- Multiple terminals can't share one reader (causes conflicts)

## Card Reader Types

Spwig POS supports Stripe Terminal card readers:

**BBPOS WisePOS E** (`bbpos_wisepos_e`):
- All-in-one Android terminal with 5" color touchscreen
- Built-in printer option (thermal receipt)
- Best for: Full-featured retail checkout, restaurants (tip prompts on color screen)
- Connectivity: Wi-Fi only
- Splash screen: Full color 480×800 portrait

**Stripe Reader S700** (`stripe_s700`):
- Countertop reader with monochrome LCD
- Compact design, splash-resistant
- Best for: Standard retail, compact checkout counters
- Connectivity: Wi-Fi or Ethernet
- Splash screen: Monochrome 480×800 portrait

**Verifone P400** (`verifone_p400`):
- Legacy countertop reader (older model)
- Still supported but not recommended for new deployments
- Best for: Existing deployments (don't replace working hardware)
- Connectivity: Wi-Fi or Ethernet
- Splash screen: Monochrome 480×800 portrait

**Future Compatibility**:
- Additional reader models may be added as Stripe Terminal expands hardware offerings
- Reader type dropdown automatically populates from provider capabilities

## Reader Registration Workflow

**Step 1: Purchase and Receive Hardware**
- Order reader from Stripe (stripe.com/terminal) or authorized reseller
- Unbox and power on reader
- Connect to Wi-Fi network (follow reader's on-screen setup)

**Step 2: Register in Stripe Dashboard**
- Navigate to **Stripe Dashboard > Terminal > Readers**
- Click **Register New Reader**
- Follow on-screen pairing process (reader displays registration code)
- Assign reader to Stripe Location (must match location in payment provider config)
- Note the **Reader ID** (looks like `tmr_ABC123...`)

**Step 3: Sync to Spwig (Automatic)**
- Spwig automatically discovers readers registered to your Stripe location
- Background job syncs every 30 minutes
- New readers appear in **POS > Card Readers** list within 30 minutes

**Step 4: Assign to Terminal (Manual)**
- Navigate to **POS > Card Readers**
- Find newly discovered reader in list
- Click to edit
- Select **Terminal** to assign reader to
- Save

**Step 5: Test Payment**
- At POS terminal, process test transaction
- Select card payment method
- POS should discover assigned reader
- Use Stripe test card (4242 4242 4242 4242) to complete test
- Verify payment completes successfully

If reader doesn't appear during test, check terminal assignment and reader status.

## Reader Status Monitoring

Readers report status to Stripe Terminal API, which Spwig syncs every 5 minutes:

**Online** (green) - Reader is powered on, connected to network, and ready to accept payments

**Offline** (red) - Reader is powered off, disconnected from network, or unreachable

**Busy** (yellow) - Reader is currently processing a payment transaction

**Last Seen** - Timestamp of reader's most recent check-in with Stripe API
- Updates every ~2 minutes when reader is online
- Useful for diagnosing connectivity issues ("reader went offline 3 hours ago" = power or network issue during business hours)

**Status Use Cases**:
- **Pre-opening check**: Verify all store readers are online before unlocking doors
- **Troubleshooting**: "Register 3 isn't accepting cards" → Check reader status → Shows offline → Check power/network
- **Audit**: "Were payments processed at Terminal 5 yesterday?" → Check last seen timestamp

## Terminal Assignment

Card readers use **one-to-one relationship** with terminals:

**Why Assignment Matters**:
- During payment, POS needs to know which reader to communicate with
- Multiple terminals sharing one reader causes conflicts (two cashiers can't use same reader simultaneously)
- Unassigned readers won't be used (orphaned hardware)

**Assignment Rules**:
- Each terminal can have **exactly one** card reader assigned
- Each card reader can be assigned to **exactly one** terminal
- Assigning reader to Terminal A automatically unassigns it from previous terminal

**Changing Assignments**:
- Edit reader record
- Change **Terminal** field to new terminal
- Save
- Previous terminal loses card reader assignment (will show "No reader assigned" error during payment)

**Unassigned Readers**:
- Newly discovered readers start unassigned
- Unassigned readers appear in list but aren't usable
- Assign to terminal to activate

## Splash Screen Customization

Reader splash screens display branding on the customer-facing screen when idle:

**What is Splash Screen?**
- Image shown on reader's display when not processing a payment
- Replaces default Stripe logo with your branding
- Visible to customers while waiting at checkout

**Auto-Generated vs Custom**:

**Auto-Generated** (default):
- Spwig generates splash screen from your store logo (if logo configured in store settings)
- Automatically sized to reader specifications (480×800 portrait)
- Monochrome for S700/P400, color for WisePOS E
- No configuration needed

**Custom Splash** (advanced):
- Upload your own custom-designed splash screen image
- Full control over design and branding
- Must meet image requirements (see below)

**Custom Splash Requirements**:
- **Resolution**: Exactly 480×800 pixels (portrait orientation)
- **Format**: PNG or JPG
- **S700/P400**: Monochrome only (black and white, no grays)
- **WisePOS E**: Full color supported
- **File size**: <200KB

**Setting Custom Splash**:
1. Edit card reader record
2. Upload image to **Splash Override Image** field (or select from Media Library)
3. Save
4. Splash sync to reader within 5 minutes

**Removing Custom Splash**:
- Clear **Splash Override Image** field
- Save
- Reader reverts to auto-generated splash (or Stripe default if no store logo)

**Testing Splash**:
- After uploading, wait 5 minutes for sync
- Visit reader device
- Verify splash appears on idle screen
- Check image quality, centering, and contrast

## Stripe Splash Configuration

Behind the scenes, Spwig manages Stripe Terminal splash screen configuration:

**stripe_splash_file_id** - Stripe's internal ID for uploaded splash image file
- Automatically set when splash is uploaded
- Used to reference splash in Stripe API

**stripe_splash_config_id** - Stripe's internal ID for splash configuration
- Links splash file to reader
- Automatically managed when assigning splash to reader

These fields are read-only and managed automatically—you don't need to interact with them directly.

## Troubleshooting Common Issues

**Issue 1: Reader shows offline but is powered on**
- **Causes**: Network connectivity issue, Wi-Fi password changed, reader out of range
- **Solution**: Check reader's network settings, reconnect to Wi-Fi, verify Stripe API is reachable from network

**Issue 2: POS says "No reader assigned" during payment**
- **Cause**: Reader not assigned to terminal, or assignment incomplete
- **Solution**: Edit reader, assign to terminal, save, test payment again

**Issue 3: Reader busy indefinitely (stuck on payment screen)**
- **Cause**: Transaction timed out or crashed, reader state not reset
- **Solution**: Reboot reader (power cycle), contact Stripe support if persists

**Issue 4: Custom splash not appearing**
- **Causes**: Image wrong resolution, not synced yet, monochrome requirement not met (S700/P400)
- **Solution**: Verify image is exactly 480×800, wait 5 minutes for sync, ensure monochrome for non-color readers

**Issue 5: Reader registered in Stripe but not appearing in Spwig**
- **Cause**: Reader registered to different Stripe location than provider configuration
- **Solution**: In Stripe Dashboard, verify reader's location matches provider's location ID

## Tips

- **One reader per terminal** - Don't share readers between terminals; prevents conflicts and simplifies accountability
- **Register readers before deploying to floor** - Complete Stripe registration and Spwig assignment before putting reader at checkout
- **Test splash screens in-store** - Display contrast varies by reader model and lighting; verify splash looks good in actual environment
- **Monitor status pre-opening** - Check reader list each morning to ensure all readers online before store opens
- **Label hardware physically** - Use label maker to mark reader with terminal name ("Terminal 1 Reader") for easy identification during troubleshooting
- **Keep readers on uninterruptible power** - Power outages mid-transaction can corrupt reader state; UPS recommended
- **Document reader serial numbers** - Keep record of serial numbers for warranty and support (found on reader hardware label)
- **Update reader firmware** - Stripe pushes firmware updates automatically, but verify readers are on latest version periodically (check Stripe Dashboard)
