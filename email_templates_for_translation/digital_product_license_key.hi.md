---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
आपका सॉफ्टवेयर लाइसेंस की चाबी - आदेश #{{ order_number }}

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
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          आपकी लाइसेंस की चाबी तैयार है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text>
          {{ product_name }} के आपके खरीदारी के लिए धन्यवाद! यहां आपकी एक्टिवेशन के लिए लाइसेंस की चाबी है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          आपकी लाइसेंस की चाबी
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          कॉपी करने के लिए क्लिक करें या ध्यान से लिखें
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          लाइसेंस विवरण:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • उत्पाद: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • संस्करण: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • लाइसेंस प्रकार: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • अधिकतम एक्टिवेशन: {{ max_activations }} उपकरण(स)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • वैधता: लाइफटाइम लाइसेंस
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • वैध तक: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          एक्टिवेशन कैसे करें:
        </mj-text>
        <mj-text font-size="14px">
          1. सॉफ्टवेयर डाउनलोड और इंस्टॉल करें
        </mj-text>
        <mj-text font-size="14px">
          2. एप्लिकेशन खोलें
        </mj-text>
        <mj-text font-size="14px">
          3. जब आपको लाइसेंस की चाबी दरख्वास्त की जाए तो इसे दर्ज करें
        </mj-text>
        <mj-text font-size="14px">
          4. प्रक्रिया को पूरा करने के लिए "एक्टिवेट" पर क्लिक करें
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          सॉफ्टवेयर डाउनलोड करें
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ महत्वपूर्ण:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • इस ईमेल को सुरक्षित रखें - आपको पुनः इंस्टॉल करने के लिए लाइसेंस की चाबी की आवश्यकता होगी
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • अपनी लाइसेंस की चाबी को अन्य लोगों के साथ शेयर न करें
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • आप अपने खाता डैशबोर्ड से उपकरणों को डिएक्टिवेट कर सकते हैं
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          एक्टिवेशन में मदद की आवश्यकता है? {{ support_email }} से संपर्क करें
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपकी लाइसेंस की चाबी तैयार है

हेलो {{ customer_name }},

{{ product_name }} के आपके खरीदारी के लिए धन्यवाद! यहां आपकी एक्टिवेशन के लिए लाइसेंस की चाबी है।

आपकी लाइसेंस की चाबी:
{{ license_key }}

लाइसेंस विवरण:
• उत्पाद: {{ product_name }}
• संस्करण: {{ product_version }}
• लाइसेंस प्रकार: {{ license_type }}
• अधिकतम एक्टिवेशन: {{ max_activations }} उपकरण(स)
{% if is_lifetime %}• वैधता: लाइफटाइम लाइसेंस{% else %}• वैध तक: {{ expiration_date }}{% endif %}

एक्टिवेशन कैसे करें:
1. सॉफ्टवेयर डाउनलोड और इंस्टॉल करें
2. एप्लिकेशन खोलें
3. जब आपको लाइसेंस की चाबी दरख्वास्त की जाए तो इसे दर्ज करें
4. प्रक्रिया को पूरा करने के लिए "एक्टिवेट" पर क्लिक करें

{% if download_url %}सॉफ्टवेयर डाउनलोड करें: {{ download_url }}

{% endif %}महत्वपूर्ण:
• इस ईमेल को सुरक्षित रखें - आपको पुनः इंस्टॉल करने के लिए लाइसेंस की चाबी की आवश्यकता होगी
• अपनी लाइसेंस की चाबी को अन्य लोगों के साथ शेयर न करें
• आप अपने खाता डैशबोर्ड से उपकरणों को डिएक्टिवेट कर सकते हैं

एक्टिवेशन में मदद की आवश्यकता है? {{ support_email }} से संपर्क करें