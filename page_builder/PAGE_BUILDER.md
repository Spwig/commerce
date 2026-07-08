# Page Builder Documentation

## Overview
The Page Builder is a drag-and-drop visual editor for creating and managing web pages. It supports modular elements, utility-based property editors, and live preview functionality.

## Architecture

### Key Components

1. **Elements**: Modular components (text, heading, button, image, container, etc.)
2. **Utilities**: Reusable property editors (color picker, gradient creator, background editor, etc.)
3. **Templates**: Django templates for rendering elements
4. **Visual Builder**: Interactive drag-and-drop interface

## Element Structure

### Element Templates
Each element type has its own directory under `/page_builder/templates/page_builder/elements/[element_type]/` containing:

- `template.html`: Main rendering template with all styling logic
- `config.json`: Element configuration and property definitions
- `visual_builder.html` (optional): Special template for visual builder if needed
- `locale/`: Translation files

### Template Requirements

#### Main Template (`template.html`)
The main template must handle ALL element styling properties:

```django
<div style="
    {% if element.content.background %}background: {{ element.content.background }};{% endif %}
    {% if element.content.text_color %}color: {{ element.content.text_color }};{% endif %}
    {# Include all other style properties #}
">
    {{ element.content.text }}
</div>
```

**Important**: The visual builder uses these templates directly, so all styling must be applied here.

### Visual Builder Integration

The visual builder partial (`/templates/page_builder/partials/visual_builder_element.html`) wraps elements with controls and renders them using their actual templates:

```django
<div class="element-wrapper" data-element-id="{{ element.id }}">
    <div class="element-controls">...</div>
    <div class="element-content">
        {% include 'page_builder/elements/'|add:element.element_type|add:'/template.html' %}
    </div>
</div>
```

**Never duplicate styling logic in the visual builder partial!**

## Utility System

### Creating New Utilities

Utilities are reusable property editors that provide advanced UI for complex properties.

#### Structure
Each utility must have:
```
/utilities/[utility_name]/
    ├── [utility_name].js      # Main JavaScript class
    ├── [utility_name].css     # Styles
    └── __init__.py           # Python module marker
```

#### JavaScript Class Requirements

```javascript
class UtilityName {
    constructor(options = {}) {
        this.options = {
            onChange: options.onChange || (() => {}),
            onApply: options.onApply || (() => {}),
            translations: options.translations || {}
        };
        // Initialize state
    }

    attach(element, value = '') {
        this.targetElement = element;

        // Get element ID for live preview
        const form = element.closest('.element-properties-form');
        this.elementId = form ? form.dataset.elementId : null;

        // Create trigger button
        this.createTrigger();
    }

    open() {
        // Create and show popup
        this.createPopup();
        this.position();
    }

    updatePreview() {
        // Update live preview in builder
        if (this.elementId && window.updateElementPreview) {
            window.updateElementPreview(this.elementId, {
                propertyName: value
            });
        }
    }

    applyValue() {
        // Save value to input
        this.targetElement.value = finalValue;

        // Trigger events for form handling
        this.targetElement.dispatchEvent(new Event('input', { bubbles: true }));
        this.targetElement.dispatchEvent(new Event('change', { bubbles: true }));

        // Update live preview
        this.updatePreview();
    }
}
```

#### Popup Design Requirements

1. **Draggable**: All utility popups must be draggable
2. **Viewport Constraints**: Prevent dragging outside viewport
3. **Z-Index Management**: Ensure popups appear above other elements
4. **Dark Mode Support**: Include dark mode styles
5. **Responsive**: Work on mobile devices

#### CSS Requirements

```css
.utility-popup {
    position: fixed;
    background: white;
    border-radius: 12px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
    z-index: 10000;
    min-width: 320px;
    max-width: 90vw;
    max-height: 90vh;
}

/* Scoped selectors to avoid conflicts */
.utility-popup .swatch {
    /* Utility-specific styles */
}

/* Dark mode */
[data-theme="dark"] .utility-popup {
    background: #1f2937;
    color: #e5e7eb;
}
```

### Registering Utilities

1. Add to property_renderer.js utility map:
```javascript
this.utilityMap = {
    'background': 'BackgroundEditor',
    // ... other utilities
};
```

2. Include in visual_builder.html:
```html
<link rel="stylesheet" href="{% static 'page_builder/utilities/[name]/[name].css' %}">
<script src="{% static 'page_builder/utilities/[name]/[name].js' %}"></script>
```

3. Reference in element's config.json:
```json
{
    "background": {
        "type": "background",
        "label": "Background",
        "utility": "background_editor"
    }
}
```

## Live Preview System

### How It Works

1. **Element ID Tracking**: Each element wrapper has `data-element-id`
2. **Property Updates**: Utilities call `window.updateElementPreview(elementId, properties)`
3. **CSS Mapping**: Properties are mapped to CSS in `visual-builder.js`

### Adding New Properties

To support a new CSS property in live preview:

1. Add to propertyMap in visual-builder.js:
```javascript
const propertyMap = {
    'background': 'background',
    'your_property': 'yourCssProperty',
    // ...
};
```

2. Ensure the template uses the property:
```django
{% if element.content.your_property %}
    your-css-property: {{ element.content.your_property }};
{% endif %}
```

## Best Practices

### DO:
- ✅ Use actual element templates in visual builder
- ✅ Keep all styling logic in element templates
- ✅ Make utilities reusable and self-contained
- ✅ Use scoped CSS selectors in utilities
- ✅ Support live preview in all utilities
- ✅ Handle both normal and hover states
- ✅ Store complex data as JSON in data attributes

### DON'T:
- ❌ Duplicate styling logic in visual builder partial
- ❌ Use global CSS classes that might conflict
- ❌ Forget to trigger input/change events
- ❌ Store complex JSON in value fields without parsing
- ❌ Forget dark mode support
- ❌ Create utilities without draggable popups

## Common Issues & Solutions

### Issue: Styles not showing in visual builder
**Solution**: Ensure the element's template.html includes all style properties

### Issue: Live preview not working
**Solution**:
1. Check element ID is retrieved correctly
2. Verify property is in propertyMap
3. Ensure updateElementPreview is called with correct format

### Issue: Utility conflicts with others
**Solution**: Use scoped CSS selectors (e.g., `.background-editor-popup .swatch`)

### Issue: Values not persisting
**Solution**:
1. Trigger input and change events
2. Store complex data in data attributes
3. Parse values correctly on load

## Development Workflow

1. **Create Element**:
   - Define config.json with properties
   - Create template.html with all styling
   - Test in visual builder

2. **Create Utility**:
   - Build JS class with standard methods
   - Add CSS with scoped selectors
   - Register in property_renderer.js
   - Include in visual_builder.html

3. **Test**:
   - Verify live preview updates
   - Check value persistence
   - Test dark mode
   - Validate mobile responsiveness

## Future Improvements

- [ ] Implement undo/redo system
- [ ] Add keyboard shortcuts
- [ ] Create preset system for utilities
- [ ] Add animation editor utility
- [ ] Implement responsive breakpoint editor
- [ ] Add CSS custom properties support