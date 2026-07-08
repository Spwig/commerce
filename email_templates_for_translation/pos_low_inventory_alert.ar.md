---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 تنبيه المخزون المنخفض: {{ product_count }} منتج{{ product_count|pluralize }} ينخفض في {{ location_name }}

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
          المخزون ينخفض
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} منتج{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} ينخفض في {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              تفاصيل التنبيه:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الموقع:</strong> {{ location_name }}<br/>
              <strong>المنتجات المتأثرة:</strong> {{ product_count }}<br/>
              <strong>تم الكشف في:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          عناصر المخزون المنخفض:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>النسخة:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>المخزون الحالي:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>نقطة إعادة الطلب:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإجراءات المقترحة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • إنشاء أوامر شراء لعناصر المخزون المنخفض<br/>
          • نقل المخزون من مواقع أخرى<br/>
          • تحديث نقاط إعادة الطلب إذا لزم الأمر<br/>
          • النظر في تعديل مستويات المخزون
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض المخزون
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          إنشاء أمر شراء
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 تنبيه المخزون المنخفض

المخزون ينخفض

{{ product_count }} منتج{{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} ينخفض في {{ location_name }}.

تفاصيل التنبيه:
- الموقع: {{ location_name }}
- المنتجات المتأثرة: {{ product_count }}
- تم الكشف في: {{ detected_at }}

عناصر المخزون المنخفض:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}النسخة: {{ item.variant_name }}{% endif %}
المخزون الحالي: {{ item.current_stock }}
نقطة إعادة الطلب: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

إجراءات موصى بها:
• إنشاء أوامر شراء لعناصر المخزون المنخفض
• نقل المخزون من مواقع أخرى
• تحديث نقاط إعادة الطلب إذا لزم الأمر
• النظر في تعديل مستويات المخزون

عرض المخزون: {{ inventory_url }}
إنشاء أمر شراء: {{ purchase_orders_url }}