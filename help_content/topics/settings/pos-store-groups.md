---
slug: pos-store-groups
title_i18n_key: POS Store Groups
category: point-of-sale
component: pos_app
keywords:
  - store groups
  - multi-location
  - franchise management
  - regional settings
  - settings inheritance
  - settings cascade
  - group configuration
  - currency override
  - language override
  - timezone override
  - multi-store
  - chain management
  - group hierarchy
  - location grouping
url_patterns:
  - /admin/pos_app/storegroup/
related:
  - pos-system-overview
  - managing-pos-terminals
  - receipt-template-customization
  - customer-display-promo-slides
published: true
---

Store groups organize multiple retail locations with shared configurations. Instead of configuring every terminal individually, group terminals by region, franchise, or location type and apply settings at the group level. Groups support settings inheritance—currency, language, timezone, receipt templates, and promotional content cascade from group to individual stores. This simplifies management for multi-location merchants while preserving flexibility for store-specific overrides when needed.

Use store groups when you operate multiple retail locations, franchises, or regional markets with different operational requirements.

![Store Group List](/static/core/admin/img/help/pos-store-groups/storegroup-list.webp)

## What Are Store Groups?

Store groups are organizational containers for warehouses and terminals that share common characteristics:

**Common Grouping Strategies**:
- **Geographic**: North Region, South Region, West Coast, East Coast
- **Franchise**: Franchisee A Stores, Franchisee B Stores, Corporate Stores
- **Format**: Mall Locations, Standalone Stores, Pop-Up Shops
- **Market**: Domestic Stores, European Stores, Asian Pacific Stores

Groups don't change the physical operation of terminals—they provide a configuration layer that simplifies management at scale.

## When to Use Store Groups

**Single Location** - Don't need groups. Configure terminals directly.

**2-3 Locations with Identical Settings** - Groups optional. May be easier to configure terminals directly.

**4+ Locations** - Groups strongly recommended. Centralized configuration saves time.

**Multi-Country Operations** - Groups essential. Different currencies, languages, and timezones require group-level overrides.

**Franchise Operations** - Groups critical. Each franchisee needs independent settings while maintaining brand consistency.

## Settings Inheritance Hierarchy

Spwig POS uses a 4-level settings cascade (highest priority to lowest):

| Level | Priority | Example | Use Case |
|-------|----------|---------|----------|
| **Terminal** | 1 (Highest) | Terminal 5 overrides paper width to 58mm | Single terminal has unique printer hardware |
| **Store** | 2 | Store 2 overrides currency to GBP | UK location among mostly US stores |
| **Group** | 3 | European Group sets timezone to CET | Regional consistency across multiple stores |
| **Site** | 4 (Lowest) | Global default: USD, English, UTC | Fallback for all unconfigured settings |

**How It Works**:
- System checks Terminal settings first
- If not set, checks Store settings
- If not set, checks Group settings
- If not set, uses Site defaults

**Example**:
- Site default: Currency = USD, Language = English
- Group "European Stores": Currency = EUR, Language = not set
- Store "Paris Flagship": Currency = not set, Language = French
- Terminal "Paris Register 1": Currency = not set, Language = not set

**Result for Paris Register 1**:
- Currency: EUR (inherited from Group)
- Language: French (inherited from Store)

This cascade allows broad defaults with surgical overrides where needed.

## Creating a Store Group

Navigate to **POS > Store Groups** and click **+ Add Store Group**:

![Store Group Add Form](/static/core/admin/img/help/pos-store-groups/storegroup-add-form.webp)

### Basic Configuration

**Group Name** - Descriptive label (e.g., "West Coast Stores", "European Franchises", "Mall Locations")

**Code** - Short unique identifier (e.g., "WEST", "EUR", "MALL"):
- Used internally for references
- Must be unique across all groups
- 2-10 characters, alphanumeric
- Uppercase recommended for consistency

**Sort Order** - Controls display order in admin lists (lower numbers appear first):
- Use multiples of 10: 10, 20, 30 (allows inserting new groups between existing)
- Helps organize groups logically (geographic order, size order, etc.)

### Regional Overrides

**Currency Override** - Set group-level currency different from site default:
- Example: European group uses EUR, Asian Pacific group uses JPY
- Terminals in this group default to this currency
- Affects price display, cash reconciliation, reports

**Language Override** - Set group-level language different from site default:
- Example: French stores use French, German stores use German
- Affects POS interface language, receipt language (if template supports it)
- Staff see POS UI in this language when logging into group terminals

**Timezone Override** - Set group-level timezone different from site default:
- Example: West Coast stores use America/Los_Angeles, European stores use Europe/Paris
- Affects shift timestamps, report scheduling, promotional slide scheduling
- Ensures shift reports align with local business hours

**When to Override**:
- **Currency**: Always override for international locations (different payment currencies)
- **Language**: Override for non-English speaking markets (customer-facing content)
- **Timezone**: Override for locations >2 hours from site default (accurate local timestamps)

## Associating Warehouses with Groups

After creating a group, assign warehouses to it:

1. Navigate to **Catalog > Warehouses**
2. Edit warehouse representing a store location
3. Set **Store Group** field to your created group
4. Save

All terminals assigned to this warehouse now inherit the group's settings.

**Example Setup**:
- Create group: "European Stores" (Currency: EUR, Language: not set, Timezone: CET)
- Create warehouses: "Paris Store", "Berlin Store", "Rome Store"
- Assign all 3 warehouses to "European Stores" group
- Create terminals: "Paris Register 1", "Berlin Register 1", "Rome Register 1"
- Each terminal inherits EUR currency and CET timezone from group
- Override language at store level: Paris=French, Berlin=German, Rome=Italian

## Settings Controlled by Groups

Groups can override these settings:

**Operational Settings**:
- Currency (affects price display and cash reconciliation)
- Language (affects POS UI language)
- Timezone (affects timestamps and scheduling)

**Content Settings** (via scoped models):
- Receipt templates (create group-specific receipt designs)
- Promotional slides (target promos to specific groups)

**Not Controlled by Groups**:
- Terminal hardware config (configured per-terminal)
- Staff assignments (configured per-terminal)
- Warehouse stock levels (configured per-warehouse)
- Payment provider accounts (configured site-wide or per-provider)

## Real-World Examples

### Example 1: International Fashion Retailer

**Setup**:
- 50 stores across 5 countries
- Each country has different currency, language, tax requirements

**Group Structure**:
- Group: "US Stores" (USD, English, America/New_York)
  - 20 warehouses (NY, LA, Chicago, etc.)
  - 60 terminals
- Group: "UK Stores" (GBP, English, Europe/London)
  - 10 warehouses (London, Manchester, etc.)
  - 30 terminals
- Group: "EU Stores" (EUR, not set, Europe/Paris)
  - 15 warehouses (Paris, Berlin, Rome, etc.)
  - 45 terminals
  - Language overridden at store level (Paris=French, Berlin=German, Rome=Italian)
- Group: "Japan Stores" (JPY, Japanese, Asia/Tokyo)
  - 5 warehouses (Tokyo, Osaka, etc.)
  - 15 terminals

**Benefits**:
- One group configuration applies to all stores in each market
- Receipt templates scoped to groups (VAT format for EU, sales tax for US)
- Promotional slides targeted by region (US: Memorial Day Sale, EU: Summer Holiday Sale)

### Example 2: Coffee Shop Chain

**Setup**:
- 30 locations, all same country, but different formats

**Group Structure**:
- Group: "Mall Locations" (not set, not set, not set)
  - 10 mall-based stores
  - Extended hours promotional slides (open until 9pm)
  - Receipt template with mall parking validation QR code
- Group: "Standalone Stores" (not set, not set, not set)
  - 15 street-front stores
  - Standard hours promotional slides
  - Standard receipt template
- Group: "Airport Locations" (not set, not set, not set)
  - 5 airport stores
  - 24-hour promotional slides
  - Receipt template with flight info QR code integration

**Benefits**:
- Different promotional content for different formats
- Location-specific receipt customizations
- Simplified management (update one group instead of updating 10 individual stores)

### Example 3: Franchise Operation

**Setup**:
- 100 stores, 20 different franchisees

**Group Structure**:
- Group: "Franchisee A" (not set, not set, not set)
  - 10 stores operated by Franchisee A
  - Franchisee A's contact info on receipts (via group receipt template)
  - Franchisee A's promotional content (local events, specials)
- Group: "Franchisee B" (not set, not set, not set)
  - 8 stores operated by Franchisee B
  - Franchisee B's contact info on receipts
  - Franchisee B's promotional content
- (Repeat for all franchisees)
- Group: "Corporate Stores" (not set, not set, not set)
  - 5 corporate-owned stores
  - Corporate branding and promotions

**Benefits**:
- Each franchisee manages their own group settings
- Brand consistency maintained via site defaults
- Franchisee independence via group overrides

## Managing Group Settings

**Changing Group Settings** affects all terminals in that group:
- Currency change: All group terminals switch to new currency on next sync
- Language change: All group terminals switch to new language on next sync
- Timezone change: All group terminals recalculate timestamps on next sync

**Impact Considerations**:
- Test changes on a single terminal before applying to entire group
- Notify staff of upcoming changes (e.g., language switching)
- Schedule changes during off-peak hours to minimize disruption

**Removing a Group**:
- Reassign all warehouses to a different group or remove group assignment
- Terminals lose group-level settings and fall back to site defaults
- Cannot delete group while warehouses are still assigned

## Tips

- **Use meaningful codes** - "WEST" is clearer than "GRP1" when reviewing configurations
- **Plan hierarchy before creating groups** - Think through your organizational structure first; restructuring later is tedious
- **Test group settings with one terminal** - Before assigning 50 warehouses to a group, test the group's settings with one terminal
- **Override sparingly at store level** - Too many store-level overrides defeats the purpose of groups
- **Document group purposes** - Note in group name what makes this group distinct (geography, format, franchisee)
- **Use sort order strategically** - Order groups by importance (Corporate Stores first) or geography (West to East) for easier navigation
- **Keep group count reasonable** - 20+ groups suggests over-segmentation; consider consolidating
- **Currency overrides are permanent** - Switching a group's currency mid-operation complicates accounting; plan carefully
