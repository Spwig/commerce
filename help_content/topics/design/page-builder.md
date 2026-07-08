---
slug: page-builder
title_i18n_key: Page Builder
category: design-content
component: page_builder
keywords:
  - page builder
  - visual editor
  - drag and drop
  - element
  - layout
  - container
  - hero
  - heading
  - text
  - image
  - button
  - page design
  - publish
  - draft
  - template
  - responsive
  - animation
  - visibility rules
url_patterns:
  - /admin/page_builder/page/
  - /admin/page_builder/pagetemplate/
related:
  - design-themes
published: true
---

The Page Builder is a visual drag-and-drop editor for creating rich, responsive pages without writing code. Add elements from a library of 39 components, style them with powerful utilities, set up animations and visibility rules, and publish with full version history.

![Page Builder](/static/core/admin/img/help/page-builder/builder-overview.webp)

## The Builder Interface

The builder has four main areas:

| Area | Location | Purpose |
|------|----------|---------|
| **Toolbar** | Top bar | Device preview (desktop/tablet/mobile), undo/redo, page settings, save draft, publish |
| **Element Library** | Left sidebar | Browse and drag 39 elements organized in 9 categories |
| **Canvas** | Center | Live WYSIWYG editing area — see changes as you make them |
| **Properties Panel** | Right sidebar | Edit the selected element's content, style, animations, and advanced settings |

## Element Library

Elements are organized into categories. Drag any element from the library onto the canvas to add it to your page.

| Category | Elements |
|----------|----------|
| **Layout** | Container, Divider, Hero Section, Modal Popup, Navigation Menu, Spacer |
| **Basic** | Heading, Text, Button, Icon |
| **Content** | Blog Post Carousel, Blog Post Grid, FAQ Accordion, Related Posts, Testimonials |
| **Media** | Image, Image Gallery, Image Accordion, Video Embed |
| **Forms** | Contact Form, Form, Newsletter Signup |
| **Marketing** | Countdown Timer, CTA Banner, Featured Blog Banner, Loyalty Banner, Promotion Banner, Trust Badges, Voucher Code Display |
| **E-commerce** | Category Showcase, Gift Card Promo, Product Carousel, Product Grid, Product List, Reviews Display, Sale Products, Store Locator |
| **Social** | Social Links |
| **Navigation** | Search Bar |

### Containers and Nesting

The **Container** element is the foundation for complex layouts. Containers can hold other elements — including other containers — letting you build multi-column grids and nested structures. Use the container's layout presets to quickly set up common column arrangements (50/50, 33/33/33, 25/75, etc.).

## Adding Elements

1. Find the element you want in the left sidebar
2. **Drag** it onto the canvas and drop it where you want it
3. Elements can be dropped between existing elements, or inside containers
4. The blue insertion line shows where the element will land
5. After dropping, the element is automatically selected and the properties panel opens

You can also reorder elements by dragging them up or down on the canvas.

## Editing Content

Select any element on the canvas to open its properties in the right panel. The **Content** tab shows fields specific to that element type.

![Properties Panel](/static/core/admin/img/help/page-builder/properties-panel.webp)

For example:
- **Heading** — text, HTML tag (H1–H6), alignment, anchor ID
- **Image** — image source (media library), alt text, link, sizing
- **Button** — label, URL, style variant, icon
- **Product Grid** — data source, number of columns, products per page, sort order
- **Hero Section** — title, subtitle, description, background, call-to-action buttons

Translatable content fields show a translation icon — click it to add translations for multi-language stores.

## Styling Elements

The **Style** tab provides visual controls for every element. Each section opens a dedicated utility editor.

![Style Tab](/static/core/admin/img/help/page-builder/style-tab.webp)

| Section | What It Controls | Utility |
|---------|-----------------|---------|
| **Typography** | Font family, size, weight, line height, letter spacing, text style | Typography Editor |
| **Colors** | Text color with hex/RGB/HSL input and theme tokens | Color Picker |
| **Background** | Solid color, gradient, image, or video backgrounds with hover states | Background Editor |
| **Border** | Border width, style, color, and radius per side | Border Editor |
| **Spacing** | Margin and padding with visual box model editor | Spacing Editor |
| **Effects** | Box shadow with presets and multi-layer support, opacity slider | Shadow Editor |

Each utility is documented in its own help topic — search for "color picker", "background editor", etc. to learn more.

## Animations

The **Animations** tab lets you add movement to elements.

### Entrance Animations

Trigger when the element scrolls into view:

| Animation | Description |
|-----------|-------------|
| Fade In | Gradually appears |
| Slide In (Up/Down/Left/Right) | Slides in from a direction |
| Zoom In | Grows from small to full size |
| Bounce In | Bounces into place |
| Pulse / Shake / Bounce / Flash / Spin | Attention-getting effects |

Configure **duration** (0.3s–1.5s), **delay** (0–1s), **timing function** (ease, ease-in, ease-out, linear), and **repeat** (once or infinite).

### Hover Animations

Trigger when a visitor hovers over the element:

| Effect | Description |
|--------|-------------|
| Scale Up / Scale Down | Grows or shrinks |
| Lift | Floats upward |
| Rotate (CW / CCW) | Rotates clockwise or counter-clockwise |
| Brighten / Fade | Changes brightness or opacity |
| Shadow Grow | Shadow expands |
| Lift with Shadow | Rises with growing shadow |
| Pulse Scale / Skew / Border Glow | Special effects |

Configure **duration**, **timing**, and **intensity** (subtle, normal, strong).

## Advanced Settings

The **Advanced** tab provides fine-grained control:

### Visibility Rules

Control when an element is shown or hidden based on conditions:

- **User status** — logged in, logged out, new customer, returning customer
- **Device** — desktop, tablet, mobile
- **Time** — date range, time of day, day of week
- **Customer group** — VIP, wholesale, etc.
- **Cart value** — minimum or maximum cart total
- **Geography** — country, region
- And 20+ more rule types

Rules can be combined with AND/OR logic for complex targeting.

### Custom CSS

| Field | Purpose |
|-------|---------|
| **Element ID** | Unique ID for anchor links or CSS targeting |
| **Custom CSS Classes** | Additional classes to apply |
| **Custom CSS Styles** | Inline CSS for one-off overrides |
| **Data Attributes** | Custom data-* attributes as key-value pairs |
| **Z-Index** | Stacking order for overlapping elements |

## Publishing Workflow

Pages use a draft/publish system with full version history:

| Status | Meaning |
|--------|---------|
| **Draft** | Work in progress — not visible to visitors |
| **Published** | Live on your store |
| **Archived** | Removed from the site but preserved |

### How It Works

1. Make changes in the builder — they are saved as a **draft**
2. Click **Save Draft** to save without publishing
3. Click **Publish** to make the current draft live
4. Each publish creates a **version snapshot**
5. You can **restore** any previous version from the version history (clock icon in the toolbar)

This means you can experiment freely — your live page stays unchanged until you explicitly publish.

## Page Templates

Save time by working with templates:

- **Save as Template** — save any page's design as a reusable template
- **Create from Template** — start a new page from an existing template
- **Template Categories** — organize templates by purpose (landing page, about, product showcase, etc.)

Templates capture the full page structure including all elements, content, and styling.

## Responsive Design

Use the device preview buttons in the toolbar to see how your page looks on different screen sizes:

- **Desktop** — full-width layout
- **Tablet** — medium viewport
- **Mobile** — narrow viewport

Elements automatically reflow based on their container settings. You can also use visibility rules to show or hide specific elements on certain devices.

## Tips

- **Start with a Container** — most layouts begin with a container to create columns and structure. Use layout presets for common arrangements.
- **Use Hero sections for page headers** — the Hero element provides title, subtitle, background image, and CTA buttons in one component.
- **Preview before publishing** — click Preview to see exactly what visitors will see, then publish when you're satisfied.
- **Use visibility rules for personalization** — show different content to logged-in vs. logged-out visitors, or target specific customer groups.
- **Keep animations subtle** — one or two entrance animations per page section look professional. Too many animations can feel overwhelming.
- **Name your containers** — use the Element ID field to label containers (e.g., "hero-section", "features") so they're easy to find in complex pages.
- **Test on all devices** — use the device preview to check your layout on desktop, tablet, and mobile before publishing.
- **Leverage templates** — save your best page designs as templates to speed up future page creation.
