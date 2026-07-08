---
slug: carrier-presets
title_i18n_key: Carrier Presets
category: orders-shipping
component: shipping
keywords:
  - carrier presets
  - manual carriers
  - DHL
  - FedEx
  - UPS
  - USPS
  - carrier logos
  - tracking URLs
  - carrier management
  - shipping carriers
url_patterns:
  - /admin/shipping/carrierpreset/
  - /admin/shipping/carrierpreset/add/
  - /admin/shipping/carrierpreset/\d+/change/
related:
  - shipping-provider-accounts
  - tracking-events
published: true
---

Carrier presets define manual carriers (DHL, FedEx, UPS, custom carriers) for shipments created without API integration—each preset provides carrier logo, tracking URL template, and display settings. System presets (DHL, FedEx, UPS, USPS) are pre-configured and cannot be deleted, while custom presets allow merchants to add regional or specialized carriers. Presets link to manual shipments where merchants enter tracking numbers manually instead of purchasing labels through provider APIs.

Use carrier presets when creating manual shipments or when you want tracking links without full API integration.

## System Presets vs Custom Presets

**System Presets** (Pre-installed):
- DHL, FedEx, UPS, USPS, Royal Mail, Canada Post, Australia Post
- Cannot be deleted (is_system=True)
- Can override tracking URL or logo
- Default tracking URL templates provided

**Custom Presets** (Merchant-created):
- Regional carriers (OnTrac, LaserShip, regional postal)
- Specialized carriers (freight, white-glove delivery)
- Can be edited or deleted
- Requires manual tracking URL template

---

## Carrier Preset Configuration

Each preset defines:

**Basic Settings**:
- **Name**: Carrier display name (e.g., "DHL Express", "Local Courier")
- **Code**: Internal identifier (e.g., "dhl", "local_courier")
- **Logo**: Carrier logo image (optional, uses icon if not provided)
- **Icon**: FontAwesome icon as fallback (e.g., "fa-truck")
- **Active**: Toggle visibility

**Tracking Configuration**:
- **Tracking URL Template**: URL pattern with {tracking_id} placeholder
- **Tracking URL Override**: Custom URL (overrides default template)

**System Settings** (system presets only):
- **Is System**: Cannot be deleted
- **Is Default**: One default per carrier type

---

## Tracking URL Templates

Tracking URLs use `{tracking_id}` placeholder:

**Examples**:

DHL: `https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}`

FedEx: `https://www.fedex.com/fedextrack/?tracknumbers={tracking_id}`

UPS: `https://www.ups.com/track?tracknum={tracking_id}`

USPS: `https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}`

Custom: `https://track.localcourier.com/tracking/{tracking_id}`

**How It Works**:
1. Merchant creates shipment with tracking number "1234567890"
2. System replaces {tracking_id} with actual number
3. Customer clicks tracking link → redirects to carrier site
4. Result: `https://www.dhl.com/en/express/tracking.html?AWB=1234567890`

---

## Creating Custom Carrier Preset

**Step-by-Step**:

1. Navigate to Settings > Shipping > Carrier Presets
2. Click "Add Carrier Preset"
3. Enter name (e.g., "OnTrac")
4. Enter code (slug: "ontrac")
5. Optional: Upload logo image
6. Select icon (fa-truck, fa-shipping-fast, etc.)
7. Enter tracking URL template with {tracking_id}
8. Toggle active = Yes
9. Save

**Example - OnTrac**:
```
Name: OnTrac
Code: ontrac
Tracking URL: https://www.ontrac.com/tracking.asp?tracking_number={tracking_id}
Icon: fa-truck
Active: Yes
```

---

## Overriding System Preset Tracking URLs

System presets can have tracking URL overrides:

**Use Case**: Your carrier account has special tracking portal

**How To Override**:
1. Edit system preset (e.g., DHL)
2. Enter override URL in "Tracking URL Override" field
3. Override takes precedence over default template
4. Save

**Example**:
```
System: DHL
Default URL: https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}
Override URL: https://track.dhl.com/special-account/{tracking_id}
Result: Override URL used for all DHL shipments
```

---

## Carrier Logos

**Logo Guidelines**:
- Format: PNG or SVG (SVG preferred for scalability)
- Size: 200×60px recommended
- Background: Transparent or white
- Color: Full-color carrier branding

**Fallback Icon**:
If no logo uploaded, system displays FontAwesome icon:
- fa-truck (default)
- fa-shipping-fast (express)
- fa-plane (air freight)
- fa-box (parcel)

---

## Using Carrier Presets in Shipments

When creating manual shipment:

1. Orders > Order Detail > Create Shipment
2. Select "Manual Shipment" mode
3. Choose carrier from preset dropdown
4. Enter tracking number
5. Optional: Override tracking URL for this shipment
6. Save

**Shipment Display**:
- Carrier logo shown (or icon)
- Tracking number displayed
- Clickable tracking link (uses preset URL template)

---

## Default Carrier

One preset can be set as default per system:

**Use Case**: Most commonly used carrier auto-selected in shipment creation

**How To Set**:
1. Edit carrier preset
2. Check "Is Default"
3. Save
4. Previous default (if any) automatically unset

**Only one default allowed** - setting new default removes previous default flag.

---

## Tips

- **Use descriptive names** - "DHL Express" better than "DHL"
- **Test tracking URLs** - Verify template works with real tracking numbers
- **Upload carrier logos** - Professional appearance in customer emails
- **Don't delete system presets** - They're pre-configured correctly
- **Use override sparingly** - Only when carrier changes tracking system
- **Set default for main carrier** - Saves time during shipment creation
- **Keep presets active** - Only deactivate if carrier discontinued
- **Document custom carriers** - Add notes about regional carriers
