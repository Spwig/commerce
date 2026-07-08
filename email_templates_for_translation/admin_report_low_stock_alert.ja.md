---
template_type: admin_report_low_stock_alert
category: Admin Reports
---

# Email Template: admin_report_low_stock_alert

## Subject
📦 在庫が少ないお知らせ - {{ product_count }} 品種を再注文する必要があります

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 在庫が少ないお知らせ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          再注文が必要です
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} 品種は再注文点を下回っています。
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>在庫:</strong> <span style="color: #dc2626;">{{ item.current_stock }}</span> / 再注文点: {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          在庫を確認する
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 LOW STOCK ALERT

再注文が必要です

{{ product_count }} 品種は再注文点を下回っています。

LOW STOCK ITEMS:
{% for item in low_stock_items %}
{{ item.product_name }}
在庫: {{ item.current_stock }} / 再注文点: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

在庫を確認する: {{ inventory_url }}