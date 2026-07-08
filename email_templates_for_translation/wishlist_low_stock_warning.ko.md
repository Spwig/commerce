---
template_type: wishlist_low_stock_warning
category: Wishlist
---

# Email Template: wishlist_low_stock_warning

## Subject
⚠️ 서두르세요! {{ product_name }}은/{{ product_name }}은 {{ shop_name }}에서/{{ shop_name }}에서 빠르게 판매되고 있습니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 재고 부족 경고!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          서두르세요, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          원하시는 상품이 재고가 부족합니다. 남은 수량은 {{ stock_remaining }} 개입니다 - 지금 바로 주문하세요!
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
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ 재고에 남은 수량은 {{ stock_remaining }} 개입니다!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          지금 바로 구매하세요
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 재고 부족 경고!

서두르세요, {{ customer_name }}!

원하시는 상품이 재고가 부족합니다. 남은 수량은 {{ stock_remaining }} 개입니다 - 지금 바로 주문하세요!

{{ product_name }}
가격: {{ product_price }}
⚠️ 재고에 남은 수량은 {{ stock_remaining }} 개입니다!

바로 구매하세요: {{ product_url }}