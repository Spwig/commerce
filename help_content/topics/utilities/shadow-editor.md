---
slug: shadow-editor
title_i18n_key: Shadow Editor
category: design-content
component: page_builder
keywords:
  - shadow
  - box shadow
  - text shadow
  - drop shadow
  - shadow editor
  - depth
  - elevation
  - page builder effects
url_patterns:
  - /admin/page_builder/page/
  - /admin/design/headerfootertemplate/
related:
  - page-builder
published: true
---

The shadow editor lets you add depth and dimension to elements with configurable box shadows and text shadows. Shadows create visual hierarchy, draw attention to important elements, and give your storefront a polished, modern feel. Open any element's **Style tab** and look for the **Effects** group to access the shadow editor.

![Shadow Editor](/static/core/admin/img/help/shadow-editor/shadow-editor.webp)

## Shadow Types

The editor provides two tabs at the top:

- **Box Shadow** — Adds a shadow around the entire element's bounding box. Use this for cards, buttons, containers, images, and sections.
- **Text Shadow** — Adds a shadow behind text characters only. Use this for headings or text overlaid on images to improve readability.

Each tab has its own independent configuration. You can apply both a box shadow and a text shadow to the same element if needed.

## Shadow Properties

Every shadow layer is defined by the following properties:

| Property | Description | Range |
|----------|-------------|-------|
| **Offset X** | Horizontal distance of the shadow from the element | -50px to 50px |
| **Offset Y** | Vertical distance of the shadow from the element | -50px to 50px |
| **Blur Radius** | How soft or diffuse the shadow edge appears. Higher values produce softer shadows. | 0px to 100px |
| **Spread Radius** | Expands or contracts the shadow size relative to the element (box shadow only) | -50px to 50px |
| **Color** | The shadow color, configurable with full opacity support via the color picker | Any color with alpha |
| **Inset** | Toggle to render the shadow inside the element instead of outside (box shadow only) | On / Off |

Adjust values using the sliders or type precise numbers directly into the input fields.

## Multiple Shadows

You can stack multiple shadow layers on a single element to create complex, realistic depth effects:

- Click the **+** button to add a new shadow layer
- Each layer appears as a row in the shadow list with its own controls
- Drag layers to reorder them — shadows render in list order, with the first layer on top
- Toggle the **eye icon** on any layer to temporarily hide it without deleting the configuration
- Click the **trash icon** to remove a layer

Combining a tight, dark shadow with a wide, soft shadow creates a natural "lifted" effect that mimics physical depth.

## Shadow Presets

Quick-apply presets let you add common shadow styles with a single click:

| Preset | Description |
|--------|-------------|
| **Small** | Subtle, close shadow for slight elevation (cards, inputs) |
| **Medium** | Moderate depth for interactive elements (buttons, dropdowns) |
| **Large** | Prominent shadow for floating elements (modals, popovers) |
| **Soft** | Wide blur with low opacity for a gentle, diffused glow |
| **Hard** | Minimal blur with higher opacity for a sharp, defined edge |
| **Inset** | Inner shadow for a pressed or recessed appearance |

After applying a preset, you can adjust individual properties to fine-tune the result.

## Current vs New Preview

At the bottom of the editor, two comparison boxes display the **current** shadow (as saved) and the **new** shadow (your pending changes). This side-by-side view makes it easy to evaluate the difference before committing. Click **Apply** to accept, or click away to discard your changes.

## Where It Appears

The shadow editor is available in the following locations:

- **Page Builder** — Style tab, Effects group on sections, containers, columns, and individual elements
- **Header/Footer Builder** — Widget-level shadow settings for elements like logos, search bars, and navigation items

Any element that supports the Effects style group will show the shadow editor controls.

## Tips

- Use subtle shadows (Small or Soft presets) for most elements — heavy shadows can make a design feel cluttered.
- Combine a close, dark shadow with a distant, light shadow for the most natural-looking elevation.
- Inset shadows work well on input fields and containers to create a "sunken" panel effect.
- Text shadows should be minimal — a 1px offset with slight blur improves legibility on image backgrounds without looking dated.
- Test your shadows against both light and dark backgrounds if your theme supports a dark mode toggle.
