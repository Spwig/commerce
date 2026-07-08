---
slug: typography-editor
title_i18n_key: Typography Editor
category: design-content
component: page_builder
keywords:
  - typography
  - font
  - font family
  - font size
  - font weight
  - line height
  - letter spacing
  - text style
  - page builder typography
  - text formatting
url_patterns:
  - /admin/page_builder/page/
  - /admin/design/headerfootertemplate/
  - /admin/design/menutemplate/
related:
  - page-builder
  - design-themes
published: true
---

The Typography Editor is a shared style utility that gives you full control over text appearance. It opens as a floating panel whenever you edit typography properties on any element across the Page Builder, Header/Footer Builder, or Menu Builder.

![Typography Editor](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## Live Preview

The editor shows a side-by-side comparison at the top of the panel:

| Box | Purpose |
|-----|---------|
| **Current** | Displays "The quick brown fox..." in the existing typography style |
| **New** | Updates in real time as you adjust settings, showing the result before you apply |

This lets you compare before and after without committing to any changes.

## Font Tab

The Font tab is the default view when the editor opens.

**Font Family** — A searchable dropdown with 70+ fonts organized by category. Each font previews in its own typeface so you can see how it looks before selecting. Fonts are loaded on demand from Google Fonts when needed.

**Font Size** — Numeric input with a unit selector supporting px, em, rem, and %. The default is 16px.

**Font Weight** — A slider from 100 (Thin) to 900 (Black):

| Value | Name |
|-------|------|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

Not every font supports all nine weights. The editor shows which weights are available for the selected font family.

**Font Style** — Toggle buttons for Normal, Italic, and Oblique.

## Spacing Tab

Fine-tune the space around and between characters:

| Control | What It Does | Default |
|---------|-------------|---------|
| **Line Height** | Vertical space between lines of text | normal |
| **Letter Spacing** | Horizontal space between individual characters | normal |
| **Word Spacing** | Horizontal space between words | normal |
| **Text Indent** | Indentation of the first line in a paragraph | 0 |

Each spacing control includes a unit selector (px, em, rem, %).

## Style Tab

Control text decoration and visual effects:

- **Text Decoration** — None, Underline, Overline, or Line-through
- **Decoration Style** — Solid, Dashed, Dotted, Double, or Wavy (applies when a decoration is active)
- **Decoration Color** — Color picker for the decoration line, defaults to the text color
- **Text Shadow** — Optional shadow effect with offset, blur, and color controls

## Transform Tab

Change the capitalization of text without editing the content:

| Option | Result |
|--------|--------|
| **None** | Text appears as written |
| **Uppercase** | ALL LETTERS ARE CAPITALIZED |
| **Lowercase** | all letters are lowercase |
| **Capitalize** | First Letter Of Each Word Is Capitalized |

Additional controls on this tab include **Text Align** (left, center, right, justify), **Vertical Align**, and **Text Direction** (LTR or RTL).

## Available Font Families

The editor includes a curated library of system and Google Fonts, grouped by category:

| Category | Fonts |
|----------|-------|
| **System** | System Default, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS |
| **Sans-Serif (Modern)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans |
| **Sans-Serif (Classic)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend |
| **Serif** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya |
| **Serif (System)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria |
| **Monospace** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono |
| **Display** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black |

Google Fonts are loaded automatically when selected. System fonts use proper CSS fallback chains for reliable rendering across platforms.

## Where It Appears

The Typography Editor is available wherever text styling is needed:

- **Page Builder** — Select any element, open the Style tab, and click the Typography section
- **Header/Footer Builder** — Style text in navigation links, logo text, menu items, and footer content
- **Menu Builder** — Control typography for menu labels and sub-menu items
- **Catalog Admin** — Used in product description and content editors where typography controls are exposed

The editor is always accessed through the same consistent interface regardless of context.

## Tips

- **Pair fonts intentionally** — use a display or serif font for headings and a clean sans-serif for body text. Classic combinations like Playfair Display + Inter or Montserrat + Merriweather work well.
- **Limit font families per page** — two or three font families per page is usually plenty. More than that can slow load times and create visual clutter.
- **Use relative units for responsive text** — em and rem scale with the base font size, making your typography adapt to different screen sizes automatically.
- **Check weight availability** — if text looks the same at 400 and 500, the selected font may not support that weight. The editor indicates which weights each font provides.
- **Preview on all devices** — text that looks good at desktop sizes may be too small or too large on mobile. Use the Page Builder device preview to verify.
- **Use the live preview** — always compare Current vs New in the preview boxes before applying to avoid unexpected changes.
