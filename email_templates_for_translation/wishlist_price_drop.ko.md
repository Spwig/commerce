---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 가격이 내려갔어요: {{ product_name }}은 이제 {{ discount_percentage }}% 할인 중입니다!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 가격이 내려갔어요!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          원하시는 위시리스트 항목을 {{ discount_percentage }}% 할인 중입니다.
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ customer_name }}님께 좋은 소식이에요!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          위시리스트에 있는 제품의 가격이 떨어졌어요! 이 기회를 놓치지 마세요.
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
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              기존 가격: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              현재 가격: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              할인 금액 {{ savings_amount }} ({{ discount_percentage }}% 할인)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          지금 구매하고 {{ discount_percentage }}% 할인 받기
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>한정 시간:</strong> 이 할인은 영원히 지속되지 않습니다. 언제든지 가격이 다시 올라갈 수 있습니다!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          위시리스트에서 제거: <a href="{{ remove_wishlist_url }}">여기 클릭</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 가격이 내려갔어요!
원하시는 위시리스트 항목을 {{ discount_percentage }}% 할인 중입니다

{{ customer_name }}님께 좋은 소식이에요!

위시리스트에 있는 제품의 가격이 떨어졌어요! 이 기회를 놓치지 마세요.

{{ product_name }}
기존 가격: {{ original_price }}
현재 가격: {{ new_price }}
할인 금액 {{ savings_amount }} ({{ discount_percentage }}% 할인)

지금 구매하고 {{ discount_percentage }}% 할인 받기: {{ product_url }}

⏰ 한정 시간: 이 할인은 영원히 지속되지 않습니다. 언제든지 가격이 다시 올라갈 수 있습니다!

위시리스트에서 제거: {{ remove_wishlist_url }}