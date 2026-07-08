---
slug: gradient-creator
title_i18n_key: Gradient Creator
category: design-content
component: page_builder
keywords:
  - gradient
  - linear gradient
  - radial gradient
  - color gradient
  - gradient creator
  - gradient stop
  - page builder gradient
  - background gradient
url_patterns:
  - /admin/page_builder/page/
  - /admin/design/headerfootertemplate/
related:
  - page-builder
  - background-editor
  - color-picker
published: true
---

The Gradient Creator lets you build smooth color transitions for element backgrounds. It is accessed through the Background Editor's Gradient tab and opens as a floating panel with a visual gradient bar, color stop controls, and preset options.

![Gradient Creator](/static/core/admin/img/help/gradient-creator/gradient-creator.webp)

## Accessing the Gradient Creator

1. Select an element in the Page Builder or Header/Footer Builder
2. Open the **Style** tab in the properties panel
3. Click the **Background** section to open the Background Editor
4. Switch to the **Gradient** tab
5. The Gradient Creator panel opens with a live preview and editing controls

## Live Preview

The top of the panel shows a side-by-side comparison:

| Box | Purpose |
|-----|---------|
| **Current** | The existing gradient (or transparent if none is set) |
| **New** | Updates in real time as you make changes |

An arrow between the two boxes indicates the direction of change.

## Gradient Types

Three gradient types are available, selectable via tabs at the top of the editor:

| Type | Description | Controls |
|------|-------------|----------|
| **Linear** | Color transitions along a straight line | Angle slider (0-360 degrees) with preset direction buttons (up, diagonal, right, down, etc.) |
| **Radial** | Color transitions radiating outward from a center point | Shape selector (circle or ellipse) and position picker (center, top, bottom, corners) |
| **Conic** | Color transitions rotating around a center point | Starting angle slider (0-360 degrees) and position picker |

### Linear Direction Controls

For linear gradients, you can set the angle three ways:
- **Angle slider** — drag from 0 to 360 degrees
- **Angle input** — type a precise degree value
- **Preset buttons** — click arrow icons for common directions (to top, to top-right, to right, to bottom-right, to bottom, to bottom-left, to left, to top-left)

## Color Stops

The gradient bar shows your current color stops as draggable markers. Each stop defines a color at a specific position along the gradient.

**Adding stops** — Click the **+** button in the Color Stops section to add a new stop. There is no hard limit on the number of stops.

**Editing stops** — Each stop in the list shows:
- A color swatch that opens the Color Picker when clicked
- A position value (0% to 100%) that you can type or adjust
- An opacity control (0 to 1)
- A delete button to remove the stop

**Reordering** — Drag stops along the gradient bar to reposition them visually.

## Gradient Presets

Six built-in presets are available for quick starting points. Click any preset to apply it instantly:

| Preset | Colors | Angle |
|--------|--------|-------|
| **Ocean** | Light blue to blue | 120 degrees |
| **Sunset** | Warm orange to coral pink (3 stops) | 45 degrees |
| **Forest** | Indigo to emerald green | 135 degrees |
| **Berry** | Pink to purple-blue | 90 degrees |
| **Flame** | Red to golden yellow | 45 degrees |
| **Night** | Dark slate to ocean blue | 180 degrees |

Presets are starting points. After applying one, you can modify the colors, add or remove stops, and change the angle to create your own variation.

## Footer Actions

| Button | Action |
|--------|--------|
| **Clear** | Removes the gradient entirely, resetting to transparent |
| **Apply** | Saves the gradient and closes the editor |

Closing the editor without clicking Apply discards your changes.

## Where It Appears

The Gradient Creator is used in:

- **Page Builder** — via the Background Editor's Gradient tab on any element
- **Header/Footer Builder** — for gradient backgrounds on header sections, navigation bars, and footer areas

It works together with the Background Editor, which also offers solid color, image, and video background options.

## Tips

- **Start with a preset** — apply a preset that is close to what you want, then adjust the colors and angle rather than building from scratch.
- **Use two or three stops** — simple gradients with two stops look clean and professional. More stops are useful for complex effects but can quickly become overwhelming.
- **Match your brand colors** — use the Color Picker to enter exact hex values from your brand palette for consistent, on-brand gradients.
- **Test with content** — gradients that look striking on their own may reduce text readability. Always check that text over gradient backgrounds has sufficient contrast.
- **Try radial for spotlight effects** — radial gradients work well for drawing attention to a center area, such as a hero section focal point.
