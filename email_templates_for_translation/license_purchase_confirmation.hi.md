---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
आपका Spwig लाइसेंस - आर्डर #{{ order_number }}

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
          आपकी खरीदारी के लिए धन्यवाद!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          आर्डर #{{ order_number }}
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
          आपकी {{ product_name }} की खरीदारी पूर्ण हो गई है। नीचे आपके लाइसेंस की जांच करें और शुरुआत करने के लिए सेटअप टोकन देखें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          आर्डर समारोह
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          उत्पाद: {{ product_name }}{% if includes_pos %} (POS शामिल है){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          राशि: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          आर्डर संख्या: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          आपका लाइसेंस की जांच
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          इस की जांच करें - आपके लिए फिर से इस्तेमाल के लिए आवश्यक होगा
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          आपका सेटअप टोकन
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          सेटअप के दौरान इस टोकन का उपयोग करें ताकि आपका स्टोर सक्रिय हो जाए
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          शुरुआत करें
        </mj-text>
        <mj-text font-size="14px">
          1. हमारे सेटअप गाइड के अनुसार Spwig को अपने सर्वर पर इंस्टॉल करें
        </mj-text>
        <mj-text font-size="14px">
          2. सेटअप के दौरान आपके सेटअप टोकन को दर्ज करें
        </mj-text>
        <mj-text font-size="14px">
          3. आपका स्टोर स्वचालित रूप से सक्रिय हो जाएगा
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          अपना खाता बनाएं
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          अपने लाइसेंस को प्रबंधित करने, डाउनलोड के अभिगमन और अपडेट प्राप्त करने के लिए एक पासवर्ड सेट करें।
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          महत्वपूर्ण:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          इस ईमेल को सुरक्षित रखें - यह आपके लाइसेंस की जांच और सेटअप टोकन के भविष्य के संदर्भ के लिए है। अन्य के साथ इन योग्यताओं को साझा न करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
आपकी खरीदारी के लिए धन्यवाद!

आर्डर #{{ order_number }}

हेलो {{ customer_name }},

आपकी {{ product_name }} की खरीदारी पूर्ण हो गई है। नीचे आपके लाइसेंस की जांच करें और शुरुआत करने के लिए सेटअप टोकन देखें।

आर्डर समारोह:
- उत्पाद: {{ product_name }}{% if includes_pos %} (POS शामिल है){% endif %}
- राशि: {{ price }}
- आर्डर संख्या: {{ order_number }}

आपका लाइसेंस की जांच:
{{ license_key }}
इस की जांच करें - आपके लिए फिर से इस्तेमाल के लिए आवश्यक होगा।

आपका सेटअप टोकन:
{{ setup_token }}
सेटअप के दौरान इस टोकन का उपयोग करें ताकि आपका स्टोर सक्रिय हो जाए।

शुरुआत करें:
1. हमारे सेटअप गाइड के अनुसार Spwig को अपने सर्वर पर इंस्टॉल करें
2. सेटअप के दौरान आपके सेटअप टोकन को दर्ज करें
3. आपका स्टोर स्वचालित रूप से सक्रिय हो जाएगा

सेटअप गाइड देखें: {{ setup_url }}
{% if activation_url %}
अपना खाता बनाएं:
एक पासवर्ड सेट करें ताकि आपके लाइसेंस को प्रबंधित कर सकें, डाउनलोड के अभिगमन और अपडेट प्राप्त कर सकें।
{{ activation_url }}
{% endif %}
महत्वपूर्ण:
इस ईमेल को सुरक्षित रखें - यह आपके लाइसेंस की जांच और सेटअप टोकन के भविष्य के संदर्भ के लिए है। अन्य के साथ इन योग्यताओं को साझा न करें।

सहायता की आवश्यकता है? {{ support_email }} से संपर्क करें