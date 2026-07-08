---
template_type: back_in_stock_waitlist_confirmation
category: Stock Notifications
---

# Email Template: back_in_stock_waitlist_confirmation

## Subject
✓ {{ product_name }} के लिए आप एवेटिंग लिस्ट में हैं - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ✓ आप {{ product_name }} के लिए एवेटिंग लिस्ट में हैं!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके रजिस्टर करने के लिए धन्यवाद! हम आपको तुरंत बताएंगे जैसे ही यह उत्पाद फिर से स्टॉक में आ जाता है।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              वेरिएंट: {{ variant_name }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>अपेक्षा करें:</strong><br/>
              हम आपको तुरंत ईमेल करेंगे जैसे ही यह आइटम फिर से स्टॉक में आ जाता है। स्टॉक सीमित है, इसलिए आपको तत्काल कार्रवाई करनी चाहिए जब आपको सूचना मिलती है!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          इंतजार के दौरान...
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          इन उत्पादों की जांच करें जो अभी स्टॉक में हैं:
        </mj-text>

        {% for product in similar_products %}
        <mj-spacer height="10px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column width="25%">
            <mj-image src="{{ product.image }}" alt="{{ product.name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="75%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product.price }}
            </mj-text>
            <mj-text font-size="13px">
              <a href="{{ product.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">उत्पाद देखें →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          अपना मन बदल गए? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">इस एवेटिंग लिस्ट से अनसबस्क्राइब करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ आप एवेटिंग लिस्ट में हैं!

हेलो {{ customer_name }},

आपके रजिस्टर करने के लिए धन्यवाद! हम आपको तुरंत बताएंगे जैसे ही यह उत्पाद फिर से स्टॉक में आ जाता है।

उत्पाद:
{{ product_name }}
{{ product_description }}
मूल्य: {{ product_price }}
{% if variant_name %}वेरिएंट: {{ variant_name }}{% endif %}

💡 अपेक्षा करें:
हम आपको तुरंत ईमेल करेंगे जैसे ही यह आइटम फिर से स्टॉक में आ जाता है। स्टॉक सीमित है, इसलिए आपको तत्काल कार्रवाई करनी चाहिए जब आपको सूचना मिलती है!

इंतजार के दौरान...
इन उत्पादों की जांच करें जो अभी स्टॉक में हैं:
{% for product in similar_products %}
- {{ product.name }} - {{ product.price }}
  {{ product.url }}
{% endfor %}

अपना मन बदल गए? इस एवेटिंग लिस्ट से अनसबस्क्राइब करें: {{ unsubscribe_url }}