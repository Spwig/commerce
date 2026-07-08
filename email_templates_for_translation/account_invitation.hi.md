---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
आपका खाता बनाएं {{ site_name }} पर

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          आपका आमंत्रण है!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ site_name }} पर अपना खाता बनाएं
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text>
          हमने देखा कि आप हमारे साथ एक अतिथि के रूप में खरीदारी कर रहे हैं। अपना पूरा खाता बनाएं ताकि आप ऑर्डर ट्रैकिंग, त्वरित चेकआउट और विशेष ऑफर जैसे लाभों का आनंद ले सकें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          आपका खरीदारी इतिहास
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          कुल ऑर्डर: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          कुल खर्च: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          खाता बनाने के क्या लाभ हैं?
        </mj-text>
        <mj-text font-size="14px">
          - अपने ऑर्डर को ट्रैक करें और ऑर्डर इतिहास देखें
        </mj-text>
        <mj-text font-size="14px">
          - बचे हुए विवरण के साथ त्वरित चेकआउट
        </mj-text>
        <mj-text font-size="14px">
          - अपने पते और पसंदों का प्रबंधन करें
        </mj-text>
        <mj-text font-size="14px">
          - विशेष ऑफर और प्रोमोशन के लिए पहुंच
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          यह लिंक आपके खाते के लिए एक पासवर्ड सेट करने की अनुमति देगा। आपका वर्तमान ऑर्डर इतिहास संरक्षित रहेगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
आपका खाता बनाएं!

हेलो {{ customer_name }},

हमने देखा कि आप हमारे साथ एक अतिथि के रूप में खरीदारी कर रहे हैं। अपना पूरा खाता बनाएं ताकि आप ऑर्डर ट्रैकिंग, त्वरित चेकआउट और विशेष ऑफर जैसे लाभों का आनंद ले सकें।

आपका खरीदारी इतिहास:
- कुल ऑर्डर: {{ total_orders }}
- कुल खर्च: {{ total_spent }}

खाता बनाने के क्या लाभ हैं?
- अपने ऑर्डर को ट्रैक करें और ऑर्डर इतिहास देखें
- बचे हुए विवरण के साथ त्वरित चेकआउट
- अपने पते और पसंदों का प्रबंधन करें
- विशेष ऑफर और प्रोमोशन के लिए पहुंच

खाता बनाएं: {{ activation_url }}

यह लिंक आपके खाते के लिए एक पासवर्ड सेट करने की अनुमति देगा। आपका वर्तमान ऑर्डर इतिहास संरक्षित रहेगा।

सहायता की आवश्यकता है? {{ support_email }} पर संपर्क करें