---
slug: shipping-packages
title_i18n_key: Shipping Packages
category: orders-shipping
component: shipping
keywords:
  - shipping packages
  - package dimensions
  - box sizes
  - envelope sizes
  - dimensional weight
  - package configuration
  - shipping boxes
  - parcel sizes
  - package types
url_patterns:
  - /admin/shipping/shippingpackage/
  - /admin/shipping/shippingpackage/add/
  - /admin/shipping/shippingpackage/\d+/change/
related:
  - shipping-methods
  - shipping-provider-accounts
published: true
---

Shipping packages define predefined box and envelope sizes for rate calculation and auto-packing—specify internal dimensions (usable space), wall thickness (external dimensions for carrier APIs), weight limits, and packaging cost. Carriers use external dimensions to calculate dimensional weight for accurate rate quotes. Packages have priority ordering for bin-packing algorithms that automatically select optimal package combinations to fit cart items.

Configure packages when using carrier APIs for real-time rates or when you need accurate dimensional weight calculations.

## Package Configuration

Each package defines:

**Dimensions**:
- **Internal Length**: Usable space inside (cm)
- **Internal Width**: Usable space inside (cm)
- **Internal Height**: Usable space inside (cm)
- **Wall Thickness**: Packaging material thickness (cm)

**External Dimensions** (auto-calculated):
```
External Length = Internal Length + (2 × Wall Thickness)
External Width = Internal Width + (2 × Wall Thickness)
External Height = Internal Height + (2 × Wall Thickness)
```

**Weight & Cost**:
- **Tare Weight**: Empty package weight (grams)
- **Max Weight**: Maximum load capacity (grams)
- **Cost**: Packaging material cost (for cost optimization)

**Properties**:
- **Name**: Package identifier (e.g., "Small Box", "Large Envelope")
- **Type**: Box or Envelope
- **Priority**: Auto-pack selection order (lower = higher priority)
- **Active**: Toggle availability

---

## Why External Dimensions Matter

Carriers calculate **dimensional weight** from external dimensions:

**Dimensional Weight Formula**:
```
Dim Weight = (Length × Width × Height) / Divisor

Common Divisors:
- DHL: 5000
- FedEx/UPS: 5000 (domestic), 6000 (international)
```

**Example**:
```
Small Box:
Internal: 20cm × 15cm × 10cm
Wall Thickness: 0.5cm
External: 21cm × 16cm × 11cm

Dimensional Weight = (21 × 16 × 11) / 5000 = 0.74kg

If actual weight = 0.5kg → Carrier bills at 0.74kg (dimensional weight higher)
```

**Why Accuracy Matters**: Inaccurate dimensions → incorrect rate quotes → customer overcharged or undercharged.

---

## Common Package Sizes

### Small Padded Envelope

```
Internal: 25cm × 18cm × 2cm
Wall Thickness: 0.3cm
Max Weight: 500g
Type: Envelope
Use: Documents, books, jewelry
```

### Small Box

```
Internal: 20cm × 15cm × 10cm
Wall Thickness: 0.5cm
Max Weight: 5kg
Type: Box
Use: Small electronics, cosmetics, accessories
```

### Medium Box

```
Internal: 30cm × 25cm × 20cm
Wall Thickness: 0.5cm
Max Weight: 15kg
Type: Box
Use: Clothing, shoes, kitchen items
```

### Large Box

```
Internal: 45cm × 35cm × 30cm
Wall Thickness: 0.6cm
Max Weight: 30kg
Type: Box
Use: Bulk items, multiple products, large electronics
```

---

## Auto-Packing Algorithm

System automatically selects packages for cart items:

**How It Works**:
1. Calculate total volume of cart items
2. Sort packages by priority (lowest number first)
3. Try to fit items into single package
4. If doesn't fit, try next package size
5. If no single package fits, combine multiple packages
6. Optimize based on `optimize_for` setting

**Optimization Modes**:
- **Cost**: Minimize packaging cost
- **Volume**: Minimize wasted space
- **Count**: Minimize number of packages

**Example**:
```
Cart Items:
- Item A: 10cm × 8cm × 5cm, 200g
- Item B: 15cm × 12cm × 8cm, 400g

Packages (by priority):
1. Small Box (20×15×10, priority=1)
2. Medium Box (30×25×20, priority=2)

Algorithm:
Try Small Box: Both items fit
Result: 1× Small Box (optimized for count)
```

---

## Package Priority

**Priority determines pack order**:

Priority 1 (highest): Small packages tried first
Priority 10: Large packages last resort

**Strategy**:
- Small packages = low priority numbers (1-3)
- Medium packages = mid priority (4-6)
- Large packages = high priority numbers (7-10)

**Why**: Start with smallest package, scale up if needed → minimizes shipping cost.

---

## Wall Thickness Accuracy

Measure actual packaging:

**How To Measure**:
1. Get empty box
2. Measure interior dimensions (internal)
3. Measure exterior dimensions (external)
4. Calculate: `(External - Internal) / 2 = Wall Thickness`

**Example**:
```
Internal Width: 20cm
External Width: 21cm
Wall Thickness: (21 - 20) / 2 = 0.5cm
```

**Common Thicknesses**:
- Padded envelope: 0.2-0.4cm
- Single-wall cardboard: 0.4-0.6cm
- Double-wall cardboard: 0.8-1.0cm

---

## Creating Package Preset

**Step-by-Step**:

1. Settings > Shipping > Shipping Packages
2. Click "Add Shipping Package"
3. Enter name (e.g., "Medium Box")
4. Select type (Box or Envelope)
5. Enter internal dimensions (L × W × H in cm)
6. Enter wall thickness (cm)
7. System auto-calculates external dimensions
8. Enter tare weight (empty package weight in grams)
9. Enter max weight (load capacity in grams)
10. Optional: Enter cost (for cost optimization)
11. Set priority (1-10)
12. Toggle active = Yes
13. Save

---

## Testing Package Selection

**Manual Test**:
1. Add products to test cart
2. Proceed to checkout
3. Select real-time shipping method (uses packages)
4. Verify reasonable rate returned
5. Check carrier response (API logs show selected packages)

**Auto-Pack Preview**:
- Some shipping provider accounts show package breakdown
- View which packages selected for cart
- Verify optimal packing

---

## Tips

- **Measure accurately** - Inaccurate dimensions → incorrect carrier rates
- **Include wall thickness** - Critical for dimensional weight
- **Start with 3-4 sizes** - Small, medium, large covers most scenarios
- **Set realistic max weights** - Box capacity, not theoretical limit
- **Use priority wisely** - Small boxes priority 1, large boxes priority 10
- **Test with real products** - Verify auto-pack selects correct sizes
- **Update when packaging changes** - New supplier = re-measure dimensions
- **Consider special items** - Fragile items may need specific box sizes
- **Keep active packages minimal** - Too many options slow auto-pack algorithm
- **Document packaging** - Note which products fit which packages
