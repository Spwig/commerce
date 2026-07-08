---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
마지막 기회! 주문이 24시간 후에 만료됩니다 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ 마지막 기회 - 24시간 후에 장바구니가 만료됩니다
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          놓치지 마세요, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          이는 최종 напоминание입니다. 주문이 24시간 후에 만료되고, 우리는 더 이상 이러한 항목을 보관할 수 없습니다.
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          총액: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          만료되기 전에 주문을 완료하세요
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          궁금한 점이 있나요? 저희 팀이 도와드릴 수 있습니다: <a href="{{ support_url }}">지원팀에 문의</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ 마지막 기회 - 24시간 후에 장바구니가 만료됩니다

놓치지 마세요, {{ customer_name }}!

이것은 최종 напоминание입니다. 주문이 24시간 후에 만료되고, 우리는 더 이상 이러한 항목을 보관할 수 없습니다.

주문 정보:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

총액: {{ cart_total }}

만료되기 전에 주문을 완료하세요: {{ cart_url }}

궁금한 점이 있나요? 저희 팀이 도와드릴 수 있습니다: {{ support_url }}

---
이것은 장바구니 #{{ cart_id }}의 최종 напоминание입니다.