---
slug: custom-fields
title_i18n_key: Custom Fields
category: store-config
component: custom_fields
keywords: [custom fields, extra fields, metadata, custom attributes, extend, product fields, order fields, category fields, customer fields, API]
url_patterns: ["/admin/custom-fields/"]
published: true
related: [add-product, store-settings]
---

Custom fields let you add extra data to Products, Categories, Orders, and Customer Profiles without modifying any code. Use them to store business-specific information such as external API IDs, warehouse locations, compliance data, or any attribute your store needs.

## Accessing Custom Fields

Navigate to **Settings > Custom Fields** in the admin sidebar.

![Custom Fields page](/static/core/admin/img/help/custom-fields/custom-fields-page.webp)

## Key Concepts

### Field Groups

Fields are organized into **groups** — logical collections that appear together as a section. For example, a "Shipping Info" group might contain fields for warehouse location, package dimensions, and hazmat classification.

### Field Definitions

Each field definition controls:
- **Name**: The label shown in forms
- **Slug**: The machine-readable key used in JSON storage and API responses
- **Field Type**: What kind of input is rendered (text, number, dropdown, etc.)
- **Validation**: Rules like min/max, max length, regex, or allowed choices
- **Visibility**: Whether the field appears on the storefront

### Supported Field Types

| Type | Description | Example Use |
|------|-------------|-------------|
| **Text** | Single-line text input | External API ID, brand code |
| **Textarea** | Multi-line text | Special handling notes |
| **Number** | Integer values | Minimum order quantity |
| **Decimal** | Decimal values | Weight override, custom dimension |
| **Yes/No** | Checkbox toggle | Is fragile, requires signature |
| **Date** | Date picker | Release date, expiry date |
| **Date & Time** | Date and time picker | Scheduled availability |
| **URL** | Web address | Supplier link, spec sheet URL |
| **Email** | Email address | Manufacturer contact |
| **Dropdown** | Single-select list | Material type, origin country |
| **Multi-select** | Multiple-select list | Certifications, tags |
| **Color** | Color picker | Brand color, label color |

## Managing Custom Fields

### Creating a Field Group

1. Open **Settings > Custom Fields**
2. Select the model tab (Products, Categories, Orders, or Customer Profiles)
3. Click **Add Group**
4. Enter a **Group Name** (e.g., "External Integrations")
5. Optionally enable **Show on storefront** if customers should see these fields
6. Click **Save Group**

### Adding a Field to a Group

1. On the group card, click **Add Field**
2. Enter a **Field Name** — the slug is generated automatically
3. Choose the **Field Type**
4. Optionally set a **Help Text** and **Default Value**
5. Configure validation options (varies by field type):
   - Text: max length, regex pattern
   - Number/Decimal: min and max values
   - Dropdown: define the list of choices
6. Set field options:
   - **Required**: Merchants must fill this field when saving
   - **Show on storefront**: Display value on the customer-facing page
   - **Translatable**: Allow the value to be translated (text/textarea only)
7. Click **Save Field**

### Editing and Reordering

- Click the **pencil icon** on any group or field to edit it
- Drag the **grip handle** to reorder groups or fields within a group
- Changes take effect immediately on all relevant forms

### Deleting Groups and Fields

- Click the **trash icon** on a group or field to delete it
- Deletions are **soft deletes** — the data is preserved in the database but hidden from forms
- This protects existing data from accidental loss

## Using Custom Fields in Forms

Once you define custom fields for a model, a **Custom Fields** tab appears automatically on the corresponding edit form.

### Products and Categories

1. Open any product or category for editing
2. Click the **Custom Fields** tab
3. Fill in the fields as needed
4. Click **Save** — values are stored alongside the record

### Orders

Custom field values for orders are displayed as a **read-only section** on the order detail page. Order custom fields are typically set via the API or at checkout.

### Customer Profiles

1. Open a customer profile
2. Click the **Custom Fields** tab
3. Fill in the fields and save

## API Access

### Listing Field Definitions

Retrieve all custom field definitions for a model:

```
GET /api/custom-fields/definitions/?model=product&app=catalog
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "External API ID",
    "slug": "external_api_id",
    "field_type": "text",
    "is_required": false,
    "group": { "name": "External Integrations" }
  }
]
```

### Reading Custom Field Values

Custom field values are included in the `custom_fields` JSON object on model API responses:

```json
{
  "id": 42,
  "name": "Blue Widget",
  "custom_fields": {
    "external_api_id": "API-12345",
    "is_fragile": true
  }
}
```

### Writing Custom Field Values

Include `custom_fields` when creating or updating a record via the API:

```json
{
  "custom_fields": {
    "external_api_id": "API-67890",
    "warehouse_location": "WH-A3"
  }
}
```

Values are validated against the field definitions. Invalid values return a `400` error with details.

### Querying by Custom Fields

Custom fields are indexed for fast database queries. Filter records using database query filters:

```
GET /api/products/?custom_fields__warehouse_location=WH-A3
```

## Storefront Display

### For Theme Developers

Use the `render_custom_fields` template tag to display custom fields on the storefront:

```python
{% load custom_fields_tags %}

{# Render all storefront-visible fields #}
{% render_custom_fields product %}

{# Get a specific field value #}
{% get_custom_field product "warehouse_location" as location %}
<p>Ships from: {{ location }}</p>
```

Only fields with **Show on storefront** enabled on both the group and field level will be rendered.

## Best Practices

- **Use descriptive names** — field names appear in forms and on the storefront
- **Set help text** — guide merchants on what to enter in each field
- **Group related fields** — keep forms organized and intuitive
- **Use defaults** — set sensible defaults to reduce data entry
- **Be selective with storefront visibility** — only show fields that are meaningful to customers
- **Use slugs in integrations** — slugs are stable identifiers; field names can change

## Troubleshooting

**Custom Fields tab not appearing:**
- Verify that at least one active field group exists for that model
- Check that the admin class includes the `CustomFieldsAdminMixin`
- Clear the cache and refresh the page

**Field values not saving:**
- Ensure required fields are filled in
- Check validation rules (min/max, regex patterns, allowed choices)
- Verify the field is active and not soft-deleted

**API returning empty custom_fields:**
- Confirm the model has the `CustomFieldsMixin`
- Check that field definitions exist for the correct content type
- Ensure the serializer includes `CustomFieldsSerializerMixin`

## Related Topics

- [Adding Products](#)
- [Store Settings](#)
