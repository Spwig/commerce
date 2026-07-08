---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
Return Received - Inspection Required for Order #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Return Inspection Required
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          A return package has been received and requires inspection.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Order:</strong> #{{ order_number }}<br/>
              <strong>Received:</strong> {{ received_at }}<br/>
              <strong>Items to Inspect:</strong> {{ items_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if admin_url %}
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          View Return in Admin
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Return Inspection Required

A return package has been received and requires inspection.

Order: #{{ order_number }}
Received: {{ received_at }}
Items to Inspect: {{ items_count }}

{% if admin_url %}View in admin: {{ admin_url }}{% endif %}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| order_number | Order identifier | ORD-12345 |
| received_at | Formatted datetime when package was received | March 17, 2026 |
| items_count | Number of items in the return | 3 |
| admin_url | Direct link to the ReturnRequest admin change page | https://shop.com/en/admin/orders/returnrequest/42/change/ |

## Notes

- Admin notification - sent to all active staff members when a return is marked as received
- Not customer-facing, uses enable_tracking=False
- Links directly to the admin change page for the return request
