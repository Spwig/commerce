---
slug: border-editor
title_i18n_key: Border Editor
category: design-content
component: page_builder
keywords:
  - border
  - border width
  - border style
  - border color
  - border radius
  - rounded corners
  - page builder border
  - element border
url_patterns:
  - /admin/page_builder/page/
  - /admin/design/headerfootertemplate/
  - /admin/design/menutemplate/
related:
  - page-builder
published: true
---

The Border Editor provides fine-grained control over element borders, including style, color, width per side, and corner radius per corner. It opens as a floating panel with a live preview and two tabs for basic and advanced settings.

![Border Editor](/static/core/admin/img/help/border-editor/border-editor.webp)

## Live Preview

A preview box at the top of the editor shows your border changes in real time. The box displays the word "Preview" inside a bordered rectangle that updates instantly as you adjust style, color, width, and radius values.

## Basic vs Advanced Mode

The editor is organized into two tabs:

| Tab | What It Contains |
|-----|-----------------|
| **Basic** | Border style, color, width (with per-side controls), and border radius (with per-corner controls) |
| **Advanced** | Individual corner radius fine-tuning and the experimental Corner Shape property |

Most border work is done entirely in the Basic tab. The Advanced tab is useful when you need precise control over individual corners or want to experiment with newer CSS features.

## Border Style

A dropdown with nine options that control the appearance of the border line:

| Style | Description |
|-------|-------------|
| **None** | No border (removes any existing border) |
| **Solid** | A single continuous line (default) |
| **Dashed** | A series of short dashes |
| **Dotted** | A series of round dots |
| **Double** | Two parallel solid lines |
| **Groove** | A carved, 3D-effect border that appears pressed into the surface |
| **Ridge** | A raised, 3D-effect border (opposite of groove) |
| **Inset** | Makes the element appear embedded or pressed in |
| **Outset** | Makes the element appear raised or popped out |

Setting the style to None removes the border entirely, regardless of width or color settings.

## Border Color

A text input field paired with a Color Picker button. Enter a hex value directly (e.g. `#3b82f6`) or click the color swatch to open the full Color Picker with hex, RGB, and HSL input modes plus a visual color area. The default color is black (`#000000`).

## Border Width

Controls the thickness of the border in pixels. The Basic tab shows four individual side inputs:

| Side | Input |
|------|-------|
| **Top** | Numeric input, minimum 0 |
| **Right** | Numeric input, minimum 0 |
| **Bottom** | Numeric input, minimum 0 |
| **Left** | Numeric input, minimum 0 |

A **link toggle button** (chain icon) next to the label controls whether all four sides are linked:

- **Linked** (default) — changing any value updates all four sides at once
- **Unlinked** — each side can have a different width, useful for effects like a bottom-only border or left accent borders

## Border Radius

Controls the rounding of each corner. The Basic tab shows four corner inputs:

| Corner | Label |
|--------|-------|
| **Top Left** | TL |
| **Top Right** | TR |
| **Bottom Left** | BL |
| **Bottom Right** | BR |

A **link toggle button** works the same way as border width:

- **Linked** (default) — all four corners share the same radius value
- **Unlinked** — each corner can have a different radius

Common radius values:

| Value | Effect |
|-------|--------|
| 0px | Sharp square corners |
| 4-8px | Subtle rounding, good for cards and buttons |
| 12-16px | Noticeable rounding, a modern, soft look |
| 50% | Full circle or pill shape (depending on element dimensions) |

The unit selector supports px, em, rem, and % for both width and radius values.

## Corner Shape (Advanced)

The Advanced tab includes an experimental **Corner Shape** property. This CSS feature controls whether rounded corners use the standard round shape or a more angular "scoop" shape. Browser support is limited, and the editor displays a compatibility warning when the current browser does not support this property.

## Footer Actions

| Button | Action |
|--------|--------|
| **Reset** | Reverts all values to their state when the editor was opened |
| **Cancel** | Closes the editor without applying changes |
| **Apply** | Saves the border settings and closes the editor |

## Where It Appears

The Border Editor is available across several builders:

- **Page Builder** — select any element, open the Style tab, and click the Border section
- **Header/Footer Builder** — add borders to header sections, navigation containers, and footer areas
- **Menu Builder** — style borders on menu items and dropdown containers

The editor reads the current computed border styles from the live element on the canvas, so it always opens with the correct existing values.

## Tips

- **Use borders sparingly** — subtle 1px borders in a light gray create clean separation between sections without adding visual weight.
- **Combine radius with shadow** — rounded corners paired with a soft box shadow (via the Shadow Editor) produce a polished card effect.
- **Try single-side borders** — unlink the sides and set only a bottom or left border for accent lines, section dividers, or sidebar indicators.
- **Use percentage radius for pills** — set all corners to 50% on a button or badge to create a pill shape that adapts to any content size.
- **Check the preview** — the live preview box updates immediately, so experiment freely before applying.
