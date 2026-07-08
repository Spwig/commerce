---
slug: pos-staff-discounts
title_i18n_key: POS Staff Discounts and Terminal Security
category: point-of-sale
component: pos_app
keywords:
  - pos staff discount
  - staff discount
  - discount limit
  - manager approval
  - manager PIN
  - cashier PIN
  - terminal lock
  - terminal unlock
  - POS security
  - lock event
  - discount permission
  - cart discount
  - item discount
  - access control
  - POS audit
url_patterns:
  - /admin/pos_app/posstaffdiscount/
  - /admin/pos_app/terminallockevent/
related:
  - managing-pos-terminals
  - pos-system-overview
  - pos-shifts-cash-management
  - staff-roles
published: true
---

POS staff discount settings let you control how much discount each staff member can apply at the point of sale. Terminal lock events provide an audit trail of every time a terminal was locked or unlocked — helping you track who accessed the terminal and whether any failed login attempts occurred.

## Staff discount limits

Each staff member who uses the POS can have individual discount permissions. By default, staff can apply up to 10% discount to items or the whole cart. You can raise or lower this limit per person, or designate staff as managers who can approve discounts that exceed standard limits.

### Configuring a staff member's discount limit

1. Navigate to **POS > Staff Discounts**
2. Click **+ Add POS Staff Discount** or click an existing staff member to edit
3. Select the **Staff Member** from the list
4. Set the discount limits:

| Field | Description |
|-------|-------------|
| **Max Discount %** | Maximum percentage discount this person can apply (e.g., `10` for 10%) |
| **Max Discount Amount** | Maximum fixed dollar amount per transaction (leave blank for no fixed cap) |
| **Can Apply Item Discounts** | Allow discounting individual line items |
| **Can Apply Cart Discounts** | Allow discounting the entire cart total |
| **Requires Reason** | When checked, the staff member must type a reason before applying any discount |

5. Click **Save**

### How discount limits work at the POS

When a cashier attempts to apply a discount:
- If the discount is within their limit, it is applied immediately
- If the discount exceeds their limit, the terminal prompts for **manager approval**
- A manager enters their PIN to authorise the override, and the discount is applied

This workflow prevents unauthorised high-value discounts while allowing flexibility when genuine discounts are warranted.

## Manager roles

Staff with the **Is Manager** flag can approve discounts that exceed other staff limits. Managers are identified at the terminal by a PIN they enter when an approval is requested.

### Setting up a manager

1. Open a staff member's discount record
2. Check **Is Manager**
3. Enter a **Manager PIN** (4-6 digits) — this is hashed securely when saved
4. Click **Save**

The manager PIN is separate from the cashier PIN used for terminal lock/unlock. A manager can have both a manager PIN (for discount approvals) and a cashier PIN (for terminal access).

### Manager PIN security

When you enter a PIN in the admin form and save, Spwig automatically hashes it — the plain PIN is never stored. The plain PIN field clears after saving, which is expected behaviour.

## Cashier PINs and card access

Each staff member can also have a **Cashier PIN** for locking and unlocking the terminal:

- **Cashier PIN** — 4-6 digit PIN used to unlock the terminal after it auto-locks or is manually locked
- **Card Identifier** — A registered card (swipe card or NFC) can also be used to unlock the terminal

To set up a cashier PIN, enter it in the **Cashier PIN** field and save. Like the manager PIN, it is automatically hashed on save.

## Terminal lock events

Every time a terminal is locked or unlocked, Spwig records a terminal lock event. This creates a complete security audit trail.

### Viewing lock events

Navigate to **POS > Terminal Lock Events** to see the full history. You can filter events by:
- Terminal
- Event type
- Date range

### Event types

| Event | Meaning |
|-------|---------|
| **Manual Lock** | A staff member deliberately locked the terminal |
| **Auto-Lock (Idle Timeout)** | Terminal locked automatically due to inactivity |
| **Unlock by Cashier** | Cashier authenticated and unlocked the terminal |
| **Unlock by Manager** | A manager used their credentials to unlock |
| **Unlock by Card** | Terminal was unlocked using a registered swipe card |
| **Unlock by Biometric** | Terminal was unlocked using fingerprint or face recognition |
| **Failed Unlock Attempt** | An unlock attempt was made with incorrect credentials |
| **Lockout (3+ failures)** | Terminal was locked out after repeated failed attempts |

### What lock event records contain

Each event records:
- The **Terminal** involved
- The **Event Type**
- Who performed the action (**Performed By**) and who was logged in when the lock occurred (**Locked By**)
- Whether a **Manager Override** was used
- The **Unlock Method** (PIN, card, or biometric)
- **Failed Attempts** before this event (useful for spotting brute-force patterns)
- The **Cart Total** and item count at the time of the event
- The IP address of the request

### Investigating a security concern

If you suspect unauthorised access to a terminal:

1. Navigate to **POS > Terminal Lock Events**
2. Filter by the terminal in question
3. Look for events of type **Failed Unlock Attempt** or **Lockout** — these indicate repeated failed access
4. Check the **Performed By** field on successful unlocks to see who gained access
5. Cross-reference with the shift records (**POS > Shifts**) to verify the cashier who was meant to be on duty

## Tips

- Set discount limits based on staff seniority — new staff might start at 5%, experienced staff at 10-15%, and managers can approve anything higher.
- Enable **Requires Reason** for any staff with higher discount limits. Having a reason on file helps you analyse discount patterns and identify any misuse.
- Review terminal lock events weekly if your store has multiple staff or high staff turnover — irregular access patterns are easier to spot before they become a problem.
- If a staff member leaves, remove their cashier PIN and card identifier immediately to prevent terminal access.
- Use the lockout event to identify terminals that may need their auto-lock timeout adjusted — if customers are frequently triggering accidental lockouts, the idle timeout may be set too short.
- Manager PINs should be changed periodically. Update them in the staff discount record — the new PIN is hashed on save.
