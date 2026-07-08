---
slug: design-themes
title_i18n_key: Design & Themes
category: design-content
component: design
keywords:
  - design
  - theme
  - branding
  - colors
  - typography
  - header
  - footer
  - customization
  - layout
  - CSS
  - tokens
url_patterns:
  - /admin/design/
  - /admin/design/dashboard/
  - /admin/design/headertemplate/
  - /admin/design/footertemplate/
related:
  - store-settings
  - getting-started-overview
published: true
---

The Design & Theme system lets you control the look and feel of your entire storefront — from colors and typography to headers, footers, and page layouts. Navigate to **Settings > Design & Theme** to open the Design Dashboard.

![Design dashboard](/static/core/admin/img/help/design-themes/theme-dashboard.webp)

## Design Dashboard

The dashboard gives you an overview of your store's design status:

- **Active Theme** — Shows which theme is currently applied, with a preview and quick-access buttons
- **Design Stats** — Number of installed themes, custom headers, custom footers, and menus
- **Section Cards** — Jump to Themes, Header Builder, Footer Builder, Menus, or Announcements

## Themes

### Browsing Themes

Click the **Themes** section card to see all installed themes. Each theme card shows:
- Theme name and preview image
- Author and version
- Active/inactive status

### Activating a Theme

1. Click **Activate** on the theme you want to use
2. The theme is applied immediately to your storefront
3. Only one theme can be active at a time

### Theme Customization

Each theme supports a set of **design tokens** — configurable values that control the visual appearance without editing code.

Click **Customize** on your active theme to access the token editor. Available token categories include:

| Category | What It Controls |
|----------|-----------------|
| **Colors** | Primary, secondary, accent colors, backgrounds, text colors |
| **Typography** | Font families, sizes, weights, line heights |
| **Spacing** | Margins, padding, gaps between elements |
| **Borders** | Border widths, radii, colors |
| **Shadows** | Box shadows for cards, buttons, modals |
| **Buttons** | Button styles, sizes, hover effects |
| **Layout** | Container widths, grid gaps, breakpoints |

Changes preview in real-time before you save.

## Header Builder

The Header Builder lets you design your store's header using a drag-and-drop interface.

### Creating a Header

1. Navigate to **Design > Header Builder**
2. Click **Create Header** or edit an existing one
3. The builder has three rows: **Top Bar**, **Main Header**, and **Bottom Bar**
4. Drag widgets from the toolbox into any row

### Available Header Widgets

- **Logo** — Your store logo with configurable size and link
- **Navigation Menu** — Dropdown menu from your defined menus
- **Search Bar** — Product search with instant results
- **Cart Icon** — Mini-cart with item count badge
- **Account Icon** — Login/account dropdown
- **Language Selector** — Language switcher for multi-language stores
- **Currency Selector** — Currency switcher for multi-currency stores
- **Custom HTML** — Add any custom content
- **Social Icons** — Links to your social media profiles
- **Announcement Bar** — Promotional messages and offers

### Header Settings

Each header template has global settings:
- **Sticky Header** — Header stays visible when scrolling
- **Transparent Mode** — Overlay on hero images
- **Mobile Breakpoint** — When to switch to mobile layout

## Footer Builder

The Footer Builder works similarly to the Header Builder.

### Creating a Footer

1. Navigate to **Design > Footer Builder**
2. Click **Create Footer** or edit an existing one
3. The builder supports multiple columns and rows
4. Drag widgets into position

### Available Footer Widgets

- **Navigation Menu** — Footer navigation links
- **Newsletter Signup** — Email subscription form
- **Social Icons** — Social media links
- **Custom HTML** — Custom content, badges, certifications
- **Payment Icons** — Show accepted payment methods
- **Copyright** — Dynamic copyright text with year
- **Logo** — Footer logo variant

## Navigation Menus

Menus define the navigation links in your header and footer.

### Creating a Menu

1. Navigate to **Design > Menus**
2. Click **Add Menu**
3. Give the menu a name (e.g., "Main Navigation")
4. Add menu items:
   - **Page Link** — Link to a page builder page
   - **Category Link** — Link to a product category
   - **Custom URL** — Any external or internal URL
   - **Dropdown** — Nested sub-menu items
5. Drag items to reorder them
6. Save and assign the menu to a header or footer widget

## Announcements

Create promotional banners that appear at the top of your storefront.

### Creating an Announcement

1. Navigate to **Design > Announcements** (or use the Dashboard card)
2. Click **Add Announcement**
3. Configure:
   - **Message** — The announcement text (supports translations)
   - **Link** — Optional URL when clicked
   - **Style** — Background color, text color, icon
   - **Schedule** — Start and end dates
   - **Dismissible** — Whether customers can close it
4. Save and activate

Multiple announcements can be active simultaneously — they rotate automatically.

## Tips

- Start with the active theme's customizer to match your brand colors before building headers and footers.
- Use the **preview** feature in the Header and Footer builders to see changes before publishing.
- Create separate headers for desktop and mobile if you need very different layouts.
- Keep navigation simple — 5-7 top-level menu items is ideal for usability.
- Use announcements for time-sensitive promotions rather than permanent messages.
- The theme token editor supports real-time preview — experiment freely and save when satisfied.
