# MJML Component Library

This directory contains reusable MJML components for email templates.

## Components

### 1. `order_items_table.mjml`
Displays order items with thumbnails, quantities, and prices in a responsive table.

**Usage:**
```mjml
{% include 'email_system/mjml_components/order_items_table.mjml' with items=items %}
```

**Required Variables:**
- `items`: List of dicts with keys: `name`, `sku`, `quantity`, `price`, `subtotal`, `product_thumbnail_url`

---

### 2. `address_block.mjml`
Displays formatted shipping or billing address.

**Usage:**
```mjml
{% include 'email_system/mjml_components/address_block.mjml' with address=shipping_address title="Shipping Address" %}
```

**Required Variables:**
- `address`: Dict with keys: `name`, `street`, `city`, `state`, `postal_code`, `country`
- `title`: String (e.g., "Shipping Address", "Billing Address")

---

### 3. `order_timeline.mjml`
Displays visual 4-stage order progress indicator.

**Usage:**
```mjml
{% include 'email_system/mjml_components/order_timeline.mjml' with stages=timeline_stages %}
```

**Required Variables:**
- `stages`: List of 4 dicts with keys: `label`, `active` (bool), `completed` (bool)

---

### 4. `payment_summary.mjml`
Displays order totals breakdown (subtotal, shipping, tax, total).

**Usage:**
```mjml
{% include 'email_system/mjml_components/payment_summary.mjml' with subtotal=subtotal shipping=shipping tax=tax total=total %}
```

**Required Variables:**
- `subtotal`: String (e.g., "$139.97")
- `shipping`: String (e.g., "$10.00")
- `tax`: String (e.g., "$6.53")
- `total`: String (e.g., "$156.50")

---

### 5. `support_block.mjml`
Displays support contact information with icons.

**Usage:**
```mjml
{% include 'email_system/mjml_components/support_block.mjml' %}
```

**Required Variables:** (from context)
- `support_email`: String
- `support_phone`: String

---

### 6. `cta_button.mjml`
Displays prominent call-to-action button.

**Usage:**
```mjml
{% include 'email_system/mjml_components/cta_button.mjml' with url=order_url text="View Order" %}
```

**Required Variables:**
- `url`: String (button link)
- `text`: String (button label)

---

## Theme Tokens

All components use the nested `theme` context object for styling, which automatically
adapts to the merchant's active theme and Brand Builder customizations.

### Available Theme Tokens

**Colors** (`theme.color.*`):
- `theme.color.primary` - Primary brand color (buttons, links)
- `theme.color.primary_hover` - Hover state for primary
- `theme.color.secondary` - Secondary accent color
- `theme.color.text` - Primary text color
- `theme.color.text_muted` - Secondary/muted text color
- `theme.color.text_inverse` - Text on dark backgrounds (usually white)
- `theme.color.background` - Main background color
- `theme.color.background_secondary` - Alternative background (light sections)
- `theme.color.surface` - Card/panel background (usually white)
- `theme.color.border` - Border/divider color
- `theme.color.success` - Success status color (green)
- `theme.color.warning` - Warning status color (yellow/orange)
- `theme.color.error` - Error status color (red)
- `theme.color.info` - Info status color (blue)

**Typography** (`theme.font.*`):
- `theme.font.family_body` - Body text font family
- `theme.font.family_heading` - Heading font family

**Note:** Tokens use underscore notation (e.g., `text_muted`) for Django template compatibility. CSS variables use hyphens (`--theme-color-text-muted`) but are converted to underscores for email templates.

**Border Radius** (`theme.radius.*`):
- `theme.radius.sm` - Small radius (4px)
- `theme.radius.md` - Medium radius (8px)
- `theme.radius.lg` - Large radius (12px)

**Spacing** (`theme.space.*`):
- `theme.space.2` - 8px
- `theme.space.4` - 16px
- `theme.space.6` - 24px

### Usage Example

```html
<mj-button
  background-color="{{ theme.color.primary|default:'#2563eb' }}"
  color="{{ theme.color.text_inverse|default:'#ffffff' }}"
  border-radius="{{ theme.radius.md|default:'0.5rem' }}"
>
  Click Me
</mj-button>
```

Always include `|default:` filters with fallback values in case tokens aren't available.

---

## Design Guidelines

- All components use the nested `theme` context object for styling
- Components are responsive and work on mobile/desktop
- Product thumbnails are 60x60px WebP format with alt text fallback
- Default colors from Starter theme: primary #2563eb, text #1f2937, etc.
- Typography: Headers 24px, body 16px, small 14px
