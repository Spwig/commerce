---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
まだご購入をお考えですか？カートは近日中に期限切れになります - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご注文の {{ cart_item_count }} 品目 {{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} まだお待ちしています
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ご注文のカートを保持していますが、これらの商品は永遠に続きません。在庫がなくなる前に購入を完了してください！
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
              数量: {{ item.quantity }} × {{ item.price }}
            </mj-text>
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ 在庫に {{ item.stock_remaining }} 品目残っています！
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          合計: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          注文を今すぐ完了
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ {{ free_shipping_threshold }} を超える注文で送料無料<br/>
              ✓ 30日間返品保証<br/>
              ✓ セキュアなチェックアウト
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ご注文の {{ cart_item_count }} 品目 {{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} まだお待ちしています

こんにちは {{ customer_name }}、

ご注文のカートを保持していますが、これらの商品は永遠に続きません。在庫がなくなる前に購入を完了してください！

YOUR CART:
{% for item in cart_items %}
- {{ item.product_name }}
  数量: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ 在庫に {{ item.stock_remaining }} 品目残っています！{% endif %}
{% endfor %}

合計: {{ cart_total }}

Complete your order now: {{ cart_url }}

WHY SHOP WITH US:
✓ {{ free_shipping_threshold }} を超える注文で送料無料
✓ 30日間返品保証
✓ セキュアなチェックアウト

---
To stop receiving cart reminders, visit: {{ preferences_url }}