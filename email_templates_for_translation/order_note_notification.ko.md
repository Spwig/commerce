---
template_type: order_note_notification
category: Core E-commerce
---

# Email Template: order_note_notification

## Subject
주문 #{{ order_number }}에 대한 업데이트

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          주문에 대한 메시지
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }}",
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ staff_name }}이(가) 주문 <strong>#{{ order_number }}</strong>에 메모를 추가했습니다:
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
          주문 보기
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
주문에 대한 메시지

안녕하세요, {{ customer_name }},

{{ staff_name }}이(가) 주문 #{{ order_number }}에 메모를 추가했습니다:
---
{{ note_content }}
---

{% if order_url %}주문 보기: {{ order_url }}{% endif %}

도움이 필요하신가요?
이메일: {{ support_email }}
전화: {{ support_phone }}