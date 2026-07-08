---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
आपका कार्ट इंतजार कर रह है! अपना ऑर्डर पूरा करे - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आपने कार्ट में {{ cart_item_count }} आइटम{{ cart_item_count|pluralize }} छोड़ दिया है
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हमने देखा कि आपने अपनी खरीदारी को पूरा नहीं किया। आपके आइटम अभी भी अपने कार्ट में इंतजार कर रह हैं!
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
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          Total: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपना ऑर्डर पूरा करे
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          सहायता की आवश्यकता है? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">हमारी समर्थन टीम से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपने कार्ट में {{ cart_item_count }} आइटम{{ cart_item_count|pluralize }} छोड़ दिया है

हेलो {{ customer_name }},

हमने देखा कि आपने अपनी खरीदारी को पूरा नहीं किया। आपके आइटम अभी भी अपने कार्ट में इंतजार कर रह हैं!

आपका कार्ट:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

Total: {{ cart_total }}

अपना ऑर्डर पूरा करे: {{ cart_url }}

सहायता की आवश्यकता है? हमारी समर्थन टीम से संपर्क करें: {{ support_url }}

---
आप इस ईमेल को प्राप्त कर रह हैं क्योंकि आपने {{ shop_name }} में आइटम कार्ट में जोड़े।
अपने कार्ट रिमाइंडर प्राप्त करने से रोकने के लिए, जाएं: {{ preferences_url }}