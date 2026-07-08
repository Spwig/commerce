---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 价格下调提醒：{{ product_name }} 现在 {{ discount_percentage }}% 折扣！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 价格下调提醒！
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          您心愿单中的商品立减 {{ discount_percentage }}% 
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          好消息，{{ customer_name }}！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您心愿单中的一个商品价格刚刚下调了！不要错过这次节省的机会。
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
              原价： <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              现价： {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              节省 {{ savings_amount }} ({{ discount_percentage }}% 折扣)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          立即购买并节省 {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>限时：</strong> 这次促销不会持续太久。价格随时可能回升！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          从心愿单中移除： <a href="{{ remove_wishlist_url }}">点击此处</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 价格下调提醒！
节省 {{ discount_percentage }}% 您的心愿单商品

好消息，{{ customer_name }}！

您心愿单中的一个商品价格刚刚下调了！不要错过这次节省的机会。

{{ product_name }}
原价： {{ original_price }}
现价： {{ new_price }}
节省 {{ savings_amount }} ({{ discount_percentage }}% 折扣)

立即购买并节省 {{ discount_percentage }}%： {{ product_url }}

⏰ 限时：这次促销不会持续太久。价格随时可能回升！

从心愿单中移除： {{ remove_wishlist_url }}