# Button Element

A versatile, interactive button element with extensive customization options and full translation support.

## Features

- **Multiple Styles**: Primary, Secondary, Success, Danger, Warning, Info
- **Size Variants**: Small, Medium, Large, Extra Large
- **Layout Options**: Full width, Outline style, Rounded corners
- **Icons**: Support for before/after SVG icons
- **Accessibility**: ARIA labels and semantic HTML
- **Translation Ready**: Full i18n support with element-specific translations

## Configuration

### Basic Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `text` | string | "Button Text" | The button label text |
| `url` | url | "#" | Target URL for the button |
| `target` | select | "_self" | Link target behavior |

### Styling Properties

| Property | Type | Default | Options |
|----------|------|---------|---------|
| `style` | select | "primary" | primary, secondary, success, danger, warning, info |
| `size` | select | "md" | sm, md, lg, xl |
| `full_width` | boolean | false | Makes button span full container width |
| `outline` | boolean | false | Uses outline button style |
| `rounded` | boolean | false | Adds rounded corners |

### Advanced Properties

| Property | Type | Description |
|----------|------|-------------|
| `icon_before` | string | SVG path for icon before text |
| `icon_after` | string | SVG path for icon after text |
| `title` | string | Tooltip text (translatable) |
| `aria_label` | string | Accessibility label (translatable) |
| `onclick` | string | JavaScript click handler |

## Translation Support

The button element includes translations for:

- **English (en)**: Default language
- **Spanish (es)**: Complete translation set
- **French (fr)**: Complete translation set
- **German (de)**: Available
- **Portuguese (pt)**: Available
- **Chinese Simplified (zh-hans)**: Available
- **Japanese (ja)**: Complete translation set

### Translatable Strings

- Button Text (default fallback)
- Common button labels (Click here, Learn more, Get started, etc.)
- Tooltip text
- Accessibility labels

## Usage Examples

### Basic Button
```json
{
  "text": "Click Me",
  "url": "/action",
  "style": "primary"
}
```

### Call-to-Action Button
```json
{
  "text": "Get Started",
  "url": "/signup",
  "style": "success",
  "size": "lg",
  "full_width": true
}
```

### Icon Button
```json
{
  "text": "Download",
  "url": "/download",
  "style": "secondary",
  "icon_before": "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
}
```

## CSS Classes

The button element uses Tailwind CSS classes and provides the following CSS structure:

- `.btn`: Base button class
- `.btn-{style}`: Style variants (primary, secondary, etc.)
- `.btn-{size}`: Size variants (sm, lg, xl)
- `.btn-outline`: Outline style modifier
- `.w-full`: Full width modifier
- `.rounded-full`: Rounded corners modifier

## Browser Support

- Modern browsers (Chrome 60+, Firefox 60+, Safari 12+, Edge 79+)
- Progressive enhancement for older browsers
- Accessible across screen readers and assistive technologies

## Version History

### v1.0.0
- Initial release with full translation support
- Complete configuration options
- Accessibility features
- Icon support