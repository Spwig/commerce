---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
आपका डिजिटल प्रोडक्ट तैयार है - ऑर्डर #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          आपका डिजिटल प्रोडक्ट तैयार है!
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
          आपकी खरीदारी के लिए धन्यवाद! आपका डिजिटल प्रोडक्ट अब डाउनलोड के लिए तैयार है।
        </mj-text>
        <mj-text font-weight="bold">
          ऑर्डर #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          संस्करण: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          फ़ाइल का आकार: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          अब डाउनलोड करें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>महत्वपूर्ण जानकारी:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • आप इस प्रोडक्ट को {{ download_limit }} बार डाउनलोड कर सकते हैं
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • डाउनलोड लिंक {{ expiration_days }} दिनों में खत्म हो जाएगा
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • भविष्य में संदर्भ के लिए इस ईमेल को बचाए रखें
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          सहायता की आवश्यकता है? हमारी समर्थन टीम से संपर्क करें: {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपका डिजिटल प्रोडक्ट तैयार है!

हेलो {{ customer_name }},

आपकी खरीदारी के लिए धन्यवाद! आपका डिजिटल प्रोडक्ट अब डाउनलोड के लिए तैयार है।

ऑर्डर #{{ order_number }}

प्रोडक्ट: {{ product_name }}
संस्करण: {{ product_version }}
फ़ाइल का आकार: {{ file_size }}

अपना प्रोडक्ट यहां डाउनलोड करें:
{{ download_url }}

महत्वपूर्ण जानकारी:
{% if download_limit %}• आप इस प्रोडक्ट को {{ download_limit }} बार डाउनलोड कर सकते हैं
{% endif %}{% if expiration_days %}• डाउनलोड लिंक {{ expiration_days }} दिनों में खत्म हो जाएगा
{% endif %}• भविष्य में संदर्भ के लिए इस ईमेल को बचाए रखें

सहायता की आवश्यकता है? हमारी समर्थन टीम से संपर्क करें: {{ support_email }}