---
template_type: admin_report_low_stock_alert
category: Admin Reports
---

# Email Template: admin_report_low_stock_alert

## Subject
📦 库存不足提醒 - 需要重新订购 {{ product_count }} 件商品

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 库存不足提醒
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          需要重新订购
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} 件商品低于重新订购点。
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>库存:</strong> <span style="color: #dc2626;">{{ item.current_stock }}</span> / 重新订购点: {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看库存
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 库存不足提醒

需要重新订购

{{ product_count }} 件商品低于重新订购点。

低库存商品：
{% for item in low_stock_items %}
{{ item.product_name }}
库存：{{ item.current_stock }} / 重新订购点：{{ item.reorder_point }}
SKU：{{ item.sku }}

{% endfor %}

查看库存：{{ inventory_url }}