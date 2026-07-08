# Contact Form Element

A comprehensive, customizable contact form element with full validation, accessibility features, and complete translation support.

## Features

- **Flexible Field Configuration**: Show/hide and require different fields
- **Built-in Validation**: Client-side and server-side ready validation
- **Privacy Compliance**: Optional privacy policy and terms agreement
- **Responsive Design**: Mobile-first responsive layout
- **Accessibility**: Full ARIA support and semantic HTML
- **Translation Ready**: Complete i18n support with element-specific translations
- **Custom Styling**: Configurable appearance and layout options

## Field Options

### Basic Fields
- **First Name**: Optional, configurable as required
- **Last Name**: Optional, configurable as required  
- **Email Address**: Always required with validation
- **Phone Number**: Optional field with tel input type
- **Subject**: Optional subject line field
- **Message**: Required textarea with configurable rows

### Additional Features
- **Privacy Agreement**: Optional checkbox with customizable text and links
- **Custom Placeholders**: Translatable placeholder text for all fields
- **Success/Error Messages**: Configurable feedback messages
- **Form Action**: Custom form submission URL
- **Method Selection**: POST or GET form submission

## Configuration Properties

### Content Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `title` | string | "" | Custom form title |
| `description` | text | "" | Form description text |
| `action` | url | "" | Form submission URL |
| `method` | select | "post" | Form submission method |

### Field Visibility
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `show_first_name` | boolean | true | Show first name field |
| `show_last_name` | boolean | true | Show last name field |
| `show_phone` | boolean | false | Show phone number field |
| `show_subject` | boolean | false | Show subject field |

### Field Requirements
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `required_first_name` | boolean | false | Make first name required |
| `required_last_name` | boolean | false | Make last name required |
| `required_phone` | boolean | false | Make phone required |
| `required_subject` | boolean | false | Make subject required |

### Privacy & Legal
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `show_privacy_checkbox` | boolean | false | Show privacy agreement |
| `required_privacy` | boolean | true | Make privacy agreement required |
| `privacy_text` | text | "" | Custom privacy agreement text |
| `privacy_url` | url | "/privacy" | Privacy policy URL |
| `terms_url` | url | "/terms" | Terms of service URL |

### Customization
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `message_rows` | number | 5 | Textarea rows (3-10) |
| `submit_text` | string | "" | Custom submit button text |
| `success_message` | text | "" | Custom success message |
| `error_message` | text | "" | Custom error message |

## Translation Support

Complete translations available for:
- **English (en)**: Default language
- **Spanish (es)**: Full translation set
- **Japanese (ja)**: Full translation set
- **French (fr)**: Available
- **German (de)**: Available
- **Portuguese (pt)**: Available
- **Chinese Simplified (zh-hans)**: Available

### Translatable Content
- All field labels and placeholders
- Form title and description
- Privacy agreement text
- Success and error messages
- Button text and validation messages

## Usage Examples

### Basic Contact Form
```json
{
  "title": "Get in Touch",
  "description": "We'd love to hear from you",
  "show_phone": false,
  "show_subject": false
}
```

### Complete Business Form
```json
{
  "title": "Business Inquiry",
  "description": "Let's discuss your project",
  "show_phone": true,
  "required_phone": true,
  "show_subject": true,
  "required_subject": true,
  "show_privacy_checkbox": true,
  "message_rows": 6
}
```

### Custom Privacy Form
```json
{
  "show_privacy_checkbox": true,
  "privacy_text": "I consent to my data being processed according to your privacy policy and agree to receive communications.",
  "privacy_url": "/custom-privacy",
  "terms_url": "/custom-terms",
  "submit_text": "Submit Inquiry"
}
```

## Client-Side Validation

The form includes automatic validation for:
- Required field checking
- Email format validation
- Real-time visual feedback
- Error message display
- Accessibility announcements

## Server Integration

The form generates standard POST data:
```
first_name: "John"
last_name: "Doe"
email: "john@example.com"
phone: "+1234567890"
subject: "Business Inquiry"
message: "Hello, I'd like to discuss..."
privacy_agreement: "on"
```

## Styling

The element uses Tailwind CSS classes with custom enhancements:
- Responsive grid layout
- Focus states and transitions
- Error state styling
- Mobile-optimized spacing
- Custom form styling

## Accessibility Features

- Semantic HTML structure
- Proper label associations
- ARIA attributes where needed
- Keyboard navigation support
- Screen reader friendly
- High contrast support
- Focus management

## Browser Support

- Modern browsers (Chrome 60+, Firefox 60+, Safari 12+, Edge 79+)
- Progressive enhancement for older browsers
- Mobile browser optimization
- Touch-friendly interface

## Version History

### v1.0.0
- Initial release with complete field configuration
- Full translation support for 7 languages
- Client-side validation and accessibility
- Privacy compliance features
- Responsive design and custom styling