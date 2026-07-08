---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
仍然感興趣嗎？您的購物車即將過期 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          您的 {{ cart_item_count }} 項 {{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} 仍在等待
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我們為您保留了購物車，但這些商品不會永遠保留。在它們消失之前完成購買！
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
              ⚠️ 僅剩 {{ item.stock_remaining }} 個庫存！
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          總計: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          立即完成訂購
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ {{ free_shipping_threshold }} 以上訂單免運費<br/>
              ✓ 30 天無條件退貨保證<br/>
              ✓ 安全結帳
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您的 {{ cart_item_count }} 項 {{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} 仍在等待

Hi {{ customer_name }},

我們為您保留了購物車，但這些商品不會永遠保留。在它們消失之前完成購買！

您的購物車：
{% for item in cart_items %}
- {{ item.product_name }}
  數量：{{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ 僅剩 {{ item.stock_remaining }} 個庫存！{% endif %}
{% endfor %}

總計：{{ cart_total }}

立即完成訂購：{{ cart_url }}

為何選擇我們：
✓ {{ free_shipping_threshold }} 以上訂單免運費
✓ 30 天無條件退貨保證
✓ 安全結帳

---

要停止接收購物車提醒，請訪問：{{ preferences_url }}