---
template_type: wishlist_reminder_weekly
category: Wishlist
---

# Email Template: wishlist_reminder_weekly

## Subject
您的心愿单在等待 - {{ wishlist_item_count }} 件商品 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ 您的心愿单
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您有 {{ wishlist_item_count }} 件商品在心愿单中等待。这里有一些更新：
        </mj-text>

        <mj-spacer height="30px" />

        {% if price_drops_count > 0 %}
        <mj-section background-color="#dcfce7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              🔥 {{ price_drops_count }} 本周价格下降 {{ price_drops_count|pluralize }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="15px" />
        {% endif %}

        {% if back_in_stock_count > 0 %}
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#059669">
              ✓ {{ back_in_stock_count }} 件商品已重新上架
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
              Out of Stock
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看完整心愿单
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          不想接收每周提醒？<a href="{{ unsubscribe_url }}">退订</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ 您的心愿单

Hi {{ customer_name }},

您有 {{ wishlist_item_count }} 件商品在心愿单中等待。这里有一些更新：

{% if price_drops_count > 0 %}🔥 {{ price_drops_count }} 本周价格下降 {{ price_drops_count|pluralize }}{% endif %}
{% if back_in_stock_count > 0 %}✓ {{ back_in_stock_count }} 件商品已重新上架{% endif %}

YOUR WISHLIST:
{% for item in wishlist_items %}
- {{ item.product_name }}
  {% if item.price_dropped %}原价 {{ item.old_price }}，现价 {{ item.new_price }}{% else %}{{ item.price }}{% endif %}
  {% if not item.in_stock %}已售罄{% endif %}
{% endfor %}

查看完整心愿单：{{ wishlist_url }}

不想接收每周提醒？退订：{{ unsubscribe_url }}