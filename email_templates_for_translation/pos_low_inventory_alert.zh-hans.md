---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 库存不足提醒：{{ product_count }} 件商品在 {{ location_name }} 即将售罄

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
          库存即将不足
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} 件商品在 {{ location_name }} 即将售罄。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              提醒详情：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>仓库:</strong> {{ location_name }}<br/>
              <strong>受影响商品数量:</strong> {{ product_count }}<br/>
              <strong>检测时间:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          库存不足商品：
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>变体:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>当前库存:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>补货点:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          推荐操作：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 为库存不足的商品创建采购订单<br/>
          • 从其他仓库转移库存<br/>
          • 如有必要，更新补货点<br/>
          • 考虑调整安全库存水平
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看库存
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          创建采购订单
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 库存不足提醒

库存即将不足

{{ product_count }} 件商品在 {{ location_name }} 即将售罄。

提醒详情：
- 仓库: {{ location_name }}
- 受影响商品数量: {{ product_count }}
- 检测时间: {{ detected_at }}

库存不足商品：
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}变体: {{ item.variant_name }}{% endif %}
当前库存: {{ item.current_stock }}
补货点: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

推荐操作：
• 为库存不足的商品创建采购订单
• 从其他仓库转移库存
• 如有必要，更新补货点
• 考虑调整安全库存水平

查看库存: {{ inventory_url }}
创建采购订单: {{ purchase_orders_url }}