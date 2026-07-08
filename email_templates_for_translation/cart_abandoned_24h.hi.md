---
template_type: cart_abandoned_24h
category: Cart Recovery
---

# Email Template: cart_abandoned_24h

## Subject
अभी भी रुचि रखते हैं? आपका कार्ट जल्दी बंद हो जाएगा - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आपका {{ cart_item_count }} आइटम{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} अभी भी इंतजार कर रहा है
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हम आपके कार्ट को अपने लिए रख रहे हैं, लेकिन ये आइटम हमेशा नहीं रहेंगे। उनके चले जाने से पहले अपनी खरीदारी को पूरा करें!
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
            {% if item.low_stock %}
            <mj-text color="#dc2626" font-size="13px">
              ⚠️ केवल {{ item.stock_remaining }} स्टॉक में बचे हुए हैं!
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          कुल: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अब अपना ऑर्डर पूरा करें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              ✓ {{ free_shipping_threshold }} से ऊपर के ऑर्डर पर मुफ़्त शिपिंग<br/>
              ✓ 30-दिन की मनी-बैक गारंटी<br/>
              ✓ सुरक्षित चेकआउट
            </mj-text>
          </mj-column>
        </mj-section>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपका {{ cart_item_count }} आइटम{{ cart_item_count|pluralize }} {{ cart_item_count|pluralize:'is,are' }} अभी भी इंतजार कर रहा है

हेलो {{ customer_name }},

हम आपके कार्ट को अपने लिए रख रहे हैं, लेकिन ये आइटम हमेशा नहीं रहेंगे। उनके चले जाने से पहले अपनी खरीदारी को पूरा करें!

आपका कार्ट:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
  {% if item.low_stock %}⚠️ केवल {{ item.stock_remaining }} स्टॉक में बचे हुए हैं!{% endif %}
{% endfor %}

कुल: {{ cart_total }}

अब अपना ऑर्डर पूरा करें: {{ cart_url }}

हमारे साथ खरीदारी क्यों:
✓ {{ free_shipping_threshold }} से ऊपर के ऑर्डर पर मुफ़्त शिपिंग
✓ 30-दिन की मनी-बैक गारंटी
✓ सुरक्षित चेकआउट

---
अपने कार्ट रिमाइंडर रोकने के लिए जाएं: {{ preferences_url }}