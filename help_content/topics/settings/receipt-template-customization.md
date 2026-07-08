---
slug: receipt-template-customization
title_i18n_key: Receipt Template Customization
category: point-of-sale
component: pos_app
keywords:
  - receipt templates
  - receipt customization
  - thermal printer
  - receipt design
  - receipt logo
  - paper width
  - 58mm receipt
  - 80mm receipt
  - receipt header
  - receipt footer
  - tax id receipt
  - business registration
  - qr code receipt
  - receipt compliance
  - receipt branding
url_patterns:
  - /admin/pos_app/receipttemplate/
related:
  - pos-system-overview
  - managing-pos-terminals
  - pos-store-groups
published: true
---

Receipt templates control the appearance and content of printed thermal receipts at your POS terminals. Customize header and footer text, add your logo, configure compliance fields (tax IDs, business registration numbers), and include promotional QR codes. Templates support scope targeting—create a default template for all stores, group-specific templates for regions, or store-specific templates for individual locations. The system uses scope precedence rules to determine which template applies when printing a receipt.

Use receipt templates to maintain brand consistency, meet regional compliance requirements, and enhance customer engagement through promotional elements.

![Receipt Template List](/static/core/admin/img/help/receipt-template-customization/receipt-list.webp)

## Receipt Template Basics

Receipt templates define the structure and content of printed receipts from ESC/POS thermal printers. Each template specifies:

**Physical Configuration**:
- Paper width (58mm or 80mm)
- Logo image (monochrome for thermal printing)
- Font sizing and spacing

**Content Sections**:
- Header text (store name, address, contact info)
- Dynamic transaction data (items, prices, totals, payment methods)
- Footer text (return policy, thank you message, social media)
- Compliance fields (tax IDs, business registration numbers)
- Promotional QR code with label

**Scope Targeting**:
- Default template (applies to all stores unless overridden)
- Group template (applies to all stores in a group)
- Store template (applies to a specific store/warehouse)

## Scope Precedence Rules

When a terminal prints a receipt, the system selects a template using this hierarchy (highest priority to lowest):

| Priority | Scope | Example | Use Case |
|----------|-------|---------|----------|
| **1** | Store-specific | Paris Store template | Unique French tax compliance requirements |
| **2** | Group-specific | European Stores template | VAT display for all EU locations |
| **3** | Default | Global template | Fallback for all unconfigured stores |

**How It Works**:
1. Check if store has a dedicated template (warehouse-specific)
2. If not, check if store's group has a group template
3. If not, use the default template

**Example**:
- Default template: "Standard Receipt" (no scope assignment)
- Group template: "EU Receipt" (assigned to European Stores group) - includes VAT registration
- Store template: "Paris Receipt" (assigned to Paris warehouse) - includes French SIRET number

**Result**:
- Paris Store terminal: Uses "Paris Receipt" (most specific)
- Berlin Store terminal (in European Stores group, no store template): Uses "EU Receipt" (group level)
- New York Store terminal (no group, no store template): Uses "Standard Receipt" (default fallback)

## Paper Width Configuration

Thermal receipt printers use either 58mm or 80mm paper width. Choose based on your printer hardware:

| Paper Width | Characters Per Line | Best For | Typical Use |
|-------------|---------------------|----------|-------------|
| **58mm** | ~32 characters | Small footprint, portable | Food trucks, mobile POS, kiosks |
| **80mm** | ~48 characters | Standard retail | Most retail stores, restaurants |

**Cannot mix widths**: All terminals using the same template must have the same paper width printer. If you have mixed printer types, create separate templates for each width.

**Logo Size Limits**:
- **58mm**: Max width 384 pixels (recommended: 350px)
- **80mm**: Max width 576 pixels (recommended: 550px)

Logos exceeding max width are automatically scaled down, which may reduce quality.

## Logo Configuration

Receipt logos must be **monochrome** (black and white only) for thermal printer compatibility:

**Logo Requirements**:
- File format: PNG, JPG, or WebP
- Color mode: Monochrome (black pixels on white background)
- Recommended dimensions:
  - 58mm paper: 350px width × 100-150px height
  - 80mm paper: 550px width × 150-200px height
- File size: <100KB (thermal printers have limited memory)

**Creating Monochrome Logos**:
1. Start with your regular logo (color or grayscale)
2. Use image editor to convert to pure black and white (no grays)
3. Increase contrast to ensure black elements are solid
4. Export as PNG with transparent or white background

**Logo Positioning**:
- Always centered horizontally
- Prints at top of receipt (above header text)
- Followed by automatic spacing (prevents crowding with content)

**Selecting Logo**:
- Click **Browse Media Library** in template form
- Select monochrome logo asset
- Preview shows how logo will appear on receipt

**No Logo**: Leave logo field blank if you prefer text-only branding (header text can include store name).

## Header Text

Header text appears immediately after the logo (or at top if no logo). Typical content:

**Store Name and Address**:
```
Your Store Name
123 Main Street
City, State 12345
Phone: (555) 123-4567
```

**Business Hours**:
```
Monday-Friday: 9am-9pm
Saturday-Sunday: 10am-6pm
```

**Tagline or Slogan**:
```
Quality Products, Exceptional Service
```

**Formatting**:
- Use line breaks to separate information
- Center-aligned automatically
- Keep lines under character limit for paper width (32 chars for 58mm, 48 for 80mm)

**Variables Available** (optional):
- `{store_name}` - Replaced with warehouse name
- `{order_date}` - Replaced with transaction date
- `{order_number}` - Replaced with order ID

Most merchants use static text instead of variables for header consistency.

## Footer Text

Footer text appears after transaction details (items, totals, payment). Typical content:

**Return Policy**:
```
Returns within 30 days with receipt
Store credit or exchange only
```

**Thank You Message**:
```
Thank you for shopping with us!
Follow us @yourstore
```

**Customer Service**:
```
Questions? Call (555) 123-4567
or email support@yourstore.com
```

**Formatting Tips**:
- Keep most important info first (return policy, contact)
- Use line breaks for readability
- Consider adding separator line (`---`) between sections

## Compliance Fields

Many jurisdictions require specific information on receipts:

**Tax ID Label** - Customizable label for tax identification number:
- US: "Tax ID" or "EIN"
- EU: "VAT Number" or "VAT Reg No"
- Canada: "GST/HST Number"
- Australia: "ABN"

**Tax ID Value** - The actual identification number:
- Entered once in template, appears on all receipts
- Example: "VAT Number: GB123456789"

**Business Registration Label** - Customizable label for business registration:
- France: "SIRET"
- Germany: "Handelsregister"
- UK: "Company Registration Number"

**Business Registration Value** - The actual registration number:
- Example: "SIRET: 123 456 789 00010"

**Show Powered By Spwig** - Toggle to display or hide "Powered by Spwig" branding:
- Enabled by default (supports platform development)
- Disable for white-label operations

**Compliance Examples by Region**:

**European Union**:
- Tax ID Label: "VAT Number"
- Tax ID Value: "GB123456789"
- Display company registration number if required by country

**United States**:
- Generally no receipt tax ID requirement (varies by state)
- May include EIN for B2B transactions

**France (Specific)**:
- Mandatory SIRET on all receipts
- Business Registration Label: "SIRET"
- Business Registration Value: "123 456 789 00010"

**Australia**:
- ABN (Australian Business Number) recommended for GST-registered businesses
- Tax ID Label: "ABN"

Check your local jurisdiction's receipt requirements before going live.

## QR Code Promotions

Include a QR code at the bottom of receipts to drive customer engagement:

**QR Code URL** - The destination when scanned:
- Review request: `https://yourstore.com/reviews/leave-review`
- Loyalty program: `https://yourstore.com/loyalty/join`
- Next purchase discount: `https://yourstore.com/discount/THANKYOU`
- Social media: `https://instagram.com/yourstore`
- Website homepage: `https://yourstore.com`

**QR Code Label** - Text displayed above QR code:
- "Scan to leave a review and get 10% off your next purchase"
- "Join our loyalty program - Scan here"
- "Follow us on Instagram - Scan to connect"
- "Rate your experience"

**QR Code Best Practices**:
- Use short URLs (long URLs create dense, hard-to-scan codes)
- Test QR code with multiple phone cameras before deployment
- Include clear value proposition in label (what customer gets for scanning)
- Track QR code scans to measure effectiveness (use URL with tracking parameter)

**Dynamic QR Codes** (Advanced):
- Use QR redirect service (bit.ly, tinyurl) to create short URL
- Point redirect to different destinations seasonally without reprinting receipts
- Example: `https://bit.ly/yourstoreqr` → redirects to current promotion

## Creating Templates for Different Scopes

**Default Template** (recommended starting point):
1. Navigate to **POS > Receipt Templates**
2. Click **+ Add Receipt Template**
3. Leave **Warehouse** and **Store Group** fields blank (this makes it the default)
4. Configure paper width matching your most common printer type
5. Add logo, header, footer
6. Configure compliance fields for your primary market
7. Save

This template applies to all stores unless overridden.

**Group Template** (for regional variations):
1. Create new template
2. Select **Store Group** (e.g., "European Stores")
3. Leave **Warehouse** blank
4. Adjust compliance fields for the region (e.g., VAT formatting)
5. Adjust header text (e.g., regional address)
6. Save

This template applies to all stores in the group.

**Store Template** (for location-specific needs):
1. Create new template
2. Select **Warehouse** (e.g., "Paris Store")
3. Adjust all fields for this specific location
4. Save

This template applies only to this one store.

**Testing Templates**:
- Process test transaction on terminal
- Print receipt
- Verify logo clarity, text alignment, compliance fields, QR code scannability
- Adjust template and retest if needed

## Common Receipt Layouts

**Minimal Receipt** (food trucks, pop-ups):
- No logo (space savings)
- Header: Store name and phone only
- Footer: Thank you message
- No QR code

**Standard Retail Receipt**:
- Logo (monochrome brand mark)
- Header: Full store name, address, hours
- Compliance: Tax ID
- Footer: Return policy, thank you message
- QR code: Review request

**Premium Retail Receipt**:
- Logo (full brand wordmark)
- Header: Tagline, address, contact
- Compliance: Tax ID, business registration
- Footer: Return policy, customer service, social media
- QR code: Loyalty program enrollment

**Multi-Location Chain**:
- Default template: Corporate branding, standard policies
- Group templates: Regional compliance (VAT for EU, GST for Canada)
- Store templates: Location-specific address and phone

## Managing Multiple Templates

**Template Naming Convention**:
- Use scope in name: "Default Receipt", "EU Group Receipt", "Paris Store Receipt"
- Helps identify which template applies where when reviewing list

**Template Changes**:
- Changes apply immediately to future receipts
- Past receipts (already printed) are not affected
- Test changes on low-traffic terminal before deploying to all stores

**Template Duplication**:
- When creating a new template similar to existing one, duplicate the existing template and modify
- Prevents starting from scratch

**Deleting Templates**:
- Cannot delete default template while terminals exist (must have one fallback)
- Can delete group/store templates (terminals fall back to next level in hierarchy)
- Confirm no terminals are actively using template before deleting

## Tips

- **Start with 80mm if unsure** - Standard paper width works for most retail; 58mm is specialized
- **Test logo in actual printer** - What looks good on screen may print poorly; test early
- **Keep compliance fields updated** - Expired tax registrations on receipts create legal issues
- **QR codes with value prop scan better** - "Scan for 10% off" outperforms "Scan here" by 10x
- **Review character limits** - Text wrapping ruins formatting; count characters per line before deploying
- **One template per paper width** - Don't assign 80mm template to terminal with 58mm printer (logo won't fit)
- **Print test receipts monthly** - Printers degrade over time; verify quality remains acceptable
- **Use variables sparingly** - Static text is more reliable than dynamic variables (fewer failure points)
- **Backup template config** - Screenshot or export template settings before major changes (easy rollback)
- **Regional compliance varies** - Research local receipt requirements before deployment; fines for non-compliance can be severe
