---
title: Заявки на возврат и их обработка
---

Return requests track customer returns from initiation through refund completion—customers select items to return with reasons, merchants approve or reject requests, generate return labels, inspect returned items, and process refunds. The workflow progresses through 9 status stages (pending → approved → label_sent → in_transit → received → inspected → completed/rejected/cancelled) with item-level return reasons, inspection notes, and optional restocking fees.

Use this admin page to review, approve, and process customer return requests efficiently.

## Return Request Workflow

**9-Stage Process**:

### 1. Pending (Customer Initiates)

Customer submits return request:
- Selects items from order
- Provides return reason per item
- Optional customer notes
- Status: `pending`

### 2. Approved/Rejected (Merchant Reviews)

Merchant reviews request:
- **Approve**: Return allowed, proceed to label generation
- **Reject**: Return denied with rejection reason
- Status: `approved` or `rejected`

### 3. Label Sent (Return Shipping)

Return label generated:
- Merchant creates return shipment (optional)
- Return label emailed to customer
- Customer ships items back
- Status: `label_sent`

### 4. In Transit (Customer Ships)

Customer ships items:
- Tracking shows movement
- Automated status update from carrier webhook
- Status: `in_transit`

### 5. Received (Arrives at Warehouse)

Items arrive:
- Warehouse scans shipment
- Items checked in
- Status: `received`

### 6. Inspected (Quality Check)

Merchant inspects items:
- Record item condition (excellent/good/acceptable/damaged/defective)
- Add inspection notes
- Apply restocking fee if applicable
- Status: `inspected`

### 7. Completed (Refund Processed)

Refund issued:
- Create associated refund
- Payment processed
- Return closed
- Status: `completed`

**Alternative Outcomes**:
- **Cancelled**: Customer cancels before shipping
- **Rejected**: Merchant denies after review

---

## Processing Return Requests

**Step-by-Step**:

**Step 1: Review Pending Requests**
- Navigate to Orders > Return Requests
- Filter by status = "Pending"
- Click request to view details

**Step 2: Evaluate Request**
- Review order details
- Check return reasons
- Verify return policy compliance (within return window, items eligible)

**Step 3: Approve or Reject**
- Click "Approve" to accept return
- OR click "Reject" and enter rejection reason
- Save decision

**Step 4: Generate Return Label** (if approved)
- Click "Create Return Shipment"
- Select carrier/service
- System generates return label
- Label auto-emailed to customer
- Status → `label_sent`

**Step 5: Monitor Transit**
- Tracking updates auto-sync from carrier webhooks
- Status auto-advances to `in_transit` when carrier scans package

**Step 6: Receive Items**
- When items arrive, click "Mark as Received"
- Status → `received`

**Step 7: Inspect Items**
- Open return request
- Select item condition from dropdown:
  - Excellent (like new, resalable)
  - Good (minor wear, resalable)
  - Acceptable (visible wear, resalable with discount)
  - Damaged (not resalable)
  - Defective (manufacturing defect)
- Add inspection notes
- Optional: Apply restocking fee (percentage or fixed)
- Status → `inspected`

**Step 8: Process Refund**
- Click "Create Refund"
- System calculates refund amount:
  - Original item price
  - Minus restocking fee (if applied)
  - Minus shipping cost (if non-refundable)
- Create refund (links to return request)
- Status → `completed`

---

## Item-Level Return Reasons

Customers select reason per item:

**Common Reasons**:
- Wrong item received
- Item defective/damaged
- Changed mind/no longer needed
- Item doesn't match description
- Better price found
- Ordered by mistake
- Quality not as expected

**Use Reasons For**:
- Analytics (track common return causes)
- Quality control (identify defective products)
- Process improvement (reduce preventable returns)

---

## Restocking Fees

Apply fees to offset return processing costs:

**Configuration**:
- **Type**: Percentage (e.g., 15%) or Fixed (e.g., $5)
- **When to Apply**: Non-defective returns, opened items, special orders

**Example**:
```
Original purchase: $100
Restocking fee: 15%
Refund amount: $85
```

**Best Practices**:
- Clearly communicate restocking fee policy
- Don't apply to defective items
- Consider waiving for VIP customers

---

## Return Inspection Guidelines

Establish consistent inspection criteria:

**Excellent**:
- Unopened original packaging
- No visible wear
- All accessories included
- Fully resalable at full price

**Good**:
- Opened but minimal use
- Minor packaging wear
- All components present
- Resalable at full price

**Acceptable**:
- Visible use/wear
- Packaging damaged
- Missing non-essential accessories
- Resalable at discount

**Damaged**:
- Physically damaged
- Missing parts
- Not resalable
- Dispose or repair required

**Defective**:
- Manufacturing defect
- Functional failure
- Warranty claim
- Return to manufacturer

---

## Return Shipping Options

**Option 1: Customer Pays Return Shipping**
- No return label provided
- Customer selects own carrier
- Manual tracking number entry

**Option 2: Merchant Provides Pre-Paid Label**
- Generate return label through provider account
- Cost deducted from refund OR merchant absorbs
- Tracking auto-synced

**Option 3: Free Return Shipping**
- Merchant absorbs return shipping cost
- Improves customer satisfaction
- Increases return rate (consider trade-off)

---

## Filtering & Reporting

**Useful Filters**:
- Status: Pending (needs action)
- Date Range: Last 30 days
- Order: Specific order lookup
- Reason: Track return causes

**Return Analytics**:
- Return rate by product
- Most common return reasons
- Average processing time (pending → completed)
- Restocking fee revenue

---

## Tips

- **Set clear return policy** - Communicate window (30 days), conditions, fees
- **Process requests promptly** - Respond to pending requests within 24 hours
- **Inspect thoroughly** - Document condition to prevent disputes
- **Track return reasons** - Use data to improve products/descriptions
- **Automate where possible** - Carrier webhooks auto-update transit status
- **Communicate with customers** - Email updates at each status change
- **Be fair with restocking fees** - Apply consistently, waive for defects
- **Monitor return fraud** - Flag customers with excessive returns
- **Improve packaging** - Reduce damage-related returns
- **Update inventory promptly** - Restore stock after inspection
- **Learn from patterns** - High returns for specific product may indicate quality issue

Remember: Return ONLY the JSON object with "title" and "content" fields. Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown above.