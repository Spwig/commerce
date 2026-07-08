---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
장바구니가 기다리고 있어요! 주문을 완료하세요 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          당신은 장바구니에 {{ cart_item_count }}개의 상품을 남겨두셨습니다
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          귀하가 구매를 완료하지 않은 것을 확인했습니다. 장바구니에 상품들이 여전히 기다리고 있습니다!
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
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          주문 완료
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          도움이 필요하신가요? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">고객 지원팀에 문의해 주세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
장바구니에 {{ cart_item_count }}개의 상품을 남겨두셨습니다

안녕하세요 {{ customer_name }},

귀하가 구매를 완료하지 않은 것을 확인했습니다. 장바구니에 상품들이 여전히 기다리고 있습니다!

YOUR CART:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

Total: {{ cart_total }}

Complete your order: {{ cart_url }}

Need help? Contact our support team: {{ support_url }}

---

이 이메일을 받은 이유는 {{ shop_name }}에서 장바구니에 상품을 추가하셨기 때문입니다.
받지 않으려면 다음 링크를 방문하세요: {{ preferences_url }}