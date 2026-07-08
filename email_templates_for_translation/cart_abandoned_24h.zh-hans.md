---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
仍有兴趣？你的购物车即将过期 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          你的 {{ cart_item_count }} 件商品 {{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} 仍在等待
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我们正在为你保留购物车，但这些商品不会永远保留。在它们消失之前完成购买！
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
              数量：{{ item.quantity }} × {{ item.price }}
            </mj-text>
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ 仅剩 {{ item.stock_remaining }} 件库存！
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          总计：{{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          现在完成订单
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ 在 {{ free_shipping_threshold }} 以上订单免费送货<br/>
              ✓ 30 天无理由退货保证<br/>
              ✓ 安全结账
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
你的 {{ cart_item_count }} 件商品 {{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} 仍在等待

你好 {{ customer_name }}，

我们正在为你保留购物车，但这些商品不会永远保留。在它们消失之前完成购买！

你的购物车：
{% for item in cart_items %}
- {{ item.product_name }}
  数量：{{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ 仅剩 {{ item.stock_remaining }} 件！{% endif %}
{% endfor %}

总计：{{ cart_total }}

现在完成订单：{{ cart_url }}

为什么选择我们：
✓ 在 {{ free_shipping_threshold }} 以上订单免费送货
✓ 30 天无理由退货保证
✓ 安全结账

---
要停止接收购物车提醒，请访问：{{ preferences_url }}