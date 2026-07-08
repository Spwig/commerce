---
template_type: wishlist_item_added_confirmation
category: Wishlist
---

# Email Template: wishlist_item_added_confirmation

## Subject
✓ {{ product_name }} 已加入您的願望清單 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ❤️ 已加入您的願望清單！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          您已成功將 {{ product_name }} 加入願望清單。我們會持續關注它！
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
              ✓ 有貨
            </mj-text>
            {% else %}
            <mj-text font-size="13px" color="#dc2626">
              ⚠️ 無貨 - 我們會在貨回來時通知您！
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>我們會通知您：</strong><br/>
              • 價格下降<br/>
              • 補貨提醒<br/>
              • 限時促銷
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ wishlist_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看願望清單
        </mj-button>

        {% if product_in_stock %}
        <mj-spacer height="10px" />
        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          立即購買
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❤️ 已加入您的願望清單！

Hi {{ customer_name }},

您已成功將 {{ product_name }} 加入願望清單。我們會持續關注它！

{{ product_name }}
Price: {{ product_price }}
{% if product_in_stock %}✓ 有貨{% else %}⚠️ 無貨 - 我們會在貨回來時通知您！{% endif %}

💡 我們會通知您：
• 價格下降
• 補貨提醒
• 限時促銷

View my wishlist: {{ wishlist_url }}
{% if product_in_stock %}Buy now: {{ product_url }}{% endif %}