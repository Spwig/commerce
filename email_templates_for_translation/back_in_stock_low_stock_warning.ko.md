---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} 다시 돌아왔지만 재고가 급감하고 있습니다! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 재고 한정 - 빠르게 행동하세요!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} 다시 돌아왔습니다!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          기쁜 소식입니다! 기다리시던 상품이 다시 입고되었습니다. 하지만 서둘러 주세요 - 남은 재고가 {{ stock_remaining }} 개 입니다!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Variant: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ 재고에 {{ stock_remaining }} 개 남았습니다!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          지금 바로 구매하세요
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>이 상품은 지난 달에 {{ times_sold_out }}회{{ times_sold_out|pluralize }} 품절되었습니다!</strong><br/>
              다시 놓치지 않으려면 재고가 있는 동안 지금 주문하세요.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          더 이상 관심이 없으십니까? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">이 알림에서 구독을 해제하세요</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 재고 한정 - 빠르게 행동하세요!

{{ product_name }} 다시 돌아왔습니다!

안녕하세요 {{ customer_name }},

기쁜 소식입니다! 기다리시던 상품이 다시 입고되었습니다. 하지만 서둘러 주세요 - 남은 재고가 {{ stock_remaining }} 개 입니다!

PRODUCT:
{{ product_name }}
{{ product_description }}
Price: {{ product_price }}
{% if variant_name %}Variant: {{ variant_name }}{% endif %}

⚠️ 재고에 {{ stock_remaining }} 개 남았습니다!

Buy now before it's gone: {{ product_url }}

🔥 이 상품은 지난 달에 {{ times_sold_out }}회{{ times_sold_out|pluralize }} 품절되었습니다!
다시 놓치지 않으려면 재고가 있는 동안 지금 주문하세요.

Not interested anymore? Unsubscribe: {{ unsubscribe_url }}
