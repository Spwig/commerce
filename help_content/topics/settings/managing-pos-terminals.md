---
slug: managing-pos-terminals
title_i18n_key: Managing POS Terminals
category: point-of-sale
component: pos_app
keywords:
  - pos terminals
  - terminal management
  - terminal registration
  - terminal pairing
  - pairing code
  - terminal configuration
  - terminal status
  - terminal online offline
  - remote unlock
  - terminal staff
  - hardware configuration
  - terminal sync
  - offline cache
  - heartbeat monitoring
  - terminal assignment
url_patterns:
  - /admin/pos_app/posterminal/
related:
  - pos-system-overview
  - pos-shifts-cash-management
  - card-reader-management
published: true
---

Managing POS terminals is the foundation of your retail operations. Each terminal represents a physical device (tablet, computer, or dedicated POS hardware) where staff process sales. Configure terminals with warehouse assignments, staff authorizations, hardware integrations, and offline sync settings. Monitor terminal health with real-time heartbeat tracking and remotely unlock terminals when issues arise. Proper terminal management ensures smooth in-store operations and prevents configuration conflicts across locations.

Navigate to **POS > Terminals** to register new terminals, view online/offline status, and manage all terminal settings.

![Terminal List](/static/core/admin/img/help/managing-pos-terminals/terminal-list.webp)

## Terminal List View

The terminal list displays all registered terminals with key status information:

**Terminal Name** - Descriptive label for the terminal (e.g., "Checkout 1", "Main Register", "Mobile Terminal")

**UUID** - Unique identifier automatically generated on creation (used internally for device identification)

**Warehouse** - Physical location assigned to this terminal (determines stock availability and order attribution)

**Online Status** - Live indicator showing whether terminal is currently connected:
- **Green dot** - Online (heartbeat received within last 5 minutes)
- **Red dot** - Offline (no heartbeat for >5 minutes)
- **Gray dot** - Never paired (terminal created but device never connected)

**Last Heartbeat** - Timestamp of most recent ping from terminal (updates every 5 minutes when online)

**Pairing Code** - 8-character alphanumeric code used for initial device pairing (hidden after first use)

**Assigned Users** - Count of staff members authorized to use this terminal

## Creating a New Terminal

Click **+ Add Terminal** to register a new POS device:

![Add Terminal Form](/static/core/admin/img/help/managing-pos-terminals/terminal-add-form.webp)

### Basic Configuration

**Terminal Name** - Choose a descriptive name that indicates:
- Physical location: "North Entrance Register"
- Function: "Returns Desk Terminal"
- Sequence: "Checkout 1", "Checkout 2", "Checkout 3"

Names help staff identify terminals during shift assignments and troubleshooting. Use consistent naming conventions across all locations.

**Warehouse** - **REQUIRED** - Select the warehouse this terminal operates from:
- Determines which stock is available for sale
- Orders placed on this terminal are attributed to this warehouse
- Stock reservations check availability in the assigned warehouse
- **Cannot process sales without warehouse assignment**

If you have multiple retail locations, create a separate warehouse for each location and assign terminals accordingly.

**Is Active** - Toggle to enable/disable terminal without deleting configuration:
- Inactive terminals cannot be paired
- Existing sessions on inactive terminals expire immediately
- Use to temporarily disable stolen or damaged terminals

### Staff Assignment

**Assigned Users** - Select which staff members can access this terminal:
- Only assigned users can log into the terminal
- Users must also have POS permissions in their staff role
- Assigning zero users effectively locks the terminal
- Common pattern: Assign all store staff to all store terminals

**Use Case Examples**:
- **General Store**: Assign all staff to all terminals (any cashier can work any register)
- **Department Store**: Assign department-specific staff to department terminals
- **Multi-Location**: Assign location-specific staff to location terminals
- **Managers**: Assign management to all terminals for supervisory access

Users without terminal assignment see "Not authorized for this terminal" error when attempting to log in.

### Hardware Configuration

The **Hardware Config** field is a JSON structure defining peripheral devices:

**Thermal Printer**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  }
}
```

**USB Barcode Scanner**:
```json
{
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  }
}
```

**Cash Drawer** (connected to printer):
```json
{
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

**Complete Example**:
```json
{
  "printer": {
    "type": "network",
    "ip": "192.168.1.100",
    "port": 9100,
    "paper_width": 80
  },
  "scanner": {
    "type": "usb",
    "vendor_id": "0x05e0",
    "product_id": "0x1200"
  },
  "cash_drawer": {
    "enabled": true,
    "trigger": "printer_pulse"
  }
}
```

Leave blank if terminal has no peripheral hardware (suitable for mobile terminals or tablets without printer/scanner).

### Offline Cache Settings

Configure how much data the terminal caches for offline operation:

**Order Sync Days** (7-30 days, default: 14):
- Number of days of recent orders to cache locally
- Higher values = more historical data available offline
- Lower values = faster sync, less storage used
- **Recommendation**: 7 days for high-volume terminals, 14 days for normal use, 30 days for audit-heavy operations

**Order Sync Limit** (200-1000 orders, default: 500):
- Maximum number of orders to cache regardless of date range
- Prevents excessive storage use on high-volume terminals
- **Recommendation**: 200 for tablets with limited storage, 500 for standard terminals, 1000 for dedicated POS devices

**Trade-offs**:
- **Higher settings**: Better offline access to historical data, slower initial sync, more storage used
- **Lower settings**: Faster sync, less storage, limited offline history

The terminal downloads the most recent X orders (within Y days) on each sync cycle. If terminal processes 50 orders/day and sync_days is 14, expect ~700 orders cached (may hit sync_limit cap).

## Terminal Pairing Workflow

After creating a terminal, pair the physical device:

1. **Generate Pairing Code** - Automatically created when you save the terminal (8 alphanumeric characters)

2. **Note the Code** - Displayed in terminal list and detail view (expires after first successful pairing)

3. **Navigate to Terminal Device** - On the physical device (tablet/computer), open browser and go to: `https://yourstore.com/pos/`

4. **Enter Pairing Code** - Type the 8-character code when prompted

5. **Terminal Downloads Configuration** - Device receives:
   - Warehouse assignment
   - Hardware config (printer, scanner, drawer)
   - Offline cache settings
   - Assigned user list
   - Initial product catalog sync

6. **Login Prompt Appears** - Terminal shows login screen for assigned users

7. **Staff Logs In** - Enter credentials for user assigned to this terminal

8. **Initial Sync Completes** - Terminal downloads:
   - Recent orders (per sync_days and sync_limit)
   - Full product catalog for assigned warehouse
   - Customer database
   - Promotional configurations

9. **Terminal Ready** - "Ready to Sell" screen appears with search bar

10. **Pairing Code Consumed** - Code is removed from admin; generate new code if re-pairing is needed

**Pairing Code Regeneration**: If you need to re-pair a terminal (device reset, browser cache cleared, new hardware), use the **Regenerate Pairing Code** admin action. This invalidates the old code and creates a new one.

## Monitoring Terminal Status

### Heartbeat System

Terminals ping the server every **5 minutes** with a heartbeat signal containing:
- Terminal UUID
- Current timestamp
- Online user count
- Last sync timestamp
- Service Worker status

**Online Status Indicator**:
- **Green** - Heartbeat received within last 5 minutes (terminal is online and operational)
- **Red** - No heartbeat for >5 minutes (terminal offline or disconnected)
- **Gray** - Terminal never paired (no heartbeat ever received)

**Use Cases**:
- **Daily open**: Check all terminals are online before store opening
- **Troubleshooting**: Identify which terminals are experiencing connectivity issues
- **Audit**: Verify terminals are active during business hours

### Last Heartbeat Timestamp

Displays the exact date/time of the most recent heartbeat. Use this to:
- Determine how long a terminal has been offline
- Identify patterns (e.g., terminal goes offline every night at closing)
- Verify sync frequency (should update every ~5 minutes when online)

## Remote Unlock Feature

When a terminal becomes unresponsive or stuck on a screen (software crash, session timeout issues, browser hang), use the **Remote Unlock** admin action:

**How It Works**:
1. Select problematic terminal in admin list
2. Choose **Remote Unlock** from admin actions dropdown
3. Confirm action
4. Server sends unlock signal via heartbeat response
5. Terminal receives signal on next heartbeat cycle (<5 min)
6. Terminal force-logs out current user and returns to login screen

**When to Use**:
- Terminal frozen on transaction screen
- Staff unable to log out (logout button not responding)
- Session appears active but terminal is unresponsive
- Browser crashed but session cookie persists

**Important**: Remote unlock does NOT restart the device or browser—it only forces a logout and session clear. If terminal is completely frozen, staff may need to restart the browser or device manually.

## Editing Terminal Configuration

Click a terminal in the list to edit its configuration:

![Edit Terminal Form](/static/core/admin/img/help/managing-pos-terminals/terminal-edit-form.webp)

**Safe to Change While Terminal is Online**:
- Terminal name
- Assigned users
- Hardware config (takes effect after terminal restarts app)
- Offline cache settings (takes effect on next sync)

**Requires Re-Pairing**:
- Warehouse assignment (changing warehouse requires re-pairing to sync new inventory)

**Cannot Change**:
- UUID (immutable identifier)

Changes to most settings apply on the next heartbeat/sync cycle. Hardware config changes require staff to close and reopen the POS app (or refresh browser).

## Troubleshooting Common Issues

**Terminal Shows "Not Authorized" on Login**:
- Verify user is in the **Assigned Users** list for this terminal
- Verify user has POS permissions in **Staff & Permissions > Roles**
- Check terminal is marked **Is Active**

**Terminal Won't Pair (Invalid Code)**:
- Pairing codes expire after first use—regenerate if needed
- Codes are case-sensitive—verify capitalization
- Check terminal is marked **Is Active**

**Terminal Shows Offline (Red Dot)**:
- Verify device has internet connectivity
- Check terminal is actually running (browser open to /pos/ URL)
- Ensure firewall isn't blocking heartbeat requests
- Wait 5 minutes for next heartbeat cycle

**Terminal Slow to Sync**:
- Reduce **Order Sync Days** from 30 to 7
- Reduce **Order Sync Limit** from 1000 to 200
- Check network speed at terminal location
- Verify server isn't under heavy load

**Printer Not Working**:
- Verify printer IP and port in **Hardware Config**
- Test printer connectivity from terminal device (ping IP address)
- Check printer is ESC/POS compatible
- Verify printer is powered on and online

## Tips

- **Naming convention matters** - Use consistent naming (location + number) to simplify management at scale
- **Always assign warehouse before pairing** - Terminals can't process sales without warehouse assignment
- **Test hardware config before deploying** - Print test receipt to verify printer/drawer integration
- **Monitor heartbeat daily** - Set up routine to check all terminals are online at store opening
- **Lower sync limits for mobile terminals** - Tablets and phones benefit from sync_days: 7, sync_limit: 200
- **Use remote unlock sparingly** - Force-logout interrupts active transactions; confirm terminal is actually stuck first
- **Document pairing codes** - Write down code before deploying terminal to retail floor (in case setup takes longer than expected)
- **Assign manager to all terminals** - Ensures supervisors can access any register for voids, refunds, and troubleshooting
