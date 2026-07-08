---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 數量不足提醒：{{ product_count }} 個產品 {{ product_count|pluralize }} 在 {{ location_name }} 即將售罄

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 數量不足提醒
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          數量即將不足
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} 個產品 {{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} 在 {{ location_name }} 即將售罄。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              提醒細節：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>位置：</strong> {{ location_name }}<br/>
              <strong>受影響產品數量：</strong> {{ product_count }}<br/>
              <strong>檢測時間：</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          數量不足產品：
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>變體：</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>現有庫存：</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>補貨點：</strong> {{ item.reorder_point }}<br/>
              <strong>SKU：</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          建議措施：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 建立低庫存產品的採購單<br/>
          • 從其他倉庫調撥庫存<br/>
          • 如有必要，更新補貨點<br/>
          • 考慮調整安全庫存量
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看庫存
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          建立採購單
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 數量不足提醒

數量即將不足

{{ product_count }} 個產品 {{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} 在 {{ location_name }} 即將售罄。

提醒細節：
- 位置：{{ location_name }}
- 受影響產品數量：{{ product_count }}
- 檢測時間：{{ detected_at }}

數量不足產品：
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}變體：{{ item.variant_name }}{% endif %}
現有庫存：{{ item.current_stock }}
補貨點：{{ item.reorder_point }}
SKU：{{ item.sku }}

{% endfor %}

建議措施：
• 建立低庫存產品的採購單
• 從其他倉庫調撥庫存
• 如有必要，更新補貨點
• 考慮調整安全庫存量

查看庫存：{{ inventory_url }}
建立採購單：{{ purchase_orders_url }}