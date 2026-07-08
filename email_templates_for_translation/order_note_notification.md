---
template_type: order_note_notification
category: Core E-commerce
---

# Email Template: order_note_notification

## Subject
Update on Your Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          A message about your order
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ staff_name }} has added a note to your order <strong>#{{ order_number }}</strong>:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ note_content }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Order
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
A message about your order

Hi {{ customer_name }},

{{ staff_name }} has added a note to your order #{{ order_number }}:

---
{{ note_content }}
---

{% if order_url %}View your order: {{ order_url }}{% endif %}

Need help?
Email: {{ support_email }}
Phone: {{ support_phone }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| customer_name | Customer's name | Sarah |
| staff_name | Staff member who added the note | John from Support |
| order_number | Order identifier | ORD-12345 |
| note_content | The note text from the merchant | Your item has been gift-wrapped as requested. |
| order_url | Link to the order status page | https://shop.com/orders/ORD-12345/ |
| support_email | Support email address | support@shop.com |
| support_phone | Support phone number | 1-800-555-0123 |

## Notes

- Transactional email - sent when merchant adds a customer-visible note and opts to notify
- Only sent when both notify_customer=True and is_customer_visible=True
- Includes the full note content inline for convenience
- Links to order status page for further details
