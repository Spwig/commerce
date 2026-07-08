---
template_type: order_note_notification
category: Core E-commerce
---

# Email Template: order_note_notification

## Subject
Cập nhật đơn hàng #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Một thông báo về đơn hàng của bạn
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ staff_name }} đã thêm một chú thích vào đơn hàng <strong>#{{ order_number }}</strong>:
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
          Xem đơn hàng
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Một thông báo về đơn hàng của bạn

Chào {{ customer_name }},

{{ staff_name }} đã thêm một chú thích vào đơn hàng #{{ order_number }}:

---
{{ note_content }}
---

{% if order_url %}Xem đơn hàng: {{ order_url }}{% endif %}

Cần hỗ trợ?
Email: {{ support_email }}
Điện thoại: {{ support_phone }}