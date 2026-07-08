---
template_type: admin_report_low_stock_alert
category: Admin Reports
---

# Email Template: admin_report_low_stock_alert

## Subject
📦 تنبيه المخزون المنخفض - {{ product_count }} منتجات تحتاج إلى إعادة الطلب

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 تنبيه المخزون المنخفض
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          إجراء طلب جديد مطلوب
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} منتجات تحت مستوى إعادة الطلب.
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>المخزون:</strong> <span style="color: #dc2626;">{{ item.current_stock }}</span> / إجراء طلب جديد عند: {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض المخزون
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 تنبيه المخزون المنخفض

إجراء طلب جديد مطلوب

{{ product_count }} منتجات تحت مستوى إعادة الطلب.

منتجات المخزون المنخفض:
{% for item in low_stock_items %}
{{ item.product_name }}
المخزون: {{ item.current_stock }} / إجراء طلب جديد عند: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

عرض المخزون: {{ inventory_url }}