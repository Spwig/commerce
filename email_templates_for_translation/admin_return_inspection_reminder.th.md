---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
ได้รับการคืนสินค้า - ต้องการตรวจสอบการสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ต้องการตรวจสอบการคืนสินค้า
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ได้รับแพ็กเกจคืนสินค้าแล้วและต้องการให้ตรวจสอบ
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
ต้องการตรวจสอบการคืนสินค้า

ได้รับแพ็กเกจคืนสินค้าแล้วและต้องการให้ตรวจสอบ

Order: #{{ order_number }}
Received: {{ received_at }}
Items to Inspect: {{ items_count }}

{% if admin_url %}View in admin: {{ admin_url }}{% endif %}