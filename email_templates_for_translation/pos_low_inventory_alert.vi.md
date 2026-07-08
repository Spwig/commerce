---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 Cảnh báo tồn kho thấp: {{ product_count }} sản phẩm{{ product_count|pluralize }} đang cạn kiệt tại {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 Cảnh báo tồn kho thấp
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tồn kho đang cạn kiệt
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} sản phẩm{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} đang cạn kiệt tại {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết cảnh báo:
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
          Các mặt hàng tồn kho thấp:
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
          Các hành động được đề xuất:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Tạo các đơn đặt hàng mua hàng cho các mặt hàng tồn kho thấp<br/>
          • Chuyển tồn kho từ các địa điểm khác<br/>
          • Cập nhật điểm đặt hàng nếu cần<br/>
          • Xem xét điều chỉnh mức tồn kho tối thiểu
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem tồn kho
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Tạo đơn đặt hàng mua hàng
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 CẢNH BÁO TỒN KHO THẤP

Tồn kho đang cạn kiệt

{{ product_count }} sản phẩm{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} đang cạn kiệt tại {{ location_name }}.

CHI TIẾT CẢNH BÁO:
- Location: {{ location_name }}
- Products Affected: {{ product_count }}
- Detected: {{ detected_at }}

CÁC MẶT HÀNG TỒN KHO THẤP:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Variant: {{ item.variant_name }}{% endif %}
Current Stock: {{ item.current_stock }}
Reorder Point: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

CÁC HÀNH ĐỘNG ĐƯỢC ĐỀ NGHỊ:
• Tạo các đơn đặt hàng mua hàng cho các mặt hàng tồn kho thấp
• Chuyển tồn kho từ các địa điểm khác
• Cập nhật điểm đặt hàng nếu cần
• Xem xét điều chỉnh mức tồn kho tối thiểu

Xem tồn kho: {{ inventory_url }}
Tạo đơn đặt hàng mua hàng: {{ purchase_orders_url }}