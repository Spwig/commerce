# Text Element

A versatile text element with comprehensive typography and styling controls for the page builder system.

## Features

- **Rich Typography**: Font size, weight, family, line height, letter spacing
- **Color Control**: Text and background colors with custom color support
- **Alignment**: Left, center, right, justify
- **Spacing**: Margin and padding controls
- **Text Effects**: Uppercase, lowercase, capitalize, italic, underline, strikethrough
- **Layout**: Max width, truncation, white space control
- **Borders**: Width, color, radius options
- **Effects**: Shadows, opacity, z-index
- **HTML Support**: Optional HTML content rendering
- **Responsive**: Mobile-friendly design
- **Dark Mode**: Full dark theme support
- **RTL Support**: Right-to-left language support
- **Accessibility**: Proper focus states and ARIA support
- **Internationalization**: Full i18n support with translatable content

## Configuration Options

### Content
- **Text Content**: Main text content (translatable)
- **Allow HTML**: Enable HTML formatting in text

### Typography
- **Size**: Predefined size options (xs to 3xl) or custom font size
- **Weight**: Font weight options (thin to black) or custom weight
- **Color**: Predefined colors or custom color picker
- **Font Family**: Sans serif, serif, or monospace
- **Line Height**: Tight to loose or custom value
- **Letter Spacing**: Tighter to widest or custom value

### Text Effects
- **Uppercase/Lowercase/Capitalize**: Text case transformations
- **Italic**: Italic styling
- **Underline**: Underline decoration
- **Strikethrough**: Line-through decoration
- **Text Shadow**: Custom text shadow effects

### Layout & Spacing
- **Alignment**: Text alignment options
- **Margins**: Top, bottom, left, right margin controls
- **Padding**: Top, bottom, left, right padding controls
- **Max Width**: Constrain text width
- **Truncate**: Truncate overflow with ellipsis

### Visual Effects
- **Background Color**: Background color options
- **Borders**: Width, color, and radius controls
- **Shadow**: Drop shadow effects
- **Opacity**: Transparency control
- **Z-Index**: Stacking order

### Advanced
- **White Space**: Control how white space is handled
- **Word Break**: Control word breaking behavior
- **Overflow**: Control overflow behavior
- **Custom Classes**: Additional CSS classes
- **Custom Styles**: Custom CSS properties
- **Data Attributes**: Custom data attributes
- **Element ID**: Unique element identifier

## Responsive Behavior

- Automatically adjusts font size on mobile devices
- Maintains readability across screen sizes
- Responsive typography scaling
- Touch-friendly hover effects

## Accessibility Features

- Proper semantic markup
- Focus indicators for keyboard navigation
- High contrast color options
- Screen reader compatible
- ARIA attributes support

## Dark Mode Support

The text element automatically adapts to dark mode themes:
- Text colors adjust to dark theme variables
- Background colors respect theme settings
- Border colors adapt to dark mode
- Maintains readability in all themes

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Internet Explorer 11+ (with fallbacks)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Usage Examples

### Basic Text
```json
{
  "text": "Welcome to our website",
  "size": "lg",
  "weight": "semibold",
  "color": "gray-900"
}
```

### Styled Text Block
```json
{
  "text": "This is a highlighted text block",
  "size": "base",
  "weight": "medium",
  "color": "blue-700",
  "background_color": "blue-50",
  "padding_top": "4",
  "padding_bottom": "4",
  "rounded": "lg",
  "align": "center"
}
```

### Custom Typography
```json
{
  "text": "Custom styled text",
  "custom_font_size": "1.25rem",
  "custom_font_weight": "550",
  "custom_text_color": "#2563eb",
  "line_height": "relaxed",
  "letter_spacing": "wide"
}
```

## Translation Support

The text element supports full internationalization:
- Text content is translatable
- Element name and description are localized
- Supports all configured languages
- RTL language support included

## Performance Notes

- Uses CSS classes for optimal performance
- Minimal inline styles
- Efficient responsive breakpoints
- Optimized for page builder rendering