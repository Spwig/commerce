---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
이용하실래요? 장바구니가 곧 만료됩니다 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          장바구니에 있는 {{ cart_item_count }}개의 상품이 여전히 기다리고 있습니다
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요, {{ customer_name }}님,
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          고객님의 장바구니를 잡고 있지만, 이 상품들은 영원히 남아 있지 않습니다. 상품이 사라지기 전에 구매를 완료해주세요!
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
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ 재고에 남은 수량 {{ item.stock_remaining }}개만 남았습니다!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          총액: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          지금 바로 주문 완료
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ {{ free_shipping_threshold }} 이상 주문 시 무료배송<br/>
              ✓ 30일 환불 보장<br/>
              ✓ 보안 결제
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
장바구니에 있는 {{ cart_item_count }}개의 상품이 여전히 기다리고 있습니다

안녕하세요, {{ customer_name }}님,

고객님의 장바구니를 잡고 있지만, 이 상품들은 영원히 남아 있지 않습니다. 상품이 사라지기 전에 구매를 완료해주세요!

YOUR CART:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ 재고에 남은 수량 {{ item.stock_remaining }}개만 남았습니다!{% endif %}
{% endfor %}

총액: {{ cart_total }}

Complete your order now: {{ cart_url }}

WHY SHOP WITH US:
✓ {{ free_shipping_threshold }} 이상 주문 시 무료배송
✓ 30일 환불 보장
✓ 보안 결제

---
To stop receiving cart reminders, visit: {{ preferences_url }}