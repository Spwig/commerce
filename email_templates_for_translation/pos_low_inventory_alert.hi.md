---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 कम स्टॉक चेतावनी: {{ product_count }} उत्पाद {{ product_count|pluralize }} {{ location_name }} पर कम हो रहे हैं

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 कम स्टॉक चेतावनी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          स्टॉक कम हो रहा है
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ product_count }} उत्पाद {{ product_count|pluralize }} {{ product_count|pluralize:'is,are' }} {{ location_name }} पर कम हो रहे हैं।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              चेतावनी के विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>स्थान:</strong> {{ location_name }}<br/>
              <strong>प्रभावित उत्पाद:</strong> {{ product_count }}<br/>
              <strong>अनुमानित:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          कम स्टॉक वाली वस्तुएं:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>वेरिएंट:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>वर्तमान स्टॉक:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>पुनः आदेश बिंदु:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सुझाए गए कार्रवाई:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • कम स्टॉक वाले उत्पादों के लिए खरीदारी के आदेश बनाएं<br/>
          • अन्य स्थानों से स्टॉक का स्थानांतरण करें<br/>
          • यदि आवश्यक हो तो पुनः आदेश बिंदु अपडेट करें<br/>
          • पैर स्तर के समायोजन की आवश्यकता हो सकती है
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          स्टॉक देखें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          खरीदारी के आदेश बनाएं
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 कम स्टॉक चेतावनी

स्टॉक कम हो रहा है

{{ product_count }} उत्पाद {{ product_count|pluralize }} {{ location_name }} पर कम हो रहे हैं।

चेतावनी के विवरण:
- स्थान: {{ location_name }}
- प्रभावित उत्पाद: {{ product_count }}
- अनुमानित: {{ detected_at }}

कम स्टॉक वाली वस्तुएं:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}वेरिएंट: {{ item.variant_name }}{% endif %}
वर्तमान स्टॉक: {{ item.current_stock }}
पुनः आदेश बिंदु: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

सुझाए गए कार्रवाई:
• कम स्टॉक वाले उत्पदों के लिए खरीदारी के आदेश बनाएं
• अन्य स्थानों से स्टॉक का स्थानांतरण करें
• यदि आवश्यक हो तो पुनः आदेश बिंदु अपडेट करें
• पैर स्तर के समायोजन की आवश्यकता हो सकती है

स्टॉक देखें: {{ inventory_url }}
खरीदारी के आदेश बनाएं: {{ purchase_orders_url }}