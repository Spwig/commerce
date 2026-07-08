---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 價格下跌提醒：{{ product_name }} 現在 {{ discount_percentage }}% 折扣！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 價格下跌提醒！
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          在您的願望清單商品上節省 {{ discount_percentage }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          太好了，{{ customer_name }}！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您的願望清單上的產品價格剛剛下跌！千萬不要錯過這個節省的機會。
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
              原價： <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              現在： {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              節省 {{ savings_amount }} ({{ discount_percentage }}% 折扣)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          立即購買並節省 {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>臨時限定：</strong> 這場促銷不會永遠持續下去。價格可能隨時恢復！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          從願望清單中移除： <a href="{{ remove_wishlist_url }}">點擊這裡</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 價格下跌提醒！
節省 {{ discount_percentage }}% 在您的願望清單商品上

太好了，{{ customer_name }}！

您的願望清單上的產品價格剛剛下跌！千萬不要錯過這個節省的機會。

{{ product_name }}
原價： {{ original_price }}
現在： {{ new_price }}
節省 {{ savings_amount }} ({{ discount_percentage }}% 折扣)

立即購買並節省 {{ discount_percentage }}%： {{ product_url }}

⏰ 臨時限定： 這場促銷不會永遠持續下去。價格可能隨時恢復！

從願望清單中移除： {{ remove_wishlist_url }}