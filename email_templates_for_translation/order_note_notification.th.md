---
template_type: order_note_notification
category: Core E-commerce
---

# Email Template: order_note_notification

## Subject
อัปเดตเกี่ยวกับคำสั่งซื้อของคุณ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อความเกี่ยวกับคำสั่งซื้อของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ staff_name }} ได้เพิ่มหมายเหตุในคำสั่งซื้อของคุณ <strong>#{{ order_number }}</strong>:
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
          ดูคำสั่งซื้อ
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ข้อความเกี่ยวกับคำสั่งซื้อของคุณ

สวัสดี {{ customer_name }},

{{ staff_name }} ได้เพิ่มหมายเหตุในคำสั่งซื้อของคุณ #{{ order_number }}:

---
{{ note_content }}
---

{% if order_url %}ดูคำสั่งซื้อของคุณ: {{ order_url }}{% endif %}

ต้องการความช่วยเหลือ?
อีเมล: {{ support_email }}
โทรศัพท์: {{ support_phone }}