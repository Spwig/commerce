---
slug: spacing-editor
title_i18n_key: Spacing Editor
category: design-content
component: page_builder
keywords:
  - spacing
  - margin
  - padding
  - spacing editor
  - box model
  - layout spacing
  - page builder spacing
  - element spacing
url_patterns:
  - /admin/page_builder/page/
  - /admin/design/headerfootertemplate/
  - /admin/design/menutemplate/
related:
  - page-builder
published: true
---

The visual spacing editor lets you configure margin and padding using an intuitive box model diagram. Precise spacing control ensures consistent layouts and comfortable reading experiences across your storefront. Open any element's **Style tab** and look for the **Spacing** section to access the editor.

![Spacing Editor](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## The Box Model Diagram

The editor displays a visual box model with three nested layers:

- **Margin** (outer ring, typically shown in orange) — The space outside the element's border, separating it from neighboring elements
- **Padding** (inner ring, typically shown in green) — The space between the element's border and its content
- **Content** (center area) — The element's actual content, such as text or an image

Each side of the diagram (top, right, bottom, left) has a draggable handle and a numeric input. Drag a handle outward to increase the value, or inward to decrease it. You can also click directly on a side's value to type a precise number.

## Margin and Padding Tabs

Two tabs at the top of the editor switch between **Margin** and **Padding** views. When Margin is selected, the outer ring is highlighted and editable. When Padding is selected, the inner ring is highlighted and editable. The inactive ring remains visible for reference but is dimmed.

Both tabs share the same controls and unit options, so the workflow is identical for margin and padding configuration.

## Per-Side Controls

Each side has an independent value input and unit selector:

| Side | Description |
|------|-------------|
| **Top** | Space above the element (margin) or above the content (padding) |
| **Right** | Space to the right of the element or content |
| **Bottom** | Space below the element or content |
| **Left** | Space to the left of the element or content |

Click on any side's value in the diagram to select it, then type a number or use the up/down arrow keys to increment by 1. Hold Shift while pressing arrow keys to increment by 10.

## Units

The unit selector next to each value input lets you choose the measurement unit:

| Unit | Description |
|------|-------------|
| **px** | Pixels. Fixed size, consistent across devices. Best for precise, small spacing values. |
| **em** | Relative to the element's font size. Scales with typography changes. |
| **rem** | Relative to the root font size. Provides consistent scaling across the entire page. |
| **%** | Percentage of the parent element's width. Useful for fluid, responsive layouts. |
| **auto** | Lets the browser calculate the value automatically. Commonly used for horizontal centering with left/right margins. |

Choose a unit that matches your intent — use `px` for fixed gaps, `rem` for scalable spacing that respects theme typography tokens, and `%` for layouts that must adapt to container width.

## Link Sides

A **link icon** at the center of the diagram toggles linked mode:

- **Linked** (chain icon connected) — Changing any side's value updates all four sides to the same value. Useful for uniform spacing.
- **Unlinked** (chain icon broken) — Each side is controlled independently. Use this when you need different top/bottom and left/right values.

Click the link icon to toggle between modes. When you switch from unlinked to linked, all four sides are set to the value of the most recently edited side.

## Quick Presets

A row of preset buttons below the diagram provides one-click spacing configurations:

| Preset | Values |
|--------|--------|
| **None** | 0 on all sides |
| **Small** | Compact spacing suitable for tight layouts and inline elements |
| **Medium** | Balanced spacing for general-purpose use on cards and sections |
| **Large** | Generous spacing for hero areas and high-emphasis sections |
| **XL** | Extra-wide spacing for full-width banners and top-level page sections |

Presets apply to the currently active tab (Margin or Padding) and set all four sides at once. After applying a preset, you can adjust individual sides as needed.

## Where It Appears

The spacing editor is available for every element that supports layout spacing:

- **Page Builder** — Style tab, Spacing section on sections, containers, columns, and individual elements
- **Header/Footer Builder** — Row and widget spacing controls for vertical and horizontal gaps
- **Menu Builder** — Menu item padding and container margin settings

The same editor interface is used in all locations, ensuring a consistent experience across builders.

## Tips

- Use consistent spacing values across your pages — pick 2-3 standard sizes and stick with them for a clean, professional layout.
- Set margin to **auto** on left and right to horizontally center a fixed-width element within its parent.
- Prefer `rem` units for spacing if your theme uses responsive typography, so spacing scales proportionally with text size.
- Use the linked mode to set uniform padding quickly, then unlink and fine-tune individual sides if the content needs asymmetric spacing.
- Avoid excessive padding on mobile — test your spacing at narrow viewport widths to ensure content is not squeezed or overly padded.
