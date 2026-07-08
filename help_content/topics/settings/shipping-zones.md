---
slug: shipping-zones
title_i18n_key: Shipping Zones
category: orders-shipping
component: shipping
keywords:
  - shipping zones
  - geographic shipping
  - regional shipping
  - shipping by country
  - shipping by state
  - postal code shipping
  - domestic shipping
  - international shipping
  - zone-based rates
  - shipping coverage
  - delivery zones
  - shipping restrictions
  - zone priority
  - zone matching
url_patterns:
  - /admin/shipping/shippingzone/
  - /admin/shipping/shippingzone/add/
  - /admin/shipping/shippingzone/\d+/change/
related:
  - shipping-methods
  - shipping-promotions
  - setup-shipping
published: true
---

Shipping zones define geographic regions for targeted shipping rates—group countries, states, or postal codes into zones, then link shipping methods to specific zones for precise rate control. Zones use priority-based matching when addresses qualify for multiple zones (highest priority wins). This system enables sophisticated pricing strategies: charge more for remote areas, offer free shipping domestically, or provide discounted rates for specific regions.

Use zones when you need different shipping costs for different geographic areas, from simple domestic vs international splitting to complex multi-region tiered pricing.

## Understanding Shipping Zones

**What Zones Are**: Named geographic regions defined by country, state/province, and postal code patterns.

**How Zones Work**:
1. Customer enters shipping address at checkout
2. System evaluates all active zones
3. Zones matching customer's address are candidates
4. If multiple zones match, highest priority zone wins
5. Shipping methods linked to winning zone are displayed
6. Methods not linked to any zone (or linked to matching zone) are shown

**Zone Components**:
- **Name**: Zone identifier (e.g., "Domestic", "EU", "Remote Areas")
- **Countries**: List of included country codes (empty = all countries)
- **States/Provinces**: Per-country state restrictions (optional)
- **Postal Code Patterns**: Regex patterns for ZIP/postal code matching (optional)
- **Priority**: Higher number = higher priority when multiple zones match

---

## Zone Matching Logic

Zones use **progressive narrowing** to match addresses:

### Level 1: Country Matching

**Empty country list** → Zone matches ALL countries

**Country list provided** → Address country must be in list

Example:
```
Zone: "Domestic"
Countries: ["US"]
→ Matches: Any US address
→ No match: Canada, UK, etc.
```

### Level 2: State/Province Matching

**No states defined** → Zone matches ALL states in allowed countries

**States defined for specific countries** → Address state must match

Example:
```
Zone: "West Coast"
Countries: ["US"]
States: {"US": ["CA", "OR", "WA"]}
→ Matches: California, Oregon, Washington addresses
→ No match: New York, Texas, etc.
```

### Level 3: Postal Code Matching

**No patterns defined** → Zone matches ALL postal codes in allowed country/states

**Patterns defined** → Address postal code must match at least one pattern

Example:
```
Zone: "Los Angeles Metro"
Countries: ["US"]
States: {"US": ["CA"]}
Postal Patterns: ["^90[0-9]{3}$", "^91[0-9]{3}$"]
→ Matches: 90001, 91210, 90245
→ No match: 94102 (San Francisco)
```

**Regex Pattern Examples**:
- `^90[0-9]{3}$` - Los Angeles area (90000-90999)
- `^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$` - Canadian postal code format (K1A 0B1)
- `^SW[0-9]{1,2}` - London UK postcodes starting with SW

---

## Priority-Based Zone Selection

When multiple zones match an address, **priority** determines which zone applies:

**How Priority Works**:
- Higher number = higher priority
- If address matches zones with priority 100 and 50, priority 100 wins
- Only winning zone's shipping methods are available

**Use Cases**:

**Scenario 1: Specific Overrides General**
```
Zone A: "Remote Alaska"
  Countries: ["US"]
  States: {"US": ["AK"]}
  Priority: 100

Zone B: "Domestic USA"
  Countries: ["US"]
  Priority: 50

Address: Anchorage, AK
→ Matches both zones
→ Priority 100 wins
→ "Remote Alaska" zone applies (higher shipping cost)
```

**Scenario 2: Postal Code Overrides State**
```
Zone A: "Manhattan Premium"
  Countries: ["US"]
  States: {"US": ["NY"]}
  Postal Patterns: ["^100[0-2][0-9]$"]
  Priority: 100

Zone B: "New York State"
  Countries: ["US"]
  States: {"US": ["NY"]}
  Priority: 50

Address: New York, NY 10001
→ Matches both zones
→ Priority 100 wins
→ "Manhattan Premium" applies (premium delivery service)
```

---

## Creating Shipping Zones

**Step-by-Step Workflow**:

1. **Navigate to Zones**
   - Go to Settings > Shipping > Shipping Zones
   - Click "Add Shipping Zone"

2. **Basic Configuration**
   - **Name**: Descriptive identifier (e.g., "European Union", "West Coast", "Remote Areas")
   - **Priority**: Set relative importance (100 for specific, 50 for general, 1 for fallback)
   - **Active**: Toggle to enable/disable

3. **Define Geographic Coverage**

   **Option A: All Countries** (leave country list empty)
   - Zone matches every address globally
   - Use for default/fallback zones

   **Option B: Specific Countries**
   - Click "Add Country"
   - Select countries from dropdown (US, CA, UK, etc.)
   - Repeat for all included countries

   **Option C: Specific States/Provinces**
   - After adding countries, click "Add States" for each country
   - Select states from dropdown
   - Example: US → CA, OR, WA for West Coast

   **Option D: Postal Code Patterns** (advanced)
   - Enter regex patterns (one per line)
   - Test patterns with sample postal codes
   - Click "Validate Patterns" to check syntax

4. **Link to Shipping Methods**
   - Methods can be linked when editing the method (not in zone config)
   - Or link zones to existing methods: Edit Method → Shipping Zones → Select zones

5. **Set Display Priority**
   - Higher priority zones override lower priority when multiple match
   - Recommended: Specific zones (100), Regional zones (50), Default zone (1)

6. **Activate Zone**
   - Toggle "Active" = Yes
   - Save

---

## Common Zone Setups

### Setup 1: Domestic vs International

**Goal**: Different rates for domestic vs all other countries.

```
Zone 1: "Domestic"
  Countries: [Your Country Code]
  Priority: 50

Zone 2: "International"
  Countries: [Leave empty or select all other countries]
  Priority: 1
```

**Shipping Methods**:
- "Domestic Standard" → Links to Domestic zone
- "International Shipping" → Links to International zone

---

### Setup 2: Multi-Region International

**Goal**: Different rates for EU, North America, Asia, Rest of World.

```
Zone 1: "European Union"
  Countries: [AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK]
  Priority: 100

Zone 2: "North America"
  Countries: [US, CA, MX]
  Priority: 100

Zone 3: "Asia Pacific"
  Countries: [AU, CN, HK, IN, JP, KR, NZ, SG, TH, TW]
  Priority: 100

Zone 4: "Rest of World"
  Countries: [Leave empty]
  Priority: 1
```

**Shipping Methods**:
- "EU Shipping" → EU zone
- "North America Shipping" → North America zone
- "Asia Pacific Shipping" → Asia Pacific zone
- "International Standard" → Rest of World zone

---

### Setup 3: Remote Area Surcharge

**Goal**: Add surcharge for remote postal codes within domestic zone.

```
Zone 1: "Remote Domestic"
  Countries: [US]
  Postal Patterns: ["^99[0-9]{3}$", "^96[7-9][0-9]{2}$"]  # Alaska, Hawaii
  Priority: 100

Zone 2: "Standard Domestic"
  Countries: [US]
  Priority: 50
```

**Shipping Methods**:
- "Remote Shipping" → Remote Domestic zone (higher cost)
- "Standard Shipping" → Standard Domestic zone

---

### Setup 4: State-Specific Zones

**Goal**: Different rates for each US region.

```
Zone 1: "West Coast"
  Countries: [US]
  States: {"US": ["CA", "OR", "WA"]}
  Priority: 100

Zone 2: "East Coast"
  Countries: [US]
  States: {"US": ["NY", "NJ", "CT", "MA", "PA"]}
  Priority: 100

Zone 3: "Midwest"
  Countries: [US]
  States: {"US": ["IL", "IN", "OH", "MI", "WI"]}
  Priority: 100

Zone 4: "South"
  Countries: [US]
  States: {"US": ["TX", "FL", "GA", "NC", "SC"]}
  Priority: 100

Zone 5: "Other US States"
  Countries: [US]
  Priority: 50
```

---

## Postal Code Pattern Examples

Postal codes use **regex** (regular expressions) for pattern matching:

### United States (ZIP Codes)

**Format**: 5 digits (e.g., 90210)

```
California (90000-96199):  ^9[0-6][0-9]{3}$
New York (10000-14999):    ^1[0-4][0-9]{3}$
Texas (75000-79999, 88500-88599):  ^(7[5-9]|885)[0-9]{2}$
Alaska (99500-99999):      ^99[5-9][0-9]{2}$
```

### Canada (Postal Codes)

**Format**: A1A 1A1 (letter-number-letter space number-letter-number)

```
All Canadian postal codes:  ^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$
Ontario (K, L, M, N, P):    ^[KLMNP][0-9][A-Z] [0-9][A-Z][0-9]$
Quebec (G, H, J):           ^[GHJ][0-9][A-Z] [0-9][A-Z][0-9]$
```

### United Kingdom (Postcodes)

**Format**: AA1A 1AA or A1A 1AA

```
London (E, EC, N, NW, SE, SW, W, WC):  ^(E|EC|N|NW|SE|SW|W|WC)[0-9]{1,2}
Manchester (M):                        ^M[0-9]{1,2}
Birmingham (B):                        ^B[0-9]{1,2}
```

### Australia (Postcodes)

**Format**: 4 digits (e.g., 2000)

```
New South Wales (1000-2999):  ^[12][0-9]{3}$
Victoria (3000-3999, 8000-8999):  ^[38][0-9]{3}$
Queensland (4000-4999, 9000-9999):  ^[49][0-9]{3}$
```

### Pattern Testing

**Before saving patterns**, test with known postal codes:

1. Enter pattern: `^90[0-9]{3}$`
2. Test input: "90210" → Should match
3. Test input: "10001" → Should NOT match
4. Test input: "9021" → Should NOT match (only 4 digits)

Use online regex testers (regex101.com) to validate complex patterns.

---

## Zone Coverage Summary

Zones display **coverage summary** in admin list view showing what's included:

**Examples**:
- "All countries" → No country restrictions
- "US, CA, MX" → 3 countries
- "US (CA, OR, WA)" → US with 3 states
- "US (90xxx-91xxx)" → US with postal code patterns

**Use Summary To**:
- Quickly verify zone coverage without opening
- Spot overlaps or gaps in coverage
- Audit zone configuration at a glance

---

## Linking Zones to Shipping Methods

Zones and methods have **many-to-many relationship**:

**From Method Side** (Recommended):
1. Edit Shipping Method
2. Scroll to "Shipping Zones" section
3. Select applicable zones (multi-select)
4. Save method

**From Zone Side**:
- Zones don't directly link to methods
- Linking is always done from method configuration

**Method-Zone Behavior**:

**No zones linked** → Method available to ALL addresses

**Zones linked** → Method only available if customer address matches at least one linked zone

**Example**:
```
Method: "Domestic Standard"
Linked Zones: ["Domestic USA"]
→ Only shown to US addresses

Method: "International Express"
Linked Zones: ["EU", "Asia Pacific", "Rest of World"]
→ Shown to all non-US addresses
```

---

## Testing Zone Matching

Before going live, test zone configuration:

1. **Create Test Orders**
   - Use addresses in different zones
   - Verify correct zone matches

2. **Check Priority Resolution**
   - Use address that matches multiple zones
   - Verify highest priority zone wins
   - Confirm expected shipping methods appear

3. **Test Edge Cases**
   - Border postal codes (e.g., 90999 vs 91000)
   - State boundaries
   - International addresses with similar postal codes

4. **Use Zone Preview Tool** (if available)
   - Enter test address
   - See which zone(s) match
   - View priority resolution

---

## Troubleshooting

**Issue 1: No shipping methods available at checkout**

**Causes**:
- Customer address doesn't match any zone
- All methods linked to zones that don't match
- No methods exist without zone restrictions

**Solution**:
- Create fallback zone (all countries, priority 1)
- OR remove zone restrictions from at least one method
- Verify zone country/state/postal patterns

---

**Issue 2: Wrong zone matching**

**Causes**:
- Lower priority zone selected despite higher priority zone matching
- Postal code pattern syntax error (pattern fails silently)
- State code mismatch (CA vs California)

**Solution**:
- Verify priority values (higher number = higher priority)
- Test postal code patterns with regex validator
- Use 2-letter state codes (CA, not California)

---

**Issue 3: Unexpected method shown**

**Causes**:
- Method has no zones linked (available everywhere)
- Multiple zones match, unexpected zone has higher priority
- Zone coverage overlaps unintentionally

**Solution**:
- Review method's linked zones
- Check priority of matching zones
- Audit zone coverage summary for overlaps

---

## Tips

- **Start with 2 zones** - Domestic and International, expand as needed
- **Use priority wisely** - Specific zones 100, regional 50, fallback 1
- **Test postal patterns thoroughly** - Regex errors fail silently, causing zones to not match
- **Document zone logic** - Add notes to zone description explaining coverage intent
- **Avoid excessive zones** - Too many zones complicates configuration; use shipping promotions for complex scenarios
- **Use state codes, not names** - "CA" not "California", "NY" not "New York"
- **Create fallback zone** - All countries, priority 1, ensures at least one shipping option always available
- **Monitor zone performance** - If many customers see "no shipping available", audit zone coverage
- **Update zones for new regions** - Add countries to EU zone when new members join
- **Use descriptive names** - "EU (Excluding UK)" better than "Zone 3"
- **Test with real addresses** - Use customers' actual addresses during testing, not made-up ones
