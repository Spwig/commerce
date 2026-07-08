# Image Element

A comprehensive responsive image element with advanced styling and display controls.

## Features

- **Responsive Design**: Multiple width options, aspect ratios, and object fit controls
- **Visual Effects**: Filters, shadows, opacity, hover effects
- **Accessibility**: Proper alt text, title attributes, focus states
- **Linking**: Optional clickable links with target options
- **Captions**: Styled figure captions with typography controls
- **Performance**: Lazy loading, srcset support for responsive images
- **Dark Mode**: Full dark theme support
- **RTL Support**: Right-to-left language compatibility
- **Internationalization**: Full i18n support with translatable content

## Key Configuration Options

### Image Source & Display
- Image source with file picker
- Alt text (required for accessibility)
- Width and height controls
- Object fit and positioning
- Aspect ratio support

### Visual Styling
- Border radius and borders
- Drop shadows
- Visual filters (grayscale, sepia, blur, brightness, contrast)
- Opacity controls
- Hover effects

### Layout & Spacing
- Alignment options
- Margin controls
- Max width constraints
- Container styling

### Interactive Features
- Optional linking with target controls
- Hover animations
- Focus states for accessibility

### Caption Support
- Optional figure captions
- Typography controls for captions
- Caption positioning and styling

### Performance Features
- Lazy loading support
- Responsive image srcset
- Sizes attribute for responsive behavior

## Usage Example

```json
{
  "src": "/media/example.jpg",
  "alt": "Example image description",
  "width": "full",
  "object_fit": "cover",
  "rounded": "lg",
  "shadow": "md",
  "caption": "Image caption text",
  "lazy_loading": "lazy"
}
```

This element provides comprehensive image display capabilities while maintaining performance and accessibility standards.