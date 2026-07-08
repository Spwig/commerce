---
template_type: back_in_stock_waitlist_confirmation
category: Stock Notifications
---

# Email Template: back_in_stock_waitlist_confirmation

## Subject
✓ 您已加入 {{ product_name }} 的等候名單 - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ 您已加入等候名單！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          謝謝您註冊！我們會在產品重新補貨時立即通知您。
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
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              型號：{{ variant_name }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>您可以期待：</strong><br/>
              我們會在商品重新補貨時立即以電子郵件通知您。庫存有限，因此當您收到通知時請迅速行動！
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          等待期間...
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          請查看目前有庫存的類似產品：
        </mj-text>

        {% for product in similar_products %}
        <mj-spacer height="10px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column width="25%">
            <mj-image src="{{ product.image }}" alt="{{ product.name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="75%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product.price }}
            </mj-text>
            <mj-text font-size="13px">
              <a href="{{ product.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">查看產品 →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          改變主意了？<a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">取消訂閱此等候名單</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 您已加入等候名單！

Hi {{ customer_name }},

謝謝您註冊！我們會在產品重新補貨時立即通知您。

PRODUCT:
{{ product_name }}
{{ product_description }}
Price: {{ product_price }}
{% if variant_name %}型號：{{ variant_name }}{% endif %}

💡 可以期待的內容：
我們會在商品重新補貨時立即以電子郵件通知您。庫存有限，因此當您收到通知時請迅速行動！

等待期間...
請查看目前有庫存的類似產品：
{% for product in similar_products %}
- {{ product.name }} - {{ product.price }}
  {{ product.url }}
{% endfor %}

改變主意了？取消訂閱此等候名單：{{ unsubscribe_url }}