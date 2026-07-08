---
template_type: admin_report_low_stock_alert
category: Admin Reports
---

# Email Template: admin_report_low_stock_alert

## Subject
📦 कम भंडार चेतावनी - {{ product_count }} उत्पाद पुन: क्रम में ले जाने की आवश्यकता है

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 कम भंडार चेतावनी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          पुन: क्रम आवश्यकता
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} उत्पाद पुन: क्रम बिंदु के नीचे है।
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>भंडार:</strong> <span style="color: #dc2626;">
                {{ item.current_stock }}
              </span> / पुन: क्रम करें: {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          स्टॉक देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 कम भंडार चेतावनी

पुन: क्रम आवश्यकता

{{ product_count }} उत्पाद पुन: क्रम बिंदु के नीचे हैं।

कम भंडार वाली वस्तुएं:
{% for item in low_stock_items %}
{{ item.product_name }}
भंडार: {{ item.current_stock }} / पुन: क्रम करें: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

स्टॉक देखें: {{ inventory_url }}