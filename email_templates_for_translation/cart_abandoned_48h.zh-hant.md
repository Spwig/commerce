---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
最後機會！您的購物車24小時後將過期 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ 最後機會 - 購物車24小時後過期
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          別錯過了，{{ customer_name }}！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          這是您的最後提醒。您的購物車將在24小時後過期，我們無法再保留這些商品。
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
          總計：{{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          在還來得及之前完成訂購
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          有問題嗎？我們的團隊隨時為您提供幫助： <a href="{{ support_url }}">聯繫支援</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ 最後機會 - 購物車24小時後過期

別錯過了，{{ customer_name }}！

這是您的最後提醒。您的購物車將在24小時後過期，我們無法再保留這些商品。

您的購物車：
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

總計：{{ cart_total }}

在還來得及之前完成訂購：{{ cart_url }}

有問題嗎？我們的團隊隨時為您提供幫助：{{ support_url }}

---
這是購物車 #{{ cart_id }} 的最後提醒。