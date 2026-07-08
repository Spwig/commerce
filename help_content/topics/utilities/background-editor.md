---
slug: background-editor
title_i18n_key: Background Editor
category: design-content
component: page_builder
keywords:
  - background
  - background color
  - background image
  - background gradient
  - background video
  - overlay
  - hover background
  - page builder background
  - header background
url_patterns:
  - /admin/page_builder/page/
  - /admin/design/headerfootertemplate/
  - /admin/design/menutemplate/
related:
  - page-builder
  - color-picker
  - gradient-creator
published: true
---

The background editor gives you full control over element backgrounds with four types: solid color, gradient, image, and video. It also supports separate Normal and Hover states so you can create interactive visual effects. Open any element's **Style tab** and look for the **Background** section to access the editor.

![Background Editor](/static/core/admin/img/help/background-editor/background-editor.webp)

## Normal and Hover States

At the top of the background editor, a toggle switches between **Normal** and **Hover** states. Each state has its own independent background configuration:

- **Normal** — The default background shown when the page loads
- **Hover** — The background applied when a visitor moves their cursor over the element

Two small preview blocks beside the toggle show the current Normal and Hover backgrounds side by side, so you can see the contrast at a glance. Configure the Normal state first, then switch to Hover to add an interactive effect if desired.

## Background Types

Select a background type from the row of icons at the top of the editor panel:

| Type | Description |
|------|-------------|
| **Color** | A solid fill using a single color value. Quick to apply and lightweight. |
| **Gradient** | A smooth blend between two or more colors, either linear or radial. Includes built-in presets like Ocean, Sunset, Forest, and Berry. For advanced gradient editing, see the [Gradient Creator](gradient-creator) topic. |
| **Image** | An uploaded image or one selected from the media library. Supports positioning, sizing, and repeat controls. |
| **Video** | A background video URL with an optional poster image that displays while the video loads or on mobile devices. |

Only one type can be active at a time per state. Switching types does not delete your previous configuration — you can switch back and your settings will be preserved.

## Color Backgrounds

When Color is selected:

- **Hex Input** — Type a hex code directly (e.g., `#1A1A2E`)
- **Color Swatches** — Click a preset swatch for quick selection. Swatches are theme-aware and reflect your active theme's palette.
- **Edit Button** — Opens the full color picker with spectrum, sliders, and format options (see the [Color Picker](color-picker) topic)

Color backgrounds render instantly and have no performance impact, making them ideal for sections, cards, and containers.

## Gradient Backgrounds

When Gradient is selected:

- **Preset Gradients** — Choose from built-in gradients: Ocean, Sunset, Forest, Berry, and others
- **Custom Gradient** — Click **Edit** to open the gradient creator where you can set direction, type (linear or radial), and color stops
- **Angle Slider** — Adjust the gradient direction for linear gradients (0-360 degrees)

Gradients add visual depth without requiring image assets and scale perfectly to any screen size.

## Image Backgrounds

When Image is selected:

- **Upload or Media Library** — Click the image placeholder to upload a new image or select one from your media library
- **Size** — Choose **Cover** (fills the element, may crop), **Contain** (fits inside the element), or a custom size
- **Position** — Set the focal point using a 9-point grid (top-left, center, bottom-right, etc.) or enter custom X/Y percentages
- **Repeat** — Toggle repeat on or off. Useful for tiling patterns
- **Overlay** — Add a color overlay on top of the image with adjustable opacity, useful for ensuring text readability

Always optimize images before uploading. Large uncompressed images slow down page load times.

## Video Backgrounds

When Video is selected:

- **Video URL** — Enter a direct URL to an MP4 or WebM video file
- **Poster Image** — Upload a fallback image displayed while the video loads and on devices that do not autoplay video
- **Autoplay / Loop / Muted** — Video backgrounds autoplay, loop, and are muted by default to comply with browser policies

Keep background videos short (10-30 seconds), compressed, and visually subtle. They should enhance the section without distracting from content.

## Where It Appears

The background editor is available for every element that supports backgrounds:

- **Page Builder** — Sections, containers, columns, and individual elements all have a Background section in the Style tab
- **Header/Footer Builder** — Row backgrounds and individual widget backgrounds
- **Menu Builder** — Menu container and dropdown panel backgrounds

The same editor interface is used everywhere, so your workflow stays consistent across builders.

## Tips

- Use a semi-transparent color overlay on image backgrounds to ensure text remains readable regardless of the image content.
- Gradient presets are a fast way to add visual interest — apply one, then customize the angle or colors to match your brand.
- Set both Normal and Hover backgrounds on interactive cards to give visitors clear visual feedback when they explore your content.
- For image backgrounds, always set a focal point so the most important part of the image stays visible on all screen sizes.
- Prefer color or gradient backgrounds over images for sections where load speed is critical, such as above-the-fold content.
- Test video backgrounds on mobile devices — most mobile browsers will show the poster image instead of playing the video.
