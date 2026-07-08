---
template_type: back_in_stock
category: Inventory
---

# Email Template: back_in_stock

## Subject
{{ product_name }} वापस स्टॉक में है! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.success|default:'#10b981' }}" align="center">
          अच्छी खबर!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          आपकी इच्छासूची में एक आइटम वापस स्टॉक में है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column width="40%">
        {% if product_image_url %}
        <mj-image src="{{ product_image_url }}" alt="{{ product_name }}" border-radius="8px" />
        {% else %}
        <mj-image src="{{ shop_url }}/static/img/placeholder-product.png" alt="{{ product_name }}" border-radius="8px" />
        {% endif %}
      </mj-column>
      <mj-column width="60%">
        <mj-text font-size="22px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          {{ product_name }}
        </mj-text>
        {% if variant_name %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-bottom="12px">
          {{ variant_name }}
        </mj-text>
        {% endif %}
        <mj-text font-size="16px" color="{{ theme.color.success|default:'#10b981' }}" font-weight="600" padding-bottom="16px">
          <span style="display: inline-flex; align-items: center;">
            <span style="width: 8px; height: 8px; background-color: {{ theme.color.success|default:'#10b981' }}; border-radius: 50%; margin-right: 8px; display: inline-block;"></span>
            स्टॉक में है
          </span>
        </mj-text>
        <mj-button href="{{ product_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 28px">
          अब खरीदें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Urgency Message -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="15px 20px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e" align="center">
          <strong>अपना अवसर न छोड़ें!</strong> लोकप्रिय आइटम जल्दी बिकते हैं - इसे फिर से गायब होने से पहले अपना लें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Browse More -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          हमारे नवीनतम उत्पादों की खोज जारी रखें
        </mj-text>
        <mj-button href="{{ shop_url }}" background-color="transparent" color="{{ theme.color.info|default:'#3b82f6' }}" font-size="14px" border="1px solid {{ theme.color.info|default:'#3b82f6' }}" border-radius="6px" padding="12px 24px">
          हमारे स्टोर पर जाएं
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Unsubscribe Note -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="11px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" line-height="1.5">
          आप इस उत्पाद के उपलब्ध होने के बारे में सूचना प्राप्त करने के लिए रजिस्टर किए गए थे।
          यह एक बार की सूचना है - आप इस उत्पाद के बारे में अधिक ईमेल नहीं प्राप्त करेंगे।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          सहायता की आवश्यकता है? हमसे संपर्क करें: {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Spwig द्वारा संचालित
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
अच्छी खबर! {{ product_name }} वापस स्टॉक में है!

आपने हमें इस आइटम के उपलब्ध होने के बारे में सूचना प्राप्त करने के लिए कहा था, और हम आपको बताने के लिए खुश हैं कि अब यह स्टॉक में है।

उत्पाद विवरण:
{{ product_name }}{% if variant_name %}
वेरिएंट: {{ variant_name }}{% endif %}

स्थिति: स्टॉक में है

अब खरीदें:
{{ product_url }}

अपना अवसर न छोड़ें! लोकप्रिय आइटम जल्दी बिकते हैं - इसे फिर से गायब होने से पहले अपना लें।

---

हमारे नवीनतम उत्पादों की खोज जारी रखें:
{{ shop_url }}

---

आप इस उत्पाद के उपलब्ध होने के बारे में सूचना प्राप्त करने के लिए रजिस्टर किए गए थे।
यह एक बार की सूचना है - आप इस उत्पाद के बारे में अधिक ईमेल नहीं प्राप्त करेंगे।

सहायता की आवश्यकता है? हमसे संपर्क करें: {{ support_email }}

---
Spwig द्वारा संचालित - https://spwig.com