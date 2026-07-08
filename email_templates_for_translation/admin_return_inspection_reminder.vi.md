---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
Đã nhận lại hàng - Yêu cầu kiểm tra đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Yêu cầu kiểm tra hàng trả lại
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Một gói hàng trả lại đã được nhận và cần được kiểm tra.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Đơn hàng:</strong> #{{ order_number }}<br/>
              <strong>Ngày nhận:</strong> {{ received_at }}<br/>
              <strong>Số mặt hàng cần kiểm tra:</strong> {{ items_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if admin_url %}
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem đơn hàng trong phần quản trị
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Yêu cầu kiểm tra hàng trả lại

Một gói hàng trả lại đã được nhận và cần được kiểm tra.

Đơn hàng: #{{ order_number }}
Ngày nhận: {{ received_at }}
Số mặt hàng cần kiểm tra: {{ items_count }}

{% if admin_url %}Xem trong phần quản trị: {{ admin_url }}{% endif %}