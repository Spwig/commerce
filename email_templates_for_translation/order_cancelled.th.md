---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
คำสั่งซื้อของคุณ #{{ order_number }} ถูกยกเลิกแล้ว

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          คำสั่งซื้อถูกยกเลิก
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          คำสั่งซื้อของคุณ <strong>#{{ order_number }}</strong> ถูกยกเลิกแล้ว。
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>เหตุผล:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          หากมีการชำระเงินแล้ว การคืนเงินจะถูกดำเนินการตามวิธีการชำระเงินเดิม
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูรายละเอียดคำสั่งซื้อ
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
คำสั่งซื้อถูกยกเลิก

สวัสดี {{ customer_name }},

คำสั่งซื้อ #{{ order_number }} ถูกยกเลิกแล้ว。

{% if cancellation_reason %}เหตุผล: {{ cancellation_reason }}{% endif %}

หากมีการชำระเงินแล้ว การคืนเงินจะถูกดำเนินการตามวิธีการชำระเงินเดิม

{% if order_url %}ดูรายละเอียดคำสั่งซื้อ: {{ order_url }}{% endif %}

มีคำถามเกี่ยวกับการยกเลิกนี้?
อีเมล: {{ support_email }}
โทรศัพท์: {{ support_phone }}