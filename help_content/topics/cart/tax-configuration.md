---
slug: tax-configuration
title_i18n_key: Tax Configuration
category: store-config
component: cart
keywords:
  - tax
  - tax rate
  - tax rule
  - VAT
  - sales tax
  - GST
  - tax preset
  - tax zone
  - tax exemption
  - compound tax
  - tax calculation
  - shipping tax
  - tax configuration
url_patterns:
  - /admin/cart/taxrate/
related:
  - store-settings
  - setup-shipping
published: true
---

Configure tax rules for your store so that the correct taxes are automatically applied to orders based on the customer's location. You can load regional presets with one click or create custom rules for any country, state, city, or postal code.

![Tax Dashboard](/static/core/admin/img/help/tax-configuration/tax-dashboard.webp)

## Tax Dashboard

Navigate to **Orders > Shipments > Tax Rates** to open the tax dashboard. The page shows:

- **Statistics panel** — four cards displaying Total Rules, Active Rules, Countries Covered, and Tax Types in use
- **Filters** — search by name, country, or state, and filter by country, tax type (Sales Tax, VAT, GST, Custom), or status (Active/Inactive)
- **Tax rule cards** — each card shows the country flag, rule name, location, rate percentage, tax type badge, status badge, priority, and exemption count

## Loading Tax Presets

Click **Load Presets** to open the presets modal. Presets are collections of standard tax rates for a region, ready to load into your store with one click.

![Load Presets](/static/core/admin/img/help/tax-configuration/tax-presets-modal.webp)

Presets are organized by world region:

| Region | Preset Groups |
|--------|--------------|
| **Africa** | Africa VAT (25 rates) |
| **Asia Pacific** | Asia-Pacific VAT/GST (24 rates), Central Asia VAT (6 rates) |
| **Europe** | EU VAT Rates, UK VAT, Other European VAT |
| **Latin America** | Latin America VAT |
| **Middle East** | Middle East VAT |
| **North America** | US State Sales Tax, Canadian GST/HST |
| **Oceania** | Oceania GST/VAT |

### How Presets Work

1. Click **Load** on the preset group you want
2. The system creates tax rules for every country or state in that group
3. Existing rules with the same country, state, and tax type are automatically skipped to prevent duplicates
4. After loading, each rule is fully editable — adjust rates, add exemptions, or deactivate rules you do not need

You can load multiple preset groups. For example, load both EU VAT and UK VAT if you sell to customers across Europe.

## Creating Tax Rules Manually

Click **Add Tax Rate** to create a custom rule. The form has four sections:

![Tax Rate Form](/static/core/admin/img/help/tax-configuration/tax-rate-form.webp)

### Basic Information

| Field | Description |
|-------|-------------|
| **Name** | Display name for the rule (e.g., "California Sales Tax") |
| **Is Active** | Toggle to enable or disable the rule |
| **Tax Type** | Sales Tax, VAT, GST, or Custom Tax |
| **Rate (%)** | The tax rate as a percentage (e.g., enter 8.25 for 8.25%) |
| **Priority** | Higher numbers take precedence when multiple rules match the same location |

### Geographic Scope

| Field | Description |
|-------|-------------|
| **Country** | ISO 3166-1 alpha-2 code (e.g., US, GB, DE) |
| **State** | State or province (leave blank to apply to the entire country) |
| **City** | City name (optional, for city-level tax rules) |
| **Postal Codes** | List of specific postal codes (optional, for postal-code-level rules) |

Rules are matched from most specific to least specific. A rule for a specific postal code takes priority over a rule for the same state, which takes priority over a country-wide rule.

### Application Rules

| Field | Description |
|-------|-------------|
| **Applies to Shipping** | When checked, this tax also applies to shipping costs |
| **Compound Tax** | When checked, this tax is calculated on top of other taxes (the base amount plus previously applied taxes) |

### Product Exemptions

| Field | Description |
|-------|-------------|
| **Exempt Product Types** | Product types that are exempt from this tax (e.g., digital, service) |
| **Exempt Categories** | Specific product categories that are exempt from this tax |

## Tax Types

| Type | Used For | Examples |
|------|----------|---------|
| **Sales Tax** | US, Canada | State and provincial sales taxes |
| **VAT** | Europe, UK, much of Asia and Africa | Value Added Tax |
| **GST** | Australia, New Zealand, India, Singapore | Goods and Services Tax |
| **Custom Tax** | Special cases | Local surcharges, environmental taxes, luxury taxes |

## How Tax Calculation Works

When a customer reaches checkout, the system automatically calculates taxes based on their shipping address:

1. **Geographic matching** — finds all active rules that match the customer's country, then narrows by state, city, and postal code
2. **Specificity scoring** — more specific rules (postal code > city > state > country) are ranked higher
3. **Priority ordering** — within the same specificity level, higher-priority rules take precedence
4. **Product exemptions** — exempt products are excluded from each applicable rule
5. **Non-compound taxes** — calculated first on the base price of each item
6. **Compound taxes** — calculated on the base price plus all non-compound taxes already applied
7. **Shipping tax** — if a rule has "Applies to Shipping" enabled, the shipping cost is included in the taxable amount

The tax breakdown is stored with the order so you can see exactly which rules applied and how much each one contributed.

## Common Setups

### EU Store

1. Click **Load Presets** and load the **EU VAT Rates** group
2. This creates VAT rules for all EU member states with their current standard rates
3. Optionally load **UK VAT** if you also sell to the UK

### US Store

1. Click **Load Presets** and load the **US State Sales Tax** group
2. This creates sales tax rules for all US states that collect sales tax
3. For city-level taxes, manually add rules with the city field filled in and a higher priority

### Multi-Region Store

1. Load multiple preset groups for each market you sell to
2. The system applies the correct tax based on where each customer is located
3. Adjust individual rules as needed for your specific business requirements

## Tips

- **Start with presets** — load the preset groups for your target markets, then customize individual rates rather than creating every rule from scratch.
- **Use priority wisely** — set higher priority values for more specific local rules so they correctly override broader regional rules.
- **Check compound tax carefully** — compound tax is rare. Most jurisdictions use simple (non-compound) tax. Only enable compound tax when your local regulations specifically require tax-on-tax calculation.
- **Keep rules active/inactive** — rather than deleting tax rules for seasonal or temporary changes, toggle them inactive and reactivate when needed.
- **Test before going live** — after setting up your tax rules, place a test order from different addresses to verify the correct taxes are being applied.
