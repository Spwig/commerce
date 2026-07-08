---
template_type: wishlist_reminder_weekly
category: Wishlist
---

# Email Template: wishlist_reminder_weekly

## Subject
❤️ お気に入りリストは待機中 - {{ wishlist_item_count }} 品 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ お気に入りリスト
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ customer_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          お気に入りリストに {{ wishlist_item_count }} 品{{ wishlist_item_count|pluralize }} が待機しています。ここに何が起こっているか見てみましょう:
        </mj-text>

        <mj-spacer height="30px" />

        {% if price_drops_count > 0 %}
        <mj-section background-color="#dcfce7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              🔥 {{ price_drops_count }} 価格が下がった商品{{ price_drops_count|pluralize }} 今週！
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="15px" />
        {% endif %}

        {% if back_in_stock_count > 0 %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#059669">
              ✓ {{ back_in_stock_count }} 品{{ back_in_stock_count|pluralize }} 在庫あり
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="30px" />
        {% endif %}

        {% for item in wishlist_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="25%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="75%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            {% if item.price_dropped %}
            <mj-text font-size="14px">
              <span style="text-decoration: line-through; color: #9ca3af;">{{ item.old_price }}</span>
              <span style="color: #059669; font-weight: bold;"> {{ item.new_price }}</span>
            </mj-text>
            {% else %}
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ item.price }}
            </mj-text>
            {% endif %}
            {% if not item.in_stock %}
            <mj-text font-size="13px" color="#dc2626">
              在庫切れ
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          お気に入りリストをすべて見る
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          週次のお知らせは不要ですか？ <a href="{{ unsubscribe_url }}">購読解除</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ お気に入りリスト

こんにちは {{ customer_name }}、

お気に入りリストに {{ wishlist_item_count }} 品{{ wishlist_item_count|pluralize }} が待機しています。ここに何が起こっているか見てみましょう:

{% if price_drops_count > 0 %}🔥 {{ price_drops_count }} 価格が下がった商品{{ price_drops_count|pluralize }} 今週！{% endif %}
{% if back_in_stock_count > 0 %}✓ {{ back_in_stock_count }} 品{{ back_in_stock_count|pluralize }} 在庫あり{% endif %}

お気に入りリスト:
{% for item in wishlist_items %}
- {{ item.product_name }}
  {% if item.price_dropped %}Was {{ item.old_price }}, Now {{ item.new_price }}{% else %}{{ item.price }}{% endif %}
  {% if not item.in_stock %}在庫切れ{% endif %}
{% endfor %}

お気に入りリストをすべて見る: {{ wishlist_url }}

週次のお知らせは不要ですか？ 購読解除: {{ unsubscribe_url }}
