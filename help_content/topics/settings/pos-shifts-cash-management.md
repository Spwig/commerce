---
slug: pos-shifts-cash-management
title_i18n_key: POS Shifts and Cash Management
category: point-of-sale
component: pos_app
keywords:
  - pos shifts
  - shift management
  - cash reconciliation
  - opening cash
  - closing cash
  - cash drawer
  - cash counting
  - cash discrepancy
  - cash movements
  - petty cash
  - float
  - cash difference
  - shift closing
  - shift reports
  - cash audit
url_patterns:
  - /admin/pos_app/posshift/
related:
  - pos-system-overview
  - managing-pos-terminals
  - pos-store-groups
published: true
---

POS shifts track cashier work periods and ensure accurate cash accounting. Each shift represents a single cashier's time on a terminal—from opening the cash drawer with a starting cash count to closing the shift with a final count and reconciliation. The system automatically calculates expected cash based on actual cash sales and compares it to the physical count, highlighting discrepancies for investigation. Cash movements during shifts (float adds, petty cash withdrawals) are tracked with reasons for complete audit trails.

Navigate to **POS > Shifts** to view all shifts, monitor active shifts, review cash reconciliation reports, and audit historical activity.

![Shift List](/static/core/admin/img/help/pos-shifts-cash-management/shift-list.webp)

## Understanding POS Shifts

A shift is a work period during which one cashier operates one terminal. Shifts enforce cash accountability—each cashier is responsible for the cash in their drawer during their shift.

**Shift Lifecycle**:
1. **Opening** - Cashier starts shift, counts opening cash, records amount
2. **During Shift** - Processes sales, accepts payments, issues refunds
3. **Closing** - Cashier counts cash, records closing amount, system calculates discrepancy
4. **Reconciled** - Shift is finalized and locked for audit purposes

**Key Metrics Tracked**:
- **Opening Cash** - Starting cash in drawer at shift start
- **Closing Cash** - Physical cash in drawer at shift end
- **Expected Cash** - Calculated: Opening cash + cash sales - cash refunds + cash movements
- **Cash Difference** - Discrepancy: Closing cash - expected cash (positive = overage, negative = shortage)
- **Total Sales** - Sum of all sales transactions during shift
- **Total Refunds** - Sum of all refund transactions during shift
- **Transaction Count** - Number of orders processed

## Shift List View

The shift list displays all shifts with key information:

**Shift Status**:
- **Open** (green badge) - Currently active shift
- **Closed** (gray badge) - Completed shift
- **Reconciled** (blue badge) - Finalized and locked for audit

**Terminal** - Which POS terminal the shift was on

**Cashier** - Staff member who worked the shift

**Opening Cash** - Starting cash amount

**Closing Cash** - Ending cash amount (blank if shift still open)

**Expected Cash** - System-calculated expected amount based on transactions

**Cash Difference** - Discrepancy (highlighted in red if negative, green if positive, black if zero)

**Duration** - Shift length (start time to end time)

**Total Sales** - Revenue generated during shift

Use filters to view:
- Only open shifts (monitor active terminals)
- Shifts with discrepancies (cash difference ≠ 0)
- Shifts by date range (daily reconciliation reports)
- Shifts by cashier (performance audit)

## Opening a Shift

Cashiers open shifts directly from the POS terminal (cannot be opened from admin). The workflow on the terminal:

1. **Staff Logs In** - Enters credentials to access terminal

2. **Count Opening Cash** - Physically counts all cash in drawer (bills and coins)

3. **Enter Opening Amount** - Records the counted amount in POS app

4. **Shift Starts** - Terminal is ready to process sales

**Opening Cash Guidelines**:
- Standard opening cash (float) is typically $100-$300 depending on store size
- Count twice to ensure accuracy—opening errors cascade into closing discrepancies
- If drawer is empty, opening cash is $0.00 (float added via cash movement)
- Document large bills (>$50) separately to track their movement

![Shift Add Form](/static/core/admin/img/help/pos-shifts-cash-management/shift-add-form.webp)

## During the Shift

While the shift is open, the system automatically tracks:

**Cash Sales** - Any transaction where customer pays with physical cash (adds to expected cash)

**Cash Refunds** - Any refund issued in cash (subtracts from expected cash)

**Card Sales** - Credit/debit card transactions (no impact on cash)

**Split Tender** - Partial cash + partial card (only cash portion affects expected cash)

**Gift Cards & Vouchers** - Non-cash payment methods (no impact on cash)

Cashiers continue processing sales normally. The system maintains a running calculation of expected cash behind the scenes.

## Cash Movements

Cash movements are adjustments to the cash drawer during a shift:

**Float Adds** - Adding cash to drawer:
- Reason: "Adding change for large bills"
- Amount: +$100.00
- Expected cash increases by $100.00

**Petty Cash Withdrawals** - Removing cash for expenses:
- Reason: "Office supplies purchase"
- Amount: -$25.00
- Expected cash decreases by $25.00

**Bank Drops** - Removing excess cash for security:
- Reason: "Safe drop - over $500 in drawer"
- Amount: -$300.00
- Expected cash decreases by $300.00

**Recording Cash Movements on Terminal**:
1. Tap **Menu** > **Cash Movement**
2. Select type: Add or Remove
3. Enter amount
4. Enter reason (required for audit trail)
5. Confirm

All cash movements appear in the shift detail report with timestamps, amounts, and reasons.

## Closing a Shift

When a cashier finishes their work period, they close the shift:

1. **Tap Close Shift** - On terminal menu

2. **Process Remaining Transactions** - Complete any parked carts or pending sales

3. **Count Closing Cash** - Physically count all cash in drawer
   - Count bills by denomination ($100s, $50s, $20s, $10s, $5s, $1s)
   - Count coins by type (quarters, dimes, nickels, pennies)
   - Total = closing cash amount

4. **Enter Closing Amount** - Record the counted total

5. **System Calculates Discrepancy**:
   - Expected cash = Opening cash + cash sales - cash refunds + cash movements
   - Cash difference = Closing cash - expected cash
   - Example: Closing $485.00 - Expected $480.00 = +$5.00 overage

6. **Review Discrepancy** - Terminal displays the difference:
   - **Exact ($0.00)** - Perfect reconciliation
   - **Small overage (+$1 to +$5)** - Acceptable rounding or customer tip
   - **Small shortage (-$1 to -$5)** - Minor counting error, acceptable
   - **Large discrepancy (>$5)** - Recount required

7. **Recount if Needed** - If discrepancy is large (>$10), cashier should recount closing cash before finalizing

8. **Finalize Shift** - Confirm closing amount, shift status changes to "Closed"

9. **Print Shift Report** - Terminal prints cash reconciliation receipt for cashier records

![Shift Detail](/static/core/admin/img/help/pos-shifts-cash-management/shift-detail.webp)

## Cash Reconciliation Formula

The system calculates expected cash using this formula:

```
Expected Cash = Opening Cash
                + Cash Sales
                - Cash Refunds
                + Cash Adds (movements)
                - Cash Removes (movements)
```

**Example**:
- Opening Cash: $200.00
- Cash Sales: $450.00 (from 15 transactions)
- Cash Refunds: -$30.00 (1 return)
- Cash Add: +$100.00 (float added mid-shift)
- Cash Remove: -$50.00 (petty cash withdrawal)
- **Expected Cash: $200 + $450 - $30 + $100 - $50 = $670.00**

If cashier counts $675.00 at closing:
- Cash Difference: $675.00 - $670.00 = **+$5.00 overage**

## Shift Reporting and Auditing

Shift reports provide detailed reconciliation information:

**Summary Section**:
- Opening and closing cash
- Expected cash calculation
- Cash difference (overage/shortage)
- Total sales and refunds
- Transaction count
- Shift duration

**Transaction Detail**:
- All sales during shift (order IDs, amounts, payment methods)
- All refunds issued
- Timestamp of each transaction

**Cash Movement Log**:
- All adds and removes
- Reasons provided
- Timestamps

**Use Cases**:
- **Daily reconciliation** - Review all shifts at end of business day
- **Cashier performance** - Identify patterns of discrepancies by staff member
- **Theft detection** - Large, consistent shortages may indicate theft
- **Training needs** - Frequent small discrepancies suggest counting accuracy issues
- **Audit trail** - Complete record for accounting and tax purposes

## Multi-Terminal Cash Management

For stores with multiple terminals running concurrent shifts:

**Separate Drawers**: Each terminal has its own cash drawer—shifts are independent. Cashier A on Terminal 1 and Cashier B on Terminal 2 run separate shifts with separate reconciliation.

**Shared Drawer**: Some stores share one cash drawer across multiple terminals (not recommended). If doing this:
- Only one shift can be open per shared drawer at a time
- Cashiers must close shift when handing off to next cashier
- Cash movements track all adds/removes during handoffs
- Discrepancies are harder to attribute to specific cashiers

**Best Practice**: One cash drawer per terminal, one shift per cashier per session. This ensures clear accountability and simplified reconciliation.

## Handling Discrepancies

When closing cash doesn't match expected cash:

**Small Discrepancies (<$5)**:
- Acceptable due to rounding, counting errors, or customer tips
- Document in shift notes
- No further action needed unless pattern emerges

**Medium Discrepancies ($5-$20)**:
- Recount cash before finalizing shift
- Review transaction log for errors (incorrect change given, voided transaction not processed)
- Document circumstances in shift notes
- Manager review recommended

**Large Discrepancies (>$20)**:
- Mandatory recount
- Manager approval required to close shift
- Review all transactions and cash movements
- Investigate potential causes (theft, till tap, incorrect opening cash)
- May require disciplinary action depending on circumstances

**Consistent Shortages**:
- Pattern of negative discrepancies from same cashier = training issue or theft
- Implement additional oversight (manager spot-checks during shift)
- Review POS training procedures
- Consider cash handling policy updates

## Tips

- **Count opening cash twice** - Opening errors cascade into closing discrepancies; accuracy at start prevents problems at end
- **Record cash movements immediately** - Don't wait until closing to document float adds or petty cash withdrawals
- **Always provide movement reasons** - "Added $100" is useless for audit; "Added $100 for change (low on $5 bills)" is actionable
- **Recount if discrepancy >$10** - Don't finalize shift with large discrepancy without recounting
- **Print shift reports daily** - Attach to daily reconciliation paperwork for accounting
- **Review patterns, not individual discrepancies** - One -$3.00 shortage is fine; five consecutive -$3.00 shortages is a problem
- **Close shifts at end of day** - Don't leave shifts open overnight; discrepancies are easier to investigate when recent
- **Train cashiers on denomination counting** - Most errors come from miscounting bills (thinking a $5 is a $10)
- **Use coin wrappers** - Pre-wrapped coins reduce counting errors and speed up reconciliation
