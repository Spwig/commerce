---
slug: shipping-methods
title_i18n_key: Shipping Methods
category: orders-shipping
component: cart
keywords:
  - shipping methods
  - flat rate shipping
  - free shipping
  - weight-based shipping
  - price-based shipping
  - real-time rates
  - local pickup
  - table rate shipping
  - shipping cost
  - delivery options
  - shipping calculator
  - checkout shipping
  - carrier rates
  - shipping zones
url_patterns:
  - /admin/cart/shippingmethod/
  - /admin/cart/shippingmethod/add/
  - /admin/cart/shippingmethod/\d+/change/
related:
  - shipping-zones
  - shipping-promotions
  - shipping-packages
published: true
---

Shipping methods are the customer-facing delivery options displayed at checkout—each method calculates shipping costs using different pricing strategies. Spwig supports 7 method types ranging from simple flat rates to complex carrier-calculated real-time pricing. Methods can be restricted by minimum/maximum order value, weight, and geographic zones. Customers select their preferred method during checkout, and the calculated cost is added to their order total.

Use this guide to configure shipping methods that match your business model, from basic flat-rate shipping to sophisticated zone-based tiered pricing.

## Shipping Method Types

Spwig provides 7 shipping method types, each with different cost calculation logic:

### Flat Rate Shipping

**What It Is**: Fixed cost regardless of cart contents, destination, or weight.

**When to Use**:
- Simple stores with predictable shipping costs
- Single product type (similar size/weight)
- Domestic-only shipping with standard carrier rates
- Free shipping threshold promotions (use with shipping promotions)

**Configuration**:
- Set **Method Type** = Flat Rate
- Enter **Fixed Cost** (e.g., $9.99)
- Optional: Set min/max order value restrictions

**Example**: "Standard Shipping - $9.99" for all domestic orders.

---

### Free Shipping

**What It Is**: Zero cost shipping option (no charge to customer).

**When to Use**:
- Free shipping promotions
- High-value orders (combine with min order value)
- Local pickup alternative
- Loyalty program perks

**Configuration**:
- Set **Method Type** = Free Shipping
- Optional: Set **Min Order Value** (e.g., free over $50)
- Works well with shipping promotions for conditional free shipping

**Example**: "Free Shipping on Orders Over $50" with min_order_value = $50.

---

### Weight-Based Shipping

**What It Is**: Cost calculated from tiered rate table based on total cart weight.

**When to Use**:
- Products with variable weights (books, hardware, groceries)
- Weight-based carrier pricing models
- Predictable weight-to-cost ratio

**Configuration**:
1. Set **Method Type** = Weight-Based
2. Create **Shipping Rate Table** with basis_type = "weight"
3. Add **Shipping Rate Tiers** (e.g., 0-5kg = $10, 5-10kg = $15, 10-20kg = $25)
4. Optional: Restrict to specific zones

**Example**:
```
0-2kg: $8
2-5kg: $12
5-10kg: $18
10kg+: $25
```

**How It Works**: Cart calculates total weight → finds matching tier → returns tier's rate.

---

### Price-Based Shipping

**What It Is**: Cost calculated from tiered rate table based on cart subtotal.

**When to Use**:
- Shipping cost correlates with order value
- Encourage higher cart values (lower rate per dollar at higher tiers)
- Simple alternative to weight-based for similar-priced items

**Configuration**:
1. Set **Method Type** = Price-Based
2. Create **Shipping Rate Table** with basis_type = "price"
3. Add **Shipping Rate Tiers** (e.g., $0-$50 = $9.99, $50-$100 = $14.99, $100+ = $19.99)

**Example**:
```
$0-$25: $6.99
$25-$75: $9.99
$75-$150: $12.99
$150+: Free
```

**How It Works**: Cart calculates subtotal → finds matching tier → returns tier's rate.

---

### Real-Time Carrier Rates

**What It Is**: Live rates fetched from carrier APIs (FedEx, UPS, DHL) at checkout.

**When to Use**:
- Variable shipping costs by destination
- Multiple carrier options for customers
- Accurate carrier pricing without manual rate tables
- International shipping with complex pricing

**Configuration**:
1. Set **Method Type** = Real-Time
2. Create **Provider Account** (Settings > Shipping > Provider Accounts)
3. Enter carrier API credentials (account number, API key, secret)
4. Link provider account to shipping method
5. Optional: Add markup percentage or fixed markup

**Requirements**:
- Active carrier account (FedEx, UPS, DHL, etc.)
- API credentials from carrier
- Shipping packages defined (for dimensional weight calculation)

**Example**: "FedEx Ground" method fetches live FedEx rates based on cart weight, dimensions, and destination at checkout.

**How It Works**:
1. Customer enters address at checkout
2. System calls carrier API with origin, destination, package dimensions, weight
3. Carrier returns rate quote
4. Optional markup applied
5. Rate displayed to customer

---

### Local Pickup

**What It Is**: Customer picks up order at physical location (no delivery cost).

**When to Use**:
- Retail stores offering pickup
- Warehouse pickup options
- Events or market stalls
- Eliminate shipping costs for local customers

**Configuration**:
1. Set **Method Type** = Local Pickup
2. Create **Location** (Settings > Shipping > Locations)
   - Set address, operating hours, pickup capacity
3. Link location(s) to method
4. Optional: Set pickup preparation time (e.g., "Ready in 2 hours")

**Customer Experience**:
- Selects "Local Pickup" at checkout
- Chooses pickup location (if multiple)
- Selects pickup date/time based on availability
- Receives notification when order ready

**Example**: "Pickup at Store - Free" with 3 retail locations, ready within 24 hours.

---

### Table Rate Shipping

**What It Is**: Flexible tiered pricing based on weight, price, or quantity with advanced zone targeting.

**When to Use**:
- Complex pricing (different rates by zone AND weight)
- Need more control than weight-based or price-based alone
- Multiple pricing factors (e.g., weight + destination + quantity)

**Configuration**:
1. Set **Method Type** = Table Rate
2. Create **Shipping Rate Table**
3. Define **basis_type**: weight, price, or quantity
4. Add **Shipping Rate Tiers** with min/max values
5. Optional: Restrict tiers to specific zones or countries

**Difference from Weight/Price-Based**: Table rate supports geographic restrictions per tier, allowing different rates for same weight/price in different zones.

**Example**:
```
Zone A (Domestic):
  0-5kg: $10
  5-10kg: $15

Zone B (Remote):
  0-5kg: $18
  5-10kg: $25
```

**How It Works**: Cart calculates basis value (weight/price/quantity) → finds matching tier for customer's zone → returns tier's rate.

---

## Shipping Method Configuration

All shipping methods share these common settings:

### Basic Settings

- **Name**: Internal identifier (not shown to customers)
- **Display Name**: Customer-facing name at checkout (e.g., "Standard Shipping", "Express Delivery")
- **Description**: Optional help text shown at checkout (e.g., "Delivery in 3-5 business days")
- **Method Type**: One of 7 types above
- **Active**: Toggle to enable/disable method without deletion

### Cost Settings

- **Fixed Cost**: For flat-rate methods only
- **Rate Table**: For weight-based, price-based, table-rate methods
- **Provider Account**: For real-time carrier methods
- **Tax Class**: Apply tax to shipping cost (if applicable)

### Restrictions

**Order Value Restrictions**:
- **Min Order Value**: Method only available if cart subtotal ≥ amount (e.g., free shipping over $50)
- **Max Order Value**: Method hidden if cart subtotal > amount (e.g., flat rate only for orders under $100)

**Weight Restrictions**:
- **Min Weight**: Method only available if cart weight ≥ amount
- **Max Weight**: Method hidden if cart weight > amount (common for lightweight shipping options)

**Geographic Restrictions**:
- **Shipping Zones**: Link method to specific zones (domestic, international, regional)
- Empty zones = available to all addresses
- Multiple zones = available to any matching zone

### Advanced Settings

- **Priority**: Display order in checkout (lower number = higher in list)
- **Handling Fee**: Additional flat fee added to calculated cost
- **Free Shipping Threshold**: Auto-set cost to $0 if cart subtotal ≥ threshold (alternative to min_order_value)

---

## Creating a Shipping Method

**Step-by-Step Workflow**:

1. **Navigate to Shipping Methods**
   - Go to Settings > Cart > Shipping Methods
   - Click "Add Shipping Method"

2. **Choose Method Type**
   - Select appropriate type based on your pricing strategy
   - Type determines available cost configuration fields

3. **Configure Basic Info**
   - Name: Internal reference (e.g., "domestic_ground")
   - Display Name: Customer-facing (e.g., "Ground Shipping")
   - Description: Delivery timeframe (e.g., "5-7 business days")

4. **Set Cost Calculation**
   - **Flat Rate**: Enter fixed cost
   - **Weight/Price/Table Rate**: Create rate table (see below)
   - **Real-Time**: Link provider account
   - **Free/Pickup**: No cost configuration needed

5. **Add Restrictions (Optional)**
   - Min/max order value
   - Min/max weight
   - Shipping zones

6. **Set Priority**
   - Lower numbers appear first at checkout
   - Recommended order: Free (1), Local Pickup (2), Standard (3), Express (4)

7. **Activate Method**
   - Toggle "Active" = Yes
   - Save

---

## Creating Rate Tables

For weight-based, price-based, and table-rate methods:

**Step 1: Create Rate Table**
- Go to Settings > Shipping > Rate Tables
- Click "Add Rate Table"
- Set **Name** (e.g., "Domestic Weight Tiers")
- Set **Basis Type**: weight, price, or quantity

**Step 2: Add Tiers**
- Click "Add Tier"
- Set **Min Value** and **Max Value** (range for matching)
- Set **Rate** (cost for this tier)
- Optional: Restrict to specific zones or countries
- Save tier

**Step 3: Repeat for All Tiers**
- Cover full range (0 to maximum expected value)
- Ensure no gaps (e.g., 0-5, 5-10, 10-20, 20+)
- Use `null` for max value in final tier (unlimited)

**Step 4: Link to Shipping Method**
- Edit shipping method
- Select rate table from dropdown
- Save

**Example Weight-Based Table**:
```
Name: Domestic Weight Tiers
Basis: Weight

Tiers:
1. Min: 0g, Max: 2000g, Rate: $8
2. Min: 2000g, Max: 5000g, Rate: $12
3. Min: 5000g, Max: 10000g, Rate: $18
4. Min: 10000g, Max: null, Rate: $25
```

---

## Common Shipping Scenarios

### Scenario 1: Basic Domestic Shipping

**Goal**: Simple $9.99 flat rate for all domestic orders.

**Solution**:
- Method Type: Flat Rate
- Fixed Cost: $9.99
- Shipping Zone: "Domestic" (your country only)

---

### Scenario 2: Free Shipping Over $50

**Goal**: Encourage higher cart values with free shipping threshold.

**Solution Option A** (Recommended):
- Method Type: Free Shipping
- Min Order Value: $50
- Display Name: "Free Shipping (Orders $50+)"

**Solution Option B** (Using Rules):
- Method Type: Flat Rate
- Fixed Cost: $9.99
- Create Shipping Promotion:
  - Condition: Cart value ≥ $50
  - Action: Set cost to $0

---

### Scenario 3: Weight-Based Domestic + International

**Goal**: Different rates for domestic vs international based on weight.

**Solution**:
1. Create 2 zones: "Domestic", "International"
2. Create 2 rate tables: "Domestic Weight", "International Weight"
3. Create 2 methods:
   - "Domestic Shipping" → links to Domestic zone + Domestic Weight table
   - "International Shipping" → links to International zone + International Weight table

---

### Scenario 4: Multiple Carrier Options

**Goal**: Let customers choose between FedEx Ground, FedEx Express, UPS Ground.

**Solution**:
1. Create Provider Account for FedEx API
2. Create Provider Account for UPS API
3. Create 3 real-time methods:
   - "FedEx Ground" → FedEx provider, service code = "FEDEX_GROUND"
   - "FedEx Express" → FedEx provider, service code = "FEDEX_EXPRESS"
   - "UPS Ground" → UPS provider, service code = "UPS_GROUND"
4. All 3 methods query carrier APIs at checkout and display live rates

---

### Scenario 5: Local Pickup + Delivery

**Goal**: Retail store offers both pickup and delivery options.

**Solution**:
1. Create Location: "Main Store" with address, hours, prep time
2. Create 2 methods:
   - "Local Pickup" → Local Pickup type, links to Main Store location
   - "Standard Delivery" → Flat Rate $9.99
3. Customers see both options at checkout

---

## Testing Shipping Methods

Before going live, test all methods:

1. **Create Test Cart**
   - Add products with various weights/prices
   - Proceed to checkout

2. **Test Each Method**
   - Enter addresses in different zones
   - Verify correct methods appear
   - Check calculated costs match expectations

3. **Test Restrictions**
   - Add items until min_order_value met → verify free shipping appears
   - Add heavy items → verify weight-based tiers work
   - Test zone restrictions → verify methods hidden for excluded zones

4. **Test Real-Time Methods** (if applicable)
   - Use carrier test credentials
   - Verify rates returned successfully
   - Check rate accuracy against carrier website

---

## Troubleshooting

**Issue 1: Method not appearing at checkout**

**Causes**:
- Method is inactive
- Cart doesn't meet min/max order value
- Cart doesn't meet min/max weight
- Customer address doesn't match any linked zones
- No rate table tiers cover cart weight/price

**Solution**: Check restrictions, verify active status, ensure zones/tiers cover customer's scenario.

---

**Issue 2: Real-time rates failing**

**Causes**:
- Invalid API credentials
- Provider account inactive
- No shipping packages defined (carrier needs dimensions)
- Origin address not set
- Carrier API down

**Solution**: Test provider connection, verify credentials, ensure packages configured, check origin address in settings.

---

**Issue 3: Incorrect cost calculated**

**Causes**:
- Rate table tiers have gaps or overlaps
- Tier min/max values in wrong units (grams vs kg)
- Handling fee added unexpectedly
- Shipping rule modifying cost

**Solution**: Review rate table tiers, verify units, check shipping promotions priority.

---

## Tips

- **Start simple** - Use flat rate for first method, add complexity as needed
- **Test thoroughly** - Verify all methods work in staging before enabling in production
- **Use descriptive names** - "Standard Shipping (5-7 days)" better than "Method 1"
- **Set realistic delivery times** - Under-promise, over-deliver for customer satisfaction
- **Offer pickup if possible** - Reduces shipping costs, improves customer convenience
- **Monitor carrier API reliability** - Have flat-rate fallback if real-time rates fail
- **Use zones for international** - Different rates by region prevent losses on expensive destinations
- **Combine with shipping promotions** - Rules add conditional logic (free shipping promotions, surcharges for remote areas)
- **Keep methods limited** - 2-4 options at checkout prevents decision paralysis
- **Update rate tables seasonally** - Carrier rates change, review annually
- **Use priority wisely** - Put free/cheap options first, expensive options last
