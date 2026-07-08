---
slug: tax-configuration
title_i18n_key: Tax Configuration
category: store-config
component: cart
keywords:
  - tax configuration
  - sales tax
  - VAT
  - tax rates
  - tax rules
  - geographic tax
  - tax by state
  - tax by country
  - compound tax
  - tax exemptions
  - tax calculation
  - product tax
  - category tax
url_patterns:
  - /admin/cart/taxrate/
  - /admin/cart/taxrate/add/
  - /admin/cart/taxrate/\d+/change/
related:
  - shipping-methods
  - shipping-zones
published: true
---

Tax rates define sales tax, VAT, and other consumption taxes applied at checkout based on customer location and product type—configure country/state/city-level rates with optional product category exemptions. Spwig supports compound tax (tax-on-tax), priority-based rate selection, and tax preset groups for quick setup of regional tax systems (EU VAT, US Sales Tax). Rates can exempt specific product types (food, books, digital goods) or categories for compliance with local tax laws.

Use tax configuration to ensure legal compliance with tax collection requirements in your selling jurisdictions.

## Tax Rate Configuration

Each tax rate defines:

**Geographic Scope**:
- Country (required)
- State/Province (optional)
- City (optional)
- Postal Code Pattern (optional, regex)

**Rate Details**:
- **Tax Rate**: Percentage (e.g., 8.5%)
- **Name**: Display name (e.g., "California Sales Tax")
- **Priority**: Higher priority wins when multiple rates match
- **Active**: Toggle without deletion

**Exemptions**:
- **Exempt Product Types**: Digital goods, physical goods, services
- **Exempt Categories**: Specific product categories (Food, Books, Medical)

**Compound Tax**:
- **Is Compound**: Apply this rate on top of previous taxes (tax-on-tax)
- Example: Quebec PST compounds on GST

---

## Common Tax Scenarios

### US Sales Tax (State-Level)

```
Name: California Sales Tax
Country: US
State: CA
Rate: 7.25%
Priority: 50
```

### EU VAT (Country-Level)

```
Name: UK VAT
Country: GB
Rate: 20%
Priority: 50

Name: Germany VAT
Country: DE
Rate: 19%
Priority: 50
```

### Canadian GST/PST (Compound)

```
Rate 1: Federal GST
Country: CA
Rate: 5%
Priority: 100
Is Compound: No

Rate 2: Quebec PST
Country: CA
State: QC
Rate: 9.975%
Priority: 50
Is Compound: Yes  (applies to subtotal + GST)
```

### City-Level Tax

```
Name: Seattle Sales Tax
Country: US
State: WA
City: Seattle
Rate: 10.1%
Priority: 100
```

---

## Tax Exemptions

### Product Type Exemptions

Exempt entire product types:

- **Digital Goods**: Software, e-books, music
- **Physical Goods**: Tangible products
- **Services**: Consulting, installation

Example: EU VAT doesn't apply to digital goods for consumers (in some cases)

### Category Exemptions

Exempt specific product categories:

- Food & Groceries (often exempt or reduced rate)
- Books & Educational Materials
- Medical Supplies & Pharmaceuticals
- Clothing (some jurisdictions)

Configuration:
```
Name: California Sales Tax
Rate: 7.25%
Exempt Categories: ["Food & Beverages", "Prescription Medicine"]
```

---

## Tax Preset Groups

Quick-load common tax configurations:

**US Sales Tax Preset**:
- All 50 states + DC
- State-level rates
- Auto-updates when rates change

**EU VAT Preset**:
- All 27 EU member states
- Standard VAT rates
- Reverse charge logic for B2B

**To Use Presets**:
1. Settings > Cart > Tax Presets
2. Select preset group (e.g., "US Sales Tax 2026")
3. Click "Load Preset"
4. Rates imported automatically
5. Customize as needed

---

## Priority Resolution

When multiple rates match, highest priority wins:

Example:
```
Customer in Seattle, WA:

Rate A: US Federal (Priority 1) - 0%
Rate B: Washington State (Priority 50) - 6.5%
Rate C: Seattle City (Priority 100) - 3.6%

Result: Seattle rate (10.1% total) applies
```

---

## Tax Display Options

Configure in Settings > Cart > Tax Settings:

- **Prices Include Tax**: Display prices with tax included (EU style)
- **Display Tax Separately**: Show tax as line item (US style)
- **Round Tax**: Per-item or per-order
- **Tax Title**: Customize label ("VAT", "Sales Tax", "GST")

---

## Testing Tax Configuration

Before going live:

1. Create test orders from different jurisdictions
2. Verify correct tax rate applied
3. Check exemptions work for excluded categories
4. Test compound tax calculation
5. Review tax line items on invoices

---

## Compliance Notes

- **US**: Nexus rules require tax collection in states where you have physical presence or economic nexus
- **EU**: VAT registered businesses must collect VAT from EU customers
- **Canada**: GST/HST/PST varies by province
- **Consult tax professional**: Tax laws change frequently, verify current requirements

---

## Tips

- **Use tax presets** - Faster than manual entry, auto-updated
- **Monitor nexus thresholds** - Track sales by state for US economic nexus
- **Set priority correctly** - City > State > Country
- **Test compound tax** - Verify calculations match expected amounts
- **Update annually** - Tax rates change, review every January
- **Document exemptions** - Keep records of why categories are exempt
- **Use descriptive names** - "California Sales Tax 2026" better than "Tax 1"
- **Enable tax by default** - Safer than forgetting to apply tax
