---
slug: shipping-promotions
title_i18n_key: Shipping Promotions
category: orders-shipping
component: shipping
keywords:
  - shipping promotions
  - conditional shipping
  - free shipping promotions
  - shipping discounts
  - shipping surcharges
  - dynamic shipping
  - shipping promotions
  - cart-based shipping
  - zone shipping promotions
  - shipping adjustments
  - promotion priority
  - shipping conditions
  - advanced shipping
url_patterns:
  - /admin/shipping/shippingpromotion/
  - /admin/shipping/shippingpromotion/add/
  - /admin/shipping/shippingpromotion/\d+/change/
related:
  - shipping-methods
  - shipping-zones
  - sales-promotions
published: true
---

Shipping rules apply conditional cost adjustments to shipping methods based on cart contents, customer attributes, and delivery zones—automatically offer free shipping over $50, add surcharges for remote areas, or discount shipping for VIP customers. Rules use priority-based execution (higher priority first) with optional stop flags to prevent further processing. Each rule evaluates multiple conditions (cart value, weight, zones, products, customer groups) and executes one of 6 adjustment types when all conditions match.

Use shipping promotions when you need dynamic shipping costs that change based on order context, not just static rates from shipping methods.

## Shipping Promotion Types

Shipping rules apply 6 types of cost adjustments:

### Percentage Discount

**What It Does**: Reduces shipping cost by percentage (e.g., 25% off).

**Formula**: `new_cost = base_cost × (1 - percent/100)`

**Example**:
```
Base cost: $20
Discount: 25%
Result: $15
```

**Use Cases**:
- VIP customer discount (20% off all shipping)
- Seasonal promotions (15% off shipping in December)
- Bulk order discount (10% off shipping for 5+ items)

---

### Fixed Discount

**What It Does**: Subtracts fixed amount from shipping cost.

**Formula**: `new_cost = base_cost - amount` (minimum $0)

**Example**:
```
Base cost: $15
Discount: $5
Result: $10
```

**Use Cases**:
- First-time customer bonus ($5 off first order shipping)
- Newsletter signup reward ($3 off shipping)
- Loyalty program benefit ($10 off shipping per month)

---

### Override Cost

**What It Does**: Overrides shipping cost to specific amount.

**Formula**: `new_cost = fixed_amount`

**Example**:
```
Base cost: $25
Set to: $9.99
Result: $9.99
```

**Use Cases**:
- Flash sale (flat $5 shipping for all orders today)
- Category-specific shipping (books always $3.99 shipping)
- Time-based promotions (shipping capped at $9.99 this week)

---

### Free Shipping

**What It Does**: Sets shipping cost to $0.

**Formula**: `new_cost = $0`

**Example**:
```
Base cost: $18
Rule applies
Result: $0
```

**Use Cases**:
- Free shipping over $50
- Free shipping for specific products (promotional items)
- Free shipping to VIP customers
- Free shipping on orders with 3+ items

---

### Surcharge (Fixed)

**What It Does**: Adds fixed amount to shipping cost.

**Formula**: `new_cost = base_cost + amount`

**Example**:
```
Base cost: $12
Surcharge: $5
Result: $17
```

**Use Cases**:
- Remote area delivery fee
- Oversized item handling
- Saturday delivery surcharge
- Fragile item packaging fee

---

### Surcharge (Percentage)

**What It Does**: Increases shipping cost by percentage.

**Formula**: `new_cost = base_cost × (1 + percent/100)`

**Example**:
```
Base cost: $20
Surcharge: 15%
Result: $23
```

**Use Cases**:
- Peak season surcharge (20% during holidays)
- Express delivery premium (50% surcharge)
- Fuel surcharge (variable based on current rates)

---

## Promotion Conditions

Promotions evaluate **ALL conditions must pass** for rule to apply:

### Time Validity

- **Start Date**: Rule only active after this date
- **End Date**: Rule only active before this date
- **Use Case**: Seasonal promotions, limited-time offers

**Example**: Free shipping Black Friday weekend only
```
Start: 2026-11-27 00:00
End: 2026-11-30 23:59
```

---

### Cart Value Range

- **Min Cart Value**: Cart subtotal must be ≥ amount
- **Max Cart Value**: Cart subtotal must be ≤ amount
- **Use Case**: Free shipping thresholds, tiered discounts

**Example**: Free shipping for orders $50-$200
```
Min: $50
Max: $200
```

---

### Cart Weight Range

- **Min Weight**: Total cart weight must be ≥ amount
- **Max Weight**: Total cart weight must be ≤ amount
- **Use Case**: Lightweight shipment discounts, heavy item surcharges

**Example**: $5 surcharge for orders over 20kg
```
Min Weight: 20kg
Max Weight: null (unlimited)
```

---

### Item Count Range

- **Min Item Count**: Cart must have ≥ quantity of items
- **Max Item Count**: Cart must have ≤ quantity of items
- **Use Case**: Bulk order discounts, single-item fees

**Example**: Free shipping for 5+ items
```
Min Items: 5
Max Items: null
```

---

### Shipping Zone

- **Zones**: Rule only applies if customer address matches at least one selected zone
- **Empty selection**: Rule applies to ALL zones
- **Use Case**: Zone-specific surcharges or discounts

**Example**: Free shipping for Domestic zone only
```
Zones: ["Domestic USA"]
```

---

### Shipping Method

- **Methods**: Rule only applies to specific shipping methods
- **Empty selection**: Rule applies to ALL methods
- **Use Case**: Method-specific promotions

**Example**: 25% off Express Shipping
```
Methods: ["Express Delivery"]
```

---

### Product Requirements

**Requires Products**: Cart must contain at least one of these products

**Requires Categories**: Cart must contain at least one product from these categories

**Use Case**: Product-specific free shipping, promotional bundles

**Example**: Free shipping when cart contains "Promotion Item A"
```
Requires Products: [Product ID 123]
```

---

### Product Exclusions

**Excludes Products**: Rule doesn't apply if cart contains any of these products

**Excludes Categories**: Rule doesn't apply if cart contains any products from these categories

**Use Case**: Exclude heavy/oversized items from free shipping

**Example**: Free shipping except for furniture category
```
Excludes Categories: [Furniture]
```

---

### Customer Group

- **Customer Groups**: Rule only applies to customers in selected groups (VIP, Wholesale, etc.)
- **Empty selection**: Rule applies to ALL customer groups
- **Use Case**: VIP benefits, wholesale discounts

**Example**: 15% shipping discount for VIP members
```
Customer Groups: ["VIP"]
```

---

### First-Time Customer

- **First Time Customer**: Toggle to restrict rule to customers with no previous orders
- **Use Case**: New customer welcome offers

**Example**: $5 off shipping for first order
```
First Time Customer: Yes
```

---

## Promotion Priority & Execution

Promotions execute in **priority order** (higher number = earlier execution):

### Priority Mechanics

**Example Execution**:
```
Promotion A (Priority 100): Free shipping if cart > $50
Promotion B (Priority 50): 10% discount on all shipping
Promotion C (Priority 1): $2 surcharge for remote zones

Cart: $60, Remote zone
Base shipping cost: $15

Step 1: Promotion A evaluates (Priority 100)
  Cart > $50? YES
  Apply: Set cost to $0
  Cost now: $0

Step 2: Promotion B evaluates (Priority 50)
  Apply 10% discount to $0
  Cost now: $0 (still free)

Step 3: Promotion C evaluates (Priority 1)
  Add $2 surcharge to $0
  Cost now: $2

Final cost: $2
```

**Stop Further Promotions Flag**:

If Promotion A has `stop_further_promotions = True`:
```
Promotion A (Priority 100, stop_further_promotions=True): Free shipping if cart > $50
Promotion B (Priority 50): 10% discount
Promotion C (Priority 1): $2 surcharge

Cart: $60
Base: $15

Step 1: Promotion A applies, sets cost to $0
        stop_further_promotions = True → STOP

Final cost: $0 (Rules B and C never execute)
```

---

## Creating Shipping Promotions

**Step-by-Step Workflow**:

1. **Navigate to Rules**
   - Settings > Shipping > Shipping Promotions
   - Click "Add Shipping Promotion"

2. **Basic Configuration**
   - **Name**: Internal identifier (e.g., "Free Shipping Over $50")
   - **Description**: Optional notes (not shown to customers)
   - **Active**: Toggle to enable/disable
   - **Priority**: Set execution order (100 for high priority, 1 for low)

3. **Choose Promotion Type**
   - Select adjustment type (discount %, discount fixed, set cost, free, surcharge %, surcharge fixed)
   - Enter amount or percentage

4. **Set Stop Flag** (Optional)
   - Check "Stop Further Promotions" if this rule should prevent lower-priority promotions from executing
   - Use for final/absolute rules (e.g., free shipping should not have surcharges added after)

5. **Define Conditions** (Optional - leave empty for "always apply")
   - Time validity: Start/end dates
   - Cart value: Min/max
   - Cart weight: Min/max
   - Item count: Min/max
   - Zones: Select applicable zones
   - Methods: Select applicable methods
   - Products: Required or excluded
   - Customer: Groups or first-time only

6. **Save Rule**
   - Click Save
   - Rule becomes active immediately (if active toggle is Yes)

---

## Common Shipping Promotion Scenarios

### Scenario 1: Free Shipping Over $50

**Goal**: Offer free shipping when cart subtotal ≥ $50.

**Configuration**:
```
Name: Free Shipping Over $50
Type: Free Shipping
Priority: 100
Conditions:
  Min Cart Value: $50
Stop Further Promotions: Yes
```

---

### Scenario 2: Remote Area Surcharge

**Goal**: Add $10 surcharge for deliveries to remote zones.

**Configuration**:
```
Name: Remote Area Surcharge
Type: Surcharge (Fixed)
Amount: $10
Priority: 50
Conditions:
  Zones: ["Remote Areas"]
Stop Further Promotions: No
```

---

### Scenario 3: VIP Customer 20% Discount

**Goal**: VIP customers get 20% off all shipping.

**Configuration**:
```
Name: VIP Shipping Discount
Type: Discount (Percentage)
Percentage: 20
Priority: 75
Conditions:
  Customer Groups: ["VIP"]
Stop Further Promotions: No
```

---

### Scenario 4: Holiday Flat Rate

**Goal**: All shipping capped at $9.99 during December.

**Configuration**:
```
Name: December Flat Rate Promo
Type: Override Cost
Amount: $9.99
Priority: 100
Conditions:
  Start Date: 2026-12-01
  End Date: 2026-12-31
Stop Further Promotions: Yes
```

---

### Scenario 5: Heavy Item Surcharge

**Goal**: Add $15 fee for orders over 25kg.

**Configuration**:
```
Name: Heavy Order Surcharge
Type: Surcharge (Fixed)
Amount: $15
Priority: 50
Conditions:
  Min Weight: 25kg
Stop Further Promotions: No
```

---

### Scenario 6: First Order Free Shipping

**Goal**: New customers get free shipping on first order.

**Configuration**:
```
Name: First Order Free Shipping
Type: Free Shipping
Priority: 100
Conditions:
  First Time Customer: Yes
Stop Further Promotions: Yes
```

---

### Scenario 7: Category-Specific Free Shipping

**Goal**: Free shipping for orders containing promotional category items.

**Configuration**:
```
Name: Promo Category Free Shipping
Type: Free Shipping
Priority: 90
Conditions:
  Requires Categories: ["Promotions"]
Stop Further Promotions: Yes
```

---

### Scenario 8: Exclude Furniture from Free Shipping

**Goal**: Free shipping over $50, except if cart contains furniture.

**Solution**: Two rules

**Promotion 1**:
```
Name: General Free Shipping
Type: Free Shipping
Priority: 50
Conditions:
  Min Cart Value: $50
  Excludes Categories: ["Furniture"]
Stop Further Promotions: No
```

**Promotion 2**:
```
Name: Furniture Orders $5 Discount
Type: Discount (Fixed)
Amount: $5
Priority: 40
Conditions:
  Requires Categories: ["Furniture"]
  Min Cart Value: $50
Stop Further Promotions: No
```

---

## Promotion Combination Strategies

### Strategy 1: Stacking Discounts

**Allow multiple discounts to stack**:
```
Promotion A (Priority 100): 10% off for VIP → stop_further_promotions=No
Promotion B (Priority 50): 15% off orders >$100 → stop_further_promotions=No

VIP customer with $120 order:
Base: $15
After Promotion A: $13.50 (10% off)
After Promotion B: $11.48 (15% off $13.50)
```

### Strategy 2: Exclusive Rules

**Only one rule applies** (highest priority):
```
Promotion A (Priority 100): Free shipping >$50 → stop_further_promotions=Yes
Promotion B (Priority 50): 20% off all shipping → stop_further_promotions=Yes

Cart > $50:
Promotion A applies → Free shipping → STOP
Promotion B never executes
```

### Strategy 3: Conditional Surcharges

**Discounts first, surcharges last**:
```
Promotion A (Priority 100): Free shipping >$75
Promotion B (Priority 75): 15% VIP discount
Promotion C (Priority 50): 10% general discount
Promotion D (Priority 25): $5 remote area surcharge
Promotion E (Priority 1): 10% fuel surcharge

Order: $80, Remote zone, VIP customer
Base: $20
A: $80 > $75 → Free ($0)
B: VIP → 15% off $0 = $0
C: 10% off $0 = $0
D: Remote +$5 = $5
E: Fuel +10% of $5 = $5.50

Final: $5.50 (not free due to surcharges)
```

**To prevent this, use stop_further_promotions=Yes**:
```
Promotion A (Priority 100, stop=Yes): Free shipping >$75

Same order:
A: $80 > $75 → Free ($0) → STOP
Final: $0 (truly free)
```

---

## Testing Shipping Promotions

**Before going live**:

1. **Create Test Carts**
   - Cart A: $25 (below threshold)
   - Cart B: $55 (above threshold)
   - Cart C: $200 + Remote zone
   - Cart D: VIP customer

2. **Test Each Rule**
   - Proceed to checkout
   - Verify correct shipping cost displayed
   - Check rule execution order

3. **Test Priority Resolution**
   - Multiple matching rules
   - Verify highest priority executes first
   - Check stop_further_promotions behavior

4. **Test Edge Cases**
   - Cart value exactly at threshold
   - Multiple conditions matching
   - Conflicting rules

---

## Troubleshooting

**Issue 1: Promotion not applying**

**Causes**:
- Rule is inactive
- One or more conditions not met
- Higher priority rule set stop_further_promotions=Yes
- Time validity outside current date

**Solution**: Review all conditions, check priority, verify active status.

---

**Issue 2: Unexpected discount amount**

**Causes**:
- Multiple promotions stacking
- Percentage applied to already-discounted cost
- Rule priority incorrect

**Solution**: Check priority order, review stop_further_promotions flags, trace execution manually.

---

**Issue 3: Free shipping not working**

**Causes**:
- Lower priority surcharge rule adding cost after free shipping promotion
- Cart doesn't meet min value threshold
- Excluded products in cart

**Solution**: Use stop_further_promotions=Yes on free shipping promotion, verify conditions, check exclusions.

---

## Tips

- **Use high priority for free shipping** - Priority 100 ensures it executes before other adjustments
- **Set stop_further_promotions for absolute rules** - Free shipping should stop further processing
- **Test rule combinations** - Multiple promotions can interact unexpectedly
- **Use descriptive names** - "VIP 20% Discount (Priority 75)" better than "Promotion 3"
- **Document complex logic** - Add notes in description field
- **Start with simple promotions** - Add complexity gradually
- **Monitor rule performance** - Check if rules are being used or causing confusion
- **Avoid excessive promotions** - Too many promotions slow checkout, use 5-10 max
- **Use zones for geography** - Better than multiple similar rules per country
- **Combine with methods** - Rules + Methods work together for sophisticated pricing
- **Set clear time windows** - Always include end dates for promotions
- **Test edge cases** - Exactly $50, exactly 5 items, etc.
