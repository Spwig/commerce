---
slug: color-picker
title_i18n_key: Color Picker
category: design-content
component: page_builder
keywords:
  - color picker
  - color
  - hex
  - RGB
  - HSL
  - theme color
  - color token
  - design token
  - branding
  - brand color
  - page builder style
  - header builder style
url_patterns:
  - /admin/page_builder/page/
  - /admin/design/headerfootertemplate/
  - /admin/design/menutemplate/
  - /admin/catalog/product/
related:
  - page-builder
  - design-themes
published: true
---

The advanced color picker lets you choose colors using multiple input methods and theme-aware presets. It appears anywhere a color property is used across the platform — in the page builder, header/footer builder, menu builder, and catalog admin. Click any color swatch or color input field to open the picker.

![Color Picker](/static/core/admin/img/help/color-picker/color-picker.webp)

## Color Input Methods

The picker supports several ways to define a color:

| Method | Description | Example |
|--------|-------------|---------|
| **Hex** | Enter a 6-digit hex code directly | `#FF5733` |
| **RGB** | Adjust Red, Green, and Blue sliders (0-255 each) | `rgb(255, 87, 51)` |
| **HSL** | Set Hue (0-360), Saturation (0-100%), and Lightness (0-100%) | `hsl(14, 100%, 60%)` |
| **RGBA** | RGB with an alpha transparency channel | `rgba(255, 87, 51, 0.8)` |
| **HSLA** | HSL with an alpha transparency channel | `hsla(14, 100%, 60%, 0.8)` |
| **Visual Spectrum** | Click or drag on the color spectrum area to pick visually | Point-and-click selection |

You can also type a value directly into the text input at the bottom of the picker.

## Format Selector

A dropdown at the top of the picker lets you switch between **HEX**, **RGB**, **RGBA**, **HSL**, and **HSLA** output modes. When you switch formats, the current color is automatically converted — no values are lost. Choose the format that best fits your workflow or your design system requirements.

## Color Presets

Below the spectrum area, a row of quick-access color swatches provides one-click selection for common colors. These swatches are **theme-aware**: they automatically reflect the active theme's primary, secondary, accent, and neutral palette colors. This makes it easy to stay consistent with your brand without memorizing hex codes.

To apply a preset, click the swatch. The picker updates immediately to show the selected color in the spectrum and input fields.

## Opacity / Alpha

When using RGBA or HSLA mode, a horizontal **alpha slider** appears below the spectrum. Drag it to set transparency from 0% (fully transparent) to 100% (fully opaque). The opacity value is also editable as a numeric input beside the slider for precise control.

Semi-transparent colors are useful for overlays, hover effects, and layered design elements.

## Current vs New Preview

At the bottom of the picker, two side-by-side boxes display the **current** applied color and the **new** selected color. This comparison lets you evaluate the change before committing. Click **Apply** to accept the new color, or click away from the picker to cancel and keep the current value.

## Where It Appears

The color picker is a shared utility used throughout the admin:

- **Page Builder** — Element text color, background color, border color, and hover states in the Style tab
- **Header/Footer Builder** — Widget text, background, icon, and link colors
- **Menu Builder** — Menu item link colors and hover/active state colors
- **Catalog Admin** — Product badge colors and category accent colors

Any field that accepts a color value opens this same picker, so the experience is consistent everywhere.

## Tips

- Use your theme's preset swatches to maintain brand consistency across pages and components.
- Switch to HSL mode when you need to create lighter or darker variants of the same hue — just adjust the Lightness value.
- Copy the hex code from the text input to reuse the exact same color in another field or share it with a designer.
- Use RGBA with reduced opacity for subtle overlay effects on images and hero sections.
- The picker remembers recently used colors during your session, so frequently used custom colors stay accessible.
- If you paste a color value in any supported format into the hex input, the picker will recognize and convert it automatically.
