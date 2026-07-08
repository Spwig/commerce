---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} がお気に入りリストに追加されました - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ お気に入りリストに追加されました！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_name }} をお気に入りリストに成功裏に追加しました。代わりに監視します！
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
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if product_in_stock %}
            <mj-text font-size="13px" color="#059669">
              ✓ 在庫あり
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ 在庫切れ - 戻ってきたら通知します！
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>通知する内容：</strong><br/>
              • 価格の下落<br/>
              • 在庫復活通知<br/>
              • 限定セール
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          お気に入りリストを確認
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          今すぐ購入
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ お気に入りリストに追加されました！

こんにちは {{ customer_name }}、

{{ product_name }} をお気に入りリストに成功裏に追加しました。代わりに監視します！

{{ product_name }}
Price: {{ product_price }}
{% if product_in_stock %}✓ 在庫あり{% else %}⚠️ 在庫切れ - 戻ってきたら通知します！{% endif %}

💡 通知する内容：
• 価格の下落
• 在庫復活通知
• 限定セール

View my wishlist: {{ wishlist_url }}
{% if product_in_stock %}Buy now: {{ product_url }}{% endif %}