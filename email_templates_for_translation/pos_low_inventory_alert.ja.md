---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 在庫不足警告: {{ product_count }} 品種 {{ product_count|pluralize }} が {{ location_name }} で不足しています

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 在庫不足警告
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          在庫が不足しています
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} 品種 {{ product_count|pluralize:'is,are' }} が {{ location_name }} で不足しています。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              警告の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Location:</strong> {{ location_name }}<br/>
              <strong>Products Affected:</strong> {{ product_count }}<br/>
              <strong>Detected:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          在庫不足品:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Variant:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>Current Stock:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>Reorder Point:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          推奨アクション:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • 在庫不足品の購入注文を作成してください<br/>
          • 他の在庫場所から在庫を移動してください<br/>
          • 必要に応じて再注文ポイントを更新してください<br/>
          • パラメータレベルの調整を検討してください
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          在庫を確認する
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          購入注文を作成する
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 在庫不足警告

在庫が不足しています

{{ product_count }} 品種 {{ product_count|pluralize:'is,are' }} が {{ location_name }} で不足しています。

ALERT DETAILS:
- Location: {{ location_name }}
- Products Affected: {{ product_count }}
- Detected: {{ detected_at }}

LOW STOCK ITEMS:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variant: {{ item.variant_name }}{% endif %}
Current Stock: {{ item.current_stock }}
Reorder Point: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

RECOMMENDED ACTIONS:
• 在庫不足品の購入注文を作成してください
• 他の在庫場所から在庫を移動してください
• 必要に応じて再注文ポイントを更新してください
• パラメータレベルの調整を検討してください

View inventory: {{ inventory_url }}
Create purchase order: {{ purchase_orders_url }}